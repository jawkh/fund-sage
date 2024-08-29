# Copyright (c) 2024 by Jonathan AW
# scheme_eligibilty_checker.py
""" 
Summary: The SchemeEligibilityChecker class acts as a context that holds a specific scheme and its corresponding eligibility strategy. 

Design Pattern: Strategy
- This allows for a decoupled design where different schemes can use different eligibility strategies without altering the core logic.
- The class is initialized with a Scheme and an eligibility_definition, which is a concrete implementation of the BaseEligibility class. This setup is flexible and adheres to the Open/Closed Principle.
"""
from dal.models import Scheme, Applicant
from bl.schemes.base_eligibility import BaseEligibility

class SchemeEligibilityChecker:
    """
    Context class for checking eligibility for various schemes using a provided eligibility strategy.
    """

    def __init__(self, scheme: Scheme, eligibility_definition: BaseEligibility):
        """
        Initialize with a scheme and its associated eligibility definition.
        """
        self.scheme = scheme
        self.eligibility_definition = eligibility_definition

    def check_eligibility(self, applicant: Applicant) -> bool:
        """
        Check if the applicant is eligible for the scheme using the eligibility definition.
        """
        is_eligible, _ = self.eligibility_definition.check_eligibility(applicant)
        return is_eligible

    def calculate_benefits(self, applicant: Applicant) -> dict:
        """
        Calculate the benefits the applicant is eligible for under the scheme.
        """
        if self.check_eligibility(applicant):
            return self.eligibility_definition.calculate_benefits(applicant)
        return {}
