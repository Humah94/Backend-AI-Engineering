import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)
def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, completed FROM tasks ORDER BY id"
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "completed": row[2]
        }
        for row in rows
    ]
def get_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, completed FROM tasks WHERE id = %s",
        (task_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }
def create_task(title, completed):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, completed)
        VALUES (%s, %s)
        RETURNING id, title, completed
        """,
        (title, completed)
    )

    row = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }
    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }
def update_task(task_id, title, completed):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = %s, completed = %s
        WHERE id = %s
        RETURNING id, title, completed
        """,
        (title, completed, task_id)
    )

    row = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "completed": row[2]
    }
def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    deleted = cursor.rowcount

    conn.commit()

    cursor.close()
    conn.close()

    return deleted > 0