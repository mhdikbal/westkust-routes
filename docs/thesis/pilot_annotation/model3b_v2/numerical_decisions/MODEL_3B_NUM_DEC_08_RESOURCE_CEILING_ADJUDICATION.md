# NUM-DEC-08 Adjudication: Model 3B Operational Resource Ceiling

> **Design/decision only. No M0, M2, or M3 source file modified or created. No new benchmark executed. No tournament run. No historical data fitted. Nothing staged, committed, pushed, or deployed.**

> **This is the final numerical decision.** With NUM-DEC-08 adjudicated, the ledger reaches 7 `APPROVED_WITH_LIMITATIONS` + 1 `DEFERRED` (NUM-DEC-07) + 0 `PENDING_RESEARCHER_DECISION`.

---

## 1. Scope

This document adjudicates **NUM-DEC-08 only**: the operational resource ceiling governing any future Model 3B amended recovery tournament (M0/M2/M3). It is the eighth and last of the eight unresolved numerical decisions opened by `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv`. No implementation, no benchmark execution, no tournament run, and no historical-data fitting is authorized by this decision.

## 2. Authoritative Evidence

Read in full before adjudication:

```text
MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md
MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv          (51-row V2 gate spec)
MODEL_3B_RECOVERY_PROTOCOL_V2.md
MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv
MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv            (8-row ledger; NUM-DEC-01..06 APPROVED_WITH_LIMITATIONS,
                                                        NUM-DEC-07 DEFERRED, prior to this turn)
MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md
MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md
MODEL_3B_NUM_DEC_03_M2_EXACT_NULL_ADJUDICATION.md
MODEL_3B_NUM_DEC_04_M3_TAU_CALIBRATION_ADJUDICATION.md
MODEL_3B_NUM_DEC_05_M3_PRIOR_MODEL_ODDS_ADJUDICATION.md
MODEL_3B_NUM_DEC_06_M3_MARGINAL_LIKELIHOOD_ADJUDICATION.md
MODEL_3B_NUM_DEC_07_M3_ROPE_ADJUDICATION.md
```

Pilot resource evidence read directly (Section 4):

```text
docs/thesis/colab/model3b_tournament_harness/recovery_results/m0_run.log
docs/thesis/colab/model3b_tournament_harness/recovery_results/m2_run.log
docs/thesis/colab/model3b_tournament_harness/recovery_results/m3_run.log
docs/thesis/colab/model3b_tournament_harness/recovery_results/{m0,m2,m3}_raw_replicates.csv (file sizes only)
docs/thesis/colab/model3b_tournament_harness/run_recovery_{m0,m2,m3}.py (grepped for worker/concurrency config)
```

Baseline confirmed before this turn: 70/70 original gates reconciled to 51 V2 gates; NUM-DEC-01 through 06 = `APPROVED_WITH_LIMITATIONS`; NUM-DEC-07 = `DEFERRED`; NUM-DEC-08 = `PENDING_RESEARCHER_DECISION`.

## 3. Mathematical Question

A future amended M0/M2/M3 recovery tournament requires wall-clock time, CPU time, memory, and storage. The pilot run that this conversation's earlier work produced measured only the *old*, now-superseded architecture (M2 point-fit only, no profile likelihood/bootstrap; M3 single unconstrained-n MCMC only, no separate M0/M1 posteriors, no bridge sampling, no thermodynamic integration). NUM-DEC-08 resolves: **what operational resource envelope should govern a future amended tournament, and how should it be derived — from actual measured evidence, or from an unsupported round number?**

## 4. Pilot Resource Evidence

Parsed directly from the run logs with a `re.match` regex per candidate (full arithmetic reproduced below, not asserted):

### M0

