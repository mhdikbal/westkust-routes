# S1-B1 — Request Envelope and Query Order

**Status:** PLANNING ONLY. No query in this document was executed, tested, previewed, or encoded into a live URL. No network request was made. No target bibliographic content was searched.

**Authorization baseline:** `76928248500a23ac5c3b3ced0bc9014d7a2f7048`
**Workstream:** `PAINAN_INDRAPURA_STRATEGIC_HISTORY_LAB`
**Sprint / Batch:** `S1` / `S1-B1`

---

## 1. Operational Gate (unchanged by this document)

```math
G_{B1}^{\mathrm{authorize\_ready}}=1,\qquad A_{B1}^{\mathrm{exec}}=1.
```

```math
M_{B1}^{\mathrm{query}}=\mathbf 1(\text{query manifest and request envelope are frozen}).
```

During this planning turn: `M_{B1}^{query}=0`.

```math
G_{B1}^{\mathrm{run}}=G_{B1}^{\mathrm{authorize\_ready}}\cdot A_{B1}^{\mathrm{exec}}\cdot M_{B1}^{\mathrm{query}}=1\cdot1\cdot0=0.
```

S1-B1 is not executed by this document, regardless of manifest completeness.

---

## 2. Target and Provider Sets

```math
T_{B1}=\{t_1,\dots,t_{10}\},\qquad |T_{B1}|=10.
```
```math
P=\{p_1,\dots,p_6\},\qquad |P|=6.
```

Exact frozen IDs used, none added/removed/substituted: targets `ET-01, ET-03..ET-08, ET-10, ET-12, ET-13`; providers `PROV-01..PROV-06`.

---

## 3. Provider Roles and Restrictions (preserved)

```math
N_{\mathrm{confirmation}}=3,\qquad N_{\mathrm{corroboration}}=1,\qquad N_{\mathrm{discovery}}=2.
```

```text
OpenDOAR (PROV-05)         = DISCOVERY_ONLY
Google Scholar (PROV-06)   = DISCOVERY_ONLY
WorldCat (PROV-04) human-readable catalogue = CORROBORATION
WorldCat (PROV-04) credentialed API          = NOT_APPROVED_CREDENTIAL_BLOCKED (never planned; zero manifest rows use it)
```

No discovery-only provider is ever the sole basis for `IDENTITY_CONFIRMED` — see the identity gate, §9.

---

## 4. Query Unit Definition

```math
q=(t_i,p_j,s,a),
```

where `s` is one of the six allowed stages (`HARD_IDENTIFIER_LOOKUP, EXACT_TITLE_LOOKUP, TITLE_AUTHOR_LOOKUP, TITLE_YEAR_LOOKUP, DISCOVERY_ONLY_LOOKUP, CORROBORATION_LOOKUP`), no free-form stage. Every planned unit's `query_id` is deterministic: `Q-{target_id}-{provider_id}-{stage-abbreviation}-{attempt_index}`.

---

## 5. Why `HARD_IDENTIFIER_LOOKUP` Is Not the Entry Stage for Any Current Target

The preferred order (§9 of the governing instruction) places "hard identifier at confirmation provider" first. This applies only when a candidate hard-identifier *value* is already known and can be queried directly. For all ten S1-B1 targets, the hard-identifier *field* is known (`repository_or_catalogue_identity` for all; additionally `persistent_identifier` for ET-10) but its *value* is `UNRESOLVED` — that value is exactly what the lookup is meant to discover, not something already in hand to query by. Consequently, every target's manifest correctly begins at `EXACT_TITLE_LOOKUP` (the practical entry stage), with the hard-identifier field entering only as the confirmation *gate* (§9 below) once a candidate is found — not as a query stage in its own right. This is stated explicitly rather than silently defaulting, per the instruction's own conservatism principle.

---

## 6. Query Ordering, Per Target (least-expansive-applicable-path-first)

| target_id | ordered stages (provider) |
|---|---|
| ET-01 | EXACT_TITLE_LOOKUP (PROV-01) -> TITLE_YEAR_LOOKUP (PROV-01) -> CORROBORATION_LOOKUP (PROV-04) -> DISCOVERY_ONLY_LOOKUP (PROV-06) |
| ET-03..ET-08 (each) | EXACT_TITLE_LOOKUP (PROV-01) -> TITLE_AUTHOR_LOOKUP (PROV-01) -> CORROBORATION_LOOKUP (PROV-04) -> DISCOVERY_ONLY_LOOKUP (PROV-06) |
| ET-10 | EXACT_TITLE_LOOKUP (PROV-03) -> TITLE_AUTHOR_LOOKUP (PROV-03) -> DISCOVERY_ONLY_LOOKUP (PROV-05) -> CORROBORATION_LOOKUP (PROV-04) -> DISCOVERY_ONLY_LOOKUP (PROV-06) |
| ET-12 | EXACT_TITLE_LOOKUP (PROV-02) -> TITLE_AUTHOR_LOOKUP (PROV-02) -> CORROBORATION_LOOKUP (PROV-04) -> DISCOVERY_ONLY_LOOKUP (PROV-06) |
| ET-13 | EXACT_TITLE_LOOKUP (PROV-01) -> TITLE_AUTHOR_LOOKUP (PROV-01) -> CORROBORATION_LOOKUP (PROV-04) -> DISCOVERY_ONLY_LOOKUP (PROV-06) |

