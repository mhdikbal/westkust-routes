# SILLIDA V4 RELATIONAL VALIDATION ARTIFACT — AUDIT

> **RESEARCH-ONLY NONPRODUCTION AUDIT.** Documents the construction and validation of the fourth and final planned ontology validation case (V4: Sillida/Salido resource governance and constrained agency), per `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md`. This audit does not modify `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md`, the Painan, Natal V1, Koto Tangah V2, or Tiku V3 artifacts, or any prior research artifact.

## 1. Scope

This turn builds and validates exactly one artifact set: the Sillida/Salido resource-governance and constrained-agency relational validation artifact, its dedicated validator, an ontology stress-test ledger, and this audit. Its purpose is to test whether the frozen V2 Draft can represent Sillida's own resource-governance complexity — territorial cession by non-native rulers, an absent native voice, a gold-vein boundary war, a deliberately-separated mine lease, a toll relinquishment, and an armed company of enslaved persons deployed under VOC command — not to adjust the Draft so Sillida fits it. This is the LAST of the four planned validation cases; no V5 is authorized. No new historical research was performed, no DataverseNL or GLOBALISE Places discovery was run. Multi-case prototyping, Draft V2 revision, and any commit/push/deploy action are explicitly out of scope for this turn.

## 2. Frozen Ontology Target

The validation target is `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` (unchanged throughout, checksum verified — see section 3), reused without modification alongside `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md`, `CROSS_CASE_POWER_ONTOLOGY_REVIEW.md`, and the three cross-case decision-ledger CSVs. No relation type, annotation type, entity class, or controlled-vocabulary value was added, removed, or redefined anywhere in this turn's work.

## 3. Inputs and Integrity

Baseline SHA-256 checksums were recorded before construction for `linimasa_events.csv`, the 79-row interpretive ledger, Draft V2, the Painan/Natal/Koto Tangah/Tiku artifacts and their validators, the cross-case review/validation plan, and the three cross-case decision ledgers. All were re-verified byte-identical after construction (validator checks 30/31).

## 4. Source Hierarchy

Batch I4 CORE material (rows 43, 44, 56, 64, 65, 87, 99) provides CD-primary and CD-independent instruments spanning 1667-1737; Batch I8 rows 118 and 126 (Vogel 1690) provide the constrained-agency material. Evidentiary tiers vary: rows 43/44 (1667 cession) are mutually-corroborating CD_INDEPENDENT/CD_PARTIAL; rows 64/65 (1681) and 99 (1737) are CD_PRIMARY; row 56 (1679) is CD_PARTIAL; rows 118/126 (1687) are CD_INDEPENDENT (Vogel memoir tier); row 87 (1698) is CD_PRIMARY.

## 5. Actor and Location Separation

Fourteen actors and six locations were instantiated after testing the full candidate list. `LOCATION_SILLIDA` (territory) is kept distinct from `LOCATION_SILLIDA_MINE` (the specific extraction site) — the artifact's central spatial-precision achievement, directly enabling the claim/control test in section 16.

## 6. Political Offices

