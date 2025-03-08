from ariadne import QueryType, MutationType
from services import cognito_service, github_service
from routes import db_connection

query = QueryType()

@query.field("problems")
def resolve_problems(_, info, userId):
    problems_metadata = db_connection.fetch_problems_metadata(userId)
    return problems_metadata


@query.field("problem")
def resolve_problem(_, info, userId, problemId):
    problem_metadata = db_connection.fetch_problem_metadata(userId, problemId)
    if problem_metadata is None:
        raise Exception(f"Problem with ID {problemId} not found for user with ID {userId}")
    return problem_metadata

resolvers = [query]
