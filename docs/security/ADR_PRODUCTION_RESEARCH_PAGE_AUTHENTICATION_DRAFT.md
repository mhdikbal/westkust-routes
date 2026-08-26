# ADR — Production Research Page Authentication

> **Status:** `PENDING_RESEARCHER_DECISION`
> **Baseline:** `51b0bd902ef7ee708f825e7aaa565f0e0c4fd7d8`
> **This ADR does not select an option. It compares them for the researcher's own decision.**

---

## Context

Three production research pages (`/riset/pemodelan/`, `/riset/pemodelan/panduan/`, `/linimasa/`, reachable publicly at both `/atlas/...` and `/westkust/...`) plus their two backing API endpoints (`/api/research/linimasa`, `/api/research/pemodelan-dashboard`) are currently **fully public and unauthenticated** — verified in `PRODUCTION_RESEARCH_PAGE_ROUTE_INVENTORY.md` and `PRODUCTION_RESEARCH_PAGE_AUTH_THREAT_MODEL.md`.

Two pre-existing, auth-independent exposures were found during discovery and apply regardless of which option is chosen:

1. **Dual-prefix bypass:** `/atlas/` and `/westkust/` proxy to the identical upstream; protecting one without the other is a bypass.
2. **Direct backend-port exposure:** Docker's `voc_nginx` is published to `0.0.0.0:8084` with no host firewall — any option implemented only at the `silida.org` host-nginx layer is bypassable by hitting the VPS IP directly on port 8084.

Neither of these is fixed by this ADR or this discovery turn. They are noted here because they materially affect which option is *sufficient by itself* (see §"Cross-cutting prerequisite" below).

---

## Decision Criteria (plan §18)

security · setup burden · existing infrastructure · multi-user support · MFA · route precision · API protection · auditability · rollback · recurring cost · maintainability

---

## Option A — Application-Level Local Accounts

**What it would require, given the verified current state:**
- Enable `django.contrib.auth`, `django.contrib.sessions`, `django.contrib.contenttypes` in `INSTALLED_APPS` (none currently enabled)
- Add `SessionMiddleware`, `AuthenticationMiddleware`, `CsrfViewMiddleware` to `MIDDLEWARE` (none currently present)
- A user table (via Django's own migrations — first migration this app would ever run; currently there is no `DATABASES` configuration in `frontend/config/settings.py` at all, so a database would need to be provisioned for the frontend service, distinct from the backend's existing PostGIS database)
- `login_required`/`LoginRequiredMixin` (or an equivalent decorator) on the three candidate views, plus a `Depends(...)` guard on the two candidate FastAPI endpoints — **both layers**, since Django session cookies do not automatically protect FastAPI's separate service
- Password hashing via Django's built-in hashers (PBKDF2/Argon2) — no new dependency required, contradicting nothing in `requirements.txt`

**Security:** High, once correctly implemented — route-precise, can protect both the Django views and the FastAPI endpoints explicitly.
**Setup burden:** Highest of the three — genuinely new infrastructure (first database for the frontend service, first migration, first middleware stack).
**Existing infrastructure fit:** Backend already has SQLAlchemy/PostgreSQL; frontend has neither an ORM connection nor any DB currently — this is new plumbing for the frontend service specifically.
**Multi-user / role support:** Best of the three — the plan's RESEARCHER/REVIEWER/ADMIN model (plan §6) maps directly onto Django groups/permissions or a custom role field.
**MFA:** Not built-in to a minimal implementation; would require an additional package (e.g., `django-otp`) — not currently installed, would be a new dependency.
**Route precision:** Best of the three — per-view, per-API-endpoint control.
**API protection:** Directly supportable — a FastAPI dependency can validate the same session or a derived token.
**Auditability:** Full control — custom audit-event logging is exactly as designed in plan §13, straightforward to add alongside the auth code itself.
**Rollback:** Clean — this is additive code; disabling the middleware/decorators reverts to the current public state. Database migration rollback needs its own tested `migrate --fake`/reverse-migration plan once implemented.
**Recurring cost:** None (self-hosted).
**Maintainability:** Moderate — the team now owns password reset, session expiry, and account lifecycle code long-term.

