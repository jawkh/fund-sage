# Copyright (c) 2024 by Jonathan AW
# config.py
# Purpose: Holds the configuration settings for the Flask application, like database URI, secret keys, and other environment-specific configurations.

# config.py

from environs import Env
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = Env().str('SECRET_KEY', "SECRET_KEY is not set.")
    SQLALCHEMY_DATABASE_URI = Env().str('DATABASE_URL', 'DATABASE_URL is not set.')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = Env().str('JWT_SECRET_KEY', 'JWT_SECRET_KEY is not set.')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = Env().str("TEST_DATABASE_URL", "TEST_DATABASE_URL is not set.")
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = Env().str('DATABASE_URL', 'DATABASE_URL is not set.')
