#!/usr/bin/env python3
# Copyright (c) 2024 by Jonathan AW

# This script is run to auto-provision the test Administrator Accounts 
# Use this to intialize the test Administrator Accounts in the database
# Idempotent script: You can safely run this script multiple times without any side-effects.

# Dependency: __init_sys_database.py
# run this script from the root project folder after running the dependencies:
# `poetry run python3 bin/__data_prep_administrators.py`

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



def provision_administrators(crud_operations) -> int:
    # Create administrators as part of databases initialization
    i = 0
    
    AS = AdministratorService(crud_operations)
    try :
        AS.create_administrator({'username': ADMIN_USER_NAME, 'password_hash': ADMIN_USER_PASSWORD})
        print(f"username: {ADMIN_USER_NAME}     pwd: {ADMIN_USER_PASSWORD}\n")
        i += 1
    except Exception as e:
        print(f"username: {ADMIN_USER_NAME} already exists.\n")
    try:
        AS.create_administrator({'username': ADMIN_USER_NAME__2, 'password_hash': ADMIN_USER_PASSWORD__2})
        print(f"username: {ADMIN_USER_NAME__2}     pwd: {ADMIN_USER_PASSWORD__2}\n")
        i += 1
    except Exception as e:
        print(f"username: {ADMIN_USER_NAME__2} already exists.\n")
    try:
        AS.create_administrator({'username': ADMIN_USER_NAME__3, 'password_hash': ADMIN_USER_PASSWORD__3})
        print(f"username: {ADMIN_USER_NAME__3}     pwd: {ADMIN_USER_PASSWORD__3}\n\n")
        i += 1
    except Exception as e:
        print(f"username: {ADMIN_USER_NAME__3} already exists.\n\n")
    return i

if __name__ == "__main__":
    print("Provisioning Administrator Accounts...\n")
    i = provision_administrators(crud_operations)
    session.close()
    connection.close()
    print(f"{i}x Administrator Accounts created successfully.")
    print("Please note down these credentials for testing purposes.")
    print("This script is run only ONCE when the System is deployed to staging.")
    print("This script is run to provision the test Administrator Accounts.")