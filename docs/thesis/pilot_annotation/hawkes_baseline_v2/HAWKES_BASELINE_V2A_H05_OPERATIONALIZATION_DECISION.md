# HAWKES BASELINE V2-A — H-05 OPERATIONALIZATION DECISION

Checkpoint 4 of the residual-validation-and-H05 operation. Semantic
decomposition: `HAWKES_BASELINE_V2A_H05_SEMANTIC_DECOMPOSITION.csv`.

## Decision

```
H05_REASON_1 = AUTHORITATIVE_RECOVERY_ACCURACY_CRITERION_NOT_OPERATIONALIZED   [CONFIRMED]
H05_REASON_2 = RESIDUAL_VALIDATION_COMPLETED                                    [UPDATED, see below]
H05_REASON_3 = D2_PRESPECIFICATION_PROVENANCE_NOT_RECOVERED                     [CONFIRMED, unchanged]

H05_PROVISIONAL = H05_NOT_EVALUABLE_REQUIRES_RESEARCHER_REVIEW
C_H05 = 0
```

**H-05 is not converted to PASS or FAIL.** A mechanical evaluation was not
performed and is not authorized under this operation, because Reason 1 alone
is sufficient to block it, independent of Reason 2's resolution.

## Why Reason 1 is confirmed, not merely repeated

The one authoritative row that defines H-05
(`HAWKES_BASELINE_V2_H05_H08_SCOPE_ADJUDICATION.csv`) names its metric as
`"parameter recovery RB/RMSE/coverage"` — three distinct candidate metrics,
not one. Tracing its own cited evidentiary source
(`MODEL_3B_CD_FINAL_1000_RECOVERY_AUDIT.md`, the only recovery run that row
ever treats as decisive) confirms these three candidates are **not
interchangeable**: on the same historical Phase D run they produced three
different verdicts —

| candidate metric | target | Phase D outcome |
|---|---|---|
| 95% Wald CI coverage | band 0.925–0.975 | PASS for θ0/θ1, **FAIL** for alpha/beta |
| normalized RMSE (alpha/beta) | ≤0.20 | **FAIL** everywhere (0.31–0.73) |
| correct-model-selection rate (AIC/BIC) | ≥0.80 | PASS some cells, **FAIL** others (0.02–0.19) |

No authoritative text picks one of these three, states how eta/alpha/beta
are aggregated into one construct-level pass/fail, states the unit of
analysis (per-replication vs. per-design vs. pooled), states the
optimizer/CI-failure counting rule, or states whether all four V2-A
recovery arms (D7, D8, D9-correct, D10) must jointly clear the bar or any
one suffices. `>=0.80` is a real number attached to an underdetermined
metric — mapping it mechanically onto V2-A's coverage table (from the prior
checkpoint-5 reconciliation), its bias/RMSE table, or its R1/R2 residual
diagnostics from this operation would require inventing the missing pieces,
which this operation is explicitly prohibited from doing.

A second, independent barrier is on record in the same authoritative row:
`H05_PREAUTHORIZATION_CIRCULARITY_CONFIRMED` — the entitlement to run *any*
recovery design distinct from Phase D (which is what V2-A is) was, under a
naive reading of the same source, itself gated by H-05. This operation was
not authorized to adjudicate that governance circularity, and does not
attempt to.

## Why Reason 2 updates to RESIDUAL_VALIDATION_COMPLETED

Per this operation's checkpoint-3 results (provisionally accepted) and the
targeted cross-process reproducibility gate that followed:

```
C_R1 = 1   (R1 terminal for every authorized arm; all denominators reconcile
            — see HAWKES_BASELINE_V2A_RESIDUAL_INDEPENDENCE_RESULTS.csv:
            N_short_sequence_excluded=0, N_nonfinite_excluded=0 for every
            design/lag, FORMULA_IMPLEMENTATION_CHECK_PASSED against
            statsmodels)
C_R2 = 1   (R2 terminal for all 5 prespecified parent-arm cases; all 2,495
            requested bootstrap rows reached a terminal OK outcome; 0
            simulation/refit/nonfinite-statistic failures)
G_crossprocess = 1  (targeted check: event array, fitted mu/alpha/beta/eta,
            residual vector, D-statistic, and output hash all byte-identical
            across two genuinely separate OS processes for the designated
            sentinel seed 999999999 / D8-primary; code hash and seed-map
            hash independently re-verified equal to the values the 2,495-row
            run actually used)
C_provenance = 1  (conditional on G_crossprocess=1, confirmed above, AND all
            active result hashes tracing exclusively to the approved
            post-fix pipeline — verified in the prior completion audit's §1
            and re-confirmed here: engine_hash=81857728b78095013779b4d61403f621,
            designs_hash=40ce5d8c8b4c8ff4cf496b3e98d9fc6b,
            seed_map_hash=1a668a7ac64422130a943ff25185f4cd, identical across
            the R1 run, the R2 run, and this targeted check)
```

`H05_REASON_2 = RESIDUAL_VALIDATION_COMPLETED` reflects that R1 and R2, as
scoped and frozen for this operation, reached a clean terminal state. It
does **not** claim that residual validation proves the fitted models are
correctly specified (R1's non-rejection does not prove independence; R2's
bootstrap calibration is conditional on one prespecified parent realization
per arm, not arm-wide) — those limits are preserved verbatim in
`HAWKES_BASELINE_V2A_RESIDUAL_VALIDATION_REPORT.md`.

## Substantive negative finding (D9-misspecified)

```
MODEL_RELATIVE_BOOTSTRAP_RESULT: p_boot(D9-misspecified, parent_rep=0) = 0.680
TRUTH_RELATIVE_MISSPECIFICATION_STATUS: KNOWN_MISSPECIFIED_BY_DESIGN
```

The selected marginal residual statistic, even after model-relative
parametric-bootstrap calibration for one prespecified parent realization,
**did not detect** the known D9 baseline misspecification (constant-mu model
fit to nonstationary-baseline data). This is recorded as a substantive
limitation of the diagnostic's power against this specific misspecification
form — not as evidence that the misspecified model is adequate, and not as
evidence against the diagnostic's validity for other misspecification forms.

## What is NOT concluded

- H-05 is not PASS.
- H-05 is not FAIL.
- No metric was invented to force a mechanical evaluation.
- Residual-validation completion (Reason 2) does not by itself authorize
  H-05 evaluation, V2-A completion, or V2-B — Reasons 1 and 3 remain
  independently blocking.

```
G_causal = 0
G_ontology = 0
historical_corpus_fit_count = 0
V2B_execution_count = 0
Phase_D_rerun_count = 0
```
