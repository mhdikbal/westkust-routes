# SLR-DEC-06 — Targeted Evidence-Gap Plan

**Status:** PLANNING ONLY. No search, query, retrieval, screening, extraction, provider-syntax test, or DEC-06/07/08 adjudication occurs in this turn. This document specifies what methodological evidence is missing to adjudicate SLR-DEC-06, where it might be sought, how it would be evaluated, and what would make the decision evidence-ready — without collecting that evidence or presupposing its outcome.

**Baseline:** commit `8dbd48f2df36e39995a2a0795589383491d613f5` (local HEAD = origin/main = server HEAD, confirmed). SLR-DEC-05 = `ADJUDICATED_APPROVED_WITH_LIMITATIONS`. SLR-DEC-06/07/08 = `PENDING_RESEARCHER_DECISION`.

---

## 1. Purpose and Current State

SLR-DEC-06 governs whether the six search-string families (`C1`–`C6`) may be frozen for pilot and full-review search. The families have passed **documentation remediation**:

```math
G_C^{\mathrm{remediation}}=1
```

— every family has core/context terms, lexical variants, provider-syntax placeholders, filter justification, and breadth/narrowness risk documented (`SLR_SEARCH_STRING_REMEDIATION_AUDIT.md`). This is necessary but not sufficient. Remediation proves the families are *internally documented*; it does not prove they are *methodologically sound* — i.e., that an independent, authoritative source would endorse how they were built.

The candidate-source-to-decision matrix (`SLR_CANDIDATE_SOURCE_TO_DECISION_MATRIX.csv`) reports, for SLR-DEC-06 specifically:

```text
DIRECT_SUPPORT:      0
CONDITIONAL_SUPPORT: 0
BACKGROUND_ONLY:     3
NOT_APPLICABLE:      10
```

No candidate source among the 13 already surveyed directly or conditionally supports search-string *design methodology*. This is the evidence gap this plan addresses.

---

## 2. Decision Domain

```math
C=\{C_1,\ldots,C_6\},\qquad |C|=6.
```
```math
S=\{s_1,\ldots,s_{13}\},\qquad |S|=13.
```
```math
U=C\times S,\qquad |U|=6\times13=78.
```

Current provider-syntax reconciliation (unchanged, not touched this turn):

```math
0+42+36=78.
```

No syntax row is promoted, tested, or otherwise mutated by this planning turn.

---

## 3. Readiness Components and the Current Failure Point

```math
G_6^{\mathrm{decision\_ready}}=\mathbf 1[S_6=B_6=C_6=P_6=N_6=R_6=1].
```

| Component | Meaning | Current value |
|---|---|---|
| `S_6` | ≥1 directly or conditionally applicable methodological source supports search-string design | **0** |
| `B_6` | Scope and limitations explicit | 1 (already true — remediation documented boundaries) |
| `C_6` | Competing guidance/contradictions recorded | 1 (none found yet, recorded as such) |
| `P_6` | Exact provenance recorded | 1 |
| `N_6` | No arbitrary numerical rule introduced | 1 |
| `R_6` | Decision remains pending until adjudicated | 1 |

Only `S_6=0` blocks the gate. This plan exists to specify, without presupposing the result, what evidence-gathering would be required to test whether `S_6` can become `1`.

---

## 4. Evidence Questions

This plan targets methodological evidence for these questions — not review-corpus research questions, and not questions about the historical subject matter itself:

1. How should systematic-review search strings be developed and peer reviewed?
2. How should concept blocks, synonyms, lexical variants, translations, and controlled vocabulary be documented?
3. How should syntax be translated across heterogeneous providers?
4. How should search sensitivity, specificity, breadth, and narrowness be assessed without arbitrary thresholds?
5. How should known-item or seed-study checks be used without claiming total recall?
6. How should search-strategy amendments be versioned after a pilot?
7. What reporting standards apply to complete, reproducible search strategies?
8. How should multidisciplinary humanities-and-computational-method searches avoid domain collapse?

