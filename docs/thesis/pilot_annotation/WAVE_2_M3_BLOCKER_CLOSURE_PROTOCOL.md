# WAVE 2 M3 Blocker Closure Protocol (W2-P6)

> **Status: PLANNING-ONLY. All 8 blockers remain `OPEN`.** This document defines what closure would require; it closes none of them. The blocker registry itself is already implemented and immutable in Wave 1 (`docs/thesis/colab/model3b_spec_validator/applicability_validator.py::get_m3_blockers()`, `MappingProxyType`, no setter). This protocol governs a *future* code change to that registry, never a runtime state change.

## Universal Closure Conditions (instruction §15, apply to every blocker below)

A blocker may be closed in the future **only if all 8 hold simultaneously**:

```text
1. explicit mathematical requirement exists
2. implementation contract is approved
3. a positive test is available
4. a negative test is available
5. closure evidence is stored
6. historical data is NOT the sole validation basis for the implementation
7. independent review has occurred
8. closure is explicitly authorized
```

---

## Blocker 1 — `M3-BLOCK-01`

| Field | Value |
|---|---|
| blocker_id | M3-BLOCK-01 |
| source_decision | NUM-DEC-06 (compatibility audit) / NUM-DEC-03 (parallel M2 principle) |
| source_section | `applicability_validator.py::_M3_BLOCKERS["M3-BLOCK-01"]`; `WAVE_2_MATHEMATICAL_CONTRACT.md` §S1.7, §S3.1 |
| mathematical_object | `n`, `eta_n` (transform), exact null `n=0` |
| affected_component | future M3 exact-null/alternative submodel module (`REQ-M3-001`) |
| current_status | **OPEN** |
| required_resolution | a parameter representation in which `n=0` is exactly reachable — either a genuine nested-null submodel (no `eta_n` free parameter under `H0`) or a piecewise/hurdle transform with a hard `n=0` branch |
| permitted_evidence | design review + unit test confirming `n=0` is reached exactly (not asymptotically) in at least one code path; cross-reference to `WAVE_2_OPEN_DECISION_LEDGER.csv` `OD-004` |
| prohibited_shortcut | `n=epsilon` clipping; near-zero treated as exact zero; retaining the current `_to_unconstrained` clamp `[EPS,1-EPS]` |
| negative_test_required | test asserting the current clamped transform still fails (regression guard until the fix lands) |
| upstream_dependency | none (foundational) |
| downstream_dependency | M3-BLOCK-02 (priors must be defined over the corrected parameter space), M3-BLOCK-04/05 (bridge sampling/TI require a valid null model to compare against) |
| closure_gate | REQ-M3-001 acceptance criterion frozen + positive/negative tests pass + independent review |
| independent_review_required | YES |
| closure_authority | future researcher decision (new NUM-DEC-style adjudication), not this planning wave |

## Blocker 2 — `M3-BLOCK-02`

| Field | Value |
|---|---|
| blocker_id | M3-BLOCK-02 |
| source_decision | NUM-DEC-06 |
| source_section | `applicability_validator.py::_M3_BLOCKERS["M3-BLOCK-02"]`; `WAVE_2_MATHEMATICAL_CONTRACT.md` §S3.5 |
| mathematical_object | `p(mu\|M_k)`, `p(beta\|M1)` — Beta(2,2)/Gamma(2,1) kernel priors currently missing normalization constants |
| affected_component | future M3 prior-specification module (`REQ-M3-006`) |
| current_status | **OPEN** |
| required_resolution | every prior density used in marginal-likelihood computation carries its full normalization constant (proper density, not an unnormalized kernel) |
| permitted_evidence | code review confirming normalizing constants present; unit test comparing kernel-only vs. normalized log-density on synthetic inputs |
| prohibited_shortcut | leaving kernel-only priors and rescaling `BF_10` post hoc to "correct" the omission |
| negative_test_required | test asserting the current kernel-only `log_prior()` diverges from a correctly normalized reference by exactly the missing normalizing constant |
| upstream_dependency | M3-BLOCK-01 (parameter space must be settled first) |
| downstream_dependency | M3-BLOCK-04 (bridge sampling requires proper priors, per its own contract §S3.6) |
| closure_gate | REQ-M3-006 acceptance criterion frozen (`OD-009`) + tests pass + independent review |
| independent_review_required | YES |
| closure_authority | future researcher decision |

## Blocker 3 — `M3-BLOCK-03`

