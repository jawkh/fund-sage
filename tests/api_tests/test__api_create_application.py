
# Copyright (c) 2024 by Jonathan AW


import pytest
from bl.services.application_service import ApplicationService
from tests.conftest import helper
from exceptions import InvalidApplicationDataException




# def test__api_create_application_success(api_test_client, api_test_admin, mocker):
#     """
#     Positive test: Verify that the API successfully creates an application.
#     """
#     # Step 1: Authenticate to get JWT token
#     access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

#     # Mocking the applicant object
#     mock_applicant = mocker.Mock(id=1, name="John Doe", date_of_birth="", marital_status="married", marriage_date="2010-01-01T00:00:00", employment_status="unemployed")
#     mocker.patch('bl.services.application_service.get_applicant_by_id', return_value=mock_applicant)

#     application_data = {
#         "applicant_id": 1,
#         "scheme_id": 1
#     }

    
    
#     response = api_test_client.post('/api/applications', json=application_data, headers={'Authorization': f'Bearer {access_token}'})
#     data = response.get_json()

#     # # Print the response for manual inspection
#     # print("Test: test_create_application_success")
#     # helper.print_response(response)

#     assert response.status_code == 201
#     assert 'id' in data['data']
#     assert data['data']['status'] == 'rejected'
#     assert "Not eligible: Marriage duration exceeds" in data['data']['eligibility_verdict']
#     assert data['data']['awarded_benefits'] == []
    
def test__api_create_application_missing_data(api_test_client, api_test_admin):
    """
    Negative test: Verify that the API returns a 400 error when required data is missing.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    # Missing applicant_id and scheme_id
    application_data = {}

    response = api_test_client.post('/api/applications', json=application_data, headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # # Print the response for manual inspection
    # print("Test: test_create_application_missing_data")
    # helper.print_response(response)

    assert response.status_code == 400

def test__api_create_application_already_approved(api_test_client, api_test_admin, mocker, retrenchment_assistance_scheme, test_applicant):
    """
    Negative test: Verify that the API prevents creating a duplicate application if one is already approved.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    # Mocking an existing approved application
    mocker.patch.object(ApplicationService, 'create_application', side_effect=InvalidApplicationDataException("Applicant has already successfully applied to this scheme."))

    application_data = {
        "applicant_id": test_applicant.id,
        "scheme_id": retrenchment_assistance_scheme.id
    }

    response = api_test_client.post('/api/applications', json=application_data, headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # # Print the response for manual inspection
    # print("Test: test_create_application_already_approved")
    # helper.print_response(response)

    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == "Applicant has already successfully applied to this scheme."

def test__api_create_application_invalid_applicant_id(api_test_client, api_test_admin, retrenchment_assistance_scheme):
    """
    Negative test: Verify that the API returns a 400 error when an invalid applicant ID is provided.
    """
    # Step 1: Authenticate to get JWT token
    access_token = helper.get_JWT_via_user_login(api_test_client, api_test_admin)

    application_data = {
        "applicant_id": 9999,  # Invalid applicant ID
        "scheme_id": retrenchment_assistance_scheme.id
    }

    response = api_test_client.post('/api/applications', json=application_data, headers={'Authorization': f'Bearer {access_token}'})
    data = response.get_json()

    # # Print the response for manual inspection
    # print("Test: test_create_application_invalid_applicant_id")
    # helper.print_response(response)

    assert response.status_code == 400
    assert 'error' in data

