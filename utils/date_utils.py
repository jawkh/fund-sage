# Copyright (c) 2024 by Jonathan AW
""" 
Purpose: Utility functions for date calculations.

"""
from datetime import date
from dateutil.relativedelta import relativedelta


from datetime import datetime

def calculate_age(birth_date: date) -> int:
    """
    Calculate the age of a person given their birth date.
    
    Args:
        birth_date (date): The birth date of the person.
    
    Returns:
        int: The calculated age of the person.
    """
    today = date.today()
    age = today.year - birth_date.year
    
    # If the birth date has not occurred yet this year, subtract one from the age
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
        
    return age


def is_within_last_months(date: datetime, months: int) -> bool:
    """
    Check if a given date is within the last 'months' months, ignoring the time component.
    """
    cutoff_date = (datetime.now() - relativedelta(months=months)).date()
    return date.date() >= cutoff_date


def is_future_date(date: datetime) -> bool:
    """
    Check if a given date is in the future, ignoring the time component.
    
    Args:
        date (datetime): The date to check.

    Returns:
        bool: True if the date is in the future, False otherwise.
    """
    today = datetime.now().date()
    return date.date() > today
