# Copyright (c) 2024 by Jonathan AW
# config.py
# Purpose: Holds the configuration settings for the Flask application, like database URI, secret keys, and other environment-specific configurations.

# config.py

from environs import Env
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = Env().str('DATABASE_URL', 'DATABASE_URL is not set.') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SECRET_KEY = Env().str('SECRET_KEY') 
    JWT_SECRET_KEY = Env().str('JWT_SECRET_KEY') 
    JWT_ACCESS_TOKEN_EXPIRES = int(Env().str('JWT_ACCESS_TOKEN_EXPIRES', "3600"))  
    SERVER_NAME = Env().str('SERVER_NAME')  
    APPLICATION_ROOT = Env().str('APPLICATION_ROOT', '/')  
    PREFERRED_URL_SCHEME = Env().str('PREFERRED_URL_SCHEME', 'http')  

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = Env().str("DATABASE_URL", "DATABASE_URL is not set.")
    WTF_CSRF_ENABLED = False  

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = Env().str('DATABASE_URL', 'DATABASE_URL is not set.')
