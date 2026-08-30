# OD-006 Draft Adjudication — Primary M2 Coverage Metric: Coverage_c vs CoverAndValid_c

> **Status: DRAFTING-ONLY.** This document is a reviewable draft, not a final adjudication. No status change to `OD-006` in `WAVE_2_OPEN_DECISION_LEDGER.csv` is made or implied by this draft. Authorized drafting scope: `CANDIDATE_SET_DETERMINATION` + `PROVISIONAL_DECISION_WITH_LIMITATIONS`, with a final component held explicitly `IMPLEMENTATION_DEPENDENT_FINAL_DECISION`.

## 1. Decision identity

`OD-006`, source requirement `REQ-M2-008`, mathematical objects `Coverage_c`, `CoverAndValid_c`.

## 2. Exact frozen decision question

Verbatim from `WAVE_2_OPEN_DECISION_LEDGER.csv`: **topic** — "Primary M2 coverage metric: Coverage_c vs CoverAndValid_c." The question: which of the two coverage formulas is adopted as the *primary* M2 coverage acceptance metric.

## 3. Current status

`OPEN_REQUIRES_ADJUDICATION` (ledger, unchanged by this draft).

## 4. Candidate options

Stated exactly as in the ledger and evidence-to-option matrix:

- **OPT-006-A**: `Coverage_c` — conditional-on-valid-interval coverage, `Coverage_c = (1/R_valid,c) * sum 1{n_c in C_cr}`, always reported alongside `FailureRate_c` per `NUM-DEC-01`.
- **OPT-006-B**: `CoverAndValid_c` — unconditional, attempted-denominator coverage, `CoverAndValid_c = (1/R_attempted,c) * sum 1{valid interval and n_c in C_cr}`.

Ledger note: "none formally rejected — both remain candidates pending NUM-DEC review."

## 5. Internal-source evidence

- `WAVE_2_MATHEMATICAL_CONTRACT.md` S2.6 writes both formulas verbatim and states: "Which is primary = `OD-006`, `OPEN_REQUIRES_ADJUDICATION` — no new primary metric may be adopted without an explicit NUM-DEC/spec cross-check."
- **`MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md`** (SS11, SS18, SS19) already writes `Coverage_hat = (1/R_metric) * sum over valid metric-bearing replications of I[n_true in CI_b]` — this is the *same mathematical form* as `OPT-006-A` (`Coverage_c`, valid-denominator) — and already freezes a target band: `0.925 <= Coverage_hat <= 0.975` (`GATE-021-V2`). This is a directly load-bearing internal fact: adopting `OPT-006-A` as primary would make `OD-006` a *confirmatory/consistency* decision relative to an already-written frozen document, not a de-novo choice. Adopting `OPT-006-B` instead would require the already-frozen `Coverage_hat` target band to be reconciled or re-derived under a different (stricter, attempted) denominator — a nontrivial downstream consequence outside this drafting task's authorization.
- `NUM-DEC-01` mandates `R_valid,c`/`R_attempted,c`/`FailureRate_c` joint bookkeeping regardless of which coverage metric is adopted — this requirement is not affected by this decision's outcome.

## 6. Literature evidence

- **E-001** (Morris, White, Crowther 2019, `FULL_TEXT_ACCESSED`): explicit `n_sim`-based bias/coverage formulas; the ADEMP framework requires missingness/non-convergence to be reported as the first performance measure. Supports `OPT-006-A` via a structural analogy (`n_sim`-as-valid-count is inferentially, not explicitly, analogous to `R_valid,c`).
- **E-003** (`rsimsum` documentation, `FULL_TEXT_ACCESSED`): the `na.rm` parameter defaults to `TRUE` — i.e. the field's standard reference implementation (co-authored by an E-001 author) excludes missing/failed estimates from its computations by default. Corroborates `OPT-006-A` as the field-standard default *in practice*, not merely as recommendation.
- **E-002** (Pawel, Bartos, Siepe, Lohmann 2025, *The American Statistician*, DOI:10.1080/00031305.2025.2540002, `FULL_TEXT_ACCESSED` via arXiv v3 preprint text): explicit source claim — excluding failed/non-converged replications from a performance-measure denominator ("complete-case"-style) can bias results *when failures are informative* (correlated with the parameter being estimated); states "excluding failed replications artificially inflates performance" when failures are non-random. This is the central **adversarial/limiting** finding for `OD-006` — a genuine, verifiable, peer-reviewed methodological caution against `OPT-006-A`'s convention, published in 2025 (six years after E-001), specifically extending the ADEMP framework's own failure-handling guidance.

## 7. Access and provenance limits

E-001, E-002, and E-003 are all `FULL_TEXT_ACCESSED`. E-002's content was extracted from the arXiv preprint PDF version available at fetch time rather than the final *American Statistician* typeset version — the DOI resolves to the same work, but exact final wording was not independently re-verified against the publisher's typeset PDF; this is disclosed, not treated as a full-text-equivalent guarantee beyond the preprint text actually read.

## 8. Mathematical implications

`OPT-006-A` (`Coverage_c`) is mathematically identical in form to the `Coverage_hat` formula already written into `NUM-DEC-02` SS11/SS18, with an already-frozen target band (SS19). `OPT-006-B` (`CoverAndValid_c`) is mathematically distinct and would generally read lower than `OPT-006-A`, all else equal, because it folds interval-formation failure into the numerator as automatic non-coverage rather than excluding it from both numerator and denominator. Both formulas are already correctly stated (unaltered) in `WAVE_2_MATHEMATICAL_CONTRACT.md` S2.6 — this draft does not modify either formula.

