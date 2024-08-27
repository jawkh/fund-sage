# Copyright (c) 2024 by Jonathan AW

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from datetime import date
from dal.models import Administrator, Applicant, HouseholdMember, Scheme, Application, SystemConfiguration

class CRUDOperations:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    # ===============================
    # CRUD Operations for Administrator
    # ===============================

    def create_administrator(self, username: str, password_hash: str, role: str = 'admin') -> Administrator:
        """
        Create a new administrator.

        Args:
            username (str): Username of the administrator.
            password_hash (str): Hashed password of the administrator.
            role (str): Role of the administrator, default is 'admin'.

        Returns:
            Administrator: The created Administrator object.
        """
        db_admin = Administrator(username=username, password_hash=password_hash, role=role)
        self.db_session.add(db_admin)
        self.db_session.commit()
        self.db_session.refresh(db_admin)
        return db_admin

    def get_administrator(self, admin_id: int) -> Optional[Administrator]:
        """
        Retrieve an administrator by ID.

        Args:
            admin_id (int): The ID of the administrator.

        Returns:
            Optional[Administrator]: The Administrator object if found, otherwise None.
        """
        return self.db_session.query(Administrator).filter(Administrator.id == admin_id).first()

    def get_administrator_by_username(self, username: str) -> Optional[Administrator]:
        """
        Retrieve an administrator by username.

        Args:
            username (str): The username of the administrator.

        Returns:
            Optional[Administrator]: The Administrator object if found, otherwise None.
        """
        return self.db_session.query(Administrator).filter(Administrator.username == username).first()

    def get_administrators_by_filters(self, filters: Dict) -> List[Administrator]:
        """
        Retrieve multiple administrators based on common filters.

        Args:
            filters (Dict): A dictionary of filters (e.g., {"role": "admin"}).

        Returns:
            List[Administrator]: A list of Administrator objects that match the filters.
        """
        query = self.db_session.query(Administrator)
        for attribute, value in filters.items():
            query = query.filter(getattr(Administrator, attribute) == value)
        return query.all()

    def update_administrator(self, admin_id: int, update_data: Dict) -> Optional[Administrator]:
        """
        Update an administrator's details.

        Args:
            admin_id (int): The ID of the administrator to update.
            update_data (Dict): A dictionary of the data to update.

        Returns:
            Optional[Administrator]: The updated Administrator object if successful, otherwise None.
        """
        self.db_session.query(Administrator).filter(Administrator.id == admin_id).update(update_data)
        self.db_session.commit()
        return self.get_administrator(admin_id)

    def delete_administrator(self, admin_id: int) -> None:
        """
        Delete an administrator by ID.

        Args:
            admin_id (int): The ID of the administrator to delete.
        """
        self.db_session.query(Administrator).filter(Administrator.id == admin_id).delete()
        self.db_session.commit()

    # ===============================
    # CRUD Operations for Applicant
    # ===============================

    def create_applicant(self, applicant_data: Dict) -> Applicant:
        """
        Create a new applicant.

        Args:
            applicant_data (Dict): A dictionary containing the applicant's data.

        Returns:
            Applicant: The created Applicant object.
        """
        db_applicant = Applicant(**applicant_data)
        self.db_session.add(db_applicant)
        self.db_session.commit()
        self.db_session.refresh(db_applicant)
        return db_applicant

    def get_applicant(self, applicant_id: int) -> Optional[Applicant]:
        """
        Retrieve an applicant by ID.

        Args:
            applicant_id (int): The ID of the applicant.

        Returns:
            Optional[Applicant]: The Applicant object if found, otherwise None.
        """
        return self.db_session.query(Applicant).filter(Applicant.id == applicant_id).first()

    def get_applicants_by_filters(self, filters: Dict) -> List[Applicant]:
        """
        Retrieve multiple applicants based on common filters.

        Args:
            filters (Dict): A dictionary of filters (e.g., {"employment_status": "employed"}).

        Returns:
            List[Applicant]: A list of Applicant objects that match the filters.
        """
        query = self.db_session.query(Applicant)
        for attribute, value in filters.items():
            query = query.filter(getattr(Applicant, attribute) == value)
        return query.all()

    def update_applicant(self, applicant_id: int, update_data: Dict) -> Optional[Applicant]:
        """
        Update an applicant's details.

        Args:
            applicant_id (int): The ID of the applicant to update.
            update_data (Dict): A dictionary of the data to update.

        Returns:
            Optional[Applicant]: The updated Applicant object if successful, otherwise None.
        """
        self.db_session.query(Applicant).filter(Applicant.id == applicant_id).update(update_data)
        self.db_session.commit()
        return self.get_applicant(applicant_id)

    def delete_applicant(self, applicant_id: int) -> None:
        """
        Delete an applicant by ID.

        Args:
            applicant_id (int): The ID of the applicant to delete.
        """
        self.db_session.query(Applicant).filter(Applicant.id == applicant_id).delete()
        self.db_session.commit()

    # ===============================
    # CRUD Operations for HouseholdMember
    # ===============================

    def create_household_member(self, household_member_data: Dict) -> HouseholdMember:
        """
        Create a new household member.

        Args:
            household_member_data (Dict): A dictionary containing the household member's data.

        Returns:
            HouseholdMember: The created HouseholdMember object.
        """
        db_household_member = HouseholdMember(**household_member_data)
        self.db_session.add(db_household_member)
        self.db_session.commit()
        self.db_session.refresh(db_household_member)
        return db_household_member

    def get_household_member(self, member_id: int) -> Optional[HouseholdMember]:
        """
        Retrieve a household member by ID.

        Args:
            member_id (int): The ID of the household member.

        Returns:
            Optional[HouseholdMember]: The HouseholdMember object if found, otherwise None.
        """
        return self.db_session.query(HouseholdMember).filter(HouseholdMember.id == member_id).first()

    def get_household_members_by_filters(self, filters: Dict) -> List[HouseholdMember]:
        """
        Retrieve multiple household members based on common filters.

        Args:
            filters (Dict): A dictionary of filters (e.g., {"relation": "child"}).

        Returns:
            List[HouseholdMember]: A list of HouseholdMember objects that match the filters.
        """
        query = self.db_session.query(HouseholdMember)
        for attribute, value in filters.items():
            query = query.filter(getattr(HouseholdMember, attribute) == value)
        return query.all()

    def update_household_member(self, member_id: int, update_data: Dict) -> Optional[HouseholdMember]:
        """
        Update a household member's details.

        Args:
            member_id (int): The ID of the household member to update.
            update_data (Dict): A dictionary of the data to update.

        Returns:
            Optional[HouseholdMember]: The updated HouseholdMember object if successful, otherwise None.
        """
        self.db_session.query(HouseholdMember).filter(HouseholdMember.id == member_id).update(update_data)
        self.db_session.commit()
        return self.get_household_member(member_id)

    def delete_household_member(self, member_id: int) -> None:
        """
        Delete a household member by ID.

        Args:
            member_id (int): The ID of the household member to delete.
        """
        self.db_session.query(HouseholdMember).filter(HouseholdMember.id == member_id).delete()
        self.db_session.commit()

    # ===============================
    # CRUD Operations for Scheme
    # ===============================

    def create_scheme(self, scheme_data: Dict) -> Scheme:
        """
        Create a new scheme.

        Args:
            scheme_data (Dict): A dictionary containing the scheme's data.

        Returns:
            Scheme: The created Scheme object.
        """
        db_scheme = Scheme(**scheme_data)
        self.db_session.add(db_scheme)
        self.db_session.commit()
        self.db_session.refresh(db_scheme)
        return db_scheme

    def get_scheme(self, scheme_id: int) -> Optional[Scheme]:
        """
        Retrieve a scheme by ID.

        Args:
            scheme_id (int): The ID of the scheme.

        Returns:
            Optional[Scheme]: The Scheme object if found, otherwise None.
        """
        return self.db_session.query(Scheme).filter(Scheme.id == scheme_id).first()

    def get_schemes_by_filters(self, filters: Dict, fetch_valid_schemes: bool = False) -> List[Scheme]:
        """
        Retrieve multiple schemes based on common filters.

        Args:
            filters (Dict): A dictionary of filters (e.g., {"validity_start_date": "2023-01-01"}).
            fetch_valid_schemes (bool): Flag to determine whether to fetch only schemes valid as of today's date.

        Returns:
            List[Scheme]: A list of Scheme objects that match the filters and are valid if fetch_valid_schemes is True.
        """
        query = self.db_session.query(Scheme)
        
        # Apply filters provided in the function argument
        for attribute, value in filters.items():
            query = query.filter(getattr(Scheme, attribute) == value)

        # Apply validity date filtering if fetch_valid_schemes is True
        if fetch_valid_schemes:
            today = date.today()
            query = query.filter(Scheme.validity_start_date <= today).filter(
                (Scheme.validity_end_date.is_(None)) | (Scheme.validity_end_date >= today)
            )

        return query.all()

    def update_scheme(self, scheme_id: int, update_data: Dict) -> Optional[Scheme]:
        """
        Update a scheme's details.

        Args:
            scheme_id (int): The ID of the scheme to update.
            update_data (Dict): A dictionary of the data to update.

        Returns:
            Optional[Scheme]: The updated Scheme object if successful, otherwise None.
        """
        self.db_session.query(Scheme).filter(Scheme.id == scheme_id).update(update_data)
        self.db_session.commit()
        return self.get_scheme(scheme_id)

    def delete_scheme(self, scheme_id: int) -> None:
        """
        Delete a scheme by ID.

        Args:
            scheme_id (int): The ID of the scheme to delete.
        """
        self.db_session.query(Scheme).filter(Scheme.id == scheme_id).delete()
        self.db_session.commit()

    # ===============================
    # CRUD Operations for Application
    # ===============================

    def create_application(self, application_data: Dict) -> Application:
        """
        Create a new application.

        Args:
            application_data (Dict): A dictionary containing the application's data.

        Returns:
            Application: The created Application object.
        """
        db_application = Application(**application_data)
        self.db_session.add(db_application)
        self.db_session.commit()
        self.db_session.refresh(db_application)
        return db_application

    def get_application(self, application_id: int) -> Optional[Application]:
        """
        Retrieve an application by ID.

        Args:
            application_id (int): The ID of the application.

        Returns:
            Optional[Application]: The Application object if found, otherwise None.
        """
        return self.db_session.query(Application).filter(Application.id == application_id).first()

    def get_applications_by_filters(self, filters: Dict) -> List[Application]:
        """
        Retrieve multiple applications based on common filters.

        Args:
            filters (Dict): A dictionary of filters (e.g., {"status": "pending"}).

        Returns:
            List[Application]: A list of Application objects that match the filters.
        """
        query = self.db_session.query(Application)
        for attribute, value in filters.items():
            query = query.filter(getattr(Application, attribute) == value)
        return query.all()

    def update_application(self, application_id: int, update_data: Dict) -> Optional[Application]:
        """
        Update an application's details.

        Args:
            application_id (int): The ID of the application to update.
            update_data (Dict): A dictionary of the data to update.

        Returns:
            Optional[Application]: The updated Application object if successful, otherwise None.
        """
        self.db_session.query(Application).filter(Application.id == application_id).update(update_data)
        self.db_session.commit()
        return self.get_application(application_id)

    def delete_application(self, application_id: int) -> None:
        """
        Delete an application by ID.

        Args:
            application_id (int): The ID of the application to delete.
        """
        self.db_session.query(Application).filter(Application.id == application_id).delete()
        self.db_session.commit()

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

