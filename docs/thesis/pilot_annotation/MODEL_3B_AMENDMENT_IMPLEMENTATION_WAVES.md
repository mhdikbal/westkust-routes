# Model 3B — Future Implementation Wave Plan

> **Planning document only. No wave is authorized by this document. Each wave requires its own separate, explicit researcher authorization before any code is written or run.**

---

## Governing sequence (derived, smallest valid order)

```text
WAVE 1: Versioned mathematical and gate specifications
WAVE 2: M0 correction
WAVE 3: M2 correction
WAVE 4: M3 correction
WAVE 5: Advisory-gate implementation
WAVE 6: Implementation-only synthetic smoke validation
WAVE 7: Separate researcher decision on full tournament execution
```

## WAVE 1 — Versioned mathematical and gate specifications

Candidate equations; parameter spaces; estimands; exact-null definitions; applicability matrix; mandatory/advisory status; formulas; thresholds or unresolved-threshold flags; provenance; failure meanings — for all three candidates, incorporating Proposals 1-7. Output: `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv` (new file; original never overwritten). **Not created by this or any prior turn.**

## WAVE 2 — M0 correction

Full three-parameter Hessian (`theta0`, `theta1`, `log_phi`); covariance; transformations (Jacobian for `phi`); 10 targeted tests (`M0-HESS-001..010`); small fixed-seed oracle reproduction. Depends on: WAVE 1 (versioned spec must exist first, per Proposal 1's own approved future execution order).

## WAVE 3 — M2 correction

`n`-based parameterization (`alpha=n*beta`, `0<=n<1`, `beta>0`); M2-specific exact-null review (separate from M3's, per Proposal 2 §13); uncertainty method for `n` (not selected — profile likelihood / bootstrap / likelihood-based interval, per Proposal 2 §15); replication accounting (attempted/completed/converged/boundary/invalid, explicit denominator per Proposal 3 §8); 27 targeted tests (`M2-EST-001..012` + `M2-SCALE-001..015`). Depends on: WAVE 1.

## WAVE 4 — M3 correction

Explicit null/excitation models (`M0:n=0`, `M1:0<n<1`, preferred `M3-NULL-A` two-model comparison); posterior model probability `P(M1|Y)` as primary decision quantity; calibration/evaluation seed-set separation; threshold `tau` calibration (grid `0.50/0.75/0.90/0.95/0.975/0.99`, not preselected); replacement for `GATE-031` (`M3-REPL-031-A..E`); 63 targeted tests (`M3-NULL-001..020` + `M3-DEC-001..028` + `M3-G31-001..015`). Depends on: WAVE 1.

## WAVE 5 — Advisory-gate implementation

**Correction from the consistency audit (see `MODEL_3B_COMPLETE_AMENDMENT_CONSISTENCY_AUDIT.md` §9):** the applicable advisory-gate count is **17**, not the 19 recorded in Proposal 6's own adjudication — `GATE-019`/`GATE-020` (M2 branching-ratio bias) are MANDATORY tier in the frozen spec, not ADVISORY, and belong to WAVE 3's replication-accounting scope, not this wave. 21 advisory-integrity tests (`M3B-ADV-001..021`). Depends on: WAVE 2, WAVE 3, WAVE 4 (advisory gates must use each candidate's amended equations once implemented, per Proposal 6 §15).

## WAVE 6 — Implementation-only synthetic smoke validation

Tiny-scale (not pilot-scale, not full-scale) execution to confirm WAVE 1-5's code runs end-to-end without crashing, matching this session's own established `DIAGNOSTIC_ONLY` discipline. Not a scientific result. Depends on: WAVE 2-5 complete.

## WAVE 7 — Separate researcher decision on full tournament execution

Only after WAVE 1-6 are complete and reviewed does the question of a full-scale (1,000/cell M0 and M2; calibration-then-evaluation for M3) rerun become askable — and even then, it is its own separate authorization, not implied by completing WAVE 1-6. Historical-data fitting remains a further, still-separate decision beyond even a successful full rerun (per every one of the seven adjudications' own explicit `historical_fit_authorized=NO`).

---

## Authorization status

```text
No wave is authorized by this consistency audit or by any of the seven
adjudication documents it audits. Each wave requires its own explicit
future researcher authorization.
```
