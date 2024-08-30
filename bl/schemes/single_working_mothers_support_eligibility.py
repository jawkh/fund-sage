
# Copyright (c) 2024 by Jonathan AW
# This file contains the SingleWorkingMothersSupportEligibility class, which is responsible for determining eligibility for the Single Working Mothers Support Scheme and calculating the benefits the applicant is eligible for.

""" 
Design Patterns:
1. Strategy Pattern:
- The SingleWorkingMothersSupportEligibility class is a concrete strategy class that implements the BaseEligibility interface. It defines the eligibility criteria and benefit calculation logic for the Single Working Mothers Support Scheme.

2. Dependency Injection:
- The class takes a Scheme object as a dependency, allowing for better testability and separation of concerns.

3. Clear and Focused Methods:
- The check_eligibility method clearly defines the eligibility criteria for the scheme, making it easy to understand and maintain.

4. Configuration Management:
- The class uses configuration values to define the eligibility criteria and benefits for the Single Working Mothers Support Scheme, providing flexibility and easy customization.

5. Date Utils:
- The class uses date utility functions to calculate age, improving code readability and maintainability.

6. Clarity of feedback:
- The class returns a tuple with a boolean and a message to indicate eligibility status, providing clear feedback to the caller.

7. Single Responsibility Principle (SRP):
- The class focuses on determining eligibility and calculating benefits for the Single Working Mothers Support Scheme, adhering to the SRP.

8. Readability and Maintainability:
- The class structure and method names are well-organized, making the code easy to understand and maintain.

"""
""" 
single_working_mothers_support_scheme = {
        "name": "Single Working Mothers Support Scheme",
        "description": "A scheme to provide financial support and benefits to single working mothers with young children (18 and below).",
        "eligibility_criteria": {
            "sex": "F",
            "marital_status": ['single', 'divorced', 'widowed'],
            "employment_status": "employed",
            "household_composition": {
                "relation": "child",
                "age_range": {
                    "age_threshold": 18
                }
            }
        },
        "benefits": {
            "cash_assistance": {
                "disbursment_amount": 1000,
                "disbursment_frequency": "One-Off",
                "disbursment_duration_months": None,
                "description": "Cash assistance provided to all eligible applicants."
            },
            "income_tax_rebates": {
                "disbursment_amount": 1000,
                "disbursment_frequency": "annually",
                "disbursment_duration_months": 60,
                "description": "Income Tax Rebates given to all eligible applicants for every eligible children in the household."
            }
        },
        "validity_start_date": datetime(2024, 1, 1),
        "validity_end_date": None
    }
"""
# single_working_mothers_support_eligibility.py

from datetime import datetime
from dal.models import Applicant, Scheme
from bl.schemes.base_eligibility import BaseEligibility
from utils.date_utils import calculate_age
from typing import Dict, List, Any

class SingleWorkingMothersSupportEligibility(BaseEligibility):
    """
    Concrete class for determining eligibility for the Single Working Mothers Support Scheme.
    """

    def __init__(self, scheme: Scheme):
        self.scheme = scheme

    def check_eligibility(self, applicant: Applicant) -> tuple[bool, str]:
        """
        Determine if the applicant is eligible for the Single Working Mothers Support Scheme.

        Criteria:
        - The applicant must be {required_sex}.
        - The applicant must be {required_marital_statuses}.
        - The applicant must be {required_employment_status}.
        - The applicant must have at least one child {child_age_threshold} years old and below in their household.
        """
        eligibility_criteria = self.scheme.eligibility_criteria
        required_sex = eligibility_criteria.get("sex")
        required_marital_statuses = eligibility_criteria.get("marital_status")
        required_employment_status = eligibility_criteria.get("employment_status")
        child_age_threshold = eligibility_criteria.get("household_composition", {}).get("age_range", {}).get("age_threshold")

        # Check if the applicant's sex matches the required sex
        if applicant.sex != required_sex:
            return False, "Not eligible: Applicant is not female."

        # Check if the applicant's marital status is in the list of required statuses
        if applicant.marital_status not in required_marital_statuses:
            return False, "Not eligible: Applicant is not single, divorced, or widowed."

        # Check if the applicant's employment status matches the required status
        if applicant.employment_status != required_employment_status:
            return False, "Not eligible: Applicant is not employed."

        # Check if there is at least one child under 18 in the household
        for member in applicant.household_members:
            if member.relation == "child" and calculate_age(member.date_of_birth) <= child_age_threshold:
                return True, "Eligible for Single Working Mothers Support Scheme."

        return False, f"Not eligible: No child {child_age_threshold} years old or younger in the household."

    def calculate_benefits(self, applicant: Applicant) -> List[Dict[str, Any]]:
        """
        Calculate the benefits the applicant is eligible for under the Single Working Mothers Support Scheme.
        """
        # If the applicant is not eligible, return an empty list
        if not self.check_eligibility(applicant)[0]:
            return []

        benefits_config = self.scheme.benefits
        benefits = []
        
        eligibility_criteria = self.scheme.eligibility_criteria
        child_age_threshold = eligibility_criteria.get("household_composition", {}).get("age_range", {}).get("age_threshold")
        # Add cash assistance benefit
        benefits.append({
            "benefit_name": "cash_assistance",
            "description": benefits_config["cash_assistance"]["description"],
            "beneficiary": applicant.name,
            "disbursment_amount": benefits_config["cash_assistance"]["disbursment_amount"],
            "disbursment_frequency": benefits_config["cash_assistance"]["disbursment_frequency"],
            "disbursment_duration_month": benefits_config["cash_assistance"]["disbursment_duration_months"]
        })

        # Add income tax rebates for each eligible child
        for member in applicant.household_members:
            if member.relation == "child" and calculate_age(member.date_of_birth)  <= child_age_threshold:
                benefits.append({
                    "benefit_name": f"income_tax_rebates for eligible_child: {member.name}",
                    "description": benefits_config["income_tax_rebates"]["description"],
                    "beneficiary": applicant.name,
                    "disbursment_amount": benefits_config["income_tax_rebates"]["disbursment_amount"],
                    "disbursment_frequency": benefits_config["income_tax_rebates"]["disbursment_frequency"],
                    "disbursment_duration_month": benefits_config["income_tax_rebates"]["disbursment_duration_months"]
                })

        return benefits

