# Amendment Adjudication — Proposal 3: M2 Full-Scale Replication Requirement

> **Decision record only. No M2 execution performed. No source code or gate specification modified. No 1,000-per-cell run occurs. No protocol V2 or gate specification V2 created. Nothing staged, committed, pushed, or deployed.**

---

## 1. Scope

This document adjudicates **only** `PROPOSAL-03` — the requirement that M2 complete the preregistered full recovery scale of 1,000 replications per cell before final gate adjudication. `PROPOSAL-01` (M0) and `PROPOSAL-02` (M2 primary estimand) were adjudicated separately and are **not** touched by this document — both remain `APPROVED_WITH_LIMITATIONS`, `implementation_authorized=NO`, `rerun_authorized=NO`, `historical_fit_authorized=NO`. `PROPOSAL-04` through `PROPOSAL-07` are **not** adjudicated here.

## 2. Authoritative Evidence

```text
Diagnostic-audit commit:    4b94cd689c995765102b4ca4c63e2636334432bb
Authoritative status:       MODEL_3B_PILOT_DIAGNOSTIC_AUDIT_PUSHED_AND_SERVER_SYNCED
Tournament verdict:         NOT_AVAILABLE
Historical-data fitting:    NOT_AUTHORIZED
Proposal 1 status:          APPROVED_WITH_LIMITATIONS (implementation-free)
Proposal 2 status:          APPROVED_WITH_LIMITATIONS (implementation-free)
```

Primary evidentiary sources: `MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md` (protocol-completion note), `MODEL_3B_PILOT_GATE_CLASSIFICATION.csv` (GATE-019/020, `PROTOCOL_NOT_COMPLETED`), `run_recovery_m2.py`'s own module docstring (source-verified timing rationale for the 150/cell deviation).

## 3. Current Pilot Scale

```text
Actual M2 pilot scale:      150 replications per cell
Reason for shortfall (source-verified, run_recovery_m2.py module docstring):
                             ~5.8-18.6 s/replicate made the full 1,000/cell
                             run infeasible at pilot time (~6+ hours)
Classification:              PILOT_ONLY_PROTOCOL_DEVIATION (explicit, reported,
                              not silent)
```

## 4. Preregistered Full Scale

```text
Required future execution scale:  1,000 replications per cell
Current pilot scale:               150 replications per cell
Current evidence classification:   PILOT_ONLY_PROTOCOL_DEVIATION
```

## 5. Monte Carlo Precision

For an empirically estimated proportion `p_hat`:

```text
MCSE(p_hat) = sqrt( p_hat * (1 - p_hat) / R )
```

At `p_hat ≈ 0.95`:

```text
R = 150:    MCSE ≈ sqrt(0.95*0.05/150)  ≈ 0.0178
R = 1,000:  MCSE ≈ sqrt(0.95*0.05/1000) ≈ 0.0069
```

**Interpretation:** 150 replications per cell provide useful pilot diagnostics; 150 replications per cell do not satisfy the preregistered execution scale; gate outcomes near their thresholds remain too uncertain for final adjudication under this MCSE; the pilot cannot be promoted to a final tournament run on this basis alone.

## 6. Near-Threshold Interpretation

Preserved from the pilot, unchanged:

```text
Individual alpha/beta recovery:      unstable (confirmed unidentified, Proposal 2)
Alpha-beta objective ridge:          confirmed (Proposal 2, §4)
n = alpha/beta identifiability:      materially better than alpha/beta individually
Branching-ratio pilot bias:          approximately 0.020 to 0.054 (exact metric
                                      as implemented by the harness, GATE-019/020)
Threshold:                           <= 0.050
```

At least one observed cell result (0.054) sits close to or slightly beyond the 0.050 threshold. **`0.054` is not converted into either `FINAL_PASS` or `FINAL_FAILURE` by this document** — that determination requires the full preregistered execution scale and a Monte Carlo uncertainty review, neither of which is performed in this adjudication turn. A cell result at 0.054 must not be declared a final failure before the preregistered scale is run.

