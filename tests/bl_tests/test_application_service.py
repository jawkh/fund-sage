# Copyright (c) 2024 by Jonathan AW

# test_application_service.py
import pytest
from bl.services.application_service import ApplicationService
from exceptions import ApplicantNotFoundException, SchemeNotFoundException, InvalidApplicationDataException
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory

def test_create_application_invalid_applicant(application_service, crud_operations, test_administrator, retrenchment_assistance_scheme):
    """
    Test creating an application with an invalid applicant.
    """
    with pytest.raises(ApplicantNotFoundException):
        application_service.create_application(
            applicant_id=9999,  # Invalid applicant ID
            scheme_id=retrenchment_assistance_scheme.id,
            created_by_admin_id=test_administrator.id,
            schemeEligibilityCheckerFactory=SchemeEligibilityCheckerFactory(crud_operations.db_session)
        )

def test_update_application_invalid_data(application_service, test_application, scheme_eligibility_checker_factory):
    """
    Test updating an application with without any data.
    """
    application =  application_service.update_application(test_application.id, {}, scheme_eligibility_checker_factory)
    assert test_application == application # unchanged application

def test_create_application_invalid_scheme(application_service, crud_operations, test_administrator, test_applicant):
    """
    Test creating an application with an invalid scheme.
    """
    with pytest.raises(SchemeNotFoundException):
        application_service.create_application(
            applicant_id=test_applicant.id,
            scheme_id=9999,  # Invalid scheme ID
            created_by_admin_id=test_administrator.id,
            schemeEligibilityCheckerFactory=SchemeEligibilityCheckerFactory(crud_operations.db_session)
        )

def test_update_application_eligibility_check(application_service, test_application, test_applicant, retrenchment_assistance_scheme, scheme_eligibility_checker_factory):
    """
    Test updating an application and triggering eligibility re-evaluation.
    """
    update_data = {
        "applicant_id": test_applicant.id,
        "scheme_id": retrenchment_assistance_scheme.id
    }
    updated_application = application_service.update_application(test_application.id, update_data, scheme_eligibility_checker_factory)
    assert updated_application.status in ["approved", "rejected"]
