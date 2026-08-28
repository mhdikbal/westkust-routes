# Multi-Case Power-Relation Research Prototype — NONPRODUCTION

**Status: RESEARCH PROTOTYPE. NONPRODUCTION. Not connected to the public Atlas, API, database, or Graphify.**

This is a local, self-contained, read-only research page that renders 5 reviewed Draft V2.1
artifacts, one case at a time via a case switcher:

```
data/power_relations/migrated_v2_1/painan_1663_relational_research_artifact_v2_1_migrated.json
data/power_relations/migrated_v2_1/natal_1760_relational_validation_artifact_v2_1_migrated.json
data/power_relations/migrated_v2_1/koto_tangah_destruction_cycle_relational_validation_artifact_v2_1_migrated.json
data/power_relations/migrated_v2_1/tiku_1625_1740_relational_validation_artifact_v2_1_migrated.json
data/power_relations/migrated_v2_1/sillida_resource_governance_relational_validation_artifact_v2_1_migrated.json
```

It generalizes the single-case `research_prototypes/painan_1663_relational/` prototype across
all 5 now-migrated cases, per `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md` SS5-SS6 (which
specified, without building, what this prototype needed to do). See
`docs/thesis/pilot_annotation/ATLAS_MULTI_CASE_POWER_RELATIONS_PROTOTYPE_AUDIT.md` for the
construction/validation audit.

## Running it locally

The page fetches all 5 artifacts via `fetch()` with relative paths, which most browsers block
under `file://`. Serve it from the repository root with any static file server, for example:

```bash
cd /home/naro/westkust-routes
python3 -m http.server 8899
```

Then open:

```
http://localhost:8899/research_prototypes/multi_case_power_relations/index.html
```

## What it does

- Fetches all 5 `migrated_v2_1` artifacts read-only. Never writes to any of them, never mutates
  a fetched object, never sends data anywhere.
- **Never merges actors or relations across cases.** The case switcher fully replaces the active
  actor/relation set in every view; there is no shared cross-case graph anywhere on this page.
  When the same `actor_id` string recurs across independently-authored case files (e.g.
  `ACTOR_VOC`), the Case Index view reports this as a diagnostic fact, never as an automatic
  merge — consistent with DEC-01's own "no automatic actor merge" safeguard.
- Renders 8 views: Case Index (new), Overview, Actors, Relation Timeline, Relation Network,
  Claim vs Effective Control, V2.1 Additions (new), Public-Copy Preview.
- The V2.1 Additions view lists `CommercialRight`/`RightModification`/`CommandObservation`/
  `OperationParticipation` for the selected case — closed-by-default disclosure drawers, always
  labeled RESEARCH-ONLY, **never rendered as a graph edge** anywhere on this page (Draft V2.1's
  own non-negotiable safety rule for `CommandObservation`, carried through into the UI).
- Uses the same three-level progressive-disclosure pattern as the Painan prototype on every
  relation.
- Never renders a `PATRON_OF`/`CLIENT_OF` edge.
- Handles the one confirmed field-name divergence between cases (Painan's relations use
  `object_actor_id`; the other 4 use `object_id`) through a single `objectIdOf()` helper.
- Natal's and Tiku's own already-disclosed gaps (an ad hoc `VOC_INSTITUTIONAL_HESITATION_
  ANNOTATION` relation_type; two relations using a Commodity id as `object_id`) surface as
  skipped, explicitly-labeled render errors in those cases' own Overview tab — not silently
  dropped, not patched around.

## What it does not do

- No API call, no database query, no Graphify call.
- No import of any `backend/` or `frontend/` module.
- No write to any artifact file or any other file.
- No connection to the production Atlas map, `atlas.js`, or any production template.
- No cross-case actor/relation merge of any kind.

## Validation

```bash
python3 scripts/research_validators/validate_multi_case_power_relations_prototype.py
```

Checks the prototype's static source against a checklist generalizing the Painan prototype's
own 30-item checklist across 5 cases, plus the 2 `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md`
SS5 checks (closed relation-type vocabulary; actor-ID cross-case namespace diagnostic). Performs
no writes and makes no network calls.
