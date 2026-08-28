# Production Research Page — SEC-3 Audit

> **Phase:** SEC-3 completion record
> **Baselines:** parent `e813192b590917a7f96b9e3ca7da5c8c9a907be8`, SEC-2 `38120d250a2b629e86a6c66d0d4be7d0851117b5`, SEC-2A `1838815fb3314dc9528f3cf4b29f5761c0835b0a`

---

## 1. Scope

Confirms Phase SEC-3 (production-like implementation planning and isolated disposable rehearsal) was executed as specified, records what was actually built and tested, and lists the specific findings and remaining gaps before any SEC-4 production-like execution can be considered.

## 2. What Was Actually Built and Run

Unlike SEC-2/SEC-2A's symmetric two-container prototype, this turn first read production's **real** configuration read-only (`docker-compose.yml`, `nginx/nginx.conf` in this repo, and `/etc/nginx/conf.d/silida.conf` on `westkust-prod` via SSH — no secret value, certificate, or key was read or copied), then built a disposable rehearsal (`sec3_outer`/`sec3_inner`/two credential-store fault-injection variants/one rollback-demo container, network `sec3_net`, ports `127.0.0.1:38084`–`38089`) whose location structure and rate-limit zone were modeled directly on those real files. 43 tests were executed: 41 `PASS`, 2 `PASS_WITH_LIMITATION`, 0 `FAIL`.

## 3. Findings Requiring Researcher Attention

### 3.1 `SEC3-PREC-006`/`007` — Duplicated-prefix paths (`/atlas/atlas/...`, `/westkust/westkust/...`) fall through to an unprotected passthrough

```text
FINDING SEC3-F-01: OPEN_REQUIRES_REAL_DJANGO_REVERIFICATION
```

Both returned `200` instead of `401`/`404`. The response body was confirmed, via direct inspection and cross-checked against the inner access log, to be the **generic dummy homepage**, not the protected pemodelan/linimasa content — the upstream path (`/atlas/riset/pemodelan/`, after the outer `/atlas/` catch-all stripped only the first `/atlas/` segment) never matched an inner protected `location` block, so it fell to the inner catch-all. **No protected data was leaked.** However, this turn's inner catch-all was a synthetic `try_files ... =200 /public/index.html` that **always** returns success — real Django would very likely return a `404` for an unrecognized path like `/atlas/riset/pemodelan/` (the leading `/atlas/` segment is not part of any real Django URL pattern). This test therefore cannot honestly claim the real production behavior is a clean `404`; it can only claim the real production behavior is **not a protected-content leak**, because the leak would require the *inner* protected locations to match, and they structurally cannot for this exact malformed path shape. **Recommendation:** SEC-4's production-like test must re-run this exact path shape against the real Django app (not this dummy stand-in) and confirm the actual status code, before this finding can be closed as fully characterized. Marked `PASS_WITH_LIMITATION`, `researcher_review_required=true`.

### 3.2 Credential-file permission model: container UID mismatch not fully resolved for a stock image

`voc_nginx` uses the stock `nginx:1.25-alpine` image, whose worker runs as `uid=101` **inside its own container UID namespace**, which does not correspond to any host-side UID the operator controls without building a custom image. The recommended target permission (`0640` + a deliberately matching GID) could not be cleanly demonstrated in this rehearsal without that custom-image step; the rehearsal instead used mode `0644` (world-readable), which works but does not satisfy "no world-readable permission" from the SEC-3 instruction's stated preferred principle. Least-privilege *isolation itself* was verified via `docker run --user`, showing the permission-bit mechanism works correctly once the right UID/GID is assigned — the open question is specifically how to assign the right GID to a stock Alpine-based Nginx image without rebuilding it. See `PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md` §3 for the full detail and the flagged SEC-4 implementation step (a custom image, or an accepted `0644` posture matching `silida.conf`'s own real-world precedent).

### 3.3 Forwarded-IP / Cloudflare real-IP restoration not configured at host Nginx

```text
FINDING SEC3-F-02: OPEN_REQUIRES_TRUSTED_PROXY_DESIGN
```

```text
CLOUDFLARE_REAL_IP_RESTORATION: NOT_CONFIGURED
```

Reading `/etc/nginx/conf.d/silida.conf` this turn (read-only) found **no** `real_ip_header` / `set_real_ip_from` directives for Cloudflare's edge IP ranges. This means `$remote_addr` at host Nginx today is Cloudflare's edge IP, not the true client IP, for any Cloudflare-proxied request — which would collapse all clients into a shared rate-limit bucket keyed by Cloudflare's edge address once host-Nginx-level rate limiting is added (the *current* rate limiting lives only in the inner `voc_nginx` layer, behind the Docker network, where `$remote_addr` is host Nginx's own IP as seen from the container — a different, but related, aggregation concern). This was not something SEC-2/SEC-2A's prototype topology could surface (it had no Cloudflare-equivalent hop). **This is a genuine, previously-undocumented finding from reading the real config**, not a defect introduced this turn. This document does **not** select a production real-IP configuration — that remains a future SEC-3A/SEC-4 decision, which must define:

- trusted Cloudflare IPv4 and IPv6 ranges;
- automated range-update responsibility (Cloudflare rotates its published ranges);
- the exact `real_ip_header` (e.g. `CF-Connecting-IP`);
- recursive real-IP behavior (`real_ip_recursive`) if more than one proxy hop is ever introduced;
- rejection of untrusted direct forwarded headers (a client connecting directly to the origin, bypassing Cloudflare, must not be able to spoof `CF-Connecting-IP` and have it trusted);
- fallback behavior if the header is absent or malformed;
- a test procedure exercised through Cloudflare *and* via direct IP, not just one path;
- the resulting impact on access logs and rate limiting once corrected.

