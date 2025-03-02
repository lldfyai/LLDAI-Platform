import time
from ariadne import QueryType, MutationType
from app.services import cognito_service, github_service
from app.routes import db_connection

query = QueryType()
mutation = MutationType()

@query.field("githubUsernameEmail")
def resolve_github_username_email(_, info, input):
    token = github_service.get_github_access_token(input["githubCode"])
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

    # Insert user into PostgreSQL asynchronously (simulated background processing)
    db_connection.put_user(username, email, int(time.time()))

    return {
        "username": username,
        "email": email,
        "problemsSolved": 0,
        "rank": 0
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
    return {
        "user": {
            "username": username,
            "email": email,
            "problemsSolved": 0,
            "rank": 0
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
