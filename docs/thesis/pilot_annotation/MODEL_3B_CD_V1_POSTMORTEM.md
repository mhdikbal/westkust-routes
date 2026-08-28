> **PHASE A: V1 POSTMORTEM**
> **MODEL 3B-CD V1 REMAINS CLOSED**
> **NO SIMULATION RUN, NO V1 REPAIR, NO REAL-DATA FITTING IN THIS PHASE**
> **DIAGNOSIS ONLY — NOT A V2 DESIGN DOCUMENT**

---

## 1. Scope

This report diagnoses why `MODEL_3B_CD_V1` failed its preregistered simulation-recovery validation. It uses **only already-existing artifacts** — no simulation was rerun, no source file was modified, no numerical gate was changed, and no historical event was fit. Inputs (per `MODEL_3B_POSTMORTEM_AND_ALTERNATIVE_TEST_PLAN.md` §8):

- `MODEL_3B_CD_MASTER_BLUEPRINT.md`
- `MODEL_3B_CD_FINAL_1000_RECOVERY_AUDIT.md`
- `MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md`
- `MODEL_3B_CD_SIMULATION_CELL_MANIFEST.md`
- `MODEL_3B_CD_PILOT_100_AUDIT.md`
- `MODEL_3B_CD_INSTRUMENTATION_PILOT_10x10_AUDIT.md`
- the final-run aggregate outputs, failure logs, and gate evaluations referenced by the recovery audit

This is a diagnosis of **why V1 failed**, not a design proposal for what replaces it. No V2 parameter, transform, or estimator choice is authorized or implied here (plan §4.4, §40).

## 2. Frozen V1 Status

```text
MODEL_3: RETAINED_AS_POOLED_EXPLORATORY_BASELINE
MODEL_3B_CD_V1: CLOSED_AFTER_FAILED_RECOVERY_VALIDATION
SIMULATION_RECOVERY_V1: FAILED
REAL_DATA_FITTING_V1: NOT_AUTHORIZED
HISTORICAL_MECHANISM_INFERENCE: PROCESS_TRACING_ONLY
GRAPH_OUTPUT: CURRENT
```

Nothing in this report changes these statuses. They are read here, not decided here.

## 3. Technical Defects

**Exactly one technical defect was found, confined to one cell.**

`S4-G1` stopped at replicate 301/1,000 (300/1,000 completed) after an unhandled `OverflowError: math range error` raised inside `likelihood.py:91` (`math.exp(theta0 + theta1 * x_CD)`), called from `estimate.py`'s own point-estimation objective (`fit_m3b_cd`'s internal `neg_ll` — not the `inference.py` wrapper, which only catches `ValueError`) during an L-BFGS-B finite-difference gradient probe. No other cell crashed; no other unhandled exception occurred across 9,300 completed replicates and 27,900 completed fits.

**Retrospective signal already visible at pilot scale**: `MODEL_3B_CD_PILOT_100_AUDIT.md` §3.2 flagged, at n=100, that S4-G1 (the smallest nonzero `alpha_true`, `0.1×` production) already produced 2/100 replicates with `beta_hat` pinned at the optimizer's lower bound, yielding branching-ratio artifacts of ~5,369 and ~4,078. This was reported then as an outlier/artifact concern, not classified as a defect risk — in hindsight, it was the same instability surface that produced the final run's crash at n=1,000. This is documented as a missed early signal, not re-litigated as a new finding.

**Status**: `TECHNICAL_DEFECT`, `SEPARATE_FROM_GLOBAL_STATISTICAL_FAILURE` (plan §4.1). Per plan §11 and the researcher's explicit instruction, this defect is **not repaired in this phase**.

## 4. Statistical Recovery Failures

Independent of the S4-G1 defect, the 9 cells that completed in full (9,000 sequences, 27,000 fits) failed multiple preregistered hard gates with high statistical precision (n=1,000/cell — not sampling noise):

