# GET /api/research/forts/power-status-detail — Protected Research Contract (Design Only)

> **Design document. Not implemented. No endpoint created. No authentication activated.**

---

## 1. Purpose

Design a separate research-detail response contract preserving every field currently returned by `/api/forts/power-status` that is not part of the minimal public contract, per the researcher's explicit "PROTECTED" field list.

## 2. Candidate Schema (illustrative Pydantic sketch — NOT applied)

```python
# CANDIDATE ONLY -- NOT APPLIED
class ModelOutput(BaseModel):
    """One model's output, explicitly identified -- never presented as
    interchangeable with another model's output."""
    model_id: str            # "model2" | "model5" | "model6"
    model_name: str          # human-readable, e.g. "Markov (Model 2)"
    model_status: str        # "ACTIVE" | "SUPERSEDED" | "NOT_VALIDATED"
    values: dict              # model-specific fields, see § 4

class ProtectedProvenanceDetail(BaseModel):
    status: str
    label: str
    tooltip: str
    researcher_review_required: bool
    multi_source_verified: bool
    join_source: str = "docs/thesis/colab/MODEL_3B_EVENT_SOURCE_PROVENANCE_WORKING.csv"
    join_method: str = "Phase B deterministic hash join (backend/routers/forts.py:_provenance_join_hash)"

class ProtectedPowerStatusEvent(BaseModel):
    id: int
    year: Optional[int] = None
    event_date_raw: Optional[str] = None
    title: str                       # raw, unreviewed DB title -- NOT the
                                      # reviewed public title
    text_asli: str                   # UNCHANGED, byte-for-byte from source --
                                      # see § 3, no silent alteration
    source_document: str
    provenance: Optional[ProtectedProvenanceDetail] = None

class ProtectedPowerStatusItem(BaseModel):
    fort_id: int
    fort_name: str
    dominion_status: str
    as_of_event: ProtectedPowerStatusEvent
    models: List[ModelOutput] = []   # explicit, identified list -- see § 4
    evidence_state: str               # see § 6
```

## 3. `text_asli` Integrity Guarantee

`text_asli` (the primary-source quotation) **must be preserved unchanged** — no truncation, no re-encoding, no re-formatting, no summarization. It is passed through from `LinimasaEvent.text_asli` exactly as the public endpoint does today (`backend/routers/forts.py` currently does no transformation on this field). This design introduces no new transformation step for it — the protected contract's obligation here is purely "don't newly touch it," not "add new integrity tooling."

## 4. Model Output — Explicit Identity, No Conflation (Phase 6 requirement)

Per the required model-semantics guard, the protected contract must **not** flatten `cluster`, `p_self_current_status`, `dynamics_series`, `rmse` into a single undifferentiated blob. Each carries a distinct provenance that must travel with it:

```text
Model 2 (Markov, per-fort transition probabilities):
  contributes: p_self_current_status
  status: validated within its own documented scope (per project memory --
    not independently re-verified by this design turn)

Model 5 (System Dynamics):
  contributes: dynamics_series, cluster (archetype taxonomy, CLD)
  status: validated within its own documented scope

Model 6 (quantitative game theory, revealed-preference payoff from Model 2's
  E[dwell]):
  contributes: no distinct field currently visible in PowerStatusItem itself
    -- Model 6 output is separately served via the Bokeh dashboard
    (/riset/pemodelan/), not through this endpoint. If a future change adds
    Model 6 fields to this endpoint, they must carry model_id="model6" and
    the same "revealed preference, not real payoff" caveat already present
    in the Bokeh dashboard's own labeling (per COMPREHENSIVE_MODELING_
    RUNTIME_DEPLOYMENT_STATE_AUDIT.md Phase 3/4 findings) -- not a bare number.

rmse:
  belongs to whichever model computed it (backend/routers/forts.py does not
  currently disambiguate this in the flat PowerStatusItem shape) -- the
  protected contract's ModelOutput.model_id field exists specifically to
  fix this ambiguity, not carry it forward.

Model 3B-CD (Hawkes process, FAILED per COMPREHENSIVE_MODELING_RUNTIME_
  DEPLOYMENT_STATE_AUDIT.md Phase 3):
  contributes: NOTHING to this endpoint today, and must contribute nothing
  to the protected contract either. The Phase B provenance artifact this
  endpoint DOES load is a byproduct of the Model 3B research thread, but is
  not the Model 3B statistical model itself, and must never be labeled or
  presented as if the failed model's results were runtime authority.
  ProtectedProvenanceDetail's `join_source` field exists specifically to
  make this provenance's lineage explicit and separate from any model
  output field.
```

