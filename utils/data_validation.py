
# Copyright (c) 2024 by Jonathan AW

""" 
Purpose: Utility functions for validating data before processing in the Business Logic Layer (BL) services.

Design Pattern: Data Validation
- Each function validates a specific type of data (e.g., administrator, applicant, application, etc.)

"""

from datetime import datetime
from typing import Tuple
from utils.date_utils import is_future_date

def validate_administrator_data(administrator_data: dict, for_create_mode: bool) -> Tuple[bool, str]:
    """
    Validate administrator data to ensure all required fields are present and correctly formatted if for_create_mode is True. 
    In contrast, we do not need all the fields to be present for other types of queries like select, update or delete.
    Returns True if all fields are valid, False otherwise and provides a reason for failure.
    """
    # Required fields
    required_fields_for_create_mode = ['username', 'password_hash', 'salt']


    if (for_create_mode):
        # Check for missing or empty required fields
        for field in required_fields_for_create_mode:
            if field not in administrator_data or administrator_data[field] is None:
                return False, f"Missing or empty field: {field}"

    
    # Validate required fields
    if "username" in administrator_data and (not isinstance(administrator_data['username'], str) or not administrator_data['username'].strip()):
        return False, "Invalid value for username: must be a non-empty string"

    if "password_hash" in administrator_data and (not isinstance(administrator_data['password_hash'], str) or not administrator_data['password_hash'].strip()):
        return False, "Invalid value for password_hash: must be a non-empty string"

    if "salt" in administrator_data and (not isinstance(administrator_data['salt'], str) or not administrator_data['salt'].strip()):
        return False, "Invalid value for salt: must be a non-empty string"

    # Validate fields with default values
    if 'role' in administrator_data and not isinstance(administrator_data['role'], str):
        return False, "Invalid value for role: must be a string"
    # elif 'role' in administrator_data and administrator_data['role'] not in ['admin', 'user']:
    #     return False, "Invalid value for role: must be 'admin' or 'user'"

    if 'consecutive_failed_logins' in administrator_data and (
        not isinstance(administrator_data['consecutive_failed_logins'], int) or administrator_data['consecutive_failed_logins'] < 0
    ):
        return False, "Invalid value for consecutive_failed_logins: must be a non-negative integer"

    if 'account_locked' in administrator_data and not isinstance(administrator_data['account_locked'], bool):
        return False, "Invalid value for account_locked: must be a boolean"

    if 'failed_login_starttime' in administrator_data and administrator_data['failed_login_starttime'] is not None:
        if not isinstance(administrator_data['failed_login_starttime'], datetime):
            return False, "Invalid value for failed_login_starttime: must be a datetime object"
        elif is_future_date(administrator_data['failed_login_starttime']):
            return False, "Invalid value for failed_login_starttime: must be a past date"

    # If all checks pass
    return True, "All fields are valid"

    


def validate_applicant_data(applicant_data: dict, for_create_mode: bool) -> Tuple[bool, str]:
    """
    Validate applicant data to ensure all required fields are present and correctly formatted if for_create_mode is True. 
    For other operations, not all fields are required.
    
    Returns True if all fields are valid, False otherwise and provides a reason for failure.
    """
    # Required fields for creation
    required_fields_for_create_mode = ['name', 'employment_status', 'sex', 'date_of_birth', 'marital_status']

    # Check for missing or empty required fields when in creation mode
    if for_create_mode:
        for field in required_fields_for_create_mode:
            if field not in applicant_data or applicant_data[field] is None:
                return False, f"Missing or empty field: {field}"

    # Validate field types and values
    if "name" in applicant_data and (not isinstance(applicant_data['name'], str) or not applicant_data['name'].strip()):
        return False, "Invalid value for name: must be a non-empty string"
    
    if "employment_status" in applicant_data:
        if not isinstance(applicant_data['employment_status'], str) or applicant_data['employment_status'] not in ['employed', 'unemployed']:
            return False, "Invalid value for employment_status: must be 'employed' or 'unemployed'"

    if "sex" in applicant_data:
        if not isinstance(applicant_data['sex'], str) or applicant_data['sex'] not in ['M', 'F']:
            return False, "Invalid value for sex: must be 'M' or 'F'"
    
    if "date_of_birth" in applicant_data and not isinstance(applicant_data['date_of_birth'], datetime):
        return False, "Invalid value for date_of_birth: must be a datetime object"
    elif "date_of_birth" in applicant_data and is_future_date(applicant_data['date_of_birth']):
        return False, "Invalid value for date_of_birth: must be a past date"

    if "marital_status" in applicant_data:
        if not isinstance(applicant_data['marital_status'], str) or applicant_data['marital_status'] not in ['single', 'married', 'divorced', 'widowed']:
            return False, "Invalid value for marital_status: must be 'single', 'married', 'divorced', or 'widowed'"

    if 'employment_status_change_date' in applicant_data and applicant_data['employment_status_change_date'] is not None:
        if not isinstance(applicant_data['employment_status_change_date'], datetime):
            return False, "Invalid value for employment_status_change_date: must be a datetime object"
        elif 'employment_status_change_date' in applicant_data and is_future_date(applicant_data['employment_status_change_date']):
            return False, "Invalid value for employment_status_change_date: must be a past date"

    if 'created_by_admin_id' in applicant_data and applicant_data['created_by_admin_id'] is not None:
        if not isinstance(applicant_data['created_by_admin_id'], int):
            return False, "Invalid value for created_by_admin_id: must be an integer"

    # If all checks pass
    return True, "All fields are valid"

    

