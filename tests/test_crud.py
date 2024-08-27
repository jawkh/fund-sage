# Copyright (c) 2024 by Jonathan AW

import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound
from dal.models import Administrator, Applicant
from datetime import datetime

# Test CRUD operations for the Administrator model
@pytest.mark.usefixtures("setup_mock_data") # Ensure the mock data is set up before running the tests (test_admin gets id==1 first)
def test_get_administrator(crud_operations):
    """
    Test retrieving an administrator by ID and verify the details.
    """
    admin = crud_operations.get_administrator(1)
    assert admin is not None
    assert admin.username == "test_admin"
    

def test_create_administrator(crud_operations):
    """
    Test creating a new administrator and verify the administrator details.
    """
    admin = crud_operations.create_administrator(username="test_admin_2", password_hash="hashed_password")
    assert admin.username == "test_admin_2"
    assert admin.password_hash == "hashed_password"
    assert admin.role == "admin"

def test_update_administrator(crud_operations):
    """
    Test updating an administrator's details and verify the update.
    """
    updated_admin = crud_operations.update_administrator(2, {"username": "updated_admin"})
    assert updated_admin.username == "updated_admin"

    
def test_delete_administrator(crud_operations):
    crud_operations.delete_administrator(2)
    assert crud_operations.get_administrator(2) is None
    

@pytest.mark.usefixtures("setup_mock_data") 
def test_get_administrator_by_username(crud_operations):
    """
    Test retrieving an administrator by username.
    """
    admin = crud_operations.get_administrator_by_username("test_admin")
    assert admin is not None
    assert admin.username == "test_admin"


def test_get_administrators_by_filters(crud_operations):
    """
    Test retrieving administrators using filters.
    """
    crud_operations.create_administrator(username="admin_filter_test", password_hash="pass")
    admins = crud_operations.get_administrators_by_filters({"role": "admin"})
    assert len(admins) > 0
    assert any(admin.username == "admin_filter_test" for admin in admins)



# Test CRUD operations for the Applicant model
@pytest.mark.usefixtures("setup_mock_data") 
def test_create_applicant(crud_operations):
    """
    Test creating a new applicant and verify the applicant details.
    """
    applicant_data = {
        "name": "John Doe",
        "employment_status": "employed",
        "sex": "M",
        "date_of_birth": datetime(1990, 1, 1),
        "marital_status": "single",
        "created_by_admin_id": 1
    }
    applicant = crud_operations.create_applicant(applicant_data)
    assert applicant.name == "John Doe"
    assert applicant.employment_status == "employed"
    assert applicant.sex == "M"
    assert applicant.marital_status == "single"
    assert applicant.created_by_admin_id == 1   

def test_get_applicant(crud_operations):
    """
    Test retrieving an applicant by ID and verify the details.
    """
    applicant = crud_operations.get_applicant(1)
    assert applicant is not None
    assert applicant.name == "John Doe"
    assert applicant.employment_status == "employed"
    assert applicant.sex == "M"
    assert applicant.marital_status == "single"
    assert applicant.created_by_admin_id == 1   

def test_update_applicant(crud_operations):
    """
    Test updating an applicant's details and verify the update.
    """
    updated_applicant = crud_operations.update_applicant(1, {"name": "Jane Doe"})
    assert updated_applicant.name == "Jane Doe"
    assert updated_applicant.employment_status == "employed"
    assert updated_applicant.sex == "M"
    assert updated_applicant.marital_status == "single"
    assert updated_applicant.created_by_admin_id == 1 



def test_get_applicants_by_filters(crud_operations):
    """
    Test retrieving applicants using filters.
    """
    applicant_data = {
        "name": "Alice",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1995, 5, 15),
        "marital_status": "married",
        "created_by_admin_id": 1
    }
    crud_operations.create_applicant(applicant_data)
    applicants = crud_operations.get_applicants_by_filters({"employment_status": "unemployed"})
    assert len(applicants) > 0
    assert any(applicant.name == "Alice" for applicant in applicants)

