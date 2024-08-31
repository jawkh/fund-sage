# Copyright (c) 2024 by Jonathan AW

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from dal.models import Administrator

class AdministratorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Administrator
        include_relationships = True
        load_instance = True

    id = auto_field(dump_only=True)
    username = auto_field(required=True)
    password_hash = auto_field(required=True)