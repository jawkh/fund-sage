# 🛠️ API Testing Guide - POSTMAN or Swagger UI

## Subtitle:
Get ready for hands-on testing! This guide provides step-by-step instructions for setting up API endpoints in VSCode or Docker and manually testing them with POSTMAN or Swagger UI.

---

## Introduction

Welcome to the API Testing Guide for FundSage! In this guide, we'll walk through the process of manually testing the FundSage API using POSTMAN and Swagger UI. API testing is crucial for ensuring that your endpoints are working as expected, handling requests and responses correctly, and providing a smooth experience for users. Whether you're a developer, tester, or just getting started with APIs, this guide will help you understand how to test API endpoints effectively.

## API Specifications
FundSage's API Specifications are completely defined within an openapi.yaml file that is available at http://{fund-sage-baseurl}/openapi.yaml.

The following best practices have been implemented to make it more user-friendly and provides clearer guidance for developers interacting with the API through Swagger UI or other tools.

### Best Practices Incorporated:
**Enum Definitions for Query Parameters:**
- Added `enum` properties to query parameters to provide hints in Swagger UI, such as for `sort_order`, `employment_status`, `sex`, and `marital_status`.

**Example Payloads for POST Requests:**
- Provided detailed example payloads in the `requestBody` section of `POST` requests, guiding users on the expected format and structure.

**Security Schemes:**
- Added `bearerAuth` security scheme to specify that JWT tokens should be used for authentication, enhancing the understanding of authentication requirements.

**Schema References and Descriptions:**
- Defined and referenced schemas for request and response bodies, providing clarity and reducing redundancy.
- Added comprehensive descriptions for each schema property to enhance understanding.
- Use the required array to list all fields that are mandatory. Fields not listed are considered optional.
- Use the required keyword within each parameter definition to indicate if it is mandatory (required: true) or optional (required: false).

**Pagination and Sorting Parameters:**
- Included pagination and sorting parameters in the `GET` endpoints to clarify their usage and enhance the user experience.

**Use of `description` for Parameters and Properties:**
- Added description fields to all parameters and schema properties to provide more context and clarity.

**Error Handling and Responses:**
- Defined error responses for various status codes (e.g., `400`, `401`, `500`) to guide users on how to handle different error scenarios.

**JWT Authentication Indication:**
- Added security schemes and applied them to endpoints requiring JWT authentication, ensuring users are aware of authentication needs.

## Before You Begin
Followed one of the relevant guides provided in our 📚 Documentation Hub to deploy FundSage into your environment. 
- 🚀 [Quick Start - Minimal Setup Guide for FundSage](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/deployment_guide.md)
- 💻 [Setup Guide for Developers](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/setup_guide_for_dev.md)

You are highly encouraged to read through 🌐 [API Design](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/api_design.md) beforehand to understand the business logic of the FundSage APIs that you are going to test to familiarize yourself with the business logic.   

## Step-by-Step Guide

### Testing the FundSage API with POSTMAN

POSTMAN is a powerful tool for testing APIs, allowing you to send requests and view responses. Follow these steps to set up and test the FundSage API with POSTMAN:

1. **Install POSTMAN**:
   - Download and install POSTMAN from the [official website](https://www.postman.com/downloads/).

2. **Set Up Your Environment**:
   - Open POSTMAN and create a new environment. You can name it `FundSage`.
   - Add environment variables for `BASE_URL` (e.g., `http://localhost:5000`) and any other variables like `JWT_TOKEN`.

3. **Import OpenAPI Specification**:
   - Go to `File > Import`, then choose `Link`.
   - Paste the URL of your `openapi.yaml` file (e.g., `http://localhost:5000/openapi.yaml`).
   - Click `Import` to load all API endpoints into POSTMAN.

4. **Testing an Endpoint**:
   - Select an endpoint from the imported collection, such as `POST /api/auth/login`.
   - Enter the necessary parameters and headers (like `Content-Type: application/json`).
   - Click `Send` to make a request. 
   - View the response in the `Response` tab. Check the status code, response body, and headers to verify the API's behavior.

5. **Authentication Handling**:
   - For endpoints requiring authentication, ensure you retrieve a JWT token first by hitting the `/api/auth/login` endpoint.
   - Save the token in your environment variables (e.g., `JWT_TOKEN`).
   - Use this token in the `Authorization` header for subsequent requests (e.g., `Bearer {{JWT_TOKEN}}`).

### Setting Up Swagger UI for API Testing

Swagger UI provides an interactive, browser-based interface for exploring and testing your API endpoints. Here's how to use Swagger UI for FundSage:

1. **Access Swagger UI**:
   - Start your Flask application with Docker or VSCode, then open your browser and navigate to `http://localhost:5000/swagger`.

2. **Explore API Endpoints**:
   - Swagger UI will display all available API endpoints from the `openapi.yaml` file.
   - Click on any endpoint (e.g., `GET /api/applicants`) to expand its details, including parameters, responses, and a `Try it out` button.

3. **Test Endpoints Directly**:
   - Click `Try it out` for the endpoint you want to test.
   - Enter any required parameters and click `Execute`.
   - Swagger UI will display the request URL, response status, headers, and body. Review these to ensure the endpoint is functioning correctly.

4. **Handling Authentication**:
   - Use the `Authorize` button on the top right to input your JWT token. Swagger UI will handle adding the `Authorization` header to your requests automatically.

## Comparison of POSTMAN and Swagger UI

| Feature           | POSTMAN                                          | Swagger UI                                      |
|-------------------|--------------------------------------------------|-------------------------------------------------|
| **Ease of Use**   | Intuitive interface, supports collections.       | Straightforward, especially for testing directly from docs. |
| **Setup Time**    | Requires installation and environment setup.     | Quick setup; just run in a browser.             |
| **Features**      | Advanced features like scripting, automated tests, and monitors. | Basic testing features, best for interactive API exploration. |
| **Integration**   | Integrates well with CI/CD tools and development environments. | Primarily used for API documentation and quick tests. |
| **Pros**          | Great for complex testing, automation, and environment management. | Ideal for quickly testing and understanding API endpoints. |
| **Cons**          | Can be overkill for simple tasks.                | Lacks advanced testing features.                |

### Which One to Use?

- **Use POSTMAN** if you need advanced testing features, automated test scripts, or want to integrate API testing into your CI/CD pipeline.
- **Use Swagger UI** if you’re looking to quickly test endpoints directly from the API documentation, or if you want a straightforward tool for exploring API behavior without additional setup.

## API Testing Tips

1. **Handle Authentication**: Always ensure you have a valid token for endpoints requiring authentication. Update tokens regularly in your environment settings in POSTMAN or Swagger UI.
   
2. **Test Different Request Methods**: Use POSTMAN or Swagger UI to test all CRUD operations (GET, POST, PUT, DELETE) to ensure your API handles them correctly.

3. **Validate Responses**: Always check the status codes, headers, and body of the responses. Ensure that error codes like 400, 401, and 500 are handled correctly by your application.

4. **Automate Testing Scenarios**: Use POSTMAN’s scripting and automation features to create repeatable test scenarios. Automating these tests helps catch regressions quickly.

5. **Use Environment Variables**: In POSTMAN, use environment variables to manage different configurations like API endpoints, tokens, and user credentials. This makes your tests more flexible and easier to manage.

6. **Document Edge Cases**: Make sure to test and document how your API handles edge cases such as invalid data, unauthorized access, or unexpected input formats.

## Conclusion

Testing your API thoroughly is crucial for ensuring it performs as expected and handles all scenarios gracefully. Whether you choose POSTMAN or Swagger UI, both tools provide excellent features for manual API testing. Use the comparison and tips in this guide to decide which tool best suits your needs, and start testing your FundSage API today!

Happy Testing! 🚀
