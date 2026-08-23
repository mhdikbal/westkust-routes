> **PILOT RECOVERY AUDIT**
> **100 REPLICATES PER CELL**
> **PRELIMINARY DIAGNOSTICS ONLY**
> **FINAL RECOVERY NOT ASSESSED**
> **REAL-DATA FITTING NOT AUTHORIZED**

---

## 0. Scope and provenance

This document closes the pilot-scale (100 replicates/cell) technical
phase for all 10 frozen cells in
`docs/thesis/pilot_annotation/MODEL_3B_CD_SIMULATION_CELL_MANIFEST.md`.
**No new simulation was run to produce this report** — it aggregates
already-executed pilot output, copied read-only from `/tmp` scratch to
the persistent, git-ignored working directory:

```
data/model3b_working/pilot_100/<CELL_ID>/{replicates.jsonl, failures.jsonl, metadata.json, summary.json, seed_list.json}
data/model3b_working/pilot_100/PILOT_100_AGGREGATE_SUMMARY.json
data/model3b_working/pilot_100/COPY_CHECKSUM_REPORT.json
```

Every source file's SHA-256 was verified to match its copy
(`COPY_CHECKSUM_REPORT.json`: `all_files_match: true`, all 40 files);
scratch originals under `/tmp` were **not deleted** (copy, not move).

| Cell | Source run | Simulator commit |
|---|---|---|
| S1-G1, S1-G2, S1-G3, S2-G1, S3-G1, S4-G1, S6-G1, S7-G1 | Fase 2B (8-cell serial pilot) | `88acc81` |
| S5-G1 | Fase 2B-1 follow-up | `88acc81` |
| S8-G1 | dedicated 100-replicate run (`run_s8g1_pilot100.py`), using the exact-cluster Gamma generator | `d3da369` |

S8-G1's earlier 1/5/10-replicate staged smoke test
(`pilot_2b_cells/S8-G1/staged_smoke_result.json`) and the killed
old-bound attempt were **excluded** — only the dedicated 100-replicate
run's output is used here, per instruction.

**Total accounting**: 10 cells × 100 replicates = **1000/1000 replicate
records present** (verified in §2).

---

## 1. Cells covered (exactly 10)

`S1-G1, S1-G2, S1-G3, S2-G1, S3-G1, S4-G1, S5-G1, S6-G1, S7-G1, S8-G1`

---

## 2. Technical reconciliation (per cell)

| Cell | Attempted | Completed | Successful fits | Opt. failures | Invalid | Nonfinite | Boundary | Missing IDs | Dup IDs | Seed uniqueness | Reproducible |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| S1-G1 | 100 | 100 | 100 | 0 | 0 | 0 | 56 | none | none | 100/100 unique | ✓ |
| S1-G2 | 100 | 100 | 100 | 0 | 0 | 0 | 58 | none | none | 100/100 unique | ✓ |
| S1-G3 | 100 | 100 | 100 | 0 | 0 | 0 | 59 | none | none | 100/100 unique | ✓ |
| S2-G1 | 100 | 100 | 100 | 0 | 0 | 0 | 0 | none | none | 100/100 unique | ✓ |
| S3-G1 | 100 | 100 | 100 | 0 | 0 | 0 | 0 | none | none | 100/100 unique | ✓ |
| S4-G1 | 100 | 100 | 100 | 0 | 0 | 0 | 42 | none | none | 100/100 unique | ✓ |
| S5-G1 | 100 | 100 | 100 | 0 | 0 | 0 | 0 | none | none | 100/100 unique | ✓ |
| S6-G1 | 100 | 100 | 100 | 0 | 0 | 0 | 1 | none | none | 100/100 unique | ✓ |
| S7-G1 | 100 | 100 | 100 | 0 | 0 | 0 | 0 | none | none | 100/100 unique | ✓ |
| S8-G1 | 100 | 100 | 100 | 0 | 0 | 0 | 0 | none | none | 100/100 unique | ✓ |
| **Total** | **1000** | **1000** | **1000** | **0** | **0** | **0** | 216 | 0 | 0 | 1000/1000 unique | 10/10 |

