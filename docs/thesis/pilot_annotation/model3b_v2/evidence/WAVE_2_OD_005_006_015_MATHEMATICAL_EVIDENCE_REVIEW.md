# WAVE 2 — Mathematical Evidence Review: OD-005, OD-006, OD-015

> **Status: EVIDENCE-PREPARATION ONLY.** This document does not adjudicate OD-005, OD-006, or OD-015. It links external literature evidence (see `WAVE_2_OD_005_006_015_EVIDENCE_LEDGER.csv`) to the frozen Model 3B mathematical notation, using only the notation given in `MODEL_3B_V2_OD_005_006_015_LITERATURE_EVIDENCE_PREPARATION.md` Section 6 and `WAVE_2_MATHEMATICAL_CONTRACT.md`. Baseline: `deb949470d9e39322897d1a44ec8eeab33656f96`.

---

## 1. Verbatim Extraction of the Three Decisions

### OD-005

```text
decision_id: OD-005
topic: AbsBias as adopted exact-null acceptance metric
source_requirement: REQ-M2-005
mathematical_object: AbsBias_c
current_status: OPEN_REQUIRES_ADJUDICATION
candidate_options: AbsBias_c as proposed; a different exact-null-specific metric;
  RelBias with a regularized denominator (rejected in spec S8.4 discussion)
options_rejected: RelBias at n_c=0 (mathematically undefined, division by zero)
required_evidence: explicit researcher review confirming AbsBias against frozen
  NUM-DEC-01/02 documents
upstream_dependency: REQ-M2-005
downstream_impact: REQ-M2-008 (acceptance-criterion registry)
source_file: WAVE_2_OPEN_DECISION_LEDGER.csv (row OD-005);
  WAVE_2_OPEN_DECISION_ADJUDICATION_MAP.md (section OD-005)
```

### OD-006

```text
decision_id: OD-006
topic: Primary M2 coverage metric: Coverage_c vs CoverAndValid_c
source_requirement: REQ-M2-008
mathematical_object: Coverage_c, CoverAndValid_c
current_status: OPEN_REQUIRES_ADJUDICATION
candidate_options: Coverage_c (conditional on valid interval, always reported with
  failure rate); CoverAndValid_c (unconditional, attempted-denominator)
options_rejected: none formally rejected -- both remain candidates
required_evidence: cross-check against NUM-DEC-01/02's own metric-denominator language
upstream_dependency: REQ-M2-008
downstream_impact: REQ-M2-009 (MCSE target), acceptance-criterion registry
source_file: WAVE_2_OPEN_DECISION_LEDGER.csv (row OD-006);
  WAVE_2_OPEN_DECISION_ADJUDICATION_MAP.md (section OD-006)
```

### OD-015

```text
decision_id: OD-015
topic: Compute planning: storage estimate, checkpoint design, restart determinism,
  provenance manifest (Package H)
source_requirement: REQ-M3-015, REQ-CROSS-001
mathematical_object: n/a (infrastructure/reproducibility design, not a statistical
  formula question)
current_status: OPEN_REQUIRES_ADJUDICATION
candidate_options: symbolic/structural estimate scaled from Wave-1-era pilot logs;
  no benchmark executed
options_rejected: running an actual compute-cost benchmark in this planning turn
  (explicitly prohibited, S18 Package H)
upstream_dependency: REQ-CROSS-001
downstream_impact: NUM-DEC-08 resource-envelope framework (PENDING_MEASUREMENT)
source_file: WAVE_2_OPEN_DECISION_LEDGER.csv (row OD-015);
  WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md (S1-S2)
```

Cross-check performed: the "S8.4"/"S8.7" section references in `WAVE_2_OPEN_DECISION_ADJUDICATION_MAP.md` for OD-005/OD-006 refer to Section 8 of the *governing instruction* `MODEL_3B_V2_WAVE_2_PLANNING_INSTRUCTIONS.md` ("W2-P2: KONTRAK MATEMATIS M2", subsections 8.1-8.8), not to `WAVE_2_MATHEMATICAL_CONTRACT.md`'s own internal section numbering (where the equivalent content is at S2.3 and S2.6 respectively). Both numbering systems were checked and are mutually consistent in substance — **not a specification conflict**, no stop condition triggered.

