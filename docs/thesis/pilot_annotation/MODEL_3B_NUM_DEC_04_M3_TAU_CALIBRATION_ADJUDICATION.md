# NUM-DEC-04 Adjudication: M3 Posterior Model-Probability Threshold Calibration Procedure

> **Procedure only. No numerical tau selected or frozen. No M3 source file modified or created. No bridge sampling executed. No thermodynamic integration executed. No calibration executed. No tournament run. No historical data fitted. Nothing staged, committed, pushed, or deployed.**

---

## 1. Scope

This document adjudicates **NUM-DEC-04 only**: the *procedure* by which the M3 posterior excitation-model-probability threshold `tau` will eventually be calibrated. It does **not** select a final numerical value for `tau`. `NUM-DEC-07` and `NUM-DEC-08` remain `PENDING_RESEARCHER_DECISION` and are not addressed here. No implementation, calibration execution, tournament rerun, or historical-data fitting is authorized by this decision.

## 2. Authoritative Evidence

```text
MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md
MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv          (51-row V2 gate spec)
MODEL_3B_RECOVERY_PROTOCOL_V2.md
MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv
MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv            (8-row ledger; NUM-DEC-01/02/03/05/06 APPROVED_WITH_LIMITATIONS prior to this turn)
MODEL_3B_NUM_DEC_05_M3_PRIOR_MODEL_ODDS_ADJUDICATION.md
MODEL_3B_NUM_DEC_06_M3_MARGINAL_LIKELIHOOD_ADJUDICATION.md   (contains the m3_bayesian_discrete.py compatibility audit)
MODEL_3B_AMENDMENT_04_M3_EXACT_NULL_ADJUDICATION.md
MODEL_3B_AMENDMENT_05_M3_DECISION_RULE_ADJUDICATION.md
MODEL_3B_M3_NULL_BOUNDARY_AUDIT.md
docs/thesis/colab/model3b_tournament_harness/m3_bayesian_discrete.py   (read-only; re-confirmed, not modified)
```

