# Copyright (c) 2024 by Jonathan AW


from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from dal.models import HouseholdMember

class HouseholdMemberSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HouseholdMember
        include_fk = True
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field(required=True)
    relation = auto_field(required=True)
    date_of_birth = auto_field(required=True)
    employment_status = auto_field(required=True)
    sex = auto_field(required=True)
