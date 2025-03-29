from graphene import ObjectType, Int, String, List, Float

class ProblemMetadata(ObjectType):
    problem_id = Int()
    problem_title = String()
    difficulty = String()
    tags = List(String)
    time_limit = Float()
    memory_limit = Float()
    s3_path = String()

