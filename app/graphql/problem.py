# file: schema.py
from ariadne import gql, make_executable_schema
from ariadne.asgi import GraphQL

type_defs = gql("""
    type Query {
        problems: [Problem]
    }

    type Problem {
        problemId: Int
        problemTitle: String
        difficulty: String
        Tags: [String]
    }
""")
