# S1-B1 — Required-Core Bibliographic Field-Set Adjudication

**Status:** ADJUDICATION RECORD ONLY. Resolves the `D_R` blocker (class-specific required-core field sets reviewed and approved). Does not access the network, perform bibliographic lookup, retrieve or open source content, populate the provider allowlist, or authorize S1-B1 execution.

**Authoritative baseline:** `77a77c8c730d98c4d55a01ce658b32479b412a54`
**Workstream:** `PAINAN_INDRAPURA_STRATEGIC_HISTORY_LAB`
**Sprint / Batch:** `S1` / `S1-B1`

---

## 1. Purpose

Resolve `D_R = 0` (class-specific required-core bibliographic field sets reviewed and approved) by classifying every bibliographic-class × field pair by role, justifying every hard identifier and required-core designation, and documenting the one target-specific override. `D_I` (individual provider allowlist) is explicitly untouched and remains `0`.

---

## 2. Baseline Verification

```text
local HEAD = origin/main = 77a77c8 — matched
S1-B0:              COMPLETE_WITH_PATH_DOMAIN_CLARIFICATION
S1-B1:               PLANNED_ONLY / NOT_AUTHORIZED
Matching method:     RULE_BASED_CONJUNCTIVE_IDENTITY_GATE
Weighted score:      DEFERRED_NOT_REQUIRED
Global coverage threshold: NOT_SELECTED
Provider classes:    APPROVED_WITH_LIMITATIONS
Individual provider allowlist: PENDING_PREEXECUTION_FREEZE
```

All matched; adjudication proceeded.

---

## 3. Target and Class Domain

```math
T_{B1}=\{t_1,\dots,t_{10}\},\qquad |T_{B1}|=10.
```

Bibliographic-class distribution, recomputed mechanically from `S1_B1_BIBLIOGRAPHIC_IDENTITY_TARGET_MATRIX.csv` (not copied from the instruction without checking):

```text
PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION: 1   (ET-01)
UNVERIFIED_REFERENCE: 6                    (ET-03, ET-04, ET-05, ET-06, ET-07, ET-08)
CITED_ONLY_NOT_YET_LOCATED: 2               (ET-10, ET-13)
LOCAL_FILE_IDENTITY_REVIEW / CITED_ONLY_NOT_YET_LOCATED: 1  (ET-12)
```

Matches the instruction's expected distribution exactly (1/6/2/1). `B = {PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION, UNVERIFIED_REFERENCE, CITED_ONLY_NOT_YET_LOCATED, LOCAL_FILE_IDENTITY_REVIEW / CITED_ONLY_NOT_YET_LOCATED}`, `|B|=4`. No target or class added, removed, merged, or renamed.

---

## 4. Field Universe

```math
F=\{f_1,\dots,f_K\},\qquad K=12.
```

Reconstructed exactly from `S1_B1_BIBLIOGRAPHIC_IDENTITY_REVIEW_PLAN.md` §4 (not invented):

```text
title, author_or_corporate_author, publication_year, edition, volume, issue, publisher,
repository_or_catalogue_identity, persistent_identifier, catalogue_record_url, language,
physical_or_digital_format
```

`4 classes × 12 fields = 48` class-field rows, all recorded in `S1_B1_BIBLIOGRAPHIC_FIELD_ROLE_MATRIX.csv` — verified mechanically: 48 rows, 0 duplicate class-field pairs, 0 missing class-field pairs, exactly one role per pair.

---

## 5. Applicability and Role Functions

```math
a_{bk}=\mathbf 1(f_k\text{ is applicable to class }b),\qquad r_b(f_k)\in\{H,R,O,N\}.
```

```math
a_{bk}=0\iff r_b(f_k)=N,\qquad a_{bk}=1\iff r_b(f_k)\in\{H,R,O\}.
```

Verified over all 48 rows: every `NOT_APPLICABLE_TO_CLASS` row has `applicability=0`; every other row has `applicability=1`. No field carries two roles within the same class (0 duplicate class-field pairs).

Role distribution by class (from the field-role matrix):

