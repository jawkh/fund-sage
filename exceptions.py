# Copyright (c) 2024 by Jonathan AW

class ApplicantNotFoundException(Exception):
    """Raised when an applicant is not found in the database."""
    pass

class AdministratorNotFoundException(Exception):
    """Raised when an administrator is not found in the database."""
    pass

class ApplicationNotFoundException(Exception):
    """Raised when an application is not found in the database."""
    pass

class SchemeNotFoundException(Exception):
    """Raised when a scheme is not found in the database."""
    pass
