
# Copyright (c) 2024 by Jonathan AW
""" 
Description: Tests for the ApplicantService class, focusing on applicant-related and householdmembers-related functionalities, including CRUD operations, data validation.
Priority: High (core service, crucial for managing applicants and householdmembers)

"""

import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from dal.models import Applicant
from datetime import datetime
# from exceptions import InvalidDataException
from bl.services.applicant_service import ApplicantService
from exceptions import ApplicantNotFoundException, InvalidApplicantDataException, HouseholdMemberNotFoundException, InvalidHouseholdMemberDataException
from dateutil.relativedelta import relativedelta

# Test ApplicantService methods
def test_create_applicant(crud_operations, test_administrator):
    """
    Test creating a new applicant and verify the details.
    """
    applicant_data = {
        "name": "Jane Doe",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1985, 2, 15),
        "marital_status": "married",
        "employment_status_change_date": datetime(2024, 2, 15), 
        "created_by_admin_id": test_administrator.id
    }
    applicant_service = ApplicantService(crud_operations)
    new_applicant = applicant_service.create_applicant(applicant_data)
    
    assert new_applicant.name == applicant_data["name"]
    assert new_applicant.employment_status == applicant_data["employment_status"]
    assert new_applicant.created_by_admin_id == test_administrator.id

def test_get_applicant_by_id(crud_operations, test_applicant):
    """
    Test retrieving an applicant by ID and verify the details.
    """
    applicant_service = ApplicantService(crud_operations)
    fetched_applicant = applicant_service.get_applicant_by_id(test_applicant.id)
    
    assert fetched_applicant is not None
    assert fetched_applicant.name == test_applicant.name
    assert fetched_applicant.id == test_applicant.id

def test_update_applicant(crud_operations, test_applicant):
    """
    Test updating an applicant's information.
    """
    update_data = {"name": "Jane Doe", "employment_status": "unemployed"}
    applicant_service = ApplicantService(crud_operations)
    updated_applicant = applicant_service.update_applicant(test_applicant.id, update_data)
    assert updated_applicant.name == "Jane Doe"
    assert updated_applicant.employment_status == "unemployed"

def test_delete_applicant(crud_operations, test_applicant):
    """
    Test deleting an applicant record.
    """
    applicant_service = ApplicantService(crud_operations)
    applicant_service.delete_applicant(test_applicant.id)

    # Verify the applicant no longer exists
    with pytest.raises(ApplicantNotFoundException):
        applicant_service.get_applicant_by_id(test_applicant.id)

# Negative test cases
def test__neg_get_applicant_by_invalid_id(crud_operations):
    """
    Test retrieving a non-existent applicant by ID.
    """
    applicant_service = ApplicantService(crud_operations)
    with pytest.raises(ApplicantNotFoundException):
        applicant_service.get_applicant_by_id(999)  # Non-existent ID


def test__neg_create_applicant_with_empty_name(crud_operations, test_administrator):
    """
    Test creating an applicant with missing mandatory fields.
    """
    invalid_applicant_data = {
        "name": "",  # Name is required
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1985, 2, 15),
        "marital_status": "married",
        "created_by_admin_id": test_administrator.id 
    }
    applicant_service = ApplicantService(crud_operations)
    
    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(invalid_applicant_data)
        
def test__neg_create_applicant_with_invalid_created_by_admin_id(crud_operations):
    """
    Test creating an applicant with missing mandatory fields.
    """
    invalid_applicant_data = {
        "name": "aa",  # Name is required
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1985, 2, 15),
        "marital_status": "married",
        "created_by_admin_id": 999  # Non-existent admin ID
    }
    applicant_service = ApplicantService(crud_operations)
    
    with pytest.raises(IntegrityError):
        applicant_service.create_applicant(invalid_applicant_data)
        
def test__neg_create_applicant_invalid_dob(crud_operations, test_administrator):
    """
    Test creating an applicant with invalid data.
    """
    applicant_service = ApplicantService(crud_operations)
    invalid_applicant_data = {
        "name": "me",  
        "employment_status": "employed",
        "sex": "F",  
        "date_of_birth": "1990-13-01",  # Invalid date format
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }

    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(invalid_applicant_data)
        
