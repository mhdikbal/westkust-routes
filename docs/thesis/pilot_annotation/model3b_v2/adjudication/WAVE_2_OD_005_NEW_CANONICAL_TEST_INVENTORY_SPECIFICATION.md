# WAVE 2 — OD-005 New Canonical Test Inventory Specification

Status: **SPECIFICATION-ONLY**. This document specifies, but does not create, a new canonical test-obligation inventory. No file at the proposed path exists. No row has been inserted anywhere.

Authoritative baseline: `47525d62404ba0a3b0bf72e4436c98b07a967dbd`. E1: `PUSHED_AND_SERVER_SYNCED`. E2: `NOT APPLIED`. E3/OP-06: `NOT AUTHORIZED`. E4/OP-01: `NOT AUTHORIZED`. Actual inventory creation: **NOT AUTHORIZED**.

---

## 1. Basis

Carried forward from `WAVE_2_OD_005_E2_REVIEW_DECISION_DRAFT.md`: `OP-08 = ELIGIBILITY_ONLY_ZERO_EDIT_RECORD` (unchanged); Candidates A, B, C (all-amendment, all-numerical, split) each `REJECTED`; selected outcome `CREATE_NEW_OD005_AMENDMENT_TEST_INVENTORY`. That outcome is not itself an authorization to create the file — this document is the specification that a future, separate authorization would execute against.

## 2. Proposed canonical path and identity

```text
canonical_path:              docs/thesis/pilot_annotation/model3b_v2/adjudication/MODEL_3B_OD005_AMENDMENT_TEST_INVENTORY.csv
inventory_id:                OD005-TEST-INV-01
inventory_name:              Model 3B V2 OD-005 Amendment Test Inventory
inventory_scope:             The 8 future test obligations arising specifically from the OD-005 / OPT-005-B retirement amendment (OD005-AMD-001..008); no other decision's tests
canonical_path:              (see above)
owner_decision:              OD-005
record_family:               OD005_AMENDMENT
schema_version:              1
status:                      PROPOSED_NOT_CREATED
created_by_future_operation: OP-09 (see §4)
counting_rule:                N_combined = |unique(ID_N ∪ ID_A ∪ ID_OD005)|; this file is counted exactly once, additively, never merged into or replacing T_N or T_A
execution_rule:               registration in this inventory records eligibility for future test authorship/execution only; it does not itself execute or implement any test
```

Path-fitness check: located under `model3b_v2/adjudication/` (Model 3B V2 folder, consistent with sibling adjudication artifacts) — PASS. Does not collide with any existing filename (verified via `ls`, file absent) — PASS. Name states OD-005 scope explicitly (`OD005`) — PASS. Name uses `AMENDMENT_TEST_INVENTORY`, matching the existing `MODEL_3B_AMENDMENT_TEST_INVENTORY.csv` naming pattern without being identical to it or implying replacement — PASS. Nothing in the name or planned content claims tests have run — PASS. Referenceable by a future combined-reconciliation document by exact path — PASS.

## 3. Set contract

```text
|T_N| = 194, |T_A| = 121, T_N ∩ T_A = ∅, |T_315| = 315   (existing, unchanged)
T_OD005 = {OD005-AMD-001, ..., OD005-AMD-008}
T_OD005 ∩ T_N = ∅   (verified: 0 collisions found)
T_OD005 ∩ T_A = ∅   (verified: 0 collisions found)
T_323 = T_N ∪ T_A ∪ T_OD005 (candidate only, valid after future creation + reconciliation)
|T_323| = 194 + 121 + 8 = 323 (candidate cardinality, NOT established)
|T_executed| = 0
```

Current established state: existing obligation count = **315**. Proposed additional obligations = **8**. Post-E2 established count = **NOT YET ESTABLISHED**.

## 4. New operation specification (summary — full record in `WAVE_2_OD_005_NEW_E2_OPERATION_SPECIFICATION.csv`)

A new operation, `OP-09`, is specified (not executed) to eventually perform the file creation. `OP-08` is not modified, not reinterpreted, and is not the predecessor for a semantic reason other than sequencing (it is the eligibility record that this new operation formally succeeds). `OP-09`'s `operation_type = CREATE_CANONICAL_OD005_TEST_INVENTORY`; `execution_status = SPECIFIED_NOT_AUTHORIZED`. `OP-09` is unique against `OP-01`–`OP-08` (verified: existing operation IDs are exactly `OP-01` through `OP-08`, no `OP-09` present).

## 5. Schema (full catalog in `WAVE_2_OD_005_NEW_CANONICAL_TEST_INVENTORY_SCHEMA.csv`)

