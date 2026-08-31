# WAVE 2 — OD-005 E2 Target, Allocation, and Schema Review

Status: **REVIEW-ONLY**. This document analyzes but does not execute E2. No inventory file has been modified. No test has been executed.

Authoritative baseline: `47525d62404ba0a3b0bf72e4436c98b07a967dbd`. E1: `PUSHED_AND_SERVER_SYNCED`. E2 execution: **NOT AUTHORIZED**. E3/OP-06: **NOT AUTHORIZED**. E4/OP-01: **NOT AUTHORIZED**.

---

## 1. Trigger

A prior E2 execution attempt was correctly stopped (`MODEL_3B_V2_OD_005_E2_SCOPE_VIOLATION`) because `OP-08`, as frozen in `WAVE_2_OD_005_EXACT_AMENDMENT_OPERATIONS.csv`, carries a zero-edit postcondition and explicitly defers actual insertion into the 315-count inventory to "a further, separately authorized turn" — one that was never assigned its own target path, anchor, or schema mapping. This review performs that missing determination, read-only.

## 2. Baseline verification

`local HEAD = origin/main = 47525d62404ba0a3b0bf72e4436c98b07a967dbd` (confirmed). Tracked working tree clean, 0 staged. `MODEL_3B_NUMERICAL_TEST_INVENTORY.csv` = 194 data rows, 10 columns. `MODEL_3B_AMENDMENT_TEST_INVENTORY.csv` = 121 data rows, 7 columns. `194 + 121 = 315`, confirmed. 0 of the 8 proposed `OD005-AMD-*` IDs currently present in either file. No E2 write or leftover audit artifact from the prior failed attempt exists.

## 3. OP-08 frozen contract — re-confirmed

`WAVE_2_OD_005_EXACT_AMENDMENT_OPERATIONS.csv`, `OP-08` row:

- `target_path` = `adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_TEST_IMPACT.csv`
- `postcondition` = file remains byte-identical, 0 edits under this operation
- `test_inventory_effect` = defines the *eligibility condition* for `OD005-AMD-001..008` to later be added to the two 315-count files; 0 rows added by this operation itself

**Classification: `ELIGIBILITY_ONLY_ZERO_EDIT_RECORD`.** OP-08 is not reinterpreted as an insertion operation. Its historical meaning is preserved unchanged; nothing in this review alters `OP-08`'s row, the execution specification, or the operations CSV.

## 4. Test-family classification (summary — full table in `WAVE_2_OD_005_E2_TEST_FAMILY_CLASSIFICATION.csv`)

The 8 proposed tests do not share one provenance-coherent family:

