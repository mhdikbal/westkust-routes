# Production Research Page — SEC-3 Credential-Store Design

> **Design document. No real credential, path, or account was created.**
> **Baselines:** parent `e813192b590917a7f96b9e3ca7da5c8c9a907be8`, SEC-2 `38120d250a2b629e86a6c66d0d4be7d0851117b5`, SEC-2A `1838815fb3314dc9528f3cf4b29f5761c0835b0a`

---

## 1. Decision Carried Forward

SEC-2A's addendum recommended **Option A** (one host-managed htpasswd source, mounted read-only into the inner container) for the 60-day transition, marked `OPTION_A_RECOMMENDED_WITH_LIMITATIONS` / `PENDING_RESEARCHER_DECISION`. This SEC-3 turn proposes carrying that forward as:

```text
SEC-DEC-11 (proposed): OPTION_A_APPROVED_WITH_LIMITATIONS
```

**Ledger status check (this turn):** `grep -c "SEC-DEC-11" PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv` → `0`. No such row exists. Per this turn's explicit instruction, the existing ledger schema is not modified and no row is added silently. `SEC-DEC-11` is recorded here as the SEC-3 planning basis only.

### Proposed future additive ledger-row extension (not applied this turn)

If and when the researcher explicitly authorizes it, a `SEC-DEC-11` row could be appended to `PRODUCTION_RESEARCH_PAGE_SECURITY_DECISION_LEDGER.csv` following the existing schema (`decision_id,question,options,plan_recommendation,researcher_direction,depends_on,supporting_finding,rationale,status,notes`), e.g.:

```text
decision_id: SEC-DEC-11
question: Select credential-store topology for the two-layer Basic Auth transition
options: Option A (one host-managed store, dual-mount) vs Option B (two independently provisioned stores) vs Option C (app-layer/token at inner layer)
plan_recommendation: Option A
depends_on: SEC-DEC-05, SEC-DEC-08
supporting_finding: SEC2A-INNER-001..012 (12/12 PASS), SEC3 rehearsal this turn
status: <researcher fills in — PENDING at time of this document>
```

This is a proposal for the researcher's own future action, not an edit performed by this turn.

## 2. Selected Architecture