```text
PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION:                   H=1, R=4, O=7, N=0
UNVERIFIED_REFERENCE:                                     H=1, R=3, O=6, N=2
CITED_ONLY_NOT_YET_LOCATED:                                H=1, R=3, O=7, N=1
LOCAL_FILE_IDENTITY_REVIEW / CITED_ONLY_NOT_YET_LOCATED:   H=1, R=2, O=3, N=6
```

Each row sums to 12, matching `K`.

---

## 6. Hard-Identifier Gate

```math
H_i=\{f_k:r_{b(i)}(f_k)=H\text{ and }f_k\text{ applicable to }t_i\}.
```

By class, `repository_or_catalogue_identity` is the sole hard identifier for all four classes — justified per class in `S1_B1_BIBLIOGRAPHIC_FIELD_ROLE_MATRIX.csv` (`hard_identifier_reason` column, non-empty for all 4 `HARD_IDENTIFIER` rows). No field is declared hard without class-specific justification; title, author, and year are never hard identifiers in any class.

**Target-specific override — ET-10 only:**

```text
target ID:        ET-10
field:             persistent_identifier
change:            added as HARD_IDENTIFIER (class default for CITED_ONLY_NOT_YET_LOCATED is NOT_APPLICABLE_TO_CLASS)
reason:            ET-10 is a modern PhD thesis (Kathirithamby-Wells, cited window 1760-85), unlike ET-13 (Vogel, 1690) which is a 17th-century source with no DOI/repository-handle expectation. A modern thesis plausibly carries an institutional-repository handle or DOI, so persistent_identifier is class-inapplicable by default but target-applicable here.
source planning artifact: S1_B1_RESEARCHER_DECISION_ADJUDICATION.md §7 (row ET-10, hard_identifier_fields = persistent_identifier, repository_or_catalogue_identity); frozen S1_EXECUTION_TARGET_REGISTRY.csv row ET-10 (source IS-08, "Confirm whether the Kathirithamby-Wells PhD thesis... is in-window")
researcher-review status: CARRIED FORWARD FROM PRIOR ADJUDICATION, RESTATED HERE FOR FIELD-ROLE-MATRIX CONSISTENCY — not newly introduced by this turn
```

This is the only override in the batch. No override was created to make a candidate easier to confirm — it narrows eligibility (adds a hard-identifier requirement), it does not relax one.

```math
C_{ij}=\sum_{f_k\in H_i}\mathbf 1(o_{ijk}=1\land m_{ijk}=0),\qquad\text{required } C_{ij}=0.
```

A missing hard identifier is not automatically a contradiction — it may instead make confirmation impossible for that target's class, consistent with the outcome taxonomy (`NO_ELIGIBLE_IDENTITY_CANDIDATE`, not a forced contradiction).

---

## 7. Required-Core Set

```math
R_b=\{f_k:r_b(f_k)=R\}.
```

```text
PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION:                   title, publication_year, edition, publisher
UNVERIFIED_REFERENCE:                                     title, author_or_corporate_author, volume
CITED_ONLY_NOT_YET_LOCATED:                                title, author_or_corporate_author, publication_year
LOCAL_FILE_IDENTITY_REVIEW / CITED_ONLY_NOT_YET_LOCATED:   title, author_or_corporate_author
```

For target `t_i`: `R_i = R_{b(i)} \cup R_i^{override}`. Only ET-10 carries an override, and it is to `H_i` (§6), not to `R_i` — `R_i^{override} = \emptyset` for all 10 targets; `R_i = R_{b(i)}` exactly.

No required-core set is empty. `UNVERIFIED_REFERENCE` requires `volume` per §9.2 of the instruction (multi-volume series, each CD target names one specific volume) — confirmed in the field-role matrix (`volume` = `REQUIRED_CORE_METADATA` for `UNVERIFIED_REFERENCE`, not optional). `PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION` requires `edition` and `publication_year` — protects against merging distinct printings of Het Painansch Contract.

---

## 8. Required-Core Completeness and Agreement (not evaluated)

