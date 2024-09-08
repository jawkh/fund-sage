
# AWS Serverless Architecture Masterplan

## 1. Overview and Objectives

This masterplan outlines the serverless architecture for migrating an existing Flask application with PostgreSQL to AWS serverless technologies. The primary objectives are:

- Migrate the existing Flask application to AWS ECS Fargate
- Replace PostgreSQL with Amazon Aurora Serverless v2
- Expose API endpoints through AWS API Gateway
- Implement security measures including API key authorization and rate limiting
- Use AWS CDK for Infrastructure as Code (IaC) deployment
- Adhere to AWS Well-Architected Framework principles

## 2. Architecture Components
- Refer to `Dockerfile` and `docker-compose.yml` for the deployment mechanism for a simple local deployment option.   

### 2.1 Compute: AWS ECS Fargate

- Deploy Flask application as a container in ECS Fargate
- Configure container to wait for Aurora Serverless using `wait-for-it.sh` script. Enhance this if necessary to "wake up" Aurora Serverless just in case it went dormant.
- Execute idempotent database initialization scripts during container bootstrap


### 2.2 Database: Amazon Aurora Serverless v2 (PostgreSQL-compatible)

- Replace existing PostgreSQL with Aurora Serverless v2
- Configure minimum and maximum Aurora Capacity Units (ACUs)

### 2.3 API Management: AWS API Gateway

- Create a Regional REST API
- Configure API key authorization
- Implement rate limiting and throttling
- Deploy API to a 'Test' stage

### 2.4 Networking: Amazon VPC

- Create a new VPC in ap-southeast-1 region
- Configure CIDR range as per requirements
- Implement necessary subnets, route tables, and security groups

### 2.5 Monitoring and Logging: AWS CloudWatch

- Configure logging for ECS Fargate, API Gateway, and Aurora Serverless
- Set up basic monitoring and alarms

### 2.6 Secret Management: AWS Systems Manager Parameter Store

- Store environment variables and secrets
- Implement secure access from ECS Fargate

## 3. Security Considerations

- API Key authorization for API Gateway
- JWT authentication handled by Flask application
- VPC security groups for ECS Fargate and Aurora Serverless
- Encryption at rest for Aurora Serverless and Parameter Store
- Encryption in transit using HTTPS

## 4. Deployment Strategy

- Use AWS CDK for Infrastructure as Code (IaC)
- Deploy all resources to ap-southeast-1 region
- Implement a single-stack approach for simplicity

## 5. API Endpoints

As defined in `docs/openapi.yaml`.

## 6. Configuration Details

### 6.1 API Gateway

- Throttling: Default limit of 1000 requests per second
- Rate limiting: Default limit of 100 requests per minute per API key
- No caching initially

### 6.2 Aurora Serverless v2

- Minimum ACU: 0.5 (configurable)
- Maximum ACU: 1 (configurable)
- Auto Pause: Enabled after 5 minutes of inactivity (configurable)

### 6.3 ECS Fargate

- CPU: 0.25 vCPU
- Memory: 0.5 GB
- Desired count: 1

## 7. Implementation Plan

1. Set up AWS CDK development environment
2. Develop CDK stack for VPC and networking components
3. Implement Aurora Serverless v2 resource in CDK
4. Create ECS Fargate service and task definition
5. Develop API Gateway configuration in CDK
6. Implement Systems Manager Parameter Store for secrets
7. Configure CloudWatch logging and basic monitoring
8. Test deployment and verify all components

## 8. Future Considerations

- Implement CI/CD pipeline for automated deployments
- Enhance monitoring and set up advanced CloudWatch alarms
- Explore potential migration to AWS Lambda if database initialization can be handled differently
- Implement caching in API Gateway if needed for performance
- Consider multi-region deployment for high availability

## 9. Conclusion

This serverless architecture leverages AWS services to create a scalable, maintainable, and cost-effective solution. By using ECS Fargate, Aurora Serverless, and API Gateway, we maintain the functionality of the original application while gaining the benefits of serverless technologies.