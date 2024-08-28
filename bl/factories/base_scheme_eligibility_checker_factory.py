# Copyright (c) 2024 by Jonathan AW


from abc import ABC, abstractmethod

from typing import Type, Optional
from dal.models import Scheme
from bl.schemes.base_eligibility import BaseEligibility
from bl.schemes.retrenchment_assistance_eligibility import RetrenchmentAssistanceEligibility
from bl.schemes.senior_citizen_eligibility import SeniorCitizenEligibility
from dal.crud_operations import CRUDOperations
from bl.schemes.scheme_eligibilty_checker import SchemeEligibilityChecker

class BaseSchemeEligibilityCheckerFactory(ABC):
    """
    Abstract Base Factory class to create Scheme objects with their corresponding SchemeEligibility strategy.
    """

    @abstractmethod
    def load_scheme_eligibility_checker(scheme_data: dict, crud_operations: CRUDOperations) -> SchemeEligibilityChecker:
        """
        Instantiate a Scheme object and associate it with its eligibility strategy.
        """
        pass

    @abstractmethod
    def get_eligibility_strategy(scheme: Scheme, crud_operations: CRUDOperations) -> Optional[BaseEligibility]:
        """
        Retrieve the appropriate eligibility strategy based on the scheme type.
        """
        strategy_mapping = {
            "Retrenchment Assistance Scheme": RetrenchmentAssistanceEligibility,
            "Senior Citizen Scheme": SeniorCitizenEligibility,
            # More schemes and their strategies can be added here
        }
        pass