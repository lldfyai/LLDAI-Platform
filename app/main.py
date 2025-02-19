from fastapi import FastAPI
from app.routes import submission_handler
import os
from app.config import UPLOAD_DIR 


app = FastAPI(
    title="LLDify Platform",
    description="API to handle multi-file code submissions and execution",
    version="1.0.0",
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Include API routes
app.include_router(submission_handler.router, prefix="/api/v1", tags=["Submissions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Code Execution Platform!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)