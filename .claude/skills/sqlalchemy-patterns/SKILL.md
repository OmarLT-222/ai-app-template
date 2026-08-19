---
name: sqlalchemy-patterns
description: SQLAlchemy 2.0 patterns for this template — session lifecycle, model conventions, common queries, when to add Alembic. Load when adding models or working with the DB.
---

# SQLAlchemy patterns

## Model conventions
- One model per file in `src/app/models/<name>.py`.
- Import each model into `src/app/models/__init__.py` so `Base.metadata` sees it before `create_all()`.
- Use SQLAlchemy 2.0 typed style:
  ```python
  from sqlalchemy import String
  from sqlalchemy.orm import Mapped, mapped_column
  from app.db import Base

  class Post(Base):
      __tablename__ = "posts"
      id: Mapped[int] = mapped_column(primary_key=True)
      title: Mapped[str] = mapped_column(String(200))
  ```
- `__tablename__` is plural snake_case: `items`, `blog_posts`.

## Sessions
- Use `Depends(get_db)` in routes. Never open a session outside DI in request-handling code.
- Sessions are per-request: create → use → commit or rollback → close.
- Reads don't need `commit()`. Writes do.
- After a write, call `db.refresh(obj)` if you need the DB-populated fields (autoincrement id, defaults).

## Common queries
- Fetch by primary key: `db.get(Model, id)` (returns `None` if missing).
- Filter (1.x-style, still supported): `db.query(Model).filter_by(field=value).all()` / `.first()`.
- Filter (2.0-style): `db.execute(select(Model).where(Model.field == value)).scalars().all()`.
- Count: `db.query(Model).count()`.

## Relationships
- Use `relationship()` with `Mapped[list[Child]]` on the parent, `Mapped["Parent"]` on the child.
- Foreign keys: `Mapped[int] = mapped_column(ForeignKey("parents.id"))`.

## Migrations
- The template uses `Base.metadata.create_all()` on startup — fine for early dev / greenfield.
- When the schema changes and there's real data to preserve, add Alembic:
  ```
  uv add alembic
  uv run alembic init alembic
  ```
  Configure `alembic/env.py` to import `Base` from `app.db`, then generate revisions with `uv run alembic revision --autogenerate -m "..."`. Remove the `init_db()` call from `lifespan` once migrations own the schema.

## Testing
- Tests use an in-memory SQLite via `conftest.py`. Never hit the real DB in tests, never mock the ORM.