`SEC3-FWD-001` is marked `PASS`, `researcher_review_required=true` for this reason — the test itself passed (spoofing didn't bypass the limit key in the tested topology), but the surrounding architecture question it surfaced is not resolved by that pass.

## 4. Cleanup Confirmation

```text
Disposable containers removed:      confirmed (docker ps -a --filter name=sec3_ empty)
Disposable network removed:         confirmed (docker network ls has no sec3_net)
Test ports (38084-38089) listening: none (ss -tln, no match)
Dummy credential material:          shredded (shred -u); directory permission
                                     corrected before shred where needed
Ephemeral workspace:                deleted (rm -rf; confirmed absent)
Production uptime:                  unchanged -- westkust-prod voc_nginx still
                                     "Up 5 weeks", no restart
Production port 8084:               unchanged, 0.0.0.0:8084 still listening
Basic Auth in production:           still not active
Entra configuration:                not touched
```

## 5. Baseline Verification

| Item | Result |
|---|---|
| 11 SEC-0/SEC-1 files | unchanged vs `e813192b` |
| SEC-2 prototype-plan file | unchanged vs SEC-2 baseline |
| Six original SEC-2 evidence files | unchanged vs SEC-2 baseline (checksums re-verified this turn) |
| Six SEC-2A evidence paths | unchanged vs SEC-2A baseline (checksums re-verified this turn) |
| Production `docker-compose.yml` | unchanged (read-only this turn; candidate diff is a separate, unapplied document) |
| `silida.conf` | unchanged (read-only this turn) |
| `nginx/nginx.conf` | unchanged (read-only this turn) |
| Backend / Frontend / Database / Migrations | unchanged |
| Five ontology validators | Painan 23/23, Natal 28/28, Koto Tangah 34/34, Tiku 35/35, Sillida 32/32 — all PASS |
| Ontology decision-ledger working diff | unchanged — same fingerprint (`d2805d1...`) carried since an earlier turn, confirmed still present and still outside every commit made this session |

## 6. Production Isolation Statement

Every SSH command executed against `westkust-prod` this turn was read-only: `git rev-parse`, `git status --short`, `docker compose ps`, `cat`/`sha256sum` against `docker-compose.yml` and `/etc/nginx/conf.d/silida.conf`, `stat`, `ps`, `id`, `df -h`. No file was written, no service was reloaded or restarted, no container was recreated. The entire candidate-config authoring, rehearsal build, test execution, failure-injection, and rollback demonstration ran exclusively against the local, disposable Docker containers described in §2.

## 7. Output Checksums (this turn)

```text
9b5e131ed3eaea492cc247959519c93c4eb54c93a7d1b4e90fc969dca40f2201  PRODUCTION_RESEARCH_PAGE_SEC3_ACCOUNT_PROVISIONING_RUNBOOK.md
7fd221567039ea5094869b2a6708dfa90dec836e917e2c8b0a2e30286d16d7ad  PRODUCTION_RESEARCH_PAGE_SEC3_CANDIDATE_DIFF.md
0a2d42562f8c51cb8af764b34589d96f3ec7004013865946967bc20e09c65b60  PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md
500f84d1b4a3f4012ef9aa121d51f89ab540195ff98b2239d8e21117e643c369  PRODUCTION_RESEARCH_PAGE_SEC3_GO_NO_GO_CHECKLIST.md
16d35023e6e4694f0a64a4fd8f29b09408819008da030e692b866564353ee776  PRODUCTION_RESEARCH_PAGE_SEC3_PRODUCTION_LIKE_PLAN.md
99b028c0b2654e0e7bf592f9f1e5ca022b73d5e987bfa91fcab64912f4fec250  PRODUCTION_RESEARCH_PAGE_SEC3_ROLLBACK_RUNBOOK.md
177a1a264ec3f4754edd104e64c009b495fabd2c8b1e28924024cbe4c81b619e  PRODUCTION_RESEARCH_PAGE_SEC3_TEST_MATRIX.csv
c3d2aedc53502a1f4ba5a9024cf71f06d9bdb44d1a83c7a163a538df62a26cbd  PRODUCTION_RESEARCH_PAGE_SEC3_TEST_RESULTS.csv
```

(Note: `PRODUCTION_RESEARCH_PAGE_SEC3_PRODUCTION_LIKE_PLAN.md` and `PRODUCTION_RESEARCH_PAGE_SEC3_ACCOUNT_PROVISIONING_RUNBOOK.md` and `PRODUCTION_RESEARCH_PAGE_SEC3_ROLLBACK_RUNBOOK.md` had minor cross-reference section-number corrections applied after initial authoring, before this audit was written — the checksums above are the final, post-correction values that will be committed.)

---

## Final Status

```text
PRODUCTION_RESEARCH_PAGE_SEC3_PRODUCTION_LIKE_PLAN_READY_FOR_REVIEW
```

Security gate remains `NOT_PASSED`. Production implementation remains `NOT_AUTHORIZED`. Two `PASS_WITH_LIMITATION` findings (§3.1, §3.2) and one architecture question surfaced from real-config reading (§3.3) are carried forward as explicit SEC-4 preconditions, not silently resolved.
