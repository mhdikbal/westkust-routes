# Production Research Page — Environment and Route Boundary Correction Audit

> **Read-only verification turn. No production, source, or config change. Nothing staged, committed, or pushed.**

---

## 1. Researcher Correction (as proposed)

The researcher proposed recording `/atlas/` as production (`westkust-prod`) and `/westkust/` as a WSL/local-only development entry point, on the premise that shared application behavior across the two paths reflects shared source code, not shared production routing, and that the prior dual-prefix findings should be reclassified accordingly.

**This turn's read-only verification does not support that premise.** The finding is reported plainly below rather than force-fit to match it.

## 2. Production Environment

```text
Host:        westkust-prod (silida.org)
Public URL:  https://silida.org/atlas/  -> HTTP 200 (verified live, this turn)
Public URL:  https://silida.org/westkust/ -> HTTP 200 (verified live, this turn)
```

## 3. WSL Development Environment

The local WSL sandbox used throughout SEC-2A/SEC-3/SEC-3A/SEC-3B/SEC-3C (and its disposable Docker containers) never publishes anything to the public internet — it is not reachable outside this session's own tooling. It has no relationship to `https://silida.org` at all. The researcher's framing of `/westkust/` as "the WSL/local entry point" conflates two different things: the **path prefix** `/westkust/` (a routing concept) and the **WSL sandbox** (a separate, unrelated execution environment used only for disposable rate-limit testing). The disposable sandbox never served `/westkust/` or `/atlas/` as public URLs — it served synthetic `sec3a_*`/`sec3b_*`/`sec3c_*` container ports, unrelated to `silida.org`'s real routing.

## 4. Shared Source versus Shared Route — Verified, Not Assumed

The researcher's own stated principle — "shared application behavior may arise from shared source code; shared source code does not prove shared production routing" — is correct in general, and is exactly why this turn did not rely on matching application content alone. Instead, Phase 1 inspected the actual production Nginx configuration and made live requests to the actual production domain. Both independently confirm shared **routing**, not merely shared source:

- `/etc/nginx/conf.d/silida.conf` (read on `westkust-prod`, this turn) contains **two separate `location` blocks**, `location /westkust/ { ... }` and `location /atlas/ { ... }`, both nested under `server_name silida.org;` (the production public server block, not a WSL/staging block — there is no such block on this host).
- Both blocks `proxy_pass http://127.0.0.1:8084/;` — the identical backend.
- The config's own comment, written by the project team and dated, states outright: *"Atlas (alias publik dari /westkust/, konsolidasi 2026-07-08) — /atlas/ dulu halaman statis beku di Astro (salido-web), tidak pernah ikut update deploy Docker — sekarang proxy sama persis spt /westkust/ supaya cuma ada SATU sumber kebenaran."* (Atlas is a public alias of /westkust/, consolidated 2026-07-08 — /atlas/ used to be a frozen static Astro page that never followed Docker deploys; it now proxies identically to /westkust/ so there is only one source of truth.)

This is not an inference from matching content — it is the production team's own documented intent, confirmed by the live config and live HTTP responses.

## 5. Production Routing Verification (Phase 1 results)

