# Production Research Page — SEC-3 Production-Like Implementation Plan

> **Phase:** SEC-3 — Production-Like Implementation Planning and Isolated Rehearsal
> **SEC-3 is planning + disposable rehearsal. SEC-3 is NOT a production deployment.**
> **Parent security-planning baseline:** `e813192b590917a7f96b9e3ca7da5c8c9a907be8`
> **SEC-2 evidence baseline:** `38120d250a2b629e86a6c66d0d4be7d0851117b5`
> **SEC-2A evidence baseline:** `1838815fb3314dc9528f3cf4b29f5761c0835b0a`

---

## 1. Scope

This plan turns the validated SEC-2A defense-in-depth prototype into an exact, reviewable production-like implementation package. It was produced against a disposable rehearsal (`sec3_outer` / `sec3_inner`, network `sec3_net`, test ports `127.0.0.1:38084`–`38089`) built from a **real, read-only snapshot** of production's current `docker-compose.yml`, `nginx/nginx.conf` (inner, in this repository), and `/etc/nginx/conf.d/silida.conf` (outer, host-managed, read via SSH). No production file was modified to produce this plan.

## 2. Security Status Entering SEC-3

```text
SEC-0: COMPLETE
SEC-1: COMPLETE
SEC-2: FROZEN AND SERVER-SYNCED (43 tests: 40 PASS, 1 PASS_WITH_LIMITATION, 1 INFORMATIONAL_FINDING, 1 FAIL)
SEC-2A: FROZEN AND SERVER-SYNCED (18/18 PASS)
T-030: MITIGATION_PROTOTYPE_VALIDATED (NOT PRODUCTION_RESOLVED)
T-040: original FAIL retained, SUPERSEDED_BY_SEC2A_RETEST
Production port 8084: still bound to 0.0.0.0
Basic Auth: not implemented in production
SECURITY_ACCESS_CONTROL_GATE: NOT_PASSED
Production deployment: NOT_AUTHORIZED
```

## 3. Real Production Topology (discovered read-only this turn)

Production is **two nginx processes**, not a symmetric pair of identical containers as the SEC-2/SEC-2A prototype modeled by name — the prototype's "outer"/"inner" labels map onto real, structurally different components:

- **Outer = host Nginx** — a native systemd process (`nginx/1.31.2`) on `westkust-prod`, config at `/etc/nginx/conf.d/silida.conf`, owned `root:root`, mode `644`. Terminates TLS for `silida.org` (Cloudflare Origin Certificate), serves the static Astro site from `/var/www/salido/dist`, and reverse-proxies `/api/`, `/westkust/`, and `/atlas/` to `127.0.0.1:8084` (the Docker-published port of `voc_nginx`). `/atlas/` and `/westkust/` are each a **single** `location` block proxying the *entire* prefix to the inner root (`proxy_pass http://127.0.0.1:8084/;` with `proxy_redirect` rewriting), not separate blocks per sub-path — so the six protected routes must be added as **nested** `location` blocks that outrank this catch-all by nginx's longest-prefix-match rule.
- **Inner = `voc_nginx`** — a Docker container (`nginx:1.25-alpine`), config at `nginx/nginx.conf` in this repository, mounted read-only into the container, published `8084:80` on `0.0.0.0` (the exposure SEC-2 found and N1 is meant to close). It already carries a rate-limit zone (`api_limit`, `60r/m`, `burst=20 nodelay` on `/api/`, `burst=5` on `/docs` and `/openapi.json`) and a custom redacted JSON 429 page. It proxies `/api/` to `backend:8000` and everything else to `frontend:8001` (Django) over the Docker-internal network — there is no separate location per research page today; `/riset/pemodelan/`, `/riset/pemodelan/panduan/`, and `/linimasa/` are all Django URLs currently served by the unprotected catch-all `location /`.
- Host Nginx worker runs as OS user `nginx` (uid 33 on this host); the `voc_nginx` container's worker runs as `nginx` uid 101 **inside its own container UID namespace** — these are two different numeric identities even though they share a name, which matters for the credential-store permission model (§ `PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md`).
- Docker Compose itself runs as host user `ubuntu` (member of the `docker` group).

This is materially more precise than the SEC-2/SEC-2A prototype's symmetric two-container model, and the candidate diff in `PRODUCTION_RESEARCH_PAGE_SEC3_CANDIDATE_DIFF.md` is written directly against these real files, not a re-derived approximation.

## 4. Researcher Credential-Store Decision for SEC-3 Planning

```text
SEC-DEC-11 (proposed, NOT YET a ledger row): OPTION_A_APPROVED_WITH_LIMITATIONS
```

`PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv` was checked this turn: **no `SEC-DEC-11` row exists.** Per this turn's explicit instruction, the ledger schema and rows are not modified silently. The decision is recorded here only, in `PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md`, as the SEC-3 planning basis, and a specific future additive ledger-row proposal is included there. It governs this plan's design (one host-managed htpasswd source, outside Git, read by host Nginx directly, mounted read-only into `voc_nginx`, same credential hashes validated at both layers, named individual accounts, atomic rotation, least-privilege permissions, no credential content ever printed) but is **not** itself an approval to provision anything real.

