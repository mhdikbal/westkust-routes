# SLR-DEC-05 — Researcher Adjudication Recommendation

**Status:** RECOMMENDATION ONLY. This document does not adjudicate SLR-DEC-05, does not modify `SLR_RESEARCHER_DECISION_LEDGER.csv`, and does not touch SLR-DEC-06, 07, or 08. It produces a recommendation for the researcher's own separate adjudication decision.

**Baseline:** `SLR_CANDIDATE_SOURCES_VERIFIED_READY_FOR_SLR_DEC_05_06_REVIEW`.

---

## 1. Scope

Review the completed source-verification evidence and produce exactly one recommended outcome for `SLR-DEC-05` (search-source set) only. No search, query, or retrieval is executed. No decision ledger entry changes.

---

## 2. Authoritative Baseline

```text
G_B^entry = 1
G_C^remediation = 1
G_source_verification = 1
G_5^decision_ready = 1
G_6^decision_ready = 0
SLR-DEC-05: PENDING_RESEARCHER_DECISION
SLR-DEC-06: PENDING_RESEARCHER_DECISION
SLR-DEC-07: PENDING_RESEARCHER_DECISION
SLR-DEC-08: PENDING_RESEARCHER_DECISION
```

All confirmed unchanged before this review began.

---

## 3. Decision Text Under Review

`SLR-DEC-05`: **search-source set** — which of the 13 candidate sources (`SLR_SEARCH_SOURCE_REGISTRY.csv`) are frozen into `S_A`, the actual set used for pilot and full-review search.

---

## 4. Evidence Domain

```math
S=\{s_1,\dots,s_{13}\},\qquad |S|=13.
```

```math
N_5^{\mathrm{direct}}=1,\quad N_5^{\mathrm{conditional}}=2,\quad N_5^{\mathrm{review}}=10,\quad N_5^{\mathrm{contradiction}}=0.
```
```math
1+2+10+0=13.
```

These counts describe provenance states, not votes.

---

## 5. Direct Support

**`SRC-12` (Google Scholar) — the sole `DIRECT_SUPPORT` source.**

Its verified role (`SCOPE_VERIFIED`, per `SLR_CANDIDATE_SOURCE_SCOPE_VERIFICATION_LEDGER.csv`) is **discovery-only, manual, never sole bibliographic authority** — this is not a general topical similarity; it is the exact, bounded operational rule this source would play in `S_A` if included, already confirmed via the S1-B1 provider-verification work (official ToS, robots.txt-enforced automation prohibition, both directly re-applicable here since the role is identical in both contexts). This satisfies §7's requirement that the direct source "support the exact proposed rule ... rather than merely the general topic."

---

## 6. Conditional Support

**`SRC-08` (WorldCat)** and **`SRC-13` (Crossref)** — both `SCOPE_PARTIALLY_VERIFIED`. Identity and authority are confirmed (official domain, terms, API documentation, all traceable to the S1-B1 provider audit), but the specific fit for SLR-scale bulk literature search was never tested — S1-B1 verified only single-item lookup behavior for both. Their support is real but bounded: they can qualify a scoped inclusion (e.g., "included pending confirmation of bulk-search behavior"), not an unconditional one.

---

## 7. Access-Blocked Sources

Ten sources (`SRC-01, 02, 03, 04, 05, 06, 07, 09, 10, 11`) carry `SOURCE_ACCESS_BLOCKED` — no captured verification evidence exists for any of them under this review's scope. Per instruction §6/§8, these ten **must not be treated as supporting, contradicting, or neutral evidence** for SLR-DEC-05. Their absence of evidence is a limitation to be disclosed, not a basis for either approving or rejecting their eventual inclusion.

---

## 8. Contradiction Review

```math
N_5^{\mathrm{contradiction}}=0.
```

No source's verified evidence affirmatively contradicts its proposed SLR use. This absence of contradiction does not itself prove correctness of any pending inclusion decision (per §8 epistemic boundary) — it is reported as a neutral finding, not as corroboration.

---

## 9. Provenance Review

Every substantive claim in this recommendation traces to an exact, already-frozen location:

```text
SRC-12: S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv (PROV-06 row); S1_B1_PROVIDER_ALLOWLIST_VERIFICATION_AUDIT.md Sec.13 (role rules)
SRC-08: S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv (PROV-04 row); same audit, Sec.9 (WorldCat API/human-catalogue split)
SRC-13: S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv (PROV-03 row); same audit
SRC-01..07,09,10,11: SLR_CANDIDATE_SOURCE_SCOPE_VERIFICATION_LEDGER.csv (all rows: verification_status=SOURCE_ACCESS_BLOCKED, exact_location=NONE_CAPTURED)
```

No substantive statement in this recommendation lacks a citable location.

---

## 10. Evidence-Strength Assessment

```math
\widehat P_{\mathrm{verified}}=\frac{1}{13}\approx0.077,\qquad \widehat P_{\mathrm{partial}}=\frac{2}{13}\approx0.154,\qquad \widehat P_{\mathrm{blocked}}=\frac{10}{13}\approx0.769.
```

**Decision-readiness does not mean evidence-completeness or strong corroboration.** `G_5^{decision\_ready}=1` means the evidence *package* is well-formed (provenance, boundaries, and contradiction status are all explicit), not that the underlying evidence is abundant. Roughly three-quarters of the candidate source set remains entirely unverified. This is the central fact the recommendation below is built around.

---

## 11. Adjudication Dimensions

