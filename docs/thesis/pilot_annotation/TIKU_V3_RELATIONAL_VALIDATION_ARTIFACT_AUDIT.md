# TIKU V3 RELATIONAL VALIDATION ARTIFACT — AUDIT

> **RESEARCH-ONLY NONPRODUCTION AUDIT.** Documents the construction and validation of the third of four planned ontology validation cases (V3: Tiku 1625-1740), per `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md`. This audit does not modify `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md`, the Painan artifact, the Natal V1 artifact, the Koto Tangah V2 artifact, or any prior research artifact.

## 1. Scope

This turn builds and validates exactly one artifact set: the Tiku 1625-1740 relational validation artifact, its dedicated validator, an ontology stress-test ledger, and this audit. Its purpose is to test whether the frozen V2 Draft can represent Tiku's own 115-year, multi-episode complexity spanning Aceh's early administration, a mid-period secession, a punitive reconciliation, an unresolved killing, and a late local political rivalry — not to adjust the Draft so Tiku fits it. No new historical research was performed, no DataverseNL or GLOBALISE Places discovery was run; all source material is restricted to what Batch I11 already approved. V4 (Sillida), multi-case prototyping, and any commit/push/deploy action are explicitly out of scope for this turn.

## 2. Frozen Ontology Target

The validation target is `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` (unchanged throughout, checksum verified — see section 3), reused without modification alongside `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md`, `CROSS_CASE_POWER_ONTOLOGY_REVIEW.md`, and the three cross-case decision-ledger CSVs. No relation type, annotation type, entity class, or controlled-vocabulary value was added, removed, or redefined anywhere in this turn's work.

## 3. Inputs and Integrity

Baseline SHA-256 checksums were recorded before construction for: `linimasa_events.csv`, the 79-row interpretive ledger, Draft V2, the Painan/Natal/Koto Tangah artifacts and their validators, the cross-case review/validation plan, and the three cross-case decision ledgers. All were re-verified byte-identical after construction (validator check 33/34).

## 4. Source Hierarchy

Per the frozen material, evidentiary tiers vary sharply across the 7 CORE_I11 episodes: 1625 and 1684 are CD-primary VOC trade/treaty records; 1641 is a CD-primary Aceh-court instrument; 1649's full text was never independently re-read (title/date only, `CANNOT_DETERMINE` provenance); 1662 is uniquely strong — a GLOBALISE/Huygens-translated Batavia daghregister entry carrying Soureradja's own first-person self-narration (`source_asymmetry=MIXED`, the richest local voice in this artifact); 1693-95 (the Sas killing) is reported only via a later RGP editorial aside with an explicitly estimated date; 1740 is secondary-academic only (`buku-padang-1718`).

## 5. Actor and Location Separation

`LOCATION_TIKU` is modeled as a single Location entity, kept distinct from every actor. The 1625 relation deliberately targets `ACTOR_VOC` (the party affected), not a fabricated Tiku-actor, since the source names no local actor for that episode — directly testing and passing the research question's own first item ("Tiku sebagai lokasi bukan satu aktor politik").

## 6. Political Offices

`ACTOR_ACEH_COURT` (institution) is kept separate from `ACTOR_PANGLIMA_SOURERADJA` (the office-holder) and from `ACTOR_ACEH_MONOPOLY_OFFICIALS_1625` (unnamed enforcement agents) — three distinct actor records for what a less careful model might collapse into one "Aceh" actor.

## 7. Commodities and Trade

`COMMODITY_PEPPER` and `COMMODITY_SALT` are modeled as Commodity attribute-records per Draft V2 section 1's own classification, each with its own tracking ID, kept distinct from `LOCATION_TIKU` and from any actor claiming a monopoly over them.

## 8. 1625 Pepper Pressure

