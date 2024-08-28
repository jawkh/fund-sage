

# Copyright (c) 2024 by Jonathan AW

import logging

def log_error(message: str):
    """
    Log an error message using Python's logging framework.
    """
    logging.error(message)

def handle_error(exception: Exception, custom_message: str = ""):
    """
    Standardized error handling function that logs the error and raises an exception.
    """
    log_error(f"{custom_message}: {str(exception)}")
    raise exception