```text
E_5 (>=1 directly applicable verified source exists):        1  (SRC-12)
P_5 (exact provenance recorded):                              1  (Sec.9)
B_5 (scope boundaries explicit):                              1  (Sec.5-7)
C_5 (contradictions recorded):                                1  (Sec.8)
N_5 (no arbitrary numerical input introduced):                1  (no threshold anywhere in this document)
L_5 (limitations from blocked/partial sources explicit):      1  (Sec.7, Sec.10)
I_5 (recommendation stays within SLR-DEC-05 scope):            1  (no statement touches DEC-06/07/08 substance)
```

---

## 12. Adjudication Gate

```math
G_5^{\mathrm{adjudication}}=\mathbf 1[E_5=P_5=B_5=C_5=N_5=L_5=I_5=1]=1.
```

A recommendation may be issued.

---

## 13. Recommended Outcome

```text
APPROVE_WITH_LIMITATIONS
```

**Precise scope of what is recommended for approval — nothing broader:**

1. **`SRC-12` (Google Scholar)** — approve for inclusion in `S_A`, strictly in its already-confirmed `DISCOVERY_ONLY` role (manual search, never sole authority for any included record). This is the only source whose direct evidence supports the exact rule being adjudicated.

2. **`SRC-08` (WorldCat)** and **`SRC-13` (Crossref)** — approve for **conditional** inclusion in `S_A`, restricted to their already-confirmed non-credentialed access pathways (WorldCat's public human-readable catalogue only; Crossref's public REST API for DOI-bearing works only), **on the explicit condition** that their suitability for SLR-scale bulk literature search is separately confirmed before either is actually used to execute a search string. Until that confirmation, both remain candidates-with-a-condition, not unconditionally frozen members of `S_A`.

3. **The remaining 10 sources** (`SRC-01, 02, 03, 04, 05, 06, 07, 09, 10, 11`) are **not** approved, conditionally or otherwise, by this recommendation. They are neither rejected — no evidence affirmatively fails them — nor approved, since no evidence exists at all. They should remain outside the frozen `S_A` until an independent, separately-authorized verification round captures evidence for each (which would then feed a future update to this same decision, not a new decision).

This is `APPROVE_WITH_LIMITATIONS` applied narrowly to exactly what the evidence supports — it is not a recommendation to approve "the 13-source candidate set" as a whole, and must not be read that way.

---

## 14. Limitations

- Only 1 of 13 candidate sources (`7.7%`) has full, direct, exactly-scoped evidentiary support.
- 2 of 13 (`15.4%`) have partial support (identity/authority confirmed, SLR-specific fit unconfirmed).
- 10 of 13 (`76.9%`) have zero captured evidence — this is the dominant fact about the evidence base, not a footnote.
- All evidence for the 3 non-blocked sources originates from a *different* use-case (S1-B1 single-item bibliographic lookup), not from SLR-scale literature-search verification specifically; only Google Scholar's role transfers without a use-case gap.
- This recommendation does not establish, and must not be read as establishing, that one verified source proves universal methodological truth, that the 13 candidates are independent evidence units, that the 10 blocked sources lend any support, that absence of contradiction proves correctness, or that this evidence validates any provider-specific query syntax.

---

## 15. SLR-DEC-06 Nonauthorization

```math
G_6^{\mathrm{decision\_ready}}=0.
```

No direct or conditional source support exists specifically for search-string design (`SLR_CANDIDATE_SOURCE_TO_DECISION_MATRIX.csv`: all `SLR-DEC-06` rows are `BACKGROUND_ONLY` or `NOT_APPLICABLE` — zero `DIRECT_SUPPORT`/`CONDITIONAL_SUPPORT`). SLR-DEC-06 is **not inferred from this SLR-DEC-05 recommendation** and is not touched here.

```text
SLR-DEC-06 = PENDING_RESEARCHER_DECISION
SLR-DEC-06 ADJUDICATION = NOT_AUTHORIZED
```

---

## 16. SLR-DEC-07/08 Nonauthorization

```text
SLR-DEC-07 mapping = 13/13 NOT_APPLICABLE (unchanged)
SLR-DEC-08 mapping = 13/13 NOT_APPLICABLE (unchanged)
```

No adjudication authorized or attempted for either.

---

## 17. Term and Syntax Immutability

```text
Ambiguous terms promoted:                0 (unchanged)
Excluded terms promoted:                 0 (unchanged)
Provider syntax VERIFIED:                0 (unchanged)
Provider syntax UNVERIFIED_NOT_EXECUTED: 42 (unchanged)
Provider syntax NOT_APPLICABLE:          36 (unchanged)
```

---

## 18. Ledger Immutability

```text
SLR_RESEARCHER_DECISION_LEDGER.csv: byte-unchanged, not opened for writing this turn
SLR-DEC-05: PENDING_RESEARCHER_DECISION (unchanged - this document is a recommendation, not an adjudication)
```

---

## 19. Stop Conditions

None triggered: source count remains 13; the 1/2/10/0 mapping reconciles; the direct-support source's provenance is exact; the direct-support source supports the exact rule (not merely the topic); no blocked source was used as substantive evidence; no conditional source was treated as direct support; no numerical threshold or vote was introduced; SLR-DEC-06/07/08 were not adjudicated; provider syntax was not promoted; no ambiguous/excluded term was promoted; zero search/query/retrieval occurred; the decision ledger did not change; no file was staged.

---

## 20. Final Status

```text
SLR_DEC_05_ADJUDICATION_RECOMMENDATION_READY_FOR_RESEARCHER_DECISION
```
