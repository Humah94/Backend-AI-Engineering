CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO tasks (title, completed)
SELECT 'Learn FastAPI', FALSE
WHERE NOT EXISTS (SELECT 1 FROM tasks);

INSERT INTO tasks (title, completed)
SELECT 'Build my first API', FALSE
WHERE NOT EXISTS (SELECT 1 FROM tasks);

INSERT INTO tasks (title, completed)
SELECT 'Practice Python', FALSE
WHERE NOT EXISTS (SELECT 1 FROM tasks);