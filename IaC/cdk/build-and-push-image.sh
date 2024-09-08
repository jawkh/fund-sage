#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Source the assume_role.sh script to set up AWS credentials
source ./assume_role.sh

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker could not be found. Please install it and try again."
    exit 1
fi

# Set variables
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION="ap-southeast-1"
ECR_REPOSITORY_NAME="gt-cdt-swe-app"
IMAGE_TAG="fundsage-latest"

# Function to check if the ECR repository exists
check_or_create_ecr_repository() {
    echo "Checking if the ECR repository $ECR_REPOSITORY_NAME exists..."
    
    # Check if repository exists
    REPO_EXISTS=$(aws ecr describe-repositories --repository-names "$ECR_REPOSITORY_NAME" --region "$AWS_REGION" 2>/dev/null || echo "not_found")

    if [ "$REPO_EXISTS" = "not_found" ]; then
        echo "ECR repository $ECR_REPOSITORY_NAME does not exist. Creating it..."
        aws ecr create-repository --repository-name "$ECR_REPOSITORY_NAME" --region "$AWS_REGION"
        echo "ECR repository $ECR_REPOSITORY_NAME created."
    else
        echo "ECR repository $ECR_REPOSITORY_NAME already exists."
    fi
}

# Check and create the ECR repository if necessary
check_or_create_ecr_repository

# Log in to Amazon ECR
echo "Logging in to Amazon ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build the Docker image
echo "Building Docker image..."
cd ../..
docker build . -t $ECR_REPOSITORY_NAME:$IMAGE_TAG

# Tag the image for ECR
docker tag $ECR_REPOSITORY_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:$IMAGE_TAG

# Push the image to ECR
echo "Pushing image to ECR..."
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:$IMAGE_TAG

echo "Image successfully built and pushed to ECR"
