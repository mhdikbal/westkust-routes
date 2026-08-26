# ATLAS POWER-RELATION ONTOLOGY — V2.1 CHANGESET DRAFT

> **PROPOSED_ONLY. NOT AUTHORIZED FOR IMPLEMENTATION.** This document is a changeset PROPOSAL, produced by read-only synthesis of the V1–V4 validation cases. It does not edit `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md`, does not create a Draft V2.1 file, and does not authorize any schema, validator, or artifact implementation. Every change below carries `implementation_status=PROPOSED_ONLY` in the accompanying changeset ledger. No change is `APPROVED`.

## 1. Executive Summary

Eight changes are proposed across six change families, addressing all 10 genuine ontology failures found in V1–V4 (one deferred with no concrete proposal yet, one recommending explicit rejection of a schema change). All 8 are additive/optional and preserve full backward compatibility with all 5 existing validated artifacts (Painan, Natal, Koto Tangah, Tiku, Sillida). Two changes are assessed `CROSS_CASE_REQUIRED` (actor identity/non-identity; rights and privileges), five are `STRONGLY_RECOMMENDED` or deferred pending further design, and one is a recommendation to make NO change based on direct cross-case counterevidence.

## 2. Scope and Non-Goals

**In scope**: a proposal for 8 minimal Draft V2.1 changes, their alternatives, their rejected options, their backward-compatibility and migration implications, and their public-display consequences. **Explicitly out of scope**: creating the changes themselves, editing Draft V2, implementing a generalized validator, building a multi-case prototype, or making any Atlas/Graphify/production change. This document is a decision input, not a decision.

## 3. Frozen V2 Baseline

`ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md`, SHA-256 `f43b1f9fcee75e7a7271994905b676616470271f89dd99d62a6758f1c4b3cd37`, unchanged throughout this synthesis. Its 10 KEEP_AS_FIRST_CLASS_ENTITY classes, 14 MVP_CORE_RELATION types, 2 EXTENDED_RESEARCH_RELATION types, 17 KEEP_AS_ANNOTATION types, and 10-value claim/control vocabulary all remain exactly as frozen.

## 4. V1–V4 Validation Results

```text
Painan (reference): 23/23 PASS, 0 genuine failures
V1 Natal:            28/28 PASS, 1 genuine failure
V2 Koto Tangah:       34/34 PASS, 3 genuine failures
V3 Tiku:              35/35 PASS, 3 genuine failures
V4 Sillida:           32/32 PASS, 3 genuine failures
```

## 5. Genuine Failure Inventory

Ten failures, see `POST_V1_V4_ONTOLOGY_FAILURE_INVENTORY.csv` (companion output) for the full authoritative record. Summary: Natal T-06; Koto Tangah T-01/T-06/T-14; Tiku T-04/T-12/T-16; Sillida T-04/T-06/T-10.

## 6. Cross-Case Failure Clusters

