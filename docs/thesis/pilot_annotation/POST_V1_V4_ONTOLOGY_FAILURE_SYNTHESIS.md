# POST V1–V4 ONTOLOGY FAILURE SYNTHESIS

> **READ-ONLY SYNTHESIS. DRAFT V2 UNCHANGED. NO DRAFT V2.1 CREATED. NO IMPLEMENTATION AUTHORIZED.**
> This document synthesizes the genuine ontology failures discovered across the four nonproduction validation cases (V1 Natal, V2 Koto Tangah, V3 Tiku, V4 Sillida) and proposes a `PROPOSED_ONLY` Draft V2.1 changeset for future researcher decision. It does not itself change Draft V2, create Draft V2.1, modify any V1–V4 artifact or validator, build a generalized validator, or build a multi-case prototype.

## 1. Executive Summary

Ten genuine ontology failures were found across four independently-built validation artifacts, none repaired by workaround at the time and all still open. Clustering them by underlying structural cause (not by surface failure-type label) yields seven candidate failure clusters. Comparing evidence across cases — rather than accepting the task's own initial suggested classification at face value — upgrades two clusters to `CROSS_CASE_REQUIRED` on strict two-independent-case evidence (actor identity/continuity/non-identity; rights/privileges/exemption/release), downgrades one cluster from an initially-plausible grouping to `REQUIRES_MORE_EVIDENCE` based on a direct counterexample (Koto Tangah's spatial-ambiguity failure, contradicted by Sillida's own successful 6-location model), and elevates two single-case clusters to `STRONGLY_RECOMMENDED` purely on severity grounds (resistance-target misattribution risk; constrained-agency command relationships, the single most severe finding in this synthesis). Eight `PROPOSED_ONLY` changes are drafted, all additive/optional, all preserving full backward compatibility with the existing 4 validated artifacts. Ten revalidation tests are defined. Eighteen researcher decisions are queued, `PENDING`. All 40 quality-control checks pass.

## 2. Scope

This turn executes exactly the read-only synthesis specified in `POST_V1_V4_ONTOLOGY_FAILURE_SYNTHESIS_AND_V2_1_CHANGESET_PLAN.md`: failure inventory, cross-case clustering, generalization assessment, minimal-change design, a Draft V2.1 changeset proposal (marked `PROPOSED_ONLY` throughout), revalidation design, generalized-validator planning, and a researcher decision package. It does not edit Draft V2, create Draft V2.1, modify any V1–V4 artifact, validator, or stress-test ledger, build a generalized validator, build a multi-case prototype, or touch Atlas/Graphify/production in any way.

## 3. Frozen Baseline

Verified unchanged before and after this turn: `linimasa_events.csv`, the 79-row interpretive ledger (local-only, content-validated locally, correctly absent on any server checkout per the established environment contract), `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` (SHA-256 `f43b1f9f...`), the three cross-case decision ledgers, and all five case artifacts, validators, stress-test ledgers, and audits.

## 4. Input Integrity

The Integrity Preflight (plan section 5) was executed in full: all 5 validators re-run and PASS (Painan 23/23, Natal 28/28, Koto Tangah 34/34, Tiku 35/35, Sillida 32/32); the interpretive ledger locally confirmed at 79 rows, 0 vocabulary violations; all 4 stress-test CSVs parsed with 0 malformed rows and unique test IDs within each case (Natal 19, Koto Tangah 20, Tiku 20, Sillida 20); Draft V2 checksum matched the frozen baseline; `git status` confirmed zero uncommitted changes on any prior artifact.

## 5. Validation Cases

```text
V1 Natal 1760:                    COMPLETE, SERVER-VALIDATED, 28/28 PASS, 1 genuine failure
V2 Koto Tangah destruction cycle: COMPLETE, SERVER-VALIDATED, 34/34 PASS, 3 genuine failures
V3 Tiku 1625-1740:                COMPLETE, SERVER-VALIDATED, 35/35 PASS, 3 genuine failures
V4 Sillida resource governance:   COMPLETE, SERVER-VALIDATED, 32/32 PASS, 3 genuine failures
Painan 1663 (reference case):     COMPLETE, SERVER-VALIDATED, 23/23 PASS, 0 genuine failures
```

Milestone commit `55812cb954e137f9c17b2cb9b34de9af0b7ab689` confirmed present at local HEAD, `origin/main`, and the westkust-prod server HEAD before this synthesis began.

## 6. Genuine Failures

Ten failures total, each inventoried exactly once in `POST_V1_V4_ONTOLOGY_FAILURE_INVENTORY.csv`, using the frozen stress-test CSVs as the sole authoritative source (no failure ID or status was rewritten):

