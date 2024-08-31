# Copyright (c) 2024 by Jonathan AW
# applicants.py

# api/routes/applicants.py

from flask import Blueprint, request, jsonify
from bl.services.applicant_service import ApplicantService
from api.schemas.applicant_schema import ApplicantSchema
from marshmallow import ValidationError

applicants_bp = Blueprint('applicants', __name__)

@applicants_bp.route('/api/applicants', methods=['GET'])
def get_applicants():
    applicants, pagecount = ApplicantService().get_all_applicants()
    return jsonify(applicants)

@applicants_bp.route('/api/applicants', methods=['POST'])
def create_applicant():
    try:
        data = request.json
        applicant_data = ApplicantSchema().load(data)
        applicant = ApplicantService().create_applicant(applicant_data, applicant_data.get('household_members', []))
        return jsonify(applicant), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
