# Copyright (c) 2024 by Jonathan AW
# applicant_service.py
# This file contains the ApplicantService class that handles the business logic related to applicants and household members. 
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

8. Flexibility and Extensibility:
- The ApplicantService class can easily accommodate new features or changes related to applicants and household members, allowing for future scalability and maintenance.
"""

from typing import List, Tuple
from dal.crud_operations import CRUDOperations
from sqlalchemy.orm import Session
from dal.models import Applicant, HouseholdMember
from exceptions import ApplicantNotFoundException, InvalidApplicantDataException, HouseholdMemberNotFoundException, InvalidHouseholdMemberDataException, InvalidPaginationParameterException, InvalidSortingParameterException
from typing import List, Optional, Dict
from bl.services.scheme_service import SchemeService
from utils.data_validation import validate_applicant_data, validate_household_member_data
from sqlalchemy import asc, desc

class ApplicantService:
    """
    Service class to handle all business logic related to applicants.
    """

    def __init__(self, crud_operations: CRUDOperations):
        self.crud_operations = crud_operations

    def get_all_applicants(self, 
                        page: int = 1, 
                        page_size: int = 100, 
                        sort_by: Optional[str] = 'name', 
                        sort_order: Optional[str] = 'asc', 
                        filters: Optional[Dict[str, any]] = None) -> Tuple[List[Applicant], int]:
        """
        Retrieve all applicants with pagination, sorting, and filtering options.

        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of applicants to retrieve per page.
            sort_by (Optional[str]): The field to sort by ('name' or 'created_at').
            sort_order (Optional[str]): The sort order ('asc' or 'desc').
            filters (Optional[Dict[str, any]]): A dictionary of filters to apply to the query.

        Returns:
            Tuple[List[Applicant], int]: A tuple containing a list of applicants for the specified page and the total count of applicants.
        """
        return self.crud_operations.get_all_applicants(page, page_size, sort_by, sort_order, filters)

    def get_applicant_by_id(self, applicant_id: int) -> Applicant:
        """
        Retrieve an applicant by ID.
        """
        applicant = self.crud_operations.get_applicant(applicant_id)
        if not applicant:
            raise ApplicantNotFoundException(f"Applicant with ID {applicant_id} not found.")
        return applicant



    def create_applicant(self, applicant_data: dict, household_members_data: Optional[List[dict]] = []) -> Applicant:
        """
        Create an applicant and their household members.

        Args:
            applicant_data (dict): Data for creating the applicant.
            household_members_data (List[dict]]): List of data for creating household members.

        Returns:
            Applicant: The created applicant with household members.
        """
        # Phase 1: Validate all data
        isApplicantDataValid, msg = validate_applicant_data(applicant_data, for_create_mode=True)
        if not isApplicantDataValid:
            raise InvalidApplicantDataException(msg)

        # Validate household member data
        for member_data in household_members_data:
            isHouseholdMemberDataValid, msg_member = validate_household_member_data(member_data, for_create_mode=True)
            if not isHouseholdMemberDataValid:
                raise InvalidHouseholdMemberDataException(msg_member)

        # Count parents to ensure a maximum of two
        parents_count = sum(1 for member in household_members_data if member.get('relation') == 'parent')
        if parents_count > 2:
            raise InvalidHouseholdMemberDataException("An applicant cannot have more than two parents.")

        # Phase 2: Delegate to CRUDOperations for record creation
        try:
            # Use the enhanced CRUDOperations method to create the applicant and household members
            applicant = self.crud_operations.create_applicant(applicant_data, household_members_data)
        except Exception as e:
            # Log the exception or handle it as needed
            raise e

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
        


