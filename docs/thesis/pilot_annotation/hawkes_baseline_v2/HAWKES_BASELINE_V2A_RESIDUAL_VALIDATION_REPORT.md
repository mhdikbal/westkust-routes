# HAWKES BASELINE V2-A — RESIDUAL VALIDATION REPORT

Consolidates R1 (residual independence) and R2 (bootstrap calibration) for
the `EXPLORATORY_HAWKES_BASELINE_V2` workstream. Entry status was
`V2A_PARTIALLY_COMPLETE_RESIDUAL_VALIDATION_PENDING`. Does not repeat the
D1–D10 recovery study, the 2,780-replication full study, the V2-A
completion audit, D10 defect reconciliation, deterministic seed
remediation, D2/D3 audits, provenance remediation, or Phase D. Uses the
existing verified post-fix V2-A outputs as authoritative inputs.

## R1 — Residual Independence

Frozen lags `L={1,2,5,10}`, Ljung–Box `Q(m)=n(n+2)Σ(ρ̂_k²/(n-k))`, formula
verified byte-identical to `statsmodels.stats.diagnostic.acorr_ljungbox` on
an independent test series before use. Computed on `z_i` and `v_i` from the
already-fitted parameters of every active post-fix recovery-family row
(no re-fitting; residuals regenerated deterministically via the fixed
seed map, never pooled across replications).

| design/arm | lag m | N_tests | N_rejected | rate | min p | median p | max p | n_unique |
|---|---|---|---|---|---|---|---|---|
| D7 | 1 | 278 | 16 | 0.0576 | 0.0009 | 0.5289 | 0.9968 | 278 |
| D7 | 2 | 278 | 17 | 0.0612 | 0.0004 | 0.5312 | 0.9949 | 278 |
| D7 | 5 | 278 | 15 | 0.0540 | 0.0011 | 0.5144 | 0.9955 | 278 |
| D7 | 10 | 278 | 12 | 0.0432 | 0.0002 | 0.5219 | 0.9976 | 278 |
| D8 | 1 | 278 | 12 | 0.0432 | 0.0069 | 0.5569 | 0.9987 | 278 |
| D8 | 2 | 278 | 6 | 0.0216 | 0.0029 | 0.5443 | 0.9981 | 278 |
| D8 | 5 | 278 | 14 | 0.0504 | 0.0004 | 0.5187 | 0.9949 | 278 |
| D8 | 10 | 278 | 16 | 0.0576 | 0.0013 | 0.5085 | 0.9968 | 278 |
| D9-correct | 1 | 278 | 9 | 0.0324 | 0.0049 | 0.4590 | 0.9997 | 278 |
| D9-correct | 2 | 278 | 16 | 0.0576 | 0.0084 | 0.4909 | 0.9875 | 278 |
| D9-correct | 5 | 278 | 14 | 0.0504 | 0.0017 | 0.5192 | 0.9991 | 278 |
| D9-correct | 10 | 278 | 13 | 0.0468 | 0.0000 | 0.5108 | 0.9931 | 278 |
| D9-misspec. | 1 | 278 | 12 | 0.0432 | 0.0043 | 0.4310 | 0.9916 | 278 |
| D9-misspec. | 2 | 278 | 16 | 0.0576 | 0.0144 | 0.4775 | 0.9988 | 278 |
| D9-misspec. | 5 | 278 | 18 | 0.0647 | 0.0013 | 0.4673 | 0.9988 | 278 |
| D9-misspec. | 10 | 278 | 17 | 0.0612 | 0.0000 | 0.5225 | 0.9969 | 278 |
| D10 | 1 | 278 | 9 | 0.0324 | 0.0008 | 0.5613 | 0.9942 | 278 |
| D10 | 2 | 278 | 11 | 0.0396 | 0.0017 | 0.5494 | 0.9991 | 278 |
| D10 | 5 | 278 | 14 | 0.0504 | 0.0037 | 0.5082 | 0.9996 | 278 |
| D10 | 10 | 278 | 12 | 0.0432 | 0.0005 | 0.5398 | 0.9987 | 278 |

`N_total_replications=278`, `N_residual_vectors_constructed=278`,
`N_short_sequence_excluded=0`, `N_nonfinite_excluded=0` for every
design/lag — the recovery family's minimum `n_events` (52–53) exceeds every
frozen lag by a wide margin. Rejection rates cluster near the nominal 5%
(range 2.2%–6.5%) with medians ≈0.43–0.56, markedly better-behaved than the
marginal KS check's self-fit bias (§ prior reconciliation). **A non-rejection
here does not prove independence** — it means this diagnostic, at these
lags, did not detect serial structure, including in the known-misspecified
D9 arm.

Multiplicity policy (frozen in the prior V2-A completion audit §6, applied
unchanged, not invented here): report each lag's rejection rate separately
per design/arm; offer the Bonferroni threshold `0.05/4=0.0125` as one
interpretive aid; never collapse into one pass/fail statistic.

## R2 — Bootstrap Calibration (bounded submanifest)

Manifest: `HAWKES_BASELINE_V2A_BOOTSTRAP_CALIBRATION_MANIFEST.csv`. Scope
approved after one correction from the researcher (MCSE framing moved from
a p=0.05-anchored target to the worst-case bound
`MCSE_max=√(0.25/B)=0.02238 < 0.03`, confirming B=499 sufficiency for one
prespecified parent realization per arm — not for arm-wide calibration).

