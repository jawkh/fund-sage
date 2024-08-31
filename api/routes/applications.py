# Copyright (c) 2024 by Jonathan AW
# applications.py

# api/routes/applications.py

from flask import Blueprint, request, jsonify
from bl.services.application_service import ApplicationService
from api.schemas.application_schema import ApplicationSchema
from marshmallow import ValidationError
from dal.database import Base, engine, SessionLocal

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/api/applications', methods=['GET'])
def get_applications():
    applications, pagecount = ApplicationService().get_all_applications()
    return jsonify(applications)

@applications_bp.route('/api/applications', methods=['POST'])
def create_application():
    try:
        data = request.json
        application_data = ApplicationSchema().load(data)
        admin_id = request.headers.get('admin_id') # placeholder for admin_id
        application = ApplicationService().create_application(application_data.get('applicant_id'), application_data.get('scheme_id'), admin_id)
        return jsonify(application), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

