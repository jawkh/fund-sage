# Copyright (c) 2024 by Jonathan AW

# This script is run to provision the production database with all the tables defined in the models.py file.
# This script is run only once when the application is deployed to production.


# Implicit Linkage via Inheritance: The linkage between the models and their schema is implicit via inheritance from Base.
# The Base class is defined in the database.py file and is imported into the models.py file.
# The Base class is used to create the metadata for the database schema and is shared across all models.
from database import Base, engine
from models import Administrator, Applicant, HouseholdMember, Scheme, Application, SystemConfiguration

# Create all tables in the production database
Base.metadata.create_all(bind=engine)
