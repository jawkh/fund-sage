# Copyright (c) 2024 by Jonathan AW
# applicants.py

# api/routes/applicants.py

from flask import Blueprint, request, jsonify, g
from bl.services.applicant_service import ApplicantService
from marshmallow import ValidationError
from dal.crud_operations import CRUDOperations
from api.schemas.all_schemas import ApplicantSchema
from exceptions import InvalidPaginationParameterException, InvalidSortingParameterException
from sqlalchemy.exc import SQLAlchemyError

applicants_bp = Blueprint('applicants', __name__)

@applicants_bp.route('/api/applicants', methods=['GET'])
def get_applicants():
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    
    # Extract pagination and sorting parameters from the request
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    sort_by = request.args.get('sort_by', default='created_at', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)
    
    # Extract filter parameters from the request
    filters = {}
    if 'employment_status' in request.args:
        filters['employment_status'] = request.args['employment_status']
    if 'sex' in request.args:
        filters['sex'] = request.args['sex']
    if 'marital_status' in request.args:
        filters['marital_status'] = request.args['marital_status']
        
    try:
        # Retrieve applicants from the service with the specified parameters
        applicants, total_count = ApplicantService(crud_operations).get_all_applicants(
            page=page, 
            page_size=page_size, 
            sort_by=sort_by, 
            sort_order=sort_order,
            filters=filters
        )
        # Use Marshmallow schema to serialize the applicant objects
        applicant_schema = ApplicantSchema(many=True)
        result = applicant_schema.dump(applicants)
        
        # Prepare response with pagination metadata
        response = {
            'data': result,  
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
    except SQLAlchemyError as e:  # Specific SQLAlchemy error handling
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@applicants_bp.route('/api/applicants', methods=['POST'])
def create_applicant():
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    applicant_service = ApplicantService(crud_operations)
    try:
        data = request.json
        applicant_data = ApplicantSchema().load(data)
        applicant = applicant_service.create_applicant(data, data.get('household_members', []))
        return jsonify(applicant), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
