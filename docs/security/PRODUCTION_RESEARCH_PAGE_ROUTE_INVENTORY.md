# Production Research Page — Route Inventory

> **Phase:** SEC-0 Discovery (read-only)
> **Baseline:** `51b0bd902ef7ee708f825e7aaa565f0e0c4fd7d8`
> **Plan:** `PLAN_PRODUCTION_RESEARCH_PAGE_ACCESS_CONTROL.md`
> **This document is inventory only — it authorizes no implementation, credential, or configuration change.**

---

## 1. Internal Application Routes (Django, root-relative)

Source: `frontend/config/urls.py` → `frontend/map_app/urls.py` (verbatim, verified against the actual `urlpatterns` list — not inferred from folder names).

| Path | View | SSR/backend call | Candidate class |
|---|---|---|---|
| `/` | `index` | none | Public |
| `/riset/tema/` | `riset_tema` | client-side fetch `/api/research/sankey-tema*` | Public (thesis-only, noindex, not in scope of this plan) |
| `/riset/petunjuk-arsip/` | `riset_petunjuk_arsip` | client-side fetch `/api/research/sankey-tema?corpus_asal=globalise` | Public (thesis-only, noindex, out of scope) |
| `/riset/jaringan/` | `riset_jaringan` | client-side fetch `/api/research/network-pelabuhan`, `/sankey-tema/rows` | Public (thesis-only, noindex, out of scope) |
| `/riset/atjeh-dagang/` | `riset_atjeh` | client-side fetch `/api/research/atjeh-trade` | Public (thesis-only, noindex, out of scope) |
| **`/riset/pemodelan/`** | `riset_pemodelan` | SSR `httpx.get(/api/research/pemodelan-dashboard)` | **PLAN CANDIDATE — protect** |
| **`/riset/pemodelan/panduan/`** | `riset_pemodelan_panduan` | SSR `httpx.get(/api/research/pemodelan-dashboard)` (same endpoint, reused) | **PLAN CANDIDATE — protect** |
| `/riset/enclave-1682/` | `riset_enclave_1682` | (not inspected this turn — outside plan §1 candidate list) | Out of scope this turn |
| **`/linimasa/`** | `linimasa` | SSR `httpx.get(/api/research/linimasa)` | **PLAN CANDIDATE — protect** |
| `/ports/<slug:slug>/` | `port_detail` | (public map feature) | Public |

All three plan-candidate views are function-based Django views with **no decorator, no middleware gate, no session check** — confirmed by reading `frontend/map_app/views.py` in full for these three functions; none reference `request.user`, `login_required`, or any guard.

---

## 2. Public-Prefixed Routes (production, silida.org)

Per `/etc/nginx/conf.d/silida.conf` (host nginx, read-only inspection via SSH — this file is **not in git**, confirmed the sole source of truth per prior session memory):

```text
https://silida.org/atlas/riset/pemodelan/
https://silida.org/atlas/riset/pemodelan/panduan/
https://silida.org/atlas/linimasa/
```

**Critical alternate-path finding:** `/westkust/` and `/atlas/` are two *separate* `location` blocks in `silida.conf`, but both `proxy_pass http://127.0.0.1:8084/` — **byte-identical destinations**. The same three pages are therefore also live and fully reachable at:

```text
https://silida.org/westkust/riset/pemodelan/
https://silida.org/westkust/riset/pemodelan/panduan/
https://silida.org/westkust/linimasa/
```

**Any access-control design that protects only the `/atlas/` location block and not `/westkust/` (or vice versa) is bypassable via the sibling prefix.** Both must be protected identically, or one must be removed/redirected before protection is added.

---

## 3. Child, Trailing-Slash, and Alternate-Path Behavior

- Django's `APPEND_SLASH` (default True) means `/atlas/linimasa` (no trailing slash) redirects to `/atlas/linimasa/` — but the redirect `Location:` header is rewritten by the host nginx's `proxy_redirect / /atlas/;` directive (and the equivalent for `/westkust/`). **Any auth layer must be tested against the no-trailing-slash entry point too**, since it passes through an extra redirect hop before reaching the final protected path.
- No query-string-based route variants exist for these three views (none of the three view functions read `request.GET`).
- No encoded-path (`%2e%2e`, double-encoding) handling is customized anywhere in Django, Docker nginx, or host nginx — relies entirely on Django's and nginx's own default normalization. Not separately verified this turn (would require live fuzzing, out of scope for read-only discovery).
- `riset_pemodelan_panduan`'s template links use relative paths (`../`, `../../../`) rather than absolute — these resolve correctly under both `/atlas/` and `/westkust/` prefixes without needing prefix-aware view code, but this also means **a protected page's internal nav links stay inside the same prefix**, so protection does not need special-case link rewriting once the location block itself is guarded.

---

## 4. API, JSON, Static JS, Source Map, Data Bundle, Image, and Font Inventory

### 4.1 Backend API endpoints actually consumed by the three candidate pages

