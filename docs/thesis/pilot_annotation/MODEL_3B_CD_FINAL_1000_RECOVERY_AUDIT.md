> **FINAL SIMULATION-RECOVERY AUDIT**
> **10 CELLS x 1,000 REPLICATES (PLANNED) — 9 CELLS COMPLETED, 1 CELL STOPPED BY IMPLEMENTATION DEFECT**
> **NUMERICAL GATES PRE-SPECIFIED**
> **REAL-DATA FITTING NOT AUTOMATICALLY AUTHORIZED**
> **RESEARCHER DECISION REQUIRED**

---

## 1. Scope

Final simulation-recovery run per `MODEL_3B_CD_FINAL_1000_EXECUTION_PLAN.md`, authorized by the researcher after approving runtime/storage/worker budget. Planned: 10 frozen cells × 1,000 replicates = 10,000 sequences × 3 models (M1/M2/M3B-CD) = 30,000 fits, 4 workers, cell-level parallelism, 100-replicate chunking with checkpoints.

**Actual outcome: 9 of 10 cells completed in full (9,000 sequences, 27,000 fits). The 10th cell (S4-G1) stopped at replicate 301/1,000 (300 completed, 900 fits) after an unhandled `OverflowError` inside the audited `estimate.py`/`likelihood.py` optimizer path — a genuine implementation defect, not a statistical result.** No auto-fix, no retry, and no source change were applied, per the plan's explicit prohibition. This report evaluates gates on the 9 completed cells and reports S4-G1 as incomplete/blocked.

## 2. Blueprint Compliance

- Read: `MODEL_3B_CD_MASTER_BLUEPRINT.md`, `MODEL_3B_CD_FINAL_1000_EXECUTION_PLAN.md`, `MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md`, `MODEL_3B_CD_SIMULATION_CELL_MANIFEST.md`, `MODEL_3B_CD_PILOT_100_AUDIT.md`, `MODEL_3B_CD_INSTRUMENTATION_PILOT_10x10_AUDIT.md` before execution.
- 10 frozen cells used exactly as manifested; no cell added/removed, no parameter/transform/kernel changed, no grid point added, no recalibration from pilot results.
- No real 141-event fitting. No Graphify during the run. No commit/push during the run.
- Cell manifest checksum used for provenance: `5a0354f241e03c9259e22697b5bf4548cf35db6b0fd1a75ccf4dbdc738360ecb`. Numerical-gate plan checksum: `527bd70d5852e972263fbd1e4e7e80d7a000d1e744f38ed9ca7b2056d3e0a106`. Density checksum: `e0b8ab7c78104e89f39a15b2e55b0b96c6b055efe273fbfc8a0fc9f1d0f5e04a` (unchanged throughout — verified before and confirmed by 9,300/9,300 valid event-time checksums after).

## 3. Preflight

All 20 guards passed before authorization (reported and approved in the prior turn): HEAD/origin sync (`f351e71`), simulator/instrumentation/persistence commit match, 115/115 unit tests, density checksum match, clean output directory, no competing process, source clean, gitignore coverage, seed ledger (10,000 planned unique seeds, generated and asserted collision-free before run start), disk space (938 GB free vs ~118 MB required), researcher-approved runtime/storage/worker budget, Graphify current, explicit researcher authorization phrase received.

## 4. Runtime and Storage Budget — Planned vs. Actual

**Planned** (from pilot-10×10 extrapolation, approved by researcher): ≈2.16 h serial, ≈33.8 min at 4 workers.

