# S1-B0 — Metadata Reconciliation Authorization Decision

**Status:** DECISION RECORD AND LOCAL FREEZE ONLY. This document authorizes the scope of a future execution; it does not itself execute S1-B0.
**Authoritative baseline:** `a82f85c0779b67dfbfc3c5459e14fe47c9ca1630`
**Workstream:** `PAINAN_INDRAPURA_STRATEGIC_HISTORY_LAB`
**Sprint:** `S1`
**Task:** `S1-B0-AUTHORIZATION`

---

## 1. Scope

This turn records one decision only: batch `S1-B0` (Metadata reconciliation) is authorized to execute in a future, separate turn, strictly within the read-only bounds defined in Section 5. No batch is executed by this document. No registry is modified. No source content is accessed. No network request is made.

---

## 2. Authoritative Baseline

Baseline commit: `a82f85c0779b67dfbfc3c5459e14fe47c9ca1630` (subject: "docs: freeze S1 execution preparation and mathematical contract").

Verified at the time of this decision:

```text
local HEAD    = a82f85c0779b67dfbfc3c5459e14fe47c9ca1630
origin/main   = a82f85c0779b67dfbfc3c5459e14fe47c9ca1630
server HEAD   = a82f85c0779b67dfbfc3c5459e14fe47c9ca1630
```

The baseline commit is already pushed to `origin/main` and server-synced to `westkust-prod:/home/ubuntu/westkust-routes`. No push or server sync is required to establish it; this decision builds on an already-synced baseline.

Authoritative inputs (tracked paths, resolved directly from Git at `docs/thesis/pilot_annotation/painan_indrapura_strategic_history_lab/planning/`):

```text
S1_EXECUTION_PREPARATION_MASTER_SPEC.md
S1_EXECUTION_TARGET_REGISTRY.csv
S1_EXECUTION_BATCH_REGISTRY.csv
S1_EXECUTION_PREPARATION_SPRINT_BOARD_UPDATE_DRAFT.md
S1_SOURCE_READINESS_MATHEMATICAL_AND_ESTIMAND_CONTRACT.md
```

---

## 3. Dependency-Graph Finding

From `S1_EXECUTION_BATCH_REGISTRY.csv`, the six batches form a strict dependency chain:

```text
S1-B0 -> S1-B1 -> S1-B2 -> S1-B4 -> S1-B5
                -> S1-B3 -> S1-B5
```

`S1-B0`'s `required_preconditions` field reads "S1 planning artifacts frozen and synced (already satisfied)" — it is the only batch whose precondition is already met without any prior batch authorization. Every other batch (`S1-B1`..`S1-B5`) requires `S1-B0`, directly or transitively, before it can be considered. `S1-B0` is therefore the unique root of the batch dependency graph.

---

## 4. Researcher Authorization

```text
S1-B0:                       AUTHORIZED
Batch name:                  Metadata reconciliation
Execution class:             LOCAL_METADATA_RECONCILIATION
Content access:              NO
Network access:              NO
Source modification:         NO
Registry modification:       NO
Claim creation:              NO
Historical inference:        NO
Source-class promotion:      NO
Downstream batch authorization: NO
Execution status:            NOT_STARTED
```

Authorizing S1-B0 must not be interpreted as authorization for any later batch.

```text
S1-B1: PLANNED_ONLY / NOT_AUTHORIZED
S1-B2: PLANNED_ONLY / NOT_AUTHORIZED
S1-B3: PLANNED_ONLY / NOT_AUTHORIZED
S1-B4: PLANNED_ONLY / NOT_AUTHORIZED
S1-B5: PLANNED_ONLY / NOT_AUTHORIZED
```

---

## 5. Authorized Metadata Operations

A future S1-B0 execution may inspect only filesystem and registry metadata needed to verify:

```text
1. whether each declared path exists
2. exact path spelling
3. path normalization consistency
4. filename consistency
5. duplicate path references
6. candidate duplicate-file references based only on already recorded metadata
7. retrieval-ID references
8. work-package-ID references
9. registry-to-filesystem agreement
10. the previously declared path_exists distribution
```

