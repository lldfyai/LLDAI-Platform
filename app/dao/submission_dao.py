from dao.connection import get_db
from models.db.tables import SubmissionMetadata 
from typing import List
class SubmissionDAO:

    def create_submission(self, submission):
        session = next(get_db())
        session.add(submission)
        session.commit()
        return submission

    def get_submission(self, submission_id):
        session = next(get_db())
        return session.query(SubmissionMetadata).filter(SubmissionMetadata.submissionId == submission_id).first()

    def full_update_submission(self, submission):
        session = next(get_db())
        session.merge(submission)
        session.commit()
        return submission
    
    def partial_update_submission(self, submission_id, updates: dict):
        """
        Directly updates specific fields of a submission without fetching the object.

        :param submission_id: ID of the submission to update
        :param updates: Dictionary of fields to update with their new values
        :return: Number of rows updated
        """
        session = next(get_db())
        rows_updated = session.query(SubmissionMetadata).filter(SubmissionMetadata.submissionId == submission_id).update(updates)
        session.commit()
        return rows_updated


    def delete_submission(self, submission_id):
        session = next(get_db())
        submission = self.get_submission(submission_id)
        if submission:
            session.delete(submission)
            session.commit()
            return True
        return False
    

    def get_submission_metadata(self, problem_id: int, user_id: int) -> List[SubmissionMetadata]:
        """
        Fetch submission metadata based on problemId and userId.

        :param problem_id: ID of the problem
        :param user_id: ID of the user
        :return: List of SubmissionMetadata objects
        """
        session = next(get_db())
        try:
            submissions = session.query(SubmissionMetadata).filter(
                SubmissionMetadata.problemId == problem_id,
                SubmissionMetadata.userId == user_id
            ).all()
            return submissions
        except Exception as e:
            print(f"Error fetching submission metadata: {e}")
            return []