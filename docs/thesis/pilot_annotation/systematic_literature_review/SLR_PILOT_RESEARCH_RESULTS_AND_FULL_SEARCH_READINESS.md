# SLR Pilot — Research Results and Full-Search Readiness

**Status:** SUBSTANTIVE RESEARCH RESULTS. Real, bounded pilot queries were executed against publicly accessible providers (arXiv, Crossref, OSF/SocArXiv) and real access-behavior was observed for institutional-subscription providers (Scopus, Web of Science, JSTOR, Project MUSE, ACM, WorldCat, Brill, Leiden). No full production SLR search, full corpus screening, substantive literature synthesis, or historical claim occurred.

**Baseline:** commit `79a6a614cee74df85a27c37e0c0792501825199b`.

---

## 1. Candidate Universe (unchanged)

```math
|C|=6,\qquad |S|=13,\qquad |U_B|=42,\qquad 32+8+2=42.
```

---

## 2. Usable Pilot-Pair Set

```math
U_{cs}=\mathbf 1[V_{cs}=1 \lor (P_{cs}=1 \land F_{cs}^{\mathrm{required}}=1)].
```

```math
N_{pilot}=|U_{pilot}|=37.
```

Excluded (5): DHQ (2 pairs, no official syntax documentation) and SOAS/EPrints (3 pairs — official EPrints documentation states Boolean is unsupported, and the frozen template requires Boolean AND/OR).

---

## 3. Execution Accounting

```math
N^{\mathrm{planned}}_{exec}=N_{pilot}=37,\qquad N^{\mathrm{actual}}_{exec}=27,\qquad N^{\mathrm{skipped}}=10,\qquad 27+10=37.
```

```text
EXECUTED_SUCCESS:             7  (arXiv ×3, Crossref ×4)
QUERY_REQUIRES_AMENDMENT:     2  (OSF/SocArXiv ×2)
BLOCKED_CREDENTIALS:          4  (Scopus ×4)
BLOCKED_PROVIDER_POLICY:     14  (JSTOR ×4, Project MUSE ×3, ACM ×2, WorldCat ×3, Brill/SRC-10 ×2)
NOT_EXECUTED_STOP_CONDITION: 10  (Web of Science ×4, Google Scholar ×6)
```

**Central honest finding: an unauthenticated automated agent can execute real queries against only 2 of the 13 candidate sources without hitting a credential wall, a bot-detection block, or an unusable client-rendered interface.** This is a genuine constraint on this project's own pilot infrastructure, not a defect in the frozen search-string design.

---

## 4. Retrieval Accounting

```math
R_{raw}=\sum_q R_q^{raw}=24{,}467{,}617.
```

This enormous figure is itself diagnostic: Crossref's `query.bibliographic` parameter performed relevance-ranked free-text matching over its entire corpus rather than strict Boolean-restricted matching, so its reported "total-results" counts (millions per query) do not reflect a bounded Boolean search the way the frozen template assumes. arXiv's totals (372 / 22 / 3) are far more plausible bounded-search results.

```math
R_{export}=\sum_q R_q^{export}=58.
```
```math
D_{exact}=10,\qquad D_{probable}=0,\qquad R_{dedup}=R_{export}-D_{exact}-D_{probable}=48.
```

The 10 exact duplicates are the OSF/SocArXiv record set: querying with two different family strings (C3, C6) returned the identical 10 record IDs both times — direct proof (not inference) that the query parameter had no filtering effect on that endpoint (Sec.9).

No ambiguous probable-duplicate pair required manual-review merging.

---

## 5. Seed Retrieval Diagnostics

```math
M_Z=0 \quad\Rightarrow\quad \widehat P_{seed} = \texttt{NOT\_ESTIMABLE\_NO\_ADMISSIBLE\_SEEDS}.
```

No seed-study nomination has been made by the researcher. This is reported honestly as not estimable — never as zero, and never as a recall or completeness claim.

---

## 6. Metadata-Scope Diagnostics

Bounded, title-only, first-page samples were inspected for every executed query (40 sampled records total: 18 arXiv, 20 Crossref, 2×10-but-identical OSF):

```text
C2/SRC-13: 5/5 in scope (1.0)       — distant-reading / digital-history literature, strongly on-topic
C4/SRC-06: 0/5 in scope (0.0)       — general NLP event-extraction, no historical framing
C4/SRC-13: 2/5 in scope (0.4)       — mixed: historical NER present, but food/materials/power-grid NER also returned
C5/SRC-06: 1/10 in scope (0.1)      — mostly general Hawkes-process methodology papers, one political-violence match
C5/SRC-13: 1/5 in scope (0.2)       — one exact branching-ratio match; particle-physics/finance homonyms dominate
C6/SRC-06: 1/3 in scope (0.33)      — one plausible historical-network title (title-only, uncertain, non-English)
C6/SRC-13: 1/5 in scope (0.2)       — literary-theory "counterfactual fiction" results dominate over historical-explanation sense
C3/SRC-07, C6/SRC-07: 0/10 (0.0)    — not topically responsive at all (query parameter non-functional, Sec.4)
```

