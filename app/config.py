import os
import boto3
import json
from botocore.exceptions import ClientError


def get_secret():
    secret_name = "lldfySecrets"
    region_name = "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret_string = get_secret_value_response['SecretString']
    return json.loads(secret_string)

# Retrieve the secret once and parse it into a dictionary
secret = get_secret()

UPLOAD_DIR = "submission_uploads"
LANGUAGE_CONFIG = {
    "java": {"dockerfile": "Dockerfile.java", "image": "java_executor"},
    "python": {"dockerfile": "Dockerfile.python", "image": "python_executor"},
}

# Replace os.getenv with values from the secret
AWS_ACCOUNT_ID = secret["AWS_ACCOUNT_ID"]
AWS_ACCESS_KEY_ID = secret["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = secret["AWS_SECRET_ACCESS_KEY"]
GITHUB_CLIENT_SECRET = secret["OAUTH2_CLIENT_SECRET"]
GITHUB_CLIENT_ID = secret["OAUTH2_CLIENT_ID"]
DB_PASSWORD = secret["DB_PASSWORD"]
DB_USER = secret["DB_USER"]
DB_NAME = secret["DB_NAME"]
DB_HOST = secret["DB_HOST"]
USER_POOL_ID = secret["USER_POOL_ID"]
CLIENT_ID = secret["COGNITO_CLIENT_ID"]
CLIENT_SECRET = secret["COGNITO_CLIENT_SECRET"]
DB_PORT = "5432"  # Hardcoded, adjust if needed
SQLALCHEMY_DB_HOST = secret["SQLALCHEMY_DB_HOST"]