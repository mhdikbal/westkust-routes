# Model 3B Mathematical Specification V2

> **Design and specification only. No M0/M2/M3 source code modified. No estimator implemented. No synthetic tournament executed. No threshold, prior-odds, or uncertainty method selected. No historical data fitted. Original gate specification and protocol not overwritten. Nothing staged, committed, pushed, or deployed.**

---

## 1. Scope

This document is the versioned mathematical specification (V2) for the amended Model 3B recovery-tournament candidate set, constructed after all seven amendment proposals (`PROPOSAL-01` through `PROPOSAL-07`) were adjudicated and the complete amendment milestone was pushed and server-synced at commit `da8c04d70f6ba107a14822fbd6da547f2f7f395d`. It consolidates the equations, parameter spaces, estimands, applicability rules, and open numerical decisions that a future implementation turn must use. It authorizes nothing beyond specification: no model correction, no estimator code, no simulation, no threshold calibration, no prior-odds selection, no historical-data fitting, and no replacement of the original 70-row gate specification.

## 2. Authoritative Baselines

```text
Complete amendment milestone commit:  da8c04d70f6ba107a14822fbd6da547f2f7f395d
Status:                                MODEL_3B_COMPLETE_AMENDMENT_ADJUDICATION_PUSHED_AND_SERVER_SYNCED
Pilot diagnostic audit commit:         4b94cd689c995765102b4ca4c63e2636334432bb
Status:                                MODEL_3B_PILOT_DIAGNOSTIC_AUDIT_PUSHED_AND_SERVER_SYNCED
Tournament verdict:                    NOT_AVAILABLE
Historical-data fitting:               NOT_AUTHORIZED
Original gate specification checksum:  d4d4d3f5215c2b76fffe0cd40bc59a6ffc78eded93db3188eb598aae468df22b
  (docs/thesis/pilot_annotation/MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv, 70 rows, UNCHANGED)
Amendment ledger status:               7/7 ADJUDICATED, 0 IMPLEMENTED, 0 RERUN AUTHORIZED, 0 HISTORICAL FIT AUTHORIZED
Consistency-audit verdict:             CONSISTENT_WITH_NONBLOCKING_CLARIFICATIONS
```

Read in full for this specification: `MODEL_3B_AMENDMENT_DECISION_LEDGER.csv`; `MODEL_3B_AMENDMENT_01` through `07` adjudication documents; `MODEL_3B_COMPLETE_AMENDMENT_CONSISTENCY_AUDIT.md`; `MODEL_3B_AMENDMENT_DEPENDENCY_MATRIX.csv`; `MODEL_3B_FUTURE_GATE_APPLICABILITY_MATRIX.csv`; `MODEL_3B_AMENDMENT_TEST_INVENTORY.csv`; `MODEL_3B_AMENDMENT_IMPLEMENTATION_WAVES.md`; `MODEL_3B_PILOT_RECOVERY_DIAGNOSTIC_AUDIT.md`; `MODEL_3B_M0_INTERVAL_COVERAGE_AUDIT.md`; `MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md`; `MODEL_3B_M3_NULL_BOUNDARY_AUDIT.md`; `MODEL_3B_GATE_AMENDMENT_PROPOSAL.md`; `MODEL_3B_PILOT_GATE_CLASSIFICATION.csv`; `MODEL_3B_RECOVERY_TOURNAMENT_DESIGN.md`; `MODEL_3B_OBSERVATION_REGIME_SIMULATION_SPEC.md`; `MODEL_3B_VARIABLE_ROLE_DECISION_MATRIX.csv`; `MODEL_3B_CANDIDATE_IMPLEMENTATION_REVIEW.md`; `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv`; `MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md`; the tournament harness under `docs/thesis/colab/model3b_tournament_harness/`.

Pilot classification distribution (preserved, post-`GATE-036` correction):

```text
VALID_GATE_VALID_FAILURE:           6
VALID_GATE_IMPLEMENTATION_FAILURE:  4
ESTIMAND_MISMATCH:                  3
PROTOCOL_NOT_COMPLETED:            24
NOT_INTERPRETABLE:                  5
TOTAL:                             42
```

## 3. Evidence Precedence

If any two documents conflict, resolve in this order (highest first):

