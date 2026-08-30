# WAVE 2 — OD-005 Retirement Review: Decision Draft

Status: **DECISION DRAFT — approves a recommendation for a future amendment-execution turn. Does not itself execute an amendment.**

## 1. Baseline

Local HEAD = origin/main = `9798e7efc840d9f8ff9bae497c3a47534295cbd4`.

## 2. Review scope

Single decision, single option: `OD-005` / `OPT-005-B`. No other open decision (`OD-001` through `OD-004`, `OD-006` through `OD-018`) is substantively reviewed or altered.

## 3. Sources reviewed

Full list in `WAVE_2_OD_005_RETIREMENT_RECOMMENDATION_REVIEW.md` §2: the four OD-005 narrow-amendment planning artifacts, the open-decision ledger, the evidence-to-option matrix, the Wave 2 mathematical contract (read in full this turn), plus the draft adjudication, specification-clarification review, clarification reconciliation, and NUM-DEC-01/02/03 (relied on by citation, confirmed byte-identical to baseline via `git diff --stat`). No literature search performed.

## 4. Exact option description

`OPT-005-B` = "a different exact-null-specific metric" — an unnamed, formula-less placeholder candidate recorded in `WAVE_2_OPEN_DECISION_LEDGER.csv`'s `OD-005` row, `candidate_options` field. No concrete formula, named estimator, or citation exists for it anywhere in the frozen Wave 2 corpus (confirmed by exhaustive source search, options analysis §1, independently re-verified this turn).

## 5. Mathematical invariance verdict

**PASS.** 13/13 mathematical objects checked (12 mandatory per governing instruction §5.8, plus `AbsBias_c`/`AC-M2-03` added adversarially) show `comparison_result=IDENTICAL`, 0 `CHANGED`, 0 `BLOCKING`. See `WAVE_2_OD_005_RETIREMENT_INVARIANCE_MATRIX.csv`.

## 6. Candidate-set effect

Pre-review candidate set `O_005^pre = {OPT-005-A, OPT-005-B}` is unchanged by this review. A future, separately authorized amendment execution would conceptually narrow the *active* set to `O_005^active = {OPT-005-A}` while the *historical* registry `O_005^historical = {OPT-005-A, OPT-005-B}` remains complete — active-candidate removal is explicitly distinct from identifier deletion (governing instruction §6).

## 7. Historical-identifier preservation

**PASS.** `OD-005` and `OPT-005-B` are not deleted, renamed, or reused. The reviewed change semantics (`MARK_OPTION_RETIRED_WITH_RATIONALE`) is additive status-marking, not deletion — confirmed against the surface map's actual `change_type` value, and against the 7-value allowed vocabulary, which contains no delete/remove semantic.

## 8. Requirement nonloss verdict

**PASS.** 10/10 requirements reviewed in `WAVE_2_OD_005_RETIREMENT_REQUIREMENT_NONLOSS_MATRIX.csv` show `preserved=YES`, 0 `loss_detected`, 0 `BLOCKING`. `R_before = R_after` holds for all 10 (one row, NL-04, discloses an explicit `superseded_by` mechanism — the future retirement-rationale text itself — which is the intended resolution path, not an undisclosed loss).

## 9. Test-obligation nonloss verdict

**PASS.** `T_existing ∩ T_removed = ∅` mechanically re-verified this turn: 0 collisions between the 8 proposed `OD005-AMD-001..008` IDs and the 315 existing test IDs. All 8 proposed tests remain `PLANNED_ONLY`. None is proposed for execution or removal from any inventory.

## 10. K1-K15 confirmation

**15/15 CONFIRMED, 0 NOT_CONFIRMED, 0 REQUIRES_CLARIFICATION.** Ground truth re-tested against independent source re-reading this turn (see recommendation-review §8 for the per-criterion table):

```text
RETIRE:      SATISFIED=14, PARTIALLY_SATISFIED=0, NOT_SATISFIED=0, NOT_APPLICABLE=1, TOTAL=15
CONCRETIZE:  SATISFIED=0,  PARTIALLY_SATISFIED=0, NOT_SATISFIED=14, NOT_APPLICABLE=1, TOTAL=15
```

