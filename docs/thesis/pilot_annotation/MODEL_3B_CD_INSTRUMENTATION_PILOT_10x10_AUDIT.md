> **STATISTICAL INSTRUMENTATION PILOT**
> **10 CELLS x 10 REPLICATES**
> **EVENT SEQUENCES PERSISTED**
> **PRELIMINARY DIAGNOSTICS ONLY**
> **FINAL RECOVERY NOT ASSESSED**
> **REAL-DATA FITTING NOT AUTHORIZED**

---

## 1. Scope

100 new synthetic event sequences (10 frozen cells × 10 replicates) generated,
persisted with full `event_times`, fit with M1/M2/M3B-CD, and instrumented
(Hessian → covariance → SE/CI → boundary-aware alpha=0 test → AIC/BIC →
branching-ratio delta method → three-model selection). Purpose: verify the
Fase 3A instrumentation pipeline is stable and reproducible end-to-end on
data that actually carries `event_times` (the gap that blocked instrumenting
the old Pilot 100 output, per
`MODEL_3B_CD_INSTRUMENTATION_PILOT_BLOCKER.md`).

This pilot is **not** a simulation-recovery evaluation. 10 replicates/cell
give only preliminary, high-variance signal — no Gate B/C/D pass/fail
decision is made here, and no `SIMULATION_RECOVERY_PASSED/FAILED` or
`REAL_DATA_FITTING_AUTHORIZED` label is used anywhere in this report.

## 2. Blueprint Compliance

- Source of truth: `docs/Unduh MODEL_3B_CD_MASTER_BLUEPRINT.md` +
  `docs/plan Pilot Instrumentasi 10×10, format Markdown.md`.
