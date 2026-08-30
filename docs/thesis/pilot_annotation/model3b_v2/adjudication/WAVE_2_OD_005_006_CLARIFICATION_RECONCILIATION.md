# OD-005 / OD-006 Specification-Clarification Reconciliation

> **Status: REVIEW ARTIFACT.** Not an amendment, not a final adjudication, not a ledger change. Authoritative baseline: `9da3d9fec04341e5fb71ecb934b8acdc59f7d044`.

## 1. Scope

Reconciles the two per-OD specification-clarification reviews (`WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md`, `WAVE_2_OD_006_SPECIFICATION_CLARIFICATION_REVIEW.md`) against each other and against the frozen sources both draw on.

## 2. Summary of classifications

| Decision | Clarification | Primary classification | Amendment required this turn? |
|---|---|---|---|
| `OD-005` | Retire vs. concretize `OPT-005-B` | **C — `ADDITIVE_NONNUMERICAL_AMENDMENT_REQUIRED`** | No — a future non-numerical amendment is recommended, not created |
| `OD-006` | Does `OPT-006-B` adoption require a separate amendment turn re `NUM-DEC-02`'s band? | **B — `RESOLVABLE_BY_CROSS_DOCUMENT_RECONCILIATION`** (procedural sub-question only) | No amendment needed for *this* procedural question; the substantive metric choice remains a separate, unresolved `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` |

## 3. No conflict between OD-005 and OD-006 results

The two reviews address independent questions (ledger housekeeping for an unnamed option, vs. a procedural governance question about threshold re-derivation) and reach different classifications (C vs. B) for reasons specific to each — this is expected, not a conflict. Neither review's source chain or conclusion contradicts the other's. Both reviews independently confirm the same underlying facts (e.g. `NUM-DEC-01`'s `R_valid,c`/`R_attempted,c`/`FailureRate_c` requirement, `NUM-DEC-02`'s `0.925`–`0.975` band) without divergence.

## 4. Primary estimand preserved

`n = alpha / beta` is referenced identically in both reviews (via `WAVE_2_MATHEMATICAL_CONTRACT.md` §S2.1) and is not touched by either clarification — `OD-005`/`OD-006` concern M2 *diagnostic* metrics (bias, coverage), not the estimand itself.

## 5. `alpha`/`beta` remain diagnostic-only

Neither review references `alpha` or `beta` as anything other than diagnostic parameters (per `WAVE_2_MATHEMATICAL_CONTRACT.md` §S2.1, `NUM-DEC-02`). No statement in either review elevates them to primary-estimand status.

## 6. Attempted denominator not replaced by valid-only denominator

Both reviews explicitly preserve the invariant `R_attempted,c = R_valid,c + sum_k R_failure,c,k` and `R_attempted,c = 1000` (`NUM-DEC-01`). The `OD-006` review's finding that `Coverage_c` (`OPT-006-A`, valid-denominator) is the metric already load-bearing in `NUM-DEC-02`'s frozen band does **not** state or imply that the attempted-denominator/`FailureRate_c` accounting requirement is relaxed — `NUM-DEC-01`'s joint-reporting mandate applies regardless of which coverage metric is eventually adopted, and both reviews say so explicitly.

## 7. Conditional coverage not used to hide failed fits

Consistent with `WAVE_2_OD_006_DRAFT_ADJUDICATION.md` §8–9 (unaltered by this reconciliation): `Coverage_c` must always be reported jointly with `FailureRate_c` and the `R_attempted,c`/`R_valid,c` split — the `OD-006` clarification review does not weaken this requirement; it only resolves a *procedural* question about what governance step would be needed if the *other* option (`CoverAndValid_c`) were instead adopted.

## 8. Complementary metric not promoted to primary without authorization

`CoverAndValid_c` remains explicitly a **candidate**, not a primary metric, in both `WAVE_2_MATHEMATICAL_CONTRACT.md` §S2.6 and the `OD-006` clarification review. This reconciliation does not promote it. The `OD-006` review's classification (`B`) answers only "would adopting it require a separate amendment turn" (yes) — it does not adopt it, does not recommend adopting it over `Coverage_c`, and explicitly defers the substantive choice to the still-open `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` component.

## 9. No new threshold or tolerance

Zero numeric values were selected in either review. `AC-M2-02` and `AC-M2-03` remain `threshold_status=OPEN_REQUIRES_ADJUDICATION`, `threshold_value=NULL` in `WAVE_2_MATHEMATICAL_CONTRACT.md` — mechanically re-verified (§16 below), unchanged.

## 10. No final decision status

Both reviews explicitly restate:

```text
OD-005 final decision: WITHHELD
OD-006 final decision: WITHHELD
```

Neither review uses `APPROVED`, `REJECTED`, `RESOLVED`, `CLOSED`, `PASS`, `FAIL`, `MANDATED`, or `FINAL` as a decision status. (Occurrences of "resolved"/"final" in this reconciliation and the two reviews appear only in the classification-letter labels themselves — e.g. `RESOLVABLE_BY_CROSS_DOCUMENT_RECONCILIATION`, `FINAL_DECISION` as a section heading — which are the required governing vocabulary from the drafting/review instructions, not an assertion that either OD has been finally decided.)

