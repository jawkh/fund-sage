# Copyright (c) 2024 by Jonathan AW

from typing import List
from dal.crud_operations import CRUDOperations
from dal.models import Scheme

class SchemeService:
    """
    Service class to handle all business logic related to financial assistance schemes.
    """

    def __init__(self, crud_operations: CRUDOperations):
        self.crud_operations = crud_operations

    def get_scheme_by_id(self, scheme_id: int) -> Scheme:
        """
        Retrieve a scheme by ID.
        """
        scheme = self.crud_operations.get_scheme(scheme_id)
        if not scheme:
            raise ValueError(f"Scheme with ID {scheme_id} not found.")
        return scheme

    def create_scheme(self, scheme_data: dict) -> Scheme:
        """
        Create a new scheme.
        """
        return self.crud_operations.create_scheme(scheme_data)

    def update_scheme(self, scheme_id: int, update_data: dict) -> Scheme:
        """
        Update a scheme's details.
        """
        return self.crud_operations.update_scheme(scheme_id, update_data)

    def delete_scheme(self, scheme_id: int) -> None:
        """
        Delete a scheme record.
        """
        self.crud_operations.delete_scheme(scheme_id)

    def get_all_schemes(self, fetch_valid_schemes: bool = True) -> List[Scheme]:
        """
        Retrieve all available schemes.
        """
        return self.crud_operations.get_schemes_by_filters({}, fetch_valid_schemes)

    def get_schemes_by_filters(self, filters: dict, fetch_valid_schemes: bool = True) -> List[Scheme]:
        """
        Retrieve schemes based on filters.
        """
        return self.crud_operations.get_schemes_by_filters(filters, fetch_valid_schemes)
    