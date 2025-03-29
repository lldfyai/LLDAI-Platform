from models.bl.problem import ProblemMetadata
from client.s3_client import generate_presigned_url

class ProblemManager:
    def __init__(self, db):
        self.db = db

    def get_problems(self):
        problems = self.db.get_problems()
        return problems

    def get_problem(self, problem_id):
        # Mocking the problem
        # ToDo: Implement the actual logic to fetch the problem from the database
        s3_path = generate_presigned_url("lldfy-problem-store", f"{problem_id}/description.md")
        problem = ProblemMetadata("1", "Two Sum", "Easy", ["Array", "Hash Table"], 1, 1, s3_path)
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