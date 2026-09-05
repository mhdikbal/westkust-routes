# Hawkes Baseline V2 — Premodeling Gate Report

**Instruction:** `docs/CLAUDE_HAWKES_BASELINE_V2_GATE_CHECKED_MASTER.md` (1092 lines, read in full).
**Workstream:** `EXPLORATORY_HAWKES_BASELINE_V2`. No SLR-DEC-06/07/08 work is included — that workstream is already completed, frozen, pushed, and synced.
**Branch executed:** Branch B (non-fitting audit only). **No model was fit, no simulation was run, no synthetic events were generated, no false-Hawkes experiment was run.**

---

## 1. Current-baseline discovery

```text
H_local  = aeccec03a9503f63230835e0a452061bb3017793
H_origin = aeccec03a9503f63230835e0a452061bb3017793
```
Local and origin reconcile. Server (`westkust-prod`) HEAD will be re-confirmed live at push/sync time, not assumed.

## 2. DEP-06 verbatim status

```text
prohibited_overlap: No Hawkes fitting, no synthetic recovery, no Phase D rerun authorized
                     before Phase G7 gates (H-01..H-08) pass
requires_future_review: YES
```
Source: `docs/thesis/pilot_annotation/painan_indrapura_strategic_history_lab/planning/G0_WORKSTREAM_DEPENDENCY_AND_COMPATIBILITY_MAP.csv`, row DEP-06. Read verbatim twice this program, byte-identical both times.

## 3. H-01 through H-08 gate table

See `HAWKES_BASELINE_V2_G7_GATE_MATRIX.csv` for the full 8-row, 12-column table. Summary:

| Gate | Result |
|---|---|
| H-01 Event ontology frozen | NOT_EVALUABLE |
| H-02 Source-observation model specified | NOT_EVALUABLE |
| H-03 Actor/episode linkage audited | NOT_EVALUABLE |
| H-04 Timestamp interval treatment specified | NOT_EVALUABLE |
| H-05 Simulation recovery passed | **FAIL** |
| H-06 Leave-source-out stability passed | NOT_EVALUABLE |
| H-07 Null-model comparisons passed | NOT_EVALUABLE |
| H-08 Historical inference gate separately authorized | **FAIL** |

```text
G_G7 = 0
```

## 4. Phase D non-rerun verification

```text
R_PhaseD = 0  (permanent)
```
Checksums re-verified byte-identical to the prior-session baseline:
- `MODEL_3B_FINAL_EPISTEMIC_STATUS.md` = `f874580223e8e0b1c86126d3a68f19f56bed8b0aad8c876f4b8372cb62ecdc34`
- `MODEL_3B_CD_V1_POSTMORTEM.md` = `1a4a83dd726f555066649a4b2c83463489737727820949fb19de2a7fcfc5a6af`
- `MODEL_3B_POST_PHASE_D_EPISTEMOLOGICAL_NOTE.md` = `355b6173bf61db7cefa1fdaaaf797136aed7b1353d83e0cd4f92f0f72a2abf66`

`docs/thesis/colab/model3_hawkes_kaskade_event.py` was run this turn **unmodified** (git diff clean before and after) solely to reproduce the already-published pooled fit — a verification of prior, non-Phase-D work, not a Phase D rerun and not new modeling. See §9 below and `HAWKES_BASELINE_V2_REPRODUCIBILITY_MANIFEST.csv`.

## 5. Explicit V2 modeling-authorization verification

```text
A_V2 = 0  (FAIL)
```
Source: `docs/thesis/pilot_annotation/RESEARCH_RESTART_OPTIONS.md`, "Option 3 — Mathematical-method restart":
> "Researcher authorization required: Yes for V2 explicitly (already stated as `NOT_AUTHORIZED`, `PLANNED_ONLY` at baseline, unchanged)"

No V2 go-decision memo exists anywhere in the repository, checked independently of the Hawkes instruction file itself to avoid circularity.

## 6. 141-event provenance gate

```text
N_unique          = 141/141   PASS
N_unresolved_dup  = 6/141     FAIL  (deduplication_review_required=true, unresolved)
N_provenance_complete (non-ambiguous, non-partial) = 95/141
N_provenance_ambiguous = 32/141
N_researcher_review_required = 81/141
```
Independently reconciled this turn via `csv.DictReader` against both `data/export/all_event_years.csv` (141 rows) and `docs/thesis/colab/MODEL_3B_EVENT_SOURCE_PROVENANCE_WORKING.csv` (141 rows, 37 columns) — both denominators agree exactly at 141. Per the strict gate definition (`P_141 = 1[N_unique=141 ∧ N_provenance_complete=141 ∧ N_unresolved_dup=0]`), **P_141 = 0 (FAIL)** because 6 unresolved duplicate flags remain open — reported honestly as a fraction (135/141 dedup-resolved), not silently forced to pass or to a different denominator.

## 7. Formula-to-SLR source gate

