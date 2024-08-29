
# Copyright (c) 2024 by Jonathan AW
""" 
Test cases for the Business Layer's ApplicantService class.
"""

import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from dal.models import Applicant
from datetime import datetime
# from exceptions import InvalidDataException
from bl.services.applicant_service import ApplicantService
from exceptions import ApplicantNotFoundException, InvalidApplicantDataException

# Test ApplicantService methods
def test_create_applicant(crud_operations, test_administrator):
    """
    Test creating a new applicant and verify the details.
    """
    applicant_data = {
        "name": "Jane Doe",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1985, 2, 15),
        "marital_status": "married",
        "employment_status_change_date": datetime(2024, 2, 15), 
        "created_by_admin_id": test_administrator.id
    }
    applicant_service = ApplicantService(crud_operations)
    new_applicant = applicant_service.create_applicant(applicant_data)
    
    assert new_applicant.name == applicant_data["name"]
    assert new_applicant.employment_status == applicant_data["employment_status"]
    assert new_applicant.created_by_admin_id == test_administrator.id

def test_get_applicant_by_id(crud_operations, test_applicant):
    """
    Test retrieving an applicant by ID and verify the details.
    """
    applicant_service = ApplicantService(crud_operations)
    fetched_applicant = applicant_service.get_applicant_by_id(test_applicant.id)
    
    assert fetched_applicant is not None
    assert fetched_applicant.name == test_applicant.name
    assert fetched_applicant.id == test_applicant.id

def test_update_applicant(crud_operations, test_applicant):
    """
    Test updating an applicant's information.
    """
    update_data = {"name": "Jane Doe", "employment_status": "unemployed"}
    applicant_service = ApplicantService(crud_operations)
    updated_applicant = applicant_service.update_applicant(test_applicant.id, update_data)
    assert updated_applicant.name == "Jane Doe"
    assert updated_applicant.employment_status == "unemployed"

def test_delete_applicant(crud_operations, test_applicant):
    """
    Test deleting an applicant record.
    """
    applicant_service = ApplicantService(crud_operations)
    applicant_service.delete_applicant(test_applicant.id)

    # Verify the applicant no longer exists
    with pytest.raises(ApplicantNotFoundException):
        applicant_service.get_applicant_by_id(test_applicant.id)

# Negative test cases
def test__neg_get_applicant_by_invalid_id(crud_operations):
    """
    Test retrieving a non-existent applicant by ID.
    """
    applicant_service = ApplicantService(crud_operations)
    with pytest.raises(ApplicantNotFoundException):
        applicant_service.get_applicant_by_id(999)  # Non-existent ID


def test__neg_create_applicant_with_empty_name(crud_operations, test_administrator):
    """
    Test creating an applicant with missing mandatory fields.
    """
    invalid_applicant_data = {
        "name": "",  # Name is required
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1985, 2, 15),
        "marital_status": "married",
        "created_by_admin_id": test_administrator.id 
    }
    applicant_service = ApplicantService(crud_operations)
    
    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(invalid_applicant_data)
        
def test__neg_create_applicant_with_invalid_created_by_admin_id(crud_operations):
    """
    Test creating an applicant with missing mandatory fields.
    """
    invalid_applicant_data = {
        "name": "aa",  # Name is required
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1985, 2, 15),
        "marital_status": "married",
        "created_by_admin_id": 999  # Non-existent admin ID
    }
    applicant_service = ApplicantService(crud_operations)
    
    with pytest.raises(IntegrityError):
        applicant_service.create_applicant(invalid_applicant_data)
        
def test__neg_create_applicant_invalid_dob(crud_operations, test_administrator):
    """
    Test creating an applicant with invalid data.
    """
    applicant_service = ApplicantService(crud_operations)
    invalid_applicant_data = {
        "name": "me",  
        "employment_status": "employed",
        "sex": "F",  
        "date_of_birth": "1990-13-01",  # Invalid date format
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }

    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(invalid_applicant_data)
        
def test__neg_create_applicant_invalid_employment_status(crud_operations, test_administrator):
    """
    Test creating an applicant with invalid data.
    """
    applicant_service = ApplicantService(crud_operations)
    invalid_applicant_data = {
        "name": "",  # Invalid name
        "employment_status": "wild and free", # Invalid employment status
        "sex": "F",  # Invalid sex
        "date_of_birth": "1990-12-01",  
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }

    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(invalid_applicant_data)

def test__neg_create_applicant_invalid_sex(crud_operations, test_administrator):
    """
    Test creating an applicant with invalid data.
    """
    applicant_service = ApplicantService(crud_operations)
    invalid_applicant_data = {
        "name": "",  # Invalid name
        "employment_status": "employed",
        "sex": "X",  # Invalid sex
        "date_of_birth": "1990-12-01",  
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }

    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(invalid_applicant_data)
        
def test__neg_create_applicant_invalid_maritalstatus(crud_operations, test_administrator):
    """
    Test creating an applicant with invalid data.
    """
    applicant_service = ApplicantService(crud_operations)
    invalid_applicant_data = {
        "name": "",  # Invalid name
        "employment_status": "employed",
        "sex": "X",  # Invalid sex
        "date_of_birth": "1990-12-01",  
        "marital_status": "unknown", # Invalid marital status
        "created_by_admin_id": test_administrator.id
    }

    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(invalid_applicant_data)

def test__neg_update_non_existent_applicant(crud_operations):
    """
    Test updating a non-existent applicant.
    """
    applicant_service = ApplicantService(crud_operations)

    with pytest.raises(ApplicantNotFoundException):
        applicant_service.update_applicant(999, {"name": "Non Existent"})
        
def test__neg_delete_non_existent_applicant(crud_operations):
    """
    Test deleting a non-existent applicant.
    """
    applicant_service = ApplicantService(crud_operations)

    with pytest.raises(ApplicantNotFoundException):
        applicant_service.delete_applicant(999)