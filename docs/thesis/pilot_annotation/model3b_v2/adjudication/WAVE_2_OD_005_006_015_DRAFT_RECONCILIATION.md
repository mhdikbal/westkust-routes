# Cross-Draft Reconciliation — OD-005, OD-006, OD-015 Adjudication Drafts

> **Status: DRAFTING-ONLY.** This document audits the three draft adjudications (`WAVE_2_OD_005_DRAFT_ADJUDICATION.md`, `WAVE_2_OD_006_DRAFT_ADJUDICATION.md`, `WAVE_2_OD_015_DRAFT_PROCEDURAL_CONTRACT.md`) for internal consistency against each other and against the frozen ledger/evidence package. It makes no adjudication of its own.

## 1. Candidate option consistency

Checked each draft's §4 ("Candidate options") against `WAVE_2_OPEN_DECISION_LEDGER.csv` and `WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv`:

| Decision | Ledger `candidate_options` | Matrix `option_id`s | Draft §4 | Match |
|---|---|---|---|---|
| OD-005 | `AbsBias_c` as proposed; a different exact-null-specific metric; `RelBias` regularized (rejected) | OPT-005-A, OPT-005-B | OPT-005-A, OPT-005-B, rejected RelBias variant | Consistent |
| OD-006 | `Coverage_c`; `CoverAndValid_c` | OPT-006-A, OPT-006-B | OPT-006-A, OPT-006-B | Consistent |
| OD-015 | symbolic/structural estimate (only concrete option); benchmark execution (rejected) | OPT-015-A | OPT-015-A, benchmark rejection noted | Consistent |

No draft introduces an option absent from the frozen ledger/matrix, and no frozen option is silently omitted from a draft.

## 2. Evidence-ID consistency

Evidence IDs cited per draft, cross-checked against `WAVE_2_OD_005_006_015_EVIDENCE_LEDGER.csv`:

- **OD-005 draft**: E-001, E-003 (substantive support), E-004 (bibliographic lead only). All three exist in the ledger under `decision_id` containing `OD-005`.
- **OD-006 draft**: E-001, E-002, E-003. All three exist in the ledger under `decision_id` containing `OD-006`.
- **OD-015 draft**: E-005 (primary substantive), E-006, E-007 (contextual/unverified only). All three exist in the ledger under `decision_id = OD-015`.

No draft cites an evidence_id outside `{E-001..E-007}`. No draft introduces a new evidence source. This was independently re-verified against the ledger (unchanged since `d363be7`, see §5 below) rather than merely asserted.

## 3. Source-access consistency

Each draft's treatment of access status matches the ledger's `access_status` column exactly:

