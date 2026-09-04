# S1 — Source Readiness Mathematical and Estimand Contract

**Status:** GOVERNANCE SPECIFICATION ONLY. This document defines mathematical objects, estimands, gates, stop rules, null controls, and future model boundaries. It does not authorize retrieval, indexing, content access, model fitting, simulation, or historical inference.

**Authoritative baseline:** `477182ea120331f2667c0eead2e7dea58bed477a`
**Workstream:** `PAINAN_INDRAPURA_STRATEGIC_HISTORY_LAB`
**Sprint:** `S1`
**Task:** `S1-EXECUTION-PREPARATION-FREEZE`

No count, proportion, confidence label, or future model input in this document may be treated as an estimated value, a historical finding, or an authorization to act.

---

## 1. Purpose

This contract closes a gap in prior planning: operational plans (`S1_EXECUTION_PREPARATION_MASTER_SPEC.md`, `S1_EXECUTION_TARGET_REGISTRY.csv`, `S1_EXECUTION_BATCH_REGISTRY.csv`, `S1_EXECUTION_PREPARATION_SPRINT_BOARD_UPDATE_DRAFT.md`) were detailed at the operational level without the mathematical estimands, decision rules, null models, and authorization gates made fully explicit. This document formally distinguishes:

```text
file availability
bibliographic identity
source identity
source admissibility
position resolution
claim admissibility
source coverage
source independence
colonial-classification risk
historical inference authorization
```

---

## 6.1 Sets and indices

```text
S = set of source records
B = set of unique bibliographic targets
F = set of local physical files
R = set of retrieval/indexing targets
W = set of work packages
C = set of future historical claims
A = set of actors
E = set of historical events
D = set of documents or document positions
```

Indices: `s in S`, `b in B`, `f in F`, `r in R`, `w in W`, `c in C`, `a in A`, `e in E`, `d in D`.

Current cardinalities under the frozen S1 planning inputs:

```text
|S| (Painan 1662-1663)            = 17  (PS-01..PS-17)
|S| (Indrapura-EIC 1680-1730)     = 8   (IS-01..IS-08, per G0 source gap report)
|R| (execution-target registry)   = 18
|W| (batch registry)               = 6
```

These are set-membership counts, not readiness or coverage claims.

---

## 6.2 Source-to-file and source-to-bibliographic mappings

```math
\phi:S\to F\cup\{\varnothing\}
```

```math
\beta:S\to B
```

Two source IDs are bibliographically equivalent when:

```math
s_i\sim_B s_j \iff \beta(s_i)=\beta(s_j).
```

The number of unique bibliographic targets is:

```math
N_B=|S/{\sim_B}|.
```

Verified current example:

```math
\beta(\mathrm{PS\mbox{-}06})=\beta(\mathrm{IS\mbox{-}07})=\mathrm{CD4}.
```

For the current unresolved source-class set:

```math
N_S^{\mathrm{UNVERIFIED}}=12,
\qquad
N_B^{\mathrm{UNRESOLVED}}=11.
```

This is a source-identity count, not a historical finding.

---

## 6.3 Availability indicators

```math
L_s=\mathbf{1}[\phi(s)\neq\varnothing]
```

```math
I_s=\mathbf{1}[\text{bibliographic identity verified}]
```

```math
E_s=\mathbf{1}[\text{edition identity resolved}]
```

```math
P_s=\mathbf{1}[\text{source position resolved}]
```

```math
Q_s=\mathbf{1}[\text{provenance chain complete}].
```

Explicit non-implications:

```math
L_s=1\not\Rightarrow I_s=1,
```

```math
I_s=1\not\Rightarrow E_s=1,
```

```math
E_s=1\not\Rightarrow P_s=1,
```

```math
\text{PathExists}(s)\not\Rightarrow\text{HistoricalAuthority}(s).
```

---

## 6.4 Source admissibility gate

```math
G_s^{\mathrm{source}}
=
L_s I_s E_s Q_s K_s,
```

where `K_s = 1` only when the declared source class is justified by recorded evidence.

For sources without a required local file, an alternative bibliographic-only gate must be defined explicitly rather than forcing `L_s=1`.

The exact gate is source-class dependent:

```math
G_s^{\mathrm{source}}=g_{k(s)}(L_s,I_s,E_s,P_s,Q_s,K_s),
```

