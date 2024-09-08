#!/bin/bash

# Function to install jq if not already installed
install_jq() {
    if ! command -v jq &> /dev/null
    then
        echo "'jq' not found, installing..."
        sudo apt update
        sudo apt install jq -y
    else
        echo "'jq' is already installed."
    fi
}

# Function to install AWS CLI if not already installed
install_aws_cli() {
    if ! command -v aws &> /dev/null
    then
        echo "'aws' CLI not found, installing..."
        sudo apt update
        sudo apt install awscli -y
    else
        echo "'aws' CLI is already installed."
    fi
}

# Install pre-requisites
install_jq
install_aws_cli

# Load the .env file if it exists
if [ -f ".env" ]; then
    # Export environment variables from the .env file
    export $(grep -v '^#' .env | xargs)
    echo "Environment variables loaded from .env"
else
    echo ".env file not found. Please create a .env file with your AWS credentials."
    exit 1
fi

# Assume the role using AWS CLI and extract the credentials
ASSUME_ROLE_OUTPUT=$(aws sts assume-role \
    --role-arn "$ROLE_ARN" \
    --role-session-name "$SESSION_NAME" \
    --external-id "$EXTERNAL_ID" \
    --query "Credentials" \
    --output json)

# Check if the assume-role command was successful
if [ $? -ne 0 ]; then
    echo "Failed to assume the role. Please check your configuration."
    exit 1
fi

# Extract credentials from the assume-role output
AWS_ACCESS_KEY_ID=$(echo $ASSUME_ROLE_OUTPUT | jq -r '.AccessKeyId')
AWS_SECRET_ACCESS_KEY=$(echo $ASSUME_ROLE_OUTPUT | jq -r '.SecretAccessKey')
AWS_SESSION_TOKEN=$(echo $ASSUME_ROLE_OUTPUT | jq -r '.SessionToken')

# Export the temporary credentials to the current shell session
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_SESSION_TOKEN

# Set default profile to use the assumed role credentials
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID" --profile temp-role
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY" --profile temp-role
aws configure set aws_session_token "$AWS_SESSION_TOKEN" --profile temp-role

# Set AWS CLI to use the temporary profile
export AWS_PROFILE=temp-role

echo "Role assumed successfully and temporary credentials set for this session."

# Verify the assumed role by getting the caller identity
aws sts get-caller-identity