```text
Cells:                          15  (S1-G1/G2/G3, S3-G1, S4-G1 x {poisson_limit, moderate_overdispersion, high_overdispersion})
Attempted replications/cell:    1,000  (n=1000 in every logged line)
Total attempted replications:   15,000
Elapsed wall time (sum of per-cell log times, serial): 4,833.2 s = 80.55 min = 1.343 h
Per-cell wall time range:       174.1 s (S1-G3/high_overdispersion) to 490.8 s (S4-G1/poisson_limit)
Per-replication time (cell wall time / n): min 0.1741 s, median 0.3247 s, mean 0.3222 s, max 0.4908 s
  (this is a CELL-LEVEL average, not a per-replication raw distribution -- see Section 5)
CPU time:                       NOT_RECORDED (log records wall time only)
Maximum concurrent processes:   NOT_RECORDED (see Section 4, worker-config grep below)
Machine/environment:            see Section 4 "Environment" subsection
Logical CPU count (this audit's inspection machine): 4
Available memory (this audit's inspection machine): 5.8 GiB total, 4.0 GiB available
Peak memory (measured during the pilot run itself): NOT_RECORDED
Output size:                    m0_raw_replicates.csv = 1,321,605 bytes for 15,000 replications
                                 = 88.11 bytes/replication (raw CSV, uncompressed)
Checkpoint size:                NOT_RECORDED (no checkpoint mechanism found in run_recovery_m0.py -- see Section 4)
Temporary storage:              NOT_RECORDED
Failed-run count:               reported only as `invalid` fraction per cell in the log (0.000-0.010), not
                                 as an absolute failed-replication count with disposition
p90 / p95 runtime (per-replication): NOT_AVAILABLE -- only per-cell aggregate wall time was logged, not a
                                 per-replication timing distribution; p90/p95 cannot be computed from this evidence
Runtime variance:                across the 15 per-cell average times: range 0.317 s (0.174 to 0.491), no
                                 within-cell variance available
Timings include setup/summary?: NOT_RECORDED -- the log line format (`t=...s`) does not document what is
                                 included; the trailing "Wrote ... .csv" line suggests summary-file writing
                                 may occur after the last logged `t=` value and is therefore NOT included in
                                 the per-cell times shown
```

### M2

```text
Cells:                           4  (S1-equiv-alpha0, S3-equiv, S5-equiv, S6-equiv)
                                  -- NOTE: this is NOT the same 15-cell grid M0 used; the M2 pilot ran a
                                  4-cell subset only
Attempted replications/cell:     150  (n=150 in every logged line)
                                  -- NOTE: this is the PRE-NUM-DEC-01 pilot scale. NUM-DEC-01 (already
                                  adjudicated) fixes the future requirement at 1,000 ATTEMPTED replications
                                  per cell, not 150. Any cost projection from this evidence must scale by
                                  (1,000/150) for replication count alone, before adding the NUM-DEC-02/03
                                  cost components entirely absent from this pilot (see Section 10).
Total attempted replications:    600
Elapsed wall time (sum, serial): 7,625.6 s = 127.09 min = 2.118 h
Per-cell wall time range:        1,293.2 s (S6-equiv) to 2,788.3 s (S3-equiv)
Per-replication time (cell wall time / n): min 8.6213 s, median 11.8137 s, mean 12.7093 s, max 18.5887 s
CPU time:                        NOT_RECORDED
Maximum concurrent processes:    NOT_RECORDED (no worker config found -- Section 4)
Peak memory:                     NOT_RECORDED
Output size:                     m2_raw_replicates.csv = 52,628 bytes for 600 replications
                                  = 87.71 bytes/replication
Checkpoint size:                 NOT_RECORDED (no checkpoint mechanism found)
Failed-run count:                reported only as `invalid` fraction per cell (0.000-0.013)
p90 / p95 runtime:                NOT_AVAILABLE (same limitation as M0)
Runtime variance:                across 4 per-cell average times: range 9.97 s (8.62 to 18.59)
Cost basis limitation:           this timing reflects POINT FITTING ONLY (single alpha/beta MLE per
                                  replication). It does NOT include profile-likelihood optimization over a
                                  grid (NUM-DEC-02), parametric-bootstrap null calibration (NUM-DEC-03), or
                                  independent evaluation-set fitting -- all mandatory for the amended M2.
```

### M3

