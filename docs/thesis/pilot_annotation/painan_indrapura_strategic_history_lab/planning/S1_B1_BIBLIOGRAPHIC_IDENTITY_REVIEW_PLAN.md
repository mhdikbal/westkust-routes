# S1-B1 — Bibliographic Identity Review Plan

**Status:** PLANNING ONLY. No network request, bibliographic lookup, source-content access, external retrieval, or claim entry is performed by this document. No registry is modified. No S1-B1 execution is authorized.

**Authoritative baseline:** `77a77c8c730d98c4d55a01ce658b32479b412a54` (S1-B0 `COMPLETE_WITH_PATH_DOMAIN_CLARIFICATION`, pushed and server-synced)
**Workstream:** `PAINAN_INDRAPURA_STRATEGIC_HISTORY_LAB`
**Sprint / Batch:** `S1` / `S1-B1`

---

## 1. Purpose

Determine whether S1-B1 (bibliographic identity review) can be authorized safely and reproducibly in a later, separate turn. This document defines the plan, mathematical contract, target-level lookup specification, evidence hierarchy, success gates, and stop conditions needed for that later authorization decision. No web lookup or bibliographic retrieval is performed now.

---

## 2. Scope of S1-B1

S1-B1 may later verify bibliographic identity for the ten targets assigned to it in the frozen batch registry (`S1_EXECUTION_BATCH_REGISTRY.csv`, row `S1-B1`), mechanically reconciled against `S1_EXECUTION_TARGET_REGISTRY.csv`:

```text
ET-01, ET-03, ET-04, ET-05, ET-06, ET-07, ET-08, ET-10, ET-12, ET-13
target count = 10, unique = 10, all present in target registry, all execution_status = PLANNED_ONLY
```

The future batch may compare public bibliographic metadata such as: title; author or corporate author; publication year; edition; volume; issue; publisher; repository or catalogue identity; persistent identifier; catalogue record URL; language; physical or digital format.

S1-B1 must not: retrieve or download source content; read full-text historical sources; extract claims; infer historical facts; promote source admissibility; modify the target registry; authorize S1-B2 or later batches.

---

## 3. Mathematical Domain

Target subset:

```math
T_{B1}=\{t_1,\dots,t_{10}\},\qquad |T_{B1}|=10.
```

For target `t_i`, the frozen expected bibliographic metadata vector:

```math
x_i=(x_{i1},x_{i2},\dots,x_{iK}),
```

and an external candidate record (future, not fetched now):

```math
y_{ij}=(y_{ij1},y_{ij2},\dots,y_{ijK}),
```

where `j` indexes candidate records and `K` is the versioned field count, derived from the field universe below, not invented:

```math
K=12.
```

---

## 4. Field Applicability

```math
a_{ik}=\mathbf 1(\text{field }k\text{ is applicable to target }t_i).
```

```math
o_{ijk}=\mathbf 1(y_{ijk}\text{ is present in candidate record }j).
```

Only fields with `a_{ik}=1` may enter identity comparison. A non-applicable field is recorded as `NOT_APPLICABLE_TO_BIBLIOGRAPHIC_CLASS`, never as a mismatch.

**Field universe (K=12):** `title, author_or_corporate_author, publication_year, edition, volume, issue, publisher, repository_or_catalogue_identity, persistent_identifier, catalogue_record_url, language, physical_or_digital_format`.

**Applicability by bibliographic class** (per-target detail in the target matrix, §11):

- `PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION` (ET-01): all 12 fields applicable — treaty-edition identity (publisher, edition, year) is exactly what remains unresolved for this target.
- `UNVERIFIED_REFERENCE` — CD-volume compilations (ET-03..ET-08): `title, publisher_or_compiling_institution (as author_or_corporate_author), volume, repository_or_catalogue_identity, catalogue_record_url, language, physical_or_digital_format` applicable; `issue` and `persistent_identifier` `NOT_APPLICABLE_TO_BIBLIOGRAPHIC_CLASS` (archival compilations predate DOI issuance); `edition` applicable only if a specific published edition (as opposed to the archival original) is being cited.
- `CITED_ONLY_NOT_YET_LOCATED` (ET-10, ET-12, ET-13): `title, author_or_corporate_author, publication_year, repository_or_catalogue_identity, language` applicable; `edition, volume, issue, catalogue_record_url, physical_or_digital_format` applicable only once a candidate is found; `persistent_identifier` applicable for ET-10 only (a modern PhD thesis may carry a DOI/institutional-repository handle) — `NOT_APPLICABLE_TO_BIBLIOGRAPHIC_CLASS` for ET-12/ET-13 (17th-century sources).

