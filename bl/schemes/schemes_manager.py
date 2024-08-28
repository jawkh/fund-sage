
# Copyright (c) 2024 by Jonathan AW

from typing import List, Dict
from dal.models import Scheme, Applicant
from bl.schemes.base_eligibility import BaseEligibility
from dal.crud_operations import CRUDOperations
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.factories.base_scheme_eligibility_checker_factory import BaseSchemeEligibilityCheckerFactory

class SchemesManager:
    """
    Class to manage different eligibility strategies for various schemes.
    """

    def __init__(self, crud_operations: CRUDOperations, schemeFactory: BaseSchemeEligibilityCheckerFactory):
        self.crud_operations = crud_operations
        self.schemeFactory = schemeFactory

    def check_schemes_eligibility_for_applicant(self, schemes_filters: dict, fetch_valid_schemes: bool, applicant: Applicant) -> List[Dict[str, any]]:
        """
        Check which schemes an applicant is eligible for using various eligibility strategies.
        """
        schemes = self.crud_operations.get_schemes_by_filters(schemes_filters, fetch_valid_schemes, self.schemeFactory)
        eligibility_results = []

        for scheme_data in schemes:
            scheme = SchemeEligibilityCheckerFactory.load_scheme_eligibility_checker(scheme_data, self.crud_operations)
            is_eligible = scheme.eligibility_strategy.check_eligibility(applicant)
            eligible_benefits = scheme.eligibility_strategy.calculate_benefits(applicant) if is_eligible else {}
            eligibility_results.append({
                "scheme_name": scheme.name,
                "scheme_description": scheme.description,
                "scheme_start_date": scheme.validity_start_date,
                "scheme_end_date": scheme.validity_end_date,
                "eligibility": is_eligible,
                "eligible_benefits": eligible_benefits
            })

        return eligibility_results
