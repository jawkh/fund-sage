# Copyright (c) 2024 by Jonathan AW
# Summary: The SeniorCitizenAssistanceEligibility class is responsible for determining eligibility for the Senior Citizen Assistance Scheme and calculating the benefits the applicant is eligible for.

""" 
summary: This module contains the SeniorCitizenEligibility class, which is a concrete strategy class for determining eligibility for the Senior Citizen Scheme.
Simplistic rule is used to determine if an applicant is eligible for senior citizen benefits based on their age. Not everything has to be super complicated. (:

Design Patterns:
1. Strategy Pattern:
- The SeniorCitizenEligibility class is a concrete strategy class that implements the BaseEligibility interface. It defines the eligibility criteria and benefit calculation logic for the Senior Citizen Scheme.

2. Dependency Injection:
- The class takes a database session object as a dependency, allowing for better testability and separation of concerns.

3. Clear and Focused Methods:
- The check_eligibility method clearly defines the eligibility criteria for the scheme, making it easy to understand and maintain.

4. Configuration Management:
- The class uses configuration values to define the eligibility criteria, providing flexibility and easy customization.

5. Date Utils:
- The class uses date utility functions to calculate age, improving code readability and maintainability.

6. Clarity of feedback:
- The class returns a tuple with a boolean and a message to indicate eligibility status, providing clear feedback to the caller.

7. Single Responsibility Principle (SRP):
- The class focuses on determining eligibility for the Senior Citizen Scheme, adhering to the SRP.

8. Readability and Maintainability:
- The class structure and method names are well-organized, making the code easy to understand and maintain.


"""

"""
senior_citizen_assistance_scheme_data = {
    "name": "Senior Citizen Assistance Scheme",
    "description": "A scheme to provide financial support and benefits to individuals aged 65 and above.",
    "eligibility_criteria": {
        "age_threshold": 65
    },
    "benefits": {
        "cpf_top_up": {
            "disbursment_amount": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_months": None,
            "description": "One-time CPF top-up of $200."
        },
        "cdc_voucher": {
            "disbursment_amount": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_months": None,
            "description": "One-time CDC voucher of $200."
        }
    },
    "validity_start_date": datetime(2024, 1, 1),
    "validity_end_date": None
}

"""
# senior_citizen_eligibility.py

from datetime import datetime
from dal.models import Applicant, Scheme
from bl.schemes.base_eligibility import BaseEligibility
from utils.date_utils import calculate_age  # Assume this utility exists
from sqlalchemy.orm import Session
from typing import Dict, List, Any

class SeniorCitizenAssistanceEligibility(BaseEligibility):
    """
    Concrete strategy class for determining eligibility for the Senior Citizen Scheme.
    """

    def __init__(self, scheme: Scheme):
        self.__scheme = scheme

    def check_eligibility(self, applicant: Applicant) -> tuple[bool, str]:
        """
        Determine if the applicant is eligible for senior citizen benefits.
        
        Criteria:
        - The applicant must be 65 years or older.
        """
        eligibility_criteria = self.__scheme.eligibility_criteria
        age_threshold = eligibility_criteria.get("age_threshold")

        applicant_age = calculate_age(applicant.date_of_birth)
        if applicant_age >= age_threshold:
            return True, "Eligible for Senior Citizen Assistance Scheme."

        return False, "Not eligible for Senior Citizen Assistance Scheme."

    def calculate_benefits(self, applicant: Applicant) -> List[Dict[str, Any]]:
        """
        Calculate the benefits the applicant is eligible for under the Senior Citizen Scheme.
        """
        is_eligible, _ = self.check_eligibility(applicant)
        benefits = []

        if is_eligible:
            benefits_config = self.__scheme.benefits
            
            # One-time CPF top-up
            benefits.append({
                "benefit_name": "cpf_top_up",
                "description": benefits_config["cpf_top_up"]["description"],
                "beneficiary": applicant.name,
                "disbursment_amount": benefits_config["cpf_top_up"]["disbursment_amount"],
                "disbursment_frequency": benefits_config["cpf_top_up"]["disbursment_frequency"],
                "disbursment_duration": benefits_config["cpf_top_up"]["disbursment_duration_months"]
            })

            # One-time CDC voucher
            benefits.append({
                "benefit_name": "cdc_voucher",
                "description": benefits_config["cdc_voucher"]["description"],
                "beneficiary": applicant.name,
                "disbursment_amount": benefits_config["cdc_voucher"]["disbursment_amount"],
                "disbursment_frequency": benefits_config["cdc_voucher"]["disbursment_frequency"],
                "disbursment_duration": benefits_config["cdc_voucher"]["disbursment_duration_months"]
            })

        return benefits

