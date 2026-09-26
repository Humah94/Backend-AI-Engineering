from fastapi import FastAPI, HTTPException, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

import repository

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid request body"}
    )


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    completed: bool = False


@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return repository.get_all_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = repository.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    return repository.create_task(task.title, task.completed)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    updated_task = repository.update_task(
        task_id,
        task.title,
        task.completed
    )

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = repository.delete_task(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return Response(status_code=204)