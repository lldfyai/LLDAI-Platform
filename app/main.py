from fastapi import FastAPI
import os
from app.config import UPLOAD_DIR

app = FastAPI(
    title="LLDify Platform",
    description="API to handle multi-file code submissions and execution",
    version="1.0.0",
)

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

#minor
@app.get("/health")
def health_check():
    return {"status": "healthy"}
# New mock REST API endpoint
@app.get("/api/v1/mock")
def read_mock():
    return {"mock": "This is a mock API response."}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Code Execution Platform!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
