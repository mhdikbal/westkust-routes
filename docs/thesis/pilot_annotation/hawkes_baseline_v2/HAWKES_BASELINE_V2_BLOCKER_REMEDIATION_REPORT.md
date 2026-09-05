# Hawkes Baseline V2 — Blocker Remediation Report

**Instruction:** `docs/CLAUDE_HAWKES_V2_BLOCKER_REMEDIATION_AND_MODELING_AUTHORIZATION.md` (937 lines, read in full).
**Authoritative baseline:** `ee5fb4b010eaf1b5295b57dc343a4e20441cf133` (verified local = origin = server before work began).
**Entry status:** `HAWKES_V2_PREMODELING_AUDIT_COMMITTED_PUSHED_AND_SERVER_SYNCED_MODELING_BLOCKED`.

**No fitting, simulation, synthetic-event generation, or false-Hawkes experiment occurred in this operation.** Phase D was not rerun. The production Hawkes code, data, visual, LR statistic, and displayed p-value were not modified.

---

## 1. Entry blockers (unchanged framing from prior audit)

```text
H-05 = FAIL   H-08 = FAIL   A_V2 = FAIL   P_141 = FAIL   F_SLR = FAIL
O_obs = PASS  E_epi = PASS  I_guard = PASS
```

## 2. Work Package A — six deduplication cases

All 6 cases adjudicated using existing per-row researcher notes already present in the working provenance CSV (no invented locators, no deleted/rewritten authoritative data). Full detail: `HAWKES_BASELINE_V2_DEDUP_ADJUDICATION.csv`.

| Case | Outcome |
|---|---|
| DEDUP-01 (Barus, Jan vs Jun 1681) | SAME_EPISODE_DISTINCT_EVENTS |
| DEDUP-02 (Koto Tangah pardon vs Vogel execution account) | DISTINCT_HISTORICAL_EVENTS |
| DEDUP-03 / DEDUP-04 (Indrapura English-defection campaign, reciprocal pair) | SAME_EPISODE_DISTINCT_EVENTS |
| DEDUP-05 (Koto Tangah 1755 vs CD6 renewal list) | REQUIRES_FOLIO_OR_SOURCE_CHECK — genuinely unresolved |
| DEDUP-06 (Bayang GM vs unread CD3 "Corpus III, nr. D") | REQUIRES_FOLIO_OR_SOURCE_CHECK — genuinely unresolved |

```text
D_u = 2 (unresolved)
G_dedup = 1[D_u=0] = 0
```
4/6 cases resolved as genuinely distinct events (no merge, no denominator change). 2/6 remain honestly unresolved pending a specific, named folio/source check — not forced to a decision.

## 3. Work Package B — 32 provenance-ambiguous events

All 32 individually classified. Full detail: `HAWKES_BASELINE_V2_PROVENANCE_REMEDIATION.csv`.

```text
16 events: ambiguity_type=OTHER_EXPLICIT, resolution_status=PROVENANCE_NOT_RESOLVED
           (primary_source_collection literally recorded as "unverified" in Phase B —
            the page/folio exists but which archival series it belongs to was never confirmed)
16 events: ambiguity_type=SECONDARY_SOURCE_ONLY, resolution_status=PROVENANCE_PARTIALLY_RESOLVED
           (buku-padang-1718 x7, Kathirithamby 1965 PhD thesis x9 — stable, previously
            identity-verified secondary academic citations, but chain back to a primary
            archival document is unverified)
```
No locator was invented. The 16 `PROVENANCE_NOT_RESOLVED` events require a genuinely new archival identification step (out of scope here); the 16 `PROVENANCE_PARTIALLY_RESOLVED` events remain eligible for sensitivity analysis sets but excluded from the strict primary set (AS1).

## 4. Work Package C — event-date, document-date, and interval audit

Full detail: `HAWKES_BASELINE_V2_DATE_SEMANTICS.csv` (141 rows).

```text
EXACT_DAY: 72   MONTH_ONLY: 10   YEAR_ONLY: 16   DATE_INTERVAL: 21   UNRESOLVED: 22
exact_event_date_eligible = 72/141
interval_eligible = 119/141
```
No document date was silently treated as an event date.

