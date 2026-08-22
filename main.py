from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()


class Task(BaseModel):
    title: str
    done: bool


# Create database and table

connection = sqlite3.connect("tasks.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
)
""")

connection.commit()
connection.close()


@app.get("/tasks")
def get_tasks():
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    connection.close()

    tasks = []

    for row in rows:
        tasks.append(
            {
                "id": row[0],
                "title": row[1],
                "done": bool(row[2])
            }
        )

    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row:
        return {
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        }

    return {"message": "Task not found!"}


@app.post("/tasks")
def create_task(task: Task):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, int(task.done))
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return {
        "id": task_id,
        "title": task.title,
        "done": task.done
    }


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (task.title, int(task.done), task_id)
    )

    connection.commit()
    connection.close()

    return {"message": "Task updated successfully!"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return {"message": "Task deleted successfully!"}