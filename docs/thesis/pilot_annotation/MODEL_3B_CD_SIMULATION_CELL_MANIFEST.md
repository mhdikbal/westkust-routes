> **CELL MANIFEST — NO NEW SIMULATION RUN TO PRODUCE THIS DOCUMENT**
> **NUMERICAL DECISION GATES UNCHANGED (frozen in
> `MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md` §9)**
> **NO PARAMETER CHANGED BASED ON PILOT 2A RESULTS**
> **NO REAL-DATA (141-event) FITTING**

---

## 0. Scope and provenance

This document freezes the set of `(scenario, grid-point)` **cells** that
Fase 2B will run at the pilot replicate count (100/cell, plan §9). It is
built from:

- `docs/thesis/pilot_annotation/MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md`
  §2 (8 scenarios) and §3 (parameter grid);
- the already-executed Pilot 2A run (scenario 3 / grid point 0,
  simulator commit `88acc81`, 100 replicates, mean runtime
  0.316s/replicate);
- simulator commit `88acc81` (unchanged — this document does not modify
  it).

**No new simulation was run to build this manifest.** Every numeric
value below is either copied verbatim from the plan's own printed grid
(§3), a plan-stated production-calibrated value (§0), a plan-stated
explicit multiplier (§2, e.g. scenario 4's "3× nilai skenario 3" /
"0.1×alpha produksi"), or the already-established `theta1=0.1` working
value carried over unchanged from the Fase 1 smoke test and Pilot 2A
(both already executed and reviewed in this same session) — **not a new
invention**. Where the plan leaves a value genuinely undetermined
(§8 poin 1), the corresponding scenario is marked **PENDING** rather
than assigned an invented number, per this task's guard ("jangan
menambah grid point tanpa alasan dari preregistered plan").

---

## 1. Frozen cells (ready to run at pilot replicate count)

### Overview table

| cell_id | scenario_id | core/stress | theta0 | theta1 | alpha | beta | true_branching_ratio | pilot_replicates | final_replicates |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| S1-G1 | scenario_1_density_only | core | -2.047943 | 0.1 | 0.0 | 0.6215* | 0.000 | 100 | 1000 |
| S1-G2 | scenario_1_density_only | core | -1.358679 | 0.1 | 0.0 | 0.6215* | 0.000 | 100 | 1000 |
| S1-G3 | scenario_1_density_only | core | -0.665532 | 0.1 | 0.0 | 0.6215* | 0.000 | 100 | 1000 |
| S2-G1 | scenario_2_excitation_only | core | -1.357513 | 0.0 | 0.4207 | 0.6215 | 0.677 | 100 | 1000 |
| S3-G1 | scenario_3_density_plus_excitation | core | -1.357513 | 0.1 | 0.4207 | 0.6215 | 0.677 | 100 (**already run — Pilot 2A**) | 1000 |
| S4-G1 | scenario_4_density_strong_excitation_weak | core | -1.357513 | 0.3 | 0.04207 | 0.6215 | 0.068 | 100 | 1000 |
| S6-G1 | scenario_6_window_n_calibration | core | -1.357513 | 0.1 | 0.4207 | 0.6215 | 0.677 | 100 (**numerically = S3-G1**) | 1000 |
| S7-G1 | scenario_7_density_transform_misspecification | stress | -1.357513 | 0.1 | 0.4207 | 0.6215 | 0.677 | 100 | 1000 |
| S5-G1 | scenario_5_density_weak_excitation_strong | core | -1.357513 | 0.01 | 0.4207 | 0.6215 | 0.6769 | 100 | 1000 |
| S8-G1 | scenario_8_kernel_misspecification_gamma | stress | -1.357513 | 0.1 | n/a (Gamma) | n/a (Gamma) | 0.6769 (target, via Gamma amplitude) | 100 | 1000 |

`*` beta is inert when alpha=0 (no self-excitation term); kept at the
production value only so `validate_beta` (beta>0 required) has a
defined, non-arbitrary input — it has no effect on S1's simulated
process. S8-G1 has no exponential `alpha`/`beta` in its *simulation*
ground truth (it simulates with a Gamma kernel, §1 detail below) — the
`alpha=0.4207`/`beta=0.6215` pair only reappears as the **fitted**
model's free parameters (exponential kernel, deliberately
misspecified).

### Per-cell detail

