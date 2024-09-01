# Copyright (c) 2024 by Jonathan AW
""" 
Service class for CRUD operations.

Design Patterns:
1. Separation of Concerns:
- The class is focused on handling CRUD operations for different models, adhering to the Single Responsibility Principle (SRP).

2. Reusability:
- The class encapsulates common database operations that can be reused across different services, promoting code reuse and maintainability.

3. Dependency Injection:
- The class takes a SQLAlchemy Session object as a dependency, allowing for better testability and separation of concerns.

4. Type Annotations:
- The use of type annotations for method arguments and return types enhances code readability and maintainability.

5. Encapsulation:
- The class encapsulates the logic for CRUD operations, providing a clean interface for interacting with the database.

6. Readability and Maintainability:
- The class structure and method names are well-organized, making the code easy to understand and maintain.


"""

from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from datetime import date
from dal.models import Administrator, Applicant, HouseholdMember, Scheme, Application, SystemConfiguration
from sqlalchemy.exc import SQLAlchemyError
from exceptions import InvalidPaginationParameterException, InvalidSortingParameterException
from sqlalchemy import asc, desc


class CRUDOperations:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    # ===============================
    # CRUD Operations for Administrator
    # ===============================

    def create_administrator(self, username: str, password_hash: str, salt: str, role: str = 'admin') -> Administrator:
        """
        Create a new administrator.

        Args:
            username (str): Username of the administrator.
            password_hash (str): Hashed password of the administrator.
            role (str): Role of the administrator, default is 'admin'.

        Returns:
            Administrator: The created Administrator object.
        """
        db_admin = Administrator(username=username, password_hash=password_hash, salt=salt, role=role)
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
    

    def get_all_applicants(self, 
                        page: int = 1, 
                        page_size: int = 10, 
                        sort_by: Optional[str] = 'name', 
                        sort_order: Optional[str] = 'asc', 
                        filters: Optional[Dict[str, any]] = None) -> Tuple[List[Applicant], int]:
        """
        Retrieve all applicants with pagination, sorting, and filtering options.

        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of applicants to retrieve per page.
            sort_by (Optional[str]): The field to sort by ('name' or 'created_at').
            sort_order (Optional[str]): The sort order ('asc' or 'desc').
            filters (Optional[Dict[str, any]]): A dictionary of filters to apply to the query.

        Returns:
            Tuple[List[Applicant], int]: A tuple containing a list of applicants for the specified page and the total count of applicants.
        """
        # Validate pagination parameters
        if page < 1:
            raise InvalidPaginationParameterException("Page number must be greater than 0.")
        if page_size < 1:
            raise InvalidPaginationParameterException("Page size must be greater than 0.")

        # Validate sorting parameters
        if sort_by not in ['name', 'created_at']:
            raise InvalidSortingParameterException(f"Invalid sort_by field '{sort_by}'. Allowed values are 'name' or 'created_at'.")
        if sort_order not in ['asc', 'desc']:
            raise InvalidSortingParameterException(f"Invalid sort_order '{sort_order}'. Allowed values are 'asc' or 'desc'.")

        # Calculate offset for pagination
        offset = (page - 1) * page_size
        
        # Define sorting criteria
        sort_column = Applicant.name if sort_by == 'name' else Applicant.created_at
        sort_direction = asc if sort_order == 'asc' else desc

        try:
            # Build base query
            query = self.db_session.query(Applicant)

            # Apply filters if provided
            if filters:
                for attribute, value in filters.items():
                    query = query.filter(getattr(Applicant, attribute) == value)

            # Apply sorting, pagination, and execute query
            applicants = (query
                        .order_by(sort_direction(sort_column))
                        .offset(offset)
                        .limit(page_size)
                        .all())
            
            # Retrieve total count of applicants for pagination purposes
            total_count = query.count()

            return applicants, total_count

        except SQLAlchemyError as e:
            # Handle any SQLAlchemy errors
            self.db_session.rollback()
            raise e
        
    def get_applicant(self, applicant_id: int) -> Optional[Applicant]:
        """
        Retrieve an applicant by ID.

        Args:
            applicant_id (int): The ID of the applicant.

        Returns:
            Optional[Applicant]: The Applicant object if found, otherwise None.
        """
        return self.db_session.query(Applicant).filter(Applicant.id == applicant_id).first()
    
    def create_applicant(self, applicant_data: Dict, household_members_data: Optional[List[Dict]] = []) -> Applicant:
        """
        Create an applicant and their household members.

        Args:
            applicant_data (Dict): A dictionary containing the applicant's data.
            household_members_data (List[Dict]]): List of dictionaries containing household members' data.

        Returns:
            Applicant: The created Applicant object with associated household members.
        """
        # Begin a transaction
        try:
            # Create the applicant instance
            db_applicant = Applicant(**applicant_data)
            self.db_session.add(db_applicant)
            self.db_session.flush()  # Flush to generate applicant.id

            # Create household member instances
            for member_data in household_members_data:
                member_data['applicant_id'] = db_applicant.id  # Link household members to the applicant
                db_household_member = HouseholdMember(**member_data)
                self.db_session.add(db_household_member)

            # Commit transaction to save both applicant and household members
            self.db_session.commit()
            self.db_session.refresh(db_applicant)
            return db_applicant

        except SQLAlchemyError as e:
            # Rollback transaction in case of any errors
            self.db_session.rollback()
            raise e
        
    

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
    


    def get_schemes_by_filters(
    self, 
    filters: Dict, 
    fetch_valid_schemes: bool = True, 
    page: int = 1, 
    per_page: int = 10
    ) -> Tuple[List[Scheme], int]:
        """
        Retrieve multiple schemes based on common filters with optional pagination.

        Args:
            filters (Dict): A dictionary of filters (e.g., {"validity_start_date": "2023-01-01"}).
            fetch_valid_schemes (bool): Flag to determine whether to fetch only schemes valid as of today's date.
            page (int): The page number for pagination.
            per_page (int): The number of schemes per page.

        Returns:
            Tuple[List[Scheme], int]: A tuple containing a list of Scheme objects that match the filters and
                                    a total count of schemes.
        """
        # Validate pagination parameters
        if page < 1:
            raise InvalidPaginationParameterException("Page number must be greater than 0.")
        if per_page < 1:
            raise InvalidPaginationParameterException("Page size must be greater than 0.")
        
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

        # Get total count before applying pagination
        total_count = query.count()

        # Apply pagination
        schemes = query.offset((page - 1) * per_page).limit(per_page).all()

        return schemes, total_count

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

    def get_approved_application_by_applicant_and_scheme(self, applicant_id: int, scheme_id: int) -> Optional[Application]:
        """
        Retrieve an approved application by applicant ID and scheme ID.
        Returns the first approved application found or None if no such application exists.
        
        This is used for Pre-eligibility checks to prevent an applicant from **successfully** applying to the same scheme multiple times.
        Applicant may apply for the same scheme multiple times but only one application should be approved.
        """
        return self.db_session.query(Application).filter(
            Application.applicant_id == applicant_id,
            Application.scheme_id == scheme_id,
            Application.status == "approved"  # Only look for approved applications
        ).first()

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

    def get_all_applications(self, 
                            page: int = 1, 
                            page_size: int = 10, 
                            sort_by: Optional[str] = 'created_at', 
                            sort_order: Optional[str] = 'asc') -> Tuple[List[Application], int]:
        """
        Retrieve all applications with pagination and sorting options.

        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of applications to retrieve per page.
            sort_by (Optional[str]): The field to sort by ('created_at').
            sort_order (Optional[str]): The sort order ('asc' or 'desc').

        Returns:
            Tuple[List[Application], int]: A tuple containing a list of applications for the specified page and the total count of applications.
        """
        # Validate pagination parameters
        if page < 1:
            raise InvalidPaginationParameterException("Page number must be greater than 0.")
        if page_size < 1:
            raise InvalidPaginationParameterException("Page size must be greater than 0.")

        # Validate sorting parameters
        if sort_by not in ['created_at']:
            raise InvalidSortingParameterException(f"Invalid sort_by field '{sort_by}'. Allowed value is 'created_at'.")
        if sort_order not in ['asc', 'desc']:
            raise InvalidSortingParameterException(f"Invalid sort_order '{sort_order}'. Allowed values are 'asc' or 'desc'.")

        # Calculate offset for pagination
        offset = (page - 1) * page_size
        
        # Define sorting criteria
        sort_column = Application.created_at
        sort_direction = asc if sort_order == 'asc' else desc

        # Retrieve applications from the database with pagination and sorting
        applications = (self.db_session
                        .query(Application)
                        .order_by(sort_direction(sort_column))
                        .offset(offset)
                        .limit(page_size)
                        .all())
        
        # Retrieve total count of applications for pagination purposes
        total_count = self.db_session.query(Application).count()

        return applications, total_count

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

    