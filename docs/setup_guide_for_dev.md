# Setup Guide for Developers

## 1. Introduction and Overview

### Purpose

This guide provides detailed instructions for deploying the **FundSage** application using Docker Compose for development or testing environments (Option 1). It also offers a high-level overview of deploying a scalable, multi-tier architecture suitable for staging or production environments (Option 2).

### Scope

- **Option 1 (Docker-Compose)**: A multi-container setup suitable for development and testing environments.
- **Option 2 (Scalable Deployment)**: An overview for staging or production environments using scalable deployment techniques.

### Audience

This guide is intended for developers and DevOps engineers familiar with Docker, Python, and VSCode.

## 2. Deployment Options Overview

### Option 1: Docker-Compose Setup

- **Purpose**: Quickly set up a development or testing environment with all dependencies using Docker Compose.
- **Components**:
  - **FundSage Flask Application**: Python-based backend application.
  - **PostgreSQL Database**: Stores application data.
  - **pgAdmin4**: Database management tool.
- **Benefits**:
  - Environment consistency across development and testing.
  - Simplifies setup with all dependencies containerized.

### Option 2: Scalable Deployment (Overview)

- **Purpose**: Suitable for staging and production environments with scalable, multi-tier architecture.
- **Components**:
  - **FundSage Flask Application**: Deployed separately for scalability.
  - **PostgreSQL Database**: Deployed in a managed cloud database service for high availability.
  - **Networking and Security**: Configurations for secure communication between services.
- **Future Guide**: Detailed instructions will be provided in a separate guide in the future.

## 3. Prerequisites

### General Requirements

- Basic knowledge of software development and VSCode.
- Familiarity with Docker and Python.

### Setup Instructions

- **For Windows Users**: Install WSL2 and Docker Desktop with WSL2 integration enabled.
- **For Ubuntu Users**: Install Docker and Docker Compose natively.

#### Installing Docker and Docker-Compose

- **Windows WSL2**:
  1. Install Docker Desktop and enable WSL2 integration.
  2. Install Docker Compose as part of Docker Desktop.
- **Ubuntu**:
  ```bash
  sudo apt update
  sudo apt install docker.io docker-compose
  sudo systemctl start docker
  sudo systemctl enable docker
  ```

## 4. Detailed Step-by-Step Instructions for Option 1 (Docker-Compose)

### 1. Environment Setup

Ensure Docker and Docker Compose are installed and running.

### 2. Project Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jawkh/gt_cdt_swe_test.git <project-root-folder>
   ```

2. **Open Project in VSCode**:
   ```bash
   code <project-root-folder>
   ```

3. **Install Recommended VSCode Plugins**:
   - Python
   - Docker
   - Python Test Explorer for Visual Studio Code

### 3. Python Environment Configuration

1. **Install Poetry**:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Configure Poetry for Project**:
   ```bash
   cd <project-root-folder>
   poetry install
   ```

3. **Set up Virtual Environment**:
   - Set up the Poetry virtual environment as the Python interpreter in VSCode.
   - Refer to the [Setup VS Code to debug Python Code and run Pytest](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/Refer/setup_VSCode_for_debugging.md)

### 4. Application Configuration

- **Configure Environment Variables**:
  1. Rename `.env copy` to `.env`:
     ```bash
     mv .env\ copy .env
     ```
  2. Use default values for a local development environment.

### 5. Deploy with Docker-Compose

1. **Build and Run Containers**:
   ```bash
   docker-compose up --build
   ```

2. **Deployment Process**:
   - Docker Compose will start the PostgreSQL, FundSage Flask App, and pgAdmin4 containers.
   - The PostgreSQL container is initialized with two databases (`fund_sage_db` and `fund_sage_db_ephemeral`).
   - The Flask application initializes the database schema and provisions necessary data. 
   - The idempotent Database initialization scripts which provision the database schema, provision the Administrator accounts for the FundStage Application and the Supported Funding Schemes will always be executed whenever the FundSage container is started. These ensure the essential records to initate the freshly deployed system to a usable state are always avaiable before the FundSage Flask Application is started. 
   - The scripts for generating Sample Applicants and create Applications for each Applicants for each supported Funding Schemes in the system are non-idempotent. They will always create more records whenever the scripts are being executed. The intention for running these optional scripts is to enrich the system's database with sufficient data for testing and demo purposes. There is option to disabled the execution of these non-idempotent scripts through configurations (env file). See appendix section for details. Configure the `PROVISION_DUMMY_APPLICANTS` and `PROVISION_DUMMY_APPLICATIONS` variables in `.env` before running the `docker-compose run --built` command for controlling the creation of dummy data during the FundSage Application's bootstrap process.

### 6. Testing

1. **Automated Testing**:
   - Run all tests using the provided script:
     ```bash
     bash bin/tests_all.sh
     ```
   - Test reports are available in the `logs/` directory. There will be a total of 4 sets of test reports, one each for `tests_dal.sh, tests_bl.sh, tests_utils.sh, tests_api.sh`; 
   - or alternatively, you can interactively execute/step-through the tests using the VSCode Test Explorer.

2. **Interactive Testing with VSCode**:
   - Use Python Test Explorer to run tests interactively.
   - Attach the VSCode debugger to step through code execution.

### 7. Manual API Testing

1. **Using Postman**:
   - Use PostMan, curl or equivalent tools for manual interactive testing.
   - Refer to 🛠️ [API Testing Guide - POSTMAN](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/api_testing.md) for the relevant details.

### 8. Debugging the Deployed FundSage Flask Application

1. **Enable Flask Debugging**:
   - Set `FLASK_DEBUG=1` in `.env`.
   - Restart the Docker Compose services:
     ```bash
     docker-compose down
     docker-compose up --build
     ```

2. **Configure VSCode for Debugging**:
   - Use the provided `.vscode/launch.json` configuration to attach VSCode's debugger.

### 9. Database Management

1. **Access pgAdmin4**:
   - Navigate to `http://localhost:8080` in your browser.
   - Login with credentials defined in the `.env` file (`PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD`).
   - Add a new server in pgAdmin4 with the connection details defined in the `.env` file.

## 5. Brief Overview of Option 2 (Scalable Deployment)

### Overview

- **Multi-Tier Architecture**:
  - Deploy the FundSage Flask application and PostgreSQL database in separate environments for scalability.
  - Use managed services for databases and load balancing.

### Future Steps

- Detailed network configurations.
- Scaling strategies.
- Security measures for production environments.

## 6. Additional Resources

### Future Updates

- A detailed guide for staging and production deployments will be provided in a future update.

## Appendix

### Integration of Database Initialization Scripts

1. **`init-db/create_db_ephemeral.sql`**:
   - Ensure the PostgreSQL container creates the `fund_sage_db_ephemeral` on initialization.

### Using pgAdmin4 for Database Administration

- **Adding Server in pgAdmin4**:
  1. Go to **File** -> **Add New Server**.
  2. Enter a name for the server (e.g., `FundSage DB`).
  3. Use connection details from the `.env` file:
     - **Host**: `db`
     - **Port**: `5432`
     - **Username**: `${POSTGRES_USER}`
     - **Password**: `${POSTGRES_PASSWORD}`

By following this deployment guide, you should be able to set up and run the FundSage application in a local development or testing environment using Docker Compose. For production deployments, stay tuned for a more detailed guide covering advanced topics and best practices.