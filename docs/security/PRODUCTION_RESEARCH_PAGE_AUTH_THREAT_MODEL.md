# Production Research Page — Authentication Threat Model

> **Phase:** SEC-0 Discovery (read-only)
> **Baseline:** `51b0bd902ef7ee708f825e7aaa565f0e0c4fd7d8`
> **This document evaluates threats against the current, pre-implementation baseline. It authorizes no change.**

---

## 1. Existing Auth/Session/Security Capability (current state, verified)

| Capability | Status | Evidence |
|---|---|---|
| Django `django.contrib.auth` | **Not installed** | `INSTALLED_APPS = ["django.contrib.staticfiles", "map_app"]` — no `auth`, `contenttypes`, `sessions`, or `admin` app |
| Session middleware | **None** | `MIDDLEWARE` has only `SecurityMiddleware`, `WhiteNoiseMiddleware`, `CommonMiddleware`, `XFrameOptionsMiddleware` — no `SessionMiddleware`, no `AuthenticationMiddleware` |
| CSRF protection | **None** | No `CsrfViewMiddleware`; no `{% csrf_token %}` usage found; no state-changing forms exist yet in this app |
| User/account model | **None** | No `AUTH_USER_MODEL`; no user table in `backend/models.py` or Django app; the only credential-shaped table is `ApiKey` (machine-to-machine, see route inventory §4.4), unrelated to human login |
| Password hashing library | **None installed**, but available for free | No `bcrypt`/`argon2`/`passlib` in either `requirements.txt`; Django itself ships PBKDF2/Argon2-capable hashers once `django.contrib.auth` is enabled — no new dependency strictly required for Option A |
| Authorization middleware | **None** | No `login_required`, no `LoginRequiredMixin`, no route decorator of any kind on the three candidate views |
| Rate limiting | **Partial, generic** | Nginx (Docker layer) `limit_req_zone` on `/api/` and `/docs`/`/openapi.json`: 60 req/min per IP, burst 20 (main API), burst 5 (docs), `nodelay`, custom JSON 429. This is **IP-based only** — no per-account limiting exists because no accounts exist |
| Audit logging | **None, app-level** | Only nginx default `access_log`/`error_log` (host and Docker layers) — request-level, not event-level; no login/logout/session/authorization-denied events are possible today because there is nothing to log |
| CORS | Configured, `allow_credentials=False` | `backend/main.py` — explicit comment: "tidak ada cookie/session — sesuai temuan audit" (no cookie/session, per prior audit finding) |
| Secret management pattern | Established, consistent | `.env` gitignored (confirmed both locally and on server, never tracked), values interpolated into `docker-compose.yml` via `${VAR}` syntax, no plaintext secret in any tracked file (grep found zero matches for hardcoded credentials patterns) |

**Overall: this is a from-zero build.** No auth scaffolding of any kind exists in either service. Django's own `contrib.auth` is the only "already available" building block (ships with the framework, no new dependency), and it is currently disabled.

---

## 2. Nginx / Prefix / Forwarded-Header Behavior (verified on production, read-only)

- **Public entry:** Cloudflare (proxied, Full-Strict TLS per prior session record) → host nginx `silida.org:443` (Cloudflare Origin Certificate) → either `/atlas/` or `/westkust/` location block → `proxy_pass http://127.0.0.1:8084/` → Docker `voc_nginx` → Django `frontend:8001`.
- **`/atlas/` and `/westkust/` are functionally identical proxies to the same upstream.** This is the single most important routing fact for any auth design: a rule applied to one prefix and not the other is trivially bypassed via the sibling prefix (see route inventory §2).
- `proxy_set_header X-Forwarded-Proto https` is hardcoded (not `$scheme`) in both `/atlas/` and `/westkust/` blocks — correct today since silida.org is HTTPS-only, but means any auth code reading `X-Forwarded-Proto` to build absolute/callback URLs will always see `https`, never plain HTTP, at this host-nginx layer.
- `proxy_redirect / /atlas/;` (and the `/westkust/` equivalent) rewrites Django's own `Location:` headers (e.g., `APPEND_SLASH` redirects) to carry the correct public prefix — **any login-redirect / "return to original destination" mechanism must be built to work correctly through this rewrite**, or it will drop the prefix and 404, exactly the bug pattern already fixed once for APPEND_SLASH (documented in prior session history).
- `sub_filter` rewrites `href="/` / `src="/` in response bodies to carry the prefix — this only touches HTML *body* content, not `Location` headers (handled separately by `proxy_redirect`) and not JSON API responses (FastAPI responses pass through the *separate* `/api/` block, which has no `sub_filter`).
- **`/api/` at the silida.org layer is prefix-agnostic** — it is not nested under `/atlas/` or `/westkust/` at all, it is its own top-level location block proxying straight to `127.0.0.1:8084/api/`. This means any API-level protection cannot piggyback on "protect the `/atlas/` block" — it needs its own explicit rule, or must be enforced at the application (FastAPI) layer itself.

