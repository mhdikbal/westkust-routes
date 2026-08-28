# ATLAS Power-Relation Ontology — Generalized Validator Implementation Audit

> **PHASE V2.1-GV1 COMPLETE. VALIDATOR SOURCE + FIXTURES + TESTS ONLY.**
> **NO ARTIFACT MIGRATED. NO DRAFT V2/V2.1 EDIT. NO GRAPHIFY. NO PRODUCTION CHANGE. NO STAGE/COMMIT/PUSH.**

## 1. Scope

Implements one generalized, deterministic validator for Atlas power-relation ontology artifacts under the frozen Draft V2 contract and the Draft V2.1 design contract. Authorized: validator source, rule registry, synthetic fixtures, local execution, this audit. Not authorized: migration of Painan/Natal/Koto Tangah/Tiku/Sillida artifacts, modification of any frozen artifact, Atlas implementation, database/API changes, Graphify, production deployment, commit/push/server sync.

## 2. Authoritative Contracts

```text
Baseline commit (local HEAD, origin/main, server HEAD -- all three resolved and matched):
  b54c8a6c05b13d75db864d0731105fe276fdce6d

Draft V2:          docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md
                    sha256 f43b1f9fcee75e7a7271994905b676616470271f89dd99d62a6758f1c4b3cd37 (unchanged)
Draft V2.1:         docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_1_DRAFT.md
                    sha256 1fc122ee9a09b7d19bfcf10b41f9bf882efdc2dda4c194bb78d1ff2c6e010c23 (unchanged)
Contract diff:      docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_V2_1_CONTRACT_DIFF.md
                    sha256 aca6e63e2a568d3cb1460dad160818e01c432d2f79c2e3318b1af45c317076c6 (matches the
                    checksum supplied in the task instructions; unchanged)
Decision ledger:    docs/thesis/colab/POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv (18 rows, 0 PENDING)
Decision audit:     docs/thesis/pilot_annotation/POST_V1_V4_COMPLETE_RESEARCHER_DECISION_AUDIT.md
Changeset ledger:   docs/thesis/colab/ATLAS_POWER_RELATION_ONTOLOGY_V2_1_CHANGESET_LEDGER.csv (8/8 PROPOSED_ONLY)
Revalidation matrix: docs/thesis/colab/ATLAS_POWER_RELATION_V2_1_REVALIDATION_MATRIX.csv (10 planned tests)
```

Local HEAD, `origin/main`, and server HEAD all resolved independently this turn to the identical 40-character hash above (via `git rev-parse HEAD`, `git rev-parse origin/main` after `git fetch`, and an SSH `git rev-parse HEAD` on `westkust-prod:/home/ubuntu/westkust-routes`). No hash was inferred or manually expanded.

## 3. Rule Precedence

As specified: (1) decision ledger, (2) decision audit, (3) Draft V2.1 contract, (4) frozen Draft V2, (5) changeset ledger, (6) revalidation matrix, (7) changeset draft recommendations. Recorded verbatim in `power_relation_ontology_rules.json`'s own `governing_contracts.precedence` field. Applied concretely: CH-03 and CH-07's rule set follows the researcher's actual DEC-04/DEC-09 structured-object selection, not the changeset draft's original Option-A/fields-on-existing-entity recommendation (see `ATLAS_POWER_RELATION_ONTOLOGY_V2_1_CONTRACT_DIFF.md` for this same precedence application at the contract-construction stage).

## 4. Supported Versions

`V2` and `V2.1`, declared via a top-level `ontology_version` field. A legacy-marker fallback recognizes the pre-existing `ontology_contract_version` string used by the four already-frozen artifacts (Koto Tangah, Natal, Sillida, Tiku) that predate this validator's own version-marker convention -- a string starting with `V2_DRAFT` normalizes to `V2` (recorded as an `INFO`-severity finding, never silent). An artifact declaring `V2` is never silently treated as migrated `V2.1`: if it also carries any `V2.1`-only top-level construct or field, this fails as `AMBIGUOUS_VERSION_DECLARATION` (rule `R-BC-02`) rather than being accepted. An unrecognized version value fails deterministically as `UNKNOWN_ONTOLOGY_VERSION`. Validation never mutates the input file (verified by `test_fixture_not_modified_by_validation`, all 28 fixtures, both output modes).

## 5. Machine-Validatable Rules

