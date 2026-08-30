# NUM-DEC-03 Adjudication: M2 Exact-Null Implementation

> **Design/decision only. No M2 source file modified or created. No null model implemented. No parametric bootstrap executed. No tournament run. No historical data fitted. Nothing staged, committed, pushed, or deployed.**

> **Document-completeness correction notice (applied after initial freeze):** the source researcher instruction for this adjudication was truncated mid-transmission during the original turn, producing a document with 29 sections and 25 required future tests (`M2-NULL-001`–`025`). The full authoritative instruction was subsequently recovered and requires **30 sections** and **30 required future tests** (`M2-NULL-001`–`030`). This is a document-completeness correction only — **no researcher decision, formula, threshold, or authorization status changed**. No content from the original document was deleted; two sections that existed outside the authoritative 30-section structure ("M2 Exact-Null Applicability Conditions", "Profiling and Null-Comparison Consistency") were relocated into their appropriate authoritative sections rather than removed.

---

## 1. Scope

This document adjudicates **NUM-DEC-03 only**: the representation of the exact null `H0: n=0` within M2's interval-censored MBPP-style Hawkes estimator. `NUM-DEC-04` through `NUM-DEC-08` remain `PENDING_RESEARCHER_DECISION` and are not addressed here. No implementation, bootstrap execution, tournament rerun, or historical-data fitting is authorized by this decision.

## 2. Authoritative Evidence

Read in full before adjudication:

```text
MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md           (S10-S14: M2 equations, parameter space, exact-null open decision)
MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv          (51-row V2 gate spec)
MODEL_3B_RECOVERY_PROTOCOL_V2.md
MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv
MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv            (8-row ledger; NUM-DEC-01/02 APPROVED_WITH_LIMITATIONS prior to this turn)
MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md
MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md
MODEL_3B_AMENDMENT_02_M2_ESTIMAND_ADJUDICATION.md    (Proposal 2 -- n=alpha/beta primary estimand)
MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md               (alpha-beta ridge; n sharply identified, alpha/beta individually not)
```

Baseline confirmed before this turn: 70/70 original gates reconciled to 51 V2 gates (`MODEL_3B_GATE_V1_TO_V2_RECONCILIATION.csv`); NUM-DEC-01 = `APPROVED_WITH_LIMITATIONS` (1,000 attempted replications/cell); NUM-DEC-02 = `APPROVED_WITH_LIMITATIONS` (profile likelihood primary for `n`, parametric bootstrap secondary, Wald diagnostic-only, Bayesian not selected); NUM-DEC-03 through NUM-DEC-08 = `PENDING_RESEARCHER_DECISION`.

## 3. Mathematical Question

M2's amended primary estimand is `n = alpha/beta` (integrated excitation mass). The mathematical specification (S13) leaves the exact-null representability of M2's own interval-censored likelihood unresolved, and explicitly states the M3 solution (S16) does not automatically transfer — M2's kernel form and estimator differ structurally from M3's discrete-time Bayesian formulation. The question NUM-DEC-03 resolves: **how is `H0: n=0` represented and tested within M2, and by what statistic and calibration method?**

## 4. Available Options

The following options were considered for representing and testing the M2 exact null:

```text
SELECTED (Option A): EXPLICIT_NESTED_NULL_SUBMODEL_WITH_BOOTSTRAP_CALIBRATED_LIKELIHOOD_RATIO
    -- exact n=0 nested submodel; nuisance parameters reoptimized under H0; likelihood-ratio
       statistic T_LR calibrated by parametric bootstrap under the exact null (not the
       interior chi-square approximation, invalid at the n=0 boundary).

REJECTED (Options B-G): epsilon clipping; near-zero n treated as exact zero; Wald lower bound
    greater than zero; profile-interval exclusion of zero as the sole existence test; Bayesian
    spike-and-slab imported from M3 without redesign; n=0 with retained H1 nuisance estimates.
    Full rationale for each rejection: Section 21 ("Rejected Exact-Null Options").
```