---

## 2. Frozen Notation Actually Used (per instruction Section 6)

Only the following frozen objects are relevant to these three decisions:

```math
n=\frac{\alpha}{\beta}.
```

No other formula from instruction Section 6 (Hawkes intensity, log-likelihood, score, Hessian, profile likelihood `D(n)`, `H_0:n=0`, `M_0`/`M_1`, `BF_10`, `P(M_1\mid Y)`) is directly implicated by OD-005, OD-006, or OD-015 — these three decisions concern **recovery-metric reporting conventions for `n`** (OD-005/006) and **systems/reproducibility design** (OD-015), not the M0/M3 estimation contract itself. Per instruction Section 6's own directive ("Hanya gunakan formula yang relevan... Jangan memaksakan seluruh formula ke setiap keputusan"), the remaining M0/M3 formulas are deliberately not forced onto this review.

The frozen `WAVE_2_MATHEMATICAL_CONTRACT.md` formulas actually in scope (S2.3, S2.6, reproduced verbatim, not modified):

```math
\widehat{\operatorname{AbsBias}}_c = \frac{1}{R_{\mathrm{valid},c}}\sum_{r\in\mathcal V_c}\left|\widehat n_{cr}-n_c\right| \quad (\text{exact-null substitute}, n_c=0).
```

```math
\widehat{\operatorname{Coverage}}_c = \frac{1}{R_{\mathrm{valid},c}}\sum_{r\in\mathcal V_c}\mathbf 1\{n_c\in C_{cr}\}, \qquad \widehat{\operatorname{CoverAndValid}}_c = \frac{1}{R_{\mathrm{attempted},c}}\sum_{r=1}^{R_{\mathrm{attempted},c}}\mathbf 1\{\text{valid interval and }n_c\in C_{cr}\}.
```

---

## 3. Notation Mapping — Literature to Model 3B

### 3.1 Morris, White & Crowther (2019) — `E-001`

| source notation | source definition | Model 3B notation | mapping condition | exact or approximate |
|---|---|---|---|---|
| `theta` | true value of the estimand in one simulation scenario | `n_c` | one Model 3B "cell" `c` = one simulation scenario with a fixed true `n_c` | **exact** — a cell is defined exactly as a single scenario in the source's sense |
| `theta_hat_i` | per-replication point estimate, `i = 1..n_sim` | `n_hat_cr` | replication index `i` maps to `r`, scenario index absorbed into cell `c` | **exact** |
| `n_sim` | count of replications *that yielded a usable result* (source explicitly separates this from replications attempted when missingness occurs, per its ADEMP missingness-reporting requirement) | `R_valid,c` (structurally) | this mapping is the crux of OD-006: the source's own `n_sim` in its bias/coverage formulas is, by the source's own missingness-handling guidance, **conditioned on non-missing results** — i.e. it already resembles `R_valid,c`, not `R_attempted,c` | **approximate** — the source does not use Model 3B's three-way `R_attempted,c`/`R_valid,c`/`R_metric,c` distinction (from NUM-DEC-01) explicitly; the mapping is inferred from the source's missingness-reporting requirement, not from an identical notational system |
| `Coverage = (1/n_sim) sum 1(theta_hat_low,i <= theta <= theta_hat_upp,i)` | coverage performance measure | `Coverage_c` | direct structural match once `n_sim -> R_valid,c` mapping (above) is accepted | **approximate** (inherits the approximation above) |

### 3.2 Pawel, Bartoš, Siepe & Lohmann (2025) — `E-002`

