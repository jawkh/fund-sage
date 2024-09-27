from datetime import datetime
from sqlalchemy.orm import class_mapper, ColumnProperty, RelationshipProperty, lazyload
from sqlalchemy.exc import SQLAlchemyError
from collections.abc import Iterable
from sqlalchemy import inspect


def serialize(obj, depth=3, visited=None):
    """
    Serialize an SQLAlchemy ORM object into a JSON-serializable dictionary.

    Args:
        obj: SQLAlchemy ORM object to serialize or a list of such objects.
        depth: Current depth of serialization to prevent deep recursion.
        visited: Set of visited objects to prevent circular references.

    Returns:
        A dictionary representation of the ORM object or a list of dictionaries.
    """
    if obj is None:
        return None

    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        # Handle lists or other iterable collections of objects
        return [serialize(item, depth=depth, visited=set() if visited is None else visited) for item in obj]

    if visited is None:
        visited = set()

    # Check if object has already been visited to prevent circular reference serialization
    if id(obj) in visited:
        return None

    visited.add(id(obj))

    serialized_data = {}

    try:
        mapper = class_mapper(obj.__class__)
    except SQLAlchemyError:
        # The object is not a valid SQLAlchemy model
        return None

    # Serialize all column properties of the object
    for column in mapper.columns:
        value = getattr(obj, column.name)
        if isinstance(value, datetime):
            value = value.isoformat()
        serialized_data[column.name] = value

    # Handle relationships if depth allows and if they are loaded
    if depth > 0:
        state = inspect(obj)
        for relationship in mapper.relationships:
            if relationship.key not in state.unloaded:  # Check if relationship is loaded
                related_obj = getattr(obj, relationship.key, None)

                if related_obj is None:
                    # If the relationship object is None, set serialized value to None
                    serialized_data[relationship.key] = None
                elif relationship.uselist:
                    # Serialize lists of related objects
                    if depth > 1:
                        serialized_data[relationship.key] = [
                            serialize(item, depth=depth-1, visited=visited) for item in related_obj
                        ]
                    else:
                        serialized_data[relationship.key] = None
                else:
                    # Serialize single related object
                    if depth > 1:
                        serialized_data[relationship.key] = serialize(
                            related_obj, depth=depth-1, visited=visited
                        )
                    else:
                        serialized_data[relationship.key] = None

    visited.remove(id(obj))
    return serialized_data