```text
Cells:                            4  (S1-equiv-n0, S3-equiv, S5-equiv, S6-equiv -- same naming convention as M2,
                                   also a 4-cell subset, not the full 15-cell grid)
Attempted replications/cell:      200  (n=200 in every logged line)
Total attempted replications:     800
Elapsed wall time (sum, serial):  6,160.4 s = 102.67 min = 1.711 h
Per-cell wall time range:         986.6 s (S6-equiv) to 1,829.5 s (S5-equiv)
Per-replication time (cell wall time / n): min 4.9330 s, median 8.3607 s, mean 7.7005 s, max 9.1475 s
CPU time:                         NOT_RECORDED
Maximum concurrent processes:     NOT_RECORDED
Peak memory:                      NOT_RECORDED
Output size:                      m3_raw_replicates.csv = 73,912 bytes for 800 replications
                                   = 92.39 bytes/replication
Checkpoint size:                  NOT_RECORDED
Failed-run count:                 not reported as failures; `conv=1.000` and `acc=` (MCMC acceptance rate,
                                   0.458-0.484) reported per cell instead
p90 / p95 runtime:                 NOT_AVAILABLE
Runtime variance:                 across 4 per-cell average times: range 4.21 s (4.93 to 9.15)
Cost basis limitation:            this timing reflects a SINGLE unconstrained-n Metropolis-Hastings run
                                   (500 draws + 200 burn-in per the module's own default, per
                                   `m3_bayesian_discrete.py` inspected during NUM-DEC-06). It does NOT include
                                   a separate M0 (exact-null) posterior run, bridge-sampling repetitions,
                                   proposal fitting, bridge-stability checks, or thermodynamic integration --
                                   all mandatory for the amended M3 (NUM-DEC-04/05/06).
```

### Environment

```text
Worker/concurrency config search: `grep -n "worker|Pool|concurrent|multiprocess|n_jobs|parallel"` across
  run_recovery_m0.py, run_recovery_m2.py, run_recovery_m3.py returned NO MATCHES. The pilot appears to have
  executed each cell SERIALLY within a single process -- effectively W=1. No parallel-efficiency evidence
  (eta_parallel) exists; it is NOT_MEASURED, not zero and not assumed to be 1.
Production-reference search:      `grep -rn "westkust-prod|prod_host|silida.org"` across the harness
  directory (.py and .log files) returned NO MATCHES. Nothing in the evidence indicates the pilot ran on
  westkust-prod.
This audit's own inspection machine (read-only characterization only, NOT a benchmark, and not confirmed to
be the identical machine that produced the pilot logs above):
  Logical CPUs:    4  (`nproc`)
  Memory:          5.8 GiB total, 1.6 GiB free, 4.0 GiB available (`free -h`)
  Disk:            1007 GiB total, 18 GiB used, 938 GiB available (`df -h` on the repository filesystem)
File timestamps (mtime) of pilot outputs, DERIVED_FROM_FILE_TIMESTAMPS class only, not exact CPU time:
  m0_run.log / m0_raw_replicates.csv / m0_summary.csv: 2026-08-29 20:26
  m2_run.log / m2_raw_replicates.csv / m2_summary.csv: 2026-08-29 21:15
  m3_run.log / m3_raw_replicates.csv / m3_summary.csv: 2026-08-29 20:50
  (M0 finished before M3, which finished before M2 -- consistent with the three being run as separate,
  sequential invocations rather than concurrently, though this is inferred from timestamps, not measured)
```

## 5. Evidence-Provenance Classification

| Observation | Classification |
|---|---|
| Per-cell wall time (`t=...s` in run.log) | `DERIVED_FROM_RUN_MANIFEST` |
| Per-replication time (cell time / n) | `DERIVED_FROM_RUN_MANIFEST` (a cell-level average, not a per-replication raw measurement) |
| p90 / p95 / true runtime distribution | `NOT_AVAILABLE` |
| CPU time (as opposed to wall time) | `NOT_AVAILABLE` |
| Peak memory during the pilot run | `NOT_AVAILABLE` |
| Worker/concurrency count during the pilot run | `DERIVED_FROM_RUN_MANIFEST` (inferred as W=1 from absence of any worker-pool code, not directly logged) |
| Output file sizes | `DIRECTLY_MEASURED` (via `ls -la` on the actual files) |
| File mtimes / run ordering | `DERIVED_FROM_FILE_TIMESTAMPS` |
| Checkpoint size / mechanism | `NOT_AVAILABLE` (no checkpoint code found) |
| This audit's local-machine CPU/memory/disk | `DIRECTLY_MEASURED` (via `nproc`/`free -h`/`df -h`, characterizing this inspection session only) |
| Whether the pilot ran on the identical machine as this audit's inspection | `NOT_AVAILABLE` — classified `UNKNOWN_ENVIRONMENT` for the pilot run itself |

Do not treat file timestamps as exact CPU time (per instruction). None of the above are treated as such in Section 4.

## 6. Researcher Decision

