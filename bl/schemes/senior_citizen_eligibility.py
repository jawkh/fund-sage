# Copyright (c) 2024 by Jonathan AW
# senior_citizen_eligibility.py

""" 
summary: This module contains the SeniorCitizenEligibility class, which is a concrete strategy class for determining eligibility for the Senior Citizen Scheme.
Simplistic rule is used to determine if an applicant is eligible for senior citizen benefits based on their age. Not everything has to be super complicated. (:
"""
from datetime import datetime
from dal.models import Applicant
from bl.schemes.base_eligibility import BaseEligibility
from utils.date_utils import calculate_age  # Assume this utility exists
from utils.config_utils import get_configuration_value
from sqlalchemy.orm import Session

class SeniorCitizenEligibility(BaseEligibility):
    """
    Concrete strategy class for determining eligibility for the Senior Citizen Scheme.
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def check_eligibility(self, applicant: Applicant) -> tuple[bool, str]:
        """
        Determine if the applicant is eligible for senior citizen benefits.
        Criteria:
        - The applicant must be 65 years or older.
        """
        age = calculate_age(applicant.date_of_birth)
        elderly_age_threshold = int(get_configuration_value(self.db_session, "ElderlyAgeThreshold", 65))
        if age >= elderly_age_threshold:
            return True, "Eligible for Senior Citizen Benefits."
        return False, "Not eligible for Senior Citizen Benefits."

    def calculate_benefits(self, applicant: Applicant) -> dict:
        """
        Calculate benefits for eligible senior citizens.
        """
        is_eligible, _ = self.check_eligibility(applicant)
        if is_eligible:
            return {"benefits": "Senior Citizen Benefits"}
        return {}
