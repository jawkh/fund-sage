# Copyright (c) 2024 by Jonathan AW

import hashlib
import os
from typing import Optional, List
from dal.crud_operations import CRUDOperations
from dal.models import Administrator
from exceptions import AdministratorNotFoundException
from environs import Env
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class AdministratorService:
    # Load environment variables
    MAX_PASSWORD_RETRIES = int(Env().str("MAX_PASSWORD_RETRIES ", "5")) 

    """
    Service class to handle all business logic related to administrators.
    """

    def __init__(self, crud_operations: CRUDOperations):
        self.crud_operations = crud_operations

    def get_administrator_by_id(self, admin_id: int) -> Administrator:
        """
        Retrieve an administrator by ID.
        """
        admin = self.crud_operations.get_administrator(admin_id)
        if not admin:
            raise AdministratorNotFoundException(f"Administrator with ID {admin_id} not found.")
        return admin
    
    def get_administrator_by_username(self, username: str) -> Administrator:
        """
        Retrieve an administrator by username.
        """
        admin = self.crud_operations.get_administrator_by_username(username)
        if not admin:
            raise AdministratorNotFoundException(f"Administrator with Username {username} not found.")
        return admin


    def create_administrator(self, admin_data: dict) -> Administrator:
        # Generate a salt
        salt = os.urandom(16).hex()
        # Hash the password with the salt
        password_hash = self.hash_password(admin_data["password_hash"], salt)
        admin_data["password_hash"] = password_hash
        admin_data["salt"] = salt
        return self.crud_operations.create_administrator(admin_data["username"], password_hash, salt)

    def update_administrator(self, admin_id: int, update_data: dict) -> Administrator:
        """
        Update an administrator's details.
        """
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
    def verify_login_credentials(self, username: str, password: str) -> Optional[Administrator]:
        """
        Verify login credentials for an administrator.
        """
        admin = self.crud_operations.get_administrator_by_username(username)
        if admin and not admin.account_locked:
            if self.verify_password(admin.password_hash, password, admin.salt):
                # Reset login failure counters on successful login
                self.reset_login_failure_counters(admin.id)
                return admin
            else:
                # Increment login failure counters
                self.increment_login_failure_counter(admin.id)
        return None
    
    
    def increment_login_failure_counter(self, admin_id: int) -> None:
        """
        Increment the consecutive_failed_logins counter and set failed_login_starttime.
        Lock the account if necessary.
        """
        admin = self.get_administrator_by_id(admin_id)
        if admin:
            current_count = admin.consecutive_failed_logins + 1
            update_data = {"consecutive_failed_logins": current_count}

            if current_count == 1:
                # Set failed_login_starttime to current time for the first failure in this lockout period
                update_data["failed_login_starttime"] = datetime.utcnow()

            if current_count >= 5:  # Assuming 5 is the lock threshold
                update_data["account_locked"] = True

            self.crud_operations.update_administrator(admin_id, update_data)

    def reset_login_failure_counters(self, admin_id: int) -> None:
        """
        Reset the consecutive_failed_logins counter and failed_login_starttime.
        """
        update_data = {
            "consecutive_failed_logins": 0,
            "failed_login_starttime": None
        }
        self.crud_operations.update_administrator(admin_id, update_data)
    
    def hash_password(self, password: str, salt: str) -> str:
        """
        Hash a password with a salt using SHA-256.
        """
        return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

    def verify_password(self, stored_password_hash: str, provided_password: str, salt: str) -> bool:
        """
        Verify a provided password against the stored password hash using the salt.
        """
        return stored_password_hash == self.hash_password(provided_password, salt)

        
    def unlock_administrator_account(self, admin_id: int) -> None:
        """
        Unlock an administrator's account, resetting the lock status and failure counters.
        """
        admin = self.get_administrator_by_id(admin_id)
        if admin:
            update_data = {
                "account_locked": False,
                "consecutive_failed_logins": 0,
                "failed_login_starttime": None
            }
            self.crud_operations.update_administrator(admin_id, update_data)

    def lock_administrator_account(self, admin_id: int) -> None:
        """
        Lock an administrator's account after too many consecutive login failures.
        """
        admin = self.get_administrator_by_id(admin_id)
        if admin:
            update_data = {"account_locked": True}
            self.crud_operations.update_administrator(admin_id, update_data)

    

    
