#!/usr/bin/env python3
# Copyright (c) 2024 by Jonathan AW

# This script is run to provision the Supported Schemes for the System. 
# Idempotent script: You can safely run this script multiple times without any side-effects.

# Dependencies: __init_sys_database.py, __data_prep_administrators.py
# run this script from the root project folder after running the dependencies:
# `poetry run python3 bin/__data_prep_supported_schemes.py`

import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dal.database import Base, engine, SessionLocal
from dal.crud_operations import CRUDOperations
from datetime import datetime, timedelta
from typing import List
from bl.services.administrator_service import AdministratorService
from bl.services.scheme_service import SchemeService

connection = engine.connect()
session = SessionLocal(bind=connection)
crud_operations = CRUDOperations(session)
scheme_service = SchemeService(crud_operations)


def retrenchment_assistance_scheme(scheme_service):
    list_of_schemes, count = scheme_service.get_schemes_by_filters(filters={"name": "Retrenchment Assistance Scheme"}, fetch_valid_schemes=False)
    if count == 0:
        # Retrenchment Assistance Scheme
        scheme_data = {
            "name": "Retrenchment Assistance Scheme",
            "description": "A scheme to provide financial support and benefits to individuals who have recently been retrenched from their jobs.",
            "eligibility_criteria": {
                "employment_status": "unemployed",
                "retrechment_period_months": 6,
            },
            "benefits": {
                "cash_assistance": {
                "disbursment_amount": 1000,
                "disbursment_frequency": "One-Off",
                "disbursment_duration_months": None,
                "description": "Cash assistance provided to all eligible applicants."
                },
                "school_meal_vouchers": {
                "amount_per_child": 100,
                "disbursment_frequency": "Monthly",
                "disbursment_duration_months": 12,
                "description": "Meal vouchers provided for each child in the household within the primary school age range (6-11 years old).",
                "eligibility": {
                    "relation": "child",
                    "age_range": {
                    "min": 6,
                    "max": 11
                    }
                }
                },
                "extra_cdc_vouchers": {
                "amount_per_parent": 200,
                "disbursment_frequency": "One-Off",
                "disbursment_duration_months": None,
                "description": "Extra CDC vouchers provided for each elderly parent above the age of 65.",
                "eligibility": {
                    "relation": "parent",
                    "age_threshold": 65
                }
                }
            },
            "validity_start_date": datetime(2024, 1, 1),
            "validity_end_date": None
        }
        scheme_service.create_scheme(scheme_data)
        print("Retrenchment Assistance Scheme created.\n")
    else:
        print("Retrenchment Assistance Scheme already exists.\n")
    
    
def middleaged_reskilling_assistance_scheme(scheme_service):
    # Middle-aged Reskilling Assistance Scheme
    list_of_schemes, count = scheme_service.get_schemes_by_filters(filters={"name": "Middle-aged Reskilling Assistance Scheme"}, fetch_valid_schemes=False)
    if count == 0:
        middleaged_reskilling_assistance_scheme_data = {
            "name": "Middle-aged Reskilling Assistance Scheme",
            "description": "A scheme to provide financial support and benefits to individuals aged 40 and above who are unemployed, encouraging reskilling and upskilling.",
            "eligibility_criteria": {
                "age_threshold": 40,
                "employment_status": "unemployed"
            },
            "benefits": {
                "skillsfuture_credit_top_up": {
                    "disbursment_amount": 1000,
                    "disbursment_frequency": "One-Off",
                    "disbursment_duration_months": None,
                    "description": "One-time Skillsfuture Credit top-up of $1000."
                },
                "study_allowance": {
                    "disbursment_amount": 2000,
                    "disbursment_frequency": "Monthly",
                    "disbursment_duration_months": 6,
                    "description": "Monthly study allowance of $5000 for up to 6 months."
                }
            },
            "validity_start_date": datetime(2024, 1, 1),
            "validity_end_date": None
        }
        scheme_service.create_scheme(middleaged_reskilling_assistance_scheme_data)
        print("Middle-aged Reskilling Assistance Scheme created.\n")
    else:
        print("Middle-aged Reskilling Assistance Scheme already exists.\n")
    
def senior_citizen_assistance_scheme(scheme_service):
    # Retrenchment Assistance Scheme
    list_of_schemes, count = scheme_service.get_schemes_by_filters(filters={"name": "Senior Citizen Assistance Scheme"}, fetch_valid_schemes=False)
    if count == 0:
        senior_citizen_assistance_scheme_data = {
            "name": "Senior Citizen Assistance Scheme",
            "description": "A scheme to provide financial support and benefits to individuals aged 65 and above.",
            "eligibility_criteria": {
                "age_threshold": 65
            },
            "benefits": {
                "cpf_top_up": {
                    "disbursment_amount": 200,
                    "disbursment_frequency": "One-Off",
                    "disbursment_duration_months": None,
                    "description": "One-time CPF top-up of $200."
                },
                "cdc_voucher": {
                    "disbursment_amount": 200,
                    "disbursment_frequency": "One-Off",
                    "disbursment_duration_months": None,
                    "description": "One-time CDC voucher of $200."
                }
            },
            "validity_start_date": datetime(2024, 1, 1),
            "validity_end_date": None
        }
        scheme_service.create_scheme(senior_citizen_assistance_scheme_data)
        print("Senior Citizen Assistance Scheme created.\n")
    else:
        print("Senior Citizen Assistance Scheme already exists.\n")
    
def single_working_mothers_support_scheme(scheme_service):
    list_of_schemes, count = scheme_service.get_schemes_by_filters(filters={"name": "Single Working Mothers Support Scheme"}, fetch_valid_schemes=False)
    if count == 0:       
        single_working_mothers_support_scheme = {
            "name": "Single Working Mothers Support Scheme",
            "description": "A scheme to provide financial support and benefits to single working mothers with young children (18 and below).",
            "eligibility_criteria": {
                "sex": "F",
                "marital_status": ['single', 'divorced', 'widowed'],
                "employment_status": "employed",
                "household_composition": {
                    "relation": "child",
                    "age_range": {
                        "age_threshold": 18
                    }
                }
            },
            "benefits": {
                "cash_assistance": {
                    "disbursment_amount": 1000,
                    "disbursment_frequency": "One-Off",
                    "disbursment_duration_months": None,
                    "description": "Cash assistance provided to all eligible applicants."
                },
                "income_tax_rebates": {
                    "disbursment_amount": 1000,
                    "disbursment_frequency": "annually",
                    "disbursment_duration_months": 60,
                    "description": "Income Tax Rebates given to all eligible applicants for every eligible children in the household."
                }
            },
            "validity_start_date": datetime(2024, 1, 1),
            "validity_end_date": None
        }
        scheme_service.create_scheme(single_working_mothers_support_scheme)
        print("Single Working Mothers Support Scheme created.\n")
    else:
        print("Single Working Mothers Support Scheme already exists.\n")
    
if __name__ == "__main__":
    print("Creating Supported Schemes...\n")
    
    retrenchment_assistance_scheme(scheme_service)
    middleaged_reskilling_assistance_scheme(scheme_service)
    senior_citizen_assistance_scheme(scheme_service)
    single_working_mothers_support_scheme(scheme_service)
    session.close()
    connection.close()