**S1-G1 / S1-G2 / S1-G3 — `scenario_1_density_only`**
- `scenario_description`: "Density effect saja — alpha=0 (murni M2); theta0, theta1 bervariasi (plan §2 row 1). Tujuan: pastikan fitting M3B-CD tidak memunculkan alpha palsu ketika data murni digerakkan densitas (Gate B poin 1)."
- `theta0` grid: {-2.047943, -1.358679, -0.665532} = ln({0.129, 0.257, 0.514}), the plan's own printed mu-grid (§3 row 1, 0.5x/1x/2x of production mu=0.2573). Note: the plan's printed "0.257" is a rounded display of 0.2573, so S1-G2's theta0 is *not bit-identical* to the production theta0 used elsewhere (-1.357513) — this is an artifact of the plan's own rounding, not introduced here.
- `theta1`: 0.1 for all three, fixed — **not yet varied** (plan §3 explicitly defers theta1's exact grid to implementation, §8 poin 1). This carries over the same "sedang" placeholder already used in Fase 1/Pilot 2A. The plan's stated intent ("theta0, theta1 bervariasi") is therefore only **partially** frozen here (theta0 dimension only); the theta1 dimension of scenario 1's grid remains open.
- `density_specification`: Spec A (`cd_documents_all_accepted`), `CD_ANNUAL_DOCUMENT_DENSITY_WORKING.csv`, window 1600–1784 (plan §3 row "x_CD(t) realisasi": real data used as-is for every scenario, not synthetic).
- `density_transform`: `log1p(1 + CD_t)` (plan §1.3, working candidate).
- `simulation_kernel`: exponential Hawkes (standard) — inert here since alpha=0.
- `fitted_kernel`: exponential Hawkes (M3B-CD estimator, `alpha` free to move off 0).
- `expected_effect_regime`: pure density-driven process; ground truth has zero self-excitation.
- `decision_gates_applicable`: Gate A (hard implementation, always); Gate B poin 1 (false-positive excitation ≤0.05 — this scenario's primary target).

**S2-G1 — `scenario_2_excitation_only`**
- `scenario_description`: "Self-excitation saja — theta1=0 (murni M1); mu≈exp(theta0) dikalibrasi ke mu=0.2573 produksi (plan §2 row 2). Tujuan: pastikan fitting M3B-CD tidak memaksakan theta1 signifikan palsu."
- `theta0 = ln(0.2573) = -1.357513`, `theta1 = 0`, `alpha = 0.4207`, `beta = 0.6215` (all production values, plan §0/§2). With `theta1=0` this cell is, by the audited equivalence proved in Fase 1B (`test_theta1_zero_makes_m3b_cd_baseline_constant_equal_m1`), mathematically identical to production Model 3 (M1) itself.
- `density_specification` / `density_transform`: as S1 (real Spec A data still used to build the covariate lookup, even though theta1=0 makes it inert).
- `simulation_kernel` / `fitted_kernel`: exponential Hawkes.
- `expected_effect_regime`: pure self-exciting process at production branching ratio 0.677; ground truth has zero density effect.
- `decision_gates_applicable`: Gate A; Gate B (theta1 false-significance direction, plan §6 poin 2 / §9 Gate B parameter-recovery metrics for theta1, alpha, beta).

**S3-G1 — `scenario_3_density_plus_excitation`**
- `scenario_description`: "Density + self-excitation bersama — alpha=0.4207, beta=0.6215 (nilai produksi) + theta1 sedang (plan §2 row 3). Kasus paling mendekati realita jika M3B-CD benar."
- Parameters: `theta0=-1.357513, theta1=0.1, alpha=0.4207, beta=0.6215`.
- **This cell was already executed in Pilot 2A** (100 replicates, simulator commit `88acc81`, mean runtime 0.316s/replicate, convergence 1.0, invalid-estimate 0.0, boundary-pileup 0.0). It is listed here for manifest completeness, not to be re-run.
- `decision_gates_applicable`: Gate A; Gate B (full parameter recovery + branching-ratio bias/coverage); Gate C (identifiability — `|correlation(theta1,alpha)|` computed across scenarios 3/4/5 per plan §9 Gate C).

**S4-G1 — `scenario_4_density_strong_excitation_weak`**
- `scenario_description`: "Density sangat kuat, excitation lemah — theta1 besar (3× nilai skenario 3); alpha kecil (0.1× alpha produksi) (plan §2 row 4). Tujuan: uji apakah theta1 'menyerap' sisa variasi yang sebetulnya berasal dari alpha kecil (Gate B poin 2)."
- `theta1 = 3 × 0.1 = 0.3` (plan's explicit multiplier, applied to the already-established scenario-3 theta1); `alpha = 0.1 × 0.4207 = 0.04207` (plan's explicit multiplier); `theta0 = -1.357513`, `beta = 0.6215` (unchanged — plan does not vary these for scenario 4).
- `decision_gates_applicable`: Gate A; Gate B poin 2 (theta1 not systematically absorbing the small true alpha); Gate C.

**S6-G1 — `scenario_6_window_n_calibration`**
- `scenario_description`: "Window & jumlah event ≈ Model 3 — T0=1600, T1=1784 (identik produksi); simulasikan realisasi hingga n≈141 event (target 130–150) (plan §2 row 6). Kalibrasi realistis langsung ke ukuran sampel aktual."
- Parameters: identical to S3-G1 (`theta0=-1.357513, theta1=0.1, alpha=0.4207, beta=0.6215`) — the plan's row 6 only restates the window/production values already used by scenario 3, it does not define a distinct parameter combination. Tracked as a **separate scenario_id** because the plan reports scenario-level metrics separately (§4: "dilaporkan per skenario... bukan agregat tunggal") and because scenario 6's specific purpose (sample-size/window realism) differs from scenario 3's (general joint recovery), even though the ground truth is numerically the same cell.
- Consequence: **Pilot 2A's 100 replicates already constitute this cell's pilot run too** (mean n=129.2, see §3 below).
- `decision_gates_applicable`: Gate A; Gate B (specifically as a check on whether the plan's own identifiability risk §5 poin 5, "window sempit + n kecil," materializes at this exact production-realistic scale).

**S7-G1 — `scenario_7_density_transform_misspecification`**
- `scenario_description`: "Misspecification density — data disimulasikan dengan x_CD(t) versi TIDAK log (mis. linear CD_t) TAPI model fitting tetap memakai log(1+CD_t) (plan §2 row 7). Uji sensitivitas branching ratio terhadap transformasi densitas yang salah dipilih (Gate D)."
- Ground-truth base parameters identical to S3-G1 (`theta0=-1.357513, theta1=0.1, alpha=0.4207, beta=0.6215`) — the plan does not redefine alpha/beta/theta for the stress scenarios, only the transform used for simulation vs. fitting.
- `density_transform`: **simulate** with `x_CD_true(t) = CD_t` (linear, the plan's first-listed example — `sqrt(CD_t)` is noted by the plan as an alternative but not required as a second mandatory cell here, to avoid adding a grid point beyond the minimum the plan requires); **fit** with `log(1+CD_t)` (deliberately misspecified, per plan §1.3/§2 row 7).
- `decision_gates_applicable`: Gate A; **Gate D only** (misspecification stress gate, plan §9 — explicitly a *separate* threshold from Gate B, not compared against Gate B's recovery ambang).

**S5-G1 — `scenario_5_density_weak_excitation_strong`** *(frozen 2026-08-23, Fase 2B-1 — researcher-supplied numeric decision under plan §8 poin 1)*
- `scenario_description`: "Density lemah, excitation kuat (plan §2 row 5). Tujuan: uji apakah alpha/beta bisa dipulihkan tanpa terdistorsi oleh theta1 residual kecil."
- Parameters, as explicitly supplied by the researcher for this freeze: `theta0 = -1.357513` (same as the production-calibrated cells), `theta1 = 0.01`, `alpha = 0.4207`, `beta = 0.6215`, `true_branching_ratio = alpha/beta = 0.6769107 ≈ 0.6769` (matches the researcher-stated value).
- **Note on divergence from the plan's qualitative text**: plan §2 row 5 describes this scenario qualitatively as "excitation kuat, mendekati batas branching ratio 0.9" — the researcher's frozen values here instead reuse the **production branching ratio** (0.6769, same as S3/S6/S7), not a value near the plan's illustrative "~0.9" ceiling. This is recorded as the researcher's explicit, authorized concretization of the previously-undetermined grid point (plan §8 poin 1 requires exactly this kind of sign-off before freezing) — not a manifest-author invention, and not silently reconciled with the plan's qualitative "~0.9" language. The distinguishing feature of scenario 5 relative to scenario 3 is therefore its much smaller `theta1` (0.01 vs 0.1, i.e. density effect an order of magnitude weaker), not a higher branching ratio.
- `density_specification` / `density_transform`: Spec A, `log1p(1+CD_t)`, as all other cells.
- `simulation_kernel` / `fitted_kernel`: exponential Hawkes (standard, matched — no misspecification here; this is a **core** scenario, not a stress test).
- `expected_effect_regime`: near-production self-excitation strength with a much weaker density signal than S3/S6 — tests whether `alpha`/`beta` recovery degrades when the density covariate contributes only a residual effect.
- `decision_gates_applicable`: Gate A; Gate B (parameter recovery for `alpha`, `beta`, branching ratio; per plan §9 Gate E.2 scenario 5 is one of the required core-recovery scenarios); Gate C (identifiability — scenario 5 is explicitly one of the 3/4/5 correlation-check scenarios in plan §9 Gate C).
- `core_or_stress_scenario`: `core_scenario` (per this task's instruction).

**S8-G1 — `scenario_8_kernel_misspecification_gamma`** *(frozen 2026-08-23, Fase 2B-1 — researcher-supplied numeric decision under plan §8 poin 6)*
- `scenario_description`: "Kernel Gamma disimulasikan, di-fit eksponensial (plan §2 row 8). Uji apakah misspecification kernel mendistorsi alpha/beta/branching ratio yang dipulihkan."
- Parameters, as explicitly supplied by the researcher for this freeze: `theta0 = -1.357513` (production baseline), `theta1 = 0.1` (same as S3/S6/S7), target self-excitation `branching_ratio = 0.6769`.
- `simulation_kernel`: **Gamma**, `shape (k) = 2`, `rate (θ) = 2.38095` (equivalently `scale = 1/θ ≈ 0.42000`). Mode of this Gamma density = `(k−1)/θ = 1/2.38095 = 0.42000` years — matches the researcher-stated "mode lag ≈ 0.42 tahun" exactly.
- `fitted_kernel`: exponential (standard M3B-CD estimator, unchanged — deliberate misspecification, per plan §2 row 8).
- **Gamma kernel amplitude — integral normalization (verified, §3 below)**: the excitation kernel used for simulation is `kernel(s) = A · GammaPDF(s; k=2, θ=2.38095)`, where `GammaPDF` integrates to exactly 1 over `[0, ∞)` by construction. The amplitude `A` was **not** set to the exponential kernel's `alpha=0.4207`, per this task's explicit instruction — instead `A = 0.6769` (the target branching ratio itself), so that `∫₀^∞ kernel(s) ds = A · 1 = 0.6769` reproduces the target branching ratio directly. Numerically verified via `scipy.integrate.quad` (see §3).
- `density_specification` / `density_transform`: Spec A, `log1p(1+CD_t)` (unchanged from all other cells — scenario 8 tests kernel misspecification only, not density-transform misspecification, which is S7's separate concern).
- `expected_effect_regime`: self-exciting process with a heavier-tailed, delayed-onset (mode 0.42y, not instantaneous-peak like the exponential kernel) excitation kernel than the fitted model assumes — tests whether the branching ratio recovered under the wrong (exponential) kernel assumption is systematically biased.
- `decision_gates_applicable`: Gate A; **Gate D only** (misspecification stress gate — separate threshold from Gate B, plan §9, same treatment as S7-G1).
- `core_or_stress_scenario`: `misspecification_stress_scenario` (per this task's instruction).

---

## 2. Boundary-gate applicability clarification

*(Added 2026-08-23, Fase 2B-1 — clarifies how the already-observed
boundary-pileup diagnostic from the 8-cell Fase 2B pilot run is to be
read against plan §9's gates. No numerical threshold is changed by this
clarification.)*

1. **Boundary-pileup as a hard-implementation-gate (Gate A) concern
   applies only when the parameter's true value is in the interior of
   its allowed range.** Gate A's role is to catch *optimizer*
   pathology (failure to converge, wandering to a bound it should not
   need to touch) — that diagnosis is only meaningful when there is no
   structural reason for the estimate to sit at the bound in the first
   place.
2. **For `alpha_true = 0`** (S1-G1/G2/G3, all three theta0 grid
   points): the true value is *exactly* at the lower bound
   (`alpha ∈ [0, ∞)`). A high boundary-pileup rate here (observed:
   0.56–0.59 in the Fase 2B pilot) is the **expected, correct**
   behavior of a well-behaved estimator — it is reported (never
   suppressed, per plan §6 poin 5) but is **not** treated as an
   implementation failure and does **not** by itself fail Gate A.
3. **For `alpha_true > 0` but small** (S4-G1, `alpha=0.04207`;
   observed boundary-pileup 0.42): the true value is technically
   interior, but close enough to the bound that some replicates'
   estimates land on or near it by finite-sample noise. This case is
   **not** a Gate A implementation failure either, but it **remains a
   live identifiability diagnostic** — a high boundary-pileup rate
   here is exactly the kind of signal plan §5 poin 2 ("alpha menyerap
   efek densitas," arah sebaliknya) and §9 Gate C are designed to
   surface. It must still be reported per grid-point (plan §4) and
   does **not** get a pass on Gate B (parameter-recovery) or Gate C
   (identifiability) simply because the true value is near a boundary —
   near-boundary truth is precisely the regime those gates need to be
   evaluated most carefully in, not a regime where they are waived.

---

## 3. Expected event-count review (Pilot 2A vs. production reference)

- Target reference (Model 3 production, pure Hawkes on real 141-event
  data): **141 events**.
- Pilot 2A mean (S3-G1 / S6-G1, 100 replicates): **129.2 events**
  (stdev 29.6, range 66–203).
- Relative difference: (129.2 − 141) / 141 ≈ **−8.37%**.

**Consistency check against the plan's own scenario definitions** (not a
recalibration):

1. The 141-event target is not a stated ground-truth requirement for
   **scenario 3** — the plan attaches that target specifically to
   **scenario 6** ("simulasikan realisasi hingga n≈141 event, target
   130–150"). Because S6-G1 and S3-G1 share an identical parameter
   combination (§1 above), Pilot 2A's result already answers scenario
   6's question: 129.2 sits essentially at the lower edge of the
   130–150 target band, and the gap (0.8 events) is far smaller than
   the standard error of the mean (stdev/√100 ≈ 2.96) — i.e., not a
   statistically notable miss.
2. Scenario 3/6 is **not** the pure production M1 process — it adds a
   density term (`theta1=0.1 * x_CD(t)`) on top of an `exp(theta0)`
   baseline calibrated to match production `mu`. There is no plan
   requirement that this combined process reproduce exactly 141 events;
   141 is the pure-M1 production count, a *related* but distinct
   reference point, not this scenario's ground truth target.
3. The observed cross-replicate spread (66–203, stdev 29.6) is large
   relative to the ~12-event gap from 141, and finite-window,
   moderate-branching-ratio (0.677) Hawkes processes are explicitly
   flagged by the plan itself (§5 poin 5) as a regime where
   "bias parameter Hawkes DIKETAHUI bisa besar" — i.e., deviation from
   a naive reference count is an *expected* feature of this regime, not
   a signal of a defect.

No recalibration was performed (per this task's explicit instruction).
A rigorous analytic (not just qualitative) check of the expected count
under finite-window truncation is left to Fase 2B's technical audit
stage, not this manifest-freezing step.

**Status:**
```
EXPECTED_COUNT_CONSISTENT_WITH_PLAN
```

---

## 4. Runtime budget (revised — 10 frozen cells)

Using the flat `mean_per_replicate = 0.316` seconds baseline (Pilot
2A's measured value) and `jumlah_cell = 10` (8 already technically
verified in Fase 2B + the 2 newly-frozen S5-G1/S8-G1):

```
pilot_runtime_serial  = 10 cells × 100 replicates × 0.316 s = 316.0 s  (~5.27 min)
final_runtime_serial  = 10 cells × 1000 replicates × 0.316 s = 3160.0 s (~52.67 min, ~0.88 h)
```

**Provisional caveat for S8-G1 specifically**: the flat 0.316s/replicate
figure is carried over from the exponential-kernel cells actually
measured in Fase 2B. S8-G1 simulates with a **Gamma** kernel (not
exponential), which was not exercised by any previously-measured cell —
its Ogata-thinning upper-bound recomputation may be more expensive per
event (Gamma density evaluation vs. a closed-form exponential). This
projection will be corrected with S8-G1's own measured runtime once its
100-replicate pilot (instructed as the next step, not part of this
manifest update) actually runs.

### Ideal parallel projection (no overhead modeled)

| Workers | Pilot (100/cell × 10 cells) | Final (1000/cell × 10 cells) |
|---|---:|---:|
| 1 (serial) | 316.0 s | 3160.0 s |
| 2 | 158.0 s | 1580.0 s |
| 4 | 79.0 s | 790.0 s |
| 8 | 39.5 s | 395.0 s |

**These parallel figures are ideal linear-speedup projections only.**
They do not account for process-startup overhead, I/O contention when
writing per-replicate output, CSV/covariate-loading amortization across
workers, or scheduling overhead — actual parallel runtime will be
higher than shown.

---

## 5. Manifest-level counts (revised)

| Metric | Value |
|---|---:|
| Scenarios defined in plan §2 | 8 |
| Scenarios frozen (executable) | **8 (all — scenario 1, 2, 3, 4, 5, 6, 7, 8)** |
| Scenarios pending (not frozen) | **0** |
| Grid points — core scenarios (frozen) | 8 (S1×3, S2, S3, S4, S5, S6) |
| Grid points — stress scenarios (frozen) | 2 (S7, S8) |
| Total frozen cells | **10** (8 already technically verified via Fase 2B pilot + 2 newly frozen, not yet piloted) |
| Cells already pilot-verified (Fase 2B, 2026-08-23) | 8 (S1-G1/G2/G3, S2-G1, S3-G1, S4-G1, S6-G1, S7-G1 — all `CELL_TECHNICALLY_READY`) |
| Cells newly frozen, **not yet piloted** | 2 (S5-G1, S8-G1) |
| `pilot_replicates` per cell | 100 (plan §9, frozen — unchanged) |
| `final_replicates` per cell | 1000 (plan §9, frozen — unchanged) |
| Pilot runtime, serial (10 cells) | 316.0 s (~5.27 min) |
| Final runtime, serial (10 cells) | 3160.0 s (~52.67 min) |
| Pilot runtime, 8 workers (ideal) | 39.5 s |
| Final runtime, 8 workers (ideal) | 395.0 s |
| Expected-event-count review | `EXPECTED_COUNT_CONSISTENT_WITH_PLAN` (unchanged — based on S3-G1/S6-G1 only) |
| Gamma kernel integral verification (S8-G1) | `∫ kernel ds = 0.6769` exact (quad abs. error ≈ 2.3×10⁻¹³); mode = 0.42000y (target ≈0.42y) |

---

## 6. Readiness decision (revised)

All 10 frozen cells (§1) are individually well-defined: 8 trace to the
plan's own printed grid/multipliers (unchanged from the prior manifest
revision) and are already pilot-verified (`CELL_TECHNICALLY_READY`,
Fase 2B, 2026-08-23); the 2 newly-added cells (S5-G1, S8-G1) carry
explicit, complete numeric parameters supplied by the researcher for
this freeze (this task's own instructions), resolving the previously
open plan §8 poin 1 (scenario 5) and §8 poin 6 (scenario 8) decisions.
**No scenario remains pending.** S5-G1's amplitude/branching-ratio
choice and S8-G1's Gamma-kernel amplitude were derived per the explicit
constraints given (branching ratio target, no reuse of the exponential
`alpha` as a Gamma amplitude without integral normalization — verified
in §1 above) rather than invented independently.

S5-G1 and S8-G1 are **frozen but not yet piloted** — their 100-replicate
technical pilot is the explicitly instructed next step, not part of
this manifest-freezing update.

**Status:**
```
CELL_MANIFEST_READY
```

**Reason**: all 8 plan-defined scenarios now have at least one frozen,
fully-specified grid point (10 cells total); 8/10 cells are already
pilot-verified technically ready, and the remaining 2 (S5-G1, S8-G1)
have complete, traceable parameters awaiting only their own 100-
replicate technical pilot — no further researcher parameter decision is
outstanding.

---

**STOP** — manifest freeze complete. No simulation was run, no
parameter was changed from Pilot 2A/Fase 2B results, no grid point was
added beyond what the researcher explicitly authorized for S5/S8 in this
task's instructions, no fitting of 141 real events was performed, the
simulator (commit `88acc81`) was not modified, the CD density series was
not modified, and no Graphify/Git/deploy action was taken.
