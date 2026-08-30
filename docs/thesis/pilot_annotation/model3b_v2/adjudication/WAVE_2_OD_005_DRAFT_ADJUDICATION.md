# OD-005 Draft Adjudication — AbsBias as Adopted Exact-Null Acceptance Metric

> **Status: DRAFTING-ONLY.** This document is a reviewable draft, not a final adjudication. No status change to `OD-005` in `WAVE_2_OPEN_DECISION_LEDGER.csv` is made or implied by this draft. Authorized drafting scope: `CANDIDATE_SET_DETERMINATION` + `PROVISIONAL_DECISION_WITH_LIMITATIONS` only.

## 1. Decision identity

`OD-005`, source requirement `REQ-M2-005`, mathematical object `AbsBias_c`.

## 2. Exact frozen decision question

Verbatim from `WAVE_2_OPEN_DECISION_LEDGER.csv`: **topic** — "AbsBias as adopted exact-null acceptance metric." The question this decision resolves: whether `AbsBias_c` (or an alternative) is adopted as the exact-null (`n_c=0`) acceptance metric for M2, given that `RelBias_c` is mathematically undefined at `n_c=0`.

## 3. Current status

`OPEN_REQUIRES_ADJUDICATION` (ledger, unchanged by this draft).

## 4. Candidate options

Stated exactly as in the ledger and evidence-to-option matrix (no paraphrase-drift):

- **OPT-005-A**: `AbsBias_c` as proposed — `WAVE_2_MATHEMATICAL_CONTRACT.md` S2.3: `AbsBias_c = (1/R_valid,c) * sum |n_hat_cr - n_c|`, exact-null substitute for `n_c=0`.
- **OPT-005-B**: "a different exact-null-specific metric" — an unspecified generic alternative named only in the ledger's `candidate_options` field; no concrete formula exists anywhere in the frozen Wave 2 artifacts.
- **Rejected option** (already rejected in the ledger, not a live candidate): `RelBias_c` with a regularized denominator — rejection basis: mathematically undefined at the exact-null point (`WAVE_2_MATHEMATICAL_CONTRACT.md` S2.3 / S8.4 discussion).

## 5. Internal-source evidence

- `WAVE_2_MATHEMATICAL_CONTRACT.md` S2.3 already writes both `RelBias_c` (undefined at `n_c=0`, by construction — division by `n_c`) and `AbsBias_c` (well-defined for `R_valid,c >= 1`) into the frozen mathematical contract, explicitly marking `AbsBias_c` as "a *candidate*, not yet adopted (`OD-005`, `OPEN_REQUIRES_ADJUDICATION`)."
- `WAVE_2_MATHEMATICAL_CONTRACT.md` S2.2 (`RESOLVED_BY_FROZEN_SPEC`, `NUM-DEC-01`) requires every bias metric to be reported alongside `FailureRate_c` (attempted-denominator), never in isolation — this constraint applies to whichever option is eventually adopted.
- `MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md` (§ selected option) fixes `R_valid(c) = R_attempt(c) - R_failed(c) - R_invalid(c)` as the metric-bearing denominator basis that `AbsBias_c` inherits.

## 6. Literature evidence