---

## Option B — Entra/OIDC Identity-Aware Proxy

**What it would require, given the verified current state:**
- An identity provider tenant/app registration (external to this repo, external cost/setup burden per plan §4)
- A proxy layer (either an OIDC-aware nginx module/auth_request setup, or a dedicated proxy like oauth2-proxy) inserted **at the host-nginx layer**, since that is the only layer that currently sees 100% of the traffic to `/atlas/` and `/westkust/` before it reaches the app
- Because of the §"dual-prefix" finding, the OIDC callback/redirect logic would need to be prefix-aware for **both** `/atlas/` and `/westkust/` — doubling the callback-URI configuration surface on the identity-provider side, or requiring one prefix to be retired/redirected to the other first
- Because of the §"direct backend-port" finding, this option is **not sufficient by itself** unless port 8084 exposure is also closed — an identity-aware proxy at the `silida.org` layer does nothing to protect `http://103.171.184.94:8084/...`

**Security:** Highest ceiling of the three (centralized identity, MFA, Conditional Access) — but only once the two cross-cutting prerequisites above are also addressed.
**Setup burden:** High — external tenant/app registration, DNS, redirect URI, forwarded-header correctness across two proxy layers (Cloudflare → host nginx → this proxy → Docker nginx → app).
**Existing infrastructure fit:** None currently in this repo — greenfield for this project (no OIDC client, no `authlib`/similar dependency found anywhere in `requirements.txt`).
**Multi-user / role support:** Strong, delegated to the IdP — but mapping IdP groups to the plan's RESEARCHER/REVIEWER/ADMIN roles would still need application-side logic.
**MFA:** Native to the IdP — no app-side work.
**Route precision:** Coarser than Option A by default (typically gates entire path prefixes at the proxy) unless combined with app-level checks for finer API-level distinctions.
**API protection:** Requires the `/api/research/*` paths to sit behind the same proxy layer explicitly — not automatic, since `/api/` is presently its own top-level nginx block, separate from `/atlas/`/`/westkust/` (route inventory §2).
**Auditability:** Strong at the IdP side (sign-in logs); app-side event correlation still needs to be built.
**Rollback:** Proxy-layer removal is relatively clean, but touches production nginx configuration directly (higher blast radius per change than Option A's app-code-only changes).
**Recurring cost:** Possible licensing/tenant cost depending on provider — not evaluated here (organizational decision, out of scope for this codebase discovery).
**Maintainability:** Lower long-term burden than Option A (no local password/account lifecycle to maintain) once initial setup is done.

---

## Option C — Nginx Basic Auth Stopgap

**What it would require, given the verified current state:**
- An `htpasswd` file and `auth_basic`/`auth_basic_user_file` directives added to **both** the `/atlas/` and `/westkust/` location blocks in `silida.conf` (again, the dual-prefix finding applies directly — a single-block edit is bypassable)
- A corresponding rule for the `/api/research/linimasa` and `/api/research/pemodelan-dashboard` paths specifically (not all of `/api/`, since other API paths under `/api/research/*` are explicitly out of scope per the route inventory and plan §1) — this requires either splitting `/api/research/` into its own location block with narrower matching, or an equivalent nginx-level rule scoped precisely enough to avoid over-blocking the out-of-scope research pages (`/riset/tema/`, `/riset/jaringan/`, `/riset/atjeh-dagang/`, `/riset/petunjuk-arsip/`) which share the same `/api/research/` prefix
- Because of the direct-backend-port finding, **this option is also insufficient by itself** unless port 8084 is closed — Basic Auth added only to `silida.conf` does not protect `http://103.171.184.94:8084/...`

**Security:** Lowest of the three, but non-trivial as a genuine stopgap once the two cross-cutting prerequisites are handled — credentials travel as a base64-encoded (not encrypted-beyond-TLS) header on every request, no session expiry beyond the browser's own credential cache, no per-user audit trail beyond "which shared credential was used."
**Setup burden:** Lowest of the three by a wide margin — no application code change, no new database, no external tenant.
**Existing infrastructure fit:** Uses only what's already running (nginx); no new dependency anywhere.
**Multi-user / role support:** Weak — `htpasswd` supports multiple named users, but there is no role distinction (RESEARCHER/REVIEWER/ADMIN from plan §6 would need to be layered on top separately, e.g., at the application level later).
**MFA:** Not supported by Basic Auth itself.
**Route precision:** Coarse by default (whole location blocks) but can be scoped to specific `location` matches, including the narrower `/api/research/linimasa` and `/api/research/pemodelan-dashboard` paths if the nginx config is restructured to isolate them from the other, out-of-scope `/api/research/*` paths.
**API protection:** Achievable, but requires the extra location-block precision noted above — not automatic.
**Auditability:** Minimal — nginx access logs show which `htpasswd` username authenticated per request, no structured login/logout/session events (plan §13's event list is not satisfiable by Basic Auth alone).
**Rollback:** Very clean — remove the `auth_basic` lines, reload nginx. Lowest blast radius of the three options.
**Recurring cost:** None.
**Maintainability:** Manual credential rotation (`htpasswd` file edits), browser credential caching makes logout meaningless without clearing browser data — explicitly why the plan (§4, "Option C: Hanya Stopgap") frames this as time-bounded, not a destination architecture.

---

## Cross-Cutting Prerequisite (applies to all three options)

Neither the dual-prefix finding nor the direct-backend-port finding is specific to one option — **every option's effectiveness depends on how these two are handled**:

- **Dual-prefix (`/atlas/` + `/westkust/`):** whichever option is chosen must apply to both prefixes identically, or one prefix must be retired/redirected before the other is protected.
- **Direct-backend-port (`0.0.0.0:8084`, no firewall):** an application-layer control (Option A, or Option B/C combined with app-level API guards) survives this exposure since it checks identity regardless of entry path; a *proxy-only* control (Option B or C implemented solely in `silida.conf`) does **not** survive it unless the port exposure is separately closed.

This is presented as a finding for the researcher's decision, not a recommendation to close the port in this turn — doing so would be a Nginx/Docker configuration change, explicitly forbidden in this discovery phase.

---

## Recommended Target (per plan §4/§5, restated)

```text
RECOMMENDED TARGET (plan's own text):
Option A or Option B

TEMPORARY STOPGAP (plan's own text):
Option C only with explicit researcher approval and expiry date
```

The SEC-0/SEC-1 discovery and design turns did not select between these options — that selection is recorded below, as the researcher's own explicit direction, not as this ADR's own recommendation.

---

## Researcher Decision (recorded — implementation not yet authorized)

```text
Transitional architecture:
OPTION_C_APPROVED_WITH_LIMITATIONS

Long-term target:
OPTION_B_APPROVED_WITH_LIMITATIONS

Containment:
N1_APPROVED_WITH_LIMITATIONS

Dual prefix:
P1_APPROVED

Security gate:
NOT_PASSED
```

Full rationale, safeguards, and dependencies for each of these are recorded per-decision in `PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv` (SEC-DEC-01 through SEC-DEC-10). This ADR records the researcher's architecture *direction*; it is not itself an implementation record — no Basic Auth, Entra/OIDC, or network-containment change has been made. Recording this direction does not authorize implementation, production deployment, or a passed security gate.

---

## Status

```text
RESEARCHER_DIRECTION_RECORDED_IMPLEMENTATION_NOT_AUTHORIZED
```
