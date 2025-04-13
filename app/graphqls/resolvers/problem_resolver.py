from services.problems_manager import ProblemManager
from ariadne import QueryType, make_executable_schema, load_schema_from_path
from routes import db_connection
type_defs = load_schema_from_path("graphqls/schema/schema.graphql")

query = QueryType()
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
    problems_metadata = problems_manager.get_problems(userId)
    if not problems_metadata:
        raise Exception(f"No problems found for user with ID {userId}.")
    return [problem.to_dict() for problem in problems_metadata]

problemSchema = make_executable_schema(type_defs, query)