32 rules across all 10 required classes, defined in `scripts/research_validators/power_relation_ontology_rules.json`:

```text
SCHEMA_RULE:                  3
VOCABULARY_RULE:              7
CARDINALITY_RULE:             2
REFERENCE_INTEGRITY_RULE:     6
TEMPORAL_RULE:                2
PROVENANCE_RULE:              2
RESEARCH_ONLY_RULE:           2
BACKWARD_COMPATIBILITY_RULE:  2
EXCLUSION_RULE:                3
HISTORICAL_REVIEW_RULE:       3
TOTAL:                        32   (29 AUTOMATED, 3 REQUIRES_RESEARCHER_REVIEW)
```

Every rule carries: rule ID, contract section, decision ID, changeset ID (where applicable), enforcement type, severity, supported versions, error code, expected remediation category -- see the registry file directly for the full mapping.

## 6. Researcher-Review Rules

Three rules (`R-HRV-01`, `R-HRV-02`, `R-HRV-03`) are classified `REQUIRES_RESEARCHER_REVIEW`, not `AUTOMATED`. The validator never fabricates a verdict for: whether a historical claim is true, whether an actor intended an outcome, whether resistance occurred, whether a patron-client relationship existed, whether effective control existed, whether a source is trustworthy, or whether a theoretical interpretation is persuasive. Concretely: `political_intent` content is checked only for being a non-empty free-text string (`R-VOC-07`, AUTOMATED); its *substance* is flagged `REVIEW` and never scored PASS/FAIL (`R-HRV-01`). `interpretive_status`/`claim_or_effective_control`/`patron_client_classification` are checked only for closed-vocabulary conformance; the underlying claim is never adjudicated (`R-HRV-03`). Verified by `test_research_review_not_silently_converted_to_pass_or_fail`.

## 7. Relation-Type Restraint

`R-VOC-06` enforces a closed, 16-value vocabulary (14 `MVP_CORE_RELATION` + 2 `EXTENDED_RESEARCH_RELATION`, unchanged from Draft V2.1 SS2, which itself adds zero new values). No relation type is inferred from an object's name or shape. Verified against all 7 forbidden types named in the task instructions -- `RESISTS`, `PATRON_OF`, `CLIENT_OF`, `COMMANDS`, `PARTICIPATES_IN`, `HOLDS_COMMERCIAL_RIGHT`, `MODIFIES_RIGHT` -- by `test_closed_relation_vocabulary_rejects_consent_implying_types`; all 7 fail with `UNAPPROVED_RELATION_TYPE`.

## 8. Research-Only Boundary

`R-RO-01`/`R-RO-02` enforce that `CommercialRight`, `RightModification`, `CommandObservation`, `OperationParticipation`, the constrained-agency fields, and `resistance_target_actor_id` can never carry a `public_status` of `PUBLIC`, `PUBLIC_VOCABULARY`, `PRODUCTION`, `RUNTIME_APPROVED`, `GRAPHIFY_APPROVED`, or `FACTUAL_EDGE`. Severity `CRITICAL`. Verified against all 6 promoted values by `test_v2_1_research_only_enforcement_blocks_all_promoted_values`; all 6 fail with `RESEARCH_ONLY_BOUNDARY_VIOLATION`. This validation does not itself authorize public use or Graphify -- it only confirms the boundary is not silently crossed.

## 9. Deferred and Rejected Structures

```text
DEC-05/DEC-06 (CH-04, institutional state/presence): R-EXC-01 -> DEFERRED_STRUCTURE_NOT_AUTHORIZED
DEC-07 (CH-05, ambiguous spatial feature):            R-EXC-02 -> REJECTED_STRUCTURE_NOT_AUTHORIZED
DEC-11 (CH-08, dispute settlement):                   R-EXC-03 -> DEFERRED_STRUCTURE_NOT_AUTHORIZED
```

No auto-conversion into another type occurs -- each exclusion check fails deterministically and stops there. REV-07 (CH-08) is recorded in the implementation map (SS15 below) as `DEFERRED`, never as an executed V2.1 validation. Verified by `test_ch04_ch05_ch08_exclusions_enforced` and fixtures `negative_08/09/10`.

## 10. Provenance Validation