```math
K_{ij}^{\mathrm{req}}=\prod_{f_k\in R_i}o_{ijk},\qquad M_{ij}^{\mathrm{req}}=\prod_{f_k\in R_i}m_{ijk},\qquad E_{ij}=\mathbf 1\left[C_{ij}=0\land K_{ij}^{\mathrm{req}}=1\land M_{ij}^{\mathrm{req}}=1\right].
```

Not evaluated in this turn — no lookup has occurred, so no candidate record `y_{ij}` exists to compute `o_{ijk}`/`m_{ijk}` against.

---

## 9. Class-Specific Review

### 9.1 Published primary source or document edition (ET-01)

Required-core (`title, publication_year, edition, publisher`) distinguishes a specific bibliographic manifestation, matching the frozen registry's own stop condition ("stop if no external catalogue/publisher record confirms the edition"). No rule in this field set permits merging distinct editions merely because titles match — `edition` and `publication_year` are both required-core, independently of title agreement.

### 9.2 Unverified reference (ET-03..ET-08)

Required-core (`title, author_or_corporate_author, volume`) is sufficient to determine whether the cited CD-volume reference corresponds to one identifiable bibliographic object. `volume` is required-core, not optional, for every one of the 6 CD targets, since each names a specific volume (CD1..CD6) — protects against a volume-number mismatch being silently accepted.

### 9.3 Cited only, not yet located (ET-10, ET-13)

Required-core (`title, author_or_corporate_author, publication_year`) is conservative and limited to what is already frozen in the citing material (Kathirithamby-Wells / Vogel names and years are already cited in the dossier, not invented here). No author, date, publisher, repository, or identifier is invented for either target. A record may legitimately remain `ONE_CANDIDATE_UNVERIFIED` or `NO_CANDIDATE_FOUND`.

### 9.4 Local file identity review / cited only, not yet located (ET-12)

This adjudication addresses only the external bibliographic identity component (`title, author_or_corporate_author` required-core; `repository_or_catalogue_identity` hard). The local file-content identity component (whether a locally-traced git-history file corresponds to the confirmed bibliographic object) remains explicitly out of S1-B1 scope, since content access is prohibited. `Custe De Manancabo.docx` was not inspected in producing this document.

---

## 10. Optional Corroborating Fields

```math
O_b=\{f_k:r_b(f_k)=O\}.
```

Per-class optional sets are listed in full in `S1_B1_BIBLIOGRAPHIC_FIELD_ROLE_MATRIX.csv`. No optional-field agreement count is converted into a hidden weighted score anywhere in this document or the matrix — optional fields cannot compensate for `C_{ij}>0`, `K_{ij}^{req}=0`, or `M_{ij}^{req}=0`; this is stated as a hard rule, not merely implied.

---

## 11. Diagnostic Coverage

```math
Q_{ij}=\frac{\sum_{k=1}^{K}a_{ik}o_{ijk}}{\sum_{k=1}^{K}a_{ik}},\qquad K_i^{\mathrm{app}}=\sum_{k=1}^{K}a_{ik}>0.
```

Status unchanged: `DIAGNOSTIC_ONLY`, `NO_GLOBAL_NUMERICAL_THRESHOLD`. No identity is derived from `Q_{ij}` anywhere in this adjudication.

---

## 12. Field-Set Adjudication Gate

| Indicator | Meaning | Value | Evidence |
|---|---|---|---|
| `F_K` | Exact field universe reconstructed | 1 | §4 — K=12, no invented field |
| `F_A` | Class-field applicability complete | 1 | §5 — 48/48 rows, applicability consistent with role |
| `F_H` | Hard-identifier roles justified | 1 | §6 — all 4 HARD_IDENTIFIER rows carry a non-empty reason |
| `F_R` | Required-core sets complete and nonempty where needed | 1 | §7 — 4/4 classes have nonempty `R_b`; volume/edition protections confirmed |
| `F_O` | Optional fields separated from required fields | 1 | §10 — distinct role column, no compensation rule |
| `F_N` | Not-applicable fields explicit | 1 | §5 — 9 `NOT_APPLICABLE_TO_CLASS` rows across the 4 classes, all explicit |
| `F_T` | All ten targets map to a reviewed class and field set | 1 | §3, §7 — 10/10 targets covered via their class's `R_b`/`H_b` |
| `F_X` | All overrides explicit | 1 | §6 — the single ET-10 override fully documented (target ID, field, change, reason, source, review status) |
| `F_0` | Zero network/content/retrieval/claim/registry mutation/downstream execution occurred | 1 | §16 below |

