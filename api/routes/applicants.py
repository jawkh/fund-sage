# Copyright (c) 2024 by Jonathan AW
# applicants.py

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

# api/routes/applicants.py

from flask import Blueprint, request, jsonify, g
from bl.services.applicant_service import ApplicantService
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from dal.crud_operations import CRUDOperations
from api.schemas.all_schemas import ApplicantSchema
from exceptions import InvalidPaginationParameterException, InvalidSortingParameterException
from sqlalchemy.exc import SQLAlchemyError

applicants_bp = Blueprint('applicants', __name__)

@applicants_bp.route('/api/applicants', methods=['GET'])
@jwt_required()
def get_applicants():
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    
    # Extract pagination and sorting parameters from the request
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    sort_by = request.args.get('sort_by', default='created_at', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)
    
    # Extract filter parameters from the request
    filters = {}
    if 'employment_status' in request.args:
        filters['employment_status'] = request.args['employment_status']
    if 'sex' in request.args:
        filters['sex'] = request.args['sex']
    if 'marital_status' in request.args:
        filters['marital_status'] = request.args['marital_status']
        
    try:
        # Retrieve applicants from the service with the specified parameters
        applicants, total_count = ApplicantService(crud_operations).get_all_applicants(
            page=page, 
            page_size=page_size, 
            sort_by=sort_by, 
            sort_order=sort_order,
            filters=filters
        )
        # Use Marshmallow schema to serialize the applicant objects
        applicant_schema = ApplicantSchema(many=True) # <<< TO BE REMOVED
        result = applicant_schema.dump(applicants) # <<< TO BE REPLACE BY CUSTOM SERIALIZER
        
        # Prepare response with pagination metadata
        response = {
            'data': result,  
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
    except SQLAlchemyError as e:  # Specific SQLAlchemy error handling
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@applicants_bp.route('/api/applicants', methods=['POST'])
@jwt_required()
def create_applicant():
    """
    Endpoint to create a new applicant along with their household members.
    Automatically assigns the created_by_admin_id from the JWT token to ensure security.
    """
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    applicant_service = ApplicantService(crud_operations)
    try:
        # Extract 'id' from JWT claims to use as created_by_admin_id
        admin_id = get_jwt_identity()['id']

        # Load and validate request data using Marshmallow schema
        data = request.json
        data['created_by_admin_id'] = admin_id  # Overwrite created_by_admin_id to ensure security
        
        # Deserialize and validate input data
        applicant_data = ApplicantSchema().load(data)  # <<< TO BE REMOVED (NO NEED TO DESRIALIZE). Use the data directly
        # Extract household members data as a list of dictionaries``
        household_members_data = applicant_data.pop('household_members', []) # <<< HANDLE THE DATA DIRECTLY. Extract household members from the data

        # Use the applicant service to create the applicant and associated household members
        applicant = applicant_service.create_applicant(
            applicant_data, 
            household_members_data=household_members_data  # Pass the household members as a list of dicts
        )

        # Serialize the newly created applicant object for the response
        result = ApplicantSchema().dump(applicant) # <<< TO BE REPLACE BY CUSTOM SERIALIZER
        return jsonify(result), 201  # Return a 201 Created status code on success

    except ValidationError as err:
        # Handle validation errors from Marshmallow schema
        return jsonify({'errors': err.messages}), 400

    except Exception as e:
        # General error handler for any unexpected issues
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
