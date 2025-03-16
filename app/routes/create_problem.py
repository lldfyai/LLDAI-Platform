from fastapi import APIRouter,FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from routes.db_connection import insert_problem_metadata

router = APIRouter()

class Problem(BaseModel):
    problemTitle: str
    difficulty: str
    Tags: List[str]
    timeLimit: float
    memoryLimit: float
    s3_path: str
    description: str

@router.post("/create_problem/")
async def create_problem(problem: Problem):
    try:
        print(problem)
        insert_problem_metadata(
            problem_title=problem.problemTitle,
            difficulty=problem.difficulty,
            tags=problem.Tags,
            time_limit=problem.timeLimit,
            memory_limit=problem.memoryLimit,
            s3_path=problem.s3_path,
            description=problem.description
        )
        return {"message": "Problem added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

