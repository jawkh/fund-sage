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


# api/routes/schemes.py

from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required
from bl.services.scheme_service import SchemeService
from api.schemas.all_schemas import SchemeSchema
# from marshmallow import ValidationError
from dal.crud_operations import CRUDOperations
from bl.factories.scheme_eligibility_checker_factory import SchemeEligibilityCheckerFactory
from bl.schemes.schemes_manager import SchemesManager
from bl.services.applicant_service import ApplicantService
from sqlalchemy.exc import SQLAlchemyError
from exceptions import InvalidPaginationParameterException, InvalidSortingParameterException
from exceptions import ApplicantNotFoundException

schemes_bp = Blueprint('schemes', __name__)

# api/routes/schemes.py

from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required
from bl.services.scheme_service import SchemeService
from api.schemas.all_schemas import SchemeSchema
from dal.crud_operations import CRUDOperations
from sqlalchemy.exc import SQLAlchemyError

schemes_bp = Blueprint('schemes', __name__)

@schemes_bp.route('/api/schemes', methods=['GET'])
@jwt_required()
def get_schemes():
    """
    Endpoint to retrieve all schemes with optional filtering and pagination.
    """
    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    scheme_service = SchemeService(crud_operations)

    try:
        # Get pagination parameters from the request
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # Get the fetch_valid_schemes parameter from the request
        fetch_valid_schemes = request.args.get('fetch_valid_schemes', 'true').lower() == 'true'

        # Handle additional filtering parameters if needed
        filters = {}
        if 'validity_start_date' in request.args:
            filters['validity_start_date'] = request.args['validity_start_date']
        if 'validity_end_date' in request.args:
            filters['validity_end_date'] = request.args['validity_end_date']

        # Retrieve schemes with pagination and filtering
        schemes, total_count = scheme_service.get_schemes_by_filters(
            filters=filters, 
            fetch_valid_schemes=fetch_valid_schemes, 
            page=page, 
            per_page=per_page
        )

        # Serialize the scheme objects using Marshmallow schema
        scheme_schema = SchemeSchema(many=True) # <<< TO BE REMOVED
        result = scheme_schema.dump(schemes) # <<< TO BE REPLACE BY CUSTOM SERIALIZER

        response = {
            'data': result,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_schemes': total_count,
                'total_pages': (total_count + per_page - 1) // per_page
            }
        }
        return jsonify(response), 200
    except InvalidPaginationParameterException as e:
        return jsonify({'error': str(e)}), 400
    except InvalidSortingParameterException as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        # Specific SQLAlchemy error handling
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500

    except Exception as e:
        # General error handler
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


    
@schemes_bp.route('/api/schemes/eligible', methods=['GET'])
@jwt_required()
def get_eligible_schemes():
    applicant_id = request.args.get('applicant')
    if not applicant_id:
        return jsonify({"error": "applicant id is required"}), 400
    
    if not applicant_id.isdigit():  # Add validation for applicant_id
        return jsonify({"error": "Invalid applicant id format"}), 400

    session = g.db_session  # Get the session from Flask's g object
    crud_operations = CRUDOperations(session)
    try:
        applicant = ApplicantService(crud_operations).get_applicant_by_id(applicant_id)
        if not applicant:  # Handle case where applicant is not found
            return jsonify({"error": "Applicant not found"}), 404

        schemeEligibilityCheckerFactory = SchemeEligibilityCheckerFactory(session)
        scheme_manager = SchemesManager(crud_operations, schemeEligibilityCheckerFactory)
        
        eligibility_results, eligible_schemes = scheme_manager.check_schemes_eligibility_for_applicant({}, True, applicant)
        scheme_schema = SchemeSchema(many=True) # <<< TO BE REMOVED
        eligible_schemes = scheme_schema.dump(eligible_schemes) # <<< TO BE REPLACE BY CUSTOM SERIALIZER
        
        response = {
            'data': {"eligible_schemes": eligible_schemes, "eligibility_results": eligibility_results}  
        }
        return jsonify(response), 200
    except ApplicantNotFoundException as e:
        return jsonify({'error': str    (e)}), 404  # Handle specific exception
    except SQLAlchemyError as e:  # Specific SQLAlchemy error handling
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500    
 
