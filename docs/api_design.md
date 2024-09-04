# Fund Sage - API Design

## Project Overview

**Fund Sage** is a comprehensive Financial Assistance Scheme Management System designed to showcase best practices in software engineering. The project aims to provide a robust, scalable, and secure solution for managing various financial assistance schemes, enabling administrators to effectively handle applications and applicants. By adhering to industry standards, **Fund Sage** demonstrates the implementation of a RESTful API solution that ensures clarity, efficiency, and maintainability, making it a valuable resource for developers and businesses alike.

## API Design Overview

The **Fund Sage** API is designed following RESTful principles, ensuring a clear, resource-oriented structure. It features robust security measures, including JWT tokens for authentication and authorization, ensuring secure access to sensitive data and operations. The API efficiently handles data through standardized endpoints, promoting ease of use and consistency across the system. This design not only meets functional requirements but also incorporates non-functional aspects such as error handling, authorization checks, and adherence to RESTful best practices.

## Original Requirements

The API design for **Fund Sage** was guided by specific functional and non-functional requirements to ensure a comprehensive solution. 

### Functional Requirements:

- Implement RESTful API endpoints for managing Beneficiaries, Schemes, and Applications.
- Authentication and authorization for frontend and API access management.
- Core endpoints to be implemented include:
  
| Method | Path                                      | Purpose                                                         |
| ------ | ----------------------------------------- | --------------------------------------------------------------- |
| GET    | /api/applicants                           | Get all applicants.                                             |
| POST   | /api/applicants                           | Create a new applicant.                                         |
| GET    | /api/schemes                              | Get all schemes.                                                |
| GET    | /api/schemes/eligible?applicant={id}      | Get all schemes that an applicant is eligible to apply for.     |
| GET    | /api/applications                         | Get all applications.                                           |
| POST   | /api/applications                         | Create a new application.                                       |

### Non-Functional Requirements:

- Proper implementation of RESTful principles.
- Clear and concise endpoints.
- Proper endpoint authorization checks.
- Robust error handling logic.

## Solution Highlights

### Functional Features

1. **Comprehensive Eligibility Assessment**:
   - The `GET /api/schemes/eligible` endpoint returns a full **Schemes Eligibility Assessment Report** for an applicant across all available schemes, detailing both __eligible and ineligible__ schemes. This promotes transparency and helps testers verify thorough scheme evaluation, omitting expired or future schemes.
   - Although the **Schemes Eligibility Assessment Report** reports on all the existing active Schemes in the sytem, the API will only return the full details of the eligible Schemes that are related to the applicant, hence adhering to the original functional requirements.
2. **Application Handling**:
   - The `POST /api/applications` endpoint allows for the creation of new applications:
     - **Auto-approval** for applications to __eligible__ schemes, providing detailed information on the scheme, applicant, and awarded benefits.
     - **Auto-rejection** for applications to __ineligible__ schemes, with full details and reasons for rejection.
     - Ensures each applicant can __Successfully__ apply for each scheme __only once__, but allows __reapplication__ if previously __rejected__ due to changed financial conditions. The system will prevent an existing beneficiary from attempting to apply for the same scheme again.
3. **Household Members**:
   - Whenever an Applicant record is being retrieved, the System will automatically retrieve the details of the Applicant's Household members too. The details of the applicant's household members are considered key data points for executing scheme eligibility decision and benefits computation logic.   

4. **Pagination Support**:
   - Implements pagination for endpoints that retrieve multiple records, enhancing performance and usability.

### Non-Functional Features

1. **Adherence to REST API Best Practices**:
   - Endpoints are designed to follow RESTful principles, ensuring consistency and predictability in API behavior.

2. **Security Measures**:
   - The /auth api endpoint, which performs the user authentications and issues out JWT token to authenticated users, will automatically lock the administrator account after more than 5 (configurable) consecutive failed login attempts within a 10 min timeframe (configurable). This mechanism protects the system against brute force attacks. Locked accounts can be unlocked by another administrator via the /auth/unlock api.
   - The system stores the hash the user password before saving it into the database to protect against password theft.    
   - Utilizes JWT tokens for secure API access, protecting sensitive data and operations.

## API Endpoints and Usage

Below is a detailed breakdown of the API endpoints provided by **Fund Sage**:

| Method | Endpoint                                | Purpose                                                                  | Example Request                      |
| ------ | --------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------ |
| POST   | `/api/auth`                             | User login endpoint. Requires JSON payload with 'username' and 'password'. Returns a JWT access token if authentication is successful. Automatically lock the administrator account after more than 5 (configurable) consecutive failed login attempts within a 10 min timeframe (configurable).|`POST /api/auth`|  
| POST   | `/api/auth/unlock` *(coming soon...)*                     | Unlock a locked admin user account.|`POST /api/auth/unlock`|  
| POST   | `/api/auth/changepassword *(coming soon...)*               | Allows administrator to change his/her current password. Needs to supply the existing password |`POST /api/auth/changepassword`|  
| GET    | `/api/applicants`                       | Retrieve a list of all applicants.                                       | `GET /api/applicants`                |
| POST   | `/api/applicants`                       | Create a new applicant.                                                  | `POST /api/applicants`               |
| GET    | `/api/schemes`                          | Retrieve a list of all schemes.                                          | `GET /api/schemes`                   |
| GET    | `/api/schemes/eligible?applicant={id}`  | Retrieve eligible schemes for a specific applicant.                      | `GET /api/schemes/eligible?applicant=1` |
| GET    | `/api/applications`                     | Retrieve a list of all applications.                                     | `GET /api/applications`              |
| POST   | `/api/applications`                     | Create a new application.                                                | `POST /api/applications`             |

## Use Cases and User Stories

The following user stories guided the design of the **Fund Sage** API, ensuring it meets the needs of system administrators:

1. **View All Schemes**: 
   - *As a system administrator, I want to view all available financial assistance schemes.*
   - The `GET /api/schemes` endpoint provides a list of all schemes, fulfilling this requirement.

2. **Add New Applicants**:
   - *As a system administrator, I want to add new scheme applicants.*
   - The `POST /api/applicants` endpoint allows administrators to add new applicants, ensuring all necessary data is captured before scheme application.

3. **Eligibility Assessment**:
   - *As a system administrator, I want to view the schemes that an applicant is eligible to apply for.*
   - The `GET /api/schemes/eligible?applicant={id}` endpoint provides a comprehensive list of schemes that an applicant is eligible for, based on their data.

## Detailed Software Engineering Principles

For an in-depth understanding of the software engineering principles applied in this project, please refer to the [Detailed Software Engineering Principles](./docs/Detailed_Software_Engineering_Principles.md) document.

---

By adhering to these detailed guidelines and principles, **Fund Sage** ensures a robust, secure, and efficient API that meets the needs of both business analysts and API testers, while providing a solid foundation for future development and scalability.