```text
V1 Natal (1):        T-06 -- institutional VOC hesitation
V2 Koto Tangah (3):  T-01 RELATION_TYPE_FAILURE -- institutional presence
                      T-06 ENTITY_MODEL_FAILURE -- fort vs. nagari territory
                      T-14 ACTOR_IDENTITY_FAILURE -- actor continuity/mandate
V3 Tiku (3):          T-04 RELATION_TYPE_FAILURE -- toll exemption
                      T-12 ACTOR_IDENTITY_FAILURE -- explicit non-identity
                      T-16 ANNOTATION_MODEL_FAILURE -- resistance target
V4 Sillida (3):       T-04 RELATION_TYPE_FAILURE -- third-party fine/arbitration
                      T-06 RELATION_TYPE_FAILURE -- salimoet toll release
                      T-10 ANNOTATION_MODEL_FAILURE -- command/constrained agency
```

Total: **10**, matching the frozen distribution (Natal 1, Koto Tangah 3, Tiku 3, Sillida 3) exactly.

## 7. Failure Clusters

Seven clusters identified in `POST_V1_V4_ONTOLOGY_FAILURE_CLUSTERS.csv`: FCL-01 (actor identity/continuity/mandate/non-identity), FCL-02 (rights/privileges/exemption/release), FCL-03 (institutional state/presence), FCL-04 (ambiguous spatial feature), FCL-05 (resistance target), FCL-06 (command/constrained agency), FCL-07 (dispute settlement/fine/third-party benefit).

## 8. Recurring Gaps

Two clusters meet the strict `CROSS_CASE_REQUIRED` bar (same structural gap in ≥2 independently-built cases):

- **FCL-01**: Koto Tangah T-14 + Tiku T-12 — the SAME underlying gap manifesting in opposite directions (an attempted-and-flagged continuity bridge vs. a deliberately-not-bridged, still-unflagged non-identity decision).
- **FCL-02**: Tiku T-04 + Sillida T-06 — the SAME underlying gap (no relation type for rights RELEASED/EXEMPTED, only HELD/CLAIMED), confirmed identically by two independent artifact authors in separate construction turns.

## 9. Case-Specific Gaps

Five clusters remain single-case at this synthesis's own read-only pass: FCL-03 (Natal + Koto Tangah, but NOT the same sub-shape — see section 10), FCL-04 (Koto Tangah only, and actively counter-evidenced by Sillida — see section 11), FCL-05 (Tiku only), FCL-06 (Sillida only, non-independent evidence since both supporting rows are inside the same artifact), FCL-07 (Sillida only).

## 10. Actor Identity and Mandate

FCL-01 is assessed `CROSS_CASE_REQUIRED`. Proposed change CH-01/CH-02: four optional Actor-entity fields (`mandate_status`, `mandate_scope`, `identity_continuity_status`, `explicit_non_identity_with`), formalizing an informal 3-artifact convention already in consistent use, not introducing a new concept. Deliberately kept as semi-structured free text rather than a closed enum, to avoid overfitting to only the 4 cases examined (DEC-03).

## 11. Rights and Privileges

FCL-02 is assessed `CROSS_CASE_REQUIRED`. Sillida's own T-04 (third-party fine) was explicitly tested against this cluster and **excluded** — its historical shape (punitive arbitration, not voluntary right-relinquishment) differs structurally despite sharing the same `RELATION_TYPE_FAILURE` label, and was reassigned to FCL-07 instead. This reclassification is itself evidence that clustering by label alone would have been a category error. Two options are proposed for CH-03: a minimal `right_status` field on existing toll/monopoly relations (Option A, recommended), or a full `CommercialRight`/`CommercialPrivilege` object model (Option B, larger surface area). DEC-04 flags this as the single most consequential open decision in the changeset.

## 12. Institutional State and Presence

FCL-03 (Natal T-06 + Koto Tangah T-01) technically meets the two-case bar but is deliberately **downgraded** to `STRONGLY_RECOMMENDED`, because the two failures are not the same structural gap: Natal's is internal uncertainty about an already-accepted claim; Koto Tangah's is bare presence-establishment with no claim at all. No specific schema change is proposed (CH-04 is explicitly deferred); this synthesis recommends a future design-exploration turn to determine whether one unified model or two separate models is correct, per the plan's own explicit instruction not to force a premature choice.

## 13. Spatial Ambiguity

