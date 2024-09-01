
# Copyright (c) 2024 by Jonathan AW

import pytest
from datetime import datetime, date
from utils.date_utils import convert_to_datetime

def test_convert_valid_datetime():
    """
    Test that a valid datetime object is returned unchanged.
    """
    dt = datetime(2024, 9, 1, 12, 30, 0)
    assert convert_to_datetime(dt) == dt

def test_convert_valid_date():
    """
    Test that a valid date object is converted to a datetime object with time set to 00:00:00.
    """
    d = date(2024, 9, 1)
    result = convert_to_datetime(d)
    assert isinstance(result, datetime)
    assert result == datetime(2024, 9, 1, 0, 0, 0)

def test_convert_valid_datetime_string():
    """
    Test that a valid ISO 8601 datetime string is correctly converted to a datetime object.
    """
    dt_str = '2010-04-10T00:00:00'
    expected_dt = datetime(2010, 4, 10, 0, 0, 0)
    result = convert_to_datetime(dt_str)
    assert isinstance(result, datetime)
    assert result == expected_dt

def test_convert_valid_date_string():
    """
    Test that a valid date string is correctly converted to a datetime object with time set to 00:00:00.
    """
    d_str = '2010-04-10'
    expected_dt = datetime(2010, 4, 10, 0, 0, 0)
    result = convert_to_datetime(d_str)
    assert isinstance(result, datetime)
    assert result == expected_dt

def test_invalid_datetime_string_format():
    """
    Test that an invalid datetime string raises a ValueError.
    """
    invalid_dt_str = '10-04-2010'
    with pytest.raises(ValueError, match="String is not in a recognized date/datetime format."):
        convert_to_datetime(invalid_dt_str)

def test_non_date_string():
    """
    Test that a non-date string raises a ValueError.
    """
    non_date_str = 'not a date'
    with pytest.raises(ValueError, match="String is not in a recognized date/datetime format."):
        convert_to_datetime(non_date_str)

def test_invalid_type_integer():
    """
    Test that an invalid type (integer) raises a TypeError.
    """
    with pytest.raises(TypeError, match="Object is neither a datetime, date, nor a string representing a date or datetime."):
        convert_to_datetime(123456)

def test_invalid_type_list():
    """
    Test that an invalid type (list) raises a TypeError.
    """
    with pytest.raises(TypeError, match="Object is neither a datetime, date, nor a string representing a date or datetime."):
        convert_to_datetime(['2010-04-10'])

def test_date_string_with_time_information():
    """
    Test that a date string with time information is correctly converted to a datetime object.
    """
    d_str_with_time = '2010-04-10 12:30:45'
    with pytest.raises(ValueError, match="String is not in a recognized date/datetime format."):
        convert_to_datetime(d_str_with_time)

def test_empty_string():
    """
    Test that an empty string raises a ValueError.
    """
    with pytest.raises(ValueError, match="String is not in a recognized date/datetime format."):
        convert_to_datetime('')

def test_null_input():
    """
    Test that a None input raises a TypeError.
    """
    assert None == convert_to_datetime(None)
