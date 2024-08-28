# Copyright (c) 2024 by Jonathan AW
# applicant_service.py

"""
Summary: The ApplicantService class is focused on handling the business logic related to applicants.

Design Patterns:
1. Clear Separation of Concerns:
- The class is well-organized with each method handling a specific piece of logic related to applicants. This follows the Single Responsibility Principle (SRP).

2. Data Validation:
- The use of a validate_applicant_data function before creating or updating applicants is a good practice. This ensures data integrity and avoids invalid entries in the database.

3. Error Handling:
- The use of a custom exception (ApplicantNotFoundException) when an applicant is not found is a good practice. This helps in maintaining clear and understandable error handling.

"""

from typing import List
from dal.crud_operations import CRUDOperations
from dal.models import Applicant
from exceptions import ApplicantNotFoundException, InvalidApplicantDataException
from typing import List, Optional, Dict
from bl.services.scheme_service import SchemeService
from utils.data_validation import validate_applicant_data

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
        if not validate_applicant_data(applicant_data):
            raise InvalidApplicantDataException("Invalid applicant data provided.")
        applicant = self.crud_operations.create_applicant(applicant_data)
        return applicant

    def update_applicant(self, applicant_id: int, update_data: dict) -> Applicant:
        """
        Update an applicant's details.
        """
        if not validate_applicant_data(update_data):
            raise InvalidApplicantDataException("Invalid applicant data provided.")
        applicant = self.crud_operations.update_applicant(applicant_id, update_data)
        return applicant

    def delete_applicant(self, applicant_id: int) -> None:
        """
        Delete an applicant record.
        """
        self.crud_operations.delete_applicant(applicant_id)


