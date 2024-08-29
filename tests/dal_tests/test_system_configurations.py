# Copyright (c) 2024 by Jonathan AW
# test_system_configurations.py
""" 
Tests for the Data Access Layer CRUD operations for system configurations service.
"""
import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound
from dal.models import Administrator, Applicant
from datetime import datetime


def test_create_system_configuration(system_config):
    # Arrange
    config_data = {"key": "UniqueTestConfig1", "value": "TestValue", "description": "Test Description"}

    # Act
    new_config = system_config.create_system_configuration(config_data)

    # Assert
    assert new_config.key == config_data["key"]
    assert new_config.value == config_data["value"]
    assert new_config.description == config_data["description"]

def test_get_system_configuration(system_config):
    # Arrange
    config_data = {"key": "UniqueTestConfig2", "value": "TestValue", "description": "Test Description"}
    new_config = system_config.create_system_configuration(config_data)

    # Act
    config = system_config.get_system_configuration(new_config.id)

    # Assert
    assert config.id == new_config.id
    assert config.key == new_config.key

def test_get_system_configurations_by_filters(system_config):
    # Arrange
    config_data = {"key": "UniqueTestConfig3", "value": "TestValue", "description": "Test Description"}
    system_config.create_system_configuration(config_data)

    # Act
    configs = system_config.get_system_configurations_by_filters({"key": "UniqueTestConfig3"})

    # Assert
    assert len(configs) > 0
    assert configs[0].key == "UniqueTestConfig3"

def test_update_system_configuration(system_config):
    # Arrange
    config_data = {"key": "UniqueTestConfig4", "value": "TestValue", "description": "Test Description"}
    new_config = system_config.create_system_configuration(config_data)
    update_data = {"value": "UpdatedValue"}

    # Act
    updated_config = system_config.update_system_configuration(new_config.id, update_data)

    # Assert
    assert updated_config.value == "UpdatedValue"

def test_delete_system_configuration(system_config):
    # Arrange
    config_data = {"key": "TestConfigToDelete", "value": "TestValue", "description": "Test Description"}
    new_config = system_config.create_system_configuration(config_data)

    # Act
    system_config.delete_system_configuration(new_config.id)
    deleted_config = system_config.get_system_configuration(new_config.id)

    # Assert
    assert deleted_config is None