| Gate | Threshold | Result |
|---|---|---|
| False-positive excitation (S1×3) | ≤0.05 | **FAIL** — 7.3%–9.6% |
| Relative bias alpha/beta (core, α_true>0) | ≤0.10 | **FAIL** — ~13%–35% |
| Branching-ratio absolute/relative bias | ≤0.05 / ≤0.10 | **FAIL** — median-robust underrecovery 16%–18% |
| 95% CI coverage, alpha/beta | 0.925–0.975 | **FAIL** — actual 60%–84% |
| Correct-model-selection rate (S3/S5/S6, true=M3B-CD) | ≥0.80 | **FAIL** — AIC 15.6%–19.2%, BIC 2.2%–3.7% |
| Convergence rate | ≥0.95 | PASS (0.999–1.0) |
| Production-scenario power (S3-G1) | ≥0.80 | PASS (0.985) |
| Normalized absolute bias theta0 | ≤0.25 | PASS (0.002–0.078, core cells) |
| Sign recovery (alpha) | ≥0.95 | PASS (0.994–0.999) |

These failures recur across independent, differently-parameterized core cells (S2, S3, S5, S6) — not an artifact of one grid point.

## 5. Inference Failures

Distinct from point-estimate bias, the **uncertainty quantification itself** is unreliable wherever `alpha_true>0`:

- Wald 95% CI coverage for alpha/beta is 60%–84% against a nominal 92.5%–97.5% target — the confidence interval, built from the finite-difference Hessian at the MLE, systematically fails to bracket the true value at anywhere near its nominal rate.
- Coverage for `theta0`/`theta1` is comparatively well-calibrated (0.94–0.99 across cells) — the inference failure is specific to `alpha`/`beta`, not the instrumentation pipeline in general (the same Hessian/covariance code produces correct coverage for the density parameters).
- `MODEL_3B_CD_PILOT_100_AUDIT.md` §4 already flagged, before the final run, that interval coverage was `NOT_ESTIMABLE` from the 100-replicate pilot's estimator scope — the final run closed that instrumentation gap (Fase 3A/3B) and the resulting, now-computable coverage number is itself the failure.
- The branching-ratio delta-method CI inherits the same undercoverage problem, compounded by the `alpha/beta` ratio's sensitivity to near-boundary `beta_hat` values (§3, §6).

## 6. Model-Selection Failures

The single most consequential finding of the final run: **when the true generating process is M3B-CD (density + self-excitation jointly present), AIC and BIC overwhelmingly select the simpler M1 (pure Hawkes, no density term) instead.**

| Cell | Correct model | AIC correct-rate | BIC correct-rate |
|---|---|---:|---:|
| S3-G1 | m3b_cd | 16.8% | 3.1% |
| S5-G1 | m3b_cd | 15.6% | 2.2% |
| S6-G1 | m3b_cd | 19.2% | 3.7% |

810–820 of 1,000 replicates per cell are misclassified as M1. This holds despite `theta1`'s own point estimate being comparatively well-behaved in isolation (§4) — the failure is specifically in the model-comparison step, where AIC/BIC's complexity penalty outweighs the marginal likelihood gain from adding the density term once self-excitation is already present. `theta1`-`alpha` correlation (Gate C) was checked and is **not** the mechanism (S3: 0.003, S5: 0.019 — both far under the 0.70 identifiability-risk threshold), so this is not a collinearity problem; it is a genuine power problem in distinguishing the two nested-but-different processes via information criteria at this sample-size/effect-size regime. Both stress cells (S7, S8) show the *same* pattern despite being deliberately misspecified — suggesting this is a general property of the framework, not specific to correct specification (recovery audit §20).

## 7. Parameterization Risks (alpha-beta)

V1 estimates `alpha` and `beta` as separate free parameters and forms `branching_ratio = alpha/beta` post hoc. Several independent lines of evidence in this postmortem point to this choice as a contributing structural weakness, not merely an estimation-noise artifact:

