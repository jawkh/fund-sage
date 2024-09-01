# Copyright (c) 2024 by Jonathan AW

import pytest
from bl.services.applicant_service import ApplicantService
from dal.crud_operations import CRUDOperations
from exceptions import ApplicantNotFoundException
from tests.conftest import helper

def test__api_create_applicant_success(api_test_client, api_test_db__NonTransactional, api_test_admin):
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)
    
    # Step 2: Prepare applicant data
    applicant_data = {
        "name": "John Doe",
        "employment_status": "unemployed",
        "sex": "M",
        "date_of_birth": "1985-01-15T00:00:00",
        "marital_status": "single",
        "employment_status_change_date": None,
        "household_members": [
            {"name": "Child One", "relation": "child", "date_of_birth": "2010-04-10T00:00:00", "employment_status": "unemployed", "sex": "F"},
            {"name": "Parent One", "relation": "parent", "date_of_birth": "1950-05-20T00:00:00", "employment_status": "unemployed", "sex": "M"}
        ]
    }

    # Step 3: Send POST request to create applicant with JWT token in header
    response = api_test_client.post(
        '/api/applicants',  # Direct URL path used here
        json=applicant_data,
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 201  # Expect a 201 Created status
    data = response.get_json()
    assert 'id' in data
    assert data['name'] == applicant_data['name']
    assert len(data['household_members']) == len(applicant_data['household_members'])
    
    # Cleanup: Remove the created applicant
    crud_operations = CRUDOperations(api_test_db__NonTransactional)
    applicant_service = ApplicantService(crud_operations)
    applicant_service.delete_applicant(data['id'])
    with pytest.raises(ApplicantNotFoundException):
        applicant_service.get_applicant_by_id(data['id']) is None



def test__api_create_applicant_missing_data(api_test_client, api_test_admin):
    """
    Test creating an applicant with missing required fields to trigger validation errors.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)
    
    # Step 2: Prepare Applicant data with missing required fields
    applicant_data = {
        "name": "",
        "employment_status": "unemployed"
        # Missing other required fields like sex, date_of_birth, marital_status
    }

    # Step 3: Send POST request to create applicant with JWT token in header
    response = api_test_client.post(
        '/api/applicants',  # Direct URL path used here
        json=applicant_data,
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 400  # Expect a 400 Bad Request status
    data = response.get_json()
    assert 'errors' in data


def test__api_create_applicant_unauthorized(api_test_client):
    """
    Test creating an applicant without JWT token to trigger unauthorized access.
    """
    # Step 1: Prepare Applicant data with all required fields
    applicant_data = {
        "name": "Jane Doe",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": "1980-01-01T00:00:00",
        "marital_status": "married",
        "employment_status_change_date": None,
        "household_members": []
    }

    # Step 2: Send POST request to create applicant with JWT token in header
    response = api_test_client.post(
        '/api/applicants',  # Direct URL path used here
        json=applicant_data
    )

    assert response.status_code == 401  # Expect a 401 Unauthorized status
    data = response.get_json()
    assert 'msg' in data
    assert data['msg'] == "Missing Authorization Header"


def test__api_create_applicant_invalid_household_member_data(api_test_client, api_test_admin):
    """
    Test creating an applicant with invalid household member data.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)
    
    # Step 2: Applicant data with invalid household member relation
    applicant_data = {
        "name": "Michael Smith",
        "employment_status": "employed",
        "sex": "M",
        "date_of_birth": "1990-02-20T00:00:00",
        "marital_status": "divorced",
        "employment_status_change_date": None,
        "household_members": [
            {"name": "Child One", "relation": "unknown_relation", "date_of_birth": "2015-04-10T00:00:00", "employment_status": "unemployed", "sex": "F"}
        ]
    }

    # Step 3: Send POST request to create applicant with JWT token in header
    response = api_test_client.post(
        '/api/applicants',  # Direct URL path used here
        json=applicant_data,
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 400  # Expect a 400 Bad Request status due to invalid relation type
    data = response.get_json()
    assert 'errors' in data
