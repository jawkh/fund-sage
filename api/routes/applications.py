# Copyright (c) 2024 by Jonathan AW
# applications.py

# api/routes/applications.py

from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required
from bl.services.application_service import ApplicationService
from api.schemas.all_schemas import ApplicationSchema
from marshmallow import ValidationError
from dal.database import Base, engine, SessionLocal
from dal.crud_operations import CRUDOperations
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from exceptions import InvalidPaginationParameterException, InvalidSortingParameterException

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/api/applications', methods=['GET'])
@jwt_required()
def get_applications():
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    
    # Extract pagination and sorting parameters from the request
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    sort_by = request.args.get('sort_by', default='created_at', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)
    
    try: 
        applications, total_count = ApplicationService(crud_operations).get_all_applications(
            page=page, 
            page_size=page_size, 
            sort_by=sort_by, 
            sort_order=sort_order
        )
        
        # Use Marshmallow schema to serialize the application objects
        application_schema = ApplicationSchema(many=True)
        result = application_schema.dump(applications)
        
        # Prepare response with pagination metadata
        response = {
            'data': result,  # Serialized application objects
            'pagination': {
                'current_page': page,
                'page_size': page_size,
                'total_pages': (total_count // page_size) + (1 if total_count % page_size else 0),
                'total_count': total_count
            }
        }
        return jsonify(response), 200
    except InvalidPaginationParameterException as e:
        return jsonify({'error': str(e)}), 400
    except InvalidSortingParameterException as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@applications_bp.route('/api/applications', methods=['POST'])
@jwt_required()
def create_application():
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    appllication_service = ApplicationService(crud_operations)
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(session) 
    try:
        data = request.json
        application_data = ApplicationSchema().load(data)
        admin_id = request.headers.get('admin_id') # placeholder for admin_id
        application = appllication_service.create_application(data.get('applicant_id'), data.get('scheme_id'), admin_id, schemeEligibilityCheckerFactory)
        return jsonify(application), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

