# Copyright (c) 2024 by Jonathan AW
# administrator_service.py
# This file contains the implementation of the AdministratorService class, which provides business logic related to administrators.
"""
# Summary:
The AdministratorService class provides a comprehensive implementation of the business logic related to administrators. 

# Design Patterns:
1. Clear Separation of Concerns:
- The class is focused on handling administrator-related operations, adhering to the Single Responsibility Principle (SRP).

2. Data Validation:
- The class uses the validate_administrator_data function to validate administrator data before creating or updating an administrator, ensuring data integrity and consistency.

3. Error Handling:
- Custom exceptions (InvalidAdministratorDataException, AdministratorNotFoundException) are used to handle specific error scenarios related to administrators, providing clear and meaningful feedback.

4. Dependency Injection:
- The class takes a CRUDOperations object as a dependency, allowing for better testability and separation of concerns.

5. Use of Type Annotations:
- The use of type annotations for method arguments and return types enhances code readability and maintainability.

6. Security Measures:
- The class implements security measures such as password hashing, password verification, and account locking to enhance the security of administrator accounts.

7. Encapsulation:
- The class encapsulates the logic for managing administrators, providing a clean interface for interacting with administrator data.

8. Readability and Maintainability:
- The class structure and method names are well-organized, making the code easy to understand and maintain.

"""

import hashlib
import os
import string
import random
from typing import Optional, List
from dal.crud_operations import CRUDOperations
from dal.models import Administrator
from exceptions import InvalidAdministratorDataException, AdministratorNotFoundException 
from environs import Env
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv()
from utils.data_validation import validate_administrator_data

