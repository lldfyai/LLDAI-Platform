from dao.submission_dao import SubmissionDAO

class SubmissionManager:
    def __init__(self):
        self.db = SubmissionDAO()

    def create_submission(self, submission_data):
        return self.db.create_submission(submission_data)

    def get_submission(self, submission_id):
        return self.db.get_submission(submission_id)

    def full_update_submission(self, submission_data):
        return self.db.full_update_submission(submission_data)
    
    def partial_update_submission(self, submission_id, updates):
        return self.db.partial_update_submission(submission_id, updates)