# NUM-DEC-05 Adjudication: M3 Prior Model Odds

> **Design/decision only. No M3 source file modified or created. No prior implemented in code. No marginal likelihood calculated. No threshold tau calibrated. No tournament run. No historical data fitted. Nothing staged, committed, pushed, or deployed.**

---

## 1. Scope

This document adjudicates **NUM-DEC-05 only**: the prior model odds `P(M0)` and `P(M1)` used for synthetic calibration of M3's exact-null-versus-excitation model comparison. `NUM-DEC-04`, `NUM-DEC-06`, `NUM-DEC-07`, and `NUM-DEC-08` remain `PENDING_RESEARCHER_DECISION` and are not addressed here. No implementation, marginal-likelihood computation, threshold calibration, tournament execution, or historical-data fitting is authorized by this decision.

## 2. Authoritative Evidence

Read in full before adjudication:

```text
MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md
MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv          (51-row V2 gate spec)
MODEL_3B_RECOVERY_PROTOCOL_V2.md
MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv
MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv            (8-row ledger; NUM-DEC-01/02/03 APPROVED_WITH_LIMITATIONS prior to this turn)
MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md
MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md
MODEL_3B_NUM_DEC_03_M2_EXACT_NULL_ADJUDICATION.md    (completeness-corrected: 30 sections, 30 future tests M2-NULL-001..030)
MODEL_3B_AMENDMENT_04_M3_EXACT_NULL_ADJUDICATION.md  (Proposal 4 -- M3 must represent H0: n=0 exactly, in-support; preferred M3-NULL-A explicit two-model comparison)
MODEL_3B_AMENDMENT_05_M3_DECISION_RULE_ADJUDICATION.md (Proposal 5 -- primary decision quantity P(M1|Y), threshold tau prospectively calibrated, not decided there)
MODEL_3B_M3_NULL_BOUNDARY_AUDIT.md                   (source-verified: n=expit(logit_n) structurally excludes n=0 in the pre-amendment M3 implementation)
```

