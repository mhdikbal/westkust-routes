# S1-B1 — Researcher Decision Adjudication

**Status:** DECISION RECORD ONLY. Resolves three open S1-B1 planning decisions (matching architecture, coverage architecture, provider-class governance). Does not authorize or execute bibliographic lookup, network access, source-content access, retrieval, or claim entry. Does not modify any frozen registry.

**Authoritative baseline:** `77a77c8c730d98c4d55a01ce658b32479b412a54`
**Workstream:** `PAINAN_INDRAPURA_STRATEGIC_HISTORY_LAB`
**Sprint / Batch:** `S1` / `S1-B1`

---

## 1. Scope

Adjudicate exactly three open S1-B1 planning decisions:

1. matching architecture (weighted vs. rule-based identity matching);
2. coverage architecture (minimum comparable-field coverage);
3. provider-class governance (provider allowlist structure).

This turn records planning decisions only.

---

## 2. Authoritative Baseline

```text
S1-B0:              COMPLETE_WITH_PATH_DOMAIN_CLARIFICATION (commit 77a77c8, pushed/server-synced)
S1-B1:               PLANNED_ONLY / NOT_AUTHORIZED
S1-B2 through S1-B5: PLANNED_ONLY / NOT_AUTHORIZED
```

Verified against `S1_B1_AUTHORIZATION_READINESS_AUDIT.md` §2 and current `git rev-parse HEAD` = `origin/main` = `77a77c8`. Baseline matched; adjudication proceeded.

Target domain, mechanically reconciled (unchanged from the planning turn):

```math
T_{B1}=\{t_1,\dots,t_{10}\},\qquad |T_{B1}|=10.
```

`ET-01, ET-03, ET-04, ET-05, ET-06, ET-07, ET-08, ET-10, ET-12, ET-13` — matches `S1_B1_BIBLIOGRAPHIC_IDENTITY_TARGET_MATRIX.csv` exactly; no target added, removed, merged, or substituted.

---

## 3. Open Decisions

```text
1. matching architecture      -> ADJUDICATED THIS TURN
2. coverage architecture      -> ADJUDICATED THIS TURN
3. provider-class governance  -> ADJUDICATED THIS TURN
(class-specific required-core fields and individual provider allowlist remain open — §13)
```

---

## 4. Matching Architecture Decision

```text
PRIMARY_MATCHING_METHOD:   RULE_BASED_CONJUNCTIVE_IDENTITY_GATE
WEIGHTED_SCORE:            DIAGNOSTIC_ONLY_NOT_AUTHORIZED_FOR_IDENTITY_CONFIRMATION
NUMERICAL_FIELD_WEIGHTS:   NOT_SELECTED
```

No numerical weights `w_k` are assigned. The weighted score:

```math
S_{ij}=\frac{\sum_k w_k a_{ik}o_{ijk}m_{ijk}}{\sum_k w_k a_{ik}o_{ijk}}
```

remains documented as a possible diagnostic concept only. It cannot override `C_{ij}>0`, cannot itself produce `IDENTITY_CONFIRMED`, and cannot merge editions, volumes, repositories, or archival objects.

```text
WEIGHTED_SCORE_DEFERRED_NOT_REQUIRED_FOR_S1_B1
```

---

## 5. Field Applicability

Unchanged from `S1_B1_BIBLIOGRAPHIC_IDENTITY_REVIEW_PLAN.md` §4:

```math
a_{ik}=\mathbf 1(\text{field }k\text{ is applicable to target }t_i),\qquad
o_{ijk}=\mathbf 1(y_{ijk}\text{ is observed}).
```

Field universe `K=12` (§4 of the plan). No field applicability was changed by this adjudication.

---

## 6. Hard-Identifier Gate

```math
m_{ijk}=\mathbf 1\left[N_k(x_{ik})=N_k(y_{ijk})\right].
```

