# Production Research Page — SEC-3 Candidate Diff

> **These are redacted candidate patches for review. None of them have been applied to production.**
> **Baselines:** parent `e813192b590917a7f96b9e3ca7da5c8c9a907be8`, SEC-2 `38120d250a2b629e86a6c66d0d4be7d0851117b5`, SEC-2A `1838815fb3314dc9528f3cf4b29f5761c0835b0a`

---

## Source Snapshot (read-only, this turn)

| File | Location | Owner:Mode | SHA-256 (as read this turn) |
|---|---|---|---|
| `docker-compose.yml` | repo root | `naro:naro 644` (local checkout) | `5961cda2b144314a25f3d3fa5fe9ed3c947ff96345d0899498a0220181c44ca3` |
| `nginx/nginx.conf` (inner) | repo | `naro:naro 644` (local checkout) | `78b3203b336337a0e64290af305e27c91f8d228f69ebeabac97bceddaea4a38b` |
| `/etc/nginx/conf.d/silida.conf` (outer, host-managed) | `westkust-prod`, outside Git | `root:root 644` | `07d350c6f983aacc32e6aa76467b93665f3cb73540341211071f041cca1205ee` |

No certificate, private key, `.env`, or credential value was read or copied. `silida.conf`'s TLS block (`ssl_certificate`/`ssl_certificate_key` paths only, no key material) was read to understand structure; the actual `.pem`/`.key` file contents were never opened.

---

## A. Docker Compose — N1 loopback binding

**Current** (`docker-compose.yml`, `nginx:` service, `ports:`):

```yaml
    ports:
      - "8084:80"
```

Docker Compose short syntax `"8084:80"` binds to `0.0.0.0` by default — this is exactly the SEC-1/SEC-2 finding (F-03): any network-reachable client can hit `<host-ip>:8084` directly, bypassing host Nginx and any auth added there.

**Candidate:**

```yaml
    ports:
      - "127.0.0.1:8084:80"
```

Verified this turn (disposable rehearsal): a container published as `127.0.0.1:PORT:80` is reachable on loopback and refuses connections from a non-loopback interface (`curl` exit 7, connection refused) — see `SEC3-N1-001`/`002` in the test results. A companion container published `0.0.0.0:PORT:80` was reachable from both, reproducing today's exposure for direct comparison.

**Rollback:** revert the single line to `"8084:80"`. No other Compose field changes.

---

## B. Host Nginx (`/etc/nginx/conf.d/silida.conf`) — protect both prefixes identically

**Current structure** (relevant excerpt, read this turn): `/atlas/` and `/westkust/` are each **one** `location` block proxying the *entire* prefix to `http://127.0.0.1:8084/` with `proxy_redirect` and `sub_filter` rewriting — there are no per-sub-path blocks today.

**Candidate:** insert three nested, more-specific `location` blocks *above* each existing prefix block (nginx matches the longest literal prefix first, so a nested block with a longer path wins over its parent regardless of file order — verified in the rehearsal, `SEC3-PREC-001..004`):

```nginx
    # ── inserted ABOVE the existing "location /atlas/ { ... }" block ──
    location /atlas/riset/pemodelan/panduan/ {
        auth_basic "Westkust Research — Restricted";
        auth_basic_user_file CONTAINER_PATH_PLACEHOLDER;   # see credential-store design doc
        add_header Cache-Control "no-store" always;
        add_header X-Robots-Tag "noindex, nofollow" always;
        proxy_pass http://127.0.0.1:8084/riset/pemodelan/panduan/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_redirect / /atlas/;
    }
    location /atlas/riset/pemodelan/ {
        auth_basic "Westkust Research — Restricted";
        auth_basic_user_file CONTAINER_PATH_PLACEHOLDER;
        add_header Cache-Control "no-store" always;
        add_header X-Robots-Tag "noindex, nofollow" always;
        proxy_pass http://127.0.0.1:8084/riset/pemodelan/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_redirect / /atlas/;
    }
    location /atlas/linimasa/ {
        auth_basic "Westkust Research — Restricted";
        auth_basic_user_file CONTAINER_PATH_PLACEHOLDER;
        add_header Cache-Control "no-store" always;
        add_header X-Robots-Tag "noindex, nofollow" always;
        proxy_pass http://127.0.0.1:8084/linimasa/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_redirect / /atlas/;
    }

    # location /atlas/ { ... existing block, unchanged, now only reached
    #                     for everything else under /atlas/ ... }
```