## 7. Researcher Decision

```text
PROPOSAL-03: APPROVED_WITH_LIMITATIONS

Candidate:                  M2
Required future scale:       1,000 replications per cell
Current pilot:                150 replications per cell
Current result:               PILOT_ONLY, NOT FINAL
Implementation authorized:    NO
Rerun authorized:             NO (not in this turn)
Historical fit authorized:    NO
```

## 8. Replication Denominator

The default requirement is **1,000 attempted preregistered replications per cell**, with full accounting of every outcome — not silently redefined as "1,000 valid/converged replications" unless that interpretation is explicitly derived from the frozen protocol text. Reviewing `MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md`, the protocol's own language ("1,000 replicates per cell") does not itself disambiguate attempted vs. valid-for-metric-calculation counts. Per the instruction's own required handling:

```text
REPLICATION_DENOMINATOR_REQUIRES_EXPLICIT_PREEXECUTION_DECISION
```

Both `ATTEMPTED_REPLICATIONS` and `SUCCESSFULLY_COMPLETED_REPLICATIONS`/`VALID_FOR_METRIC_CALCULATION` counts must be preserved and reported separately in any future execution — the denominator is not silently collapsed to one interpretation by this adjudication.

## 9. Failure Accounting

A successful replication, for future execution, is defined as one in which: simulation completes; estimator returns; convergence status is recorded; all required estimands are finite; all required diagnostics are computed; the output row is structurally valid. **An optimization failure is itself scientific evidence** and must not be silently resimulated away — no future run may keep resampling a cell until 1,000 favorable or converged results are obtained. The future execution report must distinguish and separately record, per cell:

```text
cell ID; model-generating parameters; CD scenario; observation regime;
true n; true beta; planned replications; attempted replications;
completed replications; convergence failures; boundary solutions;
invalid outputs; elapsed time; seed range/manifest; metric denominator;
MCSE for every rate/proportion metric
```

## 10. Seed Policy

```text
- deterministic and recorded seed derivation, per cell and per replicate
- no silent replacement of a failed run's seed with a new one
- no exclusion of boundary solutions without a preregistered rule
- duplicate-seed detection required before any future run is accepted as valid
```

## 11. Checkpoint and Resume

A future full-scale implementation must support: cell-level checkpointing; atomic output writes; immutable completed-cell results; resume without changing seeds; duplicate-seed detection; duplicate-replication detection; a checksum manifest; and an interruption audit trail. **Checkpointing must not alter the sampling process** — resuming after an interruption must reproduce exactly the same sequence of draws as an uninterrupted run (M2-SCALE-008/009 below).

## 12. Early-Stopping Policy

```text
Default: NO DATA-DEPENDENT EARLY STOPPING
```

A future run may stop only for: infrastructure failure; invalid environment; deterministic implementation defect; researcher-issued stop; or a prespecified futility rule **approved before execution**. **No futility rule is approved by Proposal 3.** Stopping early because interim gate results look favorable or unfavorable is explicitly prohibited.

## 13. Computational Feasibility

Before any future full run, a resource estimate is required, derived from the observed pilot timing (§3: ~5.8–18.6 s/replicate):

```text
estimate = (observed s/replicate) x (1,000 replications/cell) x (number of cells)
```

The estimate must report: expected CPU time; expected wall-clock time; memory; output size; checkpoint strategy; deterministic resume behavior; maximum allowed retries; failure recovery; storage cleanup. **The replication count must not be lowered solely because execution is expensive.** If full execution proves infeasible under this estimate, the correct response is to return to the researcher for review — not to silently substitute 150 or any other reduced count as if it satisfied this requirement. This document does not itself perform that resource estimate (it requires re-running or extrapolating from the actual pilot timing data, which is execution-adjacent analysis reserved for the implementation turn) — it only fixes the requirement and the prohibition on silent downgrading.

## 14. Dependency on Proposal 2

