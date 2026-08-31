# G0 — Plan-vs-Repository and Overlap Audit

**Status:** AUDIT ONLY. No modeling, no visualization, no data fill, no test execution, no Atlas change, no `model3b_v2` change, no Hawkes work, no Phase D rerun. Nothing staged, committed, pushed, or deployed by this document or this turn.

**Audited plan, canonical path (verified read-only, single match in repository):**
```text
docs/PLAN_PAINAN_INDRAPURA_GAME_THEORY_HAWKES_COUNTERFACTUAL_LAB.md
```

---

## 1. Corrected Baseline Status

The plan document's own "Baseline teknis aktif" section (its lines 8–28) is carried forward here with one correction: it must not be read as "OP-10 provenance workflow already done."

```text
local HEAD = origin/main = server HEAD = b26478b09f4818b23b0fbb18b0035d17839795d4

OP-10 source specification                     = PUSHED_AND_SERVER_SYNCED
OP-10 source-specification provenance commit   = b26478b09f4818b23b0fbb18b0035d17839795d4
OP-10 registry row                             = NOT YET ADDED
OP-10 assignment application                   = NOT YET APPLIED
Successor specification update                 = NOT YET APPLIED
Successor reconciliation                       = NOT CREATED
OP-10 execution                                = NOT AUTHORIZED
E3                                              = NOT AUTHORIZED
E4                                              = NOT AUTHORIZED
Executed tests                                 = 0
```

**Correct formulation:** OP-10 SOURCE-SPECIFICATION PROVENANCE COMPLETE; REGISTRY ASSIGNMENT AND SUCCESSOR-SPEC APPLICATION STILL PENDING.

This new Painan–Indrapura workstream does not depend on, block, or need to wait for OP-10 registry assignment or successor reconciliation — see §3 below for the non-overlap finding. It is recorded here only because the plan document under audit cites the OP-10 baseline as its own precondition.

---

## 2. Plan-vs-Repository Audit

### 2.1 What the plan document assumes

The audited plan (§§5, 11) proposes, as if starting from an empty slate:

- an actor registry (`actor_id, actor_label, actor_type, valid_from, valid_to, faction_id, representation_scope, source_id, confidence`);
- a relation ledger (`relation_id, source_actor, target_actor, relation_type, start_interval, end_interval, contract_clause, source_id, source_position, confidence, colonial_classification_flag`);
- a decision-point ledger;
- a contract-clause ledger;
- a counterfactual scenario registry;
- a "strategic game board" visualization layer;
- entity/relation vocabulary explicitly including `PROTECTION_PROMISE`, `TRADE_ACCESS`, `EXCLUSIVE_TRADE_CLAIM`, `ALLIANCE_SWITCH`, `RIVAL_CLAIM_SUPPORT`, `COLONIAL_CLASSIFICATION`, `REPRESENTATION_CLAIM`, etc.

Nowhere does the plan document reference, cite, or acknowledge any existing repository artifact for Painan 1663 or Indrapura power relations.

### 2.2 What already exists in the repository (found this turn, read-only)

This is the central audit finding. The repository already contains a mature, versioned, partially-frozen workstream covering the same subject matter:

| Existing artifact | Path | Relevance |
|---|---|---|
| Ontology contract, frozen baseline (Draft V2) | `docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` | Defines first-class entities `Actor, Institution, IndividualOfficeHolder, Location, Treaty, HistoricalEvent, ParentEpisode, Claim, PowerRelation, EffectiveControlObservation` |
| Ontology contract, extension draft | `docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_1_DRAFT.md` | Adds `StrategicInteraction` (already `KEEP_RESEARCH_ONLY`), `CommercialRight`, `RightModification`, `CommandObservation`, `OperationParticipation`; carries a frozen §6 "Evidence Contract" |
| Episode dossiers (4, fully populated) | `docs/thesis/pilot_annotation/{BARUS,INDERAPURA,KOTO_TANGAH,PARIAMAN}_EPISODE_DOSSIER_DRAFT.md` | `INDERAPURA_EPISODE_DOSSIER_DRAFT.md` already documents 3 dated Indrapura events (1665/1686/1716) with verbatim source quotations from Vogel and CD4, commitment classification, and interpretive status |
| Painan 1663 relational research artifact (live data) | `data/power_relations/painan_1663_relational_research_artifact.json`, `data/power_relations/migrated_v2_1/painan_1663_relational_research_artifact_v2_1_migrated.json` | Already-coded `actors`, `treaties`, `relations` for exactly the Painan 1663 case the new plan targets |
| Painan 1663 relational prototype (working UI) | `research_prototypes/painan_1663_relational/` (`index.html`, `prototype.js`, `prototype.css`, `README.md`) | An existing, running visualization prototype for the same case |
| Prototype validators | `scripts/research_validators/validate_painan_1663_relational_artifact.py`, `validate_painan_1663_relational_prototype.py` | Existing validation logic for the JSON artifact and prototype |
| Painan 1663 working analysis (game theory, patron-client, causal hypothesis) | `docs/thesis/colab/PAINAN_1663_GAME_THEORY_WORKING.csv`, `PAINAN_1663_PATRON_CLIENT_WORKING.csv`, `PAINAN_1663_POWER_CAUSAL_HYPOTHESIS_MATRIX.csv`, `PAINAN_1663_POWER_THEORY_WORKING.csv`, `PAINAN_TRACTAAT_1663_CAUSAL_HERMENEUTIC_WORKING.csv` | Prior working files already exploring game-theory framing of the same treaty |
| Deep-dive note | `docs/thesis/pilot_annotation/PAINAN_1663_POWER_THEORY_PATRON_CLIENT_DEEP_DIVE.md` | Existing patron-client theoretical framing for Painan |
| Indrapura status correction | `docs/thesis/pilot_annotation/I2_INDRAPURA_STATUS_CORRECTION.md` | Confirms the Indrapura dossier is not a stub and corrects a prior audit's factual error about its non-existence |