1. **Near-boundary beta collapse.** Both the pilot-100 (S4-G1, 2/100 replicates) and final-1000 runs (S1: 5–6/1,000 replicates; S2/S3/S5: 1–2/1,000) show a recurring minority of replicates where `beta_hat` converges near the optimizer's lower bound, making `alpha/beta` numerically explode. This is a symptom of the unconstrained ratio parameterization, not of the underlying process.
2. **Systematic, not just noisy, branching-ratio bias.** The *median* (outlier-robust) branching ratio is 16%–18% below truth in every correctly-specified core scenario — a stable, reproducible shift, not merely inflated variance from the ratio construction.
3. **The S4-G1 crash occurred in exactly the regime** (`theta1=0.3`, `alpha=0.04207` — the smallest nonzero alpha and largest theta1 among all 10 cells) where the alpha-beta parameterization's boundary sensitivity is most acute.

Whether a constrained/transformed parameterization (e.g. `branching_ratio n` × `beta`, or log/logit transforms — plan §4.4, §40) would resolve this is **not evaluated here** and is explicitly out of scope for this phase; it is recorded as a candidate question for Phase E, not a recommendation.

## 8. Branching-Ratio Under-Recovery (cross-referenced with §4/§7)

Consistent across three independent measurement points:

| Stage | n/cell | Core-scenario median relative bias |
|---|---:|---|
| Pilot 100 (`MODEL_3B_CD_PILOT_100_AUDIT.md` §3.2) | 100 | ~13%–20% (S2/S3/S5/S6) |
| Pilot 10×10 (`MODEL_3B_CD_INSTRUMENTATION_PILOT_10x10_AUDIT.md` §14/§17) | 10 | directionally consistent, flagged `PRELIMINARY_WARNING` |
| Final 1,000 (`MODEL_3B_CD_FINAL_1000_RECOVERY_AUDIT.md` §17) | 1,000 | 16%–18% (median-robust, S2/S3/S5/S6) — CONFIRMED |

This is not a sampling artifact of any one run; it reproduced at three separate scales with the same sign and similar magnitude before it was formally confirmed.

## 9. False-Positive Excitation

`S1-G1/G2/G3` (ground truth `alpha=0`, testing whether the estimator spuriously detects excitation from density-only data) show a boundary-aware LR-test rejection rate of 7.3%–9.6% against a preregistered ≤5% target — roughly 1.5×–2× the nominal rate, consistent across all three `theta0` grid points at n=1,000 (recovery audit §14). The boundary-aware Self & Liang (1987) test itself was independently re-verified correct (label and LR-formula match in 9,300/9,300 replicates) — the elevated rate is a property of the estimator's finite-sample behavior at this boundary, not a bug in the test.

## 10. Source Circularity (structural risk, not measured in V1)

V1's simulation-recovery study never tested — and could not test — whether the 141 real historical events are circularly dependent on the same Corpus Diplomaticum series used as the density covariate. This is a **separate, pre-existing structural risk** documented in `MODEL_3B_CD_MASTER_BLUEPRINT.md` §4/§5.4/§17 ("CD bukan exposure eksogen murni") and is exactly what Phase B of the postmortem-and-alternative-test plan is designed to audit. It is listed here because it independently blocks real-data fitting even in a hypothetical world where V1 had passed every recovery gate — the simulation-recovery failure (§4–§9) and the source-circularity risk (§10) are two separate reasons real-data fitting is not authorized, not one reason stated twice.

## 11. What V1 Does and Does Not Establish

**V1 established:**
1. The full engineering pipeline (simulate → persist → fit M1/M2/M3B-CD → instrument → checkpoint → audit) works reproducibly at scale (9,300/9,300 checksum-valid sequences, 0 duplicate seeds/IDs, 0 nonfinite/out-of-window events, 0 boundary-test label or LR-formula errors).
2. Event-sequence persistence and statistical instrumentation (Hessian, covariance, SE, CI, boundary-aware LR test, AIC/BIC, branching-ratio delta method) are implemented correctly and function as designed.
3. The V1 model specification, as estimated, fails multiple preregistered statistical recovery gates.
4. The failure is not caused solely by the S4-G1 defect (§3–§9 hold independent of it).
5. Nine independently-parameterized completed cells show consistent failures in false-positive control, parameter recovery, CI coverage, branching-ratio recovery, and model selection.
6. Fitting V1 to the 141 historical events was correctly withheld.