Baseline confirmed before this turn: 70/70 original gates reconciled to 51 V2 gates; NUM-DEC-01 = `APPROVED_WITH_LIMITATIONS` (1,000 attempted replications/cell); NUM-DEC-02 = `APPROVED_WITH_LIMITATIONS` (profile likelihood for M2's `n`); NUM-DEC-03 = `APPROVED_WITH_LIMITATIONS`, completeness-corrected (30 sections/30 tests, M2 exact null); NUM-DEC-05 = `APPROVED_WITH_LIMITATIONS` (M3 prior odds, equal primary + 3-scenario mandatory sensitivity); NUM-DEC-06 = `APPROVED_WITH_LIMITATIONS` (bridge sampling primary, thermodynamic integration secondary, `log_BF_10`; compatibility classification `FEASIBLE_WITH_IMPLEMENTATION_WORK` with 5 confirmed blockers in `m3_bayesian_discrete.py`); NUM-DEC-04, 07, 08 = `PENDING_RESEARCHER_DECISION`.

## 3. Mathematical Question

Given `P(M1|Y)` as the primary future decision quantity for M3 excitation existence, what is the **procedure** by which a decision threshold `tau` will be calibrated, evaluated, and frozen — such that the exact-null false-positive rate is controlled without eliminating the ability to detect genuine positive excitation? This adjudication answers the procedural question only; it does not answer "what is tau."

## 4. Current Implementation Blockers

Preserved verbatim from NUM-DEC-06's compatibility audit of `m3_bayesian_discrete.py` (not re-derived, not revised here):

```text
1. n_branch is clamped into [EPS, 1-EPS] by _to_unconstrained() -- exact n=0
   is structurally unreachable in the current parameterization.
2. M3 cannot currently represent exact n=0 as a separate nested null model
   (no M0 fitting routine exists at all).
3. log_prior() omits explicit normalizing constants for the Beta(n) and
   Gamma(beta) prior kernels -- improper for marginal-likelihood comparison.
4. fit_m3_mcmc's Metropolis-Hastings proposes in unconstrained space
   (theta0, theta1, logit(n), log(beta)) but evaluates the acceptance ratio
   from the CONSTRAINED-space log_posterior with no Jacobian correction for
   the change of variables -- a correctness defect in the existing sampler.
5. No bridge-sampling implementation exists anywhere in the harness.
6. No thermodynamic-integration implementation exists anywhere in the
   harness.
```

**Therefore: tau calibration cannot be executed on the current M3 implementation.** NUM-DEC-04 approves only the future calibration *procedure* — it does not, and cannot yet, produce a calibrated value.

## 5. Null and Excitation Models

```text
M0 (null):        n = 0
M1 (excitation):   0 < n < 1
```

Definitions and their exact representability are governed by the future M2-style exact-null work for M3 (referenced in `MODEL_3B_AMENDMENT_04_M3_EXACT_NULL_ADJUDICATION.md`), not decided or revised in this document.

## 6. Posterior Model Probability

```text
log_BF_10        = log p(Y | M1) - log p(Y | M0)                      (NUM-DEC-06)

P(M1 | Y)         = [ BF_10 * P(M1) ] / [ BF_10 * P(M1) + P(M0) ]

logit[P(M1 | Y)]  = log_BF_10 + log[ P(M1) / P(M0) ]     (numerically stable form, preferred)
```

`BF_10` must not be obtained by exponentiating `log_BF_10` outside a declared numerically safe range (NUM-DEC-06, preserved).

## 7. Researcher Decision

```text
NUM-DEC-04:                        APPROVED_WITH_LIMITATIONS
CANDIDATE:                         M3
DECISION:                          PROSPECTIVE_SYNTHETIC_THRESHOLD_CALIBRATION_WITH_INDEPENDENT_EVALUATION
PRIMARY DECISION QUANTITY:         P(M1 | Y)
FINAL TAU VALUE:                   NOT_SELECTED  -- this adjudication approves a PROCEDURE, not a number
CANDIDATE CALIBRATION GRID:        0.50, 0.75, 0.90, 0.95, 0.975, 0.99   (comparison only, none adopted)
PRIMARY PRIOR ODDS:                P(M0) = 0.50, P(M1) = 0.50
MANDATORY SENSITIVITY:             0.75/0.25 ; 0.50/0.50 ; 0.25/0.75
NECESSARY FPR TARGET:              MAX over mandatory null scenarios of FPR_hat_s(tau) <= 0.05
FNR / POWER:                       MUST be evaluated jointly with FPR
INCONCLUSIVE OUTCOME:              REQUIRED as a decision-architecture category
IMPLEMENTATION:                    NOT_AUTHORIZED
CALIBRATION EXECUTION:             NOT_AUTHORIZED
TOURNAMENT:                        NOT_AUTHORIZED
HISTORICAL FIT:                    NOT_AUTHORIZED
```

**Tau is not selected anywhere in this document.** Every subsequent section describes the future procedure that will, at a later and separately authorized turn, produce a value.

## 8. Candidate Threshold Grid

```text
0.50, 0.75, 0.90, 0.95, 0.975, 0.99
```

Approved for future calibration comparison only. No grid value is adopted as final here. The grid itself must be stored exactly and must not be silently extended or reduced during future implementation (`M3-TAU-001`, `M3-TAU-002`).

## 9. Prior-Odds Scenarios

```text
NULL_FAVORING:        P(M0)=0.75, P(M1)=0.25
EQUAL (primary):       P(M0)=0.50, P(M1)=0.50
EXCITATION_FAVORING:  P(M0)=0.25, P(M1)=0.75
```

All three scenarios (frozen by NUM-DEC-05, not revised here) must be used in future calibration. Posterior probabilities must not be averaged across scenarios, and the scenario producing the most favorable classification must not be selected preferentially.

## 10. Calibration Dataset

Future design (record only, not built here): a deterministic seed manifest, `M3_TAU_CALIBRATION_SET`, used to evaluate candidate `tau` values, estimate exact-null FPR, evaluate FNR/power, inspect prior-odds sensitivity, and inspect baseline/observation-process confounding, culminating in a **separate, later** researcher decision that selects one `tau`. The calibration set must **not** be used for final gate evaluation.

## 11. Independent Evaluation Dataset

Future design (record only, not built here): a separate, independent, **unopened** deterministic seed manifest, `M3_TAU_EVALUATION_SET`. It must remain unopened until all of the following are frozen:

```text
1. exact-null M3 is implemented
2. excitation M3 is implemented
3. proper internal parameter priors are frozen
4. Jacobian-correct posterior sampling is validated
5. bridge sampling is validated
6. thermodynamic-integration cross-check is completed on the required subset
7. prior model odds are frozen
8. tau is selected and frozen
9. model and gate versions are frozen
```

No calibration or implementation is performed in this adjudication.

## 12. False-Positive Rate

```text
FPR_hat(tau) = (1 / R0_metric) * sum over r in metric-bearing null replications of I[P(M1|Y_r) >= tau]
```

Necessary criterion: `FPR_hat(tau) <= 0.05` — necessary but **not sufficient** (see Section 18). For each estimate, report: `R_attempt`, `R_valid`, `R_metric`, failed model comparisons, bridge failures, TI failures where applicable, prior-sensitive comparisons, MCSE, uncertainty interval. Planned attempts must never be substituted for the metric denominator when fewer outputs are valid.

## 13. False-Negative Rate

```text
FNR_hat(tau) = (1 / R1_metric) * sum over r in metric-bearing positive replications of I[P(M1|Y_r) < tau]
```

Reported per positive-`n` scenario: `n_true`, signal class, FNR, power, MCSE, unsuccessful model-comparison count, prior-odds sensitivity.

## 14. Power

```text
Power_hat(tau) = 1 - FNR_hat(tau)
```

A threshold satisfying `FPR<=0.05` but eliminating meaningful positive-signal detection **must be rejected** — low FPR achieved by never detecting excitation is not an acceptable outcome (Section 20).

## 15. Monte Carlo Uncertainty

```text
MCSE(p_hat) = sqrt[ p_hat * (1 - p_hat) / R_metric ]
```

Future calibration must report MCSE for: FPR, FNR, power, failure rate, prior-sensitive decision rate, inconclusive rate. When a confidence/MC-uncertainty interval around FPR crosses 0.05, classify: `BORDERLINE_FPR_REQUIRES_RESEARCHER_REVIEW` — such a threshold must not be silently classified as passing.

## 16. Multiple Null Scenarios

FPR control must hold across **every** mandatory null scenario, not only pooled FPR. Required reporting: scenario-specific FPR, pooled FPR, worst-case FPR, MCSE for each, denominator for each. If a scenario has insufficient valid model-comparison results: `THRESHOLD_CALIBRATION_INCOMPLETE` — it must not be pooled away.

## 17. Worst-Case FPR Requirement

```text
max over mandatory null scenarios of FPR_hat_s(tau) <= 0.05
```

This worst-case rule is approved as the **default** necessary calibration requirement (not merely the pooled criterion).

## 18. Positive-Signal Scenarios

A future prespecified positive-`n` grid is required, taken from the frozen recovery design or separately adjudicated **before** calibration — this adjudication does not invent or modify that grid. If no complete positive-`n` grid currently exists, record: `M3_POSITIVE_SIGNAL_GRID_REQUIRES_PREIMPLEMENTATION_CONFIRMATION`. Positive scenarios must vary: signal strength; lag decay/weight pattern; baseline intensity; overdispersion; observation-process distortion; episode dependence; missing and duplicate reporting.

## 19. Threshold Selection Procedure

The future prospective procedure must follow exactly these 15 ordered steps (none executed in this adjudication):

```text
 1. Freeze model equations and internal priors.
 2. Freeze prior model odds and sensitivity scenarios.
 3. Freeze bridge-sampling and TI implementations.
 4. Freeze calibration and evaluation seed manifests.
 5. Run calibration data only.
 6. Evaluate every candidate tau in the prespecified grid.
 7. Retain thresholds satisfying FPR <= 0.05 across all mandatory null scenarios.
 8. Among retained thresholds, evaluate FNR and power across the prespecified positive-n grid.
 9. Reject thresholds that achieve FPR control only by eliminating useful power.
10. Evaluate decision sensitivity across the three prior-odds scenarios.
11. Produce a threshold-calibration report.
12. Obtain an explicit researcher decision selecting tau.
13. Freeze tau in a new versioned specification.
14. Open the independent evaluation set.
15. Evaluate final performance without changing tau.
```

`tau` must not be optimized against the evaluation set, and must not be selected separately per evaluation cell.

## 20. Prohibited Automatic Selection Rules

The final threshold must **not** be defined automatically by:

```text
- choosing the lowest tau with FPR <= 0.05
- choosing the highest overall accuracy
- maximizing Youden's J
- minimizing total misclassification
- selecting the best historical-data result
- selecting the value favoring excitation
- selecting the value favoring the null
- selecting tau = 0.95 by convention alone
```

The future calibration report must present the trade-offs to the researcher; a **separate** researcher decision selects the final value (Step 12, Section 19).

## 21. Inconclusive Outcome

The final decision architecture must support:

```text
EXCITATION_SUPPORTED
NO_EXCITATION_SUPPORTED
INCONCLUSIVE
```

## 22. Three-Way Reporting

A future two-threshold architecture may use `EXCITATION_SUPPORTED` if `P(M1|Y) >= tau_excitation`, `NO_EXCITATION_SUPPORTED` if `P(M0|Y) >= tau_null`, and `INCONCLUSIVE` otherwise. **NUM-DEC-04 does not select `tau_excitation` or `tau_null`.** A single calibrated `tau` may remain the primary FPR/FNR calculation threshold, while the final three-way reporting rule requires a separate symmetric or asymmetric calibration. Record explicitly, not hidden:

```text
THREE_WAY_REPORTING_THRESHOLDS: REQUIRE_PREIMPLEMENTATION_DECISION
```

## 23. Prior Sensitivity

For every candidate `tau`, future calibration must evaluate categorical decisions under all three prior-odds scenarios (Section 9). Required statuses: `PRIOR_ROBUST`, `PRIOR_SENSITIVE`, `INCONCLUSIVE_ACROSS_PRIORS`. The exact numerical definition of prior robustness remains unresolved:

```text
PRIOR_ROBUSTNESS_TOLERANCE: REQUIRES_PREIMPLEMENTATION_DECISION
```

No tolerance is invented here.

## 24. Marginal-Likelihood Stability

Threshold calibration may use a posterior model probability only when: the bridge estimate is valid; repeated bridges are stable; required TI validation is satisfactory; no material method disagreement exists; internal priors are proper; Jacobians are correct; posterior diagnostics pass (all per NUM-DEC-06). Otherwise, classify the replication `MODEL_COMPARISON_INVALID` — it must not enter `R_metric` for FPR/FNR, but it remains in attempted-run accounting.

## 25. Relationship to NUM-DEC-05

NUM-DEC-05 selected equal model odds as the primary synthetic baseline plus mandatory null-favoring and excitation-favoring sensitivity scenarios. NUM-DEC-04 must use all three (Section 9) — NUM-DEC-05 is not revised here.

## 26. Relationship to NUM-DEC-06

NUM-DEC-06 selected bridge sampling as the primary marginal-likelihood method and thermodynamic integration as secondary validation. NUM-DEC-04 depends on successful future implementation and validation of both method layers, and on resolution of the five confirmed blockers (Section 4) — NUM-DEC-06 is not revised here.

## 27. Relationship to NUM-DEC-07

NUM-DEC-07 (M3 ROPE `epsilon_n`) remains pending. ROPE concerns excitation magnitude conditional on M1; tau concerns model existence. `P(n <= epsilon_n | Y, M1)` must not be used as a substitute for `P(M0 | Y)` unless separately adjudicated.

## 28. Baseline and Observation Confounding

Future calibration's mandatory null scenarios must vary: baseline intensity; baseline temporal changes; overdispersion; CD-0; CD-1 where mathematically defined; CD-2 observation probability; source concentration; parent-child episode dependence; missing reporting; duplicate reporting; exogenous shocks; count sparsity; prior model odds. The threshold must not systematically classify these non-excitation mechanisms as self-excitation.

## 29. Required Future Tests

Record but do not execute:

```text
M3-TAU-001: Candidate tau grid is stored exactly.
M3-TAU-002: No candidate tau is silently added or removed.
M3-TAU-003: Calibration and evaluation seed manifests are independent.
M3-TAU-004: Evaluation data remain unopened during calibration.
M3-TAU-005: Exact-null FPR is computed for every mandatory null scenario.
M3-TAU-006: Worst-case null-scenario FPR is reported.
M3-TAU-007: Pooled FPR is reported separately.
M3-TAU-008: FPR MCSE is reported.
M3-TAU-009: FNR is computed for every positive n scenario.
M3-TAU-010: Power is reported as one minus FNR.
M3-TAU-011: FNR and power MCSE are reported.
M3-TAU-012: Thresholds eliminating all meaningful power are rejected.
M3-TAU-013: All three prior-odds scenarios are evaluated.
M3-TAU-014: Prior-sensitive decisions are reported.
M3-TAU-015: Model-comparison failures remain in attempted-run accounting.
M3-TAU-016: Invalid model comparisons do not enter metric denominators.
M3-TAU-017: Bridge stability is checked before posterior probability is used.
M3-TAU-018: TI validation status is checked.
M3-TAU-019: Proper prior normalization is verified.
M3-TAU-020: Transformation Jacobians are verified.
M3-TAU-021: No lower-bound greater than zero shortcut is used.
M3-TAU-022: No estimated n greater than zero shortcut is used.
M3-TAU-023: Tau is not selected by historical-data performance.
M3-TAU-024: Tau is not selected using the final evaluation set.
M3-TAU-025: The final selected tau requires explicit researcher approval.
M3-TAU-026: The final selected tau is versioned and frozen before evaluation.
M3-TAU-027: INCONCLUSIVE remains an available outcome.
M3-TAU-028: Three-way reporting thresholds remain explicitly governed.
M3-TAU-029: Baseline-confounding null scenarios are included.
M3-TAU-030: CD-2 observation-process scenarios are included.
M3-TAU-031: Episode-dependence scenarios are included.
M3-TAU-032: Missing-report scenarios are included.
M3-TAU-033: Duplicate-report scenarios are included.
M3-TAU-034: Exogenous-shock scenarios are included.
M3-TAU-035: No historical data enter threshold calibration.
M3-TAU-036: Raw calibration rows reconcile with threshold summaries.
M3-TAU-037: Repeated calculations from the same evidence are deterministic.
M3-TAU-038: No threshold receives final PASS before independent evaluation.
```

Total required future tests: **38** (`M3-TAU-001`–`038`), 38 unique IDs, no gaps, no duplicates.

## 30. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```

No M3 source file (`m3_bayesian_discrete.py` or any other) is modified or created by this adjudication. None of the five confirmed blockers (Section 4) is fixed here.

## 31. Calibration Nonauthorization

```text
CALIBRATION EXECUTION: NOT_AUTHORIZED
```

No candidate `tau` value is evaluated against any data, synthetic or historical, in producing this adjudication.

## 32. Tournament Nonauthorization

```text
TOURNAMENT EXECUTION: NOT_AUTHORIZED
```

No synthetic recovery execution, calibration run, or evaluation run occurs as part of producing this adjudication.

## 33. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```

No historical data file is read, written, or referenced by this adjudication.

## 34. Decision Summary

```text
NUM-DEC-04:                     APPROVED_WITH_LIMITATIONS
Nature of this decision:        PROCEDURE ONLY -- tau itself is NOT selected
Selected procedure:             PROSPECTIVE_SYNTHETIC_THRESHOLD_CALIBRATION_WITH_INDEPENDENT_EVALUATION
Primary decision quantity:      P(M1 | Y)
Final tau value:                NOT_SELECTED
Candidate grid (comparison only): 0.50, 0.75, 0.90, 0.95, 0.975, 0.99
Primary prior odds:             P(M0)=0.50, P(M1)=0.50 (NUM-DEC-05)
Mandatory sensitivity:          0.75/0.25 ; 0.50/0.50 ; 0.25/0.75 (NUM-DEC-05)
Necessary FPR criterion:        max over mandatory null scenarios of FPR_hat_s(tau) <= 0.05 (necessary, not sufficient)
FNR / power requirement:        mandatory, jointly evaluated; power-eliminating thresholds rejected
Inconclusive outcome:           required decision-architecture category
Three-way reporting thresholds: REQUIRE_PREIMPLEMENTATION_DECISION (unresolved, disclosed)
Prior-robustness tolerance:     REQUIRES_PREIMPLEMENTATION_DECISION (unresolved, disclosed)
Positive-signal grid status:    M3_POSITIVE_SIGNAL_GRID_REQUIRES_PREIMPLEMENTATION_CONFIRMATION (if not already frozen elsewhere)
Implementation blockers:        5, inherited unchanged from NUM-DEC-06 (Section 4)
Relationship to NUM-DEC-05:     uses equal-odds primary + mandatory sensitivity grid unchanged
Relationship to NUM-DEC-06:     depends on bridge sampling + TI validation, both currently unimplemented
Relationship to NUM-DEC-07:     ROPE (pending) is not a substitute for this model-existence threshold
Required future tests:          38 (M3-TAU-001..038)
Implementation authorized:      NO
Calibration execution authorized: NO
Tournament execution authorized: NO
Historical fit authorized:      NO
Remaining pending:              NUM-DEC-07, NUM-DEC-08
```

```text
MODEL_3B_NUM_DEC_04_M3_TAU_CALIBRATION_ADJUDICATED
```
