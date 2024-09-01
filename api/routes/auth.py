# api/routes/auth.py

from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import create_access_token
from dal.crud_operations import CRUDOperations
from bl.services.administrator_service import AdministratorService
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """
    User login endpoint.
    Requires JSON payload with 'username' and 'password'.
    Returns a JWT access token if authentication is successful.
    """
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    administrator_service = AdministratorService(crud_operations)

    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing required parameters [username / password]'}), 400
    
    try:
        # Authenticate user
        admin, mesg = administrator_service.verify_login_credentials(username, password)
        if not admin:
            return jsonify({"error": mesg}), 401

        # Generate JWT token
        access_token = create_access_token(identity={'id': admin.id, 'username': admin.username})
        return jsonify(access_token=access_token), 200

    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
