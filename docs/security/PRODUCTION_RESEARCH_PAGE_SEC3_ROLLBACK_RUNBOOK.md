# Production Research Page — SEC-3 Rollback Runbook

> **Procedure document, rehearsed in a disposable environment only. Every command below marked NOT_AUTHORIZED_FOR_EXECUTION has not been run against production.**

---

## 1. Trigger Conditions (any one is sufficient to roll back)

- One prefix (`/atlas/` or `/westkust/`) found unprotected after deployment.
- One research API found public after deployment.
- Port 8084 still externally reachable after the N1 candidate is applied.
- Inner loopback boundary absent (direct same-host access to `voc_nginx`'s protected routes succeeds without a credential).
- Credential file discovered world-readable.
- A duplicate/second interactive authentication prompt appears in normal browser use.
- Protected body content appears in any unauthorized response.
- Cache behavior found unsafe (protected content cacheable by an intermediary).
- Any unrelated production diff is discovered alongside this change.

## 2. Rollback Sequence — NOT_AUTHORIZED_FOR_EXECUTION

```text
NOT_AUTHORIZED_FOR_EXECUTION
1. Restore /etc/nginx/conf.d/silida.conf from the pre-change backup (see
   PRODUCTION_RESEARCH_PAGE_SEC3_PRODUCTION_LIKE_PLAN.md's exact-operation-plan
   backup step).
2. nginx -t   (syntax check the restored file before reload)
3. systemctl reload nginx   (host Nginx, config-only reload, no process restart)
4. Restore nginx/nginx.conf (repo) from the pre-change backup / git revert of
   the SEC-4 commit that introduced the candidate blocks.
5. docker compose up -d --no-deps --build nginx   (recreate only the voc_nginx
   service; the read-only bind mount picks up the restored config on
   container recreation -- a bind-mounted file change alone does not require
   an image rebuild, but --build is included for a config-as-image scenario;
   for a pure bind-mount restore, `docker compose up -d --no-deps nginx`
   without --build is sufficient and preferred as the lower-blast-radius
   option)
6. Restore docker-compose.yml's ports: line to "8084:80" if the N1 candidate
   had been applied.
7. docker compose up -d --no-deps nginx   (re-apply the restored binding)
8. Verify: curl http://<public-host>/atlas/riset/pemodelan/ returns 200 with
   no auth challenge (pre-change baseline restored).
9. Verify: production container uptime for backend/frontend/db/redis is
   UNCHANGED (only nginx was recreated).
10. Leave the credential file in place (do not delete) unless it was newly
    provisioned this cycle -- removing it is a separate, explicit decision,
    not an automatic rollback step, since real accounts may already be in
    active use elsewhere if this is a rotation rollback rather than an
    initial-deployment rollback.
11. Record the rollback in the SEC-4 evidence trail: timestamp, trigger
    condition, operator, and confirmation of steps 8-9.
```

## 3. Rehearsed This Turn (disposable environment only)

- A disposable inner variant with `auth_basic` removed (the rollback target state) was built fresh and confirmed to return `200` with no challenge on a previously-protected route — `SEC3-ROLLBACK-001`, `PASS`.
- Two deliberately broken candidate configs (outer and inner) both failed `nginx -t` — confirming the syntax-check step in the sequence above (step 2) is not a formality; it genuinely blocks a broken candidate from ever reaching a live reload.
- A simulated single-location regression (`auth_basic off` on one of the eight new outer blocks) was mechanically detected by grepping the rendered candidate config for the literal string `auth_basic off` — this is the exact check that should run automatically before step 3 in a real SEC-4 execution, not a manual read-through.

## 4. What Rollback Does Not Need to Touch

If only steps 1–3 and 4–7 above are executed (Nginx config + N1 binding), rollback never needs to touch: `backend`, `frontend`, `db`, `redis`, the database, migrations, or any application code. This mirrors the SEC-2/SEC-2A rollback rehearsals, which demonstrated the same scoping property in their own disposable environments.

## 5. Rollback Authority

Not assigned by this document — listed in `PRODUCTION_RESEARCH_PAGE_SEC3_PRODUCTION_LIKE_PLAN.md` § 9, item 9, as a remaining decision.
