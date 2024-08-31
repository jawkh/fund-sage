# Copyright (c) 2024 by Jonathan AW

# test_application_service.py
import pytest
from bl.services.application_service import ApplicationService
from exceptions import ApplicantNotFoundException, SchemeNotFoundException, InvalidApplicationDataException,  InvalidPaginationParameterException, InvalidSortingParameterException
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



def test_get_all_applications_pagination(application_service, multiple_applications):
    """
    Test retrieving all applications with pagination.
    """
    # Retrieve the first page with 2 applications per page
    applications, total_count = application_service.get_all_applications(page=1, page_size=2)

    assert len(applications) == 2  # Expect 2 applications on the first page
    assert total_count == len(multiple_applications)  # Total count should match the number of created applications

def test_get_all_applications_sorting_by_created_at(application_service, multiple_applications):
    """
    Test retrieving all applications with sorting by 'created_at' in ascending order.
    """
    applications, total_count = application_service.get_all_applications(page=1, page_size=5, sort_by='created_at', sort_order='asc')

    # Verify applications are sorted by 'created_at'
    assert len(applications) == 5
    assert applications[0].created_at <= applications[1].created_at
    assert applications[1].created_at <= applications[2].created_at

def test_get_all_applications_invalid_pagination(application_service):
    """
    Test get_all_applications with invalid pagination parameters.
    """
    with pytest.raises(InvalidPaginationParameterException) as exc_info:
        application_service.get_all_applications(page=-1, page_size=2)  # Invalid page number
    assert str(exc_info.value) == "Page number must be greater than 0."

    with pytest.raises(InvalidPaginationParameterException) as exc_info:
        application_service.get_all_applications(page=1, page_size=0)  # Invalid page size
    assert str(exc_info.value) == "Page size must be greater than 0."

def test_get_all_applications_invalid_sorting(application_service):
    """
    Test get_all_applications with invalid sorting parameters.
    """
    with pytest.raises(InvalidSortingParameterException) as exc_info:
        application_service.get_all_applications(page=1, page_size=2, sort_by='invalid_field', sort_order='asc')
    assert str(exc_info.value) == "Invalid sort_by field 'invalid_field'. Allowed value is 'created_at'."

    with pytest.raises(InvalidSortingParameterException) as exc_info:
        application_service.get_all_applications(page=1, page_size=2, sort_by='created_at', sort_order='invalid_order')
    assert str(exc_info.value) == "Invalid sort_order 'invalid_order'. Allowed values are 'asc' or 'desc'."
