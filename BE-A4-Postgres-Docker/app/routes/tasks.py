from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.repositories.in_memory import InMemoryTaskRepository
from app.services.task_service import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])

repository = InMemoryTaskRepository()
service = TaskService(repository)


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


@router.get("/")
def get_tasks():
    return service.get_all_tasks()


@router.get("/{task_id}")
def get_task(task_id: int):
    task = service.get_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("/")
def create_task(task: TaskCreate):
    return service.create_task(task.title)


@router.put("/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    updated_task = service.update_task(
        task_id,
        task.title,
        task.done,
    )

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@router.delete("/{task_id}")
def delete_task(task_id: int):
    deleted = service.delete_task(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted"}