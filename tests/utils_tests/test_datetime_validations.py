import pytest
from datetime import datetime, timedelta
from utils.data_validation import (
    validate_administrator_data,
    validate_applicant_data,
    validate_household_member_data,
    validate_scheme_data,
    validate_application_data,
    validate_system_configuration_data,
)
from utils.date_utils import is_future_date

# Helper function to create a future datetime
def future_date():
    return datetime.now() + timedelta(days=1)

# Helper function to create a past datetime
def past_date():
    return datetime.now() - timedelta(days=1)

### Test Cases for is_future_date Function

def test_is_future_date_with_future_date():
    assert is_future_date(future_date()) == True

def test_is_future_date_with_past_date():
    assert is_future_date(past_date()) == False

def test_is_future_date_with_current_date():
    assert is_future_date(datetime.now()) == False

### Test Cases for validate_administrator_data Function

@pytest.mark.parametrize("admin_data, expected_result, expected_message", [
    ({"failed_login_starttime": future_date()}, False, "Invalid value for failed_login_starttime: must be a past date"),
    ({"failed_login_starttime": datetime.now()}, True, "All fields are valid"),
    ({"failed_login_starttime": None}, True, "All fields are valid"),
])
def test_validate_administrator_data_datetime(admin_data, expected_result, expected_message):
    result, message = validate_administrator_data(admin_data, for_create_mode=False)
    assert result == expected_result
    assert message == expected_message

### Test Cases for validate_applicant_data Function

@pytest.mark.parametrize("applicant_data, expected_result, expected_message", [
    ({"date_of_birth": future_date()}, False, "Invalid value for date_of_birth: must be a past date"),
    ({"date_of_birth": past_date()}, True, "All fields are valid"),
    ({"employment_status_change_date": future_date()}, False, "Invalid value for employment_status_change_date: must be a past date"),
    ({"employment_status_change_date": past_date()}, True, "All fields are valid"),
])
def test_validate_applicant_data_datetime(applicant_data, expected_result, expected_message):
    result, message = validate_applicant_data(applicant_data, for_create_mode=False)
    assert result == expected_result
    assert message == expected_message

### Test Cases for validate_household_member_data Function

@pytest.mark.parametrize("household_data, expected_result, expected_message", [
    ({"date_of_birth": future_date()}, False, "Invalid value for date_of_birth: must be a past date"),
    ({"date_of_birth": past_date()}, True, "All fields are valid"),
])
def test_validate_household_member_data_datetime(household_data, expected_result, expected_message):
    result, message = validate_household_member_data(household_data, for_create_mode=False)
    assert result == expected_result
    assert message == expected_message

### Test Cases for validate_scheme_data Function

@pytest.mark.parametrize("scheme_data, expected_result, expected_message", [
    ({"validity_start_date": future_date(), "validity_end_date": past_date()}, False, "Invalid value for validity_end_date: must be after validity_start_date"),
    ({"validity_start_date": past_date(), "validity_end_date": future_date()}, True, "All fields are valid"),
    ({"validity_start_date": past_date(), "validity_end_date": None}, True, "All fields are valid"),
])
def test_validate_scheme_data_datetime(scheme_data, expected_result, expected_message):
    result, message = validate_scheme_data(scheme_data, for_create_mode=False)
    assert result == expected_result
    assert message == expected_message

### Test Cases for validate_application_data Function

@pytest.mark.parametrize("application_data, expected_result, expected_message", [
    ({"submission_date": future_date()}, False, "Invalid value for submission_date: must be a past date"),
    ({"submission_date": past_date()}, True, "All fields are valid"),
])
def test_validate_application_data_datetime(application_data, expected_result, expected_message):
    result, message = validate_application_data(application_data, for_create_mode=False)
    assert result == expected_result
    assert message == expected_message

### Test Cases for validate_system_configuration_data Function

@pytest.mark.parametrize("config_data, expected_result, expected_message", [
    ({"last_updated": future_date()}, True, "All fields are valid"),
    ({"last_updated": past_date()}, True, "All fields are valid"),
    ({"last_updated": datetime.now()}, True, "All fields are valid"),
])
def test_validate_system_configuration_data_datetime(config_data, expected_result, expected_message):
    result, message = validate_system_configuration_data(config_data, for_create_mode=False)
    assert result == expected_result
    assert message == expected_message
