# SLR-DEC-05 — Researcher Decision Record

**Status:** DECISION RECORD ONLY. The authoritative decision ledger (`SLR_RESEARCHER_DECISION_LEDGER.csv`) is not modified in this turn. This artifact records the researcher's adopted outcome for `SLR-DEC-05` and the required pre-ledger term-inventory reconciliation. A separate, later, narrowly-scoped instruction is required to amend the ledger row itself.

**Baseline:** `SLR_DEC_05_ADJUDICATION_RECOMMENDATION_READY_FOR_RESEARCHER_DECISION`.

---

## 1. Scope

Record the researcher's decision for `SLR-DEC-05` only, and reconcile a term-inventory count discrepancy that must be resolved before any future ledger amendment. No other decision is touched. No ledger write occurs in this turn.

---

## 2. Authoritative Baseline

```text
SLR-DEC-05 recommendation:  APPROVE_WITH_LIMITATIONS (per SLR_DEC_05_RESEARCHER_ADJUDICATION_RECOMMENDATION.md)
SLR-DEC-05 ledger status:   PENDING_RESEARCHER_DECISION (unchanged)
SLR-DEC-06 ledger status:   PENDING_RESEARCHER_DECISION, G_6^decision_ready = 0
SLR-DEC-07 ledger status:   PENDING_RESEARCHER_DECISION
SLR-DEC-08 ledger status:   PENDING_RESEARCHER_DECISION
```

---

## 3. Recommendation Reviewed

`SLR_DEC_05_RESEARCHER_ADJUDICATION_RECOMMENDATION.md` recommended `APPROVE_WITH_LIMITATIONS`, scoped to: SRC-12 confirmed discovery-only; SRC-08/SRC-13 conditional pending bulk-search-suitability verification; 10 access-blocked sources neither approved nor rejected. The researcher has reviewed this recommendation and adopts it as-is.

---

## 4. Researcher Decision

```text
SLR-DEC-05:
APPROVE_WITH_LIMITATIONS
```

This is a recorded researcher decision, not yet a ledger amendment.

---

## 5. Evidence Domain

```math
|S|=13,\qquad N_5^{\mathrm{direct}}=1,\ N_5^{\mathrm{conditional}}=2,\ N_5^{\mathrm{review}}=10,\ N_5^{\mathrm{contradiction}}=0,\qquad 1+2+10+0=13.
```
```math
\widehat P_{\mathrm{verified}}=\tfrac1{13},\quad \widehat P_{\mathrm{partial}}=\tfrac2{13},\quad \widehat P_{\mathrm{blocked}}=\tfrac{10}{13}.
```

Unchanged from the recommendation artifact; these are provenance states, not votes.

---

## 6. Direct Support

`SRC-12` (Google Scholar) — the sole `DIRECT_SUPPORT` source, verified in its exact proposed role (`DISCOVERY_ONLY`, manual, never sole bibliographic authority).

---

## 7. Conditional Support

`SRC-08` (WorldCat) and `SRC-13` (Crossref) — identity/authority confirmed via S1-B1, bulk-literature-search suitability unconfirmed.

---

## 8. Access-Blocked Sources

Ten sources (`SRC-01, 02, 03, 04, 05, 06, 07, 09, 10, 11`) — `SOURCE_ACCESS_BLOCKED`, zero captured evidence. Not treated as supporting, contradicting, or neutral evidence for this decision.

---

## 9. Approved Scope

```text
SRC-12:
  Approved only for its verified discovery-only methodological role. Not approved as
  an independently sufficient bibliographic authority for any included record.

SRC-08 and SRC-13:
  Conditional support only. Includable in a future frozen S_A pending a separate,
  later verification of bulk-search suitability (a use-case distinct from the
  single-item lookup already verified in S1-B1). Not unconditionally frozen by
  this decision.

Ten SOURCE_ACCESS_BLOCKED candidates:
  Not approved, not rejected, and not treated as substantive evidence of any kind.
  Their status is unresolved pending independent future verification.
```

This decision must **not** be interpreted as: approval of all 13 sources; approval of any provider-specific query syntax; permission to execute any search string; approval of SLR-DEC-06, 07, or 08; or evidence that one verified source establishes universal methodological practice.

---

## 10. Explicit Limitations