def validate_household_member_data(household_member_data: dict, for_create_mode: bool = True) -> Tuple[bool, str]:
    """
    Validate household member data to ensure all required fields are present and correctly formatted if for_create_mode is True. 
    For other operations, not all fields are required.
    
    Returns True if all fields are valid, False otherwise and provides a reason for failure.
    """
    # Required fields for creation
    required_fields_for_create_mode = ['name', 'relation', 'date_of_birth'] # Removing 'applicant_id' from here. We need to assign it in the service layer after the applicant record has been created.

    # Check for missing or empty required fields when in creation mode
    if for_create_mode:
        for field in required_fields_for_create_mode:
            if field not in household_member_data or household_member_data[field] is None:
                return False, f"Missing or empty field: {field}"

    # Validate field types and values
    if "applicant_id" in household_member_data and not isinstance(household_member_data['applicant_id'], int):
        return False, "Invalid value for applicant_id: must be an integer"

    if "name" in household_member_data and (not isinstance(household_member_data['name'], str) or not household_member_data['name'].strip()):
        return False, "Invalid value for name: must be a non-empty string"

    if "relation" in household_member_data:
        if not isinstance(household_member_data['relation'], str) or household_member_data['relation'] not in ['parent', 'child', 'spouse', 'sibling', 'other']:
            return False, "Invalid value for relation: must be 'parent', 'child', 'spouse', 'sibling', or 'other'"

    if "date_of_birth" in household_member_data and not isinstance(household_member_data['date_of_birth'], datetime):
        return False, "Invalid value for date_of_birth: must be a datetime object"
    elif "date_of_birth" in household_member_data and is_future_date(household_member_data['date_of_birth']):
        return False, "Invalid value for date_of_birth: must be a past date"

    if "employment_status" in household_member_data:
        if household_member_data['employment_status'] is not None and not isinstance(household_member_data['employment_status'], str):
            return False, "Invalid value for employment_status: must be a string or None"
        if household_member_data['employment_status'] not in [None, 'employed', 'unemployed']:
            return False, "Invalid value for employment_status: must be 'employed', 'unemployed', or None"

    if "sex" in household_member_data:
        if household_member_data['sex'] is not None and not isinstance(household_member_data['sex'], str):
            return False, "Invalid value for sex: must be a string or None"
        if household_member_data['sex'] not in [None, 'M', 'F']:
            return False, "Invalid value for sex: must be 'M', 'F', or None"

    # If all checks pass
    return True, "All fields are valid"


from datetime import datetime
from typing import Tuple
from sqlalchemy import JSON

