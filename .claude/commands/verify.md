---
description: Run tests, boot the server, hit /health. Confirms the app is in a working state.
---

## Steps

1. Run `uv run pytest -q`. Report pass/fail count.
2. If tests pass, start the server in the background:
   ```
   uv run uvicorn app.main:app --port 8000
   ```
3. Wait briefly for boot, then `curl http://127.0.0.1:8000/health`.
4. Stop the server.
5. Summarize: test outcome, boot status, health response body.

If any step fails, stop and report the failure with the error output — do not attempt fixes unless asked.
