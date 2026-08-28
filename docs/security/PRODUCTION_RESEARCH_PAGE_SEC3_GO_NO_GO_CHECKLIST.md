# Production Research Page — SEC-3 Go/No-Go Checklist

> **This checklist is not a decision record. No box below has been checked by this turn — it is the criteria list for a future, separately authorized SEC-4 go/no-go review.**

---

## GO — only if every item below is true

- [ ] Exact diff reviewed by the researcher (`PRODUCTION_RESEARCH_PAGE_SEC3_CANDIDATE_DIFF.md` §A–F)
- [ ] Option A credential store explicitly approved (`SEC-DEC-11`, currently `PENDING_RESEARCHER_DECISION` — see `PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md` §1)
- [ ] File owner/group/mode approved (design proposes `0640` + matching container GID as target, `0644` as the verified-safe fallback — see credential-store design §3)
- [ ] Pilot-user list approved (named individuals, per `SEC-DEC-08`)
- [ ] Secure delivery channel approved (`PRODUCTION_RESEARCH_PAGE_SEC3_ACCOUNT_PROVISIONING_RUNBOOK.md` §2 item 11)
- [ ] Rate-limit threshold approved for the newly-protected routes specifically (not just the reused `api_limit` zone default — see candidate diff §F)
- [ ] Maintenance window approved (date, time, duration)
- [ ] Backups completed (`silida.conf`, `nginx/nginx.conf`, `docker-compose.yml`, immediately before the change)
- [ ] Rollback commands validated against the real production host (not just the disposable rehearsal — this turn only rehearsed rollback in a disposable environment, `SEC3-ROLLBACK-001`)
- [ ] `nginx -t` passes on both the real candidate `silida.conf` and the real candidate `nginx/nginx.conf`, on the actual host/container
- [ ] `docker compose config` renders the candidate `docker-compose.yml` without error
- [ ] Production-like test matrix passes against a production-like (not production) environment (SEC-3's own disposable rehearsal is a prerequisite input, not a substitute for this step)
- [ ] No bypass found (location-precedence, missing/repeated slash, encoded path, duplicated prefix — and specifically, the real Django app's actual behavior on a duplicated-prefix path like `/atlas/atlas/...` has been confirmed, resolving the `PASS_WITH_LIMITATION` finding at `SEC3-PREC-006`/`007`)
- [ ] Monitoring owner assigned
- [ ] Day-45 review owner assigned (`SEC-DEC-07`)

## NO-GO — any one of these is sufficient to block

- [ ] One prefix (`/atlas/` or `/westkust/`) is unprotected
- [ ] One research API is public
- [ ] Port 8084 remains externally reachable after the candidate N1 change
- [ ] Inner loopback boundary is absent (direct same-host access to a protected inner route succeeds unauthenticated)
- [ ] Credential file is world-readable
- [ ] A duplicate/second interactive authentication prompt persists in normal browser use
- [ ] Protected body content leaks in any unauthorized response
- [ ] Cache behavior is unsafe (an intermediary can cache protected content)
- [ ] Rollback cannot complete cleanly
- [ ] Any unrelated production diff exists at the time of the change window

## Current Status of Every GO Item (as of this SEC-3 turn)

| GO item | Status |
|---|---|
| Exact diff reviewed | Diff produced this turn; researcher review not yet performed |
| Option A approved | `PENDING_RESEARCHER_DECISION` |
| Owner/group/mode approved | Design proposed, not approved; GID-matching mechanics flagged as unresolved for a stock image |
| Pilot-user list approved | Does not exist yet |
| Secure delivery channel approved | Not yet decided |
| Rate-limit threshold approved | Not finalized (candidate diff §F reuses the existing zone as a starting point only) |
| Maintenance window approved | Not scheduled |
| Backups completed | Not yet — no production change has occurred to back up around |
| Rollback commands validated on real host | Not yet — only disposable-environment rehearsal this turn |
| `nginx -t` passes on real candidate configs | Not yet run against the real files — only against the rehearsal's structurally-equivalent candidates |
| `docker compose config` renders | Not yet run against the real candidate Compose file |
| Production-like test matrix passes | This turn's disposable rehearsal passed 41 PASS / 2 PASS_WITH_LIMITATION (0 FAIL) — see test results; a production-like (not production) run is still required |
| No bypass found | No bypass with actual data leakage found; two `PASS_WITH_LIMITATION` findings require the real-Django follow-up noted above |
| Monitoring owner assigned | Not yet |
| Day-45 review owner assigned | Not yet |

**Net result: GO conditions are not yet met.** This is expected — SEC-3 is planning and rehearsal, not the gate itself. The gate is `SEC-4`. Production must remain, at minimum, because: Option A credential store is not finally approved; the production user list is absent; the credential delivery channel is undecided; the actual server UID/GID permission model is unverified (see `PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md` §3); duplicated-prefix behavior needs real-Django verification (`SEC3-F-01`); Cloudflare real-IP restoration is unresolved (`SEC3-F-02`); the maintenance window is not approved; no production backup has been taken; the production Nginx and Compose changes have not been reviewed for execution; external production negative tests have not run; and the security gate remains `NOT_PASSED`.

```text
PRODUCTION: NO_GO
SECURITY_ACCESS_CONTROL_GATE: NOT_PASSED
```

This status ("plan ready for review") is not, and must not be reinterpreted as, deployment readiness.