- **`AMENDMENT_CONTRACT_TEST`** (3): `OD005-AMD-001`, `OD005-AMD-002` (ledger-row schema parse, positive/negative), `OD005-AMD-007` (cross-reference integrity of the amendment package's own citations). Purpose is the OD-005 amendment package's internal structural correctness, not a Model-3B numerical decision.
- **`VALIDATOR_IMPLEMENTATION_TEST`** (2): `OD005-AMD-003`, `OD005-AMD-008`. Purpose is `schema_validator.py` source-code behavior — a family with **no existing home in either 315-count file**.
- **`CROSS_FAMILY_TEST`** (3): `OD005-AMD-004/005/006`. Purpose is mathematical-contract invariance (`AC-M2-03`/`R_valid,c`/`FailureRate_c`), substantively resembling the numerical inventory's existing `M2-UNC`-style tests, but triggered and sourced by the OD-005 amendment (`ATX-05`), not a `NUM-DEC` decision directly.

0 `UNRESOLVED` classifications (all 8 tests were assignable to a named family), but 0 of the 8 land cleanly and unambiguously in a single existing 315-count family without cross-reference caveats.

## 5. Candidate allocation evaluation

**Candidate A — all 8 → amendment inventory (129 + 194 = 323).** Rejected. Schema-mapping matrix shows 5 of 10 required fields (`source_requirement`, `test_level`, `input_fixture_future`, `negative_condition`, `execution_stage`) are `NOT_REPRESENTABLE` in the 7-column schema — not a combination problem, an outright absence of any target field. Provenance-incoherent for 6/8 tests (only `OD005-AMD-003/008`'s validator-implementation character loosely echoes this file's candidate-implementation-proposal scope, and even that fit is imperfect since the file tracks *Model-3B-candidate* proposals, not validator-code proposals).

**Candidate B — all 8 → numerical inventory (202 + 121 = 323).** Rejected as primary, though less structurally broken than A. No field is entirely `NOT_REPRESENTABLE`, but 4 of 10 fields (`source_requirement`, `input_fixture_future`, `negative_condition`, `execution_stage`) would collapse into one shared `notes` column, and 2 columns (`source_decision`, `test_family`) would be forced outside their established controlled vocabulary (NUM-DEC identifiers; model-component family names) to hold OP-0x identifiers and check-type labels instead. Provenance-incoherent for 5/8 tests (`001/002/007` are ledger/cross-reference tests, not numerical-decision tests; `003/008` are validator tests with no home here either).

**Candidate C — split allocation.** Rejected as actionable this turn. The arithmetic works (`k_A + k_N = 8`), but the underlying family split (3 amendment-ish, 2 validator-only, 3 math-ish) does not resolve onto just two destinations: the 2 `VALIDATOR_IMPLEMENTATION_TEST` records have no lossless target in *either* existing schema, so a split still leaves a residual, homeless family. Fragmenting one coherent 8-test amendment obligation across 2–3 files would also weaken future validator discoverability and reporting clarity (both explicitly listed evaluation criteria), for no compensating schema benefit.

## 6. Schema review (full matrix in `WAVE_2_OD_005_E2_SCHEMA_MAPPING_MATRIX.csv`)

Numerical inventory: 3 `DIRECT`, 5 `LOSSLESS_COMBINATION`/`CROSS_REFERENCE_REQUIRED` (all collapsing into shared fields or reinterpreting existing enums), 0 `NOT_REPRESENTABLE`, 2 `CROSS_REFERENCE_REQUIRED` on enum-bearing columns. Amendment inventory: 3 `DIRECT`, 5 `NOT_REPRESENTABLE`, 2 `CROSS_REFERENCE_REQUIRED`. Neither target achieves a fully lossless 10/10 field mapping without either silent field loss (amendment) or free-text field collapse plus enum reinterpretation (numerical). Per §8's own gate ("no field is silently discarded," "no free-text combination becomes ambiguous"), **neither existing schema is forced.**

## 7. Insertion anchor review (full table in `WAVE_2_OD_005_E2_INSERTION_ANCHOR_REVIEW.csv`)

Both existing files have an unambiguous **physical** append boundary (`DETERMINISTIC_APPEND_BOUNDARY`) — that part is not the blocker. The blocker is that the schema-mapping precondition for using either anchor is unresolved, so both are classified `AMBIGUOUS` at the authorization level even though the byte-level append point itself is clear. The one column-complete option — the already-existing 10-column `WAVE_2_OD_005_EXACT_TEST_OBLIGATIONS.csv`, which by construction already satisfies the lossless 10-field contract — is not itself a counted inventory file; using it as one requires `NEW_FILE_CREATION_REQUIRED`-class action (a new canonical-inventory designation), which this review does not perform.

## 8. New-operation requirement

`NO_INSERTION_OPERATION_CAN_BE_SPECIFIED_YET`. Which single frozen operation would perform the eventual write depends on which canonical-inventory outcome (§9 of the instructions) is separately authorized next; specifying an operation ID now would itself be a guess. `OP-08` remains unchanged and is not overloaded to also mean insertion.

## 9. Recommendation

**`CREATE_NEW_OD005_AMENDMENT_TEST_INVENTORY`** is the best-supported outcome, not created this turn: neither existing schema provides lossless representation (§6); a new inventory would not duplicate the 315 records; the required schema already exists by construction (`WAVE_2_OD_005_EXACT_TEST_OBLIGATIONS.csv`'s 10 columns); identifier/provenance rules are already explicit (`OD005-AMD-*` namespace, `OP-*`/`ATX-*` cross-references); it would be additive and machine-readable. `EXTEND_EXISTING_SCHEMA_REQUIRES_SEPARATE_ADJUDICATION` (adding the missing 4–5 columns to one existing file) is a viable fallback if a future authorization prefers consolidation over a third family file, but it is not preferred here since it would require modifying the schema of an existing 194- or 121-row file that this review is not authorized to touch.

See `WAVE_2_OD_005_E2_REVIEW_DECISION_DRAFT.md` for the formal decision record.
