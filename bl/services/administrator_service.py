# Copyright (c) 2024 by Jonathan AW

from typing import List
from dal.crud_operations import CRUDOperations
from dal.models import Administrator
from exceptions import AdministratorNotFoundException

class AdministratorService:
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
        """
        Create a new administrator record.
        """
        return self.crud_operations.create_administrator(admin_data["username"], admin_data["password_hash"])

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
