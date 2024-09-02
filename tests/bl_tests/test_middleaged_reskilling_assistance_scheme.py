
# Copyright (c) 2024 by Jonathan AW



import pytest
from dal.models import Applicant, Scheme, Application, HouseholdMember
from datetime import datetime
from dateutil.relativedelta import relativedelta

from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager
from exceptions import InvalidApplicantDataException

# Middle-aged Reskilling Assistance Scheme Tests
def test_middleaged_reskilling_assistance_eligibility(application_service, applicant_service, crud_operations, test_administrator, middleaged_reskilling_assistance_scheme):
    """
    Test end-to-end workflow for Middle-aged Reskilling Assistance Scheme eligibility and benefits calculation.
    """
    # Step 1: Create a new applicant
    applicant_data = {
        "name": "John Smith",
        "employment_status": "unemployed",  # Eligible for Middle-aged Reskilling Assistance Scheme (unemployed)
        "sex": "M",
        "date_of_birth": datetime(1980, 1, 1),  # 44 years old (eligible for middle-aged schemes) (age threshold is 40)
        "marital_status": "married",
        "employment_status_change_date": datetime.today() - relativedelta(days=30),  # 1 month ago
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Verify the applicant was created successfully
    assert applicant is not None
    assert applicant.name == "John Smith"

    # Step 2: Create a new application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=middleaged_reskilling_assistance_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify the application was created successfully
    assert application is not None
    assert application.status == "approved"  # The application will be auto-approved if the applicant is eligible

    # Step 3: Check eligibility for the scheme using SchemesManager
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(middleaged_reskilling_assistance_scheme, applicant)

    # Verify eligibility results
    assert eligibility_results is not None
    assert eligibility_results.report["is_eligible"] == (application.status == "approved")
    assert eligibility_results.report["scheme_name"] == middleaged_reskilling_assistance_scheme.name
    assert eligibility_results.report["scheme_description"] == middleaged_reskilling_assistance_scheme.description
    assert eligibility_results.report["scheme_start_date"] == middleaged_reskilling_assistance_scheme.validity_start_date
    assert eligibility_results.report["scheme_end_date"] == middleaged_reskilling_assistance_scheme.validity_end_date

    # Verify the expected benefits
    expected_benefits = [
        {
            "benefit_name": "skillsfuture_credit_top_up",
            "description": "One-time Skillsfuture Credit top-up of $1000.",
            "beneficiary": applicant.name,
            "disbursment_amount": 1000,
            "disbursment_frequency": "One-Off",
            "disbursment_duration": None
        },
        {
            "benefit_name": "study_allowance",
            "description": "Monthly study allowance of $5000 for up to 6 months.",
            "beneficiary": applicant.name,
            "disbursment_amount": 2000,
            "disbursment_frequency": "Monthly",
            "disbursment_duration": 6
        }
    ]

    for expected_benefit in expected_benefits:
        assert any(benefit == expected_benefit for benefit in eligibility_results.report["eligible_benefits"]), f"Expected {expected_benefit['benefit_name']} not found in list."
