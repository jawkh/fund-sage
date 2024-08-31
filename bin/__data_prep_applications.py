#!/usr/bin/env python3
# Copyright (c) 2024 by Jonathan AW

# This script is run to provision the test Applications  
# This script is run only ONCE when the System is deployed to staging.

import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.database import Base, engine, SessionLocal
from dal.models import Administrator, Applicant, HouseholdMember, Scheme, Application, SystemConfiguration
from dal.crud_operations import CRUDOperations
from bl.services.administrator_service import AdministratorService



connection = engine.connect()
session = SessionLocal(bind=connection)
crud_operations = CRUDOperations(session)

