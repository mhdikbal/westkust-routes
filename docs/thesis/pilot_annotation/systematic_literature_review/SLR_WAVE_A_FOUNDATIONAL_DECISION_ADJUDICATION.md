# SLR — Wave A Foundational Decision Adjudication

**Canonicalization note:** this artifact was originally authored and named `SLR_WAVE_A_DECISION_ADJUDICATION.md`. It has been renamed to the authoritative filename `SLR_WAVE_A_FOUNDATIONAL_DECISION_ADJUDICATION.md` during the Wave A output-completeness reconciliation. No content was duplicated — the prior filename no longer exists as a separate file; this is the single canonical record of the Wave A adjudication, under its provenance-preserved history.

**Status:** ADJUDICATION RECORD. Resolves 8 of the 12 researcher decisions from `SLR_RESEARCHER_DECISION_LEDGER.csv`. Does not freeze the SLR protocol, does not approve any search source or string, does not authorize search execution, and does not integrate these decisions into the eight original planning artifacts yet — that additive-integration step is deliberately deferred to after Wave B/C, per the researcher's own stated sequence (§5 below).

**Baseline:** SLR pre-freeze audit (`SLR_PROTOCOL_PREFREEZE_AUDIT_COMPLETE_RESEARCHER_DECISIONS_PENDING`), `G_SLR^pre-freeze = 1`.

---

## 1. Wave Structure

```text
Wave A (decidable now, no search-design dependency):    SLR-DEC-01, 02, 03, 04, 09, 10, 11, 12
Wave B (blocked on search-design remediation):          SLR-DEC-05, 06
Wave C (blocked on Wave B):                              SLR-DEC-07, 08
```

`SLR-DEC-06` cannot be adjudicated yet because `G_C^{string}=0` for all six families — each has `K_c=H_c=X_c=1` (core concepts, humanities context, and zero execution all confirmed) but `V_c=P_c=F_c=B_c=0` (lexical variants, provider-specific syntax translation, filter rationale, and breadth/narrowness risk are all undocumented). `SLR-DEC-05` cannot be adjudicated yet because most of the 13 candidate sources carry `NOT_VERIFIED_FOR_SLR_USE` — the three sources verified for S1-B1 (WorldCat, Google Scholar, Crossref) were verified for single-item lookup, not SLR-scale literature-search behavior, and that verification does not transfer automatically.

```math
G_{SLR}^{\mathrm{WaveA}}=\mathbf 1[W_1=W_3=W_4=W_9=W_{10}=W_{11}=W_{12}=W_0=1],
```

where `W_k=1` denotes decision `SLR-DEC-0k` adjudicated and `W_0=1` denotes zero search/retrieval/screening/extraction/model-execution occurred during adjudication.

Expected and confirmed this turn:

```math
G_{SLR}^{\mathrm{WaveA}}=1.
```

This does **not** imply protocol freeze-readiness — `G_C^{string}=0` still holds independently and blocks Wave B regardless of `G_SLR^WaveA`.

---

## 2. SLR-DEC-01 — Review Type

**Decision:** `APPROVED_WITH_LIMITATIONS`

```text
SYSTEMATIC_SCOPING_REVIEW
PRISMA_2020_COMPATIBLE_REPORTING
NO_PRESUMED_META_ANALYSIS
```

**Rationale:** matches the review type already consistently drafted across all eight original artifacts and confirmed contradiction-free by the pre-freeze audit (`D_T=1`). The "limitation" flagged is explicit: quantitative pooling remains not-presumed-applicable and requires a future, separately justified amendment demonstrating design/estimand compatibility before any pooling occurs — this is a limitation on scope, not a caveat on the decision's validity.

---

## 3. SLR-DEC-02 — Language Scope

**Decision:** `APPROVED_WITH_LIMITATIONS`

```text
LANGUAGES: English, Dutch, German, French, Indonesian
NO ENGLISH-ONLY EXCLUSION AT SCREENING
```