```text
1. raw immutable simulation and recovery outputs
2. source code actually executed (tournament harness)
3. MODEL_3B_AMENDMENT_DECISION_LEDGER.csv (final seven-proposal decisions)
4. the seven adjudication documents (01-07)
5. MODEL_3B_COMPLETE_AMENDMENT_CONSISTENCY_AUDIT.md and its superseding clarifications
6. frozen original gate specification and execution protocol
7. pilot diagnostic audit
8. earlier planning documents
9. terminal summaries
10. this specification's own governing workflow instruction
```

**Superseding clarification, binding on this specification:** `PROPOSAL-06`'s own text states "19 advisory gates" (correcting an originally-proposed "21"). The consistency audit found this 19 itself required one further correction: `GATE-019`/`GATE-020` (M2 branching-ratio bias) are M2-**mandatory**, not advisory, because they carry the `MANDATORY` tag in the frozen gate specification's own `mandatory_advisory_status` column. The authoritative future count is therefore **17**, not 19. Both `PROPOSAL-06`'s original wording and this correction are preserved verbatim in their own documents; this specification uses `17` as the operative number (§27).

## 4. Observation Regime

The historical application uses annual or interval-level observation, never artificial exact-timestamp ordering. Every candidate's simulation generator and estimator must represent the full observation pipeline:

```text
latent event process
  -> source-observation process
  -> annual interval censoring
  -> same-year ties/counts
  -> parent-child episode dependence
  -> missing and duplicate reporting
  -> candidate-specific preprocessing
  -> estimator
  -> recovery metrics
```

No candidate's exact-null, decision-rule, or calibration work (M2 §13, M3 §16, §19) may be validated only under idealized continuous timestamps — this reproduces the root-cause audit's confirmed `RECOVERY_OBSERVATION_REGIME_MISMATCH` defect if skipped.

## 5. Candidate Set

```text
M0: exposure-adjusted Poisson / Negative Binomial baseline
M1: original V1 benchmark only, non-authoritative (MODEL_VALIDATION_FAILURE / INFERENCE_NOT_AUTHORIZED)
M2: interval-censored Hawkes / MBPP-style candidate
M3: Bayesian discrete-time Hawkes with exact-null comparison
M4: EXCLUDED_INSUFFICIENT_PRECISE_SUBSET (12 HIGH-confidence exact-event dates; must not be
    restored by pooling HIGH and MEDIUM dates)
```

This specification's substantive content (§7-22) covers M0, M2, and M3. M1 is addressed only as a benchmark boundary (§24); M4 is addressed only as an exclusion record (§25).

## 6. Applicability Rule

Let `Theta_m` be the parameter space of model `m`, and `q_g(theta)` the estimand a gate `g` evaluates.

```text
A(g,m) = 1  if q_g(theta) is defined on Theta_m
A(g,m) = 0  if q_g(theta) is not defined on Theta_m
```

If `A(g,m)=0`, the gate status is `NOT_APPLICABLE_TO_MODEL_DOMAIN` — never `FAIL`, `NOT_COMPUTED`, or `PROTOCOL_NOT_COMPLETED`. A non-applicable gate must not affect a candidate's PASS/FAIL verdict.

Five distinct states are used throughout this specification and must not be conflated:

```text
ZERO:              parameter exists and equals zero
NOT_APPLICABLE:    parameter or estimand is absent from the model domain
NOT_COMPUTED:      applicable metric exists but was not calculated
FAIL:              applicable metric was validly calculated and failed its gate
NOT_INTERPRETABLE: output exists but cannot support the intended inference
```

---

## 7. M0 Equations

Poisson candidate:

```text
Y_t ~ Poisson(mu_t)
```

Negative Binomial candidate (confirmed convention, source-verified against `run_recovery_m0.py::neg_loglik_nb`/`simulate_nb_counts`):

```text
Y_t ~ NegBin(mu_t, phi)
E[Y_t]   = mu_t
Var(Y_t) = mu_t + mu_t^2 / phi
```

Linear predictor:

```text
log(mu_t) = X_t' * gamma + log(E_t)
```

where `E_t` is the approved exposure definition, not an automatically assumed historical event-intensity covariate.

## 8. M0 Parameter Space and Estimands