The selection is recorded formally in Section 6 ("Researcher Decision"). Option A was selected because it is the only option among those considered that (i) represents `n=0` exactly rather than approximately, (ii) reestimates nuisance parameters under the null rather than inheriting them from the alternative fit, and (iii) calibrates its decision threshold empirically at the parameter-space boundary rather than assuming an interior asymptotic approximation.

## 5. M2 Kernel and Parameterization

```text
Excitation kernel:            g(u) = alpha * exp(-beta * u),  u > 0
Integrated excitation mass:   n = integral_0^inf g(u) du = alpha / beta
Prospective parameterization: alpha = n * beta,  0 <= n < 1,  beta > 0
```

## 6. Researcher Decision

```text
NUM-DEC-03:                          APPROVED_WITH_LIMITATIONS
CANDIDATE:                           M2
SELECTED OPTION:                     EXPLICIT_NESTED_NULL_SUBMODEL_WITH_BOOTSTRAP_CALIBRATED_LIKELIHOOD_RATIO
NULL:                                H0: n = 0
ALTERNATIVE:                         H1: 0 < n < 1
PRIMARY COMPARISON STATISTIC:        LIKELIHOOD-RATIO STATISTIC (T_LR)
NULL CALIBRATION:                    PARAMETRIC BOOTSTRAP UNDER H0
INTERIOR CHI-SQUARE CUTOFF:          NOT ASSUMED AT THE BOUNDARY (diagnostic reference only)
MIXTURE / HURDLE / BAYESIAN INDICATOR: NOT SELECTED FOR M2
IMPLEMENTATION:                      NOT_AUTHORIZED
TOURNAMENT EXECUTION:                NOT_AUTHORIZED
HISTORICAL FIT:                      NOT_AUTHORIZED
```

## 7. Exact Null

Under `H0: n=0`:

```text
alpha = 0
g(u)  = 0  for all u
```

The model reduces exactly to the shared non-excitation interval-count baseline. The null **must** be represented exactly. The following are explicitly **not** acceptable representations of the null:

```text
n = epsilon
n approximately zero
logit(n) at a large negative finite value
alpha clipped to a small positive value
a numerical lower bound greater than zero
```

This mirrors the M3 exact-null defect (`n = expit(logit_n)` structurally excludes `n=0`, MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md S16) but is adjudicated independently for M2 per S13's explicit non-transfer instruction.

## 8. Excitation Alternative

Under `H1: 0 < n < 1`, the excitation kernel is strictly positive (`alpha > 0`, `beta > 0`) and the process is genuinely self-exciting, subject to the stationarity constraint `n < 1`. `H1` is the regime over which the profile-likelihood uncertainty method (`NUM-DEC-02`) constructs its confidence set for the magnitude of `n`, **conditional on existence already being established** by the exact-null comparison adjudicated in this document (Section 15, "Relationship to NUM-DEC-02"). `H1` shares every structural component with `H0` other than the excitation term itself (Section 9, "Null Model") — it is not a separately specified model, but the unconstrained counterpart of the same nested family.

## 9. Null Model

The future M2 implementation must contain an **explicit constrained null submodel**. The null and excitation models must share, where applicable:

```text
interval observation model
baseline equation
baseline covariates
exposure definition
CD scenario
dispersion convention
source-observation mechanism
interval boundaries
missing-report assumptions
duplicate-report assumptions
parent-child episode assumptions
```

The only intended structural difference must be the excitation component. If the null and alternative cannot be made nested, classify:

```text
M2_NULL_AND_ALTERNATIVE_NOT_NESTED
```

and return for researcher review. Comparing models with mismatched baseline or observation structures is not permitted, silently or otherwise.

## 10. Nuisance Reoptimization

```text
theta_1 = (n, psi)      parameters under H1
theta_0 = psi_0         parameters under H0
```

Every nuisance parameter identifiable under H0 must be **reestimated** under the null. It is not acceptable to compute the null likelihood by setting `n = 0` while retaining nuisance estimates fitted under H1 (this is explicitly rejected as option `M2-NULL-G`, S21).

```text
ell_0 = max over psi_0 of ell(n = 0, psi_0)
ell_1 = max over 0 < n < 1 and psi of ell(n, psi)
```

## 11. Likelihood-Ratio Statistic

