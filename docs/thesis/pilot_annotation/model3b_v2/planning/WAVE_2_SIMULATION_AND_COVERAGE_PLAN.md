# WAVE 2 Simulation-Recovery, Coverage Plan, and Failure Taxonomy (W2-P4)

> **Status: PLANNING-ONLY.** No simulation is run, no benchmark is executed, no cell is authorized for execution by this document.

## 1. Candidate Factors (instruction §13.1)

```text
mu, n, beta, T, N, initial condition, observation-window regime
```

**Full Cartesian product across these factors is explicitly prohibited** (instruction §13.1). Every simulation cell that a future implementation proposes must carry an explicit scientific justification tied to a `WAVE_2_REQUIREMENT_DEPENDENCY_MATRIX.csv` requirement ID — this document does not enumerate cells, only the mandatory regime categories and design constraints a future cell-selection process must satisfy.

## 2. Mandatory Regimes (§13.2)

| Regime | Definition | Resource note |
|---|---|---|
| Exact null | `n=0` | Requires `REQ-M2-010`/`REQ-M3-001` exact-null representability — currently `OPEN`/blocked (`M3-BLOCK-01` for M3) |
| Near-null | `0<n<<1` | — |
| Moderate excitation | `n ∈ N_moderate` (range not yet fixed — `OPEN_REQUIRES_ADJUDICATION`, part of `OD-007`/`OD-013` grid design) | — |
| Near-critical | `n → 1⁻` | `E[lambda] = mu/(1-n)` — mandatory resource guardrails and explosion checks required as `n` approaches 1; see failure code `EXPLOSION_OR_EVENT_CAP_FAILURE` below |

## 3. Execution-Stage Distinctions (§13.3) — must never blur into each other

```text
SMOKE TEST              -- minimal-scale wiring check, no acceptance-criterion evaluation
PILOT COMPUTATIONAL CHECK -- small-scale numerical sanity check, still no gate adjudication
LOCKED PARTIAL BATCH     -- a checkpointed subset of a preregistered design, frozen before execution
FULL PREREGISTERED RUN   -- the complete design, R_attempted=1000/cell, only after M0-gate/M2/M3 contracts and NUM-DEC-08 resource envelope are frozen
```

None of these stages may alter the frozen requirement `R_attempted,c = 1000` for a full run once authorized (§13.3). No stage is authorized by this document; all remain future work.

## 4. Seed Hierarchy (§13.4)

```math
s_{c,r,m} = f(s_{\mathrm{master}}, c, r, m)
```

for cell `c`, replication `r`, method/component `m`. The derivation function `f` is `OD-014`, `OPEN_REQUIRES_ADJUDICATION` — collision resistance, reproducibility, and independence must be evaluated before `f` is fixed (candidates: hash-based derivation, counter-based RNG, splittable RNG — see `WAVE_2_OPEN_DECISION_LEDGER.csv`).

## 5. Failure Taxonomy (instruction §14 — 24 codes, 9 required fields each)

Every attempted replication across M0/M2/M3 must terminate in exactly one code below, or `VALID`. No silent filtering is permitted (`REQ-M2-004`, `RESOLVED_BY_FROZEN_SPEC` for the taxonomy itself; per-code retry/exclusion policy is `OPEN_REQUIRES_ADJUDICATION` for most codes, marked below).

