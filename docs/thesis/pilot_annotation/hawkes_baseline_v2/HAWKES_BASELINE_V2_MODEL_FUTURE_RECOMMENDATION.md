# HAWKES BASELINE V2 — MODEL-FUTURE RECOMMENDATION (CORRECTED)

Baseline: `f228b4a74d90234061b21c3d5969f5820955ab65`. Corrected per researcher
adjudication of Checkpoint 1
(`docs/CLAUDE_HAWKES_V2_DIALECTICAL_CHECKPOINT1_CORRECTION_AND_F3_DECISION.md`).
No new computation performed in either the original or this corrected
version.

## What was wrong in the original version

Checkpoint 1 was not accepted as originally written because two
option-comparison conclusions were logically unsupported:

1. **"F1 dominated by F2"** — asserted without a complete criterion-by-
   criterion Pareto-dominance proof. Categorical values are not
   automatically ordered across all ten criteria; dominance requires
   `for all k: x_a,k >= x_b,k` and `exists k: x_a,k > x_b,k` made explicit
   for every criterion, which the original document did not do.
2. **"F4 inadmissible because Hawkes is NOT_RULED_OUT"** — conflated an
   evidentiary status with a governance choice. `NOT_RULED_OUT` means
   evidence does not establish family-wide failure; it does not prohibit a
   researcher from retiring Hawkes from this specific corpus on cost,
   epistemic, or design grounds.

Both conclusions are withdrawn. Corrected per-option status is recorded in
`HAWKES_BASELINE_V2_MODEL_FUTURE_OPTIONS.csv` (columns
`researcher_status`, `evidentiary_status`).

## Researcher decision (Checkpoint 1)

```
F3_SUSPEND_PENDING_ONTOLOGY_AND_OBSERVATION_MODEL_REMEDIATION
STATUS = ADOPTED_BY_RESEARCHER
DECISION_TYPE = RESEARCHER_DECISION
DECISION_SCOPE = CURRENT_CORPUS_AND_CURRENT_MODELING_WORKSTREAM
FAMILY_WIDE_REJECTION = NO
RETROSPECTIVE_MODEL_INVALIDATION = NO
```

This is a governance decision that the corpus is not presently ready for
either exploratory fitting or Hawkes-derived visualization. It is **not** a
finding that the Hawkes family failed, and it does not modify any frozen
V2-A or Phase D artifact.

## Status of the four options after correction

```
F1  RETAIN_AS_EXPLORATORY_SECONDARY_MODEL           STATUS=NOT_CURRENTLY_AUTHORIZED   EVIDENTIARY_STATUS=OPEN
F2  RETAIN_AS_DESCRIPTIVE_VISUALIZATION_ONLY         STATUS=NOT_SELECTED               RISK=MAY_REIFY_CORPUS_INTENSITY_AS_HISTORICAL_INTENSITY
F3  SUSPEND_PENDING_ONTOLOGY_AND_OBSERVATION_MODEL_REMEDIATION   STATUS=ADOPTED_BY_RESEARCHER
F4  RETIRE_FROM_THIS_CORPUS                          STATUS=NOT_SELECTED               EVIDENTIARY_STATUS=OPEN_GOVERNANCE_OPTION
```

F1 and F4 are **not selected and not excluded** — both remain legitimate
open options for a future decision point, neither disqualified by the
evidence gathered in this operation. F2 was considered and not selected;
its reification risk (`N_corpus(t) != H(t)`) is recorded explicitly rather
than assumed away by the word "descriptive." F3 is the researcher's active
choice.

## Consequences of F3 (in force now)

```
A_Hawkes_historical_fit = 0
A_Hawkes_visualization  = 0
A_V2B                    = 0
A_causal_interpretation  = 0
A_ontology_promotion     = 0

G_causal = 0
G_ontology = 0
V2-B = BLOCKED
historical inference = NOT_AUTHORIZED
```

F3 remains in force until a future operation evaluates the remediation
domain `R-O1..R-O10` (defined in
`HAWKES_BASELINE_V2_CAUSAL_ONTOLOGY_BOUNDARY.md` Section 5) and the
prospective gate:

```
G_reconsider^future = 1[ Q_R-O1 = ... = Q_R-O10 = PASS  AND  G_sourcecrit = 1 ]
```

This gate is prospective only and is not evaluated in this operation.

## Final interpretive state

```
HAWKES_SUSPENDED_PENDING_ONTOLOGY_AND_OBSERVATION_MODEL_REMEDIATION
```

## What this recommendation does not do

It does not authorize V2-B, historical fitting, causal interpretation,
ontology promotion, or retirement of the Hawkes family. It does not begin
remediation work. It does not alter any frozen V2-A or Phase D result. It
does not reconsider the F3 decision — F3 is recorded as adopted, not
re-opened for debate in this document.
