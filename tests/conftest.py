# Copyright (c) 2024 by Jonathan AW
# conftest.py

""" 
Shared fixtures for testing.

Design Patterns:

1. Fixture:
- Fixtures are used to provide a fixed baseline upon which tests can reliably and repeatedly execute. They are used to set up necessary resources, such as database connections, before running tests and to clean up after the tests are complete.

2. Dependency Injection:
- The fixtures provide instances of classes and services with their dependencies injected, promoting separation of concerns and testability.
- The fixtures inject dependencies such as CRUDOperations, SystemConfig, SchemeService, and ApplicantService into the test functions, allowing for better testability and separation of concerns.

3. Encapsulation:
- The fixtures encapsulate the setup and teardown logic for database connections and testing sessions, providing a clean interface for test functions.

4. Clear Separation of Concerns:
- Each fixture is focused on providing a specific resource or service required for testing, following the Single Responsibility Principle (SRP).

5. Readability and Maintainability:
- The fixtures are well-organized and named descriptively, making the code easy to understand and maintain.

6. Use of Pytest:
- Pytest fixtures are used to set up the testing environment and provide the necessary resources for testing, enhancing the testability of the application.



"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from environs import Env
from datetime import datetime

from dal.crud_operations import CRUDOperations
from dal.system_config import SystemConfig
from dal.database import Base
from bl.services.applicant_service import ApplicantService
from bl.services.scheme_service import SchemeService

# Load environment variables
load_dotenv()
TEST_DATABASE_URL = Env().str("TEST_DATABASE_URL", "TEST_DATABASE_URL is not set.")


# Create a new engine for the test database
test_engine = create_engine(TEST_DATABASE_URL)

# Create a configured "Session" class for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def setup_database():
    """
    Set up the database once for the entire test session.
    This fixture will create all the tables at the start of the session and drop them at the end.
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop all tables after the test session is complete
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="session")
def connection(setup_database):
    """
    Creates a single database connection for the test session.
    """
    connection = test_engine.connect()
    yield connection
    connection.close()

@pytest.fixture(scope="function")
def test_db(connection):
    """
    Creates a new database session for each test function, using a transaction that rolls back after each test.
    """
    transaction = connection.begin()  # Begin a new transaction on the connection
    session = TestingSessionLocal(bind=connection)  # Bind the session to the same connection
    try:
        yield session  # This is where the test using the session will run
        session.flush()  # Ensure all changes are flushed to the database
        transaction.rollback()  # Rollback the transaction to clean up after the test
    finally:
        session.close()  # Close the session to release the connection
    

@pytest.fixture(scope="function")
def crud_operations(test_db):
    """
    Fixture to provide a CRUDOperations instance with a testing session. (using a transaction that rolls back after each test)
    """
    return CRUDOperations(test_db)

@pytest.fixture(scope="function")
def system_config(test_db):
    """
    Fixture to provide a system_config instance with a testing session. (using a transaction that rolls back after each test)
    """
    return SystemConfig(test_db)

@pytest.fixture(scope="function")
def scheme_service(crud_operations):
    """
    Fixture to provide a SchemeService instance for testing.
    """
    return SchemeService(crud_operations)

@pytest.fixture(scope="function")
def applicant_service(crud_operations):
    """
    Fixture to provide an ApplicantService instance with dependencies for testing.
    """
    return ApplicantService(crud_operations)


@pytest.fixture(scope="function")
def test_administrator(crud_operations):
    """
    Fixture to create essential mock data required for testing.
    Ensures referential integrity for 'Applications' by creating necessary 'Schemes' records first.
    """
    # Create mock administrators
    yield crud_operations.create_administrator(username="test_admin", password_hash="correct_password", salt="salt")

