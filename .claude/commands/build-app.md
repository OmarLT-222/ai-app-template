---
description: Execute PLAN.md — scaffold the app, run tests, boot the server.
---

Read `PLAN.md`. If it does not exist, tell the user to run `/plan-app` first and stop. If it contains "Blocking questions", relay them to the user and stop.

## Steps

1. Create one task per file in the plan with `TaskCreate`. Also create tasks for: "Add dependencies", "Delete sample files", "Run tests", "Verify boot".
2. **Add dependencies**: run `uv add <pkg>` for each package under "Dependencies to add" in the plan.
3. **Delete sample files** listed under "Cleanup" (typically `src/app/models/item.py`, `src/app/routes/items.py`, `tests/test_items.py`). Also remove the corresponding import from `src/app/models/__init__.py` and the `items` router include in `src/app/main.py`.
4. **Create / modify files** in the order given in the plan. Mark each task complete as you go. Follow every convention in `CLAUDE.md` and the relevant skills (`fastapi-patterns`, `sqlalchemy-patterns`, `pytest-patterns`).
5. **Tests**: run `uv run pytest -q`. Fix any failures before moving on.
6. **Verify boot**: start the server in the background with `uv run uvicorn app.main:app --port 8000`, wait briefly, `curl http://127.0.0.1:8000/health`, stop the server.
7. **Report**: what was built, tests passing, any followups from `PLAN.md`.

After building, offer to run `/add-frontend` if the spec called for one.
