# Copyright (c) 2024 by Jonathan AW
# scheme_service.py
# This file contains the SchemeService class that handles the business logic related to financial assistance schemes.

from typing import List, Optional, Type, Dict
from dal.crud_operations import CRUDOperations
from dal.models import Scheme
from exceptions import SchemeNotFoundException, InvalidSchemeDataException  
from utils.data_validation import validate_scheme_data
from typing import List, Tuple
""" 
Summary: The SchemeService class is responsible for handling all business logic related to financial assistance schemes, including CRUD operations and potentially complex logic involving scheme eligibility

Design Patterns:
1. Clear Separation of Concerns:
- Each method in the class has a clear and specific responsibility, following the Single Responsibility Principle (SRP).

2. Data Validation:
- The use of validate_scheme_data for validating scheme data before creating or updating a scheme ensures data integrity and consistency.

3. Error Handling:
- Custom exceptions (SchemeNotFoundException, InvalidSchemeDataException) are used to handle specific error scenarios related to schemes, providing clear and meaningful feedback.

4. Dependency Injection:
- The class takes a CRUDOperations object as a dependency, allowing for better testability and separation of concerns.

5. Use of Type Annotations:
- The use of type annotations for method arguments and return types enhances code readability and maintainability.

"""
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
            raise SchemeNotFoundException(f"Scheme with ID {scheme_id} not found.")
        return scheme

    def create_scheme(self, scheme_data: dict) -> Scheme:
        """
        Create a new scheme.
        """
        isvalid , msg = validate_scheme_data(scheme_data, True)
        if not isvalid:
            raise InvalidSchemeDataException(msg)
        scheme = self.crud_operations.create_scheme(scheme_data)
        return scheme

    def update_scheme(self, scheme_id: int, update_data: dict) -> Scheme:
        """
        Update a scheme's details.
        """
        if not self.get_scheme_by_id(scheme_id):
            raise SchemeNotFoundException(f"Scheme with ID {scheme_id} not found.")
        isvalid , msg = validate_scheme_data(update_data, False)
        if not isvalid:
            raise InvalidSchemeDataException(msg)
        scheme = self.crud_operations.update_scheme(scheme_id, update_data)
        return scheme

    def delete_scheme(self, scheme_id: int) -> None:
        """
        Delete a scheme record.
        """
        if not self.get_scheme_by_id(scheme_id):
            raise SchemeNotFoundException(f"Scheme with ID {scheme_id} not found.")
        self.crud_operations.delete_scheme(scheme_id)

    def get_all_schemes(self, fetch_valid_schemes: bool=True) -> List[Scheme]:
        """
        Retrieve all schemes, optionally filtering for valid schemes based on current date.
        """
        schemes, rec_count = self.crud_operations.get_schemes_by_filters({}, fetch_valid_schemes)
        return schemes
    
    def get_schemes_by_filters(
        self, 
        filters: dict = {}, 
        fetch_valid_schemes: bool = True, 
        page: int = 1, 
        per_page: int = 10
    ) -> Tuple[List[Scheme], int]:
        """
        Retrieve schemes with optional filters and pagination.

        Args:
            filters (dict): Filters to apply to the query.
            fetch_valid_schemes (bool): Flag to determine whether to fetch only valid schemes.
            page (int): The page number for pagination.
            per_page (int): The number of items per page for pagination.

        Returns:
            Tuple[List[Scheme], int]: A list of schemes and total count of schemes.
        """
        return self.crud_operations.get_schemes_by_filters(
            filters=filters,
            fetch_valid_schemes=fetch_valid_schemes,
            page=page,
            per_page=per_page
        )

