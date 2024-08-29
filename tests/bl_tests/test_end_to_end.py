# Copyright (c) 2024 by Jonathan AW




# test_end_to_end.py
import pytest
from dal.models import Applicant, Scheme, Application, HouseholdMember
from datetime import datetime, timedelta
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager

def test_create_application_and_check_eligibility(application_service, applicant_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
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
        "employment_status_change_date": datetime.today() - timedelta(days=90),  # 3 months ago (within the last 6 months) - Eligible for Retrenchment Assistance Scheme (unemployed within the last 6 months)
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
    assert eligibility_results.is_eligible == (application.status == "approved") 
    assert eligibility_results.scheme_name == retrenchment_assistance_scheme.name
    assert eligibility_results.scheme_description == retrenchment_assistance_scheme.description
    assert eligibility_results.scheme_start_date == retrenchment_assistance_scheme.validity_start_date
    assert eligibility_results.scheme_end_date == retrenchment_assistance_scheme.validity_end_date
    
    # assert "cash_assistance" in [benefit["benefit_name"] for benefit in eligibility_results.eligible_benefits]

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
    assert any(benefit == cash_assistance_benefit for benefit in eligibility_results.eligible_benefits), "Expected cash_assistance_benefit not found in list."
    assert any(benefit == school_meal_vouchers_benefit for benefit in eligibility_results.eligible_benefits), "Expected school_meal_vouchers_benefit not found in list."
    assert any(benefit == extra_cdc_vouchers_benefit for benefit in eligibility_results.eligible_benefits), "Expected extra_cdc_vouchers_benefit not found in list."
    
