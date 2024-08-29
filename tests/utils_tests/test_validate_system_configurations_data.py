# Copyright (c) 2024 by Jonathan AW

import pytest
from datetime import datetime
from utils.data_validation import validate_administrator_data, validate_application_data, validate_applicant_data, validate_household_member_data, validate_scheme_data, validate_system_configuration_data  # Adjust import path as needed


# validate system configuration data

def test_validate_system_configuration_data_valid():
    config_data = {
        "key": "max_login_attempts",
        "value": "5",
        "description": "Maximum number of allowed login attempts before account lockout.",
        "last_updated": datetime(2024, 1, 1, 10, 30, 0)
    }
    is_valid, message = validate_system_configuration_data(config_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_system_configuration_data_missing_required_fields():
    config_data = {
        "key": "max_login_attempts"
    }
    is_valid, message = validate_system_configuration_data(config_data, for_create_mode=True)
    assert not is_valid
    assert message == "Missing or empty field: value"

def test__neg_validate_system_configuration_data_invalid_data_type():
    config_data = {
        "key": "max_login_attempts",
        "value": 5,  # Invalid type
        "description": "Maximum number of allowed login attempts before account lockout."
    }
    is_valid, message = validate_system_configuration_data(config_data, for_create_mode=True)
    assert not is_valid
    assert message == "Invalid value for value: must be a non-empty string"

def test__neg_validate_system_configuration_data_invalid_values():
    config_data = {
        "key": "max_login_attempts",
        "value": "5",
        "description": 12345  # Invalid type
    }
    is_valid, message = validate_system_configuration_data(config_data, for_create_mode=True)
    assert not is_valid
    assert message == "Invalid value for description: must be a string or None"

def test_validate_system_configuration_data_optional_fields():
    config_data = {
        "key": "max_login_attempts",
        "value": "5",
        "last_updated": datetime(2024, 1, 1, 10, 30, 0)
    }
    is_valid, message = validate_system_configuration_data(config_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"


def test_validate_system_configuration_data_update_valid():
    config_data = {
        "value": "10"
    }
    is_valid, message = validate_system_configuration_data(config_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_system_configuration_data_update_invalid_field_type():
    config_data = {
        "value": 10  # Invalid type
    }
    is_valid, message = validate_system_configuration_data(config_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for value: must be a non-empty string"

def test__neg_validate_system_configuration_data_update_invalid_value():
    config_data = {
        "description": 12345  # Invalid type
    }
    is_valid, message = validate_system_configuration_data(config_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for description: must be a string or None"

def test_validate_system_configuration_data_update_partial_fields():
    config_data = {
        "key": "max_login_attempts"
    }
    is_valid, message = validate_system_configuration_data(config_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"