## 11. No ledger change

Mechanically confirmed: `git diff --stat` against baseline `9da3d9f` for `WAVE_2_OPEN_DECISION_LEDGER.csv` is empty (§16).

## 12. No amendment made this turn

Both reviews explicitly recommend a *future* amendment path (§14 of each) without creating one. No new file modifies the ledger's `candidate_options` field, `NUM-DEC-02`, or any frozen gate specification.

## 13. Aggregate finding

| Metric | Value |
|---|---|
| Clarifications reviewed | 2 (`CLARIFY-OD-005-01`, `CLARIFY-OD-006-01`) |
| OD set | exactly `{OD-005, OD-006}` |
| Conflicts found | 0 |
| Ambiguities found | 1 (`OD-005`, in-scope) + 0 (`OD-006`'s procedural sub-question) — 1 total within scope; the 1 ambiguity noted in `OD-006`'s review (informativeness of future M2 failure modes) is explicitly out of `CLARIFY-OD-006-01`'s scope and already tracked separately as the `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` component |
| Unsupported conclusions | 0 — every classification traces a complete `source path → section/row → explicit statement → mathematical consequence → clarification classification` chain |
| Numerical values selected | 0 |
| Final adjudication statuses used | 0 |

## 14. Recommended sequencing (per the user's stated intent)

1. `OD-006`'s procedural sub-question is already answered by cross-document reconciliation (`B`) — no further amendment work is needed *for that sub-question specifically*. It may be cited directly in a future `OD-006` adjudication proposal.
2. `OD-005` requires a narrowly-scoped, non-numerical additive amendment (choosing retire-vs-concretize for `OPT-005-B`) before an `OD-005` adjudication proposal can be finalized — per the user's own framing, this amendment should be planned as a separate, explicitly-authorized turn, not folded into this review.
3. `OD-006`'s substantive candidate-selection question (`Coverage_c` vs. `CoverAndValid_c`) remains withheld pending implementation evidence about M2's actual failure-mode informativeness — unaffected by this reconciliation.

## 15. Stop-condition check

None of the 10 stop conditions from the governing instruction triggered:

1. Exact clarification consistent across draft and ledger for both OD — confirmed (§2 of each per-OD review).
2. No conflicting answers found across frozen sources.
3. No classification chosen via silent assumption — both source chains are complete and disclosed.
4. Neither closure requires a numeric value.
5. Neither closure *for the clarification as scoped* requires implementation/calibration evidence not yet available (the `OD-006` review explicitly separates the answered procedural question from the still-pending, already-tracked implementation-dependent component).
6. `OD-005`'s amendment scope is bounded (one field, two named remedies) — not open-ended.
7. Neither result changes the primary estimand.
8. Neither result changes the denominator requirement (`NUM-DEC-01` unchanged).
9. Neither result implicitly changes any decision status (`WITHHELD` preserved for both).
10. No protected artifact changed (§16).

## 16. Immutability verification

Mechanically verified via `git diff --stat` against baseline `9da3d9fec04341e5fb71ecb934b8acdc59f7d044`:

```text
18 frozen V2 artifacts .............. unchanged
8 NUM-DEC documents .................. unchanged
Wave 1 files (model3b_spec_validator/) unchanged
10 Wave 2 planning artifacts ......... unchanged
Open-decision ledger ................. unchanged
Adjudication map ...................... unchanged
Batch matrix ........................... unchanged
5 evidence artifacts (OD-005/006/015). unchanged
4 adjudication drafts ................. unchanged
M0/M2/M3 estimation code .............. unchanged
Atlas application code ................ unchanged
Phase D artifacts ...................... unchanged
```

Semantic-status re-confirmation (unchanged):

```text
OD-005 final decision: WITHHELD
OD-006 final decision: WITHHELD
OD-015 final decision: WITHHELD
NUM-DEC-07: DEFERRED
tau final: UNSET
ROPE: DEFERRED
M3 blockers: 8 OPEN
315 substantive tests: NOT EXECUTED
M0 final PASS: NOT ESTABLISHED
M2 recovery and coverage: NOT ESTABLISHED
M3 model selection: NOT EXECUTED
historical inference: NOT_AUTHORIZED
Model 3B-CD V1: MODEL_VALIDATION_FAILURE
Hawkes family: NOT_RULED_OUT
Phase D: COMPLETED_VALID_NEGATIVE_RESULT / DO NOT RERUN
```

## 17. Final status

```text
MODEL_3B_V2_OD_005_006_ADDITIVE_AMENDMENT_REQUIRED
```

Rationale: `OD-005`'s clarification lands on classification `C` (`ADDITIVE_NONNUMERICAL_AMENDMENT_REQUIRED`), which is the more restrictive of the two outcomes (`OD-006`'s procedural sub-question resolves cleanly under `B`). Per the governing instruction's own sequencing note, the overall status reflects the most blocking outcome across the two reviewed clarifications. `OD-006`'s substantive metric-selection question remains separately tracked as evidence-dependent and is not the basis for this turn's final status, since it was never in scope for `CLARIFY-OD-006-01`.
