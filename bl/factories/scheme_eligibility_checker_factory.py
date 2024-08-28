# Copyright (c) 2024 by Jonathan AW
# scheme_eligibility_checker_factory.py
""" 
Design Pattern: Factory Method

1. Factory Method Implementation:
- The SchemeEligibilityCheckerFactory class implements the Factory Method pattern by providing a method to create SchemeEligibilityChecker objects based on the scheme type.
- The get_eligibility_definition method retrieves the appropriate eligibility definition based on the scheme type, allowing for extensibility and flexibility in adding new eligibility strategies.
"""

from typing import Dict, Optional, Callable
from sqlalchemy.orm import Session
from dal.models import Scheme
from bl.schemes.base_eligibility import BaseEligibility
from bl.schemes.retrenchment_assistance_eligibility import RetrenchmentAssistanceEligibility
from bl.schemes.senior_citizen_eligibility import SeniorCitizenEligibility
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
            "Retrenchment Assistance Scheme": lambda: RetrenchmentAssistanceEligibility(self.db_session),
            "Senior Citizen Scheme": lambda: SeniorCitizenEligibility(self.db_session),
            # More schemes and their strategies can be added here
        }

        # Retrieve the factory function for the scheme's eligibility strategy
        eligibility_definition_factory = eligibility_definitions_mapping.get(scheme.name)

        if not eligibility_definition_factory:
            raise EligibilityStrategyNotFoundException(f"No eligibility strategy found for scheme: {scheme.name}")

        # Call the factory function to instantiate the eligibility strategy
        return eligibility_definition_factory()