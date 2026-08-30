# Amendment Adjudication — Proposal 5: M3 Excitation Decision Rule

> **Decision record only. No exact-null model implemented. No decision rule implemented. No threshold selected. No prior odds selected. No M3 recovery rerun. No gate specification changed. No historical data fitted. Nothing staged, committed, pushed, or deployed.**

---

## 1. Scope

This document adjudicates **only** `PROPOSAL-05` — replacing M3's invalid decision rule (a strictly-positive estimate or lower interval bound) with a calibrated model-existence decision rule operating on the exact-null-versus-excitation model design approved under `PROPOSAL-04`. `PROPOSAL-01` through `PROPOSAL-04` were adjudicated separately and are **not** touched — all four remain `APPROVED_WITH_LIMITATIONS`, `implementation_authorized=NO`, `rerun_authorized=NO`, `historical_fit_authorized=NO`. `PROPOSAL-06` and `PROPOSAL-07` are **not** adjudicated here.

## 2. Authoritative Evidence

```text
Diagnostic-audit commit:    4b94cd689c995765102b4ca4c63e2636334432bb
Authoritative status:       MODEL_3B_PILOT_DIAGNOSTIC_AUDIT_PUSHED_AND_SERVER_SYNCED
Tournament verdict:         NOT_AVAILABLE
Historical-data fitting:    NOT_AUTHORIZED
Proposal 1 status:          APPROVED_WITH_LIMITATIONS (implementation-free)
Proposal 2 status:          APPROVED_WITH_LIMITATIONS (implementation-free)
Proposal 3 status:          APPROVED_WITH_LIMITATIONS (implementation-free)
Proposal 4 status:          APPROVED_WITH_LIMITATIONS (implementation-free)
```

## 3. Current Invalid Decision Rule

The current M3 implementation uses `n = expit(logit_n)` and an excitation decision equivalent to `lower interval bound > 0.0`. Since every finite `logit_n` produces `0 < n < 1` (Proposal 4, §5), the current rule forces an excitation-positive decision under the exact-null experiment, regardless of data. Observed: **200 of 200 null-cell replications classified as excitation present.**

```text
Classification:    M3_DECISION_RULE_INVALID_FOR_EXACT_NULL_TEST
NOT classified as: M3_GENUINE_100_PERCENT_FALSE_POSITIVE_MODEL_FAILURE
```

## 4. Proposal 4 Dependency

`PROPOSAL-04` established that exact `n=0` must exist in the model support (preferred direction: `M3-NULL-A`, explicit two-model comparison). **`PROPOSAL-05` establishes how evidence selects between the exact-null and excitation models, given that support now exists.** Proposal 5 depends on Proposal 4 and does **not** replace or modify it.

## 5. Null and Excitation Models

```text
M0:  n = 0
M1:  0 < n < 1
z:   excitation-state indicator (z=0 -> M0, z=1 -> M1)
```

## 6. Researcher Decision

```text
PROPOSAL-05: APPROVED_WITH_LIMITATIONS

Candidate:                   M3 Bayesian discrete-time Hawkes
Primary decision quantity:    Posterior probability of the excitation model
Decision threshold:            Must be calibrated prospectively under
                                exact-null simulations
Target false-positive rate:    <= 0.05
Fixed universal threshold:     NOT ASSUMED
Bayes factor:                  SECONDARY DIAGNOSTIC
ROPE:                          SUPPLEMENTARY MAGNITUDE INTERPRETATION ONLY
Implementation:                 NOT_AUTHORIZED
Rerun:                          NOT_AUTHORIZED
Historical fit:                 NOT_AUTHORIZED
```

## 7. Primary Decision Quantity

```text
P(M1 | Y)   equivalently   P(z = 1 | Y)
```

Preferred future decision form: declare excitation present only if `P(M1|Y) >= tau`, where `tau` is selected prospectively through synthetic calibration. **`tau` is not set in this adjudication turn.**

## 8. Mathematical Decision Rule

