import os
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

CV_CONTAINER_S3 = "applicant-cv-container"
S3_BUCKET_REGION = "ap-south-1"

s3 = boto3.client("s3")

# check the bucket availability, if it not available create new bucket
def s3_bucket_availability():

    bucket_availability = False

    # check availability of bucket
    try :
        availble_buckets = s3.list_buckets()
        
        for bucket in availble_buckets['Buckets']:
            if bucket['Name'] == CV_CONTAINER_S3:
                bucket_availability = True
                break
                
    except:
        print("Something went wrong in data fetching from amazon...")
    

    # create new bucket if there bucket didnt exists
    try:
        if not bucket_availability:
            s3.create_bucket(
                Bucket=CV_CONTAINER_S3,
                CreateBucketConfiguration={'LocationConstraint': S3_BUCKET_REGION}
            )
    except ClientError as e:
        print("Something went wrong in bucket creation process... " , e)



# change file name and store in s3 bucket
def store_cv_in_s3(cv_file_path, file_name):
    
    # check availability of bucket
    s3_bucket_availability()

    # upload cv into s3
    try:
        s3.upload_file(cv_file_path, CV_CONTAINER_S3, file_name)
    except ClientError as e:
        print(f"Something went wrong in cv uploading process... : {e}")
    