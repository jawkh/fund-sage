# Copyright (c) 2024 by Jonathan AW
# base_eligibility.py
""" 
Design Pattern: Strategy

1. Use of Abstract Base Class (ABC):
- The class BaseEligibility is correctly designed as an abstract base class. This ensures that all subclasses provide implementations for the check_eligibility and calculate_benefits methods, enforcing a consistent interface.

2. Default Implementations:
- The default_check_eligibility and default_calculate_benefits methods provide default behaviors that indicate when eligibility checkers are not configured. This is useful as a fallback mechanism and maintains the robustness of the code by preventing crashes due to missing implementations.
"""

from abc import ABC, abstractmethod
from dal.models import Applicant

class BaseEligibility(ABC):
    """
    Abstract base class for all eligibility classes.
    Provides default logic for non-configured eligibility criteria.
    """

    @abstractmethod
    def check_eligibility(self, applicant: Applicant) -> tuple[bool, str]:
        """
        Abstract method for checking eligibility. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def calculate_benefits(self, applicant: Applicant) -> dict:
        """
        Abstract method for calculating benefits. Must be implemented by subclasses.
        """
        pass

    def default_eligibility_response(self) -> tuple[bool, str]:
        """
        Default method indicating that the scheme's eligibility criteria are not configured.
        """
        return False, "Scheme Eligibility Checker Not Configured!"

    def default_benefits_response(self) -> dict:
        """
        Default method indicating no benefits are available due to lack of criteria.
        """
        return {}
