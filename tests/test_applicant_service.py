
# Copyright (c) 2024 by Jonathan AW
""" 
Test cases for the Business Layer's ApplicantService class.
"""

import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound
from dal.models import Applicant
from datetime import datetime
from exceptions import ApplicantNotFoundException

# Test ApplicantService methods
def test_create_applicant(applicant_service, test_administrator):
    """
    Test creating a new applicant and verify the details.
    """
    applicant_data = {
        "name": "Jane Doe",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1985, 2, 15),
        "marital_status": "married",
        "created_by_admin_id": test_administrator.id
    }
    new_applicant = applicant_service.create_applicant(applicant_data)
    
    assert new_applicant.name == applicant_data["name"]
    assert new_applicant.employment_status == applicant_data["employment_status"]
    assert new_applicant.created_by_admin_id == test_administrator.id

def test_get_applicant_by_id(applicant_service, test_applicant):
    """
    Test retrieving an applicant by ID and verify the details.
    """
    fetched_applicant = applicant_service.get_applicant_by_id(test_applicant.id)
    
    assert fetched_applicant is not None
    assert fetched_applicant.name == test_applicant.name
    assert fetched_applicant.id == test_applicant.id

def test_update_applicant(applicant_service, test_applicant):
    """
    Test updating an applicant's information.
    """
    update_data = {"employment_status": "unemployed"}
    updated_applicant = applicant_service.update_applicant(test_applicant.id, update_data)
    
    assert updated_applicant.employment_status == "unemployed"


# Negative test cases
def test_get_applicant_by_invalid_id(applicant_service):
    """
    Test retrieving a non-existent applicant by ID.
    """
    with pytest.raises(ApplicantNotFoundException):
        applicant_service.get_applicant_by_id(999)  # Non-existent ID

def test_create_applicant_with_invalid_data(applicant_service):
    """
    Test creating an applicant with missing mandatory fields.
    """
    invalid_applicant_data = {
        "name": "",  # Name is required
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1985, 2, 15),
        "marital_status": "married",
        "created_by_admin_id": 999  # Non-existent admin ID
    }
    
    with pytest.raises(IntegrityError):
        applicant_service.create_applicant(invalid_applicant_data)