**Actual**: total wall time from launch to termination ≈ **2h17m (≈8,220 s)** — substantially longer than the approved 33.8-minute projection. Root cause, confirmed from measured per-replicate runtimes: **4-way CPU contention on a 4-core machine (`nproc=4`)**. The pilot's per-replicate timings were measured with a single serial process (no contention); the final run's actual per-replicate cost measured under real 4-worker concurrent load was **3.5×–4.3× higher** than the pilot projection (e.g. S7-G1: 1.858 s → 6.432 s/replicate; S8-G1: 0.804 s → 3.49 s/replicate). This inflation also **reordered the bottleneck**: worker 3 (S8-G1→S2-G1→S1-G1) became the longest-running worker (7,112 s) rather than worker 0 (S7-G1 alone, 6,452 s), reversing the pre-run projection. This is a runtime-estimation gap, not a correctness defect — flagged explicitly for any future run's budget planning (recommend re-deriving per-replicate cost from a small *concurrent* pilot, not a serial one).

Per-worker actual:

| Worker | Cells | Runtime | Peak RSS |
|---|---|---:|---:|
| 0 | S7-G1 | 6,451.7 s | 106.7 MB |
| 1 | S3-G1, S1-G3, S1-G2 | 7,065.9 s | 105.7 MB |
| 2 | S5-G1, S6-G1, S4-G1 | **crashed during S4-G1** (S5/S6 completed) | not logged (crash pre-empted final log write) |
| 3 | S8-G1, S2-G1, S1-G1 | 7,112.1 s | 106.0 MB |

Sum of all completed per-replicate runtimes: 27,446.8 s (across 9,300 sequences); memory: peak RSS per worker stayed at **≈105–107 MB**, far under the pre-run conservative <500 MB estimate — memory was never a constraint.

Output size: 64 MB actual (vs. ≈59–118 MB projected) — within budget.

## 5. Seed Ledger

10,000 unique seeds generated and asserted collision-free (`base_seed + replicate_id`, base offsets 90,000,000/90,100,000/…/90,900,000, disjoint from Pilot 100 and Pilot 10×10 ranges) before the run started (`manifests/seed_ledger.json`). Of these, **9,300 were consumed** (9,000 for the 9 completed cells + 300 for S4-G1 before it stopped). Verified independently from every completed record: **0 duplicate seeds, 0 duplicate replicate IDs** across all 9,300 records re-scanned post-hoc.

## 6. Checkpoint and Resume Integrity

All 9 completed cells: 10/10 chunks each, every `checkpoint_chunk_NN.json` present with `status: "ok"`. S4-G1: 3/10 chunks written and checkpointed (`status: "ok"` for chunks 1–3, replicate IDs 1–300 contiguous, no gaps); chunk 4 was **not written** — the crash occurred on the first replicate of chunk 4 (replicate 301), before that chunk's output was flushed, so no partial/corrupt chunk file exists (fails safely: nothing after replicate 300 was persisted). Resume was not exercised in this run (no restart occurred); the checkpoint state left behind is consistent with what a resume would need (last completed chunk = 3, next replicate ID = 301) — actually restarting S4-G1 is a decision item for §23/§25, not carried out here.

## 7. Event-Sequence Integrity

