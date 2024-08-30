
# Copyright (c) 2024 by Jonathan AW

# This test file tests the Single Working Mothers Support Scheme eligibility and benefits calculation.
# test_single_working_mothers_support_scheme.py

import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager
from dal.models import Applicant, HouseholdMember

# Fixture for Single Working Mothers Support Scheme
@pytest.fixture(scope="function")
def single_working_mothers_support_scheme(scheme_service):
    """
    Fixture to create a mock Single Working Mothers Support Scheme for testing.
    """
    single_working_mothers_support_scheme = {
        "name": "Single Working Mothers Support Scheme",
        "description": "A scheme to provide financial support and benefits to single working mothers with young children (18 and below).",
        "eligibility_criteria": {
            "sex": "F",
            "marital_status": ['single', 'divorced', 'widowed'],
            "employment_status": "employed",
            "household_composition": {
                "relation": "child",
                "age_range": {
                    "age_threshold": 18
                }
            }
        },
        "benefits": {
            "cash_assistance": {
                "disbursment_amount": 1000,
                "disbursment_frequency": "One-Off",
                "disbursment_duration_months": None,
                "description": "Cash assistance provided to all eligible applicants."
            },
            "income_tax_rebates": {
                "disbursment_amount": 1000,
                "disbursment_frequency": "annually",
                "disbursment_duration_months": 60,
                "description": "Income Tax Rebates given to all eligible applicants for every eligible children in the household."
            }
        },
        "validity_start_date": datetime(2024, 1, 1),
        "validity_end_date": None
    }
    yield scheme_service.create_scheme(single_working_mothers_support_scheme)

