# Copyright (c) 2024 by Jonathan AW
# test_administrator_service.py

""" 
Description: Tests for the AdministratorService class, covering functionalities related to administrator management, including CRUD operations and account security features (e.g., password verification, account locking/unlocking).
Priority: High (foundational service, essential for system security)
"""

import pytest
from bl.services.administrator_service import AdministratorService
from exceptions import AdministratorNotFoundException
from sqlalchemy.exc import IntegrityError


# Tests for CRUD operations in AdministratorService

def test_create_administrator(crud_operations):
    """
    Test creating a new administrator and verify the administrator details.
    """
    admin_service = AdministratorService(crud_operations)
    admin_data = {
        "username": "test_admin",
        "password_hash": "my_password"
    }

    # Create the administrator
    new_admin = admin_service.create_administrator(admin_data)

    # Verify the details of the created administrator
    assert new_admin.username == "test_admin"
    assert new_admin.role == "admin"

def test_get_administrator_by_id(crud_operations, test_administrator):
    """
    Test retrieving an administrator by ID.
    """
    admin_service = AdministratorService(crud_operations)
    admin = admin_service.get_administrator_by_id(test_administrator.id)

    assert admin is not None
    assert admin.username == test_administrator.username

def test_get_administrator_by_username(crud_operations, test_administrator):
    """
    Test retrieving an administrator by username.
    """
    admin_service = AdministratorService(crud_operations)
    admin = admin_service.get_administrator_by_username(test_administrator.username)

    assert admin is not None
    assert admin.username == test_administrator.username

def test_update_administrator(crud_operations, test_administrator):
    """
    Test updating an administrator's details.
    """
    admin_service = AdministratorService(crud_operations)
    updated_admin = admin_service.update_administrator(test_administrator.id, {"username": "updated_admin"})

    assert updated_admin.username == "updated_admin"

def test_delete_administrator(crud_operations, test_administrator):
    """
    Test deleting an administrator record.
    """
    admin_service = AdministratorService(crud_operations)
    admin_service.delete_administrator(test_administrator.id)

    # Verify the administrator no longer exists
    # with pytest.raises(AdministratorNotFoundException):
    assert admin_service.get_administrator_by_id(test_administrator.id) is None

# Tests for security-related methods in AdministratorService

@pytest.mark.parametrize (
    "created_username, password, login_username, login_password", 
    [("admin1", "  password1", " admin1 ", "password1"), 
    ("  ADMIN2", "password2  ", "Admin2", "  password2"), 
    ("admin3  ", "password3 ", " ADMIN3 ", "  password3  ")])
def test_verify_login_credentials_success(crud_operations, created_username, password, login_username, login_password):
    """
    Test successful verification of login credentials.
    """
    admin_service = AdministratorService(crud_operations)
    correct_password = "correct_password"
    new_admin = admin_service.create_administrator({"username": created_username, "password_hash": password})

    verified_new_admin, mesg = admin_service.verify_login_credentials(login_username, password) # Verifying the conditions: username is case-insensitive and will be auto stripped of leading/trailing whitespaces
    assert verified_new_admin is not None
    assert verified_new_admin.username == new_admin.username
    assert mesg == f"Welcome [{new_admin.username}]!"

def test__neg_verify_login_credentials_failure(crud_operations):
    """
    Test failed verification of login credentials.
    """
    admin_service = AdministratorService(crud_operations)
    admin_service.create_administrator({"username": "admin_fail", "password_hash": "my_password"})

    admin, mesg = admin_service.verify_login_credentials("admin_fail", "wrong_password")
    assert admin is None
    assert mesg == f"Invalid password. {AdministratorService.MAX_PASSWORD_RETRIES - 1} attempts remaining."

