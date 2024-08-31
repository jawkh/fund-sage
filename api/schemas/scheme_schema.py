# Copyright (c) 2024 by Jonathan AW


from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from dal.models import Scheme

class SchemeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Scheme
        include_relationships = True
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field(required=True)
    description = auto_field(required=True)
    eligibility_criteria = auto_field(required=True)
    benefits = auto_field(required=True)
    validity_start_date = auto_field(required=False)
    validity_end_date = auto_field(required=False)
