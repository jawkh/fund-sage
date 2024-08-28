# Copyright (c) 2024 by Jonathan AW

""" 
ORM classes for the database tables.
These are used to define the schema of the database tables.
The relationships between the tables are also defined here.
We also define CheckConstraints at the table level.

Provisioning Databases: Use SQLAlchemy ORM models to create both production and test databases to ensure schema consistency.

We will use these ORM classes to interact with the database using SQLAlchemy.
We will be able to perform CRUD operations on the tables using these classes.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, CheckConstraint
from sqlalchemy.orm import relationship, configure_mappers
from sqlalchemy.sql import func
from dal.database import Base

class Administrator(Base):
    """ 
    Summary: ORM class for the Administrators table in the database.
    Encapsulates the schema of the Administrators table.
    Encapsulates the relationships with the Applicants and Applications tables.
    """
    __tablename__ = 'Administrators'

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(255), unique=True, nullable=False)
    password_hash: str = Column(String(255), nullable=False)
    salt: str = Column(String(255), nullable=False) 
    role: str = Column(String(50), default='admin')
    consecutive_failed_logins: int = Column(Integer, default=0)
    failed_login_starttime: DateTime = Column(DateTime, nullable=True)
    account_locked: bool = Column(Boolean, default=False)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: DateTime = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with Applicants
    applicants_created = relationship("Applicant", back_populates="creator")
    applications_created = relationship("Application", back_populates="creator")  # New relationship to Application


class Applicant(Base):
    """ 
    Summary: ORM class for the Applicants table in the database.
    """
    __tablename__ = 'Applicants'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    employment_status: str = Column(String(50), nullable=False)
    sex: str = Column(String(1), nullable=False)
    date_of_birth: DateTime = Column(DateTime, nullable=False)
    marital_status: str = Column(String(50), nullable=True)
    employment_status_change_date: DateTime = Column(DateTime, nullable=True)
    created_by_admin_id: int = Column(Integer, ForeignKey('Administrators.id'))
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: DateTime = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("Administrator", back_populates="applicants_created")
    household_members = relationship("HouseholdMember", back_populates="applicant", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="applicant", cascade="all, delete-orphan")

    # Add CheckConstraints at the table level
    __table_args__ = (
        CheckConstraint("employment_status IN ('employed', 'unemployed')", name="check_employment_status"),
        CheckConstraint("sex IN ('M', 'F')", name="check_sex"),
        CheckConstraint("marital_status IN ('single', 'married', 'divorced', 'widowed')", name="check_marital_status"),
    )


class HouseholdMember(Base):
    """ 
    Summary: ORM class for the HouseholdMembers table in the database.
    """
    __tablename__ = 'HouseholdMembers'

    id: int = Column(Integer, primary_key=True, index=True)
    applicant_id: int = Column(Integer, ForeignKey('Applicants.id', ondelete='CASCADE'))
    name: str = Column(String(255), nullable=False)
    relation: str = Column(String(50), nullable=False)
    date_of_birth: DateTime = Column(DateTime, nullable=False)
    employment_status: str = Column(String(50), nullable=True)
    sex: str = Column(String(1), nullable=True)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: DateTime = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with Applicant
    applicant = relationship("Applicant", back_populates="household_members")

    # Add CheckConstraints at the table level
    __table_args__ = (
        CheckConstraint("relation IN ('parent', 'child', 'spouse', 'sibling', 'other')", name="check_relation"),
        CheckConstraint("employment_status IN ('employed', 'unemployed')", name="check_employment_status"),
        CheckConstraint("sex IN ('M', 'F')", name="check_sex"),
    )




class Scheme(Base):
    """ 
    summary: ORM class for the Schemes table in the database.
    """
    __tablename__ = 'Schemes'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    description: str = Column(String, nullable=False)
    eligibility_criteria: dict = Column(JSON, nullable=False)
    benefits: dict = Column(JSON, nullable=True)
    validity_start_date: DateTime = Column(DateTime, nullable=False)
    validity_end_date: DateTime = Column(DateTime, nullable=True)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: DateTime = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with Applications
    applications = relationship("Application", back_populates="scheme", cascade="all, delete-orphan")




class Application(Base):
    """ 
    summary: ORM class for the Applications table in the database.
    """
    __tablename__ = 'Applications'

    id: int = Column(Integer, primary_key=True, index=True)
    applicant_id: int = Column(Integer, ForeignKey('Applicants.id', ondelete='CASCADE'))
    scheme_id: int = Column(Integer, ForeignKey('Schemes.id', ondelete='CASCADE'))
    status: str = Column(String(50), nullable=False)
    submission_date: DateTime = Column(DateTime(timezone=True), default=func.now())
    created_by_admin_id: int = Column(Integer, ForeignKey('Administrators.id')) 
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: DateTime = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    applicant = relationship("Applicant", back_populates="applications")
    scheme = relationship("Scheme", back_populates="applications")
    creator = relationship("Administrator", back_populates="applications_created")  

    # Add CheckConstraints at the table level
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'approved', 'rejected')", name="check_status"),
    )



class SystemConfiguration(Base):
    """ 
    summary: ORM class for the SystemConfigurations table in the database.
    """
    __tablename__ = 'SystemConfigurations'

    id: int = Column(Integer, primary_key=True, index=True)
    key: str = Column(String(255), unique=True, nullable=False)
    value: str = Column(String(255), nullable=False)
    description: str = Column(String, nullable=True)
    last_updated: DateTime = Column(DateTime(timezone=True), server_default=func.now())


configure_mappers() # Configure mappers to ensure all relationships are properly set up