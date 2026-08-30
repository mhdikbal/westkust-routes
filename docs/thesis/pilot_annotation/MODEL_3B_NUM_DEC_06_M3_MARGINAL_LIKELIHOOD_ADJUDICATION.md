# NUM-DEC-06 Adjudication: M3 Marginal-Likelihood and Bayes-Factor Computation Method

> **Design/decision only. No bridge sampler implemented. No thermodynamic integration implemented. No marginal likelihood calculated. No Bayes factor calculated. No threshold calibrated. No simulation run. No historical data fitted. Nothing staged, committed, pushed, or deployed.**

---

## 1. Scope

This document adjudicates **NUM-DEC-06 only**: the method M3 will use to compute marginal likelihoods `p(Y|M0)`, `p(Y|M1)`, and the Bayes factor `BF_10`, once implemented. `NUM-DEC-04` (threshold tau), `NUM-DEC-07` (ROPE), and `NUM-DEC-08` (resource ceiling) remain `PENDING_RESEARCHER_DECISION` and are not addressed here. No implementation, marginal-likelihood execution, threshold calibration, tournament rerun, or historical-data fitting is authorized by this decision.

## 2. Authoritative Evidence

```text
MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md
MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv
MODEL_3B_RECOVERY_PROTOCOL_V2.md
MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv
MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv                        (8-row ledger; NUM-DEC-01/02/03/05 APPROVED_WITH_LIMITATIONS prior to this turn)
MODEL_3B_NUM_DEC_05_M3_PRIOR_MODEL_ODDS_ADJUDICATION.md           (P(M0)=P(M1)=0.50 primary + 3-scenario sensitivity grid)
MODEL_3B_AMENDMENT_04_M3_EXACT_NULL_ADJUDICATION.md
MODEL_3B_AMENDMENT_05_M3_DECISION_RULE_ADJUDICATION.md
MODEL_3B_M3_NULL_BOUNDARY_AUDIT.md
docs/thesis/colab/model3b_tournament_harness/m3_bayesian_discrete.py   (actual M3 source -- read in full for the compatibility audit, S5)
docs/thesis/colab/model3b_tournament_harness/run_recovery_m3.py
docs/thesis/colab/model3b_tournament_harness/m3_smoke_test.py
docs/thesis/colab/model3b_tournament_harness/recovery_results/{m3_summary.csv, m3_raw_replicates.csv, m3_run.log}   (read-only, pilot context; not authorization to rerun)
```

