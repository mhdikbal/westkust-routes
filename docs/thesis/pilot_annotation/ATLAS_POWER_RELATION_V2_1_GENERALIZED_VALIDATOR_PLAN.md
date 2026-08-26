# ATLAS POWER-RELATION V2.1 GENERALIZED VALIDATOR PLAN

> **PLANNING DOCUMENT ONLY. NO IMPLEMENTATION AUTHORIZED.** This document defines what a future generalized validator (covering Painan, Natal, Koto Tangah, Tiku, Sillida, and any future case under a Draft V2.1) would need to check. It does not implement that validator. The five existing per-case validators (23/23, 28/28, 34/34, 35/35, 32/32) remain unmodified and are the current, authoritative validation mechanism until any future turn separately authorizes generalized-validator implementation.

## 1. Purpose

Each of the five current validators (`validate_painan_1663_relational_artifact.py` through `validate_sillida_relational_artifact.py`) independently re-implements a near-identical set of checks (unique IDs, no orphan endpoints, controlled-vocabulary conformance, dependency policy, production isolation) with case-specific additions layered on top. A future generalized validator would factor out the common core while preserving every case-specific check, reducing duplication and making cross-case consistency (e.g., the CH-03 same-option-across-cases requirement identified in the synthesis) machine-enforceable rather than reliant on manual discipline.

## 2. Common Schema Validation

Applies to every case artifact:

```text
- valid JSON
- schema_version and ontology_contract_version present and match the frozen Draft V2 checksum
- status = RESEARCH_ONLY_NONPRODUCTION
- ONTOLOGY_VALIDATION_CASE_<N> tag present and correctly numbered
- authorization_notice contains all 4 required production-isolation markers
```

## 3. Entity Identity Validation

```text
- unique actor IDs, location IDs, commodity IDs, instrument IDs (where present)
- no orphan relation/observation endpoints
- IF CH-01/CH-02 adopted: explicit_non_identity_with references are symmetric (if A lists B, B's own record should not silently contradict it) and reference valid actor_ids
- IF CH-01 adopted: mandate_status/continuity_status remain free-text-with-guidance, never silently coerced into an enum by validator logic
```

## 4. Temporal Validation

```text
- valid_from <= valid_to where both given
- no single relation spans an implausibly long duration without explicit justification (the per-case validators currently use ad hoc thresholds -- 20 years for Koto Tangah, 25 for Tiku; a generalized validator should make this threshold an explicit, documented parameter, not a hardcoded per-file constant)
- superseded_by / contradicted_by references are valid relation_ids within the same artifact
```

## 5. Relation Validation

```text
- relation_type restricted to the frozen Draft V2 set (MVP_CORE / EXTENDED_RESEARCH / CASE_SPECIFIC / REQUIRES_MORE_EVIDENCE)
- forbidden relation types never present (project-wide accumulated list: PATRON_OF, CLIENT_OF, DESTROYS, REPEATEDLY_COERCES, FAILS_TO_DETER, REBELS_AGAINST, OATH_BREAKER_OF, SUBMITS_TO, SECEDES_FROM, SUBDUES, KILLS, RESISTS, CONTINUES_AS_SAME_ACTOR, ENSLAVES, COMMANDS_SLAVE_COMPANY, ALLY_OF, VOLUNTARILY_SUPPORTS, OWNS_TERRITORY, TRANSFERS_SOVEREIGNTY, GRANTS_TRADE_ACCESS_TO, MAINTAINS_PARALLEL_ALIGNMENT_WITH except where a case meets its double-instantiation evidence bar, IMPOSES_PUNITIVE_CLASSIFICATION_ON)
- claim_or_effective_control restricted to the frozen 10-value vocabulary
```

## 6. Annotation Validation

```text
- evidence_strength, provenance_status, interpretive_status, explicit_or_inferred, commitment_credibility, patron_client_classification all restricted to their frozen controlled vocabularies
- no patron-client or resistance value ever encoded as a relation_type (structural check: no relation_type string contains PATRON, CLIENT, or RESIST)
- IF CH-06 adopted: resistance_target_actor_id, when populated, references a valid actor_id distinct from the relation's own object
```

