#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if the user provided a valid argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <deploy|destroy>"
    exit 1
fi

# Check if the provided argument is either "deploy" or "destroy"
ACTION=$1
if [ "$ACTION" != "deploy" ] && [ "$ACTION" != "destroy" ]; then
    echo "Invalid argument. Please provide 'deploy' or 'destroy'."
    exit 1
fi

# Source the assume_role.sh script to set up AWS credentials
source ./assume_role.sh

# Set variables
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION="ap-southeast-1"

# Export AWS environment variables for CDK
export AWS_ACCOUNT_ID
export AWS_REGION

echo "AWS Account ID: $AWS_ACCOUNT_ID"
echo "AWS Region: $AWS_REGION"

# Check if CDK bootstrapping is required
BOOTSTRAP_VERSION=$(aws ssm get-parameter \
    --name /cdk-bootstrap/hnb659fds/version \
    --region $AWS_REGION \
    --query "Parameter.Value" \
    --output text 2>/dev/null || echo "not_bootstrapped")

if [ "$BOOTSTRAP_VERSION" = "not_bootstrapped" ]; then
    echo "CDK environment not bootstrapped. Bootstrapping now..."
    cdk bootstrap aws://$AWS_ACCOUNT_ID/$AWS_REGION
else
    echo "CDK environment already bootstrapped (version $BOOTSTRAP_VERSION)."
fi

# Perform the requested CDK action (deploy or destroy)
if [ "$ACTION" = "deploy" ]; then
    echo "Deploying the CDK stack..."
    cdk deploy
elif [ "$ACTION" = "destroy" ]; then
    echo "Destroying the CDK stack..."
    cdk destroy
fi
