
# Copyright (c) 2024 by Jonathan AW
# middleaged_reskilling_assistance_eligibility.py

""" 
Summary of MiddleagedReskillingAssistanceEligibility: 
The MiddleagedReskillingAssistanceEligibility class is responsible for determining eligibility for the Middle-aged Reskilling Assistance Scheme and calculating the benefits the applicant is eligible for.

Design Patterns:
1. Strategy Pattern:
It defines the eligibility criteria and benefit calculation logic for the Middleaged Reskilling Assistance Scheme.

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
middleaged_reskilling_assistance_scheme_data = {
    "name": "Middle-aged Reskilling Assistance Scheme",
    "description": "A scheme to provide financial support and benefits to individuals aged 40 and above who are unemployed, encouraging reskilling and upskilling.",
    "eligibility_criteria": {
        "age_threshold": 40,
        "employment_status": "unemployed"
    },
    "benefits": {
        "skillsfuture_credit_top_up": {
            "disbursment_amount": 1000,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_months": None,
            "description": "One-time Skillsfuture Credit top-up of $1000."
        },
        "study_allowance": {
            "disbursment_amount": 2000,
            "disbursment_frequency": "Monthly",
            "disbursment_duration_months": 6,
            "description": "Monthly study allowance of $5000 for up to 6 months."
        }
    },
    "validity_start_date": datetime(2024, 1, 1),
    "validity_end_date": None
}
    
"""

from datetime import datetime
from dal.models import Applicant, Scheme
from bl.schemes.base_eligibility import BaseEligibility
from utils.date_utils import calculate_age  # Assume this utility exists
from sqlalchemy.orm import Session
from typing import Dict, List, Any

class MiddleagedReskillingAssistanceEligibility(BaseEligibility):
    """
    Concrete strategy class for determining eligibility for the Middle-aged Reskilling Assistance Scheme.
    """

    def __init__(self, scheme: Scheme):
        self.scheme = scheme

    def check_eligibility(self, applicant: Applicant) -> tuple[bool, str]:
        """
        Determine if the applicant is eligible for middle-aged reskilling assistance.

        Criteria:
        - The applicant must be 40 years or older.
        - The applicant must be unemployed.
        """
        eligibility_criteria = self.scheme.eligibility_criteria
        age_threshold = eligibility_criteria.get("age_threshold", 40)
        required_employment_status = eligibility_criteria.get("employment_status", "unemployed")

        applicant_age = calculate_age(applicant.date_of_birth)
        if applicant_age >= age_threshold and applicant.employment_status == required_employment_status:
            return True, "Eligible for Middle-aged Reskilling Assistance."
        
        return False, "Not eligible for Middle-aged Reskilling Assistance."

    def calculate_benefits(self, applicant: Applicant) -> List[Dict[str, Any]]:
        """
        Calculate the benefits the applicant is eligible for under the Middle-aged Reskilling Assistance Scheme.
        """
        is_eligible, _ = self.check_eligibility(applicant)
        benefits = []

        if is_eligible:
            benefits_config = self.scheme.benefits
            
            # One-time Skillsfuture Credit top-up
            benefits.append({
                "benefit_name": "skillsfuture_credit_top_up",
                "description": benefits_config["skillsfuture_credit_top_up"]["description"],
                "beneficiary": applicant.name,
                "disbursment_amount": benefits_config["skillsfuture_credit_top_up"]["disbursment_amount"],
                "disbursment_frequency": benefits_config["skillsfuture_credit_top_up"]["disbursment_frequency"],
                "disbursment_duration": benefits_config["skillsfuture_credit_top_up"]["disbursment_duration_months"]
            })

            # Monthly study allowance
            benefits.append({
                "benefit_name": "study_allowance",
                "description": benefits_config["study_allowance"]["description"],
                "beneficiary": applicant.name,
                "disbursment_amount": benefits_config["study_allowance"]["disbursment_amount"],
                "disbursment_frequency": benefits_config["study_allowance"]["disbursment_frequency"],
                "disbursment_duration": benefits_config["study_allowance"]["disbursment_duration_months"]
            })

        return benefits