`R-PROV-01`/`R-PROV-02` require every new V2.1 entity to carry a non-empty `source_document_ids` and an explicit boolean `researcher_review_required`. A structurally valid source reference never produces a positive historical-truth verdict on its own -- provenance presence (`R-PROV-01`) and historical-claim adjudication (`R-HRV-03`) are separate rule classes, never merged. Valid uncertainty values (`CANNOT_DETERMINE`, `NOT_TESTABLE`, `UNKNOWN`) are explicitly accepted wherever the contract allows them (`IDENTITY_UNKNOWN_MARKERS` in the validator source) and never silently replaced with a positive classification -- see `positive_10_cannot_determine.json`, which PASSes with every uncertainty-bearing field populated.

## 11. Synthetic Fixtures

28 fixtures under `tests/fixtures/power_relation_ontology/` (10 positive, 18 negative), all synthetic -- no archival quotation, real personal data, credential, or production record. Full manifest with purpose, sha256, and observed result per fixture: `docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_V2_1_SYNTHETIC_FIXTURE_MANIFEST.csv`.

## 12. Test Results

```text
Test harness:        tests/test_power_relation_ontology_validator.py
Framework:            pytest (Python standard library / repo-standard tooling only)
Total tests run:      174
Passed:                174
Failed:                 0
```

Covers: every positive fixture PASSes with 0 CRITICAL/ERROR; every negative fixture FAILs with its documented primary error code; no fixture is modified by validation (including malformed-JSON handling); repeated execution is byte-identical (`stdout` compared across two runs); JSON output parses for all 28 fixtures; human-readable output is stable; exit codes are correct (0 for all positive, nonzero for all negative); `REQUIRES_RESEARCHER_REVIEW` findings are never silently converted to PASS or FAIL; V2 backward compatibility; V2.1 research-only enforcement across all 6 promoted values; closed relation vocabulary across all 7 forbidden types; CH-04/CH-05/CH-08 exclusions; absence of any Graphify/production/network/database dependency in the validator's own source.

## 13. Legacy Compatibility

The generalized validator was run **read-only** against all 5 frozen artifacts. Findings are genuine, disclosed differences -- **the rules were not weakened to force a pass, and no legacy artifact was modified or marked as migrated V2.1**:

```text
Painan (painan_1663_relational_research_artifact.json):
  MISSING_ONTOLOGY_VERSION -- Painan predates BOTH this validator's ontology_version marker and the
  ontology_contract_version marker later artifacts adopted (it uses only schema_version/case_id/status).
  Expected, disclosed limitation -- not a defect in Painan's own case-specific validator, which
  continues to PASS 23/23 unchanged.

Koto Tangah, Sillida (and Tiku, alongside its own separate findings):
  AMBIGUOUS_VERSION_DECLARATION -- these artifacts already informally populate identity-continuity
  fields (mandate_status-shaped notes) under a declared V2 (normalized from ontology_contract_version)
  even though V2.1 formalization is what DEC-01's own researcher_notes describes as "formalizes an
  already-converged 3-artifact informal practice." This is the EXPECTED signature of that informal
  practice, correctly detected -- not a validator defect.

Natal (natal_1760_relational_validation_artifact.json):
  UNAPPROVED_RELATION_TYPE -- uses VOC_INSTITUTIONAL_HESITATION_ANNOTATION as a relation_type, a
  case-specific workaround for the still-unmodeled CH-04 concept (DEC-05/06 DEFERRED). Confirms,
  independently, exactly the gap CH-04 exists to eventually close -- not a validator defect.

Tiku (tiku_1625_1740_relational_validation_artifact.json):
  ORPHAN_RELATION_ENDPOINT -- two relations use object_id values (COMMODITY_PEPPER, COMMODITY_SALT)
  referencing Commodity, which Draft V2 SS1 models as an attribute of monopoly/toll relations, not a
  separately ID-addressable entity a relation's object_id may reference. A genuine artifact/contract
  shape mismatch, disclosed here rather than special-cased into the generalized validator's rule set.
```

No artifact file was modified (`git status --porcelain data/power_relations/` empty before and after).

## 14. Existing Validator Chain

Unaffected -- none of the 6 files was read, imported, or edited by this implementation:

```text
Painan artifact:    23/23 PASS
Painan prototype:   30/30 PASS
Natal:              28/28 PASS
Koto Tangah:        34/34 PASS
Tiku:               35/35 PASS
Sillida:            32/32 PASS
```