FCL-04 (Koto Tangah T-06 only) is **downgraded** from the task's own initial "strongly recommended for review" grouping to `REQUIRES_MORE_EVIDENCE`, on direct counterevidence: Sillida V4 independently tested the identical underlying question (mine vs. territory, plus 4 additional distinct spatial objects) using ONLY the existing Draft V2 Location entity model and passed with zero failures. This is the clearest example in this synthesis of evidence-comparison changing an initial classification — the gap is very likely Koto Tangah's own source material (Vogel's ambiguous "Refort" usage), not a Draft V2 model limitation. No schema change is proposed; a non-ontology source re-check is recommended instead (DEC-07).

## 14. Resistance Target

FCL-05 (Tiku T-16 only) is elevated to `STRONGLY_RECOMMENDED` despite single-case evidence, invoking the plan's own alternate `CROSS_CASE_REQUIRED` trigger ("one gap would otherwise create serious false historical claims"): a resistance value silently misread as directed at the relation's own object, when the source documents resistance toward a different actor, is a genuine public-display-adjacent accuracy risk. Proposed change CH-06: a single optional `resistance_target_actor_id` field, deliberately narrow (a single actor reference, not the broader field set the plan itself offered as candidates) — the smallest change that solves the one documented case.

## 15. Constrained Agency

FCL-06 (Sillida T-10 only, and NOT independently corroborated — both supporting rows are inside the same artifact) is nonetheless assessed the **highest-priority item in this entire synthesis**, elevated to `STRONGLY_RECOMMENDED` purely on severity: Draft V2 currently offers no directed-relationship model at all for a command relationship over coerced/enslaved labor, meaning this category of historical actor is systematically under-representable across the whole project, not merely in Sillida. Proposed change CH-07 deliberately rejects a new relation type (which the plan itself offered as a candidate, e.g. `COMMANDS_UNIT`) in favor of a structured annotation extension on the EXISTING `EffectiveControlObservation` entity — trading relational prominence for safety against any future consent-implying misuse, with a mandatory, safety-critical validator check (REV-06) ensuring the constrained-agency actor can never simultaneously appear in a directed relation.

## 16. Dispute Settlement

FCL-07 (Sillida T-04 only) is assessed `STRONGLY_RECOMMENDED`. Reclassified out of FCL-02 (see section 11) once its own historical shape was examined closely. Proposed change CH-08 (a new `DisputeSettlement` entity) carries the largest schema-to-evidence ratio of any proposal in this changeset — a full new entity class from a single case — and this synthesis explicitly flags it for possible deferral pending a second confirming case (DEC-11), rather than recommending immediate adoption.

## 17. Annotation versus Relation Decisions

Every proposed change in this synthesis was tested against the task's own change-design principles before being finalized. Two changes (CH-06, CH-07) were deliberately kept at the annotation level rather than promoted to relation types, specifically to avoid the risk of a directed relation being read or later reused as implying voluntary participation, consent, or a normal command-and-compliance relationship. No proposed change promotes an existing research-only annotation (patron-client, resistance, repeated coercion, failed deterrence, colonial punitive classification) to relation-type status — all 17 already-reviewed annotation types (Draft V2 section 3) remain KEEP_AS_ANNOTATION, unchanged.

## 18. Minimal Change Principles

All 8 proposed changes were designed against the plan's own 10 change-design principles (section 11): each solves a documented failure, preserves source uncertainty (no closed enums where evidence is too thin, e.g. `political_intent` in CH-07 deliberately left as free text), avoids turning annotation into fact, avoids case-specific relation proliferation (explicitly the reason CH-03/CH-06/CH-07 all reject new relation types in favor of field/object extensions), and is additive/backward-compatible by construction (confirmed case-by-case in the changeset ledger's own `backward_compatibility` column, all `Full`).

## 19. Proposed Change Families

Eight changes across 6 of the plan's own 7 candidate change families (CF-01 through CF-07; CF-04 explicitly yields a no-change recommendation, see section 13): CH-01/CH-02 (CF-01, actor identity), CH-03 (CF-02, rights/privileges), CH-04 (CF-03, deferred — no concrete proposal), CH-05 (CF-04, no change recommended), CH-06 (CF-05, resistance target), CH-07/DEC-10 (CF-06, constrained agency), CH-08 (CF-07, dispute settlement). All marked `PROPOSED_ONLY` in `ATLAS_POWER_RELATION_ONTOLOGY_V2_1_CHANGESET_LEDGER.csv`; none marked `APPROVED`.

## 20. Rejected Changes