Represented as `REL_1625_REQUIRES_MONOPOLY` (Aceh's monopoly officials → VOC), `claim_or_effective_control=COMMERCIAL_CONTROL`, no territorial-control inference drawn — directly per the task's own item 1 instruction.

## 9. 1641 Toll Exemption

Represented as `REL_1641_CLAIMS_JURISDICTION` (Aceh court → Tiku location), `claim_or_effective_control=CLAIM` only. No local Tiku official is inferred to administer this claim, and effective local compliance is left `NOT_TESTABLE`. The exemption act itself proved unrepresentable without inventing vocabulary — see section 29 (T-04).

## 10. 1649 Fixed-Price Treaty

Represented as `REL_1649_CLAIMS_COMMODITY_MONOPOLY` (VOC → pepper), `claim_or_effective_control=COMMERCIAL_CONTROL`, explicitly not a sovereignty claim. Subject actor is flagged `researcher_review_required` since the full instrument text was never independently re-read.

## 11. 1662 Soureradja Secession

The artifact's central mandate test. Represented as four relations: `REL_1662_SWITCHES_SOURERADJA` and `REL_1662_REQUESTS_PROTECTION_SOURERADJA` (Soureradja individually) plus `REL_1662_SWITCHES_PONGELOUS` (the 12-village collective, kept as a separate relation record per the no-homogenization discipline). Groenewegen is tagged as broker. `ACTOR_PONGELOUS_12_DESA_TICCO_1662`'s own `mandate_status` field explicitly states the act is collective, the 12 villages are not individually named, and the act is NOT confirmed to bind the whole of Tiku — directly honoring the task's hard rule against upgrading "comparatively strong collective mandate" into "confirmed mandate over Tiku."

## 12. 1684 Coercion and Pro-Aceh Faction

`REL_1684_MILITARY_FORCE` (`MILITARY_PRESENCE`, not durable control) is superseded by `REL_1684_RECONCILES` (`FORMAL_ACCEPTANCE`, `patron_client_classification=PATRON_CLIENT_CONTESTED`). `ACTOR_PRO_ACEH_FACTION_1684` is kept as its own actor, distinct from `ACTOR_TIKU_REGENTS_1684`, per the source's own explicit attribution of the rebellion's trigger to a specific faction rather than the whole community.

## 13. 1693–1695 Sas Episode

Represented ONLY as a standalone observation (`OBS_1693_1695_SAS_KILLING`), with `perpetrator_status=UNIDENTIFIED` and no relation of any kind — forcing a relation, or the forbidden `KILLS` relation type, would fabricate content (a perpetrator, a motive, a political target) the source does not supply. This is the artifact's thinnest-evidenced item, deliberately left thin rather than filled in.

## 14. 1740 Raja Ibrahim–Raja Kinali Conflict

Represented as `REL_1740_CONTESTS_SUCCESSION` (Raja Kinali → Raja Ibrahim), resolved by a named local rival, not by VOC or Aceh — the artifact's clearest test of local political agency "not reducible to Aceh or VOC policy." The illegal salt refining itself is represented separately via `REL_1740_CLAIMS_MONOPOLY_SALT`, with no VOC enforcement/military relation fabricated (only discovery is documented; the killing is attributed to Raja Kinali's men, not VOC).

## 15. Mandate Analysis

Only one bounded, collective mandate is documented in this artifact's frozen scope (1662, Soureradja + 12 pongelous). No other episode documents a claimed representative mandate over Tiku as a whole. This absence is itself a finding: Tiku's own historical record, across 115 years, never produces a single actor whose mandate is shown to bind "all of Tiku."

## 16. Claim versus Effective Control

Seven distinct `claim_or_effective_control` values are used across the timeline (`COMMERCIAL_CONTROL`, `CLAIM`, `MILITARY_PRESENCE`, `FORMAL_ACCEPTANCE`, `UNKNOWN_EFFECTIVE_CONTROL`) — no relation asserts durable effective control across the whole 1625-1740 period.

## 17. Alignment and Absence of Hedging

