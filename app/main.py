from fastapi import FastAPI
from routes import sse_route
from fastapi import BackgroundTasks, Response
import os
from ariadne.asgi import GraphQL
from config import UPLOAD_DIR
from fastapi.middleware.cors import CORSMiddleware
from graphqls.resolvers.resolver import schema
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from services.cognito_service import verify_auth_token
from dao.user_dao import UserDao

app = FastAPI(
    title="LLDify Platform",
    description="API to handle multi-file code submissions and execution",
    version="1.0.0",
)

@app.middleware("http")
async def add_response_to_context(request: Request, call_next):
    response = Response()
    request.state.response = response
    response = await call_next(request)
    return response


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Only enforce authentication on protected APIs
        if request.url.path == "/graphql":
            try:
                # Parse the request body to inspect the GraphQL query
                body = await request.json()
                query = body.get("query", "")
                # Skip authentication for login and register mutations
                if "mutation" in query and ("login" in query or "register" in query) or "githubUsernameEmail" in query:
                    print("Skipping authentication for login or register mutation")
                    return await call_next(request)
            except Exception as e:
                print(f"Error parsing GraphQL query: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")

            # Enforce authentication for other APIs
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                raise HTTPException(status_code=401, detail="Authorization header missing")

            # Expect header format: "Bearer <token>"
            parts = auth_header.split(" ")
            if len(parts) != 2 or parts[0].lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid Authorization header format")

            token = parts[1]
            try:
                # Get email from the token
                email = verify_auth_token(token)

                # Fetch userId using email
                user_dao = UserDao()
                user_id = user_dao.get_user_id_by_email(email)

                # Attach userId to the request state
                request.state.user_id = user_id
            except Exception as e:
                raise HTTPException(status_code=401, detail=str(e))
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
app.include_router(sse_route.router, prefix="/api/v1", tags=["SSE"])



@app.post("/graphql")
async def graphql_server(request: Request, background_tasks: BackgroundTasks, response: Response):
    context = {
        "request": request,
        "background_tasks": background_tasks,
        "response": response
    }
    graphql = GraphQL(schema, context_value=context)
    return await graphql.handle_request(request)



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