# Task API

A simple CRUD API for managing tasks, built with Python, FastAPI, PostgreSQL, and Docker.

## Run the API

The application can be run locally or with Docker Compose.

### Run with Docker Compose

Start both the FastAPI application and PostgreSQL database with:

```powershell
docker compose up -d
```

Check the running containers with:

```powershell
docker compose ps
```

The API will run at:

```text
http://127.0.0.1:8001
```

Swagger UI is available at:

```text
http://127.0.0.1:8001/docs
```

To stop the containers:

```powershell
docker compose down
```

The PostgreSQL data is stored in a Docker named volume, so the data survives a normal container restart or `docker compose down`.

> Do not use `docker compose down -v` unless you intentionally want to delete the PostgreSQL volume and database data.

## Endpoints

| Method | Endpoint           | Description     |
| ------ | ------------------ | --------------- |
| GET    | `/`                | Welcome message |
| GET    | `/health`          | Health check    |
| GET    | `/tasks`           | List all tasks  |
| POST   | `/tasks`           | Create a task   |
| GET    | `/tasks/{task_id}` | Get one task    |
| PUT    | `/tasks/{task_id}` | Update a task   |
| DELETE | `/tasks/{task_id}` | Delete a task   |

## Response Status Codes

* `200 OK` — Successful GET and PUT requests
* `201 Created` — Task successfully created
* `204 No Content` — Task successfully deleted
* `400 Bad Request` — Invalid or missing task title
* `404 Not Found` — Task ID does not exist

## Database

The application uses PostgreSQL for persistent task storage.

PostgreSQL runs in Docker using the official `postgres:16` image.

The database uses a Docker named volume:

```text
postgres_data
```

This volume keeps the database data available when the containers are restarted.

The database table is created by:

```text
postgres/init.sql
```

The initialization script creates the `tasks` table and provides the three starter tasks for a fresh database.

## Repository Layer

The PostgreSQL database operations are separated into:

```text
repository.py
```

The repository handles:

* Reading all tasks
* Reading a task by ID
* Creating tasks
* Updating tasks
* Deleting tasks

The FastAPI routes in `main.py` call the repository instead of directly executing SQL.

## Docker Architecture

The application uses two Docker services:

```text
FastAPI application
        |
        v
   repository.py
        |
        v
PostgreSQL database
        |
        v
  Docker volume
```

The services are defined in:

```text
docker-compose.yml
```

The FastAPI container connects to PostgreSQL using the Docker service name:

```text
db
```

The database connection used inside Docker is:

```text
postgresql://postgres:postgres@db:5432/tasks
```

## Environment Variables

The local database connection is stored in `.env`.

Example:

```text
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tasks
```

The real `.env` file is ignored by Git and is not committed to the repository.

A safe template is provided in:

```text
.env.example
```

## A3 — Containerize the Stack

For A3, the original SQLite storage was replaced with PostgreSQL running in Docker.

The project was updated to include:

* PostgreSQL 16
* Docker Compose
* A PostgreSQL repository layer
* A Dockerfile for the FastAPI application
* Environment-based database configuration
* A PostgreSQL initialization script
* A persistent Docker volume

### A3 Dockerfile

The FastAPI application is packaged using:

```text
Dockerfile
```

The Docker image installs the dependencies from:

```text
requirements.txt
```

and starts the application with Uvicorn on port `8001`.

### A3 Docker Compose

The `docker-compose.yml` file starts:

```text
backend_ai_app
backend_ai_postgres
```

The PostgreSQL service has a health check so the FastAPI service waits for the database to become healthy.

### Persistence Test

To verify database persistence:

1. A new task was created through the FastAPI Swagger UI.
2. The task was stored in PostgreSQL.
3. Both Docker containers were restarted with:

```powershell
docker compose restart
```

4. The API was tested again.
5. The previously created task was still present.

This confirmed that the PostgreSQL data persisted through a container restart.

## Project Structure

```text
Backend-AI-Engineering/
├── main.py
├── repository.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── postgres/
│   └── init.sql
├── tasks.db
├── README.md
├── swagger.png
├── database.png
├── .env.example
└── .gitignore
```

## Swagger UI

![Swagger UI](swagger.png)

## Previous SQLite Database Viewer

The SQLite database from the earlier database assignment was inspected using DB Browser for SQLite.

![Database Viewer](database.png)

## curl -i Example

```text
HTTP/1.1 200 OK
date: Sun, 20 Sep 2026 22:31:55 GMT
server: uvicorn
content-length: 15
content-type: application/json

{"status":"ok"}
```

## AI vs Me

### My original version vs. AI version

I first built the Task API myself, then gave an AI assistant my own prompt to build the same API. I tested the AI-generated version before comparing it with my version.

#### Difference 1: Endpoints

My version includes `/` and `/health` in addition to the five CRUD endpoints. The AI version only included the five CRUD endpoints because my Stage 7 prompt did not mention `/` or `/health`.

#### Difference 2: Task structure

My version uses a `completed` boolean field and starts with three sample tasks. The first AI version used a `done` field and started with an empty task list. My prompt did not specify the exact field name or initial tasks, so the AI made those decisions itself.

#### Difference 3: Validation

My version includes a custom validation handler so invalid request bodies return `400`. The first AI version correctly returned `400` for an empty title, but a missing title would use FastAPI's default `422` validation response. My prompt was not specific enough about how missing-title validation should be handled.

### What AI did better

The AI version used a separate `next_id` counter to assign task IDs. I understand that this keeps track of the next ID and increases it after each new task. This is more reliable when tasks are deleted.

### What AI got wrong or ignored

The first AI version did not fully handle a missing title as a `400` error. FastAPI would return `422` for that case, which did not match my requirement.

### What my prompt forgot

My original prompt did not specify the exact task fields, initial sample tasks, `/` and `/health` endpoints, or the exact JSON error format. The AI made its own decisions for those details.

### One rematch

I improved my prompt by explicitly specifying the task fields, three starting tasks, a separate `next_id` counter, and `400` handling for both missing and empty titles.

The improved prompt produced a version that matched these requirements more closely.
