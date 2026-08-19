---
description: Interview the user to define a new app. Produces SPEC.md at the repo root.
---

You are starting a new app from this template. Interview the user and produce `SPEC.md`.

Delegate the interview to the `spec-writer` subagent. Pass it this instruction:

> Interview the user about a new app they want to build on this template (Python + FastAPI + uv + SQLAlchemy + SQLite). Ask 2-3 questions per batch using `AskUserQuestion`. Cover: one-liner, entities and their fields, endpoints (verb + path + purpose), frontend (skip / React+Vite / HTMX / plain), auth (none / session / JWT), integrations, persistence (SQLite unless there's a real reason for Postgres), extras (background jobs, uploads, websockets). Push back on vague answers. Write `SPEC.md` at the repo root when done, including an "Open questions" section.

After `spec-writer` returns, read `SPEC.md`, print its Summary and Endpoints sections back to the user for confirmation, and tell them: "Review `SPEC.md`. When ready, run `/plan-app`."
