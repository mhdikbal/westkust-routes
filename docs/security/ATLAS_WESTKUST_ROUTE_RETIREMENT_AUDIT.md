# ATLAS /westkust/ Route Retirement — Audit

> **Read-only planning turn. No route changed. No production, Nginx, Cloudflare, DNS, or application config modified. No credential created. Nothing staged, committed, or pushed.**

---

## 1. Decision Status Carried Forward

```text
ROUTE-DEC-01: APPROVED_WITH_LIMITATIONS
Canonical route: /atlas/
Legacy route:    /westkust/
Target behavior: /westkust/<path>?<query> -> /atlas/<path>?<query>
Production execution: NOT_AUTHORIZED
```

### Six Implementation Decisions — Adjudicated

The six remaining decisions listed in § 6 below were adjudicated by the researcher and recorded in `ATLAS_WESTKUST_ROUTE_RETIREMENT_DECISION_LEDGER.csv` and `ATLAS_WESTKUST_ROUTE_RETIREMENT_ADJUDICATION.md`:

```text
ROUTE-IMPL-DEC-01: APPROVED_WITH_LIMITATIONS  (redirect syntax: simple Nginx return-based 301)
ROUTE-IMPL-DEC-02: APPROVED_WITH_LIMITATIONS  (static asset handling: audit-and-preserve-compatibility-first)
ROUTE-IMPL-DEC-03: APPROVED                   (observation period: 30 days, review at Day 0/1/7/14/30)
ROUTE-IMPL-DEC-04: DEFERRED                   (SEO infrastructure: separate milestone)
ROUTE-IMPL-DEC-05: NOT_AUTHORIZED             (production execution)
ROUTE-IMPL-DEC-06: REJECTED                   (Basic Auth bundling)
```

Redirect design direction is established by these decisions; the redirect itself remains **NOT_IMPLEMENTED**. Production execution remains **NOT_AUTHORIZED**. Basic Auth bundling with this route-retirement work is **rejected** — the two remain on independent authorization tracks. `SECURITY_ACCESS_CONTROL_GATE` remains **NOT_PASSED**. This adjudication does not modify the discovery findings (§ 2 of `ATLAS_WESTKUST_ROUTE_RETIREMENT_DISCOVERY.md`) or the dependency ledger rows (`ATLAS_WESTKUST_ROUTE_DEPENDENCY_LEDGER.csv`), both of which stand unchanged from the frozen baseline.

## 2. Phase 4 — Authentication Consequence (two stages)

### Transition stage

- `/atlas/` application routes protected (per `PRODUCTION_RESEARCH_PAGE_SEC3_CANDIDATE_DIFF.md` § B, already designed);
- `/westkust/` **still tested** as a possible compatibility path — not yet redirect-only, both prefixes remain independently reachable and independently protected during this stage;
- both research APIs (`/api/research/linimasa`, `/api/research/pemodelan-dashboard`) protected regardless of which page prefix a client arrived through;
- direct port 8084 containment (N1) required, unaffected by this retirement plan.

### Post-retirement stage

- `/westkust/` becomes redirect-only — no application content is served beneath it, only a `301` to the equivalent `/atlas/` path;
- `/atlas/` is the sole public application prefix;
- both research APIs remain directly protected, independent of the page-prefix redirect (the APIs were never proxied through the page-prefix mechanism to begin with — see `ATLAS_WESTKUST_ROUTE_DEPENDENCY_LEDGER.csv` DEP-05);
- inner `voc_nginx` protection remains required (defense-in-depth, unaffected);
- N1 containment remains required, unaffected.

**Verification that the redirect cannot bypass authentication or cache protected content:** a `301` response itself carries no protected body — it is a bare `Location` header and a short generic message. Whether the redirect is issued *before* or *after* an `auth_basic` check (i.e., whether `/westkust/protected-path` demands a credential before or after redirecting) is a specific ordering decision for the eventual candidate config, not yet fixed by this plan — but either ordering is safe: if the redirect fires first, the client still must authenticate at the `/atlas/` destination before receiving content; if the auth check fires first, an anonymous request never reaches the redirect at all. Neither path can serve protected content over an unauthenticated `/westkust/` request. `RETIRE-AUTH-001`/`002` in the test matrix record this as a design-review finding, not yet a live test (no candidate config has been implemented).

## 3. Phase 5 — SEO and Canonicalization

Planned, not implemented: canonical URL points to `/atlas/`; a sitemap (if ever added) would emit `/atlas/` only; public navigation would emit `/atlas/` only; documentation links would migrate to `/atlas/`; `/westkust/` remains redirect-only; no duplicate indexing; no conflicting canonical tags; no protected research URL ever included in a public sitemap (neither research API nor the protected pages are public-indexable content once Basic Auth is eventually implemented). **Important finding from discovery:** no canonical-link, `og:url`, `robots.txt`, or `sitemap.xml` mechanism currently exists anywhere in the application (`ATLAS_WESTKUST_ROUTE_DEPENDENCY_LEDGER.csv` DEP-06) — this workstream would need to *build* that infrastructure, not merely redirect an existing value to a new target.

## 4. Phase 6 — CARTO Basemap Consequence

