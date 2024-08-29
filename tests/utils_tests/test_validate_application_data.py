
# Copyright (c) 2024 by Jonathan AW

""" 
Purpose: Tests for the data validation functions used in the Business Logic Layer (BL) services. [Application Data]
"""

import pytest
from datetime import datetime
from utils.data_validation import validate_administrator_data, validate_application_data, validate_applicant_data, validate_household_member_data, validate_scheme_data, validate_system_configuration_data  # Adjust import path as needed


# Validate application data

def test_validate_application_data_valid():
    application_data = {
        "applicant_id": 1,
        "scheme_id": 2,
        "status": "pending",
        "submission_date": datetime(2024, 1, 1),
        "created_by_admin_id": 3
    }
    is_valid, message = validate_application_data(application_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_application_data_missing_required_fields():
    application_data = {
        "applicant_id": 1,
        "scheme_id": 2
    }
    is_valid, message = validate_application_data(application_data, for_create_mode=True)
    assert not is_valid
    assert message == "Missing or empty field: status"

def test__neg_validate_application_data_invalid_data_type():
    application_data = {
        "applicant_id": "1",  # Invalid type
        "scheme_id": 2,
        "status": "pending"
    }
    is_valid, message = validate_application_data(application_data, for_create_mode=True)
    assert not is_valid
    assert message == "Invalid value for applicant_id: must be an integer"

def test__neg_validate_application_data_invalid_values():
    application_data = {
        "applicant_id": 1,
        "scheme_id": 2,
        "status": "unknown",  # Invalid value
        "submission_date": datetime(2024, 1, 1)
    }
    is_valid, message = validate_application_data(application_data, for_create_mode=True)
    assert not is_valid
    assert message == "Invalid value for status: must be 'pending', 'approved', or 'rejected'"

def test_validate_application_data_optional_fields():
    application_data = {
        "applicant_id": 1,
        "scheme_id": 2,
        "status": "pending",
        "submission_date": datetime(2024, 1, 1)
    }
    is_valid, message = validate_application_data(application_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"
    
    

def test_validate_application_data_update_valid():
    application_data = {
        "status": "approved"
    }
    is_valid, message = validate_application_data(application_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_application_data_update_invalid_field_type():
    application_data = {
        "applicant_id": "1"  # Invalid type
    }
    is_valid, message = validate_application_data(application_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for applicant_id: must be an integer"

def test__neg_validate_application_data_update_invalid_value():
    application_data = {
        "status": "unknown"  # Invalid value
    }
    is_valid, message = validate_application_data(application_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for status: must be 'pending', 'approved', or 'rejected'"

def test_validate_application_data_update_partial_fields():
    application_data = {
        "created_by_admin_id": 2
    }
    is_valid, message = validate_application_data(application_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"
