#!/usr/bin/env python3
# Copyright (c) 2024 by Jonathan AW

# This script is run to provision the Applications for all the Applicants for all the schemes in the database. 
# This script is not idempotent. Running this script each time will create 1 set of additional applications for each applicant for each scheme in the database. (Applicants are allowed to apply for a scheme multiple times if they were not successful in the previous applications. Successful applicants will not be allowed to reapply.)

# Dependencies: __init_sys_database.py, __data_prep_administrators.py, __data_prep_supported_schemes.py, __data_prep_random_applicants.py
# run this script from the root project folder after running the dependencies: 
# `poetry run python3 bin/__data_prep_applications.py`


import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import logging
from dal.database import engine, SessionLocal
from dal.crud_operations import CRUDOperations
from bl.services.application_service import ApplicationService
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.services.applicant_service import ApplicantService
from bl.services.scheme_service import SchemeService
from bl.services.administrator_service import AdministratorService
from api import create_app
from dotenv import load_dotenv
from environs import Env
# Load environment variables (e.g., API_BASE_URL)
load_dotenv()
ADMIN_USER_NAME = Env().str("ADMIN_USER_NAME", "ADMIN_USER_NAME is not set.")
ADMIN_USER_PASSWORD = Env().str("ADMIN_USER_PASSWORD", "ADMIN_USER_PASSWORD is not set.")

connection = engine.connect()
session = SessionLocal(bind=connection)
    
# Setup logging
logging.basicConfig(filename='application_creation.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def create_applications_business_layer():
    """
    Create application records using the Business Layer code.
    """
    # Database setup
    
    crud_operations = CRUDOperations(session)
    # Get the system administrator for creating applicants
    creator = AdministratorService(crud_operations).get_administrator_by_username(ADMIN_USER_NAME)
    application_service = ApplicationService(crud_operations)
    scheme_eligibility_checker_factory = SchemeEligibilityCheckerFactory(session)
    applicant_service = ApplicantService(crud_operations)
    schemes_service = SchemeService(crud_operations)
    
    # Fetch all applicants and schemes from the database
    applicants, totalCount = applicant_service.get_all_applicants()
    schemes = schemes_service.get_all_schemes()

    for applicant in applicants:
        for scheme in schemes:
            try:
                
                # Create application using the business logic layer
                application = application_service.create_application(
                    applicant_id=applicant.id,
                    scheme_id=scheme.id,
                    created_by_admin_id=creator.id,  
                    schemeEligibilityCheckerFactory=scheme_eligibility_checker_factory
                )
                logging.info(f"Application [{application.id}] created for Applicant [{applicant.id}] and Scheme [{scheme.id}] -Status: [{application.status}] -Eligibility: [{application.eligibility_verdict}] -Benefit: [{application.awarded_benefits}]")
                
            except Exception as e:
                logging.error(f"Error creating application for Applicant {applicant.id} and Scheme {scheme.id}: {str(e)}")

def create_applications_api():
    """
    Create application records by making requests to the API endpoint.
    """
    api_base_url = os.getenv('API_BASE_URL')
    app = create_app()
    test_client = app.test_client()
    

    # Establish an application context
    with app.app_context():
        # Step 1: Authenticate to get JWT token
        response = test_client.post('/api/auth/login', json={'username': ADMIN_USER_NAME, 'password': ADMIN_USER_PASSWORD})
        assert response.status_code == 200
        token_data = response.get_json()
        access_token = token_data['access_token']
        response = test_client.get('/api/applicants' ,headers={'Authorization': f'Bearer {access_token}'})
        applicants = response.get_json()

        response = test_client.get('/api/schemes' ,headers={'Authorization': f'Bearer {access_token}'})
        schemes = response.get_json()

        
        for applicant in applicants["data"]:
            for scheme in schemes["data"]:
                try:
                    
                    # Prepare request data for the API
                    data = {
                        "applicant_id": applicant["id"],
                        "scheme_id": scheme["id"],
                    }
                    response = test_client.post('/api/applications', json=data, headers={'Authorization': f'Bearer {access_token}'})
                    data = response.get_json()
                    if response.status_code == 201:
                        logging.info(f"Application created successfully for Applicant [{applicant['name']}] for Scheme [{scheme['name']}].")
                    else:
                        logging.error(f"Failed to create application via API for Applicant [{applicant['name']}] for Scheme [{scheme['name']}]: {response.text}")
                
                except Exception as e:
                    logging.error(f"Error creating application via API for Applicant [{applicant['name']}] and Scheme [{scheme['name']}]: {str(e)}")

def generate_batch_run_report():
    """
    Generate a report summarizing the results of the application creation process.
    """
    # This is a placeholder. You can customize it as needed.
    print("Batch run report:")
    with open('application_creation.log', 'r') as log_file:
        for line in log_file:
            print(line.strip())

if __name__ == "__main__":
    # mode = input("Select mode of operation (1 for Business Layer Code Mode, 2 for API Endpoint Mode): ")
    
    # if mode == "1":
    #     create_applications_business_layer()
    # elif mode == "2":
    #     create_applications_api()
    # else:
    #     print("Invalid mode selected. Please choose 1 or 2.")
    print("Provisioning Applications for all existing Applicants for all supported schemes..\n")
    print ("This script is not idempotent. Running this script each time will create 1 set of additional applications for each applicant for each scheme in the database.\nApplicants are allowed to apply for a scheme multiple times if they were not successful in the previous applications.\nSuccessful applicants will not be allowed to reapply.\n")
    create_applications_business_layer() 
    
    # Close the session and connection
    session.close()
    connection.close()

    # Generate the batch run report
    generate_batch_run_report()