where `k(s)` is the declared source class. No single universal rule applies across all source classes (`PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION`, `SECONDARY_SCHOLARSHIP`, `UNVERIFIED_REFERENCE`, `REPOSITORY_DERIVED_ARTIFACT`, `WORKING_RESEARCH_DATA`).

---

## 6.5 Claim-entry gate

```math
G_c^{\mathrm{claim}}
=
\mathbf{1}[
\text{source ID resolves}
\land
\text{source class declared}
\land
\text{source position resolved}
\land
\text{source relation declared}
\land
\text{confidence status declared}
\land
\text{colonial classification reviewed}
\land
\text{claim wording separated from source wording}
].
```

Required current state:

```math
\sum_{c\in C}G_c^{\mathrm{claim}}=0,
```

because claim entry is not authorized and no claim rows exist.

---

## 6.6 Coverage estimands

```math
\widehat{\Gamma}_{\mathrm{id}}
=
\frac{\sum_{s\in S} I_s}{|S|}.
```

```math
\widehat{\Gamma}_{\mathrm{edition}}
=
\frac{\sum_{s\in S} E_s}{|S|}.
```

```math
\widehat{\Gamma}_{\mathrm{position}}
=
\frac{\sum_{s\in S} P_s}{|S|}.
```

```math
\widehat{\Gamma}_{\mathrm{prov}}
=
\frac{\sum_{s\in S} Q_s}{|S|}.
```

These estimands are not computed in this turn because not all indicator values are frozen. Current result status:

```text
DEFINED_NOT_ESTIMATED
```

---

## 6.7 Case and source-class stratification

```math
\widehat{\Gamma}_{h,k}
=
\frac{\sum_{s\in S}\mathbf{1}[h(s)=h,k(s)=k]G_s^{\mathrm{source}}}
{\sum_{s\in S}\mathbf{1}[h(s)=h,k(s)=k]}.
```

Reporting must be by case (`h in {Painan 1662-1663, Indrapura-EIC 1680-1730}`) and source class, not only pooled totals, so that abundant repository-derived artifacts cannot mask weak primary or document-edition coverage.

---

## 6.8 Source independence and duplication

```math
s_i\sim_F s_j
\iff
\phi(s_i)=\phi(s_j)\neq\varnothing.
```

```math
N_{\mathrm{eff}}^{\mathrm{source}}
=
|S/{\sim_F,\sim_B}|,
```

with the exact quotient construction finalized only after identity review.

```text
Raw source-ID count must never be reported as independent-source count.
```

---

## 6.9 Colonial-classification risk

```math
Z_i^{\mathrm{colonial}}\in\{0,1,\mathrm{REQUIRES\_REVIEW}\}.
```

No colonial label may be treated as ground truth when `Z_i^{\mathrm{colonial}}=1` or unresolved.

```math
Y_i\sim p(Y_i\mid E_i,S_i,J_i),
```

where `E_i` is the latent event, `Y_i` the recorded label, `S_i` source position, and `J_i` institutional interest or classification regime. This is a future observation-model contract, not an estimated model.

---

## 6.10 Decision rules for S1 execution authorization

```math
A_b
=
\mathbf{1}[
\text{target set resolved}
\land
\text{input paths/references resolved}
\land
\text{output schema frozen}
\land
\text{rollback deterministic}
\land
\text{scope separately authorized}
].
```

A batch may execute only if `A_b=1`. Current state for all six registered batches:

```math
A_b=0\quad\forall b,
```

because this turn does not authorize execution.

---

## 6.11 Batch ordering relation

```math
b_i\prec b_j
```

when batch `b_j` requires an output of `b_i`. The future batch graph must be acyclic:

```math
\operatorname{CycleCount}(\mathcal{B},\prec)=0.
```

Metadata reconciliation is eligible to precede content and external access but is not authorized here.

---

## 6.12 Stop conditions

```math
H_b
=
\mathbf{1}[
\text{identity conflict}
\lor
\text{path conflict}
\lor
\text{unfrozen schema}
\lor
\text{unauthorized content access}
\lor
\text{source-class promotion without evidence}
\lor
\text{non-deterministic rollback}
].
```

Execution must stop whenever `H_b=1`.

---

## 6.13 Null and negative controls for future indexing

Specified, not run:

