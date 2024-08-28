
# Copyright (c) 2024 by Jonathan AW

from datetime import datetime

def validate_applicant_data(applicant_data: dict) -> tuple[bool, str]:
    """
        Validate applicant data to ensure all required fields are present and correctly formatted.
        Returns True if all fields are valid, False otherwise and provides a reason for failure.
        """
    required_fields = ['name', 'sex', 'employment_status', 'date_of_birth', 'marital_status', 'employment_status_change_date']
    
    for field in required_fields:
        if field not in applicant_data or not applicant_data[field]:
            return False, f"Missing or empty field: {field}"

    # Check if date_of_birth is a valid date
    try:
        datetime.strptime(applicant_data['date_of_birth'], "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format for date_of_birth"
    
    # Check if employment_status_change_date is a valid date
    try:
        datetime.strptime(applicant_data['employment_status_change_date'], "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format for employment_status_change_date"
    
    # Check if sex is valid (M or F)
    if applicant_data['sex'] not in ['M', 'F']:
        return False, "Invalid value for sex"
    
    # Check if employment_status is valid (employed or unemployed)
    if applicant_data['employment_status'] not in ['employed', 'unemployed']:
        return False, "Invalid value for employment_status"
    
    # Check if marital_status is valid (single, married, divorced, widowed)
    if applicant_data['marital_status'] not in ['single', 'married', 'divorced', 'widowed']:
        return False, "Invalid value for marital_status"
    
    return True, "All fields are valid"  
    
