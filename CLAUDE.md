# CLAUDE.md

Guidance for Claude Code when working in this repo.

## Stack
- Python 3.11+
- FastAPI (sync routes by default)
- uv (package manager)
- SQLAlchemy 2.0 + SQLite (dev); swap to Postgres when the app needs it
- pytest with in-memory SQLite

## Layout
```
src/app/
├── main.py       FastAPI app + router wiring
├── config.py     pydantic-settings, loads .env
├── db.py         SQLAlchemy engine + Base + init_db()
├── deps.py       DI helpers (get_db)
├── models/       one file per model, imported in __init__.py
└── routes/       one file per resource
tests/
├── conftest.py   `client` fixture with in-memory SQLite
└── test_*.py
```

## Conventions

**Routes**
- One router per resource file. `router = APIRouter(prefix="/<resource>", tags=["<resource>"])`.
- Every route has `response_model=<PydanticModel>`.
- Sync `def`, not `async def`, unless the route awaits real async I/O.
- Errors: `raise HTTPException(status_code, detail)`.

**Models**
- One SQLAlchemy model per file. Import into `models/__init__.py` so `Base.metadata` sees it.
- Use SQLAlchemy 2.0 typed style: `Mapped[T]` + `mapped_column()`.
- `__tablename__` is plural snake_case (`items`, `blog_posts`).

**Tests**
- Every endpoint has at least a success test and one per explicit error case.
- Use the `client` fixture — never mock the DB.
- `uv run pytest -q` must pass before marking a task done.

**Package manager**
- Always use `uv add` / `uv remove` / `uv run`. Never `pip`, never bare `python`.

**Commits**
- Only when the user asks.

## Slash commands
- `/new-app` — interview to produce `SPEC.md`
- `/plan-app` — turn `SPEC.md` into `PLAN.md`
- `/build-app` — execute `PLAN.md`, scaffold the app
- `/add-feature <desc>` — add a feature to an existing app
- `/add-frontend` — bolt on a React/HTMX/plain frontend
- `/dockerize` — generate Dockerfile, .dockerignore, optional docker-compose.yml
- `/verify` — run tests + boot the app + hit `/health`

## Skills (loaded on relevance)
- `fastapi-patterns`, `sqlalchemy-patterns`, `uv-workflow`, `pytest-patterns`

## Subagents
- `spec-writer` — interviews for `SPEC.md`
- `architect` — writes `PLAN.md`
- `refactor-reviewer` — post-implementation review
- `test-writer` — writes tests for existing routes

## Sample code
`src/app/models/item.py`, `src/app/routes/items.py`, and `tests/test_items.py` are placeholders showing the pattern. `/build-app` deletes them unless the actual app happens to want an Item entity.
