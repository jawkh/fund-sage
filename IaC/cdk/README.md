# GT CDT SWE Test - AWS CDK Deployment

This directory contains the AWS CDK implementation for deploying the GT CDT SWE Test application to AWS.

## Prerequisites

Before you begin, ensure you have the following installed:

- [AWS CLI](https://aws.amazon.com/cli/) installed and configured with appropriate credentials
- [Docker](https://www.docker.com/get-started) installed
- [nvm (Node Version Manager)](https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-and-updating) installed

## Node.js Setup

This project requires Node.js version 18. Follow these steps to set up the correct Node.js version:

1. Open a terminal and navigate to the project directory.

2. Install Node.js version 18 using nvm:
   ```
   nvm install 18
   ```

3. Set Node.js version 18 as the active version for this project:
   ```
   nvm use 18
   ```

4. Verify that you're using the correct Node.js version:
   ```
   node --version
   ```
   You should see output indicating version 18.x.x.

5. Install the AWS CDK CLI globally:
   ```
   npm install -g aws-cdk
   ```


## Setting Up AWS IAM Programmatic User Account for IaC

### Steps to Create an IAM Programmatic User for CDK:

1. **Log in to AWS Management Console**:
- Go to [AWS Management Console](https://aws.amazon.com/console/) and log in with your administrator credentials.

2. **Create an IAM User**:
- In the search bar, type **IAM** and select **IAM** from the services menu.
- On the IAM dashboard, select **Users** from the left navigation panel.
- Click **Add User**.

3. **Configure User Details**:
- Enter a **User name** (e.g., `cdk-deploy-user`).
- Uncheck **Provide user access to the AWS Management Console - optional**
- Click **Next: Permissions**.

4. **Set Permissions**:
- On the "Set permissions" page, choose **Attach policies directly**.
- Select the **AdministratorAccess** managed policy. This will grant the user full access to manage AWS resources required for CDK.

5. **Add Tags (Optional)**:
- Add any tags if needed (e.g., `Purpose: CDKDeployment`).

6. **Review and Create User**:
- Review your user configuration and permissions.
- Click **Create User**.

7. **Download the Credentials**:
- Navigate to the newly created user account. 
- Click **Create access key**
- Select **Command Line Interface (CLI)**
- Copy the **Access Key** and **Secret access key**
- Once the user is created, you'll be shown the **Access Key ID** and **Secret Access Key**. **Download** or **copy** these credentials, as this is the only time you can see them.

Create a .env file in the IaC/cdk directory using the .env copy file as a reference:

```.env
# Fill in the credentials of the Programmatic User
AWS_ACCESS_KEY_ID="<YOUR_ACCESS_KEY_ID>"
AWS_SECRET_ACCESS_KEY="<YOUR_SECRET_ACCESS_KEY>"
AWS_DEFAULT_REGION="<YOUR_REGION>"
```

## IaC Configurations

The deployment can be customized by modifying the `config.ts` file. This file contains settings for:

- VPC CIDR range and configuration
- Aurora Serverless v2 capacity units and auto-pause settings
- API Gateway rate limiting and throttling settings
- ECS Fargate task CPU, memory, and desired count
- Application environment variables
### Environment Variables

The following environment variables are set in the ECS task definition:

- FLASK_APP
- FLASK_RUN_HOST
- FLASK_RUN_PORT
- FLASK_ENV
- SECRET_KEY
- JWT_SECRET_KEY
- JWT_ACCESS_TOKEN_EXPIRES
- SERVER_NAME
- APPLICATION_ROOT
- PREFERRED_URL_SCHEME
- MAX_PASSWORD_RETRIES
- PASSWORD_RETRIES_TIME_WINDOW_MINUTES
- FLASK_DEBUG
- PROVISION_DUMMY_APPLICATIONS
- PROVISION_DUMMY_APPLICANTS

You can customize these values in the `config.ts` file under the `app` section.
Adjust these values as needed before deployment.

## Deployment Steps

1. Ensure you're in the `IaC/cdk` directory:
   ```
   cd IaC/cdk
   ```

2. Install project dependencies:
   ```
   npm install
   ```

3. Build and push the Docker image to ECR:
   ```
   chmod +x build-and-push-image.sh
   ./build-and-push-image.sh
   ```

4. Deploy the CDK stack:
   ```
   ./cdk.sh deploy
   ```

   Note: You may run the following script to destroy all the resources provisioned by the CDK (WARNING - proceed with caution as you will lose the data in the AuroraDB)
   ```
   ./cdk.sh destroy
   ```

5. After the deployment is complete, the CDK will output the API Gateway URL and other important information. Make note of these outputs for future use.

## Stack Overview

The CDK stack (`GtCdtSweStack`) creates the following resources:

- VPC with public and private subnets
- Aurora Serverless v2 database
- ECS Fargate cluster and service with auto-scaling
- ECR repository for the Docker image
- Application Load Balancer
- API Gateway with rate limiting and API key authorization
- Systems Manager Parameter Store for secrets management
- CloudWatch logs and alarms
## Secrets Management

The CDK stack automatically creates a Parameter Store entry for the database password:

- Parameter name: `/gt-cdt-swe/db-password`
- Description: Database password for GT CDT SWE application

This parameter is securely passed to the ECS task as an environment variable.

The database connection URL is stored in AWS Secrets Manager and is also securely passed to the ECS task.

To add or modify Parameter Store entries, you can use the AWS Management Console or the AWS CLI:

```
aws ssm put-parameter --name "/gt-cdt-swe/your-parameter-name" --value "your-value" --type SecureString
```

Remember to update the CDK stack if you add new parameters that need to be passed to the ECS task.

## Cleaning Up

To remove all resources created by the CDK stack, run:

```
cdk destroy
```

Note: This will delete all resources, including the database. Make sure to backup any important data before destroying the stack.

## Troubleshooting

- If you encounter issues with Node.js versions, make sure you've followed the Node.js setup instructions in this README.
- If you encounter issues with the ECS service not starting, check the CloudWatch logs for the ECS service and task.
- Ensure that the Docker image is successfully built and pushed to ECR before deploying the CDK stack.
- Verify that the AWS CLI is properly configured with the correct credentials and region.
- If you need to modify environment variables or secrets, update the `config.ts` file and redeploy the stack.

For more information on AWS CDK, refer to the [official documentation](https://docs.aws.amazon.com/cdk/latest/guide/home.html).