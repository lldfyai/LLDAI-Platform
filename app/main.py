from fastapi import FastAPI
from routes import submission_handler
import os
from config import UPLOAD_DIR 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="LLDify Platform",
    description="API to handle multi-file code submissions and execution",
    version="1.0.0",
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Include API routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(submission_handler.router, prefix="/api/v1", tags=["Submissions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Code Execution Platform!"}