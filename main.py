from fastapi import FastAPI

app = FastAPI()

# Store tasks in a list
tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    },
    {
        "id": 2,
        "title": "Finish Assignment",
        "completed": False
    }
]

# Home page
@app.get("/")
def home():
    return {"message": "Welcome to my Task API!"}


# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# Get one task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return {"message": "Task not found!"}


# Create a task
@app.post("/tasks")
def create_task(task: dict):
    tasks.append(task)
    return {
        "message": "Task added successfully!",
        "task": task
    }


# Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: dict):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task["title"]
            task["completed"] = updated_task["completed"]
            return {
                "message": "Task updated successfully!",
                "task": task
            }
    return {"message": "Task not found!"}


# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {
                "message": "Task deleted successfully!"
            }
    return {"message": "Task not found!"}