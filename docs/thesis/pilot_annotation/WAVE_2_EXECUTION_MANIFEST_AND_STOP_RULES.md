# WAVE 2 Execution Manifest Design and Stop Rules (W2-P8)

> **Status: PLANNING-ONLY.** This document designs a manifest schema and lists stop conditions. It executes nothing and authorizes no future execution.

## 1. Future Execution Manifest Schema (instruction §22)

```text
manifest_version
repository_baseline           -- e.g. 979eaeb0d9b5d8dcd90faebd75a5dff5cd26d055
specification_hashes          -- sha256 of each of the 5 frozen V2 specs at time of execution
code_commit_future             -- commit hash of the implementation wave that will execute this manifest
container_digest_future
model_stage                    -- M0-gate | M2 | M3
cell_id
replication_id
master_seed
component_seed
parameter_truth                -- ground-truth (mu, n, beta) etc. for synthetic cells
attempt_status                 -- VALID | one of the 24 failure_taxonomy codes
failure_code
start_time_future
end_time_future
software_versions_future
output_hash_future
```

The manifest must support:

```text
- deterministic restart (same replication_id + same seed resumes identically)
- no silent replacement (a failed scientific run keeps its ID/seed forever; never regenerated with a new seed)
- attempted-replication accounting (R_attempted invariant, NUM-DEC-01)
- per-cell completeness check (all R_attempted,c=1000 rows present with a terminal status before a cell is EXECUTION_COMPLETE)
- artifact hashing (output_hash_future ties every row to an immutable output blob)
- separation of SMOKE / PILOT / LOCKED_PARTIAL_BATCH / FULL_PREREGISTERED_RUN stages (never merged in the same manifest table)
- provenance from requirement to output (every row traceable to a requirement_id in WAVE_2_REQUIREMENT_DEPENDENCY_MATRIX.csv)
```

This schema is a design artifact only — no manifest instance is created, no `manifest_version` is assigned, no row is populated.

## 2. Structural Compute-Planning Estimate (Package H — symbolic only, no benchmark executed)

Per instruction §18 Package H: "jangan menjalankan compute-cost benchmark. Gunakan symbolic atau structural dependency estimates saja." This section is therefore deliberately qualitative:

```text
number of cells:                 depends on §WAVE_2_SIMULATION_AND_COVERAGE_PLAN.md cell-selection process (not yet run)
R_attempted per cell:             1,000 (M2, fixed, NUM-DEC-01) -- M3's calibration/evaluation cell counts remain OPEN (OD-013)
nested-bootstrap cost driver:     each M2 attempted replication implies >1 optimizer call (point fit + profile-grid fits +
                                   bootstrap null/alternative refits) -- exact multiplier is an OPEN implementation-design
                                   parameter (Package C/D), not benchmarked here
Bayesian sampling cost driver:    each M3 attempted replication implies 2 posterior runs (M0-null, M1-excitation) +
                                   repeated bridge estimates (>=3 per NUM-DEC-06) + TI on the prespecified subset only --
                                   exact multiplier is OPEN (Package F)
storage estimate:                 qualitative only -- raw replication rows, posterior draws, profile-likelihood outputs,
                                   bridge outputs, TI outputs, checkpoints, logs, summaries, manifests (NUM-DEC-08's own
                                   9 storage classes, all still PENDING_MEASUREMENT)
checkpoint design:                per-cell, per-stage (SMOKE/PILOT/LOCKED/FULL never share a checkpoint namespace)
restart determinism:              governed by the manifest schema in §1 above
provenance manifest:              governed by the manifest schema in §1 above
```

No number in this section is a measured quantity. NUM-DEC-08's resource envelope (`M3-BLOCK-08`) remains the sole authority for eventual measured values, via its own separately-authorized profiling turn.

## 3. Stop Conditions (instruction §23 — 19 listed, checked against this Wave 2 output)

| # | Stop condition | Triggered in this Wave 2 run? |
|---|---|---|
| 1 | substantive conflict between the 5 V2 specs | NO |
| 2 | conflict with any NUM-DEC | NO |
| 3 | a formula undeterminable without changing a frozen decision | NO — all open formula elements are recorded as `OPEN_REQUIRES_ADJUDICATION`, not forced |
| 4 | need to select a final tau | NO — tau stays `PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION` |
| 5 | need to set ROPE | NO — ROPE stays `DEFERRED_BY_NUM_DEC_07` |
| 6 | need to close an M3 blocker | NO — all 8 remain `OPEN` |
| 7 | need to run a benchmark or calibration | NO — none run |
| 8 | need to fit historical data | NO — none fit |
| 9 | dependency cycle | NO — mechanically verified acyclic |
| 10 | a test that cannot be mapped to a requirement | NO — all 315 future tests remain in their existing inventories, unexecuted; no new test was invented outside the existing 121+194 |
| 11 | a symbol with double meaning affecting implementation | Partially present (`M0`, `M1`) but resolved via `PROPOSED_INTERNAL_LABEL` disambiguation, not left ambiguous |
| 12 | an acceptance criterion that can only be set arbitrarily | NO — every unset criterion is recorded `threshold_status=OPEN_REQUIRES_ADJUDICATION`, `threshold_value=NULL`, never guessed |
| 13 | exact null not representable as a nested submodel | Present as a **known, already-documented** defect (`M3-BLOCK-01`) — not a new discovery requiring this planning wave to stop; it is exactly what the blocker-closure protocol exists to track |
| 14 | requirement changing the primary estimand away from `n` | NO |
| 15 | requirement demoting bridge sampling from primary | NO |
| 16 | requirement removing TI as secondary | NO |
| 17 | unintended change to any of the 18 frozen artifacts | NO — mechanically verified 0 diff |
| 18 | change to estimation code or Wave 1 files | NO — mechanically verified 0 diff |
| 19 | unauthorized staging/commit/push/sync/deploy/restart | NO — none performed |

**No stop condition halted this planning wave.** Condition 13 deserves explicit note: it names a state (exact null not representable) that *already exists* in the current M3 sampler and is *already* tracked as `M3-BLOCK-01` from a prior turn — Wave 2 planning documenting a pre-existing, already-disclosed blocker is not the same as Wave 2 *discovering* a new specification conflict. No downstream Wave 2 decision was drafted as if `M3-BLOCK-01` were resolved.

## 4. What This Enables (and does not enable)

This manifest design and stop-rule check enable a **future, separately authorized** implementation wave to build a manifest-driven execution harness. They do **not** authorize:

- Wave 2 implementation of any manifest-writing code
- any smoke test, pilot check, locked-partial batch, or full run
- any resource measurement beyond the symbolic/structural estimate in §2
