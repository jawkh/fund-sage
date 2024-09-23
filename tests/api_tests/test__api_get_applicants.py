# Copyright (c) 2024 by Jonathan AW


import pytest
from sqlalchemy.exc import SQLAlchemyError
from tests.conftest import helper 

def test__api_get_applicants_success(api_test_client, api_test_admin):
    """
    Positive test: Verify that the API returns applicants with the correct pagination and sorting.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    response = api_test_client.get('/api/applicants?page=1&page_size=5&sort_by=created_at&sort_order=asc' ,headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # # Print the response for manual inspection
    # print("Test: test_get_applicants_success")
    # helper.print_response(response)

    assert response.status_code == 200
    assert 'data' in data
    assert 'pagination' in data
    assert isinstance(data['data'], list)
    assert 'current_page' in data['pagination']
    assert data['pagination']['current_page'] == 1
    assert data['pagination']['page_size'] == 5
    assert data['pagination']['total_pages'] >= 1  # Should be at least 1 if there are any applicants

def test__api_get_applicants_filter_by_employment_status(api_test_client, api_test_admin):
    """
    Positive test: Verify that the API correctly filters applicants by employment status.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    response = api_test_client.get('/api/applicants?employment_status=employed' ,headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # # Print the response for manual inspection
    # print("Test: test_get_applicants_filter_by_employment_status")
    # helper.print_response(response)
    
    assert response.status_code == 200
    assert 'data' in data
    for applicant in data['data']:
        assert applicant['employment_status'] == 'employed'

def test__api_get_applicants_invalid_page_size(api_test_client, api_test_admin):
    """
    Negative test: Verify that the API returns a 400 error for invalid page size.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    response = api_test_client.get('/api/applicants?page=1&page_size=-1' ,headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()
    
    # # Print the response for manual inspection
    # print("Test: test_get_applicants_filter_by_employment_status")
    # helper.print_response(response)

    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == "Page size must be greater than 0."

def test__api_get_applicants_invalid_sort_by(api_test_client, api_test_admin):
    """
    Negative test: Verify that the API returns a 400 error for an invalid sort_by field.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    response = api_test_client.get('/api/applicants?sort_by=invalid_field' ,headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # # Print the response for manual inspection
    # print("Test: test_get_applicants_invalid_sort_by")
    # helper.print_response(response)
    
    assert response.status_code == 400
    assert 'error' in data
    assert data['error'].startswith("Invalid sort_by field")


def test__api_get_applicants_invalid_pagination_parameter(api_test_client, api_test_admin):
    """
    Negative test: Verify that the API returns a 400 error for an invalid pagination parameter.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    response = api_test_client.get('/api/applicants?page=0&page_size=10' ,headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # # Print the response for manual inspection
    # print("Test: test_get_applicants_invalid_pagination_parameter")
    # helper.print_response(response)
    
    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == "Page number must be greater than 0."

def test__api_get_applicants_filter_by_multiple_criteria(api_test_client, api_test_admin):
    """
    Positive test: Verify that the API correctly filters applicants by multiple criteria.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    response = api_test_client.get('/api/applicants?employment_status=employed&sex=male&marital_status=single' ,headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # # Print the response for manual inspection
    # print("Test: test_get_applicants_filter_by_multiple_criteria")
    # helper.print_response(response)
    
    assert response.status_code == 200
    assert 'data' in data
    for applicant in data['data']:
        assert applicant['employment_status'] == 'employed'
        assert applicant['sex'] == 'male'
        assert applicant['marital_status'] == 'single'