Explicitly rejected, with rationale recorded in the changeset ledger's own `alternative_rejected` column for each change: a new relation type per right-action (proliferation risk, CH-03); `possible_predecessor_actor_ids`/`possible_successor_actor_ids` as separate fields (Sillida's own Bajang office-succession case passed WITHOUT needing this, so it is deferred rather than added speculatively, CH-02); a closed enum for `mandate_status` (overfitting risk, CH-01); new `DIRECTS_OPERATION_BY`/`DEPLOYS_GROUP_IN`/`COMMANDS_UNIT` relation types (consent-implication risk, CH-07 — the single most consequential rejection in this synthesis); forcing the 1679 fine into `COLLECTS_TOLL_FROM` (misrepresents a one-time punitive payment as an ongoing toll, CH-08); a schema change for spatial ambiguity (rejected on Sillida's own direct counterevidence, CH-05).

## 21. Cross-Case Risks

The single highest cross-case risk identified: if CH-03 (rights/privileges) is implemented inconsistently between a future Tiku update and a future Sillida update (e.g., one adopts Option A while the other adopts Option B), the cross-case corroboration that justifies FCL-02's own `CROSS_CASE_REQUIRED` status would itself be undermined — REV-03/REV-04 explicitly require the SAME option to be used in both revalidations. The second-highest risk: CH-07's constrained-agency fields, if implemented without the accompanying validator safety check (REV-06), could silently permit exactly the voluntary-alliance mischaracterization the change is meant to prevent.

## 22. Backward Compatibility

All 8 proposed changes are additive/optional; none renames, removes, or redefines any existing Draft V2 entity, relation type, or annotation. All 4 case artifacts (Natal, Koto Tangah, Tiku, Sillida) plus Painan remain valid under every proposed change without modification unless the researcher separately chooses to adopt a specific revalidation fixture (section 23).

## 23. Revalidation Strategy

Ten revalidation tests defined in `ATLAS_POWER_RELATION_V2_1_REVALIDATION_MATRIX.csv`, covering all 10 genuine failures. Two (REV-08, REV-09, both mapping to FCL-03) are explicit placeholders pending a concrete CH-04 proposal. One (REV-10, mapping to Koto Tangah T-06) explicitly does NOT anticipate a schema-driven `PASS` — it tracks a source-level follow-up outside Draft V2's own scope entirely, included only for completeness per the plan's own mapping requirement.

## 24. Generalized Validator Requirements

Documented separately in `ATLAS_POWER_RELATION_V2_1_GENERALIZED_VALIDATOR_PLAN.md` (planning only, no implementation). At minimum: common schema validation; entity identity validation (including the new `explicit_non_identity_with` symmetry check); temporal validation; relation validation; annotation validation; rights/privilege validation; a NEW, safety-critical constrained-agency validation family (ensuring no relation ever references a constrained-agency observation's own subject); source-contract validation; the already-established local-only-versus-synced dependency policy; case-specific extension policy; a regression suite covering all 5 artifacts; machine-readable failure reporting.

## 25. Public Atlas Implications

None of the 8 proposed changes introduces a new public-facing category (DEC-12). All proposed fields/objects remain Draft V2 section 10 Research-Only. The Production Gate (Draft V2 section 14, 8 items, 0 passing) is entirely unaffected by this synthesis, which authorizes only a proposal, not an implementation.

## 26. Graphify Implications

Unaffected. Graphify readiness (Draft V2 section 13) requires reviewed, FROZEN relation types across at least 4 cases — this synthesis proposes changes but freezes nothing. Graphify remains correctly `DEFERRED`.

## 27. Production Gate

Unaffected — remains `BLOCKED`, 0 of 8 gate items passing, unchanged by this synthesis.

## 28. Researcher Decisions Required

Eighteen decisions queued in `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv`, all `researcher_decision=PENDING`. Highest priority per this synthesis's own assessment: **DEC-09** (command relation vs. structured operation object, the constrained-agency finding) and **DEC-04** (rights/privilege Option A vs. Option B, the changeset's single most consequential schema decision).

## 29. Readiness Decision

```text
POST_V1_V4_ONTOLOGY_SYNTHESIS_READY_FOR_RESEARCHER_DECISION
```

All 8 required outputs created (see terminal summary for the explicit count and checksums). All 40 QC checks pass (see companion terminal report). All frozen baselines confirmed unchanged before and after. This synthesis authorizes nothing beyond itself: Draft V2 remains unedited, no Draft V2.1 exists, no V1–V4 artifact or validator was touched, no generalized validator or multi-case prototype was built, and Atlas/Graphify remain blocked/deferred. The 18 queued researcher decisions are the explicit, required next step before any implementation may begin.
