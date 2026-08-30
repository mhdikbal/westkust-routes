# Model 3B V2 — Artifact Index

**This is a navigation index only. It makes no new claims and changes no decision, status, formula, or identifier.**

## Authoritative baseline

Repository commit: `9da3d9fec04341e5fb71ecb934b8acdc59f7d044` (this housekeeping reorganization is layered on top of that baseline as an unstaged working-tree change — the commit itself remains the content-authoritative reference point until a future commit records this move).

## Status summary (verified against source files at the time this index was written)

| Item | Status |
|---|---|
| Model 3B-CD V1 | `MODEL_VALIDATION_FAILURE` |
| Historical inference | `NOT_AUTHORIZED` |
| Hawkes family | `NOT_RULED_OUT` |
| Phase D | `COMPLETED_VALID_NEGATIVE_RESULT` / `DO NOT RERUN` (9/9 arms, 90,000 simulations) |
| Wave 1 (spec-validation infrastructure) | committed, tests passing (25/25), not moved by this reorg — stays at `docs/thesis/colab/model3b_spec_validator/` |
| Wave 2 planning | frozen (10 planning contracts) |
| Open-decision ledger | 18 rows: 16 `OPEN_REQUIRES_ADJUDICATION`, 1 `DEFERRED` (**OD-016**, ROPE epsilon_n), 1 `NONBLOCKING_CLARIFICATION` |
| OD-005 | final decision `WITHHELD`; clarification classification `ADDITIVE_NONNUMERICAL_AMENDMENT_REQUIRED` |
| OD-006 | final decision `WITHHELD`; clarification classification `RESOLVABLE_BY_CROSS_DOCUMENT_RECONCILIATION`; substantive choice remains implementation-dependent |
| OD-015 | final decision `WITHHELD`; readiness `EVIDENCE_PARTIAL` |
| NUM-DEC ledger (8 decisions) | 7 `APPROVED_WITH_LIMITATIONS`, 1 `DEFERRED` (NUM-DEC-07, M3 ROPE) |
| tau (M3 threshold) | procedure approved (NUM-DEC-04), final numeric value `UNSET` |
| ROPE | `DEFERRED` (both at the NUM-DEC-07 and OD-016 level) |
| M3 implementation blockers | 8 `OPEN` (registry: `docs/thesis/colab/model3b_spec_validator/applicability_validator.py::get_m3_blockers()`, immutable `MappingProxyType`) |
| Combined future-test inventory | 315 substantive tests (121 amendment + 194 numerical-decision), `NOT EXECUTED` |

## Folder structure and function

```
model3b_v2/
├── README.md                 — this file
├── specifications/           — 5 frozen V2 specs (mathematical spec, gate spec, protocol,
│                                applicability matrix, numerical-decision ledger)
├── numerical_decisions/      — 8 NUM-DEC adjudication documents (NUM-DEC-01..08)
├── reconciliation/           — 70-to-51 gate reconciliation, numerical-decision digest,
│                                3 consistency-audit outputs
├── planning/                 — 10 Wave 2 planning contracts (mathematical contract,
│                                component map, coverage plan, blocker-closure protocol,
│                                tau preregistration, execution manifest, open-decision
│                                ledger, cross-document audit, dependency matrix,
│                                formula/symbol registry)
├── evidence/                 — literature-evidence package for OD-005/006/015 (search log,
│                                evidence ledger, evidence-to-option matrix, mathematical
│                                evidence review, adjudication readiness report)
├── adjudication/             — open-decision adjudication map + batch matrix, 4 draft
│                                adjudications (OD-005, OD-006, OD-015, cross-draft
│                                reconciliation), 3 specification-clarification review
│                                artifacts (OD-005, OD-006, cross-reconciliation)
├── validators/                — reserved for Wave 1 validator documentation; the Wave 1
│                                runtime Python package itself is deliberately NOT relocated
│                                here (see housekeeping report) and remains at
│                                docs/thesis/colab/model3b_spec_validator/
└── manifests/                 — this reorganization's own inventory, move manifest,
                                 checksum manifest, and housekeeping report
```

## Read-only / frozen rule

Every file under `specifications/`, `numerical_decisions/`, `reconciliation/`, `planning/`, `evidence/`, and `adjudication/` is a **frozen research record**. Do not edit their content. Path-only changes (like this reorganization) are the sole exception, and even those require content-hash verification before and after (see `manifests/MODEL_3B_V2_MOVE_MANIFEST.csv`).

## Key artifacts (relative links from this file)

- Mathematical specification: [`specifications/MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md`](specifications/MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md)
- Numerical-decision ledger: [`specifications/MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv`](specifications/MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv)
- Open-decision ledger (16 open + 1 deferred + 1 nonblocking): [`planning/WAVE_2_OPEN_DECISION_LEDGER.csv`](planning/WAVE_2_OPEN_DECISION_LEDGER.csv)
- OD-005/006/015 adjudication drafts: [`adjudication/WAVE_2_OD_005_DRAFT_ADJUDICATION.md`](adjudication/WAVE_2_OD_005_DRAFT_ADJUDICATION.md), [`adjudication/WAVE_2_OD_006_DRAFT_ADJUDICATION.md`](adjudication/WAVE_2_OD_006_DRAFT_ADJUDICATION.md), [`adjudication/WAVE_2_OD_015_DRAFT_PROCEDURAL_CONTRACT.md`](adjudication/WAVE_2_OD_015_DRAFT_PROCEDURAL_CONTRACT.md)
- Specification-clarification reviews: [`adjudication/WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md`](adjudication/WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md), [`adjudication/WAVE_2_OD_006_SPECIFICATION_CLARIFICATION_REVIEW.md`](adjudication/WAVE_2_OD_006_SPECIFICATION_CLARIFICATION_REVIEW.md)
- This reorganization's housekeeping report: [`manifests/MODEL_3B_V2_HOUSEKEEPING_REPORT.md`](manifests/MODEL_3B_V2_HOUSEKEEPING_REPORT.md)

## Not relocated (stays outside `model3b_v2/`)

- Wave 1 runtime validator package: `docs/thesis/colab/model3b_spec_validator/`
- M0/M2/M3 estimation code: `docs/thesis/colab/model3b_tournament_harness/`
- CD-era simulator (pre-V2, historical): `docs/thesis/colab/model3b_cd_simulator/`
- Pre-V2 historical archive documents (Amendment series, CD-era plans/audits, Phase 0 material, original 70-row gate spec, etc.) remain at `docs/thesis/pilot_annotation/` — see `manifests/MODEL_3B_V2_ARTIFACT_INVENTORY.csv` for the full list with rationale.
