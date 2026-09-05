# S1-B1 — Bibliographic Identity Lookup Execution Authorization Decision

**Status:** AUTHORIZATION DECISION RECORD ONLY. This document authorizes the scope of a future S1-B1 execution turn. It does not itself execute a lookup, make a network request, access source content, retrieve a source, create a claim, promote a source class, or modify any registry.

**Planning baseline:** `25fb7a1b02e029e58231eccb178c926fc170772a`
**Workstream:** `PAINAN_INDRAPURA_STRATEGIC_HISTORY_LAB`
**Sprint / Batch:** `S1` / `S1-B1`

---

## 1. Scope

Record one versioned authorization for the future execution of S1-B1 (controlled bibliographic metadata lookup) covering: permitted scope, request accounting, provider constraints, target-level matching rules, denominators, success gates, stop conditions, and epistemic boundaries. No query is executed by this document.

---

## 2. Authoritative Baseline

Verified before authoring this decision:

```text
local HEAD  = 25fb7a1b02e029e58231eccb178c926fc170772a
origin/main = 25fb7a1b02e029e58231eccb178c926fc170772a
server HEAD = 25fb7a1b02e029e58231eccb178c926fc170772a
```

All eight frozen S1-B1 planning artifacts read from this commit:

```text
S1_B1_BIBLIOGRAPHIC_IDENTITY_REVIEW_PLAN.md
S1_B1_BIBLIOGRAPHIC_IDENTITY_TARGET_MATRIX.csv
S1_B1_AUTHORIZATION_READINESS_AUDIT.md
S1_B1_RESEARCHER_DECISION_ADJUDICATION.md
S1_B1_BIBLIOGRAPHIC_FIELD_ROLE_MATRIX.csv
S1_B1_REQUIRED_CORE_FIELD_ADJUDICATION.md
S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv
S1_B1_PROVIDER_ALLOWLIST_VERIFICATION_AUDIT.md
```

Required state, confirmed:

```text
S1-B0 = COMPLETE_WITH_PATH_DOMAIN_CLARIFICATION
S1-B1 = PLANNED_ONLY / NOT_AUTHORIZED
D_R = 1
D_I = 1
G_B1^authorize_ready = 1
S1-B2 through S1-B5 = PLANNED_ONLY / NOT_AUTHORIZED
```

All matched; authorization decision proceeded.

---

## 3. Researcher Authorization

```text
S1-B1:                    AUTHORIZED_FOR_FUTURE_CONTROLLED_BIBLIOGRAPHIC_METADATA_LOOKUP
EXECUTION STATUS:         NOT_STARTED
TARGETS:                  10 frozen targets
PROVIDERS:                6 frozen providers
SOURCE RETRIEVAL:         NOT_AUTHORIZED
SOURCE-CONTENT ACCESS:    NOT_AUTHORIZED
CLAIM CREATION:           NOT_AUTHORIZED
SOURCE-CLASS PROMOTION:   NOT_AUTHORIZED
REGISTRY MODIFICATION:    NOT_AUTHORIZED
S1-B2 THROUGH S1-B5:      NOT_AUTHORIZED
```

This authorization becomes operational only after this decision artifact is committed, pushed, and server-synced in separate turns.

---

## 4. Readiness Versus Execution Authorization

```math
G_{B1}^{\mathrm{authorize\_ready}}=\mathbf 1\left[G_{B1}^{\mathrm{decision}}=1\land D_R=1\land D_I=1\right]=1.
```

```math
A_{B1}^{\mathrm{exec}}=\mathbf 1(\text{this authorization artifact is frozen and synchronized}).
```

During this local decision-recording turn:

```math
A_{B1}^{\mathrm{exec}}=0.
```

After a later successful commit, push, and server sync (separate turns), `A_{B1}^{\mathrm{exec}}` becomes `1`. Operational execution gate:

```math
G_{B1}^{\mathrm{exec}}=G_{B1}^{\mathrm{authorize\_ready}}\cdot A_{B1}^{\mathrm{exec}}.
```

Currently:

```math
G_{B1}^{\mathrm{exec}}=1\cdot 0=0.
```

No S1-B1 query may run unless `G_{B1}^{exec}=1`. This turn stops before that operational state is reached — readiness must not be collapsed into authorization, and authorization must not be collapsed into execution.

---

## 5. Target Domain

```math
T_{B1}=\{t_1,\dots,t_{10}\},\qquad |T_{B1}|=10.
```