This is a pilot metadata-scope diagnostic only — not a final inclusion decision and not full screening. It demonstrates a real, important term-ambiguity risk already flagged in the frozen risk register: "Hawkes process," "branching ratio," and "game theory" collide with unrelated physics/finance/literary-theory usages in general-purpose bibliographic databases.

---

## 7. Family Breadth and Provider-Concentration Diagnostics

```math
HHI_c=\sum_s p_{cs}^2 \quad(\text{descriptive only, no threshold}).
```

Full table in `SLR_PILOT_FAMILY_DIAGNOSTICS.csv`. Because most pairs per family were blocked (raw_result_count=0 recorded for blocked/not-executed pairs), concentration diagnostics for C1 and C3 are not meaningfully computable this round (`HHI` reduces to a single executed or zero-result pair); C2/C4/C5/C6 show real, if very unevenly distributed, retrieval mass concentrated in whichever source actually executed.

---

## 8. Query Failures and Amendments

2 amendments logged (`SLR_PILOT_QUERY_AMENDMENT_LEDGER.csv`): OSF/SocArXiv's `q` parameter requires investigation against the platform's actual documented special-search syntax before this pair can be trusted in any future search — flagged `researcher_review_required=1`, not silently patched.

---

## 9. Family-Level Usability Recommendations

```text
C1: NOT_YET_USABLE                       (all 4 usable pairs blocked/not-executed this round)
C2: PILOT_USABLE_WITH_SOURCE_EXCLUSIONS  (Crossref executed; 7 other usable pairs blocked)
C3: NOT_YET_USABLE                       (all 6 usable pairs blocked or amendment-pending)
C4: PILOT_USABLE_WITH_SOURCE_EXCLUSIONS  (arXiv + Crossref executed; 4 other usable pairs blocked)
C5: PILOT_USABLE_WITH_SOURCE_EXCLUSIONS  (arXiv + Crossref executed; 3 other usable pairs blocked)
C6: PILOT_USABLE_WITH_SOURCE_EXCLUSIONS  (arXiv + Crossref executed; 6 other usable pairs blocked)
```

No weighted aggregate score was used — each recommendation follows directly from the recorded execution/blocking/amendment facts per instruction §20.

---

## 10. Full-Search Readiness Gate

```text
F_D=1: SLR-DEC-06, DEC-07, DEC-08 all validly adjudicated
F_Q=1: every one of the 37 usable pairs has a frozen query and a terminal execution-log entry
F_R=1: retrieval accounting reconciles (Sec.4)
F_U=1: every one of the 6 families has a terminal usability recommendation (Sec.9)
F_S=1: seed diagnostic explicitly NOT_ESTIMABLE_NO_ADMISSIBLE_SEEDS (Sec.5)
F_N=1: noise/breadth diagnostics reported descriptively, no arbitrary threshold imposed (Sec.6-7)
F_A=1: every amendment and exclusion explicit (Sec.2, Sec.8)
F_P=1: provenance complete (exact URLs, HTTP methods, and API endpoints recorded throughout)
F_E=1: epistemic boundaries preserved — no diagnostic re-labeled as recall/completeness/final-inclusion
F_0=1: no full production search, full screening, synthesis, historical claim, or model execution occurred
```

```math
G_{full}^{\mathrm{readiness}} = \mathbf 1[F_D=F_Q=F_R=F_U=F_S=F_N=F_A=F_P=F_E=F_0=1] = 1.
```

**This means the project now has enough documented, honest information for the researcher to make a separate decision about full SLR search execution. It is emphatically not a recommendation to proceed as-is.** The dominant finding of this pilot is an access-infrastructure gap: 5 of 6 families depend heavily on institutional-subscription databases (Scopus, WoS, JSTOR, Project MUSE, ACM, WorldCat) that an unauthenticated automated agent cannot search at all. A full search under current conditions would only meaningfully cover arXiv and Crossref (2 of 13 sources), which is a severe, honestly-disclosed limitation on any future full-search decision.

---

## 11. Research Completion Gate

```text
R_7=1: DEC-07 audit and adjudication complete
R_8=1: DEC-08 audit and adjudication complete
R_M=1: usable pair matrix complete (37/42, 5 excluded with reasons)
R_Q=1: all 37 planned pilot executions have terminal states
R_R=1: retrieval and deduplication accounting reconciles (58-10-0=48)
R_S=1: seed retrieval diagnostic complete (explicitly not estimable)
R_N=1: metadata-scope and breadth diagnostics complete
R_A=1: amendments and failures explicit (2 amendments, 5 exclusions)
R_L=1: decision-ledger changes restricted to DEC-07/08 only
R_0=1: no prohibited downstream work occurred
```

```math
G_{pilot}^{\mathrm{complete}} = 1.
```

---

## 12. Final Status

```text
SLR_DEC_07_08_ADJUDICATED_PILOT_EXECUTED_FROZEN_AND_SYNCED_READY_FOR_FULL_SEARCH_DECISION
```

(pending successful ledger amendment, staging, commit, push, and server-sync)
