from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")


# Data model for creating/updating a task
class Task(BaseModel):
    title: str


# In-memory storage
tasks = []
next_id = 1


# 1. GET /tasks
# Returns all tasks currently stored in memory.
@app.get("/tasks")
def get_tasks():
    return tasks


# 2. GET /tasks/{task_id}
# Returns one task by its ID.
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# 3. POST /tasks
# Creates a new task and gives it the next available ID.
@app.post("/tasks", status_code=201)
def create_task(task: Task):
    global next_id

    # Check for an empty title
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    new_task = {
        "id": next_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)
    next_id += 1

    return new_task


# 4. PUT /tasks/{task_id}
# Updates the title of an existing task.
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    for existing_task in tasks:
        if existing_task["id"] == task_id:
            existing_task["title"] = task.title
            return existing_task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# 5. DELETE /tasks/{task_id}
# Deletes a task by its ID.
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )