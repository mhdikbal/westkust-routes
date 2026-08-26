# Production Research Page — Basic Auth Nonproduction Implementation Specification

> **Status:** SPECIFICATION ONLY — describes a nonproduction prototype to be built in a future, separately authorized turn. Nothing in this document has been implemented, deployed, or applied.
> **Baseline:** `51b0bd902ef7ee708f825e7aaa565f0e0c4fd7d8`
> **Governing decisions:** `PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv` (SEC-DEC-01 through SEC-DEC-10, all decided this turn)
> **This document contains no real username, password, password hash, sensitive secret path, or executable production command sequence.**

---

## 1. Scope

Specifies the nonproduction/local-or-production-like Basic Auth prototype (Option C, SEC-DEC-05: `APPROVED_WITH_LIMITATIONS`) that would satisfy the researcher's own containment-first requirement: port-8084 exposure closed (N1) and both public prefixes protected (P1) *before* Basic Auth is treated as a real boundary rather than a partially-bypassable one. This spec covers design and test procedure only — no step in it is authorized to run against production this turn.

## 2. Researcher Decisions (as recorded)

```text
SEC-DEC-01  APPROVED                            network containment before auth
SEC-DEC-02  N1_APPROVED_WITH_LIMITATIONS         127.0.0.1:8084:80; N2 DEFERRED
SEC-DEC-03  APPROVED                            P1 -- protect both prefixes identically
SEC-DEC-04  APPROVED                            both research APIs, AUTHENTICATED_RESEARCH_API
SEC-DEC-05  APPROVED_WITH_LIMITATIONS            Option C nonproduction prototype first
SEC-DEC-06  APPROVED_WITH_LIMITATIONS            Option B (Entra/OIDC) long-term target
SEC-DEC-07  60_DAYS                              review before day 45, no auto-extend
SEC-DEC-08  NAMED_INDIVIDUAL_ACCOUNTS_ONLY        no shared account, no self-registration
SEC-DEC-09  APPROVED_WITH_LIMITATIONS             conservative IP-based limiting, pending prototype-tested thresholds
SEC-DEC-10  APPROVED_WITH_LIMITATIONS             separate maintenance window, defined rollback triggers
```

## 3. Current Architecture (unchanged by this spec)

```text
Cloudflare (edge TLS)
→ silida.org:443 (host nginx, native systemd, Cloudflare Origin Cert)
→ /atlas/ and /westkust/ location blocks, both proxy_pass http://127.0.0.1:8084/
→ voc_nginx (Docker, currently published 0.0.0.0:8084 -- N1 changes this to 127.0.0.1 only)
→ frontend:8001 (Django) / backend:8000 (FastAPI) -- Docker-internal, expose-only, unaffected
```

## 4. Protected Routes

```text
/atlas/riset/pemodelan/
/atlas/riset/pemodelan/panduan/
/atlas/linimasa/
/westkust/riset/pemodelan/
/westkust/riset/pemodelan/panduan/
/westkust/linimasa/
```

All six protected identically (P1), per SEC-DEC-03.

## 5. Protected APIs

```text
/api/research/linimasa
/api/research/pemodelan-dashboard
```

Both classified `AUTHENTICATED_RESEARCH_API` (SEC-DEC-04). Shared-consumer audit (SEC-1) confirmed no other page depends on either — no public/private response split required.

## 6. N1 Containment Change (specification, not applied)

```text
docker-compose.yml, service "nginx":
  ports:
    - "8084:80"
  ->
  ports:
    - "127.0.0.1:8084:80"
```

This is the *entire* scope of the N1 change — no other line in `docker-compose.yml` is touched. See §23 for preconditions before this may be applied.

## 7. Dual-Prefix Policy (P1)

Each of the six protected routes in §4 gets its own nested, path-specific `location` block inside the existing `/atlas/`/`/westkust/` parent blocks — not a blanket lock on the parent prefix (which also serves out-of-scope public pages). Each new block repeats the parent's `proxy_redirect`, `X-Forwarded-*` headers, and `sub_filter` rules (nginx does not inherit these into a more-specific child match). Full precedence/regex reasoning: `PRODUCTION_RESEARCH_PAGE_DUAL_PREFIX_AND_API_POLICY.md` §2.

## 8. Basic Auth Location-Block Design (pseudocode, redacted)

```nginx
# ILLUSTRATIVE — not applied to any file this turn
location /atlas/linimasa/ {
    auth_basic "Restricted";
    auth_basic_user_file <path-outside-repo>;   # see section 9
    limit_req zone=host_auth_limit burst=<TBD-by-prototype>;

    add_header Cache-Control "no-store" always;
    add_header X-Robots-Tag "noindex, nofollow" always;

    proxy_pass http://127.0.0.1:8084/;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_redirect / /atlas/;
    sub_filter_once off;
    sub_filter 'href="/' 'href="/atlas/';
    sub_filter "href='/" "href='/atlas/";
}
# mirrored for the other 5 routes in section 4, and (without sub_filter) the 2 APIs in section 5
```

