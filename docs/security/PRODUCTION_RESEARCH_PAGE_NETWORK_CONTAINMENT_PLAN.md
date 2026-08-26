# Production Research Page — Network Containment Plan

> **Phase:** SEC-1 Architecture Design (no implementation)
> **Baseline:** `51b0bd902ef7ee708f825e7aaa565f0e0c4fd7d8`
> **Finding addressed:** F-03 — `voc_nginx` published on `0.0.0.0:8084`, host firewall inactive
> **This document designs; it does not edit Docker Compose, Nginx, or firewall state.**

---

## 1. Actual Network Path, Traced (not assumed)

Verified this turn, read-only, on the production server:

```text
Host nginx: systemd service, native process (/usr/sbin/nginx), PID confirmed via `ps aux`
            NOT a container, NOT attached to any Docker network
            → confirmed: `systemctl is-active nginx` = active (separate from Docker lifecycle)

Docker network: westkust-routes_default (bridge, local) — confirmed via `docker compose config`
                Only backend, db, frontend, redis, nginx (voc_nginx) containers are members

Current path (public):
  Cloudflare (edge TLS)
  → silida.org:443 (host nginx, Cloudflare Origin Cert)
  → proxy_pass http://127.0.0.1:8084/...   (host nginx reaches Docker via the PUBLISHED PORT on loopback, not via the Docker bridge network — host nginx has no route into westkust-routes_default at all)
  → voc_nginx container (Docker bridge, listens :80 inside container, published as 0.0.0.0:8084 on the host)
  → frontend:8001 or backend:8000 (Docker-internal, bridge network, `expose`-only, not published)

Current path (direct, unintended):
  Any client → <VPS-IP>:8084 → voc_nginx directly, bypassing Cloudflare and host nginx entirely
  (possible because docker-proxy binds 0.0.0.0:8084, and `ufw status` = inactive)
```

**Critical structural fact:** host nginx is not a member of the Docker network. It reaches the app stack *only* through the published port on the loopback interface. There is no Docker-native alternative that lets a non-containerized host process reach a container except through a published port (or a Unix socket bind-mounted onto the host filesystem, not currently configured). This directly determines which of N1/N2 is achievable without deeper re-architecture (see §3).

---

## 2. Alternative N1 — Bind Published Port to Loopback Only

**Exact current traffic path:** as above — `0.0.0.0:8084` reachable from any interface.

**Proposed traffic path:**

```text
docker-compose.yml, nginx service:
  ports:
    - "8084:80"          # current — binds 0.0.0.0
  →
  ports:
    - "127.0.0.1:8084:80"   # proposed — binds loopback only
```

Host nginx's existing `proxy_pass http://127.0.0.1:8084/...` (already loopback-addressed in `silida.conf`) continues to work unchanged — **this alternative requires zero change to `silida.conf`**, only to `docker-compose.yml`.

**Affected Compose service:** `nginx` (voc_nginx) only.
**Affected host Nginx upstream:** none — `127.0.0.1:8084` is already the exact address host nginx targets; only the *bind interface* on the Docker side changes, not the address host nginx calls.
**Availability impact:** none for legitimate traffic (Cloudflare → host nginx → `127.0.0.1:8084` is unaffected, since it was already loopback-addressed). Only removes reachability from `<VPS-IP>:8084` directly.
**Rollback method:** revert the `ports:` line to `"8084:80"`, then `docker compose up -d nginx` (single-service recreation).
**Expected `docker compose` action:** `docker compose up -d nginx` — Compose detects the port-binding change and recreates only the `nginx` service container; `backend`, `frontend`, `db`, `redis` are unaffected.
**Container recreation required:** yes, for `nginx` only (port bindings are set at container-creation time, not hot-reloadable).
**Downtime expected:** brief (`voc_nginx` container restart, typically sub-second to a few seconds) — the same class of interruption as any routine `docker compose up -d nginx` deploy already performed in this project's history (per prior session record, this is a familiar, low-risk operation type).
**Test procedure:**
1. Before: confirm `curl -sI http://<VPS-IP>:8084/` succeeds (reproduces the current exposure).
2. Apply the change (not this turn).
3. After: confirm `curl -sI http://<VPS-IP>:8084/` times out or connection-refuses from an external host.
4. Confirm `curl -sI https://silida.org/atlas/` and `.../westkust/` still return 200 (public path unaffected).
5. Confirm `curl -sI https://silida.org/api/research/linimasa` still functions (until Phase 3's API policy is separately applied).
6. Run the five ontology validators (unrelated regression check, standard practice in this repo per prior sessions) to confirm no incidental breakage of the container stack.

**Residual bypass risk:** **low.** The only remaining path to the app is through host nginx (`silida.org`), which is under the researcher's control and already carries TLS + security headers. No known residual direct-port bypass. (A theoretical residual: if the VPS ever gains a second network interface or the loopback restriction is misapplied — mitigated by the test procedure's explicit external-`curl` check.)