- 10 of 13 candidate sources (76.9%) remain entirely unverified; this decision does not resolve that.
- The 3 non-blocked sources' evidence originates from a different use-case (S1-B1 single-item lookup) than SLR bulk search; only SRC-12's role transfers without a use-case gap.
- This decision does not constitute strong corroborating evidence — it reflects a well-formed but narrow evidence package.

---

## 11. Adjudication Gate

```math
E_5=P_5=B_5=C_5=N_5=L_5=I_5=1 \Rightarrow G_5^{\mathrm{adjudication}}=1.
```
```math
R_5=1 \ (\text{researcher explicitly adopts } \texttt{APPROVE\_WITH\_LIMITATIONS}),\qquad L_5^{\mathrm{recorded}}=1,\qquad D_6=D_7=D_8=0.
```
```math
G_5^{\mathrm{decision}}=\mathbf 1[G_5^{\mathrm{adjudication}}=1 \land R_5=1 \land L_5^{\mathrm{recorded}}=1 \land D_6=D_7=D_8=0]=1.
```

---

## 12. Term-Inventory Reconciliation

**Two reported count sets:**

```text
Earlier remediation report (SLR_SEARCH_STRING_REMEDIATION_AUDIT.md, Sec.5):
  59 total, 13 REQUIRES_REVIEW, 1 EXCLUDED_AMBIGUOUS_TERM

Latest adjudication report (SLR_DEC_05_RESEARCHER_ADJUDICATION_RECOMMENDATION.md, validation pass):
  47 DRAFT_CANDIDATE, 11 REQUIRES_REVIEW, 1 EXCLUDED_AMBIGUOUS_TERM  (47+11+1=59)
```

**Authoritative recount**, mechanically from `SLR_SEARCH_TERM_VARIANT_REGISTRY.csv` (59 rows) this turn:

```text
usage_status schema (mutually exclusive, exhaustive, confirmed 3 values only):
  DRAFT_CANDIDATE:          47
  REQUIRES_REVIEW:          11
  EXCLUDED_AMBIGUOUS_TERM:   1
  TOTAL:                    59   (47+11+1=59, reconciles)
```

**Cross-tab consistency check** (used to determine whether the difference is a reporting error or an actual undocumented status change) — every other independent tally in the earlier remediation audit was recomputed mechanically this turn and matches exactly:

```text
By family — audit: C1:10 C2:8 C3:13 C4:9 C5:10 C6:9   |  now: identical
By language — audit: en:46 nl:6 id:4 de:2 fr:1        |  now: identical
By variant_type — audit: PREFERRED_TERM:36, TRANSLATED_CONCEPT_CANDIDATE:15,
  HYPHENATION_VARIANT:5, SPELLING_VARIANT:2, MORPHOLOGICAL_VARIANT:1  |  now: identical
```

Since family, language, and variant_type distributions are byte-identical to the earlier audit while only the `REQUIRES_REVIEW` prose figure differs (13 vs. 11), no row's `usage_status` (or any other field) has changed since the registry was created — a status change would necessarily perturb at least one of these independent cross-tabs, and none moved.

**Authoritative `REQUIRES_REVIEW` row IDs (11, mechanically confirmed):**

```text
TV-C1-008, TV-C1-009, TV-C2-008, TV-C3-007, TV-C3-008, TV-C3-010,
TV-C3-011, TV-C3-012, TV-C4-009, TV-C6-008, TV-C6-009
```

**Correction (supersedes an earlier, unsupported explanation in this section):** a prior version of this section attributed the 13-vs-11 discrepancy to three specific `DRAFT_CANDIDATE` rows (TV-C1-006, TV-C1-007, TV-C3-006) allegedly folded into the earlier count. That explanation was arithmetically unsupported (11 authoritative rows + 3 alleged rows = 14, not 13) and was not reconstructed from any row-level evidence — it must not be treated as a proven claim.

A targeted reconciliation searched every surviving artifact for a row-level listing underlying the earlier "13" figure. The figure appears in exactly two places (`SLR_SEARCH_STRING_REMEDIATION_AUDIT.md` Sec.5 and `SLR_CANDIDATE_SOURCE_VERIFICATION_AUDIT.md`, the second apparently restating the first), both as an aggregate narrative count with no row IDs. No git history exists for this untracked file, and no backup or prior-version copy exists anywhere. The exact membership of the earlier 13-row set is therefore **not recoverable**.