```text
delta_tau(Y) = 1 if P(M1|Y) >= tau, else 0

delta_tau(Y) = 1  means the decision procedure selects the excitation model.

FPR_hat(tau) = (1/R0) * sum_{r=1}^{R0} I[ P(M1|Y_r) >= tau ]   (exact-null sims)
FNR_hat(tau) = (1/R1) * sum_{r=1}^{R1} I[ P(M1|Y_r) <  tau ]   (positive-excitation sims)
```

The decision threshold must be selected before the final recovery tournament and then **frozen**.

## 9. Threshold Calibration

**Primary requirement:** the selected `tau` must satisfy `FPR_hat(tau) <= 0.05` for the mandatory exact-null calibration scenarios. **This condition is necessary but not sufficient** — the threshold must also be evaluated for: false-negative rate; detection power; calibration across source-observation scenarios; calibration across baseline-intensity scenarios; calibration across overdispersion scenarios; calibration across episode-dependence scenarios; sensitivity to prior model odds; sensitivity to missing and duplicate reporting; stability across seeds. **A threshold must not be chosen solely because it produces `FPR<=0.05` in one easy null cell** — per the researcher's own framing, FPR must not be satisfied by an extreme threshold that eliminates all excitation-detection capability; it must be assessed jointly with FNR, calibration, and power against a positive-`n` grid.

**No universal 0.95 assumption**: `tau=0.95` is not assumed universally correct. A candidate value such as 0.95 may be included in a calibration grid, but must not be adopted without evidence. Prospective diagnostic grid (not an execution authorization):

```text
tau candidates: 0.50, 0.75, 0.90, 0.95, 0.975, 0.99
```

**Preferred threshold-selection procedure (recorded, not executed):**
```text
1. Evaluate a prespecified threshold grid on a separate calibration dataset.
2. Identify thresholds satisfying FPR<=0.05 across all mandatory null scenarios.
3. Among qualifying thresholds, evaluate FNR and power over the
   prespecified positive-n grid.
4. Reject thresholds that achieve low FPR only by eliminating meaningful
   positive-signal detection.
5. Select one threshold through explicit researcher adjudication.
6. Freeze the selected threshold before final recovery evaluation.
7. Use an independent evaluation seed set for the final tournament.
```

## 10. Calibration and Evaluation Separation

```text
CALIBRATION SET:  used to choose tau
EVALUATION SET:   used to assess final recovery gates
```

`tau` must **not** be calibrated and evaluated on the same replications. The evaluation set must remain unopened until the threshold and decision rule are frozen. No historical data may be used to choose `tau`.

## 11. False-Positive Rate

```text
FPR_hat(tau) = (1/R0) * sum_{r=1}^{R0} I[ P(M1|Y_r) >= tau ]
```
Mandatory calibration requirement: `FPR_hat(tau) <= 0.05` across all mandatory exact-null scenarios (§9), assessed jointly with FNR (§12) — never in isolation.

## 12. False-Negative Rate

```text
FNR_hat(tau) = (1/R1) * sum_{r=1}^{R1} I[ P(M1|Y_r) < tau ]
```
Evaluated over a prespecified positive-`n` grid. A threshold that minimizes FPR by driving FNR toward 1 (i.e., the model never detects real excitation) is explicitly rejected by the selection procedure in §9, step 4.

## 13. Monte Carlo Uncertainty

