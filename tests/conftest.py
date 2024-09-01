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
from datetime import datetime, timedelta 
from dal.crud_operations import CRUDOperations
from dal.system_config import SystemConfig
from dal.database import Base, SessionLocal
from bl.services.applicant_service import ApplicantService
from bl.services.scheme_service import SchemeService
from bl.services.application_service import ApplicationService
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables
load_dotenv()
API_TEST_DATABASE_URL = Env().str("DATABASE_URL", "DATABASE_URL is not set.") # API Test DB - Used for both automated pytest and manual testings using PostMan
TEST_DATABASE_URL = Env().str("TEST_DATABASE_URL", "TEST_DATABASE_URL is not set.") # For non-API automated pytest only. DB Tables will be provisioned and destroyed for each test session. 

# Create a new engine for the test database
test_engine = create_engine(TEST_DATABASE_URL)
api_test_engine = create_engine(API_TEST_DATABASE_URL)
# Create a configured "Session" class for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
ApiTestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=api_test_engine)



@pytest.fixture(scope="session", autouse=True)
def initialize_database(setup_emphemeral_database, setup_api_test_database): # Ensure the setup_emphemeral_database and setup_api_test_database fixtures are called before this fixture
    pass

@pytest.fixture(scope="session")
def setup_emphemeral_database():
    """
    Set up the database Tables once for the entire test session.
    This fixture will create all the tables at the start of the session and drop them at the end.
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # # Drop all tables after the test session is complete
    Base.metadata.drop_all(bind=test_engine) 

@pytest.fixture(scope="session")
def setup_api_test_database():
    """
    Set up the database Tables once and for all.
    Database Tables will not be destroyed after the test session.
    """
    # Create all tables
    Base.metadata.create_all(bind=api_test_engine)
    yield

@pytest.fixture(scope="session")
def test_db_connection():
    """
    Creates a single database connection for the test session.
    """
    connection = test_engine.connect()
    yield connection
    connection.close()
    
@pytest.fixture(scope="session")
def api_test_db_connection():
    """
    Creates a single database connection for the test session.
    """
    connection = api_test_engine.connect()
    yield connection
    connection.close()

@pytest.fixture(scope="function")
def test_db(test_db_connection):
    """
    Creates a new database session for each test function, using a transaction that rolls back after each test.
    """
    transaction = test_db_connection.begin()  # Begin a new transaction on the connection
    session = TestingSessionLocal(bind=test_db_connection)  # Bind the session to the same connection
    try:
        yield session  # This is where the test using the session will run
        session.flush()  # Ensure all changes are flushed to the database
        transaction.rollback()  # Rollback the transaction to clean up after the test
    finally:
        session.close()  # Close the session to release the connection

@pytest.fixture(scope="function")
def api_test_db(api_test_db_connection):
    """
    Creates a new database session for each test function, using a transaction that rolls back after each test.
    """
    transaction = api_test_db_connection.begin()  # Begin a new transaction on the connection
    session = ApiTestingSessionLocal(bind=api_test_db_connection)  # Bind the session to the same connection
    try:
        yield session  # This is where the test using the session will run
        session.flush()  # Ensure all changes are flushed to the database
    finally:
        session.close()  # Close the session to release the connection

@pytest.fixture(scope="function")
def api_test_db__NonTransactional(api_test_db_connection):
    """
    Creates a new database session for each test function. Will not roll back after each test.
    """
    session = ApiTestingSessionLocal(bind=api_test_db_connection)  # Bind the session to the api test db connection
    try:
        yield session  # This is where the test using the session will run
        session.flush()  # Ensure all changes are flushed to the database
    finally:
        session.close()  # Close the session to release the connection

@pytest.fixture(scope="function")
def crud_operations(test_db):
    """
    Fixture to provide a CRUDOperations instance with a testing session. (using a transaction that rolls back after each test)
    """
    yield CRUDOperations(test_db)
    

    
    
@pytest.fixture(scope="function")
def scheme_eligibility_checker_factory(test_db):
    """
    Fixture to provide a SchemeEligibilityCheckerFactory instance with a testing session. (using a transaction that rolls back after each test)
    """
    yield SchemeEligibilityCheckerFactory(test_db)

@pytest.fixture(scope="function")
def scheme_manager(crud_operations, scheme_eligibility_checker_factory):
    """
    Fixture to provide a SchemesManager instance with dependencies for testing.
    """
    yield SchemesManager(crud_operations, scheme_eligibility_checker_factory)
    
    

@pytest.fixture(scope="function")
def system_config(test_db):
    """
    Fixture to provide a system_config instance with a testing session. (using a transaction that rolls back after each test)
    """
    yield SystemConfig(test_db)

@pytest.fixture(scope="function")
def scheme_service(crud_operations):
    """
    Fixture to provide a SchemeService instance for testing.
    """
    yield SchemeService(crud_operations)

@pytest.fixture(scope="function")
def applicant_service(crud_operations):
    """
    Fixture to provide an ApplicantService instance with dependencies for testing.
    """
    yield ApplicantService(crud_operations)

@pytest.fixture(scope="function")
def application_service(crud_operations):
    """
    Fixture to provide an ApplicationService instance with dependencies for testing.
    """
    yield ApplicationService(crud_operations)

@pytest.fixture(scope="function")
def test_administrator(crud_operations):
    """
    Fixture to create essential mock data required for testing.
    Ensures referential integrity for 'Applications' by creating necessary 'Schemes' records first.
    """
    try:
    # Create mock administrators
        yield crud_operations.create_administrator(username="test_admin", password_hash="correct_password", salt="salt")
    except SQLAlchemyError as e:
        print(e)
        raise e
    
@pytest.fixture(scope="function")
def retrenchment_assistance_scheme(scheme_service):
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
    # yield crud_operations.create_scheme(scheme_data)
    yield scheme_service.create_scheme(scheme_data)
    
@pytest.fixture(scope="function")
def middleaged_reskilling_assistance_scheme(scheme_service):
    """
    Fixture to create essential mock data required for testing.
    Ensures referential integrity for 'Applications' by creating necessary 'Schemes' records first.
    """
    # Retrenchment Assistance Scheme
    middleaged_reskilling_assistance_scheme_data = {
        "name": "Middle-aged Reskilling Assistance Scheme",
        "description": "A scheme to provide financial support and benefits to individuals aged 40 and above who are unemployed, encouraging reskilling and upskilling.",
        "eligibility_criteria": {
            "age_threshold": 40,
            "employment_status": "unemployed"
        },
        "benefits": {
            "skillsfuture_credit_top_up": {
                "disbursment_amount": 1000,
                "disbursment_frequency": "One-Off",
                "disbursment_duration_months": None,
                "description": "One-time Skillsfuture Credit top-up of $1000."
            },
            "study_allowance": {
                "disbursment_amount": 2000,
                "disbursment_frequency": "Monthly",
                "disbursment_duration_months": 6,
                "description": "Monthly study allowance of $5000 for up to 6 months."
            }
        },
        "validity_start_date": datetime(2024, 1, 1),
        "validity_end_date": None
    }
    yield scheme_service.create_scheme(middleaged_reskilling_assistance_scheme_data)
    
@pytest.fixture(scope="function")
def senior_citizen_assistance_scheme(scheme_service):
    """
    Fixture to create essential mock data required for testing.
    Ensures referential integrity for 'Applications' by creating necessary 'Schemes' records first.
    """
    # Retrenchment Assistance Scheme
    senior_citizen_assistance_scheme_data = {
        "name": "Senior Citizen Assistance Scheme",
        "description": "A scheme to provide financial support and benefits to individuals aged 65 and above.",
        "eligibility_criteria": {
            "age_threshold": 65
        },
        "benefits": {
            "cpf_top_up": {
                "disbursment_amount": 200,
                "disbursment_frequency": "One-Off",
                "disbursment_duration_months": None,
                "description": "One-time CPF top-up of $200."
            },
            "cdc_voucher": {
                "disbursment_amount": 200,
                "disbursment_frequency": "One-Off",
                "disbursment_duration_months": None,
                "description": "One-time CDC voucher of $200."
            }
        },
        "validity_start_date": datetime(2024, 1, 1),
        "validity_end_date": None
    }
    yield scheme_service.create_scheme(senior_citizen_assistance_scheme_data)

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
    
    
    # Assuming these are additions to conftest.py



@pytest.fixture(scope="function")
def multiple_applicants(crud_operations, test_administrator):
    """Fixture to create multiple applicants for pagination testing."""
    applicants_data = [
        {"name": "Bob Johnson", "employment_status": "unemployed", "sex": "M", "date_of_birth": datetime(1970, 8, 20), "marital_status": "married", "created_by_admin_id": test_administrator.id},
        {"name": "Alice Smith", "employment_status": "employed", "sex": "F", "date_of_birth": datetime(1985, 5, 1), "marital_status": "single", "created_by_admin_id": test_administrator.id},
        {"name": "Carol White", "employment_status": "employed", "sex": "F", "date_of_birth": datetime(1992, 11, 15), "marital_status": "single", "created_by_admin_id": test_administrator.id},
        {"name": "David Black", "employment_status": "unemployed", "sex": "M", "date_of_birth": datetime(1988, 2, 10), "marital_status": "single", "created_by_admin_id": test_administrator.id},
        {"name": "Eve Green", "employment_status": "employed", "sex": "F", "date_of_birth": datetime(1995, 4, 25), "marital_status": "married", "created_by_admin_id": test_administrator.id},
    ]
    
    for data in applicants_data:
        crud_operations.create_applicant(data)

    yield applicants_data  # Yielding data for further verification if needed





@pytest.fixture(scope='function')
def setup_applicants(applicant_service: ApplicantService, test_administrator):
    """
    Fixture to create 20 diverse applicants with household members for testing.
    
    Args:
        applicant_service (ApplicantService): An instance of the ApplicantService.

    Returns:
        List[int]: A list of created applicant IDs for further use in tests.
    """
    applicants_data = []
    household_data = []

    # Create diverse applicants
    for i in range(20):
        applicant_data = {
            "name": f"Applicant {i}",
            "employment_status": "employed" if i % 2 == 0 else "unemployed",
            "sex": "M" if i % 2 == 0 else "F",
            "date_of_birth": datetime.now() - timedelta(days=365 * (20 + i)),  # Ages between 20 to 40
            "marital_status": "single" if i % 3 == 0 else "married",
            "created_by_admin_id": test_administrator.id,
        }

        # Create household members for each applicant
        household_members_data = []
        if i % 2 == 0:
            household_members_data.append({
                "name": f"Child {i}",
                "relation": "child",
                "date_of_birth": datetime.now() - timedelta(days=365 * 5),  # Child age 5
                "employment_status": "unemployed",
                "sex": "F" if i % 2 == 0 else "M",
            })
        if i % 3 == 0:
            household_members_data.append({
                "name": f"Spouse {i}",
                "relation": "spouse",
                "date_of_birth": datetime.now() - timedelta(days=365 * (20 + i)),  # Similar age to applicant
                "employment_status": "employed",
                "sex": "F" if i % 2 != 0 else "M",
            })

        applicants_data.append(applicant_data)
        household_data.append(household_members_data)

    # Create applicants and household members using the service
    created_applicants = []
    for applicant_data, household_members_data in zip(applicants_data, household_data):
        created_applicant = applicant_service.create_applicant(applicant_data, household_members_data)
        created_applicants.append(created_applicant.id)

    yield created_applicants

#################################################
# Test Fixtures for Flask Application and Client
from api import create_app

@pytest.fixture(scope='module')
def api_test_client():
    
    app = create_app()
    testing_client = app.test_client()

    # Establish an application context
    with app.app_context():
        yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def api_test_db__NonTransactional():
    # Setup the database for tests
    session = SessionLocal()

    # Initialize the database here
    # e.g., insert test data

    yield session  # this is where the testing happens!

    # Teardown the database after tests
    session.close()

import uuid
from bl.services.administrator_service import AdministratorService


@pytest.fixture
def api_test_admin(api_test_db__NonTransactional):
    """
    Fixture to create and clean up a temporary administrator for testing.
    """
    
    crud_operations__NonTransactional = CRUDOperations(api_test_db__NonTransactional)
    admin_service = AdministratorService(crud_operations__NonTransactional)
    username = str(uuid.uuid4())  # Generate a unique username for each test run
    temp_admin = admin_service.create_administrator({'username': username, 'password_hash': 'Helloworld123!'})

    yield temp_admin  # Provide the created admin for the test

    # Cleanup after the test
    admin_service.delete_administrator(temp_admin.id)
    assert admin_service.get_administrator_by_id(temp_admin.id) is None
    
class helper:
    def print_response(response):
        """
        Helper function to print the response data in a readable JSON format.
        """
        import json  # Import json for pretty-printing

        try:
            # Try to pretty print the JSON response
            print(json.dumps(response.get_json(), indent=4))
        except (TypeError, ValueError):
            # If the response is not in JSON format, print the raw data
            print(response.data)
            
    def get_JWT_via_user_login(test_client, api_test_create_temp_admin):
        # Step 1: Authenticate to get JWT token
        response = test_client.post('/api/auth/login', json={'username': api_test_create_temp_admin.username, 'password': 'Helloworld123!'})
        assert response.status_code == 200
        token_data = response.get_json()
        assert 'access_token' in token_data
        access_token = token_data['access_token']
        return access_token