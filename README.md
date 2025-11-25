# aws_to_biquery_project

https://github.com/pythonbaker/aws_to_biquery_project.git

Created with git init(pythonbaker account)

To check which git account :
git remote -v (origin  https://github.com/pythonbaker/aws_to_biquery_project.git (fetch)
origin  https://github.com/pythonbaker/aws_to_biquery_project.git (push))

Create a project to transfer data from AWS to BigQuery using Python.

## Overview
This project will extract the zip files from AWS S3, process the data, and load it into Google BigQuery.

## Prerequisites
- Python 3.x
- AWS account with access to S3
- Google Cloud account with access to BigQuery
- Required Python libraries: `boto3`, `google-cloud-bigquery`

Links
-- https://console.cloud.google.com/bigquery?hl=en&project=healthcare-data-project-462311&inv=1&invt=Ab1AwQ&ws=!1m0



## setup
Create the repository
convert to poetry project:
``` poetry init --no-interaction --name aws-bq-project --desc
ription "AWS to BigQuery data transfer project" --python "^3.11"```

test file:
``` zip -r /Users/sonali.cornelio/Downloads/aws-bq-test.zip /Users/sonali.cornelio/Downloads/aws-bq-test```

upload the zip file to S3 bucket via AWS console.
-- s3://source-bucket-80469/aws-bq-test.zip
-- https://source-bucket-80469.s3.ap-southeast-2.amazonaws.com/aws-bq-test.zip

## GCP Credentials
1. Create a service account in GCP with BigQuery permissions(using the already created one).
2. Download the JSON key file and save it as `gcp-key.json` in the project root.
3. Add `gcp-key.json` to `.gitignore` to avoid committing sensitive information.
4. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to point to the `gcp-key.json` file.
5. Alternatively, set the environment variable in your CI/CD pipeline settings.

## AWS Credentials
Set up AWS credentials environment variables and save them in your local `.env` file or CI/CD pipeline settings.


bucket with zip files: source-bucket-80469
download and extract the zip files from S3 using boto3.
unzip the files using zipfile module.
load the extracted data into BigQuery using google-cloud-bigquery library.