| arm | parent_rep | D_obs | N_conv/N_req | N_finite_stat | exceed | p_exceed | p_boot | MCSE_boot | status |
|---|---|---|---|---|---|---|---|---|---|
| D7 | 0 | 0.0577 | 499/499 | 499 | 331 | 0.6633 | 0.6640 | 0.0212 | R2_TERMINAL_COMPLETE |
| D8 | 0 | 0.0663 | 499/499 | 499 | 111 | 0.2224 | 0.2240 | 0.0186 | R2_TERMINAL_COMPLETE |
| D9-correct | 0 | 0.0467 | 499/499 | 499 | 488 | 0.9780 | 0.9780 | 0.0066 | R2_TERMINAL_COMPLETE |
| D9-misspec. | 0 | 0.0705 | 499/499 | 499 | 339 | 0.6794 | 0.6800 | 0.0209 | R2_TERMINAL_COMPLETE |
| D10 | 0 | 0.0688 | 499/499 | 499 | 241 | 0.4830 | 0.4840 | 0.0224 | R2_TERMINAL_COMPLETE |

`F_sim=F_refit=F_stat=0` for every arm; total 2,495/2,495 requested
bootstrap rows terminal. `p_boot` uses the `(1+exceed)/(B+1)` correction;
`p_exceed` is the raw exceedance proportion `/499` — the two are reported
separately, never conflated.

**Interpretation boundary (frozen, not renegotiated by these results):**
`p_boot(a, parent_rep=0)` estimates a bootstrap tail probability
*conditional on one prespecified fitted parent dataset per arm*. It does
not estimate arm-wide calibration across all 278 replications. Prohibited
statements: "D7/D8/D9/D10 residual calibration is proven"; "V2-A marginal
calibration is globally established."

**D9-misspecified, reported separately per the frozen requirement:**

```
MODEL_RELATIVE_BOOTSTRAP_RESULT: p_boot = 0.680
TRUTH_RELATIVE_MISSPECIFICATION_STATUS: KNOWN_MISSPECIFIED_BY_DESIGN
```

Substantive negative finding: the selected marginal residual statistic,
even after model-relative parametric-bootstrap calibration for one
prespecified parent realization, did not detect the known D9 baseline
misspecification. This is not model validation.

## Targeted cross-process reproducibility gate

Designated sentinel seed `999999999`, designated arm D8/primary (not
counted toward B=499). Two genuinely separate OS processes compared:

| field | in-process | subprocess | match |
|---|---|---|---|
| n_events | 156 | 156 | ✓ |
| event array hash | c8d5f97f... | c8d5f97f... | ✓ |
| mu_hat | 0.30298257823818925 | (identical) | abs_diff=0.0 ≤ 1e-9 |
| alpha_hat | 0.3444242782065656 | (identical) | abs_diff=0.0 ≤ 1e-9 |
| beta_hat | 0.534534009970965 | (identical) | abs_diff=0.0 ≤ 1e-9 |
| eta_hat | 0.6443449280716005 | (identical) | abs_diff=0.0 ≤ 1e-9 |
| residual-vector hash | 19746f30... | 19746f30... | ✓ |
| D-statistic | 0.035019305964440084 | (identical) | abs_diff=0.0 ≤ 1e-9 |
| output hash | ff73bfcc... | ff73bfcc... | ✓ |

```
G_crossprocess = 1
```

Code hash (`v2a_validation_engine.py`=`81857728b78095013779b4d61403f621`,
`v2a_designs.py`=`40ce5d8c8b4c8ff4cf496b3e98d9fc6b`) and seed-map hash
(`1a668a7ac64422130a943ff25185f4cd`) independently re-verified equal to the
values the 2,495-row R2 run actually used.

## Accounting preserved

```
C_R1 = 1
C_R2 = 1
C_provenance = 1
H05_REASON_2 = RESIDUAL_VALIDATION_COMPLETED
H05_REASON_1 = AUTHORITATIVE_RECOVERY_ACCURACY_CRITERION_NOT_OPERATIONALIZED
H05_REASON_3 = D2_PRESPECIFICATION_PROVENANCE_NOT_RECOVERED
H05 = H05_NOT_EVALUABLE_REQUIRES_RESEARCHER_REVIEW
C_H05 = 0
G_V2A_complete = 0
G_causal = 0
G_ontology = 0
historical_corpus_fit_count = 0
V2B_execution_count = 0
Phase_D_rerun_count = 0
```

Full semantic decomposition and decision:
`HAWKES_BASELINE_V2A_H05_SEMANTIC_DECOMPOSITION.csv`,
`HAWKES_BASELINE_V2A_H05_OPERATIONALIZATION_DECISION.md`. Ontology/causal
boundary: `HAWKES_BASELINE_V2A_ONTOLOGY_CAUSAL_BOUNDARY.md`. Final gate:
`HAWKES_BASELINE_V2A_FINAL_COMPLETION_GATE.csv`.

## Final status

```
HAWKES_V2A_RESIDUAL_VALIDATION_COMPLETE_H05_NOT_EVALUABLE
```

Not `HAWKES_V2A_COMPLETE_H05_PASS_V2B_REVIEW_READY` or
`_H05_FAIL_V2B_BLOCKED` — H-05 was not mechanically evaluated. Not
`HAWKES_V2A_REQUIRES_TARGETED_REPAIR` — no unrepaired defect exists; R1 and
R2 both reached clean terminal states with zero failures. V2-B is not
authorized by this status regardless of any future H-05 resolution — a
separate authorization decision remains mandatory.
