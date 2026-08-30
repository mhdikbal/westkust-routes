# WAVE 2 — OD-005 Exact Amendment Execution Specification for Retirement of OPT-005-B

Status: **SPECIFICATION-ONLY**. This document specifies, but does not execute, an amendment. No exact additive text in this specification or its companion CSVs has been applied to any source artifact.

Baseline: local HEAD = origin/main = `81af816e7d8691ae515ab22dc671499ddfa36aee`.

Review outcome carried forward: `APPROVED_WITH_LIMITATIONS_TO_RETIRE` (`WAVE_2_OD_005_RETIREMENT_REVIEW_DECISION_DRAFT.md`).

Amendment execution: **NOT AUTHORIZED**. Ledger modification: **NOT AUTHORIZED**. Validator/code modification: **NOT AUTHORIZED**.

---

## 1. Scope

Single object: `OD-005` / `OPT-005-B`. Eight target operations, drawn exactly from `WAVE_2_OD_005_NARROW_AMENDMENT_SURFACE_MAP.csv`'s 8 rows (baseline `9798e7e`), no target added or removed. Full operation detail in `WAVE_2_OD_005_EXACT_AMENDMENT_OPERATIONS.csv`; full additive-text detail in `WAVE_2_OD_005_EXACT_ADDITIVE_TEXT_CATALOG.csv`.

## 2. Sources read this turn (read-only, no new literature search)

Four OD-005 narrow-amendment planning artifacts, four retirement recommendation review artifacts (all re-confirmed byte-identical to commit `81af816`), plus the open-decision ledger, evidence-to-option matrix, and mathematical contract (re-read in full during the retirement recommendation review turn and confirmed unchanged since via `git diff --stat`). Draft adjudication, specification-clarification review, and NUM-DEC-01/02/03 relied on by citation, confirmed byte-identical to baseline.

## 3. Retirement semantics (governing instruction §5)

```text
O_005^pre           = {OPT-005-A, OPT-005-B}                 (current, unchanged by this specification)
O_005^active,post    = O_005^pre \ {OPT-005-B}                (future, only if amendment is separately authorized and executed)
O_005^historical,post = O_005^pre                              (future, unchanged -- OPT-005-B stays in the historical registry)

ACTIVE CANDIDATE REMOVAL != IDENTIFIER DELETION
```

`OPT-005-B`'s future status: `RETIRED_WITH_RATIONALE`. **Not applied at this turn.**

## 4. Eight target operations (summary — full detail in the Operations CSV)

| Operation | Target | Change type | Subwave | Separate authorization required |
|---|---|---|---|---|
| OP-01 | `planning/WAVE_2_OPEN_DECISION_LEDGER.csv` | `MARK_OPTION_RETIRED_WITH_RATIONALE` | E4 | YES |
| OP-02 | `evidence/WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv` | `ADD_CROSS_REFERENCE` | E1 | YES |
| OP-03 | `adjudication/WAVE_2_OD_005_DRAFT_ADJUDICATION.md` | `ADD_CLARIFYING_DEFINITION` | E1 | YES |
| OP-04 | `adjudication/WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md` | `ADD_CROSS_REFERENCE` | E1 | YES |
| OP-05 | `planning/WAVE_2_MATHEMATICAL_CONTRACT.md` | `ADD_PROHIBITED_INTERPRETATION` | E1 | YES |
| OP-06 | `docs/thesis/colab/model3b_spec_validator/schema_validator.py` | `ADD_VALIDATOR_REQUIREMENT` | E3 | YES |
| OP-07 | `adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_PLAN.md` | `ADD_OPERATIONAL_CONTRACT` | E1 | YES |
| OP-08 | `adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_TEST_IMPACT.csv` | `ADD_FUTURE_TEST_REQUIREMENT` | E2 | YES |

All 8 `change_type` values are within the 7-value allowed vocabulary (`RETIRED_WITH_RATIONALE` used inside prose text, not as a `change_type` field value, is distinct from `MARK_OPTION_RETIRED_WITH_RATIONALE`, which IS the vocabulary value used for OP-01). No target requires a rewrite or deletion of baseline content — every operation is a verbatim append at a named anchor.

