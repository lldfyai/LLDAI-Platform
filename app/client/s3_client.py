import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

    
s3_client = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-west-2")

def upload_file(file_path, bucket, object_path=None):
    """Upload a file to an S3 bucket."""
    if object_path is None:
        object_path = file_path
    s3_client.upload_file(file_path, bucket, object_path)

def download_file(bucket, object_path, file_name):
    """Download a file from an S3 bucket."""
    s3_client.download_file(bucket, object_path, file_name)

def read_file(bucket, object_path):
    """Read a file from an S3 bucket."""
    obj = s3_client.get_object(Bucket=bucket, Key=object_path)
    return obj['Body'].read().decode('utf-8') 

def delete_file(bucket, object_path):
    """Delete a file from an S3 bucket."""  
    s3_client.delete_object(Bucket=bucket, Key=object_path)         

def generate_presigned_url(bucket, object_path, expiration=3600):
    """Generate a presigned URL to share an S3 object."""
    return s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': object_path}, ExpiresIn=expiration)

def list_objects(bucket, prefix=None):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        else:
            print(f"No objects found in bucket '{bucket}' with prefix '{prefix}'.")
            return []
    except Exception as e:
        print(f"Error listing objects in bucket '{bucket}': {e}")
        return []