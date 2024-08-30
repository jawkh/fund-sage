# Copyright (c) 2024 by Jonathan AW

# test_schemes_manager.py
import pytest
from bl.schemes.schemes_manager import SchemesManager
from exceptions import SchemeNotFoundException

def test_check_schemes_eligibility_no_schemes(scheme_manager, test_applicant):
    """
    Test checking eligibility when no schemes match the filters.
    """
    results = scheme_manager.check_schemes_eligibility_for_applicant({}, False, test_applicant)
    assert results == []
