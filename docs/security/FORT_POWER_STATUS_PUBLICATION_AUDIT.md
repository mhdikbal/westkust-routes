# GET /api/forts/power-status — Publication Split Audit

> **Consolidated audit. Decision recording and implementation planning only. No source, API, or authentication modified. Nothing staged/committed/pushed/deployed.**

---

## 1. Endpoint and Frontend Consumer

```text
Endpoint: GET /api/forts/power-status?year=...
Router:   backend/routers/forts.py:392, mounted at /api/forts, tag "Map"
Consumer: frontend/map_app/static/map_app/js/atlas.js drawPowerStatus()
          (atlas.js:770-834) -- the ONLY consumer, called from the public
          Atlas map's "status kekuasaan" toggle (#btn-power-status)
```

## 2. Current Field Count

```text
18 leaf fields total (including nested as_of_event.* and
as_of_event.provenance.*), full inventory in
FORT_POWER_STATUS_FIELD_CLASSIFICATION.csv
```

## 3. Fields Required by the Public Map (per Phase 1 evidence, not assumption)

```text
fort_name, dominion_status, as_of_event.year, as_of_event.title
```

## 4. Fields Not Used by the Public Map at All

```text
fort_id, as_of_event.id, as_of_event.event_date_raw, rmse,
as_of_event.provenance.researcher_review_required,
as_of_event.provenance.multi_source_verified
```
(Backend returns these; `atlas.js` never reads them — confirmed by exhaustive grep across the whole file, not just the `drawPowerStatus` function.)

## 5. Source-Excerpt Fields

```text
as_of_event.text_asli -- the primary-source quotation itself; also currently
UNUSED_BY_FRONTEND, making it the single clearest candidate for protection
(zero public-map cost to removing it)
```

## 6. Provenance Fields

```text
as_of_event.provenance.status, .label, .tooltip (currently rendered as a
badge), .researcher_review_required, .multi_source_verified (currently
unused)
```

## 7. Model-Output Fields

```text
cluster (Model 5), p_self_current_status (Model 2), dynamics_series
(Model 5/6-adjacent dwell series), rmse (unattributed to a specific model
in the current flat schema -- flagged in
FORT_POWER_STATUS_PROTECTED_RESEARCH_CONTRACT.md § 4 as needing explicit
model_id disambiguation in any future implementation)
```

## 8. Publication Classification

```text
Current:  PUBLIC_WITH_UNREVIEWED_RESEARCH_DETAIL
Target:   PUBLIC_MAP_SUMMARY_WITH_PROTECTED_RESEARCH_DETAIL
```

## 9. Contracts and Migration (see companion documents for full detail)

```text
Public-summary contract:    FORT_POWER_STATUS_PUBLIC_SUMMARY_CONTRACT.md
  -- fort_id, fort_name, dominion_status, as_of_event.year, as_of_event.title
  -- title/dominion_status flagged as PENDING PUBLIC-COPY REVIEW, not yet
     confirmed as reviewed public copy

Protected-detail contract:  FORT_POWER_STATUS_PROTECTED_RESEARCH_CONTRACT.md
  -- all remaining fields, with explicit per-model identity (§4 of that doc)
  -- text_asli preserved byte-for-byte, no silent alteration
  -- REQUIRES_RESEARCH_AUTHENTICATION (not yet implemented anywhere)

Recommended migration option: OPTION B (add-migrate-retire sequence)
  -- full comparison in FORT_POWER_STATUS_ENDPOINT_MIGRATION_PLAN.md
```

## 10. Temporary Risk Classification (until implementation)

```text
PUBLIC_RESEARCH_DETAIL_EXPOSURE_PENDING_REMEDIATION

- endpoint remains publicly reachable (no change made by this turn)
- no password or secret exposure identified in this endpoint specifically
- source quotations (text_asli) and model diagnostics (cluster,
  p_self_current_status, dynamics_series, rmse) are publicly available today
- publication intent for this endpoint was never explicitly adjudicated
  before this turn -- it inherited public status by default, not by review
- public map dependency (fort_name, dominion_status, year, title) prevents
  immediate shutdown of the endpoint without a replacement -- confirmed by
  Phase 1 evidence, not assumed
- remediation requires endpoint separation per Option B, not an in-place
  field removal
```

## 11. Model-Semantics Guard (Phase 6 verification)

Verified the current public response does **not** conflate:
```text
- Phase B provenance artifact: present (as_of_event.provenance), correctly
  scoped to ONE event per the ProvenanceInfo model's own documented semantic
  guard (backend/routers/forts.py:350-359) -- not conflated with fort-level
  status
- Failed Model 3B Hawkes process: ABSENT from this endpoint entirely --
  confirmed no field, no reference, no import from this endpoint touches
  the Model 3B-CD simulator or its results. The provenance artifact this
  endpoint loads is a Model-3B-adjacent BYPRODUCT (Phase B), not the failed
  model itself -- per COMPREHENSIVE_MODELING_RUNTIME_DEPLOYMENT_STATE_AUDIT.md
  Phase 3/9, this distinction is already correctly maintained in the current
  code (the provenance artifact is loaded via a clearly-commented separate
  path, backend/routers/forts.py:17-35) and this audit found no evidence of
  drift from that documented intent
- Model 2: p_self_current_status, clearly attributable
- Model 5: cluster, dynamics_series, clearly attributable
- Model 6 quantitative game theory: NOT present in this endpoint (lives
  separately in the Bokeh dashboard) -- confirmed no conflation risk exists
  here specifically, though the protected-contract design (§4 of that doc)
  pre-emptively documents how any future addition must be labeled
- Qualitative Painan/Barus game theory: NOT present in this endpoint,
  confirmed no conflation risk
```
No field in this endpoint currently implies the failed Model 3B-CD statistical model carries runtime authority. This finding matches the comprehensive audit's Phase 9 conclusion and is not contradicted by anything found in this closer read.

## 12. Secret Scan

```text
NO_SECRET_PATTERN_MATCH
```
Checked across all 5 new documents plus the field-classification CSV. No credential, key, or token value appears anywhere.

## 13. What Was NOT Done (hard boundaries respected)

```text
- backend/routers/forts.py: NOT edited (read-only inspection only)
- frontend/map_app/static/map_app/js/atlas.js: NOT edited (read-only
  inspection only, confirmed unchanged: git status shows no diff)
- No new route created
- No response contract changed
- No authentication activated
- No container rebuilt or restarted
- Nothing staged, committed, pushed, or deployed
```

## 14. Git Status

```text
6 new untracked files under docs/security/ (this document + 5 companions)
No tracked file modified by this turn
Ontology decision-ledger working diff: unchanged (verified before and after)
```

## 15. Confirmations

```text
No source or API changed: CONFIRMED
No stage/commit/push/deploy: CONFIRMED
```

---

## Final Status

```text
FORT_POWER_STATUS_PUBLICATION_SPLIT_PLAN_READY_FOR_REVIEW
```