Provider assignment rationale (no fabricated scope claim; grounded in each provider's documented metadata scope from `S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv`):

- `PROV-01` (Nationaal Archief, Dutch national archives) is the confirmation-tier provider for the Dutch/VOC-origin targets (ET-01, ET-03..ET-08 the Corpus Diplomaticum volumes, and ET-13 Vogel).
- `PROV-02` (The National Archives, UK) is the confirmation-tier provider for the English/EIC-origin target (ET-12, Fort York/Batang Capas material).
- `PROV-03` (Crossref) is the confirmation-tier provider for the one modern, DOI-eligible target (ET-10, the PhD thesis) — the only target whose `persistent_identifier` field is applicable, per `S1_B1_BIBLIOGRAPHIC_FIELD_ROLE_MATRIX.csv`.
- `PROV-05` (OpenDOAR) is applicable, discovery-only, solely to ET-10 — a repository directory is relevant only to a modern deposited item, not a 17th/18th-century archival source.
- `PROV-04` (WorldCat, human-readable catalogue only) and `PROV-06` (Google Scholar, manual discovery only) are broadly applicable corroboration/discovery fallbacks for all ten targets, always placed last in each target's escalation order, consistent with §9 ("discovery-only provider only if no eligible candidate has been found").

### 6.1 Escalation indicator

```math
e_{ir}=\mathbf 1(\text{stage }r\text{ did not yield a sufficient terminal result}).
```

Stage `r+1` may be attempted only if `e_{ir}=1`. This rule is encoded in the manifest's `predecessor_query_id` and `escalation_condition` columns for every stage after the first — it is not evaluated in this planning turn (no stage has been executed).

---

## 7. Target-Provider Applicability Summary

```text
70 total manifest rows = 41 PLANNED query units + 29 NOT_APPLICABLE_TO_TARGET_CLASS pair records
```

Every one of the 60 target x provider pairs is accounted for exactly once at the pair level (either as one or more PLANNED query-unit rows, or as exactly one NOT_APPLICABLE_TO_TARGET_CLASS row) — the manifest was not defaulted to all `10 x 6 = 60` query executions; only applicable, ordered query units were included as real planned queries.

Non-applicable pairs and reasons (all in `S1_B1_TARGET_PROVIDER_QUERY_MANIFEST.csv`, `notes` column):

```text
PROV-01 not applicable to: ET-10, ET-12  (Dutch/VOC archival scope does not match English/EIC or modern-academic origin)
PROV-02 not applicable to: ET-01, ET-03..ET-08, ET-10, ET-13  (English/EIC archival scope does not match Dutch/VOC or modern-academic origin)
PROV-03 not applicable to: ET-01, ET-03..ET-08, ET-12, ET-13  (persistent_identifier is NOT_APPLICABLE_TO_CLASS for these targets per the field-role matrix)
PROV-05 not applicable to: ET-01, ET-03..ET-08, ET-12, ET-13  (repository-directory scope does not match archival-source targets)
```

`PROV-04` and `PROV-06` are `PLANNED` for all ten targets (no `NOT_APPLICABLE` rows for either).

---

## 8. Planned Request Counts

```math
R_{ij}^{\mathrm{plan}}=\sum_s\sum_a \mathbf 1(q_{ijsa}\text{ is planned}).
```

Per-provider totals (`R_j^{plan} = sum over i of R_ij^plan`):

```text
PROV-01: 16   (8 targets x 2 stages each: ET-01, ET-03..ET-08, ET-13)
PROV-02: 2    (1 target x 2 stages: ET-12)
PROV-03: 2    (1 target x 2 stages: ET-10)
PROV-04: 10   (10 targets x 1 corroboration stage each)
PROV-05: 1    (1 target x 1 discovery stage: ET-10)
PROV-06: 10   (10 targets x 1 discovery stage each)
```

Batch maximum planned requests (conditional ceiling, not a guaranteed actual count):

```math
R_{\max}^{\mathrm{plan}}=\sum_{i=1}^{10}\sum_{j=1}^{6}R_{ij}^{\mathrm{plan}}=16+2+2+10+1+10=41.
```

This is a maximum conditional envelope. The actual number of requests made during execution will very likely be lower, since escalation stops as soon as a target reaches a sufficient terminal result (e.g. `IDENTITY_CONFIRMED` at the first stage means the later stages for that target are never attempted). `41 != 10 x 6 = 60` — the manifest was not defaulted to the full cross-product.

---

## 9. Provider Request Limits

Preserved exactly, no numerical rate invented:

```text
PROV-02: maximum 3000 requests/day, maximum 1 request/second (official, documented)
PROV-03: maximum 50 requests/second (official, documented)
PROV-01, PROV-04, PROV-05: NO_AUTOMATED_REQUEST_RATE_APPLICABLE (manual human-readable catalogue access only)
PROV-06: NO_AUTOMATED_REQUEST_RATE_APPLICABLE (manual discovery search only; robots.txt disallows automation)
```

For a provider with a documented count limit `L_j`: `R_j^{plan} <= L_j`.

```text
PROV-02: R_j^plan = 2 <= L_j = 3000/day  -> satisfied, trivially
PROV-03: R_j^plan = 2 <= 50/sec (rate, not count) -> satisfied, trivially; no count ceiling documented for Crossref, only a rate ceiling
```

No manual pathway (PROV-01, PROV-04, PROV-05, PROV-06) is converted into automated scraping — all four remain explicitly human-driven with no automated request rate at all.

---

## 10. Request Envelope Gate

For each used provider `p_j`, evaluate `E_j^{scope}, E_j^{method}, E_j^{count}, E_j^{rate}, E_j^{credential}, E_j^{role}`:

| provider | scope | method | count | rate | credential | role | `G_j^envelope` |
|---|---|---|---|---|---|---|---|
| PROV-01 | 1 | 1 (human catalogue) | 1 (no automated count applicable) | 1 (N/A) | 1 (none required) | 1 (confirmation, matches role) | 1 |
| PROV-02 | 1 | 1 (official API) | 1 (2 <= 3000/day) | 1 (well under 1/sec used serially) | 1 (none required) | 1 (confirmation, matches role) | 1 |
| PROV-03 | 1 | 1 (official API) | 1 (no count ceiling; only rate) | 1 (2 requests, well under 50/sec) | 1 (none required) | 1 (confirmation, matches role) | 1 |
| PROV-04 | 1 | 1 (human catalogue only, never API) | 1 (N/A) | 1 (N/A) | 1 (credentialed API excluded entirely, no blocked pathway planned) | 1 (corroboration only, never confirmation) | 1 |
| PROV-05 | 1 | 1 (human catalogue) | 1 (N/A) | 1 (N/A) | 1 (none required) | 1 (discovery only, never confirmation) | 1 |
| PROV-06 | 1 | 1 (manual discovery only) | 1 (N/A) | 1 (N/A) | 1 (none required) | 1 (discovery only, never confirmation) | 1 |

```math
G_{B1}^{\mathrm{envelope}}=\prod_{j\in P_{\mathrm{used}}}G_j^{\mathrm{envelope}}=1.
```

All six used providers pass the envelope gate. Not `S1_B1_REQUEST_ENVELOPE_REQUIRES_REVIEW`.

---

## 11. Request Accounting Schema (for future execution, not evaluated now)

```math
R^{\mathrm{attempt}}=R^{\mathrm{success}}+R^{\mathrm{failed}}+R^{\mathrm{blocked}},\qquad R^{\mathrm{skipped}}\notin R^{\mathrm{attempt}}.
```

Before execution, all counters are required to be:

```math
R^{\mathrm{attempt}}=R^{\mathrm{success}}=R^{\mathrm{failed}}=R^{\mathrm{blocked}}=0.
```

Confirmed: no query has been executed by this planning turn.

---

## 12. Retry Rule

```math
A_q^{\max} \text{ is not assigned a positive value in this document.}
```

```text
NO_AUTOMATIC_RETRY
```

A failed request may be reconsidered only after review, using the same target, provider, query stage, and a new logged attempt index — it must never silently change query terms.

---

## 13. Candidate Record Output Contract (reference only, not populated)

```text
target_id, candidate_id, provider_id, provider_role, query_id, record_url, record_identifier,
observed_metadata_fields, hard_identifier_status, required_core_completeness, required_core_agreement,
provider_conflict_status, candidate_eligibility, final_target_status, notes
```

No source text, quotations, OCR, images, PDFs, DOCX content, or downloaded files may ever enter this ledger.

---

## 14. Identity Gate (reference only, not evaluated)

```math
E_{ij}=\mathbf 1\left[C_{ij}=0\land K_{ij}^{\mathrm{req}}=1\land M_{ij}^{\mathrm{req}}=1\right],\qquad Z_i=\sum_{j\in J_i}E_{ij}.
```

Identity may be confirmed only if `Z_i=1` and no provider hard-field conflict exists. Each manifest row's `identity_rule_reference` column points to the authorization decision's full gate definitions (§12-15 of `S1_B1_BIBLIOGRAPHIC_LOOKUP_EXECUTION_AUTHORIZATION_DECISION.md`) rather than re-evaluating them here.

---

## 15. Manifest Completeness Gate

`M_T` (all ten targets appear) = 1; `M_P` (only six frozen providers appear) = 1; `M_A` (all 60 target-provider applicability decisions recorded) = 1; `M_Q` (all planned query units have unique IDs and deterministic templates) = 1; `M_O` (ordering and escalation explicit) = 1; `M_E` (provider request envelopes pass) = 1; `M_C` (candidate-output schema complete) = 1; `M_I` (identity-rule references complete) = 1; `M_S` (stop conditions explicit) = 1; `M_0` (zero query/network/retrieval/content/claim/registry/downstream-batch occurred) = 1.

```math
G_{B1}^{\mathrm{manifest}}=\mathbf 1[M_T=M_P=M_A=M_Q=M_O=M_E=M_C=M_I=M_S=M_0=1]=1.
```

```text
S1_B1_QUERY_MANIFEST_READY_FOR_RESEARCHER_REVIEW
```

This does **not** set `M_{B1}^{query}=1`. That occurs only after a separate freeze and synchronization.

---

## 16. Stop Conditions (none triggered)

```text
target/provider count wrong:                  NO (10/6 exact)
target or provider invented:                   NO
blocked provider pathway planned:               NO (WorldCat API never used)
discovery-only provider given confirmation role: NO
applicability unjustified:                      NO (every applicable/non-applicable decision has a documented reason)
query requiring retrieval/content access:        NO
invented metadata in query terms:                NO (query_field_references cite only frozen field names, no values fabricated)
query URL executed/tested:                      NO
network request occurred:                       NO
request rate invented:                          NO
automatic retry count invented:                  NO
manifest ID duplicated:                          NO (70/70 unique)
envelope accounting unreconciled:                NO
registry changed:                                NO
claim/promotion created:                         NO
S1-B2 through S1-B5 begun:                       NO
file staged:                                     NO
```

---

## 17. ET-10 Escalation Order Correction (appended additively)

**Provenance:** appended after §1-16 above (unmodified) following a separate row-by-row freeze audit that found a structural defect in the ET-10 chain, and a subsequent targeted correction turn. No artifact was staged or committed at the point the defect was found — the freeze was correctly withheld pending correction.

**Defect found:** the original ET-10 chain placed the OpenDOAR discovery-only stage (`Q-ET-10-PROV-05-DOL-01`) before the WorldCat corroboration stage (`Q-ET-10-PROV-04-COL-01`), producing role sequence `CONFIRMATION -> CONFIRMATION -> DISCOVERY_ONLY -> CORROBORATION -> DISCOVERY_ONLY` with a prohibited `DISCOVERY_ONLY -> CORROBORATION` transition.

**Correction applied:** the WorldCat corroboration stage was moved before both discovery-only stages. Corrected chain:

```text
Q-ET-10-PROV-03-ETL-01 (CONFIRMATION)
 -> Q-ET-10-PROV-03-TAL-02 (CONFIRMATION)
   -> Q-ET-10-PROV-04-COL-01 (CORROBORATION)
     -> Q-ET-10-PROV-05-DOL-01 (DISCOVERY_ONLY)
       -> Q-ET-10-PROV-06-DOL-01 (DISCOVERY_ONLY)
```

Role sequence: `1,1,2,3,3` — nondecreasing, `V_ET-10^order=0`; both discovery-only stages form a terminal suffix, `V_ET-10^discovery=0`.

Only `predecessor_query_id` and `escalation_condition` were changed, and only for these three query IDs: `Q-ET-10-PROV-04-COL-01`, `Q-ET-10-PROV-05-DOL-01`, `Q-ET-10-PROV-06-DOL-01`. All query IDs, targets, providers, provider roles, query stages, attempt indices, applicability statuses, query field references, query templates, access methods, request counts, rate statuses, credential statuses, candidate-schema versions, and identity-rule references remained unchanged. The complete 70-row audit was rerun after correction and all gates passed (§18 of `S1_B1_QUERY_MANIFEST_READINESS_AUDIT.md`). This correction does not execute S1-B1, and does not alter any of the batch-level invariants (`|Q|=70`, `|Q^plan|=41`, `|U^NA|=29`, `|U^A|=31`, additional stages=10, provider totals=41, stage totals=41).
