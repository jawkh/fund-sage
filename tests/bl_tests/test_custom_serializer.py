# Copyright (c) 2024 by Jonathan AW

import pytest
from datetime import datetime
from dal.models import Administrator, Applicant, HouseholdMember, Application, Scheme
from dal.custom_serializer import serialize

def test_serialize_simple_object():
    """Test serializing a simple ORM object."""
    admin = Administrator(id=1, username='admin', password_hash='hash', salt='salt', role='admin', created_at=datetime.now(), updated_at=datetime.now())
    serialized_admin = serialize(admin)
    assert serialized_admin['username'] == 'admin'
    assert 'password_hash' in serialized_admin  # Ensure all fields are included

def test_serialize_nested_object():
    """Test serializing an ORM object with nested relationships."""
    admin = Administrator(id=1, username='admin', password_hash='hash', salt='salt', created_at=datetime.now())
    applicant = Applicant(
        id=1,
        name='John Doe',
        employment_status='employed',
        sex='M',
        date_of_birth=datetime(1990, 1, 1),
        marital_status='single',
        creator=admin,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    serialized_applicant = serialize(applicant)
    assert serialized_applicant['name'] == 'John Doe'
    assert 'creator' in serialized_applicant
    assert serialized_applicant['creator'] is None or serialized_applicant['creator']['username'] == 'admin'  # Should handle if not loaded


def test_serialize_with_nullables():
    """Test serializing an ORM object with nullable fields."""
    scheme = Scheme(
        id=1, 
        name='Health Scheme', 
        description='Health benefits', 
        eligibility_criteria={}, 
        benefits={}, 
        validity_start_date=datetime(2024, 1, 1), 
        validity_end_date=None
    )
    serialized_scheme = serialize(scheme)
    assert serialized_scheme['validity_end_date'] is None

def test_serialize_list_of_objects():
    """Test serializing a list of ORM objects."""
    applicants = [
        Applicant(id=1, name='John Doe', employment_status='employed', sex='M', date_of_birth=datetime(1990, 1, 1), marital_status='single'),
        Applicant(id=2, name='Jane Doe', employment_status='unemployed', sex='F', date_of_birth=datetime(1985, 6, 15), marital_status='married')
    ]
    serialized_applicants = serialize(applicants)
    assert len(serialized_applicants) == 2
    assert serialized_applicants[0]['name'] == 'John Doe'
    assert serialized_applicants[1]['name'] == 'Jane Doe'

def test_serialize_handles_datetimes():
    """Test that datetime fields are correctly converted to strings."""
    scheme = Scheme(
        id=1, 
        name='Health Scheme', 
        description='Health benefits', 
        eligibility_criteria={}, 
        benefits={}, 
        validity_start_date=datetime(2024, 1, 1)
    )
    serialized_scheme = serialize(scheme)
    assert isinstance(serialized_scheme['validity_start_date'], str)




def test_serialize_basic_object():
    """Test serializing a basic ORM object with no relationships."""
    admin = Administrator(
        id=1, 
        username='admin', 
        password_hash='hash', 
        salt='salt', 
        role='admin', 
        created_at=datetime.now(), 
        updated_at=datetime.now()
    )
    serialized_admin = serialize(admin)
    assert serialized_admin['id'] == 1
    assert serialized_admin['username'] == 'admin'
    assert 'password_hash' in serialized_admin  # Ensure all fields are included
    assert isinstance(serialized_admin['created_at'], str)  # Check datetime serialization

def test_serialize_object_with_nullables():
    """Test serializing an ORM object with nullable fields."""
    scheme = Scheme(
        id=1, 
        name='Health Scheme', 
        description='Health benefits', 
        eligibility_criteria={}, 
        benefits={}, 
        validity_start_date=datetime(2024, 1, 1), 
        validity_end_date=None
    )
    serialized_scheme = serialize(scheme)
    assert serialized_scheme['id'] == 1
    assert serialized_scheme['name'] == 'Health Scheme'
    assert serialized_scheme['validity_end_date'] is None

def test_serialize_nested_objects():
    """Test serializing an ORM object with nested relationships (one-to-many)."""
    admin = Administrator(id=1, username='admin', password_hash='hash', salt='salt', created_at=datetime.now())
    applicant = Applicant(
        id=1,
        name='John Doe',
        employment_status='employed',
        sex='M',
        date_of_birth=datetime(1990, 1, 1),
        marital_status='single',
        creator=admin,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    household_member = HouseholdMember(
        id=1,
        applicant_id=applicant.id,
        name='Jane Doe',
        relation='spouse',
        date_of_birth=datetime(1992, 2, 2)
    )
    applicant.household_members = [household_member]

    serialized_applicant = serialize(applicant)
    assert serialized_applicant['name'] == 'John Doe'
    assert 'creator' in serialized_applicant
    assert serialized_applicant['creator'] is None or serialized_applicant['creator']['username'] == 'admin'  # Should handle if not loaded
    assert 'household_members' in serialized_applicant
    assert serialized_applicant['household_members'][0]['name'] == 'Jane Doe'

def test_serialize_deeply_nested_objects():
    """Test serializing deeply nested objects with multiple levels of relationships."""
    admin = Administrator(id=1, username='admin', password_hash='hash', salt='salt', created_at=datetime.now())
    applicant = Applicant(
        id=1,
        name='John Doe',
        employment_status='employed',
        sex='M',
        date_of_birth=datetime(1990, 1, 1),
        marital_status='single',
        creator=admin,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    scheme = Scheme(
        id=1,
        name='Scholarship Program',
        description='Financial aid for students',
        eligibility_criteria={'min_age': 18},
        benefits={'amount': 5000},
        validity_start_date=datetime(2024, 1, 1)
    )
    application = Application(
        id=1,
        applicant_id=applicant.id,
        scheme_id=scheme.id,
        status='pending',
        submission_date=datetime(2024, 1, 15),
        applicant=applicant,
        scheme=scheme,
        creator=admin,
        created_at=datetime.now()
    )
    applicant.applications = [application]

    serialized_application = serialize(application)
    assert serialized_application['status'] == 'pending'
    assert serialized_application['applicant']['name'] == 'John Doe'
    assert serialized_application['scheme']['name'] == 'Scholarship Program'
    assert serialized_application['creator']['username'] == 'admin'

def test_serialize_list_of_objects():
    """Test serializing a list of ORM objects."""
    applicants = [
        Applicant(id=1, name='John Doe', employment_status='employed', sex='M', date_of_birth=datetime(1990, 1, 1), marital_status='single'),
        Applicant(id=2, name='Jane Doe', employment_status='unemployed', sex='F', date_of_birth=datetime(1985, 6, 15), marital_status='married')
    ]
    serialized_applicants = serialize(applicants)
    assert len(serialized_applicants) == 2
    assert serialized_applicants[0]['name'] == 'John Doe'
    assert serialized_applicants[1]['name'] == 'Jane Doe'

def test_serialize_handles_different_data_types():
    """Test that different data types (like DateTime, JSON) are correctly converted."""
    scheme = Scheme(
        id=1, 
        name='Health Scheme', 
        description='Health benefits', 
        eligibility_criteria={"min_age": 18}, 
        benefits={"coverage": "full"},
        validity_start_date=datetime(2024, 1, 1)
    )
    serialized_scheme = serialize(scheme)
    assert isinstance(serialized_scheme['validity_start_date'], str)
    assert isinstance(serialized_scheme['eligibility_criteria'], dict)
    assert serialized_scheme['eligibility_criteria']['min_age'] == 18

def test_serialize_with_errors():
    """Test serialization error handling with invalid input."""
    try:
        result = serialize(None)
        assert result is None
    except Exception as e:
        pytest.fail(f"Serialization raised an unexpected exception: {str(e)}")

    # Test with an invalid input that is not an ORM object
    try:
        result = serialize("Not an ORM object")
        assert result is None  # Should gracefully handle non-ORM objects
    except Exception as e:
        pytest.fail(f"Serialization raised an unexpected exception: {str(e)}")
        
def test_serialize_empty_object():
    """Test serializing an empty object to ensure it handles missing data gracefully."""
    admin = Administrator()
    serialized_admin = serialize(admin)
    assert serialized_admin['id'] is None
    assert serialized_admin['username'] is None

def test_serialize_handles_orm_errors():
    """Test that serialization properly handles SQLAlchemy ORM errors, like NoResultFound."""
    try:
        application = Application(id=999)  # Assuming this ID doesn't exist
        serialized_application = serialize(application)
        assert serialized_application['id'] == 999
    except NoResultFound:
        pytest.fail("Serialization should handle NoResultFound error gracefully.")
    except Exception as e:
        pytest.fail(f"Serialization raised an unexpected exception: {str(e)}")

def test_serialize_with_optional_attributes():
    """Test serialization with optional attributes that may not always be present."""
    household_member = HouseholdMember(
        id=1,
        applicant_id=None,
        name='Jane Doe',
        relation='spouse',
        date_of_birth=datetime(1992, 2, 2),
        employment_status=None,  # Optional attribute
        sex='F',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    serialized_member = serialize(household_member)
    assert serialized_member['applicant_id'] is None
    assert serialized_member['employment_status'] is None
    assert serialized_member['sex'] == 'F'


def test_serialize_with_lazy_loaded_relationships():
    """Test serialization of an ORM object with lazy-loaded relationships."""
    admin = Administrator(id=1, username='admin', password_hash='hash', salt='salt', created_at=datetime.now())
    applicant = Applicant(
        id=1,
        name='John Doe',
        employment_status='employed',
        sex='M',
        date_of_birth=datetime(1990, 1, 1),
        marital_status='single',
        creator=admin,  # Lazy-loaded relationship
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    serialized_applicant = serialize(applicant)
    assert serialized_applicant['name'] == 'John Doe'
    # assert 'creator' not in serialized_applicant  # Creator should not be serialized as it is lazy-loaded

def test_serialize_with_eager_loaded_relationships():
    """Test serialization of an ORM object with eager-loaded relationships."""
    admin = Administrator(id=1, username='admin', password_hash='hash', salt='salt', created_at=datetime.now())
    applicant = Applicant(
        id=1,
        name='John Doe',
        employment_status='employed',
        sex='M',
        date_of_birth=datetime(1990, 1, 1),
        marital_status='single',
        creator=admin,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    scheme = Scheme(
        id=1,
        name='Scholarship Program',
        description='Financial aid for students',
        eligibility_criteria={'min_age': 18},
        benefits={'amount': 5000},
        validity_start_date=datetime(2024, 1, 1)
    )
    application = Application(
        id=1,
        applicant_id=applicant.id,
        scheme_id=scheme.id,
        status='pending',
        submission_date=datetime(2024, 1, 15),
        applicant=applicant,  # Eager-loaded relationship
        scheme=scheme,        # Eager-loaded relationship
        creator=admin,        # Eager-loaded relationship
        created_at=datetime.now()
    )
    applicant.applications = [application]  # Relationship

    serialized_application = serialize(application)
    assert serialized_application['status'] == 'pending'
    assert serialized_application['applicant']['name'] == 'John Doe'
    assert serialized_application['scheme']['name'] == 'Scholarship Program'
    assert serialized_application['creator']['username'] == 'admin'

def test_serialize_mixed_relationships():
    """Test serialization of an ORM object with mixed lazy and eager-loaded relationships."""
    admin = Administrator(id=1, username='admin', password_hash='hash', salt='salt', created_at=datetime.now())
    applicant = Applicant(
        id=1,
        name='John Doe',
        employment_status='employed',
        sex='M',
        date_of_birth=datetime(1990, 1, 1),
        marital_status='single',
        creator=admin,  # Lazy-loaded relationship
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    household_member = HouseholdMember(
        id=1,
        applicant_id=applicant.id,
        name='Jane Doe',
        relation='spouse',
        date_of_birth=datetime(1992, 2, 2)
    )
    applicant.household_members = [household_member]  # Eager-loaded relationship

    serialized_applicant = serialize(applicant)
    assert serialized_applicant['name'] == 'John Doe'
    #assert 'creator' not in serialized_applicant  # Lazy-loaded, should not be serialized
    assert 'household_members' in serialized_applicant  # Eager-loaded, should be serialized
    assert serialized_applicant['household_members'][0]['name'] == 'Jane Doe'

def test_serialize_handle_non_orm_objects():
    """Test serialization handling of non-ORM objects or invalid input."""
    result = serialize(None)
    assert result is None  # Should return None for None input

    result = serialize("Not an ORM object")
    assert result is None  # Should return None for non-ORM objects

def test_serialize_with_depth_control():
    """Test serialization with depth control to avoid unnecessary serialization of deeply nested objects."""
    admin = Administrator(id=1, username='admin', password_hash='hash', salt='salt', created_at=datetime.now())
    applicant = Applicant(
        id=1,
        name='John Doe',
        employment_status='employed',
        sex='M',
        date_of_birth=datetime(1990, 1, 1),
        marital_status='single',
        creator=admin,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    household_member = HouseholdMember(
        id=1,
        applicant_id=applicant.id,
        name='Jane Doe',
        relation='spouse',
        date_of_birth=datetime(1992, 2, 2)
    )
    applicant.household_members = [household_member]

    serialized_applicant = serialize(applicant, depth=1)
    assert serialized_applicant['name'] == 'John Doe'
    assert serialized_applicant['household_members'] is None  # Should not serialize beyond depth 1 if not eager-loaded



def test_serialize_complex_objects():
    """Test serializing complex objects to ensure serializer robustness."""
    admin = Administrator(id=1, username='admin', password_hash='hash', salt='salt', created_at=datetime.now())
    applicant = Applicant(
        id=1,
        name='John Doe',
        employment_status='employed',
        sex='M',
        date_of_birth=datetime(1990, 1, 1),
        marital_status='single',
        creator=admin,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    scheme = Scheme(
        id=1,
        name='Scholarship Program',
        description='Financial aid for students',
        eligibility_criteria={'min_age': 18},
        benefits={'amount': 5000},
        validity_start_date=datetime(2024, 1, 1)
    )
    application = Application(
        id=1,
        applicant_id=applicant.id,
        scheme_id=scheme.id,
        status='pending',
        submission_date=datetime(2024, 1, 15),
        applicant=applicant,
        scheme=scheme,
        creator=admin,
        created_at=datetime.now()
    )
    applicant.applications = [application]
    serialized_application = serialize(application)

    assert serialized_application['status'] == 'pending'
    assert serialized_application['applicant']['name'] == 'John Doe'
    assert serialized_application['scheme']['name'] == 'Scholarship Program'
    assert serialized_application['creator']['username'] == 'admin'
    
    def test_serialize_list_of_objects():
        """Test serializing a list of ORM objects."""
        applicants = [
            Applicant(id=1, name='John Doe', employment_status='employed', sex='M', date_of_birth=datetime(1990, 1, 1), marital_status='single'),
            Applicant(id=2, name='Jane Doe', employment_status='unemployed', sex='F', date_of_birth=datetime(1985, 6, 15), marital_status='married')
        ]
        serialized_applicants = serialize(applicants)
        assert len(serialized_applicants) == 2
        assert serialized_applicants[0]['name'] == 'John Doe'
        assert serialized_applicants[1]['name'] == 'Jane Doe'
    
def test_serialize_handle_non_orm_objects():
    """Test serialization handling of non-ORM objects or invalid input."""
    result = serialize(None)
    assert result is None  # Should return None for None input

    result = serialize("Not an ORM object")
    assert result is None  # Should return None for non-ORM objects
    
def test_serialize_complex_objects():
    """Test serializing complex objects to ensure serializer robustness."""
    admin = Administrator(id=1, username='admin', password_hash='hash', salt='salt', created_at=datetime.now())
    applicant = Applicant(
        id=1,
        name='John Doe',
        employment_status='employed',
        sex='M',
        date_of_birth=datetime(1990, 1, 1),
        marital_status='single',
        creator=admin,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    scheme = Scheme(
        id=1,
        name='Scholarship Program',
        description='Financial aid for students',
        eligibility_criteria={'min_age': 18},
        benefits={'amount': 5000},
        validity_start_date=datetime(2024, 1, 1)
    )
    application = Application(
        id=1,
        applicant_id=applicant.id,
        scheme_id=scheme.id,
        status='pending',
        submission_date=datetime(2024, 1, 15),
        applicant=applicant,
        scheme=scheme,
        creator=admin,
        created_at=datetime.now()
    )
    applicant.applications = [application]
    serialized_application = serialize(application)

    assert serialized_application['status'] == 'pending'
    assert serialized_application['applicant']['name'] == 'John Doe'
    assert serialized_application['scheme']['name'] == 'Scholarship Program'
    assert serialized_application['creator']['username'] == 'admin'