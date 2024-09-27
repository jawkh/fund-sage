# api/routes/auth.py

from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from dal.crud_operations import CRUDOperations
from bl.services.administrator_service import AdministratorService
from sqlalchemy.exc import SQLAlchemyError
from exceptions import AdministratorNotFoundException, InvalidAdministratorDataException

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

@auth_bp.route('/api/auth/reset-admin-password', methods=['POST'])
@jwt_required()
def reset_admin_password():
    """
    Reset password endpoint for another Administrator account.
    Requires authentication via JWT.
    Expects JSON payload with 'target_username'.
    Returns the new generated password.
    """
    session = g.db_session
    crud_operations = CRUDOperations(session)
    administrator_service = AdministratorService(crud_operations)

    data = request.json
    target_username = data.get('target_username')

    if not target_username:
        return jsonify({'error': 'Missing required parameter [target_username]'}), 400

    try:
        current_user = get_jwt_identity()
        admin_id = current_user['id']

        new_password = administrator_service.reset_admin_password(admin_id, target_username)

        return jsonify({'message': 'Password reset successful', 'new_password': new_password}), 200

    except AdministratorNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except InvalidAdministratorDataException as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
