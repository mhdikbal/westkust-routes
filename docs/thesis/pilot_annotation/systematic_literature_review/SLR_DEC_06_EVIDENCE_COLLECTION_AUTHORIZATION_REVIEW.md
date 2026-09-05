# SLR-DEC-06 — Controlled Methodological-Evidence Collection Authorization Review

**Status:** AUTHORIZATION REVIEW ONLY. No evidence source is accessed, no web search or database query is executed, no methodological publication is retrieved, no provider syntax is tested or promoted, no candidate manifest is created, and SLR-DEC-06 is not adjudicated. This document assesses whether the frozen DEC-06 evidence-gap plan is sufficiently bounded to authorize, in a later and separate turn, only the *preparation* of a finite evidence-candidate manifest.

**Baseline:** commit `a7f8694c81b7a4e1fddf86b683887507abb031d1` — local HEAD = origin/main = server HEAD, confirmed. `SLR-DEC-06 = PENDING_RESEARCHER_DECISION`, `SLR-DEC-07/08 = PENDING_RESEARCHER_DECISION`, `G_06^gap_plan=1`, `G_6^decision_ready=0`.

---

## 1. Purpose

Determine whether the DEC-06 evidence-gap plan (5 artifacts, frozen and synced) is bounded enough — in domain, admissibility rule, track separation, accounting contract, and stop conditions — to authorize a **manifest-preparation-only** turn next. This review does not authorize evidence collection itself.

---

## 2. Authorized Future Evidence Domain

Unchanged from the gap plan — exactly 8 classes:

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

```math
|K_6| = 9 \quad (\text{unchanged}).
```

No historical review-corpus publication is authorized merely because it discusses a C1–C6 topic — the domain is methodological evidence about *how to search*, not the historical subject matter of the review itself.

---

## 3. Future Collection Unit (defined, not executed)

```math
a_j = \mathbf 1(\text{candidate evidence location } j \text{ is deliberately accessed}).
```
```math
N^{\mathrm{attempt}} = \sum_j a_j.
```

No maximum request count is invented in this review. The future manifest must derive its own denominator \(|E^*|\) from its actual row count once written.

---

## 4. Evidence Admissibility (unchanged from the gap plan)

```math
A_j^{\mathrm{evidence}} = \mathbf 1[I_j = M_j = D_j = P_j = L_j = 1].
```

- \(I_j\): identity and authority verified;
- \(M_j\): methodological relevance verified;
- \(D_j\): exact DEC-06 component supported;
- \(P_j\): exact provenance location recorded;
- \(L_j\): applicability boundary and limitation recorded.

Accessibility, recency, citation count, or institutional prestige alone never satisfies this gate.

---

## 5. Two-Track Separation

```text
TRACK A: methodological search-design guidance
TRACK B: official provider-syntax documentation
```

**Track A** informs: concepts, variants, translations, filters, breadth/narrowness risk, seed checking, versioning, reporting (8 of the 9 `K_6` components).

**Track B** informs only: syntax (the 9th `K_6` component) — verifying what a provider officially supports. Track B never validates the methodological quality of the six search-string families; it is a strictly narrower, mechanical documentation-matching exercise against the 42 applicable family-source pairs.

The two tracks are never combined into a single support count — a Track B finding cannot substitute for, or count toward, Track A's `N_k^support` for any of the 8 Track-A components, and vice versa.

---

## 6. Provider-Syntax Domain (unchanged)

```math
|C\times S| = 78,\qquad 0+42+36=78.
```
```math
\widehat P_{\mathrm{syntax}} = \frac{N_{\mathrm{verified}}}{42} = \frac{0}{42} = 0.
```

No acceptance threshold is authorized by this review. Any future change to a syntax row's verification state may occur only in a separately authorized collection turn, and only with exact provider provenance recorded per row.

---

## 7. Candidate-Manifest Requirement (specification only — not created here)

A future, separate turn must produce a finite candidate set:

