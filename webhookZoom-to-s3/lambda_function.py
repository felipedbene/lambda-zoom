import json
import os
import requests
import logging
import boto3
import uuid
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    #print(event)
    evento = json.loads(event["body"])
    
    #Zoom meta data from the webhook
    download_token = evento["download_token"]
    account_id = evento["payload"]["account_id"]
    host_id = evento["payload"]["object"]["host_id"]
    topic = evento["payload"]["object"]["topic"].replace(" ","")
    base = "{}/{}/{}/".format(account_id,host_id,topic)
    
    if "bucket" in os.environ :
        s3bucket = os.getenv("bucket")
    else :
        s3bucket = "notasdofelip"
    
    for media in evento["payload"]["object"]["recording_files"] :
        print(media["file_type"])
        meeting_id = media["meeting_id"]
        
        tmp = str(uuid.uuid4())
        
        name = base + meeting_id + "." + media["file_type"]
        
        print("Token : "+ download_token)
        print("Url:" + media["download_url"] )
        response = requests.get(media["download_url"] + "?access_token=" + download_token )
        with open("/tmp/"+tmp, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        print("wrote file {}".format(name))
        fd.close()
        if upload_file("/tmp/"+tmp, s3bucket,name) :
            print("Uploaded file {} to {}".format(name,s3bucket))
        else :
            print("error uploading file to s")
    
    return {
        'statusCode': 200,
        'body': json.dumps('{} uploaded to bucket {}'.format(name,s3bucket))
    }

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print("uploaded file: "+ file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True