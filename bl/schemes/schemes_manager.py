
# Copyright (c) 2024 by Jonathan AW
# schemes_manager.py

""" 
Summary: The SchemesManager class acts as a facade to manage different eligibility strategies for various schemes. It manages the eligibility checking process across different schemes for a given applicant. It uses a factory to load the appropriate SchemeEligibilityChecker for each scheme.

Design Pattern: Facade
- The methods 'check_schemes_eligibility_for_applicant' and 'check_scheme_eligibility_for_applicant' effectively handle the eligibility checking process, iterating through schemes and applying the relevant eligibility checks.

"""

from typing import List, Dict, NamedTuple
from dal.models import Scheme, Applicant
from bl.schemes.base_eligibility import BaseEligibility
from dal.crud_operations import CRUDOperations
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.factories.base_scheme_eligibility_checker_factory import BaseSchemeEligibilityCheckerFactory

"""
EligibilityResult NamedTuple is introduced to clearly define the structure of the eligibility check results, improving readability and type safety.
"""
class EligibilityResult(NamedTuple):
    scheme_name: str
    scheme_description: str
    scheme_start_date: str
    scheme_end_date: str
    is_eligible: bool
    eligible_benefits: dict
    
class SchemesManager:
    """
    Class to manage different eligibility strategies for various schemes.
    """

    def __init__(self, crud_operations: CRUDOperations, schemeFactory: BaseSchemeEligibilityCheckerFactory):
        self.crud_operations = crud_operations
        self.schemeFactory = schemeFactory

    def check_schemes_eligibility_for_applicant(self, schemes_filters: dict, fetch_valid_schemes: bool, applicant: Applicant) -> List[EligibilityResult]:
        """
        Check which schemes an applicant is eligible for using various eligibility strategies.
        """
        schemes = self.crud_operations.get_schemes_by_filters(schemes_filters, fetch_valid_schemes)
        eligibility_results = []

        for scheme in schemes:
            eligibility_results.append(self.check_scheme_eligibility_for_applicant(scheme, applicant))

        return eligibility_results
    
    def check_scheme_eligibility_for_applicant(self, scheme: Scheme, applicant: Applicant) -> EligibilityResult:
        """
        Check if an applicant is eligible for a specific scheme.
        """
        scheme_eligibility_checker = self.schemeFactory.load_scheme_eligibility_checker(scheme)
        is_eligible = scheme_eligibility_checker.check_eligibility(applicant)
        eligible_benefits = scheme_eligibility_checker.calculate_benefits(applicant) if is_eligible else {}
        return EligibilityResult(
            scheme_name=scheme.name,
            scheme_description=scheme.description,
            scheme_start_date=scheme.validity_start_date,
            scheme_end_date=scheme.validity_end_date,
            is_eligible=is_eligible,
            eligible_benefits=eligible_benefits
        )
