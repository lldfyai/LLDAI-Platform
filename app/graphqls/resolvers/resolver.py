from services.problems_manager import ProblemManager
from ariadne import QueryType,MutationType, make_executable_schema, load_schema_from_path
from services import cognito_service, github_service
from services.user_manager import UserManager
type_defs = load_schema_from_path("graphqls/schema/schema.graphql")

query = QueryType()
mutation = MutationType()
user_manager = UserManager()
problems_manager = ProblemManager()


@query.field("problem")
def resolve_problem(_, info, problemId):
    # Call the resolver function to fetch the problem
    problem_metadata = problems_manager.get_problem(problemId)
    if problem_metadata is None:
        raise Exception(f"Problem with ID {problemId} not found.")
    return problem_metadata.to_dict()

@query.field("problems")
def resolve_problems(_, info, userId):
    # Call the resolver function to fetch all problems for the user
    problems_metadata = problems_manager.get_problems()
    if not problems_metadata:
        raise Exception(f"No problems found for user with ID {userId}.")
        # Convert SQLAlchemy objects to dictionaries
    return [
        {
            "problemId": problem.problemId,
            "problemTitle": problem.problemTitle,
            "difficulty": problem.difficulty.name if problem.difficulty else None,
            "tags": problem.tags,
            "timeLimit": problem.timeLimit,
            "memoryLimit": problem.memoryLimit
        }
        for problem in problems_metadata
    ]

@query.field("githubUsernameEmail")
def resolve_github_username_email(_, info, input):
    token = github_service.get_github_access_token(input["githubCode"])
    print("github_token", token)
    print("successful ping")
    username = github_service.get_github_username(token)
    email = github_service.get_github_primary_email(token)

    # Check if the user already exists in Cognito
    try:
        user_exists = cognito_service.check_user_exists(email)
    except Exception as e:
        raise Exception(f"Error checking user existence: {str(e)}")
    return {
        "githubToken": token,
        "username": username,
        "email": email,
        "existing":  user_exists
    }

@mutation.field("register")
def resolve_register(_, info, input):
    username = input.get("username")
    email = input.get("email")
    password = input.get("password")
    github_token = input.get("githubToken")
    print("github_token", github_token)

    if not email:
        if not github_token:
            raise Exception("GitHub OAuth code required if username or email is missing")
        token = github_token
        if not username:
            username = github_service.get_github_username(token)
        email = github_service.get_github_primary_email(token)

    # Register the user in Cognito
    try:
        cognito_service.register_cognito_user(username, email, password)
    except Exception as e:
        raise Exception(str(e))

    # Use UserManager to create the user
    user_id = user_manager.create_user(username, email)

    # Generate login token
    login_token = cognito_service.get_login_token(email, username, password)

    return {
            "user": {
            "username": username,
            "email": email,
            "problemsSolved": 0,
            "rank": 0,
            "userId": user_id
        },

        "token": login_token,  # Include the login token in the response,
        "githubToken": github_token  # Include the GitHub token if provided
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
            "problemsSolved": user_details["totalSolved"],
            "rank": user_details["rating"],
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
schema = make_executable_schema(type_defs, query)