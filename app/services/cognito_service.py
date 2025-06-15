import hmac
import hashlib
import base64
import boto3
import requests
import jwt
from jwt import PyJWKClient
from fastapi import HTTPException
from config import COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET, USER_POOL_ID, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
COGNITO_REGION= "us-west-2"
# Initialize the Cognito client
cognito = boto3.client("cognito-idp", region_name=COGNITO_REGION,
                       aws_access_key_id= AWS_ACCESS_KEY_ID,
                       aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
COGNITO_KEYS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"

def verify_auth_token(auth_token: str) -> dict:
    """
    Verify a Cognito JWT token using the JWKS via PyJWKClient.
    Returns the decoded token on success.
    Raises HTTPException with specific error details for invalid tokens.
    """
    # Basic structure check
    if auth_token.count(".") != 2:
        raise HTTPException(status_code=401, detail="Invalid token format")

    try:
        # Get unverified headers to extract the key id (kid)
        headers = jwt.get_unverified_header(auth_token)
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token header")

    kid = headers.get("kid")
    if not kid:
        raise HTTPException(status_code=401, detail="Missing key identifier (kid) in token header")

    # Use PyJWKClient to fetch the signing key from Cognito
    try:
        jwk_client = PyJWKClient(COGNITO_KEYS_URL)
        signing_key = jwk_client.get_signing_key_from_jwt(auth_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error fetching signing key: {str(e)}")

    # Validate issuer
    issuer = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"
    try:
        decoded_token = jwt.decode(
            auth_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=COGNITO_CLIENT_ID,  # Should match your app client ID
            issuer=issuer,
            options={"require_exp": True, "require_iat": True}
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidAudienceError:
        raise HTTPException(status_code=401, detail="Invalid audience claim")
    except jwt.InvalidIssuerError:
        raise HTTPException(status_code=401, detail="Invalid issuer claim")
    except jwt.InvalidAlgorithmError:
        raise HTTPException(status_code=401, detail="Invalid algorithm used")
    except jwt.DecodeError as e:
        raise HTTPException(status_code=401, detail=f"Token decoding failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token validation error: {str(e)}")

    # Additional Cognito-specific validations
    if decoded_token.get("token_use") != "id":
        raise HTTPException(status_code=401, detail="Invalid token use. Expected ID token")
    if not decoded_token.get("email_verified", False):
        raise HTTPException(status_code=403, detail="Email not verified")

    # Extract email from the token
    email = decoded_token.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Email not found in token")

    return email

def check_user_exists(email: str) -> bool:
    """
    Check if a user exists in Cognito.

    :param email: Email of the user
    :return: True if the user exists, False otherwise
    """
    try:
        response = cognito.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=email
        )
        return True
    except cognito.exceptions.UserNotFoundException:
        return False
    except Exception as e:
        print(f"Error checking user existence: {str(e)}")
        raise e
    

def get_secret_hash_using_client_id(username, client_id):
    """Generate SECRET_HASH for Cognito authentication."""
    message = username + client_id
    dig = hmac.new(COGNITO_CLIENT_SECRET.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()
def get_secret_hash(username: str) -> str:
    """Compute Cognito secret hash for authentication."""
    msg = username + COGNITO_CLIENT_ID
    dig = hmac.new(COGNITO_CLIENT_SECRET.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()
def get_login_token(email: str, username: str, password: str) -> str:
    try:
        auth_params = {
            "USERNAME": username if username else email,
            "PASSWORD": password,
            "SECRET_HASH": get_secret_hash_using_client_id(username, COGNITO_CLIENT_ID)
        }
        auth_response = cognito.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
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
            ClientId=COGNITO_CLIENT_ID,
            Username=email,
            SecretHash=get_secret_hash(email)
        )
    except cognito.exceptions.UserNotFoundException:
        return "User not found."

def reset_password(email, confirmation_code, new_password):
    try:
        return cognito.confirm_forgot_password(
            ClientId=COGNITO_CLIENT_ID,
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
