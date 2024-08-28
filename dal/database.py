# Copyright (c) 2024 by Jonathan AW

from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv
# load_dotenv()

# Load environment variables
DATABASE_URL = Env().str("DATABASE_URL", "DATABASE_URL is not set. ") 

# Ensure the DATABASE_URL is set correctly
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please configure your environment variables.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models using the declarative base
Base = declarative_base()