**Anchor-resolution status (corrected this turn, OP-06 anchor review):** 7 documentation/data operations (`OP-01` through `OP-05`, `OP-07`, `OP-08`) have uniquely resolved insertion anchors, each confirmed against a single, grep-verified occurrence in its target file. `OP-06` is a separately authorized E3 implementation obligation. `OP-06` is not executable under the current amendment authorization: read-only inspection of `docs/thesis/colab/model3b_spec_validator/schema_validator.py` (§7 below) found no existing structural component that validates candidate-option-level status, so no insertion anchor can be determined without a separate E3 implementation-design turn. This specification does **not** claim "8/8 anchors resolve."

## 5. Mathematical invariance carried forward

13/13 mathematical objects (conditional intensity, `n=alpha/beta`, parameter domain, exact null, log-likelihood, full Hessian, `J`, `Var`, `R_attempted,c=1000`, `R_valid,c`, failure accounting, `Coverage_c`/`CoverAndValid_c`, profile likelihood, plus the adversarial `AbsBias_c`/AC-M2-03 check) were independently verified `IDENTICAL` in `WAVE_2_OD_005_RETIREMENT_INVARIANCE_MATRIX.csv` during the review turn. This specification re-affirms: **none of the 8 operations edits any S1-S4 formula**. OP-05's `ADD_PROHIBITED_INTERPRETATION` text (`ATX-05`) exists specifically to make this non-interference explicit and permanent in the frozen mathematical contract, not to alter it.

## 6. Ledger treatment plan (governing instruction §10)

Current state: `OD-005 current_status = OPEN_REQUIRES_ADJUDICATION`.

The ledger's `current_status` column, as observed across all 19 rows at baseline, uses only 3 controlled values: `OPEN_REQUIRES_ADJUDICATION`, `DEFERRED`, `NONBLOCKING_CLARIFICATION`. **No enum value in this observed vocabulary represents "approved with limitations, implementation-dependent."** Per instruction §10, this specification does not invent a new enum value. Instead:

1. `current_status` is specified to remain `OPEN_REQUIRES_ADJUDICATION` (OP-01's postcondition, `WAVE_2_OD_005_EXACT_AMENDMENT_OPERATIONS.csv` row OP-01).
2. The additive change targets the `candidate_options` field only (ATX-01), which the ledger schema already permits to carry free-text content — no schema change required for this specific field.
3. No new `current_status` enum value is created by this specification.
4. **A separate future requirement is recorded here**: a ledger-schema adjudication turn may eventually be needed to decide whether `current_status` should ever carry a value distinguishing "approved-with-limitations pending execution" from "fully open" — this specification takes no position on that question and does not treat OD-005 as closed. OD-005 may still have dependencies beyond OPT-005-B's disposition (its `downstream_impact` field names `REQ-M2-008`/`AC-M2-03`, which remain open regardless of OPT-005-B's fate).

## 7. Validator treatment plan (governing instruction §11) — including OP-06 anchor review

Future validator behavior is fully specified in `ATX-06` (8 explicit behaviors: recognize the historical identifier, recognize `RETIRED_WITH_RATIONALE` if authorized by frozen spec, reject `OPT-005-B` as an active candidate, reject missing rationale, reject identifier deletion, reject unknown replacement identifiers, reject mathematical-contract mutation, leave other active choices unaffected).

**Determination**: validator implementation (OP-06) is classified `E3`, distinct from the `E1` documentation-tier operations (OP-02, OP-03, OP-04, OP-05, OP-07). It is not bundled with any E1 operation and requires its own separate authorization and code review, per instruction §11's explicit requirement to determine this separation rather than assume it.

**OP-06 anchor review (read-only, this turn)**: `docs/thesis/colab/model3b_spec_validator/schema_validator.py` (113 lines) was inspected structurally, without printing code, additive text, or a patch. It contains 1 class (`ValidationResult`) and 4 module-level functions (`validate_gate_spec`, `validate_ledger`, `validate_applicability_matrix`, `validate_specification_set`). `validate_ledger` is the nearest existing related function — it validates the ledger's row-level `current_status` distribution against `EXPECTED_LEDGER_DISTRIBUTION` — but no existing function, class, mapping, or schema field validates candidate-option-level status (there is no existing "candidate-option enum" in this file at all). Because a new structural component would need to be designed to host OP-06's requirement, and that design choice is an architectural decision, OP-06's classification is **`E3_IMPLEMENTATION_SPECIFICATION_REQUIRED`** (not `STRUCTURAL_ANCHOR_RESOLVED_READ_ONLY`, since no existing symbol resolves the anchor without design work; not `VALIDATOR_TARGET_AMBIGUOUS_REQUIRES_REVIEW`, since there is no ambiguity between competing candidates — there are zero existing candidates).

