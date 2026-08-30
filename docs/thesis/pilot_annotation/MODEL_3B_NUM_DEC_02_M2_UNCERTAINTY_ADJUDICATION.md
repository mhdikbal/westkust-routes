# MODEL 3B — NUM-DEC-02 Adjudication: M2 Uncertainty Method for n

Status: `APPROVED_WITH_LIMITATIONS`
Decision scope: NUM-DEC-02 ONLY. NUM-DEC-01 remains as previously adjudicated (`APPROVED_WITH_LIMITATIONS`, unchanged by this document). NUM-DEC-03 through NUM-DEC-08 remain `PENDING_RESEARCHER_DECISION` and are not addressed here.
Implementation authorized: NO. Tournament execution authorized: NO. Historical fit authorized: NO.

## 1. Scope

This document adjudicates exactly one unresolved numerical decision from `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv`: **NUM-DEC-02, M2 uncertainty method for the primary estimand n = alpha/beta**. No other numerical decision (NUM-DEC-01 is already decided and untouched; NUM-DEC-03..08 remain pending) is adjudicated here. No profile-likelihood or bootstrap code is created or modified. No bootstrap or simulation runs. No historical data is fit.

## 2. Authoritative Evidence

Read in full before this adjudication:
- `MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md`
- `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv` (51 rows; GATE-021-V2 explicitly notes: `"Blocked on NUM-DEC-02 (M2 uncertainty method)."`)
- `MODEL_3B_RECOVERY_PROTOCOL_V2.md`
- `MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv`
- `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv` (pre-decision baseline for this turn: NUM-DEC-01 `APPROVED_WITH_LIMITATIONS`, NUM-DEC-02..08 `PENDING_RESEARCHER_DECISION`)
- `MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md` — governs replication accounting (`R_attempt = R_valid + R_failed + R_invalid`, `R_attempt(c) = 1000`) reused directly in the bootstrap coverage-reporting rules below (§17)
- `MODEL_3B_AMENDMENT_02_M2_ESTIMAND_ADJUDICATION.md` (Proposal 2 — establishes n = alpha/beta as M2's primary estimand, and originally left the uncertainty method for n unresolved — SS15)
- `MODEL_3B_AMENDMENT_03_M2_FULL_SCALE_ADJUDICATION.md` (Proposal 3)
- `MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md` — direct empirical confirmation of the alpha-beta ridge: at fixed true `n`, NLL varies by only 1.74 units across a 20× range of `beta` (0.2→4.0), while moving `n` by 40% at fixed `beta` costs 551 NLL units — three orders of magnitude more curvature. This is the concrete evidentiary basis for rejecting a local-Hessian-only (Wald) interval as primary.

## 3. Mathematical Question

Proposal 2 established `n = alpha/beta` as M2's primary estimand but left its uncertainty quantification (standard error / confidence interval) unresolved (SS15). GATE-021-V2 (`ci_coverage_95pct`) cannot be computed until a method is selected. This decision selects that method and fixes the construction/validation rules that follow.

## 4. Available Methods

| Method | Description | Suitability given the ridge evidence |
|---|---|---|
| Profile likelihood for n | Reoptimize nuisance parameters (including `beta`) at each fixed `n`; invert the likelihood-ratio statistic | Matches the identified direction directly; does not assume local Gaussian symmetry |
| Parametric bootstrap | Simulate-refit-record for empirical coverage | Cannot stand alone as primary — provides no analytic interval by itself; used to validate another method |
| Wald / inverse-Hessian interval | Local quadratic approximation around the MLE | Unreliable given the confirmed alpha-beta ridge (near-flat curvature in the mis-identified direction, sharp in the identified one — a single local Hessian conflates both) |
| Bayesian posterior interval | Would require converting M2 into a Bayesian model | Not selected — M2 is not currently a Bayesian model; adopting one imports an entire separate decision chain (priors, calibration) not authorized here |

## 5. M2 Primary Estimand

Excitation kernel: `g(u) = alpha * exp(-beta * u)`. Primary estimand:

```
n = integral_0^infinity g(u) du = alpha / beta
```

Prospective (stationarity-safe) parameterization: `alpha = n * beta`, with `0 <= n < 1`, `beta > 0`. Let `theta = (n, psi)` where `psi` contains nuisance parameters (`beta`, baseline parameters, observation parameters, exposure parameters, and any others defined by the versioned M2 specification).

## 6. Researcher Decision

**Selected primary method: `PROFILE_LIKELIHOOD_FOR_N`.**
**Selected secondary validation: `PARAMETRIC_BOOTSTRAP_COVERAGE_VALIDATION`.**
**Wald / inverse-Hessian interval: `DIAGNOSTIC_ONLY`** — never the primary uncertainty method for M2.
**Bayesian posterior interval: `NOT_SELECTED_FOR_M2`.**

Status recorded in the ledger: `APPROVED_WITH_LIMITATIONS`. Implementation, tournament execution, and historical-data fitting all remain `NOT_AUTHORIZED`.

## 7. Profile-Likelihood Definition

```
ell_p(n) = max_psi ell(n, psi)
n_hat = argmax_n ell_p(n)
```

For an interior estimate, the candidate likelihood-ratio confidence set is:

```
CI_PL = { n : 2 * [ell_p(n_hat) - ell_p(n)] <= c }
```

with conventional asymptotic candidate `c = chi-square(1 df, 0.95) ~= 3.841`. This candidate value is a starting point for the interior region only (§9) — it is **not** automatically valid at the boundary `n = 0` (§10).

## 8. Nuisance Parameters

`psi` is fully reoptimized at every fixed candidate value of `n` (this is what distinguishes profile likelihood from a fixed-nuisance Wald approximation). Reasons this is required, not merely preferred, are recorded in full in §5 as the seven-point justification below.

**Why profile likelihood is primary (all seven reasons recorded):**
1. `n` is the approved primary M2 estimand (Proposal 2).
2. `alpha` and `beta` are not separately identified at annual resolution (confirmed empirically, `MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md` §1).
3. The objective has a ridge in `(alpha, beta)` space.
4. A local Gaussian approximation based only on the inverse Hessian may not represent an asymmetric or ridge-shaped likelihood.
5. Profiling allows nuisance parameters to be reoptimized for each candidate `n`.
6. Profile likelihood preserves the likelihood-based frequentist structure of the current M2 candidate.
7. Profile likelihood does not require converting M2 into a Bayesian model.

## 9. Interior Likelihood-Ratio Interval

For `n` strictly interior to `(0, 1)`, `CI_PL` as defined in §7 with `c ~= 3.841` is the candidate interval. This is the primary method for all interior estimates.

## 10. Boundary Limitation

At `n = 0`, the parameter lies on the boundary of `0 <= n < 1`. The ordinary interior chi-square approximation must **not** be assumed valid for exact-null inference at the boundary. Recorded:

- `INTERIOR_PROFILE_LIKELIHOOD: PRIMARY_METHOD`
- `EXACT_NULL_BOUNDARY_CRITICAL_VALUE: REQUIRES_NUM_DEC_03_AND_SYNTHETIC_CALIBRATION`

NUM-DEC-02 does **not** select the exact-null implementation or the boundary critical-value rule. NUM-DEC-03 remains `PENDING_RESEARCHER_DECISION` and governs that question.

## 11. Parametric-Bootstrap Role

Approved strictly as **secondary validation**, evaluating: empirical coverage of the profile-likelihood interval; boundary behavior; finite-sample distortion; bias of `n`; interval width; failure rate; sensitivity to source-observation scenarios; sensitivity to weak identifiability of `beta`.

Per synthetic replication `b`:
1. Simulate data using the prespecified generating parameters.
2. Fit M2 using the future approved implementation.
3. Compute `n_hat_b`.
4. Compute the profile-likelihood interval.
5. Record whether the true `n` lies inside the interval.
6. Retain optimization and profiling failures as outcomes (never discarded).

```
Coverage_hat = (1 / R_metric) * sum over b in valid metric-bearing replications of I[n_true in CI_b]
```

The report must also disclose `R_attempt`, `R_valid`, `R_metric`, interval failures, profiling failures, and excluded-output reasons. **NUM-DEC-01 remains governing for all replication accounting** — the `R_attempt = R_valid + R_failed + R_invalid` decomposition and the failed-run policy apply identically to bootstrap replications.

**Bootstrap cannot replace failed runs**: no silent resimulation of failed bootstrap or recovery fits; every failed fit remains recorded; no replacement seed is generated merely to obtain the planned number of successful intervals.

## 12. Wald Diagnostic Status

Wald / inverse-Hessian intervals may be computed only as **diagnostics**, never as the primary uncertainty method for M2. Reasons: the confirmed alpha-beta ridge; possible asymmetry; the parameter boundary at `n=0`; nuisance-parameter uncertainty; and the demonstrated weakness of incomplete covariance treatment documented elsewhere in this project (the M0 full-Hessian correction, Proposal 1). A disagreement between the Wald and profile-likelihood intervals is **not** automatically classified as a profile-likelihood failure — the disagreement itself is diagnostic evidence about the local geometry of the likelihood surface.

## 13. Bayesian-Interval Exclusion

A Bayesian posterior interval is **not** selected for M2 in this decision. M2 remains a likelihood-based interval-censored candidate. A Bayesian redesign of M2 would require a fully separate set of future decisions: prior on `n`, prior on `beta`, prior-predictive calibration, posterior calibration, an exact-null model, and a model-comparison rule. None of this is imported from M3. `P(M1|Y)` (M3's primary decision quantity) is **not** reused as the M2 primary uncertainty quantity — M3 is Bayesian model comparison, M2 remains likelihood-based unless separately redesigned in a future decision. No M3 threshold, prior odds, Bayes-factor method, or ROPE is adopted for M2 by this decision.

## 14. Profile Grid

A future implementation (not built now) must define a deterministic profile grid or adaptive profiling procedure over `0 <= n < 1`:
- Include `n = 0` when supported by the NUM-DEC-03 design.
- Resolve the region near `n_hat`.
- Record grid points, optimized nuisance parameters, and optimizer status at every point.
- Preserve objective values.
- Detect disconnected confidence regions, one-sided intervals, intervals reaching `n = 0`, and intervals approaching the upper stationarity boundary.
- Not force every confidence set to be a symmetric two-sided interval.

## 15. Allowed Interval Forms

The future implementation must support all of the following, and the last two must never be silently converted into an ordinary symmetric interval:

```
TWO_SIDED_INTERVAL
LOWER_ONE_SIDED_INTERVAL
UPPER_ONE_SIDED_INTERVAL
BOUNDARY_INCLUDING_INTERVAL
DISCONNECTED_CONFIDENCE_SET
PROFILE_FAILED
```

## 16. Optimization Requirements

For every fixed `n` in a future implementation: optimize all nuisance parameters permitted by the model; use deterministic initialization rules; record convergence and boundary solutions; use multiple starts only if preregistered; do not keep only the most favorable run without recording all starts; verify the profile maximum is not worse because of optimizer failure; preserve the seed and configuration. These are specification requirements for future implementation, not code delivered here.

## 17. Recovery Metrics

Future gate families for `n` (record as required, not implemented, only applicable ones affect M2): (1) absolute bias of `n`; (2) RMSE of `n`; (3) empirical coverage of the profile-likelihood interval; (4) median/distribution of interval width; (5) profile optimization failure rate; (6) boundary-including interval rate; (7) one-sided interval rate; (8) false-positive excitation under exact null, after NUM-DEC-03; (9) false-negative rate or power under positive `n`; (10) source-removal stability; (11) episode-removal stability.

Allowed metric formulas:

```
Bias_hat(n) = (1/R_metric) * sum over r in metric-bearing replications of (n_hat_r - n_true)
RMSE_hat(n) = sqrt[ (1/R_metric) * sum over r of (n_hat_r - n_true)^2 ]
Coverage_hat(n) = (1/R_metric) * sum over r of I[n_true in CI_PL_r]
MeanWidth = (1/R_width) * sum over r of (U_r - L_r)   [only when finite and connected]
```

No ordinary width is computed for disconnected confidence sets without a separately defined rule.

## 18. Monte Carlo Uncertainty

```
MCSE(Coverage_hat) = sqrt[ Coverage_hat * (1 - Coverage_hat) / R_metric ]
```

using the **actual** metric-bearing denominator — never defaulting to 1,000 when fewer than 1,000 intervals are valid. This is consistent with, and directly reuses, the `R_effective` rule fixed by NUM-DEC-01 §14.

## 19. Coverage Target

The existing frozen target is preserved unless a later versioned gate decision changes it:

```
0.925 <= Coverage_hat <= 0.975
```

NUM-DEC-02 does not alter this threshold (`GATE-021-V2` `threshold: between 0.925 and 0.975`). It selects only the method used to construct and validate uncertainty for `n`.

## 20. Observation-Regime Validation

A future profile-likelihood method may be accepted only if synthetic coverage is adequate across mandatory scenarios, including: exact-null/near-null where applicable; weak excitation; moderate excitation; strong-but-stationary excitation; weak beta identification; varying source concentration; varying observation intensity; episode dependence; missing reports; duplicate reports. Validation in only an easy interior scenario is insufficient.

## 21. Relationship to NUM-DEC-01

NUM-DEC-01 (1,000 attempted replications per cell, `R_attempt = R_valid + R_failed + R_invalid`) governs all replication accounting for the parametric-bootstrap validation described in §11 and the Monte Carlo precision rule in §18. NUM-DEC-02 introduces no separate or conflicting accounting convention.

## 22. Relationship to NUM-DEC-03

NUM-DEC-03 governs the exact-null implementation for M2. NUM-DEC-02 does **not** decide: whether exact null uses a separate model; whether a mixture or hurdle representation is used; the boundary distribution of the likelihood-ratio statistic; or the excitation selection rule. Required dependency chain:

```
NUM-DEC-02 (profile likelihood for n)  +  NUM-DEC-03 (exact-null implementation)
    -->  M2 FINAL UNCERTAINTY AND FALSE-POSITIVE CALIBRATION
```

## 23. Separation from M3

`P(M1|Y)` is not reused as the M2 primary uncertainty quantity. M3 is Bayesian model comparison; M2 remains likelihood-based unless separately redesigned. No M3 threshold, prior odds, Bayes-factor method, or ROPE is adopted for M2 by this decision.

## 24. Required Future Tests

Recorded, not executed:

| Test ID | Requirement |
|---|---|
| M2-UNC-001 | Profile likelihood computed over `n`, not separately over `alpha` as the primary estimand. |
| M2-UNC-002 | Nuisance parameters reoptimized at every fixed `n`. |
| M2-UNC-003 | Profile objective reproduces the unconstrained optimum at `n_hat`. |
| M2-UNC-004 | Profile grid includes all prespecified boundary regions. |
| M2-UNC-005 | Profile likelihood invariant to equivalent `alpha = n*beta` reconstruction within numerical tolerance. |
| M2-UNC-006 | One-sided intervals represented explicitly. |
| M2-UNC-007 | Boundary-including intervals represented explicitly. |
| M2-UNC-008 | Disconnected confidence sets detected. |
| M2-UNC-009 | Optimizer failures at profile points recorded. |
| M2-UNC-010 | No failed profile silently replaced. |
| M2-UNC-011 | Parametric-bootstrap coverage uses synthetic data only. |
| M2-UNC-012 | Bootstrap simulation and fitting use the same approved observation regime. |
| M2-UNC-013 | Coverage reports `R_attempt`, `R_valid`, and `R_metric`. |
| M2-UNC-014 | Coverage MCSE reported. |
| M2-UNC-015 | Bias and RMSE use the actual metric-bearing denominator. |
| M2-UNC-016 | Wald interval diagnostic-only. |
| M2-UNC-017 | Profile and Wald disagreement reported. |
| M2-UNC-018 | Exact-null critical value remains unresolved until NUM-DEC-03. |
| M2-UNC-019 | No Bayesian prior introduced into M2. |
| M2-UNC-020 | Historical data not used during uncertainty validation. |

## 25. Implementation Nonauthorization

`implementation_authorized: NO`. No profile-likelihood code, no bootstrap code, and no modification to `m2_mbpp.py` or any harness file is created or executed as part of this adjudication. Everything in §7–§20 is a specification for a future authorized implementation phase.

## 26. Tournament Nonauthorization

`tournament_execution_authorized: NO`. No synthetic recovery run, no bootstrap replication, and no tournament of any scale is executed by this adjudication.

## 27. Historical-Fit Nonauthorization

`historical_fit_authorized: NO`. No historical VOC trade data is fit, referenced numerically, or used to inform this decision. NUM-DEC-02 is a pre-registration/design decision only.

## 28. Decision Summary

| Field | Value |
|---|---|
| Decision ID | NUM-DEC-02 |
| Topic | M2 uncertainty method for n |
| Status | APPROVED_WITH_LIMITATIONS |
| Primary method | PROFILE_LIKELIHOOD_FOR_N |
| Secondary validation | PARAMETRIC_BOOTSTRAP_COVERAGE_VALIDATION |
| Wald status | DIAGNOSTIC_ONLY |
| Bayesian status | NOT_SELECTED_FOR_M2 |
| Boundary status | REQUIRES_NUM_DEC_03 (interior primary; boundary n=0 deferred) |
| Coverage target | 0.925 <= Coverage_hat <= 0.975 (unchanged) |
| Future tests specified | 20 (M2-UNC-001..020), none executed |
| Implementation authorized | NO |
| Tournament execution authorized | NO |
| Historical fit authorized | NO |
| Remaining pending decisions | NUM-DEC-03 through NUM-DEC-08 (6/8) |

---

## Validation

Performed mechanically (python/csv) against the touched files:

- NUM-DEC-01 row diffed field-by-field before/after this task: zero mismatches (byte-identical).
- NUM-DEC-02 is the only newly decided row this turn.
- Ledger status distribution after this decision: 2 `APPROVED_WITH_LIMITATIONS` (NUM-DEC-01, NUM-DEC-02), 6 `PENDING_RESEARCHER_DECISION` (NUM-DEC-03 through NUM-DEC-08).
- Five V2 specification files (`MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md`, `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`, `MODEL_3B_RECOVERY_PROTOCOL_V2.md`, `MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv`) unchanged — the ledger CSV is the one file expected and confirmed to change.
- `MODEL_3B_GATE_V1_TO_V2_RECONCILIATION.csv` unchanged.
- Original `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` unchanged.
- `MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md` unchanged.
- No `.py` implementation file created or modified.
- No bootstrap run; no simulation executed; no historical data referenced.
- Secret scan on the two touched/created files: clean.
- `git status`: nothing staged.

**Final status: `MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATED`**