Seven clusters (FCL-01 through FCL-07), see `POST_V1_V4_ONTOLOGY_FAILURE_CLUSTERS.csv`. Two meet the strict two-independent-case `CROSS_CASE_REQUIRED` bar (FCL-01 actor identity; FCL-02 rights/privileges). One initially-plausible two-case cluster (FCL-03) is deliberately downgraded to `STRONGLY_RECOMMENDED` on structural-dissimilarity grounds. One single-case cluster (FCL-04) is downgraded to `REQUIRES_MORE_EVIDENCE` on direct cross-case counterevidence (Sillida's own success). Two single-case clusters (FCL-05, FCL-06) are elevated to `STRONGLY_RECOMMENDED` on severity grounds alone, per the plan's own alternate trigger.

## 7. Generalization Decisions

```text
FCL-01 (actor identity/mandate/non-identity):     CROSS_CASE_REQUIRED
FCL-02 (rights/privileges/exemption/release):     CROSS_CASE_REQUIRED
FCL-03 (institutional state/presence):            STRONGLY_RECOMMENDED (downgraded from initial 2-case reading)
FCL-04 (ambiguous spatial feature):               REQUIRES_MORE_EVIDENCE (downgraded on Sillida counterevidence)
FCL-05 (resistance target):                       STRONGLY_RECOMMENDED (severity-elevated from single case)
FCL-06 (command/constrained agency):              STRONGLY_RECOMMENDED (severity-elevated from single, non-independent case)
FCL-07 (dispute settlement/fine):                 STRONGLY_RECOMMENDED (single case, plausible recurrence)
```

## 8. Actor Identity and Mandate

**CH-01/CH-02**: four OPTIONAL fields on the existing Actor entity — `mandate_status`, `mandate_scope`, `identity_continuity_status`, `explicit_non_identity_with`. Formalizes an already-converged 3-artifact informal convention. Deliberately semi-structured (not a closed enum) to avoid overfitting to only 4 cases. Rejected alternatives: a new `ActorContinuityClaim` entity (over-engineered); a closed `mandate_status` enum (overfitting risk); separate predecessor/successor fields (no case currently demonstrates the need — Sillida's own office-succession test passed without them).

## 9. Rights and Commercial Privileges

**CH-03**: the changeset's single most consequential decision. Option A (recommended, minimal): a `right_status` field (`HELD`/`GRANTED`/`EXEMPTED`/`RELINQUISHED`/`RENEWED`) on existing toll/monopoly relation types. Option B (larger): a full `CommercialRight`/`CommercialPrivilege` object model with its own `GRANTS`/`WAIVES`/`RELEASES`/`REVOKES`/`RENEWS`/`EXEMPTS` action vocabulary, per the governing plan's own CF-02 candidate design. Sillida's own T-04 (third-party fine) was tested against this family and explicitly excluded — reclassified to section 14 below, since a punitive arbitration outcome is not the same historical shape as a voluntary rights-release. Rejected: a new relation type per right-action (proliferation).

## 10. Institutional State and Presence

**CH-04**: explicitly DEFERRED. No concrete field or object is proposed. The two supporting failures (Natal's institutional hesitation, Koto Tangah's institutional presence) are related but not the same structural shape, and this changeset declines to force a premature unified design. A future design-exploration turn is recommended before any specific change is proposed here.

## 11. Ambiguous Spatial Features

**CH-05**: NO CHANGE PROPOSED. Sillida V4's own successful 6-location model (using only the existing Location entity and its Port/Fort/Mine subtype attribute) directly counterexamples the need for a new spatial-ambiguity field to solve Koto Tangah's own T-06. A non-ontology source re-check of Vogel's "Refort" usage is recommended instead, entirely outside this changeset's own scope.

## 12. Resistance Target

**CH-06**: one OPTIONAL field, `resistance_target_actor_id`, on the existing `resistance_candidate` annotation — used only when the resistance target differs from the relation's own object. Deliberately narrower than the plan's own broader candidate field list (`resistance_target_institution_ids`, `resistance_scope`), since no case yet demonstrates a need beyond a single target-actor reference.

## 13. Command and Constrained Agency

**CH-07**: the highest-severity finding in this changeset. Four OPTIONAL structured fields (`coercion_status`, `ability_to_refuse`, `political_intent`, `voice_availability`) added to the EXISTING `EffectiveControlObservation` entity — deliberately NOT a new relation type, to foreclose any future risk of a directed relation being read as implying consent or voluntary alliance. `political_intent` is deliberately left as free text, never a closed enum, so the model can never force a premature loyalty/resistance classification the sources do not support. Requires a mandatory, safety-critical validator addition (section 19) ensuring the constrained-agency actor can never simultaneously appear as subject/object of any relation.

## 14. Dispute Settlement

**CH-08**: a new `DisputeSettlement` research-only entity class (fields: `disputing_actor_ids`, `mediating_actor_ids`, `paying_actor_ids`, `receiving_actor_ids`, `resource_or_object`, `amount_or_share_as_written`, `settlement_date`, `source_document_ids`), for third-party arbitration/fine outcomes (Sillida's own 1679 Bayang-Sillida fine, where a dyadic relation model cannot cleanly represent 3+ distinct party roles). This is the largest schema-to-evidence ratio (a full entity class from a single case) in the changeset — flagged for possible deferral pending a second confirming case.

## 15. Changes Proposed

CH-01 through CH-08, all `PROPOSED_ONLY`, all additive, all documented with alternatives and rejections in `ATLAS_POWER_RELATION_ONTOLOGY_V2_1_CHANGESET_LEDGER.csv`.

## 16. Changes Rejected

A new relation type per right-action; a closed `mandate_status` enum; predecessor/successor actor-id fields (deferred, not currently evidenced); new `DIRECTS_OPERATION_BY`/`DEPLOYS_GROUP_IN`/`COMMANDS_UNIT` relation types (consent-implication risk — the single most consequential rejection in this changeset); forcing the 1679 fine into `COLLECTS_TOLL_FROM`; a spatial-ambiguity schema change (rejected on Sillida's own counterevidence); a closed `political_intent` enum.

## 17. Backward Compatibility

All 8 changes are additive/optional. All 5 existing artifacts remain valid without modification under every proposed change. No existing entity, relation type, or annotation is renamed, removed, or redefined.

## 18. Migration Impact

`right_status` (CH-03) and `resistance_target_actor_id` (CH-06) require an actual artifact CONTENT addition (not merely schema recognition) to close their respective failures — this is a genuine, if small, migration for Tiku and Sillida specifically. CH-01/CH-02 require no data change (schema recognition only, since the informal fields already exist under the same names). CH-07 requires restructuring one existing observation (Sillida's `OBS_CONSTRAINED_AGENCY_ARMED_ENSLAVED_COMPANY`) into the new structured fields. CH-08 requires one new object addition (also Sillida).

## 19. Validator Impact

Every change requires a validator update of some kind, documented per-change in the changeset ledger's own `validator_change` column. The single most safety-critical addition: CH-07 requires a NEW check family verifying no relation_type ever references the same actor_id as a constrained-agency observation's own subject — without this check, the change's entire safety rationale (foreclosing consent-implying misuse) is unenforced.

## 20. Public-Display Impact

None. All 8 proposed changes remain Draft V2 section 10 Research-Only fields/objects. No new public-facing category is introduced by this changeset.

## 21. Graphify Impact

None. Graphify readiness requires frozen relation types across ≥4 cases; this changeset proposes, but does not freeze, anything. Graphify remains `DEFERRED`.

## 22. Revalidation Plan

Ten tests defined in `ATLAS_POWER_RELATION_V2_1_REVALIDATION_MATRIX.csv`, mapping to all 10 genuine failures (two as explicit placeholders pending CH-04's own future design; one explicitly not expecting a schema-driven resolution).

## 23. Rollback Strategy

Because every proposed field/object is optional and additive, rollback for any single change is limited to: (a) removing the new optional field/entity from the schema definition, (b) reverting the specific artifact content additions made for that change's own revalidation fixture (documented per-revalidation in the matrix), and (c) reverting the corresponding validator check. No change requires renaming or restructuring any existing, already-validated artifact content, minimizing rollback blast radius.

## 24. Researcher Decisions Required

Eighteen decisions in `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv`, all `PENDING`. Highest priority: DEC-09 (constrained agency, CH-07) and DEC-04 (rights/privileges Option A vs. B, CH-03).

## 25. Final Readiness Decision

```text
POST_V1_V4_ONTOLOGY_SYNTHESIS_READY_FOR_RESEARCHER_DECISION
```

This changeset draft is ready for researcher review. It does not authorize Draft V2.1 creation, implementation, revalidation execution, or any schema change. All 8 changes await explicit `researcher_decision` values in the companion decision ledger before any further action.
