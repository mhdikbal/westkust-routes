---
name: verify
description: Project verify skill for westkust-routes — how to drive the running app (Django+FastAPI+Leaflet, docker compose) and capture real evidence before marking a change done.
---

# Verify — westkust-routes

This repo has no automated browser-test harness. Verification means driving
the actual running stack (already up via `docker compose up -d`) with a real
headless browser and capturing what happens — not re-running pytest/Django
tests (that's CI's job, covered separately by CLAUDE.md's TDD workflow).

## Stack is already running locally

```
docker compose up -d          # nginx :8084 -> frontend (Django) + backend (FastAPI)
curl http://localhost:8084/   # should be 200
```

Backend/frontend containers have **no bind mount** — after editing source,
you MUST `docker compose up -d --build <service>` before changes are live
(a `docker compose exec ... python ...` against a stale container will look
like a bug that isn't one).

## Driving the browser (Playwright, cold-started 2026-07-07)

`npx playwright --version` works (npm package present), but the **installed
playwright version's expected Chromium revision does NOT match what's cached**
in `~/.cache/ms-playwright/`. `chromium.launch()` with no args fails with
"Executable doesn't exist at .../chromium_headless_shell-<newer-rev>/...".

Fix: point `executablePath` at whatever revision IS actually cached instead
of letting Playwright pick:

```bash
ls ~/.cache/ms-playwright/          # find the actual cached chromium-<rev> dir
```

```js
import { chromium } from 'playwright';
const browser = await chromium.launch({
  executablePath: '/home/naro/.cache/ms-playwright/chromium-<rev>/chrome-linux64/chrome',
  args: ['--no-sandbox'],
});
```

Run scripts as standalone `.mjs`/`.js` files (not `node -e` heredoc-style for
anything beyond a few lines — same "silent traceback swallowing" trap as bash
heredocs, per `feedback_visual_verification.md` memory). `npm install
playwright` once per scratchpad dir if `node_modules` isn't already there.

## Viewports that matter

- Desktop: `1440x900`
- Mobile: `390x844` — **the app hides `.nav-center` entirely below
  `max-width:768px`** (year slider, stats badge, direction toggle, source
  toggle — anything added to that container). This is existing, deliberate
  behavior, not a bug to fix on sight — but always check new navbar controls
  against it so you don't mistake "hidden by design" for "broken."

## What's worth checking on a map/navbar change

1. Screenshot both viewports before touching anything (baseline).
2. Click the new control, capture the **network request** it fires (`page.on('request', ...)`
   filtered to the relevant `/api/...` path) — confirms the query param actually
   reaches the backend, not just that the button visually toggles.
3. Check `aria-pressed` flips correctly across the whole button group, not just
   the one you clicked.
4. Exercise the **empty-result** case deliberately (e.g. filter to a value with
   zero matching rows) — confirm the map clears cleanly (stats badge shows 0,
   no leftover stale lines, no console error) rather than assuming the happy
   path generalizes.
5. `page.on('pageerror', ...)` and `page.on('console', msg => msg.type()==='error')`
   — capture both. A pre-existing missing-favicon 404 is normal noise here;
   don't let it block a PASS, but don't silently swallow other errors either.

## Screenshot output

Save to the session scratchpad
(`/tmp/claude-*/*/scratchpad/`), not the repo — these are throwaway evidence
for the current verification pass, not project artifacts.
