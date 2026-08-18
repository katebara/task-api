 ![CI](https://github.com/katebara/task-api/actions/workflows/ci.yml/badge.svg)
# Task Manager API

A small Flask REST API for managing tasks, built as a CI/CD practice
project. See [PIPELINE.md](./PIPELINE.md) for a full writeup of the
automated pipeline (lint → format check → tests) that runs on every push.

## Endpoints

| Method | Path          | Description       |
|--------|---------------|--------------------|
| GET    | `/health`     | Health check       |
| GET    | `/tasks`      | List all tasks     |
| POST   | `/tasks`      | Create a task      |
| GET    | `/tasks/<id>` | Get one task       |
| PUT    | `/tasks/<id>` | Update a task      |
| DELETE | `/tasks/<id>` | Delete a task      |

## Running Locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
python run.py
```

The API will be available at `http://127.0.0.1:5000`.

### Example requests

```bash
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn CI/CD"}'

curl http://127.0.0.1:5000/tasks
```

## Running Tests

```bash
pytest -v
```

## Linting & Formatting

```bash
flake8 app tests run.py
black app tests run.py       # auto-format
black --check app tests run.py   # check only, no changes (used in CI)
```

## Project Structure

```
task-api/
├── app/
│   ├── __init__.py     # Flask app factory
│   └── routes.py       # API endpoints
├── tests/
│   ├── conftest.py     # pytest fixtures
│   └── test_tasks.py   # test suite
├── .github/workflows/
│   └── ci.yml           # GitHub Actions pipeline
├── run.py               # entry point
├── requirements.txt
├── requirements-dev.txt
├── PIPELINE.md           # one-page pipeline writeup
└── README.md
```