```text
Theta_M0 = { gamma, phi },  phi > 0
eta_phi = log(phi)  =>  phi = exp(eta_phi)
```

Applicable estimands: regression coefficients `gamma`; dispersion `phi` (where used); expected interval counts `mu_t`; predictive count distribution; interval coverage; convergence and boundary rates.

Not applicable to `Theta_M0`: `alpha`; `beta`; branching ratio `n`; excitation FPR/FNR; excitation detection power. The following original gates remain outside M0's model domain: `GATE-002`, `GATE-003`, `GATE-005`, `GATE-006`, `GATE-036`.

## 9. M0 Full-Hessian Requirement

Confirmed defect (source-verified, `run_recovery_m0.py::run_cell`): the executed code computes only the diagonal Hessian entries (`f00`, `f11`) and inverts each independently, and excludes `phi`/`log_phi` from the covariance entirely ("`phi` treated nuisance"). For minimized negative log-likelihood, using the complete estimated parameter vector `theta = (gamma_0, gamma_1, ..., eta_phi)`:

```text
Cov_hat(theta_hat) = H_NLL(theta_hat)^-1

H_ij = d^2(NLL) / d(theta_i) d(theta_j)      (all cross-partials required)
```

A diagonal-only Hessian is prohibited. For a transformed parameter `h(theta)`:

```text
Cov[h(theta_hat)] ~= J_h * Cov(theta_hat) * J_h'
```

Diagnostic oracle (fixed-seed, n=60, not a full rerun): full-Hessian coverage 93.3%, inside the frozen target band [92.5%, 97.5%]; original diagonal-only coverage 54.4-61.5%, outside the band (`GATE-007`).

```text
M0_IMPLEMENTATION_CORRECTION_APPROVED
M0_FINAL_PASS_NOT_ESTABLISHED
```

M0 is not implemented in this phase.

---

## 10. M2 Equations

Exponential excitation kernel:

```text
g(u) = alpha * exp(-beta * u),  u > 0
n = integral_0^inf g(u) du = alpha / beta
```

Approved prospective reparameterization (future direction only, not implemented):

```text
alpha = n * beta,   0 <= n < 1,   beta > 0
```

Interval-censored observation model, for interval `I_t = [t, t+1)`:

```text
Lambda_t = integral over I_t of lambda(s | H_s) ds
```

The precise M2 likelihood must be extracted from the existing `m2_mbpp.py` implementation and literature-backed design, then written explicitly in a future implementation review. Not resolved here:

```text
M2_INTERVAL_LIKELIHOOD_EXACT_FORM_REQUIRES_IMPLEMENTATION_REVIEW
```

## 11. M2 Parameter Space and Primary Estimand

M2 as executed is parameterized directly as `(theta0, theta1, alpha, beta)` (source-verified, `m2_mbpp.py::fit_m2` optimizer bounds). Primary estimand for the amended specification:

```text
n = alpha / beta   (integrated excitation mass / branching ratio)
```

Secondary diagnostics: `alpha`; `beta`; decay timescale `1/beta`; objective-profile width; interval-level expected excitation mass; predictive interval counts. `alpha`/`beta` are `DIAGNOSTIC_ONLY`, not primary recovery targets, unless a future design proves separate identifiability. `n` must not be interpreted as a historical causal probability, actor-level behavioral coefficient, evidence of intent, conflict contagion, equilibrium, or an ontology/Graphify factual edge.

## 12. M2 Identifiability Boundary

Objective-ridge evidence, directly evaluated against `neg_ic_ll_density_baseline` on one synthetic dataset (seed `777001`, `S3-equiv`, `n_true=0.6769`):

```text
n fixed, beta varied ~20x (0.2 -> 4.0):     NLL varies ~1.74 units
beta fixed, n varied ~40%:                  NLL varies >500 units
```

```text
M2_ALPHA_BETA_SEPARATION_NOT_IDENTIFIED
M2_INTEGRATED_EXCITATION_ESTIMAND_PREFERRED
```

Favorable identifiability of `n` is necessary but not sufficient for a pass verdict; pilot ran at 150/1,000 replications per cell (§14 dependency).

## 13. M2 Exact-Null Open Decision

