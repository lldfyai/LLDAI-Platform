import os
import boto3
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
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
UPLOAD_DIR = "submission_uploads"
LANGUAGE_CONFIG = {
    "java": {"dockerfile": "Dockerfile.java", "image": "java_executor"},
    "python": {"dockerfile": "Dockerfile.python", "image": "python_executor"},
}
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
GITHUB_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
USER_POOL_ID = os.getenv("USER_POOL_ID")
CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
DB_PORT = "5432"
SQLALCHEMY_DB_HOST = os.getenv("SQLALCHEMY_DB_HOST")

Modify code and update os.getenv to secret = get_secret_value_response['SecretString']