# Copyright (c) 2024 by Jonathan AW


from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from dal.models import Applicant

class ApplicantSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Applicant
        include_relationships = True
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field(required=True)
    employment_status = auto_field(required=True)
    sex = auto_field(required=True)
    date_of_birth = auto_field(required=True)
    marital_status = auto_field(required=True)
    employment_status_change_date = auto_field(required=False)
    created_by_admin_id = auto_field(dump_only=True)
