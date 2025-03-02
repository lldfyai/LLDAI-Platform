from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
import json
import asyncio
from fastapi.responses import JSONResponse
import os
import shutil
import uuid
from config import UPLOAD_DIR
from services.code_executor import CodeExecutor
from enum import Enum
from pydantic import BaseModel


router = APIRouter()

class SubmissionState(Enum):
    RECEIVED = "Received"
    PROCESSING = "Processing"
    COMPLETED = "Completed"

class SubmissionHandler:
    def __init__(self):
        self.executor = CodeExecutor()
        # ToDo: Results store for submissions can be rerieved from DB as well
        self.submission_store = {}  # Tracks submission state & results

    async def save_files(self, files_metadata, user_folder):
        # ToDo: Implement file saving logic in S3 bucket
        file_paths = []
        for filename, content in files_metadata.items():
            file_path = os.path.join(user_folder, filename)
            with open(file_path, "wb") as buffer:
                buffer.write(content.encode())
            file_paths.append(file_path)
        return file_paths

    async def handle_submission(self, submission_id, files_metadata, language, user_id, problem_id):
        
        await asyncio.sleep(25)  # Simulate processing delay
        submission_folder = os.path.join(UPLOAD_DIR, user_id, problem_id, submission_id)
        os.makedirs(submission_folder, exist_ok=True)

        await self.save_files(files_metadata, submission_folder)
        self.submission_store[submission_id]["state"] = SubmissionState.PROCESSING.value

        await asyncio.sleep(25)  # Simulate processing delay

        result = self.executor.execute_code_in_docker(submission_id, language, submission_folder)

        self.submission_store[submission_id]["state"] = SubmissionState.COMPLETED.value
        self.submission_store[submission_id]["result"] = result


        return {"submission_id": submission_id, "state": SubmissionState.COMPLETED.value, "result": result}



submission_handler = SubmissionHandler()

class SubmissionRequest(BaseModel):
    problem_id: str
    lang: str
    files_metadata: dict

@router.post("/submit/")
async def submit_code(submission: SubmissionRequest, background_tasks: BackgroundTasks):
    try:
        submission_id = str(uuid.uuid4())
        submission_handler.submission_store[submission_id] = {
            "state": SubmissionState.RECEIVED.value,
            "result": None
        }
        background_tasks.add_task(submission_handler.handle_submission, submission_id, submission.files_metadata, submission.lang, "1", submission.problem_id) # Hardcoding the user_id for now. Should be fetched from the JWT token
        return JSONResponse({"submission_id": submission_id, "state": SubmissionState.RECEIVED.value})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sse/status/{submission_id}")
async def sse_status(submission_id: str):
    """Streams submission status updates using SSE (Server-Sent Events)."""
    async def event_stream():
        while  submission_handler.submission_store.get(submission_id, {}).get("state") not in [SubmissionState.COMPLETED.value, "Failed"]:
            yield f"data: {json.dumps( submission_handler.submission_store[submission_id])}\n\n"
            await asyncio.sleep(1)  # Reduce polling frequency

        # Final update
        yield f"data: {json.dumps( submission_handler.submission_store[submission_id])}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
