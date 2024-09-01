#!/usr/bin/env python3
# Copyright (c) 2024 by Jonathan AW

# This script is run to provision the test Applicant Accounts 
# This script is run only ONCE when the System is deployed to staging.

# Dependency: __data_prep_administrators.py

import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.database import Base, engine, SessionLocal
from dal.models import Administrator, Applicant, HouseholdMember, Scheme, Application, SystemConfiguration
from dal.crud_operations import CRUDOperations
from datetime import datetime, timedelta
from typing import List
from bl.services.applicant_service import ApplicantService
from bl.services.administrator_service import AdministratorService
from random import randint
from datetime import datetime, timedelta
from dotenv import load_dotenv
from environs import Env
# Load environment variables (e.g., API_BASE_URL)
load_dotenv()
ADMIN_USER_NAME = Env().str("ADMIN_USER_NAME", "ADMIN_USER_NAME is not set.")


connection = engine.connect()
session = SessionLocal(bind=connection)
crud_operations = CRUDOperations(session)

# Get the system administrator for creating applicants
creator = AdministratorService(crud_operations).get_administrator_by_username(ADMIN_USER_NAME)

def setup_applicants(applicant_service: ApplicantService, creator) -> List[int]:
    """
    Create 20 diverse applicants with household members for testing.
    
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
            "employment_status": "employed" if i % 2 == 0 else "unemployed", # Half employed, half unemployed
            "employment_status_change_date": datetime.now() - timedelta(days=30 * randint(3, 7)),  # Employed/Unemployed for 3 to 7 months
            "sex": "M" if i % 2 == 0 else "F", # Half Male, Half Female
            "date_of_birth": datetime.now() - timedelta(days=365 * randint(35, 80)),  # Ages between 35 to 80 yo
            "marital_status": "married" if i % 2 == 0 else "single", # Half married, half single
            "created_by_admin_id": creator.id,
        }

        # Create household members for each applicant
        household_members_data = []
        if i % 2 == 0:
            household_members_data.append({
                "name": f"Child A",
                "relation": "child",
                "date_of_birth": datetime.now() - timedelta(days=365 * randint(5, 19)),  # Ages between 5 to 19 yo
                "employment_status": "unemployed",
                "sex": "F" if i % 2 == 0 else "M"
            })
        if i % 2 == 0:
            household_members_data.append({
                "name": f"Child B",
                "relation": "child",
                "date_of_birth": datetime.now() - timedelta(days=365 * randint(5, 19)),  # Ages between 5 to 19 yo
                "employment_status": "unemployed",
                "sex": "F" if i % 2 == 0 else "M"
            })
        if i % 3 == 0:
            household_members_data.append({
                "name": f"Spouse",
                "relation": "spouse",
                "date_of_birth": datetime.now() - timedelta(days=365 * randint(35, 80)),  # Ages between 35 to 80 yo (similar to applicant)
                "employment_status": "employed",
                "sex": "F" if i % 2 != 0 else "M" # Opposite Sex as Applicant
            })
        if i % 2 == 0:
            household_members_data.append({
                "name": f"Parent",
                "relation": "parent",
                "date_of_birth": datetime.now() - timedelta(days=365 * randint(55, 100)),  # Ages between 55 to 100 yo
                "employment_status": "unemployed",
                "sex": "F" if i % 2 == 0 else "M"
            })

        applicants_data.append(applicant_data)
        household_data.append(household_members_data)

    # Create applicants and household members using the service
    created_applicants = []
    for applicant_data, household_members_data in zip(applicants_data, household_data):
        created_applicant = applicant_service.create_applicant(applicant_data, household_members_data)
        created_applicants.append(created_applicant.id)
        print(f"Applicant [{created_applicant.name}] created.\n")

    
if __name__ == "__main__":
    print("Creating Applicant Accounts...\n")
    AS = ApplicantService(crud_operations)
    setup_applicants(AS, creator)
    session.close()
    connection.close()
    print("Applicant Accounts created successfully.")
    print("This script is run only ONCE when the System is deployed to staging.")
    print("This script is run to provision the test Applicant Accounts.")