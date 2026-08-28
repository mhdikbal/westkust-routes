# Production Research Page — SEC-3B Rate-Limit Analysis

> **Analysis of a test-environment failure. No production rate-limit conclusion is drawn from this document.**

---

## 1. What Was Observed

Across three separate sessions (SEC-3, SEC-2A, SEC-3A, and now SEC-3B), the identical `nginx` `limit_req` shared-memory-zone rate-limiting mechanism was configured multiple times, with multiple different thresholds, in multiple different disposable containers and networks:

| Session | Config | Result |
|---|---|---|
| SEC-2A | `rate=2r/s burst=3 nodelay` | **Enforced correctly** — real `401`/`503` mix observed |
| SEC-3 | reused production's `api_limit` zone (`60r/m burst=20 nodelay`) | **Enforced correctly** — `200×21, 429×4` on a 25-request burst |
| SEC-3A (initial attempt) | `rate=5r/s`, then `1r/s`, `burst=2-3 nodelay` | **Did not enforce** — all requests `200` |
| SEC-3A (isolation control) | `rate=1r/m`, no burst | **Did not enforce** — 3/3 requests `200` |
| SEC-3B (this turn, brand-new container/network) | `rate=1r/m`, no burst | **Did not enforce** — 10/10 requests `200` |

## 2. Root-Cause Reconfirmation — Corrected Classification

SEC-3A's audit classified the failure as `TEST_ENVIRONMENT_LIMITATION_REQUIRES_FRESH_STATE`, which implies the problem was specific to that session's accumulated Docker/process state and would clear with a fresh start. **This turn tested that assumption directly and it did not hold**: a container that had never previously existed, on a network created moments before, with a threshold two orders of magnitude stricter than any previously tried, still failed to enforce. Session staleness is therefore ruled out as the (sole) cause.

```text
CORRECTED CLASSIFICATION: NGINX_LIMIT_REQ_MODULE_NOT_ENFORCING_IN_THIS_SANDBOX_PLATFORM
```

This is evidence-bounded to what was directly observed: the `limit_req` mechanism does not enforce in the current sandbox execution environment, independent of session history, threshold value, burst configuration, or zone freshness. It is **not** a claim that:

- `nginx`'s rate-limiting feature is broken in general (it worked correctly in SEC-2A and SEC-3, in this same overall multi-day series, on presumably the same underlying host);
- the trust-boundary / real-IP-restoration design from `PRODUCTION_RESEARCH_PAGE_SEC3A_CLOUDFLARE_REAL_IP_DESIGN.md` is flawed — that design's correctness does not depend on this mechanism actually enforcing in this sandbox, only on the key it would use (`$remote_addr` post-restoration) being derived correctly, which was independently and successfully demonstrated by other SEC-3A tests (`IP-001`, `IP-003`, `IP-004`, `IP-005`);
- production rate limiting fails or would fail — this document draws no conclusion about production, which was never touched and whose Nginx runs on real infrastructure, not this sandbox.

## 3. What Changed Between "It Worked" and "It Stopped Working"

Not determined within this turn's budget. Candidate, unconfirmed causes: a change in the sandbox's container-runtime configuration between sessions; a host-level resource-accounting or cgroup change; a platform restriction on the timer/shared-memory primitives `ngx_http_limit_req_module` depends on (`mmap(MAP_SHARED|MAP_ANON)` and its internal clock sampling) that was introduced or triggered partway through this work. No process, kernel, or Docker-daemon-level diagnostic beyond what is recorded in `PRODUCTION_RESEARCH_PAGE_SEC3B_TEST_RESULTS.csv`'s evidence locators was performed, since none was clearly promising within the narrow SEC-3B scope and remaining budget, and pursuing it further would have exceeded the "do not expand scope" instruction for this phase.

## 4. Consequence

Per the instruction's own explicit contingency, `SEC3A-IP-007`/`SEC3A-IP-008` are not reinterpreted from this invalid environment, and the twelve dependent SEC-3B tests were correctly left `BLOCKED` rather than fabricated. `SEC3-F-02` remains open. This is a genuine limitation of the test environment available to this session, not a security finding about production and not a design defect in the trust-boundary work already completed.

## 5. Rate-Limit Key Recommendation (unaffected by this environment failure)

The recommendation stands, **contingent on eventual live verification in a working environment**:

```text
$binary_remote_addr, after validated trusted real-IP restoration
Recommendation status: RECOMMENDED_WITH_LIMITATIONS
```

Required limitations (unchanged from `PRODUCTION_RESEARCH_PAGE_SEC3A_CLOUDFLARE_REAL_IP_DESIGN.md` § 4, restated here for SEC-3B traceability):

- only trust headers from approved immediate proxy addresses;
- provider load-balancer trust must be verified (the actual immediate peer, `10.1.10.126`, remains classified only as `PRIVATE_PROVIDER_INTERNAL_ADDRESS`, per `SEC3-F-03`);
- Cloudflare/header provenance must be documented;
- IPv4 and IPv6 trust coverage required;
- CIDR/trust-source lifecycle required (`PRODUCTION_RESEARCH_PAGE_SEC3A_CIDR_LIFECYCLE_RUNBOOK.md`);
- direct access must be contained by N1;
- production threshold remains separately approved;
- production logs should retain both immediate and restored address fields;
- privacy review applies to retained client-IP data.

This recommendation is **not implemented in production** by this document.