```text
T_LR = 2 * (ell_1 - ell_0)
     = 2 * [ ell(n_hat, psi_hat) - ell(n = 0, psi_hat_0) ]
```

Required numerical properties:

```text
- T_LR must be finite
- T_LR must be nonnegative within a declared numerical tolerance
- null and alternative likelihood conventions must match (identical sign, identical scaling)
- nuisance parameters must be reoptimized independently in each fit
- convergence must be recorded for both the null and alternative fits
```

A materially negative `T_LR` indicates optimizer failure, a sign mismatch, a non-nested implementation, or another numerical inconsistency. It must **not** be silently clamped to zero without explicit disclosure.

## 12. Boundary Limitation

`n = 0` lies on the boundary of `0 <= n < 1`. The ordinary interior likelihood-ratio cutoff — chi-square with one degree of freedom — is therefore **not automatically valid**. The conventional interior critical value:

```text
chi-square_1,0.95 ~= 3.841
```

may be recorded only as a **diagnostic reference**. It is **not adopted** as the M2 exact-null decision threshold. Selected calibration method:

```text
PARAMETRIC_BOOTSTRAP_UNDER_EXACT_NULL
```

## 13. Parametric-Bootstrap Calibration

Future implementation requirement (record only, not executed here). For each calibration scenario under H0:

```text
1. Set true n = 0 exactly.
2. Generate synthetic interval data using the approved observation regime.
3. Fit the explicit null model.
4. Fit the excitation model.
5. Calculate T_LR.
6. Retain all convergence, boundary, and invalid-output statuses.
7. Build the empirical null distribution of T_LR.
```

For `B` validly accounted calibration attempts:

```text
c_alpha = empirical quantile at (1 - alpha) of the null T_LR distribution
c_0.05  = empirical 0.95 quantile of T_LR under H0        (alpha = 0.05)
```

**`c_0.05` is not selected or computed in this adjudication turn.**

## 14. Calibration and Evaluation Separation

```text
M2_NULL_CALIBRATION_SET:  estimates the null critical value; must not determine the final reported FPR
M2_NULL_EVALUATION_SET:   estimates final FPR; must remain unopened until the critical value and procedure are frozen
```

Deterministic, disjoint seed manifests are required for the two sets. No historical data may be used in either set.

## 15. False-Positive Rate

Future candidate rule (record only):

```text
select excitation if:  T_LR > c_0.05         (c_0.05 frozen from a separate calibration set)

FPR_hat = (1 / R0_metric) * sum over valid metric-bearing null replications of I(T_LR > c_0.05)
```

Necessary target: `FPR_hat <= 0.05`, evaluated jointly with FNR, power, and complete accounting per the versioned V2 gate specification and MCSE reporting (S23) — never satisfied by a rule that eliminates all detection power (S16).

## 16. False-Negative Rate and Power

After calibrating the null decision rule, future positive scenarios must evaluate:

```text
false-negative rate
detection power
bias of n
RMSE of n
profile-likelihood coverage
predictive calibration
convergence
sensitivity to weak beta identification
```

```text
FNR_hat = (1 / R1_metric) * sum over valid metric-bearing positive replications of I(T_LR <= c_0.05)
```

A low false-positive rate achieved by never selecting excitation is **not acceptable**. The future decision rule must report both FPR and FNR/power together.

## 17. Relationship to NUM-DEC-01

NUM-DEC-01's accounting (1,000 attempted replications per cell) remains authoritative. Bootstrap-calibration attempts and final evaluation attempts must each carry:

```text
immutable replication IDs
deterministic seeds
attempted / valid / metric-bearing / failed / invalid counts
complete reconciliation
```

No repeated simulation to obtain a target number of favorable `T_LR` values is permitted.

## 18. Relationship to NUM-DEC-02

NUM-DEC-02 selected `PROFILE_LIKELIHOOD_FOR_N` as the primary uncertainty method for the **magnitude** of excitation (`n`, conditional on excitation existing). NUM-DEC-03 selects `EXPLICIT_NESTED_NULL_SUBMODEL_WITH_BOOTSTRAP_CALIBRATED_LIKELIHOOD_RATIO` for the **existence** of excitation versus the exact null. These are different quantities requiring different machinery:

```text
Profile likelihood:               uncertainty for excitation magnitude n
Likelihood-ratio model comparison: existence of excitation versus exact null
```

Required order:

```text
EXACT-NULL MODEL COMPARISON
  -> EXCITATION-EXISTENCE DECISION
    -> PROFILE-LIKELIHOOD UNCERTAINTY FOR n CONDITIONAL ON H1
```

An interval lower bound greater than zero must not be used as a substitute for exact-null testing (rejected option `M2-NULL-E`, S21).

## 19. Profile-Likelihood Boundary Status

Profile likelihood (NUM-DEC-02) may include `n = 0` in the confidence set. Ordinary interior chi-square calibration at `n = 0` is not adopted for that interval either. Boundary inclusion must be reported explicitly via candidate statuses:

```text
PROFILE_INTERVAL_EXCLUDES_ZERO
PROFILE_INTERVAL_INCLUDES_ZERO
PROFILE_INTERVAL_ONE_SIDED_AT_ZERO
PROFILE_INTERVAL_FAILED
```

These statuses remain diagnostic unless tied prospectively to the approved exact-null decision rule of this document (S15).

**Consistency between profiling and null comparison** (relocated from the former standalone section "Profiling and Null-Comparison Consistency" — content preserved, not deleted): the future implementation must ensure that the profile-likelihood computation (NUM-DEC-02) and the null-model comparison (this document) are mutually consistent:

```text
- the same likelihood function is used for profile likelihood and model comparison
- identical interval-count conventions are used
- identical source-observation assumptions are used
- identical CD scenario definitions are used
- identical parameter transformations are used
- identical optimizer tolerances are documented
```

No model comparison is valid if the null and alternative use mismatched likelihood definitions, and no profile-likelihood interval is valid if it is built from a likelihood definition that differs from the one used in the exact-null comparison.

## 20. Separation from M3

```text
M3 (Bayesian model comparison):     P(M1 | Y)
M2 (likelihood-based comparison):   T_LR = 2 * (ell_1 - ell_0)
```

Not imported into M2: M3 prior model odds, M3 posterior model probability, M3 Bayes-factor rule, M3 ROPE, M3 threshold tau. The scientific null (`excitation absent`) is similar across candidates, but the inference machinery is different by design and must remain so.

## 21. Rejected Exact-Null Options

```text
M2-NULL-B: epsilon clipping                                              -- REJECTED (violates exact-null requirement, S7)
M2-NULL-C: near-zero n treated as exact zero                             -- REJECTED (same)
M2-NULL-D: Wald lower bound greater than zero                            -- REJECTED (Wald diagnostic-only per NUM-DEC-02; not an existence test)
M2-NULL-E: profile interval exclusion of zero as the sole existence test -- REJECTED (S19: diagnostic only, not the decision rule)
M2-NULL-F: Bayesian spike-and-slab imported from M3 without redesign     -- REJECTED (S20: separation from M3; would require its own prior/calibration decisions)
M2-NULL-G: n=0 while retaining alternative-model nuisance estimates      -- REJECTED (S10: nuisance parameters must be reestimated under H0)
```

## 22. Baseline-Confounding Scenarios

Exact-null calibration must include scenarios where temporal variation arises from mechanisms other than excitation:

```text
changing baseline intensity
CD-1 latent-event covariation
CD-2 observation probability
overdispersion
source concentration
parent-child episode dependence
missing reports
duplicate reports
exogenous shocks
```

The test must not classify these mechanisms as excitation merely because counts cluster temporally.

## 23. Monte Carlo Uncertainty

```text
MCSE(FPR_hat) = sqrt[ FPR_hat * (1 - FPR_hat) / R0_metric ]
MCSE(FNR_hat) = sqrt[ FNR_hat * (1 - FNR_hat) / R1_metric ]
```