**Zero** optimizer failures, invalid estimates, nonfinite results,
missing/duplicate replicate IDs, or seed collisions across all 1000
records. All 10 cells independently re-verified reproducible
(replicate #1 re-run separately during each pilot execution).
Boundary-pileup counts are reported here as raw counts — their
interpretation (implementation failure vs. diagnostic) is addressed
per-cell in §3 and per the manifest's boundary-gate applicability
clarification (S2 already in the manifest).

---

## 3. Preliminary recovery diagnostics (per cell)

**Reading key**: values are computed directly from the 100 point
estimates per cell. `NOT_ESTIMABLE` marks a plan §9 metric that
requires infrastructure (standard errors/CI, or competing-model fits)
**not implemented in this pilot's estimator** — see §5. `NOT_APPLICABLE`
marks a metric that is structurally undefined for that cell's ground
truth (e.g. relative bias when the true value is exactly 0).

### 3.1 theta0 normalized absolute bias (Gate B target ≤ 0.25)

| Cell | theta0 NAB | vs. 0.25 threshold |
|---|---:|---|
| S1-G1 | 0.080 | under |
| S1-G2 | 0.055 | under |
| S1-G3 | 0.108 | under |
| S2-G1 | 0.023 | under |
| S3-G1 | 0.022 | under |
| S4-G1 | 0.060 | under |
| S5-G1 | 0.011 | under |
| S6-G1 | 0.004 | under |
| S7-G1 | **0.797** | **over — 3.2× threshold** |
| S8-G1 | 0.028 | under |

S7-G1's large `theta0` bias is the **expected signature of its
deliberate misspecification** (simulated with linear `x_CD_true(t)`,
fitted with `log(1+CD_t)`) — this is Gate D territory (plan §9), not a
Gate B failure; it is a confirmatory finding that the stress test is
actually stressing the intended mechanism.

### 3.2 Branching ratio recovery (Gate B: abs bias ≤ 0.05 **AND** rel bias ≤ 0.10)

| Cell | True BR | Median BR̂ | Mean BR̂ | Abs. bias (median) | Rel. bias (median) | Extreme outliers (BR̂>5) | Gate B (median-based) |
|---|---:|---:|---:|---:|---:|---:|---|
| S1-G1 | 0.000 | 0.000 | 0.044 | 0.000 | n/a (true=0) | 0 | pass |
| S1-G2 | 0.000 | 0.000 | 0.044 | 0.000 | n/a (true=0) | 0 | pass |
| S1-G3 | 0.000 | 0.000 | 0.050 | 0.000 | n/a (true=0) | 0 | pass |
| S2-G1 | 0.677 | 0.545 | 0.527 | −0.132 | 0.195 | 0 | **miss** |
| S3-G1 | 0.677 | 0.588 | 0.547 | −0.089 | 0.131 | 0 | **miss** |
| S4-G1 | 0.068 | 0.038 | **94.548** | −0.030 | 0.440 | **2** | **miss** (median rel. bias) |
| S5-G1 | 0.677 | 0.551 | 0.545 | −0.126 | 0.187 | 0 | **miss** |
| S6-G1 | 0.677 | 0.573 | 0.571 | −0.104 | 0.153 | 0 | **miss** |
| S7-G1 | 0.677 | 0.614 | 0.592 | −0.063 | 0.093 | 0 | **miss** (abs. bias only) |
| S8-G1 | 0.677 | 0.680 | 0.664 | +0.003 | 0.004 | 0 | pass |

**Two findings worth flagging explicitly, not smoothing over:**

1. **S4-G1's mean (94.5) is an artifact, not a recovery signal.** 2 of
   100 replicates have `beta_hat` pinned at the optimizer's lower bound
   (`1e-6`), producing `alpha_hat/beta_hat` ratios of ~5369 and ~4078
   that dominate the arithmetic mean. The **median** (0.038, vs. true
   0.068) is the representative value and is reported alongside the
   mean rather than letting the mean stand alone — this is exactly the
   kind of grid point (`alpha_true` small, `0.1×` production) where the
   plan's own §5 poin 2 risk ("alpha menyerap efek densitas") predicts
   instability.
2. **Every correctly-specified core scenario with `alpha_true` well
   away from 0** (S2, S3, S5, S6) **systematically under-recovers the
   branching ratio by ~13–20% at n=100**, missing the pre-specified
   Gate B relative-bias threshold (≤0.10) on the median estimate. S7
   (misspecified, expected to miss) and S8 (Gamma-kernel misspecified,
   **passes** — branching ratio recovery is robust to *this particular*
   kernel misspecification) bracket that finding.

This is a **preliminary pilot-scale signal, not a final verdict** — see
§6 for why n=100 cannot settle this, and §8 for what it does and does
not imply for the final 1000-replicate run.

### 3.3 Absolute relative bias (theta1, alpha, beta) and NRMSE

Reported in full in `PILOT_100_AGGREGATE_SUMMARY.json` per cell.
Headline caveat: several `theta1` NRMSE values are very large (2–29)
purely because `theta1_true` is small (0.01–0.3) in most cells —
**NRMSE normalized by a near-zero true value is not a reliable
indicator on its own** and is reported here for completeness, not as a
standalone red flag; absolute bias and sign recovery (below) are the
more interpretable companions for small-magnitude parameters.

### 3.4 Sign recovery (theta1, alpha; only where true ≠ 0)

| Cell | theta1 sign recovery (95% Wilson CI) | alpha sign recovery (95% Wilson CI) |
|---|---|---|
| S1-G1 | 0.660 (0.563–0.745) | n/a (true=0) |
| S1-G2 | 0.710 (0.615–0.790) | n/a (true=0) |
| S1-G3 | 0.840 (0.756–0.899) | n/a (true=0) |
| S2-G1 | n/a (true=0) | 1.000 (0.963–1.000) |
| S3-G1 | 0.720 (0.625–0.799) | 1.000 (0.963–1.000) |
| S4-G1 | 1.000 (0.963–1.000) | 0.600 (0.502–0.691) |
| S5-G1 | 0.530 (0.433–0.625) | 1.000 (0.963–1.000) |
| S6-G1 | 0.670 (0.573–0.754) | 0.990 (0.946–0.998) |
| S7-G1 | 1.000 (0.963–1.000) | 1.000 (0.963–1.000) |
| S8-G1 | 0.620 (0.522–0.709) | n/a (true=0/undefined) |

`alpha` sign recovery is strong (≥0.60, mostly ≥0.99) wherever
`alpha_true > 0`. `theta1` sign recovery is markedly weaker (0.53–0.84)
for cells where `theta1_true` is small (0.01–0.1) — consistent with a
weak, noise-dominated density signal at this replicate count, not
necessarily a defect. Gate B's `≥0.95` sign-recovery threshold is
**not met for `theta1` in most cells** at n=100 — flagged, not
adjudicated (§6).

### 3.5 Gate C — pooled correlation(theta1̂, alphâ), scenarios 3/4/5

```
pooled correlation = -0.177  (n=300 pooled replicates, S3-G1 + S4-G1 + S5-G1)
Gate C threshold: |correlation| < 0.70
Result: WELL BELOW threshold — no identifiability warning signal at pilot scale.
```

This is a genuinely reassuring finding: `theta1` and `alpha` are not
collapsing into each other statistically in this pilot, even though
S4/S5 were specifically designed to probe that risk (plan §5 poin 1/2).

---

## 4. Metrics NOT_ESTIMABLE from this pilot (implementation gap, not a pipeline defect)

The following plan §9 metrics require infrastructure this pilot's
estimator does not compute, and are therefore **NOT_ESTIMABLE** from
the collected data, for every cell:

| Metric | Why not estimable |
|---|---|
| **Nominal 95% CI coverage** (Gate B) | No standard-error/confidence-interval computation is implemented anywhere in `estimate.py` — plan §8 poin 3 itself notes there is no project precedent (Model 3 production never reported a CI either). |
| **False-positive excitation** (formal, Gate B) | Requires an LR-test or a CI on `alpha` to decide "significantly different from 0"; neither was computed per replicate. A **descriptive proxy** (boundary-hit rate, RMSE vs. 0) is reported in §3/JSON for the `alpha_true=0` cells, explicitly labeled as not the plan's formal metric. |
| **Production-scenario power** (Gate E poin 5) | Same significance-test dependency as above. |
| **Correct-model-selection rate** (Gate C) | Requires fitting M1 and M2 separately (for AIC/BIC/LR-test comparison against M3B-CD) per replicate; this pilot only fit M3B-CD. |

None of this is a defect in the simulator/estimator audited in Fase 1B
— it is a **scope gap between what the pilot harness collected and
what plan §9's full gate set needs**. This is the single most important
finding this preliminary audit surfaces for the next implementation
step (§8).

---

## 5. Monte Carlo uncertainty

Every proportion reported above (convergence rate, boundary-pileup
rate, sign-recovery rate) carries substantial sampling uncertainty at
`n=100`: Wilson 95% CIs run roughly ±5–10 percentage points depending
on the point estimate (see per-metric CIs in §3.4 and in
`PILOT_100_AGGREGATE_SUMMARY.json`). **A single replicate landing on
either side of a threshold at n=100 is well within Monte Carlo noise**
and must not be read as a final verdict — this is precisely why the
plan (§9) requires 1000 replicates/cell before any gate decision is
made, and why this document produces `PRELIMINARY_*` labels, never
`SIMULATION_RECOVERY_PASSED/FAILED`.

---

## 6. Per-cell preliminary status

Status logic (unchanged plan §9 thresholds, applied verbatim): Gate A
(convergence ≥0.95 **and** invalid-estimate ≤0.05) is authoritative for
`PRELIMINARY_FAILURE_SIGNAL` (implementation-level). Where Gate A
passes, the branching-ratio Gate B check (median-based, abs ≤0.05
**and** rel ≤0.10) is applied as a diagnostic; a miss there yields
`PRELIMINARY_WARNING` (recovery-level concern, not an implementation
failure, and not adjudicated at n=100).

| Cell | Gate A | Branching-ratio Gate B (diagnostic) | Preliminary status |
|---|---|---|---|
| S1-G1 | pass | n/a (true BR=0) | `PRELIMINARY_PASS` |
| S1-G2 | pass | n/a (true BR=0) | `PRELIMINARY_PASS` |
| S1-G3 | pass | n/a (true BR=0) | `PRELIMINARY_PASS` |
| S2-G1 | pass | miss | `PRELIMINARY_WARNING` |
| S3-G1 | pass | miss | `PRELIMINARY_WARNING` |
| S4-G1 | pass | miss (outlier-driven mean; median also misses rel. bias) | `PRELIMINARY_WARNING` |
| S5-G1 | pass | miss | `PRELIMINARY_WARNING` |
| S6-G1 | pass | miss | `PRELIMINARY_WARNING` |
| S7-G1 | pass | miss (expected — misspecification stress cell) | `PRELIMINARY_WARNING` |
| S8-G1 | pass | pass | `PRELIMINARY_PASS` |

No cell reached `PRELIMINARY_FAILURE_SIGNAL` — every cell's simulation
+ fitting pipeline ran cleanly to completion with full convergence.

---

## 7. What this audit does NOT conclude

- **Not** `SIMULATION_RECOVERY_PASSED` or `SIMULATION_RECOVERY_FAILED`
  — plan §9's full gate set (A–E) cannot be evaluated with 100
  replicates or with this pilot's uninstrumented estimator (§4).
- **Not** `REAL_DATA_FITTING_AUTHORIZED` — no 141-event fitting was
  performed or is implied by any result here.
- **Not** a manifest or numerical-gate revision — no threshold in
  `MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md` §9 was changed; the
  branching-ratio diagnostic in §3.2/§6 applies the existing thresholds
  verbatim as a descriptive check, not a redefinition.

---

## 8. Decision — readiness for the final 1000-replicate run

**Pipeline mechanics**: fully ready. All 10 cells completed 1000/1000
replicate records combined with zero optimizer failures, zero invalid
estimates, zero nonfinite results, zero missing/duplicate replicate
IDs, and 10/10 independently-verified reproducibility. Runtime,
seeding, and provenance tracking all worked as designed (§2).

**Gate-evaluability**: incomplete. Running 1000 replicates/cell today,
with the estimator exactly as currently implemented, would still leave
**interval coverage, formal false-positive excitation, power, and
correct-model-selection rate NOT_ESTIMABLE** (§4) — the final run's
data would be unable to render an actual Gate B/C verdict on those four
metrics no matter how many replicates are run, because the underlying
per-replicate statistics (SE/CI, competing-model fits) are never
computed. Spending the final run's ~3160s (10 cells × 1000 × ~0.3s,
per the manifest's flat projection) without that instrumentation would
under-deliver relative to what plan §9 actually requires to close.

**Status:**
```
FINAL_1000_RUN_REQUIRES_IMPLEMENTATION_REVISION
```

**What "REQUIRES_IMPLEMENTATION_REVISION" means here**: the simulation/
fitting pipeline itself does not need rework (§2 shows it is clean and
robust) — this status means the **harness around it** needs two
additions before the final 1000-replicate run is worth executing:

1. A standard-error/CI computation for the M3B-CD fit (method still an
   open plan §8 poin 3 decision — profile-likelihood, bootstrap, or
   asymptotic), enabling formal false-positive-excitation, power, and
   interval-coverage metrics.
2. Per-replicate M1/M2 comparison fits (alongside the existing M3B-CD
   fit), enabling the correct-model-selection-rate metric (Gate C).

`TECHNICALLY_READY` would mean "run 1000 now, as-is" — that is
explicitly **not** what this finding supports, since it would burn the
final-run budget without being able to close two of five plan §9
gates. `BLOCKED` would overstate the problem — nothing here is broken,
under-specified, or contradicts the frozen plan/manifest; it is a
scoped, well-understood instrumentation gap with a clear fix.

---

**STOP** — pilot-100 finalization complete. No new replicates were run,
no simulator/manifest/gate change was made, no real-data (141-event)
fitting was performed, and no commit/push/Graphify/deployment action
was taken.