| Check | Result |
|---|---|
| 1. Production vhost exposes `/atlas/`? | **Yes** — `location /atlas/` under `server_name silida.org` |
| 2. Same public production host also exposes `/westkust/`? | **Yes** — `location /westkust/` under the same `server_name silida.org` |
| 3. `/westkust/` status | **Publicly routed** — live `HTTP 200` from the public internet, not absent, not rejected, not merely local |
| 4. Alternate production host/port serving the same app? | `www.silida.org` redirects to `silida.org` (301, per the config's canonicalization block); `www.silida.org/westkust/` returned `502` in this turn's spot-check — consistent with the canonical-redirect design (the `www` server blocks 301-redirect to the apex before any `/westkust/`-specific location would be reached; the `502` observed is not evidence of a second application, and was not investigated further as it is outside this turn's scope) |
| 5. Direct port 8084 without the public prefix | `curl` from the production host's own loopback to `http://127.0.0.1:8084/westkust/` and `http://127.0.0.1:8084/atlas/` both return `404` — because the backend (Django) has no route literally named `/westkust/` or `/atlas/`; the host Nginx `proxy_redirect`/`sub_filter` machinery is what maps the public prefix onto the backend's real, prefix-less routes (`/`, `/riset/pemodelan/`, `/linimasa/`, etc.). This is consistent with, not contradictory to, both prefixes being live production aliases — it confirms the prefix-stripping happens at the host Nginx layer, exactly as SEC-1/SEC-3's original discovery documented. |
| 6. Host header behavior | An unmatched `Host: evil.example.com` against `silida.org`'s IP returns `403` (Cloudflare-level rejection reached before any application response) — not a bypass |

## 6. Corrected Classification

Per the researcher's own Phase 2 decision tree:

```text
DUAL_PREFIX_PRODUCTION_BYPASS: CONFIRMED
```

Not Option A (`/westkust/` absent), not Option B (`/westkust/` redirects to `/atlas/` — it does not; both serve content directly, independently, at their own paths). Both prefixes are live, independent, publicly-routed production aliases of the identical backend application, exactly as every prior SEC-1 through SEC-3D document has described them. **No reclassification is warranted or applied.**

## 7. Corrected Authentication Boundary

No correction is needed. The production authentication boundary, as already designed in `PRODUCTION_RESEARCH_PAGE_SEC3_CANDIDATE_DIFF.md` § B and rehearsed throughout SEC-2/SEC-2A/SEC-3/SEC-3A, correctly targets **both** prefixes symmetrically:

```text
/atlas/riset/pemodelan/
/atlas/riset/pemodelan/panduan/
/atlas/linimasa/

/westkust/riset/pemodelan/
/westkust/riset/pemodelan/panduan/
/westkust/linimasa/

/api/research/linimasa
/api/research/pemodelan-dashboard
```

This is required in production, not merely as "local/WSL validation scope" — both prefixes are equally public and equally unauthenticated today.

## 8. Corrected Basemap Scope

No correction is needed here either. `ATLAS_BASEMAP_API_KEY_REQUIRED_DISCOVERY.md` § 5 already correctly stated: *"per the production topology already documented ..., both `/atlas/` and `/westkust/` are host-Nginx aliases proxying to this identical Django root. The watermarked CARTO tile therefore affects both public prefixes identically."* This turn's verification (§ 4–5 above) confirms that statement was accurate, not merely assumed. The single active source locator (`frontend/map_app/static/map_app/js/atlas.js:378`, CARTO `light_all` raster style, missing API key, `HTTP 200` with a watermarked image) is unchanged and remains the correct, sole diagnosis.

## 9. Historical Security Findings Affected

None. Re-checked explicitly:

| Finding | Status |
|---|---|
| Port 8084 external exposure | **Unaffected, still valid** |
| Unauthenticated research APIs | **Unaffected, still valid** |
| Absence of production Basic Auth | **Unaffected, still valid** |
| Inner-loopback defense-in-depth requirement | **Unaffected, still valid** |
| Option A credential-store design | **Unaffected, still valid** |
| `SEC3-F-01` (real-Django prefix behavior) | **Unaffected, still `TARGETED_MITIGATION_VALIDATED`** |
| `SEC3-F-02` (numeric rate-limit closure) | **Unaffected, still `OPEN_REQUIRES_TARGETED_RATE_LIMIT_RETEST`** |
| `SEC3-F-03` (immediate provider-load-balancer peer) | **Unaffected, still recorded as-is** |
| CARTO API-key watermark root cause | **Unaffected, still `ATLAS_BASEMAP_API_KEY_REQUIRED_DIAGNOSED`** |

The environment-boundary question this turn investigated is orthogonal to all nine — none of them depended on `/westkust/` being local-only, and none is invalidated by it being confirmed public.

## 10. Historical Evidence Preserved

No test result cell in any SEC-2/SEC-2A/SEC-3/SEC-3A/SEC-3B/SEC-3C CSV was modified by this turn. The dual-prefix test rows throughout that series (e.g. `SEC2-T-006` through `T-011`, `SEC3-OUTER-001` through `-008`, `SEC3A-DJ-001` through `-020`) were modeling real production topology, not a portable-but-unconfirmed hypothesis — this turn's verification retroactively confirms their premise was correct, it does not reclassify them as merely "validation of portable route-prefix behavior."

## 11. Required Document Corrections

**None identified.** A full-repository search for the exact phrases and concepts named in the correction request ("both public prefixes," "production aliases," "identical production proxies," "dual-prefix production bypass," "protect /atlas/ and /westkust/ identically") was performed across every committed and uncommitted `docs/security/*.md` and `docs/security/*.csv` file in this series. Every occurrence found is `CORRECT` per this turn's own verification (§ 5–6) — none require a qualifier, none are incorrect, and none needed a historical-test-description reclassification, because the underlying claim they made was accurate. This section exists to record that the search was performed and found no discrepancy, not to list corrections that turned out not to be needed.

## 12. Remaining Security Findings

Unchanged from `PRODUCTION_RESEARCH_PAGE_SEC3D_AUDIT.md` and `ATLAS_BASEMAP_WATERMARK_AUDIT.md` — `SEC3-F-02` still open pending a working rate-limit test environment; `SEC3D-DEC-01..16` still `PENDING`; basemap watermark still undiagnosed for remediation (diagnosis complete, no fix chosen).

## 13. Production Status

```text
PRODUCTION: NO_GO (unchanged)
SECURITY_ACCESS_CONTROL_GATE: NOT_PASSED (unchanged)
Port 8084: still externally exposed, unchanged
Basic Auth: still not implemented, unchanged
```

## 14. Final Classification

```text
ATLAS_ENVIRONMENT_ROUTE_BOUNDARY_CORRECTION_READY_FOR_REVIEW
```

The correction requested could not be applied as proposed, because direct read-only verification of the actual production host contradicts its premise. This is reported to the researcher for a decision, not silently overridden or silently applied. No document, finding, or evidence file in the existing security series required modification as a result of this audit.
