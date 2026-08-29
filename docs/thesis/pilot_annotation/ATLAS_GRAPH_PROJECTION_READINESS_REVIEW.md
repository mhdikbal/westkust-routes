# Graph Projection Readiness Review

> **FROZEN — GRAPH PROJECTION CONTRACT v1.0 (2026-08-28).**
> This document is now the binding contract for any future power-relations graph projection. Its node-projection candidates (§1), edge-projection rules (§2), required edge metadata (§3), and actor-identity rule (§4) may not be altered, weakened, or silently reinterpreted by a future build step — only superseded by a new, explicitly-recorded decision that reopens this contract by name. Freezing this contract does **not** by itself authorize building anything (§5 already said so; restated here so freezing cannot be read as expanding scope). SHA-256 of this frozen content is recorded in `ATLAS_GRAPH_PROJECTION_CONTRACT_FREEZE_AUDIT.md`.

**Date:** 2026-08-28
**Scope:** Langkah 3 of the post-freeze roadmap for the multi-case power-relations prototype (commit `77b79b68`). Reviews how the five Draft V2.1 migrated artifacts under `data/power_relations/migrated_v2_1/` *could* be projected into a graph structure without distorting provenance, uncertainty, or the RESEARCH_ONLY boundary — grounded in the actual field names and validator rules already in the codebase (`scripts/research_validators/power_relation_ontology_rules.json`, `validate_power_relation_ontology.py`).

**This is a review, not an implementation.** No graph is built here. No Graphify code is touched. No node or edge is materialized. This document is a readiness *contract draft* for a future, separately-authorized build step (Langkah 5 in the roadmap: "Build disposable graph projection"). Nothing here authorizes that build.

## 0. Why this is not Graphify

`graphify-out/` (this repo's existing code-knowledge-graph tool) indexes *source code* — files, symbols, imports. A power-relations graph projection would index *historical claims* — actors, places, and the relations asserted between them, each carrying provenance and uncertainty metadata that source-code nodes don't need. The two are structurally unrelated; nothing in this review proposes routing one through the other, and Langkah 8/9 of the roadmap keep them explicitly separate ("JANGAN mencampur Graphify dengan CARTO atau route redirect").

## 1. Node Projection Candidates

### 1.1 Eligible for projection now (public-facing candidate, pending Langkah 7 decision)

| Entity | Source in artifact | Notes |
|---|---|---|
| **Actor** | `actors[]` | `actor_id`, `label`/`normalized_label`/`source_label`. Carries `mandate_status`, `identity_continuity_status`, `explicit_non_identity_with` (DEC-01/DEC-02, semi-structured, RESEARCH_ONLY) — those fields project as node *attributes*, never silently promoted to public claims. |
| **Location** | `locations[]` | `location_id`, label fields. Used as relation endpoints identically to Actor (`objectIdOf()` in the prototype already treats both as valid endpoint types). |
| **Office** | Implicit in `actors[]` via mandate/role fields (no separate `offices[]` array exists in any of the 5 artifacts today) | **Not yet a first-class entity in the migrated data.** Listed as a candidate per the user's own framing, but there is nothing to project until a case populates a structured Office concept — currently office-holding is prose inside Actor records (`RECOGNIZES_OFFICE_HOLDER`/`APPOINTS_OFFICE_HOLDER` relation types exist in the closed vocabulary, but no artifact instantiates a separate Office node type). Flag as **DEFERRED_NO_DATA**, not rejected. |
| **Event** | `event_ids` on relations/observations (Tiku, Sillida use `EVT-*` ids referencing `linimasa_events.csv` rows) | Only an ID reference today, not an embedded object inside the migrated artifacts. Projecting Event as its own node requires joining against `linimasa_events` — out of this review's scope; flag as **DEFERRED_REQUIRES_JOIN**. |
| **Source** | `source_document_ids`, `source_passage_locator` | Present on every relation and every V2.1 addition entity. Eligible as a provenance node (what a relation cites), not as a historical-claim node itself. |

### 1.2 Research-only — NOT automatically public nodes

`CommercialRight`, `RightModification`, `CommandObservation`, `OperationParticipation` (Draft V2.1 §10-equivalent additions; validator rule `R-RO-01` requires `public_status == RESEARCH_ONLY` wherever the field is present, and rejects `PUBLIC`/`PUBLIC_VOCABULARY`/`PRODUCTION`/`RUNTIME_APPROVED`/`GRAPHIFY_APPROVED`/`FACTUAL_EDGE`).

If any of these four are projected at all, they must:
- carry an explicit `RESEARCH_ONLY` node-level tag in the graph, not just in the source JSON;
- never be graph-traversable in the same query path as public Actor/Location/relation nodes without that tag surfacing to the caller;
- never receive a `GRAPHIFY_APPROVED`/`PUBLIC` status by projection alone — `R-RO-01` makes that promotion an explicit, separately-authorized contract change, not a side effect of building a graph.

`OperationParticipation` has zero instances across all 5 current artifacts — this review has no real data to validate its projection shape against, so any future projection of it is **untested by definition** until a case populates one.

## 2. Edge Projection Rules

### 2.1 Only the closed 18-value vocabulary may become an edge type

Per `power_relation_ontology_rules.json`'s `closed_relation_vocabulary` (validator rule `R-VOC-06`, the same rule the multi-case prototype's `AUTHORIZED_RELATION_TYPES` mirrors exactly):

