# Model 3B Recovery Execution Protocol V2

> **Design and specification only. This protocol does NOT authorize execution. No simulation, estimator run, tournament, calibration, or historical-data fit occurs as a result of this document. Nothing staged, committed, pushed, or deployed.**

---

## 0. Status

```text
EXECUTION_STATUS: NOT_AUTHORIZED
```

This document specifies how a future, separately-authorized execution turn must be conducted. It does not itself execute anything.

## 1. Immutable Model and Gate Versions

The following are inputs to this protocol and must remain byte-unchanged by any future execution:

```text
Mathematical specification:  MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md
Gate specification:          MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv
Original gate specification: MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv (70 rows,
                              checksum d4d4d3f5215c2b76fffe0cd40bc59a6ffc78eded93db3188eb598aae468df22b)
Original protocol:           MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md
Amendment ledger:             MODEL_3B_AMENDMENT_DECISION_LEDGER.csv
Seven adjudication documents: MODEL_3B_AMENDMENT_01 through 07
Consistency audit:            MODEL_3B_COMPLETE_AMENDMENT_CONSISTENCY_AUDIT.md
```

A future execution must record the exact version/checksum of each input it used before beginning. Any drift from the versions above requires the execution to halt and return to researcher review, not silently proceed against a mismatched input.

## 2. Candidate Equations

Execution must implement exactly the equations in `MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md`:

```text
M0: SS7-9   (Poisson/NegBin baseline, full-Hessian covariance)
M2: SS10-14 (interval-censored Hawkes/MBPP, n=alpha/beta primary)
M3: SS15-22 (Bayesian discrete-time Hawkes, exact-null + P(M1|Y) decision rule)
```

No candidate equation may be altered, simplified, or substituted during implementation without a new versioned amendment.

## 3. Simulation Factors

The simulation generator must reproduce the full observation pipeline (Math Spec V2 §4):

```text
latent event process -> source-observation process -> annual interval censoring
-> same-year ties/counts -> parent-child episode dependence -> missing/duplicate
reporting -> candidate-specific preprocessing -> estimator -> recovery metrics
```

CD scenarios (Math Spec V2 §23) must be run separately and not conflated:

```text
CD-0: CD excluded
CD-1: CD modulates latent event intensity
CD-2: CD modulates observation/detection probability (logit(p_t)=zeta_0+zeta_1*CD_t)
```

## 4. Cell Definitions

Cell grids must match the amended parameter spaces:

```text
M0 cells:  gamma/exposure grid x phi grid (no excitation dimension)
M2 cells:  n grid x beta grid x CD scenario x observation-regime scenario
M3 cells:  n_d grid (including an EXACT n_d=0 null cell) x lag-kernel beta grid
           x CD scenario x observation-regime scenario
```

Every candidate's cell list must include at minimum: an exact-null cell (`alpha_true=0` / `n_true=0` / `n_d_true=0`, as applicable); a positive-excitation grid; a baseline-only sensitivity cell; source-observation and episode-dependence stress cells; missing/duplicate-reporting stress cells.

## 5. Seed Derivation

```text
- deterministic, recorded seed derivation, per cell and per replicate
- no silent replacement of a failed run's seed with a new one
- no exclusion of boundary solutions without a preregistered rule
- duplicate-seed detection required before any run is accepted as valid
- M3 calibration-set seeds and evaluation-set seeds must be drawn from
  disjoint, separately recorded seed manifests (Math Spec V2 SS19)
```

## 6. Replication Denominator Policy — UNRESOLVED

```text
STATUS: REPLICATION_DENOMINATOR_REQUIRES_PREIMPLEMENTATION_DECISION (NUM-DEC-01)
```

Whether "N replications per cell" means N *attempted* or N *valid/converged* is not decided by this protocol. Both `ATTEMPTED_REPLICATIONS` and `SUCCESSFULLY_COMPLETED_REPLICATIONS`/`VALID_FOR_METRIC_CALCULATION` counts must be computed and reported separately for every cell regardless of which interpretation is later adopted. Execution must not silently pick one interpretation.

## 7. Atomic Output Writes

Every replicate's raw output row must be written atomically (no partial-row writes visible to a concurrent reader). Cell-level output files must not be overwritten in place; new writes must be append-only or checksum-verified replacements of a complete file.

## 8. Checkpoint and Resume

```text
- cell-level checkpointing
- atomic output writes (SS7)
- immutable completed-cell results (a completed cell's rows are never
  edited after being marked complete)
- resume without changing seeds
- duplicate-seed detection
- duplicate-replication detection
- checksum manifest covering every raw output file
- interruption audit trail (what was interrupted, when, and what was
  in flight)
```

Checkpointing must not alter the sampling process — resuming after an interruption must reproduce exactly the same sequence of draws as an uninterrupted run.

## 9. Duplicate-Seed Detection

Before any cell's results are accepted as valid, the seed manifest for that cell must be checked for duplicates across all attempted and completed replications. A duplicate seed invalidates the affected replicate(s), which must be flagged, not silently kept or silently redrawn.

## 10. Failed-Optimization Accounting

An optimization/estimation failure is itself scientific evidence and must never be silently resimulated away. Per cell, the execution report must separately record: cell ID; model-generating parameters; CD scenario; observation regime; true `n`/`n_d`/`alpha`,`beta` as applicable; planned replications; attempted replications; completed replications; convergence failures; boundary solutions; invalid outputs; elapsed time; seed range/manifest reference; metric denominator used; MCSE for every rate/proportion metric.

## 11. No Silent Replacement

