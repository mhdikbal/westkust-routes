# Amendment Adjudication — Proposal 2: M2 Primary Estimand Change

> **Decision record only. No M2 source code modified. No reparameterization implemented. No M2 recovery rerun. No gate specification changed (original or amended-V2). No historical data fitted. Nothing staged, committed, pushed, or deployed.**

---

## 1. Scope

This document adjudicates **only** `PROPOSAL-02` — changing M2's primary recovery estimand from separately-recovered `alpha`/`beta` to the integrated excitation mass `n = alpha/beta`. `PROPOSAL-01` (M0 Hessian/covariance correction) was adjudicated separately and is unaffected — its `implementation_authorized`/`rerun_authorized`/`historical_fit_authorized` all remain `NO`, unchanged by this document. `PROPOSAL-03` through `PROPOSAL-07` are **not** adjudicated here and remain `PROPOSED_ONLY`/`NOT_ADJUDICATED`.

## 2. Authoritative Evidence

```text
Diagnostic-audit commit:    4b94cd689c995765102b4ca4c63e2636334432bb
Authoritative status:       MODEL_3B_PILOT_DIAGNOSTIC_AUDIT_PUSHED_AND_SERVER_SYNCED
Tournament verdict:         NOT_AVAILABLE
Historical-data fitting:    NOT_AUTHORIZED
Proposal 1 status:          APPROVED_WITH_LIMITATIONS (implementation-free)
```

Primary evidentiary sources: `MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md` (objective-ridge diagnostic), `MODEL_3B_PILOT_GATE_CLASSIFICATION.csv` (GATE-017/018/019/020/021), `docs/thesis/colab/model3b_tournament_harness/m2_mbpp.py` (executed estimator, source-verified).

## 3. Original M2 Parameterization

M2 is executed with a direct `(theta0, theta1, alpha, beta)` parameterization — `m2_mbpp.py::fit_m2`'s optimizer bounds are `[(None,None),(None,None),(0.0,None),(_EPS,None)]`, optimizing `alpha` and `beta` **directly**, not `n` or any reparameterized form. This is the parameterization the pilot's GATE-017 (`absolute_relative_bias_excitation_params`, individual alpha bias) and part of GATE-021 (alpha/beta CI coverage) evaluated against.

## 4. Objective-Ridge Evidence

Directly evaluated (not inferred) via `neg_ic_ll_density_baseline` — the exact function `fit_m2` optimizes — over a grid on one synthetic M2 dataset (fixed seed `777001`, `S3-equiv` cell, `n_true=0.6769`):

```text
Fixed n, beta varied ~20x (0.2 -> 4.0):     NLL varies by  1.74 units (218.92 to 220.66)
Fixed beta, n varied ~40%:                  NLL varies by >500 units
```

This is a textbook flat ridge along `alpha/beta ≈ n_true`, confirmed on synthetic data with known ground truth, not inferred from the pilot's fit results alone. Consistent with the pilot's own observed pattern: individual `alpha` bias 4,450–5,480%; alpha/beta coverage 3–20%; `n` (branching ratio, GATE-019/020) absolute bias 0.020–0.054, relative bias 0.030–0.080 — the metrics computed by the pilot's own harness under its existing exact definitions, not redefined here.

## 5. Identifiability Interpretation

```text
M2_ALPHA_BETA_SEPARATION_NOT_IDENTIFIED
M2_INTEGRATED_EXCITATION_ESTIMAND_PREFERRED
```

At annual observation resolution, the objective is far more sensitive to `n` than to the `alpha`/`beta` split. This does **not** establish `M2_FINAL_PASS`, `M2_MODEL_VALIDATED`, `M2_HISTORICAL_FIT_AUTHORIZED`, or `M2_PRODUCTION_READY` — the pilot ran at 150/1,000 replications per cell (§14 below), and identifiability being favorable is a necessary, not sufficient, condition for a pass verdict.