## 5. Work Package D — analysis-set registry

Full detail: `HAWKES_BASELINE_V2_ANALYSIS_SET_REGISTRY.csv`. The 141-event corpus itself was not overwritten.

```text
AS0_FULL_CORPUS                    n=141
AS1_PROVENANCE_CLEARED             n=95   (candidate primary set)
AS2_EXACT_EVENT_DATES              n=72
AS3_INTERVAL_ELIGIBLE              n=119
AS4_ONE_EVENT_PER_PARENT_EPISODE   n=85
AS5_EXCLUDE_UNRESOLVED_DEDUP       n=139  (candidate primary set)
AS6_EXCLUDE_VOC_ONLY_CLASSIFICATIONS  n=141 (NOT_EVALUABLE — no such column exists in the current schema)
```
Every denominator was derived mechanically from the underlying columns, not assumed.

## 6. Work Package E — supplementary point-process SLR

Bounded, separate from the completed search-method SLR; the final C1-C6 substantive review was **not** run. Full detail: `HAWKES_BASELINE_V2_POINT_PROCESS_SLR_LEDGER.csv`.

```text
5 candidates evaluated, 1 admitted (A_j^method=1): Laub, Lee, Pollett, Taimre (2024)
4 identity-confirmed but blocked on exact provenance (P_j): Ogata (1988, JASA) for the
  time-rescaling theorem, Self & Liang (1987, JASA) for boundary-null LRT theory,
  Kwan et al. (2024), Potiron et al.
```
Two new, correctly-identified primary references were found this operation (Ogata 1988; Self & Liang 1987) via bounded WebSearch — both are the right sources for their respective gaps, but their exact section/theorem provenance was not confirmed against full text this session (likely paywalled).

## 7. Formula-source remediation

Full detail: `HAWKES_BASELINE_V2_FORMULA_SOURCE_LEDGER_REMEDIATED.csv`.

```text
Before this operation: 10/14 formulas passed A_r^formula
After this operation:  13/14 formulas pass A_r^formula
Residual gap: F-08 (time-rescaling theorem) — correct source (Ogata 1988) now identified,
              exact section/theorem number (P_r) still unconfirmed
F_SLR = 1[F_R=F_A] = 1[13=14] = 0  (FAIL, unchanged verdict, narrowed to one named blocker)
```

## 8. Boundary-null LR remediation

Full detail: `HAWKES_BASELINE_V2_BOUNDARY_NULL_TEST_SPECIFICATION.csv`. No corrected p-value was computed.

```text
INTERIM_INFERENCE_POLICY = MODEL_COMPARISON_WITHOUT_ASYMPTOTIC_P_VALUE (fully admissible now,
                              A_q=1 — report AIC/BIC differences instead of the disputed p-value)
Candidate long-term fix:      BOUNDARY_MIXTURE_REFERENCE_CANDIDATE_NOT_YET_VALIDATED
                              (Self & Liang 1987 is the identified candidate source for a one-sided
                              boundary parameter; NOT adopted as an established reference distribution
                              this operation — beta may be unidentified under alpha=0, and the exact
                              Hawkes-specific regularity conditions required by Self & Liang have not
                              been verified. No specific mixture form is asserted as correct.)
```
CURRENT_PRODUCTION_P_VALUE = NUMERICALLY_REPRODUCED_BUT_NOT_METHODOLOGICALLY_VALIDATED, unchanged and undisturbed. No corrected p-value was calculated or reported.

## 9. H-05 and H-08 resolution

Full detail: `HAWKES_BASELINE_V2_G7_GATE_MATRIX_REMEDIATED.csv`.

```text
H-05: FAIL (unchanged) — a V2 recovery design fully distinct from Phase D was specified
      (Work Package G, D_distinct=1) but NOT executed (execution prohibited this operation)
H-08: FAIL (unchanged) — out of this operation's scope; a separate historical-inference
      authorization decision was neither sought nor granted here
G_G7 = 0 (unchanged; H-01/02/03/04/06/07 remain NOT_EVALUABLE)
```
The gates were not redefined to fit available evidence.

## 10. Distinct V2 recovery design