def test_lock_and_unlock_administrator_account(crud_operations):
    """
    Test locking an administrator's account after too many failed login attempts.
    """
    admin_service = AdministratorService(crud_operations)
    new_admin = admin_service.create_administrator({"username": "new_admin", "password_hash": "my_password"})
    # Lock the account after too many failed attempts
    for _ in range(AdministratorService.MAX_PASSWORD_RETRIES + 1):
        a, mesg =  admin_service.verify_login_credentials(new_admin.username, "wrong_password")

    # Ensure the account is locked
    assert mesg == "Account is locked. Please contact the administrator."
    locked_admin = admin_service.get_administrator_by_id(new_admin.id)
    assert locked_admin.account_locked

    # Unlock the account
    admin_service.unlock_administrator_account(new_admin.id)

    unlocked_admin = admin_service.get_administrator_by_id(new_admin.id)
    assert not unlocked_admin.account_locked

    
# def test_increment_login_failure_counter(crud_operations, test_administrator):
#     """
#     Test incrementing the login failure counter and locking the account after reaching the maximum retries.
#     """
#     admin_service = AdministratorService(crud_operations)

#     # Increment the failure counter
#     for _ in range(AdministratorService.MAX_PASSWORD_RETRIES):
#         admin_service.__increment_login_failure_counter(test_administrator.id)

#     # Ensure the account is locked
#     admin = admin_service.get_administrator_by_id(test_administrator.id)
#     assert admin.account_locked
#     assert admin.consecutive_failed_logins == AdministratorService.MAX_PASSWORD_RETRIES

def test_reset_login_failure_counters(crud_operations, test_administrator):
    """
    Test resetting login failure counters after successful login.
    """
    admin_service = AdministratorService(crud_operations)

    # Increment failure counters
    admin_service.verify_login_credentials(test_administrator.username, "wrong_password")
    admin_service.verify_login_credentials(test_administrator.username, "wrong_password")

    # Reset counters after a successful login
    admin_service.reset_login_failure_counters(test_administrator.id)

    admin = admin_service.get_administrator_by_id(test_administrator.id)
    assert admin.consecutive_failed_logins == 0
    assert admin.failed_login_starttime is None

def test__neg_repeated_failed_logins_until_account_is_locked(crud_operations, test_administrator):
    """
    Test repeated failed login attempts until the account is locked.
    """
    admin_service = AdministratorService(crud_operations)
    for _ in range(AdministratorService.MAX_PASSWORD_RETRIES):
        admin_service.verify_login_credentials(test_administrator.username, "wrong_password")

    locked_admin = admin_service.get_administrator_by_id(test_administrator.id)
    assert locked_admin.account_locked

def test__neg_repeated_failed_logins_successful_login_on_final_chance(crud_operations, test_administrator):
    """
    Test multiple failed logins followed by a successful login on the final allowed attempt.
    """
    admin_service = AdministratorService(crud_operations)
    correct_password = "correct_password"
    new_admin = admin_service.create_administrator({"username": "admin_test", "password_hash": correct_password})
    # Simulate failed login attempts
    for _ in range(AdministratorService.MAX_PASSWORD_RETRIES - 1):
        admin_service.verify_login_credentials(new_admin.username, "wrong_password")

    # Attempt successful login on the final chance
    admin, mesg = admin_service.verify_login_credentials(new_admin.username, correct_password)
    assert admin is not None
    assert admin.username == new_admin.username
    assert mesg == f"Welcome [{new_admin.username}]!"

    # Ensure the account is not locked
    admin = admin_service.get_administrator_by_id(new_admin.id)
    assert not admin.account_locked
    assert admin.consecutive_failed_logins == 0

# Negative Test Cases

def test__neg_failed_create_administrator_due_to_username_conflict(crud_operations, test_administrator):
    """
    Test creating an administrator with a username that already exists.
    """
    admin_service = AdministratorService(crud_operations)
    admin_data = {
        "username": test_administrator.username,  # Duplicate username
        "password_hash": "my_password"
    }

    with pytest.raises(IntegrityError):
        admin_service.create_administrator(admin_data)

