class ProblemMetadata:
    """
    Business Logic (BL) entity for Problem metadata.
    Represents the structure of a problem in the business logic layer.
    """

    def __init__(self, problem_id, problem_title, difficulty, tags, time_limit, memory_limit, s3_path):
        self.problem_id = problem_id
        self.problem_title = problem_title
        self.difficulty = difficulty
        self.tags = tags
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.s3_path = s3_path

    def to_dict(self):
        """
        Convert the ProblemMetadata object to a dictionary.
        Useful for serialization or returning as a response.
        """
        return {
            "problem_id": self.problem_id,
            "problem_title": self.problem_title,
            "difficulty": self.difficulty,
            "tags": self.tags,
            "time_limit": self.time_limit,
            "memory_limit": self.memory_limit,
            "s3_path": self.s3_path
        }