```text
MCSE(FPR_hat) = sqrt( FPR_hat * (1-FPR_hat) / R0 )
MCSE(FNR_hat) = sqrt( FNR_hat * (1-FNR_hat) / R1 )
```
Future gate reports must include: estimate; denominator; MCSE; uncertainty interval; threshold comparison. A result near 0.05 must not be classified confidently without accounting for Monte Carlo uncertainty (consistent with Proposal 3's MCSE treatment for M2).

## 14. Prior Model Odds

```text
P(M1|Y) / P(M0|Y) = BF_10(Y) * [P(M1)/P(M0)]
```
Future implementation must record: `P(M0)`; `P(M1)`; the Bayes-factor or marginal-likelihood method used; sensitivity to reasonable prior model odds; posterior model probability. **Proposal 5 does not select exact prior odds.** Default equal prior model odds (`P(M0)=0.5`, `P(M1)=0.5`) may be evaluated as **one candidate**, but are not adopted by this adjudication. A separate versioned implementation review must justify prior odds.

## 15. Bayes-Factor Status

```text
BF_10 = p(Y|M1) / p(Y|M0)
```
Approved as a **secondary diagnostic** — not adopted as the sole primary decision rule. Universal evidence categories (`BF_10>3`, `>10`, `>100`) are not assumed without explicit threshold provenance and synthetic calibration. If Bayes factors are used, the future implementation must document: marginal-likelihood estimator; estimator uncertainty; prior sensitivity; numerical stability; reproducibility; behavior under exact-null simulations.

## 16. ROPE Status

A region of practical equivalence (`0 <= n <= epsilon_n`) may **supplement** magnitude interpretation but does **not replace** the exact-null-versus-excitation-state comparison approved under Proposal 4. `epsilon_n` is not selected by Proposal 5. Any future `epsilon_n` requires one of: literature-derived substantive interpretation; simulation-design requirement; comparative benchmark; explicit researcher policy — and must **not** be derived from the observed historical fit.

## 17. Null Decision versus Magnitude

Future M3 output must separate: (1) excitation existence, `P(M1|Y)`; (2) excitation magnitude conditional on excitation, posterior distribution of `n` given `M1`. Required reporting: `P(M1|Y)` **and, separately**, `E[n|Y,M1]` and a credible interval for `n` conditional on `M1`. **A model-averaged small positive `n` must not be reported as proof of excitation existence** — this is exactly the failure mode Proposal 4/5 together are designed to prevent.

## 18. Inconclusive Outcome

Future M3 decisions must support at least:

```text
EXCITATION_SUPPORTED
NO_EXCITATION_SUPPORTED
INCONCLUSIVE   (mandatory outcome, must not be engineered away)
```

A candidate rule may define `EXCITATION_SUPPORTED: P(M1|Y)>=tau_high`, `NO_EXCITATION_SUPPORTED: P(M0|Y)>=tau_null`, `INCONCLUSIVE: neither condition met` — but `tau_high`/`tau_null` are **not** selected here; if a symmetric rule is proposed, it must be separately calibrated. No dataset may be forced into either excitation or no-excitation.

## 19. Baseline-Confounding Guard

The decision rule must be tested where apparent persistence arises from: baseline changes; CD observation effects; overdispersion; source concentration; parent-child episode dependence; missing reporting; duplicate reporting; exogenous shocks. **The M3 decision rule must not label these mechanisms as excitation merely because counts are temporally clustered** — directly targeting the root-cause audit's confirmed confounds (source-observation confounding, parent/child dependence).

## 20. Observation-Regime Requirements

All calibration must reproduce the Atlas observation regime: year-level counts; no artificial within-year ordering; source-observation scenarios; episode dependence; missing events; duplicate reporting; prespecified CD roles. The decision rule must **not** be validated only under idealized continuous timestamps.

## 21. Applicability Boundary

The M3 excitation decision rule applies only when: the candidate model contains an exact null; the excitation alternative is defined; the data-generating scenario identifies true null or positive excitation; decision quantities are finite; prior model odds are recorded; the calibration protocol is complete.

## 22. Relationship to M0

```text
M0: NOT_APPLICABLE_TO_MODEL_DOMAIN
```
Consistent with the diagnostic audit's Mathematical Domain ruling (GATE-002/003/005/006/036) — M0 has no excitation parameter, so this decision rule does not apply to it.

## 23. Relationship to M2

```text
M2: SEPARATE_EXACT_NULL_AND_DECISION_RULE_REVIEW_REQUIRED
```
Consistent with Proposal 4 §17 (`M2_EXACT_NULL_REVIEW: SEPARATE_DEPENDENCY`) — the M3 decision rule does not automatically apply to M2. Proposal 2 and Proposal 3 are unaltered.

## 24. Required Future Tests (recorded, NOT executed this turn)

```text
M3-DEC-001: Exact-null simulation returns valid model-comparison output.
M3-DEC-002: Positive-excitation simulation returns valid model-comparison output.
M3-DEC-003: Posterior probabilities sum to one.
M3-DEC-004: Prior model odds are explicitly recorded.
M3-DEC-005: Threshold calibration uses a separate seed set.
M3-DEC-006: Final evaluation uses an unopened independent seed set.
M3-DEC-007: Exact-null FPR is computed correctly.
M3-DEC-008: Positive-scenario FNR is computed correctly.
M3-DEC-009: MCSE is reported for FPR.
M3-DEC-010: MCSE is reported for FNR.
M3-DEC-011: Threshold satisfies FPR <= 0.05 across mandatory null scenarios.
M3-DEC-012: Threshold does not eliminate all positive-signal power.
M3-DEC-013: Weak-signal scenarios may produce INCONCLUSIVE.
M3-DEC-014: Baseline changes are not systematically classified as excitation.
M3-DEC-015: Observation-process variation is not systematically classified
            as excitation.
M3-DEC-016: Episode dependence is included in calibration scenarios.
M3-DEC-017: Missing and duplicate reporting scenarios are included.
M3-DEC-018: Prior-odds sensitivity is reported.
M3-DEC-019: Bayes-factor computation is numerically stable if used.
M3-DEC-020: Magnitude estimation is reported conditional on M1.
M3-DEC-021: No estimated n > 0 shortcut is used.
M3-DEC-022: No lower-bound > 0 shortcut is used without exact-null model
            comparison.
M3-DEC-023: M0 excitation gates remain not applicable.
M3-DEC-024: M2 decision rule remains separately governed.
M3-DEC-025: No historical data are used in calibration.
M3-DEC-026: Repeated execution is deterministic under the same seed manifest.
M3-DEC-027: Calibration and final evaluation outputs reconcile with raw
            replication rows.
M3-DEC-028: Original 200/200 result remains preserved as historical
            pilot evidence.
```

## 25. Original-Evidence Preservation

**Not modified by this document:** original M3 source (`m3_bayesian_discrete.py`); the original 200/200 null result; original M3 raw outputs; the original 70-row gate specification; the diagnostic audit; Proposal 1, 2, 3, and 4 adjudications — confirmed byte-unchanged (§ Validation below). The original decision-rule failure remains part of the audit trail, unretracted.

## 26. Future Versioning

Any future implementation must create versioned specifications. Suggested identifiers (not created in this turn): `MODEL_3B_M3_EXACT_NULL_SPECIFICATION_V2`, `MODEL_3B_M3_DECISION_RULE_SPECIFICATION_V2`, `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2`.

## 27. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```
No exact-null model, decision rule, or threshold is implemented. No `tau` value, no prior odds, no `epsilon_n` is selected by this document.

## 28. Rerun Nonauthorization

```text
RERUN: NOT_AUTHORIZED
```
No M3 execution (of any scale) is performed.

## 29. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```
`data/research/linimasa_events.csv` and `data/export/linimasa_events.csv` are not read, written, or referenced by any executed code in this adjudication turn.

## 30. Decision Summary

```text
PROPOSAL-05: APPROVED_WITH_LIMITATIONS
Primary decision quantity:     P(M1|Y)
Threshold:                     NOT SET -- requires prospective synthetic
                                calibration (grid: 0.50/0.75/0.90/0.95/0.975/0.99)
Target FPR:                    <= 0.05, jointly with FNR/power/calibration
Bayes factor:                  SECONDARY DIAGNOSTIC
ROPE:                          SUPPLEMENTARY MAGNITUDE ONLY
Inconclusive outcome:           MANDATORY
Calibration/evaluation split:   REQUIRED, distinct seed manifests
Prior model odds:               NOT SELECTED, equal-odds is one candidate only
M0 applicability:                NOT_APPLICABLE_TO_MODEL_DOMAIN
M2 applicability:                SEPARATE_EXACT_NULL_AND_DECISION_RULE_REVIEW_REQUIRED
Dependency:                      Proposal 4 (does not replace or modify it)
Implementation:                   NOT_AUTHORIZED
Rerun:                            NOT_AUTHORIZED
Historical fit:                   NOT_AUTHORIZED
```

## Final Status (this document)

```text
MODEL_3B_AMENDMENT_05_M3_DECISION_RULE_ADJUDICATED
```
