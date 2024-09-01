#!/usr/bin/env python3
# Copyright (c) 2024 by Jonathan AW

# This script is run to provision the test Administrator Accounts 
# This script is run only ONCE when the System is deployed to staging.

import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.database import Base, engine, SessionLocal
from dal.models import Administrator, Applicant, HouseholdMember, Scheme, Application, SystemConfiguration
from dal.crud_operations import CRUDOperations
from bl.services.administrator_service import AdministratorService
from dotenv import load_dotenv
from environs import Env
load_dotenv()

connection = engine.connect()
session = SessionLocal(bind=connection)
crud_operations = CRUDOperations(session)
ADMIN_USER_NAME = Env().str("ADMIN_USER_NAME", "ADMIN_USER_NAME is not set.")
ADMIN_USER_PASSWORD = Env().str("ADMIN_USER_PASSWORD", "ADMIN_USER_PASSWORD is not set.")
ADMIN_USER_NAME__2 = Env().str("ADMIN_USER_NAME__2", "ADMIN_USER_NAME__2 is not set.")
ADMIN_USER_PASSWORD__2 = Env().str("ADMIN_USER_PASSWORD__2", "ADMIN_USER_PASSWORD__2 is not set.")
ADMIN_USER_NAME__3 = Env().str("ADMIN_USER_NAME__3", "ADMIN_USER_NAME__3 is not set.")
ADMIN_USER_PASSWORD__3 = Env().str("ADMIN_USER_PASSWORD__3", "ADMIN_USER_PASSWORD__3 is not set.")



def test_administrator(crud_operations):
    """
    Fixture to create essential mock data required for testing.
    Ensures referential integrity for 'Applications' by creating necessary 'Schemes' records first.
    """
    # Create mock administrators
    AS = AdministratorService(crud_operations)
    AS.create_administrator({'username': ADMIN_USER_NAME, 'password_hash': ADMIN_USER_PASSWORD})
    print("username: sa     pwd: sa__Pa55w0rd\n")
    AS.create_administrator({'username': ADMIN_USER_NAME__2, 'password_hash': ADMIN_USER_PASSWORD__2})
    print("username: ba     pwd: ba__Pa55w0rd\n")
    AS.create_administrator({'username': ADMIN_USER_NAME__3, 'password_hash': ADMIN_USER_PASSWORD__3})
    print("username: pm     pwd: pm__Pa55w0rd\n\n")
    
    
if __name__ == "__main__":
    print("Provisioning Test Administrator Accounts...\n")
    print("Test Administrator Accounts:\n")
    test_administrator(crud_operations)
    session.close()
    connection.close()
    print("Administrator Accounts created successfully.")
    print("Please note down these credentials for testing purposes.")
    print("This script is run only ONCE when the System is deployed to staging.")
    print("This script is run to provision the test Administrator Accounts.")