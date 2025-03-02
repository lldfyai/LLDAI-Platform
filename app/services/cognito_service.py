import hmac
import hashlib
import base64
import boto3

from app.config import CLIENT_ID, CLIENT_SECRET, USER_POOL_ID, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

cognito = boto3.client("cognito-idp", region_name="us-west-2",
                       aws_access_key_id= AWS_ACCESS_KEY_ID,
                       aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
def get_secret_hash_using_client_id(username, client_id):
    """Generate SECRET_HASH for Cognito authentication."""
    message = username + client_id
    dig = hmac.new(CLIENT_SECRET.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()
def get_secret_hash(username: str) -> str:
    """Compute Cognito secret hash for authentication."""
    msg = username + CLIENT_ID
    dig = hmac.new(CLIENT_SECRET.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()
def get_login_token(email: str, username: str, password: str) -> str:
    try:
        auth_params = {
            "USERNAME": username if username else email,
            "PASSWORD": password,
            "SECRET_HASH": get_secret_hash_using_client_id(username, CLIENT_ID)
        }
        auth_response = cognito.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters=auth_params
        )
        return auth_response["AuthenticationResult"]["IdToken"]
    except cognito.exceptions.NotAuthorizedException as e:
        print("Cognito NotAuthorizedException:", str(e))
        raise Exception("Invalid credentials")
def register_cognito_user(username: str, email: str, password: str):
    """Register a new user with Cognito."""
    try:
        cognito.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=username,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "email_verified", "Value": "true"},
            ],
            TemporaryPassword=password,  # Temporary password
            MessageAction="SUPPRESS",  # Suppress default email message
        )
        # Set permanent password
        cognito.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=username,
            Password=password,
            Permanent=True
        )
        # Confirm user sign up
        # Try to confirm the user signup
        try:
            cognito.admin_confirm_sign_up(
                UserPoolId=USER_POOL_ID,
                Username=username
            )
        except cognito.exceptions.NotAuthorizedException as e:
            # If the user is already confirmed, ignore this error.
            if "User cannot be confirmed. Current status is CONFIRMED" in str(e):
                pass
            else:
                raise
    except cognito.exceptions.UsernameExistsException:
        raise Exception("Username already exists")

def forgot_password(email: str):
    try:
        return cognito.forgot_password(
            ClientId=CLIENT_ID,
            Username=email,
            SecretHash=get_secret_hash(email)
        )
    except cognito.exceptions.UserNotFoundException:
        return "User not found."

def reset_password(email, confirmation_code, new_password):
    try:
        return cognito.confirm_forgot_password(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=confirmation_code,
            Password=new_password,
            SecretHash=get_secret_hash(email)  # ✅ Include SECRET_HASH
        )
    except cognito.exceptions.CodeMismatchException:
        raise Exception("Invalid confirmation code.")
    except cognito.exceptions.ExpiredCodeException:
        raise Exception("Confirmation code expired.")
    except Exception as e:
        raise Exception(str(e))
