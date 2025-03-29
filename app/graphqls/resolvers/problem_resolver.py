from graphene import ObjectType, Field, Int
import graphene
from graphqls.models import ProblemMetadata
from services.problems_manager import ProblemManager
from ariadne import QueryType, make_executable_schema, load_schema_from_path

type_defs = load_schema_from_path("graphqls/schema/schema.graphql")

query = QueryType()
problems_manager = ProblemManager(None)


@query.field("problem")
def resolve_problem(_, info, problemId):
    # Call the resolver function to fetch the problem
    problem_metadata = problems_manager.get_problem(problemId)
    if problem_metadata is None:
        raise Exception(f"Problem with ID {problemId} not found.")
    return problem_metadata.to_dict()

problemSchema = make_executable_schema(type_defs, query)