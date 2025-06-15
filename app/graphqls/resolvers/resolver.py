from services.problems_manager import ProblemManager
from ariadne import QueryType,MutationType, make_executable_schema, load_schema_from_path, ScalarType
from services import cognito_service, github_service
from services.user_manager import UserManager
from services.submission_manager import SubmissionManager
from services.submission_handler import SubmissionHandler
from models.bl.submission import SubmissionRequest
from models.bl.enums import SupportedLanguages
from fastapi import Response

type_defs = load_schema_from_path("graphqls/schema/schema.graphql")

query = QueryType()
mutation = MutationType()

json_scalar = ScalarType("JSON")

@json_scalar.serializer
def serialize_json(value):
    return value

@json_scalar.value_parser
def parse_json(value):
    return value

user_manager = UserManager()
problems_manager = ProblemManager()
submission_manager = SubmissionManager()
submission_handler = SubmissionHandler(submission_manager=submission_manager)



@query.field("problem")
def resolve_problem(_, info, problemId):
    # Call the resolver function to fetch the problem
    problem_metadata = problems_manager.get_problem(problemId)
    if problem_metadata is None:
        raise Exception(f"Problem with ID {problemId} not found.")
    
    return {
            "problemId": problem_metadata.problem_id,
            "problemTitle": problem_metadata.problem_title,
            "difficulty": problem_metadata.difficulty.name if problem_metadata.difficulty else None,
            "tags": problem_metadata.tags,
            "timeLimit": problem_metadata.time_limit,
            "memoryLimit": problem_metadata.memory_limit,
            "s3Path": problem_metadata.s3_path
    }


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
    response: Response = info.context["response"]  # Get the Response object from the context
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
    # Set the token as a cookie
    response.set_cookie(
        key="token",
        value=login_token,
        httponly=True,
        path="/",
        max_age=3600  # 1 hour
    )
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
    response: Response = info.context["response"] 
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
    
    login_token = cognito_service.get_login_token(email, username, password)
    # Set the token as a cookie
    response.set_cookie(
        key="token",
        value=login_token,
        httponly=True,
        path="/",
        max_age=3600  # 1 hour
    )
    return {
        "user": {
            "username": user_details["username"],
            "email": user_details["email"],
            "problemsSolved": user_details["totalSolved"],
            "rank": user_details["rating"],
            "userId": user_details["userId"]
        },
        "token": login_token,
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
    
@query.field("getSubmissionMetadata")
def resolve_get_submission_metadata(_, info, problemId, userId):
    try:
        submissions = submission_manager.get_submission_metadata(problemId, userId)
        return [
            {
                "submissionId": str(submission.submissionId),
                "problemId": submission.problemId,
                "userId": submission.userId,
                "language": submission.language.name if submission.language else None,
                "state": submission.state.name if submission.state else None,
                "statusCode": submission.statusCode,
                "testsPassed": submission.testsPassed,
                "totalTests": submission.totalTests,
                "executionTime": submission.executionTime,
                "memory": submission.memory,
                "createdAt": submission.createdAt.isoformat() if submission.createdAt else None
            }
            for submission in submissions
        ]
    except Exception as e:
        print(f"Error resolving getSubmissionMetadata: {e}")
        return []

@mutation.field("submitCode")
async def resolve_submit_code(_, info, input):
    problem_id = input.get("problemId")
    lang = input.get("lang")
    files_metadata = input.get("filesMetadata")

    submission_request = SubmissionRequest(
        problem_id=problem_id,
        lang=SupportedLanguages[lang],
        files_metadata=json.loads(files_metadata) if isinstance(files_metadata, str) else files_metadata
    )
    
    background_tasks = info.context["background_tasks"]

    submission = await submission_handler.process_submission(submission_request, background_tasks)

    return submission



schema = make_executable_schema(type_defs, [query, mutation, json_scalar])
