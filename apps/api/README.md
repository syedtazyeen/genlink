# genlink-api

**`genlink-api`** is the backend API for the **genink project**, built with **FastAPI** and **Poetry** for dependency management.

## Development Setup

#### 1. Save your `.env` file

#### 2. Install dependencies

```bash
poetry install
```

> Poetry will handle creating the virtual environment and installing the dependencies.

#### 3. Running FastAPI Locally

```bash
poetry shell
uvicorn app.main:app --reload
```

> The API will be available at `http://localhost:8000`.
