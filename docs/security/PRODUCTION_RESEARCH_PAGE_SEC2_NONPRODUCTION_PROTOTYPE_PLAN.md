# Production Research Page — SEC-2 Nonproduction Prototype Plan & Execution Record

> **Phase:** SEC-2 (isolated, nonproduction prototype — executed this turn)
> **Baseline:** `e813192b590917a7f96b9e3ca7da5c8c9a907be8`
> **Status:** `SEC2_NONPRODUCTION_PROTOTYPE_PASS` (see §8 for exact scope of this status)
> **This document describes and records an isolated test-workspace exercise. No production system was modified.**

---

## 1. Purpose

Build and run, entirely outside the repository and outside production, a disposable prototype that empirically tests the four things the researcher named as required before production is considered:

1. N1: host proxy can still reach the upstream via loopback after binding it to `127.0.0.1` only.
2. Direct access cannot bypass the host proxy under N1.
3. The dual-prefix + two-API boundary produces a consistent challenge.
4. Every change is reversible without touching other data or services.

## 2. Precondition Verification (Phase 1)

All eight preconditions checked and passed before the prototype was built:

```text
Local HEAD:                e813192b590917a7f96b9e3ca7da5c8c9a907be8
origin/main:                e813192b590917a7f96b9e3ca7da5c8c9a907be8
Server HEAD:                e813192b590917a7f96b9e3ca7da5c8c9a907be8
Production tracked tree:    clean
Ontology ledger diff:       unchanged (5 insertions / 5 deletions, same as prior turns)
11 security files:          all checksums match the frozen commit values
Five ontology validators:   Painan 23/23, Natal 28/28, Koto Tangah 34/34, Tiku 35/35, Sillida 32/32 -- all PASS
Production containers:      backend/frontend Up 29h, db Up 8 weeks, nginx Up 5 weeks, redis Up 7 weeks -- no active deployment
```

## 3. Temporary Workspace

```text
Path (deleted at cleanup):  /tmp/westkust-auth-sec2-<timestamp>/
Contents:                    backend/ (dummy content + nginx configs), host_proxy/ (nginx config),
                              htpasswd/ (ephemeral credential, deleted at cleanup), results/ (unused, superseded by scratchpad CSVs)
```

**Manifest of what was placed in the workspace** (all newly authored for this test, nothing copied from production credential/cert/session material):

| Item | Source | Redaction |
|---|---|---|
| `backend/nginx.conf` template | newly authored, modeled on the *structure* of `nginx/nginx.conf`'s location-block pattern | no production content copied |
| `backend/html/*` dummy pages/APIs | newly authored placeholder content | no production content copied |
| `host_proxy/nginx.conf` | newly authored, modeled on the *structure* of `silida.conf`'s `/atlas/`, `/westkust/`, and `/api/` location blocks (from the read-only SEC-0 discovery notes, not by copying the live file) | no domain name, no certificate path, no real upstream address beyond the test's own loopback ports |
| `htpasswd/sec2_test.htpasswd` | freshly generated inside the workspace via a disposable `httpd:2.4-alpine` container | synthetic username (`sec2_test_user_*`), random 24-character password, bcrypt hash only — plaintext never written to any file |

**Nothing copied:** `.env`, TLS certificates/keys, production `htpasswd` (does not exist in production yet), database files, session secrets, tokens, cookies, or any credential value.

## 4. Prototype Topology (Phase 3)

```text
Test client (curl, this session)
  -> test host proxy   (nginx:1.25-alpine, --network host, listen 127.0.0.1:18085)
     -> test backend    (nginx:1.25-alpine, --network host, listen {0.0.0.0|127.0.0.1}:18084 -- swapped per test phase)
        -> dummy protected pages and dummy API JSON responses
```

`--network host` (native Linux Docker networking, available in this WSL2 environment) was used so the test host proxy reaches the test backend exactly the way production's *native, non-containerized* host nginx reaches Docker's `voc_nginx` — via a host-loopback-published port, not via Docker's internal bridge network. This mirrors the network-containment plan's own finding that host nginx is not a Docker network member.

Test-only ports: `127.0.0.1:18084` (backend), `127.0.0.1:18085` (host proxy) — neither collides with production's `8084`.

Topology included: one `/atlas/`-equivalent prefix, one `/westkust/`-equivalent prefix, three candidate protected page paths under each (six total), two protected research API paths, and one public control route (`/control/public`) that remained unauthenticated throughout.

