---
name: fastapi-patterns
description: FastAPI conventions used in this template — router layout, dependency injection, response models, error handling. Load when writing routes or debugging request/response issues.
---

# FastAPI patterns

## Router layout
- One file per resource in `src/app/routes/<resource>.py`.
- Each file exposes `router = APIRouter(prefix="/<resource>", tags=["<resource>"])`.
- Register in `src/app/main.py`: `app.include_router(<resource>.router)`.

## Dependency injection
- DB session: `db: Session = Depends(get_db)` — `get_db` lives in `app/deps.py`.
- Config: import the module-level `settings` from `app.config`. Don't call `Settings()` again.
- Shared logic (auth, pagination, etc.): create a dependency function returning the value, use with `Depends(...)`.

## Request / response models
- Every route has `response_model=<PydanticModel>`.
- Request bodies: Pydantic model named `<Resource>In`.
- Responses: `<Resource>Out`. For ORM → Pydantic conversion, add `model_config = {"from_attributes": True}`.
- Lists: `response_model=list[<Resource>Out]`.

## Errors
- Raise `HTTPException(status_code, detail)` for user-facing errors.
- Don't catch and re-raise generic exceptions — let FastAPI surface them in dev.
- 404 for missing resources, 422 comes free from Pydantic, 401/403 for auth.

## Async vs sync
- Default to sync (`def`, not `async def`). FastAPI runs sync routes in a threadpool.
- SQLAlchemy 2.0 sync sessions are fine for sync routes.
- Only use `async def` when the route awaits real async I/O (aiohttp, an async DB driver, `asyncio.sleep`).

## Startup / shutdown
- Use the `lifespan` context manager (already wired in `main.py`), not deprecated `@app.on_event`.
