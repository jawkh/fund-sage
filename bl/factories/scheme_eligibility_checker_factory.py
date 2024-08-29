# Copyright (c) 2024 by Jonathan AW
# scheme_eligibility_checker_factory.py
""" 
Design Pattern: 

1. Factory Method:
- The SchemeEligibilityCheckerFactory class implements the Factory Method pattern to create SchemeEligibilityChecker objects based on the type of scheme. This approach allows for flexible instantiation of eligibility checkers for different schemes.

2. Dependency Injection:
- The class takes a database session as a dependency, enabling it to interact with the database to retrieve scheme information.

3. Error Handling:
- The get_eligibility_definition method raises an EligibilityStrategyNotFoundException if no eligibility strategy is found for a given scheme. This exception provides clear feedback when an issue occurs.

4. Use of Lambdas for Instantiation:
- The use of lambdas in the eligibility_definitions_mapping dictionary allows for flexible instantiation of eligibility strategies based on the scheme type. This approach ensures that the correct eligibility strategy is used for each scheme.

5. Type Annotations:
- The use of type annotations for method arguments and return types enhances code readability and type safety.

6. Encapsulation:
- The class encapsulates the logic for creating SchemeEligibilityChecker objects, providing a clean interface for loading eligibility checkers for different schemes.

7. Readability and Maintainability:
- The class structure and method names are well-organized, making the code easy to understand and maintain.


"""
# scheme_eligibility_checker_factory.py

from typing import Dict, Optional, Callable
from sqlalchemy.orm import Session
from dal.models import Scheme
from bl.schemes.base_eligibility import BaseEligibility
from bl.schemes.retrenchment_assistance_eligibility import RetrenchmentAssistanceEligibility
from bl.schemes.senior_citizen_assistance_eligibility import SeniorCitizenAssistanceEligibility
from bl.schemes.middleaged_reskilling_assistance_eligibility import MiddleagedReskillingAssistanceEligibility
from bl.factories.base_scheme_eligibility_checker_factory import BaseSchemeEligibilityCheckerFactory
from bl.schemes.scheme_eligibilty_checker import SchemeEligibilityChecker
from exceptions import EligibilityStrategyNotFoundException

class SchemeEligibilityCheckerFactory(BaseSchemeEligibilityCheckerFactory):
    """
    Factory class to create SchemeEligibilityChecker objects,
    which pair a Scheme with its corresponding Eligibility definitions.
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def load_scheme_eligibility_checker(self, scheme: Scheme) -> SchemeEligibilityChecker:
        """
        Load a SchemeEligibilityChecker for a given scheme by determining the appropriate eligibility strategy.

        Args:
            scheme (Scheme): The scheme for which to load the eligibility checker.

        Returns:
            SchemeEligibilityChecker: An instance pairing the scheme with its eligibility strategy.
        """
        eligibility_definition = self.get_eligibility_definition(scheme)
        return SchemeEligibilityChecker(scheme, eligibility_definition)
        

    
    def get_eligibility_definition(self, scheme: Scheme) -> Optional[BaseEligibility]:
        """
        Retrieve the appropriate eligibility definition based on the scheme type.

        Args:
            scheme (Scheme): The scheme for which to retrieve the eligibility definition.

        Returns:
            Optional[BaseEligibility]: An instance of the eligibility strategy if found.

        Raises:
            EligibilityStrategyNotFoundException: If no strategy is found for the given scheme.
        """
        # Use lambdas to handle instantiation logic for each strategy
        # Use of Lambdas for Consistency: Lambdas ensure all values in eligibility_definitions_mapping are callable, maintaining type consistency and allowing for more flexible initialization logic.
        eligibility_definitions_mapping: Dict[str, Callable[[], BaseEligibility]] = {
            "Retrenchment Assistance Scheme": lambda: RetrenchmentAssistanceEligibility(scheme),
            "Senior Citizen Assistance Scheme": lambda: SeniorCitizenAssistanceEligibility(scheme),
            "Middle-aged Reskilling Assistance Scheme": lambda: MiddleagedReskillingAssistanceEligibility(scheme),
            # More schemes and their strategies can be added here
        }

        # Retrieve the factory function for the scheme's eligibility strategy
        eligibility_definition_factory = eligibility_definitions_mapping.get(scheme.name)

        if not eligibility_definition_factory:
            raise EligibilityStrategyNotFoundException(f"No eligibility strategy found for scheme: {scheme.name}")

        # Call the factory function to instantiate the eligibility strategy
        return eligibility_definition_factory()