Read exactly from `S1_B1_BIBLIOGRAPHIC_IDENTITY_TARGET_MATRIX.csv`: `ET-01, ET-03, ET-04, ET-05, ET-06, ET-07, ET-08, ET-10, ET-12, ET-13`. No target may be added, removed, merged, or substituted.

Terminal execution-status taxonomy for every target (8 classes, from the frozen plan):

```text
LOOKUP_NOT_EXECUTED
NO_CANDIDATE_FOUND
ONE_CANDIDATE_UNVERIFIED
IDENTITY_CONFIRMED
MULTIPLE_CANDIDATES_AMBIGUOUS
HARD_IDENTIFIER_CONTRADICTION
PROVIDER_METADATA_CONFLICT_REQUIRES_REVIEW
NETWORK_OR_PROVIDER_FAILURE
```

---

## 6. Provider Scope

Only the six frozen providers from `S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv` may be used: `PROV-01` (Nationaal Archief), `PROV-02` (The National Archives, UK), `PROV-03` (Crossref), `PROV-04` (WorldCat), `PROV-05` (OpenDOAR), `PROV-06` (Google Scholar).

```math
N_{\mathrm{confirmation}}=3,\qquad N_{\mathrm{corroboration}}=1,\qquad N_{\mathrm{discovery}}=2.
```

No provider, domain, endpoint, access method, or credential may be added during execution.

---

## 7. Provider Restrictions

```text
PROV-05 OpenDOAR:                     DISCOVERY_ONLY
PROV-06 Google Scholar:                DISCOVERY_ONLY
PROV-04 WorldCat human-readable catalogue: CORROBORATION
PROV-04 WorldCat credentialed API:      NOT_APPROVED_CREDENTIAL_BLOCKED
```

`OpenDOAR` and `Google Scholar` may never independently produce `IDENTITY_CONFIRMED` — both are `DISCOVERY_ONLY`, incapable of confirmation or corroboration under §8 of `S1_B1_PROVIDER_ALLOWLIST_VERIFICATION_AUDIT.md`. The WorldCat credentialed API pathway remains blocked regardless of any future convenience; only its no-auth human-readable catalogue pathway is usable, and only in a `CORROBORATION` role.

---

## 8. Request Accounting

```math
R^{\mathrm{attempt}}=\sum_{i=1}^{10}\sum_{j=1}^{6}R_{ij}^{\mathrm{attempt}}.
```

```math
R^{\mathrm{attempt}}=R^{\mathrm{success}}+R^{\mathrm{failed}}+R^{\mathrm{blocked}}.
```

`R^{skipped}` (planned provider-target pairs not attempted because an earlier stop condition applied) is reported separately and is **not** included in the attempted-request denominator. No failed request may be silently retried with a different query or provider — any retry requires the same target, provider, query class, and a logged attempt index.

---

## 9. Request Envelope

No numerical request ceiling is invented in this authorization decision. For each provider `p_j`:

```math
L_j = \text{official documented request limit, where applicable}.
```

From `S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv`:

```text
PROV-01 (Nationaal Archief):    AUTOMATED_ACCESS_NOT_APPLICABLE — manual/human-readable catalogue only
PROV-02 (UK National Archives): OFFICIAL_LIMIT_DOCUMENTED — <=3000 calls/day, <=1 req/sec
PROV-03 (Crossref):              OFFICIAL_LIMIT_DOCUMENTED — 50 req/sec, X-Rate-Limit headers
PROV-04 (WorldCat, human catalogue): AUTOMATED_ACCESS_NOT_APPLICABLE — manual only
PROV-05 (OpenDOAR):              AUTOMATED_ACCESS_NOT_APPLICABLE — manual only
PROV-06 (Google Scholar):        NO_AUTOMATED_ACCESS_PLANNED — manual discovery search only, robots.txt disallows automation
```

Planned execution requires `R_j^{plan} \le L_j` wherever an official limit exists (PROV-02, PROV-03); for the remaining four providers, `NO_AUTOMATED_REQUEST_RATE_APPLICABLE` — access is manual/human-driven only, with no automated request rate at all.

**Before execution, a future turn must derive a target-provider query manifest from the frozen plan and show the maximum planned request count without executing it.** If an exact safe request envelope cannot be established at that time, the required status is `S1_B1_REQUEST_ENVELOPE_REQUIRES_REVIEW`, and execution must stop. This authorization decision does not itself construct that manifest — it only authorizes that a future turn may construct one, plus the lookup that follows once the manifest is reviewed.