class AdministratorService:
    # Load environment variables

    """
    Service class to handle all business logic related to administrators.
    """
    MAX_PASSWORD_RETRIES = int(Env().str("MAX_PASSWORD_RETRIES", "5")) # Maximum number of consecutive failed login attempts 
    
    def __init__(self, crud_operations: CRUDOperations):
        self.crud_operations = crud_operations
        # self.MAX_PASSWORD_RETRIES = int(Env().str("MAX_PASSWORD_RETRIES", "5")) # Maximum number of consecutive failed login attempts 
        self.PASSWORD_RETRIES_TIME_WINDOW_MINUTES = int(Env().str("PASSWORD_RETRIES_TIME_WINDOW_MINUTES", "10"))
        
    def get_administrator_by_id(self, admin_id: int) -> Administrator:
        """
        Retrieve an administrator by ID.
        """
        return self.crud_operations.get_administrator(admin_id) # Check if the admin exists. 
    
    def get_administrator_by_username(self, username: str) -> Administrator:
        """
        Retrieve an administrator by username.
        """
        username = username.strip().lower() # Remove leading and trailing whitespaces. Sets username to lowercase
        return self.__get_admin_by_username(username) # Check if the admin exists. 


    def create_administrator(self, admin_data: dict) -> Administrator:
        
        if ("password_hash" in admin_data):
            admin_data["password_hash"] = admin_data["password_hash"].strip() # Remove leading and trailing whitespaces
        
        # Generate a salt
        salt = os.urandom(16).hex()
        raw_password = admin_data["password_hash"] # Extract the raw password from the data
        # Hash the password with the salt
        password_hash = self.__hash_password(raw_password, salt)
        
        if ("username" in admin_data): 
            admin_data["username"] = admin_data["username"].strip().lower() # Remove leading and trailing whitespaces. Sets username to lowercase
            
        admin_data["password_hash"] = password_hash # Replace the raw password with the hashed password
        admin_data["salt"] = salt
        
        isValid, msg = validate_administrator_data(admin_data, True)
        if not isValid:
            raise InvalidAdministratorDataException(msg)

        return self.crud_operations.create_administrator(admin_data["username"], password_hash, salt)

    def update_administrator(self, admin_id: int, update_data: dict) -> Administrator:
        """
        Update an administrator's details.
        """
        isValid, msg = validate_administrator_data(update_data, False)
        if not isValid:
            raise InvalidAdministratorDataException(msg)
        return self.crud_operations.update_administrator(admin_id, update_data)

    def delete_administrator(self, admin_id: int) -> None:
        """
        Delete an administrator record.
        """
        self.crud_operations.delete_administrator(admin_id)

    def get_all_administrators(self) -> List[Administrator]:
        """
        Retrieve all administrators.
        """
        return self.crud_operations.get_administrators_by_filters({})

    # Security methods
    def verify_login_credentials(self, username: str, password: str) -> tuple[Optional[Administrator], str]:
        """
        Verify login credentials for an administrator.
        """
        if not username or not password:
            return None, "Missing required parameters [username / password]"
        
        if username:
            username = username.strip().lower() # Remove leading and trailing whitespaces. Sets username to lowercase
        if password:
            password = password.strip() # Remove leading and trailing whitespaces
        
        try:
            admin = self.__get_admin_by_username(username) # Check if the admin exists. Raises an exception if not found.
        except AdministratorNotFoundException as e:
            return None, str(e)
            
        if admin: 
            if not admin.account_locked:
                if self.__verify_password(admin.password_hash, password, admin.salt):
                    # Reset login failure counters on successful login
                    self.__reset_login_failure_counters(admin.id)
                    return admin, f"Welcome [{admin.username}]!"
                else:
                    # Increment login failure counters
                    consecutive_failed_logins = self.__increment_login_failure_counter(admin.id)
                    mesg = f"Invalid password. {self.MAX_PASSWORD_RETRIES - consecutive_failed_logins} attempts remaining."
            else:
                mesg = "Account is locked. Please contact the administrator."
        else:
            mesg = "Invalid username. Please try again."
        return None, mesg
    
    def __increment_login_failure_counter(self, admin_id: int) -> int:
        """
        Increment the consecutive_failed_logins counter and set failed_login_starttime.
        Lock the account if necessary, considering the retry time window.
        """
        admin = self.__get_admin_by_id(admin_id) # Check if the admin exists. Raises an exception if not found.
        current_time = datetime.now(timezone.utc)  # Use timezone-aware datetime
        current_count = admin.consecutive_failed_logins
        time_window = timedelta(minutes=self.PASSWORD_RETRIES_TIME_WINDOW_MINUTES)  # Configure this as needed

        # Check if the current attempt is outside the retry time window
        if admin.failed_login_starttime:
            admin.failed_login_starttime = admin.failed_login_starttime.replace(tzinfo=timezone.utc) # Ensure timezone-aware datetime
            time_since_first_failure = current_time - admin.failed_login_starttime

            if time_since_first_failure > time_window:
                # Reset the counter and starttime if outside the retry window
                update_data = {
                    "consecutive_failed_logins": 1,  # Start fresh with the current failed attempt
                    "failed_login_starttime": current_time
                }
            else:
                # Increment the counter if within the retry window
                current_count += 1
                update_data = {"consecutive_failed_logins": current_count}
        else:
            # First failed attempt within a new window
            current_count = 1
            update_data = {
                "consecutive_failed_logins": current_count,
                "failed_login_starttime": current_time
            }

        # Lock account if the failed attempts reach the threshold
        if current_count >= self.MAX_PASSWORD_RETRIES:
            update_data["account_locked"] = True

        self.crud_operations.update_administrator(admin_id, update_data)
        return current_count


    def __reset_login_failure_counters(self, admin_id: int) -> None:
        """
        Reset the consecutive_failed_logins counter and failed_login_starttime.
        """
        update_data = {
            "consecutive_failed_logins": 0,
            "failed_login_starttime": None
        }
        self.crud_operations.update_administrator(admin_id, update_data)
    
    def __hash_password(self, password: str, salt: str) -> str:
        """
        Hash a password with a salt using SHA-256.
        """
        return hashlib.sha256(f'{salt}:{password}'.encode('utf-8')).hexdigest()

    def __verify_password(self, stored_password_hash: str, provided_password: str, salt: str) -> bool:
        """
        Verify a provided password against the stored password hash using the salt.
        """
        return stored_password_hash == self.__hash_password(provided_password, salt)

        
    def unlock_administrator_account(self, admin_id: int) -> None:
        """
        Unlock an administrator's account, resetting the lock status and failure counters.
        """
        self.__get_admin_by_id(admin_id) # Check if the admin exists. Raises an exception if not found.
        update_data = {
            "account_locked": False,
            "consecutive_failed_logins": 0,
            "failed_login_starttime": None
        }
        self.crud_operations.update_administrator(admin_id, update_data)

    def __lock_administrator_account(self, admin_id: int) -> None:
        """
        Lock an administrator's account after too many consecutive login failures.
        """
        self.__get_admin_by_id(admin_id) # Check if the admin exists. Raises an exception if not found.
        update_data = {"account_locked": True}
        self.crud_operations.update_administrator(admin_id, update_data)


    def __get_admin_by_id(self, admin_id: int) -> Administrator:
        admin = self.crud_operations.get_administrator(admin_id)
        if not admin:
            raise AdministratorNotFoundException(f"Administrator with ID {admin_id} not found.")
        return admin

    def __get_admin_by_username(self, username: str) -> Administrator:
        """
        Retrieve an administrator by username.
        """
        if username:
            username = username.strip().lower() # Remove leading and trailing whitespaces. Sets username to lowercase
        else:
            raise AdministratorNotFoundException("Username cannot be empty.") 
        
        admin = self.crud_operations.get_administrator_by_username(username)
        if not admin:
            raise AdministratorNotFoundException(f"Administrator with Username {username} not found.")
        return admin

    def reset_admin_password(self, admin_id: int, target_username: str) -> str:
        """
        Reset the password for another administrator.
        """
        # Verify the requesting admin exists (authorization check would go here in a real-world scenario)
        self.__get_admin_by_id(admin_id)

        # Get the target administrator
        target_admin = self.__get_admin_by_username(target_username)

        # Generate a new secure password
        new_password = self.__generate_secure_password()

        # Hash the new password
        salt = target_admin.salt
        password_hash = self.__hash_password(new_password, salt)

        # Update the target administrator's password
        update_data = {
            "password_hash": password_hash,
            "account_locked": False,  # Unlock the account if it was locked
            "consecutive_failed_logins": 0,  # Reset failed login attempts
            "failed_login_starttime": None
        }
        self.crud_operations.update_administrator(target_admin.id, update_data)

        return new_password

    def __generate_secure_password(self, length: int = 16) -> str:
        """
        Generate a secure random password.
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(alphabet) for i in range(length))
        return password