| Field | Value |
|---|---|
| blocker_id | M3-BLOCK-03 |
| source_decision | NUM-DEC-06 |
| source_section | `applicability_validator.py::_M3_BLOCKERS["M3-BLOCK-03"]`; `WAVE_2_MATHEMATICAL_CONTRACT.md` §S1.7 |
| mathematical_object | MCMC acceptance ratio; Jacobian `G(eta)` of the unconstrained-to-constrained transform |
| affected_component | future M3 posterior-sampling module (predecessor to `REQ-M3-009`) |
| current_status | **OPEN** |
| required_resolution | acceptance ratio computed from the unconstrained-space target density (constrained-space log-posterior **plus** the log-Jacobian term), not the constrained-space density alone |
| permitted_evidence | derivation review; unit test comparing accept/reject decisions with vs. without the Jacobian term on a synthetic case where the discrepancy is analytically known |
| prohibited_shortcut | ignoring the Jacobian on the (false) assumption it cancels; adding an ad hoc correction factor without derivation |
| negative_test_required | test asserting the current sampler's acceptance ratio (no Jacobian) diverges from the corrected one on a synthetic case |
| upstream_dependency | none directly (independent defect from M3-BLOCK-01/02, but shares the same source file) |
| downstream_dependency | M3-BLOCK-04 (any posterior draws feeding bridge sampling must come from a correctly-targeted sampler) |
| closure_gate | derivation reviewed + tests pass + independent review |
| independent_review_required | YES |
| closure_authority | future researcher decision |

## Blocker 4 — `M3-BLOCK-04`

| Field | Value |
|---|---|
| blocker_id | M3-BLOCK-04 |
| source_decision | NUM-DEC-06 |
| source_section | `applicability_validator.py::_M3_BLOCKERS["M3-BLOCK-04"]`; `WAVE_2_MATHEMATICAL_CONTRACT.md` §S3.6 |
| mathematical_object | `Z`, bridge identity `Z = E_g[h(theta)q(theta)] / E_p[h(theta)g(theta)]` |
| affected_component | future bridge-sampling module (`REQ-M3-009`) |
| current_status | **OPEN — no implementation exists** |
| required_resolution | a working bridge-sampling implementation satisfying all 15 design sub-decisions in `OD-010`, validated against a toy model with known closed-form `Z` before any real use |
| permitted_evidence | toy-model validation results; convergence/ESS diagnostics; repeated-run stability report |
| prohibited_shortcut | harmonic-mean estimator (already rejected, NUM-DEC-06); Savage-Dickey as primary (already rejected); using a single unvalidated run without stability checks |
| negative_test_required | test asserting the module does not exist / raises `NotImplementedError` today (regression guard) |
| upstream_dependency | M3-BLOCK-01, M3-BLOCK-02, M3-BLOCK-03, M3-BLOCK-06 |
| downstream_dependency | M3-BLOCK-05 (TI cross-checks against bridge output) |
| closure_gate | OD-010 resolved + toy-model validation passes + independent review |
| independent_review_required | YES |
| closure_authority | future researcher decision |

## Blocker 5 — `M3-BLOCK-05`

| Field | Value |
|---|---|
| blocker_id | M3-BLOCK-05 |
| source_decision | NUM-DEC-06 |
| source_section | `applicability_validator.py::_M3_BLOCKERS["M3-BLOCK-05"]`; `WAVE_2_MATHEMATICAL_CONTRACT.md` §S3.7 |
| mathematical_object | `p_t(theta\|Y)`, `log p(Y) = integral_0^1 E_t[log p(Y\|theta)] dt` |
| affected_component | future thermodynamic-integration module (`REQ-M3-010`) |
| current_status | **OPEN — no implementation exists** |
| required_resolution | a working TI implementation with a validated temperature ladder, run only on the NUM-DEC-06 prespecified validation subset |
| permitted_evidence | discretization-error study; per-temperature convergence diagnostics; repeated-run stability report |
| prohibited_shortcut | uniform-spacing ladder adopted without a discretization-error study near `t=0`; running TI on every replication instead of the prespecified subset |
| negative_test_required | test asserting the module does not exist / raises `NotImplementedError` today |
| upstream_dependency | M3-BLOCK-04 (bridge output is the comparison baseline) |
| downstream_dependency | none further (TI is the terminal secondary-validation step) |
| closure_gate | OD-011 resolved + discretization study passes + independent review |
| independent_review_required | YES |
| closure_authority | future researcher decision |

## Blocker 6 — `M3-BLOCK-06`