The actual metric-bearing denominator must be reported; planned attempts must never be substituted for valid metric denominators (consistent with NUM-DEC-01's accounting rules).

## 24. Critical-Value Uncertainty

The empirical critical value itself carries finite-simulation uncertainty. Future implementation must report:

```text
calibration attempt count
valid T_LR count
empirical quantile method
interpolation convention
uncertainty/stability assessment for the critical value
seed sensitivity
scenario specificity
```

## 25. Scenario-Specific versus Pooled Calibration

The future implementation must compare `SCENARIO_SPECIFIC_CRITICAL_VALUES` versus `POOLED_NULL_CRITICAL_VALUE`. No pooling choice is made in NUM-DEC-03:

```text
M2_NULL_CRITICAL_VALUE_POOLING: REQUIRES_PREIMPLEMENTATION_REVIEW
```

This is a methodological implementation detail, not a new numerical-ledger decision, unless later evidence shows it materially changes candidate adjudication.

## 26. Required Future Tests

Items `M2-NULL-001` through `M2-NULL-007` are **verbatim from the researcher's original source instruction**. That instruction was truncated mid-sentence at item `M2-NULL-008` ("Nuisance..."); items `M2-NULL-008` through `M2-NULL-025` were completed by the adjudicating agent at that time to give every requirement stated elsewhere in the original document at least one traceable future test, and this was disclosed rather than hidden.

**Superseding completeness note:** the full authoritative instruction was subsequently recovered by the researcher and requires `M2-NULL-001` through `M2-NULL-030` — five additional tests (`M2-NULL-026`–`030`) beyond what either the truncated instruction or the agent's completion produced. This note records that supersession explicitly: the original document did **not** contain all 30 tests, and this correction adds the five missing ones without renumbering or altering `M2-NULL-001`–`025`.

**Verbatim (source-specified, turn 1):**

```text
M2-NULL-001: The model parameter space includes exact n = 0.
M2-NULL-002: Under n = 0, alpha equals exactly zero.
M2-NULL-003: Under n = 0, the excitation kernel is exactly zero.
M2-NULL-004: The null model retains the approved interval observation model.
M2-NULL-005: The null and alternative share baseline structure.
M2-NULL-006: The null and alternative share exposure structure.
M2-NULL-007: The null and alternative share dispersion convention.
```

**Agent-completed (disclosed, due to source truncation after M2-NULL-007, turn 1):**

```text
M2-NULL-008: Nuisance parameters under H0 are reestimated at n=0, never inherited from the H1 fit.
M2-NULL-009: T_LR is verified finite for every calibration and evaluation replication.
M2-NULL-010: T_LR is verified nonnegative within declared numerical tolerance.
M2-NULL-011: A materially negative T_LR is flagged and disclosed, never silently clamped to zero.
M2-NULL-012: Bootstrap null calibration sets true n=0 exactly in the data-generating process.
M2-NULL-013: M2_NULL_CALIBRATION_SET and M2_NULL_EVALUATION_SET use disjoint deterministic seed manifests.
M2-NULL-014: The evaluation set is verified unopened until the critical value and procedure are frozen.
M2-NULL-015: No historical data is used in either the calibration set or the evaluation set.
M2-NULL-016: FPR_hat uses R0_metric (valid metric-bearing null replications), never R0_attempt.
M2-NULL-017: FNR_hat and detection power are computed and reported for positive-excitation scenarios.
M2-NULL-018: MCSE(FPR_hat) and MCSE(FNR_hat) are reported using actual metric-bearing denominators.
M2-NULL-019: All four profile-likelihood boundary statuses (S19) are represented explicitly, none silently collapsed.
M2-NULL-020: The same likelihood function and identical interval-count/observation/CD-scenario/parameter-transformation conventions are used for profiling and null comparison.
M2-NULL-021: Optimizer tolerances used in both the null and alternative fits are documented.
M2-NULL-022: Baseline-confounding scenarios (S22, 9 listed) do not trigger a false excitation-existence decision.
M2-NULL-023: The M2_NULL_AND_ALTERNATIVE_NOT_NESTED check is performed for every configuration and returned for review if triggered.
M2-NULL-024: Scenario-specific versus pooled critical values are compared before any pooling is assumed.
M2-NULL-025: None of the six rejected options (M2-NULL-B through M2-NULL-G) are used as substitutes for the approved design.
```

**Verbatim (source-specified, completeness-correction turn 2 — the five previously missing tests):**

```text
M2-NULL-026: Baseline-confounding null scenarios are included.
             Required meaning: the exact-null calibration must include scenarios where time
             variation comes from changes in baseline intensity rather than excitation.
M2-NULL-027: CD-2 observation-process scenarios are included.
             Required meaning: the calibration must include scenarios where CD modifies
             observation or detection probability, not latent historical event intensity.
M2-NULL-028: Episode-dependence scenarios are included.
             Required meaning: parent-child and same-episode dependence must be represented
             so that episode structure is not incorrectly classified as self-excitation.
M2-NULL-029: Missing and duplicate reporting scenarios are included.
             Required meaning: the calibration must evaluate both omitted events and repeated
             reports of the same historical episode.
M2-NULL-030: No historical data enter null calibration.
             Required meaning: all exact-null calibration and decision-rule development must
             use synthetic data only. Historical data cannot be used to choose the critical
             value, pooling rule, threshold, or scenario weights.
```

Total required future tests: **30** (`M2-NULL-001`–`030`), 30 unique IDs, no duplicates, no gaps.

## 27. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```

No M2 source file (`m2_mbpp.py` or any other) is modified or created by this adjudication. No null submodel, no bootstrap calibration routine, and no decision-rule code is written.

## 28. Tournament Nonauthorization

```text
TOURNAMENT EXECUTION: NOT_AUTHORIZED
```

No synthetic recovery execution, calibration run, or evaluation run occurs as part of producing this adjudication.

## 29. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```

No historical data file is read, written, or referenced by this adjudication.

## 30. Decision Summary

```text
NUM-DEC-03:                     APPROVED_WITH_LIMITATIONS
DOCUMENT COMPLETENESS:          CORRECTED (30/30 sections, 30/30 future tests -- see completeness notice above)
Selected design:                EXPLICIT_NESTED_NULL_SUBMODEL_WITH_BOOTSTRAP_CALIBRATED_LIKELIHOOD_RATIO
H0 / H1:                        n = 0  /  0 < n < 1
Comparison statistic:           T_LR = 2 * (ell_1 - ell_0)
Boundary calibration:           parametric bootstrap under exact null (interior chi-square = diagnostic reference only)
Critical value c_0.05:          NOT computed in this turn
Calibration/evaluation sets:    disjoint, deterministic, no historical data
Relationship to NUM-DEC-02:     existence (NUM-DEC-03) precedes conditional-magnitude uncertainty (NUM-DEC-02)
Relationship to NUM-DEC-01:     1,000-attempted-replications/cell accounting governs all calibration/evaluation runs
Rejected options:               M2-NULL-B through M2-NULL-G (6)
Required future tests:          30 (M2-NULL-001..007 verbatim source turn 1; 008..025 agent-completed turn 1, disclosed;
                                 026..030 verbatim source turn 2, completeness correction)
Implementation authorized:      NO
Tournament execution authorized: NO
Historical fit authorized:      NO
Remaining pending:              NUM-DEC-04, NUM-DEC-05, NUM-DEC-06, NUM-DEC-07, NUM-DEC-08

Applicability preconditions (relocated from the former standalone section "M2 Exact-Null
Applicability Conditions" -- content preserved, not deleted). Exact-null excitation gates are
applicable to M2 only after all seven conditions below are met; before that, the exact-null
test is classified REQUIRES_PREIMPLEMENTATION_VALIDATION:

  1. n = 0 exists exactly in the parameter space
  2. null and alternative models are correctly specified
  3. nuisance parameters are reoptimized under both models
  4. the likelihood-ratio computation is valid
  5. the bootstrap null calibration completes
  6. the evaluation set is independent
  7. the decision critical value is frozen

Applicability status:           REQUIRES_PREIMPLEMENTATION_VALIDATION (7 preconditions unmet)
Pooling of critical values:     REQUIRES_PREIMPLEMENTATION_REVIEW (not decided)
```

```text
MODEL_3B_NUM_DEC_03_M2_EXACT_NULL_ADJUDICATION_COMPLETENESS_CORRECTED
```