```text
NULL-01: no fabricated page or folio position
NULL-02: no source-class promotion from path existence alone
NULL-03: no duplicate physical file counted as an independent source
NULL-04: no claim row without source-position resolution
NULL-05: no colonial label silently converted into an event ontology value
```

```math
V=\sum_{j=1}^{5}\mathbf{1}[\mathrm{NULL\mbox{-}0j\ violated}].
```

Required for future batch acceptance:

```math
V=0.
```

---

## 6.14 Future game-theory boundary

```math
U_i(a,X_t)
=
B_i^{\mathrm{trade}}
+B_i^{\mathrm{security}}
+B_i^{\mathrm{legitimacy}}
+B_i^{\mathrm{faction}}
+B_i^{\mathrm{route}}
-C_i^{\mathrm{tribute}}
-C_i^{\mathrm{monopoly}}
-C_i^{\mathrm{dependency}}
-C_i^{\mathrm{war}}
-R_i^{\mathrm{retaliation}}.
```

```text
No numerical payoff is authorized.
No perfect-rationality assumption is authorized.
No equilibrium claim is authorized.
All terms remain qualitative components pending S5.
```

---

## 6.15 Future counterfactual boundary

```math
P(Y^{(s)}\mid E,\mathcal{A}_s),
```

```math
\mathcal{R}_s
=
\{Y^{(s)}(\theta):\theta\in\Theta_{\mathrm{source\mbox{-}supported}}\}.
```

```math
C(h+1)\le C(h).
```

```text
Counterfactual execution is NOT AUTHORIZED.
These formulas are governance placeholders for S6.
```

---

## 6.16 Future Hawkes boundary

```math
\lambda_k(t)
=
\mu_k(t)
+
\sum_j\sum_{t_i^{(j)}<t}
\alpha_{kj}q_i g_{kj}(t-t_i^{(j)}).
```

```text
mu_k(t) = baseline intensity
alpha_kj = candidate cross-excitation parameter
q_i = provenance/observability weight
g_kj = temporal kernel
```

```math
\text{temporal excitation}\not\Rightarrow\text{historical causation}.
```

```text
Hawkes family = NOT_RULED_OUT
Hawkes feasibility = DEFERRED_TO_G7
Model fitting = NOT AUTHORIZED
Historical inference = NOT AUTHORIZED
Phase D = DO NOT RERUN
```

(Phase D refers to the closed V1 Hawkes workstream: `FAILED_VALIDATION` / `RESEARCH_ONLY` / `INFERENCE_NOT_AUTHORIZED`, a completed valid negative result. It is referenced here only as a boundary condition, not reopened.)

---

## 6.17 Identifiability and authorization status

Every estimand or model object in this contract is classified as exactly one of:

```text
DEFINED_NOT_ESTIMATED
DEFERRED_TO_S5
DEFERRED_TO_S6
DEFERRED_TO_G7
NOT_IDENTIFIABLE_FROM_CURRENT_DATA
NOT_AUTHORIZED
```

Status assignment:

```text
Gamma_id, Gamma_edition, Gamma_position, Gamma_prov, Gamma_h,k = DEFINED_NOT_ESTIMATED
G_s^source, G_c^claim, A_b, H_b, N_eff^source        = DEFINED_NOT_ESTIMATED
Game-theory utility decomposition (Section 6.14)      = DEFERRED_TO_S5
Counterfactual target and envelope (Section 6.15)     = DEFERRED_TO_S6
Hawkes candidate intensity (Section 6.16)              = DEFERRED_TO_G7
Colonial observation model p(Y_i | E_i, S_i, J_i)      = NOT_AUTHORIZED
Any numeric historical payoff or equilibrium claim     = NOT_AUTHORIZED
```

No current numeric estimate is permitted.

---

## 7. Summary of Governance Scope

This document is additive and definitional. It does not:

- change any indicator, estimand, or gate value from its current unresolved/undefined state;
- authorize retrieval, indexing, extraction, claim entry, or modeling;
- alter the four execution-preparation artifacts it accompanies;
- alter the canonical sprint board or any frozen G0/S1 planning artifact.

Next authorized action after this freeze: controlled push and server sync of the five S1 execution-preparation artifacts (this file plus the four artifacts listed in Section 1). Batch execution remains unauthorized.