## 9. Option-by-option assessment

**OPT-006-A (`Coverage_c`)**: `adjudication_readiness = EVIDENCE_SUFFICIENT_FOR_REVIEW`. Statistical risk: medium if reported alone, **low** if — as `NUM-DEC-01`/`NUM-DEC-02` already require — always reported jointly with `FailureRate_c` and `R_attempted,c`/`R_valid,c`. Silent-default risk: medium — not in the formula itself, but in a *future implementation* silently dropping the mandatory joint `FailureRate_c` disclosure that makes this option statistically safe; this is a documentation/implementation-discipline risk, not a mathematical defect. Whether M2's actual future failure modes (optimizer non-convergence, profile-likelihood boundary failures, bootstrap fit failures) will in practice be *informative* (correlated with `n_c`) — the condition under which E-002's caution becomes decisive — **cannot be established without running the corrected M2 implementation** and observing real failure patterns.

**OPT-006-B (`CoverAndValid_c`)**: `adjudication_readiness = SPECIFICATION_CLARIFICATION_REQUIRED`. Directly responsive to E-002's caution and conservative by construction (never overstates coverage due to hidden failures), but conflates "interval failed to form" with "interval formed but missed the true value" unless cross-tabulated against the failure taxonomy (already required elsewhere in Wave 2 planning). Its largest open item: adopting it as primary would require the already-frozen `NUM-DEC-02` `Coverage_hat` target band (`0.925`–`0.975`) to be re-derived or reinterpreted under the stricter attempted denominator — this re-derivation is **not performed and not authorized in this draft**.

## 10. Adversarial assessment

The central adversarial tension for `OD-006` is E-002 (2025, cautioning against complete-case-style exclusion when failures are informative) versus E-001/E-003 (field convention, complete-case-style exclusion as the *de facto* default). This is a genuine, disclosed, unresolved tension — not manufactured for balance. Conditions under which the leading candidate (`OPT-006-A`) could fail: informative missingness (a model-misspecification / boundary-behavior / weak-identifiability dependency, per the governing instruction's adversarial-check item list) — specifically plausible near the `n=0` boundary or under weak `beta` identification, both scenarios already flagged elsewhere in the frozen M2/M3 contract. Conditions under which `OPT-006-B` could fail: if interval-formation failure and true-value miss are not cross-tabulated, the metric conflates two distinct failure semantics. Neither option is evidence-supported as unconditionally superior; the adversarial evidence instead clarifies that the *choice is conditional on an empirical fact (informativeness of M2's actual failure modes) that does not yet exist*, because the corrected M2 implementation has not been run.

## 11. Draft recommendation

`DRAFT_CANDIDATE_SET_FOR_REVIEW`: both options remain live candidates. The evidence package supports a **provisional** characterization — `OPT-006-A` is the internally consistent choice with the already-frozen `NUM-DEC-02` target band and carries lower statistical risk *conditional on* mandatory joint `FailureRate_c` disclosure (which is already required regardless); `OPT-006-B` is the more conservative choice under E-002's caution but carries an unresolved downstream consequence for the frozen target band. Whether M2's actual failure modes are informative — the fact that would resolve this tension — is `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` and is explicitly **not** decided here.

## 12. Limitations

- E-002's content is from the arXiv preprint text, not independently re-verified against the publisher's final typeset PDF (see §7).
- No source in this package quantifies *how* informative M2's actual failure modes are or will be — this is an empirical question about the (not-yet-implemented) corrected M2 code, not a literature question.
- The re-derivation of `NUM-DEC-02`'s frozen `0.925`–`0.975` band under `OPT-006-B`'s denominator is identified as necessary but is out of scope for this drafting task.

## 13. Required specification clarification

Whether `OPT-006-B`, if ultimately adopted, requires the `NUM-DEC-02` target band to be formally re-derived/reinterpreted as a separate, explicitly-authorized specification-amendment turn (analogous to the earlier `NUM-DEC` amendment pattern used elsewhere in this project), rather than assumed to carry over unchanged.

## 14. Required implementation evidence

Whether M2's actual failure modes (post-correction of the blockers identified in `NUM-DEC-06`'s compatibility audit) are informative — i.e. correlated with `n_c` — cannot be determined without running the corrected M2 implementation and observing real failure patterns across the full mandatory scenario set. This is the single decisive `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` component of `OD-006`.

## 15. Required calibration evidence

None identified beyond the implementation-evidence item in §14 — no simulation, benchmark, or calibration run is required to state the candidate-set/provisional characterization in this draft, and none is performed here.

## 16. Prohibited shortcuts

This draft does not: select `OPT-006-A` or `OPT-006-B` as final; re-derive or alter the `NUM-DEC-02` `0.925`–`0.975` target band; run any simulation to test informativeness; set an acceptance threshold; or use final-status language for `OD-006`.

## 17. Proposed resolution type

`CANDIDATE_SET_DETERMINATION` + `PROVISIONAL_DECISION_WITH_LIMITATIONS` + `IMPLEMENTATION_DEPENDENT_FINAL_DECISION` (matches the classification already frozen in `WAVE_2_OPEN_DECISION_ADJUDICATION_MAP.md` and `WAVE_2_OD_005_006_015_ADJUDICATION_READINESS_REPORT.md` — not altered here).

## 18. Final decision withheld

```text
OD-006 final decision: WITHHELD
```

No final adjudication is made. `OD-006` remains `OPEN_REQUIRES_ADJUDICATION` in the ledger. The implementation-dependent component cannot be resolved before the corrected M2 implementation exists and its failure modes are observed.
