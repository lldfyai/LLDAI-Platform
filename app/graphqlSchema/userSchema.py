from ariadne import make_executable_schema, load_schema_from_path
from graphqlSchema.resolvers import resolvers
import os
schema_path = os.path.join(os.path.dirname(__file__), "userSchema.graphql")
type_defs = load_schema_from_path(schema_path)
userSchema = make_executable_schema(type_defs, resolvers)
