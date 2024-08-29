# Copyright (c) 2024 by Jonathan AW
# test_crud.py
""" 
Test Data Access Layer CRUD operations for the Administrator, Applicant, Scheme and Application models.
"""
import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound
from dal.models import Administrator, Applicant
from datetime import datetime

# Test CRUD operations for the Administrator model
def test_get_administrator(crud_operations, test_administrator):
    """
    Test retrieving an administrator by ID and verify the details.
    """
    admin = crud_operations.get_administrator(test_administrator.id)
    assert admin is not None
    assert admin.username == test_administrator.username
    

def test_create_administrator(crud_operations):
    """
    Test creating a new administrator and verify the administrator details.
    """
    admin = crud_operations.create_administrator(username="test_admin_2", password_hash="hashed_password", salt="salt")
    assert admin.username == "test_admin_2"
    assert admin.password_hash == "hashed_password"
    assert admin.role == "admin"

def test_update_administrator(crud_operations, test_administrator):
    """
    Test updating an administrator's details and verify the update.
    """
    updated_admin = crud_operations.update_administrator(test_administrator.id, {"username": "updated_admin"})
    assert updated_admin.username == "updated_admin"

    
def test_delete_administrator(crud_operations, test_administrator):
    crud_operations.delete_administrator(test_administrator.id)
    assert crud_operations.get_administrator(test_administrator.id) is None
    

def test_get_administrator_by_username(crud_operations, test_administrator):
    """
    Test retrieving an administrator by username.
    """
    admin = crud_operations.get_administrator_by_username(test_administrator.username)
    assert admin is not None
    assert admin.username == test_administrator.username


def test_get_administrators_by_filters(crud_operations):
    """
    Test retrieving administrators using filters.
    """
    crud_operations.create_administrator(username="admin_filter_test", password_hash="pass", salt="salt")
    admins = crud_operations.get_administrators_by_filters({"role": "admin"})
    assert len(admins) > 0
    assert any(admin.username == "admin_filter_test" for admin in admins)



# Test CRUD operations for the Applicant model
def test_create_applicant(crud_operations, test_administrator):
    """
    Test creating a new applicant and verify the applicant details.
    """
    applicant_data = {
        "name": "John Doe",
        "employment_status": "employed",
        "sex": "M",
        "date_of_birth": datetime(1990, 1, 1),
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }
    applicant = crud_operations.create_applicant(applicant_data)
    assert applicant.name == "John Doe"
    assert applicant.employment_status == "employed"
    assert applicant.sex == "M"
    assert applicant.marital_status == "single"
    assert applicant.created_by_admin_id == test_administrator.id   


def test_get_applicant(crud_operations, test_applicant):
    """
    Test retrieving an applicant by ID and verify the details.
    """
    applicant = crud_operations.get_applicant(test_applicant.id)
    assert applicant is not None
    assert applicant.name == test_applicant.name
    assert applicant.employment_status == test_applicant.employment_status
    assert applicant.sex == test_applicant.sex
    assert applicant.marital_status == test_applicant.marital_status
    assert applicant.created_by_admin_id == test_applicant.created_by_admin_id   


def test_update_applicant(crud_operations, test_applicant):
    """
    Test updating an applicant's details and verify the update.
    """
    updated_applicant = crud_operations.update_applicant(test_applicant.id, {"name": "Jane Doe"})
    updated_applicant_from_db = crud_operations.get_applicant(test_applicant.id)
    assert updated_applicant.name == updated_applicant_from_db.name
    assert updated_applicant.employment_status == updated_applicant_from_db.employment_status
    assert updated_applicant.sex == updated_applicant_from_db.sex
    assert updated_applicant.marital_status == updated_applicant_from_db.marital_status
    assert updated_applicant.created_by_admin_id == updated_applicant_from_db.created_by_admin_id


def test_get_applicants_by_filters(crud_operations, test_administrator):
    """
    Test retrieving applicants using filters.
    """
    applicant_data = {
        "name": "Alice",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1995, 5, 15),
        "marital_status": "married",
        "created_by_admin_id": test_administrator.id
    }
    crud_operations.create_applicant(applicant_data)
    applicants = crud_operations.get_applicants_by_filters({"employment_status": "unemployed"})
    assert len(applicants) > 0
    assert any(applicant.name == "Alice" for applicant in applicants)

def test_create_update_application(crud_operations, test_applicant, retrenchment_assistance_scheme):
    """
    Test creating a new application and verify the application details,
    including the relationship with the administrator who created it.
    """
    application_data = {
        "applicant_id": test_applicant.id,
        "scheme_id": retrenchment_assistance_scheme.id,  # Assume there is a valid scheme with ID 1
        "status": "pending",
        "created_by_admin_id": test_applicant.created_by_admin_id  # Link to the admin who created it
    }
    new_application = crud_operations.create_application(application_data)
    new_application_from_db = crud_operations.get_application(new_application.id)
    assert new_application.applicant_id == new_application_from_db.applicant_id
    assert new_application.scheme_id == new_application_from_db.scheme_id
    assert new_application.status == new_application_from_db.status
    assert new_application.created_by_admin_id == new_application_from_db.created_by_admin_id
    assert new_application.creator.username == new_application_from_db.creator.username  

    approved_application = crud_operations.update_application(new_application.id, {"status": "approved"})
    approved_application_from_db = crud_operations.get_application(approved_application.id)
    assert approved_application_from_db.status == "approved"
    


def test_delete_application(crud_operations, test_application):
    """
    Test deleting an application and verify it no longer exists.
    """
    crud_operations.delete_application(test_application.id)
    assert crud_operations.get_application(test_application.id) is None


# Tests for Scheme model
def test_get_scheme(crud_operations, retrenchment_assistance_scheme):
    """
    Test retrieving a scheme by ID and verify the details.
    """
    scheme = crud_operations.get_scheme(retrenchment_assistance_scheme.id)
    assert scheme is not None
    assert scheme.name == retrenchment_assistance_scheme.name
    

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

def test_delete_applicant(crud_operations, test_applicant):
    """
    Test deleting an applicant and verify it no longer exists.
    """
    crud_operations.delete_applicant(test_applicant.id)
    assert crud_operations.get_applicant(test_applicant.id) is None
    

# Negative test cases for CRUD operations
def test__neg_get_non_existent_application(crud_operations):
    """
    Negative test case: Try to retrieve a non-existent application by ID.
    """
    assert crud_operations.get_application(999) == None
        

def test__neg_create_application_with_invalid_admin(crud_operations, test_applicant, retrenchment_assistance_scheme):
    """
    Negative test case: Try to create an application with a non-existent administrator ID.
    """
    application_data = {
        "applicant_id": test_applicant.id,
        "scheme_id": retrenchment_assistance_scheme.id,
        "status": "pending",
        "created_by_admin_id": 999  # Non-existent admin ID
    }
    with pytest.raises(IntegrityError):
        crud_operations.create_application(application_data)