```text
NUM-DEC-08:                          APPROVED_WITH_LIMITATIONS
DECISION TYPE:                       EVIDENCE_DERIVED_OPERATIONAL_RESOURCE_ENVELOPE
SELECTED OPTION:                     EVIDENCE_DERIVED_STAGED_RESOURCE_ENVELOPE
RESOURCE CEILING:                    NOT A SINGLE ARBITRARY NUMBER -- a layered operational envelope
                                      (Section 14) with formulas (Section 9, 12, 13) and stop rules
                                      (Section 17); numeric fields PENDING_MEASUREMENT (Section 16 below,
                                      formerly requested as a standalone section, folded into Section 14)
PRIMARY EXECUTION ENVIRONMENT:       DEDICATED_NONPRODUCTION_RESEARCH_ENVIRONMENT
PRODUCTION EXECUTION:                PROHIBITED
BUDGET BASIS:                        MEASURED_PILOT_COST_PLUS_VALIDATED_COMPONENT_OVERHEAD
IMPLEMENTATION:                      NOT_AUTHORIZED
SMALL SYNTHETIC PROFILING:           AUTHORIZED_ONLY_AS_PREIMPLEMENTATION_RESOURCE_MEASUREMENT IN A FUTURE
                                      SEPARATELY-AUTHORIZED TURN -- NOT authorized in this turn
FULL TOURNAMENT:                     NOT_AUTHORIZED
HISTORICAL FIT:                      NOT_AUTHORIZED
```

**No new benchmark was executed to produce this document.** Section 4's evidence is entirely reconstructed from files that already existed on disk before this adjudication began.

## 7. Execution Environment

The future amended tournament's primary execution environment is `DEDICATED_NONPRODUCTION_RESEARCH_ENVIRONMENT` — a machine or container distinct from `westkust-prod` (the production Docker host serving the live Django/FastAPI application). Evidence in Section 4 confirms the pilot itself contains no references to production hostnames or paths, consistent with prior execution having already respected this boundary, though the exact identity of the pilot's execution machine cannot be confirmed from available evidence (`UNKNOWN_ENVIRONMENT`, Section 5).

## 8. Production Prohibition

The production host and its running containers must **not** be used for: full tournament execution; bridge-sampling calibration; thermodynamic integration; large bootstrap runs; resource saturation tests; stress testing; historical model fitting. Production may be inspected read-only for status only (matching the established pattern used throughout this conversation for `westkust-prod` sync verification) — no benchmark or model execution is authorized there, and none occurred in producing this document.

## 9. Runtime Model

```text
For candidate m, cell c:
  R_attempt(m,c)  = planned attempted replications
  t_hat(m,c)      = estimated wall-clock time per attempted replication

  T_serial_hat    = sum over m,c of R_attempt(m,c) * t_hat(m,c)
  T_ideal_hat     = T_serial_hat / W                          (W = worker count; NOT used operationally)
  T_parallel_hat  = T_serial_hat / (W * eta_parallel)
  T_total_hat     = T_parallel_hat + T_calibration_hat + T_validation_hat
                    + T_summary_hat + T_checkpoint_overhead_hat
  T_budget        = s_T * T_total_hat
```

Applying `t_hat(m,c)` from the DIRECTLY-derived pilot medians (Section 4) as illustrative arithmetic only — **not** a frozen projection, because none of the missing cost components (Section 10, 11) are included and `eta_parallel`/`s_T` are unmeasured:

```text
T_serial_hat (pilot-architecture-only, POINT-FIT COST, missing NUM-DEC-02/03/04/05/06 components):
  M0: 15,000 attempted x 0.3222 s (mean)  ~ 4,833 s   (matches the measured sum exactly, since this IS the
                                                        measured sum -- consistency check passes)
  M2: 600 attempted x 12.7093 s (mean)    ~ 7,626 s   (at 150/cell; NUM-DEC-01 requires 1,000/cell, so a
                                                        replication-count-only scale-up gives
                                                        7,626 s * (1000/150) ~ 50,838 s per the SAME
                                                        4-cell subset -- still excludes profile-likelihood
                                                        and bootstrap cost entirely)
  M3: 800 attempted x 7.7005 s (mean)     ~ 6,160 s   (single unconstrained-n MCMC only; excludes the
                                                        separate M0/M1 posteriors, bridge sampling, and TI
                                                        entirely)

eta_parallel: NOT_MEASURED (pilot ran serially, W=1 inferred -- Section 4)
s_T:          RESEARCHER_POLICY_PENDING_MEASUREMENT (no runtime-variability evidence exists to derive it;
              not invented here per instruction)
T_calibration_hat, T_validation_hat, T_summary_hat, T_checkpoint_overhead_hat: PENDING_MEASUREMENT
  (none of these were separately instrumented in the pilot logs)
T_total_hat, T_budget: NOT COMPUTED -- insufficient measured components to combine responsibly; computing a
  single number here would misrepresent an incomplete formula as a resource decision, which this
  adjudication explicitly avoids (Section 16).
```