def test__neg_create_applicant_invalid_employment_status(crud_operations, test_administrator):
    """
    Test creating an applicant with invalid data.
    """
    applicant_service = ApplicantService(crud_operations)
    invalid_applicant_data = {
        "name": "",  # Invalid name
        "employment_status": "wild and free", # Invalid employment status
        "sex": "F",  # Invalid sex
        "date_of_birth": "1990-12-01",  
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }

    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(invalid_applicant_data)

def test__neg_create_applicant_invalid_sex(crud_operations, test_administrator):
    """
    Test creating an applicant with invalid data.
    """
    applicant_service = ApplicantService(crud_operations)
    invalid_applicant_data = {
        "name": "",  # Invalid name
        "employment_status": "employed",
        "sex": "X",  # Invalid sex
        "date_of_birth": "1990-12-01",  
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }

    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(invalid_applicant_data)
        
def test__neg_create_applicant_invalid_maritalstatus(crud_operations, test_administrator):
    """
    Test creating an applicant with invalid data.
    """
    applicant_service = ApplicantService(crud_operations)
    invalid_applicant_data = {
        "name": "",  # Invalid name
        "employment_status": "employed",
        "sex": "X",  # Invalid sex
        "date_of_birth": "1990-12-01",  
        "marital_status": "unknown", # Invalid marital status
        "created_by_admin_id": test_administrator.id
    }

    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(invalid_applicant_data)

def test__neg_invalid_data_future_employment_status_change_date(applicant_service, test_administrator):
    """
    Test eligibility for the Retrenchment Assistance Scheme with a future employment status change date.
    """
    # Create an ineligible applicant with a future employment status change date
    applicant_data = {
        "name": "Eve Brown",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1990, 12, 30),
        "marital_status": "single",
        "employment_status_change_date": datetime.today() + relativedelta(months=1),  # Future date
        "created_by_admin_id": test_administrator.id
    }
    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(applicant_data)
    
def test__neg_update_non_existent_applicant(crud_operations):
    """
    Test updating a non-existent applicant.
    """
    applicant_service = ApplicantService(crud_operations)

    with pytest.raises(ApplicantNotFoundException):
        applicant_service.update_applicant(999, {"name": "Non Existent"})
        
def test__neg_delete_non_existent_applicant(crud_operations):
    """
    Test deleting a non-existent applicant.
    """
    applicant_service = ApplicantService(crud_operations)

    with pytest.raises(ApplicantNotFoundException):
        applicant_service.delete_applicant(999)
        
        
        
# Test Cases that involves Applicant's HouseholdMembers

# Test creating a new household member for an applicant
def test_create_household_member(crud_operations, test_applicant):
    """
    Test creating a new household member and verify the details.
    """
    household_member_data = {
        "name": "Alice Doe",
        "relation": "child",
        "date_of_birth": datetime(2015, 6, 15),
        "employment_status": "unemployed",
        "sex": "F",
        "applicant_id": test_applicant.id
    }
    applicant_service = ApplicantService(crud_operations)
    new_member = applicant_service.create_household_member(test_applicant.id, household_member_data)

    assert new_member.name == household_member_data["name"]
    assert new_member.relation == household_member_data["relation"]
    assert new_member.applicant_id == test_applicant.id


# Test updating a household member's details
def test_update_household_member(crud_operations, test_applicant):
    """
    Test updating a household member's information.
    """
    applicant_service = ApplicantService(crud_operations)
    member_data = {
        "name": "Alice Doe",
        "relation": "child",
        "date_of_birth": datetime(2015, 6, 15),
        "employment_status": "unemployed",
        "sex": "F"
    }
    new_member = applicant_service.create_household_member(test_applicant.id, member_data)
    updated_data = {"name": "Alice Smith"}
    updated_member = applicant_service.update_household_member(new_member.id, updated_data)

    assert updated_member.name == "Alice Smith"

