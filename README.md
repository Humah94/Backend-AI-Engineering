# Task API

A simple CRUD API for managing tasks, built with Python and FastAPI.

## Run the API

Start the server with:

```powershell
& "$env:LocalAppData\Programs\Python\Python313\python.exe" -m uvicorn main:app --reload


The API will run at `http://127.0.0.1:8000`.

Swagger UI is available at `http://127.0.0.1:8000/docs`.

## Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a task |
| GET | `/tasks/{task_id}` | Get one task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## curl -i Example

```text
HTTP/1.1 200 OK
date: Sun, 20 Sep 2026 22:31:55 GMT
server: uvicorn
content-length: 15
content-type: application/json

{"status":"ok"}


![Swagger UI](swagger.png)

## Project Structure

```text
## Project Structure

```text
Backend-AI-Engineering/
├── main.py
├── README.md
├── swagger.png
└── .gitignore

## Response Status Codes

- `200 OK` — Successful GET and PUT requests
- `201 Created` — Task successfully created
- `204 No Content` — Task successfully deleted
- `400 Bad Request` — Invalid or missing task title
- `404 Not Found` — Task ID does not exist