```math
E^* = \{e_1,\ldots,e_J\}.
```

\(J\) must be read off the actual number of manifest rows once written — never asserted in narrative prose ahead of the rows existing. Every manifest row must carry these 17 fields:

```text
evidence_candidate_id, track, evidence_class, DEC06_component,
candidate_source_or_issuing_body, candidate_document_title_or_documentation_area,
discovery_path, access_path, expected_authority_basis, expected_provenance_location,
collection_action, prohibited_action, predecessor_candidate_id, escalation_condition,
execution_status, stop_condition, notes
```

Every row in that future manifest must be `execution_status=PLANNED_ONLY` at the moment of its creation.

```math
K_{\mathrm{manifest}} = 17.
```

*Correction note:* Pre-freeze independent review mechanically recounted the unchanged ordered manifest schema and found 17 fields. Earlier references to 16 fields were an off-by-one documentation error. No field was added, removed, renamed, reordered, or redefined, and the future candidate count \(J\) remains undetermined.

---

## 8. Request and Access Envelope (specification only)

```math
N^{\mathrm{attempt}} \le |E^*|.
```
```math
N^{\mathrm{attempt}} = N^{\mathrm{success}} + N^{\mathrm{failed}} + N^{\mathrm{blocked}}.
```
```math
N^{\mathrm{attempt}} + N^{\mathrm{skipped}} = |E^*| \quad (\text{once every row reaches a terminal state}).
```

No automatic retry is authorized in any future collection run.

---

## 9. Stop Conditions for a Future Collection Run

**Branch-level stop** (an individual candidate's line of pursuit halts, others may continue):

- source identity or authority is ambiguous;
- exact methodological location cannot be recorded;
- access would require unknown credentials or circumvention;
- the source redirects into an unrelated full-text collection;
- a review-corpus search would begin;
- provider syntax would need experimentation rather than reading official documentation;
- a methodological claim conflicts with another admissible source (`C_abk=1`, per the gap plan's contradiction rule);
- a threshold would need to be invented to proceed.

**Run-level stop** (the entire future collection turn halts):

- the finite manifest would be exceeded;
- a source outside the 8-class authorized domain is proposed;
- SLR-DEC-06 would be adjudicated automatically as a side effect;
- SLR-DEC-07/08 work would begin;
- the decision ledger or any frozen protocol artifact would change;
- S1-B2 or Model 3B/Hawkes work would begin.

---

## 10. Authorization Readiness Gate

```text
A_D=1: evidence domain finite and explicit (Sec.2)
A_T=1: Track A / Track B separated (Sec.5)
A_M=1: finite candidate-manifest contract defined (Sec.7)
A_E=1: request/access accounting defined (Sec.8)
A_P=1: provenance and admissibility rules defined (Sec.4)
A_C=1: contradiction handling defined (inherited from gap plan Sec.13, restated Sec.9 above)
A_S=1: stop conditions complete (Sec.9)
A_B=1: epistemic boundaries preserved (Sec.2, Sec.5 — Track B not conflated with methodological validity)
A_0=1: zero collection/search/syntax-test/decision-mutation occurred this turn
```

```math
G_{06}^{\mathrm{authorization\_ready}} = \mathbf 1[A_D=A_T=A_M=A_E=A_P=A_C=A_S=A_B=A_0=1] = 1.
```

This gate assesses only whether a later manifest-preparation package *can* be frozen — it does not itself authorize evidence access.

---

## 11. Recommendation

```text
AUTHORIZE_MANIFEST_PREPARATION_ONLY
```

This permits, in a later and separate turn, only the preparation of a finite evidence-candidate manifest (per Sec.7's field contract). It does **not** permit accessing any evidence source, executing any search or query, testing or promoting any provider-syntax row, or adjudicating SLR-DEC-06.

---

## 12. Final Status

```text
SLR_DEC_06_MANIFEST_PREPARATION_AUTHORIZATION_RECOMMENDATION_READY_FOR_RESEARCHER_REVIEW
```
