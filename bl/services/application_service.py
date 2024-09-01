# Copyright (c) 2024 by Jonathan AW
# This file contains the ApplicationService class that handles the business logic related to applications, specifically handling CRUD operations for applications.
""" 
Summary: The ApplicationService class is responsible for managing the business logic related to applications, specifically handling CRUD operations for applications.

Design Patterns:

1. Clear and Focused Methods:
- The class has well-defined methods for each CRUD operation, adhering to the Single Responsibility Principle (SRP).

2. Error Handling:
- The use of custom exceptions (ApplicationNotFoundException, ApplicantNotFoundException, SchemeNotFoundException) is good practice for maintaining clear and specific error handling.

3. Logical Sequence:
- The create_application method checks for the existence of an applicant and scheme before proceeding with the creation, ensuring that all necessary conditions are met before an application is created. It auto-determines the application status based on eligiblity checks on the applicant.

4. data_validation:
- The use of validate_application_data for validating application data before creating or updating an application ensures data integrity and consistency.

5. Dependency Injection:
- The class takes a CRUDOperations object as a dependency, allowing for better testability and separation of concerns.

6. Use of Factories:
- The class uses the BaseSchemeEligibilityCheckerFactory to instantiate the SchemesManager, which allows for flexibility in determining the eligibility of applicants for different schemes.

7. Use of type annotations:
- The use of type annotations for method arguments and return types enhances code readability and maintainability.

8. Encapsulation:
- The class encapsulates the logic for managing applications, providing a clean interface for interacting with application data.
"""
# application_service.py