- **E-001** (Morris, White, Crowther 2019, *Statistics in Medicine*, DOI:10.1002/sim.8086, `FULL_TEXT_ACCESSED`): explicit source claim — relative bias is defined only for true parameter `|theta|>0` and is undefined by division-by-zero at `theta=0`; absolute bias is the standard alternative performance measure for boundary/zero true values. Supports `OPT-005-A`; contradicts using `RelBias_c` as the sole exact-null metric.
- **E-003** (Gasparini & White, `rsimsum` package documentation, accessed 2026-08-30, `FULL_TEXT_ACCESSED`): documentation lists bias, relative bias, coverage, and bias-eliminated coverage as computable measures in the field's standard reference toolkit (co-authored by one of the E-001 authors). Indirect corroboration of `AbsBias_c` as a standard candidate alongside relative bias — the excerpt accessed does not itself state the zero-boundary restriction explicitly.
- **E-004** (Burton, Altman, Royston, Holder 2006, *Statistics in Medicine*, DOI:10.1002/sim.2673, `METADATA_ONLY`): **bibliographic lead only.** Citation and existence confirmed via cross-listing search; **no methodological claim is asserted from this source** anywhere in this draft. Included solely for foundational-lineage completeness (E-001 itself builds on this 2006 predecessor's checklist approach), per the evidence-preparation instruction's requirement to identify foundational sources.

No option-005-B evidence exists — see §9.

## 7. Access and provenance limits

E-001 and E-003 are both `FULL_TEXT_ACCESSED` with verifiable stable identifiers (DOI / package URL) — claims from them are used only within the scope actually read (relative-bias undefinedness at zero; absolute bias as standard alternative; the field-toolkit's computable-measures list). E-004 is `METADATA_ONLY` and is used exclusively as a bibliographic/provenance pointer, never as support for any substantive claim about `AbsBias_c` itself — this restriction was independently re-verified in the two prior narrow-review audits of this evidence package (both found 0 claim-access mismatches).

## 8. Mathematical implications

`AbsBias_c` is defined and finite whenever `R_valid,c >= 1`; it introduces no new symbol or notation change to `WAVE_2_MATHEMATICAL_CONTRACT.md` S2.3, which already carries its formula. `RelBias_c` remains undefined at `n_c=0` by construction regardless of this decision's outcome — that mathematical fact is not in question, only which metric is *adopted* as the exact-null acceptance measure. Per S2.2, whichever option is adopted must always be reported jointly with `FailureRate_c` and the `R_attempted,c`/`R_valid,c` accounting — this draft does not relax that requirement for either option.

## 9. Option-by-option assessment

**OPT-005-A (`AbsBias_c`)**: `adjudication_readiness = EVIDENCE_SUFFICIENT_FOR_REVIEW` (evidence-to-option matrix). Supported by E-001 and E-003 (both verified, low provenance risk, low statistical risk). Implementation consequence: none beyond what NUM-DEC-01/02/03 already imply — would need to be written into a future acceptance-criterion registry row currently marked `threshold_status=OPEN_REQUIRES_ADJUDICATION`. Calibration consequence: none — adopting `AbsBias_c` requires no calibration, only a researcher decision.

**OPT-005-B (unspecified alternative)**: `adjudication_readiness = SPECIFICATION_CLARIFICATION_REQUIRED` (evidence-to-option matrix). No concrete formula exists to evaluate against literature or Model 3B notation; mathematical/implementation/calibration consequences are all `undefined` because no specific metric has been named. This option cannot be assessed further without first being replaced by a named formula, or retired.

## 10. Adversarial assessment

Evidence supporting `AbsBias_c` (E-001, E-003) is not opposed by any source found in this search — the "opposing" search results instead confirm the *exclusion* of the already-rejected `RelBias_c` option is well founded (RelBias's undefinedness at zero is stated affirmatively, not merely assumed). Condition under which the `AbsBias_c` recommendation could fail to apply: if a future implementation's optimizer produces `n_hat_cr` values that are themselves unstable or badly scaled near the `n=0` boundary (a boundary-behavior / numerical-precision dependency) — `AbsBias_c` as a summary statistic does not itself diagnose that instability; it would need to be reported alongside the boundary-solution and profile-optimization-failure taxonomy already specified in `WAVE_2_MATHEMATICAL_CONTRACT.md`'s failure taxonomy (§14 of the governing Wave 2 instruction). This is a limiting condition on interpretation, not a contradiction of the metric's mathematical validity.

## 11. Draft recommendation

`DRAFT_CANDIDATE_SET_FOR_REVIEW`: the evidence package supports narrowing the live candidate set to `OPT-005-A` (`AbsBias_c`) as the substantively evidenced option, with `OPT-005-B` flagged for retirement-or-concretization rather than continued placeholder status. This is a **draft characterization of the evidence**, not a final selection — see §18.

## 12. Limitations

- No literature source directly states that `AbsBias_c` should be the *sole* exact-null metric versus reported alongside a second boundary-appropriate diagnostic (e.g. a signed-bias check) — this narrow residual question is not resolved here.
- E-003's corroboration of `AbsBias_c` is indirect (the source documents relative bias and bias generally, not an explicit zero-boundary restriction).
- Evidence coverage is thin on the "modern/evaluative" and "adversarial" dimensions specifically for `OPT-005-A` — no source was found that argues *against* `AbsBias_c`, which is disclosed as a thinness, not treated as confirmation.

## 13. Required specification clarification

Whether `OPT-005-B` should be formally retired from the ledger's `candidate_options` field (leaving `OPT-005-A` as the sole live candidate) or replaced with a concretely-named alternative formula for future evaluation. This clarification question is raised for review, not resolved by this draft.

## 14. Required implementation evidence

None identified — `AbsBias_c` requires no new implementation component beyond what `NUM-DEC-01`/`NUM-DEC-02`/`NUM-DEC-03` already specify (per §9 above).

## 15. Required calibration evidence

None identified — see §9 (calibration consequence: none for `OPT-005-A`; undefined/not applicable for `OPT-005-B` absent a concrete formula).

## 16. Prohibited shortcuts

This draft does not: select a numeric threshold or tolerance for `AbsBias_c`; assert a final acceptance criterion value; retire `OPT-005-B` from the ledger; change `E-004`'s access status or role; treat `E-004` as substantive evidence; or use final-status language for `OD-005`.

## 17. Proposed resolution type

`CANDIDATE_SET_DETERMINATION` + `PROVISIONAL_DECISION_WITH_LIMITATIONS` (matches the classification already frozen in `WAVE_2_OPEN_DECISION_ADJUDICATION_MAP.md` and `WAVE_2_OD_005_006_015_ADJUDICATION_READINESS_REPORT.md` — not altered here).

## 18. Final decision withheld

```text
OD-005 final decision: WITHHELD
```

No final adjudication is made. `OD-005` remains `OPEN_REQUIRES_ADJUDICATION` in the ledger. This draft is submitted for independent review before any final decision is authorized.
