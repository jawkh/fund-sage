# Copyright (c) 2024 by Jonathan AW

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from dal.models import Application

class ApplicationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        include_fk = True
        include_relationships = True
        load_instance = True

    id = auto_field(dump_only=True)
    applicant_id = auto_field(required=True)
    scheme_id = auto_field(required=True)
    status = auto_field(required=True)
    created_by_admin_id = auto_field(dump_only=True)
