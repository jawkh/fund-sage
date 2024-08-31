# Copyright (c) 2024 by Jonathan AW

# api/routes/schemes.py

from flask import Blueprint, request, jsonify
from bl.services.scheme_service import SchemeService
from api.schemas.scheme_schema import SchemeSchema
from marshmallow import ValidationError

schemes_bp = Blueprint('schemes', __name__)

@schemes_bp.route('/api/schemes', methods=['GET'])
def get_schemes():
    schemes = SchemeService().get_all_schemes()
    return jsonify(schemes)

@schemes_bp.route('/api/schemes/eligible', methods=['GET'])
def get_eligible_schemes():
    applicant_id = request.args.get('applicant')
    if not applicant_id:
        return jsonify({"error": "Applicant ID is required"}), 400
    
    eligible_schemes = SchemeService().get_eligible_schemes_for_applicant(applicant_id)
    return jsonify(eligible_schemes)
