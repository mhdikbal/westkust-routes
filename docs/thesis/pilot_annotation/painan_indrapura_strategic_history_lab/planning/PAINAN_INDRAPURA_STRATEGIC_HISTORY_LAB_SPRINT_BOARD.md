# Painan–Indrapura Strategic History Lab — Sprint Board

Board date: 2026-08-31
Repository baseline before freeze: `b26478b09f4818b23b0fbb18b0035d17839795d4`
Workstream: `PAINAN_INDRAPURA_STRATEGIC_HISTORY_LAB`
Program status: `ON_TRACK_WITH_GOVERNANCE_GATES`
Implementation status: `NOT STARTED`

This board is a workflow-tracking control artifact only. Percentages and status tokens below measure procedural completion, not historical truth, source adequacy, or model validity.

---

## 1. Workstream Separation

```text
WS-A Model 3B V2 / OD-005 / OP-10        = SEPARATE_ACTIVE_PROVENANCE_WORKFLOW
WS-B Painan-Indrapura Strategic History Lab = G0_LOCAL_FREEZE_IN_PROGRESS
WS-C Existing Atlas Power Relations       = EXISTING_ONTOLOGY_BASELINE_REQUIRES_COMPATIBILITY_REVIEW
WS-D Hawkes / Event-Process Feasibility   = DEFERRED_FEASIBILITY_WORKSTREAM
```

These four workstreams are tracked separately and do not share substantive content, only the global epistemic-boundary flags recorded in §5 below.

---

## 2. S0 Board (Workstream Governance and Location)

```text
S0-01 DONE
S0-02 DONE
S0-03 DONE
S0-04 DONE
S0-05 DONE
S0-06 DONE
S0-07 DONE
S0-08 DONE
S0-09 DONE
S0-10 DONE
S0-11 IN_PROGRESS
S0-12 BLOCKED pending S0-11 local commit review
```

S0-11 evidence_commit = `PENDING_CURRENT_LOCAL_FREEZE_COMMIT`

This token is a planning placeholder only, used because this board is written before the freeze commit exists. It is not amended afterward to become self-referential; the actual commit hash is recorded in the S0-11 terminal report, not in this file.

---

## 3. Future Sprint Summaries

```text
S1 Source Readiness                            = BLOCKED pending G0 freeze and sync
S2 Claim, Actor, and Representation Audit       = NOT AUTHORIZED
S3 Treaty and Contract Decomposition            = NOT AUTHORIZED
S4 Atlas Ontology Compatibility                 = BLOCKED pending G0 freeze and sync
S5 Strategic Game Specification                 = NOT AUTHORIZED
S6 Visual and Counterfactual Protocol           = NOT AUTHORIZED
S7 Hawkes and Event-Process Feasibility         = DEFERRED
S8 Integrated Scenario Laboratory               = NOT AUTHORIZED
```

Brief scope notes:

- **S1** — resolve the source gaps recorded in `G0_SOURCE_GAP_REPORT.md` (Veevers local copy, EIC Fort York material, CD1–CD6 volume index, Indrapura EIC-side coverage, Batangkapas 1662 antecedent).
- **S2** — audit claim, actor, and representation entries once sources are resolved; not authorized before S1.
- **S3** — decompose the Painan treaty's clauses (diplomatic transcription, translation, local/company interpretation split); not authorized before S1–S2.
- **S4** — formally resolve the Atlas ontology compatibility review named in `G0_CANONICAL_LOCATION_RECOMMENDATION.md` §3, selecting one of the four recorded outcomes.
- **S5** — specify the strategic-mechanism/game-theory framework (audited plan §6); not authorized before S3–S4.
- **S6** — specify the visual grammar and counterfactual protocol (audited plan §8, §12); not authorized before S5.
- **S7** — evaluate Hawkes/event-process feasibility against gates H-01–H-08 (audited plan §9.5); deferred, no synthetic recovery without separate authorization; Phase D must not be rerun.
- **S8** — integrated simulation design, only if S1–S7 pass; not authorized.

---

## 4. Critical Path

```text
CURRENT = S0-11 LOCAL FREEZE
NEXT    = S0-12 CONTROLLED PUSH AND SERVER SYNC
THEN    = S1 SOURCE RESOLUTION + S4 ATLAS COMPATIBILITY INVENTORY
LATER   = S5 STRATEGIC GAME SPECIFICATION
LATER   = S6 COUNTERFACTUAL AND VISUALIZATION PROTOCOL
LATER   = S7 HAWKES FEASIBILITY
LAST    = S8 INTEGRATED IMPLEMENTATION
```

---

## 5. Epistemic Boundaries

```text
Model 3B-CD V1 = MODEL_VALIDATION_FAILURE
Hawkes family = NOT_RULED_OUT
Historical inference = NOT_AUTHORIZED
Phase D = COMPLETED_VALID_NEGATIVE_RESULT / DO NOT RERUN
Modeling = NOT STARTED
Counterfactual visualization = NOT IMPLEMENTED
Atlas compatibility outcome selected = 0
```

```text
OP-10 SOURCE-SPECIFICATION PROVENANCE COMPLETE;
REGISTRY ASSIGNMENT AND SUCCESSOR-SPEC APPLICATION STILL PENDING.
```

---

## 6. Progress Metrics (Workflow Only)

```text
S0 before current commit = 10/12 tasks procedurally complete or ready for freeze
G0 substantive deliverables = 7/7 valid
G0 Git visibility = 7/7 visible
G0 local freeze = in progress
Modeling implementation = 0%
Hawkes feasibility review = 0%
Counterfactual visualization implementation = 0%
```

These percentages describe workflow/procedural completion only. They do not measure, imply, or substitute for historical truth, source adequacy, or model validity.

---

## 7. Board Update Contract

Every future board update must record exactly these fields:

```text
board_date
repository_baseline
workstream
sprint_id
task_id
previous_status
new_status
evidence_artifact
commit_hash
blocked_by
next_authorized_action
protected_artifact_change_count
executed_test_count
```

Allowed task statuses:

```text
BACKLOG
READY_TO_START
IN_PROGRESS
BLOCKED
READY_FOR_REVIEW
FROZEN_LOCALLY
PUSHED_AND_SERVER_SYNCED
DEFERRED
NOT_AUTHORIZED
CLOSED_VALID_NEGATIVE_RESULT
```

Future updates must not include historical claims, payoff values, simulation results, or implementation results.
