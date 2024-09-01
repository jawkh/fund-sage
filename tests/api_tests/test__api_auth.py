
# Copyright (c) 2024 by Jonathan AW
# tests/test_auth.py

import pytest
import uuid
from flask_jwt_extended import create_access_token
from bl.services.administrator_service import AdministratorService
from dal.crud_operations import CRUDOperations

def test_login_success(test_client, test_db__NonTransactional):
    crud_operations = CRUDOperations(test_db__NonTransactional)
    AS = AdministratorService(crud_operations)
        
    try:
        username = str(uuid.uuid4())
        temp_admin = AS.create_administrator({'username': username, 'password_hash': 'Helloworld123!'}) # Create a temporary administrator record
        
        # Mock a successful login
        response = test_client.post('/api/auth/login', json={'username': temp_admin.username, 'password': 'Helloworld123!'})
        data = response.get_json()
        assert response.status_code == 200
        assert 'access_token' in data
    finally:
        AS.delete_administrator(temp_admin.id) # Clean up
        assert AS.get_administrator_by_id(temp_admin.id) is None   # Ensure the admin was deleted
    
    
def test_login_failure(test_client):
    # Mock a failed login
    response = test_client.post('/api/auth/login', json={'username': 'sa', 'password': 'wrong_password'})
    data = response.get_json()
    assert response.status_code == 401
    assert 'error' in data
    assert data['error'] == f"Invalid password. {AdministratorService.MAX_PASSWORD_RETRIES - 1} attempts remaining."

def test_protected_endpoint_without_token(test_client):
    # Attempt to access a protected endpoint without a token
    response = test_client.get('/api/applicants')
    data = response.get_json()
    assert response.status_code == 401
    assert 'msg' in data
    assert data['msg'] == "Missing Authorization Header"

def test_protected_endpoint_with_token(test_client):
    # Login to get a token
    response = test_client.post('/api/auth/login', json={'username': 'sa', 'password': 'sa__Pa55w0rd'})
    token = response.get_json().get('access_token')

    # Access a protected endpoint with the token
    response = test_client.get('/api/applicants', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