```math
G_{B1}^{\mathrm{field}}=\mathbf 1[F_K=F_A=F_H=F_R=F_O=F_N=F_T=F_X=F_0=1]=1.
```

```text
D_R = 1
REQUIRED_CORE_FIELD_SETS_APPROVED_WITH_LIMITATIONS
```

This gate does not authorize network execution.

---

## 13. Relationship to B1 Authorization Gate

```math
G_{B1}^{\mathrm{authorize}}=\mathbf 1\left[G_{B1}^{\mathrm{decision}}=1\land D_I=1\land D_R=1\right].
```

This task changed only `D_R` (0→1). `D_I` (individual provider allowlist frozen) remains untouched:

```math
D_I=0.
```

Therefore, even with `D_R=1`:

```math
G_{B1}^{\mathrm{authorize}}=\mathbf 1[1\land 0\land 1]=0.
```

**S1-B1 remains not authorized.**

---

## 14. Stop-Condition Check

```text
field universe fails to reconcile:               NO (K=12, matches plan §4)
target count differs from 10:                     NO
any target lacks a class:                          NO (10/10 mapped)
class has contradictory field roles:                NO (0 duplicate class-field pairs)
required-core set empty without justification:      NO (4/4 classes nonempty)
hard identifier lacks applicability support:         NO (4/4 justified)
volume-specific target omits volume from required:  NO (UNVERIFIED_REFERENCE.volume = REQUIRED_CORE_METADATA)
manifestation-specific target merges distinct editions: NO (PUBLISHED_PRIMARY.edition = REQUIRED_CORE_METADATA)
override lacks frozen-metadata support:              NO (ET-10 override cites S1_B1_RESEARCHER_DECISION_ADJUDICATION.md + frozen target registry)
numerical weight or global threshold introduced:      NO
field value/URL/identifier/provider result fabricated: NO
network request made:                                NO
source content accessed:                             NO
retrieval begun:                                     NO
registry changed:                                    NO
claim created:                                       NO
S1-B2 through S1-B5 begun:                            NO
file staged:                                          NO
```

No stop condition triggered.

---

## 15. Batch-Level Estimands (unchanged, not computed)

```math
|T_{B1}|=10 \text{ (fixed denominator)}; \qquad z_i, u_i, h_i, v_i, e_i \text{ all undefined pending lookup execution.}
```

---

## 16. Prohibited-Operation Counters

```text
network requests               = 0
bibliographic queries executed  = 0
source-content files opened     = 0
sources retrieved/downloaded    = 0
individual providers populated  = 0 (allowlist remains schema-only, PENDING_PREEXECUTION_FREEZE)
claims created                  = 0
registry rows modified          = 0
downstream batches started      = 0
```

---

## 17. Final Status

```text
S1_B1_REQUIRED_CORE_FIELD_SETS_ADJUDICATED_PROVIDER_ALLOWLIST_STILL_PENDING
```

---

## 18. Provider Allowlist Verification Update (appended additively)

**Provenance:** appended after §1-17 above (unmodified) following a separate controlled-web provider-verification turn. Full detail: `S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST.csv` (6 providers verified via controlled, provider-level-only web access), `S1_B1_PROVIDER_ALLOWLIST_VERIFICATION_AUDIT.md`.

```text
individual_provider_allowlist:  D_I = 1 (was 0)
```

```math
G_{B1}^{\mathrm{authorize}}=\mathbf 1\left[G_{B1}^{\mathrm{decision}}=1\land D_I=1\land D_R=1\right]=1.
```

S1-B1 remains not authorized; a separate researcher authorization decision and a separate freeze of the provider allowlist/planning package remain outstanding. Updated final status: `S1_B1_INDIVIDUAL_PROVIDER_ALLOWLIST_READY_FOR_RESEARCHER_FREEZE_EXECUTION_NOT_AUTHORIZED`.