No applicable field value, catalogue URL, DOI, ISBN, archival identifier, publication year, author, compiler, or edition is asserted or fabricated anywhere in this document or the accompanying matrix — where unresolved, the field is recorded as `UNRESOLVED`, not populated with an invented value.

---

## 5. Field-Level Agreement

For every applicable field, a versioned normalization function `N_k(\cdot)` normalizes representation only (Unicode normalization, whitespace trimming, documented punctuation normalization, case normalization where bibliographically safe, exact year parsing, persistent-identifier canonicalization). It must not translate titles, infer missing authors, merge editions, equate different years, replace archival identifiers, or treat approximate similarity as exact identity.

```math
m_{ijk}=\mathbf 1\left[N_k(x_{ik})=N_k(y_{ijk})\right].
```

**Normalization-rule status:** `SPECIFIED` (rules above). No `N_k` is executed in this turn — there is no candidate record `y_{ij}` to normalize against, since no lookup has run.

---

## 6. Weighted Identity Score (planning-only)

```math
S_{ij}=\frac{\sum_{k=1}^{K}w_k a_{ik}o_{ijk}m_{ijk}}{\sum_{k=1}^{K}w_k a_{ik}o_{ijk}},
```

defined only where the denominator is positive. `w_k \ge 0` is a preregistered field weight.

**Required status:**

```text
FIELD_WEIGHTS_PENDING_RESEARCHER_DECISION
```

No weight value is selected in this planning turn. `S_ij` never overrides a hard-identifier contradiction (§7).

---

## 7. Hard Identifiers and Contradictions

Preregistered hard-identifier field set `H` (subset of the K=12 fields, per target, only where actually applicable — none invented):

- ET-01: `H = {repository_or_catalogue_identity}` once a specific printed edition is identified; `persistent_identifier` not expected for a 17th-century treaty edition.
- ET-03..ET-08 (CD1-CD6): `H = {repository_or_catalogue_identity}` only — no DOI/ISBN expected for archival compilation volumes.
- ET-10 (modern PhD thesis): `H = {persistent_identifier, repository_or_catalogue_identity}` — a thesis may carry an institutional-repository handle or DOI.
- ET-12, ET-13: `H = {repository_or_catalogue_identity}` only — 17th-century sources, no DOI/ISBN.

```math
C_{ij}=\sum_{k\in H}\mathbf 1(a_{ik}=1\land o_{ijk}=1\land m_{ijk}=0).
```

**Required identity gate:** `C_{ij}=0`. Any hard-identifier contradiction prevents automatic identity confirmation regardless of `S_ij`.

---

## 8. Evidence Coverage

```math
Q_{ij}=\frac{\sum_{k=1}^{K}a_{ik}o_{ijk}}{\sum_{k=1}^{K}a_{ik}}.
```

The denominator is the applicable-field count for target `i`, not the global field count `K=12`.

**Required status:**

```text
MINIMUM_BIBLIOGRAPHIC_COVERAGE_PENDING_RESEARCHER_DECISION
```

No numerical minimum for `Q_ij` is selected in this planning turn.

---

## 9. Candidate Multiplicity and Ambiguity

```math
J_i=\{j:\text{candidate record }j\text{ was found for }t_i\},\qquad n_i=|J_i|.
```

**Outcome taxonomy (7 classes):**