## 6. Primary Estimand Decision

```text
PROPOSAL-02: APPROVED_WITH_LIMITATIONS

M2 primary estimand:      n = alpha / beta  (branching ratio / integrated
                           excitation mass)
Secondary estimands:      interval-level integrated excitation mass;
                           predictive interval counts
Alpha and beta:           DIAGNOSTIC_ONLY, not primary recovery targets at
                           annual observation resolution, unless a future
                           design proves separate identifiability
Implementation:            NOT_AUTHORIZED (this turn)
Full M2 rerun:              NOT_AUTHORIZED (this turn)
Historical fit:             NOT_AUTHORIZED
```

## 7. Secondary Diagnostic Parameters

`alpha` and `beta` remain available as diagnostic parameters. Future reports may display: `alpha` estimate; `beta` estimate; decay timescale `1/beta`; objective-profile width; boundary behavior; sensitivity to fixed or grid-selected `beta`. Separate `alpha`/`beta` recovery must **not** independently fail the primary M2 candidate if: `n` is recovered; predictive interval counts are calibrated; uncertainty is valid; all other primary gates pass; and weak separate identifiability is explicitly disclosed. This does not delete the original `alpha`/`beta` gates (§11).

## 8. Mathematical Definition of n

For the exponential excitation kernel already in use:

```text
g(u) = alpha * exp(-beta * u),   u > 0
n = integral_0^infinity g(u) du = alpha / beta
```

`n` is the model's integrated excitation mass under this kernel — the expected number of "child" events directly triggered per "parent" event, integrated over all future time, under the fitted parameters.

## 9. Stationarity Boundary

Approved **for future implementation review only**, not implemented this turn:

```text
n = alpha / beta
alpha = n * beta
0 <= n < 1
beta > 0
```

This stationarity-safe parameterization is a **methodological direction**, not a guaranteed fix. Reparameterization to `(n, beta)` does not by itself establish that `beta` becomes well-identified — the objective-ridge evidence (§4) shows `n` is sharply identified while `beta` is not; `beta` may remain weakly identified even after this reparameterization, and this must be checked, not assumed, in any future implementation.

## 10. Historical-Interpretation Boundary

`n` is a **model-based integrated excitation quantity**. `n` must **not** automatically be interpreted as: a historical causal probability; the probability that one archival event caused another; an actor-level behavioral coefficient; a measure of historical intent; proof of conflict contagion; evidence of equilibrium; or a factual edge for ontology or Graphify. At annual observation resolution, `n` represents the integrated excitation mass recoverable **under the candidate model and observation process** — a statistical property of the fitted model, not a historiographical claim.

## 11. Original-Gate Preservation

The frozen 70-row `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` is **not modified** by this document. The original `alpha`/`beta` recovery gates (GATE-017, part of GATE-021) remain historically preserved and are **not** deleted or reclassified in the original pilot's own `MODEL_3B_PILOT_GATE_CLASSIFICATION.csv` (that file's existing `ESTIMAND_MISMATCH` classification for GATE-017/GATE-021 stands unchanged — this document does not touch it). This amendment states, prospectively, that in any future amended M2 run's own (separately versioned) gate specification, individual `alpha`/`beta` gates would become:

```text
SECONDARY_DIAGNOSTIC
```
or, where the original wording assumed separate identifiability as the pass criterion:
```text
ESTIMAND_MISMATCH_SUPERSEDED_FOR_FUTURE_AMENDED_RUN
```

**Required rule, binding on any future implementation:**
```text
original result remains immutable
  -> amendment applies prospectively
  -> amended run uses a new versioned gate specification
```

## 12. Future Gate Versioning