from typing import List, Tuple, Optional
from dal.crud_operations import CRUDOperations
from dal.models import Application, Scheme
from exceptions import ApplicationNotFoundException, ApplicantNotFoundException, SchemeNotFoundException, InvalidApplicationDataException, AdministratorNotFoundException, InvalidPaginationParameterException, InvalidSortingParameterException
from bl.factories.base_scheme_eligibility_checker_factory import BaseSchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager
from utils.data_validation import validate_application_data
from sqlalchemy import asc, desc
class ApplicationService:
    """
    Service class to handle all business logic related to applications.
    """

    def __init__(self, crud_operations: CRUDOperations):
        self.crud_operations = crud_operations


    def get_all_applications(self, 
                            page: int = 1, 
                            page_size: int = 100, 
                            sort_by: Optional[str] = 'created_at', 
                            sort_order: Optional[str] = 'asc') -> Tuple[List[Application], int]:

        return self.crud_operations.get_all_applications(page, page_size, sort_by, sort_order)

    def get_application_by_id(self, application_id: int) -> Application:
        """
        Retrieve an application by ID.
        """
        application = self.crud_operations.get_application(application_id)
        if not application:
            raise ApplicationNotFoundException(f"Application with ID {application_id} not found.")
        return application

    def create_application(self, applicant_id: int, scheme_id: int, created_by_admin_id: int, schemeEligibilityCheckerFactory: BaseSchemeEligibilityCheckerFactory) -> Application:
        """
        Create a new application for a given applicant and scheme.
        
        Logical Flow for Creating an Application:
        1. Retrieve Applicant and Scheme:
        - The function starts by retrieving the applicant and scheme using the provided IDs. If either is not found, a corresponding exception is raised. This is a good practice to ensure that all prerequisites are met before proceeding with further logic.
        
        2. Pre-Eligibility Check:
        - The function checks if an approved application already exists for the applicant and scheme. If such an application is found, it raises an exception to prevent duplicate applications for the same scheme.
        
        3. Eligibility Check:
        - The SchemesManager is instantiated with the crud_operations and schemeEligibilityCheckerFactory to check the applicant's eligibility for the scheme.
        - The eligibility_results dictionary contains a boolean flag, "is_eligible", which is used to set the application status ("approved" if eligible, "rejected" if not). This ensures that the application status reflects the eligibility result.
        
        4. Application Creation:
        - An application_data dictionary is constructed with the appropriate values, including the determined status.
        - The application is created using the crud_operations.create_application method, which is a standard way to interact with the database.
        """
        
        applicant = self.crud_operations.get_applicant(applicant_id)
        if not applicant:
            raise ApplicantNotFoundException(f"Applicant with ID {applicant_id} not found.")

        scheme = self.crud_operations.get_scheme(scheme_id)
        if not scheme:
            raise SchemeNotFoundException(f"Scheme with ID {scheme_id} not found.")
        
        admin = self.crud_operations.get_administrator(created_by_admin_id)
        if not admin:
            raise AdministratorNotFoundException(f"Administrator with ID {created_by_admin_id} not found.")

        # Check if an approved application already exists for this applicant and scheme
        # If an approved application exists, prevent duplicate applications
        # This is to ensure that an applicant does not **successfully** apply multiple times for the same scheme
        # If the applicant has a rejected or pending application, they can apply again
        existing_application = self.crud_operations.get_approved_application_by_applicant_and_scheme(applicant_id, scheme_id)
        if existing_application and existing_application.status == "approved":
            raise InvalidApplicationDataException(f"Applicant {applicant_id} has already successfully applied to scheme {scheme_id}.")


        # Checks that the Applicant is eligible for the Scheme to determine the status of the application
        scheme_manager = SchemesManager(self.crud_operations, schemeEligibilityCheckerFactory)
        eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(scheme, applicant)
        status = "pending"
        
        status = "approved" if eligibility_results.is_eligible else "rejected"
        
        application_data = {
            "applicant_id": applicant_id,
            "scheme_id": scheme_id,
            "status": status,
            "eligibility_verdict": eligibility_results.eligibility_message, 
            "awarded_benefits": eligibility_results.eligible_benefits,  
            "created_by_admin_id": created_by_admin_id
        }
        isvalid , msg = validate_application_data(application_data, True)
        if not isvalid:
            raise InvalidApplicationDataException(msg)
        
        return self.crud_operations.create_application(application_data)

    
    def update_application(self, application_id: int, update_data: dict, schemeEligibilityCheckerFactory: BaseSchemeEligibilityCheckerFactory) -> Application:
        """
        Update an application's details and re-evaluate eligibility if necessary.
        
        Logical Flow for Updating an Application:
        
        1. Fetch Existing Application:
        - Retrieve the application to ensure it exists and get the current data for eligibility evaluation.
        
        2. Check for Relevant Updates:
        - Determine if the update involves fields that affect eligibility (e.g., changes in applicant information or scheme details).
        
        3. Re-Evaluate Eligibility:
        - If relevant updates are made, re-check eligibility using the SchemesManager and update the application status accordingly.
        
        4. Update Application:
        - Perform the update with the new status if eligibility has changed; otherwise, proceed with a standard update.
        """
        application = self.get_application_by_id(application_id)
        if not application:
            raise ApplicationNotFoundException(f"Application with ID {application_id} not found.")
        
        isvalid , msg = validate_application_data(update_data, False)
        if not isvalid:
            raise InvalidApplicationDataException(msg)
        
        # Determine if eligibility needs to be re-evaluated
        needs_eligibility_check = False
        if "applicant_id" in update_data or "scheme_id" in update_data:
            needs_eligibility_check = True

        if needs_eligibility_check:
            applicant_id = update_data.get("applicant_id", application.applicant_id)
            scheme_id = update_data.get("scheme_id", application.scheme_id)
            
            applicant = self.crud_operations.get_applicant(applicant_id)
            if not applicant:
                raise ApplicantNotFoundException(f"Applicant with ID {applicant_id} not found.")

            scheme = self.crud_operations.get_scheme(scheme_id)
            if not scheme:
                raise SchemeNotFoundException(f"Scheme with ID {scheme_id} not found.")

            # Re-check eligibility
            scheme_manager = SchemesManager(self.crud_operations, schemeEligibilityCheckerFactory)
            eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(scheme, applicant)
            
            # Update the status based on new eligibility results
            update_data["status"] = "approved" if eligibility_results.is_eligible else "rejected"
            update_data["eligibility_verdict"] = eligibility_results.eligibility_message  
            update_data["awarded_benefits"] = eligibility_results.eligible_benefits  
            
        updated_application = self.crud_operations.update_application(application_id, update_data)
        return updated_application


    def delete_application(self, application_id: int) -> None:
        """
        Delete an application record.
        """
        application = self.get_application_by_id(application_id)
        if not application:
            raise ApplicationNotFoundException(f"Application with ID {application_id} not found.")
        self.crud_operations.delete_application(application_id)

