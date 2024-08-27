# Copyright (c) 2024 by Jonathan AW

from typing import List
from dal.crud_operations import CRUDOperations
from dal.models import Application, Scheme
from exceptions import ApplicantNotFoundException

class ApplicationService:
    """
    Service class to handle all business logic related to applications.
    """

    def __init__(self, crud_operations: CRUDOperations):
        self.crud_operations = crud_operations

    def get_application_by_id(self, application_id: int) -> Application:
        """
        Retrieve an application by ID.
        """
        application = self.crud_operations.get_application(application_id)
        if not application:
            raise ApplicationNotFoundException(f"Application with ID {application_id} not found.")
        return application

    def create_application(self, applicant_id: int, scheme_id: int, created_by_admin_id: int) -> Application:
        """
        Create a new application for a given applicant and scheme.
        """
        applicant = self.crud_operations.get_applicant(applicant_id)
        if not applicant:
            raise ApplicantNotFoundException(f"Applicant with ID {applicant_id} not found.")

        scheme = self.crud_operations.get_scheme(scheme_id)
        if not scheme:
            raise SchemeNotFoundException(f"Scheme with ID {scheme_id} not found.")

        # Additional business logic for application creation can be added here
        application_data = {
            "applicant_id": applicant_id,
            "scheme_id": scheme_id,
            "status": "pending",
            "created_by_admin_id": created_by_admin_id
        }
        return self.crud_operations.create_application(application_data)

    def update_application(self, application_id: int, update_data: dict) -> Application:
        """
        Update an application's details.
        """
        return self.crud_operations.update_application(application_id, update_data)

    def delete_application(self, application_id: int) -> None:
        """
        Delete an application record.
        """
        self.crud_operations.delete_application(application_id)

    def check_applicant_eligibility(self, applicant_id: int) -> List[Scheme]:
        """
        Delegate to ApplicantService to check the schemes for which the applicant is eligible.
        """
        return self.applicant_service.check_eligibility(applicant_id)
