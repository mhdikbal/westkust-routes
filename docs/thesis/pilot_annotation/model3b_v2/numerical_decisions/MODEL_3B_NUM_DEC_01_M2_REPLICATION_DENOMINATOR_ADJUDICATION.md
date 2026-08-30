# MODEL 3B — NUM-DEC-01 Adjudication: M2 Replication Denominator

Status: `APPROVED_WITH_LIMITATIONS`
Decision scope: NUM-DEC-01 ONLY. NUM-DEC-02 through NUM-DEC-08 remain `PENDING_RESEARCHER_DECISION` and are not addressed by this document.
Implementation authorized: NO. Tournament execution authorized: NO. Historical fit authorized: NO.

## 1. Scope

This document adjudicates exactly one unresolved numerical decision from `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv`: **NUM-DEC-01, M2 replication denominator** — the interpretation of Proposal 3's "1,000 replications per cell" requirement. No other numerical decision (NUM-DEC-02..08) is adjudicated, implemented, or executed here. No M2 code is modified. No tournament runs. No historical data is fit.

## 2. Authoritative Evidence

Read in full before this adjudication:
- `MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md`
- `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv` (51 rows, V2 gate schema)
- `MODEL_3B_RECOVERY_PROTOCOL_V2.md`
- `MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv`
- `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv` (8 rows, pre-decision baseline: 8/8 `PENDING_RESEARCHER_DECISION`)
- `MODEL_3B_GATE_V1_TO_V2_RECONCILIATION.csv` (75 data rows; 70/70 original gates accounted for, 51 V2 gates all traceable — verified mechanically prior to this task, unchanged by it)
- `MODEL_3B_V2_NUMERICAL_DECISION_DIGEST.md` (contains the pre-adjudication NUM-DEC-01 digest: options, evidence available/missing, consequences)
- `MODEL_3B_AMENDMENT_02_M2_ESTIMAND_ADJUDICATION.md` (Proposal 2 — establishes n=alpha/beta as M2's primary estimand)
- `MODEL_3B_AMENDMENT_03_M2_FULL_SCALE_ADJUDICATION.md` (Proposal 3 — establishes the 1,000-replications/cell requirement this decision resolves)

## 3. Mathematical Question

Proposal 3 mandated "1,000 replications per cell" for the M2 synthetic recovery study at full scale, but did not specify whether this denominator counts (a) attempted replications, (b) replications yielding a valid/successful fit, or (c) both reported under separate accounting. The ledger's own options field named three candidates: `ATTEMPTED_REPLICATIONS_PER_CELL`, `VALID_FOR_METRIC_CALCULATION_REPLICATIONS_PER_CELL`, `BOTH_REPORTED_SEPARATELY_NO_SINGLE_DENOMINATOR_ADOPTED`. This decision selects among them and fixes the accounting rules that follow from the choice.

## 4. Available Options

| Option | Description | Risk |
|---|---|---|
| A — Attempted-replication denominator | `R_attempt = 1000` fixed per cell; valid/failed/invalid all counted against it | None of the risks below; requires richer per-replication bookkeeping |
| B — Valid/successful-fit denominator | Resimulate until 1,000 successful fits obtained | Silently discards evidence of optimizer failure; can make a poorly-behaved candidate look artificially reliable; violates failed-run-as-evidence principle |
| C — Both reported, no single denominator adopted | Defers the choice, reports both | Does not resolve which denominator gates/rates actually use; leaves ambiguity for every downstream metric computation |

## 5. Researcher Decision

**Selected: Option A — 1,000 ATTEMPTED replications per cell** (`R_attempt(c) = 1000`), not 1,000 successful replications. No resimulation is permitted merely to raise the valid-fit count toward 1,000.

Status recorded in the ledger: `APPROVED_WITH_LIMITATIONS`. Selected decision value: `1000_ATTEMPTED_REPLICATIONS_PER_CELL`.

## 6. Attempted Replication Definition

For each cell `c`:

```
R_attempt(c) = 1000
R_attempt(c) = R_valid(c) + R_failed(c) + R_invalid(c)
```

`R_attempt` is fixed at the outset of execution for a cell and is never adjusted upward or downward once execution begins. It is the total count of replication attempts planned and consumed for that cell, regardless of how many produce a usable fit.

## 7. Replication Identity

Every replication has an immutable identity:

```
replication_id = hash(protocol_version, candidate, cell_id, replication_index, seed)
```

This decision fixes the *conceptual* identity requirement only. The exact hashing implementation (algorithm, encoding, collision handling) is **not selected** in this adjudication and is deferred to implementation time, which itself remains unauthorized (§18).

## 8. Outcome Categories

Every attempted replication terminates in exactly one of the following mutually exclusive categories:

- `VALID_METRIC_BEARING`
- `OPTIMIZATION_FAILED`
- `NONCONVERGED`
- `BOUNDARY_SOLUTION`
- `NUMERICALLY_INVALID`
- `STRUCTURALLY_INVALID`
- `INTERRUPTED_BEFORE_ESTIMATION`

No replication may be left uncategorized in a completed cell.

## 9. Primary Denominators

`R_attempt` is the denominator for all execution-accounting and reliability rates:

```
ConvergenceRate = R_valid / R_attempt
FailureRate = (R_failed + R_invalid) / R_attempt
```

`R_attempt` is used for: convergence rate, optimization-failure rate, invalid-output rate, boundary-solution rate, total execution accounting, and computational failure summaries.

## 10. Metric-Specific Denominators

A metric that is only mathematically defined on valid fits (e.g. parameter bias, RMSE, interval coverage) may use `R_metric`, subject to:

```
R_metric <= R_valid <= R_attempt
```

only when the metric is mathematically defined for those particular outputs (e.g. a boundary solution may or may not contribute to `R_metric` depending on the metric and parameter domain — see §12).

For every such metric, the following must be reported together, never `R_metric` alone:
- `R_attempt`
- `R_valid`
- `R_metric`
- exclusion count
- exclusion reasons
- denominator difference (`R_attempt − R_metric`, `R_valid − R_metric`)
- whether the exclusion may bias the result

## 11. Failed-Run Policy

Failed and invalid replications constitute scientific evidence about candidate reliability. They must never be:
- silently discarded
- silently replaced
- rerun with a new seed
- excluded from convergence/failure-rate denominators
- converted to zero
- counted as PASS
- hidden from aggregate summaries

The seed assigned to a failed replication remains consumed. No replacement seed is generated merely to raise the valid-result count toward 1,000.

## 12. Boundary-Solution Policy

`BOUNDARY_SOLUTION` is reported as its own category, distinct from both valid and invalid outcomes. It is never auto-classified as invalid. Its treatment for any specific metric's `R_metric` depends on the parameter domain and the metric definition — this determination is made per-metric at implementation time (unauthorized here), not fixed globally by this decision.

## 13. Infrastructure Interruption and Resume

`INTERRUPTED_BEFORE_ESTIMATION` replications are further distinguished as `INFRASTRUCTURE_INTERRUPTION` when caused by host failure, process termination, storage failure, or invalid execution environment — as opposed to a model-estimation failure. An infrastructure-interrupted replication may be **resumed** using the identical deterministic seed and configuration; it must not be restarted with a different seed, and the resume must not create a duplicate `replication_id`.

Deterministic reconciliation per cell:

```
planned_attempts = 1000
unique_replication_ids = attempted_replications
attempted = valid + optimization_failed + nonconverged
          + numerically_invalid + structurally_invalid
          + infrastructure_interrupted_pending_resume
```

After all valid resumes are resolved, unresolved infrastructure interruptions must equal zero, or the cell remains `EXECUTION_INCOMPLETE`.

## 14. Monte Carlo Precision

```
MCSE(p_hat) = sqrt( p_hat * (1 - p_hat) / R_effective )
```

`R_effective` is the denominator actually used for the rate in question:
- `R_effective = R_attempt` for convergence and failure rates
- `R_effective = R_metric` for valid-fit parameter metrics

`R_effective` must never default to 1,000 when fewer than 1,000 outputs actually support the metric being estimated.

## 15. Final-Cell Completeness

A cell may be classified `EXECUTION_COMPLETE` only if all of the following hold:
1. Exactly 1,000 unique attempted replications are accounted for.
2. Every replication has a terminal status.
3. No duplicate seed exists.
4. No duplicate `replication_id` exists.
5. No unresolved infrastructure interruption remains.
6. All metric denominators reconcile.
7. Raw rows and summary counts match.

`EXECUTION_COMPLETE` does **not** mean the candidate passed. A cell with many optimization failures can be complete but scientifically failed.

**Gate consequence:** if too few replications yield valid metric-bearing outputs, the denominator is never resimulated upward to compensate. The affected metric/candidate is classified only via statuses that exist in the versioned V2 gate specification (e.g. `INSUFFICIENT_VALID_METRIC_OUTPUT`, `NUMERICAL_RELIABILITY_FAILURE`). This decision does not invent a new minimum-valid-output threshold. Where no such threshold currently exists in the V2 gate spec, the condition is recorded as `VALID_METRIC_MINIMUM_REQUIRES_PREIMPLEMENTATION_RULE`.

## 16. Relationship to Proposal 3

Proposal 3 (`MODEL_3B_AMENDMENT_03_M2_FULL_SCALE_ADJUDICATION.md`) required "1,000 replications per cell" without specifying the denominator's exact meaning (flagged there as `REPLICATION_DENOMINATOR_REQUIRES_EXPLICIT_PREEXECUTION_DECISION`, SS8). NUM-DEC-01 resolves that open item as: **1,000 attempted, uniquely identified, fully accounted replications per cell.** This decision does not alter the historical 150-replications/cell M2 pilot record, which remains an immutable historical fact.

## 17. Remaining Numerical Decisions

NUM-DEC-01 decides only the M2 replication denominator. It does **not** decide:
- NUM-DEC-02 — M2 uncertainty method for n
- NUM-DEC-03 — M2 exact-null implementation
- NUM-DEC-04 — M3 threshold tau
- NUM-DEC-05 — M3 prior model odds
- NUM-DEC-06 — M3 marginal-likelihood/Bayes-factor method
- NUM-DEC-07 — M3 ROPE epsilon_n
- NUM-DEC-08 — operational resource ceiling

All seven remain `PENDING_RESEARCHER_DECISION`, verified mechanically unchanged in §Validation below.

## 18. Implementation Nonauthorization

`implementation_authorized: NO`. No M2 code (`m2_mbpp.py` or any harness file) is created, modified, or executed as part of this adjudication. The replication-identity hashing scheme, outcome-classification logic, and denominator bookkeeping described above are specifications for a future authorized implementation phase, not code delivered now.

## 19. Tournament-Execution Nonauthorization

`tournament_execution_authorized: NO`. No synthetic recovery run, no simulation, and no tournament of any scale (pilot or full 1,000-replication) is executed by this adjudication.

## 20. Historical-Fit Nonauthorization

`historical_fit_authorized: NO`. No historical VOC trade data is fit, referenced numerically, or used to inform this decision. NUM-DEC-01 is a pre-registration/design decision only.

## 21. Decision Summary

| Field | Value |
|---|---|
| Decision ID | NUM-DEC-01 |
| Topic | M2 replication denominator |
| Status | APPROVED_WITH_LIMITATIONS |
| Selected value | 1000_ATTEMPTED_REPLICATIONS_PER_CELL |
| Primary denominator | R_attempt = 1000 (fixed per cell) |
| Metric denominator | R_metric ≤ R_valid ≤ R_attempt, always disclosed jointly |
| Failed-run policy | Retained as evidence; never discarded/replaced/rerun |
| Boundary-solution policy | Separate category; validity metric/domain-dependent, not auto-invalid |
| Infrastructure resume | Same seed/config; no duplicate replication_id |
| Implementation authorized | NO |
| Tournament execution authorized | NO |
| Historical fit authorized | NO |
| Remaining pending decisions | NUM-DEC-02 through NUM-DEC-08 (7/8) |

---

## Validation

Performed mechanically (python/csv) against the touched files:

- NUM-DEC-01 is the only ledger row with `current_status != PENDING_RESEARCHER_DECISION` — confirmed (1 `APPROVED_WITH_LIMITATIONS`, 7 `PENDING_RESEARCHER_DECISION`).
- Every field of rows NUM-DEC-02..08 diffed before/after: **zero mismatches**.
- Five V2 specification files (`MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md`, `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`, `MODEL_3B_RECOVERY_PROTOCOL_V2.md`, `MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv`) unchanged — the ledger CSV is the one file expected and confirmed to change.
- `MODEL_3B_GATE_V1_TO_V2_RECONCILIATION.csv` unchanged.
- Original `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` unchanged.
- No `.py` implementation file created or modified.
- No simulation executed; no historical data referenced.
- Secret scan on the two touched/created files: clean.
- `git status`: nothing staged.

**Final status: `MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATED`**
