# HAWKES BASELINE V2-A — H-05 GOVERNANCE AMENDMENT PROPOSAL

One narrow prospective proposal, per the semantic-contract and candidate-
operationalization findings (`HAWKES_BASELINE_V2A_H05_SEMANTIC_CONTRACT.csv`,
`HAWKES_BASELINE_V2A_H05_OPERATIONALIZATION_CANDIDATES.csv`). This does not
invent a result for the already-completed V2-A study.

## Why an amendment, not a mechanical evaluation

`G_H05^semantic = 0` (8 of 10 components ambiguous, absent, or only
derivable in hindsight) and `Σ A_o^oper = 0` (all 8 candidate
operationalizations inadmissible). Per the governing instruction's own
gate (`G_H05^operational = 1[G_H05^semantic=1 ∧ Σ A_o^oper=1]`), mechanical
evaluation is not permitted from either direction independently — this is
not a single missing piece, but a converging failure on two separate tests.

## Part A — Diagnostic Reporting Contract (no invented composite)

For every future validation run, report the following **separately**, by
eligible arm and by parameter — never averaged, weighted, or combined into
one scalar:

```
Bias
Relative bias (RB), only where the true parameter is nonzero
RMSE
Unconditional coverage (N_covered / B, optimizer/CI failures counted, not excluded)
Optimizer failure rate (F_opt)
Hessian/CI failure rate (F_CI)
Residual diagnostic results (marginal + independence, reported as descriptive
  diagnostics per the standing MARGINAL_KS_SAME_SAMPLE_PARAMETER_ESTIMATION_BIAS
  finding, never as a calibrated p-value)
```

This reporting contract does **not** by itself define a PASS/FAIL decision.
Reporting a table is not a gate.

## Part B — Decision Contract (structure choice)

Two governance structures were considered:

- **Structure 1** (prospective binary gate): requires independently
  prespecified tolerance/threshold values for the replication-level success
  rule and the pass threshold, fixed *before* any future run executes.
- **Structure 2** (retire the binary gate; adopt a validation-profile
  decision): defines categories and consequences structurally, without any
  numeric threshold that would need post hoc justification.

**This proposal selects Structure 2.** Reason: every numeric threshold this
operation could write down for Structure 1 (a coverage band, a relative-bias
tolerance, a replication-level pass rule) would necessarily be chosen with
the already-observed V2-A coverage table in view (67.3%–95.3% across 12
cells). No such number can be shown to derive independently of that
knowledge within this operation, so Structure 1 is not adoptable now without
reintroducing exactly the post hoc risk this operation was tasked with
eliminating. A future, separate operation — ideally one that fixes
Structure-1 tolerances *before* seeing any new run's results — remains free
to propose Structure 1 instead; this proposal does not foreclose that.

### Structure 2 — prospective validation-profile categories

| category | definition | consequence |
|---|---|---|
| `PROFILE_CONSISTENT` | For every eligible arm/parameter cell in Part A's report: `F_opt` and `F_CI` are both below a rate the researcher judges operationally negligible for that design's sample size, AND no cell shows coverage that is a large, qualitatively obvious departure from nominal (e.g., coverage far outside any plausible finite-sample band around the nominal rate) | Recovery-family evidence is reported as supportive; enables *researcher review* of V2-B readiness — not automatic authorization |
| `PROFILE_INCONSISTENT` | One or more cells show optimizer/CI failure rates or coverage departures that a researcher judges operationally material, following inspection of the Part A report | Recovery-family evidence is reported as inadequate; V2-B remains blocked pending redesign or a Structure-1 amendment with independently prespecified tolerances |
| `PROFILE_NOT_EVALUABLE` | Eligible arms/parameters cannot be enumerated in advance, or the Part A report cannot be produced for the eligible set | Same consequence as today: `NOT_EVALUABLE_REQUIRES_RESEARCHER_REVIEW` |

