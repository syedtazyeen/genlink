FROM python:3.11-slim

ENV POETRY_VERSION=1.8.2
ENV PATH="/root/.local/bin:$PATH"

# System deps
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml ./

# Install deps (only main by default)
RUN poetry install --no-root --only main

# Copy source
COPY . .

# Reinstall main deps cleanly
RUN poetry install --no-root --only main --no-interaction --no-ansi

EXPOSE 8080
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]