M2 must support `H0: n=0` and `H1: 0<n<1`. Exact-null representability for M2's own interval-censored MBPP-likelihood estimator is unresolved and must be checked independently — the M3 solution (§16) does not automatically transfer, since M2's kernel form and estimator differ structurally from M3's discrete-time Bayesian formulation.

```text
M2_EXACT_NULL_REVIEW: SEPARATE_DEPENDENCY (blocking preimplementation decision)
```

## 14. M2 Replication and Uncertainty Open Decisions

Required future scale: 1,000 replications per cell. Current pilot: 150 replications per cell.

```text
MCSE(p_hat) = sqrt( p_hat * (1 - p_hat) / R )
MCSE_150   ~= 0.0178   (at p_hat ~= 0.95)
MCSE_1000  ~= 0.0069   (at p_hat ~= 0.95)
```

Near-threshold pilot branching-ratio bias (0.020-0.054 absolute, vs <=0.050 threshold) is not converted into `FINAL_PASS`/`FINAL_FAILURE` by any adjudicated document. Denominator status:

```text
REPLICATION_DENOMINATOR_REQUIRES_PREIMPLEMENTATION_DECISION
```

Both `ATTEMPTED_REPLICATIONS` and `SUCCESSFULLY_COMPLETED_REPLICATIONS`/`VALID_FOR_METRIC_CALCULATION` counts must be preserved and separately reported; failed optimizations are themselves evidence and must never be silently replaced.

Uncertainty method for `n` is unresolved. Candidates (none selected): profile likelihood; parametric bootstrap; revised likelihood-based interval under `(n, beta)`; Bayesian posterior interval if M2 becomes Bayesian.

---

## 15. M3 Equations

General discrete-time annual count model:

```text
Y_t ~ CountDistribution(Lambda_t)
Lambda_t = mu_t + sum_{k=1}^{K} w_k * Y_{t-k}
n_d = sum_{k=1}^{K} w_k              (integrated discrete excitation)
```

If a normalized lag kernel is used:

```text
w_k = n_d * h_k(beta),   h_k(beta) >= 0,   sum_{k=1}^{K} h_k(beta) = 1
```

The actual implementation must confirm this kernel normalization from source in a future review; it is not assumed to already hold.

## 16. M3 Exact-Null Model

Confirmed from source (`m3_bayesian_discrete.py::_from_unconstrained`, not assumed): `n = expit(logit_n) = 1/(1+exp(-logit_n))`. For every finite `logit_n`, `0 < n < 1` — `n=0` is structurally unreachable. This is the mechanical cause of the pilot's 200/200 (100%) false-positive result at the null cell; it is not evidence of a substantive over-detection tendency.

```text
Null model:  M0^(3): n_d = 0   (equivalently w_1 = ... = w_K = 0)
```

Preferred future design (`M3-NULL-A`): explicit two-model comparison sharing all non-excitation components (baseline, exposure, observation model, overdispersion, covariates, temporal aggregation, source-observation assumptions). Acceptable alternative: hurdle/latent-indicator (`M3-NULL-B`). Conditionally acceptable: spike-and-slab (`M3-NULL-C`), requiring a documented prior and sensitivity analysis. Rejected as an exact-null fix: epsilon clipping, near-zero-as-zero, logit(n)-alone-with-near-zero-declaration (`M3-NULL-D/E/F`).

```text
Current null-test status: M3_CURRENT_NULL_TEST_NOT_INTERPRETABLE
NOT classified as: M3_FINAL_MODEL_FAILURE / GENUINE_100_PERCENT_FALSE_POSITIVE_MODEL_FAILURE
```

Baseline nesting is required (excitation model at `n_d=0` must equal the null model), or `NULL_AND_ALTERNATIVE_NOT_NESTED` must be explicitly recorded.

## 17. M3 Excitation Model

```text
Excitation model: M1^(3): 0 < n_d < 1
```

The excitation-existence decision and excitation-magnitude estimation must remain separate quantities (never conflated into one continuous posterior), per the hurdle-alternative structure (§16) and the conditional-magnitude requirement (§21).

## 18. M3 Posterior Model-Probability Decision

Primary decision quantity:

```text
P(M1^(3) | Y)   equivalently   P(z=1 | Y)
delta_tau(Y) = 1{ P(M1^(3)|Y) >= tau }
```