Let `H_i` be the applicable hard-identifier set for target `i` (from `S1_B1_BIBLIOGRAPHIC_IDENTITY_TARGET_MATRIX.csv`, column `hard_identifier_fields`):

```text
ET-01:            repository_or_catalogue_identity
ET-03..ET-08:      repository_or_catalogue_identity
ET-10:             persistent_identifier, repository_or_catalogue_identity
ET-12, ET-13:      repository_or_catalogue_identity
```

Hard contradiction count:

```math
C_{ij}=\sum_{k\in H_i}\mathbf 1(a_{ik}=1\land o_{ijk}=1\land m_{ijk}=0).
```

Required: `C_{ij}=0` for every candidate proceeding to identity adjudication. No field can override a hard-identifier contradiction — not the weighted score (§4), not high coverage (§8), not provider rank (§9).

---

## 7. Required-Core Completeness

Let `R_i` be the target-class-specific required-core metadata field set. `R_i` is not invented — it is proposed here from the frozen metadata schema and each target's exact needs (full field-by-field table in `S1_B1_BIBLIOGRAPHIC_IDENTITY_TARGET_MATRIX.csv`, columns `required_core_fields` / `optional_corroborating_fields`), and **remains subject to researcher review before S1-B1 execution authorization** (blocker 1, §13).

Every proposed field is labeled one of: `HARD_IDENTIFIER`, `REQUIRED_CORE_METADATA`, `OPTIONAL_CORROBORATING_METADATA`, `NOT_APPLICABLE_TO_CLASS`.

| target_id | bibliographic_class | HARD_IDENTIFIER | REQUIRED_CORE_METADATA | OPTIONAL_CORROBORATING_METADATA | NOT_APPLICABLE_TO_CLASS |
|---|---|---|---|---|---|
| ET-01 | PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION | repository_or_catalogue_identity | title, publisher, publication_year, edition | author_or_corporate_author, volume, issue, catalogue_record_url, language, physical_or_digital_format, persistent_identifier | (none) |
| ET-03..ET-08 | UNVERIFIED_REFERENCE (CD1-CD6) | repository_or_catalogue_identity | title, volume, author_or_corporate_author (compiling institution) | catalogue_record_url, language, physical_or_digital_format, edition | issue, persistent_identifier |
| ET-10 | CITED_ONLY_NOT_YET_LOCATED (modern thesis) | persistent_identifier, repository_or_catalogue_identity | title, author_or_corporate_author, publication_year | language, edition, volume, issue, catalogue_record_url, physical_or_digital_format | (none) |
| ET-12 | LOCAL_FILE_IDENTITY_REVIEW / CITED_ONLY_NOT_YET_LOCATED | repository_or_catalogue_identity | title, author_or_corporate_author | publication_year, language | persistent_identifier, edition, volume, issue, catalogue_record_url, physical_or_digital_format (until a candidate is found) |
| ET-13 | CITED_ONLY_NOT_YET_LOCATED | repository_or_catalogue_identity | title, author_or_corporate_author, publication_year | language | persistent_identifier, edition, volume, issue, catalogue_record_url, physical_or_digital_format (until a candidate is found) |

Required-core completeness and agreement:

```math
K^{\mathrm{req}}_{ij}=\prod_{k\in R_i}o_{ijk},\qquad M^{\mathrm{req}}_{ij}=\prod_{k\in R_i}m_{ijk}.
```

`K^{req}_{ij}=1` only when every required-core field is observed; `M^{req}_{ij}=1` only when every required-core field agrees after approved normalization.

Rule-based candidate eligibility gate:

```math
E_{ij}=\mathbf 1\left[C_{ij}=0\land K^{\mathrm{req}}_{ij}=1\land M^{\mathrm{req}}_{ij}=1\right].
```

A candidate may proceed to identity adjudication only if `E_{ij}=1`. No `R_i` set here is empty; none requires a `REQUIRES_RESEARCHER_REVIEW` exception marker.

