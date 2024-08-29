# Copyright (c) 2024 by Jonathan AW
# system_config.py
""" 
SystemConfig class for CRUD operations on SystemConfiguration objects.

Design Patterns:
1. Encapsulation:
- The SystemConfig class encapsulates the logic for interacting with SystemConfiguration objects, providing a clean interface for data access.

2. Data Validation:
- The class uses the validate_system_configuration_data function to validate system configuration data before creating or updating a configuration, ensuring data integrity and consistency.

3. Error Handling:
- Custom exceptions (InvalidSystemConfigDataException) are used to handle specific error scenarios related to system configurations, providing clear and meaningful feedback.

4. Dependency Injection:
- The class takes a SQLAlchemy Session object as a dependency, allowing for better testability and separation of concerns.

5. Use of Type Annotations:
- The use of type annotations for method arguments and return types enhances code readability and maintainability.

6. Single Responsibility Principle (SRP):
- The class is focused on handling CRUD operations for SystemConfiguration objects, adhering to the SRP.

7. Readability and Maintainability:
- The class structure and method names are well-organized, making the code easy to understand and maintain.


"""

from dal.models import SystemConfiguration
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from utils.data_validation import validate_system_configuration_data
from exceptions import InvalidSystemConfigDataException

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
        isvalid , msg = validate_system_configuration_data(config_data, True)
        if not isvalid:
            raise InvalidSystemConfigDataException(msg)
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
        isvalid , msg = validate_system_configuration_data(update_data, False)
        if not isvalid:
            raise InvalidSystemConfigDataException(msg)
        
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

