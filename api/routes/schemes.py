# Copyright (c) 2024 by Jonathan AW

# api/routes/schemes.py

from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required
from bl.services.scheme_service import SchemeService
from api.schemas.all_schemas import SchemeSchema
# from marshmallow import ValidationError
from dal.crud_operations import CRUDOperations
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager
from bl.services.applicant_service import ApplicantService
from sqlalchemy.exc import SQLAlchemyError

schemes_bp = Blueprint('schemes', __name__)

@schemes_bp.route('/api/schemes', methods=['GET'])
@jwt_required()
def get_schemes():
    """
    Endpoint to retrieve all schemes with optional filtering for valid schemes.
    Implements pagination, filtering, and a flag to fetch only valid schemes.
    """
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    scheme_service = SchemeService(crud_operations)

    try:
        # Optional: Handle pagination parameters
        page = request.args.get('page', type=int, default=1)
        per_page = request.args.get('per_page', type=int, default=10)

        # Optional: Handle 'fetch_valid_schemes' parameter
        fetch_valid_schemes = request.args.get('fetch_valid_schemes', 'true').lower() == 'true'

        # Optional: Handle additional filtering parameters if needed
        filters = {}  # Initialize an empty dictionary to hold filters
        if 'validity_start_date' in request.args:
            filters['validity_start_date'] = request.args['validity_start_date']
        if 'validity_end_date' in request.args:
            filters['validity_end_date'] = request.args['validity_end_date']

        # Retrieve schemes with optional filters and 'fetch_valid_schemes' flag
        schemes = scheme_service.get_schemes_by_filters(filters, fetch_valid_schemes=fetch_valid_schemes)
        paginated_schemes = schemes[(page - 1) * per_page: page * per_page]  # Apply pagination

        # Serialize the scheme objects using Marshmallow schema
        scheme_schema = SchemeSchema(many=True)
        result = scheme_schema.dump(paginated_schemes)

        response = {
            'data': result,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_schemes': len(schemes),
                'total_pages': (len(schemes) + per_page - 1) // per_page,  # Calculate total pages
            }
        }
        return jsonify(response), 200

    except SQLAlchemyError as e:
        # Specific SQLAlchemy error handling
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500

    except Exception as e:
        # General error handler
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


    
@schemes_bp.route('/api/schemes/eligible', methods=['GET'])
@jwt_required()
def get_eligible_schemes():
    applicant_id = request.args.get('applicant')
    if not applicant_id:
        return jsonify({"error": "applicant id is required"}), 400
    
    if not applicant_id.isdigit():  # Add validation for applicant_id
        return jsonify({"error": "Invalid applicant id format"}), 400

    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    try:
        applicant = ApplicantService(crud_operations).get_applicant_by_id(applicant_id)
        if not applicant:  # Handle case where applicant is not found
            return jsonify({"error": "Applicant not found"}), 404

        schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(session)
        scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
        
        eligibility_results, eligible_schemes = scheme_manager.check_schemes_eligibility_for_applicant({}, True, applicant)
        scheme_schema = SchemeSchema(many=True)
        eligible_schemes = scheme_schema.dump(eligible_schemes)
        
        response = {
            'data': {"eligible_schemes": eligible_schemes, "eligibility_results": eligibility_results}  
        }
        return jsonify(response), 200
    except SQLAlchemyError as e:  # Specific SQLAlchemy error handling
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500    
 