---

## 10. Candidate Record Logging

```math
J_i=\{j:\text{candidate bibliographic records discovered for }t_i\},\qquad n_i=|J_i|.
```

Every candidate record in a future execution must log exactly:

```text
target_id, candidate_id, provider_id, provider_role, query_id, record_url, record_identifier,
observed_metadata_fields, hard_identifier_status, required_core_completeness, required_core_agreement,
provider_conflict_status, candidate_eligibility, final_target_status, notes
```

The log may contain bibliographic metadata only — never source text, historical quotations, OCR output, archival images, or document downloads.

---

## 11. Field Applicability and Normalization

```math
a_{ik}=\mathbf 1(\text{field }k\text{ applies}),\qquad o_{ijk}=\mathbf 1(\text{candidate field is observed}),\qquad m_{ijk}=\mathbf 1[N_k(x_{ik})=N_k(y_{ijk})].
```

`a_{ik}` for each target is fixed by `S1_B1_BIBLIOGRAPHIC_FIELD_ROLE_MATRIX.csv` (48 class-field pairs, K=12 fields, 4 classes) and may not be altered during execution. `N_k(\cdot)` normalizes representation only (per `S1_B1_BIBLIOGRAPHIC_IDENTITY_REVIEW_PLAN.md` §5) and may not translate titles, infer missing authors, merge editions, equate different years, or replace archival identifiers.

---

## 12. Hard-Identifier Gate

```math
C_{ij}=\sum_{k\in H_i}\mathbf 1(o_{ijk}=1\land m_{ijk}=0).
```

`H_i` for each target is fixed by `S1_B1_REQUIRED_CORE_FIELD_ADJUDICATION.md` §6 (`repository_or_catalogue_identity` for all ten; `persistent_identifier` additionally for ET-10 only, per its documented override). Required: `C_{ij}=0` for a candidate to proceed. No hard-identifier contradiction may be overridden by high coverage, a diagnostic score, or provider rank.

---

## 13. Required-Core Gate

```math
K_{ij}^{\mathrm{req}}=\prod_{k\in R_i}o_{ijk},\qquad M_{ij}^{\mathrm{req}}=\prod_{k\in R_i}m_{ijk}.
```

`R_i` for each target is fixed by `S1_B1_REQUIRED_CORE_FIELD_ADJUDICATION.md` §7 (class-specific: `{title, publication_year, edition, publisher}` for `PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION`; `{title, author_or_corporate_author, volume}` for `UNVERIFIED_REFERENCE`; `{title, author_or_corporate_author, publication_year}` for `CITED_ONLY_NOT_YET_LOCATED`; `{title, author_or_corporate_author}` for `LOCAL_FILE_IDENTITY_REVIEW / CITED_ONLY_NOT_YET_LOCATED`).

Candidate eligibility, rule-based and conjunctive, with no numerical weight or global threshold:

```math
E_{ij}=\mathbf 1\left[C_{ij}=0\land K_{ij}^{\mathrm{req}}=1\land M_{ij}^{\mathrm{req}}=1\right].
```

---

## 14. Identity Confirmation Gate

```math
Z_i=\sum_{j\in J_i}E_{ij}.
```

Identity may be confirmed only if exactly one eligible candidate exists:

```math
Z_i=1
```

and there is no unresolved provider hard-field conflict for that candidate. If `Z_i=0`, status `NO_ELIGIBLE_IDENTITY_CANDIDATE`/`NO_CANDIDATE_FOUND`. If `Z_i>1`, status `MULTIPLE_CANDIDATES_AMBIGUOUS` — no candidate may be selected by score tie-breaking, provider preference, or convenience. No weighted score or global coverage threshold may decide identity, ever.

---

## 15. Provider Conflict Gate

```math
V_{ij,k}^{(p,q)}=\mathbf 1[N_k(y_{ijk}^{(p)})\ne N_k(y_{ijk}^{(q)})],\qquad V_{ij}^{(p,q)}=\sum_{k\in H_i}V_{ij,k}^{(p,q)}.
```

If `V_{ij}^{(p,q)}>0`, required status `PROVIDER_METADATA_CONFLICT_REQUIRES_REVIEW`. Provider rank (§13 of `S1_B1_PROVIDER_ALLOWLIST_VERIFICATION_AUDIT.md`) may not resolve the conflict automatically.