## 5. Distinguishing Failed/Superseded Models

`model_status` on `ModelOutput` (§ 2) must be set per-model, not defaulted:

```text
model2:  ACTIVE (unless a future decision supersedes it)
model5:  ACTIVE (unless a future decision supersedes it)
model6:  ACTIVE, but ALWAYS carries the revealed-preference caveat
model3b: NOT_VALIDATED -- this endpoint carries no model3b field, but if one
         is ever added, it must be labeled NOT_VALIDATED / FAILED explicitly,
         never silently included as if equivalent to model2/5/6
```
This is a design requirement for any future implementation, not a value populated by this turn.

## 6. Evidence and Uncertainty State

`evidence_state` (§ 2) is a placeholder field name for whatever future implementation carries forward the existing `provenance.researcher_review_required` / `provenance.multi_source_verified` booleans plus any additional per-model uncertainty indicator (e.g. Model 2's confidence interval, Model 5's cluster-assignment confidence, if such fields exist elsewhere in `fort_model_metrics` but aren't currently surfaced by this endpoint at all — not verified by this design turn, flagged as an open question for whoever implements this).

## 7. Authentication and Operational Requirements

```text
Authentication: REQUIRES_RESEARCH_AUTHENTICATION -- same authentication
  mechanism as the other two protected research endpoints
  (/api/research/linimasa, /api/research/pemodelan-dashboard), once that
  mechanism exists (SEC-2/SEC-3 Basic Auth work, still NOT_IMPLEMENTED
  anywhere in production per the comprehensive audit). This endpoint should
  not be the first one to receive authentication in isolation -- it should
  join the same protection mechanism the other two are already queued for.
Audit-log requirement: every request to this endpoint should be logged
  (requester, timestamp, year parameter) -- no such logging currently
  exists for ANY endpoint in this application; this would be new
  infrastructure, not a reuse of something that already exists. Flagged as
  a dependency, not assumed to be trivial.
Cache policy: no public-cache policy -- unlike the current endpoint's Redis
  cache-aside pattern (backend/routers/forts.py:403-407, shared across all
  callers), a protected endpoint should either use a private/authenticated
  cache keyed by requester, or no cache at all, to avoid one authenticated
  user's cached response being reachable by another without their own
  authentication check running. Not designed further here -- flagged as an
  implementation-time decision, not resolved by this planning turn.
```

## 8. Requirements Checklist

```text
[x] preserve full provenance (ProtectedProvenanceDetail carries all 5 fields
    including the 2 currently unused by the public badge)
[x] preserve text_asli without silent alteration (§ 3)
[x] preserve source-document references (source_document field retained)
[x] preserve model outputs with model identity and version (ModelOutput.model_id
    -- "version" itself is not currently tracked anywhere in fort_model_metrics
    per this design turn's read of the schema; flagged as a gap, not invented)
[x] distinguish Model 2, Model 5, Model 6 (§ 4)
[x] mark failed or superseded models (§ 5, model_status field)
[x] do not imply Hawkes Model 3B validation (§ 4, explicit exclusion)
[x] include evidence and uncertainty state (§ 6, flagged as needing further
    design at implementation time)
[x] add future authentication requirement (§ 7)
[x] add audit-log requirement (§ 7)
[x] use no public-cache policy (§ 7)
```

## 9. Status

```text
DESIGN_ONLY_NOT_IMPLEMENTED
```
