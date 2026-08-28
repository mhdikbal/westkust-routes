# ATLAS /westkust/ Route Retirement — Decision Adjudication

> **Decision-recording turn only. No redirect implemented. No Nginx, source, API, Basic Auth, CARTO, or port-8084 change. Nothing staged, committed, or pushed.**

---

## 1. Scope

Records the researcher's adjudication of the six implementation decisions left open by `ATLAS_WESTKUST_ROUTE_RETIREMENT_AUDIT.md` § 6 ("Remaining Decisions"), which were carried forward as recommendations-only during the controlled local freeze. This turn converts those recommendations into recorded decisions in a dedicated ledger. It authorizes no implementation.

## 2. Authoritative Baseline

```text
Route-retirement planning commit: 15178c9b3f13801141ab77c3d4ad979590ee4c47
Status: ATLAS_WESTKUST_ROUTE_RETIREMENT_PLAN_PUSHED_AND_SERVER_SYNCED
```

## 3. Current Production State

```text
/atlas/:     serves the application (200, live-verified)
/westkust/:  serves the same application (200, live-verified)
Redirect:    not implemented
Nginx:       unchanged
Production:  unchanged
```

## 4. Canonical Route Decision

`/atlas/` is the canonical public application route. `/westkust/` will become a redirect-only legacy compatibility route. This classification was already established (`ROUTE-DEC-01`, `ATLAS_WESTKUST_ROUTE_RETIREMENT_AUDIT.md` § 1) and is not re-adjudicated here — it is the fixed premise under which the six decisions below were made.

## 5. Redirect Syntax Decision

`ROUTE-IMPL-DEC-01` — **APPROVED_WITH_LIMITATIONS**. A simple Nginx `return`-based `301` redirect, preserving the suffix path and query string exactly once (`/westkust/` → `/atlas/`; `/westkust/<path>` → `/atlas/<path>`; `/westkust/<path>?<query>` → `/atlas/<path>?<query>`). Required safeguards: no open redirect; no `/atlas/atlas/` duplication; no `/westkust/westkust/` duplication; no query-string duplication; `GET`/`HEAD` validated; non-`GET` behavior separately reviewed; syntax tested in a disposable configuration first. The exact directive form (`return` vs. a `location ~` regex-capture block) remains to be finalized during the disposable rehearsal — this decision approves the *direction*, not a copy-paste-ready snippet. Production execution not authorized by this decision.

## 6. Static Asset Decision

`ROUTE-IMPL-DEC-02` — **APPROVED_WITH_LIMITATIONS**. `/westkust/` will not be preserved as a long-term static-application path. Legacy static-asset requests may be redirected only after compatibility testing (the `RETIRE-CAND-*` static-asset smoke tests) proves asset loading remains correct. Safeguards: no global replacement of the word "westkust" anywhere in the repository (repository name, service name, hostname, filesystem paths, and historical documentation are unaffected unless they are active public URL references); no state where an `/atlas/`-served page depends on a `/westkust/`-served asset or vice versa. Production execution not authorized by this decision.

## 7. Observation Period

`ROUTE-IMPL-DEC-03` — **APPROVED**. A 30-day observation period after any future production activation, with review points at Day 0, Day 1, Day 7, Day 14, and Day 30. Monitored items: legacy route traffic, deep-link distribution, redirect status codes, redirect loops, `404` results, asset failures, query-string preservation, and authentication consequences. This decision governs *what will be monitored if and when* execution is separately authorized (`ROUTE-IMPL-DEC-05`) — it does not itself start any monitoring, since no redirect is active.

## 8. SEO Decision

`ROUTE-IMPL-DEC-04` — **DEFERRED**. Full SEO/canonicalization infrastructure (sitemap implementation, robots infrastructure, full canonical metadata system, search-console integration, automated SEO pipeline) is deferred to a separate milestone, consistent with the discovery finding that no such infrastructure currently exists anywhere in the application (`ATLAS_WESTKUST_ROUTE_RETIREMENT_DISCOVERY.md` § 3). Required future direction once that milestone is undertaken: public navigation uses `/atlas/`; `/atlas/` is canonical; `/westkust/` is not canonical; protected research routes remain outside any public sitemap.