---

## 5. Evidence Classes

```text
SYSTEMATIC_REVIEW_SEARCH_GUIDELINE
SEARCH_STRATEGY_REPORTING_STANDARD
PEER_REVIEW_OF_SEARCH_STRATEGY_GUIDANCE
DATABASE_OR_PROVIDER_OFFICIAL_SYNTAX_DOCUMENTATION
MULTILINGUAL_INFORMATION_RETRIEVAL_GUIDANCE
HUMANITIES_BIBLIOGRAPHIC_SEARCH_METHOD
KNOWN_ITEM_OR_SEED_VALIDATION_METHOD
SEARCH_UPDATE_AND_AMENDMENT_GUIDANCE
```

No individual publication, guideline, or standard is named from memory in this plan. Only classes and discovery plans are specified; actual candidate evidence items are identified and verified in a future, separately authorized turn.

---

## 6. Evidence Admissibility

For a future candidate evidence item \(e_j\):

```math
A_j^{\mathrm{evidence}}=\mathbf 1[I_j=1\land M_j=1\land D_j=1\land P_j=1\land L_j=1].
```

- \(I_j\): identity and source authority verified;
- \(M_j\): methodological relevance to search design verified;
- \(D_j\): supports an exact DEC-06 design component (§7);
- \(P_j\): exact provenance location recorded;
- \(L_j\): limitations and applicability boundary recorded.

Accessibility alone (e.g., "this document exists and can be fetched") does not satisfy the gate — it must additionally verify identity, methodological relevance, a specific component link, provenance, and limitations.

---

## 7. Component-to-Evidence Coverage Model

```math
K_6=\{\text{concepts, variants, translations, syntax, filters, risk, seed checking, versioning, reporting}\},\qquad |K_6|=9.
```

For component \(k\) and future evidence item \(j\):

```math
M_{kj}=\mathbf 1(e_j \text{ directly supports component } k).
```
```math
N_k^{\mathrm{support}}=\sum_j M_{kj}\,A_j^{\mathrm{evidence}}.
```
```math
G_6^{\mathrm{coverage}}=\mathbf 1\!\left[\min_{k\in K_6} N_k^{\mathrm{support}} \ge 1\right].
```

This is a **future** evidence-coverage gate description, not a present source-count vote. No minimum evidence-item count is invented here; the requirement is only that each component eventually have at least one admissible supporting item. The full mapping of each of the 9 components to its candidate evidence class(es) is provided in the companion `SLR_DEC_06_COMPONENT_EVIDENCE_REQUIREMENT_MATRIX.csv`.

---

## 8. Provider-Syntax Evidence Gap

For every applicable family–source pair \((c,s)\):

```math
V_{cs}^{\mathrm{syntax}}=\mathbf 1(\text{official provider documentation verifies the proposed syntax translation}).
```

Current state (unchanged):

```math
\sum_{(c,s)\in U} V_{cs}^{\mathrm{syntax}} = 0,\qquad N_{\mathrm{applicable}}=42,\qquad N_{\mathrm{NA}}=36.
```
```math
\widehat P_{\mathrm{syntax}} = \frac{\sum V_{cs}^{\mathrm{syntax}}}{42}.
```

No minimum numerical percentage is selected in this plan. A later, separate adjudication must decide between two policy options (neither chosen here):

1. every applicable family-source pair used in the pilot must be individually verified against official provider documentation before use; or
2. unverified pairs are simply excluded from the pilot source set, and the pilot proceeds with a reduced, but fully-verified, subset.

---

## 9. Search-String Family Evidence Gap

```math
G_C^{\mathrm{remediation}}=1
```

does not establish methodological validity. For family \(c\), a future evidence-support indicator is defined:

