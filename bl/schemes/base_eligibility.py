# Copyright (c) 2024 by Jonathan AW
# base_eligibility.py
""" 
Design Pattern: Strategy

1. Abstract Base Class:
- The BaseEligibility class is an abstract base class that defines the interface for all eligibility classes. It provides default implementations for non-configured eligibility criteria and benefits.

2. Abstract Methods:
- The check_eligibility and calculate_benefits methods are abstract and must be implemented by subclasses. This enforces the implementation of specific eligibility criteria and benefit calculations for each scheme.

3. Default Responses:
- The default_eligibility_response and default_benefits_response methods provide default responses when eligibility criteria are not configured. This ensures consistent behavior and error handling.

4. Type Annotations:
- The use of type annotations for method arguments and return types enhances code readability and maintainability.

5. Encapsulation:
- The BaseEligibility class encapsulates the common behavior of eligibility classes, promoting code reuse and maintainability.

6. Clear Naming:
- The class name and method names are clear and descriptive, making the code easy to understand and navigate.

7. Compliance with Liskov Substitution Principle (LSP):
- The BaseEligibility class adheres to the LSP by defining a common interface for all eligibility classes. This allows subclasses to be substituted for the base class without affecting the behavior of the system.

8. Readability and Maintainability:
- The class structure and method names are well-organized, enhancing code readability and maintainability.

9. Compliance with Open/Closed Principle (OCP):
- The BaseEligibility class is designed to be open for extension and closed for modification. Subclasses can extend the behavior of the base class by implementing specific eligibility criteria and benefit calculations.

10. Compliance with Interface Segregation Principle (ISP):
- The BaseEligibility class segregates the interface for eligibility checks and benefit calculations, ensuring that each class has a clear and focused responsibility.

11. Compliance with Dependency Inversion Principle (DIP):
- The BaseEligibility class depends on abstractions (abstract methods) rather than concrete implementations, promoting loose coupling and flexibility in defining eligibility criteria and benefits.

12. Testability:
- The class design allows for easy testing of eligibility checks and benefit calculations. By providing clear interfaces and default responses, the class ensures reliable behavior and testability.

13. Error Handling:
- The default methods provide error messages when eligibility criteria are not configured, enhancing error handling and user feedback.

14. Flexibility:
- The BaseEligibility class provides a flexible framework for defining eligibility criteria and benefits, allowing for easy customization and extension of eligibility rules.

15. Separation of Concerns:
- The class focuses on defining the common behavior of eligibility classes, following the Single Responsibility Principle (SRP). It separates the concerns of eligibility checks and benefit calculations, promoting code organization and clarity.

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
