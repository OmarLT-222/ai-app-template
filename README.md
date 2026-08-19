# ai-app-template

A **Python + FastAPI + uv** starter template with a `.claude/` layer that turns Claude Code into a productive pair-programmer for this stack.

The template is for apps you **build with Claude Code's help**. Clone it, describe your idea, and let Claude scaffold the rest.

---

## Quick start

### 1. Get the code

```bash
git clone <this-repo> my-new-app
cd my-new-app
```

### 2. Set up the environment

```bash
uv sync
```

That single command creates `.venv/` in the project root, installs everything from `uv.lock`, and downloads a matching Python interpreter if you don't already have one. **You never activate the venv** — every command goes through `uv run`, which auto-selects it.

### 3. (Optional) Sanity-check the baseline

```bash
uv run pytest -q                          # should pass (3 tests)
uv run uvicorn app.main:app --reload      # http://127.0.0.1:8000/health
```

Ctrl-C to stop the server.

### 4. Configure env vars

```bash
cp .env.example .env
```

Nothing to change yet — defaults use local SQLite.

### 5. Drive the build in Claude Code

```
/new-app       # answers questions, writes SPEC.md — review before continuing
/plan-app      # writes PLAN.md — review before continuing
/build-app     # deletes Item samples, scaffolds your models/routes/tests,
                # runs pytest, boots the server, hits /health
```

Each command's output is yours to edit before running the next one. That's the intended iteration loop.

### 6. From there

- Add features: `/add-feature "let posts have tags"`
- Add UI: `/add-frontend`
- Package for deploy: `/dockerize`
- Sanity check after manual edits: `/verify`

### About the venv, explicitly

- **No** to `python -m venv`
- **No** to `source .venv/bin/activate`
- **No** to `pip install`
- **Yes** to `uv sync` once after cloning, then `uv run <anything>` for the rest of the project's life

`.venv/` exists on disk (visible after `uv sync`) — it's just managed for you and gitignored.

---

## What ships

**Baseline scaffold** (`src/app/`)
- FastAPI app with `/health` and a sample `Item` CRUD (deleted by `/build-app` unless the spec keeps it)
- SQLAlchemy 2.0 + SQLite, schema via `Base.metadata.create_all()` on startup
- `pydantic-settings` for config (`.env`-driven)
- pytest with an in-memory SQLite `client` fixture in `tests/conftest.py`

**`.claude/` layer**
- 7 slash commands for the build lifecycle
- 4 skills auto-loaded when relevant
- 4 subagents for interview, planning, review, and test-writing
- Permissions pre-allowlisted for common `uv` and read-only git commands

---

## Layout

```
.
├── .claude/
│   ├── commands/          slash commands (/new-app, /plan-app, ...)
│   ├── skills/            auto-loaded when descriptions match
│   ├── agents/            subagents delegated by commands
│   └── settings.json      pre-allowed permissions
├── src/app/
│   ├── main.py            FastAPI app + router wiring
│   ├── config.py          pydantic-settings, loads .env
│   ├── db.py              SQLAlchemy engine + Base + init_db()
│   ├── deps.py            DI helpers (get_db)
│   ├── models/            one file per model
│   └── routes/            one file per resource
├── tests/
│   ├── conftest.py        `client` fixture with in-memory SQLite
│   └── test_*.py
├── CLAUDE.md              conventions Claude follows in this repo
├── pyproject.toml         uv-managed dependencies
├── .env.example
└── .gitignore
```

---

## Slash commands

| Command | What it does |
|---|---|
| `/new-app` | Delegates to `spec-writer` to interview you and produce `SPEC.md` |
| `/plan-app` | Delegates to `architect` to turn `SPEC.md` into a file-by-file `PLAN.md` |
| `/build-app` | Executes `PLAN.md` — deletes samples, scaffolds files, runs tests, boots the server |
| `/add-feature <desc>` | Adds an incremental feature; updates `SPEC.md` and writes a scoped plan to `docs/features/<slug>.md` |
| `/add-frontend` | Bolts on React+Vite, HTMX+Jinja2, or plain HTML/JS |
| `/dockerize` | Generates a multi-stage Dockerfile, `.dockerignore`, and optional `docker-compose.yml` (SQLite volume or Postgres service) |
| `/verify` | Runs tests, boots the server, hits `/health`, reports status |

The intended flow for a new app is `/new-app` → `/plan-app` → `/build-app`. Each command reads what the previous one wrote, so you can iterate on the spec or plan without re-running the whole chain.

---

## Skills

Auto-loaded when their descriptions match the current task. You don't invoke them directly.

| Skill | Loaded when |
|---|---|
| `fastapi-patterns` | Writing routes, debugging request/response issues |
| `sqlalchemy-patterns` | Adding models, working with the DB |
| `uv-workflow` | Adding/removing dependencies, running commands |
| `pytest-patterns` | Writing or fixing tests |

---

## Subagents

Invoked by slash commands, but you can also call them directly with `Task`/`Agent`.

| Subagent | Purpose |
|---|---|
| `spec-writer` | Interviews you, produces `SPEC.md` |
| `architect` | Reads `SPEC.md`, produces `PLAN.md` |
| `refactor-reviewer` | Post-implementation review — duplication, convention drift, over-engineering |
| `test-writer` | Writes pytest tests for existing routes |

---

## Conventions (enforced by `CLAUDE.md`)

- **Routes**: one router per resource file, `response_model` on every endpoint, sync `def` unless real async I/O is needed
- **Models**: one SQLAlchemy model per file, SQLAlchemy 2.0 typed style (`Mapped[T]` + `mapped_column()`), plural snake_case tablenames
- **Tests**: every endpoint has at least a success test, uses the `client` fixture, never mocks the DB
- **Package manager**: `uv add` / `uv remove` / `uv run` — never `pip`, never bare `python`
- **Commits**: Claude commits only when you ask

Full details in [`CLAUDE.md`](./CLAUDE.md).

---

## Manual usage (no Claude)

The scaffold is a normal FastAPI project:

```bash
uv sync
uv run uvicorn app.main:app --reload    # dev server
uv run pytest -q                         # tests
uv add <package>                         # add a runtime dep
uv add --dev <package>                   # add a dev dep
```

`.env` is loaded automatically by `pydantic-settings`; start with `cp .env.example .env`.

---

## Adding Alembic (when you outgrow `create_all`)

The template uses `Base.metadata.create_all()` on startup, which is fine for greenfield. When the schema starts changing with real data to preserve:

```bash
uv add alembic
uv run alembic init alembic
```

Configure `alembic/env.py` to import `Base` from `app.db`, then generate revisions with `uv run alembic revision --autogenerate -m "..."`. Remove the `init_db()` call from the `lifespan` in `main.py` once migrations own the schema.

---

## Customizing the template

- **Change conventions**: edit `CLAUDE.md` — it's the source of truth Claude reads.
- **Add a skill**: create `.claude/skills/<name>/SKILL.md` with `name` and `description` frontmatter. Auto-loads when the description matches.
- **Add a command**: create `.claude/commands/<name>.md`. Available as `/<name>`.
- **Add a subagent**: create `.claude/agents/<name>.md` with `name`, `description`, and `tools` frontmatter.
- **Loosen or tighten permissions**: edit `.claude/settings.json`.
