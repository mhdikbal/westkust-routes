# Production Research Page — Auth Discovery Audit

> **Phase:** SEC-0 Discovery (read-only) — completion record
> **Baseline:** `51b0bd902ef7ee708f825e7aaa565f0e0c4fd7d8`
> **Plan:** `PLAN_PRODUCTION_RESEARCH_PAGE_ACCESS_CONTROL.md`

---

## 1. Scope

Verifies that Phase SEC-0 (read-only discovery) was performed as specified in the plan, records what was inspected, what was found, and confirms the security guards held throughout.

## 2. Method

All findings sourced from: reading `frontend/config/urls.py`, `frontend/map_app/urls.py`, `frontend/map_app/views.py` (full three candidate view functions), `frontend/map_app/templates/map_app/{riset_pemodelan,riset_pemodelan_panduan,linimasa}.html`, `frontend/config/settings.py`, `frontend/requirements.txt`, `backend/main.py`, `backend/routers/research.py` (linimasa + pemodelan-dashboard route definitions), `backend/routers/staging.py`, `backend/models.py`, `backend/requirements.txt`, `nginx/nginx.conf`, `docker-compose.yml`, `.gitignore`; plus read-only SSH inspection of the production server: `/etc/nginx/conf.d/silida.conf`, `docker compose ps`, `ss -tlnp`, `ufw status`, `.env` file existence/permissions (not contents).

## 3. Internal Route Inventory

Complete — see `PRODUCTION_RESEARCH_PAGE_ROUTE_INVENTORY.md` §1. Nine Django routes enumerated from the actual `urlpatterns` list; three are the plan's candidates (`/riset/pemodelan/`, `/riset/pemodelan/panduan/`, `/linimasa/`).

## 4. Public Route Inventory

Complete — see route inventory §2. Confirmed via live `silida.conf` read: both `/atlas/...` and `/westkust/...` public prefixes exist and proxy identically.

## 5. Child and Alternate Routes

Complete — see route inventory §3. Trailing-slash/`APPEND_SLASH` behavior, prefix-redirect rewriting, and relative-link structure all verified from actual template/config content, not assumed.

## 6. API Inventory

Complete — see route inventory §4. Two backend endpoints directly consumed by the three candidate pages identified and classified; the pre-existing, unrelated `X-API-Key` mechanism on `/api/staging/extractions` documented for context.

## 7. Static-Data Leakage Risks

Assessed — see route inventory §4.3 and §5. Finding: the two candidate API endpoints (`/api/research/linimasa`, `/api/research/pemodelan-dashboard`) are directly reachable independent of the HTML pages, and are not currently namespaced under either public prefix. This is the most actionable static-data-leakage-adjacent finding from this discovery (technically an API-authorization gap, not a static-bundle leak, since no separate static JSON bundle exists for these two pages).

## 8. Actual Framework

Verified, not assumed — see route inventory §6. Django 5.0.4 (frontend) confirmed via `requirements.txt` + `settings.py` internals (`ROOT_URLCONF`, `WSGI_APPLICATION`); FastAPI 0.111.0 (backend) confirmed via `requirements.txt` + `main.py` (`FastAPI(...)`, `uvicorn`).

## 9. Existing Auth Capability

Verified — see threat model §1. **None.** No `django.contrib.auth`, no session middleware, no user model, no authorization middleware anywhere in either service.

## 10. Existing Session Capability

Verified — see threat model §1. **None.** No `SessionMiddleware`; FastAPI CORS explicitly configured `allow_credentials=False` with a code comment confirming "no cookie/session, per prior audit."

## 11. Existing CSRF Protection

Verified — see threat model §1. **None** — no `CsrfViewMiddleware`, no `{% csrf_token %}` usage anywhere (no state-changing form exists yet in the Django app to protect).

## 12. Existing Rate Limiting

Verified — see threat model §1. **Partial, generic, IP-based only:** Docker-layer nginx `limit_req_zone`, 60 req/min per IP on `/api/`, burst 20 (main), burst 5 (`/docs`, `/openapi.json`), custom JSON 429 response. No per-account limiting exists because no accounts exist.

## 13. Existing Audit Logging

Verified — see threat model §1. **None at application level.** Only nginx default `access_log`/`error_log` at both the Docker and host layers — request-level, not security-event-level.

## 14. Nginx Prefix Behavior

Verified live on production — see threat model §2. Confirmed `/atlas/` and `/westkust/` are separate location blocks proxying to the identical upstream (`http://127.0.0.1:8084/`), each with its own `proxy_redirect` and `sub_filter` rewriting — the dual-prefix bypass finding is a direct reading of this config, not inference.

## 15. Forwarded-Header Behavior

Verified — see threat model §2. `X-Forwarded-Proto` is hardcoded to `https` in both public-prefix blocks (not `$scheme`); `X-Forwarded-For`/`Host` are passed through standard `proxy_set_header` directives at both the host-nginx and Docker-nginx layers.

## 16. Direct-Backend Exposure

