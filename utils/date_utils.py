# Copyright (c) 2024 by Jonathan AW
""" 
Purpose: Utility functions for date calculations.

"""
from datetime import datetime, timedelta

def calculate_age(birth_date: datetime) -> int:
    """
    Calculate the age of a person given their birth date.
    """
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def is_within_last_months(date: datetime, months: int) -> bool:
    """
    Check if a given date is within the last 'months' months.
    """
    cutoff_date = datetime.now() - timedelta(days=30 * months)
    return date >= cutoff_date