---

## 16. Batch Estimands

With fixed denominator `|T_{B1}|=10`:

```math
\widehat P_{\mathrm{confirmed}}=\tfrac{1}{10}\sum_i \mathbf 1(\text{IDENTITY\_CONFIRMED}_i),\quad
\widehat P_{\mathrm{ambiguous}}=\tfrac{1}{10}\sum_i \mathbf 1(\text{AMBIGUOUS}_i),
```
```math
\widehat P_{\mathrm{contradiction}}=\tfrac{1}{10}\sum_i \mathbf 1(\text{HARD\_CONTRADICTION}_i),\quad
\widehat P_{\mathrm{provider\_conflict}}=\tfrac{1}{10}\sum_i \mathbf 1(\text{PROVIDER\_CONFLICT}_i),
```
```math
\widehat P_{\mathrm{execution\_failure}}=\tfrac{1}{10}\sum_i \mathbf 1(\text{NETWORK\_OR\_PROVIDER\_FAILURE}_i).
```

These estimands describe lookup outcomes only; they do not estimate source truth, historical truth, or evidentiary independence. Not computed by this document — no lookup has run.

---

## 17. Success Gate

`T_A` (all ten targets reach a terminal status), `R_A` (request accounting reconciles), `P_A` (only allowed providers/methods used), `C_A` (all candidates logged), `I_A` (identity gates applied exactly), `N_A` (no hard conflict overridden), `S_A` (no source content/retrieval), `M_A` (no registry/claim/promotion mutation), `D_A` (no downstream batch begins):

```math
G_{B1}^{\mathrm{complete}}=\mathbf 1[T_A=R_A=P_A=C_A=I_A=N_A=S_A=M_A=D_A=1].
```

If `G_{B1}^{complete}=1`, future execution status may be `S1_B1_BIBLIOGRAPHIC_IDENTITY_REVIEW_COMPLETE`. Completion does not require all ten identities to be confirmed — ambiguous, not-found, contradiction, and provider-failure outcomes are valid terminal evidence if properly recorded.

---

## 18. Stop Conditions

Future execution must stop if: the synchronized authorization artifact is absent; the target count differs from 10; the provider allowlist differs from the frozen six rows; an unapproved provider or method is required; a provider requires unapproved credentials; a request ceiling or rate cannot be established; a hard identifier conflicts; multiple eligible candidates remain; a provider metadata conflict occurs; a query would require retrieval or source-content access; a record URL would trigger a source download rather than metadata display; a query or identifier would need fabrication; any registry edit appears necessary; a claim or source promotion begins; S1-B2 through S1-B5 begins; any protected artifact changes.

Target-level ambiguity or not-found status does not necessarily stop the whole batch — it stops processing that target and records the terminal status; the batch continues to the next target.

---

## 19. Retrieval and Content Prohibition

```text
source retrieval:        NOT_AUTHORIZED (this decision, and any future execution turn it authorizes)
source-content access:   NOT_AUTHORIZED
OCR/transcription:       NOT_AUTHORIZED
document downloads:      NOT_AUTHORIZED
```

---

## 20. Claim and Registry Prohibition

```text
claim creation:            NOT_AUTHORIZED
source-class promotion:    NOT_AUTHORIZED
target registry edits:     NOT_AUTHORIZED
batch registry edits:      NOT_AUTHORIZED
```

---

## 21. Downstream Batch Nonauthorization

```text
S1-B2: PLANNED_ONLY / NOT_AUTHORIZED
S1-B3: PLANNED_ONLY / NOT_AUTHORIZED
S1-B4: PLANNED_ONLY / NOT_AUTHORIZED
S1-B5: PLANNED_ONLY / NOT_AUTHORIZED
```

Nothing in this authorization decision authorizes any downstream batch.

---

## 22. Production Isolation

This decision, and any future execution it authorizes, touch only repository-tracked planning/execution-log documentation. Neither this decision nor a future S1-B1 execution may change backend, frontend, API, database, Atlas, Graphify, or `westkust-prod` container state, or run a build, restart, reload, migration, or deployment.

---

## 23. Execution Status

```text
NOT_STARTED
```

---

## 24. Final Decision

```text
S1_B1_BIBLIOGRAPHIC_METADATA_LOOKUP_AUTHORIZED_NOT_STARTED
```
