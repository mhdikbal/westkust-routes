# ATLAS /westkust/ Route Retirement — Discovery

> **Read-only discovery. No route changed. No Nginx edited. No redirect implemented. No production, config, or source modification.**

---

## 1. Current Classification

```text
/atlas/     -- PRODUCTION_PUBLIC_ALIAS (canonical target per ROUTE-DEC-01)
/westkust/  -- PRODUCTION_PRIMARY_OR_LEGACY_PREFIX (legacy route, targeted for retirement)
```

Both currently serve the identical live production application (`silida.conf`, both `location` blocks `proxy_pass http://127.0.0.1:8084/`), per `ATLAS_ENVIRONMENT_AND_ROUTE_BOUNDARY_CORRECTION.md`.

## 2. Live Route Inventory (read-only, this turn)

| Check | `/atlas/` | `/westkust/` |
|---|---|---|
| Root, trailing slash | `200` | `200` |
| Root, no trailing slash | `301` → same prefix `.../<prefix>/` | `301` → same prefix `.../<prefix>/` |
| `/linimasa/`, trailing slash | `200` | `200` |
| `/linimasa`, no trailing slash | `301` → `.../linimasa/` | `301` → `.../linimasa/` |
| `/riset/pemodelan/` | `200` | `200` |
| `/riset/pemodelan/panduan/` | `200` | `200` |
| `/linimasa/?tahun=1700` (query string) | `200`, no redirect | `200`, no redirect |
| `HEAD /linimasa/` | `200` | `200` |
| Static asset (`/static/map_app/js/atlas.js`) | `200` | `200` |

Both prefixes behave identically across every check performed — status codes, `APPEND_SLASH` redirect behavior (each redirects within its own prefix, never cross-prefix), query-string preservation, `HEAD` support, and static asset delivery.

Duplicated-prefix behavior (`/atlas/atlas/...`, `/westkust/westkust/...`) was already characterized against the real Django app in `PRODUCTION_RESEARCH_PAGE_SEC3A_REAL_DJANGO_TEST_RESULTS.csv` (`SEC3A-DJ-008`/`009`): Django's own 404 handler rejects these, no protected content leaks. Not re-tested this turn — reused as existing evidence per the instruction not to repeat prior test categories unnecessarily.

## 3. Repository Dependency Search

Searched: literal `/westkust/` path strings, the bare word `westkust`, absolute `silida.org/westkust` URLs, canonical-link/sitemap/robots mechanisms, JS route construction, Django `reverse()`/`redirect()` calls, Nginx location blocks in the repo's own `nginx/nginx.conf`, `docker-compose.yml` healthchecks, and `docs/` documentation.

**Result: zero literal `/westkust/` path references anywhere in application code, the repository's own `nginx/nginx.conf`, or `docker-compose.yml`.** The `/westkust/` (and `/atlas/`) prefix exists **only** in `silida.conf` — the host Nginx config, which lives on `westkust-prod` outside this Git repository, not tracked in version control at all. Full classified hit list: `ATLAS_WESTKUST_ROUTE_DEPENDENCY_LEDGER.csv`.

Notable absence: **no `<link rel="canonical">`, no `og:url` meta tag, and no `robots.txt`/`sitemap.xml`** exist anywhere in `frontend/map_app/templates/`. This means canonicalization infrastructure does not currently exist to *update* — implementing SEO canonicalization (§ Phase 5 of the plan) would mean *adding* this mechanism for the first time, not modifying an existing one.

The bare word `westkust` appears widely (project name `westkust-routes`, server host `westkust-prod`, repository/service identifiers, unrelated ontology-research documents referencing a researcher's Google Drive folder path) — none of these are route references and none require any change.

## 4. Basemap Cross-Check

Both `/atlas/` and `/westkust/` serve the identical `atlas.js` (confirmed live, § 2 static asset check — same file, same `HTTP 200`, same CARTO `light_all` keyless tile configuration diagnosed in `ATLAS_BASEMAP_API_KEY_REQUIRED_DISCOVERY.md`). Retiring `/westkust/` does not touch this file or fix the watermark — that remains `ATLAS_BASEMAP_PROVIDER_OPTIONS.md`'s separate, unresolved workstream.

## 5. Final Status

```text
ATLAS_WESTKUST_ROUTE_RETIREMENT_PLAN_READY_FOR_REVIEW
```

See `ATLAS_CANONICAL_ROUTE_REDIRECT_PLAN.md` for the candidate redirect design and `ATLAS_WESTKUST_ROUTE_RETIREMENT_AUDIT.md` for the consolidated record.
