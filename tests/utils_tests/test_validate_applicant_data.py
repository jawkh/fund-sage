# Copyright (c) 2024 by Jonathan AW

import pytest
from datetime import datetime
from utils.data_validation import validate_administrator_data, validate_application_data, validate_applicant_data, validate_household_member_data, validate_scheme_data, validate_system_configuration_data  # Adjust import path as needed


# Validate applicant data
def test_validate_applicant_data_valid():
    applicant_data = {
        "name": "John Doe",
        "employment_status": "employed",
        "sex": "M",
        "date_of_birth": datetime(1990, 1, 1),
        "marital_status": "single"
    }
    is_valid, message = validate_applicant_data(applicant_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_applicant_data_missing_required_fields():
    applicant_data = {
        "name": "John Doe",
        "employment_status": "employed"
    }
    is_valid, message = validate_applicant_data(applicant_data, for_create_mode=True)
    assert not is_valid
    assert message == "Missing or empty field: sex"

def test__neg_validate_applicant_data_invalid_data_type():
    applicant_data = {
        "name": "John Doe",
        "employment_status": "employed",
        "sex": "M",
        "date_of_birth": "1990-01-01",  # Invalid type
        "marital_status": "single"
    }
    is_valid, message = validate_applicant_data(applicant_data, for_create_mode=True)
    assert not is_valid
    assert message == "Invalid value for date_of_birth: must be a datetime object"

def test__neg_validate_applicant_data_invalid_values():
    applicant_data = {
        "name": "John Doe",
        "employment_status": "unknown",  # Invalid value
        "sex": "X",  # Invalid value
        "date_of_birth": datetime(1990, 1, 1),
        "marital_status": "single"
    }
    is_valid, message = validate_applicant_data(applicant_data, for_create_mode=True)
    assert not is_valid
    assert message == "Invalid value for employment_status: must be 'employed' or 'unemployed'"

def test_validate_applicant_data_optional_fields():
    applicant_data = {
        "name": "John Doe",
        "employment_status": "employed",
        "sex": "M",
        "date_of_birth": datetime(1990, 1, 1),
        "marital_status": "single",
        "employment_status_change_date": None
    }
    is_valid, message = validate_applicant_data(applicant_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"

# Validate household member data
def test_validate_household_member_data_valid():
    household_member_data = {
        "applicant_id": 1,
        "name": "Jane Doe",
        "relation": "child",
        "date_of_birth": datetime(2010, 5, 20),
        "employment_status": "unemployed",
        "sex": "F"
    }
    is_valid, message = validate_household_member_data(household_member_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_household_member_data_missing_required_fields():
    household_member_data = {
        "applicant_id": 1,
        "name": "Jane Doe"
    }
    is_valid, message = validate_household_member_data(household_member_data, for_create_mode=True)
    assert not is_valid
    assert message == "Missing or empty field: relation"

def test__neg_validate_household_member_data_invalid_data_type():
    household_member_data = {
        "applicant_id": 1,
        "name": "Jane Doe",
        "relation": "child",
        "date_of_birth": "2010-05-20",  # Invalid type
        "employment_status": "unemployed",
        "sex": "F"
    }
    is_valid, message = validate_household_member_data(household_member_data, for_create_mode=True)
    assert not is_valid
    assert message == "Invalid value for date_of_birth: must be a datetime object"

def test__neg_validate_household_member_data_invalid_values():
    household_member_data = {
        "applicant_id": 1,
        "name": "Jane Doe",
        "relation": "unknown",  # Invalid value
        "date_of_birth": datetime(2010, 5, 20),
        "employment_status": "unemployed",
        "sex": "F"
    }
    is_valid, message = validate_household_member_data(household_member_data, for_create_mode=True)
    assert not is_valid
    assert message == "Invalid value for relation: must be 'parent', 'child', 'spouse', 'sibling', or 'other'"

def test_validate_household_member_data_optional_fields():
    household_member_data = {
        "applicant_id": 1,
        "name": "Jane Doe",
        "relation": "child",
        "date_of_birth": datetime(2010, 5, 20)
    }
    is_valid, message = validate_household_member_data(household_member_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"
    

def test_validate_applicant_data_update_valid():
    applicant_data = {
        "name": "Jane Doe"
    }
    is_valid, message = validate_applicant_data(applicant_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_applicant_data_update_invalid_field_type():
    applicant_data = {
        "date_of_birth": "1990-01-01"  # Invalid type
    }
    is_valid, message = validate_applicant_data(applicant_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for date_of_birth: must be a datetime object"

def test__neg_validate_applicant_data_update_invalid_value():
    applicant_data = {
        "sex": "X"  # Invalid value
    }
    is_valid, message = validate_applicant_data(applicant_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for sex: must be 'M' or 'F'"

def test_validate_applicant_data_update_partial_fields():
    applicant_data = {
        "employment_status": "unemployed"
    }
    is_valid, message = validate_applicant_data(applicant_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"


def test_validate_household_member_data_update_valid():
    household_member_data = {
        "relation": "spouse"
    }
    is_valid, message = validate_household_member_data(household_member_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_household_member_data_update_invalid_field_type():
    household_member_data = {
        "date_of_birth": "2010-05-20"  # Invalid type
    }
    is_valid, message = validate_household_member_data(household_member_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for date_of_birth: must be a datetime object"

def test__neg_validate_household_member_data_update_invalid_value():
    household_member_data = {
        "relation": "unknown"  # Invalid value
    }
    is_valid, message = validate_household_member_data(household_member_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for relation: must be 'parent', 'child', 'spouse', 'sibling', or 'other'"

def test_validate_household_member_data_update_partial_fields():
    household_member_data = {
        "employment_status": "employed"
    }
    is_valid, message = validate_household_member_data(household_member_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"