---

## 6. Content-Access Prohibition

A future S1-B0 execution must not:

```text
open source-file content
read DOCX, PDF, image, CSV, Markdown, or archive contents
unzip or extract files
calculate content-derived hashes
run OCR
parse document metadata from file internals
```

---

## 7. Network Prohibition

A future S1-B0 execution must not:

```text
access external websites
perform bibliographic lookup
retrieve sources
```

S1-B0's own registry row already declares `content_access=NO`, `network_access=NO` for all 18 targets under this batch's scope.

---

## 8. Source and Registry Immutability

A future S1-B0 execution must not:

```text
copy, move, rename, delete, or create source files
modify either frozen registry (S1_EXECUTION_TARGET_REGISTRY.csv, S1_EXECUTION_BATCH_REGISTRY.csv)
instantiate a claim ledger
create historical claims
promote source admissibility
begin S1-B1, S1-B2, S1-B3, S1-B4, or S1-B5
touch Custe De Manancabo.docx
```

`Custe De Manancabo.docx` status, verified at the time of this decision and required to remain unchanged through S1-B0 execution:

```text
UNTRACKED
UNSTAGED
UNMODIFIED
UNTOUCHED
```

---

## 9. S1-B1 through S1-B5 Nonauthorization

No operation in this decision, and no operation a future S1-B0 execution may perform, authorizes:

```text
S1-B1 Bibliographic identity review        — remains PLANNED_ONLY / NOT_AUTHORIZED
S1-B2 Local source-position indexing       — remains PLANNED_ONLY / NOT_AUTHORIZED
S1-B3 External source retrieval            — remains PLANNED_ONLY / NOT_AUTHORIZED
S1-B4 Repository-derived artifact audit    — remains PLANNED_ONLY / NOT_AUTHORIZED
S1-B5 Methodology gates                    — remains PLANNED_ONLY / NOT_AUTHORIZED
```

Each requires its own separate, later authorization decision once its own precondition is actually met.

---

## 10. Success Criteria

A future S1-B0 execution may later be classified `COMPLETE` only if:

```text
1. all 18 target rows are accounted for
2. the live filesystem agrees with the frozen path_exists values
3. YES remains 13
4. NO remains 5
5. no duplicate target ID exists
6. no dangling retrieval ID exists
7. no dangling work-package ID exists
8. no undeclared path substitution occurs
9. no file content is accessed
10. no source or registry is modified
```

---

## 11. Stop Conditions

A future S1-B0 execution must stop immediately if:

```text
any declared path_exists value differs from the live filesystem
a declared path is ambiguous
an expected file is missing unexpectedly
an undeclared duplicate path is found
a dangling ID appears
a target requires content access to resolve
a source file must be opened to decide identity
a registry correction appears necessary
any tracked or protected artifact changes
```

A discrepancy must produce:

```text
S1_B0_METADATA_RECONCILIATION_REQUIRES_REVIEW
```

The registry must not be corrected automatically.

---

## 12. Expected Execution Output

When S1-B0 is later executed (a separate turn, after this authorization is frozen and server-synced), it should produce a short report of this form:

```text
S1-B0 RESULT:
COMPLETE or REQUIRES_REVIEW

TARGETS CHECKED:
18/18

PATH_EXISTS AGREEMENT:
18/18

DECLARED YES:
13

DECLARED NO:
5

LIVE YES:
13

LIVE NO:
5

DANGLING IDS:
0

CONTENT ACCESSED:
0

NETWORK REQUESTS:
0

FILES MODIFIED:
0

REGISTRIES MODIFIED:
0

DOWNSTREAM BATCHES STARTED:
0
```

The expected frozen baseline this report will be checked against (declared values, not execution results — the future B0 execution must independently verify them):

```text
execution targets                 = 18
batches                            = 6
declared path_exists YES           = 13
declared path_exists NO            = 5
dangling retrieval IDs             = 0
dangling work-package IDs          = 0
fabricated paths                   = 0
all targets before this decision   = PLANNED_ONLY
all batches before this decision   = PLANNED_ONLY
```

