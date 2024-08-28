# conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from environs import Env
from datetime import datetime

from dal.crud_operations import CRUDOperations
from dal.database import Base
# from dal.models import Administrator, Applicant, HouseholdMember, Scheme, Application, SystemConfiguration

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
def test_administrator(crud_operations):
    """
    Fixture to create essential mock data required for testing.
    Ensures referential integrity for 'Applications' by creating necessary 'Schemes' records first.
    """
    # Create mock administrators
    yield crud_operations.create_administrator(username="test_admin", password_hash="hashed_password", salt="salt")

@pytest.fixture(scope="function")
def test_scheme(crud_operations):
    """
    Fixture to create essential mock data required for testing.
    Ensures referential integrity for 'Applications' by creating necessary 'Schemes' records first.
    """
    # Create mock schemes
    scheme_data = {
        "name": "Mock Scheme",
        "description": "A mock scheme for testing purposes",
        "eligibility_criteria": {"employment_status": "unemployed"},
        "benefits": {"amount": 500.0},
        "validity_start_date": "2023-01-01",
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
    yield crud_operations.create_applicant(applicant_data)
    
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