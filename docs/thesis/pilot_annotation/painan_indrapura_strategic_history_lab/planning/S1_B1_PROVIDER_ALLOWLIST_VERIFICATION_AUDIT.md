# S1-B1 — Individual Provider Allowlist Verification Audit

**Status:** PROVIDER-INFRASTRUCTURE VERIFICATION ONLY. Controlled web access was used exclusively to verify provider-level facts (official identity, domain, terms, API/rate-limit documentation). No S1-B1 target title, author, identifier, or candidate bibliographic record was queried. No source content was accessed, retrieved, or downloaded. No claim was created. No frozen registry or target matrix was modified. S1-B1 execution is NOT authorized by this document.

**Authoritative baseline:** `77a77c8c730d98c4d55a01ce658b32479b412a54`
**Workstream:** `PAINAN_INDRAPURA_STRATEGIC_HISTORY_LAB`
**Sprint / Batch:** `S1` / `S1-B1`

---

## 1. Scope

Resolve the sole remaining S1-B1 execution-readiness blocker, `D_I = 0`, by verifying a candidate individual-provider allowlist using controlled web access restricted to provider-level facts only.

---

## 2. Authoritative Baseline

```text
S1-B0:            COMPLETE_WITH_PATH_DOMAIN_CLARIFICATION (commit 77a77c8, pushed/server-synced)
S1-B1:             PLANNED_ONLY / NOT_AUTHORIZED
G_B1^decision:     1
D_R:               1
D_I:               0 (before this task)
G_B1^authorize:    0
```

Verified: local HEAD = `origin/main` = `77a77c8`; `D_R=1` confirmed in `S1_B1_REQUIRED_CORE_FIELD_ADJUDICATION.md` §12. All matched; task proceeded.

---

## 3. Controlled Web Boundary

Permitted query subjects used: provider official site, provider catalogue/API documentation, provider authentication requirements, provider rate-limit documentation, provider terms of use, provider robots policy, provider persistent-identifier scope, provider institutional ownership.

**Six web searches were executed, all provider-level only:**

```text
1. "Nationaal Archief Netherlands official website API documentation"
2. "The National Archives UK Kew official website API documentation discovery catalogue"
3. "WorldCat official terms of use API search"
4. "Crossref REST API documentation terms of use rate limit"
5. "OpenDOAR directory of open access repositories official site terms"
6. "Google Scholar terms of service automated access robots.txt policy"
```

None of these queries named, referenced, or could return results specific to: Het Painansch Contract, Corpus Diplomaticum volumes, any ET-01 through ET-13 target title or author, any source identifier, Painan or Indrapura historical claims, full-text archives, source downloads, OCR material, or historical document images. Zero target-lookup queries were made.

---

## 4. Provider Universe

```math
P=\{p_1,\dots,p_6\},\qquad J=6.
```

`J=6` was derived from documented candidate-provider needs (the hard-identifier and required-core field roles established in `S1_B1_BIBLIOGRAPHIC_FIELD_ROLE_MATRIX.csv`), not preselected for symmetry:

```text
PROV-01: Nationaal Archief (National Archives of the Netherlands)   — class 1
PROV-02: The National Archives (UK, Kew)                             — class 1
PROV-03: Crossref                                                    — class 3
PROV-04: WorldCat (OCLC)                                             — class 4
PROV-05: OpenDOAR (Directory of Open Access Repositories)            — class 4
PROV-06: Google Scholar                                              — class 6
```

No candidate provider was added or removed after verification began.

---

## 5. Provider Classes

```text
1 = issuing repository or archival catalogue     -> PROV-01, PROV-02
2 = publisher or journal record                  -> none verified this turn (see §15)
3 = persistent-identifier authority              -> PROV-03
4 = national or university library catalogue     -> PROV-04, PROV-05
5 = recognized bibliographic database            -> none verified this turn (see §15)
6 = discovery only                                -> PROV-06
```

Each provider carries exactly one primary class (`S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv`, column `provider_class`).

---

## 6. Verification Variables

For each provider, `i_j, d_j, m_j, a_j, t_j, r_j, q_j, s_j` were evaluated from official sources only:

```text
PROV-01: i=1 d=1 m=1 a=1 t=1 r=AUTOMATED_ACCESS_NOT_APPLICABLE q=1 s=1
PROV-02: i=1 d=1 m=1 a=1 t=1 r=1 (OFFICIAL_LIMIT_DOCUMENTED) q=1 s=1
PROV-03: i=1 d=1 m=1 a=1 t=1 r=1 (OFFICIAL_LIMIT_DOCUMENTED) q=1 s=1
PROV-04: i=1 d=1 m=1 a=1 (documented: auth required for API, not for human catalogue) t=1 (partially documented) r=AUTOMATED_ACCESS_NOT_APPLICABLE q=1 s=1
PROV-05: i=1 d=1 m=1 a=1 t=1 r=AUTOMATED_ACCESS_NOT_APPLICABLE q=1 s=1
PROV-06: i=1 d=1 m=1 a=1 (documented: automated access prohibited) t=1 r=NO_AUTOMATED_ACCESS_PLANNED q=1 s=1
```

These are provider-readiness indicators only; they do not measure historical reliability of any source.

---

## 7. Provider Admissibility Gate

```math
A_P(p_j)=\mathbf 1[i_j=d_j=m_j=a_j=t_j=q_j=s_j=1].
```

All six candidate providers satisfy `A_P(p_j)=1` (see `admissibility_gate` column). For PROV-01, PROV-04, and PROV-05, automated access is not planned and is recorded as `AUTOMATED_ACCESS_NOT_APPLICABLE` rather than treated as missing evidence, per the instruction's explicit exception. No provider evidence gap was filled with an assumption; where terms were only partially documented (PROV-04's full legal text), the provider's approved query method and role were downgraded accordingly (human catalogue only, `CORROBORATION` not `CONFIRMATION`) rather than the gap being papered over.

No provider entered the allowlist with `A_P(p_j)=0`.

---

## 8. Evidence Hierarchy

Every provider row cites at least one official source (`verification_source_url`/`verification_source_title`), all at evidence-priority tier 1 or 2 (official institutional documentation or official API documentation) except PROV-06, which cites tier 3 (official terms-of-use page) since Google Scholar has no official API. No provider was approved from a search-result snippet alone — every `verified_fact` cites the specific official page(s) returned by the search, not the search-engine summary text itself as the source of record.

---

## 9. Authentication and Credentials

```text
PROV-01, PROV-02, PROV-03, PROV-05: no authentication required for the approved query method
PROV-04 (WorldCat): API requires institutional credential (WSKey) — NOT authorized this task; public worldcat.org catalogue search does not require credentials and is the approved method instead
PROV-06 (Google Scholar): no login required for manual browsing; automated/API access is prohibited by terms regardless of credentials
```

No credential-requiring pathway was approved. `credentials_authorized = NO` for PROV-04 (the only provider where a credential-gated pathway exists); its `approved_query_method` was set to the non-credentialed alternative rather than treating the whole provider as blocked, since a legitimate no-auth pathway exists and is officially documented.

---

## 10. Query Methods

```text
PROV-01: OFFICIAL_HUMAN_READABLE_CATALOGUE
PROV-02: OFFICIAL_API (documented, rate-limited)
PROV-03: OFFICIAL_API (documented, rate-limited)
PROV-04: OFFICIAL_HUMAN_READABLE_CATALOGUE (API pathway NOT_APPROVED_CREDENTIAL_BLOCKED)
PROV-05: OFFICIAL_HUMAN_READABLE_CATALOGUE
PROV-06: DISCOVERY_SEARCH_ONLY (manual only; automation prohibited by terms)
```

No API endpoint was guessed for any provider; PROV-02 and PROV-03's endpoints are exactly as published in their own official documentation.

---

## 11. Terms and Access Boundaries

All six providers have a documented terms/access boundary (`terms_review_status` = `DOCUMENTED` for five, `PARTIALLY_DOCUMENTED` for PROV-04, where the general access-tier structure was confirmed but the complete legal text was not retrieved in this turn). No provider was approved on an unclear-terms basis without a corresponding downgrade — PROV-04 was accordingly restricted to its no-auth human-catalogue pathway only.

---

## 12. Rate-Limit Treatment