The conservative, evidence-supported statement is:

```text
The authoritative inventory contains 47 DRAFT_CANDIDATE,
11 REQUIRES_REVIEW, and 1 EXCLUDED_AMBIGUOUS_TERM.
The earlier narrative count of 13 cannot be reconstructed at row level
and is treated as a reporting error of undetermined row composition.
No term status changed.
```

```text
R_reported membership:      NOT_RECOVERABLE
R_extra:                    UNDEFINED_FROM_SURVIVING_EVIDENCE
R_missing:                  UNDEFINED_FROM_SURVIVING_EVIDENCE
term-status mutations:      0
term promotions:            0
```

This value is classified as `UNRECONSTRUCTABLE_NARRATIVE_REPORTING_ERROR` — not as `PROVEN_THREE_ROW_FOLDING_ERROR`, `PROVEN_TWO_ROW_OVERCOUNT`, `TERM_STATUS_DRIFT`, or `AUTHORIZED_TERM_RECLASSIFICATION`.

**Reconciliation gate:**

```math
G_{\mathrm{term}}^{\mathrm{reconcile}}=\mathbf 1[\text{authoritative rows counted mechanically}\land\text{schema documented}\land\text{difference explained as unrecoverable, not invented}\land N_{\mathrm{promoted}}=0]=1.
```

```text
N_promoted (rows moved into DRAFT_CANDIDATE or out of REQUIRES_REVIEW/EXCLUDED this turn): 0
```

No `SLR_DEC_05_DECISION_RECORDING_BLOCKED_BY_TERM_STATUS_DRIFT` condition triggered.

---

## 13. Provider-Syntax Immutability

```text
VERIFIED = 0
UNVERIFIED_NOT_EXECUTED = 42
NOT_APPLICABLE = 36
0+42+36=78  (reconciles)
```

No provider syntax is approved, verified, or otherwise changed by this decision.

---

## 14. SLR-DEC-06 Nonauthorization

```math
G_6^{\mathrm{decision\_ready}}=0.
```
```text
SLR-DEC-06 = PENDING_RESEARCHER_DECISION (unchanged)
SLR-DEC-06 ADJUDICATION = NOT_AUTHORIZED
```

Not inferred from or affected by this SLR-DEC-05 decision.

---

## 15. SLR-DEC-07/08 Nonauthorization

```text
SLR-DEC-07 = PENDING_RESEARCHER_DECISION (unchanged)
SLR-DEC-08 = PENDING_RESEARCHER_DECISION (unchanged)
```

No adjudication authorized or attempted.

---

## 16. Decision-Ledger Immutability

```text
SLR_RESEARCHER_DECISION_LEDGER.csv: BYTE-UNCHANGED, not opened for writing this turn
SLR-DEC-05 ledger row: PENDING_RESEARCHER_DECISION (unchanged — decision recorded here, not yet applied to ledger)
```

---

## 17. Search and Retrieval Prohibition

```text
queries submitted/tested/retrieved: 0
databases queried: 0
records retrieved: 0
```

---

## 18. Stop Conditions

None triggered: 13-source denominator unchanged; DEC-05 mapping remains 1/2/10/0; recommendation artifact supports `APPROVE_WITH_LIMITATIONS`; term counts reconciled mechanically with an explained, non-drift cause; zero term promotions; no blocked source treated as evidence; provider syntax unchanged (0/42/36); DEC-06/07/08 unchanged; decision ledger unchanged; zero search/query/retrieval; nothing staged.

---

## 19. Future Ledger-Amendment Boundary

This record is a precondition for, but is not itself, a ledger amendment. A separate, later, explicitly authorized instruction is required to write `APPROVE_WITH_LIMITATIONS` (with this record's exact approved-scope language) into the `SLR-DEC-05` row of `SLR_RESEARCHER_DECISION_LEDGER.csv`. That instruction must reference this record by name and must not broaden scope beyond what is recorded in Section 9.

---

## 20. Final Status

```text
SLR_DEC_05_RESEARCHER_DECISION_RECORDED_AWAITING_SEPARATE_LEDGER_AMENDMENT
```
