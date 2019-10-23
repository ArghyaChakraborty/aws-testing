"""
This script uploads a file in a given AWS S3 bucket. It deletes the file if it already exists & then upload the file & makes it public
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
s3_client = boto3.client('s3')


try :
    file_object = s3_client.get_object(Bucket = "arghya1988.work.testbucket1", Key='download.jfif')
    if file_object :
        print("Object aleady exists : "+str(file_object))
        print("Deleting Object ...")
        s3_client.delete_object(Bucket = "arghya1988.work.testbucket1", Key='download.jfif')
except Exception as ex :
    print("Object does not exist "+str(ex))


# Upload a new file
print("Uploading : "+script_path+'/download.jfif to arghya1988.work.testbucket1')
data = open(script_path+'/download.jfif', 'rb')
response = s3.Bucket('arghya1988.work.testbucket1').put_object(ACL='public-read', Key='download.jfif', Body=data)