Proposal 3 applies prospectively to the amended M2 design adjudicated under `PROPOSAL-02`: primary estimand `n = alpha/beta`; secondary diagnostics `alpha`, `beta`, integrated interval excitation, predictive interval counts. **Proposal 3 does not independently authorize Proposal 2's implementation** — both proposals require a later, single, versioned implementation package; neither is self-sufficient on its own to authorize execution.

## 15. Original-Protocol Preservation

**Not modified by this document:** the original recovery-tournament design (`MODEL_3B_RECOVERY_TOURNAMENT_DESIGN.md`); the original execution protocol (`MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md`); the original 70-row gate specification (`MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv`); the raw 150-per-cell M2 pilot outputs; the original M2 source (`m2_mbpp.py`); the diagnostic audit; the Proposal 1 and Proposal 2 adjudication documents — all confirmed byte-unchanged (§ Validation below).

A future amended execution must use **new versioned files**. Suggested future identifiers (not created in this turn): `MODEL_3B_RECOVERY_TOURNAMENT_PROTOCOL_V2`, `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2`.

## 16. Required Future Tests (recorded, NOT executed this turn)

```text
M2-SCALE-001: Cell list matches the approved versioned protocol.
M2-SCALE-002: Seed mapping is deterministic and unique.
M2-SCALE-003: One thousand planned replications are accounted for per cell.
M2-SCALE-004: Attempted, completed, converged, boundary, and invalid counts
              reconcile.
M2-SCALE-005: No failed replication is silently replaced.
M2-SCALE-006: Metric denominators are explicitly recorded.
M2-SCALE-007: MCSE is reported for every rate and proportion gate.
M2-SCALE-008: Checkpoint and resume reproduce uninterrupted results.
M2-SCALE-009: Repeated execution with the same seed manifest is deterministic.
M2-SCALE-010: No historical data enter the recovery run.
M2-SCALE-011: No interim gate result changes the execution plan.
M2-SCALE-012: Raw outputs and summaries reconcile exactly.
M2-SCALE-013: All cells use the approved n-based primary estimand.
M2-SCALE-014: Original and amended gate versions remain separately traceable.
M2-SCALE-015: Execution resource usage remains within the approved
              operational ceiling.
```

## 17. Implementation Nonauthorization

```text
IMPLEMENTATION: NOT_AUTHORIZED
```
No M2 source file is modified by this document. No protocol V2 or gate specification V2 file is created.

## 18. Rerun Nonauthorization

```text
FULL RERUN: NOT_AUTHORIZED_IN_THIS_TURN
```
No 1,000-per-cell (or any scale) M2 execution is performed by this document.

## 19. Historical-Fit Nonauthorization

```text
HISTORICAL FIT: NOT_AUTHORIZED
```
`data/research/linimasa_events.csv` and `data/export/linimasa_events.csv` are not read, written, or referenced by any executed code in this adjudication turn.

## 20. Decision Summary

```text
PROPOSAL-03: APPROVED_WITH_LIMITATIONS
Required future scale:        1,000 replications per cell
Current pilot scale:          150 replications per cell
Current result:               PILOT_ONLY, NOT FINAL
Near-threshold cell (0.054):  neither PASS nor FAIL declared
Replication denominator:      REPLICATION_DENOMINATOR_REQUIRES_EXPLICIT_
                               PREEXECUTION_DECISION (both counts preserved)
Early stopping:                prohibited by default, no futility rule approved
Computational feasibility:     required before execution, downgrade-on-cost
                               prohibited
Dependency:                    Proposal 2 (primary estimand) -- joint
                               versioned implementation required
Implementation:                 NOT_AUTHORIZED
Full rerun:                     NOT_AUTHORIZED_IN_THIS_TURN
Historical fit:                 NOT_AUTHORIZED
```

## Final Status (this document)

```text
MODEL_3B_AMENDMENT_03_M2_FULL_SCALE_ADJUDICATED
```