---

## 13. Production Isolation

This decision, and the future S1-B0 execution it authorizes, touch only repository-tracked planning documentation. Neither this decision nor S1-B0 itself may:

```text
change backend, frontend, API, or database code
change Atlas, Painan prototype, or Indrapura dossier content
change Model 3B or OP-10
rebuild, restart, or reload any container
run a migration or seed script
```

`westkust-prod` containers and production runtime state are unaffected by this decision.

---

## 14. Decision Status

```text
S1_B0_METADATA_RECONCILIATION_AUTHORIZED_NOT_STARTED
```

---

## 15. Mathematical Reconciliation Contract

**Provenance:** this section was appended additively to the authorization record above, prior to remote publication of commit `cc745ec661ea6eb547bea0fc89c699875c31373c`, under the permanent Mathematical-Contract-in-Markdown rule: every brainstorming, plan, authorization, and execution instruction with a formal decision process must carry its relevant mathematical definitions inside the Markdown artifact itself, not only in chat, terminal prose, or executable code. Sections 1-14 above are unmodified; their authorization wording and history stand as originally recorded. This section formalizes Sections 5, 10, and 11 as mechanically testable indicator functions and gates. It does not execute S1-B0, does not modify the frozen registries, and does not constitute a historical claim.

### 15.1 Target set

```math
T=\{t_1,\dots,t_{18}\},\qquad |T|=18.
```

### 15.2 Path-agreement indicators

For each target `t_i`, define the frozen-registry status:

```math
r_i=
\begin{cases}
1 & \text{registry declares } \mathrm{path\_exists}=\mathrm{YES}\\
0 & \text{registry declares } \mathrm{path\_exists}=\mathrm{NO}
\end{cases}
```

and the live-filesystem status:

```math
f_i=
\begin{cases}
1 & \text{declared path exists on the live filesystem}\\
0 & \text{otherwise}
\end{cases}
```

Agreement indicator:

```math
a_i=\mathbf{1}[r_i=f_i].
```

Total agreement and discrepancy count:

```math
A=\sum_{i=1}^{18}a_i,
\qquad
D=\sum_{i=1}^{18}|r_i-f_i|.
```

Required declared distribution (from `S1_EXECUTION_TARGET_REGISTRY.csv`, frozen at baseline `a82f85c0779b67dfbfc3c5459e14fe47c9ca1630`):

```math
\sum_{i=1}^{18} r_i = 13,
\qquad
\sum_{i=1}^{18} (1-r_i) = 5.
```

Required live distribution, to be independently verified at S1-B0 execution time (not assumed equal to the declared distribution by this contract):

```math
\sum_{i=1}^{18} f_i = 13,
\qquad
\sum_{i=1}^{18} (1-f_i) = 5.
```

Success requires:

```math
A=18
\qquad\text{and}\qquad
D=0.
```

### 15.3 Dangling-reference indicators

Let `R` be the valid retrieval-ID set and `W` the valid work-package-ID set, both as declared in `S1_EXECUTION_TARGET_REGISTRY.csv` and `S1_EXECUTION_BATCH_REGISTRY.csv` at baseline. Let `rho(t_i)` denote the retrieval-ID reference of `t_i` and `omega(t_i)` its work-package-ID reference, where applicable.

```math
d_i^R=\mathbf{1}[\rho(t_i)\notin R],
\qquad
d_i^W=\mathbf{1}[\omega(t_i)\notin W].
```

```math
D_R=\sum_{i=1}^{18} d_i^R,
\qquad
D_W=\sum_{i=1}^{18} d_i^W.
```

Required:

```math
D_R=0,
\qquad
D_W=0.
```

Null/reference convention: as verified against the frozen registry at baseline, every one of the 18 targets carries a non-blank `retrieval_id` (`R-01`..`R-18`) and a non-blank `work_package_id`; no target uses a null-ID convention. No ID may be invented if this changes at execution time — an unexpected blank must be treated as `d_i^R=1` or `d_i^W=1`, not silently excluded from the sum.

