# KOTO TANGAH V2 RELATIONAL VALIDATION ARTIFACT — AUDIT

> **RESEARCH-ONLY NONPRODUCTION AUDIT.** Documents the construction and validation of the second of four planned ontology validation cases (V2: Koto Tangah destruction cycle), per `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md`. This audit does not modify `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md`, the Painan artifact, the Natal V1 artifact, or any prior research artifact.

## 1. Scope

This turn builds and validates exactly one artifact set: the Koto Tangah destruction-cycle relational validation artifact, its dedicated validator, an ontology stress-test ledger, and this audit. Its purpose is to test whether the frozen V2 Draft can represent Koto Tangah's own 95-year, multi-episode complexity (1660-1755) — not to adjust the Draft so Koto Tangah fits it. No new historical research was performed and no DataverseNL or other new-source discovery was run; all source material is restricted to what Batch I10 already approved. V3 (Tiku), multi-case prototyping, and any commit/push/deploy action are explicitly out of scope for this turn.

## 2. Frozen Ontology Target

The validation target is `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` (unchanged throughout, checksum verified before and after — see section 3), reused without modification alongside `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md`, `CROSS_CASE_POWER_ONTOLOGY_REVIEW.md`, and the three cross-case decision-ledger CSVs. No relation type, annotation type, or controlled-vocabulary value was added, removed, or redefined anywhere in this turn's work.

## 3. Inputs and Integrity

