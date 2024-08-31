# Copyright (c) 2024 by Jonathan AW

""" 
1. Custom Exceptions:
- The exceptions module contains custom exceptions that are raised in different parts of the application to handle specific error scenarios.
"""
class ApplicantNotFoundException(Exception):
    """Raised when an applicant is not found in the database."""
    pass

class AdministratorNotFoundException(Exception):
    """Raised when an administrator is not found in the database."""
    pass

class ApplicationNotFoundException(Exception):
    """Raised when an application is not found in the database."""
    pass

class HouseholdMemberNotFoundException(Exception):
    """Raised when a household member is not found in the database."""
    pass

class SchemeNotFoundException(Exception):
    """Raised when a scheme is not found in the database."""
    pass

class InvalidSchemeDataException(Exception):
    """Raised when invalid data is provided for a scheme."""
    pass

class InvalidApplicantDataException(Exception):
    """Raised when invalid data is provided for an applicant."""
    pass

class InvalidAdministratorDataException(Exception):
    """Raised when invalid data is provided for an Administrator."""
    pass

class InvalidApplicationDataException(Exception):
    """Raised when invalid data is provided for an application."""
    pass

class InvalidHouseholdMemberDataException(Exception):
    """Raised when invalid data is provided for a household member."""
    pass

class InvalidSystemConfigDataException(Exception):
    """Raised when invalid System Configuration is provided."""
    pass

class EligibilityStrategyNotFoundException(Exception):
    """Exception raised when no eligibility strategy is found for a scheme."""
    pass

class InvalidPaginationParameterException(Exception):
    """Invalid pagination parameter provided."""
    pass

class InvalidSortingParameterException(Exception):
    """Invalid sorting parameter provided."""
    pass