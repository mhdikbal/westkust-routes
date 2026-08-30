# Amendment Adjudication — Proposal 4: M3 Exact-Null Representation

> **Decision record only. No M3 source code modified. No null model implemented. No M3 recovery rerun. No gate specification changed (original or amended-V2). No historical data fitted. Nothing staged, committed, pushed, or deployed.**

---

## 1. Scope

This document adjudicates **only** `PROPOSAL-04` — the requirement that M3 (Bayesian discrete-time Hawkes) represent the exact no-excitation state `n=0` inside its model support, rather than approximating it through a continuous transformation whose support is strictly positive. `PROPOSAL-01` (M0), `PROPOSAL-02` (M2 primary estimand), and `PROPOSAL-03` (M2 full-scale requirement) were adjudicated separately and are **not** touched by this document — all three remain `APPROVED_WITH_LIMITATIONS`, `implementation_authorized=NO`, `rerun_authorized=NO`, `historical_fit_authorized=NO`. `PROPOSAL-05` through `PROPOSAL-07` are **not** adjudicated here.

## 2. Authoritative Evidence

```text
Diagnostic-audit commit:    4b94cd689c995765102b4ca4c63e2636334432bb
Authoritative status:       MODEL_3B_PILOT_DIAGNOSTIC_AUDIT_PUSHED_AND_SERVER_SYNCED
Tournament verdict:         NOT_AVAILABLE
Historical-data fitting:    NOT_AUTHORIZED
Proposal 1 status:          APPROVED_WITH_LIMITATIONS (implementation-free)
Proposal 2 status:          APPROVED_WITH_LIMITATIONS (implementation-free)
Proposal 3 status:          APPROVED_WITH_LIMITATIONS (implementation-free)
```

Primary evidentiary sources: `MODEL_3B_M3_NULL_BOUNDARY_AUDIT.md` (transform and decision-rule code inspection), `docs/thesis/colab/model3b_tournament_harness/m3_bayesian_discrete.py::_from_unconstrained` (executed transform, source-verified), `MODEL_3B_PILOT_GATE_CLASSIFICATION.csv` GATE-030/GATE-035.

## 3. Current M3 Parameterization

Confirmed directly from `m3_bayesian_discrete.py::_from_unconstrained` (not assumed): the sampler works on an unconstrained scale `eta` (`logit_n`) and recovers `n` via

```text
n = expit(logit_n) = 1 / (1 + exp(-logit_n))
```

For every finite `logit_n`, `0 < n < 1` — `n=0` is structurally unreachable by this transform, for any real-valued sampler state.

## 4. Exact-Null Failure

The decision rule (`lo > 0.0` on the posterior 95% credible interval) is applied at the `n_true=0` synthetic cell. Since `n=0` is outside the model's own support, the posterior lower bound is true by construction, independent of the data — this mechanically produces the observed **200/200 (100%) false-positive rate**. This is the same mechanism the diagnostic audit already confirmed by direct code inspection (`MODEL_3B_PILOT_RECOVERY_DIAGNOSTIC_AUDIT.md` §M3), not re-derived here, only restated as the basis for this amendment.

## 5. Mathematical Support Analysis

```text
n = logit^-1(eta) = 1 / (1 + e^-eta)

For every finite eta:            0 < n < 1
Therefore:                       n = 0 not-in support(n)

The model structurally cannot represent H0: n = 0.
```

**Consequence:** the observed 200/200 false-positive result is not evidence of a substantive tendency to over-detect excitation — it is a mechanical consequence of parameter support that always excludes zero, combined with a decision rule that treats any strictly-positive lower bound as detected excitation. Restated per the researcher's own framing:

```text
THE 200/200 FALSE-POSITIVE RESULT IS NOT FINAL PROOF THAT M3 FAILED. THAT
RESULT IS A CONSEQUENCE OF PARAMETER SUPPORT THAT IS ALWAYS POSITIVE, GIVEN
A DECISION RULE THAT TREATS EVERY n > 0 AS EXCITATION.
```

## 6. Researcher Decision

```text
PROPOSAL-04: APPROVED_WITH_LIMITATIONS

Candidate:                    M3 Bayesian discrete-time Hawkes
Required change:              Model must represent exact null n=0 explicitly
Preferred direction:           Explicit two-model comparison, or hurdle indicator
Current continuous logit
  parameterization:            NOT VALID for exact-null testing
Implementation:                 NOT_AUTHORIZED
Rerun:                          NOT_AUTHORIZED
Historical fit:                 NOT_AUTHORIZED

Required status of the current null experiment:
  M3_CURRENT_NULL_TEST_NOT_INTERPRETABLE

NOT classified as:
  M3_FINAL_MODEL_FAILURE
  GENUINE_100_PERCENT_FALSE_POSITIVE_MODEL_FAILURE
  M3_FINAL_PASS
  M3_HISTORICAL_FIT_ELIGIBLE
```

## 7. Preferred Two-Model Design

```text
M3-NULL-A (PREFERRED): Explicit two-model comparison

Null model:        H0: n = 0
Excitation model:   H1: 0 < n < 1
```