- E-001, E-002, E-003, E-005: `FULL_TEXT_ACCESSED` — used for substantive claims, each scoped to what was actually verified (no draft extends a claim beyond the scope stated in the ledger's `exact_relevant_methodological_point`).
- E-004: `METADATA_ONLY` — used in the OD-005 draft exclusively as a bibliographic lead; no methodological claim is attributed to it.
- E-006, E-007: `ABSTRACT_ONLY` — used in the OD-015 draft exclusively as contextual/unverified citations; neither is cited for method detail, formula, threshold, default, or implementation recommendation.

Consistent with both prior narrow-review audits of this evidence package, which independently found 0 claim-access mismatches.

## 4. Mathematical notation consistency

All three drafts use notation exactly as frozen in `WAVE_2_MATHEMATICAL_CONTRACT.md`: `n = alpha/beta` (with `alpha`, `beta` diagnostic-only); `R_attempted,c = 1000`, `R_attempted,c = R_valid,c + sum_k R_failure,c,k`; `AbsBias_c`, `RelBias_c` (S2.3); `Coverage_c`, `CoverAndValid_c` (S2.6). No draft redefines a symbol, introduces a competing notation, or silently changes a formula's meaning. The OD-015 draft correctly declines to introduce any new mathematical notation, consistent with its ledger `mathematical_object = n/a`.

## 5. Denominator consistency

`R_valid,c`-based (conditional) and `R_attempted,c`-based (attempted/unconditional) denominators are kept explicitly distinct in both the OD-005 and OD-006 drafts:

- OD-005: `AbsBias_c` uses `R_valid,c` (per S2.3) and is required to be reported alongside `FailureRate_c` (attempted-denominator) — both drafts state this jointly-reported requirement, never presenting `AbsBias_c` in isolation.
- OD-006: the entire decision *is* the choice between a `R_valid,c`-denominator metric (`Coverage_c`) and an `R_attempted,c`-denominator metric (`CoverAndValid_c`) — the OD-006 draft preserves this distinction throughout and does not conflate the two or silently drop failed replications from either.

No draft reports a coverage or bias metric without its accompanying attempted-replication/failure-rate context, satisfying the governing instruction §5.3's explicit prohibition.

## 6. Resolution-type consistency

| Decision | Frozen classification (`WAVE_2_OPEN_DECISION_ADJUDICATION_MAP.md` / `WAVE_2_OD_005_006_015_ADJUDICATION_READINESS_REPORT.md`) | Draft §17 "Proposed resolution type" | Match |
|---|---|---|---|
| OD-005 | `CANDIDATE_SET_DETERMINATION` + `PROVISIONAL_DECISION_WITH_LIMITATIONS` | Same | Consistent |
| OD-006 | `CANDIDATE_SET_DETERMINATION` + `PROVISIONAL_DECISION_WITH_LIMITATIONS` + `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` | Same | Consistent |
| OD-015 | `PROCEDURAL_CONTRACT` + `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` | Same | Consistent |

No draft claims a resolution type beyond what was already frozen prior to this drafting turn.

## 7. Dependency consistency

- OD-005 upstream `REQ-M2-005`, downstream `REQ-M2-008` (the acceptance-criterion registry, which is also OD-006's source requirement) — both drafts are internally aware of this shared downstream link; neither draft resolves `REQ-M2-008` on OD-005's behalf.
- OD-006 upstream `REQ-M2-008`, downstream `REQ-M2-009` (MCSE target) and the acceptance-criterion registry — the OD-006 draft explicitly flags that its `OPT-006-B` branch has an unresolved downstream consequence for `NUM-DEC-02`'s frozen `Coverage_hat` target band, and does not attempt to resolve that consequence itself.
- OD-015 upstream `REQ-CROSS-001`, downstream `NUM-DEC-08`'s resource-envelope framework (`M3-BLOCK-08`) — the OD-015 draft explicitly defers all 8 resource-ceiling dimensions to `NUM-DEC-08`'s separately-authorized profiling turn and does not attempt to measure or estimate them numerically.

No dependency reference in any draft is dangling; all resolve to real requirement IDs in `WAVE_2_REQUIREMENT_DEPENDENCY_MATRIX.csv` or real NUM-DEC/decision IDs.

## 8. No final-status leakage

Searched all three drafts for the prohibited final-status vocabulary (`APPROVED`, `REJECTED`, `RESOLVED`, `CLOSED`, `PASS`, `FAIL`, `MANDATED`, `FINAL`) used as a decision status. None found used in that role anywhere (the words "resolved"/"final" appear only in frozen cross-references such as `RESOLVED_BY_FROZEN_SPEC` — quoting the frozen mathematical contract's own section labels — and in phrases like "final decision withheld," which is the *required* language per the governing instruction, not a final-status assertion).

## 9. No threshold selection

No draft selects a numeric threshold, tolerance, tau, prior, ROPE value, bootstrap count, profile-likelihood grid parameter, temperature ladder, checkpoint interval, retry limit, seed function, or hash algorithm. Where a formula's parameters remain open (e.g. `OD-007`'s profile-likelihood grid design, `OD-008`'s bootstrap `B`), the drafts correctly cite them as still-open dependencies rather than resolving them.

## 10. No implementation claim

No draft claims that any implementation has been built, corrected, tested, or run. The OD-006 draft explicitly states its implementation-dependent component (whether M2's failure modes are informative) "cannot be determined without running the corrected M2 implementation" — phrased as a requirement, not a claim of completion. The OD-015 draft's 15-item implementation-evidence contract lists every `current_status` as `PLANNED_ONLY`.

## 11. No calibration claim

No draft claims any calibration, benchmark, or simulation was run. All three drafts explicitly state "none identified" or "none performed" in their §15 ("Required calibration evidence") where applicable, or list calibration evidence as not yet required.

## 12. No historical-inference claim

No draft references historical data, historical fitting, or historical inference authorization. All evidence used is either internal frozen Wave 2/NUM-DEC documentation or the previously-frozen literature-evidence package (E-001 through E-007) — no draft introduces historical Model 3B data.

## 13. Final decisions

```text
OD-005 final decision: WITHHELD
OD-006 final decision: WITHHELD
OD-015 final decision: WITHHELD
```

## 14. Immutability confirmation

Re-verified via `git diff --stat` against baseline `d363be74349a46723a36b7b1401ac5008aadbb3d` for: the 18 earlier frozen V2 artifacts, all 8 NUM-DEC documents, all 10 Wave 2 planning artifacts, the open-decision ledger, the adjudication map, the batch matrix, all 5 literature-evidence artifacts, Wave 1 (`docs/thesis/colab/model3b_spec_validator/`), and M0/M2/M3 estimation code (`docs/thesis/colab/model3b_tournament_harness/`) — **all empty (no changes)**. `NUM-DEC-07` remains `DEFERRED` (re-read directly from the ledger). The M3 blocker registry (`applicability_validator.py::get_m3_blockers()`) is untouched — all 8 blockers remain `OPEN`. Tau retains no final numeric value. ROPE remains deferred. None of the 315 substantive future tests were executed or had status changed. `Model 3B-CD V1 = MODEL_VALIDATION_FAILURE` and `Phase D = COMPLETED_VALID_NEGATIVE_RESULT / DO NOT RERUN` are unaffected by this drafting turn — this drafting work makes no claim about either.

## 15. Summary verdict

The three draft adjudications and this reconciliation document are internally consistent with each other, with the frozen ledger and evidence-to-option matrix, and with the frozen mathematical contract. No stop condition (governing instruction §13) was triggered: the exact decision question is consistent across sources for all three decisions; candidate-option sets are consistent; the evidence package was sufficient for the authorized drafting boundary in each case; no draft required new literature search or a threshold/tolerance value; OD-006 was cleanly separable into its provisional and implementation-dependent components; OD-015 was cleanly bounded to procedural-contract-only content; no recommendation requires changing a frozen specification or implicitly closing an M3 blocker; no formula or denominator conflicts with the frozen contract; no claim exceeds verified source access; no baseline, code, or frozen artifact was changed; no final status leaked into any draft; and the work did not expand to any of the other 13 open decisions.