- **One** host-managed credential source (not two independently provisioned copies — Option B, used only to prove independent validation in the SEC-2A prototype, is explicitly not the production choice).
- Stored **outside** the Git repository and outside the project checkout directory entirely (not `nginx/htpasswd`, not anywhere under `/home/ubuntu/westkust-routes/`) — this is a hard requirement carried from every prior SEC-0/SEC-1/SEC-2/SEC-2A output.
- **Host Nginx** (`/etc/nginx/conf.d/silida.conf`, native process, `root:root`-owned config) reads the file directly from the host filesystem — no mount needed at that layer.
- The **same file** is mounted **read-only** into the `voc_nginx` container (`nginx:1.25-alpine`, container worker `uid=101`).
- Both layers validate the **same credential hashes** — one rotation event updates both simultaneously, with no window where the layers hold different credentials (this is the property that made the SEC-2A double-challenge assessment succeed with a single browser-visible prompt: the client's real `Authorization` header, once supplied to the outer layer, is forwarded unmodified to the inner layer, which independently checks it against this same file).
- **Named individual accounts only** (per `SEC-DEC-08`, already `APPROVED` as policy) — no shared account, no self-registration.
- **Atomic rotation** — replace the file via `mv` (same filesystem, atomic rename), never edit in place with an in-place write that could be read mid-write.
- **Least-privilege permissions** — detailed in § 3.
- **Credential content never printed** into any report or terminal summary, this turn or any future turn.
- **Production provisioning remains separately gated** — this document is a design, not an authorization to create the file.

## 3. Permission Model

### Real, discovered identities (read-only, this turn)

| Component | Identity | Where |
|---|---|---|
| Host Nginx worker process | OS user `nginx`, uid `33` | `westkust-prod`, native systemd process |
| `voc_nginx` container worker | container-local user `nginx`, `uid=101 gid=101` | inside the `nginx:1.25-alpine` image's own UID namespace — **not** the same numeric identity as the host `nginx` user despite the shared name |
| Docker Compose / `docker` CLI | OS user `ubuntu` | member of the `docker` group |
| `silida.conf` itself (for comparison) | `root:root`, mode `644` | `/etc/nginx/conf.d/silida.conf` |

### Candidate permission model

```text
Owner:  a dedicated security-owner account (or root) — NOT the deploying `ubuntu`
        user, to keep credential-file writes out of the routine deployment path
Group:  a dedicated group whose membership includes the host Nginx worker (uid 33)
Mode:   0640  (owner rw, group r, others none)
```

This satisfies "host Nginx has read access" (via group membership) and "no world-readable permission" (mode excludes `others`) simultaneously, and was verified structurally sound in the disposable rehearsal this turn:

- **Bind-mount + container UID mismatch is the real constraint.** A read-only Docker bind mount preserves the host's numeric UID/GID on the file; it does **not** remap them into the container's UID namespace. `voc_nginx`'s worker is uid **101** inside its own namespace, which almost certainly does not correspond to the host's dedicated security-owner or group UID. **This means mode `0640` alone, correctly set for the host Nginx worker, will very likely deny the container's worker (uid 101) read access**, causing an inner-layer `500` (fail-closed, not a leak, but an outage of the intended dual-layer design) — unless the file's numeric GID is deliberately chosen to also equal `101` (matching the container image's baked-in `nginx` gid), or the file is made group-readable by a group whose GID happens to be shared, or (the simpler, verified-safe fallback) mode `0644` is used instead, accepting that any host-local process can read it — which is the same posture `silida.conf` itself already has (`root:root 644`) and is standard for Nginx credential files that must be read by an Nginx worker whose exact UID cannot be controlled from outside a container image.
- **This turn's rehearsal used mode `0644`** for exactly this reason (to work around the uid mismatch inside the sandbox, matching `silida.conf`'s own real-world precedent) — see `PRODUCTION_RESEARCH_PAGE_SEC3_TEST_RESULTS.csv` `SEC3-PERM-001`. **The `0640` + matching-GID design above is the recommended target for production** specifically because production administrators can choose the container's numeric GID deliberately (e.g. via a custom `nginx:1.25-alpine`-based image that creates its `nginx` group with GID `101` and adding a host group with the same GID `101` as the file's group) in a way this disposable, unmodified stock-image rehearsal could not cleanly demonstrate without building a custom image — flagged as a **SEC-4 implementation step**, not resolved here.
- **Least-privilege read isolation was verified** via `docker run --user`: a process running as the file owner's UID reads the file successfully; a process running as an unrelated UID (`65534`/`nobody`) is denied (`Permission denied`) — confirming the permission-bit mechanism itself works as expected once the correct UID/GID is assigned.
- **Fail-closed on missing file:** confirmed — `SEC3-MISS-001`, `403`, no protected content.
- **Fail-closed on unreadable file:** confirmed — `SEC3-MISS-002`, `500`, no protected content.
- **`chmod 777` is explicitly rejected** — not used anywhere in this design or rehearsal.
- **Atomic replacement:** modeled as `mv new.htpasswd credstore.htpasswd` (same-filesystem rename is atomic on Linux) rather than any in-place edit; not executed against a real file this turn since no real file was created — this is a documented procedure for SEC-4, not a rehearsed mechanism (rehearsing it meaningfully requires a live reload cycle against the target permission model, which depends on the GID decision flagged above).

## 4. Rotation Procedure (design only, not executed)

```text
1. Generate the new credential line(s) into a NEW file (never overwrite in place).
2. Verify the new file's syntax with `htpasswd -v` or equivalent, off any live path.
3. Set ownership and mode identically to the file it will replace.
4. Atomically replace: mv new_file live_path (same filesystem).
5. No reload is required for host Nginx or voc_nginx — auth_basic_user_file is
   read per-request, not cached at startup (verified structurally: SEC-2A's
   missing/unreadable-store tests already showed per-request file access, not
   startup-time loading, for the same directive).
6. Verify with one authenticated smoke-test request per protected route.
7. Retain the immediately-prior file as a dated rollback copy, permissioned
   identically, for the remainder of the maintenance window only.
```

## 5. Compatibility with the Entra/OIDC Target

This design is explicitly transitional (60 days, per `SEC-DEC-07`). It does not block the Entra/OIDC target (`SEC-DEC-06`): the credential file is deleted, and both nginx layers' `auth_basic` blocks are replaced by whatever the OIDC-integrated design requires, at end of the transition window (day 45 review, day 60 expiry) — no data or schema from this design carries forward into that migration.