...and the symmetric set for `/westkust/riset/pemodelan/panduan/`, `/westkust/riset/pemodelan/`, `/westkust/linimasa/` inserted above the existing `location /westkust/ { ... }` block, each proxying to the same inner paths (`/riset/pemodelan/panduan/`, `/riset/pemodelan/`, `/linimasa/`) with `proxy_redirect / /westkust/;`.

**And** two carved-out API blocks inserted above the existing `location /api/ { ... }`:

```nginx
    location = /api/research/linimasa {
        auth_basic "Westkust Research — Restricted";
        auth_basic_user_file CONTAINER_PATH_PLACEHOLDER;
        proxy_pass http://127.0.0.1:8084/api/research/linimasa;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
    location = /api/research/pemodelan-dashboard {
        auth_basic "Westkust Research — Restricted";
        auth_basic_user_file CONTAINER_PATH_PLACEHOLDER;
        proxy_pass http://127.0.0.1:8084/api/research/pemodelan-dashboard;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }

    # location /api/ { ... existing block, unchanged, now only reached
    #                   for every other /api/ path ... }
```

**Verified this turn** (rehearsal, same nested-precedence structure): all 6 page paths and both API paths returned 401 anonymous / 200 valid; the pre-existing unrelated `/api/` traffic and the `/atlas/`/`/westkust/` root passthrough were unaffected.

**Rollback:** delete the eight inserted `location` blocks; the three pre-existing catch-all blocks (`/atlas/`, `/westkust/`, `/api/`) are untouched by this candidate and need no edit to roll back.

---

## C. Inner `voc_nginx` (`nginx/nginx.conf`) — protect the same six targets at the inner layer

**Current structure:** `/riset/pemodelan/`, `/riset/pemodelan/panduan/`, and `/linimasa/` are Django URLs served by the single catch-all `location /` (proxies to `frontend:8001`, not rate-limited). `/api/research/linimasa` and `/api/research/pemodelan-dashboard` are covered only by the general `location /api/` (proxies to `backend:8000`, `limit_req zone=api_limit burst=20 nodelay`).

**Candidate:** insert the same shape of nested, more-specific `location` blocks above the existing `location /` and `location /api/`:

```nginx
    # ── inserted ABOVE "location /api/ { ... }" ──
    location = /api/research/linimasa {
        limit_req zone=api_limit burst=20 nodelay;
        auth_basic "Westkust Research — Restricted";
        auth_basic_user_file CONTAINER_PATH_PLACEHOLDER;
        add_header Cache-Control "no-store" always;
        add_header X-Robots-Tag "noindex, nofollow" always;
        set $backend_upstream http://backend:8000;
        proxy_pass $backend_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location = /api/research/pemodelan-dashboard {
        limit_req zone=api_limit burst=20 nodelay;
        auth_basic "Westkust Research — Restricted";
        auth_basic_user_file CONTAINER_PATH_PLACEHOLDER;
        add_header Cache-Control "no-store" always;
        add_header X-Robots-Tag "noindex, nofollow" always;
        set $backend_upstream http://backend:8000;
        proxy_pass $backend_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # ── inserted ABOVE "location / { ... }" ──
    location /riset/pemodelan/panduan/ {
        auth_basic "Westkust Research — Restricted";
        auth_basic_user_file CONTAINER_PATH_PLACEHOLDER;
        add_header Cache-Control "no-store" always;
        add_header X-Robots-Tag "noindex, nofollow" always;
        set $frontend_upstream http://frontend:8001;
        proxy_pass $frontend_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location /riset/pemodelan/ {
        auth_basic "Westkust Research — Restricted";
        auth_basic_user_file CONTAINER_PATH_PLACEHOLDER;
        add_header Cache-Control "no-store" always;
        add_header X-Robots-Tag "noindex, nofollow" always;
        set $frontend_upstream http://frontend:8001;
        proxy_pass $frontend_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location /linimasa/ {
        auth_basic "Westkust Research — Restricted";
        auth_basic_user_file CONTAINER_PATH_PLACEHOLDER;
        add_header Cache-Control "no-store" always;
        add_header X-Robots-Tag "noindex, nofollow" always;
        set $frontend_upstream http://frontend:8001;
        proxy_pass $frontend_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
```