## 5. What This Plan Produces

| # | Deliverable | File |
|---|---|---|
| 1 | This plan | `PRODUCTION_RESEARCH_PAGE_SEC3_PRODUCTION_LIKE_PLAN.md` |
| 2 | Exact redacted candidate diff (A–F) | `PRODUCTION_RESEARCH_PAGE_SEC3_CANDIDATE_DIFF.md` |
| 3 | Credential-store design + permission model | `PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md` |
| 4 | Account provisioning runbook (no real accounts) | `PRODUCTION_RESEARCH_PAGE_SEC3_ACCOUNT_PROVISIONING_RUNBOOK.md` |
| 5 | Test matrix | `PRODUCTION_RESEARCH_PAGE_SEC3_TEST_MATRIX.csv` |
| 6 | Test results (this turn's rehearsal) | `PRODUCTION_RESEARCH_PAGE_SEC3_TEST_RESULTS.csv` |
| 7 | Rollback runbook | `PRODUCTION_RESEARCH_PAGE_SEC3_ROLLBACK_RUNBOOK.md` |
| 8 | Go/No-Go checklist | `PRODUCTION_RESEARCH_PAGE_SEC3_GO_NO_GO_CHECKLIST.md` |
| 9 | This turn's audit | `PRODUCTION_RESEARCH_PAGE_SEC3_AUDIT.md` |

## 6. Rehearsal Summary

A disposable topology matching the real production shape (outer proxy with nested protected locations under `/atlas/` and `/westkust/`, inner nginx reusing production's actual rate-limit zone, N1-candidate loopback-only publish vs. a comparison 0.0.0.0 publish) was built and torn down entirely within this turn. Full results are in `PRODUCTION_RESEARCH_PAGE_SEC3_TEST_RESULTS.csv`. Headline results:

- N1 candidate (`127.0.0.1:38085`): loopback reachable, non-loopback connection refused (`curl` exit 7) — confirms the binding change alone closes remote-network access, exactly as SEC-1/SEC-2 predicted.
- Comparison current-binding container (`0.0.0.0:38086`): reachable from both loopback and LAN IP — reproduces today's actual exposure for contrast.
- Both prefixes, all six protected pages, both carved-out research APIs, and the unrelated-API/public-control passthrough all behaved correctly (401 anonymous, 200 valid, unrelated public routes untouched).
- One real, non-leaking finding: `/atlas/atlas/...` and `/westkust/westkust/...` doubled-prefix paths fall through the nested protected blocks into the general unprotected passthrough and return `200` from a **dummy** always-succeed catch-all — verified via the inner access log that **no protected content** was served (the upstream path never matched an inner protected `location`). This is flagged as a **location-precedence finding**, not a data leak: it depends on the dummy backend's synthetic 200 fallback, which does not model Django's real 404 behavior on an unrecognized path. See `PRODUCTION_RESEARCH_PAGE_SEC3_AUDIT.md` §3 for the honest detail and the specific pre-deployment verification this requires against the real Django app.
- Fail-closed for missing/unreadable credential store: 403 / 500 respectively, no protected content in either body — consistent with SEC-2A.
- Least-privilege file permission behavior verified via container `--user` namespacing (no host `sudo` available in this sandbox): the file owner's UID reads successfully; an unrelated UID (`65534`/`nobody`) is denied.
- Rate limiting reused production's actual `api_limit` zone (`60r/m burst=20 nodelay`) with auth added on top: a 25-request authenticated burst produced `200×21, 429×4` — burst capacity works identically with Basic Auth layered on, single navigation unaffected.
- Failure rehearsal: a syntax-broken outer config and a syntax-broken inner config both failed `nginx -t` before ever being eligible for a real reload; a simulated one-location `auth_basic off` regression was mechanically detectable by grepping the rendered candidate config; rollback to a no-auth baseline demonstrably restores the pre-SEC-3 unauthenticated state.

Full detail, per-test-ID: `PRODUCTION_RESEARCH_PAGE_SEC3_TEST_RESULTS.csv`.

## 7. Exact Production Operation Plan (prepared, not executed)

Every command below is marked `NOT_AUTHORIZED_FOR_EXECUTION`. None has been run against production this turn or any prior turn. No real credential value appears anywhere in this sequence.

```text
NOT_AUTHORIZED_FOR_EXECUTION
 1. Backup sequence:
      cp /etc/nginx/conf.d/silida.conf /etc/nginx/conf.d/silida.conf.pre-sec4.bak
      cp nginx/nginx.conf nginx/nginx.conf.pre-sec4.bak   (repo checkout, not committed)
      cp docker-compose.yml docker-compose.yml.pre-sec4.bak
 2. Credential-store provisioning sequence:
      -- per PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md sec.4 --
      generate new htpasswd file at HOST_PATH_PLACEHOLDER (never in Git)
      set owner/group/mode per the approved permission model
 3. Account provisioning sequence:
      -- per PRODUCTION_RESEARCH_PAGE_SEC3_ACCOUNT_PROVISIONING_RUNBOOK.md --
      for each approved pilot user: generate credential, htpasswd -B append,
      atomic replace, deliver via the approved secure channel
 4. Outer Nginx candidate-file installation:
      install the reviewed candidate silida.conf (PRODUCTION_RESEARCH_PAGE_SEC3_CANDIDATE_DIFF.md sec.B)
      to /etc/nginx/conf.d/silida.conf
 5. Inner Nginx candidate-file installation:
      install the reviewed candidate nginx/nginx.conf (candidate diff sec.C)
      to the repository checkout path mounted by voc_nginx
 6. Compose N1 edit:
      apply candidate diff sec.A to docker-compose.yml
 7. Syntax checks:
      nginx -t   (host, against the installed candidate silida.conf)
      docker compose run --rm nginx nginx -t   (or equivalent, against the
        candidate nginx/nginx.conf, before recreating the live container)
 8. Compose config validation:
      docker compose config   (render and validate the full candidate file)
 9. Single-service recreation:
      docker compose up -d --no-deps nginx   (voc_nginx only -- backend,
        frontend, db, redis are not touched by this change)
10. Host Nginx reload:
      systemctl reload nginx   (config-only reload, no process restart)
11. Post-change smoke tests:
      re-run the SEC-3 test matrix (PRODUCTION_RESEARCH_PAGE_SEC3_TEST_RESULTS.csv
        test IDs) against the real production-like environment
12. External direct-IP negative test:
      from a network location outside the host, confirm <host-ip>:8084 is
        refused (N1 verification against the real public IP, not just the
        disposable rehearsal's loopback/LAN-IP pair)
13. Rollback sequence:
      PRODUCTION_RESEARCH_PAGE_SEC3_ROLLBACK_RUNBOOK.md sec.2, if any NO-GO
        trigger condition is observed
14. Evidence capture:
      checksums, test results, uptime before/after, git status --
        committed as a SEC-4 evidence freeze, same pattern as SEC-2/SEC-2A
15. Final decision gate:
      researcher sign-off against PRODUCTION_RESEARCH_PAGE_SEC3_GO_NO_GO_CHECKLIST.md
        before step 9 is executed for real
```

## 8. Result Classification

```text
PRODUCTION_RESEARCH_PAGE_SEC3_PRODUCTION_LIKE_PLAN_READY_FOR_REVIEW
```

Rationale: all production-like tests passed or were verified fail-closed/non-leaking; the candidate diff (§ `PRODUCTION_RESEARCH_PAGE_SEC3_CANDIDATE_DIFF.md`) is complete for all six required change categories (A–F); the credential-store design is complete with an explicit permission model; the rollback procedure is complete and rehearsed; remaining production decisions are enumerated explicitly in § 9 below and are not resolved by this plan. No production file was changed to produce this classification.

This is **not**:

```text
SECURITY_ACCESS_CONTROL_GATE_PASSED  -- not issued
PRODUCTION_AUTH_APPROVED             -- not issued
DEPLOYMENT_AUTHORIZED                -- not issued
```

## 9. Decisions Still Required Before Any Production Change (SEC-4 gate)

1. Final approval of Option A credential store (this plan recommends it; approval is a separate researcher act)
2. Exact server-local credential path (not finalized in broadly-visible documents per this turn's instruction — see § `PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md` for the placeholder convention)
3. Owner/group/mode for that path
4. Pilot-user list and individual roles (SEC-DEC-08 already requires named individual accounts; no names exist yet)
5. Secure credential delivery channel
6. Final rate-limit threshold for the *protected* routes specifically (this rehearsal reused the existing `api_limit` zone as a starting point, not a finalized value — see `PRODUCTION_RESEARCH_PAGE_SEC3_CANDIDATE_DIFF.md` § F)
7. Maintenance date and time (SEC-DEC-10 requires a separately authorized window)
8. Monitoring owner
9. Rollback authority (who is authorized to execute `PRODUCTION_RESEARCH_PAGE_SEC3_ROLLBACK_RUNBOOK.md` in production)
10. Day-45 Entra/OIDC review owner (SEC-DEC-07's 60-day clock has not started; production is not yet activated)

## 10. Next Steps (explicitly not this turn)

```text
SEC-3 evidence review
  -> freeze SEC-3 milestone (commit, local only)
  -> push and server-sync evidence
  -> decide the ten remaining items in § 9
  -> create a separately authorized SEC-4 production implementation plan
  -> approve maintenance window
  -> provision named accounts securely
  -> deploy with rollback gate
```

```text
NEXT:            SEC-3 evidence freeze (separate turn)
PRODUCTION:       UNCHANGED
SECURITY GATE:    NOT_PASSED
```