```text
PROV-01: AUTOMATED_ACCESS_NOT_APPLICABLE
PROV-02: OFFICIAL_LIMIT_DOCUMENTED (<=3000 calls/day, <=1 req/sec, per official guidance)
PROV-03: OFFICIAL_LIMIT_DOCUMENTED (50 req/sec, X-Rate-Limit headers, 503/429 back-off documented)
PROV-04: AUTOMATED_ACCESS_NOT_APPLICABLE
PROV-05: AUTOMATED_ACCESS_NOT_APPLICABLE
PROV-06: NO_AUTOMATED_ACCESS_PLANNED (robots.txt disallows automated crawling of search paths)
```

No rate limit was invented for any provider. No numerical request envelope is set beyond what is officially documented (PROV-02, PROV-03); all other providers are restricted to manual/human access with no automated request envelope at all.

---

## 13. Provider Roles

```text
PROV-01 (class 1): CONFIRMATION, within its own issuing/holding scope
PROV-02 (class 1): CONFIRMATION, within its own issuing/holding scope
PROV-03 (class 3): CONFIRMATION, for identifiers within its DOI registry scope only
PROV-04 (class 4): CORROBORATION (downgraded from potential confirmation due to the credential-gated API being unavailable; the no-auth catalogue-search pathway is treated as corroborating, not confirming, consistent with class-4 rules allowing either role "depending on record authority")
PROV-05 (class 4): DISCOVERY_ONLY (a repository directory, not a bibliographic-record source — cannot itself confirm or corroborate a specific work's identity)
PROV-06 (class 6): DISCOVERY_ONLY (always, per class-6 rule — cannot confirm identity alone)
```

Provider rank does not override a conflicting hard identifier for any target — this rule is preserved unevaluated (§14 below), since no target record has been looked up.

---

## 14. Provider Conflict Rule

```math
V_{ij,k}^{(p,q)}=\mathbf 1\left[N_k(y_{ijk}^{(p)})\ne N_k(y_{ijk}^{(q)})\right],\qquad V_{ij}^{(p,q)}=\sum_{k\in H_i}V_{ij,k}^{(p,q)}.
```

Specified, not evaluated — no target record exists to compare across providers. If `V_ij^(p,q) > 0` in a future execution turn, status `PROVIDER_METADATA_CONFLICT_REQUIRES_REVIEW` applies, and the preferred provider class (§13) must not resolve the conflict automatically.

---

## 15. Required-Class Coverage

`C_req`, the set of provider classes actually needed to satisfy a hard-identifier or required-core field across the ten S1-B1 targets (per `S1_B1_BIBLIOGRAPHIC_FIELD_ROLE_MATRIX.csv`):

```text
class 1 (issuing repository/archival catalogue): gates repository_or_catalogue_identity, the HARD_IDENTIFIER for all four bibliographic classes -> REQUIRED
class 3 (persistent-identifier authority):        gates persistent_identifier, the HARD_IDENTIFIER override for ET-10 only -> REQUIRED
class 4 (national/university library catalogue): explicitly named in the plan's source hierarchy (tier 4) as the cross-check for CD-volume compiler/edition identity, a REQUIRED_CORE_METADATA field -> REQUIRED (as corroboration, not as a hard-identifier gate)
```

`C_req = {1, 3, 4}`. Classes 2 (publisher/journal record) and 5 (recognized bibliographic database) are part of the general six-tier hierarchy but are not themselves required to satisfy any target's hard-identifier or required-core field — the `publisher` required-core field (ET-01 only) is satisfiable via a class-1 or class-4 catalogue record without a dedicated class-2 provider, and no target's admissibility gate depends on a class-5 source. Per the instruction's own rule ("do not add an inapplicable provider class merely to make the hierarchy look complete"), classes 2 and 5 were **not** populated in this task, and this is recorded as a documented gap, not a fabricated inclusion.

```math
I_1=1,\quad I_3=1,\quad I_4=1,\qquad G_P^{\mathrm{coverage}}=\prod_{c\in\{1,3,4\}}I_c=1.
```

All required provider classes have at least one admissible provider.

---

## 16. Provider Gate Evaluation