**Limitation, explicitly recorded:** full-text inclusion is conditional — a record only proceeds past full-text screening if language competence or documented translation support exists for that specific record. A non-English record is never excluded at title/abstract screening solely for its language; it may still be excluded at full-text stage under the explicit reason `EXCL_LANGUAGE_NOT_PROCESSABLE` (already defined in the eligibility document's exclusion taxonomy) if no competence or translation support materializes for it specifically.

**Rationale:** matches the candidate policy already drafted in the protocol (§9) and directly addresses the audit's own flagged risk that English-only search would miss foundational Dutch/German colonial-archive-criticism and hermeneutic-theory literature (domains S1, S3).

---

## 4. SLR-DEC-03 — Temporal Scope

**Decision:** `APPROVED_WITH_LIMITATIONS`

```text
METHOD_SPECIFIC_DATE_WINDOWS
```

```text
S1 (computational hermeneutics) and S3 (colonial archive criticism): NO_LOWER_DATE_LIMIT
  - foundational hermeneutic theory (e.g. Gadamer-era and earlier) and archival theory
    are explicitly in scope regardless of publication date.
S2, S4, S5, S6 (digital humanities, historical NLP, Hawkes/temporal modeling,
  network/game-theory/counterfactual methodology): NO_LOWER_DATE_LIMIT AS A DEFAULT,
  with the explicit acknowledgment that empirical density is expected to concentrate
  from the point each underlying method became practically computable
  (e.g. Hawkes processes from their 1971 origin; historical NLP/entity-extraction
  literature concentrated post-2000). This is a documented EXPECTATION about where
  evidence will cluster, NOT an applied cutoff filter.
```

**No universal cutoff is adopted.** No upper date limit is applied (the review runs to the present). Any future decision to apply an actual filter cutoff (rather than this documented expectation) requires a separate, explicitly provenanced amendment — not silently applied during search-string construction.

**Rationale:** avoids the audit's flagged risk of an indefensible universal cutoff, while acknowledging that method-specific literatures have real, known historical starting points that inform (but do not filter) the search.

---

## 5. SLR-DEC-04 — Publication-Type Scope

**Decision:** `APPROVED_WITH_LIMITATIONS`

```text
INCLUDE: peer-reviewed journal articles; books and book chapters; conference
  proceedings; doctoral theses; preprints; institutional reports; review articles.
INCLUDE WITH ADDITIONAL SCRUTINY: software/method documentation, editorials/
  perspectives — these are extracted only if they contain substantive
  methodological or conceptual content (i.e. they still must pass M(r)=1 and
  E(r)=1 at full-text stage; being a permitted TYPE does not waive the
  eligibility gate).
NO EXCLUSION OF HUMANITIES MONOGRAPHS/CHAPTERS FOR NOT BEING JOURNAL ARTICLES.
```

**Limitation, explicitly recorded:** grey literature, preprints, and theses are flagged in extraction (`EXT-01 publication_type`) so that the synthesis can distinguish peer-reviewed from non-peer-reviewed evidence when weighing contradictions — this is a transparency requirement, not an eligibility restriction.

**Rationale:** directly consistent with the project's own recent finding in S1-B1 (ET-10), where the single most load-bearing candidate record was an unpublished 1965 PhD thesis, not a journal article — excluding theses/grey literature by default would have been methodologically self-defeating for exactly this kind of source landscape.

---

## 6. SLR-DEC-09 — Deduplication Policy

**Decision:** `APPROVED_WITH_LIMITATIONS`

```text
FUZZY_SIMILARITY_GENERATES_CANDIDATES_ONLY
NO_AUTOMATIC_FUZZY_MERGE
tau_s: NOT SELECTED (remains without a numeric value)
```

**Limitation, explicitly recorded:** every fuzzy-candidate pair, regardless of similarity score, requires manual adjudication before being merged. No numeric `\tau_s` threshold is introduced by this decision — if a future turn wishes to calibrate one against a labeled duplicate sample, that is a separate, additional decision requiring its own provenance, not an amendment to this one.

**Rationale:** adopts the protocol's own already-documented conservative default (§8, §15) exactly as previously recommended by the pre-freeze audit, without inventing a number.

---

## 7. SLR-DEC-10 — Screening Arrangement

**Decision:** `APPROVED_WITH_LIMITATIONS`

```text
SINGLE_PRIMARY_PLUS_BLINDED_AUDIT_SAMPLE
```

**Limitation, explicitly recorded:** a second independent human screener is not assumed to exist for this project. This is disclosed as a limitation in any future review write-up, not concealed. An audit sample (size and selection method to be specified at the point screening actually begins, not invented now) is blind-reviewed by a second pass to estimate agreement; disagreements go to adjudication, not majority inference. No numeric Cohen's kappa threshold is imposed by this decision.

**Rationale:** matches the protocol's own explicit fallback for the realistic single-screener case (§10), formally adopted rather than left as an unstated default.

---

## 8. SLR-DEC-11 — Extraction Audit Arrangement

**Decision:** `APPROVED_WITH_LIMITATIONS`

```text
SINGLE_EXTRACTION_PLUS_AUDIT_SAMPLE
```

**Limitation, explicitly recorded:** consistent with SLR-DEC-10's single-screener realism, extraction is performed once per included record, with an audit sample re-extracted independently to check schema-application consistency across the 22 extraction fields. Audit-sample size/selection is specified at the point extraction actually begins.

**Rationale:** parallels the screening-arrangement decision for the same practical-resourcing reason, applied to the extraction stage instead of the screening stage.

---

## 9. SLR-DEC-12 — Appraisal Use in Synthesis

**Decision:** `APPROVED_WITH_LIMITATIONS`

```text
NON_WEIGHTED_DESCRIPTIVE_USE_ONLY
```

**Limitation, explicitly recorded:** the 10 appraisal dimensions (`SLR_APPRAISAL_AND_EPISTEMIC_BOUNDARY.md` §1) are reported individually and descriptively in synthesis (e.g., in the evidence map and methodological matrix); they are never collapsed into a weighted composite score. Adopting a weighted score in the future would require a separate methodological decision with its own construct-validity justification — not an amendment folded into this one.

**Rationale:** matches the appraisal document's own existing prohibition (§1) and the pre-freeze audit's confirmation that no weighted aggregation appears anywhere in the current artifacts (`D_A=1`).

---

## 10. Decision Ledger Update

`SLR_RESEARCHER_DECISION_LEDGER.csv` updated in place: the `status` column for SLR-DEC-01, 02, 03, 04, 09, 10, 11, 12 changes from `PENDING_RESEARCHER_DECISION` to `ADJUDICATED_APPROVED_WITH_LIMITATIONS`, each with its adopted decision text recorded in a new `adjudicated_decision` column. SLR-DEC-05, 06, 07, 08 are explicitly **not** touched and remain `PENDING_RESEARCHER_DECISION`.

---

## 11. What Remains Blocked (Wave B, Wave C)

```text
SLR-DEC-05 (search-source set):        PENDING_RESEARCHER_DECISION - blocked on SLR-specific
                                        verification of the 13 candidate sources (most currently
                                        NOT_VERIFIED_FOR_SLR_USE)
SLR-DEC-06 (search-string families):   PENDING_RESEARCHER_DECISION - blocked on remediating
                                        V_c, P_c, F_c, B_c for all six C1-C6 families
                                        (G_C^string = 0)
SLR-DEC-07 (pilot source/family set):  PENDING_RESEARCHER_DECISION - blocked on Wave B
SLR-DEC-08 (seed-study set):           PENDING_RESEARCHER_DECISION - blocked on Wave B
                                        (m not invented, no seed study populated from memory)
```

---

## 12. Recommended Sequence Going Forward (as stated by the researcher, restated for the record)

```text
1. Wave A adjudication                                    <- COMPLETE (this document)
2. Remediate C1-C6 search strings (add V_c, P_c, F_c, B_c)
3. Verify the 13 search sources specifically for SLR scope/use
4. Adjudicate SLR-DEC-05 and SLR-DEC-06
5. Construct the seed-study set and pilot design
6. Adjudicate SLR-DEC-07 and SLR-DEC-08
7. Integrate ALL 12 decisions additively into the eight original artifacts
8. Re-run the full consistency audit
9. Freeze the SLR protocol
10. Only then run the pilot search
```

No additive integration into the eight original planning artifacts occurs in this turn — that step is explicitly deferred to step 7 above, after Waves B and C complete, per the researcher's own instruction not to integrate piecemeal.

---

## 13. Stop-Condition Check (this turn)

```text
search or database query executed:       NO
literature record retrieved:              NO
SLR-DEC-05/06/07/08 adjudicated:          NO (explicitly held pending, as instructed)
numeric threshold invented (tau_s, kappa): NO
eight original artifacts modified:        NO (integration deferred to step 7)
S1-B2 or model execution:                 NO
file staged:                              NO
```

No stop condition triggered.

---

## 14. Final Status

```text
SLR_WAVE_A_DECISIONS_ADJUDICATED_WAVE_B_AND_C_PENDING
```
