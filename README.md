# FundSage

> **TL;DR:**  
> FundSage is a showcase project designed to demonstrate best practices in software engineering within a simulated Financial Assistance Scheme Management System. This project illustrates the application of SOLID design principles, robust testing strategies, and efficient deployment processes. Follow the steps below to get the project up and running on your local machine, and explore our documentation for a deeper understanding of the architecture and design decisions.

## Overview

FundSage is a fictitious system crafted to manage various financial assistance schemes, their eligibility criteria, applications, and benefit distribution. This project is built to highlight clean, maintainable, and scalable software engineering practices, making it an excellent resource for both novice and experienced developers.

## Key Features

- **Adherence to Software Engineering Principles**: Implements SOLID principles, DRY (Don't Repeat Yourself), and KISS (Keep It Simple, Stupid) throughout the codebase.
- **Extensibility with SOLID Design Principles**: Adheres to SOLID principles to ensure the system is easily extensible and maintainable:
    - **Single Responsibility Principle (SRP)**: Each class or module has a single, well-defined responsibility, enhancing code clarity and reducing complexity.
    - **Open/Closed Principle (OCP)**: The system is open for extension but closed for modification, allowing new schemes to be added without changing existing code.
    - **Liskov Substitution Principle (LSP)**: Objects of a superclass can be replaced with objects of a subclass without affecting the application, ensuring robust inheritance hierarchies.
    - **Interface Segregation Principle (ISP)**: Many client-specific interfaces are better than one general-purpose interface, preventing the implementation of unnecessary methods.
    - **Dependency Inversion Principle (DIP)**: High-level modules are not dependent on low-level modules; both depend on abstractions, fostering a decoupled architecture.
- **ORM for Data Persistence**: Efficient data management using SQLAlchemy, ensuring a clear separation between business logic and data access layers.
- **Database Synchronization**: Automatic handling of database schema changes through migration scripts.
- **Quality Assurance with Pytest**: Comprehensive testing strategy covering unit, integration, and end-to-end tests to ensure code reliability and robustness.
- **Container Packaging**: Simplified deployment using Docker to encapsulate the entire application environment, ensuring consistency across different stages of development and production.

```
MyProject
├── api/                     # Presentation Layer (API frontend)
│   ├── __init__.py          # Initialize Flask app and configure extensions
│   ├── routes/
│   │   ├── __init__.py      # Initialize routes
│   │   ├── applicants.py    # Endpoint for applicant operations
│   │   ├── schemes.py       # Endpoint for scheme operations
│   │   ├── applications.py  # Endpoint for application operations
│   │   └── auth.py          # Endpoint for authentication
│   └── schemas/
│       ├── __init__.py      # Initialize schemas (mostly deprecated - retained only for basic PL input validations)
│       ├── applicant.py     # Marshmallow schema for Applicant
│       ├── scheme.py        # Marshmallow schema for Scheme
│       └── application.py   # Marshmallow schema for Application
├── bl/                      # Business Layer
│   ├──factories/            # BL Artefacts (Factory Pattern for contructing Schemes Strategy)
│   ├──schemes/              # BL Artefacts (Strategy Pattern for custom Schemes Business Logic)
│   ├──services/             # BL Artefacts (Business Services - 1-to-1 with DAL for encapsulation)
│   └── ..
├── dal/                     # Data Access Layer
│   ├── crud_operations.py   # CRUD operations
│   ├── models.py            # ORM models
│   └── ..
├── docs/                    # placeholders for all the project markdown documentations
│   └── ..
├── imgs/                    # placeholders for images used for project markdown documentations
│   └── ..
├── logs/                    # logs from executing the python database provisioning scripts ,pytests scripts or Flasks app
│   ├── versions/            # Migration scripts
│   └── env.py               # Migration environment setup
├── tests/                   # Home of all the Test files
│   ├── api_tests            # automated api tests  
│   ├── bl_tests             # automated business layer tests
│   ├── dal tests            # automated data access layer tests
│   ├── util tests           # automated utilities tests
│   └── conftest.py          # text fixtures
├── utils/
│   ├── ...                  # Utility functions and helpers
├── .env copy                # Environment variables Templates
├── config.py                # Flask's configurations
├── poetry.lock              # Fuill Manifests of the Project's python dependencies
├── pyproject.toml           # Explicitly declared project's python dependencies
├── README.md                # This page itself (:
└── ...
```

## Getting Started ~ (*draft instructions*)

### Prerequisites

To set up the development environment for FundSage, you'll need the following (I use Windows WSL2 personally):

- **Operating System**: Ubuntu Linux Distro [or Windows WSL 2 with Ubuntu Distro]
- **IDE**: Visual Studio Code
- **Docker**: Docker [ or Docker Desktop for Windows] 
- **Version Control**: Git Client

### Platform & Tools Setup

#### 1. Python 3

Ensure Python 3.10+ is installed on your machine. You can download the installer from the [official Python website](https://www.python.org/downloads/).

#### 2. Poetry for Package and Dependency Management

Poetry simplifies dependency management and ensures the environment is consistent across different setups.

- **Install Poetry**: Follow the instructions on the official Poetry website to install it.
- **Install Dependencies**: Once Poetry is installed, navigate to the project directory and run:
    
    ```bash  
    poetry install
    ```
    This will install all dependencies listed in the `pyproject.toml` and `poetry.lock` files, including `pytest` for testing, `SQLAlchemy` for ORM, and `Flask` for REST API development.

#### 3. PostgreSQL

Set up PostgreSQL using Docker:

- **Run PostgreSQL Docker Container**:
    ```bash
    docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
    ```
    Replace `mysecretpassword` with a secure password of your choice.

#### 4. pgAdmin4

For managing the PostgreSQL database, you can either install pgAdmin4 on Windows or run it in Docker:

- **Run pgAdmin4 Docker Container**: *single line command*
    ```bash
    docker run -p 80:80 --name pgadmin -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" -e "PGADMIN_DEFAULT_PASSWORD=admin" -d dpage/pgadmin4
    ```
Replace the email and password with your credentials.

#### 5. Postman for API Testing

Download and install Postman for manual API testing.

### Custom Setup Steps

#### 1. Cloning the Git Repository

Clone the FundSage repository from GitHub

    ```bash 
    git clone https://github.com/jawkh/gt_cdt_swe_test.git cd gt_cdt_swe_test
    ```   

#### 2. Setting Up VSCode for Debugging

Configure VSCode for debugging by adding the following to your `.vscode/launch.json` file:

    ```
    {
        "name": "Python: Flask",
        "type": "debugpy",
        "request": "launch",
        "module": "flask",
        "env": {
            "FLASK_APP": "api",
            "FLASK_ENV": "development",
            "FLASK_DEBUG": "1"
        },
        "args": [
            "run",
            "--no-debugger",
            "--no-reload"
        ],
        "jinja": true,
        "justMyCode": false
    }
    ```

#### 3. Running Database Setup Scripts on PostgreSQL

Run the provided Python scripts in the `/bin` folder to set up the database and prepopulate it with test records, including: 

- Administrators (for accessing the system)
- Supported Schemes
- Sample Applicants so that you can copy their profile for your own PostMan testing
- Sample Applications for testing the Application queries in PostMan

**Generate Database Schema**:

    ```bash
    poetry run python3 bin/__init_sys_database.py
    ```    

**Pre-populate Database with Sample Records**:
    
    ```bash
    poetry run python bin/__data_prep_administrators.py
    poetry run python bin/__data_prep_supported_schemes.py
    poetry run python bin/__data_prep_random_applicants.py
    poetry run python bin/__data_prep_applications.py
    ```

#### 4. Setting Up the .env File

Create a `.env` file in the root directory of the project using the `env copy` template provided:

    ```bash
    cp .env.example .env
    ```

Edit the `.env` file to include your database credentials and any other necessary configuration.

#### 5. Running Pytest Scripts

Run all tests using the bash shell scripts located in the `/bin` folder:

    ```bash
    bash bin/tests_all.sh`
    ```

## Documentation

For detailed information on the software engineering practices applied, please refer to the following documents in the `docs/` directory:

- [**Software Engineering Principles**](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/sw__eng_principles.md): In-depth explanation of the principles and patterns applied in the project. ~ coming soon...
- [**Database and Data Access Layer Design**](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/db_design.md): Overview of the database schema and decisions made in the design process. ~ coming soon...
- [**API Design**](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/api_design.md): Details on the RESTful API design, including endpoints, request/response formats, and error handling strategies. 
- [**API Testing Guide - POSTMAN**](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/api_testing.md): Step-by-step instructions for setting up the API endpoints on your VSCode IDE or a Docker container and manual testing guide for POSTMAN. ~ coming soon...  
- [**Deployment Guide**](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/deployment_guide.md): Instructions on how to package and deploy the application using Docker. ~ coming soon...


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
