---
description: Add a frontend layer (React+Vite, HTMX, or plain HTML/JS) to the app.
---

Ask which frontend flavor the user wants using `AskUserQuestion`:

- **React + Vite + TypeScript** — SPA in `frontend/`, dev-serves on :5173, calls the FastAPI backend
- **HTMX + Jinja2** — server-rendered templates in `templates/`, tighter FastAPI integration
- **Plain HTML/JS** — a single `static/index.html` served by FastAPI

## Steps by choice

**React + Vite:**
1. Run `npm create vite@latest frontend -- --template react-ts` (confirm with the user before installing).
2. Add CORS middleware to `src/app/main.py`:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])
   ```
3. Update `README.md` with dev instructions: backend on `:8000`, frontend on `:5173`.

**HTMX + Jinja2:**
1. `uv add jinja2`
2. Create `templates/index.html` (loads HTMX from a CDN) and `static/` for assets.
3. In `src/app/main.py`, mount static and configure templates:
   ```python
   from fastapi.staticfiles import StaticFiles
   from fastapi.templating import Jinja2Templates
   app.mount("/static", StaticFiles(directory="static"), name="static")
   templates = Jinja2Templates(directory="templates")
   ```
4. Add an index route that renders `templates/index.html`.

**Plain HTML/JS:**
1. Create `static/index.html` with `fetch` calls to the API.
2. In `src/app/main.py`, `app.mount("/", StaticFiles(directory="static", html=True), name="static")` (mount **after** all API routers).

## After
Update `SPEC.md` with a `## Frontend` section noting the choice. Report to the user how to run both processes.
