# ORM Data Access Layer (DAL) ~ DRAFT

The ORM Data Access Layer (DAL) is a foundational component of this project, enabling seamless interaction with the database using SQLAlchemy ORM. This layer is designed with several key software engineering principles and practices to ensure robust, maintainable, and high-performance data handling.

## Key Features and Design Patterns

1. **Object-Relational Mapping (ORM) with SQLAlchemy**:
   - The project uses SQLAlchemy ORM to define the schema and relationships of the database tables. This abstraction allows developers to interact with the database using Python objects, reducing the need for direct SQL queries and enhancing code readability and maintainability.
   - **Example**: The `Administrator` class defines the schema for the `Administrators` table and encapsulates relationships with other tables like `Applicants` and `Applications`.

2. **Data Validation with Check Constraints**:
   - SQLAlchemy Check Constraints are employed to enforce data integrity at the database level, ensuring that only valid data is stored. This reduces the risk of data corruption and enforces business rules directly within the schema.
   - **Example**: The `Applicant` class includes constraints like `CheckConstraint("employment_status IN ('employed', 'unemployed')")`, ensuring that only predefined employment statuses are allowed.

3. **Encapsulation and Separation of Concerns**:
   - The DAL encapsulates all database interactions, providing a clean interface for CRUD operations while adhering to the Single Responsibility Principle (SRP). This separation of concerns makes the codebase more modular and easier to maintain.
   - **Example**: The `CRUDOperations` class contains methods for each CRUD operation, such as `create_administrator()`, `get_administrator()`, and `update_administrator()`, keeping database logic separate from business logic.

4. **Reusability and Maintainability**:
   - The `CRUDOperations` class is designed to be reusable across different parts of the application. By providing a standardized way to perform database operations, this class promotes code reuse and reduces duplication.
   - **Example**: Common operations like `create()`, `update()`, and `delete()` are defined once and reused throughout the application, which simplifies maintenance and reduces errors.

5. **Type Annotations and Readability**:
   - Type annotations are extensively used throughout the codebase to specify the types of function arguments and return values. This enhances code readability and helps with static type checking, reducing bugs and improving developer productivity.
   - **Example**: Method signatures in the `CRUDOperations` class, such as `def get_administrator(self, admin_id: int) -> Optional[Administrator]:`, provide clear expectations about input and output types.

6. **Advanced Serialization Techniques**:
   - A custom serializer function is used to convert SQLAlchemy ORM objects into JSON-serializable dictionaries. This serializer supports deep object graph traversal with configurable depth, preventing circular references and making it easy to serialize complex objects.
   - **Example**: The `serialize()` function in `utils/serializer.py` handles serialization of ORM objects, including relationships, with proper depth management to avoid recursion issues.

7. **Error Handling and Robustness**:
   - Comprehensive error handling is implemented to manage SQLAlchemy exceptions and ensure database operations do not leave the system in an inconsistent state. Transactions are rolled back in case of errors to maintain data integrity.
   - **Example**: In methods like `create_applicant()` and `create_household_member()`, SQLAlchemy errors are caught and transactions are rolled back to prevent partial updates.

8. **Support for Pagination and Sorting**:
   - The DAL supports pagination and sorting out of the box, making it easy to handle large datasets efficiently. This is particularly useful for endpoints that return lists of items, ensuring performance and usability are maintained.
   - **Example**: Methods like `get_all_applicants()` and `get_all_applications()` include parameters for `page`, `page_size`, `sort_by`, and `sort_order` to support flexible data retrieval.

9. **Normalization and Referential Integrity**:
   - The database schema is designed with normalization principles to minimize redundancy and ensure data integrity. Foreign key constraints enforce referential integrity, linking related tables and maintaining consistent relationships.
   - **Example**: ForeignKey relationships, such as `applicant_id` in the `Application` class, ensure that each application is associated with a valid applicant, maintaining data consistency.

10. **Configuration and Flexibility**:
    - The DAL is flexible and easy to configure, with support for multiple database backends and environments (development, testing, production). The use of SQLAlchemy's session management and environment-specific configurations ensures seamless integration and deployment.
    - **Example**: The `Session` object is passed to the `CRUDOperations` class, allowing for easy switching betI en different database connections and settings.

By adhering to these best practices and leveraging poI rful tools like SQLAlchemy ORM, our project’s data access layer is both robust and flexible, supporting the needs of modern web applications.