**Finding:** the audited plan's `operation_type`-level vocabulary (relation types, actor registry, contract-clause ledger) is not a green-field proposal. It substantially covers the same ground as the already-frozen V2.1 ontology's `Actor`, `Treaty`, `PowerRelation`, `Claim`, and (most directly) `StrategicInteraction` entities, and the same historical case (Painan 1663) already has a coded JSON artifact and a running visualization prototype. Building the new plan's data contracts (§11 of the audited plan) without first reconciling against this existing material would risk creating a second, incompatible representation of the same facts.

This finding is stated as a fact requiring resolution. It does not itself decide how the two workstreams relate — see the separate `G0_CANONICAL_LOCATION_RECOMMENDATION.md`, which records `RELATIONSHIP_TO_EXISTING_ATLAS_ONTOLOGY_REQUIRES_FORMAL_COMPATIBILITY_REVIEW` rather than pre-selecting an outcome.

---

## 3. Non-Overlap Verification Against OP-10 / E3 / E4 / Phase D

Checked this turn (read-only):

```text
model3b_v2/ subject matter        = OD-005 numerical test-obligation reconciliation
                                     for the Model 3B-CD Hawkes-family recovery
                                     tournament infrastructure
Painan–Indrapura plan subject     = West Sumatra historical/strategic-relation
                                     content (treaties, actors, coalitions,
                                     event timing)
File-path overlap                 = 0 (no file under model3b_v2/ references
                                     Painan, Indrapura, Batang Capas, EIC, Vogel,
                                     or Painansch Contract; no file under the new
                                     workstream references OP-01..OP-10, OD-005,
                                     E1..E4, or the OD-005 registry schema)
Entity/schema overlap             = 0 (model3b_v2's registry columns
                                     operation_id/owner_decision/... share no
                                     field names or semantics with the plan's
                                     actor/relation/contract-clause ledgers)
```

**Result: zero subject-matter, file-path, or schema overlap between the two workstreams.**

The only things shared between them are four global epistemic-status flags, which this new workstream inherits **read-only** and must not restate as its own finding or re-adjudicate:

```text
Model 3B-CD V1      = MODEL_VALIDATION_FAILURE
Hawkes family        = NOT_RULED_OUT
Historical inference = NOT_AUTHORIZED
Phase D              = COMPLETED_VALID_NEGATIVE_RESULT / DO NOT RERUN
```

The audited plan's own §9.1 and §14 (Phase G7) already state these correctly and already forbid rerunning Phase D. This audit confirms those statements are consistent with the current `model3b_v2` state as of this turn and adds nothing further.

---

## 4. No-Execution Boundary (restated)

This turn, and everything produced under it, does not:

```text
modify model3b_v2 (registry, schema, successor specifications, or any other file)
continue OP-10 execution, add a registry row, or create the successor reconciliation
modify Atlas application code
run any model or any test
run Hawkes or any event-process fitting
produce any visualization
fill in any historical data
stage, commit, push, or deploy anything
```

## 5. Final Status

```text
MODEL_3B_V2_UNCHANGED = TRUE
ATLAS_UNCHANGED = TRUE
OP-10 STATUS = SOURCE-SPECIFICATION PROVENANCE COMPLETE; REGISTRY ASSIGNMENT AND SUCCESSOR-SPEC APPLICATION STILL PENDING
OVERLAP WITH OP-10/E3/E4/PHASE D = NONE (subject-matter, file-path, schema)
OVERLAP WITH EXISTING ATLAS POWER-RELATIONS WORKSTREAM = SUBSTANTIAL, UNRESOLVED, REQUIRES FORMAL COMPATIBILITY REVIEW (see G0_CANONICAL_LOCATION_RECOMMENDATION.md)
```
