# 💰 FundSage

> **TL;DR:**  
> **FundSage** is a showcase project crafted to highlight best practices in software engineering within a simulated Financial Assistance Scheme Management System. 🚀 This project demonstrates the application of **SOLID design principles**, robust testing strategies, and streamlined deployment processes. Dive into our documentation to set up the project on your local machine or to explore the architecture and design decisions in depth! 📚


## 🌟 Overview

**FundSage** is a fictitious system designed to manage various financial assistance schemes, including their eligibility criteria, application processes, and benefit distribution. This project showcases clean, maintainable, and scalable software engineering practices, making it an invaluable learning resource for both novice and experienced developers. 🚀

## 🔑 Key Features

- **🔧 Adherence to Software Engineering Principles**: The codebase strictly follows best practices like SOLID principles, well-architectured enterprise solution design, proper implementation of RESTful principles and good coding and extensive testing practices to ensure clean and effective code that has good quality, readabilty, maintainability and extensibility.

- **🔍 Extensibility with SOLID Design Principles**: FundSage is built with SOLID principles at its core, allowing for easy extensibility and maintenance:
  - **📝 Single Responsibility Principle (SRP)**: Each class or module is dedicated to a single responsibility, enhancing clarity and reducing complexity.
  - **🚪 Open/Closed Principle (OCP)**: The system is designed to be open for extension but closed for modification, making it easy to add new schemes without altering existing code.
  - **🔄 Liskov Substitution Principle (LSP)**: Ensures that objects of a superclass can be replaced with objects of a subclass without impacting the functionality, supporting a robust inheritance structure.
  - **🔗 Interface Segregation Principle (ISP)**: Prefers multiple, client-specific interfaces over a single general-purpose interface, avoiding unnecessary methods and enhancing flexibility.
  - **🔄 Dependency Inversion Principle (DIP)**: Promotes a decoupled architecture by ensuring high-level modules are not dependent on low-level modules; both rely on abstractions.

- **🗄️ ORM for Data Persistence**: Utilizes SQLAlchemy for efficient data management, clearly separating business logic from data access layers.

- **🔄 Database Synchronization**: Automatically handles database schema changes with migration scripts, keeping your data model in sync.

- **✅ Quality Assurance with Pytest**: Implements a comprehensive testing strategy using Pytest to cover unit, integration, and end-to-end tests, ensuring code reliability and robustness.

- **📦 Container Packaging**: Uses Docker for containerization to streamline deployment, encapsulating the entire application environment for consistent development and production stages.

## 📂 Project Folder Structure at a Glance

```
Project_Root
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
├── bin/
│       ├── __init_sys_database.py # database initialization scripts
│       ├── ...
│       ├── tests_all.sh # automated test scripts
│       └── ...
├── init-db
│       └── create_db_ephemeral.sql # script for provisioning the ephemeral test database for automated test scripts. 
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
├── tests/                   # Home of all the Test files
│   ├── api_tests/            # automated api tests  
│   ├── bl_tests /           # automated business layer tests
│   ├── dal tests/            # automated data access layer tests
│   ├── util tests/           # automated utilities tests
│   └── conftest.py          # text fixtures
├── utils/
│   ├── ...                  # Utility functions and helpers
├── .env copy                # Environment variables Templates
├── config.py                # Flask's configurations
├── poetry.lock              # Fuill Manifests of the Project's python dependencies
├── pyproject.toml           # Explicitly declared project's python dependencies
├── Dockerfile     # Dockerfile for FundSage Container image
├── docker-compose.yml # for packaging and deploying multi-containers solution
├── wait-for-it.ini # util for deployment dependencies
├── README.md                # This page itself 
└── ...
```

## 📚 Documentation Hub

Explore our comprehensive documentation to master the software engineering practices used in FundSage! All documents are available in the `docs/` directory:

### 🚀 [Quick Start - Minimal Setup Guide for FundSage](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/deployment_guide.md)
Kick off your journey with FundSage! Follow this minimal setup guide to get up and running quickly.

### 🌐 [API Design](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/api_design.md) 
Dive deep into the RESTful API design. Learn about endpoints, request/response formats, and error handling strategies to integrate smoothly with FundSage.

### 🛠️ [API Testing Guide - POSTMAN](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/api_testing.md) 
Get ready for hands-on testing! This guide will soon provide step-by-step instructions for setting up API endpoints in VSCode or Docker and manually testing them with POSTMAN.

### 💻 [Setup Guide for Developers](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/setup_guide_for_dev.md)
Set up your development environment like a pro! Follow these instructions to configure your tools and debug your code using Visual Studio Code.

### 🗄️ [Database and Data Access Layer Design](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/db_design.md) 
Understand the foundations of FundSage's database schema and ORM choices. This document covers all the design decisions made for data management.

### 🛡️ [Software Engineering Principles](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/sw__eng_principles.md) 
Discover the core principles and best practices that guide the development of FundSage. This document provides a comprehensive overview of our software engineering philosophy.

### 🏗️ [Business Layer Design](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/bl_design.md) 
Explore the design patterns and architectural principles used in the business layer of FundSage. Gain insights into how FundSage structure and manage business logic.

### ✅ [Robust Testing Strategy](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/testing_strategy.md)
Testing is key! Learn about FundSage's wide-coverage automated regression testing approach that has saved me countless times. 🛡️



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