```text
FPR_hat(tau) = (1/R0) * sum_{r=1}^{R0} 1{ P(M1^(3)|Y_r) >= tau }   (exact-null sims)
FNR_hat(tau) = (1/R1) * sum_{r=1}^{R1} 1{ P(M1^(3)|Y_r) <  tau }   (positive-excitation sims)
```

Necessary calibration target: `FPR_hat(tau) <= 0.05`, evaluated jointly with FNR, power, calibration, and confounding resistance — never in isolation, and never satisfied by a threshold that eliminates all detection power.

The decision architecture must support three outcomes, `INCONCLUSIVE` mandatory and not engineered away:

```text
EXCITATION_SUPPORTED
NO_EXCITATION_SUPPORTED
INCONCLUSIVE
```

## 19. M3 Calibration and Evaluation Separation

```text
CALIBRATION SET: selects tau
EVALUATION SET:  measures final gate performance
```

The same replications must never be used for both threshold selection and final evaluation. No historical data may be used to choose `tau`. Prospective diagnostic grid (not an execution authorization): `tau in {0.50, 0.75, 0.90, 0.95, 0.975, 0.99}`.

## 20. M3 Prior and Threshold Open Decisions

```text
P(M1^(3)|Y) / P(M0^(3)|Y) = BF_10(Y) * [ P(M1^(3)) / P(M0^(3)) ]
```

Unresolved: `P(M0^(3))`; `P(M1^(3))`; exact marginal-likelihood method; Bayes-factor diagnostic levels; `tau`. Equal odds (0.5/0.5) may be evaluated as one candidate only, not adopted. Bayes factor `BF_10 = p(Y|M1)/p(Y|M0)` is approved as a **secondary diagnostic** only, never the sole primary rule; no universal `BF_10>3/>10/>100` categories are assumed without calibration.

## 21. M3 Conditional Magnitude

```text
E[ n_d | Y, M1^(3) ]   and a corresponding credible interval
```

```text
EXACT_NULL -> MODEL_EXISTENCE_DECISION -> CONDITIONAL_MAGNITUDE_ESTIMATION
```

A model-averaged small positive `n_d` must never be reported as proof of excitation existence.

## 22. GATE-031 Prospective Retirement

Original `GATE-031` (`absolute_relative_bias_excitation_params`, M3, MANDATORY) assumed a separate alpha-like amplitude parameter that never existed in either `Theta_M3_old` (pilot) or `Theta_M3_new` (amended). Pilot classification: `ESTIMAND_MISMATCH` (`implementation_valid=TRUE`, `estimand_valid=FALSE`).

```text
GATE-031: RETIRED_PROSPECTIVELY_FOR_M3_V2
```

Applies only to a future amended M3 V2 specification; does not apply to M0, M2, or the frozen pilot record; does not delete, invalidate, or auto-pass anything. Replacement mapping (`M3-REPL-031-A` through `E`), covering the gate's original scientific purpose exactly:

```text
M3-REPL-031-A: exact-null representability (Proposal 4)
M3-REPL-031-B: posterior model-probability calibration (Proposal 5)
M3-REPL-031-C: false-positive rate under exact null (Proposal 5)
M3-REPL-031-D: false-negative rate / power under positive excitation (Proposal 5)
M3-REPL-031-E: conditional magnitude recovery under M1 (Proposal 5 SS17; GATE-033/034 also serve this)
```

---

## 23. CD-0/CD-1/CD-2

Three distinct scenarios, none assumed correct by default:

```text
CD-0: CD excluded
CD-1: CD modulates latent historical event intensity
CD-2: CD modulates observation or detection probability
```

The simulation specification must distinguish the latent process from the observation process, e.g.:

```text
N_t* ~ LatentEventProcess(lambda_t*)
Y_t | N_t* ~ Binomial(N_t*, p_t)
```

Under CD-2:

```text
logit(p_t) = zeta_0 + zeta_1 * CD_t
```

This is a candidate observation equation only, not an adopted final equation unless already supported by the frozen design.

## 24. M1 Benchmark Boundary

```text
M1: MODEL_VALIDATION_FAILURE
    INFERENCE_NOT_AUTHORIZED
```

