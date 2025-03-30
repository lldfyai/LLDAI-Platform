from models.bl.problem import ProblemMetadata
from client.s3_client import generate_presigned_url
from config import PROBLEM_S3_BUCKET
from dao.problem_dao import ProblemDAO

class ProblemManager:
    def __init__(self):
        self.db = ProblemDAO()   

    def get_problems(self):
        problems = self.db.get_problems()
        return problems

    def get_problem(self, problem_id):
        problem_metadata = self.db.get_problem_by_id(problem_id)
        if problem_metadata is None:
            return None # Problem not found             
        s3_path = generate_presigned_url(PROBLEM_S3_BUCKET, f"{problem_id}/description.md")
        problem = ProblemMetadata(problem_metadata.problemId, problem_metadata.problemTitle, problem_metadata.difficulty, problem_metadata.tags, problem_metadata.timeLimit, problem_metadata.memoryLimit, s3_path)
        return problem

    def create_problem(self, problem):
        problem_id = self.db.create_problem(problem)
        return problem_id

    def update_problem(self, problem_id, problem):
        self.db.update_problem(problem_id, problem)
        return problem_id

    def delete_problem(self, problem_id):
        self.db.delete_problem(problem_id)
        return problem_id