The three neighboring ceding rulers (Bajang, Indrapura, Trosang) are each their own actor, kept separate from `ACTOR_SILLIDA_REGENTS` (present only in 1679/1698) and from `ACTOR_SULTHAN_SAMPOURNA_PAINAN` (Painan's own self-described legitimate ruler). Bajang's office is tested for succession: `ACTOR_SULTHAN_ACHMET_CHIA_BAJANG` (1667/1681) and `ACTOR_SULTHAN_NIAMOELIA_BAJANG` (1679) are kept as two separate actors holding the same office at different times, with no invented succession chain.

## 7. Commodities and Trade

`COMMODITY_GOLD` is modeled as a single Commodity attribute-record per Draft V2 section 1, kept distinct from `LOCATION_SILLIDA_MINE`, `LOCATION_SOENGAI_KEPAHIAN_GOLD_VEIN`, and every actor claiming or trading it.

## 8. 1625 Pepper Pressure

Not applicable to this case (Tiku-specific; not part of Sillida's own CORE_I4/I8 scope).

## 9. 1641 Toll Exemption

Not applicable to this case (see instead section 12 below for Sillida's own 1698 toll relinquishment, a structurally parallel finding).

## 10. 1649 Fixed-Price Treaty

Not applicable to this case.

## 11. 1662 Soureradja Secession

Not applicable to this case (Tiku-specific).

## 12. 1684 Coercion and Pro-Aceh Faction

Not applicable to this case in that specific form; the structurally analogous episode here is the 1667/1681 territorial cession by non-native rulers (sections 13-14) and the 1678-79 Bayang-Sillida gold-vein war (section 15).

## 13. Sillida and Pulau Cingkuak Surrender (1667/1681)

Represented as `REL_1667_RECOGNIZES_BAJANG`, `REL_1667_RECOGNIZES_INDRAPURA`, `REL_1667_RECOGNIZES_TROSANG` (each `RECOGNIZES_OFFICE_HOLDER`, `claim_or_effective_control=FORMAL_ACCEPTANCE`), reconfirmed 14 years later by three parallel 1681 relations. None of the three ceding rulers is Sillida-native — the source itself never establishes the legal basis for their claimed authority to transfer Sillida's own territory (task item 1, directly answered).

## 14. Absence of Native Sillida Voice

`ACTOR_SILLIDA_REGENTS` is conspicuously absent from both the 1667 cession and its 1681 reconfirmation; it appears only in 1679 (as a fine-recipient) and 1698 (jointly relinquishing the salimoet right). This artifact does not bridge that gap by asserting continuity, nor does it invent a native ruler to fill the 1667/1681 silence (task item 2).

## 15. Bayang-Sillida Gold-Mine War and Boundary (1678-79)

Represented via `REL_1679_CONTESTS_RESOURCE` (Bajang's 1679 ruler ↔ Sillida's regents), object location `LOCATION_SOENGAI_KEPAHIAN_GOLD_VEIN` referenced in notes, `claim_or_effective_control=CONTESTED_CONTROL`. VOC's own "bedrevene rebellie" (committed rebellion) framing is preserved as annotation only (task items 4-5, 13).

## 16. Mine Lease, Sovereignty Claim, and Toll Relinquishment (1698, 1737)

`REL_1737_LEASES_MINE` (`LEASES_RESOURCE_TO`, `COMMERCIAL_CONTROL`) and `REL_1737_CLAIMS_JURISDICTION_MINE` (`CLAIMS_JURISDICTION_OVER`, `CLAIM`) jointly represent VOC's own explicitly-stated deliberate separation of sovereignty from operation (task items 7, 9) — the artifact's cleanest claim-vs-control demonstration across all four validation cases. `REL_1698_COLLECTS_TOLL_SALIMOET` represents the standing salimoet right in the source-supported direction (regents as beneficiary); the relinquishment act itself is a disclosed gap (task item 6, section 29 T-06).

## 17. Sapoelo Boabandaers Capture and Batoe Bannaw Expedition (1687)

`REL_1687_MILITARY_FORCE_SELAS` (`resistance_candidate=PARTIALLY_SUPPORTED`, for Radja doa Selas only) and `REL_1687_MILITARY_FORCE_BATOEBANNAW` (`resistance_candidate=NOT_TESTABLE`) both reuse the frozen ledger's own row-30 values verbatim. `REL_1687_CONTESTS_RESOURCE_TRADEROUTE` represents the underlying Batoe Bannaw/Songy Abou trade-route dispute.

## 18. Mandate Analysis

Only the 1667/1679 pledge to expel Achinders-style explicit collective mandates (as seen in Koto Tangah/Tiku) do not recur here; instead, Sillida's own mandate question is structural and unresolved throughout — no actor in this artifact is ever shown holding a documented, source-confirmed mandate to represent Sillida's own resident population.

## 19. Claim versus Effective Control

Distinct values are used across the timeline: `FORMAL_ACCEPTANCE` (1667/1681 cessions, 1681 Painan self-cession), `CONTESTED_CONTROL` (1679 war), `CLAIM` (1737 sovereignty), `COMMERCIAL_CONTROL` (1737 lease), `MILITARY_PRESENCE` (1687), `TREATY_OBLIGATION` (1698 toll). No relation asserts durable, undifferentiated effective control across the whole span.

## 20. Command Relationship and Constrained Agency

`OBS_CONSTRAINED_AGENCY_ARMED_ENSLAVED_COMPANY` is the artifact's central finding (task items 10-12): the armed enslaved company from the Sillida mine, deployed in both 1687 operations, is represented ONLY as a standalone observation, never as a relation. Its own political intent is `CANNOT_DETERMINE`, strictly separated from Radja doa Selas's own `PARTIALLY_SUPPORTED` resistance value.

## 21. Power and Game-Theory Annotation

Economic leverage, coercive power, classificatory power, and commitment strategy (the deliberate lease-vs-sovereignty separation) appear only as free-text `theoretical_annotation`/notes content. No numeric payoff, equilibrium, best-move, or winner/loser language appears anywhere (validator checks 28-29).

## 22. Relation Construction

Fourteen relations across six relation types: `RECOGNIZES_OFFICE_HOLDER` ×7, `CONTESTS_RESOURCE_WITH` ×2, `LEASES_RESOURCE_TO` ×1, `CLAIMS_JURISDICTION_OVER` ×1, `USES_MILITARY_FORCE_AGAINST` ×2, `COLLECTS_TOLL_FROM` ×1.

## 23. Relations Considered but Rejected

`EXERCISES_EFFECTIVE_CONTROL_OVER` (never instantiated — no episode's evidence rises to durable, territory-wide effective control); `NEGOTIATES_WITH` (rejected for the cessions — these are concluded deeds, not documented bilateral negotiations); `CLAIMS_COMMODITY_MONOPOLY` (considered for the gold trade but rejected in favor of the more precise `LEASES_RESOURCE_TO`/`CLAIMS_JURISDICTION_OVER` pair for the 1737 case, and `CONTESTS_RESOURCE_WITH` for the 1679/1687 disputes); a relation type for third-party fine/arbitration (rejected — not in Draft V2, logged as T-04); a relation type for right relinquishment (rejected — not in Draft V2, logged as T-06); any relation type for the armed enslaved company's command relationship (rejected — none available without forbidden vocabulary, logged as T-10).

## 24. Temporal Model

`valid_from`, `valid_to`, `date_precision`, `superseded_by`, and `observed_at` are populated on every relation/observation. No relation spans the full 1648-1737+ range; large, undocumented gaps (e.g. 1648 to 1667, nearly two decades) are left as genuine gaps.

## 25. Evidence Contract

Every relation carries independently-assessed `provenance_status` and `evidence_strength`, from `CD_PRIMARY`/`HIGH`-adjacent (1737 lease) down to `CD_INDEPENDENT`/`LOW` (1687 Vogel-sourced military actions) — no homogenization.

## 26. Contradiction Handling

No direct source contradiction was found in the frozen CORE_I4/I8 material (unlike Koto Tangah's 1671/1678 relapse or 1682 CD3-vs-Vogel divergence); the closest analog is the tension between the 1667/1681 cessions' own silence on Sillida's native voice and the 1679/1698 rows' documented presence of Sillida's regents — preserved as an open question (section 14), not resolved either way.

## 27. Validator Results

`scripts/research_validators/validate_sillida_relational_artifact.py`: **32/32 checks PASS**. The Painan, Natal, Koto Tangah, and Tiku validators were independently re-run and remain 23/23, 28/28, 34/34, and 35/35 PASS respectively, confirming no cross-contamination.

## 28. Stress-Test Results

`SILLIDA_V4_ONTOLOGY_STRESS_TEST.csv`: 20 tests — **17 PASS**, **3 FAIL** (T-04, T-06, T-10 — see section 29).

## 29. Ontology Failures

Three genuine failures, none repaired by changing Draft V2:

- **T-04 — RELATION_TYPE_FAILURE**: no Draft V2 relation type represents a third-party arbitration outcome (VOC imposing and collecting the largest share of a punitive fine in a dispute it did not originate) distinct from either an ongoing toll or a direct military-force relation.
- **T-06 — RELATION_TYPE_FAILURE**: the 1698 salimoet relinquishment cannot be represented without either inventing a new relation type or reversing `COLLECTS_TOLL_FROM`'s own direction to mean its semantic opposite. This is the SAME underlying gap as Tiku V3's own T-04 (1641 toll exemption), now confirmed a THIRD time in a different commercial-instrument form.
- **T-10 — ANNOTATION_MODEL_FAILURE**: Draft V2 provides no relation type or structured annotation for a command relationship over coerced/enslaved labor that is neither a fabricated new relation type (forbidden) nor a mischaracterization via an existing one (also forbidden). This is the artifact's single most significant finding — constrained agency of this specific, severe kind (chattel-coerced military labor) has no representable directed relationship in Draft V2 at all, only a standalone observation.

## 30. Comparison with Natal, Koto Tangah, and Tiku Failures

| Case | Failure | Category | Underlying gap |
|---|---|---|---|
| Natal V1 | T-06 | (pre-categorization) | No relation type for institutional hesitation about an already-received claim |
| Koto Tangah V2 | T-01 | RELATION_TYPE_FAILURE | No relation type for a bare institutional-presence fact |
| Koto Tangah V2 | T-06 | ENTITY_MODEL_FAILURE | No source-supported fort-vs-territory location split |
| Koto Tangah V2 | T-14 | ACTOR_IDENTITY_FAILURE | No continuity_status field in Draft V2's Identity Rules |
| Tiku V3 | T-04 | RELATION_TYPE_FAILURE | No relation type for a toll/trade EXEMPTION |
| Tiku V3 | T-12 | ACTOR_IDENTITY_FAILURE | Same gap as Koto Tangah T-14, recurring |
| Tiku V3 | T-16 | ANNOTATION_MODEL_FAILURE | No target-actor field on resistance_candidate |
| Sillida V4 | T-04 | RELATION_TYPE_FAILURE | No relation type for third-party fine/arbitration |
| Sillida V4 | T-06 | RELATION_TYPE_FAILURE | No relation type for right RELINQUISHMENT (same gap as Tiku T-04, third confirmation) |
| Sillida V4 | T-10 | ANNOTATION_MODEL_FAILURE | No representable relationship for command-over-coerced-labor |

**Cross-case pattern confirmed across all four cases**: (1) the RELATION_TYPE_FAILURE pattern for negative/inverse commercial acts (exemptions, relinquishments) now has THREE independent confirmations (Tiku T-04, Sillida T-06, and structurally Sillida T-04) — Draft V2's relation vocabulary consistently represents rights HELD or CLAIMED but never rights RELEASED or EXEMPTED; (2) the actor-identity/continuity gap (Koto Tangah T-14, Tiku T-12) does NOT recur in Sillida in the same bridging form, but manifests instead as the mandate-uncertainty finding (section 18) and the office-succession test (section 6) — suggesting the underlying Identity Rules gap is broader than continuity alone; (3) Sillida V4 introduces a genuinely NEW failure category instance (T-10, constrained agency) not seen in any prior case, confirming the task's own expectation that V4 would surface case-specific gaps beyond the recurring ones.

## 31. Draft V2 Compatibility Decision

```
SILLIDA_V4_ONTOLOGY_VALIDATION_PASS_WITH_LIMITATIONS
```

17 of 20 tested ontology components were representable without any vocabulary change, relation-type extension, entity-class addition, or silent schema addition. The 3 failures are genuine, disclosed gaps — one with strong cross-case corroboration (relinquishment/exemption relation types, now 3x confirmed) and one entirely new to this case (constrained-agency command relationships) — recorded as findings for future researcher-gated review, not repaired here. This decision does NOT authorize any Draft V2 modification or production integration.

## 32. Researcher Decisions Required

1. Whether Draft V2 should add a relation type (or a directional sub-field on existing toll/monopoly types) for rights relinquishment/exemption, now that this gap has THREE independent case confirmations (Tiku T-04, Sillida T-04, Sillida T-06).
2. Whether Draft V2 should define a structured command-relationship construct for coerced/constrained-agency labor under military command (T-10) — the single most severe and clearest-cut new gap surfaced across all four cases.
3. Whether the actor-identity/continuity gap (Koto Tangah T-14, Tiku T-12) and the mandate-uncertainty pattern seen here (section 18) should be unified into one Identity Rules revision rather than addressed separately.
4. Whether the resistance_candidate schema-completeness and target-actor questions (flagged in Natal V1, Koto Tangah V2, Tiku V3) should be resolved once, project-wide.

## 33. Production Isolation

No backend, frontend, API, database, migration, Atlas, Graphify, Docker, or Nginx file was touched this turn. No commit, push, or deploy was performed.

## 34. Final Readiness Decision

```text
NATAL_V1_ONTOLOGY_VALIDATION:        COMPLETE, SERVER-VALIDATED (unchanged this turn)
KOTO_TANGAH_V2_ONTOLOGY_VALIDATION:  COMPLETE, SERVER-VALIDATED (unchanged this turn)
TIKU_V3_ONTOLOGY_VALIDATION:         COMPLETE, SERVER-VALIDATED (unchanged this turn)
SILLIDA_V4_ONTOLOGY_VALIDATION:      SILLIDA_V4_ONTOLOGY_VALIDATION_PASS_WITH_LIMITATIONS
DRAFT_V2:                            FROZEN_AS_TEST_TARGET (unchanged, checksum-verified)
ALL FOUR VALIDATION CASES:           COMPLETE
NEXT (future, researcher-gated):     SYNTHESIZE V1-V4 GENUINE FAILURES -> GROUP RECURRING VS CASE-SPECIFIC ->
                                       PREPARE V2.1 CHANGESET -> RESEARCHER DECISION -> CONTROLLED REVISION ->
                                       REVALIDATE ALL FOUR CASES -> GENERALIZED VALIDATOR -> LOCAL MULTI-CASE
                                       PROTOTYPE -> VISUAL REVIEW -> ATLAS/GRAPHIFY EVALUATION
MULTI-CASE PROTOTYPE:                NOT AUTHORIZED
ATLAS PRODUCTION INTEGRATION:        BLOCKED
GRAPHIFY:                            DEFERRED
```

V4 is judged complete for this turn's scope: Draft V2 was tested against Sillida's resource-governance and constrained-agency complexity without modification, producing both confirmations (17 PASS) and genuine, disclosed failures (3 FAIL) — including a third independent confirmation of the relinquishment/exemption relation-type gap and a wholly new, severe finding about constrained-agency command relationships. This completes the four-case validation sequence (V1-V4) as planned. Per the explicit stop condition governing this task: revising Draft V2, building a multi-case prototype, touching Atlas/Graphify, or staging/committing/pushing any of this turn's outputs are all NOT authorized by this turn and are deferred to separate, future, researcher-gated turns — beginning with the cross-V1-V4 failure synthesis named above.