M1 is usable only as a historical benchmark within synthetic recovery comparison. M1 may not win inferential authorization automatically, fit historical data, generate public claims, generate ontology edges, or become a Graphify source.

## 25. M4 Exclusion

```text
HIGH-confidence exact-event dates: 12
M4: EXCLUDED_INSUFFICIENT_PRECISE_SUBSET
```

M4 must not be restored by pooling HIGH and MEDIUM date-precision tiers.

## 26. Mandatory versus Advisory Gates

```text
MANDATORY_GATE: directly contributes to candidate go/no-go
ADVISORY_GATE:  provides diagnostic evidence but does not independently determine go/no-go
```

Advisory gates do not automatically change a candidate's PASS/FAIL verdict unless a future versioned spec explicitly promotes a gate to mandatory before execution. A severe advisory finding (numerical failure, invalid CI, severe calibration defect, data loss, non-identifiability, protocol violation) halts execution for researcher review regardless of formal advisory status.

## 27. Seventeen Advisory Gates

Authoritative future count: **17** (superseding both the originally-proposed 21 and Proposal 6's own intermediate 19; see §3). Derivation: 24 total `PROTOCOL_NOT_COMPLETED` gates minus 7 M2/M3-`MANDATORY` gates undermined by protocol shortfall (`GATE-015`, `GATE-016`, `GATE-019`, `GATE-020`, `GATE-029`, `GATE-032`, `GATE-051`) = 17 genuinely advisory-tier, genuinely never-computed gates. `GATE-031` (`ESTIMAND_MISMATCH`) is excluded from this inventory entirely — its treatment is §22, not this count.

```text
Metric                          | M0      | M2      | M3      | Applicable candidates
---------------------------------|---------|---------|---------|----------------------
boundary_solution_rate           | GATE-038| GATE-052| GATE-059| all three
held_out_predictive_score        | GATE-039| GATE-053| GATE-060| all three
source_removal_stability         | GATE-040| GATE-054| GATE-061| all three
episode_removal_stability        | GATE-041| GATE-055| GATE-062| all three
calibration                      | GATE-042| GATE-056| GATE-063| all three
false_negative_excitation_rate   |   --    | GATE-050| GATE-057| M2, M3 only (M0=GATE-036, NOT_APPLICABLE)

Count: 5 metrics x 3 candidates = 15, plus false_negative_excitation_rate x 2 = 2 => 17.
```

`GATE-019`/`GATE-020` (M2 branching-ratio bias) are **not** in this 17 — they are M2-mandatory and already carry observed pilot values (0.020-0.054); their remediation path is §14 (M2 replication scale), not the advisory inventory.

## 28. Future Test Inventory

Preserved, 121 unique approved future test IDs, none executed:

```text
M0-HESS-001 through 010:   10
M2-EST-001 through 012:    12
M2-SCALE-001 through 015:  15
M3-NULL-001 through 020:   20
M3-DEC-001 through 028:    28
M3B-ADV-001 through 021:   21
M3-G31-001 through 015:    15
TOTAL:                     121
```

Verified mechanically: `MODEL_3B_AMENDMENT_TEST_INVENTORY.csv` contains exactly 121 rows, 7 columns (`test_id, candidate, source_proposal, description, implementation_status, uses_historical_data, conflicts_with_other_amendment`). Do not confuse the **17 advisory gates** (§27) with the **21 `M3B-ADV` advisory-gate-integrity future tests** listed here — these are different populations of different cardinality.

## 29. Numerical Decisions Still Pending

Eight decisions, all `PENDING_RESEARCHER_DECISION` (full ledger: `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv`):

```text
NUM-DEC-01: M2 replication denominator
NUM-DEC-02: M2 uncertainty method for n
NUM-DEC-03: M2 exact-null implementation
NUM-DEC-04: M3 threshold tau
NUM-DEC-05: M3 prior model odds
NUM-DEC-06: M3 marginal-likelihood or Bayes-factor method
NUM-DEC-07: M3 ROPE epsilon_n, if retained
NUM-DEC-08: operational resource ceiling
```

No numeric value is selected for any of the eight in this specification.

## 30. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```

No M0, M2, or M3 source file is modified or created by this specification. No full-Hessian correction, no `n`-primary reparameterization, no exact-null model, no decision-rule code is written.

## 31. Tournament-Rerun Nonauthorization

```text
TOURNAMENT RERUN: NOT_AUTHORIZED
```

No synthetic recovery execution, at any scale, occurs as part of producing this specification.

## 32. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```

`data/research/linimasa_events.csv` and `data/export/linimasa_events.csv` are not read, written, or referenced by any executed code in this phase.

## 33. Production Isolation

No Atlas, Graphify, API, database, backend, frontend, or production configuration file is read, modified, rebuilt, or restarted by this specification. No Docker command, `nginx` reload, or deployment action is executed. No content of this specification is staged, committed, pushed, or synced to the production server.

## 34. Final Status

```text
MODEL_3B_MATHEMATICAL_SPECIFICATION_V2_READY_FOR_RESEARCHER_DECISION
```

*(Status above is the original as-frozen text from this document's first draft. It is superseded, not deleted, by §35 below now that all eight numerical decisions have been adjudicated.)*

## 35. Numerical Adjudication Integration

All eight items on `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv` have been separately adjudicated by the researcher. This section records, additively, which mathematical elements of this specification each decision resolves, and which remain pending measurement or calibration. It does not authorize implementation, execution, or historical fitting — see §30-§32, unchanged.

Governing decisions and what each resolves:

```text
NUM-DEC-01 (APPROVED_WITH_LIMITATIONS)
  Resolves: M2 replication-accounting denominator.
  Result:   1,000 ATTEMPTED replications per cell (not 1,000 successful); R_attempt =
            R_valid + R_failed + R_invalid; failed scientific runs never replaced;
            infrastructure resume reuses the same replication ID and seed.
  Pending:  none (procedure fully specified).

NUM-DEC-02 (APPROVED_WITH_LIMITATIONS)
  Resolves: M2 uncertainty method for the primary estimand n = alpha/beta.
  Result:   Profile likelihood is the primary method; parametric bootstrap validates
            coverage; Wald/inverse-Hessian is diagnostic-only; Bayesian intervals are
            not selected for M2.
  Pending:  boundary (n=0) critical value depends on NUM-DEC-03's exact-null design.

NUM-DEC-03 (APPROVED_WITH_LIMITATIONS, completeness-corrected: 30 sections / 30
  M2-NULL tests)
  Resolves: M2 exact-null representation and existence test.
  Result:   H0: n=0 as an explicit nested null submodel vs H1: 0<n<1; nuisance
            parameters reoptimized separately under H0 and H1;
            T_LR = 2*(ell_1 - ell_0); boundary critical value calibrated by
            parametric bootstrap under H0, not the interior chi-square(1) reference.
  Pending:  the bootstrap critical value c_0.05 itself (requires implementation +
            calibration run, not authorized here).

NUM-DEC-04 (APPROVED_WITH_LIMITATIONS -- procedure only)
  Resolves: the CALIBRATION PROCEDURE for the M3 posterior-probability threshold tau.
  Result:   prospective synthetic calibration with independent calibration/evaluation
            sets; candidate grid {0.50, 0.75, 0.90, 0.95, 0.975, 0.99} for comparison
            only; worst-case FPR<=0.05 across all mandatory null scenarios (necessary,
            not sufficient); FNR/power evaluated jointly; INCONCLUSIVE outcome
            required; no automatic selection rule permitted.
  Pending:  the final numeric tau value -- explicitly NOT_SELECTED by this decision.

NUM-DEC-05 (APPROVED_WITH_LIMITATIONS)
  Resolves: M3 prior model odds P(M0), P(M1).
  Result:   primary synthetic-calibration scenario P(M0)=P(M1)=0.50 (prior odds = 1);
            mandatory sensitivity grid {0.75/0.25 null-favoring, 0.50/0.50 equal,
            0.25/0.75 excitation-favoring} -- synthetic calibration settings, not
            historical beliefs about excitation prevalence.
  Pending:  none (procedure and primary/sensitivity values fully specified).

NUM-DEC-06 (APPROVED_WITH_LIMITATIONS; compatibility classification
  FEASIBLE_WITH_IMPLEMENTATION_WORK)
  Resolves: M3 marginal-likelihood / Bayes-factor computation method.
  Result:   bridge sampling primary; thermodynamic integration secondary validation
            on a prespecified subset; log_BF_10 = log_m1 - log_m0; harmonic-mean
            estimator rejected; Savage-Dickey not selected as primary; BIC not a
            marginal-likelihood substitute; WAIC/PSIS-LOO remain predictive
            diagnostics only.
  Pending:  implementation of both methods (see confirmed blockers below).

NUM-DEC-07 (DEFERRED)
  Resolves: whether to select a ROPE boundary epsilon_n for excitation magnitude.
  Result:   deferred -- no epsilon_n selected, no basis currently exists; excitation
            existence is decided via M0-vs-M1 model comparison (NUM-DEC-03/05/06),
            not via ROPE; ROPE is not required for the first amended tournament.
  Pending:  epsilon_n itself, and the conditions under which NUM-DEC-07 may be
            reopened (literature / predictive-effect calibration / decision-theoretic
            loss / comparative benchmark / explicit researcher policy).

NUM-DEC-08 (APPROVED_WITH_LIMITATIONS -- framework only)
  Resolves: the operational resource-envelope FRAMEWORK for full tournament
            execution.
  Result:   dedicated nonproduction research environment; production execution
            prohibited; layered envelope (15 dimensions) plus staged execution
            waves (R0-R9) plus 16 stop conditions plus retry/overrun policy;
            evidence-derived cost model (T_serial_hat, T_parallel_hat, T_total_hat,
            T_budget, S_total_hat, M_peak_hat).
  Pending:  every exact numeric ceiling (workers, wall-clock, CPU-hours, memory,
            disk, free-space minimum, output size, checkpoint interval, retry
            count) -- all PENDING_MEASUREMENT, no benchmark has been authorized or
            run.
```

Confirmed M3 implementation blockers (from NUM-DEC-06's compatibility audit of `m3_bayesian_discrete.py`, none marked resolved by this integration):

```text
1. n_branch is clamped to [EPS, 1-EPS] -- exact n=0 is structurally unreachable
2. exact n=0 is absent from the current implementation's support
3. log_prior() omits required normalization constants (Beta(2,2), Gamma(2,1))
4. the MCMC proposal is generated in unconstrained space
5. the acceptance ratio omits the transformation Jacobian for that reparameterization
6. bridge sampling does not yet exist in the codebase
7. thermodynamic integration does not yet exist in the codebase
8. internal parameter priors are not yet versioned and frozen
```

Placeholder standardization applied additively across the five V2 outputs (original descriptive tokens preserved in meaning, mapped to explicit decision references):

```text
UNRESOLVED_REQUIRES_REPLICATION_DENOMINATOR      -> RESOLVED_BY_NUM_DEC_01
UNRESOLVED_REQUIRES_N_UNCERTAINTY_METHOD         -> RESOLVED_BY_NUM_DEC_02
UNRESOLVED_REQUIRES_M2_EXACT_NULL                -> RESOLVED_BY_NUM_DEC_03
UNRESOLVED_REQUIRES_TAU                          -> PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION
UNRESOLVED_REQUIRES_MODEL_PRIOR_ODDS             -> RESOLVED_BY_NUM_DEC_05
UNRESOLVED_REQUIRES_MARGINAL_LIKELIHOOD_METHOD   -> RESOLVED_BY_NUM_DEC_06
UNRESOLVED_REQUIRES_ROPE                         -> DEFERRED_BY_NUM_DEC_07
UNRESOLVED_REQUIRES_RESOURCE_CEILING             -> FRAMEWORK_RESOLVED_BY_NUM_DEC_08_VALUES_PENDING_MEASUREMENT
```

A resolved PROCEDURE (NUM-DEC-04, NUM-DEC-08) is not the same as a resolved numerical VALUE. No numeric tau, epsilon_n, or resource-ceiling value is introduced by this integration.

```text
IMPLEMENTATION AUTHORIZED BY THIS INTEGRATION:   NO
TOURNAMENT EXECUTION AUTHORIZED:                 NO
CALIBRATION EXECUTION AUTHORIZED:                NO
HISTORICAL FIT AUTHORIZED:                       NO
```

## 36. Final Status (Superseding)

```text
MODEL_3B_V2_NUMERICAL_DECISIONS_INTEGRATED_AND_READY_FOR_FREEZE
```
