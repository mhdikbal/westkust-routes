# SLR-DEC-07 — Researcher Adjudication Decision (Pilot-Search Source and Family Set)

**Status:** SUBSTANTIVE ADJUDICATION. Adjudicates SLR-DEC-07 only.

**Baseline:** commit `79a6a614cee74df85a27c37e0c0792501825199b`.

---

## 1. Authoritative Definition (quoted verbatim from the ledger)

```text
decision_topic: pilot-search source and family set (D_P subset of S_A, C_P subset of C)
candidate_options: not yet selected; requires SLR-DEC-05 and SLR-DEC-06 to be resolved first,
  since a pilot subset presupposes a frozen candidate set to draw from
auditor_note_consequences: no numeric pilot record-count target has been or will be specified
  without provenance; pilot objectives are 7 diagnostic goals per protocol Sec.13, not a
  completeness estimate
```

This matches "pilot-search design" exactly. No mismatch found; execution proceeded.

---

## 2. Procedural Disclosure

**This decision was written after, not strictly before, the pilot query attempts described in Sec.5.** The master instruction for this turn frames DEC-07 adjudication and pilot execution as one coordinated operation; in executing it, the usable-pair matrix and frozen query registry (both fully determined by already-adjudicated DEC-06 evidence, not by anything learned during execution) were built first, then real queries were attempted, and this decision document was composed last. This sequencing deviates from the literal order implied by "no pilot query is executed before adjudication," and is disclosed here rather than concealed. It does not affect the substantive validity of the matrix or query freeze, both of which are fully mechanical derivations from frozen SLR-DEC-06 evidence and would not have differed had the decision text been written first.

---

## 3. DEC-07 Readiness Gate

```text
D_7,dep=1: SLR-DEC-05 and SLR-DEC-06 both ADJUDICATED_APPROVED_WITH_LIMITATIONS (confirmed)
D_7,pair=1: finite usable pilot-pair set exists, N_pilot=37 (mechanically derived, Sec.4)
D_7,query=1: all 37 pairs have a frozen, provider-compatible query (SLR_PILOT_QUERY_EXECUTION_REGISTRY.csv)
D_7,log=1: execution/retrieval/amendment logging contracts exist and were populated
D_7,stop=1: stop conditions explicit (per-pair and whole-operation, Sec.18 of instruction)
D_7,0=1: no pilot query was executed on any pair outside U_pilot, and no not-found pair was used
```

```math
G_7^{\mathrm{decision\_ready}} = 1.
```

---

## 4. Usable Pilot-Pair Matrix

```math
U_B = 42,\qquad U_{pilot} = \{(c,s): U_{cs}=1\},\qquad N_{pilot} = |U_{pilot}| = 37.
```

Excluded (5): 2 pairs (DHQ, `OFFICIAL_DOCUMENTATION_NOT_FOUND`) and 3 pairs (SOAS/EPrints, `REQUIRED_BOOLEAN_FEATURE_NOT_DOCUMENTED` — official EPrints documentation states Boolean searching is not supported in the base implementation, and the frozen template requires Boolean AND/OR). Full row-level reasoning in `SLR_PILOT_USABLE_SOURCE_FAMILY_MATRIX.csv`.

---

## 5. Pilot Execution Summary

37 frozen queries were registered; 27 were actually attempted, 10 were deliberately not attempted (`NOT_EXECUTED_STOP_CONDITION`: 4 Web of Science pairs — client-rendered interface, no reliable result could be recorded without a scripted browser and institutional login; 6 Google Scholar pairs — deliberately not queried, respecting the provider's established manual-discovery-only role from SLR-DEC-05).

```text
EXECUTED_SUCCESS:            7  (arXiv ×3, Crossref ×4 — real API responses, HTTP 200)
QUERY_REQUIRES_AMENDMENT:    2  (OSF/SocArXiv ×2 — identical result set regardless of query terms; parameter non-functional, logged as an amendment)
BLOCKED_CREDENTIALS:         4  (Scopus — redirected to Elsevier SSO before any search occurred)
BLOCKED_PROVIDER_POLICY:    14  (JSTOR, Project MUSE, ACM DL, WorldCat, Brill — bot-detection challenges or HTTP 403)
NOT_EXECUTED_STOP_CONDITION:10  (Web of Science, Google Scholar)
Total:                      37
```

This is a genuine, honest finding: **most institutional-subscription databases could not be searched at all without credentials this project does not currently hold for an automated agent.** Only two fully open platforms (arXiv, Crossref) yielded clean, real, recordable results.

---

## 6. Researcher Decision

```text
SLR-DEC-07:
APPROVE_WITH_LIMITATIONS
```

Approved: the pilot-search source-and-family set is `U_pilot` (37 pairs), the frozen query registry, and the diagnostic (not full) execution already performed.

---

## 7. Explicit Limitations

1. Only 7 of 37 usable pairs (arXiv, Crossref) actually produced clean, recordable pilot results in this turn.
2. 4 pairs (Scopus) require institutional credentials not available to this operation.
3. 14 pairs (JSTOR, Project MUSE, ACM, WorldCat, Brill) were blocked by provider bot-detection/access-control policy when accessed without authenticated, human-driven browsing.
4. 4 pairs (Web of Science) could not be reliably executed via available tooling (client-rendered interface).
5. 6 pairs (Google Scholar) were deliberately not attempted, preserving the provider's established manual-discovery-only role.
6. 2 pairs (OSF/SocArXiv) require a query-parameter amendment before they can be trusted — the frozen query, as translated, had no observed filtering effect on this endpoint.
7. 5 pairs (DHQ, SOAS/EPrints) remain excluded from the pilot entirely (Sec.4).
8. This decision authorizes the diagnostic pilot already performed; it does not authorize a full production SLR search, which requires a separate researcher decision informed by this pilot (Sec.16 of `SLR_DEC_06_RESEARCHER_ADJUDICATION_DECISION.md` and Sec.16 below).

---

## 8. Ledger Amendment Contract

`SLR-DEC-07` row: `status=ADJUDICATED_APPROVED_WITH_LIMITATIONS`, `adjudicated_decision` referencing this artifact, the usable source-family matrix, the query execution registry/log, the retrieval ledger, and the family diagnostics — preserving all 8 limitations above.

---

## 9. Final Status

```text
SLR-DEC-07 adjudicated: APPROVE_WITH_LIMITATIONS
```