**Stop gate**: E3 (`OP-06`) must not execute, and no code text, function body, or patch for `schema_validator.py` may be written, before a separate, dedicated E3 implementation-specification turn is authorized, produced, reviewed, and locally frozen. This specification records `OP-06` and `ATX-06` as a preserved future obligation only — it neither invents an anchor nor discards the requirement.

## 8. Eight future-test obligations

Full schema in `WAVE_2_OD_005_EXACT_TEST_OBLIGATIONS.csv` (10 columns, 8 rows, `OD005-AMD-001` through `OD005-AMD-008`). All `status=PLANNED_ONLY`, all `historical_data_used=NO`. None is added to the 315-existing-test inventory by this specification (that action is OP-08's own subject and is explicitly deferred to a separate `E2` authorization).

## 9. Requirement and test nonloss (governing instruction §13)

`R_before = R_after`: every operation's `postcondition` field in the Operations CSV states the target's pre-existing content is retained verbatim, with only an append. `T_315^before = T_315^after`: 0 edits to `MODEL_3B_NUMERICAL_TEST_INVENTORY.csv` or `MODEL_3B_AMENDMENT_TEST_INVENTORY.csv` are specified anywhere in this document. `T_proposed ∩ T_315 = ∅`: mechanically re-verified this turn (see terminal report).

## 10. Operation order (governing instruction §15)

```text
1. Verify baseline (81af816e7d8691ae515ab22dc671499ddfa36aee) and clean tracked tree.
2. Verify exact target hashes (see WAVE_2_OD_005_EXACT_CHECKSUM_AND_ROLLBACK_PLAN.md) against the 8 targets.
3. Apply exact additive text (ATX-02 through ATX-05, ATX-07) to the 5 E1 documentation/planning targets -- REQUIRES SEPARATE AUTHORIZATION.
4. Apply exact additive text (ATX-01) to the ledger's candidate_options field only, current_status unchanged -- REQUIRES SEPARATE AUTHORIZATION, subwave E4.
5. Apply future-test inventory addition (ATX-08's eligibility condition) ONLY IF separately authorized -- subwave E2.
6. Apply validator implementation (ATX-06) ONLY IF separately authorized and code-reviewed -- subwave E3.
7. Run structural validators ONLY IF separately authorized.
8. Compute post-amendment SHA-256 hashes for every file actually touched.
9. Produce an amendment audit report comparing pre/post hashes, pre/post K1-K15, and pre/post mathematical-invariance status.
10. Stop before staging.
```

Subwaves:

```text
E1  Documentation amendment   (OP-02, OP-03, OP-04, OP-05, OP-07)
E2  Test-inventory amendment  (OP-08)
E3  Validator implementation  (OP-06)
E4  Ledger update             (OP-01)
```

**E2, E3, and E4 are not implicitly authorized by E1's eventual authorization, and none of the four subwaves is authorized by this specification-only turn.**

## 11. Checksum and rollback

See `WAVE_2_OD_005_EXACT_CHECKSUM_AND_ROLLBACK_PLAN.md` for the full historical-hash table, post-amendment hash procedure, and rollback instructions per operation.

## 12. Precondition / postcondition / stop-condition summary

Precondition (all 8 operations, checked before any future execution): baseline `81af816e7d8691ae515ab22dc671499ddfa36aee` unchanged, tracked tree clean, target file's SHA-256 matches the historical value recorded in the Operations CSV.

Postcondition (all 8 operations): target file retains 100% of its pre-amendment content; only the exact additive text is appended at the named anchor; no formula, no ledger `current_status`, no test status, no identifier is altered beyond what each operation's row explicitly states.

Stop conditions (governing instruction §24): none triggered this turn — see terminal report §30.

## 13. Explicit non-authorization boundary

This specification does **not** authorize: applying any `ATX-01` through `ATX-08` text to any target; marking `OPT-005-B` retired in any source artifact; any ledger, validator, or code change; any addition to the 315-test inventory; any numeric value selection; staging, committing, pushing, server-syncing, deploying, rebuilding, or restarting anything.