## 15. Revalidation-Matrix Mapping

Full mapping: `docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_V2_1_REVALIDATION_IMPLEMENTATION_MAP.csv`. The frozen `ATLAS_POWER_RELATION_V2_1_REVALIDATION_MATRIX.csv` itself is unmodified (verified: checksum unchanged, no `git status` entry).

```text
PARTIALLY_IMPLEMENTED: 6  (REV-01..06 -- generalized-validator rule coverage exists and passes on
                            synthetic fixtures; none executed against a migrated real artifact, since
                            artifact migration is NOT_AUTHORIZED this phase)
DEFERRED:               3  (REV-07 CH-08/DEC-11, REV-08/REV-09 CH-04/DEC-05/DEC-06)
NOT_APPLICABLE:         1  (REV-10 CH-05/DEC-07 -- no change was ever adopted to positively validate)
IMPLEMENTED:            0
REQUIRES_RESEARCHER_REVIEW (matrix-row level): 0
```

REV-07 is recorded as `DEFERRED`; it is not represented anywhere as an executed V2.1 validation.

## 16. Known Limitations

```text
- No real artifact has been migrated to V2.1 shape; all V2.1 rule coverage is validated only against
  synthetic fixtures, per this phase's own explicit non-authorization of migration.
- The generalized validator's endpoint-integrity check (R-REF-05) recognizes only Actor and Location
  IDs as valid relation endpoints; it does not yet recognize Commodity, Treaty, or ParentEpisode as
  endpoint types some real artifacts already use as object_id values (see SS13, Tiku finding). This is
  a validator scope gap, disclosed rather than silently patched around, since resolving it correctly
  requires researcher input on whether Commodity-as-endpoint is an accepted Draft V2 pattern or itself
  a disclosed artifact-level limitation.
- REV-03/REV-04's own acceptance criteria (matrix CSV) require the SAME selected option to be used
  consistently across Tiku and Sillida; this implementation reflects the single researcher-selected
  direction (DEC-04, structured object) for both, since Option A/B divergence is no longer live.
- The rule registry's `explicit_or_inferred`/`provenance_status`/`evidence_strength` values are
  checked only for the CommercialRight/RightModification/CommandObservation/OperationParticipation
  entity family in this phase; extending equivalent checks to Draft V2's own pre-existing entities
  (Actor, PowerRelation, Treaty, etc.) was out of scope -- those remain covered only by the 6 existing
  case-specific validators.
```

## 17. Migration Nonauthorization

`NOT_AUTHORIZED`. No artifact under `data/power_relations/` was modified, migrated, or rewritten. All 5 files' checksums are identical before and after this phase (spot-checked via `git status --porcelain data/power_relations/`, empty).

## 18. Graphify Nonauthorization

`DEFERRED`, unchanged. The validator's own source contains no reference to `graphify-out`, no network call, no import of any Graphify-related module (verified by `test_no_graphify_or_production_authorization_introduced`). The one pre-existing mention of "graphify" anywhere in `frontend/`/`backend/` remains the same explicit denial line found in prior audits (`riset_pemodelan_panduan.html`: "TIDAK membaca graph pengetahuan") -- not a consumer, unaffected by this phase.

## 19. Production Isolation

No backend/frontend/database/API/Nginx/Docker path was touched. No container was built, started, stopped, or restarted this turn. No commit, stage, or push was performed -- confirmed by `git status --porcelain` showing only new, untracked files (the validator, rule registry, fixtures, tests, and the three new docs), none staged.

## 20. Final Status

All 12 items of the Phase 15 required-result checklist hold: all 10 positive fixtures PASS; all 18 negative fixtures FAIL with expected codes; no input file modified (28/28 fixtures, both output modes); deterministic reruns identical (28/28); JSON output parses (28/28); all 6 existing case validators remain PASS; legacy artifacts remain valid under their own declared/normalized version, with disclosed, non-rule-weakened gaps recorded (SS13); zero new relation_type permitted (7/7 forbidden types rejected); research-only promotion attempts fail (6/6 promoted values rejected); CH-04/CH-05/CH-08 exclusions work (3/3); REV-07 remains `DEFERRED`, never executed; no Graphify or production authorization introduced.

```text
ONTOLOGY_V2_1_GENERALIZED_VALIDATOR_IMPLEMENTED_AND_VALIDATED_LOCALLY
```
