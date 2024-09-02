# Copyright (c) 2024 by Jonathan AW


import pytest
from dal.models import Applicant, Scheme, Application, HouseholdMember
from datetime import datetime
from dateutil.relativedelta import relativedelta

from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager
from exceptions import InvalidApplicantDataException

# Senior Citizen Assistance Scheme Tests
def test_senior_citizen_assistance_eligibility(application_service, applicant_service, crud_operations, test_administrator, senior_citizen_assistance_scheme):
    """
    Test end-to-end workflow for Senior Citizen Assistance Scheme eligibility and benefits calculation.
    """
    # Step 1: Create a new applicant
    applicant_data = {
        "name": "Elderly Jane",
        "employment_status": "employed",  # Employment status doesn't matter for Senior Citizen Assistance Scheme
        "sex": "F",
        "date_of_birth": datetime(1950, 12, 1),  # 73 years old (eligible for senior schemes) (age threshold is 65)
        "marital_status": "widowed",
        "employment_status_change_date": None,
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Verify the applicant was created successfully
    assert applicant is not None
    assert applicant.name == "Elderly Jane"

    # Step 2: Create a new application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=senior_citizen_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify the application was created successfully
    assert application is not None
    assert application.status == "approved"  # The application will be auto-approved if the applicant is eligible

    # Step 3: Check eligibility for the scheme using SchemesManager
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(senior_citizen_assistance_scheme, applicant)

    # Verify eligibility results
    assert eligibility_results is not None
    assert eligibility_results.report["is_eligible"] == (application.status == "approved")
    assert eligibility_results.report["eligibility_message"] == "Eligible for Senior Citizen Assistance Scheme."
    assert eligibility_results.report["scheme_name"] == senior_citizen_assistance_scheme.name
    assert eligibility_results.report["scheme_description"] == senior_citizen_assistance_scheme.description
    assert eligibility_results.report["scheme_start_date"] == senior_citizen_assistance_scheme.validity_start_date
    assert eligibility_results.report["scheme_end_date"] == senior_citizen_assistance_scheme.validity_end_date

    # Verify the expected benefits
    expected_benefits = [
        {
            "benefit_name": "cpf_top_up",
            "description": "One-time CPF top-up of $200.",
            "beneficiary": applicant.name,
            "disbursment_amount": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration": None
        },
        {
            "benefit_name": "cdc_voucher",
            "description": "One-time CDC voucher of $200.",
            "beneficiary": applicant.name,
            "disbursment_amount": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration": None
        }
    ]

    for expected_benefit in expected_benefits:
        assert any(benefit == expected_benefit for benefit in eligibility_results.report["eligible_benefits"]), f"Expected {expected_benefit['benefit_name']} not found in list."



def test_ineligible_applicant_senior_citizen_assistance(application_service, applicant_service, crud_operations, test_administrator, senior_citizen_assistance_scheme):
    """
    Test for an applicant who does not meet any eligibility criteria.
    """
    # Step 1: Create a new applicant who is not eligible for any scheme
    applicant_data = {
        "name": "Ineligible Applicant",
        "employment_status": "employed",  # Not eligible for schemes requiring unemployment
        "sex": "M",
        "date_of_birth": datetime(2000, 1, 1),  # Too young for senior schemes
        "marital_status": "single",
        "employment_status_change_date": datetime.today() - relativedelta(days=5),  
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Verify the applicant was created successfully
    assert applicant is not None
    assert applicant.name == "Ineligible Applicant"

    # Step 2: Create a new application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=senior_citizen_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify the application was created successfully but is not approved
    assert application is not None
    assert application.status == "rejected"  # The application should be rejected since the applicant is not eligible

    # Step 3: Check eligibility for the scheme using SchemesManager
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(senior_citizen_assistance_scheme, applicant)

    # Verify eligibility results
    assert eligibility_results is not None
    assert eligibility_results.report["is_eligible"] == (application.status == "approved")
    assert eligibility_results.report["eligibility_message"] == "Not eligible for Senior Citizen Assistance Scheme."
    
    assert len(eligibility_results.report["eligible_benefits"]) == 0  # No benefits should be calculated for ineligible applicants

def test_borderline_eligibility_senior_citizen_assistance(application_service, applicant_service, crud_operations, test_administrator, senior_citizen_assistance_scheme):
    """
    Test for an applicant on the borderline of eligibility criteria.
    """
    # Step 1: Create a new applicant who is exactly 65 years old (borderline case)
    applicant_data = {
        "name": "Borderline Senior",
        "employment_status": "unemployed",  # Employment status doesn't matter for Senior Citizen Assistance Scheme
        "sex": "F",
        "date_of_birth": datetime.today() - relativedelta(years=65),  # Exactly 65 years old today (borderline case)
        "marital_status": "single",
        "employment_status_change_date": None,
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Verify the applicant was created successfully
    assert applicant is not None
    assert applicant.name == "Borderline Senior"

    # Step 2: Create a new application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=senior_citizen_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify the application was created successfully and is approved
    assert application is not None
    assert application.status == "approved"  # The application will be auto-approved if the applicant is exactly 65 years old

    # Step 3: Check eligibility for the scheme using SchemesManager
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(senior_citizen_assistance_scheme, applicant)

    # Verify eligibility results
    assert eligibility_results is not None
    assert eligibility_results.report["is_eligible"] == (application.status == "approved")
    assert eligibility_results.report["eligibility_message"] == "Eligible for Senior Citizen Assistance Scheme."
    assert eligibility_results.report["scheme_name"] == senior_citizen_assistance_scheme.name
    assert eligibility_results.report["scheme_description"] == senior_citizen_assistance_scheme.description
    assert eligibility_results.report["scheme_start_date"] == senior_citizen_assistance_scheme.validity_start_date
    assert eligibility_results.report["scheme_end_date"] == senior_citizen_assistance_scheme.validity_end_date
    
    assert len(eligibility_results.report["eligible_benefits"]) > 0  # Benefits should be calculated for borderline eligible applicants



def test_senior_citizen_eligibility_age_64_and_11_months(applicant_service, crud_operations, test_administrator, senior_citizen_assistance_scheme):
    """
    Test case for an applicant who is 64 years and 11 months old.
    """
    # Create an applicant who is 64 years and 11 months old
    applicant_data = {
        "name": "Senior Citizen Nearly 65",
        "employment_status": "employed",
        "sex": "M",
        "date_of_birth": datetime(datetime.today().year - 64, datetime.today().month - 1, datetime.today().day),
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)
    
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(senior_citizen_assistance_scheme, applicant)
    
    # Verify that the applicant is not eligible due to being under 65 years old
    assert not eligibility_results.report["is_eligible"]
    assert eligibility_results.report["eligibility_message"] == "Not eligible for Senior Citizen Assistance Scheme."
    assert eligibility_results.report["eligible_benefits"] == []

def test__neg_senior_citizen_eligibility_future_birth_date(applicant_service, test_administrator):
    """
    Test case for an applicant whose birth date is set in the future.
    """
    # Create an applicant with a birth date in the future
    applicant_data = {
        "name": "Future Born Applicant",
        "employment_status": "employed",
        "sex": "F",
        "date_of_birth": datetime(datetime.today().year + 1, 1, 1),  # Future birth date
        "marital_status": "married",
        "created_by_admin_id": test_administrator.id
    }

    # Attempt to create the applicant and catch any validation errors
    with pytest.raises(InvalidApplicantDataException):
        applicant_service.create_applicant(applicant_data)
