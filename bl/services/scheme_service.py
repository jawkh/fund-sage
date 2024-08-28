# Copyright (c) 2024 by Jonathan AW
from typing import List, Optional, Type
from dal.crud_operations import CRUDOperations
from dal.models import Scheme, Applicant
from bl.schemes.base_eligibility import BaseEligibility
from bl.factories.scheme_eligibility_checker_factory import BaseSchemeEligibilityCheckerFactory
from bl.schemes.scheme_eligibilty_checker import SchemeEligibilityChecker
class SchemeService:
    """
    Service class to handle all business logic related to financial assistance schemes.
    """

    def __init__(self, crud_operations: CRUDOperations, eligibility_strategy: Optional[BaseEligibility] = None):
        self.crud_operations = crud_operations
        self.eligibility_strategy = eligibility_strategy or BaseEligibility()

    def get_scheme_by_id(self, scheme_id: int, ) -> Scheme:
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

    def get_all_schemes(self, fetch_valid_schemes: bool, schemeFactory: Optional[BaseSchemeEligibilityCheckerFactory] = None) -> List[SchemeEligibilityChecker]:
        """
        Args:
            fetch_valid_schemes (bool): _description_
            schemeFactory (Optional[BaseSchemeFactory], optional): _description_. Defaults to None. Required for checking scheme eligibility.

        Returns:
            List[SchemeEligibilityChecker]: _description_
        """
        return self.crud_operations.get_schemes_by_filters({}, fetch_valid_schemes, schemeFactory)

    def get_schemes_by_filters(self, filters: dict, fetch_valid_schemes: bool, schemeFactory: Optional[BaseSchemeEligibilityCheckerFactory] = None) -> List[SchemeEligibilityChecker]:
        """_summary_

        Args:
            filters (dict): _description_
            fetch_valid_schemes (bool): _description_
            schemeFactory (Optional[BaseSchemeFactory], optional): _description_. Defaults to None. Required for checking scheme eligibility.

        Returns:
            List[SchemeEligibilityChecker]: _description_
        """
        schemes_data = self.crud_operations.get_schemes_by_filters(filters, fetch_valid_schemes)
        return [schemeFactory.load_scheme_eligibility_checker(scheme_data, self.crud_operations) for scheme_data in schemes_data] 
