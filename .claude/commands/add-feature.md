---
description: Add a feature to an existing app. Updates SPEC, plans, and implements.
argument-hint: [short feature description]
---

You are adding a feature to an existing app.

If `$ARGUMENTS` is non-empty, treat it as the feature description. Otherwise, ask the user for a short description.

## Steps

1. Read `SPEC.md` for current state. If it doesn't exist, tell the user `/new-app` is the way to start a fresh app; for ad-hoc features, proceed but note the spec is missing.
2. Read relevant files under `src/app/` and `tests/` to understand what's there.
3. Ask 1-3 targeted clarifying questions using `AskUserQuestion` if the feature is ambiguous.
4. Append the new entities / endpoints / notes to `SPEC.md` under a `## Feature: <slug>` section.
5. Delegate a scoped plan to `architect`. Do not overwrite `PLAN.md` — write the plan to `docs/features/<slug>.md`.
6. Implement, following `CLAUDE.md` conventions.
7. Add tests using the `client` fixture. Run `uv run pytest -q`.
8. Report what changed with file:line references.