The two models must share all non-excitation components as consistently as possible: baseline structure; exposure; observation model; overdispersion where applicable; covariates; temporal aggregation; source-observation assumptions.

**Reason this is preferred (recorded, not implemented):** exact null represented without approximation; model comparison is auditable; null and excitation states remain conceptually distinct; fewer hidden mixture-prior choices than spike-and-slab; compatible with a later decision-rule adjudication (Proposal 5); easier to test through synthetic null and positive-excitation scenarios.

```text
Preferred future implementation direction:
  EXPLICIT_NULL_VERSUS_EXCITATION_MODEL_COMPARISON
```

## 8. Hurdle Alternative

```text
M3-NULL-B (SECOND ACCEPTABLE): Hurdle / latent-indicator formulation

z ~ Bernoulli(pi)
if z = 0:  n = 0
if z = 1:  n ~ continuous distribution on (0, 1)
```

The excitation-existence decision and excitation-magnitude estimation must remain **separate** quantities, not conflated into one continuous posterior.

## 9. Spike-and-Slab Alternative

```text
M3-NULL-C (CONDITIONALLY ACCEPTABLE): Spike-and-slab formulation

P(n = 0) > 0   and   P(0 < n < 1) > 0
```

Requires a carefully documented prior and sensitivity analysis before it could be treated as equivalent to Options A/B — not specified further here.

## 10. Rejected Epsilon Approximation

**Not approved as the exact-null solution:**

```text
M3-NULL-D: Continuous positive prior plus epsilon clipping
M3-NULL-E: Treating an extremely small positive n as mathematically
           identical to n = 0
M3-NULL-F: Using logit(n) alone and declaring absence when the estimate
           is near zero
```

A region of practical equivalence (ROPE) may later **supplement** the exact-null model, but may **not replace** the exact-null requirement without a separate researcher decision.

## 11. Null and Alternative Equations

```text
Discrete-time observation model:
  Y_t ~ CountDistribution(Lambda_t)

Excitation model:
  Lambda_t = mu_t + sum_{k=1}^{K} w_k * Y_{t-k}

Integrated discrete excitation:
  n_d = sum_{k=1}^{K} w_k

Null model:
  w_1 = w_2 = ... = w_K = 0   =>   n_d = 0

Excitation model:
  at least one w_k > 0, with 0 < n_d < 1 (if stationarity requires the
  integrated excitation mass to remain below one)

If M3 uses a parametric kernel:
  w_k = n_d * h_k(beta)
  require: h_k(beta) >= 0  and  sum_{k=1}^{K} h_k(beta) = 1
  so that: sum_{k=1}^{K} w_k = n_d
```

**This equation set is recorded as a requirement for the future implementation to confirm against the actually-executed kernel normalization from source — it is not assumed to already hold in any existing code.** No source file is inspected against this specific normalization requirement in this adjudication turn, since doing so is implementation-adjacent analysis reserved for the implementation review step.

## 12. Baseline Nesting

**Required conceptual nesting:** the excitation model evaluated at `n=0` must equal the null model, for all shared parameters and observations. If exact nesting is impossible because the specifications differ, the future implementation must record:

```text
NULL_AND_ALTERNATIVE_NOT_NESTED
```

and require separate calibration of the comparison method. Unequal baseline, dispersion, exposure, or covariate structures between H0 and H1 must not be concealed.

## 13. Prior Requirements

**No prior value is selected by this document.** If a Bayesian indicator or mixture design is later implemented, the implementation review must record: prior probability for the null model; prior probability for the excitation model; prior for `n` conditional on excitation; prior for decay/lag weights; prior predictive behavior; sensitivity to prior odds; posterior calibration under the exact null; identifiability between baseline persistence and excitation. Prior settings require their own versioned implementation review — not settled here.

## 14. Observation-Regime Requirements

The exact-null design must operate under the **same observation regime as the historical application** — year-level temporal aggregation; same-year ties represented through counts rather than artificial ordering; source-observation scenarios; parent-child episode dependence; missing-event and duplicate-report scenarios where prescribed. The exact-null implementation must **not** be validated only on idealized continuous timestamps — doing so would reintroduce the exact observation-regime mismatch the root-cause audit already identified as the dominant confirmed defect (`RECOVERY_OBSERVATION_REGIME_MISMATCH`).

## 15. Relationship to Proposal 5

Proposal 4 decides **only** that exact `n=0` must be representable in M3's model support. Proposal 4 does **not** decide: the final model-selection statistic; the final posterior-probability threshold; the final Bayes-factor threshold; the final information criterion; the final ROPE; the final false-positive gate; the final prior on excitation magnitude; the final prior probability of the null state. Those belong to `PROPOSAL-05` (or another explicitly linked future amendment) — no decision rule is silently imported into this document.

## 16. Separation from M0

