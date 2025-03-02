class CodeExecResponseModel:
    def __init__(self, status_code, lang, run_success, exec_runtime, memory, problem_id, finished, total_correct, total_testcases, submission_id, status_msg, evaluation_state, failed_testcase=None, expected_output=None, actual_output=None, error_msg=None):
        self.status_code = status_code
        self.lang = lang
        self.run_success = run_success
        self.exec_runtime = exec_runtime
        self.memory = memory
        self.problem_id = problem_id
        self.finished = finished
        self.total_correct = total_correct
        self.total_testcases = total_testcases
        self.failed_testcase = failed_testcase
        self.expected_output = expected_output
        self.actual_output = actual_output
        self.submission_id = submission_id
        self.status_msg = status_msg
        self.error_msg = error_msg
        self.evaluation_state = evaluation_state

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "lang": self.lang,
            "run_success": self.run_success,
            "exec_runtime": self.exec_runtime,
            "memory": self.memory,
            "problem_id": self.problem_id,
            "finished": self.finished,
            "total_correct": self.total_correct,
            "total_testcases": self.total_testcases,
            "failed_testcase": self.failed_testcase,
            "expected_output": self.expected_output,
            "actual_output": self.actual_output,
            "submission_id": self.submission_id,
            "status_msg": self.status_msg,
            "error_msg": self.error_msg,
            "evaluation_state": self.evaluation_state
        }