# Copyright (c) 2024 by Jonathan AW

# test_retrenchment_assistance_scheme.py

import pytest
from dal.models import Applicant, Scheme, Application, HouseholdMember
from datetime import datetime
from dateutil.relativedelta import relativedelta

from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager
from exceptions import InvalidApplicantDataException
from datetime import datetime, timedelta

# Retrenchment Assistance Scheme Tests
def test_retrenchment_assistance_eligibility(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test end-to-end workflow of creating an application for a scheme and checking eligibility and benefits calculation.
    """
    # Step 1: Create a new applicant
    applicant_data = {
        "name": "Jane Doe",
        "employment_status": "unemployed", # Eligible for Retrenchment Assistance Scheme (unemployed)
        "sex": "F",
        "date_of_birth": datetime(1985, 6, 15), 
        "marital_status": "single",
        "employment_status_change_date": datetime.today() - relativedelta(months=3),  # 3 months ago (within the last 6 months) - Eligible for Retrenchment Assistance Scheme (unemployed within the last 6 months)
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Verify the applicant was created successfully
    assert applicant is not None
    assert applicant.name == "Jane Doe"

    # Step 2: Add household members to the applicant
    household_member_data = [
        {"name": "Child One", "relation": "child", "date_of_birth": datetime(2015, 4, 10), "employment_status": "unemployed", "sex": "M"}, # 11 years old (eligible for school meal vouchers)
        {"name": "Parent One", "relation": "parent", "date_of_birth": datetime(1950, 7, 20), "employment_status": "unemployed", "sex": "F"}, # 74 years old (eligible for extra CDC vouchers)
    ]
    for member in household_member_data:
        applicant_service.create_household_member(applicant_id=applicant.id, member_data=member)

    # Verify household members were added
    household_members = applicant.household_members # Get household members from the database to verify they were added. Use SQLAlchemy relationship (lazy loading)
    assert len(household_members) == 2

    # Step 3: Create a new application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=retrenchment_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify the application was created successfully
    assert application is not None
    assert application.status == "approved" # The application will be auto-approved if the applicant is eligible (unemployed and employment status changed within the last 6 months)

    # Step 4: Check eligibility for the scheme using SchemesManager (This is the official way to test eligibility before creating the application)
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)

    # Verify eligibility results
    assert eligibility_results is not None
    assert eligibility_results.report["is_eligible"] == (application.status == "approved") 
    assert eligibility_results.report["eligibility_message"] == "Eligible for Retrenchment Assistance Scheme."
    assert eligibility_results.report["scheme_name"] == retrenchment_assistance_scheme.name
    assert eligibility_results.report["scheme_description"] == retrenchment_assistance_scheme.description
    assert eligibility_results.report["scheme_start_date"] == retrenchment_assistance_scheme.validity_start_date
    assert eligibility_results.report["scheme_end_date"] == retrenchment_assistance_scheme.validity_end_date
    
    # assert "cash_assistance" in [benefit["benefit_name"] for benefit in eligibility_results.report["eligible_benefits"]]

    cash_assistance_benefit = {
        "benefit_name": "cash_assistance",
        "description": "Cash assistance provided to all eligible applicants.",
        "beneficiary": applicant.name,
        "disbursment_amount": 1000,
        "disbursment_frequency": "One-Off",
        "disbursment_duration_month": None
    }
    
    school_meal_vouchers_benefit = {
        "benefit_name": "school_meal_vouchers",
        "description": "Meal vouchers provided for each child in the household within the primary school age range (6-11 years old).",
        "beneficiary": "Child One",
        "disbursment_amount": 100,
        "disbursment_frequency": "Monthly",
        "disbursment_duration_month": 12
    }
    
    extra_cdc_vouchers_benefit = {
        "benefit_name": "extra_cdc_vouchers",
        "description": "Extra CDC vouchers provided for each elderly parent above the age of 65.",
        "beneficiary": "Parent One",
        "disbursment_amount": 200,
        "disbursment_frequency": "One-Off",
        "disbursment_duration_month": None
    }
    
    # Check if the expected benefits are in the list using any()
    assert any(benefit == cash_assistance_benefit for benefit in eligibility_results.report["eligible_benefits"]), "Expected cash_assistance_benefit not found in list."
    assert any(benefit == school_meal_vouchers_benefit for benefit in eligibility_results.report["eligible_benefits"]), "Expected school_meal_vouchers_benefit not found in list."
    assert any(benefit == extra_cdc_vouchers_benefit for benefit in eligibility_results.report["eligible_benefits"]), "Expected extra_cdc_vouchers_benefit not found in list."
    

def test_multiple_eligible_household_members_retrenchment_assistance(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test an eligible applicant with multiple children and parents qualifying for different benefits under the Retrenchment Assistance Scheme.
    """
    # Step 1: Create a new applicant
    applicant_data = {
        "name": "Eligible Applicant",
        "employment_status": "unemployed",  # Eligible for Retrenchment Assistance Scheme
        "sex": "M",
        "date_of_birth": datetime(1970, 5, 15),
        "marital_status": "married",
        "marriage_date": datetime(2024, 8, 1),
        "employment_status_change_date": datetime.today() - relativedelta(months=4),  # 4 months ago
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Step 2: Add multiple household members
    household_member_data = [
        {"name": "Child One", "relation": "child", "date_of_birth": datetime(2016, 3, 10), "employment_status": "unemployed", "sex": "F"},  # 8 years old
        {"name": "Child Two", "relation": "child", "date_of_birth": datetime(2013, 8, 25), "employment_status": "unemployed", "sex": "M"},  # 11 years old
        {"name": "Parent One", "relation": "parent", "date_of_birth": datetime(1945, 6, 30), "employment_status": "unemployed", "sex": "F"},  # 79 years old
        {"name": "Parent Two", "relation": "parent", "date_of_birth": datetime(1950, 12, 15), "employment_status": "unemployed", "sex": "M"},  # 74 years old
    ]
    for member in household_member_data:
        applicant_service.create_household_member(applicant_id=applicant.id, member_data=member)

    # Verify household members were added
    household_members = applicant.household_members
    assert len(household_members) == 4

    # Step 3: Create a new application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=retrenchment_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify the application was created successfully
    assert application is not None
    assert application.status == "approved"

    # Step 4: Check eligibility and benefits calculation
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)

    # Verify eligibility results
    assert eligibility_results.report["is_eligible"] == (application.status == "approved")

    expected_benefits = [
        {
            "benefit_name": "cash_assistance",
            "description": "Cash assistance provided to all eligible applicants.",
            "beneficiary": applicant.name,
            "disbursment_amount": 1000,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_month": None
        },
        {
            "benefit_name": "school_meal_vouchers",
            "description": "Meal vouchers provided for each child in the household within the primary school age range (6-11 years old).",
            "beneficiary": "Child One",
            "disbursment_amount": 100,
            "disbursment_frequency": "Monthly",
            "disbursment_duration_month": 12
        },
        {
            "benefit_name": "school_meal_vouchers",
            "description": "Meal vouchers provided for each child in the household within the primary school age range (6-11 years old).",
            "beneficiary": "Child Two",
            "disbursment_amount": 100,
            "disbursment_frequency": "Monthly",
            "disbursment_duration_month": 12
        },
        {
            "benefit_name": "extra_cdc_vouchers",
            "description": "Extra CDC vouchers provided for each elderly parent above the age of 65.",
            "beneficiary": "Parent One",
            "disbursment_amount": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_month": None
        },
        {
            "benefit_name": "extra_cdc_vouchers",
            "description": "Extra CDC vouchers provided for each elderly parent above the age of 65.",
            "beneficiary": "Parent Two",
            "disbursment_amount": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_month": None
        }
    ]

    for expected_benefit in expected_benefits:
        assert any(benefit == expected_benefit for benefit in eligibility_results.report["eligible_benefits"]), f"Expected {expected_benefit['benefit_name']} not found in list."


def test_recent_employment_status_change_retrenchment_assistance(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test an applicant who was retrenched exactly at the eligibility period threshold.
    """
    # Step 1: Create a new applicant
    applicant_data = {
        "name": "Edge Case Applicant",
        "employment_status": "unemployed",  # Eligible for Retrenchment Assistance Scheme
        "sex": "M",
        "date_of_birth": datetime(1988, 11, 20),
        "marital_status": "married",
        "marriage_date": datetime(2024, 8, 1),
        "employment_status_change_date": datetime.today() - relativedelta(months=6),  # Exactly 6 months ago (Fringe test case: Right on the threshold)
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Verify the applicant was created successfully
    assert applicant is not None
    assert applicant.name == "Edge Case Applicant"

    # Step 2: Create a new application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=retrenchment_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify the application was created successfully
    assert application is not None
    assert application.status == "approved"

    # Step 3: Check eligibility for the scheme using SchemesManager
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)

    # Verify eligibility results
    assert eligibility_results.report["is_eligible"] == (application.status == "approved")
    assert len(eligibility_results.report["eligible_benefits"]) > 0  # Should have benefits calculated

# Negative Test Cases

def test__neg_overdue_employment_status_change_retrenchment_assistance(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test an applicant who was retrenched slightly outside the eligibility period (e.g., more than six months ago).
    """
    # Step 1: Create a new applicant
    applicant_data = {
        "name": "Overdue Applicant",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1975, 4, 10),
        "marital_status": "single",
        "employment_status_change_date": datetime.today() - relativedelta(days=200),  # 200 days ago, outside 6 months period
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Verify the applicant was created successfully
    assert applicant is not None
    assert applicant.name == "Overdue Applicant"

    # Step 2: Create a new application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=retrenchment_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify the application was created successfully but is rejected
    assert application is not None
    assert application.status == "rejected"

    # Step 3: Check eligibility for the scheme using SchemesManager
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)

    # Verify eligibility results
    assert eligibility_results.report["is_eligible"] == (application.status == "approved")  # Should be false
    assert len(eligibility_results.report["eligible_benefits"]) == 0  # No benefits should be calculated for ineligible applicants


def test_employed_applicant_retrenchment_assistance(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test an applicant who is currently employed and should not be eligible for retrenchment assistance benefits.
    """
    # Step 1: Create a new applicant
    applicant_data = {
        "name": "Employed Applicant",
        "employment_status": "employed",  # Not eligible for Retrenchment Assistance Scheme
        "sex": "M",
        "date_of_birth": datetime(1980, 1, 1),
        "marital_status": "married",
        "marriage_date": datetime(2024, 8, 1),
        "employment_status_change_date": None,
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Verify the applicant was created successfully
    assert applicant is not None
    assert applicant.name == "Employed Applicant"

    # Step 2: Create a new application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=retrenchment_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify the application was created successfully but is rejected
    assert application is not None
    assert application.status == "rejected"

    # Step 3: Check eligibility for the scheme using SchemesManager
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)

    # Verify eligibility results
    assert eligibility_results.report["is_eligible"] == (application.status == "approved")  # Should be false
    assert len(eligibility_results.report["eligible_benefits"]) == 0  # No benefits should be calculated for ineligible applicants


def test_non_retrenched_unemployed_applicant_retrenchment_assistance(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test an applicant who is unemployed but not recently retrenched (e.g., has been unemployed for over a year).
    """
    # Step 1: Create a new applicant
    applicant_data = {
        "name": "Long-term Unemployed Applicant",
        "employment_status": "unemployed",  # Unemployed but not recently retrenched
        "sex": "F",
        "date_of_birth": datetime(1990, 5, 20),
        "marital_status": "single",
        "employment_status_change_date": datetime.today() - relativedelta(days=400),  # More than a year ago
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Verify the applicant was created successfully
    assert applicant is not None
    assert applicant.name == "Long-term Unemployed Applicant"

    # Step 2: Create a new application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=retrenchment_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify the application was created successfully but is rejected
    assert application is not None
    assert application.status == "rejected"

    # Step 3: Check eligibility for the scheme using SchemesManager
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)

    # Verify eligibility results
    assert eligibility_results.report["is_eligible"] == (application.status == "approved")  # Should be false
    assert len(eligibility_results.report["eligible_benefits"]) == 0  # No benefits should be calculated for ineligible applicants

# parametrize the test cases (positive and negative)

@pytest.mark.parametrize("employment_status, months_since_unemployment, expected_eligibility", [
    ("unemployed", 2, True),
    ("unemployed", 6, True),
    ("unemployed", 7, False),
    ("employed", 0, False),
])
def test_retrenchment_assistance_eligibility(applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme, employment_status, months_since_unemployment, expected_eligibility):
    # Create an applicant with varying employment statuses and unemployment duration
    applicant_data = {
        "name": "Test Applicant",
        "employment_status": employment_status,
        "sex": "M",
        "date_of_birth": datetime(1990, 1, 1),
        "marital_status": "married",
        "marriage_date": datetime.today() - relativedelta(days=10), 
        "employment_status_change_date": datetime.today() - relativedelta(months=months_since_unemployment),
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)
    
    assert eligibility_results.report["is_eligible"] == expected_eligibility


def test__neg_retrenchment_assistance_eligibility_missing_employment_change_date(applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test case for an applicant who is unemployed but has no employment status change date set.
    """
    # Create an applicant who is unemployed but has no employment status change date
    applicant_data = {
        "name": "Test Applicant No Change Date",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1990, 4, 15),
        "marital_status": "married",
        "marriage_date": datetime(1990, 4, 15),
        "employment_status_change_date": None,  # No change date provided (missing data) - should not be eligible
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)
    
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)
    
    # Verify that the applicant is not eligible due to missing employment status change date
    assert not eligibility_results.report["is_eligible"]
    assert eligibility_results.report["eligible_benefits"] == []


def test_retrenchment_assistance_eligibility_children_outside_age_range(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test eligibility for the Retrenchment Assistance Scheme with children outside the school meal vouchers age range.
    """
    # Create an eligible applicant
    applicant_data = {
        "name": "John Doe",
        "employment_status": "unemployed",
        "sex": "M",
        "date_of_birth": datetime(1980, 1, 1),
        "marital_status": "married",
        "marriage_date": datetime.today() - relativedelta(months=4),  # Within the last 6 months
        "employment_status_change_date": datetime.today() - relativedelta(months=4),  # Within the last 6 months
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add household members (children outside the eligible age range for meal vouchers)
    household_member_data = [
        {"name": "Child Under Age", "relation": "child", "date_of_birth": datetime(2019, 5, 10), "employment_status": "unemployed", "sex": "F"}, # 5 years old
        {"name": "Child Over Age", "relation": "child", "date_of_birth": datetime(2012, 3, 15), "employment_status": "unemployed", "sex": "M"}   # 12 years old
    ]
    for member in household_member_data:
        applicant_service.create_household_member(applicant_id=applicant.id, member_data=member)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=retrenchment_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was approved
    assert application is not None
    assert application.status == "approved"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)

    assert eligibility_results.report["is_eligible"]
    assert eligibility_results.report["eligibility_message"] == "Eligible for Retrenchment Assistance."
    assert any(benefit["benefit_name"] == "cash_assistance" for benefit in eligibility_results.report["eligible_benefits"])
    assert not any(benefit["benefit_name"] == "school_meal_vouchers" for benefit in eligibility_results.report["eligible_benefits"])  # No school meal vouchers


def test_retrenchment_assistance_eligibility_elderly_parents_below_age_threshold(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test eligibility for the Retrenchment Assistance Scheme with elderly parents below the age threshold for extra CDC vouchers.
    """
    # Create an eligible applicant
    applicant_data = {
        "name": "Mary Johnson",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1975, 4, 20),
        "marital_status": "married",
        "marriage_date": datetime.today() - relativedelta(months=4),  # Within the last 6 months
        "employment_status_change_date": datetime.today() - relativedelta(months=3),  # Within the last 6 months
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add household members (parents below the age threshold for extra CDC vouchers)
    household_member_data = [
        {"name": "Father", "relation": "parent", "date_of_birth": datetime(1960, 12, 10), "employment_status": "unemployed", "sex": "M"}  # 64 years old
    ]
    for member in household_member_data:
        applicant_service.create_household_member(applicant_id=applicant.id, member_data=member)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=retrenchment_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was approved
    assert application is not None
    assert application.status == "approved"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)

    assert eligibility_results.report["is_eligible"]
    assert eligibility_results.report["eligibility_message"] == "Eligible for Retrenchment Assistance."
    assert any(benefit["benefit_name"] == "cash_assistance" for benefit in eligibility_results.report["eligible_benefits"])
    assert not any(benefit["benefit_name"] == "extra_cdc_vouchers" for benefit in eligibility_results.report["eligible_benefits"])  # No extra CDC vouchers


def test_retrenchment_assistance_eligibility_no_children_no_parents(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test eligibility for the Retrenchment Assistance Scheme for an applicant with no children and no elderly parents.
    """
    # Create an eligible applicant
    applicant_data = {
        "name": "Alice Cooper",
        "employment_status": "unemployed",
        "sex": "F",
        "date_of_birth": datetime(1985, 2, 14),
        "marital_status": "married",
        "marriage_date": datetime.today() - relativedelta(months=4),  # Within the last 6 months
        "employment_status_change_date": datetime.today() - relativedelta(months=5),  # Within the last 6 months
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # No household members added

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=retrenchment_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was approved
    assert application is not None
    assert application.status == "approved"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)

    assert eligibility_results.report["is_eligible"]
    assert eligibility_results.report["eligibility_message"] == "Eligible for Retrenchment Assistance."
    assert any(benefit["benefit_name"] == "cash_assistance" for benefit in eligibility_results.report["eligible_benefits"])
    assert not any(benefit["benefit_name"] == "school_meal_vouchers" for benefit in eligibility_results.report["eligible_benefits"])  # No school meal vouchers
    assert not any(benefit["benefit_name"] == "extra_cdc_vouchers" for benefit in eligibility_results.report["eligible_benefits"])  # No extra CDC vouchers


def test_retrenchment_assistance_eligibility_children_at_age_threshold(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test eligibility for the Retrenchment Assistance Scheme with children exactly at the upper age limit for school meal vouchers.
    """
    # Create an eligible applicant
    applicant_data = {
        "name": "Mark Williams",
        "employment_status": "unemployed",
        "sex": "M",
        "date_of_birth": datetime(1982, 8, 8),
        "marital_status": "married",
        "marriage_date": datetime.today() - relativedelta(months=4),  # Within the last 6 months
        "employment_status_change_date": datetime.today() - relativedelta(months=2),  # Within the last 6 months
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add a household member (child exactly at the upper age limit for school meal vouchers)
    household_member_data = {
        "name": "Child Exact Age", "relation": "child", "date_of_birth": datetime(datetime.today().year - 11, 9, 1), "employment_status": "unemployed", "sex": "F"  # 11 years old
    }
    applicant_service.create_household_member(applicant_id=applicant.id, member_data=household_member_data)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=retrenchment_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was approved
    assert application is not None
    assert application.status == "approved"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)

    assert eligibility_results.report["is_eligible"]
    assert eligibility_results.report["eligibility_message"] == "Eligible for Retrenchment Assistance."
    assert any(benefit["benefit_name"] == "cash_assistance" for benefit in eligibility_results.report["eligible_benefits"])
    assert any(benefit["benefit_name"] == "school_meal_vouchers" for benefit in eligibility_results.report["eligible_benefits"])  # Eligible for school meal vouchers




def test_eligible_applicant(crud_operations, retrenchment_assistance_scheme):
    applicant = Applicant(
        employment_status="unemployed",
        employment_status_change_date=datetime.now() - timedelta(days=30),
        marital_status="married",
        marriage_date=datetime.now() - timedelta(days=60)
    )
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)
    
    assert eligibility_results.report["is_eligible"]
    assert eligibility_results.report["eligibility_message"] == "Eligible for Retrenchment Assistance."

def test_ineligible_employed_applicant(crud_operations, retrenchment_assistance_scheme):
    applicant = Applicant(
        employment_status="employed",
        marital_status="married",
        marriage_date=datetime.now() - timedelta(days=60)
    )
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)
    
    assert not eligibility_results.report["is_eligible"]
    assert "Not eligible: Applicant is not unemployed." == eligibility_results.report["eligibility_message"] 

def test_ineligible_long_term_unemployed(crud_operations, retrenchment_assistance_scheme):
    applicant = Applicant(
        employment_status="unemployed",
        employment_status_change_date=datetime.now() - timedelta(days=200),
        marital_status="married",
        marriage_date=datetime.now() - timedelta(days=60)
    )
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)
    
    assert not eligibility_results.report["is_eligible"]
    assert "Not eligible: Retrenchment period exceeds the required duration." in eligibility_results.report["eligibility_message"] 

def test_ineligible_not_married(crud_operations, retrenchment_assistance_scheme):
    applicant = Applicant(
        employment_status="unemployed",
        employment_status_change_date=datetime.now() - timedelta(days=30),
        marital_status="single"
    )
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)
    assert not eligibility_results.report["is_eligible"]
    assert "Not eligible: Applicant is not married." in eligibility_results.report["eligibility_message"] 

def test_ineligible_married_too_long(crud_operations, retrenchment_assistance_scheme):
    applicant = Applicant(
        employment_status="unemployed",
        employment_status_change_date=datetime.now() - timedelta(days=30),
        marital_status="married",
        marriage_date=datetime.now() - timedelta(days=400)
    )
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)
    
    assert not eligibility_results.report["is_eligible"]
    assert "Not eligible: Marriage duration exceeds 12 months." in eligibility_results.report["eligibility_message"]

def test_missing_marriage_date(crud_operations, retrenchment_assistance_scheme):
    applicant = Applicant(
        employment_status="unemployed",
        employment_status_change_date=datetime.now() - timedelta(days=30),
        marital_status="married"
    )
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(retrenchment_assistance_scheme, applicant)
    assert not eligibility_results.report["is_eligible"]
    assert "Not eligible: Missing marriage date information." in eligibility_results.report["eligibility_message"]