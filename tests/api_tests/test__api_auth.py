# Copyright (c) 2024 by Jonathan AW
# tests/test_auth.py

import pytest
import uuid
from flask_jwt_extended import create_access_token
from bl.services.administrator_service import AdministratorService
from dal.crud_operations import CRUDOperations


def test_login_success(api_test_client, api_test_db__NonTransactional):
    crud_operations = CRUDOperations(api_test_db__NonTransactional)
    AS = AdministratorService(crud_operations)
        
    try:
        username = str(uuid.uuid4())
        temp_admin = AS.create_administrator({'username': username, 'password_hash': 'Helloworld123!'}) # Create a temporary administrator record
        
        # Mock a successful login
        response = api_test_client.post('/api/auth/login', json={'username': temp_admin.username, 'password': 'Helloworld123!'})
        data = response.get_json()
        assert response.status_code == 200
        assert 'access_token' in data
    finally:
        AS.delete_administrator(temp_admin.id) # Clean up
        assert AS.get_administrator_by_id(temp_admin.id) is None   # Ensure the admin was deleted
    
    
def test_login_failure(api_test_client, api_test_db__NonTransactional):
    crud_operations = CRUDOperations(api_test_db__NonTransactional)
    AS = AdministratorService(crud_operations)
    
    try:
        username = str(uuid.uuid4())
        temp_admin = AS.create_administrator({'username': username, 'password_hash': 'Helloworld123!'}) # Create a temporary administrator record
        
        response = api_test_client.post('/api/auth/login', json={'username': temp_admin.username, 'password': 'wrong_password'})
        data = response.get_json()
        assert response.status_code == 401
        assert 'error' in data
        assert data['error'] == f"Invalid password. {AdministratorService.MAX_PASSWORD_RETRIES - 1} attempts remaining."
    finally:
        AS.delete_administrator(temp_admin.id) # Clean up
        assert AS.get_administrator_by_id(temp_admin.id) is None   # Ensure the admin was deleted

def test_protected_endpoint_without_token(api_test_client):
    # Attempt to access a protected endpoint without a token
    response = api_test_client.get('/api/applicants')
    data = response.get_json()
    assert response.status_code == 401
    assert 'msg' in data
    assert data['msg'] == "Missing Authorization Header"

def test_protected_endpoint_with_token(api_test_client, api_test_db__NonTransactional):
    crud_operations = CRUDOperations(api_test_db__NonTransactional)
    AS = AdministratorService(crud_operations)
    
    try:
        username = str(uuid.uuid4())
        temp_admin = AS.create_administrator({'username': username, 'password_hash': 'Helloworld123!'}) # Create a temporary administrator record
 
        # Login to get a token
        response = api_test_client.post('/api/auth/login', json={'username': temp_admin.username, 'password': 'Helloworld123!'})
        token = response.get_json().get('access_token')

        # Access a protected endpoint with the token
        response = api_test_client.get('/api/applicants', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
    finally:
        AS.delete_administrator(temp_admin.id) # Clean up
        assert AS.get_administrator_by_id(temp_admin.id) is None   # Ensure the admin was deleted

# New tests for reset_admin_password function

def test_reset_admin_password_success(api_test_client, api_test_db__NonTransactional):
    crud_operations = CRUDOperations(api_test_db__NonTransactional)
    AS = AdministratorService(crud_operations)
    
    try:
        # Create two temporary administrator records
        admin1_username = str(uuid.uuid4())
        admin1 = AS.create_administrator({'username': admin1_username, 'password_hash': 'Helloworld123!'})
        
        admin2_username = str(uuid.uuid4())
        admin2 = AS.create_administrator({'username': admin2_username, 'password_hash': 'Helloworld123!'})
        
        # Login as admin1 to get a token
        response = api_test_client.post('/api/auth/login', json={'username': admin1_username, 'password': 'Helloworld123!'})
        token = response.get_json().get('access_token')
        
        # Reset password for admin2
        response = api_test_client.post('/api/auth/reset-admin-password', 
                                        json={'target_username': admin2_username},
                                        headers={'Authorization': f'Bearer {token}'})
        
        data = response.get_json()
        assert response.status_code == 200
        assert 'message' in data
        assert 'new_password' in data
        assert data['message'] == 'Password reset successful'
        
        # Verify that admin2 can log in with the new password
        new_password = data['new_password']
        response = api_test_client.post('/api/auth/login', json={'username': admin2_username, 'password': new_password})
        assert response.status_code == 200
        
    finally:
        AS.delete_administrator(admin1.id)
        AS.delete_administrator(admin2.id)
        assert AS.get_administrator_by_id(admin1.id) is None
        assert AS.get_administrator_by_id(admin2.id) is None

def test_reset_admin_password_without_auth(api_test_client, api_test_db__NonTransactional):
    crud_operations = CRUDOperations(api_test_db__NonTransactional)
    AS = AdministratorService(crud_operations)
    
    try:
        username = str(uuid.uuid4())
        temp_admin = AS.create_administrator({'username': username, 'password_hash': 'Helloworld123!'})
        
        # Attempt to reset password without authentication
        response = api_test_client.post('/api/auth/reset-admin-password', 
                                        json={'target_username': username})
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'msg' in data
        assert data['msg'] == "Missing Authorization Header"
        
    finally:
        AS.delete_administrator(temp_admin.id)
        assert AS.get_administrator_by_id(temp_admin.id) is None

def test_reset_admin_password_nonexistent_user(api_test_client, api_test_db__NonTransactional):
    crud_operations = CRUDOperations(api_test_db__NonTransactional)
    AS = AdministratorService(crud_operations)
    
    try:
        username = str(uuid.uuid4())
        temp_admin = AS.create_administrator({'username': username, 'password_hash': 'Helloworld123!'})
        
        # Login to get a token
        response = api_test_client.post('/api/auth/login', json={'username': username, 'password': 'Helloworld123!'})
        token = response.get_json().get('access_token')
        
        # Attempt to reset password for a non-existent user
        nonexistent_username = str(uuid.uuid4())
        response = api_test_client.post('/api/auth/reset-admin-password', 
                                        json={'target_username': nonexistent_username},
                                        headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert f"Administrator with Username {nonexistent_username} not found" in data['error']
        
    finally:
        AS.delete_administrator(temp_admin.id)
        assert AS.get_administrator_by_id(temp_admin.id) is None
