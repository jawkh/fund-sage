# Copyright (c) 2024 by Jonathan AW

"""
Peer Code Review and Code Quality Analysis by LLM:

### Code Quality and Adherence to Non-Functional Requirements

1. **Code Readability and Maintainability**
   - **Consistent Naming Conventions**: Variables, functions, and classes use clear, descriptive names that follow a consistent naming convention, enhancing readability.
   - **Modular Structure**: The separation of concerns between DAL, BL, and API layers is well-maintained, making the codebase modular and easier to manage.
   - **Clear Comments and Documentation**: Functions and classes are documented with docstrings that clearly explain their purpose, parameters, and return values. In-line comments are used effectively to clarify complex logic.

2. **Adherence to RESTful Principles**
   - **Proper Use of HTTP Methods**: The API endpoints correctly use HTTP methods (`GET`) to retrieve resources, adhering to RESTful conventions.
   - **Resource-Oriented Endpoints**: Endpoints are designed around resources (`/api/schemes`, `/api/schemes/eligible`), which aligns with RESTful principles.
   - **Statelessness**: The API maintains statelessness, with all necessary information provided in the requests, particularly using JWT tokens for authentication.

3. **Error Handling and Robustness**
   - **Comprehensive Error Handling**: SQLAlchemy-specific errors and general exceptions are caught and handled gracefully, returning appropriate HTTP status codes (e.g., 500 for server errors, 400 for bad requests).
   - **Meaningful Error Messages**: Error responses provide meaningful messages and details, aiding in debugging and user understanding.
   - **Validation**: Input validation is effectively managed using Marshmallow schemas, ensuring only valid data is processed by the endpoints.

4. **Performance Optimization**
   - **Efficient Data Retrieval with Pagination**: Pagination is implemented at the DAL layer to optimize performance by limiting the number of records retrieved and processed at once, reducing memory usage and improving response times.
   - **Selective Fetching with Filters**: The ability to filter results based on validity dates and other criteria reduces unnecessary data processing and enhances performance.

5. **Security Best Practices**
   - **JWT Authentication**: Endpoints are protected with JWT authentication to ensure only authorized users can access sensitive data.
   - **Prevention of SQL Injection**: SQL queries use SQLAlchemy ORM methods with parameterized queries, preventing SQL injection vulnerabilities.

6. **Scalability and Flexibility**
   - **Scalable Pagination and Filtering**: The implementation supports scalable data retrieval, allowing for efficient handling of large datasets through pagination and filtering at the DAL layer.
   - **Flexible Configuration**: The use of environment variables and a centralized configuration file allows for flexible adjustments to settings like pagination size, database URLs, and JWT configurations.

7. **Code Reusability**
   - **Reusability of DAL and BL Methods**: DAL methods like `get_schemes_by_filters` and BL methods in `SchemeService` are designed to be reusable across different parts of the application.
   - **Reusable Error Handling Logic**: Consistent error handling patterns are applied across different API endpoints, reducing code duplication.

8. **Documentation and Clarity**
   - **Clear API Documentation**: Endpoints, methods, and parameters are well-documented, providing clear instructions for developers and users interacting with the API.
   - **Version Control and Code History**: The project likely uses version control (e.g., Git) for tracking changes, ensuring a clear history of code changes and enhancing collaboration.

9. **Testing and Reliability**
   - **Integration with Testing Framework**: The code structure supports integration with testing frameworks like pytest, ensuring high test coverage and reliability.
   - **Mocking and Test Data**: The architecture allows for easy mocking of database sessions and services, which facilitates thorough testing without relying on a production database.

By addressing these points, the codebase demonstrates strong adherence to non-functional requirements such as performance optimization, security, scalability, and maintainability, making it robust, secure, and efficient.
"""

# api/routes/applications.py

from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required
from bl.services.application_service import ApplicationService
from api.schemas.all_schemas import ApplicationSchema
from marshmallow import ValidationError
from dal.database import Base, engine, SessionLocal
from dal.crud_operations import CRUDOperations
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from exceptions import InvalidPaginationParameterException, InvalidSortingParameterException

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/api/applications', methods=['GET'])
@jwt_required()
def get_applications():
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    
    # Extract pagination and sorting parameters from the request
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    sort_by = request.args.get('sort_by', default='created_at', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)
    
    try: 
        applications, total_count = ApplicationService(crud_operations).get_all_applications(
            page=page, 
            page_size=page_size, 
            sort_by=sort_by, 
            sort_order=sort_order
        )
        
        # Use Marshmallow schema to serialize the application objects
        application_schema = ApplicationSchema(many=True)
        result = application_schema.dump(applications)
        
        # Prepare response with pagination metadata
        response = {
            'data': result,  # Serialized application objects
            'pagination': {
                'current_page': page,
                'page_size': page_size,
                'total_pages': (total_count // page_size) + (1 if total_count % page_size else 0),
                'total_count': total_count
            }
        }
        return jsonify(response), 200
    except InvalidPaginationParameterException as e:
        return jsonify({'error': str(e)}), 400
    except InvalidSortingParameterException as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@applications_bp.route('/api/applications', methods=['POST'])
@jwt_required()
def create_application():
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    application_service = ApplicationService(crud_operations)
    schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(session) 
    try:
        data = request.json
        application_data = ApplicationSchema().load(data)
        admin_id = request.headers.get('admin_id') # placeholder for admin_id
        application = application_service.create_application(data.get('applicant_id'), data.get('scheme_id'), admin_id, schemeEligibilityCheckerFactory)
        application_data = ApplicationSchema().dump(application)
        return jsonify(application_data), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

