# Production Research Page — Option B Entra/OIDC Target Design

> **Phase:** SEC-1 Architecture Design (no implementation)
> **Status:** TARGET DESIGN ONLY — no Entra tenant, app registration, or IdP configuration created
> **Baseline:** `51b0bd902ef7ee708f825e7aaa565f0e0c4fd7d8`

---

## 1. Public Callback URI with `/atlas/` Prefix

Given the traced network path (network containment plan §1) and the existing `proxy_redirect / /atlas/;` behavior, the OIDC callback endpoint must be registered with the identity provider as:

```text
https://silida.org/atlas/auth/callback     (illustrative path — final path TBD at implementation)
```

not a bare `https://silida.org/auth/callback` — because the application itself is prefix-unaware (it uses root-relative routes internally, per prior session record, with the prefix applied entirely at the host-nginx layer). If the identity-aware proxy or application constructs the callback URL from its own internal, unprefixed view of its routes, the resulting redirect URI will not match what's registered with the IdP, and the flow will fail — this is the exact class of bug already found and fixed once for Django's `APPEND_SLASH` redirects (documented in this project's own prior session history) and must not be reintroduced for OIDC callbacks.

## 2. Handling of `/westkust/`

Per the dual-prefix policy (P1: protect identically), **a second, mirrored callback URI must also be registered**:

```text
https://silida.org/westkust/auth/callback
```

Both must be present in the IdP's allowed redirect-URI list simultaneously during the transitional period (until/unless P2 — canonical-prefix redirect — is later adopted, at which point only one callback URI would remain necessary). This doubles the IdP-side configuration surface, a cost explicitly noted in the ADR's Option B assessment (`ADR_PRODUCTION_RESEARCH_PAGE_AUTHENTICATION_DRAFT.md`).

## 3. Forwarded Host/Proto/Prefix

The identity-aware proxy (whichever component terminates the OIDC flow — options include an `auth_request`-based nginx module pointed at a small local auth service, or a dedicated proxy like `oauth2-proxy` placed between host nginx and the protected location blocks) must construct its own redirect/state URLs using:

- `X-Forwarded-Host: silida.org` (not the Docker-internal `frontend`/`backend` container names)
- `X-Forwarded-Proto: https` (already hardcoded correctly in the existing `/atlas/`/`/westkust/` blocks — confirmed in SEC-0 discovery)
- **A forwarded-prefix header is not currently set anywhere in `silida.conf`** (no `X-Forwarded-Prefix` directive exists on any existing block) — this is a **new requirement** the design must introduce: whichever proxy component handles the callback needs to know whether the original request came in via `/atlas/` or `/westkust/` in order to redirect back to the correct prefix after login (§7 below). Design recommendation: add `proxy_set_header X-Forwarded-Prefix /atlas/;` (and the `/westkust/` equivalent) to the new child location blocks specifically, distinct from the parent blocks which do not currently set this header.

## 4. Identity-Aware Proxy Placement

Given the F-03 direct-backend-port finding (network containment plan), the identity-aware proxy is only effective if it sits at a layer that **all** legitimate traffic must pass through. Two candidate placements, with tradeoffs:

- **At the host-nginx layer (`silida.conf`), via `auth_request`:** covers both `/atlas/` and `/westkust/` HTML traffic, and the API location blocks if configured identically — but does **not** by itself cover a request arriving via the F-03 direct-port path (`<VPS-IP>:8084`), since that path never reaches `silida.conf` at all. **This placement alone is insufficient** unless SEC-DEC-01/02 (network containment, N1) is approved and applied first — confirming the researcher's own stated dependency ("Jangan membuat akun dulu... sistem akan tampak terkunci melalui domain tetapi tetap terbuka melalui prefix lain atau port 8084").
- **At the application layer (FastAPI dependency + Django middleware/decorator validating the same session/token):** survives the F-03 exposure regardless of entry path, since the check happens inside the application itself, not only at a proxy in front of it. This is the stronger design and is recommended as the primary enforcement point, with the host-nginx `auth_request` (if used) treated as defense-in-depth rather than the sole boundary.

## 5. Preauthentication Boundary

Recommended target: reject anonymous requests to the six protected paths (four HTML child locations + two API child locations, per the dual-prefix and API policy document) **before** they reach Django/FastAPI application code at all, when the proxy-layer placement (§4) is used — this satisfies plan §4's Option B advantage ("anonymous requests dapat ditolak sebelum mencapai backend"). Where application-layer enforcement (§4, second bullet) is used instead, the boundary is the first line of the protected view function / route dependency, which is the earliest point achievable given the F-03 constraint.

## 6. Entra Group-to-Role Mapping

Maps directly onto the plan's own role model (`PLAN_PRODUCTION_RESEARCH_PAGE_ACCESS_CONTROL.md` §6):

```text
Entra security group  →  Application role
research-pilot-readers →  RESEARCHER
research-pilot-review  →  REVIEWER
research-pilot-admin   →  ADMIN
```

Group names above are illustrative — actual group naming is an organizational decision outside this codebase's scope. The application-side mapping logic (reading group claims from the OIDC ID token and assigning a role) is new code that does not exist yet in either service (confirmed: no role/permission field exists anywhere in `backend/models.py` or Django's currently-disabled auth system).

