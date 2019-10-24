"""
This script uploads a file in a given AWS S3 bucket. It creates the bucket if it doesn't exist. It deletes the file if it already exists & then upload the file & makes it public
Prerequisits : 
- For this script to work, [Block all public access] should be off in the given S3 bucket
- Also, an IAM user must be created in AWS console & the region, access key details should be available in users home directory
    Ex. cat <home directory of the user who is executing the script>/.aws/credentials
    [default]
    region = us-east-2
    aws_access_key_id = <aws_access_key_id of IAM user>
    aws_secret_access_key = <aws_secret_access_key of IAM user>
- Moreover, boto3 python module should be installed
API : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#s3
"""

import boto3
import os


script_path = os.path.dirname(os.path.abspath(__file__))

# Let's use Amazon S3
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

bucket_name = "arghya1988.work.testbucket"
key_name = "download.jfif"

# Check and create a bucket
if s3.Bucket(bucket_name) not in s3.buckets.all() :
    try :
        print("Bucket does not exist ")
        print("Creating bucket "+bucket_name)
        response = s3.Bucket(bucket_name).create(ACL='public-read-write', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
        print(str(response))
    except Exception as ex :
        print("Exeption in creating bucket "+str(ex))
else :
    print("Bucket already exists")

# Check and upload a file
try :
    file_object = s3_client.get_object(Bucket = bucket_name, Key=key_name)
    if file_object :
        print("Object aleady exists : "+str(file_object))
        print("Deleting Object ...")
        s3_client.delete_object(Bucket = bucket_name, Key=key_name)
except Exception as ex :
    print("Object does not exist "+str(ex))


# Upload a new file
print("Uploading : "+script_path+'/'+key_name+' to '+bucket_name)
data = open(script_path+'/'+key_name, 'rb')
response = s3.Bucket(bucket_name).put_object(ACL='public-read', Key=key_name, Body=data)