# Enhanced tests for Application model
@pytest.mark.usefixtures("setup_mock_data") 
def test_create_application(crud_operations):
    """
    Test creating a new application and verify the application details,
    including the relationship with the administrator who created it.
    """
    applicant_data = {
        "name": "John Doe",
        "employment_status": "employed",
        "sex": "M",
        "date_of_birth": datetime(1990, 1, 1),
        "marital_status": "single",
        "created_by_admin_id": 1
    }
    applicant = crud_operations.create_applicant(applicant_data)

    application_data = {
        "applicant_id": applicant.id,
        "scheme_id": 1,  # Assume there is a valid scheme with ID 1
        "status": "pending",
        "created_by_admin_id": 1  # Link to the admin who created it
    }
    application = crud_operations.create_application(application_data)
    assert application.applicant_id == applicant.id
    assert application.scheme_id == 1
    assert application.status == "pending"
    assert application.created_by_admin_id == 1
    assert application.creator.username == "test_admin"  # Verify relationship to Administrator


def test_get_application(crud_operations):
    """
    Test retrieving an application by ID and verify the details,
    including the administrator who created it.
    """
    application = crud_operations.get_application(1)
    assert application is not None
    assert application.applicant_id is not None
    assert application.scheme_id == 1
    assert application.status == "pending"
    assert application.creator.username == "test_admin"  # Verify relationship to Administrator


def test_update_application(crud_operations):
    """
    Test updating an application's details and verify the update.
    """
    updated_application = crud_operations.update_application(1, {"status": "approved"})
    assert updated_application.status == "approved"
    

def test_delete_application(crud_operations):
    """
    Test deleting an application and verify it no longer exists.
    """
    crud_operations.delete_application(1)
    assert crud_operations.get_application(1) is None


# Tests for Scheme model
@pytest.mark.usefixtures("setup_mock_data") 
def test_get_scheme(crud_operations):
    """
    Test retrieving a scheme by ID and verify the details.
    """
    scheme = crud_operations.get_scheme(1)
    assert scheme is not None
    assert scheme.name == "Mock Scheme"
    

def test_create_scheme(crud_operations):
    """
    Test creating a new scheme and verify the scheme details.
    """
    scheme_data = {
        "name": "Test Scheme",
        "description": "Description for test scheme",
        "eligibility_criteria": {"employment_status": "unemployed"},
        "benefits": {"amount": 300.0},
        "validity_start_date": datetime(2023, 1, 1),
        "validity_end_date": None
    }
    scheme = crud_operations.create_scheme(scheme_data)
    assert scheme.name == "Test Scheme"
    assert scheme.description == "Description for test scheme"
    assert scheme.eligibility_criteria == {"employment_status": "unemployed"}


    
# Delete Operations shall be the final test cases for the CRUD operations (preserve referential integrity of preceding tests) 

def test_delete_applicant(crud_operations):
    """
    Test deleting an applicant and verify it no longer exists.
    """
    crud_operations.delete_applicant(1)
    assert crud_operations.get_applicant(1) is None

# Negative test cases for CRUD operations
def test_get_non_existent_application(crud_operations):
    """
    Negative test case: Try to retrieve a non-existent application by ID.
    """
    assert crud_operations.get_application(999) == None
        
def test_create_application_with_invalid_admin(crud_operations):
    """
    Negative test case: Try to create an application with a non-existent administrator ID.
    """
    applicant_data = {
        "name": "Jane Smith",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1985, 2, 15),
        "marital_status": "married",
        "created_by_admin_id": 1
    }
    applicant = crud_operations.create_applicant(applicant_data)

    application_data = {
        "applicant_id": applicant.id,
        "scheme_id": 1,
        "status": "pending",
        "created_by_admin_id": 999  # Non-existent admin ID
    }
    with pytest.raises(IntegrityError):
        crud_operations.create_application(application_data)