## 7. MFA and Conditional Access

Delegated entirely to the identity provider — no application-side implementation required, per the ADR's Option B assessment. This is one of Option B's clearest advantages over both A and C.

## 8. Logout

Must invalidate both (a) the local session/cookie the application itself set, and (b) redirect to the IdP's own logout endpoint (OIDC `end_session_endpoint`) to clear the IdP-side session — a local-only logout would leave the user still authenticated at the IdP, able to silently re-obtain a new local session without re-entering credentials, which may or may not be the desired behavior (a decision for whoever finalizes the Phase SEC-2 prototype, not this turn).

## 9. Session Expiry

Recommended to follow the same candidate planning targets already recorded in the access-control plan (`PLAN_PRODUCTION_RESEARCH_PAGE_ACCESS_CONTROL.md` §8): idle timeout 30–60 minutes, absolute lifetime 8–12 hours, remember-me disabled for the pilot — these targets are stated in the plan as **not yet approved**, and remain not-yet-approved after this design turn; carried forward as-is.

## 10. Service-Account Policy

No service/machine account use case has been identified for these three pages during discovery (all three are human-facing SSR pages, not API-only integrations) — the existing `ApiKey` mechanism already serves the one identified machine-to-machine case (`/api/staging/extractions`, unrelated to this plan). Design recommendation: **no new service account** is needed for Option B's initial scope; revisit only if a future automated consumer of the two research APIs is identified.

## 11. Emergency Recovery

If the IdP becomes unreachable (outage, misconfiguration, tenant issue), the design must not lock out legitimate access to the *rest* of the site (public Atlas pages, which must remain unaffected per the plan's own acceptance criteria). Recommended design principle: the identity-aware proxy/dependency must fail closed *only* for the six protected paths, and must not be positioned such that its failure cascades to the public `/`, `/ports/`, or the four out-of-scope research pages. An emergency local-admin bypass (e.g., a break-glass mechanism) is explicitly listed in the plan (§15) as a required recovery capability — concrete design deferred to Phase SEC-2, since it depends on which enforcement placement (§4) is finalized.

## 12. Audit Events

Same event list as the plan specifies (§13): login success/failure, logout, session revoked, password changed (N/A for Option B — passwords are IdP-managed, not application-managed), account created (N/A, IdP-managed), authorization denied, rate-limit triggered, configuration version. For Option B specifically, login success/failure events are partially available from the IdP's own sign-in logs (external to this codebase) — application-side audit logging should still record the *authorization* decision (which role/route was granted or denied) locally, since IdP logs alone do not capture "user X was denied `/riset/pemodelan/` because they lack the REVIEWER group," only "user X signed in successfully."

## 13. Direct-Port Containment Prerequisite

**Restated explicitly, as the plan requires:** Option B's security guarantee holds only for traffic that passes through the layer where the identity check is enforced. If enforcement is proxy-only (§4, first bullet) and network containment (SEC-DEC-01/02) is not yet applied, the F-03 direct-port path remains a complete bypass of the entire Option B mechanism, regardless of how well-configured the IdP integration is. **This is why SEC-DEC-01 is listed as the first, foundational decision in the security decision ledger — Option B (and Option C) are both contingent on it, not independent of it.**

---

## Not Performed This Turn

No Entra tenant created. No app registration created. No client ID/secret generated or referenced. No IdP configuration of any kind performed. This document is a target-architecture design only, for future Phase SEC-2+ implementation once SEC-DEC-06 (and its prerequisites) are approved.
