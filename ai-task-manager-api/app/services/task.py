from sqlalchemy.orm import Session

from app.repositories import task as task_repository
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate):
    return task_repository.create_task(db, task_data)


def get_tasks(db: Session):
    return task_repository.get_tasks(db)


def get_task(db: Session, task_id: int):
    return task_repository.get_task(db, task_id)


def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = task_repository.get_task(db, task_id)

    if task is None:
        return None

    return task_repository.update_task(db, task, task_data)


def delete_task(db: Session, task_id: int):
    task = task_repository.get_task(db, task_id)

    if task is None:
        return False

    task_repository.delete_task(db, task)
    return True