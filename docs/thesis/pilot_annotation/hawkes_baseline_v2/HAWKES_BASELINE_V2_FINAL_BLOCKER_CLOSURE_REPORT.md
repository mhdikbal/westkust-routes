# Hawkes Baseline V2 — Final Blocker Closure Report

**Baseline:** `435684c45f37582141df55477ecd3869056aa7a9`
**Entry state:** `HAWKES_V2_BLOCKER_REMEDIATION_COMMITTED_PUSHED_AND_SERVER_SYNCED_MODELING_REMAINS_BLOCKED`
**Governing instructions applied:** `docs/CLAUDE_HAWKES_V2_FINAL_BLOCKER_CLOSURE_AND_AUTHORIZATION.md` (sha256 `b1fae3f354404e2b2cc2ebdbdc2f10ee723d769ff655d4b375449e275e1a1999`) and `docs/CLAUDE_HAWKES_V2_CHECKPOINT5_DEADLOCK_RESOLUTION.md` (sha256 `e6688c45a9ca9af68a6deb88ba90d75bdbb8d21adc3d012a13a4223224f835dd`)
**Phase D rerun:** zero (permanently prohibited, unaffected)
**Fitting / simulation / synthetic events / false-Hawkes battery:** zero executions

## 1. Entry blockers

```text
G_G7=0
G_dedup=0, two unresolved cases (DEDUP-05, DEDUP-06)
P_141=0
F_SLR=0, one active formula-source gap (F-08)
H-05=FAIL
H-08=FAIL
A_V2=0
G_V2_model=0
```

## 2. Dedup closure (checkpoint 1)

Both remaining cases were resolved this operation via direct full-text extraction of the existing repository PDFs `docs/cd/CD6.pdf` and `docs/cd/CD3.pdf` (no locator invented; sources already present in the repository):

- **DEDUP-05** (Koto Tangah 1755): anchored to CD6 document **CMLXXVII** ("SUMATRA'S WESTKUST," 13 October 1755; CD6 pp.64–65; footnote locator Contractenboek XVII no. 25, Arsip Negara Djakarta). Outcome: `SAME_EVENT_MULTIPLE_REPORTS_KEEP_ONE_EVENT_LINK_REPORTS`. The secondary monograph (buku-padang-1718, p.238) is retained as a linked corroborating report.
- **DEDUP-06** (Bayang GM vs. "Corpus III, nr. D"): anchored to CD3 document **D** ("SUMATRA'S WESTKUST," 22 December 1687; CD3 pp.442–443), which matches the RGP editorial citation exactly. Outcome: `SAME_EVENT_MULTIPLE_REPORTS_KEEP_ONE_EVENT_LINK_REPORTS`. The GM source (RGP Deel 5, 05/p0162.xml) is retained as a linked report. A naming discrepancy ("Radja Itam" appearing in the GM account but attributable in CD3 to the adjacent, separate same-day Troussan document) is preserved as an explicit, unresolved source-level attribution discrepancy — not silently corrected, and not used to spin off a separate event.

Result: `D_u^primary = 0`, `G_dedup^primary = 1`. Dedup-related headcount change = 0. Neither the authoritative working CSV (`MODEL_3B_EVENT_SOURCE_PROVENANCE_WORKING.csv`) nor either source PDF was modified — this is an analysis-set patch proposal only (`HAWKES_BASELINE_V2_TWO_CASE_DEDUP_CLOSURE.csv`).

## 3. Primary analysis set (checkpoint 2)

Every singly-registered set (AS0, AS1, AS2, AS3, AS4, AS5) fails `P_s` — each satisfies at most one of provenance-sufficiency or date-semantic sufficiency, never both. AS6 remains `NOT_EVALUABLE` (no qualifying classification column exists).

Selected: **`PRIMARY_INTERSECTION_OF_REGISTERED_SETS` = AS1_PROVENANCE_CLEARED ∩ AS3_INTERVAL_ELIGIBLE**, mechanically derived from the `provenance_status` and `event_date_precision` columns.

