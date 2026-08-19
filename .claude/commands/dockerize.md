---
description: Generate a Dockerfile, .dockerignore, and optionally a docker-compose.yml tuned for this template's stack.
---

You are adding Docker support to an app built on this template.

## Interview

Use `AskUserQuestion` in one batch:

1. **Database in the container** — SQLite with a mounted volume / Postgres via docker-compose / no DB
2. **Compose file** — yes (dev-friendly with volume mounts + hot reload) / no (Dockerfile only)
3. **Python version** — 3.11 / 3.12 (default) / 3.13

Skip questions where the current `SPEC.md` already answers them.

## Preflight

- If `uv.lock` doesn't exist, run `uv lock` first — the Dockerfile depends on it for reproducible builds.
- If `Dockerfile` already exists, ask before overwriting.

## Generate

### `Dockerfile` (always)

Multi-stage build using Astral's official uv image:

```dockerfile
# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python<VERSION>-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Install deps first for layer caching — only rebuilt when pyproject/lock change
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy source and install the project itself
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---- Runtime stage ----
FROM python:<VERSION>-slim-bookworm

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Substitute `<VERSION>` with the chosen Python version.

### `.dockerignore` (always)

```
.venv
__pycache__
**/__pycache__
.git
.gitignore
.env
*.db
.pytest_cache
.ruff_cache
dist
build
*.egg-info
node_modules
frontend/node_modules
frontend/dist
docs
tests
```

Remove `tests` from the ignore list if the user wants to run tests inside the container.

### `docker-compose.yml` (if requested)

**SQLite + volume:**
```yaml
services:
  app:
    build: .
    ports: ["8000:8000"]
    volumes:
      - ./src:/app/src
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:////app/data/app.db
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Then create the `data/` directory and add `/data/` to `.gitignore`.

**Postgres:**
```yaml
services:
  app:
    build: .
    ports: ["8000:8000"]
    volumes:
      - ./src:/app/src
    environment:
      - DATABASE_URL=postgresql+psycopg://app:app@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=app
      - POSTGRES_PASSWORD=app
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

If Postgres is chosen, also `uv add "psycopg[binary]"` and note in the report that `src/app/db.py` will need the async/sync driver picked according to the SQLAlchemy URL.

**No DB:**
Same as SQLite version but drop the volume and environment lines.

## Post-generation

1. Update `.gitignore` to include `/data/` if SQLite volume was chosen.
2. Update `README.md` under a new `## Docker` section with the exact commands to build and run (`docker build -t app . && docker run -p 8000:8000 app`, or `docker compose up`).
3. Verify the build works: `docker build -t app-test .` (only if Docker is available — check with `command -v docker`). If it isn't, note it and skip.
4. Report: files created, how to run, any followups (e.g., "switch to Alembic before running with a mounted DB volume").
