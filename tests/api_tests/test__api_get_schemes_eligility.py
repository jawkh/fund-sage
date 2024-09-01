
# Copyright (c) 2024 by Jonathan AW


import pytest
from tests.conftest import helper

# ====================== Tests for get_schemes Endpoint ======================

def test_api_get_schemes_success(api_test_client, api_test_admin):
    """
    Positive test: Verify that the API returns schemes with the correct pagination and filtering.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    # Step 2: Call the endpoint
    response = api_test_client.get('/api/schemes?page=1&per_page=5&fetch_valid_schemes=true', headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # Print the response for manual inspection
    print("Test: test_api_get_schemes_success")
    helper.print_response(response)

    assert response.status_code == 200
    assert 'data' in data
    assert 'pagination' in data
    assert isinstance(data['data'], list)
    assert 'current_page' in data['pagination']
    assert data['pagination']['current_page'] == 1
    assert data['pagination']['per_page'] == 5
    assert 'total_schemes' in data['pagination']

def test_api_get_schemes_invalid_page_parameter(api_test_client, api_test_admin):
    """
    Negative test: Verify that the API returns a 400 error for invalid page parameter.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    response = api_test_client.get('/api/schemes?page=-1&per_page=10', headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # Print the response for manual inspection
    print("Test: test_api_get_schemes_invalid_page_parameter")
    helper.print_response(response)

    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == "Page number must be greater than 0."



# ====================== Tests for get_eligible_schemes Endpoint ======================

def test_api_get_eligible_schemes_success(api_test_client, api_test_admin):
    """
    Positive test: Verify that the API returns eligible schemes for a valid applicant.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    # Assume the applicant ID 1 exists in the database
    applicant_id = 1
    response = api_test_client.get(f'/api/schemes/eligible?applicant={applicant_id}', headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # Print the response for manual inspection
    print("Test: test_api_get_eligible_schemes_success")
    helper.print_response(response)

    assert response.status_code == 200
    assert 'data' in data
    assert 'eligible_schemes' in data['data']
    assert 'eligibility_results' in data['data']
    assert isinstance(data['data']['eligible_schemes'], list)
    assert isinstance(data['data']['eligibility_results'], list)

def test_api_get_eligible_schemes_missing_applicant_id(api_test_client, api_test_admin):
    """
    Negative test: Verify that the API returns a 400 error if the applicant ID is missing.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    response = api_test_client.get('/api/schemes/eligible', headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # Print the response for manual inspection
    print("Test: test_api_get_eligible_schemes_missing_applicant_id")
    helper.print_response(response)

    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == "applicant id is required"

def test_api_get_eligible_schemes_invalid_applicant_id_format(api_test_client, api_test_admin):
    """
    Negative test: Verify that the API returns a 400 error for invalid applicant ID format.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    response = api_test_client.get('/api/schemes/eligible?applicant=invalid_id', headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # Print the response for manual inspection
    print("Test: test_api_get_eligible_schemes_invalid_applicant_id_format")
    helper.print_response(response)

    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == "Invalid applicant id format"

def test_api_get_eligible_schemes_applicant_not_found(api_test_client, api_test_admin):
    """
    Negative test: Verify that the API returns a 404 error if the applicant is not found.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    response = api_test_client.get('/api/schemes/eligible?applicant=9999', headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # Print the response for manual inspection
    print("Test: test_api_get_eligible_schemes_applicant_not_found")
    helper.print_response(response)

    assert response.status_code == 404
    assert 'error' in data
