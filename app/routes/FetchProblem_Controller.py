from db_connection import fetch_problems_metadata
from db_connection import fetch_problem_metadata

from ariadne import gql, make_executable_schema, QueryType
from db_connection import fetch_problems_metadata
from ariadne.asgi import GraphQL
from fastapi import FastAPI

from ariadne.load_schema import load_schema_from_path

type_defs = gql("""
    type Query {
        problems: [Problem]
        problem(problemId: Int!): Problem
    }

    type Problem {
        problemId: Int
        problemTitle: String
        difficulty: String
        Tags: [String]
        description: String
    }
""")

# Create a query type
query = QueryType()

@query.field("problems")
def resolve_problems(*_):
    problems_metadata = fetch_problems_metadata()
    return problems_metadata

@query.field("problem")
def resolve_problem(_, info, problemId):
    problem_metadata = fetch_problem_metadata(problemId)
    if problem_metadata is None:
        raise Exception(f"Problem with ID {problemId} not found")
    return problem_metadata


# Create executable schema
schema = make_executable_schema(type_defs, query)

# Create a GraphQL app using Ariadne's GraphQL component
graphql_app = GraphQL(schema, debug=True)

# Initiate FastAPI
app = FastAPI()

# Register the GraphQL app
app.add_route("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