**Verified live on production — CRITICAL FINDING.** See threat model §3. `voc_nginx` (Docker layer) is bound to `0.0.0.0:8084` / `[::]:8084`, confirmed via `docker compose ps` and `ss -tlnp` on the server. `ufw status` returned `inactive` — no host firewall exists. This is a pre-existing exposure of the entire application (not created or modified by this discovery turn) and applies regardless of which authentication option is eventually chosen at the `silida.org` host-nginx layer.

## 17. TLS Termination

Verified — see threat model §4. Cloudflare Origin Certificate at the host-nginx layer (`silida-origin.pem`/`.key`, `TLSv1.2`/`TLSv1.3`), confirmed by reading the live `silida.conf`. Docker-internal hop is plain HTTP by design, but is exposed directly to the internet via the §16 finding.

## 18. Secret-Management Pattern

Inspected structurally only — see threat model §5. `.env` confirmed gitignored both locally and on the server (path and gitignore-match checked; **no file contents read, no values printed**). `docker-compose.yml` interpolation pattern confirmed via `grep` for `${VAR}` syntax, not value inspection. Existing hashed-secret precedent (`ApiKey.key_hash`) confirmed by reading the model/router code, not by reading any live key value (none exist in code — they are runtime-provisioned and stored hashed in the database).

## 19. Option A Assessment

Complete — see ADR. Application-level local accounts: highest security ceiling achievable without external dependency, highest setup burden (first database + first migration for the frontend service), best route/API precision, best auditability control.

## 20. Option B Assessment

Complete — see ADR. Entra/OIDC identity-aware proxy: highest overall security ceiling (centralized identity, MFA), but requires external tenant setup and is **not sufficient alone** against the §16 direct-backend-port finding, and must be made dual-prefix-aware per §14.

## 21. Option C Assessment

Complete — see ADR. Nginx Basic Auth: lowest setup burden and lowest security ceiling, explicitly framed by the plan itself as a stopgap only; also **not sufficient alone** against the §16 finding, and requires careful location-block scoping to avoid over-blocking the out-of-scope `/riset/tema/`, `/riset/jaringan/`, `/riset/atjeh-dagang/`, `/riset/petunjuk-arsip/` pages that share the `/api/research/` prefix.

## 22. Recommended Option, Clearly Marked Recommendation Only

**No option is selected by this discovery turn or its outputs**, per plan §11 and §18 ("No option may be selected automatically"). The ADR restates the plan's own stated target (Option A or B primary, Option C as a time-bounded, separately-approved stopgap only) without adopting it as a decision. Status remains `PENDING_RESEARCHER_DECISION`.

## 23. Implementation Prerequisites (for whichever option is eventually chosen)

1. Researcher decision on Option A vs. B vs. C-as-stopgap (Phase SEC-1, out of scope for this turn).
2. Resolution of the dual-prefix finding (§14/threat model §2) — apply to both `/atlas/` and `/westkust/`, or retire one.
3. Resolution or explicit acceptance of the direct-backend-port finding (§16) — this is a standing exposure independent of the auth decision and should be evaluated on its own timeline.
4. Explicit approval of session/timeout/rate-limit/role policy parameters (plan §§6, 8, 9 — currently only "candidate planning targets," not approved).
5. Local nonproduction prototype (Phase SEC-2) before any staging or production change.

## 24. Rollback Requirements

Not yet applicable — no implementation occurred this turn. Rollback design is a Phase SEC-1 output per the plan (§18, "rollback design"), to be authored once an option is selected.

## 25. Security Gate Status

```text
SECURITY_ACCESS_CONTROL_GATE: NOT_PASSED
```

Unchanged by this discovery turn, per plan §22 — this gate requires researcher-approved architecture, implementation, and testing, none of which occurred here.

## 26. Git Status

```text
 M docs/thesis/colab/POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv   (pre-existing, from prior turn — untouched this turn)
?? docs/security/                                                 (new — this turn's four output documents)
?? PLAN_PRODUCTION_RESEARCH_PAGE_ACCESS_CONTROL.md                 (pre-existing, root, read this turn)
... (pre-existing untracked files, unchanged from session start)
```

Nothing staged. Nothing committed. `docs/security/` is not covered by any existing `.gitignore` rule (confirmed via `git check-ignore`) and would need explicit staging to enter git — none occurred.

## 27. Confirmation No Credentials Created

Confirmed. No username, password, htpasswd file, API key, or account of any kind was created, generated, or modified during this turn.

## 28. Confirmation No Configuration Changed

Confirmed. `nginx/nginx.conf`, `docker-compose.yml`, `/etc/nginx/conf.d/silida.conf` (production), Django `settings.py`, and FastAPI `main.py` were all read-only inspected; none were edited. No `INSTALLED_APPS`, `MIDDLEWARE`, or dependency list was modified.

## 29. Confirmation No Restart/Rebuild/Deploy

Confirmed. No `docker compose build`/`up`/`restart`/`down` command was executed, locally or on the production server. No `git add`, `commit`, or `push` occurred.

---

## Final Status

```text
PRODUCTION_RESEARCH_PAGE_AUTH_DISCOVERY_READY_FOR_RESEARCHER_DECISION
```
