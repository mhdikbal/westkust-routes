# NUM-DEC-07 Adjudication: M3 ROPE epsilon_n

> **Design/decision only. No epsilon_n selected. No ROPE implemented. No M3 model implemented. No calibration or tournament executed. No historical data fitted. Nothing staged, committed, pushed, or deployed.**

---

## 1. Scope

This document adjudicates **NUM-DEC-07 only**: whether to select a region-of-practical-equivalence (ROPE) boundary `epsilon_n` for interpreting the magnitude of M3's excitation parameter `n`, conditional on the excitation model. `NUM-DEC-08` remains `PENDING_RESEARCHER_DECISION` and is not addressed here. The decision recorded is **`DEFERRED`** — a distinct status from the `APPROVED_WITH_LIMITATIONS` used for NUM-DEC-01 through NUM-DEC-06 — meaning the ROPE question is left open rather than resolved with a selected value. No implementation, calibration execution, tournament rerun, or historical-data fitting is authorized by this decision.

## 2. Authoritative Evidence

Read in full before adjudication:

```text
MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md
MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv          (51-row V2 gate spec)
MODEL_3B_RECOVERY_PROTOCOL_V2.md
MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv
MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv            (8-row ledger; NUM-DEC-01..06 APPROVED_WITH_LIMITATIONS prior to this turn)
MODEL_3B_NUM_DEC_04_M3_TAU_CALIBRATION_ADJUDICATION.md
MODEL_3B_NUM_DEC_05_M3_PRIOR_MODEL_ODDS_ADJUDICATION.md
MODEL_3B_NUM_DEC_06_M3_MARGINAL_LIKELIHOOD_ADJUDICATION.md
MODEL_3B_AMENDMENT_04_M3_EXACT_NULL_ADJUDICATION.md
MODEL_3B_AMENDMENT_05_M3_DECISION_RULE_ADJUDICATION.md
```

