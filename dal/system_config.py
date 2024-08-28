# Copyright (c) 2024 by Jonathan AW

""" 
SystemConfig class for CRUD operations on SystemConfiguration objects.
"""

from dal.models import SystemConfiguration
from sqlalchemy.orm import Session
from typing import Dict, List, Optional

class SystemConfig():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    # ===============================
    # CRUD Operations for SystemConfiguration
    # ===============================

    def create_system_configuration(self, config_data: Dict) -> SystemConfiguration:
        """
        Create a new system configuration.

        Args:
            config_data (Dict): A dictionary containing the configuration's data.

        Returns:
            SystemConfiguration: The created SystemConfiguration object.
        """
        db_config = SystemConfiguration(**config_data)
        self.db_session.add(db_config)
        self.db_session.commit()
        self.db_session.refresh(db_config)
        return db_config

    def get_system_configuration(self, config_id: int) -> Optional[SystemConfiguration]:
        """
        Retrieve a system configuration by ID.

        Args:
            config_id (int): The ID of the configuration.

        Returns:
            Optional[SystemConfiguration]: The SystemConfiguration object if found, otherwise None.
        """
        return self.db_session.query(SystemConfiguration).filter(SystemConfiguration.id == config_id).first()

    def get_system_configurations_by_filters(self, filters: Dict) -> List[SystemConfiguration]:
        """
        Retrieve multiple system configurations based on common filters.

        Args:
            filters (Dict): A dictionary of filters (e.g., {"key": "max_login_attempts"}).

        Returns:
            List[SystemConfiguration]: A list of SystemConfiguration objects that match the filters.
        """
        query = self.db_session.query(SystemConfiguration)
        for attribute, value in filters.items():
            query = query.filter(getattr(SystemConfiguration, attribute) == value)
        return query.all()

    def update_system_configuration(self, config_id: int, update_data: Dict) -> Optional[SystemConfiguration]:
        """
        Update a system configuration's details.

        Args:
            config_id (int): The ID of the configuration to update.
            update_data (Dict): A dictionary of the data to update.

        Returns:
            Optional[SystemConfiguration]: The updated SystemConfiguration object if successful, otherwise None.
        """
        self.db_session.query(SystemConfiguration).filter(SystemConfiguration.id == config_id).update(update_data)
        self.db_session.commit()
        return self.get_system_configuration(config_id)

    def delete_system_configuration(self, config_id: int) -> None:
        """
        Delete a system configuration by ID.

        Args:
            config_id (int): The ID of the configuration to delete.
        """
        self.db_session.query(SystemConfiguration).filter(SystemConfiguration.id == config_id).delete()
        self.db_session.commit()

