# GET /api/forts/power-status — Public Summary Contract (Design Only)

> **Design document. Not implemented. No endpoint created or modified.**

---

## 1. Purpose

Design the minimal public response contract for the retained public map endpoint, based on the Phase 1 frontend-dependency audit (`FORT_POWER_STATUS_FIELD_CLASSIFICATION.csv`) — not assumption.

## 2. Candidate Schema (illustrative Pydantic sketch — NOT applied)

```python
# CANDIDATE ONLY -- NOT APPLIED
class PublicPowerStatusEvent(BaseModel):
    year: Optional[int] = None
    title: str          # reviewed public title -- see § 5, not the raw DB title as-is

class PublicPowerStatusItem(BaseModel):
    fort_id: int
    fort_name: str
    dominion_status: str
    as_of_event: PublicPowerStatusEvent
```

## 3. Field Justification (every field required for the existing public map, per Phase 1)

| Field | Why required | Evidence |
|---|---|---|
| `fort_id` | Not currently read by `atlas.js`, but a stable identifier is reasonable to retain for future frontend use (e.g. linking to `openFortById()`, an existing pattern used elsewhere for fort markers) — included as a low-risk identity field, not a content field | `FORT_POWER_STATUS_FIELD_CLASSIFICATION.csv` — `UNUSED_BY_FRONTEND` today, but zero risk to keep since it carries no research content |
| `fort_name` | Coordinate lookup (`FORT_COORDS[item.fort_name]`) and popup header | `atlas.js:788, 822` |
| `dominion_status` | Marker color/label, core to the map's entire visual purpose | `atlas.js:794-795` |
| `as_of_event.year` | Popup meta line | `atlas.js:826` |
| `as_of_event.title` | Popup event description line | `atlas.js:825` — **but see § 5, the current raw value is not confirmed as reviewed public copy** |

## 4. Fields Deliberately Excluded (not model diagnostics, but still not carried into the minimal contract)

```text
as_of_event.id           -- UNUSED_BY_FRONTEND, no public need identified
as_of_event.event_date_raw -- UNUSED_BY_FRONTEND, no public need identified
```
Excluding these is a minimal-surface-area choice, not a security necessity — they carry no research-sensitive content. If a future public feature needs them, they can be added back through the same review discipline as any other public field addition, not silently.

## 5. Public-Copy Review Requirement

`as_of_event.title` is currently the **raw** `LinimasaEvent.title` database column — written for internal/research bookkeeping, never explicitly reviewed against a "is this wording appropriate for public display" standard. The researcher's decision names a distinct concept, "judul publik yang telah direview" (a reviewed public title), which this contract's `title` field is meant to eventually hold. **Until that review pass happens, this contract's `title` field would, if implemented today, still carry the unreviewed raw value** — this is flagged, not silently resolved, per the researcher's explicit instruction not to promote unreviewed content to "approved for publication" status merely because it's convenient. The review process itself (who reviews, what standard, how flagged events are handled) is out of scope for this design turn.

Likewise, `dominion_status` is listed by the researcher as "status ringkas yang telah direview" — the current raw enum value is already terse and closer to a genuine "summary" than free-text `title`, but the same review-pending caveat formally applies to it.

## 6. Backward-Compatibility Analysis

```text
Removed fields (currently returned, would no longer be):
  cluster, p_self_current_status, dynamics_series, rmse,
  as_of_event.event_date_raw, as_of_event.text_asli,
  as_of_event.source_document, as_of_event.provenance (all subfields),
  as_of_event.id

atlas.js consequence if this contract replaced the current endpoint AS-IS,
without any frontend change:
  - marker loses cluster pennant, dwell ring, sparkline (all already
    conditionally rendered -- code already null-checks these, no crash)
  - popup loses source_document line and provenance badge (provenanceBadgeHTML
    already returns "" on missing provenance -- no crash)
  - VISUAL REGRESSION: the map layer would look materially plainer (no
    Model 2/5/6 visual signals) -- this is a real, visible product change,
    not a silent no-op, even though nothing crashes
```

**This is why Option B (§ `FORT_POWER_STATUS_ENDPOINT_MIGRATION_PLAN.md`) is recommended over swapping this endpoint's contract directly** — atlas.js would need to be migrated to call a new protected endpoint (with authentication) for the Model 2/5/6 visual layer *before* this minimal contract could replace the current one without a visible regression.

## 7. Requirements Checklist

```text
[x] enough fields for the existing public map (per Phase 1 evidence)
[x] no model diagnostic fields (cluster/p_self_current_status/dynamics_series/rmse excluded)
[x] no primary-source quotation by default (text_asli excluded)
[x] no internal provenance structure by default (provenance excluded)
[ ] uncertainty retained where necessary -- N/A, no uncertainty field exists
    in the minimal public contract; if a future public "confidence" indicator
    is wanted, it would need its own reviewed design, not a passthrough of
    provenance.researcher_review_required
[x] deterministic JSON schema (Pydantic model, same discipline as the
    current endpoint)
[x] explicit null handling: year remains Optional[int]=None (unchanged
    from current); title has no natural null case (LinimasaEvent.title is
    NOT NULL in the current schema per PowerStatusEvent)
[x] explicit year handling: same `year <= requested_year`, "most recent
    qualifying event" query logic as today -- unchanged, this is Layer 1
    map-state logic, not a research-detail concern
[x] no silent substitution of claim for effective control -- this contract
    changes what is EXPOSED, not what is QUERIED; the underlying "most
    recent dominion_status event" selection logic (backend/routers/forts.py:398-401,
    already carefully commented against exactly this failure mode) is
    completely unchanged by this design
```

## 8. Status

```text
DESIGN_ONLY_NOT_IMPLEMENTED
```
