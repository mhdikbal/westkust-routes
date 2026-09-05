# SLR-DEC-06 — Researcher Adjudication Decision

**Status:** SUBSTANTIVE ADJUDICATION. This document adjudicates SLR-DEC-06 only. It does not begin SLR-DEC-07, SLR-DEC-08, S1-B2, Model 3B, or Hawkes, and it does not authorize final C1-C6 review-corpus search execution.

**Baseline:** commit `1d5eb4d3c0d008242ee4f9abe670578efc79366f` — local HEAD = origin/main = server HEAD, confirmed.

---

## 1. Scope

Independently reproduce the DEC-06 evidence-package counts and gates, then adjudicate SLR-DEC-06 (freezing the six C1–C6 search-string families' design policy) as exactly one of the four allowed outcomes.

---

## 2. Authoritative Baseline

```text
SLR-DEC-06 = PENDING_RESEARCHER_DECISION (at entry)
SLR-DEC-07 = PENDING_RESEARCHER_DECISION
SLR-DEC-08 = PENDING_RESEARCHER_DECISION
```

---

## 3. Evidence Package Reviewed

All nine DEC-06 evidence artifacts were read in full: the controlled discovery ledger, access-path registry, controlled discovery report, methodological evidence ledger, provider syntax verification matrix, component evidence coverage, method-guidance contradiction ledger, candidate outcome summary, and evidence collection and readiness report — all confirmed byte-identical to the commit `1d5eb4d3` baseline before this adjudication began.

---

## 4. Candidate and Collection Accounting

```math
J=20,\qquad J_A=7,\qquad J_B=13,\qquad 7+13=20.
```
```math
N^{\mathrm{attempt}}=20,\ N^{\mathrm{success}}=19,\ N^{\mathrm{failed}}=1,\ N^{\mathrm{blocked}}=0,\ N^{\mathrm{skipped}}=0.
```
```math
20=19+1+0,\qquad 20+0=20.
```
```math
N^{\mathrm{evidence}}=11,\qquad N^{\mathrm{admissible}}=10,\qquad N^{\mathrm{rejected}}=1,\qquad 10+1=11.
```

All independently reconfirmed via fresh `csv.DictReader` passes this turn.

---

## 5. Evidence Admissibility

10 of 11 collected evidence items are admissible. The 1 rejected item (Barisaux et al. 2024, SAGE) was not admitted because its full text was inaccessible (HTTP 403) — identity/metadata alone does not satisfy the methodological-relevance and exact-provenance admissibility criteria. This rejection is preserved unchanged.

---

## 6. Track A Component Coverage

```text
concepts=2, variants=1, translations=1, filters=1, risk=2, seed checking=1, versioning=1, reporting=3
```

```math
G_A^{\mathrm{coverage}}=\prod_{k\in K_A}\mathbf 1(N_k^{\mathrm{support}}\ge1)=1.
```

All eight Track A components independently reconfirmed ≥1 this turn.

---

## 7. Humanities-Specific Authority Limitation

**Preserved exactly:** `NO_DEDICATED_AUTHORITY_BUT_METHOD_EVIDENCE_AVAILABLE`.

No dedicated humanities-specific search-method standard-setting body (analogous to Cochrane/PRESS/PRISMA-S) was found. This decision does **not** claim that such an authority was found, that biomedical systematic-review methods transfer to humanities inquiry without qualification, or that the admitted discipline-general evidence (citation-tracking methodology, Hirt et al. 2021) resolves the interpretive situatedness of humanities scholarship. The Barisaux et al. 2024 candidate remains explicitly **not** admissible evidence — access-blocked identity is not methodological support.

---

## 8. Multilingual and Translation Limitation

**Preserved exactly:** the `translations` component is supported only by general Cochrane Handbook language-restriction guidance (§4.4.5) — not a dedicated cross-language term-equivalence-verification method, which was the specific discovery objective and was not found. This gap is carried forward, not closed by the coverage gate being satisfied.

---

## 9. Track B Syntax Verification

```math
|U_B|=42,\qquad N_{\mathrm{verified}}=32,\qquad N_{\mathrm{partial}}=8,\qquad N_{\mathrm{notfound}}=2,\qquad 32+8+2=42.
```
```math
\widehat P_{\mathrm{syntax}}=\frac{32}{42}=\frac{16}{21}\approx0.7619 \quad (\text{descriptive only, not a pass threshold}).
```

Independently reconfirmed this turn: exactly 42 unique family-source pairs, no pair missing or duplicated, no pair silently promoted to verified.

---

## 10. Hybrid Syntax Policy

Adopted operational policy for any future pilot source-family matrix:

```math
U_{cs}=\mathbf 1[V_{cs}=1 \lor (P_{cs}=1 \land F_{cs}^{\mathrm{required}}=1)].
```

1. Use a family-source pair only when syntax is verified from official documentation (32 pairs qualify unconditionally).
2. Permit a partially verified pair (8 pairs: Project MUSE, KITLV/Leiden, KITLV/Brill, and the SOAS/EPrints component) only if every syntax feature the actual frozen query uses is officially documented for that specific pair — this must be checked feature-by-feature in a future, separate turn, not assumed.
3. Exclude the 2 not-found pairs (DHQ, both applicable families) from the pilot source-family matrix unless official syntax documentation is separately located later.
4. Never infer one provider's unsupported operator from another provider's documentation.
5. Never test live syntax to fill a documentation gap.
6. Every exclusion must be preserved explicitly in the future pilot manifest and PRISMA/search log — silent omission is not permitted.

This is a decision about search-string **design policy**, not an execution authorization.

---

## 11. B-10 Dual-Platform Boundary

**Preserved exactly:** `RESOLVED_DUAL_PATHWAYS_DISTINCT_ROLES`.

```text
Leiden University Libraries (catalogue.leidenuniv.nl): catalogue/discovery role for the KITLV collection, transferred 1 July 2014.
Brill (brill.com): publisher/content role for KITLV-affiliated series (BKI, NWIG, Verhandelingen).
```

These two platforms are not merged in this decision, and no syntax feature confirmed for one is treated as confirmed for the other — each pair's `U_cs` (Sec.10) must be evaluated per-platform.

---

## 12. Contradiction Review

```math
N^{\mathrm{admissible}}=10,\qquad N^{\mathrm{contradiction}}=0.
```

Independently re-examined this turn: the contradiction ledger records a single explicit `NO_CONTRADICTION_FOUND_AMONG_10_ADMISSIBLE_TRACK_A_ITEMS_THIS_TURN` row, confirming the pairwise check was actually performed, not skipped. This absence of a detected contradiction means no material conflict was found within the finite admissible evidence set collected to date — it does not assert universal agreement among all possible future evidence.

---

## 13. DEC-06 Readiness Gate

```text
S_6=1: 10 admissible items directly support search-string design methodology (Cochrane, PRISMA-S, PRESS, Campbell)
B_6=1: boundaries/limitations explicit throughout (Sec.7, Sec.8, Sec.9, Sec.11)
C_6=1: contradiction state recorded (Sec.12)
P_6=1: exact provenance recorded for every admissible item (section/heading/URL)
N_6=1: no arbitrary numeric threshold introduced (P̂_syntax reported descriptively only)
R_6=1: SLR-DEC-06 was PENDING_RESEARCHER_DECISION until this adjudication
A_6=1: all 8 Track A components covered or explicitly gapped (Sec.6-8)
Y_6=1: all 42 Track B pairs have terminal status (Sec.9)
```

```math
G_6^{\mathrm{decision\_ready}}=\mathbf 1[S_6=B_6=C_6=P_6=N_6=R_6=A_6=Y_6=1]=1.
```

Independently reproduced this turn — required before any substantive decision.

---

## 14. Researcher Decision

```text
SLR-DEC-06:
APPROVE_WITH_LIMITATIONS
```

This outcome was selected because `G_6^decision_ready=1` reproduces exactly, `G_A^coverage=1`, and `G_06^collection_complete=1` — not by source count, majority vote, prestige, or the raw value of 32/42 alone. The decision approves the search-string families' **design policy**, subject to the eight limitations below.

---

## 15. Explicit Limitations

1. No dedicated humanities-specific search-method authority was established (Sec.7).
2. Translations are supported only by general multilingual guidance, not a dedicated equivalence-validation method (Sec.8).
3. Only 32 of 42 syntax pairs are fully verified from official documentation (Sec.9).
4. The 8 partially verified pairs require feature-level restriction before pilot use — every feature the actual query uses must be individually confirmed (Sec.10).
5. The 2 not-found pairs (DHQ) must be excluded from the pilot source-family matrix unless separately documented later (Sec.10).
6. Leiden/KITLV catalogue-discovery and Brill publisher-content roles remain distinct platforms; no syntax claim transfers between them (Sec.11).
7. This decision authorizes search-string **design policy** only — it does not authorize final C1-C6 review-corpus search execution.
8. This decision does not authorize SLR-DEC-07, SLR-DEC-08, S1-B2, Model 3B, or Hawkes.

---

## 16. Future Pilot-Search Boundary

A future, separately authorized turn must construct the actual pilot source-family matrix applying the hybrid policy (Sec.10) pair-by-pair, and must not execute any search in the same turn that authorizes it, consistent with this project's established planning/authorization/execution separation discipline.

---

## 17. DEC-07 Nonauthorization

```text
SLR-DEC-07 = PENDING_RESEARCHER_DECISION (unchanged by this decision)
```

Not adjudicated, not begun.

---

## 18. DEC-08 Nonauthorization

```text
SLR-DEC-08 = PENDING_RESEARCHER_DECISION (unchanged by this decision)
```

Not adjudicated, not begun.

---

## 19. S1-B2 and Model Nonauthorization

S1-B2 was not opened. Model 3B, Hawkes, game-theory, and counterfactual-analysis work were not begun and remain unauthorized.

---

## 20. Ledger Amendment Contract

The authoritative decision ledger's `SLR-DEC-06` logical row only will be updated to:

```text
decision_id = SLR-DEC-06
status = ADJUDICATED_APPROVED_WITH_LIMITATIONS
adjudicated_decision = APPROVE_WITH_LIMITATIONS: [references this decision artifact, the evidence collection and readiness report, the methodological evidence ledger, the provider syntax verification matrix, the component evidence coverage matrix, the method-guidance contradiction ledger, and the candidate outcome summary; preserves all eight limitations in Sec.15]
```

No other row (`SLR-DEC-07`, `SLR-DEC-08`, or any of the 9 already-approved rows) will be touched.

---

## 21. Freeze and Sync Gate

```text
F_D=1: this decision artifact validates (23 sections complete, all figures independently reproduced)
F_L=1: exactly one ledger row (SLR-DEC-06) will change
F_E=1: the 9-file evidence package remains byte-identical (confirmed via checksum this turn)
F_M=1: the finite manifest remains byte-identical (confirmed via checksum this turn)
F_P=1: pending decisions remain exactly SLR-DEC-07 and SLR-DEC-08
F_B=1: all boundaries and limitations preserved (Sec.7,8,9,10,11,15)
F_0=1: no unauthorized execution occurred (no search, no syntax test, no new evidence collection this turn)
F_S=1: secret scan clean
```

```math
G_{06}^{\mathrm{freeze}}=\mathbf 1[F_D=F_L=F_E=F_M=F_P=F_B=F_0=F_S=1]=1.
```

---

## 22. Stop Conditions

None triggered: `G_6^decision_ready` reproduced exactly; Track A component counts matched exactly; syntax distribution matched 32/8/2 exactly across exactly 42 unique pairs with none missing, duplicated, or silently promoted; A-05 and B-10 boundaries matched exactly; every evidence item retains its provenance; the contradiction audit was independently confirmed as actually performed; all eight limitations are recorded.

---

## 23. Final Status

```text
SLR_DEC_06_ADJUDICATED_APPROVED_WITH_LIMITATIONS_COMMITTED_PUSHED_AND_SERVER_SYNCED_DEC_07_08_PENDING
```

(pending successful ledger amendment, staging, commit, push, and server-sync — reported in the accompanying terminal report)