```text
n_primary = 86
D_primary = 1, R_primary = 1, T_primary = 1, E_primary = 1, P_primary = 1
141 total = 86 included + 55 excluded
55 = 33 provenance-only + 9 date-only + 13 both
```

Estimand: `eta_primary_86 = ∫₀^∞ g(u) du` over the 86 provenance-cleared, interval-eligible observed coded events, under a future authorized model specification. This estimand does **not** generalize to the full 141-event corpus, does not represent all historical events, and interval-eligible is explicitly not exact-date — uncertain event dates remain bounded by `[L_i, U_i]`, with no midpoint/January-1/document-date point-substitution introduced.

Registered alongside (mandatory, not discarded):
- `AS1 ∩ AS2` (n=54) — mandatory exact-event-date sensitivity set.
- `AS_EPISODE_SENS = AS_PRIMARY ∩ AS4` — future episode sensitivity set; denominator to be derived mechanically at future modeling time, **not** reused from AS4's standalone 85.
- `AS0_FULL_CORPUS` (n=141) — full-corpus descriptive sensitivity only, with provenance/date-semantic limitations stated explicitly.

`P_analysis = 1`.

## 4. Formula-source closure (checkpoint 3)

F-08 (time-rescaling theorem) disposition: **`FORMULA_SUPPORT_NOT_RESOLVED`**.

```text
I_r=1, M_r=1, P_r=0, L_r=1, D_r=1 -> A_r_formula=0
F_R=13, F_A=14, F_SLR=0
```

F-08 is **not** removed from the core V2 formula domain and **not** reclassified as project-specific/exploratory. Retrieval trail this operation: bibliographic identity, journal, volume 83, issue 401, year, and page range (9–27) verified via WebSearch; full text remains inaccessible through the currently authorized access path; an accessible secondary technical review (Simply Statistics, "Deep Dive – Y. Ogata's Residual Analysis for Point Processes") was checked explicitly and did not supply the required exact section/theorem/equation locator. A new lead — the time-rescaling result is an application of a prior theoretical result of **Papangelou** — is recorded as a lead requiring primary-source verification, not a completed provenance finding. No locator was invented.

## 5. Boundary-null final specification (checkpoint 4)

```text
CURRENT_PRODUCTION_P_VALUE = NUMERICALLY_REPRODUCED_BUT_NOT_METHODOLOGICALLY_VALIDATED  (preserved verbatim)
CORRECTED_P_VALUE = NOT_COMPUTED
```

Adopted future procedure: **`MODEL_COMPARISON_WITHOUT_ASYMPTOTIC_P_VALUE`**, reclassified as a **`FUTURE_MODEL_EVALUATION_AND_REPORTING_FRAMEWORK`** — explicitly **not** a direct hypothesis test of `H0: eta=0`. `I_q_status = NOT_APPLICABLE_NO_BOUNDARY_NULL_REFERENCE_USED` (`R_q_boundary=0` ⇒ `I_q_effective=1` because no boundary-null reference is invoked, not because beta has been shown identified under alpha=0). `A_q_framework=1` is the governing field; the legacy `A_q_test` field is retained only with this reclassification note.

Kept explicitly unvalidated/unpromoted:
- `BOUNDARY_MIXTURE_REFERENCE = BOUNDARY_MIXTURE_REFERENCE_CANDIDATE_NOT_YET_VALIDATED` (Self & Liang 1987 candidate; no chi-square mixture weight asserted).
- `PARAMETRIC_BOOTSTRAP_LR = CANDIDATE_NOT_YET_FULLY_SPECIFIED` (null simulator, nuisance-parameter handling, Monte Carlo precision, provenance, and stop conditions not yet specified).

## 6. H-05 / H-08 (checkpoint 5)

```text
H-05 raw result = FAIL
H-08 raw result = FAIL
G_G7_raw = 0
```

