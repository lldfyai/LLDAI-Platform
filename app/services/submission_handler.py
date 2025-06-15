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
from models.bl.submission import SubmissionRequest



class SubmissionHandler:
    def __init__(self, submission_manager):
        self.executor = CodeExecutor()
        self.submission_manager = submission_manager

    async def process_submission(self, submission: SubmissionRequest, background_tasks: BackgroundTasks):
        try:
            submission_id = str(uuid.uuid4())
            new_submission = SubmissionMetadata(
                submissionId=submission_id, 
                problemId=submission.problem_id,
                userId=1,  # Hardcoding the user_id for now. Should be fetched from the JWT token
                language=Language[submission.lang.name],
                state=SubmissionState.RECEIVED,
                createdAt=datetime.now()
            )
            # Save the submission metadata to the database
            self.submission_manager.create_submission(new_submission)            
            background_tasks.add_task(self.handle_submission, submission_id, submission.files_metadata, submission.lang, "1", submission.problem_id) # Hardcoding the user_id for now. Should be fetched from the JWT token

            print(f"Submission {submission_id} received for problem {submission.problem_id} in language {submission.lang.name}")

            return {"submissionId": submission_id, "state": SubmissionState.RECEIVED.value}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def save_files(self, files_metadata, user_folder):
        file_paths = []
        for filename, content in files_metadata.items():
            file_path = os.path.join(user_folder, filename)
            with open(file_path, "wb") as buffer:
                buffer.write(content.encode())
            file_paths.append(file_path)
        return file_paths

    async def copy_to_s3_and_cleanup(self, user_id, problem_id, submission_id, submission_folder):
        """
        Copies all files in the submission folder to S3 and deletes the folder from the local host.
        
        :param submission_id: ID of the submission
        :param submission_folder: Path to the submission folder on the local host
        """
        try:
            # Define the S3 bucket and folder path
            s3_bucket = SUBMISSION_S3_BUCKET  # Replace with your S3 bucket name
            s3_folder = f"{user_id}/{problem_id}/{submission_id}/"

            # Iterate through all files in the submission folder
            for root, _, files in os.walk(submission_folder):
                for file_name in files:
                    local_file_path = os.path.join(root, file_name)
                    s3_object_path = os.path.join(s3_folder, file_name)

                    # Preserve the directory structure in S3 by calculating the relative path
                    relative_path = os.path.relpath(local_file_path, submission_folder)
                    s3_object_path = os.path.join(s3_folder, relative_path)

                    # Upload the file to S3
                    upload_file(local_file_path, s3_bucket, s3_object_path)
                    print(f"Uploaded {local_file_path} to S3 at {s3_object_path}")

            # Delete the local submission folder after successful upload
            shutil.rmtree(submission_folder)
            print(f"Deleted local folder: {submission_folder}")

        except Exception as e:
            print(f"Error during copy_to_s3_and_cleanup: {e}")
            raise

    async def handle_submission(self, submission_id, files_metadata, language, user_id, problem_id):
        
        await asyncio.sleep(15)  # Simulate processing delay
        submission_folder = os.path.join(UPLOAD_DIR, user_id, problem_id, submission_id)
        os.makedirs(submission_folder, exist_ok=True)

        await self.save_files(files_metadata, submission_folder)
        self.submission_manager.partial_update_submission(
            submission_id=submission_id,
            updates={"state": SubmissionState.PROCESSING})
            
        await asyncio.sleep(15)  # Simulate processing delay

        result = self.executor.execute_code_in_docker(submission_id, problem_id, language, submission_folder)

        self.submission_manager.partial_update_submission(
            submission_id=submission_id,
            updates={
                "state": SubmissionState.COMPLETED,
                "statusCode": result.get("output").get("status_code"),
                "testsPassed": result.get("output").get("total_correct"),
                "totalTests": result.get("output").get("total_testcases")
            })
            
        await self.copy_to_s3_and_cleanup(user_id, problem_id, submission_id, submission_folder)

        return {"submission_id": submission_id, "state": SubmissionState.COMPLETED.value, "result": result}
