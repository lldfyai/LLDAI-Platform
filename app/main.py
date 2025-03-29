from fastapi import FastAPI
from routes import submission_handler
import os
from ariadne.asgi import GraphQL
from config import UPLOAD_DIR
from fastapi.middleware.cors import CORSMiddleware
from graphqls.resolvers.problem_resolver import problemSchema
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from services.cognito_service import verify_auth_token

app = FastAPI(
    title="LLDify Platform",
    description="API to handle multi-file code submissions and execution",
    version="1.0.0",
)
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Only enforce authentication on protected endpoints:
        if request.url.path.startswith("/graphql") or request.url.path.startswith("/api/v1"):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                raise HTTPException(status_code=401, detail="Authorization header missing")

            # Expect header format: "Bearer <token>"
            parts = auth_header.split(" ")
            if len(parts) != 2 or parts[0].lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid Authorization header format")

            token = parts[1]
            # Verify the token (this will raise an HTTPException if invalid)
            verify_auth_token(token)
        response = await call_next(request)
        return response

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Include API routes comment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add our custom authentication middleware
#app.add_middleware(AuthMiddleware)
app.include_router(submission_handler.router, prefix="/api/v1", tags=["Submissions"])
graphql_app = GraphQL(problemSchema, debug=True)
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