def validate_scheme_data(scheme_data: dict, for_create_mode: bool = True) -> Tuple[bool, str]:
    """
    Validate scheme data to ensure all required fields are present and correctly formatted if for_create_mode is True. 
    For other operations, not all fields are required.
    
    Returns True if all fields are valid, False otherwise and provides a reason for failure.
    """
    # Required fields for creation
    required_fields_for_create_mode = [
        'name', 
        'description', 
        'eligibility_criteria', 
        'benefits', 
        'validity_start_date'
    ]

    # Check for missing or empty required fields when in creation mode
    if for_create_mode:
        for field in required_fields_for_create_mode:
            if field not in scheme_data or scheme_data[field] is None:
                return False, f"Missing or empty field: {field}"

    # Validate field types and values
    if "name" in scheme_data and (not isinstance(scheme_data['name'], str) or not scheme_data['name'].strip()):
        return False, "Invalid value for name: must be a non-empty string"
    
    if "description" in scheme_data and (not isinstance(scheme_data['description'], str) or not scheme_data['description'].strip()):
        return False, "Invalid value for description: must be a non-empty string"

    if "eligibility_criteria" in scheme_data and not isinstance(scheme_data['eligibility_criteria'], dict):
        return False, "Invalid value for eligibility_criteria: must be a JSON object (dict)"

    if "benefits" in scheme_data and not isinstance(scheme_data['benefits'], dict):
        return False, "Invalid value for benefits: must be a JSON object (dict)"

    if "validity_start_date" in scheme_data and not isinstance(scheme_data['validity_start_date'], datetime):
        return False, "Invalid value for validity_start_date: must be a datetime object"

    if "validity_end_date" in scheme_data:
        if scheme_data['validity_end_date'] is not None and not isinstance(scheme_data['validity_end_date'], datetime):
            return False, "Invalid value for validity_end_date: must be a datetime object or None"
        elif scheme_data['validity_end_date'] is not None and scheme_data['validity_end_date'] < scheme_data['validity_start_date']:
            return False, "Invalid value for validity_end_date: must be after validity_start_date"

    # If all checks pass
    return True, "All fields are valid"

from datetime import datetime
from typing import Tuple

def validate_application_data(application_data: dict, for_create_mode: bool = True) -> Tuple[bool, str]:
    """
    Validate application data to ensure all required fields are present and correctly formatted if for_create_mode is True. 
    For other operations, not all fields are required.
    
    Returns True if all fields are valid, False otherwise and provides a reason for failure.
    """
    # Required fields for creation
    required_fields_for_create_mode = [
        'applicant_id', 
        'scheme_id', 
        'status'
    ]

    # Check for missing or empty required fields when in creation mode
    if for_create_mode:
        for field in required_fields_for_create_mode:
            if field not in application_data or application_data[field] is None:
                return False, f"Missing or empty field: {field}"

    # Validate field types and values
    if "applicant_id" in application_data and not isinstance(application_data['applicant_id'], int):
        return False, "Invalid value for applicant_id: must be an integer"

    if "scheme_id" in application_data and not isinstance(application_data['scheme_id'], int):
        return False, "Invalid value for scheme_id: must be an integer"

    if "status" in application_data:
        if not isinstance(application_data['status'], str) or application_data['status'] not in ['pending', 'approved', 'rejected']:
            return False, "Invalid value for status: must be 'pending', 'approved', or 'rejected'"

    if "submission_date" in application_data and not isinstance(application_data['submission_date'], datetime):
        return False, "Invalid value for submission_date: must be a datetime object"
    elif "submission_date" in application_data and is_future_date(application_data['submission_date']):
        return False, "Invalid value for submission_date: must be a past date"

    if "created_by_admin_id" in application_data and application_data['created_by_admin_id'] is not None:
        if not isinstance(application_data['created_by_admin_id'], int):
            return False, "Invalid value for created_by_admin_id: must be an integer"

    # If all checks pass
    return True, "All fields are valid"


from datetime import datetime
from typing import Tuple

def validate_system_configuration_data(config_data: dict, for_create_mode: bool = True) -> Tuple[bool, str]:
    """
    Validate system configuration data to ensure all required fields are present and correctly formatted if for_create_mode is True. 
    For other operations, not all fields are required.
    
    Returns True if all fields are valid, False otherwise and provides a reason for failure.
    """
    # Required fields for creation
    required_fields_for_create_mode = ['key', 'value']

    # Check for missing or empty required fields when in creation mode
    if for_create_mode:
        for field in required_fields_for_create_mode:
            if field not in config_data or config_data[field] is None:
                return False, f"Missing or empty field: {field}"

    # Validate field types and values
    if "key" in config_data and (not isinstance(config_data['key'], str) or not config_data['key'].strip()):
        return False, "Invalid value for key: must be a non-empty string"

    if "value" in config_data and (not isinstance(config_data['value'], str) or not config_data['value'].strip()):
        return False, "Invalid value for value: must be a non-empty string"

    if "description" in config_data and config_data['description'] is not None:
        if not isinstance(config_data['description'], str):
            return False, "Invalid value for description: must be a string or None"

    if "last_updated" in config_data and not isinstance(config_data['last_updated'], datetime):
        return False, "Invalid value for last_updated: must be a datetime object"

    # If all checks pass
    return True, "All fields are valid"
