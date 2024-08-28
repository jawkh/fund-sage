# Copyright (c) 2024 by Jonathan AW

from dal.models import Scheme
from bl.schemes.base_eligibility import BaseEligibility

class SchemeEligibilityChecker:
    """
    Context class for checking eligibility for various schemes.
    """

    def __init__(self, scheme: Scheme, eligibility_strategy:BaseEligibility):
        self.eligibility_strategy = eligibility_strategy
        self.scheme = scheme

    