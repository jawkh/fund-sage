# Copyright (c) 2024 by Jonathan AW
# applicant_service.py

"""
Summary: The ApplicantService class is focused on handling the business logic related to applicants and householdmembers.

Design Patterns:

1. Clear Separation of Concerns:
- The class is focused on handling applicant and household member-related operations, adhering to the Single Responsibility Principle (SRP).

2. Error Handling:
- Custom exceptions (ApplicantNotFoundException, InvalidApplicantDataException, HouseholdMemberNotFoundException, InvalidHouseholdMemberDataException) are used to handle specific error scenarios related to applicants and household members, providing clear and meaningful feedback.

3. Data Validation:
- The use of validate_applicant_data and validate_household_member_data for validating applicant and household member data ensures data integrity and consistency.

4. Dependency Injection:
- The class takes a CRUDOperations object as a dependency, allowing for better testability and separation of concerns.

5. Use of Type Annotations:
- The use of type annotations for method arguments and return types enhances code readability and maintainability.

6. Encapsulation:
- The class encapsulates the logic for managing applicants and household members, providing a clean interface for interacting with applicant and household member data.

7. Readability and Maintainability:
- The class structure and method names are well-organized, making the code easy to understand and maintain.


"""

from typing import List
from dal.crud_operations import CRUDOperations
from dal.models import Applicant, HouseholdMember
from exceptions import ApplicantNotFoundException, InvalidApplicantDataException, HouseholdMemberNotFoundException, InvalidHouseholdMemberDataException
from typing import List, Optional, Dict
from bl.services.scheme_service import SchemeService
from utils.data_validation import validate_applicant_data, validate_household_member_data

class ApplicantService:
    """
    Service class to handle all business logic related to applicants.
    """

    def __init__(self, crud_operations: CRUDOperations):
        self.crud_operations = crud_operations

    def get_applicant_by_id(self, applicant_id: int) -> Applicant:
        """
        Retrieve an applicant by ID.
        """
        applicant = self.crud_operations.get_applicant(applicant_id)
        if not applicant:
            raise ApplicantNotFoundException(f"Applicant with ID {applicant_id} not found.")
        return applicant

    def create_applicant(self, applicant_data: dict) -> Applicant:
        isvalid , msg = validate_applicant_data(applicant_data, True)
        
        if not isvalid:
            raise InvalidApplicantDataException(msg)
        applicant = self.crud_operations.create_applicant(applicant_data)
        return applicant

    def update_applicant(self, applicant_id: int, update_data: dict) -> Applicant:
        """
        Update an applicant's details.
        """
        isvalid , msg = validate_applicant_data(update_data, False)
        
        if not isvalid:
            raise InvalidApplicantDataException(msg)
        
        if not self.get_applicant_by_id(applicant_id):
            raise ApplicantNotFoundException(f"Applicant with ID {applicant_id} not found.")
        
        applicant = self.crud_operations.update_applicant(applicant_id, update_data)
        return applicant

    def delete_applicant(self, applicant_id: int) -> None:
        """
        Delete an applicant record.
        """
        # checks if the applicant exists before deleting
        if not self.get_applicant_by_id(applicant_id):
            raise ApplicantNotFoundException(f"Applicant with ID {applicant_id} not found.")
        self.crud_operations.delete_applicant(applicant_id)
        
    # New CRUD Operations for HouseholdMember

    def create_household_member(self, applicant_id: int, member_data: dict) -> HouseholdMember:
        """
        Create a new household member associated with an applicant.
        """
        
        applicant = self.get_applicant_by_id(applicant_id)  # Ensure applicant exists
        member_data["applicant_id"] = applicant_id  # Set the foreign key to link to the applicant
        isvalid , msg = validate_household_member_data(member_data, True)
        if not isvalid:
            raise InvalidHouseholdMemberDataException(msg)
        return self.crud_operations.create_household_member(member_data)

    def get_household_member_by_id(self, member_id: int) -> HouseholdMember:
        """
        Retrieve a household member by ID.
        """
        member = self.crud_operations.get_household_member(member_id)
        if not member:
            raise HouseholdMemberNotFoundException(f"Household Member with ID {member_id} not found.")
        return member

    def update_household_member(self, member_id: int, update_data: dict) -> HouseholdMember:
        """
        Update a household member's details.
        """
        isvalid , msg = validate_household_member_data(update_data, False)
        if not isvalid:
            raise InvalidHouseholdMemberDataException(msg)
        
        member = self.crud_operations.get_household_member(member_id)
        if not member:
            raise HouseholdMemberNotFoundException(f"Household Member with ID {member_id} not found.")
        return self.crud_operations.update_household_member(member_id, update_data)

    def delete_household_member(self, member_id: int) -> None:
        """
        Delete a household member record.
        """
        member = self.crud_operations.get_household_member(member_id)
        if not member:
            raise HouseholdMemberNotFoundException(f"Household Member with ID {member_id} not found.")
        self.crud_operations.delete_household_member(member_id)
        