## 10. M2 Cost Components

M2's future execution includes, per NUM-DEC-01/02/03: 1,000 attempted replications/cell (not 150 — see Section 4); null-model fit; excitation-model fit; profile likelihood for `n` over a grid; nuisance reoptimization at every profile point; parametric-bootstrap null calibration; independent null evaluation; positive-scenario FNR/power evaluation. A single M2 attempted replication may therefore require **multiple** optimizer calls, not the single point-fit the pilot measured:

```text
N_fit_M2 (approx.)  =  N_base_fits  +  G * K  +  N_bootstrap_related_fits
```

where `G` (profile-grid size) and `K` (starts per profile point) are future implementation design parameters, **not selected here**. The measured pilot cost (Section 4, M2) reflects `N_base_fits` alone and must not be treated as a proxy for the full future `N_fit_M2` cost.

## 11. M3 Cost Components

M3's future execution includes, per NUM-DEC-03(applicable-to-M2 analogue)/04/05/06: separate exact-null (M0) and excitation (M1) posterior runs; multiple chains; warmup; posterior sampling; bridge-sampling repetitions; proposal fitting; bridge-stability tests; the three NUM-DEC-05 prior-sensitivity scenarios; calibration and evaluation sets (NUM-DEC-04); thermodynamic integration on the NUM-DEC-06 prespecified validation subset; checkpointing; raw posterior diagnostics; summary generation:

```text
T_M3  =  T_M0_posterior  +  T_M1_posterior  +  T_bridge  +  T_TI_subset  +  T_diagnostics
```