**V1 did NOT establish:**
1. That all archival-density controls are impossible.
2. That every Hawkes reformulation will fail.
3. That temporal clustering in the 141-event dataset is entirely an archival artifact.
4. That temporal clustering is historically causal.
5. That a new model may be fitted without a new validation design.
6. Anything about source circularity between CD and the 141-event dataset (§10 — untested by V1).

## 12. Questions V1 Cannot Answer

1. Whether the branching-ratio underrecovery (§8) and CI undercoverage (§5) are caused by the alpha-beta parameterization specifically, versus a more fundamental identifiability limit of this data regime.
2. Whether a constrained/transformed parameterization, profile likelihood, or bootstrap CI would resolve the inference failures (§5, §7) — untested, out of scope for V1.
3. Whether the model-selection failure (§6) is specific to AIC/BIC, or would persist under a different comparison procedure (e.g. a formal LR test between M1 and M3B-CD, which V1's boundary-aware test already partially provides for the alpha=0 null but was not used as the primary model-selection criterion).
4. Whether the 141 real historical events are circularly dependent on CD (§10) — requires Phase B, not answerable from V1's simulation-only evidence.
5. Whether residual temporal clustering survives conditioning on documentation density at all, independent of a full Hawkes parameterization — this is Phase D's question, deliberately designed to not require stable alpha/beta estimation.

## 13. Requirements for Alternative Tests

Based on the failure taxonomy above, any alternative test approach (Phases B–E) should:

1. Not require stable point estimation of `alpha`/`beta` under the current parameterization, given §5/§7's demonstrated fragility (favors Phase D's density-only-null clustering test over an immediate V2 Hawkes refit).
2. Separately establish event-source independence from CD (§10) before any density-covariate approach is reused, since a circularity-tainted covariate would undermine even a statistically well-behaved estimator.
3. If a future V2 Hawkes model is considered, treat parameterization (§7), CI methodology (§5), and model-selection procedure (§6) as three separately-diagnosed risks requiring their own preregistered remedies — not one generic "redo the fit" fix.
4. Preserve the false-positive finding (§9) as a reason to preregister the null-hypothesis test procedure for any future excitation claim, rather than relying on a point estimate's sign or magnitude alone.

## 14. V2 Prohibited Actions

Per the governing plan (§18, §40, §49) and reaffirmed here:

- Do not repair or rerun V1.
- Do not alter V1's numerical gates, manifest, or cell parameters.
- Do not fit V1 (or any undeclared "V1.1") to the 141 real historical events.
- Do not begin implementing any V2 candidate feature (direct n-beta parameterization, log/logit transforms, profile likelihood, bootstrap CI, Bayesian inference, explicit observation model, etc. — plan §40) in this phase or without a separate go decision (Phase E).
- Do not treat this postmortem's diagnostic findings as a V2 specification — they are failure classification, not design.

## 15. Researcher Decisions Required

1. Whether to proceed to **Phase B** (141-event source provenance and circularity audit) as the plan's recommended next step (§45), given it is independent of any V2 decision and useful even if no V2 is ever built.
2. Whether the alpha-beta parameterization risk (§7) and model-selection failure (§6) should be treated as reasons to prefer **Phase D**'s density-only-null clustering test (which sidesteps both) over a Hawkes-based V2 candidate, when Phase E is eventually reached.
3. Whether the S4-G1 defect (§3) warrants a documented, standalone bug report for future reference, independent of any V1 repair (which remains prohibited).
4. How the false-positive finding (§9) should be weighed against the branching-ratio and model-selection findings (§6, §8) when framing the thesis's methodological narrative — i.e., whether "the model cannot reliably distinguish the two hypotheses" (§6) is the primary framing, with the other findings as supporting detail, or whether all findings should be presented with equal weight.

---

**STOP** — Phase A postmortem complete. No simulation was run, no V1 file was modified, no gate was changed, no dataset was altered, and no 141-event fitting was performed. Not proceeding to Phase B, Graphify, or Git in this turn.