Confirmed: both prefixes currently share the identical keyless CARTO `light_all` raster tile configuration (live-verified this turn, `ATLAS_WESTKUST_ROUTE_RETIREMENT_DISCOVERY.md` § 2, static asset check). Redirecting `/westkust/` to `/atlas/` does **not** itself fix the CARTO watermark — the watermark is a property of `atlas.js`'s tile URL, served identically regardless of which prefix a client uses to reach the page. Basemap remediation remains `ATLAS_BASEMAP_PROVIDER_OPTIONS.md`'s separate, unresolved workstream (Workstream B from the prior turn's three-workstream split). No CARTO key was created this turn. `frontend/map_app/static/map_app/js/atlas.js` remains unchanged (checksum unchanged from every prior turn's reading).

## 5. Phase 7 — Compatibility and Rollback

| Element | Design |
|---|---|
| Pre-change route snapshot | `ATLAS_WESTKUST_ROUTE_RETIREMENT_DISCOVERY.md` § 2 (this turn's live inventory) serves as the baseline |
| Nginx config backup | Full `silida.conf` backup before any candidate edit, per the same pattern already established in `PRODUCTION_RESEARCH_PAGE_SEC3_PRODUCTION_LIKE_PLAN.md` § 7 |
| Syntax validation | `nginx -t` before any reload, same discipline as every prior SEC-3/SEC-3A/SEC-3B/SEC-3C turn |
| Redirect smoke tests | `RETIRE-CAND-001..010` in `ATLAS_WESTKUST_ROUTE_RETIREMENT_TEST_MATRIX.csv` |
| Deep-link tests | Re-run `RETIRE-PRE-001..005` against the post-change state, confirm identical or correctly-redirected results |
| Authentication tests | `RETIRE-AUTH-001/002`, re-verified live once Basic Auth is eventually implemented (separate, still-pending workstream) |
| API tests | Confirm both research APIs unaffected — they are not proxied through the page-prefix redirect at all |
| Rollback trigger | Any of: redirect loop; lost query strings; broken deep links; static assets fail; `/atlas/` itself becomes unavailable; authentication bypass; API regression; unexpected `POST`/non-`GET` behavior |
| Rollback procedure | Restore the pre-change `silida.conf` backup, `nginx -t`, `systemctl reload nginx` — identical low-blast-radius pattern as every prior rollback runbook in this series |
| Observation period | Not fixed by this plan — a specific duration (hours vs. days) before considering the redirect "settled" is a remaining decision, not resolved here |

## 6. Remaining Decisions (not resolved by this planning turn)

> **Note:** No decision ledger exists for this workstream (unlike the ontology validation series, which uses `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv`). Per explicit researcher instruction, this freeze turn does not create one and does not treat the values below as recorded decisions — they are the researcher's own stated recommendations, captured here as planning output only. Formal adjudication (if any) remains a separate, future, explicitly authorized step.

1. **Exact Nginx directive syntax for the redirect** (design sketch only, `ATLAS_CANONICAL_ROUTE_REDIRECT_PLAN.md` § 1). *Researcher recommendation:* the simplest `return`-based Nginx rule that preserves path and query string exactly once, per the candidate sketch already drafted — not the more complex `rewrite`/regex-capture alternative, unless the smoke-test phase finds it insufficient.
2. **Whether static assets under `/westkust/` also redirect, or remain dual-served** (§ 1 caveat). *Researcher recommendation:* audit first, preserve compatibility first — do not redirect or otherwise change static-asset behavior until the audit (`RETIRE-CAND-*` smoke tests) confirms no client depends on `/westkust/`-prefixed static URLs directly.
3. **Observation period length before/after the change.** *Researcher recommendation:* **30 days** of dual-serving/monitoring before considering the redirect (or the eventual retirement of `/westkust/` application content) settled.
4. **Whether to build canonical-link/sitemap infrastructure now or defer it** (Phase 5 finding). *Researcher recommendation:* defer — treat SEO/canonicalization infrastructure as a **separate milestone**, not bundled into this redirect work.
5. **Exact maintenance window and execution authorization for actually applying the redirect** — a separate, explicitly authorized turn, not this one. *Researcher recommendation:* **PENDING** — production execution is not authorized by this planning turn and remains a future, separately-authorized decision.
6. **Relationship to the still-open `SEC3-F-02` and still-pending Basic Auth implementation.** *Researcher recommendation:* **do not bundle** — keep the route-retirement candidate Nginx edit separate from the Basic Auth candidate edit; each proceeds on its own authorization track.

These six values are recorded here as the researcher's stated recommendations only. They are not implemented, not applied to any config, and not entered into any decision ledger by this turn.

## 7. Secret Scan

```text
NO_SECRET_PATTERN_MATCH
```

No credential, API key, password, or sensitive value appears in any of the five outputs. Live HTTP checks captured only status codes, `Location` headers, and generic content-length/type — no cookies, no Authorization headers (none exist, since production has no Basic Auth), no response bodies beyond confirming a `200`/`301` status class.

## 8. Baseline Verification

| Item | Result |
|---|---|
| Production `silida.conf` | unchanged (read-only inspection only) |
| `atlas.js` | unchanged |
| Docker Compose / backend / frontend / database | unchanged |
| All prior SEC-2 through SEC-3D and ATLAS_* documents | unchanged |
| Ontology decision-ledger working diff | unchanged |
| Five ontology validators | not re-run this turn (unaffected by a route-planning-only turn; last confirmed PASS in the immediately preceding turn) |

## 9. Production Status

```text
PRODUCTION: NO_GO (unchanged)
SECURITY_ACCESS_CONTROL_GATE: NOT_PASSED (unchanged)
Port 8084: unchanged
Basic Auth: still not implemented
```

---

## Final Status

```text
ATLAS_WESTKUST_ROUTE_RETIREMENT_PLAN_READY_FOR_REVIEW
```