No cell may be resampled to reach a target replication count without explicit, preregistered documentation of the replacement rule (and even then, only for infrastructure-level failures — not for estimator convergence or optimization failures, which are themselves evidence per §10). Silent replacement of any replicate is prohibited absolutely.

## 12. Calibration/Evaluation Separation for M3

```text
CALIBRATION SET:  used exclusively to select tau (M3 threshold, NUM-DEC-04)
                   and, if relevant, prior model odds (NUM-DEC-05)
EVALUATION SET:   used exclusively to compute final recovery-gate results
```

The evaluation set must remain unopened (not inspected, not summarized, not used for any interim decision) until the threshold and decision rule are frozen. No historical data may be used in either set. This separation applies specifically to the M3 exact-null/decision-rule gates (`GATE-030-V2`, `GATE-031-V2-REPL-A` through `E`); it does not apply to M0 or M2's non-decision-rule gates.

## 13. Metric Denominators

Every rate or proportion metric must state its denominator explicitly in the output (attempted vs. completed vs. converged vs. valid-for-metric, as applicable per gate — see `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv` `denominator` column). Denominators must never be silently interchanged between reports of the same metric.

## 14. MCSE Reporting

Every rate/proportion gate result (FPR, FNR, coverage, invalid-estimate rate, convergence rate, boundary-solution rate, false-positive/false-negative excitation rate) must report Monte Carlo standard error alongside the point estimate:

```text
MCSE(p_hat) = sqrt( p_hat * (1 - p_hat) / R )
```

A result within approximately one MCSE of its threshold must not be classified as a confident PASS or FAIL without explicitly disclosing this proximity.

## 15. No Data-Dependent Early Stopping

```text
DEFAULT: NO DATA-DEPENDENT EARLY STOPPING
```

Execution may stop only for: infrastructure failure; invalid environment; a deterministic implementation defect; a researcher-issued stop; or a prespecified futility rule approved *before* execution begins. No futility rule is approved by this protocol. Stopping early because interim gate results look favorable or unfavorable is explicitly prohibited.

## 16. Threshold Freeze Before Final Evaluation

All M3 decision-rule parameters (`tau`, prior model odds, Bayes-factor diagnostic levels if used, `epsilon_n` if a ROPE is retained) must be selected using only the calibration set (§12) and then frozen — recorded in a versioned, immutable artifact — before the evaluation set is opened. No threshold may be adjusted after evaluation-set results are seen.

## 17. Historical-Data Prohibition

```text
HISTORICAL FIT: NOT_AUTHORIZED BY THIS PROTOCOL
```

`data/research/linimasa_events.csv` and `data/export/linimasa_events.csv` (or any other historical dataset) must not be read, written, or referenced by any code path this protocol governs. Historical-data fitting requires a separate, explicit future authorization, issued only after all eight numerical decisions (§NUM-DEC ledger) are resolved and the specification/gate/protocol trio is frozen.

## 18. Raw-Output Checksum Manifest

Every raw output file produced by a future execution must be checksummed (e.g., SHA-256) and the checksum recorded in a manifest alongside: file path; cell ID; replication range covered; generation timestamp; generating code version/commit. The manifest itself must be checksummed and treated as immutable once execution completes.

## 19. Deterministic Summary Generation

Summary/aggregate metrics (bias, RMSE, coverage, FPR/FNR, MCSE, etc.) must be computed by a deterministic, versioned summarization step that reads only from the immutable raw-output files (§18) — re-running the summarization step against the same raw outputs must reproduce identical summary results. Summary generation must never re-derive or infer missing raw rows.

## 20. Stop Conditions

A future execution must halt and return to researcher review upon any of:

```text
1. an input file (SS1) does not match its recorded version/checksum
2. a duplicate seed is detected (SS9)
3. a cell result cannot be reconciled against its raw rows (SS19)
4. a severe advisory finding occurs (numerical failure, invalid CI, severe
   calibration defect, data loss, non-identifiability, protocol violation)
   — per PROPOSAL-06's severe-finding override, regardless of whether the
   affected gate is formally advisory or mandatory
5. any of the eight numerical decisions (NUM-DEC-01 through 08) remain
   unresolved at the point execution would need them
6. resource usage exceeds the operational ceiling established under
   NUM-DEC-08
7. any attempt is made to use historical data (SS17)
8. the M3 evaluation set would need to be opened before the threshold
   freeze (SS16) is complete
```

None of these conditions are resolved or waived by this protocol. This protocol authorizes no execution of any kind.

## 21. Numerical Adjudication Integration

All eight items on `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv` are now adjudicated (7 `APPROVED_WITH_LIMITATIONS`: NUM-DEC-01, 02, 03, 04, 05, 06, 08; 1 `DEFERRED`: NUM-DEC-07; 0 `PENDING_RESEARCHER_DECISION`). Stop Condition 5 (§20) — "any of the eight numerical decisions remain unresolved at the point execution would need them" — is therefore no longer a live blocker for the *decision* layer; it remains a live blocker for every unresolved *numerical value* within those decisions (final tau, epsilon_n if reopened, every NUM-DEC-08 resource-ceiling number), since a resolved procedure is not a resolved value. See `MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md` §35 for the full per-decision resolution/pending breakdown. This section does not authorize execution — Stop Conditions 1-4 and 6-8 (§20) remain fully in force, and §17 (Historical-Data Prohibition) is unaffected.

```text
IMPLEMENTATION AUTHORIZED BY THIS INTEGRATION:   NO
TOURNAMENT EXECUTION AUTHORIZED:                 NO
CALIBRATION EXECUTION AUTHORIZED:                NO
HISTORICAL FIT AUTHORIZED:                       NO
```
