# Copyright (c) 2024 by Jonathan AW
# base_scheme_eligibility_checker_factory.py
# Summary: The BaseSchemeEligibilityCheckerFactory class defines an abstract factory for creating SchemeEligibilityChecker objects. It enforces the implementation of the load_scheme_eligibility_checker method in concrete subclasses.
""" 
Design Pattern: Abstract Factory

1. Use of Abstract Base Class (ABC):
- The BaseSchemeEligibilityCheckerFactory class is correctly defined as an abstract base class, using Python's ABC module. This setup ensures that any concrete subclass must implement the load_scheme_eligibility_checker method.

2. Single Responsibility Principle (SRP):
- The class adheres to the SRP by focusing solely on defining a contract for creating SchemeEligibilityChecker objects. It does not contain any additional logic, making it easy to understand and maintain.

3. Encapsulation:
- The class encapsulates the logic for creating SchemeEligibilityChecker objects, providing a clean interface for loading eligibility checkers for different schemes.

4. Type Annotations:
- The use of type annotations for method arguments and return types enhances code readability and type safety.

5. Abstract Method:
- The load_scheme_eligibility_checker method is defined as an abstract method, ensuring that concrete subclasses must implement this method. This design enforces consistency and allows for flexible instantiation of eligibility checkers.

6. Readability and Maintainability:
- The class structure and method names are well-organized, making the code easy to understand and maintain.

7. Flexibility and Extensibility:
- The abstract factory pattern allows for the creation of different types of SchemeEligibilityChecker objects based on the scheme type. This flexibility enables the system to support various eligibility strategies for different schemes.
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