# Test deleting a household member
def test_delete_household_member(crud_operations, test_applicant):
    """
    Test deleting a household member.
    """
    applicant_service = ApplicantService(crud_operations)
    member_data = {
        "name": "Bob Doe",
        "relation": "spouse",
        "date_of_birth": datetime(1980, 1, 1),
        "employment_status": "employed",
        "sex": "M"
    }
    new_member = applicant_service.create_household_member(test_applicant.id, member_data)
    applicant_service.delete_household_member(new_member.id)

    with pytest.raises(HouseholdMemberNotFoundException):
        applicant_service.get_household_member_by_id(new_member.id)

# Negative test: Test creating a household member with invalid relation
def test__neg_create_household_member_invalid_relation(crud_operations, test_applicant):
    """
    Test creating a household member with an invalid relation.
    """
    applicant_service = ApplicantService(crud_operations)
    invalid_member_data = {
        "name": "Invalid Relation",
        "relation": "invalid",  # Invalid relation
        "date_of_birth": datetime(2015, 6, 15),
        "employment_status": "employed",
        "sex": "F",
        "applicant_id": test_applicant.id
    }

    with pytest.raises(InvalidHouseholdMemberDataException):
        applicant_service.create_household_member(test_applicant.id, invalid_member_data)

# Negative test: Test updating a non-existent household member
def test__neg_update_non_existent_household_member(crud_operations):
    """
    Test updating a non-existent household member.
    """
    applicant_service = ApplicantService(crud_operations)

    with pytest.raises(HouseholdMemberNotFoundException):
        applicant_service.update_household_member(999, {"name": "Non Existent"})

# Negative test: Test deleting a non-existent household member
def test__neg_delete_non_existent_household_member(crud_operations):
    """
    Test deleting a non-existent household member.
    """
    applicant_service = ApplicantService(crud_operations)

    with pytest.raises(HouseholdMemberNotFoundException):
        applicant_service.delete_household_member(999)


# Test lazy loading of household members
def test_lazy_loading_household_members(crud_operations, test_applicant):
    """
    Test lazy loading of household members for an applicant.
    """
    applicant_service = ApplicantService(crud_operations)

    # Initially retrieve applicant without accessing household members
    applicant = applicant_service.get_applicant_by_id(test_applicant.id)
    assert applicant is not None

    # Access household members to trigger lazy loading
    household_members = applicant.household_members
    assert isinstance(household_members, list)
    assert len(household_members) >= 0  # Check that the lazy-loaded relationship works

# Test lazy loading of household members after adding a new member
def test_lazy_loading_household_members_after_addition(crud_operations, test_applicant):
    """
    Test lazy loading of household members after adding a new member to the applicant.
    """
    applicant_service = ApplicantService(crud_operations)

    # Add a new household member
    member_data = {
        "name": "Carol Doe",
        "relation": "sibling",
        "date_of_birth": datetime(1992, 8, 25),
        "employment_status": "employed",
        "sex": "F",
        "applicant_id": test_applicant.id
    }
    new_member = applicant_service.create_household_member(test_applicant.id, member_data)

    # Retrieve the applicant again to test lazy loading
    applicant = applicant_service.get_applicant_by_id(test_applicant.id)
    household_members = applicant.household_members  # Trigger lazy loading

    assert any(member.name == "Carol Doe" for member in household_members)
    assert len(household_members) > 0

# Test lazy loading with multiple household members
def test_lazy_loading_multiple_household_members(crud_operations, test_applicant):
    """
    Test lazy loading of multiple household members for an applicant.
    """
    applicant_service = ApplicantService(crud_operations)

    # Add multiple household members
    members_data = [
        {
            "name": "Alice Doe",
            "relation": "child",
            "date_of_birth": datetime(2015, 6, 15),
            "employment_status": "unemployed",
            "sex": "F"
        },
        {
            "name": "Bob Doe",
            "relation": "parent",
            "date_of_birth": datetime(1955, 4, 10),
            "employment_status": "unemployed",
            "sex": "M"
        }
    ]

    for member_data in members_data:
        applicant_service.create_household_member(test_applicant.id, member_data)

    # Retrieve the applicant again to test lazy loading of multiple household members
    applicant = applicant_service.get_applicant_by_id(test_applicant.id)
    household_members = applicant.household_members  # Trigger lazy loading

    assert any(member.name == "Alice Doe" for member in household_members)
    assert any(member.name == "Bob Doe" for member in household_members)