**H05_PREAUTHORIZATION_CIRCULARITY_CONFIRMED**: `D_distinct=1`, recovery execution count=0, recovery result=`NOT_OBSERVED`. H-05 is `FAIL` because the required passing execution does not yet exist — this is a governance-structure deadlock (`H-05 = A_recovery · R_pass`, but `A_recovery` would circularly require `H-05=1` under a naive reading), not evidence that the distinct V2 recovery design failed. Phase D's documented failure remains the only executed result and is explicitly excluded from standing in for H-05.

**H-08 scope adjudication**: verbatim source (`docs/PLAN_PAINAN_INDRAPURA_GAME_THEORY_HAWKES_COUNTERFACTUAL_LAB.md`, Sec.9.1, lines 556–561) distinguishes "Hawkes family = NOT_RULED_OUT" from "Historical inference = NOT_AUTHORIZED."
```text
H_08_technical = 1
H_08_historical = 0   (permanent stop condition, unchanged)
H08 technical carve-out = NOT_YET_AUTHORIZED
```
No authoritative document defines an explicit technical-only gate subset for G7; the raw full product (`H-01..H-08`) is therefore **retained**, not shrunk. `G_G7_raw = 0` unchanged.

## 7. Recomputed G7 and gates (checkpoints 5–6)

See `HAWKES_BASELINE_V2_G7_FINAL_GATE_MATRIX.csv` for the full H-01..H-08 recomputation (no gate changed from `FAIL`/`NOT_EVALUABLE` to `PASS` this operation).

```text
G_G7_raw = 0
D_distinct = 1
P_analysis = 1
F_SLR = 0
O_obs = 1
E_epi = 1
I_guard = 1
G_V2A_preauth = 0   (validation-only staged gate; blocked independently by F_SLR=0)
G_V2_preauth = 0
A_V2 = 0
G_V2_model = 0
```

## 8. Final recommendation

```text
DEFER_PENDING_F08_PROVENANCE_AND_AUTHORIZE_SEPARATE_V2_VALIDATION_GATE_AMENDMENT_REVIEW
```

This recommends — but does not adopt — a future two-stage governance split:
- **Stage V2-A (prospective, validation-only):** execute the already-distinct recovery design and false-Hawkes controls only; no historical-corpus fitting beyond calibration necessity; no historical inference; no Phase D rerun. H-05 becomes an *output* gate of V2-A, not a precondition for authorizing it.
- **Stage V2-B (prospective, exploratory historical-corpus fitting):** possible only after V2-A's H-05 actually passes, with `F_SLR`, `P_analysis`, and other gates still holding; historical inference remains prohibited throughout.

No V2-A or V2-B authorization artifact exists. `Phase D` remains permanently closed.

## 9. Zero-execution counts

```text
Phase D reruns = 0
Hawkes/Poisson fits = 0
Simulation-recovery executions = 0
Synthetic-event generations = 0
False-Hawkes battery executions = 0
Corrected p-values computed = 0
Production Hawkes code/data/visualization files modified = 0
```

## 10. Protected artifacts (unmodified, checksums verified this operation)

```text
docs/thesis/colab/model3_hawkes_kaskade_event.py            sha256=3bd763405eb43d8a1cce63ae3b7a3a23f38add485f5a01b0216413f2066ee608
docs/thesis/colab/MODEL_3B_EVENT_SOURCE_PROVENANCE_WORKING.csv sha256=8a93667b88543f9eb8905b0168d62dd6450395b99de96c31ab962be1f9d59528
docs/thesis/pilot_annotation/MODEL_3B_FINAL_EPISTEMIC_STATUS.md sha256=f874580223e8e0b1c86126d3a68f19f56bed8b0aad8c876f4b8372cb62ecdc34
docs/cd/CD6.pdf   sha256=ad1441914ee52b8362dc94033866deeded030a8d2264d0f549e29c2900c09c9d (read-only)
docs/cd/CD3.pdf   sha256=716c216cc6963a66f894888bbd4c95630a0e736ab86f0f74d6807d0851311f7c (read-only)
```

## 11. Final status

```text
HAWKES_V2_FINAL_BLOCKER_CLOSURE_COMPLETE_MODELING_REMAINS_BLOCKED
```
