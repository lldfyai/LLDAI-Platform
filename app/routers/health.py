from fastapi import APIRouter

health_router = APIRouter(tags=["Health"])

@health_router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI ECS Demo",
        "version": "1.0.0"
    }