Baseline confirmed before this turn: 70/70 original gates reconciled to 51 V2 gates (`MODEL_3B_GATE_V1_TO_V2_RECONCILIATION.csv`); NUM-DEC-01 = `APPROVED_WITH_LIMITATIONS` (1,000 attempted replications/cell); NUM-DEC-02 = `APPROVED_WITH_LIMITATIONS` (profile likelihood primary for M2's `n`, bootstrap secondary); NUM-DEC-03 = `APPROVED_WITH_LIMITATIONS`, completeness-corrected (30 sections, 30 future tests, M2 exact-null explicit nested submodel with bootstrap-calibrated likelihood-ratio); NUM-DEC-04 through NUM-DEC-08 = `PENDING_RESEARCHER_DECISION`.

## 3. Mathematical Question

Proposal 4 (`MODEL_3B_AMENDMENT_04`) established that M3 must represent the exact null `H0: n=0` in-support (preferred direction `M3-NULL-A`, explicit two-model comparison). Proposal 5 (`MODEL_3B_AMENDMENT_05`) established that the primary future decision quantity is the posterior model probability `P(M1|Y)`, with threshold `tau` calibrated prospectively — but did not select the prior model odds that the posterior itself depends on. The question NUM-DEC-05 resolves: **what prior probabilities `P(M0)` and `P(M1)` are assigned to the null and excitation models for synthetic calibration, and how must sensitivity to that choice be evaluated?**

## 4. Available Options

```text
EQUAL_ODDS_0_5_0_5_AS_ONE_CANDIDATE_ONLY          -- symmetric baseline, evaluated alongside a mandatory sensitivity grid
RESEARCHER_SPECIFIED_INFORMATIVE_ODDS             -- a single non-symmetric prior asserted without a grid
SENSITIVITY_ANALYSIS_ACROSS_A_GRID_NO_SINGLE_VALUE_ADOPTED -- report a grid without designating any primary value
```

**Selected:** `EQUAL_ODDS_0_5_0_5_AS_ONE_CANDIDATE_ONLY`, but not in isolation — equal odds is adopted as the **primary calibration scenario**, combined with a **mandatory** three-point sensitivity grid (Section 9, Section 10) that this document freezes as part of the decision itself. This differs from the bare `EQUAL_ODDS...AS_ONE_CANDIDATE_ONLY` option in the original ledger option list by making the sensitivity grid non-optional rather than a separately deferred evaluation.

## 5. Null and Excitation Models

```text
M0 (null):        n = 0
M1 (excitation):   0 < n < 1
```

These are the same nested M3 models whose exact in-support representation was required by Proposal 4 (`MODEL_3B_AMENDMENT_04` §7, §11) and whose decision quantity was fixed as `P(M1|Y)` by Proposal 5 (`MODEL_3B_AMENDMENT_05` §7).

## 6. Posterior-Odds Identity

```text
P(M1|Y) / P(M0|Y)  =  BF_10(Y) * [ P(M1) / P(M0) ]

BF_10(Y) = p(Y|M1) / p(Y|M0)
```

Under equal model odds, `P(M1)/P(M0) = 1`, therefore:

```text
posterior odds = BF_10(Y)          (holds ONLY under equal prior odds)
```

This equivalence is a consequence of the specific prior odds selected in Section 8, and **must not be stated as a universal identity** — under either sensitivity scenario (Sections 9–10), posterior odds differ from `BF_10(Y)` by the corresponding nonunit prior-odds factor.

## 7. Researcher Decision

```text
NUM-DEC-05:                                APPROVED_WITH_LIMITATIONS
CANDIDATE:                                 M3
PRIMARY CALIBRATION PRIOR ODDS:            P(M0) = 0.50,  P(M1) = 0.50
INTERPRETATION:                            EQUAL_MODEL_ODDS_FOR_SYNTHETIC_CALIBRATION, NOT A HISTORICAL BELIEF
PRIOR-SENSITIVITY GRID:                    REQUIRED (mandatory, not optional)
IMPLEMENTATION:                            NOT_AUTHORIZED
CALIBRATION:                               NOT_AUTHORIZED
TOURNAMENT:                                NOT_AUTHORIZED
HISTORICAL FIT:                            NOT_AUTHORIZED
```

`P(M0)=0.50, P(M1)=0.50` is explicitly **not**: a historical probability; a statement that excitation is historically 50% likely; a posterior result; a substantive historical prior; or authorization to fit historical data.

## 8. Equal-Odds Baseline

```text
PRIOR-ODDS-SCENARIO-B (PRIMARY):  P(M0) = 0.50,  P(M1) = 0.50  ->  prior odds M1/M0 = 1
Classification:                    EQUAL
```

Reasons equal odds is selected as the primary calibration scenario (all seven recorded, none imply the others):

```text
1. Equal odds provide a symmetric synthetic-calibration baseline.
2. Equal odds avoid favoring either the null model or excitation model before synthetic evidence is observed.
3. Equal odds simplify auditing the relationship between Bayes factors and posterior model probabilities (Section 6).
4. Equal odds are not claimed to represent historical prevalence.
5. Equal odds do not eliminate the need for sensitivity analysis (Sections 9-10 remain mandatory).
6. Equal odds do not select the marginal-likelihood computation method (NUM-DEC-06, Section 14).
7. Equal odds do not select the later decision threshold tau (NUM-DEC-04, Section 15).
```

## 9. Null-Favoring Sensitivity

```text
PRIOR-ODDS-SCENARIO-A:  P(M0) = 0.75,  P(M1) = 0.25  ->  prior odds M1/M0 = 1/3
Classification:          NULL_FAVORING
```

Approved as part of the minimum design grid. Not an alternative historical belief — a synthetic-calibration sensitivity point. Must not be removed because it produces an unfavorable M3 result for the candidate under this prior.

## 10. Excitation-Favoring Sensitivity

```text
PRIOR-ODDS-SCENARIO-C:  P(M0) = 0.25,  P(M1) = 0.75  ->  prior odds M1/M0 = 3
Classification:          EXCITATION_FAVORING
```

Approved as part of the minimum design grid, on the same basis as Section 9. The three scenarios (Sections 8–10) together form the mandatory sensitivity grid. The final M3 report must display results under **all three** scenarios — never only the equal-odds result, and never an average across prior-odds scenarios (Section 20 governs how cross-scenario stability, not a pooled value, is reported).

## 11. Model-Probability Validity

Required for every prior-odds scenario in the grid:

```text
0 < P(M0) < 1
0 < P(M1) < 1
P(M0) + P(M1) = 1
```

Rejected, in any future implementation:

```text
- negative probabilities
- probabilities greater than one
- probabilities that do not sum to one
- implicit unrecorded prior odds
- data-dependent prior probabilities
- priors selected after seeing the final evaluation results
```

## 12. Model Odds versus Parameter Priors

NUM-DEC-05 determines **only** `P(M0)` and `P(M1)` — the prior probability mass assigned to the null model versus the excitation model as a whole. It does **not** determine priors internal to `M1` for:

```text
- n (excitation magnitude, conditional on M1)
- beta or lag-decay parameters
- baseline coefficients
- dispersion
- CD effects
- observation-process parameters
- episode effects
```

Internal parameter priors require a future, separately versioned implementation review (consistent with `MODEL_3B_AMENDMENT_04` §13, which likewise deferred all within-model prior settings). Model odds must not be silently inferred from parameter-prior mass, and parameter priors must not be silently inferred from the selected model odds — the two are independent design decisions.

## 13. Calibration Requirements

The future calibration phase must evaluate whether `P(M1|Y)` behaves properly under **each** prior-odds scenario (Sections 8–10):

```text
- Under exact-null simulations: P(M1|Y) must not systematically concentrate near one merely because of the prior or implementation.
- Under positive-excitation simulations: P(M1|Y) must respond to increasing signal strength.
```

The selected threshold `tau` (NUM-DEC-04) must be calibrated separately, under the frozen prior-odds design established by this document. **NUM-DEC-05 does not select `tau`.**

## 14. Relationship to NUM-DEC-06

`NUM-DEC-06` will select or adjudicate the method for computing `p(Y|M0)` and `p(Y|M1)`, or another reproducible model-comparison quantity. `NUM-DEC-05` does **not** select:

```text
- bridge sampling
- nested sampling
- thermodynamic integration
- Chib-type marginal likelihood
- Savage-Dickey ratio
- information criteria
- approximate Bayes factors
```

Required dependency:

```text
NUM-DEC-05 (MODEL PRIOR ODDS)  +  NUM-DEC-06 (MODEL-COMPARISON COMPUTATION)  ->  NUM-DEC-04 (THRESHOLD TAU CALIBRATION)
```

## 15. Relationship to NUM-DEC-04

`NUM-DEC-04` remains pending. The posterior-probability threshold `tau` cannot be adjudicated coherently until:

```text
1. prior model odds are frozen (this document)
2. model-comparison computation is specified (NUM-DEC-06)
3. calibration design is frozen
4. exact-null implementation exists (per NUM-DEC-03-analogous M3 implementation, not yet authorized)
5. calibration output is available
```

`tau` is not assigned in NUM-DEC-05.

## 16. Relationship to NUM-DEC-07

`NUM-DEC-07` (M3 ROPE `epsilon_n`) remains pending. ROPE concerns excitation **magnitude** (e.g. `0 <= n <= epsilon_n`), a supplementary interpretation of `M1`'s internal parameter (`MODEL_3B_AMENDMENT_04` §10). Model prior odds (`NUM-DEC-05`) concern excitation **existence** — `M0` versus `M1`. ROPE probability must not be used as a substitute for `P(M0|Y)` unless separately adjudicated; existence and magnitude remain distinct quantities, consistent with the M2 existence/magnitude separation already established in `NUM-DEC-03` §18.

## 17. Historical-Prior Prohibition

Model odds must **not** be constructed from:

```text
- the observed historical event pattern
- the historical fit
- Phase D results
- Model 6 output
- qualitative game-theory annotations
- ontology relation counts
- the number of apparent clusters
- public production data
```

Model odds must be frozen **before** any historical fit. No empirical-Bayes model-odds selection is authorized.

## 18. Reporting Requirements

A future M3 result must report:

```text
- prior P(M0)
- prior P(M1)
- prior odds
- Bayes factor or selected comparison quantity
- posterior P(M0|Y)
- posterior P(M1|Y)
- selected tau
- decision outcome
- sensitivity across all three prior-odds scenarios (Sections 8-10)
- calibration-set version
- evaluation-set version
```

Posterior model probability must never be reported without its prior odds.

## 19. Calibration/Evaluation Separation

Prior odds and sensitivity scenarios must be frozen **before** opening the final evaluation set. The calibration set may be used to calibrate `tau` after `NUM-DEC-06` is decided and implemented. The evaluation set must remain unopened until:

```text
- exact-null model is frozen
- excitation model is frozen
- prior odds are frozen        (this document)
- comparison method is frozen  (NUM-DEC-06)
- tau is frozen                (NUM-DEC-04)
```

No historical data may be used in either set.

## 20. Decision-Stability Analysis

Future reports must calculate whether the final categorical decision changes across the three prior-odds scenarios (Sections 8–10). Required statuses:

```text
PRIOR_ROBUST
PRIOR_SENSITIVE
INCONCLUSIVE_ACROSS_PRIORS
```

The exact categorical-decision rule remains governed by `NUM-DEC-04`. No robustness threshold is invented in this document.

## 21. Prior-Predictive Checks

Before any final synthetic evaluation, a future implementation must perform prior-predictive checks for `M0` and `M1`, verifying:

```text
- count scales are plausible within the synthetic design
- M1 does not generate almost-certain explosive behavior
- M0 does not generate degenerate counts
- prior model odds do not hide invalid within-model priors
- exact-null simulations remain excitation-free
```

`NUM-DEC-05` does not select the within-model prior distributions (Section 12).

## 22. Required Future Tests

Record but do not execute — 20 tests, `M3-ODDS-001` through `M3-ODDS-020`:

```text
M3-ODDS-001: P(M0) and P(M1) are explicitly stored.
M3-ODDS-002: P(M0) + P(M1) equals one within numerical tolerance.
M3-ODDS-003: Neither model prior probability is zero.
M3-ODDS-004: Equal odds produce prior odds of one.
M3-ODDS-005: Null-favoring values produce prior odds M1/M0 of one-third.
M3-ODDS-006: Excitation-favoring values produce prior odds M1/M0 of three.
M3-ODDS-007: Posterior probabilities sum to one.
M3-ODDS-008: Under equal odds, posterior odds equal Bayes factor within tolerance.
M3-ODDS-009: Prior odds are not estimated from historical data.
M3-ODDS-010: Prior odds are frozen before threshold calibration.
M3-ODDS-011: Prior odds are frozen before final evaluation.
M3-ODDS-012: All three sensitivity scenarios are evaluated.
M3-ODDS-013: No scenario is dropped based on unfavorable results.
M3-ODDS-014: Posterior probabilities are reported with prior odds.
M3-ODDS-015: Decision stability across prior scenarios is reported.
M3-ODDS-016: Model odds remain separate from internal parameter priors.
M3-ODDS-017: Prior-predictive checks are completed for both models.
M3-ODDS-018: Exact-null simulations contain no excitation.
M3-ODDS-019: Calibration and evaluation seed manifests remain separate.
M3-ODDS-020: No historical data enter calibration or prior selection.
```

## 23. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```

No M3 source file (`m3_bayesian_discrete.py` or any other) is modified or created by this adjudication. No prior, no model-odds parameter, and no decision-rule code is written.

## 24. Calibration Nonauthorization

```text
CALIBRATION: NOT_AUTHORIZED
```

No prior-sensitivity calibration run, no synthetic data generation, and no calibration-set construction occurs as part of producing this adjudication.

## 25. Tournament Nonauthorization

```text
TOURNAMENT EXECUTION: NOT_AUTHORIZED
```

No synthetic recovery execution, calibration run, or evaluation run occurs as part of producing this adjudication.

## 26. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```

No historical data file is read, written, or referenced by this adjudication.

## 27. Decision Summary

```text
NUM-DEC-05:                     APPROVED_WITH_LIMITATIONS
Candidate:                      M3
Null / excitation models:       M0: n=0  /  M1: 0<n<1
Posterior-odds identity:        P(M1|Y)/P(M0|Y) = BF_10(Y) * [P(M1)/P(M0)]  (equals BF_10(Y) only under equal odds)
Primary calibration prior:      P(M0)=0.50, P(M1)=0.50  (prior odds M1/M0 = 1)  -- EQUAL, synthetic-calibration only, not a historical belief
Mandatory sensitivity grid:     NULL_FAVORING P(M0)=0.75/P(M1)=0.25 (odds 1/3);
                                 EQUAL P(M0)=0.50/P(M1)=0.50 (odds 1, primary);
                                 EXCITATION_FAVORING P(M0)=0.25/P(M1)=0.75 (odds 3)
Model-probability validity:     0<P(M0)<1, 0<P(M1)<1, P(M0)+P(M1)=1; no negative/>1/non-summing/implicit/data-dependent/post-hoc priors
Parameter-prior separation:     model odds != within-M1 parameter priors; neither inferred from the other
Historical-prior prohibition:   model odds frozen before any historical fit; no empirical-Bayes selection
Relationship to NUM-DEC-06:     required before model-comparison computation is specified
Relationship to NUM-DEC-04:     required before tau calibration; tau NOT assigned here
Relationship to NUM-DEC-07:     ROPE (magnitude) != model odds (existence); no substitution without separate adjudication
Decision-stability requirement: PRIOR_ROBUST / PRIOR_SENSITIVE / INCONCLUSIVE_ACROSS_PRIORS, rule governed by NUM-DEC-04
Prior-predictive requirement:   required for M0 and M1 before final evaluation; within-model priors not selected here
Required future tests:          20 (M3-ODDS-001..020)
Implementation authorized:      NO
Calibration authorized:         NO
Tournament execution authorized: NO
Historical fit authorized:      NO
Remaining pending:              NUM-DEC-04, NUM-DEC-06, NUM-DEC-07, NUM-DEC-08
```

```text
MODEL_3B_NUM_DEC_05_M3_PRIOR_MODEL_ODDS_ADJUDICATED
```