Baseline confirmed before this turn: 70/70 original gates reconciled to 51 V2 gates; NUM-DEC-01 = `APPROVED_WITH_LIMITATIONS` (1,000 attempted replications/cell); NUM-DEC-02 = `APPROVED_WITH_LIMITATIONS` (profile likelihood for M2's `n`); NUM-DEC-03 = `APPROVED_WITH_LIMITATIONS`, completeness-corrected (30 sections/30 tests, M2 exact-null); NUM-DEC-05 = `APPROVED_WITH_LIMITATIONS` (M3 prior model odds, equal primary + 3-scenario sensitivity grid); NUM-DEC-04/06/07/08 = `PENDING_RESEARCHER_DECISION`.

## 3. Mathematical Question

NUM-DEC-05 fixed the prior model odds `P(M0)`, `P(M1)`. The posterior model probability `P(M1|Y)` also requires the **evidence ratio** `BF_10(Y) = p(Y|M1)/p(Y|M0)`. The question NUM-DEC-06 resolves: **by what method are `p(Y|M0)` and `p(Y|M1)` computed, and what is the primary model-comparison quantity reported to NUM-DEC-04's future threshold calibration?**

## 4. Candidate Methods

```text
SELECTED (primary):       BRIDGE_SAMPLING
SELECTED (secondary):     THERMODYNAMIC_INTEGRATION (validation subset only)
REJECTED:                 HARMONIC_MEAN_ESTIMATOR
NOT SELECTED AS PRIMARY:  SAVAGE_DICKEY_DENSITY_RATIO
NOT MARGINAL-LIKELIHOOD SUBSTITUTES: BIC, WAIC, PSIS-LOO, DIC
NOT CONSIDERED (not in the ledger's original option set, not adjudicated here): importance sampling, reversible-jump MCMC
```

Full rationale for each rejection/non-selection: Sections 21-23.

## 5. Compatibility Audit

The actual M3 source, `docs/thesis/colab/model3b_tournament_harness/m3_bayesian_discrete.py` (286 lines), was read in full before recording this decision, per the mandatory pre-adjudication compatibility check.

**What exists:**

```text
- A single model class: log_posterior(theta0, theta1, n_branch, beta, counts, year_covariates_ordered)
  (line 148), combining log_prior() (line 133) and loglik_m3() (line 114). n_branch ranges
  continuously over [0,1) via a logit reparameterization in the sampler -- there is NO separate
  n=0 (M0) model anywhere in this file.
- fit_m3_mcmc() (lines 168-219): a hand-rolled random-walk Metropolis-Hastings sampler on the
  unconstrained reparameterization (theta0, theta1, logit(n), log(beta)), producing posterior
  draws and an acceptance-rate diagnostic ("ok" if 0.05<rate<0.95, else "degenerate").
- log_posterior() already returns a pointwise UNNORMALIZED log posterior (log-prior + log-
  likelihood) -- structurally the correct input type for bridge sampling's numerator/denominator
  expectations, once the blockers below are fixed.
- log_prior() (lines 133-145): theta0 ~ N(0,2^2), theta1 ~ N(0,1), n ~ Beta(2,2), beta ~ Gamma(2,1)
  -- explicit, but see Blocker 2.
- pointwise_loglik_m3() and waic() (lines 123-131, 222-230): existing WAIC computation, confirming
  the codebase already has one predictive-diagnostic pathway (correctly kept out of the marginal-
  likelihood role, S23).
```

**Concrete blockers found (verified directly against the code, not assumed):**

```text
BLOCKER 1 -- No M0 (null) model exists.
  There is exactly one model in this file. n_branch=0 is reachable only as a limit of the
  continuous [0,1) parameterization via `_to_unconstrained()` (line 156-158), which explicitly
  CLAMPS n to [_EPS, 1-_EPS] before taking logit(n/(1-n)) -- n=0 exactly is structurally
  unreachable, the same defect the mathematical specification (S16) already documents for M3's
  prior implementation and that NUM-DEC-03 separately resolved for M2. A genuinely separate
  M0 model (fixed n=0, only psi_0 nuisance parameters, its own log_posterior_m0()) does not
  exist and must be built from scratch.

BLOCKER 2 -- log_prior() omits normalizing constants (kernel-only).
  Line 141: `lp += -0.5 * (theta0**2) / 4.0` -- the Normal(0,2^2) KERNEL only; the constant
  `-0.5*log(2*pi*4)` is omitted. Line 142: same pattern for theta1 ~ N(0,1) (constant
  `-0.5*log(2*pi)` omitted). Line 143: Beta(2,2) kernel `(2-1)*log(n)+(2-1)*log(1-n)`, omitting
  `-log(Beta(2,2))` (the Beta-function normalizing constant). Line 144: Gamma(2,1) kernel
  `(2-1)*log(beta)-beta`, omitting `-log(Gamma(2))`. Within a SINGLE model these missing
  constants are irrelevant (they cancel in MCMC acceptance ratios and in WAIC). They are NOT
  irrelevant for marginal-likelihood/bridge-sampling comparison ACROSS models of different
  dimension (M0 lacks the n and beta terms entirely) -- an unnormalized prior would bias
  log_BF_10 by exactly the omitted constants' difference. This directly triggers the Prior
  Normalization Requirement (S13): BRIDGE_SAMPLING_NOT_VALID_FOR_MODEL_COMPARISON until fixed.

BLOCKER 3 -- fit_m3_mcmc lacks the change-of-variables Jacobian correction.
  The sampler proposes in UNCONSTRAINED space (`proposal = u + rng.normal(...)`, line 197,
  a symmetric random walk on (theta0, theta1, logit(n), log(beta))) but evaluates the Metropolis
  acceptance ratio using `log_posterior(theta0_p, theta1_p, n_p, beta_p, ...)` (line 199) --
  i.e. the log-posterior EVALUATED IN CONSTRAINED COORDINATES, with no `+log|d(n,beta)/d(logit(n),
  log(beta))|` Jacobian term added anywhere in the file. For a symmetric proposal on unconstrained
  coordinates to target the correct posterior, the accepted density must be the UNCONSTRAINED
  density (constrained density x Jacobian), not the constrained density alone. This is a
  correctness defect in the EXISTING single-model sampler, independent of the M0/M1 split --
  posterior draws from this sampler, if trusted as-is, are systematically biased, and any
  bridge-sampling estimate built on top of them would inherit that bias.

BLOCKER 4 -- No bridge-sampling, proposal-density, or thermodynamic-integration code exists.
  Confirmed by grep across run_recovery_m3.py and m3_smoke_test.py: zero matches for
  "bridge", "thermodynamic", or "marginal". This is expected greenfield work, not a defect.

BLOCKER 5 -- No multi-chain / R-hat convergence diagnostics.
  The module's own docstring (lines 180-184) states this explicitly: "the pre-registered
  recovery study would use far more draws and multiple chains with R-hat convergence
  diagnostics -- neither is implemented here". Confirmed absent from fit_m3_mcmc().
```

**Classification: `FEASIBLE_WITH_IMPLEMENTATION_WORK`.**

None of the five blockers are architectural dead ends. `log_posterior()`'s structure (already the correct unnormalized-log-posterior *shape* bridge sampling needs) is directly extensible, matching the module's own stated design intent ("if a future turn authorizes installing PyMC/numpyro, this module's `log_posterior` function is directly reusable"). The classification is therefore `FEASIBLE_WITH_IMPLEMENTATION_WORK`, not `NOT_FEASIBLE_WITH_CURRENT_ARCHITECTURE` — but **operational selection of bridge sampling is contingent on resolving Blockers 1-3 first**, and this is recorded explicitly in the ledger (`compatibility_classification` field) rather than left implicit.

## 6. Null and Excitation Models

```text
M0 (null):        n = 0
M1 (excitation):  0 < n < 1
```

Consistent with NUM-DEC-03's M2 exact-null representation and the M3 exact-null defect noted in `MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md` S16. `M0` and `M1` may have different parameter dimensions (Section 11).

## 7. Marginal-Likelihood Definition

```text
p(Y | M_j) = integral over Theta_j of  p(Y | theta_j, M_j) * p(theta_j | M_j)  d theta_j
log_m_j    = log p(Y | M_j)
```

## 8. Bayes-Factor Definition

```text
BF_10     = p(Y | M1) / p(Y | M0)
log_BF_10 = log_m_1 - log_m_0                    (stable numerical form)
```

`BF_10` must **not** be computed by exponentiating `log_BF_10` unless the value lies inside a declared numerically safe range.

```text
P(M1 | Y) = [ BF_10 * P(M1) ] / [ BF_10 * P(M1) + P(M0) ]
logit[P(M1 | Y)] = log_BF_10 + log[ P(M1) / P(M0) ]        (preferred, numerically stable form)
```

## 9. Researcher Decision

```text
NUM-DEC-06:                            APPROVED_WITH_LIMITATIONS  (compatibility-contingent, S5)
CANDIDATE:                             M3 Bayesian discrete-time Hawkes
PRIMARY MARGINAL-LIKELIHOOD METHOD:    BRIDGE_SAMPLING
SECONDARY VALIDATION METHOD:           THERMODYNAMIC_INTEGRATION (prespecified validation subset only)
PRIMARY MODEL-COMPARISON QUANTITY:     log_BF_10 = log_m_1 - log_m_0
HARMONIC-MEAN ESTIMATOR:               REJECTED
SAVAGE-DICKEY RATIO:                   NOT_APPLICABLE_AS_PRIMARY_METHOD
BIC / WAIC / LOO:                      NOT_MARGINAL_LIKELIHOOD_SUBSTITUTES
BAYES-FACTOR EVIDENCE LABELS:          NOT_SELECTED
IMPLEMENTATION:                        NOT_AUTHORIZED
MARGINAL-LIKELIHOOD COMPUTATION:       NOT_AUTHORIZED
THRESHOLD CALIBRATION:                 NOT_AUTHORIZED
TOURNAMENT:                            NOT_AUTHORIZED
HISTORICAL FIT:                        NOT_AUTHORIZED
```

## 10. Bridge-Sampling Method

```text
p(Y | M) = E_q[ p(Y,theta|M) h(theta) ]  /  E_{p(theta|Y,M)}[ q(theta) h(theta) ]
```

with `h(theta)` the bridge function and `q(theta)` a proposal density. Bridge sampling must estimate `log p(Y|M0)` and `log p(Y|M1)` **separately**. Required inputs for each model: posterior draws; unnormalized log posterior; normalized prior density; likelihood; parameter-transform Jacobian; proposal density; parameter names and order; model version; data version; seed manifest. The implementation must **not** use `M1` posterior draws to estimate `M0` evidence or vice versa unless a mathematically valid bridge construction is explicitly documented.

## 11. Separate Parameter Spaces

```text
M0:  n = 0        -- no excitation-magnitude parameter estimated
M1:  0 < n < 1    -- includes excitation magnitude and any conditional kernel parameters
```

`M0` and `M1` may have different parameter dimensions. Bridge sampling must respect each model's **actual** parameter space. Do **not** pad `M0` with a fake epsilon-valued excitation parameter merely to force equal dimensions (this is also rejected explicitly as option `M2-NULL-C`-equivalent behavior for M2, and the analogous mistake is prohibited here for M3).

## 12. Parameter Transformations and Jacobians

For constrained parameters, every transform must be documented, e.g.:

```text
Positive parameter:      theta = exp(eta)                Jacobian: log|d theta/d eta| = eta
Unit-interval parameter: n = expit(eta)                   Jacobian: log|dn/deta| = log n + log(1-n)
```

The exact-null model must **not** represent `n=0` through a finite logit transformation — the excitation-model transform applies only under `M1`; the null model remains a separate exact-null model. Do not omit Jacobian terms from marginal-likelihood calculations. **This is currently violated** by the existing `fit_m3_mcmc` sampler (Blocker 3, S5) — future implementation work under this decision must add the missing Jacobian correction before any bridge-sampling estimate can be trusted.

## 13. Prior Normalization

Marginal likelihood is sensitive to complete prior normalization. Every prior must have: explicit density; normalization constant; support; parameterization; version; source or rationale. Improper priors are **prohibited** for marginal-likelihood comparison. If any model parameter uses an improper prior:

```text
BRIDGE_SAMPLING_NOT_VALID_FOR_MODEL_COMPARISON
```

and implementation must stop. Do not silently replace an improper prior during computation. **This requirement is currently unmet** by the existing `log_prior()` (Blocker 2, S5) — its Normal/Beta/Gamma components are kernel-only, missing normalizing constants that would otherwise cancel within one model but bias `log_BF_10` across `M0` vs `M1`'s differing dimensionality.

## 14. Internal Parameter Priors

`NUM-DEC-05` selected model prior odds only. `NUM-DEC-06` does **not** select internal priors for: `n`; lag decay (`beta`); baseline coefficients (`theta0`, `theta1`); dispersion; CD effects; observation-process parameters; episode parameters. Before bridge sampling can be implemented, all internal parameter priors must be proper, versioned, and subjected to prior-predictive checks.

```text
M3_INTERNAL_PARAMETER_PRIORS: REQUIRE_VERSIONED_IMPLEMENTATION_REVIEW
```

## 15. Posterior-Sampling Preconditions

Bridge sampling may proceed only when posterior sampling under both models passes: convergence diagnostics; effective sample-size diagnostics; finite log-density checks; multiple-chain comparison; initialization diagnostics; no unresolved divergence or equivalent sampler pathology; stable parameter transformations; posterior-support coverage. Do not calculate marginal likelihood from an invalid posterior run.

```text
Required status if diagnostics fail: MARGINAL_LIKELIHOOD_NOT_COMPUTABLE_FROM_INVALID_POSTERIOR
```

The existing `fit_m3_mcmc` provides only a single-chain acceptance-rate diagnostic ("ok"/"degenerate") — multi-chain/R-hat diagnostics (Blocker 5, S5) do not yet exist and are required future implementation work.

## 16. Bridge Replication

Each marginal-likelihood estimate must be repeated independently. Minimum future design: at least 3 independent bridge estimates per model; independently seeded posterior draws or valid nonoverlapping posterior subsets; repeated proposal fitting; log marginal-likelihood variance or range reported. The exact number of posterior draws is **not** selected in this adjudication.

```text
BRIDGE_POSTERIOR_DRAW_COUNT: REQUIRES_PREIMPLEMENTATION_RESOURCE_REVIEW
```

Future execution must report: `log_m0` estimates; `log_m1` estimates; `log_BF_10` estimates; repeated-estimate mean; standard deviation; range; convergence/percentage-error diagnostic where supported; failed estimates.

## 17. Bridge Stability

Do not accept one bridge estimate without stability assessment. Required comparisons: repeated seeds; alternative proposal initialization; posterior sample-split agreement; transformed-parameter versus equivalent validated implementation where feasible; bridge-estimation diagnostics. A bridge result is **unstable** if repeated estimates produce substantively different posterior model decisions under the same prior odds and tau. The exact numerical stability tolerance remains:

```text
REQUIRES_PREIMPLEMENTATION_DECISION
```

Do not invent a tolerance here.

## 18. Thermodynamic Integration

Approved only as a **secondary validation** method. Let `beta_temp` be an inverse-temperature parameter, `0 <= beta_temp <= 1`, with power posterior `p_beta(theta|Y,M) proportional to p(Y|theta,M)^beta_temp * p(theta|M)`. Then:

```text
log p(Y | M) = integral from 0 to 1 of  E_beta[ log p(Y | theta, M) ]  d beta_temp
```

Future implementation must specify: temperature ladder; integration rule; number of draws per temperature; warmup; convergence; discretization error; replicate stability; computational cost. No temperature ladder is selected here. No thermodynamic-integration run is authorized here.

## 19. Validation Subset

Thermodynamic integration need not automatically run for every tournament replication. It may be used on a prespecified validation subset that includes: exact-null scenarios; weak excitation; moderate excitation; strong stationary excitation; baseline-confounding scenario; CD-2 observation-process scenario; episode-dependence scenario. The subset must be selected **before** seeing bridge-sampling results. Do not select only cases where bridge sampling appears favorable.

## 20. Method Agreement

A future report must compare `log_m0_bridge` vs `log_m0_TI`; `log_m1_bridge` vs `log_m1_TI`; `log_BF_10_bridge` vs `log_BF_10_TI`. The exact acceptable discrepancy is not selected in this adjudication:

```text
BRIDGE_TI_AGREEMENT_TOLERANCE: REQUIRES_PREIMPLEMENTATION_DECISION
```

If disagreement is material: `MODEL_COMPARISON_NUMERICALLY_UNRESOLVED`. Do not select whichever method favors excitation.

## 21. Rejected Harmonic-Mean Estimator

```text
HARMONIC-MEAN ESTIMATOR: REJECTED
```

Reason: unstable; potentially infinite variance; dominated by low-likelihood regions; inadequate for authoritative model comparison.

## 22. Savage-Dickey Status

```text
SAVAGE-DICKEY DENSITY RATIO: NOT_SELECTED_AS_PRIMARY
```

Reason: the exact null is represented as a separate model (per NUM-DEC-03's M2-analogous design and this document's S6), not a point-null density ratio within one continuous parameterization; parameter spaces differ between `M0` and `M1`; required prior nesting and compatibility conditions must not be assumed; the boundary null complicates direct use; there is no need to force the comparison into a point-null density-ratio identity when an explicit nested-model likelihood-ratio/bridge-sampling design is already adopted.

## 23. Information-Criterion Status

```text
BIC:       NOT_A_MARGINAL_LIKELIHOOD_ESTIMATOR_FOR_THIS_DECISION
WAIC:      PREDICTIVE_DIAGNOSTIC_ONLY
PSIS-LOO:  PREDICTIVE_DIAGNOSTIC_ONLY
DIC:       NOT_SELECTED
```

Information criteria may provide supplementary predictive diagnostics (the existing `waic()` function in `m3_bayesian_discrete.py`, S5, is confirmed to already occupy exactly this diagnostic role) but must not be substituted for the selected marginal-likelihood method.

## 24. Bayes-Factor Evidence Labels

Do not adopt universal verbal categories such as "anecdotal", "moderate", "strong", "decisive" based solely on fixed BF thresholds. Bayes factor is a **secondary** evidence quantity. The primary future decision remains `P(M1|Y)`, with tau selected under `NUM-DEC-04` through synthetic calibration. No BF evidence-level threshold is selected here.

## 25. Relationship to NUM-DEC-05

`NUM-DEC-05` selected `P(M0)=0.50, P(M1)=0.50` as the primary synthetic-calibration model odds, with mandatory sensitivity `0.75/0.25`, `0.50/0.50`, `0.25/0.75`. `NUM-DEC-06` supplies `log_BF_10`. The posterior model probability must be recalculated under all three prior odds using the **same** `log_BF_10`. Do not rerun the model-comparison computation merely to change model prior odds when the within-model priors and likelihoods are unchanged.

## 26. Relationship to NUM-DEC-04

`NUM-DEC-04` remains pending. `NUM-DEC-04` may calibrate tau only after: exact-null and excitation models are implemented; internal parameter priors are frozen; bridge sampling is validated; thermodynamic-integration cross-check is satisfactory; prior odds are frozen; calibration and evaluation seed sets are frozen. `NUM-DEC-06` does not select tau.

## 27. Relationship to NUM-DEC-07

`NUM-DEC-07` remains pending. ROPE concerns magnitude conditional on `M1`. Bridge sampling determines relative evidence for model existence. Do not use ROPE probability as a marginal-likelihood substitute.

## 28. Prior Sensitivity

Marginal likelihood is sensitive to prior scale. A future implementation must report sensitivity to all versioned reasonable internal parameter-prior choices. Do not tune internal priors until the Bayes factor favors a desired model. Prior variants must be specified before final evaluation. If posterior model decisions change materially across reasonable proper priors, classify:

```text
M3_MODEL_COMPARISON_PRIOR_SENSITIVE
```

not `EXCITATION_SUPPORTED`.

## 29. Synthetic Calibration

Bridge sampling and thermodynamic integration must be calibrated on synthetic data where the generating model is known. Required generating cases: exact `M0` null; `M1` weak excitation; `M1` moderate excitation; `M1` strong but stationary excitation; baseline variation without excitation; CD-2 observation variation; episode dependence without excitation; missing reporting; duplicate reporting; overdispersion. Evaluate: finite evidence estimates; correct directional evidence; stability across seeds; prior sensitivity; misclassification rate; effect on `P(M1|Y)`; computational failure rate. No historical data may enter method selection.

## 30. Numerical Stability

All evidence calculations must operate on the log scale.

```text
log_posterior_odds = log_BF_10 + log_prior_odds
```

then use a numerically stable logistic transform. Do not calculate `exp(log_BF_10)` when avoidable. Required guards: log-sum-exp; finite-value checks; overflow detection; underflow detection; NaN rejection; positive and normalized probabilities.

## 31. Failure Statuses

Every M3 comparison must support:

```text
VALID
POSTERIOR_INVALID
BRIDGE_FAILED
BRIDGE_UNSTABLE
THERMODYNAMIC_INTEGRATION_FAILED
METHOD_DISAGREEMENT
PRIOR_SENSITIVE
NOT_COMPUTED
```

Do not replace failure statuses with a numerical zero.

## 32. Failed-Run Accounting

Any marginal-likelihood failure remains a recorded outcome. Do not: silently rerun with a favorable seed; omit failed model comparisons; keep only successful bridges; replace invalid evidence with BIC; downgrade failures to warnings automatically. All attempted and valid denominators must be reported.

## 33. Resource Dependency

Thermodynamic integration may be computationally expensive. `NUM-DEC-08` will govern the operational resource ceiling. `NUM-DEC-06` approves the method hierarchy, not unlimited computation. If thermodynamic integration is infeasible under the approved resource ceiling, return:

```text
SECONDARY_VALIDATION_RESOURCE_BLOCKED
```

Do not silently eliminate the secondary validation requirement.

## 34. Required Future Tests

Record but do not execute:

```text
M3-ML-001: M0 unnormalized log posterior is finite for valid draws.
M3-ML-002: M1 unnormalized log posterior is finite for valid draws.
M3-ML-003: All priors used in marginal likelihood are proper.
M3-ML-004: Prior normalization constants are included.
M3-ML-005: Parameter-transform Jacobians are included.
M3-ML-006: M0 exact null does not use epsilon excitation.
M3-ML-007: M1 supports 0 < n < 1.
M3-ML-008: Posterior sampling diagnostics pass before bridge sampling.
M3-ML-009: Bridge sampling estimates log p(Y|M0).
M3-ML-010: Bridge sampling estimates log p(Y|M1).
M3-ML-011: log_BF_10 equals log_m1 minus log_m0.
M3-ML-012: Equal prior odds make posterior odds equal BF_10.
M3-ML-013: Posterior probabilities sum to one.
M3-ML-014: All calculations remain on the log scale where possible.
M3-ML-015: Repeated bridge estimates are recorded.
M3-ML-016: Posterior sample-split stability is checked.
M3-ML-017: Proposal sensitivity is checked.
M3-ML-018: Bridge failures are not silently replaced.
M3-ML-019: Thermodynamic integration computes log p(Y|M0) on the validation subset.
M3-ML-020: Thermodynamic integration computes log p(Y|M1) on the validation subset.
M3-ML-021: Bridge and TI log marginal likelihoods are compared.
M3-ML-022: Material method disagreement blocks model comparison.
M3-ML-023: Harmonic-mean estimator is not used.
M3-ML-024: Savage-Dickey is not assumed valid.
M3-ML-025: BIC is not substituted for marginal likelihood.
M3-ML-026: WAIC and PSIS-LOO remain predictive diagnostics only.
M3-ML-027: Prior model odds remain separate from internal parameter priors.
M3-ML-028: All three prior-odds sensitivity scenarios are reported.
M3-ML-029: Prior-scale sensitivity is reported.
M3-ML-030: Exact-null synthetic scenarios do not systematically favor M1.
M3-ML-031: Positive-excitation scenarios show directional evidence where recoverable.
M3-ML-032: Baseline variation without excitation is tested.
M3-ML-033: CD-2 observation-process variation is tested.
M3-ML-034: Episode dependence without excitation is tested.
M3-ML-035: Missing and duplicate reporting scenarios are tested.
M3-ML-036: Failed comparisons remain in attempted-run accounting.
M3-ML-037: No Bayes-factor verbal threshold is applied automatically.
M3-ML-038: No historical data enter method calibration.
M3-ML-039: Repeated execution is deterministic under the same seed manifest.
M3-ML-040: Raw evidence outputs and summaries reconcile.
```

Total required future tests: **40** (`M3-ML-001`–`040`), 40 unique IDs, no duplicates, no gaps. Additionally required by the compatibility audit (S5), to be folded into the implementation wave that resolves Blockers 1-3: an M0 model/fitting routine must exist and pass `M3-ML-001`/`006`; `log_prior()` must include normalizing constants before `M3-ML-003`/`004` can pass; `fit_m3_mcmc` must add the Jacobian correction before `M3-ML-005` or any posterior-dependent test can be trusted.

## 35. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```

No M3 source file (`m3_bayesian_discrete.py` or any other) is modified or created by this adjudication. No M0 model, no bridge sampler, no thermodynamic-integration routine, and no Jacobian-correction fix is written.

## 36. Marginal-Likelihood Execution Nonauthorization

```text
MARGINAL-LIKELIHOOD EXECUTION: NOT_AUTHORIZED
```

No `log p(Y|M0)`, `log p(Y|M1)`, or `log_BF_10` value is computed as part of producing this adjudication.

## 37. Threshold-Calibration Nonauthorization

```text
THRESHOLD CALIBRATION: NOT_AUTHORIZED
```

No value of tau is selected, computed, or implied by this adjudication. Tau remains governed exclusively by the future `NUM-DEC-04`.

## 38. Tournament Nonauthorization

```text
TOURNAMENT EXECUTION: NOT_AUTHORIZED
```

No synthetic recovery execution, calibration run, or evaluation run occurs as part of producing this adjudication.

## 39. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```

No historical data file is read, written, or referenced by this adjudication.

## 40. Decision Summary

```text
NUM-DEC-06:                     APPROVED_WITH_LIMITATIONS (compatibility-contingent)
Compatibility classification:   FEASIBLE_WITH_IMPLEMENTATION_WORK (5 blockers identified, S5)
Selected primary method:        BRIDGE_SAMPLING
Selected secondary method:      THERMODYNAMIC_INTEGRATION (prespecified validation subset)
Primary comparison quantity:    log_BF_10 = log_m_1 - log_m_0
Null / excitation models:       M0: n=0  /  M1: 0<n<1
Rejected primary method:        HARMONIC_MEAN_ESTIMATOR
Not selected as primary:        SAVAGE_DICKEY_DENSITY_RATIO
Not ML substitutes:             BIC, WAIC, PSIS-LOO, DIC
BF verbal-evidence labels:      NOT_SELECTED
Blockers to operational use:    (1) no M0 model exists; (2) log_prior() lacks normalizing
                                 constants; (3) fit_m3_mcmc lacks Jacobian correction for its
                                 unconstrained-space proposal -- all three are prerequisites for
                                 valid bridge-sampling comparison, not yet resolved
Relationship to NUM-DEC-05:     posterior P(M1|Y) recomputed under all 3 prior-odds scenarios
                                 from the same log_BF_10
Relationship to NUM-DEC-04:     tau calibration blocked until this method is implemented and
                                 validated, priors frozen, and TI cross-check is satisfactory
Relationship to NUM-DEC-07:     ROPE is a separate, non-substitutable magnitude question
Required future tests:          40 (M3-ML-001..040)
Implementation authorized:      NO
Marginal-likelihood execution authorized: NO
Threshold calibration authorized: NO
Tournament execution authorized: NO
Historical fit authorized:      NO
Remaining pending:              NUM-DEC-04, NUM-DEC-07, NUM-DEC-08
```

```text
MODEL_3B_NUM_DEC_06_M3_MARGINAL_LIKELIHOOD_ADJUDICATED
```
