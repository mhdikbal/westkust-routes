# G0 — Canonical Location Recommendation

**Status:** `CANONICAL_LOCATION_STRATEGIC_HISTORY_LAB_APPLIED_IN_WORKING_TREE` (not `CANONICAL_LOCATION_FROZEN`, `COMMITTED`, or `SYNCED` — the recommendation below has been applied as a filesystem relocation in the working tree under a separate, later authorization; this document's own text still does not itself perform or authorize staging, commit, push, or server-sync).

---

## 1. Recommended Directory — Now Applied

```text
docs/thesis/pilot_annotation/painan_indrapura_strategic_history_lab/
```

Rationale: sibling to `model3b_v2/` under `pilot_annotation/`, because that is where the actually-relevant existing material already lives — the four episode dossiers, the Atlas Power Relations ontology drafts, and the Painan 1663 prototype/validator/artifact (see `G0_PLAN_VS_REPOSITORY_AND_OVERLAP_AUDIT.md` §2.2). Placing the new workstream elsewhere (e.g. repository root, `session-docs/`, or a wholly new top-level tree) would separate it from the material it must eventually reconcile against.

This location decision originated as a recommendation only (§2 below). It has since been applied in the working tree as a filesystem relocation with hash preservation, under a separate, later authorization — not as a Git rename, and not staged, committed, or synced. No existing file outside this relocated set was modified or moved.

## 2. Directory Naming — Two Candidates Evaluated

| Candidate | Expansion | Pro | Con |
|---|---|---|---|
| `painan_indrapura_ghl/` | **GHL = Game-Theory / Hawkes / Counterfactual Lab** | Short path segments | Ambiguous on sight; requires a defined-once glossary entry every time it is introduced in a new document (as done here) |
| `painan_indrapura_strategic_history_lab/` | (self-explanatory, no abbreviation) | Matches the audited plan's own §13 working title, "West Sumatra Strategic History Lab"; needs no glossary entry anywhere it is cited | Longer path strings |

**Recommendation:** `painan_indrapura_strategic_history_lab` is the better long-term name — self-explanatory, already matches the plan document's own chosen product name. `painan_indrapura_ghl` (GHL = Game-Theory / Hawkes / Counterfactual Lab, as defined above) was used as the actual working directory for this G0 turn's original output only because it was the label already in use before this recommendation was written. That recommendation has since been accepted and applied: the seven G0 deliverables were relocated, as a filesystem relocation with hash preservation, to `painan_indrapura_strategic_history_lab/` under a separate, later authorization.

## 3. Relationship to the Existing Atlas Power-Relations Ontology

```text
RELATIONSHIP_TO_EXISTING_ATLAS_ONTOLOGY_REQUIRES_FORMAL_COMPATIBILITY_REVIEW
```

Four possible eventual outcomes are recorded below without selecting one:

```text
EXTENSION_OF_EXISTING_ONTOLOGY
ADDITIVE_RESEARCH_LAYER
SEPARATE_ANALYTICAL_WORKSTREAM_WITH_CROSSWALK
INCOMPATIBLE_REQUIRES_ADJUDICATION
```

Selecting among them requires a dedicated compatibility-review phase — comparing the audited plan's §5/§11 entities field-by-field against `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_1_DRAFT.md` and the live `data/power_relations/painan_1663_relational_research_artifact.json` — explicitly out of scope for this G0 turn.

## 4. Confirmation

This document contains no historical data filling, no modeling result, no simulation output, and no implementation. It does not modify or move any existing repository artifact. It is a location and naming recommendation plus an enumerated (not resolved) compatibility-review question.
