# WAVE 2 Tau Calibration Preregistration (W2-P7)

> **Status: PLANNING-ONLY. No tau value is selected. No calibration is run.** This document preregisters the *procedure* by which a future, separately authorized calibration turn will select tau — it is not that turn.

## 1. Status of Tau (must not be altered by this document)

```text
Procedure resolved by NUM-DEC-04
Final numeric value: pending calibration
```

All four gate rows in `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv` that reference tau must continue to read exactly:

```text
PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION
```

Mechanically confirmed unchanged (0 diff) in `WAVE_2_CROSS_DOCUMENT_CONSISTENCY_AUDIT.md`.

## 2. Decision Rule (RESOLVED_BY_FROZEN_SPEC as a formula; not evaluated here)

```math
\text{select } M_1 \quad\text{if}\quad P(M_1\mid Y)\geq\tau.
```

Relationship to the Bayes factor:

```math
BF_{10}\geq\frac{\tau}{1-\tau}\frac{P(M_0)}{P(M_1)} \xrightarrow{\text{equal odds}} BF_{10}\geq\frac{\tau}{1-\tau}.
```

**Illustrative check only, not a recommendation and not adopted:**

```math
\tau=0.90 \Rightarrow BF_{10}\geq9, \qquad \tau=0.95 \Rightarrow BF_{10}\geq19.
```

These two numbers exist in this document solely to verify the formula is internally consistent; no downstream artifact may cite them as a chosen threshold. (Mechanically checked in `WAVE_2_CROSS_DOCUMENT_CONSISTENCY_AUDIT.md` that no file states "tau = 0.90" or "tau = 0.95" as an adopted value.)

## 3. Null False-Selection Rate (formula only)

```math
Y_0^{(r)}\sim M_0, \qquad \widehat{\operatorname{FSR}}_0(\tau)=\frac{1}{R_0}\sum_{r=1}^{R_0}\mathbf 1\left\{P(M_1\mid Y_0^{(r)})\geq\tau\right\}.
```

## 4. Detection Probability (formula only)

```math
Y_j^{(r)}\sim M_1(\theta_j), \qquad \widehat{\operatorname{DP}}_j(\tau)=\frac{1}{R_j}\sum_{r=1}^{R_j}\mathbf 1\left\{P(M_1\mid Y_j^{(r)})\geq\tau\right\}.
```

`FSR_0` and `DP_j` are formally distinct from M2's own `FailureRate_c`/`Coverage_c` — do not conflate the two frequentist evaluation families (M2 recovery diagnostics vs. M3 model-selection operating characteristics).

## 5. Candidate Constrained Rule (formula only, never executed)

```math
\tau^*=\inf\left\{\tau:\widehat{\operatorname{FSR}}_0(\tau)\leq\alpha_{\mathrm{target}}\right\}.
```

`tau*` is a *candidate* rule, not a decision. `alpha_target` is itself unselected (`OD-013`).

## 6. Preregistration Checklist (all `OPEN_REQUIRES_ADJUDICATION`, per `WAVE_2_OPEN_DECISION_LEDGER.csv` `OD-013`)

```text
[ ] alpha_target (null false-selection-rate target)
[ ] candidate tau grid
[ ] alternative grid (for sensitivity)
[ ] prior-odds sensitivity grid (reuses NUM-DEC-05's {0.75/0.25, 0.50/0.50, 0.25/0.75})
[ ] Monte Carlo precision target
[ ] number of replications (R_0, R_j per alternative setting)
[ ] handling of computational failures (reuses TAU_CALIBRATION_UNRESOLVED taxonomy code)
[ ] objective function (e.g. FSR-constrained maximize DP, vs. a joint loss)
[ ] tie-breaking rule
[ ] stability criterion (across seeds, across the 3 prior-odds scenarios)
[ ] independent confirmation method (calibration set vs. evaluation set, per NUM-DEC-04)
```

No item on this checklist may be filled in during a planning-only turn. **No final tau value is selected in this document.**

## 7. Dependency on Prior Stages

Tau calibration cannot proceed until, in order:

```text
1. M3 exact-null representable (M3-BLOCK-01 closed)
2. internal priors frozen (M3-BLOCK-02/06 closed)
3. Jacobian-correct posterior sampling validated (M3-BLOCK-03 closed)
4. bridge sampling validated (M3-BLOCK-04 closed)
5. TI cross-check satisfactory on the validation subset (M3-BLOCK-05 closed)
6. calibration/evaluation seed separation implemented (M3-BLOCK-07 closed)
7. prior model odds frozen (already true: NUM-DEC-05, RESOLVED_BY_FROZEN_SPEC)
```

Six of these seven preconditions are currently unmet (blockers 1–7 except the already-resolved prior-odds condition). This preregistration therefore documents the *procedure* a future calibration turn will follow once those preconditions are independently closed — it does not shorten that dependency chain.

## 8. Explicit Non-Selection Statement

```text
FINAL TAU VALUE:      NOT SELECTED
CALIBRATION EXECUTED: NO
HISTORICAL DATA USED: NO
```