This source does not introduce new notation requiring a mapping table — it argues in prose (not formula) that the denominator convention implicit in E-001's `n_sim` (i.e., a valid-only count) can be misleading when failures are informative, and recommends reporting on the full attempted set. No exact-vs-approximate mapping issue arises because no new symbol is introduced; the tension is at the level of **which existing Model 3B symbol** (`R_valid,c` vs `R_attempted,c`) should back the primary reported measure — this is precisely OD-006's open question, not resolved by notation alone.

### 3.3 Sandve, Nekrutenko, Taylor & Hovig (2013) — `E-005`

This source is prose guidance (reproducibility "rules"), not a mathematical framework — no formula-level notation mapping applies. Its Rule 6 ("random seed should be recorded") maps conceptually to the manifest schema's `master_seed`/`component_seed` fields (`WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md` S1), and its Rule 4 (script version control) maps to the schema's `code_commit_future` field — both **conceptual, not formula-level**, mappings.

**No parameter was equated with another merely because it uses the same symbol** — every mapping above states its exactness and, where approximate, states exactly what makes it approximate.

---

## 4. Summary of Evidentiary Bearing per Decision

**OD-005** (`AbsBias_c`): E-001 (Statistics in Medicine, 2019, peer-reviewed, FULL_TEXT_ACCESSED) states explicitly that relative bias is undefined for a true value of exactly zero and that an absolute-value bias measure is the standard substitute — this is a direct, on-point methodological match to `AbsBias_c`'s stated purpose ("exact-null substitute, `n_c=0`") in the frozen mathematical contract. E-003 (official `rsimsum` software documentation) corroborates that bias and relative bias are treated as distinct, separately computable measures in the field's standard tooling.

**OD-006** (`Coverage_c` vs `CoverAndValid_c`): the notation mapping in Section 3.1 shows E-001's own `n_sim`-based coverage formula structurally resembles `Coverage_c` (valid-only denominator) more closely than `CoverAndValid_c` (attempted denominator) — and this convention is already written, with an already-frozen target band, into `MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md` (`Coverage_hat`, `0.925 <= Coverage_hat <= 0.975`). E-003 corroborates this as the field's *default implemented* practice (`rsimsum`'s `na.rm=TRUE`). E-002 (2025, peer-reviewed) is a genuine adversarial/limiting source: it warns that a valid-only denominator can bias reported performance upward when failures are informative, and argues for careful, disclosed reporting rather than silent exclusion — which NUM-DEC-01 already structurally requires (mandatory joint `FailureRate_c` disclosure). No source in this package flatly contradicts NUM-DEC-01/02's existing convention; E-002 instead sharpens *why* the joint-disclosure requirement matters.

**OD-015** (compute-planning/manifest design): E-005 (PLOS Computational Biology, 2013, peer-reviewed, FULL_TEXT_ACCESSED) provides strong, direct support for the seed-recording, script-versioning, provenance-traceability, and intermediate-result-archiving components of the manifest schema already drafted in `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md`. It explicitly does **not** address checkpoint/restart determinism — a genuine, disclosed gap. Two further candidate sources (E-006, E-007) could not be verified past abstract-level access within this search session and are **not** used to fill that gap; the gap is reported honestly in the readiness report rather than papered over.

---

## 5. Non-Claims

This document does not claim, and none of the evidence above should be read as establishing:

- that `AbsBias_c` has been adjudicated as the final M2 exact-null acceptance metric;
- that `Coverage_c` has been adjudicated as the final primary M2 coverage metric;
- that OD-015's manifest design is complete or implementation-ready;
- any final PASS for M0, successful recovery/coverage for M2, or successful model selection for M3;
- any tau value, ROPE value, or closure of any of the eight M3 implementation blockers;
- authorization of historical-data inference or reversal of the V1 `MODEL_VALIDATION_FAILURE` status.

See `WAVE_2_OD_005_006_015_ADJUDICATION_READINESS_REPORT.md` for the per-option readiness classification and the five-way resolution-type classification, both of which are review inputs, not decisions.