def test_single_working_mothers_support_scheme_eligibility(application_service, applicant_service, crud_operations, test_administrator, single_working_mothers_support_scheme):
    """
    Test eligibility and benefits calculation for the Single Working Mothers Support Scheme.
    """
    # Create an eligible applicant
    applicant_data = {
        "name": "Anna Smith",
        "employment_status": "employed",
        "sex": "F",
        "date_of_birth": datetime(1990, 5, 15),
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add eligible household member (child under 18)
    household_member_data_child_one = {
        "name": "Child One",
        "relation": "child",
        "date_of_birth": datetime(2010, 7, 25),  # 14 years old
        "employment_status": "unemployed",
        "sex": "M"
    }
    applicant_service.create_household_member(applicant_id=applicant.id, member_data=household_member_data_child_one)
    
    # Add eligible household member (child under 18)
    household_member_data_child_two = {
        "name": "Child Two",
        "relation": "child",
        "date_of_birth": datetime(2009, 7, 25),  # 15 years old
        "employment_status": "unemployed",
        "sex": "M"
    }
    applicant_service.create_household_member(applicant_id=applicant.id, member_data=household_member_data_child_two)
    
    # Add eligible household member (child above 18)
    household_member_data_child_three = {
        "name": "Child Three",
        "relation": "child",
        "date_of_birth": datetime(2004, 7, 25),  # 20 years old (ineligible)
        "employment_status": "unemployed",
        "sex": "M"
    }
    applicant_service.create_household_member(applicant_id=applicant.id, member_data=household_member_data_child_three)
    
    # Add eligible household member (parent)
    household_member_father = {
        "name": "Dad",
        "relation": "parent", # Parent is not considered for eligibility
        "date_of_birth": datetime(1964, 7, 25),  
        "employment_status": "unemployed",
        "sex": "M"
    }
    applicant_service.create_household_member(applicant_id=applicant.id, member_data=household_member_father)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=single_working_mothers_support_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was approved
    assert application is not None
    assert application.status == "approved"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(single_working_mothers_support_scheme, applicant)

    assert eligibility_results.is_eligible
    assert eligibility_results.eligibility_message == "Eligible for Single Working Mothers Support Scheme."
    assert any(benefit["benefit_name"] == "cash_assistance" for benefit in eligibility_results.eligible_benefits)
    assert any(benefit["benefit_name"] == f"income_tax_rebates for eligible_child: {household_member_data_child_one.get('name')}" for benefit in eligibility_results.eligible_benefits)
    assert any(benefit["benefit_name"] == f"income_tax_rebates for eligible_child: {household_member_data_child_two.get('name')}" for benefit in eligibility_results.eligible_benefits)
    assert not any(benefit["benefit_name"] == f"income_tax_rebates for eligible_child: {household_member_data_child_three.get('name')}" for benefit in eligibility_results.eligible_benefits)
    assert not any(benefit["benefit_name"] == f"income_tax_rebates for eligible_child: {household_member_father.get('name')}" for benefit in eligibility_results.eligible_benefits)

    cash_assistance_benefit = {
        "benefit_name": "cash_assistance",
        "description": "Cash assistance provided to all eligible applicants.",
        "beneficiary": applicant.name,
        "disbursment_amount": 1000,
        "disbursment_frequency": "One-Off",
        "disbursment_duration_month": None
    }
    
    income_tax_rebates_benefit_child_one = {
        "benefit_name": f"income_tax_rebates for eligible_child: {household_member_data_child_one.get('name')}",
        "description": "Income Tax Rebates given to all eligible applicants for every eligible children in the household.",
        "beneficiary": applicant.name,
        "disbursment_amount": 1000,
        "disbursment_frequency": "annually",
        "disbursment_duration_month": 60
    }
    income_tax_rebates_benefit_child_two = {
        "benefit_name": f"income_tax_rebates for eligible_child: {household_member_data_child_two.get('name')}",
        "description": "Income Tax Rebates given to all eligible applicants for every eligible children in the household.",
        "beneficiary": applicant.name,
        "disbursment_amount": 1000,
        "disbursment_frequency": "annually",
        "disbursment_duration_month": 60
    }
    # Check if the expected benefits are in the list using any()
    assert any(benefit == cash_assistance_benefit for benefit in eligibility_results.eligible_benefits), "Expected cash_assistance_benefit not found in list."
    assert any(benefit == income_tax_rebates_benefit_child_one for benefit in eligibility_results.eligible_benefits), f"Expected income_tax_rebates for eligible_child: {household_member_data_child_one.get('name')} not found in list."
    assert any(benefit == income_tax_rebates_benefit_child_two for benefit in eligibility_results.eligible_benefits), f"Expected income_tax_rebates for eligible_child: {household_member_data_child_two.get('name')} not found in list."
    


def test_single_working_mothers_support_scheme_ineligible_due_to_no_child(application_service, applicant_service, crud_operations, test_administrator, single_working_mothers_support_scheme):
    """
    Test ineligibility for Single Working Mothers Support Scheme when no child 18 or below is present.
    """
    # Create an applicant with no children under 18
    applicant_data = {
        "name": "Jessica Brown",
        "employment_status": "employed",
        "sex": "F",
        "date_of_birth": datetime(1985, 3, 20),
        "marital_status": "divorced",
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add household member (child over 18)
    household_member_data = {
        "name": "Child One",
        "relation": "child",
        "date_of_birth": datetime(2000, 4, 10),  # 24 years old
        "employment_status": "unemployed",
        "sex": "M"
    }
    applicant_service.create_household_member(applicant_id=applicant.id, member_data=household_member_data)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=single_working_mothers_support_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was rejected
    assert application is not None
    assert application.status == "rejected"

    # Verify eligibility results
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(single_working_mothers_support_scheme, applicant)

    assert not eligibility_results.is_eligible
    assert eligibility_results.eligibility_message == "Not eligible: No child 18 years old or younger in the household."


def test_single_working_mothers_support_scheme_child_at_age_threshold(application_service, applicant_service, crud_operations, test_administrator, single_working_mothers_support_scheme):
    """
    Test eligibility and benefits calculation for the Single Working Mothers Support Scheme
    when the applicant has a child exactly at the age threshold.
    """
    # Create an eligible applicant
    applicant_data = {
        "name": "Mary Johnson",
        "employment_status": "employed",
        "sex": "F",
        "date_of_birth": datetime(1985, 3, 20),
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add household member (child exactly at the age threshold)
    household_member_data = {
        "name": "Child At Threshold",
        "relation": "child",
        "date_of_birth":  datetime.today() - relativedelta(years=18),  # Exactly 18 years old
        "employment_status": "unemployed",
        "sex": "M"
    }
    applicant_service.create_household_member(applicant_id=applicant.id, member_data=household_member_data)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=single_working_mothers_support_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was approved
    assert application is not None
    assert application.status == "approved"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(single_working_mothers_support_scheme, applicant)

    assert eligibility_results.is_eligible
    assert eligibility_results.eligibility_message == "Eligible for Single Working Mothers Support Scheme."
    assert any(benefit["benefit_name"] == "cash_assistance" for benefit in eligibility_results.eligible_benefits)
    assert any(benefit["benefit_name"] == f"income_tax_rebates for eligible_child: {household_member_data['name']}" for benefit in eligibility_results.eligible_benefits)


def test_single_working_mothers_support_scheme_only_adult_children(application_service, applicant_service, crud_operations, test_administrator, single_working_mothers_support_scheme):
    """
    Test that the applicant is not eligible for the Single Working Mothers Support Scheme
    when all children are above the age threshold.
    """
    # Create an applicant
    applicant_data = {
        "name": "Lisa Brown",
        "employment_status": "employed",
        "sex": "F",
        "date_of_birth": datetime(1980, 6, 10),
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add household members (all children above age threshold)
    household_member_data = [
        {
            "name": "Adult Child 1",
            "relation": "child",
            "date_of_birth": datetime.today() - relativedelta(years=19),   # 19 years old
            "employment_status": "unemployed",
            "sex": "F"
        },
        {
            "name": "Adult Child 2",
            "relation": "child",
            "date_of_birth": datetime.today() - relativedelta(years=21),   # 21 years old
            "employment_status": "unemployed",
            "sex": "M"
        }
    ]
    for member in household_member_data:
        applicant_service.create_household_member(applicant_id=applicant.id, member_data=member)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=single_working_mothers_support_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was rejected
    assert application is not None
    assert application.status == "rejected"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(single_working_mothers_support_scheme, applicant)

    assert not eligibility_results.is_eligible
    assert eligibility_results.eligibility_message == "Not eligible: No child 18 years old or younger in the household."


def test_single_working_mothers_support_scheme_not_employed(application_service, applicant_service, crud_operations, test_administrator, single_working_mothers_support_scheme):
    """
    Test that the applicant is not eligible for the Single Working Mothers Support Scheme
    when the applicant is not employed.
    """
    # Create an applicant who is not employed
    applicant_data = {
        "name": "Nancy Williams",
        "employment_status": "unemployed",  # Not eligible due to employment status
        "sex": "F",
        "date_of_birth": datetime(1985, 4, 18),
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add household member (child below age threshold)
    household_member_data = {
        "name": "Child Below Threshold",
        "relation": "child",
        "date_of_birth": datetime.today() - relativedelta(years=10),  # 10 years old
        "employment_status": "unemployed",
        "sex": "M"
    }
    applicant_service.create_household_member(applicant_id=applicant.id, member_data=household_member_data)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=single_working_mothers_support_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was rejected
    assert application is not None
    assert application.status == "rejected"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(single_working_mothers_support_scheme, applicant)

    assert not eligibility_results.is_eligible
    assert eligibility_results.eligibility_message == "Not eligible: Applicant is not employed."

def test_single_working_mothers_support_scheme_male_applicant(application_service, applicant_service, crud_operations, test_administrator, single_working_mothers_support_scheme):
    """
    Test that the applicant is not eligible for the Single Working Mothers Support Scheme
    when the applicant is male.
    """
    # Create a male applicant
    applicant_data = {
        "name": "John Doe",
        "employment_status": "employed",
        "sex": "M",  # Not eligible due to being male
        "date_of_birth": datetime(1980, 7, 12),
        "marital_status": "single",
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add household member (child below age threshold)
    household_member_data = {
        "name": "Child Below Threshold",
        "relation": "child",
        "date_of_birth": datetime.today() - relativedelta(years=12),  # 12 years old
        "employment_status": "unemployed",
        "sex": "F"
    }
    applicant_service.create_household_member(applicant_id=applicant.id, member_data=household_member_data)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=single_working_mothers_support_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was rejected
    assert application is not None
    assert application.status == "rejected"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(single_working_mothers_support_scheme, applicant)

    assert not eligibility_results.is_eligible
    assert eligibility_results.eligibility_message == "Not eligible: Applicant is not female."


def test_single_working_mothers_support_scheme_incorrect_marital_status(application_service, applicant_service, crud_operations, test_administrator, single_working_mothers_support_scheme):
    """
    Test that the applicant is not eligible for the Single Working Mothers Support Scheme
    when the applicant's marital status is not single, divorced, or widowed.
    """
    # Create an applicant with incorrect marital status
    applicant_data = {
        "name": "Jessica White",
        "employment_status": "employed",
        "sex": "F",
        "date_of_birth": datetime(1987, 5, 23),
        "marital_status": "married",  # Not eligible due to marital status
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add household member (child below age threshold)
    household_member_data = {
        "name": "Child Below Threshold",
        "relation": "child",
        "date_of_birth": datetime.today() - relativedelta(years=8),  # 8 years old
        "employment_status": "unemployed",
        "sex": "M"
    }
    applicant_service.create_household_member(applicant_id=applicant.id, member_data=household_member_data)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=single_working_mothers_support_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was rejected
    assert application is not None
    assert application.status == "rejected"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(single_working_mothers_support_scheme, applicant)

    assert not eligibility_results.is_eligible
    assert eligibility_results.eligibility_message == "Not eligible: Applicant is not single, divorced, or widowed."


def test_single_working_mothers_support_scheme_children_at_and_above_age_threshold(application_service, applicant_service, crud_operations, test_administrator, single_working_mothers_support_scheme):
    """
    Test eligibility and benefits calculation for the Single Working Mothers Support Scheme
    when the applicant has children exactly at and just above the age threshold.
    """
    # Create an eligible applicant
    applicant_data = {
        "name": "Emily Davis",
        "employment_status": "employed",
        "sex": "F",
        "date_of_birth": datetime(1983, 1, 2),
        "marital_status": "divorced",
        "created_by_admin_id": test_administrator.id
    }
    applicant = applicant_service.create_applicant(applicant_data)

    # Add household members (children at and above age threshold)
    household_member_data = [
        {
            "name": "Child At Threshold",
            "relation": "child",
            "date_of_birth": datetime.today() - relativedelta(years=18),  # Exactly 18 years old
            "employment_status": "unemployed",
            "sex": "M"
        },
        {
            "name": "Child Above Threshold",
            "relation": "child",
            "date_of_birth": datetime.today() - relativedelta(years=19),  # 19 years old
            "employment_status": "unemployed",
            "sex": "F"
        }
    ]
    for member in household_member_data:
        applicant_service.create_household_member(applicant_id=applicant.id, member_data=member)

    # Create an application for the scheme
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(crud_operations.db_session)
    application = application_service.create_application(
        applicant_id=applicant.id,
        scheme_id=single_working_mothers_support_scheme.id,
        created_by_admin_id=test_administrator.id,
        schemeEligibilityCheckerFactory=schemeEligibilityCheckerFactory
    )

    # Verify application was approved
    assert application is not None
    assert application.status == "approved"

    # Verify eligibility and benefits
    scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
    eligibility_results = scheme_manager.check_scheme_eligibility_for_applicant(single_working_mothers_support_scheme, applicant)

    assert eligibility_results.is_eligible
    assert eligibility_results.eligibility_message == "Eligible for Single Working Mothers Support Scheme."
    assert any(benefit["benefit_name"] == "cash_assistance" for benefit in eligibility_results.eligible_benefits)
    assert any(benefit["benefit_name"] == f"income_tax_rebates for eligible_child: {household_member_data[0]['name']}" for benefit in eligibility_results.eligible_benefits)
    assert not any(benefit["benefit_name"] == f"income_tax_rebates for eligible_child: {household_member_data[1]['name']}" for benefit in eligibility_results.eligible_benefits)
