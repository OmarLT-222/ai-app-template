---
name: pytest-patterns
description: Pytest conventions for this template — the client fixture, in-memory SQLite, naming, running. Load when writing or fixing tests.
---

# pytest patterns

## The `client` fixture
- Defined in `tests/conftest.py`. Provides a `TestClient` with an in-memory SQLite bound as the DB via `dependency_overrides`.
- Every route test should take `client` as its parameter.
- The DB is fresh per test — no cleanup needed.

## File layout
- One file per route module: `tests/test_<resource>.py`.
- One test function per behavior. Success path first, then each explicit error case.
- Names: `test_<verb>_<resource>_<scenario>`, e.g. `test_create_item_returns_201`, `test_get_missing_item_returns_404`.

## Writing a test
```python
def test_create_item_returns_201(client):
    r = client.post("/items", json={"name": "widget"})
    assert r.status_code == 201
    assert r.json()["name"] == "widget"
```

## Running
- All tests: `uv run pytest -q`
- One file: `uv run pytest tests/test_items.py -q`
- One test: `uv run pytest tests/test_items.py::test_create_item_returns_201 -q`
- Show print/log output: add `-s`

## Don't
- Don't mock the DB — the in-memory SQLite catches real ORM issues.
- Don't share state via module-level variables. Each test gets its own DB.
- Don't test framework behavior (that Pydantic validates required fields, that FastAPI routes work). Trust the framework, test your logic.
- Don't over-assert. If the assertion doesn't map to a real requirement, drop it.
