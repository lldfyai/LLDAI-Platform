from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
import json
import asyncio
from fastapi.responses import JSONResponse
import os
import uuid
from config import UPLOAD_DIR
from services.code_executor import CodeExecutor
from enum import Enum
from pydantic import BaseModel
from config import SUBMISSION_S3_BUCKET
import shutil
from client.s3_client import upload_file
from dao.submission_dao import SubmissionDAO
from models.db.tables import SubmissionMetadata
from models.db.enums import Language, SubmissionState
from datetime import datetime
from services.submission_manager import SubmissionManager
from services.submission_handler import SubmissionHandler


router = APIRouter()

submission_handler = SubmissionHandler(submission_manager=SubmissionManager())

@router.get("/sse/status/{submission_id}")
async def sse_status(submission_id: str):
    """Streams submission status updates using SSE (Server-Sent Events)."""
    async def event_stream():
        while True:
            # Fetch the submission state from the database using submission_manager
            submission = submission_handler.submission_manager.get_submission(submission_id)
            if not submission:
                raise HTTPException(status_code=404, detail="Submission not found")

            # Construct the response data
            data = {
                "state": submission.state.value,
                "result": {
                    "statusCode": submission.statusCode,
                    "testsPassed": submission.testsPassed,
                    "totalTests": submission.totalTests,
                    "executionTime": submission.executionTime,      
                    "memory": submission.memory
                } if submission.state == SubmissionState.COMPLETED else None
            }

            # Stream the current state
            yield f"data: {json.dumps(data)}\n\n"

            # Break the loop if the submission is completed
            if submission.state == SubmissionState.COMPLETED:
                break

            await asyncio.sleep(1)  # Reduce polling frequency
        
    return StreamingResponse(event_stream(), media_type="text/event-stream")