## 9. Production Execution Decision

`ROUTE-IMPL-DEC-05` — **NOT_AUTHORIZED**. This is the governing decision: `ROUTE-IMPL-DEC-01/02/03/04` are design and planning decisions only, and none of them individually or collectively authorizes execution. Execution remains blocked until all of the following exist and pass: an exact production candidate diff; a disposable redirect rehearsal that passes; static-path validation; non-`GET` behavior review; complete backup and rollback preparation; an approved maintenance window; recorded operator and rollback authority; approved production smoke and negative tests; and confirmation that no unrelated production diff is pending. None of these preconditions are satisfied as of this turn.

## 10. Basic Auth Bundling Decision

`ROUTE-IMPL-DEC-06` — **REJECTED**. Route retirement will not be bundled with Basic Auth implementation. Required sequence, each stage independently validated before the next begins:

```text
R1: route retirement redirect       -> STOP and validate
R2: N1 port containment              -> STOP and validate
R3: Basic Auth (protected /atlas/ pages + both research APIs) -> STOP and validate
```

## 11. Dependency Order

Redirect implementation path (technical prerequisite chain — not an authorization):

```text
redirect candidate syntax
  -> disposable rehearsal
  -> static-asset validation
  -> non-GET review
  -> exact production diff
  -> backup and rollback
  -> maintenance authorization
  -> production execution decision
```

Separate future workstream sequence (also not an authorization; independent tracks per `ROUTE-IMPL-DEC-06`):

```text
route retirement -> N1 containment -> Basic Auth -> CARTO remediation -> SEO infrastructure
```

## 12. Implementation Preconditions

All preconditions carried forward from `ROUTE-IMPL-DEC-05`: exact production candidate diff; disposable rehearsal pass; static-path validation; non-`GET` review; backup/rollback completion; approved maintenance window; recorded operator and rollback authority; approved smoke and negative tests; no unrelated production diff present. None are satisfied at this turn — this section records the checklist, not its completion.

## 13. Rollback Preconditions

A full `silida.conf` backup and `nginx -t` syntax validation are required before any future reload, following the same pattern established in every prior SEC-3/SEC-3A rollback runbook in this series. Rollback trigger conditions (redirect loop, lost query strings, broken deep links, static-asset failure, `/atlas/` unavailability, authentication bypass, API regression, unexpected non-`GET` behavior) remain as recorded in `ATLAS_WESTKUST_ROUTE_RETIREMENT_AUDIT.md` § 5 and are not re-decided here.

## 14. Remaining Open Items

- Exact Nginx directive syntax (`return` vs. regex-capture `location` block) — to be finalized in the disposable rehearsal, not this turn.
- Static-asset compatibility test execution — not yet run.
- Exact maintenance window and named operator/rollback authority — not yet assigned.
- Production candidate diff — does not yet exist.
- SEO milestone scheduling — deferred, no date set.

## 15. Production Gate Status

```text
PRODUCTION: NO_GO (unchanged)
SECURITY_ACCESS_CONTROL_GATE: NOT_PASSED (unchanged)
Redirect: NOT_IMPLEMENTED
Port 8084: unchanged
Basic Auth: still not implemented
CARTO key: absent
```

## 16. Final Decision Summary

```text
ROUTE-IMPL-DEC-01: APPROVED_WITH_LIMITATIONS  (redirect syntax direction)
ROUTE-IMPL-DEC-02: APPROVED_WITH_LIMITATIONS  (static asset handling)
ROUTE-IMPL-DEC-03: APPROVED                   (30-day observation period)
ROUTE-IMPL-DEC-04: DEFERRED                   (SEO infrastructure)
ROUTE-IMPL-DEC-05: NOT_AUTHORIZED             (production execution)
ROUTE-IMPL-DEC-06: REJECTED                   (Basic Auth bundling)
```

All six decisions carry `implementation_authorized = NOT_AUTHORIZED`. No decision claims the redirect is active. No production, Nginx, source, or API change resulted from this turn.

---

## Final Status

```text
ATLAS_WESTKUST_ROUTE_RETIREMENT_DECISIONS_RECORDED
```