## 9. Secret and htpasswd Handling

- `htpasswd` file lives at a **server-local path outside the git-tracked repository tree** — no specific path is committed to this document (per the "do not disclose sensitive topology" boundary of this turn's instructions); the actual path is chosen at implementation time and recorded only in a location outside version control (e.g., a server-local runbook, not this repo).
- File permissions target: root-owned, group/world access denied or limited to the nginx worker's own group only — exact mode confirmed against the running nginx worker identity at implementation time, not specified further here.
- No password, hash, or file content is reproduced anywhere in this specification.

## 10. Named Account Policy

Per SEC-DEC-08: one `htpasswd` entry per named individual person. No shared account, no self-registration during the pilot. The actual list of names/usernames is **not** part of this specification — it is provisioning data, decided and entered at implementation time by whoever is authorized to run that step, not by this design document.

## 11. Rate Limiting

Per SEC-DEC-09: initial policy is conservative IP-based limiting at the host-nginx layer (a *new* `limit_req_zone` in `silida.conf`, since the existing Docker-layer zone in `nginx/nginx.conf` does not cover host-nginx-terminated Basic Auth challenges — see the dual-prefix/API policy document, Basic Auth transition plan §1). Exact rate/burst values are explicitly **not finalized** — SEC-DEC-09 records the *direction* (conservative, IP-based) and defers exact thresholds to prototype testing, per the researcher's own instruction.

## 12. Cache and Search Controls

```text
Cache-Control: no-store                    (all six protected routes + both APIs)
X-Robots-Tag: noindex, nofollow            (all six protected routes + both APIs)
```

Supplements, does not replace, the existing per-page `<meta name="robots" content="noindex, nofollow">` tags already present in all three candidate templates (defense in depth, per plan's own instruction not to rely on `robots.txt` alone).

## 13. Local or Production-Like Test Environment

Recommended: a separate Docker Compose stack (or a staging VPS/isolated environment, not the production `westkust-prod` host) running the same `nginx/nginx.conf` + application images, with a **locally generated, throwaway** `htpasswd` file and test-only accounts, so that N1 and Basic Auth behavior can be verified end-to-end (including the direct-port-closure test) without touching the live production server. This environment does not exist yet and is not created by this specification.

## 14. Test Matrix

Inherits the plan's own test matrix (`PLAN_PRODUCTION_RESEARCH_PAGE_ACCESS_CONTROL.md` §20) scoped to Option C + N1:

**Authentication:** valid login (200 after correct credentials), invalid password (401), unknown user (401, generic message — no user-enumeration difference from invalid-password case).
**Authorization:** all six §4 routes and both §5 APIs deny anonymous access (401 with `WWW-Authenticate` challenge); the four out-of-scope research pages and the public root remain unauthenticated (200).
**Proxy:** both `/atlas/...` and `/westkust/...` variants of all six routes challenge identically; no duplicate-prefix bug; `proxy_redirect` correctly rewrites `Location:` headers through the auth-protected block (not just the parent).
**Network:** `curl http://<VPS-IP>:8084/...` (or the test environment's equivalent) fails to connect after N1 is applied, for both protected and previously-public routes alike (confirms N1 closes the exposure for the *whole* app, not just the protected subset).
**Regression:** public Atlas routes, map, and the four out-of-scope research pages unchanged; five ontology validators still pass (§ Phase 8 of this turn); no database migration triggered.

## 15. Negative Tests

- Request a protected route with **no** `Authorization` header → expect 401, not a silent pass-through.
- Request a protected route with a **malformed** `Authorization: Basic ...` header → expect 401, not a 500.
- Request `/api/research/linimasa` directly (bypassing the HTML page) with no credentials → expect 401 (confirms API-level enforcement, not just page-level).
- Request via the **no-trailing-slash** variant (`/atlas/linimasa`) → expect the auth challenge to occur before or during the `APPEND_SLASH` redirect chain, not only after it.
- Request with an **alternate `Host` header** (e.g., the bare VPS IP or a spoofed `Host:` value while still hitting `silida.org`'s IP) → expect this to still resolve to the `silida.org` server block (nginx `server_name` matching), not fall through to a default/unprotected server block — to be explicitly verified in the test environment, not assumed.
- Confirm **no** source map, static bundle, or cached response leaks protected content to a request that fails auth (static assets used by the protected pages are generic/public per SEC-0 discovery §4.3, so this test is expected to pass trivially, but is still run explicitly).
- After N1 is applied in the test environment: confirm direct-port access fails for **every** route, not only the six newly protected ones — proves containment is boundary-wide, not auth-specific.

## 16. Rollback Procedure

**N1:** revert `ports: - "127.0.0.1:8084:80"` to `"8084:80"` in `docker-compose.yml`; `docker compose up -d nginx` (single-service recreation, per network containment plan §2).
**Basic Auth:** remove the added `location` blocks, `auth_basic`/`auth_basic_user_file`/`limit_req` lines from `silida.conf`; `nginx -t`; `systemctl reload nginx` (reload, not restart, to avoid dropping unrelated in-flight connections) — per Basic Auth transition plan §3.
Both rollbacks are independent — either can be reverted without requiring the other to also be reverted, since N1 and the Basic Auth location blocks are separate, non-interlocking changes.

## 17. Maintenance-Window Requirements

Per SEC-DEC-10: a separately authorized maintenance window is required before any of this spec's changes are applied to production — not granted by this specification itself. Window should be scheduled to allow immediate rollback (§16) within the window if any of the SEC-DEC-10 rollback triggers occur (public-route regression, auth bypass, API exposure, redirect loop, upstream failure, direct-port exposure, or cache leakage).

## 18. Credential Provisioning Procedure (specification, not execution)

Per the access-control plan's own §7.4 (bootstrap admin requirements) adapted for Option C's simpler `htpasswd` mechanism:
1. Generate each named account's password via a secure, non-interactive method that does not print the password to a terminal that gets logged, and does not write it to shell history.
2. Hash immediately using `htpasswd`'s own bcrypt/MD5-apr1 mechanism (not a custom hash) — do not store or transmit any plaintext password after generation.
3. Deliver each person's credential to them via a channel separate from this repository and separate from any terminal output captured in a Claude Code session transcript.
4. Record only the *fact* of provisioning (who, when) in a security log (§19) — never the credential value itself.
This procedure is specified for future execution; **no step in it was performed this turn.**

## 19. Security Logging

Given Basic Auth's inherent limitation (no structured login/logout event stream — nginx logs only which `htpasswd` username authenticated per request, per SEC-0 threat model §1), the prototype's minimum logging target is: nginx access log entries showing username + route + status code (already nginx's default behavior once `auth_basic` is active, no extra configuration needed), reviewed manually or via a log-aggregation step during the pilot — full structured audit-event logging (login success/failure as discrete events, per plan §13) is deferred to the Option B (Entra/OIDC) implementation, where IdP-side sign-in logs plus application-side authorization-decision logging can satisfy that requirement more completely.

## 20. Known Limitations

- No true logout — browsers cache Basic Auth credentials until manually cleared.
- No per-user session expiry — a cached browser credential remains valid until the `htpasswd` entry is removed or the pilot expires (§22).
- No MFA.
- No role distinction (RESEARCHER/REVIEWER/ADMIN) — Basic Auth accounts are flat, undifferentiated.
- Credential rotation is manual (`htpasswd` file edit + reload).
- This is explicitly a stopgap, not a destination architecture, per the plan's own framing and SEC-DEC-06's Entra/OIDC long-term target.

## 21. Entra/OIDC Migration Trigger

Migration to Option B (SEC-DEC-06) is triggered by whichever comes first: (a) the 60-day expiry (§22) being reached without a renewed researcher decision, or (b) a researcher decision to proceed directly to Option B implementation ahead of expiry, or (c) any of the known limitations in §20 becoming operationally unacceptable during the pilot (e.g., a role distinction becomes necessary). No automatic migration occurs — each trigger requires an explicit researcher decision to act on it.

## 22. Sixty-Day Expiry

Per SEC-DEC-07: 60 days from production activation (not yet activated — no start date exists yet since Option C has not been deployed). Review required before day 45. No automatic extension — continuing past day 60 without a fresh researcher decision is out of policy. The expiry date, once activation occurs, should be recorded both in a `silida.conf` comment (illustrative, per Basic Auth transition plan §1) and updated into the security decision ledger.

## 23. Implementation Preconditions

Before any code/config for this spec is written to a real file (local prototype, Phase SEC-2):
1. This specification itself reviewed and not objected to by the researcher.
2. N1 test environment available (§13).
3. Named account list (§10) supplied by the researcher or their delegate — not fabricated by an agent.
4. Rate-limit starting parameters (§11) drafted for prototype testing.

## 24. Production Preconditions

Before any of this spec's changes are applied to the **production** `westkust-prod` server:
1. Local/prod-like prototype (§13) built and all §14 tests + §15 negative tests passing.
2. N1 validated in the isolated test environment first (containment is the researcher's own stated non-negotiable prerequisite — "containment port 8084 bukan opsional").
3. Maintenance window (§17) separately authorized.
4. A separate, explicit "authorize production implementation" decision — not implied by SEC-DEC-01 through SEC-DEC-10, which authorize *design and prototype work only*.

## 25. Final Nonauthorization Statement

```text
This specification authorizes design, review, and future nonproduction prototype
work only. It does not authorize:
  - writing any Basic Auth configuration to docker-compose.yml or silida.conf;
  - generating any htpasswd file, username, or password;
  - closing port 8084 on the production server;
  - any restart, rebuild, or recreation of any production container or service;
  - any production deployment of any kind.

IMPLEMENTATION: NOT_AUTHORIZED
PRODUCTION DEPLOYMENT: NOT_AUTHORIZED
SECURITY GATE: NOT_PASSED
```
