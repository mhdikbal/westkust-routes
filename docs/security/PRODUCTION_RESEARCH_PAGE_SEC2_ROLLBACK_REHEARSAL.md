# Production Research Page — SEC-2 Rollback Rehearsal

> **Phase:** SEC-2, Phase 12 (rollback rehearsal, isolated workspace only)
> **Baseline:** `e813192b590917a7f96b9e3ca7da5c8c9a907be8`

---

## 1. Purpose

Demonstrate — against the disposable test workspace only — that every change modeled in SEC-2 (N1 binding, dual-prefix Basic Auth blocks) can be fully reversed without touching any other data or service, before any of these changes are considered for production.

## 2. Rehearsal Steps and Results

| Step | Action | Verification | Result |
|---|---|---|---|
| 1 | Capture pre-rollback checksums of the test `host_proxy/nginx.conf` and `backend/conf_n1/nginx.conf` | SHA-256 recorded | RECORDED (test-workspace file, deleted at cleanup — checksum values were session-local reference points only, not carried into any repository file) |
| 2 | Revert Basic Auth blocks — swap the host proxy to a no-auth baseline config, recreate the container | `GET /atlas/linimasa/` returns 200 with no auth challenge | **PASS** |
| 3 | Restore pre-N1 binding — swap the backend to the `conf_current` (0.0.0.0) config, recreate the container | loopback access = 200, LAN-IP access = 200 (both restored) | **PASS** |
| 4 | Confirm only the two disposable test containers were ever recreated | Production `docker compose ps` shows backend/frontend Up 30h, db Up 8 weeks, nginx Up 5 weeks, redis Up 7 weeks — no restart, monotonic uptime progression from the turn's own precondition check (29h) | **PASS** |

## 3. Cleanup Verification (Phase 15, cross-referenced)

Performed immediately after the rehearsal, before writing this report:

```text
Disposable containers removed:    sec2_backend, sec2_hostproxy -- confirmed via `docker rm -f`, then `docker ps -a --filter name=sec2_` returned empty
Test ports no longer listening:    confirmed via `ss -tln | grep -E ':18084|:18085'` -- no match
Credential material deleted:       htpasswd file removed (shred -u, falling back to rm) before workspace deletion
Temporary workspace deleted:       `rm -rf` on the full /tmp/westkust-auth-sec2-<timestamp>/ path -- confirmed absent afterward
No dangling test-specific image:   only the generic, reusable httpd:2.4-alpine base image remains pulled locally (no test data baked into it) -- left in place as ordinary local Docker cache, not test output
```

## 4. What Rollback Did Not Need to Touch

At no point in this rehearsal was any of the following read, written, or restarted: production `docker-compose.yml`, production `silida.conf`, production `nginx/nginx.conf`, the production database, production application code, or any production container. The rehearsal exercised only the two disposable containers created for this turn.

## 5. Conclusion

Both reversible actions modeled by SEC-2 (Basic Auth block removal, port-binding restoration) were rehearsed successfully in isolation. This is a rehearsal of the *design* documented in `PRODUCTION_RESEARCH_PAGE_NETWORK_CONTAINMENT_PLAN.md` §2 (N1 rollback) and `PRODUCTION_RESEARCH_PAGE_BASIC_AUTH_TRANSITION_PLAN.md` §3 (Basic Auth rollback) — it demonstrates the *mechanism* works as designed in miniature; it does not itself constitute a production rollback test, which remains a Phase SEC-3+ activity against a production-like (not production) environment.
