import json
import base64
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """Processes Kafka events.

    Args:
        event: A dictionary containing Kafka event records.
        context: A context object for Lambda function execution.

    Returns:
        None
    """
    
    # Initialize boto3 client for S3
    s3 = boto3.client('s3')
    
    # S3 bucket name
    bucket_name = '<bucket_name>'
    
    # Folder name
    folder_name = 'incremental_data'
    
    current_datetime = datetime.now()

    for key in event['records']:
        print(f"Key: {key}")
        for record in event['records'][key]:
            print(f"Record: {record}")
            msg = base64.b64decode(record['value']).decode('utf-8')  # Decode base64 and decode as UTF-8
            print(f"Message: {msg}")
            
            try:
                # Define the file name to upload to S3
                file_name = f"seattle_911_incident_{current_datetime}_{record['offset']}.json"
                
                # Construct S3 key with folder prefix
                s3_key = f"{folder_name}/{file_name}"
                
                # Upload the message as a file to S3 bucket
                s3.put_object(Body=msg.encode('utf-8'), Bucket=bucket_name, Key=s3_key)
                
                print(f"Message uploaded to S3: {s3_key}")
                
            except Exception as e:
                print(f"Error uploading message to S3: {str(e)}")
