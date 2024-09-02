# Copyright (c) 2024 by Jonathan AW

# api/schemas/all_schema.py
""" 
Use Explicit ORM-Independent Schemas

Pros:
1. Fine-Grained Control Over Validation:
- Allows detailed and explicit control over validation rules (e.g., validate.Length, validate.OneOf), which can enforce stricter constraints beyond what the ORM provides.

2. Decoupled from ORM:
- More flexible and decoupled from the SQLAlchemy ORM. This allows for easier adjustments to the schema that do not necessarily reflect changes in the ORM model.

3. Greater Flexibility:
- Can easily customize or extend fields without relying on ORM models. It’s straightforward to add custom logic, computed fields, or modify serialization/deserialization behavior.

4. Explicit Relationships:
- Relationships (like household_members and applications) are explicitly defined, making the schema more readable and understandable, especially for those unfamiliar with the ORM or project.
""" 
from marshmallow import Schema, fields, validate, post_load
from dal.models import Administrator, Applicant, HouseholdMember, Application, Scheme

class AdministratorSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(max=255))
    password_hash = fields.Str(required=True, load_only=True, validate=validate.Length(max=255))
    salt = fields.Str(required=True, load_only=True, validate=validate.Length(max=255))
    role = fields.Str(validate=validate.OneOf(["admin", "user"]))
    consecutive_failed_logins = fields.Int(dump_only=True)
    failed_login_starttime = fields.DateTime(allow_none=True)
    account_locked = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_administrator(self, data, **kwargs):
        return Administrator(**data)

class SchemeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=255))
    description = fields.Str(required=True)
    eligibility_criteria = fields.Dict(required=True)
    benefits = fields.Dict(required=True)
    validity_start_date = fields.DateTime(required=True)
    validity_end_date = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_scheme(self, data, **kwargs):
        return Scheme(**data)


class HouseholdMemberSchema(Schema):
    id = fields.Int(dump_only=True)
    applicant_id = fields.Int(required=False) # Not required for deserialization (For Create Mode, the Applicant ID is not known yet)
    name = fields.Str(required=True, validate=validate.Length(max=255))
    relation = fields.Str(required=True, validate=validate.OneOf(["parent", "child", "spouse", "sibling", "other"]))
    date_of_birth = fields.DateTime(required=True)
    employment_status = fields.Str(validate=validate.OneOf(["employed", "unemployed"]))
    sex = fields.Str(validate=validate.OneOf(["M", "F"]))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # Do not create a HouseholdMember object directly from the schema. We need to handle a Dictionary of HouseholdMember data in our Business Logic for the Create and Update operations.
    # @post_load
    # def make_household_member(self, data, **kwargs):
    #     return HouseholdMember(**data)

    
class ApplicationSchema(Schema):
    id = fields.Int(dump_only=True)
    applicant_id = fields.Int(required=True)
    scheme_id = fields.Int(required=True)
    status = fields.Str(required=True, dump_only=True, validate=validate.OneOf(["pending", "approved", "rejected"]))
    eligibility_verdict = fields.Str(validate=validate.Length(max=1000), dump_only=True)  
    awarded_benefits = fields.Dict(dump_only=True)  
    submission_date = fields.DateTime(dump_only=True)
    created_by_admin_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    applicant = fields.Nested('ApplicantSchema', dump_only=True)
    scheme = fields.Nested('SchemeSchema', dump_only=True)
    creator = fields.Nested('AdministratorSchema', dump_only=True)

    # DO NOT create an Application object directly from the schema. We need to handle a Dictionary of Application data in our Business Logic for the Create and Update operations.
    # @post_load
    # def make_application(self, data, **kwargs):
    #     return Application(**data)

class ApplicantSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=255))
    employment_status = fields.Str(required=True, validate=validate.OneOf(["employed", "unemployed"]))
    sex = fields.Str(required=True, validate=validate.OneOf(["M", "F"]))
    date_of_birth = fields.DateTime(required=True)
    marital_status = fields.Str(required=True, validate=validate.OneOf(["single", "married", "divorced", "widowed"]))
    employment_status_change_date = fields.DateTime(allow_none=True)
    created_by_admin_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    household_members = fields.Nested('HouseholdMemberSchema', many=True)
    applications = fields.Nested('ApplicationSchema', many=True, dump_only=True)

    # DO NOT create an Applicant object directly from the schema. We need to handle a Dictionary of Applicant data in our Business Logic for the Create and Update operations.
    # @post_load
    # def make_applicant(self, data, **kwargs):
    #     return Applicant(**data)
    


""" 
SQLAlchemyAutoSchema
Cons:
1. Less Control Over Validation:
- Does not provide detailed control over validation rules, such as limiting string lengths or enforcing enumerations like in validate.OneOf(["employed", "unemployed"]).

2. Reduced Readability:
- Auto-generated fields and implicit behavior can reduce readability and understanding of the schema, especially for new developers joining the project.
"""
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
# from dal.models import Administrator

# class AdministratorSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Administrator
#         include_relationships = True
#         load_instance = True

#     id = auto_field(dump_only=True)
#     username = auto_field(required=True)
#     password_hash = auto_field(required=True)