## 5. N1 Containment Simulation (Phase 4) — Result

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | Loopback access, current (0.0.0.0) state | 200 | 200 | PASS |
| 2 | Non-loopback access, current (0.0.0.0) state | 200 (reproduces the bypass) | 200 | PASS |
| 3 | Loopback access, N1 (127.0.0.1) state | 200 | 200 | PASS |
| 4 | Non-loopback access, N1 (127.0.0.1) state | Connection refused | Connection refused (curl exit 7) | PASS |
| 5 | Host proxy reaches N1-bound loopback upstream | 200 | 200 | PASS |
| 6 | Rollback to pre-N1 binding restores original behavior | loopback=200, LAN=200 | loopback=200, LAN=200 | PASS |
| 7 | Isolated service recreation sufficient | only the disposable backend container recreated per swap | confirmed — single `docker rm`/`docker run` per swap, no other service touched | PASS |

Full evidence: `PRODUCTION_RESEARCH_PAGE_SEC2_TEST_RESULTS.csv`, rows SEC2-T-001 through SEC2-T-005 and SEC2-T-042.

**This is the core empirical result of SEC-2: N1 (bind the published port to loopback only) behaves exactly as the network containment plan predicted — loopback access is preserved for the legitimate host-proxy path, and non-loopback access is refused outright, with no partial or ambiguous behavior observed.**

## 6. Dummy Credential Generation (Phase 5)

```text
DUMMY_CREDENTIAL_CREATED_IN_EPHEMERAL_TEST_WORKSPACE
```

Username: synthetic, clearly test-scoped (prefix `sec2_test_user_`). Password: 24-character random string generated via Python's `secrets` module, held only in shell-process memory during generation and test execution, never written to any file, never printed to any command output captured in this session's transcript, never entered shell history as a standalone recoverable value (used only as an inline `curl -u` argument within single, non-logged tool invocations). Hash: bcrypt, via `httpd:2.4-alpine`'s `htpasswd -nbB`, written only to `<workspace>/htpasswd/sec2_test.htpasswd` (mode 644 for container readability, deleted at cleanup — see §9 for the permission-mode finding this surfaced).

## 7. Boundary, API, Path-Variant, Negative, and Rate-Limit Test Results

Full results (43 test rows) are in `PRODUCTION_RESEARCH_PAGE_SEC2_TEST_RESULTS.csv`. Summary:

```text
PASS:                   40
PASS_WITH_LIMITATION:    1  (SEC2-T-029, alternate-Host-header — test topology limitation, see negative test report)
INFORMATIONAL_FINDING:   1  (SEC2-T-030, direct-loopback-to-backend residual gap — see negative test report)
FAIL:                    1  (SEC2-T-040, rate-limit test-sequencing artifact — see negative test report)
```

All six protected page paths (both prefixes) and both protected APIs produced a **consistent** 401 challenge when anonymous, 401 when given invalid credentials, and 200 when given valid dummy credentials — with `Cache-Control: no-store` and `X-Robots-Tag: noindex, nofollow` present on both the 401 and 200 responses. The public control route remained unauthenticated throughout every phase.

## 8. Rollback Rehearsal (Phase 12) — Result

All four rehearsal steps passed: Basic Auth blocks reverted cleanly (protected route returned to unauthenticated 200), pre-N1 binding restored cleanly (both loopback and LAN access returned to 200), only the two disposable test containers were ever created or recreated, and production container uptime was confirmed unchanged (monotonic progression only — 29h→30h across the turn's wall-clock duration, no restart). Full detail: `PRODUCTION_RESEARCH_PAGE_SEC2_ROLLBACK_REHEARSAL.md`.

## 9. Operational Findings Worth Carrying Into Implementation Planning

Two things were learned empirically this turn that were not fully anticipated in the SEC-1 design documents:

1. **htpasswd file permission mode matters more precisely than "root-readable or least-privilege."** The first test run failed with HTTP 500 across every authenticated request because the file was `chmod 600` owned by the host user, unreadable by the containerized nginx worker's own user. Production implementation must confirm the exact UID/GID the live nginx worker runs as (host-native, not containerized, per the SEC-1 network trace) and set permissions accordingly — this was previously flagged as "TBD" in the nonproduction implementation spec (§9) and is now confirmed as a concrete, must-verify step, not a hypothetical one.
2. **Direct same-host loopback access to the backend remains unauthenticated even under N1** (SEC2-T-030). N1 closes *remote* exposure; it does not add authentication at the backend/app layer itself. This empirically confirms the ADR's own "Cross-Cutting Prerequisite" reasoning — a proxy-only enforcement design has a residual, same-host gap that only an application-layer check (or accepting that same-host access is a materially lower-trust boundary than remote access) would close.

Both are carried into the negative-test report (§ findings) and are recommended reading before Phase SEC-3.

---

## Not Performed This Turn

No production `docker-compose.yml`, `silida.conf`, or `nginx/nginx.conf` edit. No production container recreation, restart, or reload. No real username, password, or htpasswd created or provisioned. No Entra/OIDC configuration. No staging, commit, or push.