Baseline confirmed before this turn: 70/70 original gates reconciled to 51 V2 gates; NUM-DEC-01 = `APPROVED_WITH_LIMITATIONS` (1,000 attempted replications/cell); NUM-DEC-02 = `APPROVED_WITH_LIMITATIONS` (profile likelihood for M2's `n`); NUM-DEC-03 = `APPROVED_WITH_LIMITATIONS`, completeness-corrected (30 sections/30 tests, M2 exact null); NUM-DEC-04 = `APPROVED_WITH_LIMITATIONS` (prospective tau calibration **procedure** only, no final tau selected); NUM-DEC-05 = `APPROVED_WITH_LIMITATIONS` (M3 prior odds, equal primary + mandatory 3-scenario sensitivity grid); NUM-DEC-06 = `APPROVED_WITH_LIMITATIONS` (bridge sampling primary, thermodynamic integration secondary, `log_BF_10`; compatibility classification `FEASIBLE_WITH_IMPLEMENTATION_WORK` with 5 confirmed blockers in `m3_bayesian_discrete.py`). NUM-DEC-07/08 = `PENDING_RESEARCHER_DECISION`.

## 3. Mathematical Question

M3's exact-null adjudication (per `MODEL_3B_AMENDMENT_04_M3_EXACT_NULL_ADJUDICATION.md` and the M0/M1 framework carried through NUM-DEC-04/05/06) already answers the *existence* of excitation via `M0: n=0` versus `M1: 0<n<1` model comparison, decided through the posterior model probability `P(M1|Y)` and a future calibrated threshold `tau` (NUM-DEC-04). A separate, optional question remains: **should M3 additionally define a region-of-practical-equivalence boundary `epsilon_n`, so that excitation magnitude `0 < n <= epsilon_n` conditional on `M1` can be labeled "practically negligible"?** NUM-DEC-07 resolves whether to select such an `epsilon_n` now.

## 4. Exact Null versus Practical Equivalence

```text
M0: n = 0                         exact-null model (excitation absent)
M1: 0 < n < 1                     excitation model

Excitation-existence quantity:    P(M1 | Y)
Magnitude quantity (given M1):    p(n | Y, M1)

Candidate ROPE:                   0 < n <= epsilon_n   (or 0 <= n <= epsilon_n with the boundary included)
```

The exact point `n = 0` belongs to `M0`, **not** to the continuous magnitude distribution conditional on `M1`. Therefore:

```text
P(n <= epsilon_n | Y, M1)   must NOT be treated as equivalent to   P(M0 | Y)
```

Required separation of roles:

```text
EXACT_NULL:  model-existence question           -- answered by M0 vs M1 comparison
TAU:         calibrated decision threshold       -- governs P(M1|Y) >= tau  (NUM-DEC-04)
ROPE:        optional magnitude interpretation   -- assesses n conditional on M1 already being selected
```

## 5. Available Options

```text
NO_ROPE_RETAINED                              -- SELECTED (as DEFERRED, not a permanent rejection)
LITERATURE_DERIVED_EPSILON_N                  -- requires a peer-reviewed, methodologically compatible source
SIMULATION_DESIGN_REQUIREMENT_EPSILON_N       -- requires synthetic predictive-effect calibration
COMPARATIVE_BENCHMARK_EPSILON_N               -- requires a prespecified n-vs-M0-predictive-behavior benchmark
EXPLICIT_RESEARCHER_POLICY_EPSILON_N          -- requires explicit disclosed researcher policy adoption
```

None of the four value-bearing options is selected in this turn. The selected disposition is deferral, recorded formally in Section 6.

## 6. Researcher Decision

```text
NUM-DEC-07:                          DEFERRED
CANDIDATE:                           M3
TOPIC:                               ROPE epsilon_n for excitation magnitude
SELECTED OPTION:                     NO_ROPE_VALUE_SELECTED
ROPE STATUS:                         OPTIONAL_SUPPLEMENTARY_MAGNITUDE_DIAGNOSTIC
EXCITATION-EXISTENCE DECISION:       MUST USE M0 VERSUS M1 MODEL COMPARISON
CURRENT EPSILON_N:                   UNSPECIFIED
IMPLEMENTATION:                      NOT_AUTHORIZED
CALIBRATION:                         NOT_AUTHORIZED
TOURNAMENT EXECUTION:                NOT_AUTHORIZED
HISTORICAL FIT:                      NOT_AUTHORIZED
```

This is a **deferral**, not a rejection of ROPE forever, and not a selection of any value — including zero. `epsilon_n` remains genuinely unresolved, to be decided in a future, separately authorized turn if and when one of the reopening conditions in Section 9 is met.

## 7. Reasons for Deferral

```text
1.  No literature-derived substantive cutoff has been established for the Atlas annual observation regime.
2.  No historical interpretation maps a particular n value to negligible practical impact.
3.  No synthetic calibration has yet related n to predictive interval-count changes.
4.  No loss function has been approved for practical-equivalence errors.
5.  M3 exact-null and model-comparison implementations do not yet exist.
6.  Internal parameter priors are not yet frozen.
7.  Tau has not been numerically calibrated (NUM-DEC-04 approved a procedure only, not a value).
8.  Historical data must not be used to select epsilon_n.
9.  Choosing epsilon_n now would be an unsupported researcher-policy number.
10. Exact-null model comparison already supplies the necessary framework for excitation existence.
```

## 8. First-Tournament Consequence

ROPE is **not required** for the first amended M3 recovery tournament. The future M3 implementation must be capable of operating without a ROPE. Required first-stage reporting:

```text
P(M0 | Y)
P(M1 | Y)
model-comparison decision
conditional posterior for n under M1
conditional interval for n
calibration results
INCONCLUSIVE outcome where applicable
```

ROPE-based labels must remain absent unless NUM-DEC-07 is reopened and a numerical `epsilon_n` is approved.

## 9. Conditions for Reopening

NUM-DEC-07 may be reopened only after evidence exists for **at least one** of:

```text
A. LITERATURE-DERIVED THRESHOLD
B. PREDICTIVE-EFFECT CALIBRATION
C. DECISION-THEORETIC LOSS
D. COMPARATIVE BENCHMARK
E. RESEARCHER POLICY
```

No basis may be derived from the final historical fit.

## 10. Literature-Derived Option

A peer-reviewed and methodologically compatible source provides a defensible practical-effect boundary for integrated excitation at the relevant temporal scale (annual-resolution VOC-era archival counts). Not currently available; not selected here.

## 11. Predictive-Effect Option

Synthetic analysis maps candidate `n` values to material changes in predictive interval counts or another prespecified operational quantity. If reopened via this route, a future implementation would evaluate:

```text
Delta_pred(n) = D[ p(Y_future | M1, n), p(Y_future | M0) ]
```

where `D` is a prespecified predictive-distance or loss measure. The exact distance `D` is **not selected here**. Possible future categories: expected count difference; predictive-distribution distance; forecast-loss difference; posterior predictive exceedance probability. No distance measure is introduced without separate review.

## 12. Decision-Theoretic Option

A loss function explicitly defines the cost of labeling small excitation as meaningful versus negligible. Not currently available; not selected here.

## 13. Comparative-Benchmark Option

A prespecified benchmark relates `n` to `M0` predictive behavior under the Atlas observation regime. Not currently available; not selected here.

## 14. Researcher-Policy Option

A researcher explicitly adopts `epsilon_n` as a policy threshold, with the arbitrariness and consequences disclosed. Not exercised in this turn — the researcher's own instruction explicitly declined this route now ("tidak ada dasar ilmiah untuk menetapkan `epsilon_n`... nilai tersebut akan arbitrer").

## 15. Relationship to NUM-DEC-04

NUM-DEC-04 governs `tau` for selecting the excitation model using `P(M1|Y)`. NUM-DEC-07 governs only practical magnitude conditional on `M1`. NUM-DEC-07 does **not** alter: the tau candidate grid (0.50/0.75/0.90/0.95/0.975/0.99); the exact-null FPR target (worst-case `<=0.05`); the FNR/power requirement; independent calibration/evaluation-set separation; or the `INCONCLUSIVE` outcome category. The NUM-DEC-04 tau grid must **not** be reused as an `epsilon_n` grid — `tau` and `epsilon_n` have different mathematical meanings (a decision threshold on `P(M1|Y)` versus a magnitude boundary on `n` conditional on `M1`).

## 16. Relationship to NUM-DEC-05

NUM-DEC-05 governs model prior odds `P(M0)`/`P(M1)`, which affect `P(M1|Y)`. They do not define practical magnitude. `epsilon_n` must not be derived from model prior odds.

## 17. Relationship to NUM-DEC-06

NUM-DEC-06 governs marginal-likelihood and Bayes-factor computation (`log_BF_10`). Bayes factors compare models; ROPE assesses magnitude conditional on the excitation model already being selected. A Bayes-factor evidence level must not be used to define `epsilon_n`.

## 18. Prior Sensitivity

If ROPE is reconsidered in a future turn, sensitivity to internal priors on `n` under `M1` must be reported — a high posterior probability inside a ROPE may be prior-driven rather than evidence-driven. Required future checks (not calculated now):

```text
prior probability mass below epsilon_n
posterior probability mass below epsilon_n
prior-to-posterior change
stability across proper prior variants
coverage and calibration under synthetic n values
```

## 19. Reporting Boundary

Until NUM-DEC-07 is reopened, the following labels are **prohibited**:

```text
PRACTICALLY_ZERO_EXCITATION
NEGLIGIBLE_EXCITATION
SUBSTANTIVELY_MEANINGFUL_EXCITATION
ROPE_SUPPORTED
ROPE_REJECTED
```

Allowed reporting remains:

```text
EXCITATION_SUPPORTED
NO_EXCITATION_SUPPORTED
INCONCLUSIVE
```

plus conditional magnitude summaries under `M1` (e.g., posterior mean/interval for `n`) that do not attach a practical-significance label.

## 20. Required Future Tests

Record but do not execute:

```text
M3-ROPE-001: M3 can execute without a ROPE definition.
M3-ROPE-002: Exact-null decisions do not depend on epsilon_n.
M3-ROPE-003: Tau calibration does not depend on epsilon_n.
M3-ROPE-004: Posterior magnitude is reported conditional on M1.
M3-ROPE-005: P(M0 | Y) is not replaced by P(n <= epsilon_n | Y, M1).
M3-ROPE-006: No numerical epsilon_n is silently introduced.
M3-ROPE-007: No tau value is reused as epsilon_n.
M3-ROPE-008: No historical-data fit is used to determine epsilon_n.
M3-ROPE-009: No verbal practical-significance label appears without an approved epsilon_n.
M3-ROPE-010: Any future epsilon_n has explicit provenance.
M3-ROPE-011: Any future predictive-effect metric has an explicit formula.
M3-ROPE-012: Any future decision-theoretic loss is versioned.
M3-ROPE-013: Prior mass below epsilon_n is disclosed if ROPE is reopened.
M3-ROPE-014: Posterior sensitivity to internal priors is evaluated if ROPE is reopened.
M3-ROPE-015: Synthetic calibration covers values below, near, and above epsilon_n if ROPE is reopened.
M3-ROPE-016: The first amended recovery tournament does not require a ROPE to complete.
```

## 21. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```

No ROPE code is written, and no M3 source file is modified or created by this adjudication.

## 22. Calibration Nonauthorization

```text
CALIBRATION: NOT_AUTHORIZED
```

No synthetic calibration run of any kind — for `epsilon_n`, `tau`, or otherwise — occurs as part of producing this adjudication.

## 23. Tournament Nonauthorization

```text
TOURNAMENT EXECUTION: NOT_AUTHORIZED
```

No recovery tournament execution occurs as part of producing this adjudication.

## 24. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```

No historical data file is read, written, or referenced by this adjudication, and no basis for `epsilon_n` may ever be derived from the historical fit.

## 25. Decision Summary

```text
NUM-DEC-07:                    DEFERRED
Selected option:                NO_ROPE_VALUE_SELECTED
epsilon_n:                      UNSPECIFIED (not zero, not any other value -- genuinely unresolved)
ROPE status:                    OPTIONAL_SUPPLEMENTARY_MAGNITUDE_DIAGNOSTIC
Excitation-existence rule:      M0 versus M1 model comparison (P(M1|Y) vs tau, NUM-DEC-04) -- ROPE is never a substitute
First-tournament dependency:    NOT_REQUIRED
Reopening conditions:           A) literature  B) predictive-effect calibration  C) decision-theoretic loss
                                 D) comparative benchmark  E) explicit researcher policy -- never the historical fit
Relationship to NUM-DEC-04:     does not alter the tau grid, FPR target, FNR/power requirement, or INCONCLUSIVE outcome
Relationship to NUM-DEC-05:     epsilon_n not derived from model prior odds
Relationship to NUM-DEC-06:     epsilon_n not derived from Bayes-factor level
Prohibited labels until reopened: PRACTICALLY_ZERO_EXCITATION, NEGLIGIBLE_EXCITATION,
                                 SUBSTANTIVELY_MEANINGFUL_EXCITATION, ROPE_SUPPORTED, ROPE_REJECTED
Required future tests:          16 (M3-ROPE-001..016)
Implementation authorized:      NO
Calibration authorized:         NO
Tournament execution authorized: NO
Historical fit authorized:      NO
Remaining pending:              NUM-DEC-08
```

```text
MODEL_3B_NUM_DEC_07_M3_ROPE_DEFERRED
```
