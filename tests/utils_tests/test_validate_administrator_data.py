# Copyright (c) 2024 by Jonathan AW

import pytest
from datetime import datetime
from utils.data_validation import validate_administrator_data, validate_application_data, validate_applicant_data, validate_household_member_data, validate_scheme_data, validate_system_configuration_data  # Adjust import path as needed

# Validate administrator data
def test_validate_administrator_data_valid():
    # Test with valid data
    admin_data = {
        "username": "admin_user",
        "password_hash": "hashed_password",
        "salt": "random_salt",
        "role": "admin",
        "consecutive_failed_logins": 0,
        "account_locked": False,
        "failed_login_starttime": None
    }
    is_valid, message = validate_administrator_data(admin_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_administrator_data_missing_required_fields():
    # Test with missing required fields
    admin_data = {
        "username": "admin_user",
        "password_hash": "hashed_password"
    }
    is_valid, message = validate_administrator_data(admin_data, for_create_mode=True)
    assert not is_valid
    assert message == "Missing or empty field: salt"

def test__neg_validate_administrator_data_invalid_data_type():
    # Test with invalid data types
    admin_data = {
        "username": "admin_user",
        "password_hash": 123,  # Invalid type
        "salt": "random_salt"
    }
    is_valid, message = validate_administrator_data(admin_data, for_create_mode=True)
    assert not is_valid
    assert message == "Invalid value for password_hash: must be a non-empty string"


def test_validate_administrator_data_optional_fields():
    # Test with optional fields set to None
    admin_data = {
        "username": "admin_user",
        "password_hash": "hashed_password",
        "salt": "random_salt",
        "consecutive_failed_logins": 0,
        "account_locked": False,
        "failed_login_starttime": None
    }
    is_valid, message = validate_administrator_data(admin_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"



def test_validate_administrator_data_update_valid():
    # Test with valid data for update
    admin_data = {
        "username": "admin_user",
        "role": "admin"
    }
    is_valid, message = validate_administrator_data(admin_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_administrator_data_update_invalid_field_type():
    # Test with invalid field type for update
    admin_data = {
        "consecutive_failed_logins": "three"  # Invalid type
    }
    is_valid, message = validate_administrator_data(admin_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for consecutive_failed_logins: must be a non-negative integer"

def test__neg_validate_administrator_data_update_invalid_value():
    # Test with invalid value for role
    admin_data = {
        "role": 123  # Invalid type
    }
    is_valid, message = validate_administrator_data(admin_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for role: must be a string"

def test_validate_administrator_data_update_partial_fields():
    # Test with partial fields for update
    admin_data = {
        "username": "new_admin_user"
    }
    is_valid, message = validate_administrator_data(admin_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"

