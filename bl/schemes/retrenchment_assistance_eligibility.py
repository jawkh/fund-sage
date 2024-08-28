# Copyright (c) 2024 by Jonathan AW
# retrenchment_assistance_eligibility.py

""" 
Summary: The RetrenchmentAssistanceEligibility class is responsible for determining eligibility for the Retrenchment Assistance Scheme and calculating the benefits the applicant is eligible for.

# Key Features
1. Comprehensive Eligibility Check:
- The check_eligibility method effectively checks multiple criteria for determining eligibility for retrenchment assistance, using configurable values for employment status and the retrenchment period. This makes the function robust and adaptable.

2. Benefit Calculation Logic:
- The calculate_benefits method calculates benefits based on the applicant's household members, checking for children in a specific age range and elderly parents. This dynamic calculation is good practice as it adheres to the specific criteria for benefit eligibility.
"""
from datetime import datetime, timedelta
from dal.models import Applicant
from bl.schemes.base_eligibility import BaseEligibility
from utils.config_utils import get_configuration_value
from typing import Optional
from utils.date_utils import is_within_last_months, calculate_age
from sqlalchemy.orm import Session
class RetrenchmentAssistanceEligibility(BaseEligibility):
    """
    Concrete class for determining eligibility for the Retrenchment Assistance Scheme.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def check_eligibility(self, applicant: Applicant) -> tuple[bool, str]:
        """
        Determine if the applicant is eligible for retrenchment assistance.
        Target beneficiaries are those who have recently been retrenched, not those who are permanently unemployed.
        
        Criteria:
        - The applicant must be unemployed.
        - The applicant must have become unemployed within the last 'X' months.
        """
        required_employment_status = get_configuration_value(self.db_session, "RetrenchmentAssistance_EmploymentStatus", "unemployed")
        retrenchment_period_months = int(get_configuration_value(self.db_session, "RetrenchmentAssistance_PeriodMonths", 6))
        
        if applicant.employment_status == required_employment_status:
            # Check if unemployment date is within the last 'X' months [Must be Recently retrenched and not permanently unemployed]
            if applicant.employment_status_change_date:
                if applicant.employment_status_change_date and is_within_last_months(applicant.employment_status_change_date, retrenchment_period_months):
                    return True, "Eligible for Retrenchment Assistance."

        return False, "Not eligible for Retrenchment Assistance."
    
    def calculate_benefits(self, applicant: Applicant) -> dict:
        """
        Calculate the benefits the applicant is eligible for under the Retrenchment Assistance Scheme.
        Includes checks for children in the primary school age group and elderly parents.
        """
        benefits_config = get_configuration_value(self.db_session, "RetrenchmentAssistance_Benefits")
        primary_school_age_min = int(get_configuration_value(self.db_session, "PrimarySchoolAgeMin", 6))
        primary_school_age_max = int(get_configuration_value(self.db_session, "PrimarySchoolAgeMax", 11))
        elderly_age_threshold = int(get_configuration_value(self.db_session, "ElderlyAgeThreshold", 65))

        benefits = {}
        children_eligible_for_vouchers = []
        parents_eligible_for_cdc_vouchers = []

        today = datetime.today()

        # Check if the applicant has children within the primary school age range
        for child in applicant.household:
            child_age = calculate_age(child.date_of_birth)
            if child.relation == "child" and primary_school_age_min <= child_age <= primary_school_age_max:
                children_eligible_for_vouchers.append(child.name)

        # Check if the applicant has elderly parents above the age threshold
        for member in applicant.household:
            parent_age = calculate_age(member.date_of_birth)
            if member.relation == "parent" and parent_age > elderly_age_threshold:
                parents_eligible_for_cdc_vouchers.append(member.name)

        if children_eligible_for_vouchers and "SchoolMealVouchers" in benefits_config:
            benefits["SchoolMealVouchers"] = {
                "amount": benefits_config["SchoolMealVouchers"],
                "eligible_children": children_eligible_for_vouchers
            }

        if parents_eligible_for_cdc_vouchers and "ExtraCDCvouchers" in benefits_config:
            benefits["ExtraCDCvouchers"] = {
                "amount": benefits_config["ExtraCDCvouchers"],
                "eligible_parents": parents_eligible_for_cdc_vouchers
            }

        return benefits