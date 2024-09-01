# Copyright (c) 2024 by Jonathan AW


import pytest
from sqlalchemy.exc import SQLAlchemyError
from tests.conftest import helper 

def test_get_applications_success(test_client, create_temp_admin):
    """
    Positive test: Verify that the API returns applications with the correct pagination and sorting.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(test_client, create_temp_admin)
    
    response = test_client.get('/api/applications?page=1&page_size=5&sort_by=created_at&sort_order=asc',  
                            headers={'Authorization': f'Bearer {access_token}'}
                            )
    data = response.get_json()

    # Use the helper to print the response
    print("Test: test_get_applications_success")
    helper.print_response(response)

    assert response.status_code == 200
    assert 'data' in data
    assert 'pagination' in data
    assert isinstance(data['data'], list)
    assert 'current_page' in data['pagination']
    assert data['pagination']['current_page'] == 1
    assert data['pagination']['page_size'] == 5
    assert data['pagination']['total_pages'] >= 1  # Should be at least 1 if there are any applications

def test_get_applications_varied_parameters(test_client, create_temp_admin):
    """
    Positive test: Test the API’s behavior with different combinations of pagination and sorting parameters.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(test_client, create_temp_admin)

    response = test_client.get('/api/applications?page=2&page_size=3&sort_by=name&sort_order=desc', headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # Use the helper to print the response
    print("Test: test_get_applications_varied_parameters")
    helper.print_response(response)

    assert response.status_code == 200
    assert 'data' in data
    assert 'pagination' in data
    assert isinstance(data['data'], list)
    assert 'current_page' in data['pagination']
    assert data['pagination']['current_page'] == 2
    assert data['pagination']['page_size'] == 3
    assert data['pagination']['total_pages'] >= 1

def test_get_applications_invalid_page_size(test_client, create_temp_admin):
    """
    Negative test: Verify that the API returns a 400 error for an invalid page size.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(test_client, create_temp_admin)

    response = test_client.get('/api/applications?page=1&page_size=-1', headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # Use the helper to print the response
    print("Test: test_get_applications_invalid_page_size")
    helper.print_response(response)

    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == "Page size must be greater than 0."

def test_get_applications_invalid_sort_by(test_client, create_temp_admin):
    """
    Negative test: Verify that the API returns a 400 error for an invalid sort_by field.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(test_client, create_temp_admin)
    response = test_client.get('/api/applications?sort_by=invalid_field' ,headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # Use the helper to print the response
    print("Test: test_get_applications_invalid_sort_by")
    helper.print_response(response)

    assert response.status_code == 400
    assert 'error' in data
    assert data['error'].startswith("Invalid sort_by field")

def test_get_applications_sqlalchemy_error(test_client, create_temp_admin, mocker):
    """
    Negative test: Simulate a SQLAlchemy error and verify that the API returns a 500 error.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(test_client, create_temp_admin)

    # Mock the get_all_applications method to raise an SQLAlchemyError
    mocker.patch('bl.services.application_service.ApplicationService.get_all_applications', side_effect=SQLAlchemyError("Database error occurred"))

    response = test_client.get('/api/applications' ,headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # Use the helper to print the response
    print("Test: test_get_applications_sqlalchemy_error")
    helper.print_response(response)

    assert response.status_code == 500
    assert 'error' in data
    assert data['error'] == "An unexpected error occurred"