Note precisely what Structure 2 does and does not remove: it removes the
single invented ≥0.80 scalar comparison. It does **not** remove researcher
judgment — `PROFILE_CONSISTENT` vs. `PROFILE_INCONSISTENT` still requires a
human to look at the Part A table and decide, exactly as this operation's
own candidate audit (O1–O8) concluded no mechanical rule could do that
without either inventing a threshold or triggering a prohibited post hoc
pattern.

```
CURRENT FROZEN V2-A H-05 = NOT_EVALUABLE
PROSPECTIVE AMENDMENT = NOT APPLICABLE RETROSPECTIVELY
```

Any future validation run under either structure requires a separate
authorization; this proposal authorizes nothing by itself.

## Status of this proposal (not an adopted rule)

```
PROSPECTIVE_AMENDMENT_STATUS = PROSPECTIVE_GOVERNANCE_AMENDMENT_ARCHITECTURE_PROPOSED
AMENDMENT_ADOPTED = NO
AMENDMENT_OPERATIONAL = NO
RETROSPECTIVE_APPLICATION_TO_FROZEN_V2A = PROHIBITED
CURRENT_FROZEN_V2A_H05 = H05_NOT_EVALUABLE_REQUIRES_RESEARCHER_REVIEW
```

Structure 2's three categories (`PROFILE_CONSISTENT`, `PROFILE_INCONSISTENT`,
`PROFILE_NOT_EVALUABLE`) are an **architecture**, not a ready-to-run rule.
Before any future validation run could be evaluated under it, the following
must each receive independent, prospective specification — fixed before
that run's results are observed, by a method-and-governance decision this
proposal does not make:

```
eligible design domain
eligible estimator-arm domain
eligible parameter domain
required diagnostic components
metric-specific reference targets
failure treatment (optimizer and CI/Hessian)
componentwise decision rule (what makes one cell "consistent")
cross-arm aggregation rule
consequence of PROFILE_CONSISTENT
consequence of PROFILE_INCONSISTENT
consequence of PROFILE_NOT_EVALUABLE
```

```
PROFILE_CATEGORY_CRITERIA = PENDING_INDEPENDENT_METHOD_AND_GOVERNANCE_SPECIFICATION
```

No numeric threshold is created here, and none is derived from the
already-observed D7, D8, D9, or D10 results. This document proposes the
shape of a future decision, not a decision.

## Applicability to already-completed V2-A results

```
AMENDMENT_APPLIES_PROSPECTIVELY_ONLY
```

**Not** `AMENDMENT_MAY_BE_APPLIED_TO_FROZEN_RESULTS_BECAUSE_RULE_DERIVES_INDEPENDENTLY`.
Reasoning: this proposal was drafted with full knowledge of V2-A's already-
observed coverage table (67.3%–95.3% across 12 cells, `F_opt=F_CI=0`
everywhere). Any claim that this specific skeleton "derives independently"
of that knowledge cannot be verified — the coordinator who wrote it (this
operation) had already seen the numbers. Applying it retroactively to
declare a PASS or FAIL on the frozen V2-A dataset would carry exactly the
same post hoc risk this operation was tasked with eliminating, even though
no single scalar threshold was chosen to force a favorable outcome. The
methodologically clean path is a **fresh application to a new registered
design**, evaluated by someone (or a future operation) without concurrent
sight of this specific numeric table, or evaluated purely as a descriptive
report (as recommended above) rather than a PASS/FAIL gate at all.

```
AMENDMENT_REQUIRES_NEW_VALIDATION_RUN = FALSE (not authorized or requested
by this proposal — the coverage/RB table already computed in V2-A could, in
principle, simply be RE-READ under this descriptive framing without new
fitting; what cannot be done without new data is a binary PASS/FAIL scalar
verdict)
AMENDMENT_NOT_JUSTIFIED = FALSE (the underlying statistical concepts —
coverage and relative bias, reported without invented compositing — are
standard and defensible; what is not justified is compressing them into a
single retroactively-chosen number)
```

## What this proposal does not do

- It does not authorize V2-B.
- It does not convert H-05 to PASS or FAIL.
- It does not request a new simulation, fit, or bootstrap run.
- It is a draft for **researcher adoption or rejection** — adopting it is a
  separate governance act this operation does not perform.
