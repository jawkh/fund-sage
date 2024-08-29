

# Copyright (c) 2024 by Jonathan AW

""" 
Unit Testing of SchemeService:

Objective: Ensure that all functionalities within SchemeService are correctly implemented and working as expected. Since this service provides foundational support for scheme management, testing it first will establish a solid base for subsequent tests.

Key Tests to Include:
- CRUD operations for schemes.
- Filtering schemes based on validity.
- Interactions with eligibility logic for schemes.

"""
# test_scheme_service.py

import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound
from datetime import datetime
from bl.services.scheme_service import SchemeService
from exceptions import SchemeNotFoundException, InvalidSchemeDataException

# Positive Test Cases

def test_create_scheme(crud_operations):
    """
    Test creating a new scheme and verify the details.
    """
    scheme_data = {
    "name": "Senior Citizen Assistance Scheme",
    "description": "A scheme to provide financial support and benefits to individuals aged 65 and above.",
    "eligibility_criteria": {
        "age_threshold": 65
    },
    "benefits": {
        "cpf_top_up": {
            "disbursment_amount": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_months": None,
            "description": "One-time CPF top-up of $200."
        },
        "cdc_voucher": {
            "disbursment_amount": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_months": None,
            "description": "One-time CDC voucher of $200."
        }
    },
    "validity_start_date": datetime(2024, 1, 1),
    "validity_end_date": None
}
    scheme_service = SchemeService(crud_operations)
    new_scheme = scheme_service.create_scheme(scheme_data)
    
    assert new_scheme.name == scheme_data["name"]
    assert new_scheme.description == scheme_data["description"]
    assert new_scheme.eligibility_criteria == scheme_data["eligibility_criteria"]
    assert new_scheme.benefits == scheme_data["benefits"]

def test_get_scheme_by_id(crud_operations, test_scheme):
    """
    Test retrieving an existing scheme by ID and verify the details.
    """
    scheme_service = SchemeService(crud_operations)
    fetched_scheme = scheme_service.get_scheme_by_id(test_scheme.id)
    
    assert fetched_scheme is not None
    assert fetched_scheme.id == test_scheme.id
    assert fetched_scheme.name == test_scheme.name

def test_update_scheme(crud_operations, test_scheme):
    """
    Test updating a scheme's details.
    """
    update_data = {"name": "Updated Scheme Name"}
    scheme_service = SchemeService(crud_operations)
    updated_scheme = scheme_service.update_scheme(test_scheme.id, update_data)
    
    assert updated_scheme.name == "Updated Scheme Name"

def test_delete_scheme(crud_operations, test_scheme):
    """
    Test deleting a scheme record.
    """
    scheme_service = SchemeService(crud_operations)
    scheme_service.delete_scheme(test_scheme.id)
    
    with pytest.raises(SchemeNotFoundException):
        scheme_service.get_scheme_by_id(test_scheme.id)

def test_get_all_schemes(crud_operations, test_scheme):
    scheme_service = SchemeService(crud_operations)
    
    scheme_1_data = {
    "name": "Senior Citizen Assistance Scheme",
    "description": "A scheme to provide financial support and benefits to individuals aged 65 and above.",
    "eligibility_criteria": {
        "age_threshold": 65
    },
    "benefits": {
        "cpf_top_up": {
            "disbursment_amount": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_months": None,
            "description": "One-time CPF top-up of $200."
        },
        "cdc_voucher": {
            "disbursment_amount": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_months": None,
            "description": "One-time CDC voucher of $200."
        }
    },
    "validity_start_date": datetime(2027, 1, 1),
    "validity_end_date": None
}
    future_scheme = scheme_service.create_scheme(scheme_1_data)
    
    scheme_2_data = {
    "name": "Middle-aged Reskilling Assistance Scheme",
    "description": "A scheme to provide financial support and benefits to individuals aged 40 and above who are unemployed, encouraging reskilling and upskilling.",
    "eligibility_criteria": {
        "age_threshold": 40,
        "employment_status": "unemployed"
    },
    "benefits": {
        "skillsfuture_credit_top_up": {
            "disbursment_amount": 1000,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_months": None,
            "description": "One-time Skillsfuture Credit top-up of $1000."
        },
        "study_allowance": {
            "disbursment_amount": 2000,
            "disbursment_frequency": "Monthly",
            "disbursment_duration_months": 6,
            "description": "Monthly study allowance of $5000 for up to 6 months."
        }
    },
    "validity_start_date": datetime(2024, 1, 1),
    "validity_end_date": datetime(2024, 2, 1) # Valid for 1 month (expired scheme)
}
    
    expired_scheme = scheme_service.create_scheme(scheme_2_data)
    
    """
    Test retrieving all schemes and filtering for valid schemes.
    """
    scheme_service = SchemeService(crud_operations)
    schemes = scheme_service.get_all_schemes(fetch_valid_schemes=True)
    
    assert len(schemes) > 0
    assert any(scheme.id == test_scheme.id for scheme in schemes)
    assert not any(scheme.id == future_scheme.id for scheme in schemes) # future scheme should not be included
    assert not any(scheme.id == expired_scheme.id for scheme in schemes) # expired scheme should not be included

def test_get_schemes_by_filters(crud_operations, test_scheme):
    """
    Test retrieving schemes using specific filters.
    """
    scheme_service = SchemeService(crud_operations)
    schemes = scheme_service.get_schemes_by_filters({"name": test_scheme.name}, fetch_valid_schemes=True)
    
    assert len(schemes) > 0
    assert schemes[0].name == test_scheme.name

# Negative Test Cases

def test__neg_create_scheme_invalid_data(crud_operations):
    """
    Test creating a scheme with invalid data.
    """
    invalid_scheme_data = {
        "name": "",
        "description": "Invalid scheme with no name.",
        "eligibility_criteria": {"employment_status": "invalid"},
        "benefits": {"amount": -1000.0},
        "validity_start_date": "invalid-date",
        "validity_end_date": None
    }
    scheme_service = SchemeService(crud_operations)
    
    with pytest.raises(InvalidSchemeDataException):
        scheme_service.create_scheme(invalid_scheme_data)

def test__neg_get_scheme_by_invalid_id(crud_operations):
    """
    Test retrieving a scheme using a non-existent ID.
    """
    scheme_service = SchemeService(crud_operations)
    
    with pytest.raises(SchemeNotFoundException):
        scheme_service.get_scheme_by_id(999)  # Non-existent ID

def test__neg_update_non_existent_scheme(crud_operations):
    """
    Test updating a non-existent scheme.
    """
    scheme_service = SchemeService(crud_operations)
    
    with pytest.raises(SchemeNotFoundException):
        scheme_service.update_scheme(999, {"name": "Should not exist"})

def test__neg_delete_non_existent_scheme(crud_operations):
    """
    Test deleting a scheme that doesn't exist.
    """
    scheme_service = SchemeService(crud_operations)
    
    with pytest.raises(SchemeNotFoundException):
        scheme_service.delete_scheme(999)  # Non-existent ID

def test__neg_get_schemes_with_invalid_filters(crud_operations):
    """
    Test retrieving schemes with invalid filters.
    """
    scheme_service = SchemeService(crud_operations)
    schemes = scheme_service.get_schemes_by_filters({"invalid_field": "invalid_value"}, fetch_valid_schemes=True)
    
    assert len(schemes) == 0  # Expect no schemes to be returned