The existing `location /api/` and `location /` blocks are unchanged and continue to handle every other path exactly as today.

**Verified this turn:** rehearsal `SEC3-INNER-*` rows — anonymous 401, valid 200, on both the page and API paths, direct loopback and via the outer proxy.

**Rollback:** delete the five inserted blocks; the two pre-existing catch-all blocks need no edit.

---

## D. Credential Store

```text
HOST_PATH_PLACEHOLDER      -- not finalized in this broadly-visible document; see
                               PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md
                               for the placement convention and reasoning
CONTAINER_PATH_PLACEHOLDER -- referenced above as auth_basic_user_file; mounted
                               read-only into voc_nginx; same file read directly
                               by host Nginx (no mount needed at that layer,
                               it is a native process on the same filesystem)
```

Full design, permission model, and rotation procedure: `PRODUCTION_RESEARCH_PAGE_SEC3_CREDENTIAL_STORE_DESIGN.md`.

---

## E. Headers

Already exercised on every candidate protected `location` above:

```nginx
add_header Cache-Control "no-store" always;
add_header X-Robots-Tag "noindex, nofollow" always;
```

Verified this turn on both a `200` (valid credential) and would apply identically on a `401` (nginx's `add_header ... always` applies regardless of status code, as already confirmed for the same directive pattern in SEC-2 T-032/T-033).

---

## F. Rate Limiting

**Candidate (starting point only, not finalized):** reuse the existing `api_limit` zone (`60r/m`, `burst=20 nodelay`) already defined in `nginx/nginx.conf` for the two carved-out research API locations — no new zone required for the APIs. The three protected page locations are not currently rate-limited at all (matching the rest of the Django frontend, which the real production config also leaves unlimited).

**Verified this turn:** a 25-request authenticated burst against the API through the full outer→inner chain, with the existing zone, produced `200×21, 429×4` — consistent with the zone's burst capacity, with Basic Auth layered on top and no interaction defect. Single authenticated page/API requests were unaffected.

**Explicitly not finalized**, per Phase 3 instruction, until a production-like test confirms:

- normal navigation continues to feel unthrottled for a single legitimate researcher;
- static asset requests (served by host Nginx directly, not proxied) are unaffected — they don't pass through this zone at all;
- API request patterns from the actual Django templates (which page load triggers how many `/api/research/*` calls) are measured, not assumed;
- forwarded-client-IP behavior is understood — see `PRODUCTION_RESEARCH_PAGE_SEC3_PRODUCTION_LIKE_PLAN.md` §6 and the forwarded-IP test in `PRODUCTION_RESEARCH_PAGE_SEC3_TEST_RESULTS.csv` (`SEC3-FWD-001`): `$binary_remote_addr` in both nginx layers keys off the real TCP peer address, not any `X-Forwarded-For` value, so a spoofed header does not let a client evade its own rate-limit bucket — but this must still be re-verified against the real Cloudflare→host-Nginx path (Cloudflare presents its own edge IP as the TCP peer unless `real_ip` directives are configured, which `silida.conf` does not currently have — flagged as a remaining item, not resolved by this plan).

No specific numeric threshold is proposed as final in this document.