@pytest.fixture(scope="function")
def test_scheme(crud_operations):
    """
    Fixture to create essential mock data required for testing.
    Ensures referential integrity for 'Applications' by creating necessary 'Schemes' records first.
    """
    # Retrenchment Assistance Scheme
    scheme_data = {
        "name": "Retrenchment Assistance Scheme",
        "description": "A scheme to provide financial support and benefits to individuals who have recently been retrenched from their jobs.",
        "eligibility_criteria": {
            "employment_status": "unemployed",
            "retrechment_period_months": 6,
        },
        "benefits": {
            "cash_assistance": {
            "disbursment_amount": 1000,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_months": None,
            "description": "Cash assistance provided to all eligible applicants."
            },
            "school_meal_vouchers": {
            "amount_per_child": 100,
            "disbursment_frequency": "Monthly",
            "disbursment_duration_months": 12,
            "description": "Meal vouchers provided for each child in the household within the primary school age range (6-11 years old).",
            "eligibility": {
                "relation": "child",
                "age_range": {
                "min": 6,
                "max": 11
                }
            }
            },
            "extra_cdc_vouchers": {
            "amount_per_parent": 200,
            "disbursment_frequency": "One-Off",
            "disbursment_duration_months": None,
            "description": "Extra CDC vouchers provided for each elderly parent above the age of 65.",
            "eligibility": {
                "relation": "parent",
                "age_threshold": 65
            }
            }
        },
        "validity_start_date": datetime(2024, 1, 1),
        "validity_end_date": None
        }

    yield crud_operations.create_scheme(scheme_data)

@pytest.fixture(scope="function")
def test_applicant(crud_operations):
    """
    Fixture to create essential mock data required for testing.
    Ensures referential integrity for 'Applications' by creating necessary 'applicant' records first.
    """
    ad = crud_operations.create_administrator(username="test_admin_a", password_hash="hashed_password", salt="salt") # Create a mock admin used to create the applicant
    
    applicant_data = {
        "name": "John Doe",
        "employment_status": "employed",
        "sex": "M",
        "date_of_birth": datetime(1990, 1, 1),
        "marital_status": "single",
        "created_by_admin_id": ad.id
    }
    new_applicant = crud_operations.create_applicant(applicant_data)
    
    # Add a new household member
    member_data = {
        "name": "Eve Doe",
        "relation": "sibling",
        "date_of_birth": datetime(1992, 8, 25),
        "employment_status": "employed",
        "sex": "F",
        "applicant_id": new_applicant.id
    }
    new_member = crud_operations.create_household_member(member_data)
    
    # Add a new household member
    member_data = {
        "name": "Adam Doe",
        "relation": "parent",
        "date_of_birth": datetime(1992, 8, 25),
        "employment_status": "employed",
        "sex": "M",
        "applicant_id": new_applicant.id
    }
    new_member = crud_operations.create_household_member(member_data)

    yield new_applicant
    
@pytest.fixture(scope="function")
def test_application(crud_operations):
    """
    Fixture to create essential mock data required for testing.
    """
    ad = crud_operations.create_administrator(username="test_admin_b", password_hash="hashed_password", salt="salt") # Create a mock admin used to create the applicant and application
    applicant_data = {
        "name": "John Doe",
        "employment_status": "employed",
        "sex": "M",
        "date_of_birth": datetime(1990, 1, 1),
        "marital_status": "single",
        "created_by_admin_id": ad.id
    }
    applicant = crud_operations.create_applicant(applicant_data) # Create a mock applicant for the application
    
    scheme_data = {
        "name": "Mock Scheme 2",
        "description": "A mock scheme for testing purposes",
        "eligibility_criteria": {"employment_status": "unemployed"},
        "benefits": {"amount": 500.0},
        "validity_start_date": "2023-01-01",
        "validity_end_date": None
    }
    scheme = crud_operations.create_scheme(scheme_data) # Create a mock scheme for the application

    application_data = {
        "applicant_id": applicant.id,
        "scheme_id": scheme.id,  # Assume there is a valid scheme with ID 1
        "status": "pending",
        "created_by_admin_id": ad.id  # Link to the admin who created it
    }
    yield crud_operations.create_application(application_data) # Create a mock application