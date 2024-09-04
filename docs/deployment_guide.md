# Minimal Setup Guide for FundSage

## 1. Introduction

This guide provides streamlined instructions for quickly deploying the FundSage application using Docker Compose. It is designed for testers, demo purposes, or anyone who wants to deploy FundSage with minimal setup effort.

### Objective

- **Quick Deployment**: Deploy FundSage with minimal configuration to quickly test or showcase the application.
- **Audience**: Testers, project stakeholders, and demo participants with basic knowledge of Docker.

### Scope

This guide focuses exclusively on a quick and straightforward Docker Compose deployment, assuming minimal prerequisites and setup requirements.

## 2. Prerequisites

### General Requirements

- **Basic Knowledge**: Familiarity with running basic commands in a terminal.
- **Operating System**: Windows with WSL2 (Ubuntu) or native Ubuntu installation.
- **Software**: Docker and Docker Compose installed.

### Install Docker and Docker-Compose

**For Windows Users (WSL2):**

- Install Docker Desktop and enable WSL2 integration.

**For Ubuntu Users:**
    
  ```bash
  sudo apt update
  sudo apt install docker.io docker-compose
  sudo systemctl start docker
  sudo systemctl enable docker
  ```
## 3. Quick Setup Instructions
**Clone the Repository**
First, clone the FundSage repository to your local machine:
```bash
git clone https://github.com/jawkh/gt_cdt_swe_test.git <project-root-folder>
  ```

**Open the Project in VSCode (Optional)**
If you want to use Visual Studio Code for editing or viewing files, open the project folder:
  ```bash
  code <project-root-folder>
  ```
**Configure Environment Variables**
1. Rename `.env copy` to `.env`:
  ```bash
  mv .env\ copy .env
  ```
2. Edit `.env` File (Optional):
  - Most users can proceed with the default values.
  - If desired, you can change sensitive credentials or configurations for local development.

## 4. Deploy with Docker-Compose
1. Run Docker-Compose:
    Navigate to your project directory and run the following command:
    ```bash
    docker-compose up --build
    ```
2. Deployment Details:
  - Docker Compose will automatically pull the necessary Docker images and start the containers for the FundSage Flask App, PostgreSQL database, and pgAdmin4.
  - Initial data setup, including creating necessary databases and provisioning essential records, is automatically handled by startup scripts within the Docker containers.

## 5. Access the FundSage Application
Access the FundSage Application
- **FundSage API:** Once the containers are running, the FundSage API is accessible at 'http://localhost:5000/api/...' using the curl command or Postman. *Refer to 🛠️ [API Testing Guide - POSTMAN](https://github.com/jawkh/gt_cdt_swe_test/blob/main/docs/api_testing.md)
- **pgAdmin4:** For database management, open your web browser and go to:
```bash
http://localhost:8080
```
Check Database Records with pgAdmin4
- Login to pgAdmin4:
  - Go to http://localhost:8080 in your browser.
  - Use the credentials set in the .env file (PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD).
- Add a New Server:
  - Click on "Add New Server".
  - Use the connection details from your .env file:
    - Host: db
    - Port: 5432
    - Username: ${POSTGRES_USER}
    - Password: ${POSTGRES_PASSWORD}
- Explore Databases:
  - Check both fund_sage_db and fund_sage_db_ephemeral for their contents.

## Troubleshooting and Stopping the Deployment
Check Logs:
If there are issues during deployment, view the container logs:
```bash
docker-compose logs
```
Stopping the Deployment:
To stop all running containers, press Ctrl + C in the terminal where Docker Compose is running or run:
```bash
docker-compose down
```
## Summary
This guide provided a quick and minimal setup approach to deploying the FundSage application using Docker Compose. With just a few commands, you can have the application and its dependencies running locally, ideal for quick demos, testing, or initial exploration.

For more detailed instructions or advanced configuration, refer to the full Deployment Guide included in the repository.

By following this minimal setup guide, you can quickly deploy and showcase FundSage with minimal effort and setup.

