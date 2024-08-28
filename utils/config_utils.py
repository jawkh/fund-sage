# Copyright (c) 2024 by Jonathan AW


from dal.crud_operations import CRUDOperations
from sqlalchemy.orm import Session

def get_configuration_value(db_session: Session, key: str, default=None):
    """
    Retrieve a configuration value from the SystemConfigurations table.
    """
    system_configs = CRUDOperations(db_session)
    config = system_configs.get_system_configurations_by_filters({"key": key})
    if config:
        return config[0].value  # Assuming 'key' is unique, return the first result
    return default

