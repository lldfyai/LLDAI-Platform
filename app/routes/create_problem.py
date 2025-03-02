from fastapi import APIRouter,FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from app.routes.db_connection import insert_problem_metadata

router = APIRouter()

# Define a Pydantic model that corresponds to your data input
class Problem(BaseModel):
    problemTitle: str
    difficulty: str
    problemId: Optional[int] = None
    Tags: Optional[List[str]] = None
    timeLimit: Optional[float] = None
    memoryLimit: Optional[float] = None
    s3_path: Optional[str] = None
    description: Optional[str] = None

# Create an API endpoint to insert new problem metadata into the database
@router.post("/create_problem/")
async def create_problem(problem: Problem):
    try:
        insert_problem_metadata(
            problemTitle=problem.problemTitle,
            difficulty=problem.difficulty,
            Tags=problem.Tags,
            timeLimit=problem.timeLimit,
            memoryLimit=problem.memoryLimit,
            s3_path=problem.s3_path,
            description=problem.description
        )
        return {"message": "Problem added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