---

## 8. Coverage Decision

```text
GLOBAL_NUMERICAL_COVERAGE_THRESHOLD: NOT_SELECTED
PRIMARY_SUFFICIENCY_RULE:            CLASS_SPECIFIC_REQUIRED_FIELD_COMPLETENESS
Q_ij:                                DIAGNOSTIC_COVERAGE_ONLY
```

No universal threshold (0.50, 0.75, 0.80, 0.90, 1.00, or any other value) is adopted for all bibliographic classes.

```math
Q_{ij}=\frac{\sum_{k=1}^{K}a_{ik}o_{ijk}}{\sum_{k=1}^{K}a_{ik}},\qquad \text{provided }\sum_{k=1}^{K}a_{ik}>0.
```

Denominator is the applicable-field count for target `i`, not global `K`. `Q_{ij}` does not imply identity confirmation in either direction — a high `Q_ij` may still conceal a hard-identifier contradiction; a lower `Q_ij` may still support identity if the small set of bibliographically decisive fields is complete, consistent, and unique.

Primary evidence sufficiency gate:

```math
G^{\mathrm{suff}}_{ij}=\mathbf 1\left[E_{ij}=1\land U_{ij}=1\right],
```

where `U_ij=1` means the eligible candidate is unique among reviewed candidates. If `\sum_{j\in J_i}E_{ij}=1` then `U_ij=1` for that single candidate. If `\sum_{j\in J_i}E_{ij}=0`, status `NO_ELIGIBLE_IDENTITY_CANDIDATE`. If `\sum_{j\in J_i}E_{ij}>1`, status `MULTIPLE_CANDIDATES_AMBIGUOUS`. No candidate may be selected by score tie-breaking.

---

## 9. Provider-Class Governance

```text
PROVIDER_CLASS_HIERARCHY:        APPROVED_WITH_LIMITATIONS
INDIVIDUAL_PROVIDER_ALLOWLIST:   PENDING_PREEXECUTION_FREEZE
NETWORK_EXECUTION:               NOT_AUTHORIZED
```

Approved provider classes (conditional hierarchy, ranks 1-6, lower rank = more direct bibliographic authority, not historical truth):

```text
1. issuing repository or archival catalogue
2. publisher or journal record
3. DOI registration agency or equivalent persistent-identifier authority
4. national or university library catalogue
5. recognized bibliographic database
6. general search engine or secondary index — discovery only, cannot confirm identity by itself
```

Provider admissibility indicator:

```math
A_P(p)=\mathbf 1\left[\text{identity verified}\land\text{public access permitted}\land\text{no unapproved credentials}\land\text{terms/access recorded}\land\text{class assigned}\land\text{query purpose limited to bibliographic metadata}\right].
```

A provider enters the execution allowlist only if `A_P(p)=1`. No individual provider name, URL, catalogue ID, or API was fabricated, browsed, or verified in this turn — zero individual providers are listed. Proposed allowlist schema (populated with zero rows):

```text
provider_id, provider_name, provider_class, base_domain, metadata_scope, authentication_required,
credentials_authorized, terms_review_status, robots_or_rate_limit_status, approved_query_method,
identity_confirmation_role, status, notes
```

Any individual provider row, once drafted in a later turn, must remain `PENDING_PREEXECUTION_REVIEW` until independently verified and frozen.

---

## 10. Provider Conflict

For two records `y_ij^(p)` and `y_ij^(q)` on hard field `k`:

```math
V_{ij,k}^{(p,q)}=\mathbf 1\left[N_k(y_{ijk}^{(p)})\ne N_k(y_{ijk}^{(q)})\right],\qquad V_{ij}^{(p,q)}=\sum_{k\in H_i}V_{ij,k}^{(p,q)}.
```