---

## 3. Alternative N2 — Internal Docker Network, No Host Publish

**Exact current traffic path:** same as §1.

**Trace result: N2 as literally stated ("remove host publishing, use an internal Docker network or intended same-host proxy path") is NOT achievable under the current architecture without a materially larger change than this plan's scope.**

Reasoning, from the traced network path:

- Host nginx is a native systemd process, not a container. Docker's internal/bridge networking (`westkust-routes_default`) is only reachable by containers attached to it (or the Docker host's own routing to bridge IPs, which is not what `silida.org`'s config uses — it explicitly targets `127.0.0.1:8084`, a published port, not a container IP).
- For host nginx to reach `voc_nginx` *without* a published port, one of the following would be required, **none of which this plan authorizes or scopes**:
  - **(a)** Run host nginx itself inside a container attached to `westkust-routes_default` — this converts today's "native nginx + Docker app stack" architecture into "everything Dockerized," including migrating the existing Cloudflare Origin Certificate handling, the Astro static-site serving (`root /var/www/salido/dist`), and every other `location` block in `silida.conf` (not just `/atlas/`/`/westkust/`/`/api/`) into a Docker-managed nginx. This is a full infrastructure migration, not a port-binding change.
  - **(b)** Bind-mount a Unix domain socket from the `voc_nginx` container onto the host filesystem and repoint `silida.conf`'s `proxy_pass` at `unix:/path/to/socket` instead of `127.0.0.1:8084`. This is technically closer to "no host publish," but still requires editing `docker-compose.yml` (volume + command changes to `voc_nginx`) **and** `silida.conf` (both forbidden this turn), and is a nonstandard pattern for this codebase (no existing Unix-socket usage found anywhere in `docker-compose.yml`).
  - **(c)** Run host nginx and the Docker daemon such that host nginx can route directly to bridge-network container IPs (e.g., via `iptables`/routing rules) — this is fragile against container IP churn (already an identified pain point in this project's own history — see the `resolver 127.0.0.11` dynamic-DNS workaround in `nginx/nginx.conf` for exactly this class of problem) and not recommended.

**Conclusion for this design turn:** N2 is documented as **infeasible without a separately scoped re-architecture project** (option (a) above being the only structurally clean path, and itself a significant undertaking touching the entire host-nginx configuration, not just the auth-relevant blocks). **N1 is the only alternative achievable within the current architecture and this plan's scope.**

**Affected Compose service / upstream / availability / rollback / test procedure / residual risk:** not filled in further detail, since N2 is not being proposed as an executable alternative this turn — recorded here as a traced-and-rejected option, per the plan's own instruction to "trace the actual network path first" rather than assume feasibility.

---

## 4. Recommended Containment Option (design recommendation only — not a decision)

```text
N1 — bind the published port to 127.0.0.1:8084:80
```

This matches the researcher's own stated preference ("Prefer N1 ... unless network tracing proves that removing the publish entirely is safe") — and this turn's trace found the opposite: N2 is *not* safely/simply achievable, reinforcing N1 as the design to carry into SEC-DEC-02.

---

## 5. Not Performed This Turn

No `docker-compose.yml` edit, no `docker compose` command affecting running state, no firewall (`ufw`) change, no Nginx config edit (host or Docker layer), no container recreation. This document is a design artifact only.
