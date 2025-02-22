from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import uuid
from app.config import UPLOAD_DIR
from app.services.code_executor import CodeExecutor
from enum import Enum
from pydantic import BaseModel


router = APIRouter()

class SubmissionState(Enum):
    RECEIVED = "Received"
    QUEUED = "Queued"
    COMPLETED = "Completed"

class SubmissionHandler:
    def __init__(self):
        self.executor = CodeExecutor()

    async def save_files(self, files_metadata, user_folder):
        # ToDo: Implement file saving logic in S3 bucket
        file_paths = []
        for filename, content in files_metadata.items():
            file_path = os.path.join(user_folder, filename)
            with open(file_path, "wb") as buffer:
                buffer.write(content.encode())
            file_paths.append(file_path)
        return file_paths

    async def handle_submission(self, files_metadata, language, user_id, problem_id):
        submission_id = str(uuid.uuid4())
        submission_folder = os.path.join(UPLOAD_DIR, user_id, problem_id, submission_id)
        os.makedirs(submission_folder, exist_ok=True)

        await self.save_files(files_metadata, submission_folder)

        result = self.executor.execute_code_in_docker(submission_id, language, submission_folder)

        return {"submission_id": submission_id, "state": SubmissionState.COMPLETED.value, "result": result}



submission_handler = SubmissionHandler()

class SubmissionRequest(BaseModel):
    problem_id: str
    lang: str
    files_metadata: dict

@router.post("/submit/")
async def submit_code(submission: SubmissionRequest):
    try:
        result = await submission_handler.handle_submission(submission.files_metadata, submission.lang, "1", submission.problem_id) # Hardcoding the user_id for now. Should be fetched from the JWT token
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))