| failure_code | definition | detection_rule | denominator_effect | retry_permitted | retry_limit | exclusion_permitted | reporting_requirement | downstream_consequence |
|---|---|---|---|---|---|---|---|---|
| GENERATION_FAILURE | synthetic-data generator did not produce a valid event sequence | generator raises / returns malformed output | counts toward R_attempted, not R_completed | infrastructure-interruption resume only, same seed (NUM-DEC-01 pattern) | OPEN | NO | logged in attempted-run accounting | R_completed reduced |
| INVALID_EVENT_SEQUENCE | generated sequence violates ordering/domain constraints | post-generation validity check | counts toward R_completed, not R_valid | NO (scientific, not infra) | 0 | NO | logged with sequence diagnostic | excluded from all metrics |
| EXPLOSION_OR_EVENT_CAP_FAILURE | event count exceeds a preregistered cap (near-critical `n→1` risk) | count vs. cap comparison during generation | counts toward R_completed, not R_valid | NO | 0 | NO, remains in attempted-run accounting | logged with event-count value | flags near-critical cell for resource review |
| LIKELIHOOD_NONFINITE | ell(theta) evaluates to NaN/Inf at candidate theta | finite-value check post-evaluation | counts toward R_converged? NO (excluded before convergence check) | NO | 0 | NO | logged with theta value | excluded from R_valid |
| INVALID_PARAMETER_TRANSFORM | theta=g(eta) produces a value outside the parameter domain | domain check post-transform | excluded pre-fit | NO | 0 | NO | logged with eta, theta | blocks fit attempt entirely |
| OPTIMIZER_NONCONVERGENCE | optimizer fails to reach a stationary point within iteration/tolerance budget | optimizer status flag | counts toward R_completed, not R_converged | OPEN (multi-start policy TBD, `OD-007`) | OPEN | NO | logged with optimizer diagnostics | excluded from R_valid |
| BOUNDARY_SOLUTION | optimum lands on parameter-space boundary | parameter value vs. boundary comparison | reported as its own category, never auto-invalid (per NUM-DEC-03 pattern) | n/a | n/a | NO, reported separately | logged explicitly, not merged into VALID or FAILED | validity depends on parameter domain and metric (NUM-DEC-03 precedent) |
| SCORE_CHECK_FAILURE | \|\|s(theta_hat)\|\|_inf > epsilon_s | score-norm comparison | counts toward R_completed, not R_valid pending epsilon_s (OD-001) | NO | 0 | NO | logged with score-norm value | excluded from R_valid once epsilon_s set |
| HESSIAN_ASYMMETRY | E_sym exceeds tolerance (OD-002) | symmetry-error comparison | excludes covariance-dependent metrics | NO | 0 | NO | logged with E_sym value | SE/CI unavailable for this replication |
| HESSIAN_REFERENCE_MISMATCH | E_H exceeds tolerance (OD-002) vs. numerical reference | reference-comparison | excludes covariance-dependent metrics | NO | 0 | NO | logged with E_H value | flags candidate-derivative implementation defect |
| OBSERVED_INFORMATION_INVALID | J(theta_hat) not invertible or not finite | matrix-invertibility/finiteness check | excludes covariance | NO | 0 | NO | logged | SE/CI unavailable |
| COVARIANCE_NONFINITE | Var(theta_hat) contains NaN/Inf | finite-value check | excludes covariance-dependent metrics | NO | 0 | NO | logged | SE/CI unavailable |
| COVARIANCE_NOT_POSITIVE_SEMIDEFINITE | Var(theta_hat) fails PSD check | eigenvalue check | excludes covariance-dependent metrics | NO | 0 | NO | logged with min eigenvalue | SE/CI unavailable |
| PROFILE_OPTIMIZATION_FAILURE | nuisance optimization at a fixed profile grid point fails | optimizer status at profile point | excludes that grid point from D(n) | OPEN (`OD-007`) | OPEN | reported, not silently dropped | logged per grid point | profile interval may be one-sided/disconnected |
| PROFILE_ENDPOINT_FAILURE | endpoint search for confidence-interval boundary fails to converge | endpoint-search status | interval endpoint marked FAILED, not silently widened/narrowed | OPEN | OPEN | NO | logged | `PROFILE_INTERVAL_FAILED` status (NUM-DEC-02/03 vocabulary) |
| BOOTSTRAP_GENERATION_FAILURE | Y*(b) generation under H0 fails | generator check on bootstrap draw | excluded from B, does not reduce reported B silently | NO | 0 | NO, remains in attempted-bootstrap accounting | logged per b | reduces valid bootstrap sample size |
| BOOTSTRAP_NULL_FIT_FAILURE | theta0*(b) fit fails on a bootstrap replicate | fit status | excluded from bootstrap null distribution | NO | 0 | NO | logged | affects critical-value estimation precision |
| BOOTSTRAP_ALTERNATIVE_FIT_FAILURE | theta1*(b) fit fails on a bootstrap replicate | fit status | excluded from bootstrap null distribution | NO | 0 | NO | logged | affects critical-value estimation precision |
| LIKELIHOOD_RATIO_INVALID | Lambda(Y) or Lambda*(b) is negative beyond declared numerical tolerance, or nonfinite | sign/finite check | excluded from LR-based metrics; never silently clamped to zero (NUM-DEC-03) | NO | 0 | NO | logged with raw value, flagged for review | indicates optimizer failure, sign mismatch, or non-nested implementation defect |
| POSTERIOR_DIAGNOSTIC_FAILURE | M3 posterior sampling fails convergence/ESS/multi-chain diagnostics | diagnostic-suite status | excludes replication from marginal-likelihood computation entirely | NO | 0 | NO | logged with diagnostic values | `MARGINAL_LIKELIHOOD_NOT_COMPUTABLE_FROM_INVALID_POSTERIOR` (NUM-DEC-06 status) |
| BRIDGE_SAMPLING_FAILURE | bridge estimate fails to converge or produces nonfinite Z | bridge-diagnostic status | excludes replication from BF_10 | OPEN (`OD-010`) | OPEN | NO | logged | model-comparison replication marked `BRIDGE_FAILED` |
| THERMODYNAMIC_INTEGRATION_FAILURE | TI integral fails to converge on the validation subset | TI-diagnostic status | excludes replication from TI cross-check | OPEN (`OD-011`) | OPEN | NO | logged | `THERMODYNAMIC_INTEGRATION_FAILED` status; secondary-validation coverage reduced |
| MARGINAL_LIKELIHOOD_DISAGREEMENT | Delta_BTI exceeds threshold (OD-012, not yet set) | discrepancy comparison | excludes replication from final BF_10 acceptance | NO | 0 | NO | logged with both estimates | `MODEL_COMPARISON_NUMERICALLY_UNRESOLVED` |
| TAU_CALIBRATION_UNRESOLVED | tau calibration procedure cannot produce a stable/valid threshold under current evidence | calibration-stability check | excludes cell from final tau selection contribution | n/a | n/a | reported, not hidden | logged | tau-selection blocked pending resolution |
| UNCLASSIFIED_IMPLEMENTATION_FAILURE | any failure not matching the 23 codes above | fallback catch-all, must trigger a taxonomy-review flag (never a silent pass-through) | counts toward R_attempted, excluded from R_valid | NO | 0 | NO | logged with full stack/diagnostic; MUST be reviewed and, if recurring, promoted to a new named code | blocks affected replication; recurring instances block the taxonomy itself from being declared complete |

**24 codes total**, mechanically counted; matches the instruction's own list exactly (§14).

## 6. Storage of This Plan

This plan is additive documentation only. No cell from §2 is scheduled, no seed from §4 is generated, and no failure code in §5 has been triggered by an actual run. Execution scheduling and stop rules are the responsibility of `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md`.
