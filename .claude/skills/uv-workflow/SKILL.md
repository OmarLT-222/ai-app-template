---
name: uv-workflow
description: uv package manager workflow for this template — add/remove dependencies, run commands, virtual env, lock file. Load when adding libraries or when a `python`/`pip` command feels like the wrong tool.
---

# uv workflow

## Never use pip or bare python
This project uses uv. Do not run `pip install`, `python -m venv`, or `python script.py` directly. Every command that needs the project environment goes through `uv run`.

## Add / remove dependencies
- Runtime: `uv add <pkg>`
- Dev only: `uv add --dev <pkg>`
- Remove: `uv remove <pkg>`
- Pinned version: `uv add "fastapi>=0.115"`

`uv add` writes to `pyproject.toml` and updates `uv.lock` automatically.

## Run things
- Any command in the project env: `uv run <cmd>`
  - Tests: `uv run pytest -q`
  - Dev server: `uv run uvicorn app.main:app --reload`
  - One-off script: `uv run python scripts/foo.py`

## Sync
- `uv sync` — install everything from `uv.lock` into `.venv`. Run after cloning or after pulling changes that touched `pyproject.toml` / `uv.lock`.
- `uv lock` — regenerate the lock file from `pyproject.toml`.

## Virtual env
- uv manages `.venv/` at the project root. Don't create it manually.
- Activating is optional — `uv run` handles env selection.
