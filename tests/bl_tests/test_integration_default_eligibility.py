
# Copyright (c) 2024 by Jonathan AW
# This file contains integration tests for the DefaultEligibility class.
# test_integration_default_eligibility.py

import pytest
from datetime import datetime, timedelta
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager
from dal.models import Applicant, Scheme
from bl.schemes.default_eligibility import DefaultEligibility

def test_default_eligibility_for_unconfigured_scheme(applicant_service, crud_operations, test_administrator):
    """
    Test the default eligibility handling for a scheme that does not have a specific eligibility strategy.
    """
    # Step 1: Create a new applicant
    applicant_data = {
        "name": "John Doe",
        "employment_status": "unemployed",
        "sex": "M",
        "date_of_birth": datetime(1980, 5, 21),
        "marital_status": "single",
        "employment_status_change_date": datetime.today() - timedelta(days=120),  # Within last 6 months
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Verify the applicant was created successfully
    assert applicant is not None
    assert applicant.name == "John Doe"

    # Step 2: Create a new scheme without a specific eligibility strategy
    scheme_data = {
        "name": "Unconfigured Scheme",
        "description": "A scheme without a specific eligibility strategy.",
        "eligibility_criteria": {},
        "benefits": {},
        "validity_start_date": datetime(2024, 1, 1),
        "validity_end_date": None
    }
    unconfigured_scheme = crud_operations.create_scheme(scheme_data)

    # Verify the scheme was created successfully
    assert unconfigured_scheme is not None
    assert unconfigured_scheme.name == "Unconfigured Scheme"

    # Step 3: Check eligibility using SchemesManager for the unconfigured scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    
    # This is the officially supported way to check eligibility for a scheme
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(unconfigured_scheme, applicant)

    # Verify that the default eligibility checker was used
    assert eligibility_results is not None
    assert eligibility_results.is_eligible == False  # Default eligibility should return False
    assert eligibility_results.eligibility_message == "Scheme Eligibility Checker Not Configured for!"
    assert eligibility_results.eligible_benefits == []  # Default benefits should be empty

def test_factory_returns_default_eligibility_for_unconfigured_scheme(crud_operations):
    """
    Test that the SchemeEligibilityCheckerFactory returns DefaultEligibility for an unconfigured scheme.
    """
    # Step 1: Create a new scheme without a specific eligibility strategy
    scheme_data = {
        "name": "Unconfigured Scheme",
        "description": "A scheme without a specific eligibility strategy.",
        "eligibility_criteria": {},
        "benefits": {},
        "validity_start_date": datetime(2024, 1, 1),
        "validity_end_date": None
    }
    unconfigured_scheme = crud_operations.create_scheme(scheme_data)

    # Step 2: Use SchemeEligibilityCheckerFactory to get eligibility checker (This is the internal low-level way. Not recommended for normal usage)
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    eligibility_checker = schemeEligibilityCheckerFactory.load_scheme_eligibility_checker(unconfigured_scheme)

    # Verify that the DefaultEligibility class is used
    assert isinstance(eligibility_checker.eligibility_definition, DefaultEligibility)
    assert eligibility_checker.check_eligibility(None)[0] == False
    assert eligibility_checker.check_eligibility(None)[1] == "Scheme Eligibility Checker Not Configured for!"
    assert eligibility_checker.calculate_benefits(None) == []