Original planning table rows in `WAVE_2_OD_005_NARROW_AMENDMENT_OPTIONS_ANALYSIS.md` §4 are unmodified by this review.

## 11. Adversarial findings

No blocking finding identified across all 12 adversarial checks in the governing instruction §15 (requirement loss, test-obligation loss, formula change, dangling dependency, ambiguous validator behavior, broken provenance, deletion-readable wording, final-decision-readable wording, OD-006 interaction, OD-015 interaction, hidden-alternative-metric risk, absence-of-specification-only risk). One nonblocking residual item is carried forward as limitation 8 below (validator enum addition deferred to a future turn). Full detail in `WAVE_2_OD_005_RETIREMENT_RECOMMENDATION_REVIEW.md` §10.

## 12. Primary review outcome

```text
OD-005 review outcome: APPROVED_WITH_LIMITATIONS_TO_RETIRE
OPT-005-B amendment execution: NOT AUTHORIZED
OD-005 ledger status: UNCHANGED
OPT-005-B current frozen disposition: WITHHELD_PENDING_AMENDMENT_EXECUTION
```

This statement approves the recommendation for the next, separately authorized amendment-execution turn. It does not apply retirement.

## 13. Limitations (governing instruction §9, all 14 carried forward verbatim)

1. Identifier `OPT-005-B` must be preserved.
2. Retirement status must be added additively, never as a deletion.
3. Rationale and the full source chain must be cited in the eventual amendment text.
4. No mathematical contract (S1-S4 of `WAVE_2_MATHEMATICAL_CONTRACT.md`) may be changed.
5. No numeric value may be selected as part of amendment execution.
6. No existing requirement or existing test (of the 315-inventory) may be deleted.
7. The eight proposed tests (`OD005-AMD-001..008`) must remain `PLANNED_ONLY` through amendment execution.
8. `schema_validator.py` must not be changed by this review; any future enum addition is a separately reviewed, separately authorized change.
9. The open-decision ledger must not be changed at this review stage.
10. Amendment execution requires a separate, explicit authorization turn.
11. A post-amendment checksum must be produced without overwriting any historical checksum.
12. The eventual amendment must be audited before any local freeze.
13. Historical inference remains `NOT_AUTHORIZED` throughout.
14. Phase D must not be re-run under any circumstance arising from this review or a future amendment.

## 14. Amendment-execution prerequisites (for the future, separately authorized turn)

- Explicit authorization naming the exact target paths and exact additive text (not drafted by this review).
- Re-verification that baseline has not drifted since this review.
- Re-verification of all 14 limitations in §13 immediately before execution.
- A dedicated audit pass after execution, before any local freeze.
- Freeze, push, and server-sync to remain separate, individually authorized turns (per this session's established provenance-splitting pattern).

## 15. Prohibited interpretations

This decision draft must **not** be read as:

- `OPT-005-B` has been marked retired in the ledger or specification;
- the open-decision ledger has changed;
- the validator has changed;
- an amendment has been executed;
- `OD-005`'s final decision has moved from `WITHHELD`;
- `OD-006`, `OD-015`, or any other open decision has been affected;
- `NUM-DEC-07`, `OD-016`, `tau`, or `ROPE` status has changed;
- any of the 8 M3 blockers has closed;
- any of the 315 existing tests, or the 8 proposed tests, has executed;
- M0, M2, or M3 has reached any final status;
- historical inference has been authorized;
- `MODEL_VALIDATION_FAILURE` (Model 3B-CD V1) has been reversed;
- the Hawkes family has been ruled out or ruled in;
- Phase D may be re-run.

## 16. Final status boundaries

```text
OD-005 final decision: WITHHELD
OPT-005-B final disposition: WITHHELD_PENDING_AMENDMENT_EXECUTION
Amendment execution: NOT AUTHORIZED
Ledger modification: NOT AUTHORIZED
Recommendation review: APPROVED_WITH_LIMITATIONS_TO_RETIRE
```
