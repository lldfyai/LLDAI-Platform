from ariadne import QueryType, MutationType
from services import cognito_service, github_service
from services.user_manager import UserManager
from datetime import datetime
import os
import requests
from ariadne import make_executable_schema, load_schema_from_path
query = QueryType()
mutation = MutationType()

user_manager = UserManager()

@query.field("githubUsernameEmail")
def resolve_github_username_email(_, info, input):
    token = github_service.get_github_access_token(input["githubCode"])
    requests.get(
        "https://api.github.com/",
        headers={"Authorization": f"Bearer {token}"})
    print("successful ping")
    return {
        "githubToken": token,
        "username": github_service.get_github_username(token),
        "email": github_service.get_github_primary_email(token)
    }

@mutation.field("register")
def resolve_register(_, info, input):
    username = input.get("username")
    email = input.get("email")
    password = input.get("password")
    github_token = input.get("githubToken")
    if not email:
        if not github_token:
            raise Exception("GitHub OAuth code required if username or email is missing")
        token = github_token
        if not username:
            username = github_service.get_github_username(token)
        email = github_service.get_github_primary_email(token)

    try:
        cognito_service.register_cognito_user(username, email, password)
    except Exception as e:
        raise Exception(str(e))

    # Use UserManager to create the user
    user_id = user_manager.create_user(username, email)

    return {
        "username": username,
        "email": email,
        "problemsSolved": 0,
        "rank": 0,
        "userId": user_id
    }

@mutation.field("login")
def resolve_login(_, info, input):
    token = input.get("githubToken")
    password = input.get("password")
    if token:
        username = github_service.get_github_username(token)
        email = github_service.get_github_primary_email(token)
    else:
        username = input.get("username")
        email = input.get("email")
        token = None

    # Use UserManager to get user details
    user_details = user_manager.get_user(username=username, email=email)
    if not user_details:
        raise Exception("User not found")

    return {
        "user": {
            "username": user_details["username"],
            "email": user_details["email"],
            "problemsSolved": user_details["problemsSolved"],
            "rank": user_details["rank"],
            "userId": user_details["userId"]
        },
        "token": cognito_service.get_login_token(email, username, password),
        "githubToken": token
    }

@mutation.field("forgotPassword")
def resolve_forgot_password(_, info, email):
    try:
        return cognito_service.forgot_password(email)
    except Exception as e:
        return str(e)

@mutation.field("resetPassword")
def resolve_reset_password(_, info, input):
    try:
        result = cognito_service.reset_password(
            input.get("email"),
            input.get("confirmationCode"),
            input.get("newPassword")
        )
        return "Password reset successfully" if result else "Password reset failed"
    except Exception as e:
        return str(e)

resolvers = [query, mutation]
schema_path = os.path.join(os.path.dirname(__file__), "schema/userSchema.graphql")
type_defs = load_schema_from_path(schema_path)
userSchema = make_executable_schema(type_defs, resolvers)