If `V_ij^(p,q) > 0`, status `PROVIDER_METADATA_CONFLICT_REQUIRES_REVIEW`. The conflict is never silently resolved by choosing the record with the preferred provider rank.

---

## 11. Identity Confirmation Gate

```math
Z_i=\sum_{j\in J_i}E_{ij}.
```

Identity may be confirmed only if `Z_i=1`, `C_{ij}=0`, and there is no unresolved provider hard-field conflict (`V_ij^(p,q)=0`) for all admissible provider-record comparisons used for confirmation:

```math
G_i^{\mathrm{identity}}=\mathbf 1\left[Z_i=1\land C_{ij}=0\land K^{\mathrm{req}}_{ij}=1\land M^{\mathrm{req}}_{ij}=1\land V_{ij}^{(p,q)}=0\right].
```

If `G_i^identity=1`, status may be `IDENTITY_CONFIRMED`; otherwise identity remains unconfirmed or requires review. This is a bibliographic identity status only — it does not establish source admissibility, historical accuracy, or independent evidentiary support.

---

## 12. Batch-Level Estimands

Using fixed denominator `|T_{B1}|=10`:

```math
\widehat P_{\mathrm{confirmed}}=\tfrac{1}{10}\sum_i z_i,\quad
\widehat P_{\mathrm{ambiguous}}=\tfrac{1}{10}\sum_i u_i,\quad
\widehat P_{\mathrm{contradiction}}=\tfrac{1}{10}\sum_i h_i,\quad
\widehat P_{\mathrm{provider\_conflict}}=\tfrac{1}{10}\sum_i v_i,\quad
\widehat P_{\mathrm{execution\_failure}}=\tfrac{1}{10}\sum_i e_i.
```

None of these estimands is computed in this turn — lookup has not been executed, so `z_i, u_i, h_i, v_i, e_i` are all undefined pending execution, not assumed zero.

---

## 13. Remaining Preexecution Decisions

Two blockers, not resolved by this adjudication, tracked separately:

```text
1. class-specific required-core field sets (R_i, §7 above) — drafted, PENDING RESEARCHER REVIEW
2. individual provider allowlist (§9 above) — schema drafted, zero rows populated, PENDING PREEXECUTION FREEZE
```

Both must be resolved and frozen, in that order, before the S1-B1 planning package itself is frozen and before any separate network-authorization decision is made.

---

## 14. Authorization-Readiness Gates

Decision-completeness indicators: `D_M` (matching architecture decided) = 1; `D_C` (coverage/sufficiency architecture decided) = 1; `D_P` (provider-class governance decided) = 1; `D_I` (individual provider allowlist frozen) = 0; `D_R` (class-specific required-field sets researcher-approved) = 0; `D_N` (normalization rules frozen) = 1; `D_X` (stop conditions complete) = 1; `D_E` (epistemic boundaries complete) = 1; `D_0` (zero network/content/retrieval/claim/registry mutation occurred) = 1.

```math
G_{B1}^{\mathrm{decision}}=\mathbf 1[D_M=D_C=D_P=D_N=D_X=D_E=D_0=1]=1.
```

```math
G_{B1}^{\mathrm{authorize}}=\mathbf 1\left[G_{B1}^{\mathrm{decision}}=1\land D_I=1\land D_R=1\right]=0.
```

`G_{B1}^{decision}=1` but `G_{B1}^{authorize}=0`, because the individual provider allowlist and class-specific required-field sets still require a separate preexecution freeze. **Final status must not be `AUTHORIZED`.**

---

## 15. Stop Conditions

None triggered this turn:

```text
ten target rows do not reconcile:                        NO (10/10 reconciled, §2)
rule-based matching cannot be represented w/o weights:    NO (E_ij gate defined without any w_k)
target lacks proposed class-specific field classification: NO (all 10 covered, §7)
hard contradiction overridden by another field:            NO (C_ij gate is absolute, §6)
global numerical coverage threshold inserted:               NO (§8 explicitly NOT_SELECTED)
individual provider approved without verification:          NO (zero rows populated, §9)
provider URL or identifier fabricated:                       NO
any query executed:                                          NO
any network request made:                                    NO
source content accessed:                                     NO
external retrieval begun:                                    NO
registries edited:                                            NO
claims created:                                               NO
S1-B2 through S1-B5 begun:                                    NO
any file staged:                                              NO
```