| Indicator | Meaning | Value |
|---|---|---|
| `P_U` | Provider universe documented | 1 |
| `P_I` | Official identities and domains verified | 1 |
| `P_M` | Metadata scopes documented | 1 |
| `P_A` | Authentication requirements documented | 1 |
| `P_T` | Terms and access boundaries documented | 1 |
| `P_Q` | Approved query methods defined | 1 |
| `P_R` | Automated rate limits documented or explicitly not applicable | 1 |
| `P_C` | Required provider-class coverage complete | 1 |
| `P_E` | Every provider-level fact has evidence provenance | 1 |
| `P_0` | Zero target lookup / retrieval / content access / claim / registry mutation / downstream batch | 1 |

```math
G_{B1}^{\mathrm{provider}}=\mathbf 1[P_U=P_I=P_M=P_A=P_T=P_Q=P_R=P_C=P_E=P_0=1]=1.
```

---

## 17. Relationship to D_R

`D_R = 1` (unchanged, established in `S1_B1_REQUIRED_CORE_FIELD_ADJUDICATION.md`). This task did not touch `D_R`.

---

## 18. Relationship to D_I

```text
D_I = 1
INDIVIDUAL_PROVIDER_ALLOWLIST_READY_FOR_RESEARCHER_FREEZE
```

`D_I` transitions from `0` to `1` as a result of this task's provider gate evaluation (§16).

---

## 19. Relationship to S1-B1 Authorization

```math
G_{B1}^{\mathrm{authorize}}=\mathbf 1\left[G_{B1}^{\mathrm{decision}}=1\land D_R=1\land D_I=1\right]=\mathbf 1[1\land 1\land 1]=1.
```

All three preconditions of `G_{B1}^{authorize}` are now satisfied. **This does not itself authorize S1-B1.** Per the instruction's explicit rule (§16) and the researcher's stated sequence, a separate, later researcher authorization decision must still be recorded and frozen before any bibliographic lookup begins. `S1-B1 AUTHORIZED` is not written anywhere in this document.

```text
S1-B1: PLANNED_ONLY / NOT_AUTHORIZED
```

---

## 20. Stop Conditions

None triggered:

```text
official provider identity could not be verified:         NO (6/6 verified)
official domain indistinguishable from unofficial mirror:  NO
metadata scope unclear:                                     NO
terms/access boundary unclear:                               PARTIAL for PROV-04 only, and handled by downgrading its approved method/role rather than approving it on an unclear basis
credentials required without authorization:                  YES for PROV-04's API tier — handled by restricting that provider to its no-auth pathway, not approving the credentialed one
API endpoint guessed:                                        NO
undocumented rate limit invented:                             NO
target titles/authors/identifiers queried:                    NO
source content appeared in results and needed opening:        NO
source download initiated:                                    NO
provider conflict resolved without review:                    N/A (no conflict evaluated, no target record exists)
provider approved solely from a search snippet:                NO
URL or provider fact fabricated:                               NO
frozen planning registry modified:                             NO
claim created:                                                 NO
S1-B2 through S1-B5 begun:                                     NO
file staged:                                                   NO
```

No stop condition triggered. Final status is the success path.

---

## 21. Target-Lookup Nonauthorization

```text
S1-B1 target bibliographic lookup: NOT_EXECUTED, NOT_AUTHORIZED BY THIS TASK
```

No title, author, publication year, edition, volume, or identifier belonging to ET-01 through ET-13 was searched, viewed, or recorded in this task.

---

## 22. Retrieval and Content Nonauthorization

```text
source retrieval:        0
source-content access:   0
OCR / transcription:     0
document images viewed:  0
```

---

## 23. Downstream Batch Nonauthorization

```text
S1-B1: PLANNED_ONLY / NOT_AUTHORIZED (provider allowlist ready for freeze; execution still requires a separate authorization decision)
S1-B2: PLANNED_ONLY / NOT_AUTHORIZED
S1-B3: PLANNED_ONLY / NOT_AUTHORIZED
S1-B4: PLANNED_ONLY / NOT_AUTHORIZED
S1-B5: PLANNED_ONLY / NOT_AUTHORIZED
```

---

## 24. Final Status

```text
S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST_READY_FOR_RESEARCHER_FREEZE_EXECUTION_NOT_AUTHORIZED
```