| Endpoint | Consumed by | Data returned |
|---|---|---|
| `GET /api/research/linimasa` | `/linimasa/` (SSR) | Full `items` array (all fields rendered are 1:1 with what's embedded in the page) + `meta` (counts) |
| `GET /api/research/pemodelan-dashboard` | `/riset/pemodelan/` and `/riset/pemodelan/panduan/` (SSR, same call) | Bokeh `script`/`div`/`params` for 4 charts (markov, hawkes, dynamics, game_theory) |

Both endpoints are mounted under FastAPI's `research.router`, prefix `/api/research`, tag `"Research (thesis-only)"` (`backend/main.py:41`). **No authentication dependency is attached to either endpoint** — verified by reading the full route decorators; neither uses `Depends(verify_api_key)` or any other guard (that guard exists only on `staging.router`, see §4.4).

### 4.2 Reachability of these two endpoints independent of the HTML pages

Per the host nginx `location /api/` block, **all of `/api/research/*` is reachable directly** at:

```text
https://silida.org/api/research/linimasa
https://silida.org/api/research/pemodelan-dashboard
```

This is a single, prefix-agnostic path — it is **not** namespaced under `/atlas/` or `/westkust/` at all. **Protecting the HTML pages alone does not protect this data.** Anyone with the URL can fetch the full linimasa dataset and dashboard fragments today, and will continue to be able to after only the HTML pages are gated, unless these two API paths are separately included in the auth boundary.

### 4.3 Static assets used by the three candidate pages

| Asset | Path | Sensitivity |
|---|---|---|
| Bokeh JS (vendored, not CDN) | `/static/map_app/vendor/bokeh-3.9.1.min.js`, `bokeh-widgets-3.9.1.min.js` | Public — generic charting library, no research content |
| Google Fonts (EB Garamond, Space Grotesk) | external CDN, `fonts.googleapis.com`/`fonts.gstatic.com` | Public, no research content |
| Hero/illustration images | `/static/map_app/img/linimasa-hero.jpg`, `peta-untukruangtengah.png`, `treaty-panel.jpg` | Public — decorative illustrations, not research data |
| Inline data (linimasa only) | `<script type="application/json" id="linimasa-data">{{ items_json }}</script>` in the page HTML itself | **Same sensitivity as the page** — protecting the HTML page also protects this inline block (no separate fetch); no additional risk beyond §4.2's direct-API path |

No source maps are served for any of the three pages (no `.js.map` references found). No separate "data bundle" JSON files are fetched client-side by `/linimasa/` or `/riset/pemodelan/*` — both are pure SSR with data embedded at render time, unlike `/riset/tema/`, `/riset/jaringan/`, `/riset/atjeh-dagang/` (which do client-side `fetch()` and are explicitly out of scope for this plan).

### 4.4 Existing (unrelated) API-key mechanism — for context only

`backend/routers/staging.py` implements a working `X-API-Key` header-based auth dependency (`verify_api_key`), backed by a `api_keys` table (SHA-256-hashed key, `key_hash`, `label`, `active`) in `backend/models.py`. This protects only `POST /api/staging/extractions` (notebook-to-server data ingestion) — it is **machine-to-machine ingestion auth, not a user-facing login system**, and is out of scope for protecting the three candidate pages, but establishes an existing, working precedent for hashed-secret storage and header-based verification in this codebase.

---

## 5. Endpoint Classification

Per plan §3.3 vocabulary:

| Endpoint/Route | Classification |
|---|---|
| `/riset/pemodelan/`, `/riset/pemodelan/panduan/`, `/linimasa/` (both `/atlas/` and `/westkust/` prefixes) | **AUTHENTICATED_RESEARCH_API candidate** (currently PUBLIC_API in practice — no gate exists yet) |
| `GET /api/research/linimasa` | **AUTHENTICATED_RESEARCH_API candidate** (currently PUBLIC_API — must be locked alongside the HTML page, see §4.2) |
| `GET /api/research/pemodelan-dashboard` | **AUTHENTICATED_RESEARCH_API candidate** (currently PUBLIC_API — same reasoning) |
| `/riset/tema/`, `/riset/petunjuk-arsip/`, `/riset/jaringan/`, `/riset/atjeh-dagang/` and their APIs | PUBLIC_API — out of scope per plan §1 (thesis-only/noindex but not named as a candidate); no change recommended without separate researcher instruction |
| `/`, `/ports/<slug>/`, map/fort/voyage APIs | PUBLIC_API — explicitly excluded by plan §3.2 |
| `POST /api/staging/extractions`, `GET /api/staging/extractions` | SERVER_INTERNAL_ONLY (already gated by `X-API-Key`, unrelated to this plan) |
| `GET /api/health` | PUBLIC_API — monitoring endpoint, explicitly excluded by plan §3.2 |
| `/docs`, `/openapi.json` (FastAPI) | Currently PUBLIC_API (rate-limited but unauthenticated) — exposes the full schema of `/api/research/*`, including the two candidate endpoints; **not itself a plan candidate route, but worth flagging** since it discloses the shape (not content) of protected-candidate data to anyone |
| `/riset/enclave-1682/` and its dependencies | NOT_IN_USE for this discovery — not inspected, not named by the plan's candidate list |

---

## 6. Runtime Framework Verification (not assumed from filenames)

Verified by reading actual source, not inferring from directory names:

- **Frontend:** Django 5.0.4 (`frontend/requirements.txt`), served via `gunicorn`/`runserver`, static files via `whitenoise`. Confirmed via `frontend/config/settings.py` (`ROOT_URLCONF`, `WSGI_APPLICATION`, `django.middleware.*`).
- **Backend:** FastAPI 0.111.0 on `uvicorn` (`backend/requirements.txt`, `backend/main.py`), SQLAlchemy 2.0 async + `asyncpg` against PostgreSQL/PostGIS, `redis` for cache-aside.
- **Reverse proxy (Docker layer):** `nginx:1.25-alpine` (`docker-compose.yml`), config at `nginx/nginx.conf` (tracked in git).
- **Reverse proxy (host layer):** system nginx on the production VPS, config at `/etc/nginx/conf.d/silida.conf` (verified live via SSH — **not tracked in git**, sole source of truth on the server itself).
