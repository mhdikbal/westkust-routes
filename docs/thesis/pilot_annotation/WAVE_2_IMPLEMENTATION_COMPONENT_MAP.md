# WAVE 2 Implementation Component Map (W2-P0 Readiness & Dependency Audit)

> **Status: PLANNING-ONLY.** No component in this document is implemented. This is the narrative companion to `WAVE_2_REQUIREMENT_DEPENDENCY_MATRIX.csv` (37 requirements, machine-verified 0 broken dependency references, 0 cycles).

## 1. Purpose

Map every frozen requirement (from the 5 V2 specs + 8 NUM-DEC adjudications) to: the mathematical object it constrains, the future implementation component that will realize it, the future validator that will check it, the future unit/simulation test that will exercise it, its current acceptance-criterion status, its failure classification, its dependencies, and its downstream impact. Full per-requirement detail is in the CSV; this document summarizes by future-component family and reports the W2-P0 gate result.

## 2. Future Component Families

| Component family | Realizes requirements | Depends on (Wave 1 reused) |
|---|---|---|
| M0-gate intensity/likelihood/compensator module | REQ-M0-001, REQ-M0-002 | none (new) |
| M0-gate score/Hessian/covariance module | REQ-M0-003 through REQ-M0-007 | none (new) |
| M0-gate aggregator (11-check gate) | REQ-M0-008 | above |
| M2 output-schema module (primary/diagnostic split) | REQ-M2-001 | Wave 1 `schema_validator.py` pattern (extend, do not modify) |
| M2 replication-accounting module | REQ-M2-002, REQ-M2-003 | Wave 1 `schema_validator.py` pattern |
| M2 failure-classification module | REQ-M2-004 | new (24-code taxonomy, §`WAVE_2_SIMULATION_AND_COVERAGE_PLAN.md`) |
| M2 bias/RMSE metric module | REQ-M2-005, REQ-M2-006 | none (new) |
| M2 profile-likelihood module | REQ-M2-007 | reuses M0-gate score/Hessian machinery for nuisance optimization |
| M2 coverage/MCSE module | REQ-M2-008, REQ-M2-009 | none (new) |
| M2 exact-null submodel + bootstrap-calibration module | REQ-M2-010, REQ-M2-011, REQ-M2-012 | Wave 1 `applicability_validator.py` procedure-vs-value pattern (extend for M2's own tau-equivalent bootstrap critical value) |
| M3 exact-null/alternative submodel module | REQ-M3-001 | **blocked**, M3-BLOCK-01 |
| M3 prior-odds configuration module | REQ-M3-002 | Wave 1 `parser.py`/`schema_validator.py` pattern |
| M3 marginal-likelihood/BF/posterior-probability module | REQ-M3-003 through REQ-M3-005 | **blocked**, M3-BLOCK-02/03/06 |
| M3 prior-specification module | REQ-M3-006 | **blocked**, M3-BLOCK-06 |
| M3 decision-rule module (tau) | REQ-M3-007 | Wave 1 `applicability_validator.py` `PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION` recognition (reuse directly) |
| M3 ROPE-absence validator | REQ-M3-008 | Wave 1 pattern (confirm pipeline runs with ROPE disabled) |
| M3 bridge-sampling module | REQ-M3-009 | **blocked**, M3-BLOCK-02/03/04/06 |
| M3 thermodynamic-integration module | REQ-M3-010, REQ-M3-011 | **blocked**, M3-BLOCK-05 |
| Simulation-design module (shared M2/M3) | REQ-M3-012 | none (new) |
| Tau-calibration evaluation module | REQ-M3-013, REQ-M3-014 | reuses M2 bootstrap-calibration machinery pattern |
| Seed-manifest module (shared M2/M3) | REQ-M3-015 | none (new) |
| M3 blocker registry | REQ-CROSS-001 | **already implemented in Wave 1**, `applicability_validator.get_m3_blockers()` — immutable, 8 entries, no closure code path exists |

## 3. Wave 1 Reuse Summary

Three Wave 1 patterns are explicitly designated for reuse rather than reinvention in any future implementation wave:

1. **Verbatim, no-silent-default parsing** (`parser.py`) — extend to M0/M2/M3 config/manifest formats.
2. **Procedure-vs-value distinction** (`applicability_validator.py`'s recognition of `PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION`) — the same pattern applies to M2's exact-null bootstrap critical value (also a procedure-resolved/value-pending situation) and should not be reimplemented separately.
3. **Immutable blocker registry** (`get_m3_blockers()`, `MappingProxyType`) — the closure protocol in `WAVE_2_M3_BLOCKER_CLOSURE_PROTOCOL.md` is designed to eventually replace individual entries only through a versioned, reviewed code change — never a runtime mutation.

## 4. W2-P0 Gate Result

| Condition (instruction §6.4) | Result |
|---|---|
| 1. every requirement has a sourced authoritative document | PASS — see `source_document`/`source_section` columns, `WAVE_2_REQUIREMENT_DEPENDENCY_MATRIX.csv` |
| 2. every symbol is defined | PASS — 38 rows, `WAVE_2_FORMULA_SYMBOL_REGISTRY.csv` |
| 3. no symbol has two substantive meanings without disambiguation | PASS — `M0`/`M1` flagged `AMBIGUOUS_DISAMBIGUATED_BELOW` with `PROPOSED_INTERNAL_LABEL`s (registry + `WAVE_2_MATHEMATICAL_CONTRACT.md` §S0) |
| 4. M0-as-validation-stage distinguished from `M_0` null model | PASS — §S0 disambiguation |
| 5. M2/M3 do not mix frequentist coverage with Bayesian posterior probability | PASS — M2 contract (§S2) is entirely frequentist (coverage, MCSE, bootstrap p-value); M3 Bayesian contract (§S3.3–S3.7) is entirely posterior-probability-based; no formula crosses families |
| 6. tau not treated as final | PASS — `REQ-M3-007` status is `PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION`, mechanically confirmed absent as a literal value anywhere in this Wave 2 output set (see `WAVE_2_CROSS_DOCUMENT_CONSISTENCY_AUDIT.md`) |
| 7. ROPE deferred | PASS — `REQ-M3-008`/`OD-016` both `DEFERRED_BY_NUM_DEC_07` |
| 8. 8 M3 blockers remain open | PASS — `REQ-CROSS-001`, all 8 `OPEN`, immutable registry unmodified |
| 9. 315 future tests unexecuted | PASS — 121 amendment (no status column, treated as unexecuted future-test inventory per instruction §2 note) + 194 numerical (`PLANNED_ONLY`) = 315, no test executed by this planning turn |
| 10. dependency graph acyclic | PASS — mechanically verified (`WAVE_2_CROSS_DOCUMENT_CONSISTENCY_AUDIT.md` §Mechanical) |

**W2-P0 gate: PASSED.** Proceeding to W2-P1 through W2-P9 was authorized.