---

## 16. Network Nonauthorization

```text
NETWORK EXECUTION: NOT_AUTHORIZED
```

No network request was made to produce this adjudication. No bibliographic lookup was executed.

---

## 17. Retrieval Nonauthorization

No external source retrieval was performed or authorized. `ET-12`'s primary path (local git-history trace, per the frozen registry) remains unexecuted; its conditional network fallback remains unauthorized.

---

## 18. Claim and Registry Boundaries

```text
claims created:            0
registry rows modified:    0
source-content access:     0
```

`S1_EXECUTION_TARGET_REGISTRY.csv`, `S1_EXECUTION_BATCH_REGISTRY.csv`, and all other frozen G0/S1 artifacts remain byte-for-byte unchanged. `Custe De Manancabo.docx` remains untracked, unstaged, unmodified, untouched, content not inspected.

---

## 19. Downstream Batch Nonauthorization

```text
S1-B1: PLANNED_ONLY / NOT_AUTHORIZED (adjudicated, not executed)
S1-B2: PLANNED_ONLY / NOT_AUTHORIZED
S1-B3: PLANNED_ONLY / NOT_AUTHORIZED
S1-B4: PLANNED_ONLY / NOT_AUTHORIZED
S1-B5: PLANNED_ONLY / NOT_AUTHORIZED
```

---

## 20. Final Status

```text
S1_B1_RESEARCHER_DECISIONS_ADJUDICATED_EXECUTION_NOT_YET_AUTHORIZED
```

---

## 21. Blocker 1 Resolution Update (appended additively)

**Provenance:** appended after §1-20 above (unmodified) following a separate required-core field-review turn. Full detail: `S1_B1_BIBLIOGRAPHIC_FIELD_ROLE_MATRIX.csv`, `S1_B1_REQUIRED_CORE_FIELD_ADJUDICATION.md`.

Blocker 1 from §13 (class-specific required-core field sets, `R_i`) is now resolved: `D_R = 1`. Blocker 2 (individual provider allowlist, `D_I`) remains open and unchanged by this update.

```math
G_{B1}^{\mathrm{authorize}}=\mathbf 1\left[G_{B1}^{\mathrm{decision}}=1\land D_I=1\land D_R=1\right]=\mathbf 1[1\land 0\land 1]=0.
```

S1-B1 remains not authorized. Updated final status: `S1_B1_REQUIRED_CORE_FIELD_SETS_ADJUDICATED_PROVIDER_ALLOWLIST_STILL_PENDING`.

---

## 22. Blocker 2 Resolution Update (appended additively)

**Provenance:** appended after §1-21 above (unmodified) following a separate controlled-web provider-verification turn. Full detail: `S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv`, `S1_B1_PROVIDER_ALLOWLIST_VERIFICATION_AUDIT.md`.

Blocker 2 (individual provider allowlist, `D_I`) is now resolved: `D_I = 1`.

```math
G_{B1}^{\mathrm{authorize}}=\mathbf 1\left[G_{B1}^{\mathrm{decision}}=1\land D_I=1\land D_R=1\right]=1.
```

`G_{B1}^{authorize}` is now `1`, but S1-B1 remains not authorized — this gate expresses *readiness for authorization*, not authorization itself. A separate researcher authorization decision, and a separate freeze of both the provider allowlist and the full S1-B1 planning package, remain outstanding. Updated final status: `S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST_READY_FOR_RESEARCHER_FREEZE_EXECUTION_NOT_AUTHORIZED`.
