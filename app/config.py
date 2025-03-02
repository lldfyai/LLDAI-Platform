import os

UPLOAD_DIR = "submission_uploads"
CLIENT_ID =  os.environ.get("COGNITO_CLIENT_ID")
CLIENT_SECRET =  os.environ.get("COGNITO_CLIENT_SECRET")
USER_POOL_ID =  os.environ.get("USER_POOL_ID")
GITHUB_CLIENT_ID =  os.environ.get("OAUTH2_CLIENT_ID")
GITHUB_CLIENT_SECRET =  os.environ.get("OAUTH2_CLIENT_SECRET")
DB_HOST =  os.environ.get("DB_HOST")
DB_NAME =  os.environ.get("DB_NAME")
DB_USER =  os.environ.get("DB_USER")
DB_PASSWORD =  os.environ.get("DB_PASSWORD")
DB_PORT =  os.environ.get("DB_PORT")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY =  os.environ.get("AWS_SECRET_ACCESS_KEY")
LANGUAGE_CONFIG = {
    "java": {"dockerfile": "Dockerfile.java", "image": "java_executor"},
    "python": {"dockerfile": "Dockerfile.python", "image": "python_executor"},
}