| Field | Value |
|---|---|
| blocker_id | M3-BLOCK-06 |
| source_decision | NUM-DEC-06 |
| source_section | `applicability_validator.py::_M3_BLOCKERS["M3-BLOCK-06"]` |
| mathematical_object | `p(mu\|M_k)`, `p(beta\|M1)`, `p(n\|M1)`, plus baseline/dispersion/CD/observation/episode priors |
| affected_component | future M3 internal-parameter-prior module (`REQ-M3-006`) |
| current_status | **OPEN** |
| required_resolution | all internal parameter priors versioned, frozen, and prior-predictively checked, via a future researcher decision (not empirical-Bayes on the historical data) |
| permitted_evidence | prior-predictive check results under synthetic generating processes; properness/support verification |
| prohibited_shortcut | deriving priors from the very historical data being analyzed (explicit prohibition, instruction §4/§10.5) |
| negative_test_required | test asserting the module has no frozen/versioned prior set today |
| upstream_dependency | M3-BLOCK-01 (parameter space must be settled) |
| downstream_dependency | M3-BLOCK-02, M3-BLOCK-04 |
| closure_gate | OD-009 resolved via a dedicated future adjudication turn + independent review |
| independent_review_required | YES |
| closure_authority | future researcher decision (new NUM-DEC-style adjudication) |

## Blocker 7 — `M3-BLOCK-07`

| Field | Value |
|---|---|
| blocker_id | M3-BLOCK-07 |
| source_decision | NUM-DEC-04 |
| source_section | `applicability_validator.py::_M3_BLOCKERS["M3-BLOCK-07"]` |
| mathematical_object | calibration-set / evaluation-set seed manifests (`M2_NULL_CALIBRATION_SET` pattern, `s_{c,r,m}`) |
| affected_component | future seed-manifest module (`REQ-M3-015`) |
| current_status | **OPEN** |
| required_resolution | disjoint, deterministic calibration and evaluation seed manifests implemented per NUM-DEC-04's requirement, with the evaluation set provably unopened until tau, priors, and comparison method are frozen |
| permitted_evidence | manifest-disjointness test; provenance log showing evaluation-set access only after the freeze gate |
| prohibited_shortcut | reusing calibration seeds for evaluation; opening the evaluation set "just to check" before freeze |
| negative_test_required | test asserting no manifest-separation mechanism exists today |
| upstream_dependency | OD-014 (seed-derivation function `f` must be chosen first) |
| downstream_dependency | REQ-M3-013/014 (tau calibration procedure) |
| closure_gate | OD-014 resolved + manifest-separation tests pass + independent review |
| independent_review_required | YES |
| closure_authority | future researcher decision |

## Blocker 8 — `M3-BLOCK-08`

| Field | Value |
|---|---|
| blocker_id | M3-BLOCK-08 |
| source_decision | NUM-DEC-08 |
| source_section | `applicability_validator.py::_M3_BLOCKERS["M3-BLOCK-08"]` |
| mathematical_object | `T_budget`, `S_total_hat`, `M_peak_hat` (resource-envelope formulas, NUM-DEC-08) |
| affected_component | future resource-measurement / execution-manifest module (`WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md`) |
| current_status | **OPEN — all 8 ceiling dimensions `PENDING_MEASUREMENT`** |
| required_resolution | a measured (not guessed) resource envelope on a dedicated nonproduction research environment, per NUM-DEC-08's own staged-measurement procedure |
| permitted_evidence | actual benchmark results from an authorized future profiling turn (explicitly NOT this planning turn) |
| prohibited_shortcut | any round-number ceiling adopted without measurement (explicit prohibition, NUM-DEC-08) |
| negative_test_required | test asserting no measured ceiling exists in configuration today (all fields `PENDING_MEASUREMENT`) |
| upstream_dependency | none directly, but practically follows M3-BLOCK-01 through 07 since a realistic measurement needs a representative (even if still-blocked) pipeline shape |
| downstream_dependency | full-scale execution of any future tournament wave |
| closure_gate | a separately authorized profiling turn (per NUM-DEC-08 §"Small synthetic profiling: AUTHORIZED_ONLY_AS_PREIMPLEMENTATION_RESOURCE_MEASUREMENT") + measured envelope frozen + independent review |
| independent_review_required | YES |
| closure_authority | future researcher decision, explicitly not authorized in Wave 2 |

---

## Closure Status Summary

```text
M3-BLOCK-01  OPEN
M3-BLOCK-02  OPEN
M3-BLOCK-03  OPEN
M3-BLOCK-04  OPEN
M3-BLOCK-05  OPEN
M3-BLOCK-06  OPEN
M3-BLOCK-07  OPEN
M3-BLOCK-08  OPEN
```

**8/8 OPEN at the end of this planning wave.** No blocker was closed, partially closed, or reclassified. The registry `docs/thesis/colab/model3b_spec_validator/applicability_validator.py::get_m3_blockers()` was not modified (verified in `WAVE_2_CROSS_DOCUMENT_CONSISTENCY_AUDIT.md`).
