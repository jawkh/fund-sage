# Copyright (c) 2024 by Jonathan AW


from typing import Type, Optional
from dal.models import Scheme
from bl.schemes.base_eligibility import BaseEligibility
from bl.schemes.retrenchment_assistance_eligibility import RetrenchmentAssistanceEligibility
from bl.schemes.senior_citizen_eligibility import SeniorCitizenEligibility
from dal.crud_operations import CRUDOperations
from bl.factories.base_scheme_eligibility_checker_factory import BaseSchemeEligibilityCheckerFactory
from bl.schemes.scheme_eligibilty_checker import SchemeEligibilityChecker

class SchemeEligibilityCheckerFactory(BaseSchemeEligibilityCheckerFactory):
    """
    Factory class to create Scheme objects with their corresponding SchemeEligibility strategy.
    """

    def load_scheme_eligibility_checker(scheme_data: dict, crud_operations: CRUDOperations) -> SchemeEligibilityChecker:
        """
        Instantiate a Scheme object and associate it with its eligibility strategy.
        """
        scheme = Scheme(**scheme_data)
        eligibility_strategy = SchemeEligibilityCheckerFactory.get_eligibility_strategy(scheme, crud_operations)
        return SchemeEligibilityChecker(scheme, eligibility_strategy)

    def get_eligibility_strategy(scheme: Scheme, crud_operations: CRUDOperations) -> Optional[BaseEligibility]:
        """
        Retrieve the appropriate eligibility strategy based on the scheme type.
        """
        strategy_mapping = {
            "Retrenchment Assistance Scheme": RetrenchmentAssistanceEligibility,
            "Senior Citizen Scheme": SeniorCitizenEligibility,
            # More schemes and their strategies can be added here
        }
        strategy_class: Type[BaseEligibility] = strategy_mapping.get(scheme.name)
        if strategy_class:
            return strategy_class(system_config=crud_operations.system_config)
        raise ValueError(f"No eligibility strategy found for scheme: {scheme.name}")
