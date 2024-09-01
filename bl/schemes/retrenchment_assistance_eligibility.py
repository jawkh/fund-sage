# Copyright (c) 2024 by Jonathan AW
# retrenchment_assistance_eligibility.py
# Summary: The RetrenchmentAssistanceEligibility class is responsible for determining eligibility for the Retrenchment Assistance Scheme and calculating the benefits the applicant is eligible for.

""" 
Summary: The RetrenchmentAssistanceEligibility class is responsible for determining eligibility for the Retrenchment Assistance Scheme and calculating the benefits the applicant is eligible for.

Design Patterns:
1. Strategy Pattern:
- The RetrenchmentAssistanceEligibility class is a concrete strategy class that implements the BaseEligibility interface. It defines the eligibility criteria and benefit calculation logic for the Retrenchment Assistance Scheme.

2. Dependency Injection:
- The class takes a database session object as a dependency, allowing for better testability and separation of concerns.

3. Clear and Focused Methods:
- The check_eligibility method clearly defines the eligibility criteria for the scheme, making it easy to understand and maintain.

4. Configuration Management:
- The class uses configuration data from the Scheme model to determine the eligibility criteria and benefits for the Retrenchment Assistance Scheme, promoting flexibility and maintainability.

5. Type Annotations:
- The use of type annotations for method arguments and return types enhances code readability and maintainability.

6. Date Utils:
- The class uses date utility functions to calculate age and check if a date is within a specified period, improving code readability and maintainability.

7. Clarity of feedback:
- The class returns a tuple with a boolean and a message to indicate eligibility status, providing clear feedback to the caller.

8. Single Responsibility Principle (SRP):
- The class focuses on determining eligibility and calculating benefits for the Retrenchment Assistance Scheme, adhering to the SRP.


"""

""" 

retrenchment_assistance_scheme_data = {
    "name": "Retrenchment Assistance Scheme",
    "description": "A scheme to provide financial support and benefits to individuals who have recently been retrenched from their jobs.",
    "eligibility_criteria": {
        "employment_status": "unemployed",
        "retrechment_period_months": 6,
    },
    "benefits": {
        "cash_assistance": {
        "disbursment_amount": 1000,
        "disbursment_frequency": "One-Off",
        "disbursment_duration_months": None,
        "description": "Cash assistance provided to all eligible applicants."
        },
        "school_meal_vouchers": {
        "amount_per_child": 100,
        "disbursment_frequency": "Monthly",
        "disbursment_duration_months": 12,
        "description": "Meal vouchers provided for each child in the household within the primary school age range (6-11 years old).",
        "eligibility": {
            "relation": "child",
            "age_range": {
            "min": 6,
            "max": 11
            }
        }
        },
        "extra_cdc_vouchers": {
        "amount_per_parent": 200,
        "disbursment_frequency": "One-Off",
        "disbursment_duration_months": None,
        "description": "Extra CDC vouchers provided for each elderly parent above the age of 65.",
        "eligibility": {
            "relation": "parent",
            "age_threshold": 65
        }
        }
    },
    "validity_start_date": datetime(2024, 1, 1),
    "validity_end_date": None
    }

"""

# retrenchment_assistance_eligibility.py

from dal.models import Applicant, Scheme
from bl.schemes.base_eligibility import BaseEligibility
from utils.date_utils import is_within_last_months, calculate_age
from typing import Dict, List, Any

class RetrenchmentAssistanceEligibility(BaseEligibility):
    """
    Concrete class for determining eligibility for the Retrenchment Assistance Scheme.
    """

    def __init__(self, scheme: Scheme):
        self.scheme = scheme

    def check_eligibility(self, applicant: Applicant) -> tuple[bool, str]:
        """
        Determine if the applicant is eligible for retrenchment assistance.
        
        Criteria:
        - The applicant must be unemployed.
        - The applicant must have become unemployed within the last 'X' months.
        """
        eligibility_criteria = self.scheme.eligibility_criteria
        required_employment_status = eligibility_criteria.get("employment_status")
        retrenchment_period_months = eligibility_criteria.get("retrechment_period_months")

        if applicant.employment_status == required_employment_status:
            if applicant.employment_status_change_date:
                if is_within_last_months(applicant.employment_status_change_date, retrenchment_period_months):
                    return True, "Eligible for Retrenchment Assistance."

        return False, "Not eligible for Retrenchment Assistance."

    def calculate_benefits(self, applicant: Applicant) -> List[Dict[str, Any]]:
        if not self.check_eligibility(applicant)[0]:
            return []
        """
        Calculate the benefits the applicant is eligible for under the Retrenchment Assistance Scheme.
        Includes checks for children in the primary school age group and elderly parents.
        """
        benefits_config = self.scheme.benefits
        primary_school_age_min = benefits_config.get("school_meal_vouchers", {}).get("eligibility", {}).get("age_range", {}).get("min")
        primary_school_age_max = benefits_config.get("school_meal_vouchers", {}).get("eligibility", {}).get("age_range", {}).get("max")
        elderly_age_threshold = benefits_config.get("extra_cdc_vouchers", {}).get("eligibility", {}).get("age_threshold")
        school_meal_voucher_eligiblity_relation = benefits_config.get("school_meal_vouchers", {}).get("eligibility", {}).get("relation")
        extra_cdc_voucher_eligiblity_relation = benefits_config.get("extra_cdc_vouchers", {}).get("eligibility", {}).get("relation")
        benefits = []

        # Add cash assistance benefit if eligible
        benefits.append({
            "benefit_name": "cash_assistance",
            "description": benefits_config["cash_assistance"]["description"],
            "beneficiary": applicant.name,
            "disbursment_amount": benefits_config["cash_assistance"]["disbursment_amount"],
            "disbursment_frequency": benefits_config["cash_assistance"]["disbursment_frequency"],
            "disbursment_duration_month": benefits_config["cash_assistance"]["disbursment_duration_months"]
        })

        # Check if the applicant has children within the primary school age range
        for child in applicant.household_members:
            child_age = calculate_age(child.date_of_birth)
            if child.relation == school_meal_voucher_eligiblity_relation and primary_school_age_min <= child_age <= primary_school_age_max:
                benefits.append({
                    "benefit_name": "school_meal_vouchers",
                    "description": benefits_config["school_meal_vouchers"]["description"],
                    "beneficiary": child.name,
                    "disbursment_amount": benefits_config["school_meal_vouchers"]["amount_per_child"],
                    "disbursment_frequency": benefits_config["school_meal_vouchers"]["disbursment_frequency"],
                    "disbursment_duration_month": benefits_config['school_meal_vouchers']['disbursment_duration_months']
                })

        # Check if the applicant has elderly parents above the age threshold
        for member in applicant.household_members:
            parent_age = calculate_age(member.date_of_birth)
            if member.relation == extra_cdc_voucher_eligiblity_relation and parent_age > elderly_age_threshold:
                benefits.append({
                    "benefit_name": "extra_cdc_vouchers",
                    "description": benefits_config["extra_cdc_vouchers"]["description"],
                    "beneficiary": member.name,
                    "disbursment_amount": benefits_config["extra_cdc_vouchers"]["amount_per_parent"],
                    "disbursment_frequency": benefits_config["extra_cdc_vouchers"]["disbursment_frequency"],
                    "disbursment_duration_month": benefits_config["extra_cdc_vouchers"]["disbursment_duration_months"]
                })

        return benefits
