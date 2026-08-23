from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import engine, Base, get_db
from app.models import Task


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Task Management API",
    description="Task management API for the FlyRank internship project",
    version="1.0.0",
)


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


@app.post("/tasks")
def create_task(
    task_data: dict,
    db: Session = Depends(get_db)
):
    title = task_data.get("title")
    description = task_data.get("description")

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    task = Task(
        title=title,
        description=description,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }