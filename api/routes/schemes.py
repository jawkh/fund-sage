# Copyright (c) 2024 by Jonathan AW

# api/routes/schemes.py

from flask import Blueprint, request, jsonify, g
from bl.services.scheme_service import SchemeService
from api.schemas.all_schemas import SchemeSchema
# from marshmallow import ValidationError
from dal.crud_operations import CRUDOperations
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager
from bl.services.applicant_service import ApplicantService

schemes_bp = Blueprint('schemes', __name__)

@schemes_bp.route('/api/schemes', methods=['GET'])
def get_schemes():
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    try:
        schemes = SchemeService(crud_operations).get_all_schemes()
        return jsonify(schemes)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@schemes_bp.route('/api/schemes/eligible', methods=['GET'])
def get_eligible_schemes():
    applicant_id = request.args.get('applicant')
    if not applicant_id:
        return jsonify({"error": "Applicant ID is required"}), 400
    
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    try: 
        applicant = ApplicantService(crud_operations).get_applicant_by_id(applicant_id) 
        schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(session)
        scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
        eligibility_results = scheme_manager.check_schemes_eligibility_for_applicant({}, True, applicant)

        eligible_schemes = [scheme for scheme in eligibility_results if eligibility_results[scheme]['is_eligible']]
        return jsonify(eligible_schemes)
    except Exception as e:
        return jsonify({'error': str(e)}), 400  
        
