from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
from app.config import UPLOAD_DIR
from app.services.code_executor import CodeExecutor
from enum import Enum

router = APIRouter()

class SubmissionStatus(Enum):
    RECEIVED = "Received"
    QUEUED = "Queued"
    COMPLETED = "Completed"

class SubmissionHandler:
    def __init__(self):
        self.executor = CodeExecutor()

    async def save_files(self, files, user_folder):
        file_paths = []
        for file in files:
            file_path = os.path.join(user_folder, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_paths.append(file_path)
        return file_paths

    async def handle_submission(self, files, language, user_id, problem_id):
        job_id = str(uuid.uuid4())
        user_folder = os.path.join(UPLOAD_DIR, user_id, problem_id, job_id)
        os.makedirs(user_folder, exist_ok=True)
        print(f"Created user folder: {user_folder}")  # Debugging statement

        await self.save_files(files, user_folder)

        for file in files:
            file_path = os.path.join(user_folder, file.filename)
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
            else:
                print(f"File exists: {file_path}")


        result = self.executor.execute_code_in_docker(job_id, language, user_folder)

        return {"job_id": job_id, "status": SubmissionStatus.COMPLETED.value, "result": result}



submission_handler = SubmissionHandler()

@router.post("/submit/")
async def submit_code(
    files: list[UploadFile] = File(...),
    language: str = Form(...),
    user_id: str = Form(...),
    problem_id: str = Form(...)
):
    result = await submission_handler.handle_submission(files, language, user_id, problem_id)
    return JSONResponse(result)