### 15.4 Target-ID uniqueness

Let `id(t_i)` be the execution-target ID.

```math
U_T=\left|\{\,id(t_i):t_i\in T\,\}\right|,
\qquad
D_T=|T|-U_T.
```

Required:

```math
D_T=0.
```

### 15.5 Normalized-path duplicate candidates

Let `p_i` denote the declared path of `t_i`, and `N(\cdot)` a lexical path-normalization function (case/whitespace/separator normalization only). `N` must not resolve file content, compare hashes, follow undocumented substitutions, move/rename a path, or infer identical content from identical normalized form.

```math
D_P=|T|-\left|\{\,N(p_i):t_i\in T\,\}\right|.
```

If `D_P>0`, the result is not an automatic content-identity classification:

```text
D_P > 0  =>  DUPLICATE_PATH_CANDIDATE_REQUIRES_REVIEW
```

### 15.6 Content, network, and mutation boundaries

For each target, define content access:

```math
c_i=\mathbf{1}[\text{file content of } t_i \text{ is accessed}].
```

Required:

```math
\sum_{i=1}^{18} c_i = 0.
```

Let `N_{\mathrm{network}}` be the total count of network requests. Required:

```math
N_{\mathrm{network}}=0.
```

Let `M_{\mathrm{source}}`, `M_{\mathrm{registry}}`, `M_{\mathrm{claim}}`, `M_{\mathrm{promotion}}`, `M_{\mathrm{downstream}}` be, respectively, the counts of source files modified, frozen registries modified, claim entries created, source-class promotions, and downstream batches (S1-B1..S1-B5) started. Required:

```math
M_{\mathrm{source}}=0,\quad
M_{\mathrm{registry}}=0,\quad
M_{\mathrm{claim}}=0,\quad
M_{\mathrm{promotion}}=0,\quad
M_{\mathrm{downstream}}=0.
```

### 15.7 Complete success indicator

```math
G_{B0}=\mathbf{1}\Big[
A=18 \;\land\; D=0 \;\land\; D_R=0 \;\land\; D_W=0 \;\land\; D_T=0
\;\land\; \textstyle\sum_i c_i=0 \;\land\; N_{\mathrm{network}}=0
\;\land\; M_{\mathrm{source}}=0 \;\land\; M_{\mathrm{registry}}=0
\;\land\; M_{\mathrm{claim}}=0 \;\land\; M_{\mathrm{promotion}}=0
\;\land\; M_{\mathrm{downstream}}=0
\Big].
```

```text
G_B0 = 1  =>  future execution status may be S1_B0_METADATA_RECONCILIATION_COMPLETE
G_B0 = 0  =>  future execution status must be S1_B0_METADATA_RECONCILIATION_REQUIRES_REVIEW
```

`G_{B0}` does not execute the batch and does not constitute a historical claim. It is evaluated only by a future, separately authorized S1-B0 execution turn.

### 15.8 Stop conditions

The future execution must stop immediately if any of the following holds:

```math
D>0 \;\lor\; D_R>0 \;\lor\; D_W>0 \;\lor\; D_T>0 \;\lor\; \textstyle\sum_i c_i>0
\;\lor\; N_{\mathrm{network}}>0 \;\lor\; M_{\mathrm{source}}>0 \;\lor\; M_{\mathrm{registry}}>0
\;\lor\; M_{\mathrm{claim}}>0 \;\lor\; M_{\mathrm{promotion}}>0 \;\lor\; M_{\mathrm{downstream}}>0
\;\lor\; D_P>0.
```

The `D_P>0` branch requires review because it identifies duplicate *path* candidates, not proven duplicate *content*; it must not be auto-resolved.

### 15.9 Formula scope

```text
These formulas govern metadata reconciliation only.
They do not estimate a historical parameter.
They do not establish source admissibility.
They do not validate source content.
They do not create a claim.
They do not authorize S1-B1 through S1-B5.
They do not execute Hawkes, game theory, or any other model.
```
