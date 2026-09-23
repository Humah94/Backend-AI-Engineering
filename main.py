from fastapi import FastAPI, HTTPException, Response
import sqlite3
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    completed BOOLEAN NOT NULL
)
""")

conn.commit()
cursor.execute("SELECT COUNT(*) FROM tasks")

if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO tasks (id, title, completed) VALUES (?, ?, ?)",
        [
            (1, "Learn FastAPI", False),
            (2, "Build my first API", False),
            (3, "Practice Python", False),
        ]
    )

    conn.commit()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid request body"}
    )
class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    completed: bool = False
tasks = [
    {"id": 1, "title": "Learn FastAPI", "completed": False},
    {"id": 2, "title": "Build my first API", "completed": False},
    {"id": 3, "title": "Practice Python", "completed": False},
]

@app.get("/")
def home():
    return {"message": "Hello, World!"}
@app.get("/health")
def health():
    return {"status": "ok"}
@app.get("/tasks")
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, completed FROM tasks")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "completed": bool(row[2])
        }
        for row in rows
    ]
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, completed FROM tasks WHERE id = ?",
        (task_id,)
    )
    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": row[0],
        "title": row[1],
        "completed": bool(row[2])
    }
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, completed) VALUES (?, ?)",
        (task.title, task.completed)
    )

    new_id = cursor.lastrowid
    conn.commit()

    cursor.execute(
        "SELECT id, title, completed FROM tasks WHERE id = ?",
        (new_id,)
    )
    row = cursor.fetchone()

    conn.close()

    return {
        "id": row[0],
        "title": row[1],
        "completed": bool(row[2])
    }
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    )
    existing_task = cursor.fetchone()

    if existing_task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "UPDATE tasks SET title = ?, completed = ? WHERE id = ?",
        (task.title, task.completed, task_id)
    )

    conn.commit()

    cursor.execute(
        "SELECT id, title, completed FROM tasks WHERE id = ?",
        (task_id,)
    )
    row = cursor.fetchone()

    conn.close()

    return {
        "id": row[0],
        "title": row[1],
        "completed": bool(row[2])
    }
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    )
    existing_task = cursor.fetchone()

    if existing_task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return Response(status_code=204)