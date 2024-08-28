# Copyright (c) 2024 by Jonathan AW

from typing import List
from dal.crud_operations import CRUDOperations
from dal.models import Applicant
from exceptions import ApplicantNotFoundException
from typing import List, Optional, Dict
from bl.services.scheme_service import SchemeService

class ApplicantService:
    """
    Service class to handle all business logic related to applicants.
    """

    def __init__(self, crud_operations: CRUDOperations, scheme_service: Optional[SchemeService] = None):
        '''
        Initialize the ApplicantService with CRUDOperations and an optional SchemeService.
        scheme_service is required in order to compute schemes' eligibility for applicants.
        '''
        self.crud_operations = crud_operations
        self.scheme_service = scheme_service or SchemeService(crud_operations)

    def get_applicant_by_id(self, applicant_id: int) -> Applicant:
        """
        Retrieve an applicant by ID.
        """
        applicant = self.crud_operations.get_applicant(applicant_id)
        if not applicant:
            raise ApplicantNotFoundException(f"Applicant with ID {applicant_id} not found.")
        return applicant

    def create_applicant(self, applicant_data: dict) -> Applicant:
        """
        Create a new applicant record.
        """
        return self.crud_operations.create_applicant(applicant_data)

    def update_applicant(self, applicant_id: int, update_data: dict) -> Applicant:
        """
        Update an applicant's details.
        """
        return self.crud_operations.update_applicant(applicant_id, update_data)

    def delete_applicant(self, applicant_id: int) -> None:
        """
        Delete an applicant record.
        """
        self.crud_operations.delete_applicant(applicant_id)