---

## 3. Docker Networking / Direct-Backend-Bypass Finding

**HIGH-SEVERITY, pre-existing, independent of any auth work:**

```text
docker compose ps (production):
  backend   8000/tcp            (expose only — correct)
  frontend  8001/tcp            (expose only — correct)
  nginx     0.0.0.0:8084->80/tcp, [::]:8084->80/tcp   (PUBLISHED to all interfaces)

ss -tlnp (production host):
  0.0.0.0:8084  LISTEN  (docker-proxy)
  [::]:8084     LISTEN  (docker-proxy)

ufw status: inactive (no host firewall)
```

`backend` (FastAPI, 8000) and `frontend` (Django, 8001) are correctly `expose`-only in `docker-compose.yml` — not reachable from outside the Docker network directly, by design (comments in the compose file confirm this was a deliberate SEC-1 decision). **However, `voc_nginx` (the Docker-internal reverse proxy, which forwards to both of them) is bound to `0.0.0.0:8084`, and the VPS has no active firewall.**

**Consequence:** `http://103.171.184.94:8084/riset/pemodelan/`, `http://103.171.184.94:8084/linimasa/`, and `http://103.171.184.94:8084/api/research/*` are reachable **today, right now, by anyone who knows the server's IP address** — with no TLS, no Cloudflare protection, no security headers from the host-nginx layer, and (critically for this plan) **no path through the host nginx's `/atlas/` or `/westkust/` location blocks at all.**

**This means: any authentication mechanism added only inside `silida.conf`'s `/atlas/`/`/westkust/` blocks (e.g., Option C Basic Auth scoped to those locations) would be completely bypassed by hitting port 8084 directly.** An effective design must either (a) enforce auth at the application layer (Django view / FastAPI dependency) so it applies regardless of entry path, or (b) close this exposure first (firewall port 8084 to `127.0.0.1` only, since the host nginx already reaches it via `127.0.0.1:8084` — a routing detail worth the researcher's attention, not something this discovery turn changes).

This finding predates and is independent of the auth-architecture decision — it is a standing exposure of the entire application (not just the three candidate pages) that the researcher should weigh regardless of which option is chosen.

---

## 4. TLS Termination and Cache Behavior

- **Edge:** Cloudflare, proxied ("orange-cloud"), mode Full (Strict) per prior session record (not re-verified this turn since it requires Cloudflare dashboard access, out of scope for filesystem/SSH discovery).
- **Origin:** host nginx terminates TLS with a Cloudflare Origin Certificate (`silida-origin.pem`/`.key`, 15-year validity), `ssl_protocols TLSv1.2 TLSv1.3`, modern cipher list, `ssl_session_cache shared:SSL:10m`.
- **Docker-internal hop (host-nginx → voc_nginx → Django/FastAPI):** plain HTTP, no TLS — acceptable only because this hop stays inside `127.0.0.1`/Docker bridge network *in the intended path*; the §3 finding means this same plaintext hop is also reachable directly from the public internet via port 8084.
- **Cache:** `/atlas/` and `/westkust/` blocks explicitly `proxy_hide_header Cache-Control` and force `Cache-Control: no-cache, must-revalidate` on every response through those prefixes — this is favorable for auth: any future protected response passing through these blocks will not be cached by intermediate/browser caches by default. The direct `/api/` block does **not** set any cache-control override — FastAPI's own per-route caching (Redis, `X-Cache` header) is the only cache layer for API responses, and that cache key is not user/session-scoped (there are no users yet), so a straightforward per-session auth addition would need the Redis cache key strategy re-examined to avoid one authenticated user's cached response being served to another.

---

## 5. Secret-Management Pattern (paths and mechanism only — no values read or printed)

- `.env` is gitignored at the repo root (`.gitignore:39`), confirmed absent from `git ls-files` both locally and via the equivalent check on the server.
- `docker-compose.yml` interpolates all secrets (`POSTGRES_PASSWORD`, `DJANGO_SECRET_KEY`) from the shell environment / `.env` file — never hardcoded in the compose file itself.
- Server-side `.env` file exists at `/home/ubuntu/westkust-routes/.env`, permissions `-rw-rw-r--`, owner `ubuntu:ubuntu` (group-writable, world-readable — a minor hardening note for the researcher's awareness, not evaluated further since reading contents was out of scope and not performed).
- Existing precedent for a *hashed* secret pattern already exists in this codebase (`ApiKey.key_hash`, SHA-256, route inventory §4.4) — establishes that the team is already comfortable with a hash-store-compare pattern, which is directly reusable for Option A's password-hash requirement (with a stronger, salted, adaptive algorithm — SHA-256 alone is not appropriate for password hashing, only for API-key equality checks; plan §7.3 already flags this correctly).

---

## 6. Threat Evaluation (plan §16 list)

| # | Threat | Current exposure | Notes |
|---|---|---|---|
| 1 | Credential stuffing | N/A — no credentials exist yet | Becomes relevant only once Option A/C introduces passwords |
| 2 | Brute force | N/A yet | Nginx per-IP rate limit (60/min) would offer *some* generic throttling to any future login endpoint under `/api/`, but is not login-attempt-specific |
| 3 | Shared-password leakage | N/A yet | Relevant to Option C (Basic Auth is inherently shareable) more than A/B |
| 4 | Session theft | N/A — no sessions exist | Becomes relevant once Option A/B introduce cookies |
| 5 | Session fixation | N/A yet | Standard Django session middleware (once enabled) rotates session ID on login by default |
| 6 | CSRF | N/A — no state-changing endpoints protected by auth yet exist | Django's CSRF middleware, once enabled, covers this for Option A |
| 7 | Open redirect | N/A — no login-redirect mechanism exists yet | Must be designed carefully given the `/atlas/`+`/westkust/` dual-prefix finding (§2) |
| 8 | Cache leakage | **Partially mitigated already** for `/atlas/`/`/westkust/` HTML (no-cache forced); **not mitigated** for `/api/` responses (Redis cache not session-scoped) | Real risk once auth is added, unless cache key strategy changes |
| 9 | Unauthenticated API access | **CONFIRMED PRESENT TODAY** | `/api/research/linimasa` and `/api/research/pemodelan-dashboard` are fully public right now (route inventory §4.2) |
| 10 | Static-bundle disclosure | Low — no separate sensitive JSON bundle exists; linimasa data is inline in the SSR HTML itself, not a separate static file | Protecting the HTML page (and the API, per #9) is sufficient; no separate static-bundle-specific mitigation needed |
| 11 | Proxy-prefix bypass | **CONFIRMED HIGH RISK** | `/atlas/` vs `/westkust/` dual-prefix (§2); any single-prefix fix is bypassable |
| 12 | Alternate-host bypass | Not directly evaluated (would require DNS/Cloudflare-config review, out of scope) | Flagged for Phase SEC-1 follow-up |
| 13 | Direct backend-port access | **CONFIRMED HIGH RISK, PRE-EXISTING** | Port 8084 published to `0.0.0.0`, no firewall (§3) — the single most severe finding of this discovery |
| 14 | User enumeration | N/A yet | Design requirement for whichever option is chosen (plan §9 already specifies generic error messages) |
| 15 | Privilege escalation | N/A — no roles exist yet | Relevant once the RESEARCHER/REVIEWER/ADMIN role model (plan §6) is implemented |
| 16 | Insecure password reset | N/A yet | Only relevant to Option A/C (local passwords); Option B delegates this to the identity provider |
| 17 | Secrets in Git or logs | **Not found** — grep of tracked files found no hardcoded credentials; `.env` confirmed gitignored on both local and server checkouts | Low risk today; must remain a standing check for whichever option is implemented |
| 18 | Denial of service via lockout | N/A yet | Plan §9's suggested threshold (5/account/15min, 20/IP/15min) is a *planning* target only, not yet approved or implemented |

**Summary:** two threats are already live findings independent of any auth decision (#9 unauthenticated API access, #13 direct backend-port access), and one is a structural bypass risk that any chosen option must design around (#11 dual-prefix). The remaining threats are latent — they become relevant only in proportion to whichever option (A/B/C) is eventually selected, and are not yet applicable because no authentication mechanism exists to attack.