Exactly the 10 columns of the frozen exact test-obligations contract, same names, same order: `proposed_test_id, source_operation_id, source_requirement, test_level, input_fixture_future, expected_behavior, negative_condition, historical_data_used, status, execution_stage`. Primary key: `proposed_test_id` (`NOT NULL`, `UNIQUE`, `IMMUTABLE`). Foreign/reference keys: `source_operation_id` (resolves to `WAVE_2_OD_005_EXACT_AMENDMENT_OPERATIONS.csv`), `source_requirement` (resolves to the cited `ATX-*`/frozen-document requirement). Controlled enums: `status = PLANNED_ONLY` (8/8), `historical_data_used = NO` (8/8); `test_level` and `execution_stage` reuse only the values already observed in `WAVE_2_OD_005_EXACT_TEST_OBLIGATIONS.csv` — no new enum values introduced.

Because this schema is character-for-character the frozen exact-test-obligations schema, source-to-target mapping for all 10 fields is **DIRECT** for all 8 records — the field-loss and enum-reinterpretation problems found in `WAVE_2_OD_005_E2_SCHEMA_MAPPING_MATRIX.csv` for the two existing (194-row, 121-row) inventories do not recur here, because this inventory's schema was chosen to already match the source exactly rather than being retrofitted.

## 6. Record map (summary — full table in `WAVE_2_OD_005_NEW_CANONICAL_TEST_INVENTORY_RECORD_MAP.csv`)

8/8 records mapped. Family distribution preserved from the E2 review: `AMENDMENT_CONTRACT_TEST = 3` (`OD005-AMD-001`, `002`, `007`), `VALIDATOR_IMPLEMENTATION_TEST = 2` (`OD005-AMD-003`, `008`), `CROSS_FAMILY_TEST = 3` (`OD005-AMD-004`, `005`, `006`), `UNRESOLVED = 0`. `OD005-AMD-003` and `OD005-AMD-008` are recorded with `E3_dependency = YES` — their provenance is the OD-005 amendment contract, but their execution requires the separately-authorized `E3`/`OP-06` validator implementation; registering them here does not authorize or imply that implementation.

## 7. File-creation anchor (deterministic, not executed)

Anchor classification: `NEW_FILE_CREATION_REQUIRED` (the target path does not exist). Deterministic creation rule, for a future authorized turn: directory `docs/thesis/pilot_annotation/model3b_v2/adjudication/` already exists (verified); filename does not currently exist (verified); header written exactly once; 8 data rows written exactly once, in ascending lexical/numeric `OD005-AMD-001`..`008` order; UTF-8 encoding, no BOM (consistent with repository's other CSVs, none of which use a BOM); LF newlines (consistent with sibling CSVs in this repository, confirmed via prior turns' `xxd` inspection); RFC-4180-compliant CSV quoting via a real CSV serializer, not manual string concatenation; content reconstructed verbatim from `WAVE_2_OD_005_EXACT_TEST_OBLIGATIONS.csv` field-for-field, with no paraphrase.

## 8. Provenance and checksum plan (summary — see `WAVE_2_OD_005_NEW_CANONICAL_TEST_INVENTORY_SPEC_AUDIT.md` for the full record)

```text
source_baseline:                 47525d62404ba0a3b0bf72e4436c98b07a967dbd
source_test_obligations_sha256:  66e2c29ac41fcfedce696099579d7757fe0fbbd56539c3e40f43e621f470db06
new_inventory_path:              docs/thesis/pilot_annotation/model3b_v2/adjudication/MODEL_3B_OD005_AMENDMENT_TEST_INVENTORY.csv
new_inventory_sha256_future:     PENDING_AFTER_AUTHORIZED_CREATION
creation_operation_id:           OP-09
creation_commit_future:          PENDING_AFTER_AUTHORIZED_CREATION
record_count:                    8
schema_version:                  1
cross_inventory_collision_count: 0
review_reference:                WAVE_2_OD_005_E2_REVIEW_DECISION_DRAFT.md
```

No hash is computed for a file that does not exist; `new_inventory_sha256_future` is explicitly `PENDING_AFTER_AUTHORIZED_CREATION`, not a guessed or placeholder real value.

## 9. Rollback contract (specified, not exercised)

Applicable only after a future, separately authorized creation: (1) verify the file did not exist at baseline `47525d6`; (2) remove only the newly created canonical inventory; (3) remove only that future turn's creation-audit artifact; (4) verify both paths absent; (5) verify the two existing inventories remain byte-identical to baseline; (6) verify no ledger, validator, E1, or test-execution change; (7) no `git clean` or recursive deletion. Not run this turn — nothing was created.

## 10. Relationship to E3 and E4

`OP-06` remains `E3_IMPLEMENTATION_SPECIFICATION_REQUIRED`, unauthorized. The two `E3`-linked tests (`OD005-AMD-003`, `008`) are recorded in the record map as future obligations only, per §6. `OP-01` remains `NOT AUTHORIZED` (E4). Nothing in this specification changes the open-decision ledger or closes `OD-005`.

## 11. Explicit non-authorization boundary

This specification does not authorize: creating the canonical inventory file; inserting any row into it or into either existing inventory; executing `OP-09`; executing any of the 8 proposed tests or any of the 315 existing tests; changing `OP-08`, the ledger, the validator, or any Python file; claiming `323` as an established count.
