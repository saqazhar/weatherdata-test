#!/bin/bash

# Define variables
AWS_REGION="us-east-1"
S3_BUCKET_NAME="your-lambda-code-bucket"
GLUE_SCRIPT_PATH="glue-scripts"
LAMBDA_CODE_PATH="sample-api-lambda-code"
CLOUDFORMATION_TEMPLATE_PATH="sample-template.yml"
DB_USERNAME="admin"
DB_PASSWORD="yourpassword"
DB_NAME="weatherdb"
RAW_DATA_PATH="..//wx_data/"
TABLE_SCHEMA="CREATE TABLE weather_data (id INT AUTO_INCREMENT PRIMARY KEY, date DATE, temperature FLOAT, humidity FLOAT, weather VARCHAR(255));"

# Check AWS CLI access
if ! aws sts get-caller-identity --region $AWS_REGION > /dev/null 2>&1; then
  echo "AWS CLI access is not configured. Please configure it using 'aws configure'."
  exit 1
fi

# Upload Glue script to S3
echo "Uploading Glue script to S3..."
aws s3 cp $GLUE_SCRIPT_PATH s3://$S3_BUCKET_NAME/ --region $AWS_REGION

# Upload Lambda code to S3
echo "Uploading Lambda code to S3..."
aws s3 cp $LAMBDA_CODE_PATH s3://$S3_BUCKET_NAME/ --region $AWS_REGION

# Deploy CloudFormation template
echo "Deploying CloudFormation template..."
STACK_NAME="weather-stack"
aws cloudformation deploy --template-file $CLOUDFORMATION_TEMPLATE_PATH --stack-name $STACK_NAME --capabilities CAPABILITY_NAMED_IAM --region $AWS_REGION

# Get RDS endpoint
echo "Fetching RDS endpoint..."
RDS_ENDPOINT=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $AWS_REGION --query "Stacks[0].Outputs[?OutputKey=='RDSInstanceEndpoint'].OutputValue" --output text)

# Wait for RDS instance to be available
echo "Waiting for RDS instance to be available..."
aws rds wait db-instance-available --db-instance-identifier weather-rds-db --region $AWS_REGION

# Create table in RDS
echo "Creating table in RDS..."
mysql -h $RDS_ENDPOINT -u $DB_USERNAME -p$DB_PASSWORD -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
mysql -h $RDS_ENDPOINT -u $DB_USERNAME -p$DB_PASSWORD -D $DB_NAME -e "$TABLE_SCHEMA"

# Copy files to S3 raw data bucket
echo "Copying raw data files to S3 bucket..."
aws s3 cp $RAW_DATA_PATH s3://raw-data-files-bucket/ --recursive --region $AWS_REGION

# Fetch API endpoint
echo "Fetching API endpoint..."
API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $AWS_REGION --query "Stacks[0].Outputs[?OutputKey=='APIGatewayURL'].OutputValue" --output text)

echo "Deployment complete. API endpoint: $API_ENDPOINT"
