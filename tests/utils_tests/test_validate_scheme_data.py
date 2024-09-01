
# Copyright (c) 2024 by Jonathan AW

""" 
Purpose: Tests for the data validation functions used in the Business Logic Layer (BL) services. [Scheme Data]
"""

import pytest
from datetime import datetime
from utils.data_validation import validate_administrator_data, validate_application_data, validate_applicant_data, validate_household_member_data, validate_scheme_data, validate_system_configuration_data  # Adjust import path as needed

# Validate scheme data

def test_validate_scheme_data_valid():
    scheme_data = {
        "name": "Health Scheme",
        "description": "A comprehensive health benefits scheme.",
        "eligibility_criteria": {"age": "18+", "income": "below $50,000"},
        "benefits": {"coverage": "up to $10,000 per year"},
        "validity_start_date": datetime(2024, 1, 1),
        "validity_end_date": datetime(2024, 12, 31)
    }
    is_valid, message = validate_scheme_data(scheme_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_scheme_data_missing_required_fields():
    scheme_data = {
        "name": "Health Scheme",
        "description": "A comprehensive health benefits scheme."
    }
    is_valid, message = validate_scheme_data(scheme_data, for_create_mode=True)
    assert not is_valid
    assert message == "Missing or empty field: eligibility_criteria"

def test__neg_validate_scheme_data_invalid_data_type():
    scheme_data = {
        "name": "Health Scheme",
        "description": "A comprehensive health benefits scheme.",
        "eligibility_criteria": "age: 18+",  # Invalid type
        "benefits": {"coverage": "up to $10,000 per year"},
        "validity_start_date": datetime(2024, 1, 1)
    }
    is_valid, message = validate_scheme_data(scheme_data, for_create_mode=True)
    assert not is_valid
    assert message == "Invalid value for eligibility_criteria: must be a JSON object (dict)"

def test_validate_scheme_data_invalid_validity_start_date():
    scheme_data = {
        "name": "Health Scheme",
        "description": "A comprehensive health benefits scheme.",
        "eligibility_criteria": {"age": "18+", "income": "below $50,000"},
        "benefits": {"coverage": "up to $10,000 per year"},
        "validity_start_date": "2024-01-01"  # Invalid type
    }
    is_valid, message = validate_scheme_data(scheme_data, for_create_mode=True) # upgraded the validate_scheme_data function to auto convert a 'date' object to 'datetime'. Making it valid now.
    assert is_valid
    # assert message == "Invalid value for validity_start_date: must be a datetime object"

def test_validate_scheme_data_optional_fields():
    scheme_data = {
        "name": "Health Scheme",
        "description": "A comprehensive health benefits scheme.",
        "eligibility_criteria": {"age": "18+", "income": "below $50,000"},
        "benefits": {"coverage": "up to $10,000 per year"},
        "validity_start_date": datetime(2024, 1, 1)
    }
    is_valid, message = validate_scheme_data(scheme_data, for_create_mode=True)
    assert is_valid
    assert message == "All fields are valid"
    
    

def test_validate_scheme_data_update_valid():
    scheme_data = {
        "description": "Updated health benefits scheme."
    }
    is_valid, message = validate_scheme_data(scheme_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"

def test__neg_validate_scheme_data_update_invalid_field_type():
    scheme_data = {
        "eligibility_criteria": "age: 18+"  # Invalid type
    }
    is_valid, message = validate_scheme_data(scheme_data, for_create_mode=False)
    assert not is_valid
    assert message == "Invalid value for eligibility_criteria: must be a JSON object (dict)"

def test_validate_scheme_data_update_invalid_value():
    scheme_data = {
        "validity_start_date": "2024-01-01"  # Invalid type
    }
    is_valid, message = validate_scheme_data(scheme_data, for_create_mode=False) # auto convert date to datetime
    assert is_valid

def test_validate_scheme_data_update_partial_fields():
    scheme_data = {
        "name": "Updated Health Scheme"
    }
    is_valid, message = validate_scheme_data(scheme_data, for_create_mode=False)
    assert is_valid
    assert message == "All fields are valid"