Fourteen frozen/protected files were checksummed (SHA-256) before this turn's construction work began and reverified identical afterward via the dedicated validator's own check 34: `linimasa_events.csv` was additionally checksummed as a standalone guard (unused directly by this artifact, but recorded per the task's own checksum-guard list). The Painan artifact, Natal V1 artifact, Draft V2, the 79-row interpretive ledger, the three cross-case decision ledgers, the cross-case review and validation plan, the Painan prototype's three files, and both prior validators (Painan, Natal) all remain byte-identical to their pre-recorded baselines.

## 4. Source Hierarchy

Per the frozen source-asymmetry guard, four evidentiary tiers exist within the CORE_I10 material used here: (1) buku-padang-1718 (Yusri & Deddy Arsya 2024, secondary-academic, citing Kielstra/Radermacher/Valentijn) — the sole or primary source for 1660, 1665, 1670, 1671, 1705, 1712, 1737-38, and 1755; (2) Vogel's Anhang p.715 (c.1690, independent memoir tier) — the SOLE source for 1678 and 1686, and a parallel, non-corroborating source for part of 1682; (3) CD3 traktat CDLXIII p.309 (primary archival) — an independent instrument for the 1682 pardon specifically; (4) GM Deel 10, 1737-1743 (independent, already-verified) — corroborates the 1737-38 troop counts exactly, giving that single year the artifact's strongest evidentiary rating (MULTI_SOURCE_VERIFIED) despite the weakest actor-identity confidence.

## 5. Parent Episode and Child Events

Two already-frozen Phase B parent episodes are reused without modification: `EP-1670-1682-KOTOTANGAH-4XDESTRUCTIONCYCLE` (1670/1678/1682/1686) and `EP-1705-1712-KOTOTANGAH-LOYALTYCONSOLIDATION` (1705/1712). Both are recorded at the artifact's top level (`parent_episodes[]`); no child event's own date, evidence_strength, or perpetrator_status was deleted or averaged into a parent-level value (stress test T-03, PASS).

## 6. Actor Construction

Eight actors were instantiated after testing the full candidate list: `ACTOR_VOC` (Institution), `ACTOR_VAN_LEENE` and `ACTOR_GOUVERNEUR_POUTI` (individually named, 1682 only), `ACTOR_TEN_ENVOYS_COTATENGA_1682` (NamedCollective, bounded and dated, kept separate from the broader collective), `ACTOR_KOTOTANGAH_COASTAL_COLLECTIVE_1660_1755` (NamedCollective research construct bridging unnamed population mentions, `researcher_review_required=true`, `continuity_status` explicitly flagged as unconfirmed), `ACTOR_RAJA_MINANGKABAU` (mediator, modeled as Broker), `ACTOR_PANGLIMA_PADANG_OFFICE` (office reference, not a named individual), and `ACTOR_BERGVOLKEREN_ULAKAN_KOTOTANGAH_1737_1738` (NamedCollective, explicitly never merged with the coastal collective). Candidate actors NOT instantiated: an "unidentified VOC military actor" (the Institution-level `ACTOR_VOC` sufficed for every unnamed-commander year); Sire Narra (out of Koto Tangah's own core scope — the 1676 Sillida-governor accusation is CONTEXT_I10, not CORE, per the existing ledger's own grouping, and is not modeled here). Every actor record carries the 14 required fields (`actor_id, actor_type, source_label, normalized_label, valid_from, valid_to, date_precision, identity_confidence, mandate_status, continuity_status, source_document_ids, source_passage_locator, researcher_review_required, notes`).

## 7. Location and Object Construction

Three entities: `LOCATION_KOTO_TANGAH` (settlement/nagari territory, deliberately NOT split into a separate fort entity — see stress test T-06), `LOCATION_SALT_REFINERY_ULAKAN_KOTOTANGAH` (a distinct object/asset for the 1737-38 destruction), and `LOCATION_PADANG` (context location for Pouti's reported execution site). No place was defaulted into an Actor.

## 8. 1660-1665 Background

Represented as: `OBS_1660_OFFICE_PRESENCE` (an EffectiveControlObservation, `claim_or_effective_control=CLAIM`, no relation forced — see stress test T-01) for the 1660 office opening, and `REL_1665_REQUESTS_PROTECTION` (`REQUESTS_PROTECTION_FROM`, `claim_or_effective_control=TREATY_OBLIGATION`) for the 1665 protection-acceptance renewal following the rejected Acehnese incitement after Groenewegen's death.

## 9. 1670 Destruction

`REL_1670_MILITARY_FORCE` (`USES_MILITARY_FORCE_AGAINST`, VOC → coastal collective, `claim_or_effective_control=MILITARY_PRESENCE`, `evidence_strength=LOW`, `provenance_status=PROVENANCE_AMBIGUOUS`) paired with `OBS_1670_DESTRUCTION`. No durable-control value is attached; the relation is explicitly `superseded_by` the 1671 reconciliation.

## 10. 1671 Mediation and Return

`REL_1671_NEGOTIATES` (`NEGOTIATES_WITH`, broker=`ACTOR_RAJA_MINANGKABAU`) and `REL_1671_RECONCILES` (`RECONCILES_WITH`, `claim_or_effective_control=TREATY_OBLIGATION`, `commitment_credibility=LOW_CREDIBILITY` because the source itself states the alliance "did not last long"). `contradicted_by` on the reconciliation relation points forward to `REL_1678_MILITARY_FORCE`.

## 11. 1678 Destruction

`REL_1678_MILITARY_FORCE` and `OBS_1678_DESTRUCTION`, Vogel-only (`provenance_status="CD_INDEPENDENT ... SOLE source for this year"`, `evidence_strength=LOW`, `interpretive_status=CANNOT_DETERMINE`). Object is `LOCATION_KOTO_TANGAH`, not the coastal-collective actor, since Vogel's sentence names no local actor at all for this year.

## 12. 1682 Destruction and Punishment

Two separate records, deliberately not merged: `REL_1682_RECONCILES_PARDON` / `OBS_1682_DESTRUCTION_PARDON` (the ten envoys' CD3-primary pardon, `evidence_strength=MODERATE`, `claim_or_effective_control=FORMAL_ACCEPTANCE`) and `OBS_1682_POUTI_EXECUTION` (Vogel-only, `evidence_strength=LOW`, `provenance_status` explicitly flags this as UNCONFIRMED to be the same episode as the pardon). This is the artifact's clearest demonstration of collective submission and individual punitive execution as two different modes of control within one nominal episode.

## 13. 1686 Destruction

`REL_1686_MILITARY_FORCE` and `OBS_1686_DESTRUCTION`, structurally identical treatment to 1678 (same sole source, same evidence tier), `superseded_by` pointing forward to `REL_1705_CONTESTS_RESOURCE`/`REL_1705_RECONCILES` 19 years later — the gap is left open, not filled.

## 14. 1705 Renewal

`REL_1705_CONTESTS_RESOURCE` (`CONTESTS_RESOURCE_WITH`, two determinable endpoints: `ACTOR_PANGLIMA_PADANG_OFFICE` and the coastal collective, over harbor-mooring authority — not a generic "unrest" characterization) and `REL_1705_RECONCILES` (the treaty resolving it, `claim_or_effective_control=TREATY_OBLIGATION`).

## 15. 1712 Compliance Observation

`OBS_1712_COMPLIANCE` (`claim_or_effective_control=EFFECTIVE_LOCAL_COMPLIANCE`), a single-dated compliance observation (military assistance against Raja Johan) explicitly NOT treated as proof of continuous control since 1686 or since 1705.

## 16. 1737-1738 Salt Destruction

`REL_1737_MILITARY_FORCE_SALT` (`USES_MILITARY_FORCE_AGAINST`, object=`ACTOR_BERGVOLKEREN_ULAKAN_KOTOTANGAH_1737_1738`, `evidence_strength=MODERATE`, `provenance_status=MULTI_SOURCE_VERIFIED`) and `REL_1737_CLAIMS_MONOPOLY` (`CLAIMS_COMMODITY_MONOPOLY`, object=`LOCATION_SALT_REFINERY_ULAKAN_KOTOTANGAH`). The Bergvolkeren actor is never merged with the coastal 1660-1755 collective, per the source's own explicit distinction.

## 17. 1755 Renewal

`REL_1755_RENEWAL` (`RECONCILES_WITH`, `claim_or_effective_control=TREATY_OBLIGATION`, `evidence_strength=LOW`, `interpretive_status=CANNOT_DETERMINE`), explicitly not asserted as proof of uninterrupted compliance across the 43-year gap since 1712, and flagged as a possible (unconfirmed) duplicate of a wider CD6 west-coast renewal-campaign instrument per the existing Phase B candidate finding.

## 18. Retrospective Vogel Classification

Modeled as its own `DocumentaryReport` entity (`DOCREPORT_VOGEL_ANHANG_P715`), with `report_date` (c.1690) kept distinct from each of the four event dates it describes. Its classification is `VOC_ASSOCIATED_RETROSPECTIVE_CLASSIFICATION`; its `evidence_scope_note` explicitly states it provides unequal evidence for four historical actions and is not treated as neutral proof of repeated collective oath-breaking.

## 19. Claim versus Effective Control

Across the full span, seven distinct `claim_or_effective_control` values are used (`CLAIM, MILITARY_PRESENCE, TREATY_OBLIGATION, FORMAL_ACCEPTANCE, CONTESTED_CONTROL, EFFECTIVE_LOCAL_COMPLIANCE, COMMERCIAL_CONTROL`) — no single relation asserts durable effective control across the whole 1670-1755 period, satisfying the hard rule against the prohibited "VOC EXERCISES EFFECTIVE CONTROL OVER KOTO TANGAH, 1670-1755" relation.

## 20. Repeated Coercion

Kept as free-text mechanism discussion only (reused verbatim from the frozen Batch I10 ledger), never promoted to a relation type or controlled-vocabulary annotation value (validator check 22, PASS).

## 21. Failed Deterrence

Same treatment as Repeated Coercion (validator check 23, PASS) — attached to the 1671 reconciliation's own notes, explaining why the 1670 destruction did not produce a durable settlement.

## 22. Resistance Annotation

No `resistance_candidate` field is populated anywhere in this artifact, consistent with Batch I10's own already-completed finding that no CORE row reaches even PARTIALLY_SUPPORTED for resistance-to-VOC, and consistent with the Natal V1 artifact's own precedent for the same schema-completeness question (deferred, not resolved here).

## 23. Patron-Client Annotation

Every relation's `patron_client_classification` is `PATRON_CLIENT_NOT_TESTABLE`. The relationship exhibits punishment, protection, and repeated alliance renewal — exactly the surface features the task warns must not trigger an automatic patron-client reading — and this artifact does not classify it as patron-client on that basis alone (stress test T-19, PASS).

## 24. Power and Game-Theory Annotation

Repeated game, punishment, deterrence, commitment credibility, temporary accommodation, coercive power, and claim-versus-effective-control all appear only as free-text `theoretical_annotation`/notes content, never as numeric payoff, best-move, winner/loser, equilibrium, or inevitability language (validator checks 27-28, PASS).

## 25. Relation Construction

Twelve relations were built: `REL_1665_REQUESTS_PROTECTION`, `REL_1670_MILITARY_FORCE`, `REL_1671_NEGOTIATES`, `REL_1671_RECONCILES`, `REL_1678_MILITARY_FORCE`, `REL_1682_RECONCILES_PARDON`, `REL_1686_MILITARY_FORCE`, `REL_1705_CONTESTS_RESOURCE`, `REL_1705_RECONCILES`, `REL_1737_MILITARY_FORCE_SALT`, `REL_1737_CLAIMS_MONOPOLY`, `REL_1755_RENEWAL`. Relation-type distribution: `USES_MILITARY_FORCE_AGAINST` ×4, `RECONCILES_WITH` ×4, `REQUESTS_PROTECTION_FROM` ×1, `NEGOTIATES_WITH` ×1, `CONTESTS_RESOURCE_WITH` ×1, `CLAIMS_COMMODITY_MONOPOLY` ×1.

## 26. Relations Considered but Rejected

`EXERCISES_EFFECTIVE_CONTROL_OVER` (rejected throughout, per the hard rule against a durable-control claim); `CONTROLS_FORT` (rejected — no clean fort-vs-territory distinction is source-supported, see stress test T-06); `APPOINTS_OFFICE_HOLDER` (rejected — no VOC appointment act is documented for Koto Tangah in the frozen material); `COLLECTS_TOLL_FROM` (rejected for the 1705 dispute — the source describes jurisdictional authority over moorings, not an explicit toll amount); `RECOGNIZES_OFFICE_HOLDER` (rejected for the Panglima Padang office — the 1705 excerpt describes a contested claim, not a recognition act); `SWITCHES_ALIGNMENT_TO` (considered for 1665 and rejected — alignment was maintained, not switched, when the incitement was rejected); `CONTROLS_PORT` (rejected — no port-specific, as distinct from settlement-specific, control language appears).

## 27. Temporal Model

`valid_from`, `valid_to`, `date_precision`, `superseded_by`, `contradicted_by`, and `observed_at` are populated on every relation. No relation spans more than roughly 20 years (validator check 32). The 1686→1705 (19-year) and 1712→1755 (43-year) intervals are left as genuine gaps — no relation or observation was fabricated to fill either.

## 28. Contradiction Handling

Two contradiction types are preserved side by side, per Draft V2 section 8's own policy: (a) the 1671 reconciliation is `contradicted_by` the 1678 destruction (temporal relapse, not smoothed over); (b) the 1682 CD3 pardon and the 1682 Vogel-reported execution are recorded as parallel, explicitly UNCONFIRMED-to-be-the-same-episode observations, neither chosen as authoritative over the other (stress test T-20, PASS).

## 29. Validator Results

`scripts/research_validators/validate_koto_tangah_relational_artifact.py`: **34/34 checks PASS**. The Painan and Natal V1 validators were independently re-run and remain 23/23 and 28/28 PASS respectively, confirming no cross-contamination.

## 30. Stress-Test Results

`KOTO_TANGAH_V2_ONTOLOGY_STRESS_TEST.csv`: 20 tests — **17 PASS**, **3 FAIL** (T-01, T-06, T-14 — see section 31).

## 31. Ontology Failures

Three genuine failures, each logged under the task's own fixed failure-category list, none repaired by changing Draft V2:

- **T-01 — RELATION_TYPE_FAILURE**: no Draft V2 MVP_CORE relation_type cleanly represents a bare "office established" fact (1660) without overclaiming a formal jurisdictional claim the source does not state. Worked around via an EffectiveControlObservation instead of a relation, disclosed as a partial fit, not a full solution.
- **T-06 — ENTITY_MODEL_FAILURE**: the frozen sources ("Refort Cotatenga" vs. plain "Koto Tangah") do not clearly distinguish a fortified point from the wider nagari territory, so no separate fort entity was created — Draft V2's own Location/Fort subtype attribute could represent this if the sources supported it, but they do not disambiguate enough here.
- **T-14 — ACTOR_IDENTITY_FAILURE**: Draft V2's own Identity Rules (section 4) do not define a `continuity_status` field or a distinct "unverified continuity bridge" actor subtype; this artifact's own `mandate_status`/`continuity_status` fields are a disclosed extension beyond Draft V2's baseline schema, used to carry the coastal collective actor's own unresolved 95-year continuity assumption.

No `NO_FAILURE`-only categories were force-fit; all three failures are reported using only the task's own fixed 9-category list plus `NO_FAILURE`.

## 32. Draft V2 Compatibility Decision

```
KOTO_TANGAH_V2_ONTOLOGY_VALIDATION_PASS_WITH_LIMITATIONS
```

17 of 20 tested ontology components were representable without any vocabulary change, relation-type extension, or silent schema addition. The 3 failures are genuine, disclosed gaps in Draft V2's entity, relation, and identity models specifically — not execution errors — and are recorded as findings for future researcher-gated review, not repaired here. This decision does NOT authorize any Draft V2 modification or production integration.

## 33. Researcher Decisions Required

1. Whether to add a narrower relation_type (or explicit non-relation guidance) for bare institutional-presence facts (T-01).
2. Whether Koto Tangah's own sources warrant a future targeted philological check on Vogel's "Refort" usage before any fort/territory entity split is attempted (T-06).
3. Whether Draft V2 should formally define `continuity_status`/`mandate_status` as standard actor fields, or a distinct actor subtype for continuity-uncertain research constructs (T-14).
4. Whether the resistance_candidate schema-completeness question (flagged identically in Natal V1 and here) should be resolved once, project-wide, rather than per-case.

## 34. Production Isolation

No backend, frontend, API, database, migration, Atlas, Graphify, Docker, or Nginx file was touched this turn. No commit, push, or deploy was performed.

## 35. Final Readiness Decision

```text
NATAL_V1_ONTOLOGY_VALIDATION:        COMPLETE (unchanged this turn)
KOTO_TANGAH_V2_ONTOLOGY_VALIDATION:  KOTO_TANGAH_V2_ONTOLOGY_VALIDATION_PASS_WITH_LIMITATIONS
DATAVERSENL_AUDIT:                   COMPLETE_AND_SERVER_SYNCED (unchanged this turn)
DRAFT_V2:                            FROZEN_AS_TEST_TARGET (unchanged, checksum-verified)
V3 TIKU:                             NOT AUTHORIZED
MULTI-CASE PROTOTYPE:                NOT AUTHORIZED
ATLAS PRODUCTION INTEGRATION:        BLOCKED
GRAPHIFY:                            DEFERRED
```

V2 is judged complete for this turn's scope: Draft V2 was tested against Koto Tangah's full 1660-1755 destruction-and-renewal cycle without modification, producing both confirmations (17 PASS) and genuine, disclosed failures (3 FAIL) — a valid outcome under the task's own explicit framing that failure is a result of testing, not an execution error. Per the explicit stop condition governing this task: proceeding to V3 (Tiku), building a multi-case prototype, touching Atlas/Graphify/API/database, or staging/committing/pushing any of this turn's outputs are all NOT authorized by this turn and are deferred to separate, future, researcher-gated turns.