The M3 excitation-null gate must **not** be applied to M0. M0 has no excitation parameter. For M0, exact-null excitation testing is `NOT_APPLICABLE_TO_MODEL_DOMAIN` — consistent with the diagnostic audit's own Mathematical Domain ruling for GATE-002/003/005/006/036 (`MODEL_3B_PILOT_RECOVERY_DIAGNOSTIC_AUDIT.md` §17). This document does not recreate the earlier gate-domain error.

## 17. Separation from M2

Proposal 4 applies to M3 only. It does **not** automatically decide exact-null representation for M2. M2's exact-null compatibility must be checked independently under the future n-based M2 parameterization adjudicated in Proposal 2/3 — M2's structurally different estimator (interval-censored MBPP likelihood, not a Bayesian discrete-time sampler) means the M3 solution cannot be assumed to transfer.

```text
M2_EXACT_NULL_REVIEW: SEPARATE_DEPENDENCY
```

Proposal 2 and Proposal 3 are **not** altered by this document.

## 18. Required Future Tests (recorded, NOT executed this turn)

```text
M3-NULL-001: The null model represents n = 0 exactly.
M3-NULL-002: The excitation model represents 0 < n < 1.
M3-NULL-003: The excitation model reduces to the null model at n = 0 where
             nesting is claimed.
M3-NULL-004: No epsilon clipping replaces the exact null.
M3-NULL-005: Null simulations contain no excitation term.
M3-NULL-006: The same baseline model is used under H0 and H1.
M3-NULL-007: The same exposure and observation model is used under H0 and H1.
M3-NULL-008: The same overdispersion convention is used under H0 and H1.
M3-NULL-009: Prior-predictive simulation includes exact-null datasets.
M3-NULL-010: Posterior or model-comparison output is finite under the
             exact null.
M3-NULL-011: The implementation does not force positive n through
             initialization.
M3-NULL-012: The implementation does not force positive n through
             prior support.
M3-NULL-013: The null-state indicator is identifiable in synthetic data.
M3-NULL-014: The exact-null test is reproducible under fixed seed.
M3-NULL-015: Null and excitation output schemas are structurally consistent.
M3-NULL-016: The implementation reports null-state probability separately
             from excitation magnitude.
M3-NULL-017: The year-level observation regime is reproduced.
M3-NULL-018: No historical data enter implementation validation.
M3-NULL-019: M0 is excluded from excitation-null gates by applicability checks.
M3-NULL-020: M2 is not silently assigned the M3 null solution.
```

## 19. Original-Evidence Preservation

**Not modified by this document:** original M3 pilot outputs; original M3 source (`m3_bayesian_discrete.py`); the original false-positive result; the original 70-row gate specification; the diagnostic-audit classifications; raw result checksums; Proposal 1, Proposal 2, and Proposal 3 adjudications — all confirmed byte-unchanged (§ Validation below).

The original **100% false-positive excitation in null cells** result remains historically visible, unretracted, with the following interpretation attached:

```text
THIS RESULT IS NOT INTERPRETABLE AS A SUBSTANTIVE MODEL FAILURE BECAUSE THE
EXACT NULL WAS ABSENT FROM PARAMETER SUPPORT.
```

## 20. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```
No M3 source file is modified by this document. No null model, hurdle model, or spike-and-slab model is implemented. No `MODEL_3B_M3_EXACT_NULL_SPECIFICATION_V2` or `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2` file is created — these are naming suggestions only for a future, separately-authorized turn.

## 21. Rerun Nonauthorization

```text
RERUN: NOT_AUTHORIZED
```
No M3 execution (of any scale) is performed by this document.

## 22. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```
`data/research/linimasa_events.csv` and `data/export/linimasa_events.csv` are not read, written, or referenced by any executed code in this adjudication turn.

## 23. Decision Summary

```text
PROPOSAL-04: APPROVED_WITH_LIMITATIONS
Required property:            EXACT_NULL_N_EQUALS_ZERO_MUST_BE_IN_MODEL_SUPPORT
Current transform status:      n=expit(logit_n) INVALID for exact-null testing
Preferred design:              M3-NULL-A, explicit two-model comparison
                                (EXPLICIT_NULL_VERSUS_EXCITATION_MODEL_COMPARISON)
Acceptable alternative:        M3-NULL-B, hurdle/latent-indicator
Conditionally acceptable:      M3-NULL-C, spike-and-slab (requires prior +
                                sensitivity analysis)
Rejected as exact-null fix:    M3-NULL-D/E/F (epsilon clipping / near-zero
                                treated as zero / logit(n) alone)
Current null-test status:      M3_CURRENT_NULL_TEST_NOT_INTERPRETABLE
Decision-rule scope:           deferred to Proposal 5, not decided here
M0 applicability:              NOT_APPLICABLE_TO_MODEL_DOMAIN (unaffected)
M2 applicability:              SEPARATE_DEPENDENCY, not decided here
Implementation:                 NOT_AUTHORIZED
Rerun:                          NOT_AUTHORIZED
Historical fit:                 NOT_AUTHORIZED
```

## Final Status (this document)

```text
MODEL_3B_AMENDMENT_04_M3_EXACT_NULL_ADJUDICATED
```
