# Copyright (c) 2024 by Jonathan AW
# base_scheme_eligibility_checker_factory.py

""" 
Design Pattern: Abstract Factory

1. Use of Abstract Base Class (ABC):
- The BaseSchemeEligibilityCheckerFactory class is correctly defined as an abstract base class, using Python's ABC module. This setup ensures that any concrete subclass must implement the load_scheme_eligibility_checker method.

2. Single Responsibility Principle (SRP):
- The class adheres to the SRP by focusing solely on defining a contract for creating SchemeEligibilityChecker objects. It does not contain any additional logic, making it easy to understand and maintain.

"""

from abc import ABC, abstractmethod
from typing import Type
from dal.models import Scheme
from bl.schemes.scheme_eligibilty_checker import SchemeEligibilityChecker

class BaseSchemeEligibilityCheckerFactory(ABC):
    """
    Abstract Base Factory class to create SchemeEligibilityChecker objects,
    which pair a Scheme with its corresponding Eligibility definitions.
    """
    
    @abstractmethod
    def load_scheme_eligibility_checker(self, scheme: Scheme) -> SchemeEligibilityChecker:
        """
        Instantiate a SchemeEligibilityChecker object that associates the scheme 
        with its eligibility strategy.

        Args:
            scheme (Scheme): The scheme for which the eligibility checker is to be created.

        Returns:
            SchemeEligibilityChecker: An instance that pairs the scheme with its eligibility strategy.
        """
        pass