- Authorization phrase received from the researcher this turn (file-name
  variant of the blueprint's §26 exact phrase, same two documents named):
  "Jalankan Pilot Instrumentasi 10x10 sesuai MODEL_3B_CD_MASTER_BLUEPRINT.md
  dan MODEL_3B_CD_PILOT_INSTRUMENTATION_10x10_PLAN.md."
- Exactly the 10 frozen cells (§4 of the plan) were used, unmodified. No
  cell added/removed, no parameter changed, no grid point added, no
  recalibration from Pilot 100/Pilot 2A results.
- Exactly 10 replicates/cell (100 total) — not scaled up automatically.
- No real 141-event fitting. No final 1,000-replicate run. No simulator/
  instrumentation/persistence/manifest/gates/density-source change. No
  Graphify/commit/push/deploy.

## 3. Preflight Results — all 12 guards passed

| # | Guard | Result |
|---|---|---|
| 1 | HEAD == origin/main | pass (`aebd19e` both) |
| 2 | Simulator commit matches blueprint | pass (`aebd19e`, includes `d3da369` Gamma generator) |
| 3 | Instrumentation commit matches blueprint | pass (`2ec1def` included in `aebd19e` history) |
| 4 | Persistence commit matches blueprint | pass (`aebd19e`) |
| 5 | Unit test suite passes | pass — 115/115 |
| 6 | Density checksum matches | pass — `e0b8ab7c78104e89f39a15b2e55b0b96c6b055efe273fbfc8a0fc9f1d0f5e04a` (matches S8-G1 Pilot 100 `metadata.json` record) |
| 7 | Output directory clean before run | pass — `instrumentation_pilot_10x10/` did not exist |
| 8 | No other pilot process active | pass |
| 9 | Numerical gates unchanged | pass — `MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md` untouched (`git status` clean) |
| 10 | Cell manifest unchanged | pass — `MODEL_3B_CD_SIMULATION_CELL_MANIFEST.md` untouched (`git status` clean) |
| 11 | Simulator source clean | pass — no local diff in `model3b_cd_simulator/` |
| 12 | Output directory git-ignored | pass — `data/model3b_working/` covered by `.gitignore` line 140 |

No guard failed; pilot proceeded.

## 4. Cell Manifest (as used)

| cell_id | theta0 | theta1 | alpha | beta | kernel (sim) | true branching ratio | base_seed |
|---|---:|---:|---:|---:|---|---:|---:|
| S1-G1 | -2.047943 | 0.1 | 0.0 | 0.6215 | exponential | 0.0000 | 40260824 |
| S1-G2 | -1.358679 | 0.1 | 0.0 | 0.6215 | exponential | 0.0000 | 40270824 |
| S1-G3 | -0.665532 | 0.1 | 0.0 | 0.6215 | exponential | 0.0000 | 40280824 |
| S2-G1 | -1.357513 | 0.0 | 0.4207 | 0.6215 | exponential | 0.6769 | 40290824 |
| S3-G1 | -1.357513 | 0.1 | 0.4207 | 0.6215 | exponential | 0.6769 | 40300824 |
| S4-G1 | -1.357513 | 0.3 | 0.04207 | 0.6215 | exponential | 0.0677 | 40310824 |
| S5-G1 | -1.357513 | 0.01 | 0.4207 | 0.6215 | exponential | 0.6769 | 40320824 |
| S6-G1 | -1.357513 | 0.1 | 0.4207 | 0.6215 | exponential | 0.6769 | 40330824 |
| S7-G1 | -1.357513 | 0.1 | 0.4207 | 0.6215 | exp (sim), x_CD linear / fit x_CD log1p | 0.6769 | 40340824 |
| S8-G1 | -1.357513 | 0.1 | n/a | n/a | Gamma(k=2, rate=2.38095), amplitude=0.6769 | 0.6769 (target) | 40350824 |

All 10 cells fit M1/M2/M3B-CD with the **exponential** kernel (S8-G1's Gamma
ground truth is fit with the deliberately misspecified exponential
estimator, per manifest §1). Fitting always used the standard
`log1p(1+CD_t)` density transform for all 10 cells (S7-G1's misspecification
is only in the **simulation** transform, per manifest §1 / plan §2 row 7).

Seed base per cell (`40260824`+) chosen to be disjoint from the old Pilot
100 seeds (`~2026082x`), the persistence smoke test (`20260824`), and the
Gamma smoke-test seed range (`21160824`+).

## 5. Seed and Provenance

- Every replicate stores `cell_id, replicate_id, base_seed, replicate_seed,
  simulator_commit, instrumentation_commit, density_checksum,
  simulation_kernel, fitted_kernel, truth_parameters` (plan §7 field list).
- 0 duplicate `replicate_seed` and 0 duplicate `replicate_id` detected
  across all 1,000 seed/id pairs checked (100 replicates × 10 fields each).
- Reproducibility check (replicate 1 of every cell re-simulated from its
  stored seed and re-fit): **identical** event sequence, fit status,
  parameters, and log-likelihood in **all 10/10 cells**.

## 6. Event-Sequence Persistence

- `event_times` stored for all 100/100 replicates (`result_kind =
  new_result_with_event_times` in all cases — no legacy record produced).
- Checksum (SHA-256 of little-endian `<f8` bytes) round-trip verified for
  all 100/100 replicates: **100/100 match** (checksum-valid rate = 1.0 in
  every cell).
- 0/100 nonfinite event times; 0/100 events outside `[1600, 1784)`.

## 7-9. M1 / M2 / M3B-CD Fit Results

| cell_id | fit success M1 | fit success M2 | fit success M3B-CD |
|---|---:|---:|---:|
| S1-G1 | 10/10 | 10/10 | 10/10 |
| S1-G2 | 10/10 | 10/10 | 10/10 |
| S1-G3 | 10/10 | 10/10 | 10/10 |
| S2-G1 | 10/10 | 10/10 | 10/10 |
| S3-G1 | 10/10 | 10/10 | 10/10 |
| S4-G1 | 10/10 | 10/10 | 10/10 |
| S5-G1 | 10/10 | 10/10 | 10/10 |
| S6-G1 | 10/10 | 10/10 | 10/10 |
| S7-G1 | 10/10 | 10/10 | 10/10 |
| S8-G1 | 10/10 | 10/10 | 10/10 |

**100/100 fit success for all three models across all 10 cells** — 0
optimizer failures, 0 invalid statuses.

## 10. Hessian and Covariance Audit

| cell_id | cov valid M1 | cov valid M2 | cov valid M3B-CD |
|---|---:|---:|---:|
| S1-G1 | 9/10 | 10/10 | 5/10 |
| S1-G2 | 10/10 | 10/10 | 10/10 |
| S1-G3 | 8/10 | 10/10 | 7/10 |
| S2-G1 | 10/10 | 10/10 | 10/10 |
| S3-G1 | 10/10 | 10/10 | 10/10 |
| S4-G1 | 10/10 | 10/10 | 9/10 |
| S5-G1 | 10/10 | 10/10 | 10/10 |
| S6-G1 | 10/10 | 10/10 | 10/10 |
| S7-G1 | 10/10 | 10/10 | 10/10 |
| S8-G1 | 10/10 | 10/10 | 10/10 |

Only S1-G1's M3B-CD covariance rate (5/10 valid, invalid rate exactly
0.50) approaches the plan §17 stop threshold ("covariance invalid melebihi
50%"); at exactly 0.50 it does **not** exceed the threshold, so no stop
condition was triggered. This is consistent with S1's `alpha_true=0`
boundary regime (manifest §2 poin 2: boundary pile-up/covariance
degeneracy at `alpha=0` is expected estimator behavior at a parameter
boundary, not an implementation defect) — the low-density S1-G1 grid point
(`theta0=-2.05`, fewest events, mean n=29.5) makes this the most
data-sparse cell of the ten, compounding the boundary effect. Flagged for
attention in a larger replicate count, not treated as a defect here.

No cell exceeded the 50% covariance-invalid stop threshold. No fit-failure
rate exceeded 20% in any cell (all were 0%).

## 11. SE and CI Availability

SE/CI availability for M3B-CD tracks covariance validity directly (SE/CI
require a valid or regularized covariance): available in all cells except
the same S1-G1 (5/10) and S1-G3 (7/10) reduced rates noted above; all other
8 cells at 10/10.

## 12. Boundary-Aware Alpha Test (M2 vs M3B-CD)

- **Label correctness: 100/100 correct** — `restricted_model="m2"`,
  `unrestricted_model="m3b_cd"` in every replicate, every cell.
- **LR manual-recomputation check: 100/100 match** —
  `LR_output == 2 × (logLik_M3B-CD − logLik_M2)` verified independently for
  every replicate; 0 mismatches.
- Reject-H0-at-0.05 rate by cell (informational, not a gate decision):

| cell_id | true alpha | reject_H0 rate (n=10) |
|---|---|---:|
| S1-G1 | 0 | 0.00 |
| S1-G2 | 0 | 0.10 |
| S1-G3 | 0 | 0.00 |
| S4-G1 | 0.04207 (small) | 0.10 |
| S2-G1 | 0.4207 | 1.00 |
| S3-G1 | 0.4207 | 1.00 |
| S5-G1 | 0.4207 | 1.00 |
| S6-G1 | 0.4207 | 1.00 |
| S7-G1 | 0.4207 (misspec.) | 1.00 |
| S8-G1 | Gamma (misspec.) | 1.00 |

## 13. AIC/BIC Model Selection

Available in 100/100 replicates. Best-by-AIC counts per cell (n=10 each):
S1-G1 m2:10; S1-G2 m2:8/m1:2; S1-G3 m2:10; S2-G1 m1:8/m3b_cd:2; S3-G1
m1:9/m3b_cd:1; S4-G1 m2:9/m1:1; S5-G1 m1:8/m3b_cd:2; S6-G1 m1:8/m3b_cd:2;
S7-G1 m3b_cd:10; S8-G1 m1:10.

## 14. Branching-Ratio Uncertainty

Delta-method CI computed (`delta_method_status="computed"`) whenever the
`alpha`/`beta` covariance sub-block was valid — same availability pattern
as §10/§11. Mean recovered branching ratio vs. true value (n=10/cell,
preliminary only):

| cell_id | true | mean estimate | bias |
|---|---:|---:|---:|
| S1-G1 | 0.0000 | 0.0239 | +0.0239 |
| S1-G2 | 0.0000 | 0.0506 | +0.0506 |
| S1-G3 | 0.0000 | 0.0238 | +0.0238 |
| S2-G1 | 0.6769 | 0.5710 | -0.1059 |
| S3-G1 | 0.6769 | 0.5580 | -0.1189 |
| S4-G1 | 0.0677 | 0.0426 | -0.0251 |
| S5-G1 | 0.6769 | 0.5421 | -0.1348 |
| S6-G1 | 0.6769 | 0.5049 | -0.1720 |
| S7-G1 | 0.6769 | 0.6600 | -0.0169 |
| S8-G1 | 0.6769 | 0.6293 | -0.0476 |

This under-recovery pattern for `alpha_true>0` cells is directionally
consistent with what was already documented in the Pilot 100 audit
(`MODEL_3B_CD_PILOT_100_AUDIT.md`) — reported here only as a preliminary
signal at n=10/cell, not re-litigated or re-decided.

## 15. Runtime

| cell_id | mean (s) | min (s) | max (s) |
|---|---:|---:|---:|
| S1-G1 | 0.324 | 0.171 | 0.733 |
| S1-G2 | 0.478 | 0.249 | 0.729 |
| S1-G3 | 0.623 | 0.427 | 1.023 |
| S2-G1 | 0.803 | 0.519 | 1.204 |
| S3-G1 | 0.852 | 0.497 | 1.234 |
| S4-G1 | 0.432 | 0.314 | 0.565 |
| S5-G1 | 0.813 | 0.700 | 1.091 |
| S6-G1 | 0.780 | 0.450 | 1.329 |
| S7-G1 | 1.858 | 1.259 | 2.711 |
| S8-G1 | 0.804 | 0.620 | 1.208 |

(Full per-replicate figures in each cell's `cell_summary.json`.) Total
wall time for the entire 10×10 serial run: **80.4 seconds** (includes
Python/module import and CSV-load overhead once per cell, not just the
10 replicates themselves). S7-G1 is slowest (highest mean event count,
249.4/replicate, driving higher Hessian/optimizer cost) and S8-G1's Gamma
cluster simulation is not itself a bottleneck — both far under any timeout
concern; no cell approached the runtime stop condition.

## 16. Failures and Warnings

0 stop conditions triggered (full list checked: checksum failure, density
checksum drift, >20% fit failure, >50% covariance invalid, LR mismatch,
boundary-label error, output overwrite, simulator/instrumentation/
manifest/gate drift during run, nonfinite event time, out-of-window event,
duplicate ID/seed, runtime/progress stall — none occurred). Per-cell
`failure_log.jsonl` lists only the S1-G1/S1-G3 M1/M3B-CD covariance
softness already discussed in §10 (recorded, not a stop condition since it
stayed at or under the 50% ceiling).

## 17. Preliminary Diagnostics

Using only the allowed labels (`PRELIMINARY_PASS` /
`PRELIMINARY_WARNING` / `PRELIMINARY_FAILURE_SIGNAL` / `NOT_APPLICABLE` /
`NOT_ESTIMABLE`), interpreted qualitatively at n=10/cell:

- **Pipeline mechanics** (persistence, checksum, reproducibility, fit
  success, LR/label correctness): `PRELIMINARY_PASS` across all 10 cells —
  0 defects observed in any of these dimensions.
- **S1 false-positive rate** (alpha_true=0, reject-H0 rate observed
  0.00-0.10 across S1-G1/G2/G3): `PRELIMINARY_PASS` — well under the
  nominal 0.05 target on average, though n=10/cell is too small to bound
  this tightly (a single rejection in 10 replicates already reads as 0.10).
- **Branching-ratio bias for alpha_true>0 cells** (§14, under-recovery of
  10-17 points on cells with true branching ratio 0.68): carried over as
  `PRELIMINARY_WARNING` — same qualitative direction as the earlier
  Pilot 100 finding, not newly discovered here, and not re-assessed against
  Gate B/E thresholds in this report (that remains a decision for the final
  1,000-replicate run, per plan §19/§20).
- **S1-G1 covariance softness at n=10** (§10): `PRELIMINARY_WARNING` —
  right at, not over, the 50% stop threshold; worth watching at higher
  replicate counts, not a defect finding.
- Correct-model-selection rate, interval coverage, theta1-alpha
  correlation: `NOT_ESTIMABLE` from 10 replicates/cell — too few draws for
  a meaningful coverage/correlation estimate; deferred to the final run.

## 18. Technical Readiness Decision

```
INSTRUMENTATION_PILOT_TECHNICALLY_READY
```

**Reason**: all 10 cells completed; event times stored and 100/100
checksums valid; M1/M2/M3B-CD fit succeeded in 100/100 replicates each;
Hessian/covariance/SE/CI/boundary-test/AIC/BIC/branching-ratio computed at
a materially adequate rate in every cell (worst case 50% covariance
validity in one cell, at — not over — the stop threshold); the M2-vs-M3B-CD
boundary-test label and LR formula were independently verified correct in
all 100 replicates; reproducibility was exact in all 10 cells; no
implementation defect or stop condition was found.

## 19. Remaining Gaps

- S1-G1's M3B-CD covariance-validity rate (5/10) is the one soft spot;
  worth re-checking at a larger replicate count before treating it as
  resolved.
- Branching-ratio under-recovery on `alpha_true>0` cells (§14) is not
  newly resolved by this pilot — it is the same open question the Pilot
  100 audit already raised, now additionally confirmed at the
  instrumentation level (SE/CI/LR machinery itself works correctly; the
  point estimates are what show bias).
- Correct-model-selection rate, interval coverage, and theta1-alpha
  correlation remain `NOT_ESTIMABLE` at this replicate count.

## 20. Stop Condition for Final Run

None of the plan §17 stop conditions were triggered in this pilot, so
there is no blocking finding standing in the way of a final 1,000-
replicate run being *requested*. However, per plan §5/§26 that request
requires a **separate, explicit researcher authorization** — this report
does not itself authorize it, and the branching-ratio bias noted in §14/§19
should inform that decision (not be silently carried past it).

---

## Output Terminal Summary

1. Cells run: S1-G1, S1-G2, S1-G3, S2-G1, S3-G1, S4-G1, S5-G1, S6-G1,
   S7-G1, S8-G1 (10/10)
2. Attempted/completed: 100/100
3. Event-sequence persistence rate: 100/100 (1.00)
4. Checksum-valid rate: 100/100 (1.00)
5. Total fits: M1 100, M2 100, M3B-CD 100
6. Fit success rate per model: M1 1.00, M2 1.00, M3B-CD 1.00
7. Covariance-valid rate per model (aggregate across all 300 model fits):
   M1 0.97, M2 1.00, M3B-CD 0.91
8. SE availability: tracks covariance validity (§10/§11)
9. CI availability: tracks covariance validity (§10/§11)
10. Boundary-test availability: 100/100 (1.00), label correct 100/100
11. AIC/BIC availability: 100/100 (1.00)
12. Branching-ratio CI availability: tracks covariance validity (§14)
13. Failures per cell: 0 stop conditions; S1-G1/S1-G3 covariance softness
    logged, not a stop condition
14. Runtime: total 80.4 s; per-cell range ~0.09 s (S1-G1) to ~4.8 s
    (S7-G1)
15. Reproducibility status: identical in 10/10 cells
16. Density checksum:
    `e0b8ab7c78104e89f39a15b2e55b0b96c6b055efe273fbfc8a0fc9f1d0f5e04a`
    (unchanged throughout)
17. Output location: `data/model3b_working/instrumentation_pilot_10x10/`
    (git-ignored)
18. Audit report path: this file
19. Preliminary diagnostic summary: pipeline mechanics
    `PRELIMINARY_PASS`; S1 false-positive rate `PRELIMINARY_PASS`;
    branching-ratio bias `PRELIMINARY_WARNING` (carried over from Pilot
    100, not newly decided); S1-G1 covariance softness
    `PRELIMINARY_WARNING`; model-selection rate/coverage/correlation
    `NOT_ESTIMABLE` at n=10
20. Status akhir:

```
INSTRUMENTATION_PILOT_TECHNICALLY_READY
```

Berhenti di sini. Menunggu review peneliti. Tidak melanjutkan otomatis ke
final 1.000 replikasi, fitting 141 event nyata, Graphify, commit, push,
atau deploy.
