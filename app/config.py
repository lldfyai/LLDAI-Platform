import os

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
USER_POOL_ID = os.getenv("USER_POOL_ID")
CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
DB_PORT = "5432"
SQLALCHEMY_DB_HOST = os.getenv("SQLALCHEMY_DB_HOST")