```math
E_c^{\mathrm{method}}=\mathbf 1(\text{methodological evidence supports the family's construction and risk controls}).
```
```math
G_C^{\mathrm{evidence}}=\prod_{c=1}^{6} E_c^{\mathrm{method}}.
```

This gate is **not evaluated** in this planning turn — it is defined so that a future evidence-collection turn has an exact, pre-specified target to compute against.

---

## 10. Evidence Discovery Plan (by class)

Each row of the companion `SLR_DEC_06_EVIDENCE_DISCOVERY_REGISTRY.csv` specifies, for a given evidence class and a plausible provider class: the discovery objective, authoritative source types, proposed provider classes, query concept blocks (topic-level, not literal query strings), prohibited assumptions, expected evidence fields, exact provenance requirements, stop conditions, and the DEC-06 component(s) it would support. No discovery search is executed; no publication is named. The draft C1–C6 review-corpus search strings must not be reused to search for search-*method* guidance unless a separate future instruction approves that.

---

## 11. Controlled Web Boundary for a Future Turn

This planning turn does **not** authorize any web access. A future, separately authorized turn's permitted scope may include:

```text
official search-method guidance
official reporting standards
official provider syntax documentation
institutional or peer-reviewed methodological publications
```

Its prohibited scope must continue to include:

```text
execution of final C1-C6 systematic-review searches
retrieval of review-corpus studies
screening or extraction
silent provider-syntax testing
bulk database harvesting
```

---

## 12. Evidence Extraction Schema (planned, not populated)

The companion `SLR_DEC_06_EVIDENCE_EXTRACTION_SCHEMA.csv` defines exactly 15 fields (`evidence_id` through `notes`) that a future evidence-collection turn would populate per discovered item. No record is populated in this turn.

---

## 13. Contradiction Handling

For two future admissible evidence items \(e_a, e_b\) and component \(k\):

```math
C_{abk}=\mathbf 1(\text{the two admissible items prescribe materially incompatible rules for component } k).
```

If \(C_{abk}=1\), the required status is:

```text
DEC06_METHOD_GUIDANCE_CONTRADICTION_REQUIRES_RESEARCHER_REVIEW
```

Conflicts are never resolved by publication count, recency alone, or source prestige alone.

---

## 14. DEC-06 Evidence-Readiness (Planning) Gate

```text
E_U=1: evidence universe and classes explicit          (Sec.5)
E_D=1: discovery methods prespecified                   (Sec.10, registry)
E_A=1: admissibility gate explicit                       (Sec.6)
E_C=1: all 9 DEC-06 components map to evidence needs     (Sec.7, requirement matrix)
E_S=1: provider-syntax evidence needs explicit           (Sec.8)
E_X=1: extraction schema complete                        (Sec.12, schema csv)
E_K=1: contradiction handling explicit                   (Sec.13)
E_N=1: no arbitrary threshold or evidence count invented (Sec.7-9)
E_0=1: zero searches/retrievals/screenings/extractions/decision amendments occurred
```

```math
G_{06}^{\mathrm{gap\_plan}}=\mathbf 1[E_U=E_D=E_A=E_C=E_S=E_X=E_K=E_N=E_0=1]=1.
```

This does **not** change:

```math
G_6^{\mathrm{decision\_ready}}=0.
```

The evidence-gap plan being complete is a planning-quality result, not evidence itself.

---

## 15. Stop Conditions

None triggered: no evidence search or provider query executed; no individual methodological source selected from memory as verified evidence; no final C1-C6 search executed; no review-corpus record retrieved; no provider syntax tested or promoted; no numerical threshold or minimum source count invented; SLR-DEC-06 not adjudicated; SLR-DEC-07/08 work not begun; decision ledger unchanged; S1-B2/model work not begun; nothing staged.

---

## 16. Final Status

```text
SLR_DEC_06_EVIDENCE_GAP_PLAN_READY_FOR_RESEARCHER_REVIEW
```
