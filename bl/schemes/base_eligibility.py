# Copyright (c) 2024 by Jonathan AW

from abc import ABC, abstractmethod
from dal.models import Applicant

class BaseEligibility(ABC):
    """
    Abstract base class for all eligibility classes.
    Provides default logic for non-configured eligibility criteria.
    """

    def check_eligibility(self, applicant: Applicant) -> bool:
        """
        Default method indicating that the scheme's eligibility criteria are not configured.
        """
        return False


    def calculate_benefits(self, applicant: Applicant) -> dict:
        """
        Default method indicating no benefits are available due to lack of criteria.
        """
        return {"NIL": "Scheme Eligibility Checker Not Configured!"}