Full detail: `HAWKES_BASELINE_V2_RECOVERY_DISTINCTION_MATRIX.csv`. All 8 required distinction components (estimand, data-generating process, observation process, date-uncertainty mechanism, source-exposure mechanism, comparator suite, recovery criteria, Phase-D-not-rerun) are satisfied by design.

```text
D_distinct = 1  (design only — this design was NOT executed in this operation)
```

## 11. Observation and exposure contract

Full detail: `HAWKES_BASELINE_V2_EXPOSURE_CONTRACT.csv`, recomputed fresh this operation (not copied from the prior audit).

```text
O_obs = 1 (PASS) — CD covers the full 1600-1784 event range; GM (from 1660) and
                   Daghregister (1661-1681 canonical) are partial-range sensitivity candidates
```

## 12. Model feasibility and model-role recommendation

Full detail: `HAWKES_BASELINE_V2_MODEL_FEASIBILITY_REMEDIATED.csv`.

```text
M0 FEASIBLE | M1 FEASIBLE_WITH_LIMITATIONS | M2 FEASIBLE_WITH_LIMITATIONS (boundary-null caveat)
M3 NOT_FEASIBLE (H-02 unmet) | M4 FEASIBLE_WITH_LIMITATIONS (CD circularity risk flagged)
M5 FEASIBLE_WITH_LIMITATIONS | M6 NOT_FEASIBLE (strata too sparse, unchanged finding)
```
Primary comparator recommendation: `INHOMOGENEOUS_POISSON` (given CD's full-range availability as a candidate baseline covariate, once H-02 is resolved). Hawkes role recommendation: `SECONDARY_SENSITIVITY_MODEL` pending H-05/H-08/A_V2 resolution — not `PRIMARY_EXPLORATORY_MODEL` while G_G7=0, and never `NOT_AUTHORIZED` outright, since the design work here shows a defensible path forward.

## 13. Recomputed gates

```text
G_G7           = 0   (H-05 FAIL, H-08 FAIL)
D_distinct     = 1
P_141          = 1[G_dedup=1 AND analysis-set/date semantics sufficient] = 1[0 AND 1] = 0
F_SLR          = 0   (13/14 formulas pass, 1 residual gap)
O_obs          = 1
E_epi          = 1
I_guard        = 1

G_V2_preauth = G_G7 x D_distinct x P_141 x F_SLR x O_obs x E_epi x I_guard
             = 0 x 1 x 0 x 0 x 1 x 1 x 1
             = 0
```

Full detail and corrective actions for every non-1 factor: `HAWKES_BASELINE_V2_RESIDUAL_BLOCKER_MATRIX.csv`.

## 14. Validation gate

```text
R_D=1  (6 dedup cases have terminal status: 4 adjudicated, 2 explicitly unresolved)
R_P=1  (all 32 provenance-ambiguous events have terminal remediation status)
R_T=1  (date semantics and bounds explicit for all 141 events)
R_A=1  (7 analysis-set denominators reconcile mechanically)
R_S=1  (point-process SLR contains admissible support for the one fully-passing item; gaps named)
R_B=1  (boundary-null procedure methodologically specified, interim + long-term)
R_H=1  (H-05, H-08 evaluated from authoritative definitions, not redefined)
R_V=1  (V2 recovery distinction explicit, all 8 components)
R_O=1  (exposure contract provenance-grounded, recomputed fresh)
R_M=1  (model feasibility and estimands explicit for all 7 models)
R_I=1  (interpretation boundaries preserved — see Sec.24 §3 boundary text unchanged)
R_0=1  (0 fits, 0 simulations, 0 synthetic events, 0 false-Hawkes runs, Phase D untouched)

G_V2_remediation = 1
```

## 15. Since G_V2_preauth = 0

Per instruction §17-18, **no authorization recommendation of `AUTHORIZE_V2_MODELING_WITH_LIMITATIONS` may be issued, and no `HAWKES_BASELINE_V2_MODELING_AUTHORIZATION_DECISION.md` artifact is created.** See `HAWKES_BASELINE_V2_MODELING_AUTHORIZATION_RECOMMENDATION.md` for the recommendation actually issued.

## Final status

```text
HAWKES_V2_BLOCKER_REMEDIATION_COMPLETE_MODELING_REMAINS_BLOCKED
```
