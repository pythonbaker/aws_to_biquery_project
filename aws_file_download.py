import boto3
import os
import re
import json
from pathlib import Path
from zipfile import ZipFile
from pprint import pprint
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv


load_dotenv()

AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")


def test_connection():
    try:
        sts = boto3.client("sts")
        print(sts.get_caller_identity())
    except ClientError as e:
        print(f"❌ AWS connection failed: {e}")


# check if the connection is successfull with aws

# test_connection()

# list the bucket in the account


def bucket_details():
    try:
        s3 = boto3.client("s3")
        print(s3)
        response = s3.list_buckets_v2()
        # pprint(response) #pprint is used to format AWS responses for better readability.
        # print(f"This is to get first bucket name {response['Buckets'][0]['Name']}")
        for bucket in response["Buckets"]:
            print(bucket["Name"])
    except Exception as e:
        print(f"error found : {e}")


# bucket_details()
BUCKET = "source-bucket-80469"
local_path = None

# list the files in the bucket and download the zip file only
def list_objects():
    client = boto3.client("s3")
    response = client.list_objects_v2(Bucket="source-bucket-80469")
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)
    if "Contents" in response:
        for file in response["Contents"]:
            # print(file['Key'])
            filename = file["Key"]
            # print(filename)
            if filename.endswith(".zip"):
                # print(f"this is filename {filename}")
                local_path = os.path.join(download_dir, filename)
                print(local_path)
                try:
                    client.download_file(
                        BUCKET, filename, local_path
                    )
                    print(f"file {filename} has been downloaded to {local_path}")
                except Exception as e:
                    print(f"Error downloading file: {e}")

    else:
        print("no files found")
    return local_path

    # pprint(response)



# Unzip the contents of the zip file and create the dataset in bigquery , move the data into bigquery.
def unzip_file(local_path):
    if not local_path:
        raise ValueError("No file path provided")

    zip_path = Path(local_path)
    print(zip_path)

    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file not found: {local_path}")

    extract_dir = 'extracted_files'
    extract_path = Path(extract_dir).resolve()
    # print(f"this is to check path {extract_path}")
    os.makedirs(extract_path, exist_ok=True)

    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        print(f"The files are extracted to {extract_path} ")
        files = zip_ref.namelist()
        print(files)

    # load gnaf.json file which has additional details of what type of files and schema needs to be used
    #  open json file and load into this script to access the data

    with open('gnaf.json', 'r') as f:
        gnaf= json.load(f)
        # print(gnaf['dataset']['layers'][0]['layer_name'])

    # loop through the extracted files and get the name and match with the gnaf,json to create tables
    layer_files = []
    try:
        pattern = gnaf['dataset']['layers'][0]['mask']
        for file in files:
            if re.fullmatch(pattern, file):
                table_id = file
                schema = gnaf['dataset']['layers'][0]['schema']
                bq_table(table_id, schema)
                layer_files.append(file)

    except Exception as e:
        print(f"error {e}")
    print(layer_files)



local_path= list_objects()
unzip_file(local_path)





# list_objects()

# read_file(filename):
#     with open(filename) as f:
#         print(f.readline())


# read_file("text.txt")