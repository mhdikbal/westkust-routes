# Production Research Page — SEC-3A Real-Django Test Plan

> **Phase:** SEC-3A closure item 1 of 2 — targeted retest of `SEC3-F-01` only.
> **Baselines:** parent `e813192b590917a7f96b9e3ca7da5c8c9a907be8`, SEC-2 `38120d250a2b629e86a6c66d0d4be7d0851117b5`, SEC-2A `1838815fb3314dc9528f3cf4b29f5761c0835b0a`, SEC-3 `7c0621d512c8574df7b9ca041577a1080ac7e618`

---

## 1. Finding Under Test

```text
SEC3-F-01: OPEN_REQUIRES_REAL_DJANGO_REVERIFICATION
```

SEC-3's rehearsal used a synthetic, always-200 dummy backend to model the two protected-page-serving routes. Duplicated-prefix paths (`/atlas/atlas/...`, `/westkust/westkust/...`) returned `200` from that dummy fallback, with no data leak but no confirmation of real Django's own behavior. This document closes that gap.

## 2. Source-Faithful Test Method Selected

```text
D1: reuse the actual built Django application image, disposable network, no production data or secrets
```

`westkust-routes-frontend:latest` — the same image the real production `voc_frontend` container runs — was already built and present locally. Inspection of `frontend/config/settings.py` confirmed the app has **no database dependency** (`DATABASES` is not configured; the app is a thin SSR layer over the FastAPI backend via `httpx`), and `frontend/map_app/views.py` was read and confirmed to catch backend-unreachable exceptions and render a degraded-but-real page (`backend_error = True`) rather than crash. This makes D1 fully viable without any production DB, Redis, `.env`, or secret: the container was started with only `DJANGO_SECRET_KEY` (a freshly generated ephemeral value, never printed or reused), `ALLOWED_HOSTS=*`, `DEBUG=False`, and `API_BASE_URL` pointed at a nonexistent hostname (`sec3a_no_such_backend:9999`) so the backend-dependent views exercise their real degraded-mode code path rather than a live, data-bearing one.

This is source-faithful for the question `SEC3-F-01` asks — URL resolution, `APPEND_SLASH`, redirect `Location` header generation, and 404 behavior on unrecognized paths are all Django-core / URLconf behavior, entirely independent of whether the backend API call inside a specific view succeeds. It is not source-faithful for the *content* of `/riset/pemodelan/`'s Bokeh dashboard fragment (which requires a live backend) — that content was not the subject of `SEC3-F-01` and is not claimed to be validated here.

## 3. Topology

```text
test client
  -> disposable outer Nginx (sec3a_outer, models silida.conf's /atlas/ and
     /westkust/ nested-location structure, incl. proxy_redirect + sub_filter)
  -> disposable inner Nginx (sec3a_inner, loopback-published, models
     voc_nginx's protected-location structure)
  -> sec3a_django (the REAL westkust-routes-frontend:latest image)
```

Research APIs (`/api/research/linimasa`, `/api/research/pemodelan-dashboard`) are **not** part of this Django app in production (they are FastAPI `backend` routes, proxied directly by `voc_nginx`) and were modeled with the same synthetic-response approach already validated in SEC-2A/SEC-3 — consistent with the Phase 3 instruction to use synthetic responses only where database-backed content is required, and not as a substitute for the Django-specific question this document exists to answer.

## 4. Tests

Twenty tests, `SEC3A-DJ-001` through `SEC3A-DJ-020` — full detail and results in `PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_DJANGO_TEST_RESULTS.csv`.

## 5. Closure Rule

```text
SEC3-F-01 -> TARGETED_MITIGATION_VALIDATED
```

only if all 20 tests PASS, including the duplicated-prefix tests against the real Django runtime, with no protected-content leakage, no redirect loop, and no authentication bypass. The two original SEC-3 `PASS_WITH_LIMITATION` rows (`SEC3-PREC-006`, `SEC3-PREC-007`) are **not rewritten** — they are annotated `SUPERSEDED_BY_SEC3A_DJANGO_RETEST` in the SEC-3 audit only, per instruction.

## 6. Result

All 20 tests passed. See `PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_DJANGO_TEST_RESULTS.csv` and `PRODUCTION_RESEARCH_PAGE_SEC3A_AUDIT.md` §2 for the full evidence, including the key finding: the real Django application's own 404 handler (not a synthetic fallback) is what actually rejects the duplicated-prefix path, and it contains no protected content — a materially stronger result than SEC-3's synthetic-backend test could produce.

```text
SEC3-F-01: TARGETED_MITIGATION_VALIDATED
```
