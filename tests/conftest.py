# Copyright (c) 2024 by Jonathan AW

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dal.crud_operations import CRUDOperations
# from dotenv import load_dotenv
# load_dotenv()

from environs import Env


# Implicit Linkage via Inheritance: The linkage between the models and their schema is implicit via inheritance from Base.
# The Base class is defined in the database.py file and is imported into the models.py file.
# The Base class is used to create the metadata for the database schema and is shared across all models.
from dal.database import Base
from dal.models import Administrator, Applicant, HouseholdMember, Scheme, Application, SystemConfiguration


# Load environment variables
TEST_DATABASE_URL = Env().str("TEST_DATABASE_URL", "TEST_DATABASE_URL is not set. ") 

# Ensure the DATABASE_URL is set correctly
if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL is not set. Please configure your environment variables.")

# Create a new engine for the test database
# The engine is used to connect to the test_database and execute SQL commands
test_engine = create_engine(TEST_DATABASE_URL)

# Create a configured "Session" class for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="module")
def test_db():
    """
    Set up a fresh database for testing. 
    This fixture is used to create a session, yield it for the test, and then clean up by dropping all tables.
    """
    # Create all tables in the test database using the ORMBase metadata
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db  # Provide the fixture value
    finally:
        Base.metadata.drop_all(bind=test_engine)  # Drop all tables to clean up after testing
        db.close()  # Close the session after the test is complete
        
@pytest.fixture(scope="module")
def crud_operations(test_db):
    """
    Fixture to provide a CRUDOperations instance with a testing session.
    """
    return CRUDOperations(test_db)

@pytest.fixture(scope="module")
def setup_mock_data(crud_operations):
    """
    Fixture to create essential mock data required for testing.
    Ensures referential integrity for 'Applications' by creating necessary 'Schemes' records first.
    """
    # Create mock administrators
    """
    Test creating a new administrator and verify the administrator details.
    """
    admin = crud_operations.create_administrator(username="test_admin", password_hash="hashed_password", salt="salt")   
     
    # Create mock schemes
    scheme_data = {
        "name": "Mock Scheme",
        "description": "A mock scheme for testing purposes",
        "eligibility_criteria": {"employment_status": "unemployed"},
        "benefits": {"amount": 500.0},
        "validity_start_date": "2023-01-01",
        "validity_end_date": None
    }
    crud_operations.create_scheme(scheme_data)
    yield  # Ensure this fixture is properly sequenced
