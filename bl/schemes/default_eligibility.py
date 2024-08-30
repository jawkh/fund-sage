# Copyright (c) 2024 by Jonathan AW
# deault_eligibility.py
# Summary: The DefaultEligibility class is a concrete implementation of the BaseEligibility strategy. It provides default behavior for checking eligibility and calculating benefits when the eligibility criteria are not configured for a scheme.
""" 
Design Pattern: Strategy Pattern

1. DefaultEligibility Class:
- The DefaultEligibility class is a concrete implementation of the BaseEligibility strategy. It provides default behavior for checking eligibility and calculating benefits when the eligibility criteria are not configured for a scheme.

2. Default Responses:
- The check_eligibility and calculate_benefits methods return default responses indicating that the scheme's eligibility criteria are not configured. This ensures consistent behavior and error handling for unconfigured schemes.

3. Type Annotations:
- The use of type annotations for method arguments and return types enhances code readability and maintainability.

4. Clear and Focused Methods:
- The check_eligibility and calculate_benefits methods are clear and focused, providing a simple interface for handling unconfigured schemes.

5. Single Responsibility Principle (SRP):
- The class focuses on providing default behavior for unconfigured schemes, adhering to the SRP.

6. Readability and Maintainability:
- The class structure and method names are well-organized, making the code easy to understand and maintain.

"""
# default_eligibility.py
from bl.schemes.base_eligibility import BaseEligibility
from dal.models import Applicant, Scheme
from typing import Dict, List, Any

class DefaultEligibility(BaseEligibility):
    """
    Concrete class for default eligibility.
    """

    def check_eligibility(self, applicant: Applicant) -> tuple[bool, str]:
        """
        Default method indicating that the scheme's eligibility criteria are not configured.
        """
        return False, "Scheme Eligibility Checker Not Configured for!"
    
    def calculate_benefits(self, applicant: Applicant)-> List[Dict[str, Any]]:
        """
        Default method indicating no benefits are available due to lack of criteria.
        """
        return []