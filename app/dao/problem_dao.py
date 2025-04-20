from typing import Optional, List
from sqlalchemy.orm import Session
from models.db.tables import ProblemMetadata
from dao.connection import get_db

class ProblemDAO:

    def get_problem_by_id(self, problem_id: int) -> Optional[ProblemMetadata]:
        """
        Fetch a problem by its ID from the database.

        :param problem_id: ID of the problem to fetch
        :return: ProblemMetadata object if found, else None
        """
        session = next(get_db())
        problem = session.query(ProblemMetadata).filter(ProblemMetadata.problemId == problem_id).first()
        return problem

    def get_problems(self) -> List[ProblemMetadata]:
        """
        Fetch all problems from the database.

        :return: A list of ProblemMetadata objects
        """
        session = next(get_db())
        problems = session.query(ProblemMetadata).all()
        return problems