Any implemented amendment must create a **new** specification file, e.g. `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`. `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` (the original, frozen 70-row file) must **not** be overwritten. The future V2 gate specification must include, per row: `candidate`, `model_equation`, `parameter_space`, `estimand`, `null_definition`, `applicability`, `metric_formula`, `threshold`, `threshold_provenance`, `failure_meaning` — the same nine-element structure adopted as this project's standing Methodological Lesson (`MODEL_3B_PILOT_RECOVERY_DIAGNOSTIC_AUDIT.md` §17), so that a future gate demanding an estimand outside a candidate's parameter space is rejected before execution, not discovered after a full-scale run.

## 13. Exact-Null Dependency

This proposal does **not** settle how M2 represents `n = 0`. A future false-positive-excitation gate for M2 requires that the exact null be representable by M2's own implementation — this must be verified independently for M2, not assumed. **The M3 null-boundary solution (Proposal 4, not yet adjudicated) does not automatically transfer to M2** — M2's parameterization, kernel form, and estimator (interval-censored MBPP likelihood) differ structurally from M3's discrete-time Bayesian formulation, and M2's own exact-null representability must be checked on its own terms in a future, separate review.

```text
Dependency recorded: PROPOSAL-02 depends on a future exact-null and
decision-rule consistency review specific to M2, where applicable.
```

## 14. Protocol Dependency

This proposal does **not** waive M2's replication requirement.

```text
Current M2 result:    150 replications per cell
Planned M2 result:    1,000 replications per cell
```

Final M2 adjudication remains unavailable until `PROPOSAL-03` (M2 full-scale requirement) is separately decided and a later full-scale execution is explicitly authorized.

## 15. Uncertainty Requirements

A future M2 implementation must report uncertainty for `n`. Acceptable candidate methods for later review (none selected here): profile likelihood for `n`; parametric bootstrap; likelihood-based interval under the revised `(n, beta)` parameterization; Bayesian posterior interval if the implementation becomes Bayesian. No method is selected automatically by this document.

## 16. Required Future Tests (recorded, NOT executed this turn)

```text
M2-EST-001: n = alpha/beta is calculated consistently in simulator and estimator.
M2-EST-002: alpha = n * beta reproduces the intended kernel.
M2-EST-003: 0 <= n < 1 is enforced without excluding exact n = 0.
M2-EST-004: objective profiling confirms n sensitivity separately from beta sensitivity.
M2-EST-005: fixed-n / varying-beta ridge diagnostic is reproducible.
M2-EST-006: varying-n / fixed-beta objective separation is reproducible.
M2-EST-007: n bias is computed using the exact preregistered formula.
M2-EST-008: n interval coverage is assessed with a valid uncertainty method.
M2-EST-009: predictive interval counts are calibrated.
M2-EST-010: alpha and beta diagnostics are reported without being
            misrepresented as identified historical quantities.
M2-EST-011: all 1,000 replications per cell complete in a later authorized run.
M2-EST-012: no historical data are used during synthetic recovery.
```

## 17. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```
No M2 source file (`m2_mbpp.py`, `observation_pipeline.py`, `recovery_metrics.py`, or any other harness file) is modified by this document. No reparameterization code is written.

## 18. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```
`data/research/linimasa_events.csv` and `data/export/linimasa_events.csv` are not read, written, or referenced by any executed code in this adjudication turn.

## 19. Decision Summary

```text
PROPOSAL-02: APPROVED_WITH_LIMITATIONS
Primary estimand:            n = alpha / beta
Secondary estimands:         interval-level integrated excitation mass;
                              predictive interval counts
Alpha/beta status:           DIAGNOSTIC_ONLY
Stationarity parameterization: approved as future direction only
Exact-null (M2-specific):    unresolved, separate future dependency
Protocol requirement:        150/1,000 unresolved, depends on Proposal 3
Implementation:               NOT_AUTHORIZED
Full rerun:                   NOT_AUTHORIZED
Historical fit:               NOT_AUTHORIZED
```

## Final Status (this document)

```text
MODEL_3B_AMENDMENT_02_M2_ESTIMAND_ADJUDICATED
```
