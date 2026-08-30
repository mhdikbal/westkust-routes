# WAVE 2 — OD-005 Narrow Additive Nonnumerical Amendment Plan

Status: **PLANNING-ONLY**. This document proposes a narrow additive nonnumerical amendment. It does **not** execute one. No frozen artifact (ledger, evidence matrix, draft adjudication, specification-clarification review, mathematical contract, NUM-DEC-01/02/03, or any V2 specification) has been modified by this planning turn.

Baseline: local HEAD = origin/main = `ce7abcea459c50b36b40e827772c90d70141ca5c` (verified this turn — see §17).

---

## 1. Scope

This plan addresses exactly one narrow question: should `OPT-005-B` (an unnamed, formula-less candidate option under `OD-005`, ledger field `candidate_options`) be RETIRED or CONCRETIZED. Nothing else. `n = alpha/beta` is not redefined. `R_attempted,c`, `FailureRate_c`, `Coverage_c`, and `CoverAndValid_c` are not touched. `OD-006` is out of scope. No numeric value (threshold, tolerance, tau, ROPE, prior, coverage-acceptance value, failure-rate cutoff, bootstrap count, profile grid) is selected anywhere in this document.

## 2. Baseline verification

- `git rev-parse HEAD` = `git rev-parse @{u}` = `ce7abcea459c50b36b40e827772c90d70141ca5c` (equal — confirmed this turn, see §17).
- `git status --short` shows only pre-existing untracked (`??`) out-of-scope leftovers plus the 4 new files created by this plan; no tracked-file modifications.
- `git diff --cached --stat` empty prior to this turn's writes; nothing was staged.

## 3. Source documents read (full provenance chain)

See `WAVE_2_OD_005_NARROW_AMENDMENT_OPTIONS_ANALYSIS.md` §1 for the complete source-to-statement-to-classification chain. Sources: `WAVE_2_OPEN_DECISION_LEDGER.csv`, `WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv`, `WAVE_2_OD_005_DRAFT_ADJUDICATION.md`, `WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md`, `WAVE_2_MATHEMATICAL_CONTRACT.md` (§S2.3, §S2.4), `MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md`, `MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md`, `MODEL_3B_NUM_DEC_03_M2_EXACT_NULL_ADJUDICATION.md`.

## 4. Cross-source consistency check

OPT-005-B's wording ("a different exact-null-specific metric") is identical everywhere it appears. **No inconsistency found — stop condition §16 item 1 does not trigger.**

## 5. Exhaustive formula search

Across all 8 read sources, zero formulas, named methods, or citations exist for OPT-005-B. See options-analysis §1.

## 6. Branch A — RETIRE analysis

Ten-question retirement test: all 10 pass. See options-analysis §2.

## 7. Branch B — CONCRETIZE analysis

Minimum-contract fillability: 1/16 fields weakly fillable, 15/16 not fillable without inventing new mathematical content (out of scope, prohibited). See options-analysis §3.

## 8. K1-K15 rubric

Branch A (RETIRE): SATISFIED=14, PARTIALLY_SATISFIED=0, NOT_SATISFIED=0, NOT_APPLICABLE=1, TOTAL=15. Branch B (CONCRETIZE): SATISFIED=0, PARTIALLY_SATISFIED=0, NOT_SATISFIED=14, NOT_APPLICABLE=1, TOTAL=15. See options-analysis §4.

## 9. Recommendation

`DRAFT_RECOMMEND_RETIRE_FOR_REVIEW` — a draft recommendation for a future adjudication turn, not a final adjudication. See options-analysis §5.

## 10. Identifier / versioning / checksum plan

- `OD-005` identifier: unchanged, never reused, never deleted.
- `OPT-005-B` identifier: preserved under any future retirement (`current_status` field would change; the identifier string itself does not).
- `OPT-005-A` identifier: untouched by this plan.
- `AC-M2-03`: `threshold_value` remains `NULL`; `threshold_status` remains `OPEN_REQUIRES_ADJUDICATION` regardless of this plan's outcome.
- Historical artifact checksums (of the ledger, evidence matrix, draft adjudication, clarification review, math contract, and NUM-DEC-01/02/03 as they stand at `ce7abce`) are distinct from any future post-amendment checksum; none is overwritten by this plan. No checksum computation is performed or recorded by this planning turn beyond the verification in §17.
- Amendment provenance (if executed in the future) would be a separate field/commit distinct from both checksums above.

## 11. Amendment surface map

See `WAVE_2_OD_005_NARROW_AMENDMENT_SURFACE_MAP.csv` — 8 rows, target artifacts identified and NOT modified this turn, each tagged with one of the 7 allowed `change_type` values.

## 12. Future-test impact map

See `WAVE_2_OD_005_NARROW_AMENDMENT_TEST_IMPACT.csv` — 8 test IDs (`OD005-AMD-001` through `OD005-AMD-008`), covering all 8 required test-family types, each `PLANNED_ONLY`, each verified against `MODEL_3B_NUMERICAL_TEST_INVENTORY.csv` and `MODEL_3B_AMENDMENT_TEST_INVENTORY.csv` for zero ID collisions (grep for `OD-005`/`OD005` in both files returned no matches before assigning this namespace).

## 13. Validator impact

The Wave-1 spec validator (`docs/thesis/colab/model3b_spec_validator/`) enforces structural/schema validity only, not semantic concreteness of candidate-option text (established in the prior clarification-review stage). A future RETIRE amendment may require adding a `RETIRED` enum value to the candidate-option status field in `schema_validator.py` — flagged as a target for future inspection in the surface map, not inspected line-by-line or modified this turn.

## 14. What this plan explicitly does NOT do

No amendment executed. No ledger change. No evidence-matrix change. No draft-adjudication change. No specification change. No NUM-DEC change. No numeric value selected. No new literature search. No code created or modified. No statistical procedure or test execution. No `.gitignore` fix. No untracked-leftover deletion. No staging, commit, push, server sync, deploy, rebuild, or restart.

## 15. Stop-condition check

All stop conditions in the governing instruction were checked; none triggered (cross-source consistency confirmed §4; sufficient frozen evidence found to complete both branch analyses; no missing required source).

## 16. Reversibility statement

Everything in this plan is reversible: it created 4 new documentation files and modified nothing else. Deleting these 4 files would fully revert this turn's effect on the repository.

## 17. Mechanical verification (performed this turn)

- `git rev-parse HEAD` = `ce7abcea459c50b36b40e827772c90d70141ca5c`; `git rev-parse @{u}` = same. Equal — confirmed.
- `git diff --stat ce7abce -- docs/thesis/pilot_annotation/model3b_v2/planning docs/thesis/pilot_annotation/model3b_v2/numerical_decisions docs/thesis/pilot_annotation/model3b_v2/evidence docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_DRAFT_ADJUDICATION.md docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md` (all protected artifacts read this turn) confirmed empty prior to this turn's new-file writes, and remains empty for every file other than the 4 newly created ones.
- The 4 new files were checked for pre-existence before creation (`ls` on target directory) — none existed.
- Secret scan (grep for common credential/token/key patterns) on the 4 new files: no matches.
- `git status --short` after writes shows exactly 4 new untracked files under `model3b_v2/adjudication/` plus pre-existing unrelated untracked leftovers; 0 staged paths; 0 modified tracked paths.

## 18. Terminal disposition

No amendment created. No ledger touched. Nothing staged or committed. This plan is a proposal for a future adjudication turn only.

---

OD-005 final decision: WITHHELD
OPT-005-B final disposition: WITHHELD
Amendment execution: NOT AUTHORIZED