```text
NO_CANDIDATE_FOUND
ONE_CANDIDATE_UNVERIFIED
IDENTITY_CONFIRMED
MULTIPLE_CANDIDATES_AMBIGUOUS
HARD_IDENTIFIER_CONTRADICTION
LOOKUP_NOT_EXECUTED
NETWORK_OR_PROVIDER_FAILURE
```

If multiple candidates remain observationally equivalent under the approved metadata fields, none is selected arbitrarily — the outcome is `MULTIPLE_CANDIDATES_AMBIGUOUS`. All ten targets currently sit at `LOOKUP_NOT_EXECUTED`, since no query has run.

---

## 10. Source Hierarchy (candidate, for researcher review — no provider auto-approved)

1. Issuing repository or archival catalogue (the institution actually holding the CD volumes / Het Painansch Contract / Fort York material).
2. Publisher or journal record (ET-01's printed edition; ET-10's degree-granting institution's press/repository).
3. DOI registration agency or equivalent persistent-identifier authority (relevant chiefly to ET-10).
4. National or university library catalogue (e.g. WorldCat-class union catalogues, national library OPACs) — for cross-checking CD-volume compiler/edition identity.
5. Recognized bibliographic database (institutional finding aids, published bibliographies of VOC sources).
6. Secondary index or search-engine result — **discovery-only**, never sole identity confirmation.

Search-engine snippets must never serve as sole identity confirmation.

**Required status:**

```text
PROVIDER_ALLOWLIST_PENDING_RESEARCHER_DECISION
```

No provider is approved automatically by this hierarchy — it is a draft candidate hierarchy for researcher review before S1-B1 execution. No specific institution, catalogue name, or URL is asserted as an approved provider in this document.

---

## 11. Target-Level Lookup Plan

Full per-target specification (frozen expected metadata, bibliographic class, applicable fields, hard identifiers, proposed provider classes, query-template status, network/content/retrieval requirements, ambiguity risk, planned outcome taxonomy, stop condition, execution status) is recorded in `S1_B1_BIBLIOGRAPHIC_IDENTITY_TARGET_MATRIX.csv`. No query is executed. No URL, DOI, ISBN, archival identifier, publication year, author, compiler, edition, or provider record is fabricated anywhere in the matrix — unresolved fields are recorded as `UNRESOLVED`.

---

## 12. Batch-Level Estimands

```math
z_i=\mathbf 1[\text{target }i\text{ reaches IDENTITY\_CONFIRMED}]
```
```math
\widehat P_{\mathrm{confirmed}}=\frac{1}{|T_{B1}|}\sum_{i\in T_{B1}}z_i
```

```math
u_i=\mathbf 1[\text{target }i\text{ remains ambiguous}]
```
```math
\widehat P_{\mathrm{ambiguous}}=\frac{1}{|T_{B1}|}\sum_{i\in T_{B1}}u_i
```

```math
h_i=\mathbf 1[\text{a hard contradiction is found for target }i]
```
```math
\widehat P_{\mathrm{contradiction}}=\frac{1}{|T_{B1}|}\sum_{i\in T_{B1}}h_i
```

```math
e_i=\mathbf 1[\text{lookup execution fails for infrastructure/provider reasons}]
```
```math
\widehat P_{\mathrm{execution\_failure}}=\frac{1}{|T_{B1}|}\sum_{i\in T_{B1}}e_i
```

`|T_{B1}|=10` is the fixed, explicit denominator for all four estimands. These estimands describe future batch outcomes only; they do not estimate historical truth or evidentiary reliability. None is computed in this turn — all per-target indicator values (`z_i, u_i, h_i, e_i`) are undefined pending execution, not assumed zero or any other value.

---

## 13. Authorization-Readiness Gate

Planning completeness indicators (binary): `P_T` (ten targets fully specified), `P_F` (applicable field schema specified), `P_H` (hard-identifier rules specified), `P_S` (provider hierarchy/allowlist drafted), `P_N` (normalization rules specified), `P_O` (outcome taxonomy specified), `P_D` (denominators specified), `P_X` (stop conditions specified), `P_E` (epistemic boundaries specified), `P_R` (registries and source files remain unchanged).

```math
G_{B1}^{\mathrm{ready}}=\mathbf 1\left[P_T=P_F=P_H=P_S=P_N=P_O=P_D=P_X=P_E=P_R=1\right].
```

Evaluated mechanically in `S1_B1_AUTHORIZATION_READINESS_AUDIT.md`. `G_{B1}^{\mathrm{ready}}=1` does **not** authorize execution — it states only that the planning package is ready for researcher review. Field weights (§6), coverage threshold (§8), and provider allowlist (§10) remaining `PENDING_RESEARCHER_DECISION` does not block this gate — the gate requires the *rules and structure* to be specified, not that every numeric value already be chosen.

---

## 14. Stop Conditions

Stop planning and report `S1_B1_PLANNING_REQUIRES_RESEARCHER_REVIEW` if: the ten-target scope cannot be reconciled; a target ID is missing/duplicated; a query would require source-content access; a target requires external retrieval rather than metadata lookup; a provider requires credentials not already authorized; a provider's terms/access boundary cannot be determined; a matching rule would merge distinct editions/archival objects; a numerical weight or threshold lacks provenance; a URL/identifier/path/source position would need to be fabricated; the frozen registry would need modification; any source content is accessed; any network call is made; B2/B3/B4/B5 begins.

None of these conditions is triggered by this planning turn (verified in §11 of `S1_B1_AUTHORIZATION_READINESS_AUDIT.md`).

---

## 15. Epistemic Boundaries

These formulas and this plan govern bibliographic metadata identity only. They do not: establish source admissibility beyond identity confirmation; validate source content; create a historical claim; establish actor identity, causal effect, or historical truth; authorize S1-B2 through S1-B5; execute Hawkes, game theory, or counterfactual modeling.

---

## 16. Downstream Batch Status

```text
S1-B1: PLANNED_ONLY / NOT_AUTHORIZED (this document is planning-only; it does not authorize execution)
S1-B2: PLANNED_ONLY / NOT_AUTHORIZED
S1-B3: PLANNED_ONLY / NOT_AUTHORIZED
S1-B4: PLANNED_ONLY / NOT_AUTHORIZED
S1-B5: PLANNED_ONLY / NOT_AUTHORIZED
```

---

## 17. Researcher Decision Adjudication (appended additively)

**Provenance:** this section was appended after §1-16 above (unmodified) per a separate researcher-decision-adjudication instruction. Sections §6 (weighted score), §8 (coverage threshold), and §10 (provider allowlist) above are preserved as originally written; this section records the three decisions adjudicated over them, and supersedes only their *pending-decision* status, not their formulas. Full detail lives in the dedicated artifact `S1_B1_RESEARCHER_DECISION_ADJUDICATION.md`.

### 17.1 Decision 1 — Matching architecture

```text
PRIMARY_MATCHING_METHOD:    RULE_BASED_CONJUNCTIVE_IDENTITY_GATE
WEIGHTED_SCORE:              DIAGNOSTIC_ONLY_NOT_AUTHORIZED_FOR_IDENTITY_CONFIRMATION
NUMERICAL_FIELD_WEIGHTS:     NOT_SELECTED
```

No `w_k` values are assigned. `S_ij` (§6 above) remains defined but is downgraded to a non-authoritative diagnostic; it cannot override a hard-identifier contradiction, cannot itself produce `IDENTITY_CONFIRMED`, and cannot merge editions, volumes, repositories, or archival objects. Required-core completeness (`K^{req}_{ij}`) and required-core agreement (`M^{req}_{ij}`) replace weighting as the operative rule — see `S1_B1_RESEARCHER_DECISION_ADJUDICATION.md` §4-§7 for the full gate (`E_ij`).

### 17.2 Decision 2 — Coverage architecture

```text
GLOBAL_NUMERICAL_COVERAGE_THRESHOLD: NOT_SELECTED
PRIMARY_SUFFICIENCY_RULE:            CLASS_SPECIFIC_REQUIRED_FIELD_COMPLETENESS
Q_ij:                                DIAGNOSTIC_COVERAGE_ONLY
```

`Q_ij` (§8 above) remains defined exactly as written but is confirmed diagnostic-only — it does not imply identity confirmation in either direction. The operative sufficiency gate is `G^{suff}_ij` (uniqueness of the single rule-eligible candidate), detailed in `S1_B1_RESEARCHER_DECISION_ADJUDICATION.md` §8.

### 17.3 Decision 3 — Provider-class governance

```text
PROVIDER_CLASS_HIERARCHY:        APPROVED_WITH_LIMITATIONS
INDIVIDUAL_PROVIDER_ALLOWLIST:   PENDING_PREEXECUTION_FREEZE
NETWORK_EXECUTION:               NOT_AUTHORIZED
```

The 6-tier candidate hierarchy (§10 above) is adopted as a conditional class hierarchy — providers may be drawn from these six classes once individually vetted, but no individual provider (name, domain, catalogue, API) is approved, verified, or listed in this turn. Provider class 6 (search engine / secondary index) still cannot confirm identity by itself. See `S1_B1_RESEARCHER_DECISION_ADJUDICATION.md` §9-§10 for the provider admissibility indicator and conflict rule.

### 17.4 Outcome taxonomy — additive 8th class

The 7-class taxonomy in §9 above is preserved; one class is added additively:

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

`PROVIDER_METADATA_CONFLICT_REQUIRES_REVIEW` is added because a provider-vs-provider hard-field conflict (`V_ij^(p,q) > 0`) is a distinct failure mode from a single-source hard-identifier contradiction (`C_ij > 0`) and needs its own status so it is never silently resolved by rank preference.

### 17.5 Two remaining blockers before S1-B1 execution authorization

```text
1. class-specific required-core field sets (R_i) — drafted in S1_B1_RESEARCHER_DECISION_ADJUDICATION.md §7, PENDING RESEARCHER REVIEW
2. individual provider allowlist — schema only drafted in S1_B1_RESEARCHER_DECISION_ADJUDICATION.md §9, PENDING PREEXECUTION FREEZE
```

Both must be resolved and frozen, separately, before the S1-B1 planning package itself is frozen and before any network-authorization decision is made.

---

## 18. Required-Core Field-Set Adjudication (appended additively)

**Provenance:** appended after §1-17 above (unmodified) following a separate required-core field-review turn. Full detail (48-row class×field matrix, per-class justification, the single ET-10 override) lives in `S1_B1_BIBLIOGRAPHIC_FIELD_ROLE_MATRIX.csv` and `S1_B1_REQUIRED_CORE_FIELD_ADJUDICATION.md`.

Blocker 1 from §17.5 is now resolved:

```text
D_R:                          1  (was 0)
G_B1^field:                   1
REQUIRED_CORE_FIELD_SETS_APPROVED_WITH_LIMITATIONS
```

`D_I` (individual provider allowlist) is untouched and remains `0`, so `G_{B1}^{authorize}` remains `0`. Blocker 2 (individual provider allowlist verification and freeze) is the sole remaining item before S1-B1 execution authorization.

---

## 19. Provider Allowlist Verification Update (appended additively)

**Provenance:** appended after §1-18 above (unmodified) following a separate controlled-web provider-verification turn. Full detail: `S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv` (6 providers verified), `S1_B1_PROVIDER_ALLOWLIST_VERIFICATION_AUDIT.md`.

```text
D_I:                1  (was 0)
G_B1^provider:      1
INDIVIDUAL_PROVIDER_ALLOWLIST_READY_FOR_RESEARCHER_FREEZE
```

```math
G_{B1}^{\mathrm{authorize}}=\mathbf 1\left[G_{B1}^{\mathrm{decision}}=1\land D_R=1\land D_I=1\right]=1.
```

All three preconditions of `G_{B1}^{authorize}` are now satisfied. This does **not** authorize S1-B1 execution — a separate researcher authorization decision must still be recorded and frozen, and the provider allowlist itself must still be frozen by the researcher (this task produced verification, not a freeze). `S1-B1` remains `PLANNED_ONLY` / `NOT_AUTHORIZED`.