```
MVP_CORE_RELATION (14): REQUESTS_PROTECTION_FROM, PROVIDES_PROTECTION_TO, REQUIRES_MONOPOLY_FROM,
  NEGOTIATES_WITH, RECONCILES_WITH, SWITCHES_ALIGNMENT_TO, CLAIMS_JURISDICTION_OVER,
  CLAIMS_COMMODITY_MONOPOLY, CONTESTS_SUCCESSION_WITH, CONTESTS_RESOURCE_WITH,
  RECOGNIZES_OFFICE_HOLDER, COLLECTS_TOLL_FROM, LEASES_RESOURCE_TO, USES_MILITARY_FORCE_AGAINST
EXTENDED_RESEARCH_RELATION (2): EXERCISES_EFFECTIVE_CONTROL_OVER, CONTROLS_FORT
REQUIRES_MORE_EVIDENCE_RELATION (2): MAINTAINS_PARALLEL_ALIGNMENT_WITH, APPOINTS_OFFICE_HOLDER
```

A projection may create an edge type for a value in this list *only if* it also appears as an actual `relation_type` in the artifact being projected — no edge type should be pre-declared in the graph schema beyond what real relations use.

Two currently-open items constrain this further and must not be silently resolved by the projection step:
- **DEC-05/06 (CH-04, deferred):** Natal's `VOC_INSTITUTIONAL_HESITATION_ANNOTATION` relation_type is outside this vocabulary — it must not be projected as an edge at all (matches `R-VOC-06`'s own `UNAPPROVED_RELATION_TYPE` rejection). It stays unrepresented in any graph until CH-04 gets a design.
- **DEC-19 (Commodity-as-endpoint) — UPDATE 2026-08-29: decided (option b) AND implemented.** See `DEC19_TIKU_COMMODITY_ADJUDICATION_DECISION.md` §Implementation Record. A new artifact file (`tiku_1625_1740_relational_validation_artifact_v2_1_1_migrated.json`, original left unmodified) moves `REL_1649_CLAIMS_COMMODITY_MONOPOLY` and `REL_1740_CLAIMS_MONOPOLY_SALT` from `object_id=COMMODITY_*` to a `commodity` attribute + `object_id=null`; the generalized validator now passes clean against it (`ERROR=0`). **This review's own exclusion rule is superseded for these two relations specifically**: since `object_id` is now `null` rather than a Commodity id, a future projection of the `_v2_1_1_` file would not even attempt to resolve these as edges with a Commodity endpoint — the failure mode this carve-out was written to prevent no longer applies to the new file. The carve-out remains fully in force for the *original* `_v2_1_migrated.json` file, which is unchanged and still has the Commodity-endpoint `object_id` values. No graph projection has actually been built against either file; this is a readiness note, not a completed projection.

### 2.2 Must NOT be auto-derived as edges

The seven types the roadmap names, mapped to the exact source field each one would naively come from, and why deriving an edge from that field is exactly the mistake this review exists to block:

| Forbidden edge | Would naively derive from | Why blocked |
|---|---|---|
| `RESISTS` | `resistance_target_actor_id` (sibling field on a relation, DEC-08/`R-REF-06`) | `R-HRV-03`: the underlying historical claim (resistance occurred) is checked only for closed-vocabulary conformance by the validator, never adjudicated as true. Materializing it as an edge asserts a fact the ontology contract explicitly declines to assert. |
| `PATRON_OF` | — | Explicitly in `FORBIDDEN_RELATION_TYPES` in the prototype (`prototype.js`) and rejected outright by `R-VOC-06`. Never appears as a real `relation_type` in any artifact; there is no field to derive it from — flagging here only because the roadmap names it, and to confirm no projection logic should invent one from patron/client-shaped prose. |
| `CLIENT_OF` | — | Same as `PATRON_OF`. |
| `COMMANDS` | `CommandObservation.commanding_actor_id` / `commanded_actor_id` | `R-REF-03` is described in the rule registry as **safety-critical**: a CommandObservation's (commanding, commanded) actor pair must never simultaneously appear as a relation's (subject, object) pair. Deriving a `COMMANDS` edge from this pair would directly recreate the exact factual-relation shape that safety check exists to forbid. |
| `PARTICIPATES_IN` | `OperationParticipation.command_observation_id`-linked actor(s) | Same family as `COMMANDS` — an agency/coercion observation, not a factual participation claim. Zero instances in current data (§1.2), so this is a preemptive rule, not yet exercised. |
| `HOLDS_COMMERCIAL_RIGHT` | `CommercialRight.holder_actor_id` / `granting_actor_id` | `R-RO-01`: `CommercialRight.public_status` must be `RESEARCH_ONLY`. An edge between holder and grantor actors would look identical in shape to a real `relation_type` edge (e.g. `LEASES_RESOURCE_TO`) despite being governed by a completely different evidentiary standard (DEC-04's structured-object model). |
| `MODIFIES_RIGHT` | `RightModification.acting_actor_id` / `affected_actor_id` | Same rationale as `HOLDS_COMMERCIAL_RIGHT`; also chains through `right_id` to a `CommercialRight`, compounding the RESEARCH_ONLY boundary crossing if not blocked at the same layer. |

The common failure mode all seven guard against: **a research-only annotation or observation object has two actor-shaped fields, and it is structurally trivial for a graph-building script to treat any two-actor-shaped-fields object as an edge.** The existing multi-case prototype already enforces the equivalent rule for its own network view (`renderNetwork() never references commercial_rights/command_observations as edges` — validated check 11 in `validate_multi_case_power_relations_prototype.py`). This review extends that same rule to any future graph projection, not just the prototype's in-browser rendering.

## 3. Required Edge Metadata

Every projected edge must carry, mapped to the field that already exists on every `relations[]` entry in all 5 artifacts:

| Requirement | Source field(s) |
|---|---|
| Source reference | `source_document_ids` (list), `source_passage_locator` |
| Temporal scope | `valid_from`, `valid_to`, `date_precision`, `open_ended` |
| Evidence status | `evidence_strength` (LOW/MODERATE/...), `provenance_status` |
| Uncertainty | `interpretive_status` (e.g. `CANNOT_DETERMINE`, `SOURCE_DESCRIPTION_ONLY`), `explicit_or_inferred` |
| Case ID | artifact's own `case_id` (top-level field, e.g. `TIKU_V3_RELATIONAL_VALIDATION`) |
| Artifact version | `ontology_version` (`V2`/`V2.1`) + `schema_version` + the migrated file's own recorded checksum (per the migration/freeze audits) |
| Research-review state | `researcher_review_required` (boolean, present on every relation) |

None of these are new fields to invent — every one already exists on every relation in every migrated artifact today. A projection that drops any of them on the way into a graph would be lossy relative to the source data, not merely under-featured.

## 4. Actor Identity Rule

**Same label or same `actor_id` across cases ≠ same historical actor.**

This restates DEC-01/DEC-02's existing safeguard (already enforced in the multi-case prototype — validated check 7 "no cross-case actor-merge function exists" and check 9 "cross-case `actor_id` namespace diagnostic implemented and rendered") and extends it explicitly to graph projection:

- A projection must key nodes by `(case_id, actor_id)`, never by `actor_id` alone. `ACTOR_VOC` recurring across Painan/Natal/Tiku/Sillida is five independent node identities in five independent case-scoped subgraphs, not one node with five case memberships, unless a human researcher has explicitly resolved that identity (which DEC-01/DEC-02 requires to be recorded via `explicit_non_identity_with`/`identity_continuity_status` — themselves RESEARCH_ONLY fields, not silently promoted).
- Any cross-case identity overlap a projection surfaces (e.g. "these two case-scoped `ACTOR_VOC` nodes might refer to the same institution") must render as a **diagnostic annotation between two distinct nodes**, never as a graph-level merge of the two nodes into one.
- No projection script may auto-merge on label similarity, fuzzy string match, or identical `actor_id` string. This project has already seen archaic-spelling variants of the same fort name (e.g. Sillida/Salido, Priaman/Pariaman, Baros/Barus) fail to auto-resolve reliably with fuzzy matching — the risk at actor identity is the same failure mode one level up, at actor identity instead of place-name spelling.

## 5. What This Review Does Not Decide

- It does not select a graph store, format, or library.
- It does not resolve DEC-19 (Tiku Commodity-as-endpoint) or DEC-05/06 (Natal/Koto Tangah CH-04) — both stay exactly as adjudicated.
- It does not authorize building even a disposable/local graph projection (Langkah 5) — that requires a separate "freeze projection contract" step (Langkah 4) confirming this review's node/edge/metadata/identity rules as binding, which this document has not yet been asked to do.
- It does not touch Atlas, Graphify, or production in any way.

## 6. Status

`GRAPH_PROJECTION_CONTRACT_FROZEN_LOCAL` (Langkah 4, 2026-08-28) — not committed, not pushed. This document, plus the two adjudication artifacts from Langkah 2 (`ATLAS_MULTI_CASE_PROTOTYPE_KNOWN_GAP_ADJUDICATION.md`, DEC-19, REV-11), remain uncommitted pending user review and a future controlled push.

Next roadmap step per the user's own sequence: **Langkah 5 — build a disposable graph projection**, which is a separate, not-yet-requested, not-yet-authorized step. Freezing this contract makes that future build possible to scope correctly; it does not start it.