No `MAINTAINS_PARALLEL_ALIGNMENT_WITH` relation was created. Aceh's administration (1625-1649), Soureradja's 1662 switch to VOC, and the 1683-84 pro-Aceh relapse are represented as sequential, dated relations, per Batch I11's own finding of no concurrent multi-patron evidence.

## 18. Patron-Client Annotation

`patron_client_classification` is `PATRON_CLIENT_NOT_TESTABLE` for most relations and `PATRON_CLIENT_CONTESTED` specifically for the 1684 pardon — matching the task's own expected I11 disposition for both Aceh-Tiku and VOC-Tiku (`NOT_TESTABLE` or `CONTESTED`, never `SUPPORTED`). No patron-client edge exists anywhere.

## 19. Resistance Annotation

`resistance_candidate=PARTIALLY_SUPPORTED` is attached to the two 1662 alignment-switch relations, explicitly disambiguated in notes as resistance-to-Aceh (not resistance-to-VOC, the relation's own object) — surfacing a genuine annotation-model gap (section 29, T-16). Resistance-to-VOC remains `NOT_TESTABLE` throughout; the 1684 pro-Aceh faction is not generalized to a resistance reading; the 1740 illegal salt refining is not read as resistance absent a stated political target.

## 20. Broker Role

Groenewegen (1662) meets the frozen broker-role criteria and is tagged accordingly. Sas is deliberately NOT tagged as a broker in this artifact, since his broker-qualifying actions occurred in a different, out-of-scope episode (the 1693 Nias/Airbangis expedition) — within the Tiku-specific material he appears only as an unresolved killing's victim. This directly tests and confirms that "repeated appearance alone is insufficient."

## 21. Power and Game-Theory Annotation

Economic leverage, coercive power, classificatory power, bargaining, commitment problems, and local factional agency all appear only as free-text `theoretical_annotation`/notes content. No numeric payoff, equilibrium, best-move, winner/loser, or perfect-rationality language appears anywhere (validator checks 31-32).

## 22. Relation Construction

Ten relations were built across 7 dated episodes: `REL_1625_REQUIRES_MONOPOLY`, `REL_1641_CLAIMS_JURISDICTION`, `REL_1649_CLAIMS_COMMODITY_MONOPOLY`, `REL_1662_SWITCHES_SOURERADJA`, `REL_1662_REQUESTS_PROTECTION_SOURERADJA`, `REL_1662_SWITCHES_PONGELOUS`, `REL_1684_MILITARY_FORCE`, `REL_1684_RECONCILES`, `REL_1740_CONTESTS_SUCCESSION`, `REL_1740_CLAIMS_MONOPOLY_SALT`. Relation-type distribution: `SWITCHES_ALIGNMENT_TO` ×2, `CLAIMS_COMMODITY_MONOPOLY` ×2, `REQUIRES_MONOPOLY_FROM` ×1, `CLAIMS_JURISDICTION_OVER` ×1, `REQUESTS_PROTECTION_FROM` ×1, `USES_MILITARY_FORCE_AGAINST` ×1, `RECONCILES_WITH` ×1, `CONTESTS_SUCCESSION_WITH` ×1.

## 23. Relations Considered but Rejected

`GRANTS_TRADE_ACCESS_TO` (not in Draft V2's frozen set — see T-04); `EXERCISES_EFFECTIVE_CONTROL_OVER` (never instantiated — no episode's evidence rises to durable effective control); `APPOINTS_OFFICE_HOLDER` (rejected for Sontan Macona's 1740 installation — the installing party is not identified, so fabricating VOC or any actor as subject was avoided); `RECOGNIZES_OFFICE_HOLDER` (same reason, rejected for Sontan Macona); `NEGOTIATES_WITH` (rejected — the 1641/1649/1684 instruments are unilateral grants or post-conquest pardons, not documented bilateral negotiations); `CONTESTS_RESOURCE_WITH` (considered for the 1740 salt conflict but rejected in favor of the more precise `CONTESTS_SUCCESSION_WITH` for the Ibrahim-Kinali rivalry, with the salt dimension kept as its own separate `CLAIMS_COMMODITY_MONOPOLY` relation).

## 24. Temporal Model

`valid_from`, `valid_to`, `date_precision`, `superseded_by`, `contradicted_by`, and `observed_at` are populated on every relation/observation. No relation spans more than 25 years. The 1625-1641 (16-year), 1649-1662 (13-year), and 1695-1740 (45-year) intervals are left as genuine, undocumented gaps.

## 25. Evidence Contract

Every relation carries its own independently-assessed `provenance_status` and `evidence_strength`, ranging from `CD_PRIMARY`/`HIGH` (1662) down to `secondary_academic`-only/`LOW` (1740) and an explicit `CANNOT_DETERMINE` provenance for 1649 — no homogenization across episodes of differing evidentiary quality.

## 26. Contradiction Handling

The 1684 rebellion (attributed to a specific pro-Aceh faction) is not read as evidence that the whole 1662-forged VOC alignment failed community-wide — the source's own faction/community distinction is preserved rather than resolved into a single verdict either way.

## 27. Validator Results

`scripts/research_validators/validate_tiku_relational_artifact.py`: **35/35 checks PASS**. The Painan, Natal, and Koto Tangah validators were independently re-run and remain 23/23, 28/28, and 34/34 PASS respectively, confirming no cross-contamination.

## 28. Stress-Test Results

`TIKU_V3_ONTOLOGY_STRESS_TEST.csv`: 20 tests — **17 PASS**, **3 FAIL** (T-04, T-12, T-16 — see section 29).

## 29. Ontology Failures

Three genuine failures, none repaired by changing Draft V2:

- **T-04 — RELATION_TYPE_FAILURE**: the 1641 Aceh toll EXEMPTION cannot be represented without either inventing `GRANTS_TRADE_ACCESS_TO` (not in Draft V2's frozen set) or misusing `COLLECTS_TOLL_FROM` to mean its own semantic opposite. Only the underlying jurisdictional claim was represented; the exemption act itself is a disclosed gap.
- **T-12 — ACTOR_IDENTITY_FAILURE**: Draft V2's Identity Rules (section 4) provide no field to explicitly mark that two temporally-separated, surface-similar local collectives (the 1662 pongelous and the 1684 regents/inhabitants) are a researcher judgment call NOT to merge, rather than a settled ontology property. This is the SAME underlying gap as Koto Tangah's T-14, but manifests in the opposite direction: Koto Tangah attempted a continuity bridge and needed to flag its uncertainty; Tiku deliberately built NO bridge and still has no field to record that deliberate non-bridging decision as anything other than free-text notes.
- **T-16 — ANNOTATION_MODEL_FAILURE**: `resistance_candidate` (Draft V2 section 3, KEEP_AS_ANNOTATION) has no structured target-actor field, so the 1662 secession's resistance-to-Aceh (not resistance-to-VOC, the relation's own object) required a disambiguating note rather than a structured value.

## 30. Comparison with Natal and Koto Tangah Failures

| Case | Failure | Category | Underlying gap |
|---|---|---|---|
| Natal V1 | T-06 | (ontology gap, pre-categorization scheme) | No relation type for institutional hesitation/uncertainty about an already-received claim |
| Koto Tangah V2 | T-01 | RELATION_TYPE_FAILURE | No relation type for a bare institutional-presence fact without overclaiming |
| Koto Tangah V2 | T-06 | ENTITY_MODEL_FAILURE | No source-supported fort-vs-territory location split |
| Koto Tangah V2 | T-14 | ACTOR_IDENTITY_FAILURE | No `continuity_status`/`mandate_status` field in Draft V2's Identity Rules |
| Tiku V3 | T-04 | RELATION_TYPE_FAILURE | No relation type for a toll/trade exemption (the inverse of an existing type) |
| Tiku V3 | T-12 | ACTOR_IDENTITY_FAILURE | Same underlying gap as Koto Tangah T-14, recurring in the non-bridging direction |
| Tiku V3 | T-16 | ANNOTATION_MODEL_FAILURE | No target-actor field on the resistance_candidate annotation |

**Cross-case pattern confirmed**: the actor-identity/continuity gap (Koto Tangah T-14 → Tiku T-12) recurs across two independently-constructed cases, strongly suggesting — per this task's own framing — that it is a genuine Draft V2 cross-case shortfall rather than a Koto Tangah-specific anomaly. The RELATION_TYPE_FAILURE pattern also recurs (Koto Tangah T-01, Natal T-06, Tiku T-04) but in three structurally different forms (a bare presence fact, an institutional-state fact, and a semantic-inverse commercial act) — suggesting Draft V2's relation vocabulary is generally under-provisioned for negative/absence-type and institutional-state facts, not simply missing one specific relation type.

## 31. Draft V2 Compatibility Decision

```
TIKU_V3_ONTOLOGY_VALIDATION_PASS_WITH_LIMITATIONS
```

17 of 20 tested ontology components were representable without any vocabulary change, relation-type extension, entity-class addition, or silent schema addition. The 3 failures are genuine, disclosed gaps — two of which now have cross-case corroboration (actor-identity/continuity, relation-type coverage for negative/institutional facts) — recorded as findings for future researcher-gated review, not repaired here. This decision does NOT authorize any Draft V2 modification or production integration.

## 32. Researcher Decisions Required

1. Whether Draft V2 should add an explicit `continuity_status` field (or equivalent) to its Identity Rules, now that both Koto Tangah (T-14) and Tiku (T-12) independently surface the same gap.
2. Whether `COLLECTS_TOLL_FROM` should carry an exemption/collection sub-field, or whether a dedicated relation type is warranted for trade/toll exemptions (T-04, cross-referenced with Natal's own toll-adjacent 1705 finding).
3. Whether `resistance_candidate` should carry an explicit target-actor field (T-16).
4. Whether the 1649 fixed-price treaty's full CD/Daghregister text should be independently re-read in a future batch to resolve its currently-provisional subject actor.
5. Whether the resistance_candidate schema-completeness question (flagged in Natal V1 and Koto Tangah V2) should be resolved once, project-wide.

## 33. Production Isolation

No backend, frontend, API, database, migration, Atlas, Graphify, Docker, or Nginx file was touched this turn. No commit, push, or deploy was performed.

## 34. Final Readiness Decision

```text
NATAL_V1_ONTOLOGY_VALIDATION:        COMPLETE, SERVER-VALIDATED (unchanged this turn)
KOTO_TANGAH_V2_ONTOLOGY_VALIDATION:  COMPLETE, SERVER-VALIDATED (unchanged this turn)
TIKU_V3_ONTOLOGY_VALIDATION:         TIKU_V3_ONTOLOGY_VALIDATION_PASS_WITH_LIMITATIONS
DRAFT_V2:                            FROZEN_AS_TEST_TARGET (unchanged, checksum-verified)
V4 SILLIDA:                          NOT AUTHORIZED
MULTI-CASE PROTOTYPE:                NOT AUTHORIZED
ATLAS PRODUCTION INTEGRATION:        BLOCKED
GRAPHIFY:                            DEFERRED
```

V3 is judged complete for this turn's scope: Draft V2 was tested against Tiku's full 1625-1740 span without modification, producing both confirmations (17 PASS) and genuine, disclosed failures (3 FAIL) — including two failures with direct cross-case corroboration against Koto Tangah V2, strengthening the case that these are Draft V2 shortfalls rather than single-case anomalies. Per the explicit stop condition governing this task: proceeding to V4 (Sillida), building a multi-case prototype, touching Atlas/Graphify/API/database, or staging/committing/pushing any of this turn's outputs are all NOT authorized by this turn and are deferred to separate, future, researcher-gated turns.
