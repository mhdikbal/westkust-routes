# WAVE 2 — OD-005 E2 Target and Schema Review — Decision Draft

Status: **DRAFT REVIEW DECISION, NOT AN AMENDMENT**. This document records the review's conclusions per instruction §14. It authorizes no execution.

Authoritative baseline: `47525d62404ba0a3b0bf72e4436c98b07a967dbd`.

---

1. **OP-08 classification:** `ELIGIBILITY_ONLY_ZERO_EDIT_RECORD` (confirmed against `WAVE_2_OD_005_EXACT_AMENDMENT_OPERATIONS.csv`; unchanged, not reinterpreted).

2. **Selected canonical-inventory outcome:** `CREATE_NEW_OD005_AMENDMENT_TEST_INVENTORY` (recommended, not created this turn). Fallback if a future turn prefers it instead: `EXTEND_EXISTING_SCHEMA_REQUIRES_SEPARATE_ADJUDICATION` against the numerical inventory (the less-broken of the two existing schemas). `USE_EXISTING_AMENDMENT_INVENTORY` and `USE_EXISTING_NUMERICAL_INVENTORY` (unmodified, single-destination) are rejected per the Candidate A/B analysis. `USE_SPLIT_EXISTING_INVENTORIES` is rejected per the Candidate C analysis. `WITHHOLD_TARGET_DECISION` is not selected because a determinate recommendation was reachable.

3. **Per-test allocation (informational only, not applied):**
   - `OD005-AMD-001`, `OD005-AMD-002`, `OD005-AMD-007` → `AMENDMENT_CONTRACT_TEST` family
   - `OD005-AMD-003`, `OD005-AMD-008` → `VALIDATOR_IMPLEMENTATION_TEST` family (no existing 315-count home)
   - `OD005-AMD-004`, `OD005-AMD-005`, `OD005-AMD-006` → `CROSS_FAMILY_TEST` (mathematical-invariance purpose, OD-005-amendment provenance)
   - Under the recommended outcome, all 8 would reside together in one new, homogeneous canonical inventory rather than being split by family, since no split target exists for the `VALIDATOR_IMPLEMENTATION_TEST` pair in either current file.

4. **Schema-mapping verdict:** neither existing schema achieves a lossless 10/10 field mapping. Numerical inventory: 3 `DIRECT`, 5 `LOSSLESS_COMBINATION`/`CROSS_REFERENCE_REQUIRED` (4 fields forced into a shared `notes` column; 2 columns' controlled vocabulary reinterpreted), 0 `NOT_REPRESENTABLE`. Amendment inventory: 3 `DIRECT`, 2 `CROSS_REFERENCE_REQUIRED`, 5 `NOT_REPRESENTABLE`. Full detail in `WAVE_2_OD_005_E2_SCHEMA_MAPPING_MATRIX.csv`.

5. **Anchor verdict:** both existing files have an unambiguous physical `DETERMINISTIC_APPEND_BOUNDARY`, but both are held `AMBIGUOUS` at the authorization level pending schema resolution. The new-canonical-inventory option requires `NEW_FILE_CREATION_REQUIRED`, not performed here. Full detail in `WAVE_2_OD_005_E2_INSERTION_ANCHOR_REVIEW.csv`.

6. **Need for a new operation:** `NO_INSERTION_OPERATION_CAN_BE_SPECIFIED_YET`. An operation ID cannot be responsibly assigned until the canonical-inventory outcome is authorized; `OP-08` is not overloaded to serve this role.

7. **Exact count consequence:** `315 + 8 = 323` remains a **candidate** cardinality, not an achieved one. It is valid only once a target, allocation, and lossless mapping are authorized and a one-time insertion is actually performed — none of which occurred this turn.

8. **Effect on 315 baseline obligations:** 0. Both existing inventories are unmodified (194 and 121 data rows respectively, unchanged).

9. **Execution count:** 0 tests executed (0 of the 8 proposed, 0 of the 315 existing).

10. **E1 preservation:** unaffected. E1 remains `PUSHED_AND_SERVER_SYNCED`; none of the five E1 targets or the E1 audit artifact was read-write touched by this review.

11. **E3 and E4 exclusion:** `OP-06` (E3) and `OP-01` (E4) remain not executed and not authorized. This review did not produce an E3 implementation specification.

12. **Required next specification amendment:** a narrow amendment to `WAVE_2_OD_005_EXACT_AMENDMENT_EXECUTION_SPECIFICATION.md` (or a successor document) that (a) authorizes creation of a new canonical `OD-005` amendment-test inventory file (or, if preferred, an explicit schema-extension adjudication of the numerical inventory), (b) assigns it a frozen operation ID distinct from `OP-08`, (c) freezes its exact insertion anchor and field mapping, and (d) updates the combined-reconciliation document's counting rule so `315 + 8 = 323` is computed correctly without double-counting.

13. **Final E2 execution status:** **remains unauthorized.** No inventory file was modified; no row was inserted; `323` is not claimed as achieved.

---

**Review outcome:** `E2_REQUIRES_NEW_CANONICAL_INVENTORY_SPECIFICATION`
