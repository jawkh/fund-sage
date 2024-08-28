# Copyright (c) 2024 by Jonathan AW
from datetime import datetime, timedelta
from dal.models import Applicant
from bl.schemes.base_eligibility import BaseEligibility
from dal.crud_operations import SystemConfigurations
from typing import Optional

class RetrenchmentAssistanceEligibility(BaseEligibility):
    """
    Concrete strategy class for determining eligibility for the Retrenchment Assistance Scheme.
    """

    def __init__(self, system_config: Optional[SystemConfigurations] = None):
        # Use dependency injection for system configuration
        self.system_config = system_config or SystemConfigurations()

    def check_eligibility(self, applicant: Applicant) -> bool:
        """
        Determine if the applicant is eligible for retrenchment assistance.
        Target beneficiaries are those who have recently been retrenched, not those who are permanently unemployed.
        
        Criteria:
        - The applicant must be unemployed.
        - The applicant must have become unemployed within the last 'X' months.
        """
        required_employment_status = self.system_config.get_configuration("RetrenchmentAssistance_EmploymentStatus")
        retrenchment_period_months = int(self.system_config.get_configuration("RetrenchmentAssistance_PeriodMonths"))
        
        if applicant.employment_status == required_employment_status:
            # Check if unemployment date is within the last 'X' months [Must be Recently retrenched and not permanently unemployed]
            if applicant.employment_status_change_date:
                cutoff_date = datetime.now() - timedelta(days=30 * retrenchment_period_months)
                if applicant.employment_status_change_date >= cutoff_date:
                    return True
        return False
    
    def calculate_benefits(self, applicant: Applicant) -> dict:
        """
        Calculate the benefits the applicant is eligible for under the Retrenchment Assistance Scheme.
        Includes checks for children in the primary school age group and elderly parents.
        """
        benefits_config = self.system_config.get_configuration("RetrenchmentAssistance_Benefits")
        primary_school_age_min = int(self.system_config.get_configuration("PrimarySchoolAgeMin"))
        primary_school_age_max = int(self.system_config.get_configuration("PrimarySchoolAgeMax"))
        elderly_age_threshold = int(self.system_config.get_configuration("ElderlyAgeThreshold"))

        benefits = {}
        children_eligible_for_vouchers = []
        parents_eligible_for_cdc_vouchers = []

        today = datetime.today()

        # Check if the applicant has children within the primary school age range
        for child in applicant.household:
            child_age = today.year - child.date_of_birth.year - ((today.month, today.day) < (child.date_of_birth.month, child.date_of_birth.day))
            if child.relation == "child" and primary_school_age_min <= child_age <= primary_school_age_max:
                children_eligible_for_vouchers.append(child.name)

        # Check if the applicant has elderly parents above the age threshold
        for member in applicant.household:
            parent_age = today.year - member.date_of_birth.year - ((today.month, today.day) < (member.date_of_birth.month, member.date_of_birth.day))
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