Full 14-row classification in `HAWKES_BASELINE_V2_FORMULA_SOURCE_LEDGER.csv`. Key finding: the 10 SLR-admissible items in `SLR_DEC_06_METHODOLOGICAL_EVIDENCE_LEDGER.csv` are **all SLR-search-methodology sources — none is a point-process-methodology source.** No formula in this program can reach the top category `DIRECTLY_SUPPORTED_BY_ADMISSIBLE_SLR_SOURCE`; the ceiling is `STANDARD_IDENTITY_REQUIRING_PRIMARY_REFERENCE` or `SUPPORTED_WITH_LIMITATIONS`, using the 4 external §28 references instead. 10/14 formulas individually satisfy `A_r^formula`; 4 fail solely on the `P_r` (exact section-location) sub-condition because their supporting external references (Kwan et al. 2024 full text, Potiron et al., SAA teaching case) could not be extracted from PDF this session (identity/abstract-level confirmation only).

```text
F_SLR = 0  (strict product; 10/14 formulas individually pass)
```

## 8. Observation/exposure feasibility

Three existing, already-built archival document-density series were found and assessed (not fit): `CD_ANNUAL_DOCUMENT_DENSITY_WORKING.csv` (185 years, 1600-1784, 172 years with positive counts — full-range coverage), `GM_ANNUAL_DOCUMENT_DENSITY_WORKING.csv` (corpus starts 1660, 64/185 years positive), `DAGHREGISTER_ANNUAL_DOCUMENT_DENSITY_WORKING.csv` (canonical range 1661-1681 only, 14/185 years positive). Full detail in `HAWKES_BASELINE_V2_OBSERVATION_EXPOSURE_LEDGER.csv`.

```text
O_obs = 1 (PASS) — a defensible exposure series (CD) exists with explicit provenance and coverage-status caveats
```

## 9. Event-type and parent-episode feasibility

80/141 events have `parent_episode_id` populated across 24 distinct episodes (largest: `EP-1693-SAS-EXPEDITION-AIRBANGIS-NIAS`, 11 events; most have 1-3). Event types: `perjanjian`=55, `konflik`=40, `administratif`=31, `diplomasi`=11, `suksesi`=4. Source concentration: CD carries 71/141 events (HHI=0.30, moderate concentration); 57/141 events' very existence in the record depends primarily on CD alone (`CD_dependency_event_existence=primary`).

```text
E_epi = 1 (PASS, with limitations) — feasibility is established, but M6 stratified/multivariate designs
        are NOT_FEASIBLE given strata sparsity (smallest event-type class n=4, most episodes n<5)
```

## 10. Mandatory branch decision

```text
G_V2_model = G_G7 × A_V2 × D_distinct × P_141 × F_SLR × O_obs × E_epi × I_guard
           = 0 × 0 × NOT_EVALUABLE × 0 × 0 × 1 × 1 × 1
           = 0
```

**Branch B confirmed. No fitting, simulation, synthetic-event generation, or false-Hawkes experiment was run.** The Sections 9-15 non-fitting audits (this report, plus the accompanying CSVs) were executed in full as required deliverables of Branch B.

## Current baseline formula audit (§14, informational — not a new fit)

The already-published pooled exponential Hawkes fit was reproduced this turn, unmodified: `mu=0.2573, alpha=0.4207, beta=0.6215, branching ratio eta=0.6769, LR=75.668, p<0.000001` — matches the production JSON exactly (see reproducibility manifest). A genuine methodological defect is flagged, independent of any new modeling: the reported LR-test p-value tests `eta=0`, a **parameter-space boundary** (`alpha`'s lower bound in the optimizer is effectively 0), so the standard `chi2(df=2)` reference distribution used by the existing script is very likely invalid at a boundary null (a mixture-chi-square correction, e.g. Self & Liang-type, would be the standard fix). This defect exists in the currently-displayed public result and is disclosed here as a citable finding, not manufactured to justify new modeling.

Prohibited interpretations (per instruction §14, restated): this eta value must never be read as resistance contagion, historical causal transmission, defection diffusion, or the true endogenous share of historical events. It is, at most, a `MODEL_CONDITIONAL_RESULT` about the observed coded-event process `N(t)`, not the latent historical process `H(t)`.

## Minimum sufficient changes to authorize V2 modeling in a later operation

See `HAWKES_BASELINE_V2_BLOCKER_MATRIX.csv` for the full corrective-action table. In priority order:

1. **A_V2**: researcher writes the go/no-go memo described in `RESEARCH_RESTART_OPTIONS.md` Option 3.
2. **H-08**: a separate, explicit historical-inference authorization decision (independent of A_V2).
3. **H-05**: a new, non-Phase-D simulation-recovery design, built and run to pass the ≥0.80 gate.
4. **H-01/H-02/H-03/H-04/H-06/H-07**: each needs its own dedicated artifact (frozen ontology sign-off, specified O(t) model, completed linkage audit closing the 6 open dedup flags and 32 ambiguous-provenance rows, an interval-treatment spec independent of Phase D's `jitter_ties`, a leave-source-out stability run, and an 8-design false-Hawkes battery).
5. **F_SLR**: obtain readable full text for Kwan et al. 2024, Potiron et al., and the SAA teaching case, or restrict use of the 4 affected formulas to standard textbook citations instead.
6. **P_141**: resolve the 6 unresolved deduplication flags and adjudicate the 32 `PROVENANCE_AMBIGUOUS` rows.

None of these six items is this turn's work.

## Final status

```text
HAWKES_V2_PREMODELING_AUDIT_COMPLETE_MODELING_BLOCKED_BY_G7_GATES
```
