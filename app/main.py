from fastapi import FastAPI
from routes import submission_handler
import os
from ariadne.asgi import GraphQL
from app.graphql.schema import schema
from config import UPLOAD_DIR 
from fastapi.middleware.cors import CORSMiddleware
from routes.create_problem import router as create_problem_router

app = FastAPI(
    title="LLDify Platform",
    description="API to handle multi-file code submissions and execution",
    version="1.0.0",
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Include API routes comment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(submission_handler.router, prefix="/api/v1", tags=["Submissions"])
app.include_router(create_problem_router, prefix="/api/v1", tags=["Problem Management"])
graphql_app = GraphQL(schema, debug=True)
app.add_route("/graphql", graphql_app)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Code Execution Platform!"}

@app.get("/health")
def read_root():
    return {"message": "Healthyyyy!"}

# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)