## 7. Rights/Privilege Validation (pending CH-03 researcher decision)

```text
- IF Option A adopted: right_status restricted to its own frozen vocabulary (HELD/GRANTED/EXEMPTED/RELINQUISHED/RENEWED); a right_status change on a given relation requires an accompanying right_status_effective_date
- IF Option B adopted: new CommercialRight/CommercialPrivilege entity gets the same uniqueness/orphan-reference checks as existing entities (commodities, instruments)
- Cross-case consistency check: if both Tiku and Sillida artifacts are updated under CH-03, both MUST use the same option (A or B) -- a generalized validator is the correct place to enforce this, since per-case validators cannot see across artifacts
```

## 8. Constrained-Agency Validation (pending CH-07 researcher decision)

```text
- SAFETY-CRITICAL: an actor referenced by any observation's coercion_status/ability_to_refuse/voice_availability fields must NEVER also appear as subject_actor_id or object_id of any relation in the same artifact
- coercion_status, ability_to_refuse, voice_availability restricted to their own frozen 3-value vocabularies (or CANNOT_DETERMINE)
- political_intent is never validated against an enum (by design, it remains free text) -- the validator's own role is to confirm the FIELD exists and is populated, not to check its content against a closed vocabulary
```

## 9. Source Contract Validation

```text
- source_passage_locator present on every actor/relation/observation
- event_ids present, list-typed, and (where the project's own EVT- naming convention applies) correctly prefixed
- four-layer text contract preserved (source_statement_summary != historical_reconstruction != theoretical_annotation != public_display_summary, no field auto-derived from another)
```

## 10. Local-Only versus Synced Dependency Policy

```text
- reuse the exact 34A/34B (Koto Tangah) / 30-31 (Tiku, Sillida) split already established: SYNCED_FROZEN_DEPENDENCIES (explicit path list, must exist and checksum-match on every environment) versus the single LOCAL_ONLY_FROZEN_DEPENDENCIES entry (the 79-row interpretive ledger, NOT_APPLICABLE_ON_SERVER when absent, PASS_LOCAL with full content validation when present)
- a generalized validator should absorb this as ONE shared implementation rather than 3 independently-maintained copies (currently duplicated near-verbatim across the Koto Tangah, Tiku, and Sillida validators)
```

## 11. Case-Specific Extension Policy

```text
- a generalized validator must provide an explicit extension point for each case's own additional checks (e.g. Koto Tangah's destruction-year evidence-strength heterogeneity check; Tiku's mandate-boundedness check; Sillida's toll-direction check) -- these are NOT candidates for generalization themselves, since they test case-specific historical claims, not ontology structure
- the plan's own explicit warning against ad hoc ontology expansion applies equally here: a generalized validator's own extension mechanism must not become a backdoor for silently adding new controlled-vocabulary values on a per-case basis
```

## 12. Regression Suite

```text
- MUST run all 5 existing artifacts (Painan, Natal, Koto Tangah, Tiku, Sillida) against both their EXISTING per-case checks and the new common-core checks
- Painan specifically must remain 23/23 -- as the only zero-genuine-failure case, any regression there is the clearest possible signal of a generalization error
- the 10 revalidation tests (ATLAS_POWER_RELATION_V2_1_REVALIDATION_MATRIX.csv) become part of this regression suite once any CH-0x change is actually implemented
```

## 13. Machine-Readable Failure Reporting

```text
- current per-case validators report PASS/FAIL as human-readable text lines
- a generalized validator should additionally emit a structured (e.g. JSON) report keyed by check ID, ontology_component, and case_id, enabling the kind of cross-case failure aggregation this very synthesis had to perform manually by reading 4 separate stress-test CSVs
- this structured report format should itself be designed to feed a FUTURE POST_V-series synthesis automatically, rather than requiring the same manual cross-referencing this turn required
```

## 14. Explicit Non-Implementation

No code for any of the above is written in this turn. This plan exists to inform a future, separately-authorized implementation turn, and to make explicit that a generalized validator is a documented DESIGN GOAL, not a validator that currently exists. All 5 existing per-case validators remain the sole, authoritative validation mechanism until that future turn.
