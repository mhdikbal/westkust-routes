# WAVE 2 — Adjudication Readiness Report: OD-005, OD-006, OD-015

> **Status: EVIDENCE-PREPARATION ONLY. NOT AN ADJUDICATION.** No decision status is changed by this document. Baseline: `deb949470d9e39322897d1a44ec8eeab33656f96`.

---

## 1. Purpose

This report synthesizes `WAVE_2_OD_005_006_015_EVIDENCE_LEDGER.csv`, `WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv`, and `WAVE_2_OD_005_006_015_MATHEMATICAL_EVIDENCE_REVIEW.md` into a form usable by an independent future review to determine — but not to itself determine — whether OD-005, OD-006, and OD-015 can be:

1. adjudicated from frozen sources and methodological literature;
2. given only a procedural contract;
3. given only a candidate-set determination;
4. given a provisional decision with limitations;
5. left as implementation-dependent; or
6. left as calibration-dependent.

---

## 2. Minimum Evidence Coverage Check (instruction Section 12)

| Decision | ≥2 verifiable sources | ≥1 foundational/canonical | ≥1 modern/evaluative | ≥1 adversarial/limiting | ≥1 explicit Model-3B applicability assessment | Target met |
|---|---|---|---|---|---|---|
| OD-005 | YES (E-001, E-003; E-004/E-008 metadata-only, not counted toward "verifiable") | YES (E-001, and E-004 by lineage though access-limited) | partial (E-003 is current/maintained software, not a new empirical evaluation) | partial (no source *opposes* AbsBias_c directly — the adversarial check instead confirms RelBias's undefinedness, i.e. supports the exclusion of the rejected option) | YES (Section 3 of mathematical-evidence-review) | **YES, with the modern/evaluative and adversarial columns thin — disclosed, not concealed** |
| OD-006 | YES (E-001, E-002, E-003) | YES (E-001) | YES (E-002, 2025) | YES (E-002 vs. E-001/E-003 — genuine tension, see Section 3 below) | YES | **YES, fully met** |
| OD-015 | YES for seed/provenance/versioning sub-questions (E-005); NOT fully met for the checkpoint/restart-determinism sub-question specifically (E-006/E-007 abstract-only, one search-engine claim explicitly excluded as unverified) | YES (E-005) | NO — no verified modern evaluative source for the restart-determinism sub-question | YES (E-005's own scope explicitly excludes restart determinism — a real gap, reported as such) | YES | **PARTIALLY MET — reported honestly, not papered over** |

---

## 3. Adversarial Evidence Check (instruction Section 9)

### OD-005

- Supporting: E-001 (relative bias undefined at zero; absolute bias standard alternative), E-003 (field-standard tooling computes both as distinct measures).
- Limiting/opposing: none found that argues against `AbsBias_c` specifically; the "opposing" evidence instead confirms the exclusion of the already-rejected `RelBias_c` option is well founded.
- Conditions under which the recommendation could fail to apply: if a future implementation's optimizer produces `n_hat_cr` values that are themselves unstable or badly scaled near the boundary (a **boundary-behavior** and **numerical-precision** dependency, per instruction Section 9 item 4) — `AbsBias_c` as a summary statistic does not itself diagnose that instability; it would need to be reported alongside the boundary-solution and profile-optimization-failure taxonomy already specified in `WAVE_2_MATHEMATICAL_CONTRACT.md`'s failure taxonomy.
- External-validity gap: E-001/E-003 are written for general (not point-process-specific, not Hawkes-specific) simulation studies; no source reviewed here evaluates `AbsBias_c` specifically for a branching-ratio parameter of an exponential-kernel Hawkes process at annual resolution.

### OD-006

- Supporting `Coverage_c`: E-001 (structural match via notation mapping), E-003 (field-default implementation behavior).
- Limiting/opposing: **E-002 directly** — if M2's future failures are informative (correlated with `n_c`, e.g. concentrated near `n_c=0` or under weak `beta` identification, both explicitly flagged as risk factors in `MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md` and NUM-DEC-02's own text), a valid-only-denominator `Coverage_c` computed without its mandatory `FailureRate_c` companion could overstate reliability.
- Conditions under which either recommendation could fail: `Coverage_c` risks overstatement under **informative missingness** (dependency: model misspecification / boundary behavior / weak identifiability, per instruction Section 9 item 4); `CoverAndValid_c` risks conflating "no interval formed" with "interval formed but wrong" unless cross-tabulated against the failure taxonomy, and would additionally require reconciling the already-frozen `0.925–0.975` target band in NUM-DEC-02, which was written assuming the `Coverage_hat` (valid-denominator) convention.
- External-validity gap: neither E-001 nor E-002 evaluates a profile-likelihood-based confidence set for a Hawkes branching ratio specifically; both are written for general parametric point/interval estimators.

### OD-015

- Supporting: E-005 for seed/provenance/versioning/archiving.
- Limiting/opposing: E-005's own scope explicitly excludes checkpoint/restart determinism (confirmed via direct full-text query, not assumed).
- Conditions under which the recommendation could fail: a single-process reproducibility framework (E-005) may not transfer cleanly to a **parallel/distributed** execution context (the manifest schema in `WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md` anticipates multiple workers/methods `m` with a seed hierarchy `s_{c,r,m}` per the governing Wave 2 instruction Section 13.4) — this is a **simulation-design** dependency (instruction Section 9 item 4) not resolved by E-005.
- External-validity gap: E-005 is written for general computational-biology pipelines, not specifically for checkpointed Monte Carlo recovery studies with per-cell/per-replication/per-method seed hierarchies.

---

## 4. Per-Decision Adjudication-Readiness Classification

*(Values restricted to the six allowed in instruction Section 7; never `APPROVED`/`REJECTED`/`RESOLVED`/`CLOSED`/`PASS`/`FAIL`.)*

| decision_id | option | adjudication_readiness |
|---|---|---|
| OD-005 | `AbsBias_c` (OPT-005-A) | `EVIDENCE_SUFFICIENT_FOR_REVIEW` |
| OD-005 | unspecified alternative (OPT-005-B) | `SPECIFICATION_CLARIFICATION_REQUIRED` |
| OD-006 | `Coverage_c` (OPT-006-A) | `EVIDENCE_SUFFICIENT_FOR_REVIEW` |
| OD-006 | `CoverAndValid_c` (OPT-006-B) | `SPECIFICATION_CLARIFICATION_REQUIRED` |
| OD-015 | structural estimate / manifest design (OPT-015-A) | `EVIDENCE_PARTIAL` |

**Supporting/contradicting evidence counts** (from the evidence-to-option matrix, counted mechanically):

| decision_id | option | supporting_evidence_ids (count) | contradicting_evidence_ids (count) |
|---|---|---|---|
| OD-005 | OPT-005-A | E-001, E-003 (2) | none (0) |
| OD-005 | OPT-005-B | none (0) | none (0) |
| OD-006 | OPT-006-A | E-001, E-003 (2) | E-002 partial (1, disclosed as cautionary not flat) |
| OD-006 | OPT-006-B | E-002 (1) | E-003 (1) |
| OD-015 | OPT-015-A | E-005 (1, partial scope) | none (0) |

**Unresolved evidence gaps identified**: 3 —
(1) OD-005's `OPT-005-B` names no concrete formula and cannot be evaluated;
(2) OD-006's downstream consequence for NUM-DEC-02's already-frozen `0.925–0.975` `Coverage_hat` target band if `CoverAndValid_c` were ever adopted is not derived here (out of this task's authorization);
(3) OD-015's checkpoint/restart-determinism sub-question has no verified literature support in this package (E-006/E-007 abstract-only; the ParaMonte deterministic-restart claim from an earlier search-engine summary is explicitly excluded as unverified).

---

## 5. Five-Way Resolution-Type Classification (instruction Section 8)

This is a **classification for future review, not an adjudication**, refining — without modifying — the nonblocking observation already recorded in `WAVE_2_OPEN_DECISION_ADJUDICATION_MAP.md`.

### OD-005

- **`CANDIDATE_SET_DETERMINATION`** — the literature confirms the candidate set is well-formed: `RelBias_c` is correctly excluded (undefined at `n_c=0`, confirmed by E-001), and `AbsBias_c` is a standard-practice substitute.
- **`PROVISIONAL_DECISION_WITH_LIMITATIONS`** — a future adjudication turn could plausibly approve `AbsBias_c` with the limitation that it must always be reported jointly with `R_valid,c`/`FailureRate_c` (already mandated by NUM-DEC-01) and with the boundary/profile-failure taxonomy.
- Reasoning/dependency: depends on `REQ-M2-005` and the already-frozen `NUM-DEC-01` denominator rules; does not depend on unresolved M3 blockers or on tau/ROPE.

### OD-006

- **`CANDIDATE_SET_DETERMINATION`** — both `Coverage_c` and `CoverAndValid_c` are well-formed, literature-attested measures; the candidate set itself is not in question.
- **`IMPLEMENTATION_DEPENDENT_FINAL_DECISION`** — whether M2's actual failure modes turn out to be informative (the condition under which E-002's caution becomes decisive) cannot be established without running the corrected M2 implementation (post-NUM-DEC-06's confirmed blockers) and observing real failure patterns — this is precisely why the ledger's own `resolution_stage` field already says "future adjudication turn," not "resolved by literature alone."
- **`PROVISIONAL_DECISION_WITH_LIMITATIONS`** — a future turn could plausibly adopt `Coverage_c` (matching the already-frozen NUM-DEC-02 target band) provisionally, with the explicit limitation that `FailureRate_c`/`R_attempted,c`/`R_valid,c` must always accompany it, and that a **post-hoc informativeness check** (comparing failure rates across `n_c` values) should be run once real recovery data exists — a future check, not performed here.
- Reasoning/dependency: depends on `REQ-M2-008`, the already-frozen NUM-DEC-01/02 conventions, and (for the informativeness check) on the eight M3-adjacent... **no** — on M2's own future corrected-implementation behavior, which is a separate, M2-specific implementation dependency, not one of the eight M3 blockers.

### OD-015

- **`PROCEDURAL_CONTRACT`** — the manifest schema itself (`WAVE_2_EXECUTION_MANIFEST_AND_STOP_RULES.md` S1) is a well-specified procedural contract for what fields a future manifest must carry.
- **`IMPLEMENTATION_DEPENDENT_FINAL_DECISION`** — the specific checkpoint/restart-determinism mechanism is, on the evidence gathered here, more naturally resolved by implementation-time engineering (choice of a checkpointing library/pattern verified for bit-identical restart) than by further literature search alone — E-005 does not cover it, and no verified alternative source does either.
- Reasoning/dependency: depends on `REQ-CROSS-001` and NUM-DEC-08's resource-envelope framework (all 8 ceiling dimensions still `PENDING_MEASUREMENT`) — this decision's final resolution is naturally sequenced *after* NUM-DEC-08's own measurement turn, consistent with the ledger's `resolution_stage: future measurement turn`.

---

## 6. Citation and Dependency Resolution Results

- **Citation-resolution result**: of 8 evidence records, 5 carry a resolvable stable identifier that was checked against a live source in this session (E-001 DOI via PMC mirror; E-002 DOI/arXiv id via arXiv PDF; E-003 URL via official docs page; E-005 DOI via PLOS open-access page; E-006/E-007 DOI/arXiv id resolve to real abstract pages but full text was not verified). E-004 and E-008 have resolvable identifiers (DOI, journal citation) confirmed via search-engine metadata but their content was **not** independently verified — both explicitly marked `METADATA_ONLY` and excluded from any supporting/contradicting claim.
- **Dependency-resolution result**: every `upstream_dependency`/`downstream_impact` reference used in the evidence ledger and evidence-to-option matrix (`REQ-M2-005`, `REQ-M2-008`, `REQ-M2-009`, `REQ-CROSS-001`, `NUM-DEC-01`, `NUM-DEC-02`, `NUM-DEC-08`) resolves to a real row/document in the frozen Wave 2 / NUM-DEC corpus — checked directly against `WAVE_2_REQUIREMENT_DEPENDENCY_MATRIX.csv` and the cited NUM-DEC documents. No dangling reference found. No dependency cycle is possible here since this package only *reads* the existing dependency graph and adds no new requirement nodes to it.

---

## 7. Explicit Non-Claims (repeated for emphasis)

No final decision status is set anywhere in this evidence package. `OD-005`, `OD-006`, and `OD-015` remain `OPEN_REQUIRES_ADJUDICATION` in `WAVE_2_OPEN_DECISION_LEDGER.csv`, unmodified by this work. No numeric value (tau, `epsilon_n`, any threshold/tolerance/bootstrap count/profile-likelihood grid/prior/temperature ladder) is selected anywhere in this package. `NUM-DEC-07` remains `DEFERRED`. All eight M3 implementation blockers remain `OPEN`. None of the 315 substantive future tests were executed. This package is an input to a future independent review, not that review's conclusion.

---

## 8. Final Status

```text
MODEL_3B_V2_OD_005_006_015_LITERATURE_EVIDENCE_READY_FOR_REVIEW
```

This status does not mean OD-005, OD-006, or OD-015 have been adjudicated.
