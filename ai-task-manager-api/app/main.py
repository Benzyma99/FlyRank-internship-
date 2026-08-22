from fastapi import FastAPI

from app.api.task import router as tasks_router


app = FastAPI(
    title="AI Task Management API",
    description="A production-style task management API with AI capabilities",
    version="1.0.0",
)


app.include_router(tasks_router)


@app.get("/")
def root():
    return {
        "message": "AI Task Management API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }