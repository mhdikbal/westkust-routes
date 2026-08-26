# Production Research Page — Option C Basic Auth Transition Plan

> **Phase:** SEC-1 Architecture Design (no implementation)
> **Status:** NONPRODUCTION DESIGN ONLY — no htpasswd, username, or password created by this document
> **Baseline:** `51b0bd902ef7ee708f825e7aaa565f0e0c4fd7d8`
> **Scope note (per researcher direction):** Option C is permitted for design and local/prod-like testing only; production deployment remains separately gated behind SEC-DEC-01 (network containment) and SEC-DEC-03/04 (dual-prefix and API protection) being approved and applied first.

---

## 1. Design Requirements Checklist (from the plan)

| Requirement | Design |
|---|---|
| One separate username per person, no shared account | `htpasswd` supports multiple named entries; design mandates one entry per named individual (see SEC-DEC-08, pending) — never a single shared credential for the pilot group |
| Password hash outside Git | `htpasswd` file stored at a server-local path outside the repository working tree entirely (e.g. `/etc/nginx/secrets/` or equivalent, **not** `/home/ubuntu/westkust-routes/`) — never referenced by a path inside the git-tracked tree |
| htpasswd file outside repository | Same as above — repository-relative paths are explicitly excluded from the design |
| Root-readable or least-privilege file permissions | Design target: file owned by `root`, mode `640`, group-readable only by the nginx worker's group (or `600` root-only if nginx is configured to read it via a root-owned include before dropping privileges) — exact mode to be confirmed against the running nginx worker's user at implementation time, not this turn |
| HTTPS only | Already satisfied structurally — both `/atlas/` and `/westkust/` blocks live inside the `listen 443 ssl` server block in `silida.conf`; the `:80` server blocks are unconditional 301 redirects to `https://silida.org$request_uri`. No plaintext path reaches these locations at the `silida.org` layer today |
| Generic authentication realm | Design target: a realm string that does not name the research topic or institution specifically (e.g. `"Restricted"` rather than `"Atlas Power Relations Research"`), to avoid disclosing what is being protected to an unauthenticated prober |
| Both prefixes protected | Directly inherits the dual-prefix policy document (P1) — the same `htpasswd` file and `auth_basic` directive applied identically to both the `/atlas/riset/pemodelan/`+`/atlas/linimasa/` and `/westkust/riset/pemodelan/`+`/westkust/linimasa/` child location blocks |
| Both research APIs protected | Directly inherits the API protection policy document §3.4 — the same file/directive applied to the narrower `/api/research/linimasa` and `/api/research/pemodelan-dashboard` location blocks |
| `Cache-Control: no-store` | Design target: `add_header Cache-Control "no-store" always;` inside each protected location block, overriding (not merely supplementing) the existing `no-cache, must-revalidate` currently set for `/atlas/`/`/westkust/` generally — `no-store` is strictly stronger, appropriate for authenticated content specifically |
| `X-Robots-Tag: noindex, nofollow` | Design target: `add_header X-Robots-Tag "noindex, nofollow" always;` alongside the existing per-page `<meta name="robots">` tags already present in all three candidate templates (defense in depth — the plan explicitly warns not to rely on `robots.txt` alone, and this design does not) |
| Rate limiting on protected/login challenges | Design target: reuse the existing `limit_req_zone api_limit` (already defined in the Docker-layer `nginx/nginx.conf`, 60r/m) is *not* directly applicable here since Basic Auth challenges are evaluated at the *host*-nginx layer (`silida.conf`), which currently has no `limit_req_zone` of its own. Design requires a **new** `limit_req_zone` in `silida.conf` scoped to the protected location blocks specifically — parameters PENDING SEC-DEC-09 |
| Expiry date and migration target recorded | Design target: an explicit, dated comment block in the eventual `silida.conf` change (e.g. `# BASIC AUTH PILOT — activated <date>, expires <date+N>, migrate to Entra/OIDC per ADR — see docs/security/`) — expiry length PENDING SEC-DEC-07 |
| Rollback procedure | See §3 below |
| No credential value in documentation or terminal output | Honored throughout this document and this entire turn — no username, password, or hash value appears anywhere in this design or in any command run this turn |

---

## 2. Design Detail: Location Block Shape (not applied)

```text
# design sketch only — not written to silida.conf this turn

location /atlas/riset/pemodelan/ {
    auth_basic "Restricted";
    auth_basic_user_file /etc/nginx/secrets/research_pilot.htpasswd;   # path outside repo, illustrative
    limit_req zone=host_auth_limit burst=<TBD> nodelay;

    add_header Cache-Control "no-store" always;
    add_header X-Robots-Tag "noindex, nofollow" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    proxy_pass http://127.0.0.1:8084/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_read_timeout 60;
    proxy_redirect / /atlas/;

    sub_filter_once off;
    sub_filter 'href="/'  'href="/atlas/';
    sub_filter "href='/"  "href='/atlas/";
    sub_filter 'src="/'   'src="/atlas/';
    sub_filter "src='/"   "src='/atlas/";
}
# ...mirrored for /atlas/linimasa/, /westkust/riset/pemodelan/, /westkust/linimasa/,
#    and the two /api/research/{linimasa,pemodelan-dashboard} blocks (without sub_filter,
#    since API responses are JSON, not HTML with href/src rewriting needs)
```

This sketch exists to make the design concrete and reviewable; it is **not** applied to any file this turn.

---

## 3. Rollback Procedure

1. Remove the added `auth_basic`/`auth_basic_user_file`/`limit_req` lines (and the four/six new location blocks entirely, reverting to the pre-pilot `silida.conf`).
2. `nginx -t` (config syntax check) before reload — matches the pattern already established in this project's own prior nginx-config-change history (backup-before-reload, verify-before-reload).
3. `systemctl reload nginx` (or `nginx -s reload`) — reload, not restart, to avoid dropping in-flight connections to the unrelated Astro static site and `/api/` traffic.
4. Delete or securely retain the `htpasswd` file per the researcher's own data-retention preference at rollback time (not prescribed here).
5. Confirm via `curl` that the three candidate pages and two APIs return 200 without credentials again (i.e., rollback fully reverses the pilot, not a partial state).

---

## 4. Expiry and Migration Target

Design placeholder only — exact expiry length is SEC-DEC-07 (pending; researcher's own draft note names 60 days as a candidate). Migration target is Option B (Entra/OIDC), per SEC-DEC-06 (pending). The expiry date, once set, should be recorded both in the `silida.conf` comment (per §1) and in the security decision ledger (`PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv`) so it is discoverable from either the running config or the research record.

---

## 5. Explicitly Not Performed This Turn

No `htpasswd` file generated. No username created. No password created or hashed. No `silida.conf` edit. No file written outside `docs/security/`. No secret of any kind referenced by value anywhere in this document or in any command executed this turn.