Re-verified independently (not trusting the run's own in-process check) by recomputing SHA-256 of every stored `event_times` array from all 9,300 completed records: **9,300/9,300 checksum matches (100%)**. 0 nonfinite event times, 0 events outside `[1600, 1784)`, 0 duplicate seeds/replicate IDs. Density checksum unchanged throughout.

## 8. Cell-by-Cell Technical Results

| cell_id | completed | checksum-valid | convergence (M1/M2/M3B-CD) | covariance-valid (M1/M2/M3B-CD) | mean n_events |
|---|---:|---:|---|---|---:|
| S1-G1 | 1000/1000 | 100% | 1.0/1.0/1.0 | 0.931/1.0/0.585 | 27.8 |
| S1-G2 | 1000/1000 | 100% | 1.0/1.0/1.0 | 0.868/1.0/0.682 | 55.7 |
| S1-G3 | 1000/1000 | 100% | 1.0/1.0/1.0 | 0.753/1.0/0.769 | 111.1 |
| S2-G1 | 1000/1000 | 100% | 1.0/1.0/1.0 | 0.994/1.0/0.997 | 109.5 |
| S3-G1 | 1000/1000 | 100% | 1.0/1.0/1.0 | 0.988/1.0/0.999 | 129.0 |
| **S4-G1** | **300/1000** | 100% (of the 300) | 1.0/1.0/1.0 (of the 300) | 0.853/1.0/0.813 (of the 300) | 82.5 |
| S5-G1 | 1000/1000 | 100% | 1.0/1.0/1.0 | 0.993/1.0/0.998 | 110.2 |
| S6-G1 | 1000/1000 | 100% | 1.0/0.999/1.0 | 0.994/1.0/0.999 | 129.2 |
| S7-G1 | 1000/1000 | 100% | 1.0/0.999/1.0 | 0.995/1.0/1.0 | 239.1 |
| S8-G1 | 1000/1000 | 100% | 1.0/1.0/1.0 | 1.0/1.0/1.0 | 169.2 |

S1-G1/S1-G3 show reduced M3B-CD covariance-valid rates (58.5%/76.9%) — the same alpha-boundary phenomenon flagged at n=10 in the 10×10 pilot (`alpha_true=0`), now confirmed at full precision: it is a structural feature of estimating at a parameter-space boundary, not an implementation defect (manifest §2 poin 2).

## 9. M1 Recovery

Convergence 0.999–1.0 across all cells; not the primary recovery target (M1 is the restricted/comparison model except where it is itself the truth, S2-G1).

## 10. M2 Recovery

Convergence 0.999–1.0; correct-model-selection target for S1-G1/G2/G3 (see §18).

## 11. M3B-CD Recovery — Parameter Bias (mean-based, as pre-registered)

| cell | theta0 norm.abs.bias (≤0.25) | theta1 rel.bias (≤0.10) | alpha rel.bias (≤0.10) | beta rel.bias (≤0.10) |
|---|---:|---:|---:|---:|
| S1-G1 | 0.057 PASS | 0.056 PASS | N/A (α_true=0) | 6.643 — outlier-dominated (§17) |
| S1-G2 | 0.065 PASS | 0.113 **FAIL** | N/A | 12.53 — outlier-dominated |
| S1-G3 | 0.078 PASS | −0.036 PASS | N/A | 4.960 — outlier-dominated |
| S2-G1 | 0.002 PASS | N/A (θ1_true=0) | −0.350 **FAIL** | −0.132 **FAIL** |
| S3-G1 | 0.023 PASS | −0.059 PASS | −0.330 **FAIL** | −0.169 **FAIL** |
| S5-G1 | 0.017 PASS | −0.537 **FAIL** (θ1_true=0.01, tiny denominator) | −0.349 **FAIL** | −0.144 **FAIL** |
| S6-G1 | 0.015 PASS | −0.128 **FAIL** | −0.326 **FAIL** | −0.140 **FAIL** |

theta0 recovery is uniformly excellent across all core cells (well inside the ≤0.25 gate). **theta1 recovery is largely acceptable except where the true value is near zero** (S5-G1) or where sampling noise crosses the 10% line narrowly (S1-G2, S6-G1). **Alpha and beta relative bias fail the ≤0.10 gate in every core scenario where alpha_true>0** — this is the dominant, robust finding of this run (see §17 for the outlier-vs-median analysis, which confirms this is a real, not purely outlier-driven, systematic downward bias).

## 12. Covariance and CI Results

95% Wald CI coverage (target 0.925–0.975):

| cell | theta0 | theta1 | alpha | beta |
|---|---:|---:|---:|---:|
| S1-G1 | 0.978 (slightly high) | 0.974 PASS | 1.000 (at α=0 boundary, uninformative) | 0.957 PASS |
| S1-G2 | 0.978 | 0.979 (slightly high) | 1.000 | 0.952 PASS |
| S1-G3 | 0.990 (high) | 0.984 (high) | 0.997 | 0.967 PASS |
| S2-G1 | 0.940 PASS | 0.950 PASS | **0.597 FAIL** | **0.829 FAIL** |
| S3-G1 | 0.949 PASS | 0.957 PASS | **0.617 FAIL** | **0.826 FAIL** |
| S5-G1 | 0.939 PASS | 0.954 PASS | **0.605 FAIL** | **0.824 FAIL** |
| S6-G1 | 0.952 PASS | 0.952 PASS | **0.632 FAIL** | **0.843 FAIL** |

theta0/theta1 CIs are reasonably calibrated (occasionally over-covering for S1, which is conservative, not a failure direction the gate penalizes). **Alpha and beta Wald CIs severely undercover** (60–84% actual vs. 92.5–97.5% nominal) in every core alpha>0 scenario — directly consistent with the systematic negative bias in §11: the true value is often outside a CI centered on a biased point estimate.

## 13. Boundary-Aware Alpha Test

100% correct M2-vs-M3B-CD labeling, 0 LR/manual-recomputation mismatches, across all 9,300 completed replicates (re-verified independently, not just trusting in-run flags).

## 14. False-Positive Excitation (Gate B poin 1, S1 cells)

| cell | reject-H0 rate at α=0.05 (target ≤0.05) |
|---|---:|
| S1-G1 | 0.087 **FAIL** |
| S1-G2 | 0.073 **FAIL** |
| S1-G3 | 0.096 **FAIL** |

All three S1 grid points show a false-positive rate of the boundary-aware LR test roughly **1.5×–2× the nominal 5%** — a consistent, well-powered (n=1000/cell) finding, not sampling noise.

## 15. Power (production-scenario, S3-G1)

S3-G1 reject-H0 rate = **0.985** (target ≥0.80) — **PASS**, and consistently high across all alpha>0 cells (S2: 0.975, S5: 0.978, S6: 0.983, S7: 1.000, S8: 1.000). Power is not the weak point of this framework — specificity (§14) and point-estimate calibration (§11–12) are.

## 16. Parameter Bias and RMSE

See §11 (bias) and §17 (RMSE/outlier diagnosis). Normalized RMSE for alpha/beta (target ≤0.20) fails in every alpha>0 core cell (range ≈0.31–0.73 on median-clean re-analysis, before outlier inflation) — consistent with the bias finding, not a separate defect.

## 17. Branching-Ratio Recovery — Mean vs. Median (critical diagnostic)

The pre-registered statistic (mean-based) is **outlier-dominated** in every cell: a small number of replicates (S1: 3–5 per cell; S2/S3/S5: 1–2; S6/S7/S8: 0–1, out of 1000) converge to a near-zero `beta_hat` (< 0.05, vs. true 0.6215), which makes `alpha/beta` numerically explode (means as high as 48.8 for S1-G1, against a true value of 0.0). This is **not** the same phenomenon as the already-documented alpha-boundary pile-up (§8) — it is a small number of pathological optimizer outcomes on the *beta* dimension.

Median-based (outlier-robust) branching-ratio recovery:

| cell | true br | median br | mean br (outlier-dominated) | outliers (br>5 / beta<0.05) |
|---|---:|---:|---:|---:|
| S1-G1 | 0.000 | 0.000 | 48.76 | 5 / 6 |
| S1-G2 | 0.000 | 0.000 | 21.10 | 3 / 6 |
| S1-G3 | 0.000 | 0.000 | 23.63 | 5 / 10 |
| S2-G1 | 0.677 | 0.557 (−18%) | 9.87 | 1 / 1 |
| S3-G1 | 0.677 | 0.570 (−16%) | 8.78 | 1 / 2 |
| S5-G1 | 0.677 | 0.560 (−17%) | 7.31 | 1 / 2 |
| S6-G1 | 0.677 | 0.567 (−16%) | 0.55 | 0 / 1 |
| S7-G1 (stress) | 0.677 | 0.617 (−9%) | 0.61 | 0 / 1 |
| S8-G1 (stress) | 0.677 | 0.674 (−0.4%) | 0.66 | 0 / 0 |

**Two findings, both robust to the outlier issue and both important:**
1. The **median** branching ratio for every correctly-specified core alpha>0 scenario (S2/S3/S5/S6) is **systematically 16–18% below truth** — a real, precision-confirmed (n=1000) underrecovery, matching the direction already flagged as `PRELIMINARY_WARNING` from Pilot 100 and Pilot 10×10, now no longer preliminary.
2. **Counterintuitively, the two stress (misspecified) cells (S7, S8) show smaller branching-ratio bias than the correctly-specified core cells** (S7: −9%, S8: −0.4%, vs. S2–S6: −16% to −18%). This is reported exactly as observed, without recalibration or explanation-by-adjustment, per §23's prohibition on post-hoc parameter changes.

Formal branching-ratio absolute/relative bias gates (§14, mean-based as literally specified) **FAIL** in every core alpha>0 cell, driven by both the systematic median shift and the outlier contamination described above — both are genuine findings, not something to explain away.

## 18. Model Selection

| cell | correct model | AIC correct-selection rate (≥0.80) | BIC correct-selection rate (≥0.80) |
|---|---|---:|---:|
| S1-G1 | m2 | 0.901 PASS | 0.950 PASS |
| S1-G2 | m2 | 0.925 PASS | 0.974 PASS |
| S1-G3 | m2 | 0.910 PASS | 0.977 PASS |
| S2-G1 | m1 | 0.809 PASS | 0.909 PASS |
| S3-G1 | m3b_cd | **0.168 FAIL** | **0.031 FAIL** |
| S5-G1 | m3b_cd | **0.156 FAIL** | **0.022 FAIL** |
| S6-G1 | m3b_cd | **0.192 FAIL** | **0.037 FAIL** |
| S7-G1 (stress) | m3b_cd | 0.983 PASS | 0.887 PASS |

**When the true generating model is M3B-CD (density + excitation combined), both AIC and BIC overwhelmingly select the simpler M1 instead** — 810–820 of 1000 replicates in S3/S5/S6 are misclassified as M1. This is the single most consequential finding of the run: the framework, as currently specified, **cannot reliably distinguish "density effect present" from "no density effect" once self-excitation is also present**, even though theta1's own point estimate (§11) is comparatively well-behaved in isolation. S7 (density-transform misspecification) paradoxically shows the correct model-selection rate — plausibly because the deliberately-wrong linear-vs-log transform used to simulate S7 makes M1/M2 fit even worse, pushing selection toward M3B-CD by comparison, not because M3B-CD is being correctly identified for the right reason. This is reported as observed; no cause is asserted beyond what the numbers directly support.

## 19. Identifiability Diagnostics (Gate C)

`|correlation(theta1_hat, alpha_hat)|` (target < 0.70), planned jointly across S3/S4/S5:

- S3-G1: 0.0034 — PASS
- S5-G1: 0.0193 — PASS
- **S4-G1: NOT_ESTIMABLE — cell incomplete (300/1000, crashed before completion)**

Gate C is **not fully evaluable** as pre-registered (requires all three of S3/S4/S5 jointly). On the two available cells, correlation is negligible — theta1/alpha identifiability is not, by itself, the mechanism behind the model-selection failure in §18 (that failure is an AIC/BIC complexity-penalty effect, not a collinearity effect).

## 20. Stress Tests (Gate D, S7/S8 — separate threshold, not counted against core)

- S7-G1 (density-transform misspecification): theta0 norm.abs.bias 0.782, theta1 rel.bias 8.18 — both badly distorted, as expected under deliberate misspecification. Alpha/beta relative bias (−0.224/−0.118) and branching-ratio bias (−9%, §17) are, unexpectedly, *milder* than the core scenarios. Model selection correct at 0.983 (§18).
- S8-G1 (Gamma-kernel misspecification, fit with exponential): theta0/theta1 recovery close to unbiased; branching-ratio bias is the smallest of any cell in the study (−0.4%, §17); model-selection correct-rate low (0.197 AIC) — same M1-favoring pattern as the core M3B-CD cells (§18).

Per plan §15/§23, stress-scenario behavior does not automatically fail the core model, but is reported in full and factors into the overall interpretation: both stress cells show the *same* model-selection weakness as the core M3B-CD scenarios, suggesting the AIC/BIC under-selection of M3B-CD (§18) is a general property of this framework, not specific to correct specification.

## 21. Core Scenario Gate Evaluation — Summary

| Gate | Threshold | Result across core scenarios (S1×3, S2, S3, S5, S6) |
|---|---|---|
| Convergence rate | ≥0.95 | **PASS** (0.999–1.0 everywhere) |
| Invalid-estimate rate | ≤0.05 | **PASS** (≤0.001 everywhere) |
| False-positive excitation (S1) | ≤0.05 | **FAIL** (0.073–0.096) |
| Production-scenario power (S3) | ≥0.80 | **PASS** (0.985) |
| Rel. bias theta1/alpha/beta | ≤0.10 | **FAIL** (alpha/beta fail in every α_true>0 core cell; theta1 fails in 2/6 applicable cells) |
| Norm. abs. bias theta0 | ≤0.25 | **PASS** (0.002–0.078 everywhere) |
| Branching-ratio abs. bias | ≤0.05 | **FAIL** (all core α_true>0 cells) |
| Branching-ratio rel. bias | ≤0.10 | **FAIL** (all core α_true>0 cells) |
| 95% CI coverage | 0.925–0.975 | **PASS** for theta0/theta1; **FAIL** for alpha/beta in every α_true>0 core cell |
| Sign recovery (alpha) | ≥0.95 | **PASS** (0.994–0.999) |
| \|corr(theta1,alpha)\| (S3/S4/S5) | <0.70 | **PARTIAL** — PASS on S3/S5; **NOT_ESTIMABLE on S4** (incomplete) |
| Correct-model-selection rate | ≥0.80 | **PASS** for S1×3/S2; **FAIL** for S3/S5/S6 (0.02–0.19) |
| Normalized RMSE | ≤0.20 | **FAIL** (alpha/beta in every α_true>0 core cell) |
| **Gate A (hard implementation)** | run to completion, no crash | **FAIL — S4-G1 incomplete due to an unhandled `OverflowError`** |

## 22. Global Recovery Decision

```
SIMULATION_RECOVERY_FAILED
```

**Basis — two independent, sufficient grounds:**

1. **Gate A (hard implementation gate) failure.** S4-G1, a required core scenario, did not complete: an unhandled `OverflowError: math range error` (traceback in §23) crashed one worker process during point estimation for replicate 301/1000. Per the plan's own gate cascade, a hard-implementation-gate failure on any required core scenario is sufficient by itself to preclude `SIMULATION_RECOVERY_PASSED` or `_CONDITIONAL`.
2. **Independently, on the 9 cells that did complete**, multiple pre-registered hard statistical gates fail with high precision (n=1000/cell, not sampling noise): false-positive excitation (S1, §14), alpha/beta relative bias, branching-ratio bias, alpha/beta CI coverage (§11–12, §17), and — the most consequential — correct-model-selection rate for the true-M3B-CD scenarios (§18: AIC/BIC select the wrong, simpler model 80–98% of the time when density and excitation are both truly present).

Even absent the S4-G1 crash, ground (2) alone would already prevent a `PASSED` verdict; the crash additionally prevents a complete `FAILED`-vs-`CONDITIONAL` distinction from being drawn with full confidence, since one required core scenario's numbers (§19, §21) are missing outright. No fourth category is introduced; `FAILED` is the correct call under the plan's own two-ground logic.

## 23. Remaining Structural Gaps

1. **S4-G1 implementation defect (new, this run).** Root cause: `math.exp(theta0 + theta1 * x_CD)` in `likelihood.py:91` (called from `estimate.py`'s `neg_ll`, inside `fit_m3b_cd`'s own point estimation — not the `inference.py` wrapper, which does catch `ValueError` but not `OverflowError`) overflows when the L-BFGS-B optimizer's finite-difference gradient probe pushes `theta0`/`theta1` into an extreme region during a search step, for S4-G1's parameter regime (`theta1=0.3`, the largest theta1 among all 10 cells, combined with `alpha=0.04207`, the smallest nonzero alpha — a combination not present in any other cell). Not observed in Pilot 100 (1000 total records but different cell mix) nor Pilot 10×10 (only 10 replicates/cell — too few draws to hit this rare optimizer trajectory). **No fix was applied in this turn** (explicitly out of scope: "jangan mengubah simulator/estimate.py/likelihood.py"). Recommended remediation (separate authorization required): wrap the offending `math.exp` calls in `likelihood.py` with an overflow-safe clamp or catch `OverflowError` alongside the existing `ValueError` in the optimizer objective wrappers, then re-run S4-G1 (and only S4-G1) for the missing 700 replicates under a fresh, non-colliding seed range.
2. **Model-selection failure for true-M3B-CD scenarios (§18)** is the most scientifically consequential finding and is not a data or implementation artifact — it held at n=1000 with essentially zero Monte Carlo uncertainty. It should be treated as a primary finding of this recovery study, not a bug to fix before real-data authorization is considered.
3. **Branching-ratio underrecovery (§17)** is now confirmed (not preliminary) at 16–18% for correctly-specified core scenarios.
4. **Outlier-driven beta collapse** (§17, a handful of replicates per cell converging to near-zero `beta_hat`) merits its own investigation — separate from the S4-G1 crash — as a possible Gate A–adjacent instrumentation issue (optimizer robustness on the beta dimension), not evaluated further in this run.
5. Gate C (§19) is incomplete pending S4-G1.

## 24. Real-Data Authorization Gate

```
REAL_DATA_FITTING_REQUIRES_RESEARCHER_AUTHORIZATION
```

Given `SIMULATION_RECOVERY_FAILED`, real 141-event fitting is **not** automatically authorized and is not recommended as a next step without first resolving the S4-G1 implementation defect and addressing the model-selection finding (§18) as a methodological question — both decisions reserved for the researcher on a separate turn, per plan §26.

## 25. Reproducibility and Provenance

Every one of the 9,300 completed records carries `cell_id, replicate_id, base_seed, replicate_seed, simulator_commit (f351e71-line lineage, `aebd19e`), instrumentation_commit, persistence_commit, manifest_checksum, numerical_gate_checksum, density_checksum, simulation_kernel, fitted_kernel, truth_parameters, event_times, event_times_sha256`. All checksums independently re-verified in this audit (§7), not merely trusted from the run's own in-process report. Working output remains in `data/model3b_working/final_1000/` (git-ignored, untouched by this report).

## 26. Conclusions

The final run technically validated the instrumentation pipeline at full scale for 9 of 10 cells (perfect checksum integrity, 0 duplicate seeds/IDs, 0 nonfinite/out-of-window events, 0 boundary-test label or LR-formula errors across 9,300 sequences and 27,900 fits) and surfaced one genuine, previously-unseen implementation defect (S4-G1's `OverflowError`) that blocks full completion. Independently of that defect, the completed cells show that Model 3B-CD's estimator — while well-calibrated for `theta0`/`theta1` in isolation and for statistical power — **systematically underrecovers the branching ratio and, more importantly, fails to reliably select the correct model via AIC/BIC when density and self-excitation are jointly present**. Both findings are precise (n=1000/cell) and are reported as scientific results, not defects requiring recalibration. `SIMULATION_RECOVERY_FAILED` is the single global decision; no real-data fitting is authorized; the S4-G1 crash and the model-selection finding are the two concrete items for separate researcher decisions before any further phase.
