---
description: Turn SPEC.md into a file-by-file implementation plan (PLAN.md).
---

Read `SPEC.md`. If it does not exist, tell the user to run `/new-app` first and stop.

Delegate to the `architect` subagent. Pass it the full spec contents and this instruction:

> Read `SPEC.md` and `CLAUDE.md`. Produce `PLAN.md` at the repo root. For each file to create or modify, list: path, purpose, key symbols (functions, classes, routes), and its dependencies on other files in the plan. Order the file list so earlier items unblock later ones (models → routes → main.py wiring → tests). Include a "Cleanup" section listing sample files to delete (typically `src/app/models/item.py`, `src/app/routes/items.py`, `tests/test_items.py` — unless the spec keeps an Item entity). If the spec is missing critical information, list the gaps under "Blocking questions" at the top and stop.

After `architect` returns, print the file list back to the user and tell them: "Review `PLAN.md`. When ready, run `/build-app`."