The measured pilot cost (Section 4, M3) reflects a single unconstrained-`n` Metropolis-Hastings run only (`T_M1_posterior`-equivalent, and even that without the NUM-DEC-06-mandated Jacobian correction or proper prior normalization). `T_M0_posterior`, `T_bridge`, `T_TI_subset`, and `T_diagnostics` are entirely unmeasured — none of that code exists yet (confirmed during NUM-DEC-06's compatibility audit). Estimating M3 cost from the pilot MCMC run alone would systematically and substantially understate the true future cost.

## 12. Storage Model

```text
S_total_hat  =  sum over m,c of R_attempt(m,c) * s_hat(m,c)
                + S_posterior + S_profile + S_checkpoint + S_summary + S_manifest
```

Measured per-replication raw-row storage (uncompressed CSV, Section 4): M0 ≈ 88.11 bytes/replication; M2 ≈ 87.71 bytes/replication; M3 ≈ 92.39 bytes/replication. These populate `s_hat(m,c)` for `RAW_REPLICATION_ROWS` only.

| Storage class | Status |
|---|---|
| `RAW_REPLICATION_ROWS` | Measured for the pilot architecture (above); future schema will differ (more columns for profile grids, bridge diagnostics, etc.) — `PENDING_MEASUREMENT` for the amended format |
| `POSTERIOR_DRAWS` | `PENDING_MEASUREMENT` (no posterior-draw persistence observed in the pilot) |
| `PROFILE_LIKELIHOOD_OUTPUTS` | `PENDING_MEASUREMENT` (not yet implemented) |
| `BRIDGE_OUTPUTS` | `PENDING_MEASUREMENT` (not yet implemented) |
| `THERMODYNAMIC_INTEGRATION_OUTPUTS` | `PENDING_MEASUREMENT` (not yet implemented) |
| `CHECKPOINTS` | `PENDING_MEASUREMENT` (no checkpoint mechanism found in the pilot code) |
| `LOGS` | Measured for the pilot scale: `m0_run.log` 1,790 bytes / 15 cells; `m2_run.log` 783 bytes / 4 cells; `m3_run.log` 586 bytes / 4 cells — negligible relative to raw rows, but future logging verbosity is undetermined |
| `SUMMARIES` | Measured for the pilot scale: `m0_summary.csv` 2,742 bytes; `m2_summary.csv` 1,501 bytes; `m3_summary.csv` 941 bytes |
| `MANIFESTS` | `PENDING_MEASUREMENT` (no seed-manifest files observed in the pilot; NUM-DEC-01/04 both require them for the future implementation) |

Compressed vs. uncompressed: not assumed — only uncompressed (as-stored) sizes are reported above, per instruction not to assume a compression ratio without measurement.

## 13. Memory Model

```text
M_peak_estimate  =  W * M_worker_peak  +  M_coordinator  +  M_buffer
Concurrency must satisfy:  M_peak_estimate <= M_usable_limit
```

`M_worker_peak` is `NOT_RECORDED` for any candidate (Section 4 — no peak-memory instrumentation in the pilot). Worker count `W` was effectively 1 (serial execution, Section 4) — no concurrency was exercised, so no evidence exists for how memory scales with `W > 1`. Setting a future worker count equal to logical CPU count is explicitly **not** authorized automatically; memory and CPU must be reserved for OS, filesystem cache, checkpoint writing, monitoring, and process coordination, per the researcher's instruction — none of these reservations can be sized from current evidence.

## 14. Operational Envelope Dimensions

The future resource ceiling must define all fifteen dimensions separately — it is not reducible to one wall-clock number:

```text
 1. Maximum concurrent workers               PENDING_MEASUREMENT
 2. Maximum wall-clock duration per wave      PENDING_MEASUREMENT
 3. Maximum total CPU-hours                   PENDING_MEASUREMENT
 4. Maximum peak memory                       PENDING_MEASUREMENT
 5. Maximum working-disk usage                PENDING_MEASUREMENT
 6. Minimum free disk before start             PENDING_MEASUREMENT
 7. Maximum output size                       PENDING_MEASUREMENT
 8. Checkpoint interval                       PENDING_MEASUREMENT
 9. Maximum retry count                       PENDING_MEASURED_RESOURCE_POLICY (Section 18)
10. Maximum consecutive infrastructure failures PENDING_MEASUREMENT
11. Per-replication timeout                    PENDING_MEASUREMENT
12. Per-cell timeout                           PENDING_MEASUREMENT
13. Marginal-likelihood failure ceiling         PENDING_MEASUREMENT
14. Posterior-diagnostic failure ceiling        PENDING_MEASUREMENT
15. Shutdown and resume policy                 defined qualitatively in Section 18 (retry policy); no
                                               numeric parameter attached
```

No dimension above is populated with an invented default. This is the direct consequence of Section 4's finding that the pilot evidence does not cover memory, CPU time, concurrency, checkpointing, or the cost of any of the NUM-DEC-02/03/04/05/06-mandated components.

## 15. Staged Execution Waves

Future implementation must proceed through staged, checkpointed waves — none of which is authorized by this adjudication:

```text
WAVE R0: environment and dependency validation
WAVE R1: single-cell implementation smoke test
WAVE R2: small multi-scenario resource benchmark
WAVE R3: M0 corrected synthetic validation
WAVE R4: M2 implementation and resource validation
WAVE R5: M3 exact-null and posterior validation
WAVE R6: bridge-sampling stability benchmark
WAVE R7: thermodynamic-integration subset benchmark
WAVE R8: calibration-set execution                    -- STOP AND RESEARCHER REVIEW --
WAVE R9: independent final recovery evaluation
```

Every wave requires successful checksums and reconciliation before the next wave begins. **NUM-DEC-08 does not authorize any wave**, including R0.

## 16. Resource Freeze Gate

Before full-execution authorization, a future benchmark report must contain: exact hardware; operating system; runtime environment; dependency versions; candidate implementation commit; gate-specification checksum; protocol checksum; cell count; measured runtime distribution; measured memory; measured output size; projected total runtime; projected CPU-hours; projected storage; selected worker count; safety factor and its provenance; the operational ceilings (Section 14, populated); abort conditions (Section 17).

```text
Required future status:  MODEL_3B_RESOURCE_ENVELOPE_MEASURED_AND_FROZEN
Without that status:     FULL_TOURNAMENT_EXECUTION_BLOCKED
```

This document does not produce that status — Section 14's fifteen dimensions remain unpopulated, which is the expected and correct outcome of adjudicating a *procedure* rather than measuring a *number* in this turn.

## 17. Stop Conditions

Future execution must stop on any of the following sixteen conditions, preserving completed immutable outputs:

```text
 1. Disk free space below the approved minimum
 2. Memory use above the approved ceiling
 3. Repeated out-of-memory termination
 4. Repeated corrupted output
 5. Duplicate replication ID
 6. Duplicate seed
 7. Checksum mismatch
 8. Checkpoint reconciliation failure
 9. Source or specification drift
10. Abnormal model-comparison failure rate
11. Material bridge/TI disagreement
12. Invalid posterior diagnostics
13. Runaway per-replication runtime
14. Production host detection
15. Historical-data access during synthetic recovery
16. Researcher-issued stop
```

## 18. Retry Policy

```text
Model or optimizer failure:      NO AUTOMATIC REPLACEMENT
Infrastructure interruption:     resume same replication ID and same seed where safe
```

A new seed must never replace a failed *scientific* run (consistent with NUM-DEC-01's failed-run policy). Maximum infrastructure retry count remains `PENDING_MEASURED_RESOURCE_POLICY` — not invented here.

## 19. Resource Overrun Policy

If estimated resources exceed the future ceiling, the response is **not** to: silently reduce replications; silently drop difficult scenarios; silently remove thermodynamic-integration validation; silently lower posterior-draw requirements; use production resources; or proceed with partial favorable subsets. The response is:

```text
RESOURCE_CEILING_REQUIRES_RESEARCHER_REVIEW
```

Possible later researcher decisions (recorded as options only, none authorized now): allocate a larger nonproduction environment; optimize implementation without changing estimands; divide execution into more checkpointed waves; revise candidate scope through a versioned amendment; defer the candidate.

## 20. Relationship to NUM-DEC-01

NUM-DEC-01 fixes M2 execution at 1,000 attempted replications per cell. Resource constraints may not redefine this as 1,000 *successful* fits, nor reduce it silently. If the required scale exceeds the resource ceiling once that ceiling is eventually measured and frozen, M2 remains blocked pending researcher review — it does not get quietly scaled down.

## 21. Relationship to NUM-DEC-02

Resource estimates must include profile-likelihood optimization over the future grid (Section 10) — the pilot's point-fit-only timing (Section 4, M2) is not a substitute.

## 22. Relationship to NUM-DEC-03

Resource estimates must include parametric-bootstrap null calibration and independent FPR evaluation for M2's exact-null design — entirely absent from the pilot measurements.

## 23. Relationship to NUM-DEC-04

Resource estimates for M3 must include the calibration set and the independent evaluation set mandated by the tau-calibration procedure — both entail additional posterior/bridge/TI runs beyond the single MCMC chain the pilot measured.

## 24. Relationship to NUM-DEC-05

Resource estimates for M3 must include all three prior-odds sensitivity scenarios (null-favoring, equal, excitation-favoring) from NUM-DEC-05 — the pilot ran no prior-sensitivity scenarios at all.

## 25. Relationship to NUM-DEC-06

Resource estimates for M3 must include separate M0/M1 posterior fitting, bridge-sampling repetitions (minimum 3 independent estimates per model per NUM-DEC-06), bridge-stability checks, and thermodynamic integration on the prespecified validation subset — none of which exist in the current M3 implementation (confirmed by NUM-DEC-06's compatibility audit) or in the pilot's measured cost.

## 26. Relationship to NUM-DEC-07

ROPE (NUM-DEC-07) is deferred and is explicitly not required for the first amended tournament (per NUM-DEC-07 Section 8). No resource budget is allocated for ROPE calibration in this envelope. Conditional magnitude summaries under M1 remain required, but that reporting requirement carries negligible incremental resource cost relative to the model-fitting components above and is not separately budgeted here.

## 27. Required Future Tests

Record but do not execute:

```text
M3B-RES-001: Execution environment is nonproduction.
M3B-RES-002: Hardware and software versions are recorded.
M3B-RES-003: Pilot runtime evidence provenance is classified.
M3B-RES-004: Cell counts reconcile with the versioned protocol.
M3B-RES-005: M2 estimate includes profile-likelihood cost.
M3B-RES-006: M2 estimate includes bootstrap-calibration cost.
M3B-RES-007: M2 estimate includes independent evaluation cost.
M3B-RES-008: M3 estimate includes separate M0 and M1 fitting.
M3B-RES-009: M3 estimate includes bridge replication.
M3B-RES-010: M3 estimate includes TI validation subset.
M3B-RES-011: M3 estimate includes prior-sensitivity scenarios.
M3B-RES-012: M3 estimate includes calibration and evaluation sets.
M3B-RES-013: Memory estimate reflects worker concurrency.
M3B-RES-014: Disk estimate includes all raw and checkpoint outputs.
M3B-RES-015: Minimum free disk is checked before execution.
M3B-RES-016: Worker count respects measured memory.
M3B-RES-017: Runtime safety factor has explicit provenance.
M3B-RES-018: No arbitrary ceiling replaces missing measurements.
M3B-RES-019: No production host is used.
M3B-RES-020: Replication counts are not silently reduced.
M3B-RES-021: Failed scientific runs are not replaced.
M3B-RES-022: Infrastructure resume uses the same seed and ID.
M3B-RES-023: Duplicate seeds and IDs are rejected.
M3B-RES-024: Checkpoint resume matches uninterrupted execution.
M3B-RES-025: Resource overrun triggers researcher review.
M3B-RES-026: Stop conditions preserve completed outputs.
M3B-RES-027: Raw outputs reconcile with resource summaries.
M3B-RES-028: No historical data enter resource profiling.
M3B-RES-029: ROPE calibration cost is excluded from the first tournament.
M3B-RES-030: Resource envelope is frozen before full execution authorization.
```

Total: **30** future tests (`M3B-RES-001`–`030`), 30 unique IDs, no gaps, no duplicates.

## 28. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```

No M0, M2, or M3 source file is modified or created by this adjudication.

## 29. Profiling-Execution Nonauthorization

```text
PROFILING EXECUTION: NOT_AUTHORIZED IN THIS TURN
```

Any future small synthetic-profiling benchmark (Section 6) requires a **separate** researcher authorization in a future turn. No profiling benchmark, however small, was run to produce this document — Section 4's evidence is entirely pre-existing.

## 30. Tournament Nonauthorization

```text
TOURNAMENT EXECUTION: NOT_AUTHORIZED
```

No wave in Section 15 is authorized, including R0 (environment validation).

## 31. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```

No historical data file is read, written, or referenced by this adjudication.

## 32. Decision Summary

```text
NUM-DEC-08:                    APPROVED_WITH_LIMITATIONS
Selected option:                EVIDENCE_DERIVED_STAGED_RESOURCE_ENVELOPE
Execution environment:          DEDICATED_NONPRODUCTION_RESEARCH_ENVIRONMENT (production PROHIBITED)
Budget basis:                   MEASURED_PILOT_COST_PLUS_VALIDATED_COMPONENT_OVERHEAD
Pilot evidence used:            M0 15 cells x 1,000 attempted (4,833.2 s serial); M2 4 cells x 150 attempted
                                 (7,625.6 s serial, point-fit cost only); M3 4 cells x 200 attempted
                                 (6,160.4 s serial, single-MCMC cost only) -- all DERIVED_FROM_RUN_MANIFEST,
                                 no per-replication distribution, no CPU/memory measurement, serial (W=1)
Missing cost components:        M2 profile-likelihood grid, bootstrap calibration, independent evaluation
                                 (NUM-DEC-02/03); M3 separate M0 posterior, bridge sampling, bridge
                                 stability, TI validation subset, prior-sensitivity scenarios, calibration/
                                 evaluation sets (NUM-DEC-04/05/06) -- none measured, none estimated here
Numeric ceiling status:          15 operational-envelope dimensions (Section 14) all PENDING_MEASUREMENT;
                                 no arbitrary round-number ceiling (8 hours / 16 CPU / 32 GB / 100 GB, or
                                 any other unmeasured figure) is adopted anywhere in this document
Staged execution:                REQUIRED (10 waves R0-R9, R8 stops for researcher review before R9)
Resource freeze gate:            REQUIRED before full execution (MODEL_3B_RESOURCE_ENVELOPE_MEASURED_AND_FROZEN)
Stop conditions:                 16, all recorded, none invented beyond the researcher's own specification
Retry policy:                    no automatic replacement of failed scientific runs; infrastructure resume
                                 reuses the same seed/ID; max retry count PENDING_MEASURED_RESOURCE_POLICY
Relationship to NUM-DEC-01..07:  all preserved and cross-referenced (Sections 20-26); none revised
Required future tests:           30 (M3B-RES-001..030)
Implementation authorized:       NO
Profiling execution authorized:  NO (this turn)
Tournament execution authorized: NO
Historical fit authorized:       NO
Final numerical-ledger distribution: 7 APPROVED_WITH_LIMITATIONS (NUM-DEC-01, 02, 03, 04, 05, 06, 08)
                                 + 1 DEFERRED (NUM-DEC-07) + 0 PENDING_RESEARCHER_DECISION
```

```text
MODEL_3B_NUM_DEC_08_RESOURCE_CEILING_ADJUDICATED
```
