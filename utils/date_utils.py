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


from datetime import datetime, date

def convert_to_datetime(obj):
    """
    Convert an object to a datetime object if it's a string representing a date or datetime.
    If the object is already a datetime object, return it as is.
    
    Args:
    obj (Any): The object to check and convert if necessary.
    
    Returns:
    datetime: A datetime object if conversion was necessary, otherwise the original datetime object.
    
    
    # Example Usage:
    # print(convert_to_datetime('2010-04-10T00:00:00'))  # Converts to datetime object
    # print(convert_to_datetime('2010-04-10'))           # Converts to datetime object
    # print(convert_to_datetime(datetime.now()))         # Returns the datetime object unchanged
    # print(convert_to_datetime(date.today()))           # Converts date object to datetime

    """
    if obj is None:
        return None # Return None if the object is None
    
    # Check if the object is already a datetime instance
    if isinstance(obj, datetime):
        return obj

    # If the object is a date instance but not a datetime instance, convert it to datetime
    if isinstance(obj, date) and not isinstance(obj, datetime):
        return datetime.combine(obj, datetime.min.time())

    # Check if the object is a string
    if isinstance(obj, str):
        # Attempt to parse the string to a datetime object
        try:
            # First try parsing with a common datetime format (ISO 8601)
            return datetime.strptime(obj, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            try:
                # Then try a common date format if the first failed
                return datetime.strptime(obj, '%Y-%m-%d')
            except ValueError:
                # If both parsing attempts fail, raise an error
                raise ValueError("String is not in a recognized date/datetime format.")
    
    # If object is not a datetime, date, or string, raise an error
    raise TypeError("Object is neither a datetime, date, nor a string representing a date or datetime.")

