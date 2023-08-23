import boto3
import json
from datetime import datetime

s3 = boto3.client('s3', region_name='eu-west-2')
bucket_name = 'dev-lambdaapi-s3'

# Counter for the number of requests
request_count = 0

def lambda_handler(event, context):
    global request_count
    request_count += 1

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])

        num_objects = len(objects)

        if num_objects > 0:
            last_modified_object = max(objects, key=lambda obj: obj['LastModified'])
            last_modified_time = last_modified_object['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
            result = {
                "request_count": request_count,
                "num_objects": num_objects,
                "last_modified_time": last_modified_time
            }
            return {
                "statusCode": 200,
                "body": json.dumps(result)
            }
        else:
            return {
                "statusCode": 404,
                "body": "Bucket is empty."
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"An error occurred: {str(e)}"
        }
