# Copyright (c) 2024 by Jonathan AW

from datetime import datetime
from dal.models import Applicant
from bl.schemes.base_eligibility import BaseEligibility

class SeniorCitizenEligibility(BaseEligibility):
    """
    Concrete strategy class for determining eligibility for the Senior Citizen Scheme.
    """

    def check_eligibility(self, applicant: Applicant) -> tuple[bool, str]:
        """
        Determine if the applicant is eligible for senior citizen benefits.
        Criteria:
        - The applicant must be 65 years or older.
        """
        today = datetime.today()
        birth_date = datetime.strptime(applicant.date_of_birth, "%Y-%m-%d")
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age >= 65:
            return True, "Eligible for Senior Citizen Benefits."
        return False, "Not eligible for Senior Citizen Benefits."

def calculate_benefits(self, applicant: Applicant) -> dict:
    if self.check_eligibility(applicant):
        return {"benefits": "Senior Citizen Benefits"}
    