#!/usr/bin/env python3
# Copyright (c) 2024 by Jonathan AW

# This script is run to provision the staging database with all the tables defined in the ORM Models used by this System. ORM Models are defined in dal/models.py file.
# This script is run only ONCE when the application is deployed to staging.

# Implicit Linkage via Inheritance: The linkage between the models and their schema is implicit via inheritance from Base.
# The Base class is defined in the database.py file and is imported into the models.py file.
# The Base class is used to create the metadata for the database schema and is shared across all models.
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.database import Base, engine
from dal.models import Administrator, Applicant, HouseholdMember, Scheme, Application, SystemConfiguration

# Create all tables in the staging database
print("Creating all tables in the staging database...\n")
Base.metadata.create_all(bind=engine)
print("All tables created successfully.\n")
