# WAVE 2 — OD-005 Retirement Recommendation Review for OPT-005-B

Status: **REVIEW-ONLY**. This document reviews the draft recommendation `DRAFT_RECOMMEND_RETIRE_FOR_REVIEW`. It does not execute an amendment, does not modify the open-decision ledger, and does not change `OPT-005-B`'s frozen disposition.

Baseline: local HEAD = origin/main = `9798e7efc840d9f8ff9bae497c3a47534295cbd4`.

---

## 1. Scope

Single object under review: `OD-005` / `OPT-005-B`. `OD-006`, `OD-015`, and every other open decision are out of scope and are referenced only as scope boundaries, never substantively re-adjudicated.

## 2. Sources read in full this turn (read-only)

1. `docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_OPTIONS_ANALYSIS.md`
2. `docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_PLAN.md`
3. `docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_SURFACE_MAP.csv`
4. `docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_TEST_IMPACT.csv`
5. `docs/thesis/pilot_annotation/model3b_v2/planning/WAVE_2_OPEN_DECISION_LEDGER.csv` (full, all 19 rows)
6. `docs/thesis/pilot_annotation/model3b_v2/evidence/WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv` (full, all 6 rows)
7. `docs/thesis/pilot_annotation/model3b_v2/planning/WAVE_2_MATHEMATICAL_CONTRACT.md` (full, S0-S6)

Documents previously verified byte-identical to baseline and relied on by citation without re-reading verbatim this turn (confirmed via `git diff --stat` against `ce7abce`/`9798e7e` = empty for their containing directories): `WAVE_2_OD_005_DRAFT_ADJUDICATION.md`, `WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md`, `WAVE_2_OD_005_006_CLARIFICATION_RECONCILIATION.md`, `MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md`, `MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md`, `MODEL_3B_NUM_DEC_03_M2_EXACT_NULL_ADJUDICATION.md`. No literature search performed.

## 3. Review question (instruction §4)

> Apakah OPT-005-B dapat dipensiunkan melalui amendment aditif nonnumerik tanpa: (1) menghapus requirement substantif; (2) mengubah estimand primer; (3) mengubah denominator; (4) mengubah definisi coverage; (5) mengubah failure accounting; (6) mengubah profile-likelihood contract; (7) mengubah bootstrap requirement; (8) memilih threshold atau tolerance; (9) menghapus test obligation; (10) menghapus identifier atau provenance historis; (11) menutup keputusan atau blocker lain secara implisit?

**Answer: YES**, on all eleven sub-points, evidenced item-by-item below.

| # | Sub-question | Finding | Evidence |
|---|---|---|---|
| 1 | Requirement substantif dihapus? | NO | Requirement Nonloss Matrix (10/10 rows `preserved=YES`, `loss_detected=NO`) |
| 2 | Estimand primer diubah? | NO | Invariance Matrix INV-02 (`n=alpha/beta`, IDENTICAL) |
| 3 | Denominator diubah? | NO | Invariance Matrix INV-07/INV-08 (`R_attempted,c`, `R_valid,c`, IDENTICAL) |
| 4 | Definisi coverage diubah? | NO | Invariance Matrix INV-10 (`Coverage_c`/`CoverAndValid_c`, IDENTICAL; OD-006 untouched) |
| 5 | Failure accounting diubah? | NO | Invariance Matrix INV-09 (`FailureRate_c`, IDENTICAL) |
| 6 | Profile-likelihood contract diubah? | NO | Invariance Matrix INV-11 (`ell_p(n)`, `D(n)`, `C_1-gamma`, IDENTICAL; Package C/OD-007 untouched) |
| 7 | Bootstrap requirement diubah? | NO | Not referenced by any surface-map row; Package D/OD-008 untouched |
| 8 | Threshold/tolerance dipilih? | NO | 0 numeric values in surface map or test-impact CSV (mechanically verified) |
| 9 | Test obligation dihapus? | NO | Requirement Nonloss Matrix NL-08 (8/8 proposed tests `PLANNED_ONLY`, 0 collision with 315 existing) |
| 10 | Identifier/provenance dihapus? | NO | §5 below (identifier preservation) |
| 11 | Keputusan/blocker lain ditutup diam-diam? | NO | §4/§6 below (adversarial review, OD-006/OD-015 interaction) |

## 4. Mathematical invariance verdict

See `WAVE_2_OD_005_RETIREMENT_INVARIANCE_MATRIX.csv` — 13 objects checked (12 mandatory per instruction §5.8, plus `AbsBias_c`/`AC-M2-03` added adversarially since it is OD-005's own live candidate, OPT-005-A). **13/13 `comparison_result=IDENTICAL`, 0 `CHANGED`, 0 `UNRESOLVED`, 0 `BLOCKING`.**

Basis: no row in `WAVE_2_OD_005_NARROW_AMENDMENT_SURFACE_MAP.csv` proposes editing any formula in `WAVE_2_MATHEMATICAL_CONTRACT.md` S1-S4. All 8 surface-map rows target the ledger's `candidate_options` text, the evidence-matrix cross-reference, prose in the two adjudication-stage documents, an annotation on the AC-M2-03 registry row (not its `threshold_value`), a possible future validator enum addition, and the amendment's own planning/test-impact files. None of these targets is a mathematical-object definition.

## 5. Historical-identifier preservation

- `OD-005`: not renamed, not deleted, not reused for a different decision.
- `OPT-005-B`: retirement semantics per instruction §6 are `MARK_OPTION_RETIRED_WITH_RATIONALE` (surface-map row 1, `change_type` value confirmed within the 7-value allowed vocabulary). This is additive status marking, not deletion. `OPT-005-B` remains a valid, citable identifier under any future execution of this proposal.
- `OPT-005-A`: untouched.
- Historical registry `O_005^historical` (instruction §6) — per instruction's own semantics, `ACTIVE CANDIDATE REMOVAL != IDENTIFIER DELETION`; this review confirms the surface map's proposed change type (`MARK_OPTION_RETIRED_WITH_RATIONALE`, never a delete/remove type) is consistent with that constraint.

**Verdict: PASS.**

## 6. Candidate-set effect

Before (pre-review, unchanged by this review): `O_005^pre = {OPT-005-A, OPT-005-B}`.

If a future amendment executes the reviewed recommendation: `O_005^active = {OPT-005-A}` (conceptual, not yet applied); `O_005^historical = {OPT-005-A, OPT-005-B}` remains unchanged — `OPT-005-B` stays queryable with a `RETIRED` status and rationale.

This review changes neither set. It only evaluates whether a future transition from `O_005^pre` to `O_005^active` (execution deferred to a separately authorized turn) would be mathematically and provenance-safe.

## 7. Requirement and test-obligation nonloss verdict

See `WAVE_2_OD_005_RETIREMENT_REQUIREMENT_NONLOSS_MATRIX.csv` — 10 requirements reviewed, **10/10 `preserved=YES`, 0 `loss_detected`, 0 `BLOCKING`**. One row (NL-04) records a `superseded_by` value (the future retirement-rationale text itself, not yet written) because that requirement's resolution mechanism is what the eventual amendment would supply — this is the intended, disclosed mechanism, not an undisclosed loss.

Test-obligation nonloss (instruction §8.4, `T_existing ∩ T_removed = ∅`): mechanically re-verified this turn — 0 of the 315 existing test IDs collide with the 8 proposed `OD005-AMD-001..008` IDs; all 8 remain `PLANNED_ONLY`; none is proposed for removal from any inventory.

**Verdict: PASS.**

## 8. K1-K15 re-confirmation (instruction §7)

Ground truth under test (from planning, not assumed): RETIRE = 14 SATISFIED / 0 PARTIALLY_SATISFIED / 0 NOT_SATISFIED / 1 NOT_APPLICABLE, TOTAL=15. CONCRETIZE = 0 SATISFIED / 0 PARTIALLY_SATISFIED / 14 NOT_SATISFIED / 1 NOT_APPLICABLE, TOTAL=15.

| Criterion | Planning call (RETIRE / CONCRETIZE) | Independent source re-check this turn | Review result |
|---|---|---|---|
| K1 Source explicitness | SATISFIED / NOT_SATISFIED | Rationale cites only the ledger, evidence matrix, and math contract — all read in full this turn; no formula for OPT-005-B found anywhere | CONFIRMED |
| K2 Mathematical completeness | NOT_APPLICABLE / NOT_SATISFIED | Retirement defines no new object; concretization would require inventing one (0 formulas found for OPT-005-B in any source) | CONFIRMED |
| K3 Operational testability | SATISFIED / NOT_SATISFIED | `OD005-AMD-001`/`002` test exactly the binary retired-status contract | CONFIRMED |
| K4 Nonduplication | SATISFIED / NOT_SATISFIED | Ledger `options_rejected` names only `RelBias at n_c=0`, distinct from OPT-005-B; OPT-005-A row independently confirmed untouched | CONFIRMED |
| K5 Denominator safety | SATISFIED / NOT_SATISFIED | INV-07/INV-08 confirm `R_valid,c` unchanged; no denominator introduced by retirement | CONFIRMED |
| K6 Failure transparency | SATISFIED / NOT_SATISFIED | INV-09 confirms `FailureRate_c` unaffected | CONFIRMED |
| K7 Estimand compatibility | SATISFIED / NOT_SATISFIED | INV-02 confirms `n=alpha/beta` unchanged | CONFIRMED |
| K8 NUM-DEC-01/02/03 compatibility | SATISFIED / NOT_SATISFIED | NUM-DEC files confirmed byte-identical to baseline (`git diff --stat` empty); none names or depends on OPT-005-B | CONFIRMED |
| K9 Validator representability | SATISFIED / NOT_SATISFIED | Wave-1 validator enforces structural/schema validity only (established fact, `schema_validator.py` unread/unmodified this turn per scope) | CONFIRMED |
| K10 No new numerical choice | SATISFIED / NOT_SATISFIED | 0 numeric values found in surface map or test-impact CSV | CONFIRMED |
| K11 No implementation evidence required | SATISFIED / NOT_SATISFIED | Retirement is a status/documentation change; no execution implied | CONFIRMED |
| K12 Provenance completeness | SATISFIED / NOT_SATISFIED | Full source chain independently retraced this turn: ledger to evidence matrix to draft adjudication to clarification review to math contract | CONFIRMED |
| K13 Minimal amendment surface | SATISFIED / NOT_SATISFIED | Surface map confirmed at exactly 8 rows, all within the 7-value `change_type` vocabulary, only 1 mention of another OD (`OD-006`, as scope boundary only) | CONFIRMED |
| K14 Reversibility | SATISFIED / NOT_APPLICABLE | Identifier preserved (§5); re-opening/re-concretizing OPT-005-B later remains structurally possible | CONFIRMED |
| K15 Silent-default risk | SATISFIED (LOW) / NOT_SATISFIED (HIGH) | Evidence matrix's own pre-existing `silent_default_risk=high` flag for OPT-005-B is the documented basis; explicit retirement-with-rationale is the disclosed opposite of a silent default | CONFIRMED |

**15/15 CONFIRMED, 0 NOT_CONFIRMED, 0 REQUIRES_CLARIFICATION.** Original planning rows in the two source Markdown files are unmodified by this review.

## 9. Necessity, sufficiency, nonloss (instruction §8)

- **9.1 Necessity**: `NECESSARY`. Evidence matrix's own `silent_default_risk=high` flag for OPT-005-B, combined with zero formula/citation found anywhere in the frozen corpus (§1 of the options analysis, independently re-confirmed this turn), means leaving OPT-005-B open and unspecified risks exactly the silent-choice failure mode the instruction warns against. Absence of specification alone is not treated as sufficient justification (instruction §15) — necessity here rests on the *combination* of absence-of-specification, the pre-existing risk flag, and the ten-question retirement test (options analysis §2.1, independently spot-checked against ledger/evidence-matrix content this turn and found consistent).
- **9.2 Sufficiency**: `SUFFICIENT_WITH_LIMITATIONS`. Marking `OPT-005-B = RETIRED_WITH_RATIONALE` plus the cross-references and future-test obligations already scoped in the surface map and test-impact files is sufficient to resolve the ambiguity, provided the 14 limitations in §9 below are honored at amendment-execution time.
- **9.3 Requirement nonloss**: PASS — see §7 above (`R_before = R_after`, 10/10 preserved).
- **9.4 Test-obligation nonloss**: PASS — see §7 above (0 collision, 0 loss).

## 10. Adversarial review (instruction §15)

1. **Requirement possibly lost?** None found. Ledger's `downstream_impact` field for OD-005 (`REQ-M2-008`, `AC-M2-03`) is explicitly reviewed in NL-01/NL-02 and confirmed unaffected.
2. **Test obligation possibly lost?** None found. All 8 proposed tests remain `PLANNED_ONLY`; no existing test in the 315-inventory targets OPT-005-B (grep-confirmed: no `OD-005`/`OD005` prefix exists in either existing inventory file).
3. **Formula possibly changed?** None found. 13/13 invariance objects `IDENTICAL` (§4).
4. **Dependency possibly dangling?** Checked: `AC-M2-03`'s `downstream_impact`/`dependency` fields reference `REQ-M2-008` only, which is preserved (NL-02); no dependency chain terminates at OPT-005-B specifically.
5. **Validator behavior possibly ambiguous?** One residual item, already flagged and non-blocking: `schema_validator.py` may need a `RETIRED` enum value added in a *future* turn (surface-map row 6). This is disclosed, not hidden, and test `OD005-AMD-003` exists to catch a validator gap if it is not eventually addressed.
6. **Historical provenance possibly broken?** None found. §5 above confirms identifier/provenance preservation.
7. **Wording possibly readable as deletion?** Checked directly: surface-map row 1's `change_type` is `MARK_OPTION_RETIRED_WITH_RATIONALE`, not any delete/remove-type value; the 7-value vocabulary contains no deletion semantic at all.
8. **Wording possibly readable as a final implementation decision?** Checked directly: every "proposed_additive_content_summary" cell in the surface map (all 8 rows) uses `WITHHELD`/`N/A`/deferred-to-future-turn language; `WAVE_2_OD_005_NARROW_AMENDMENT_PLAN.md` closes with the explicit `WITHHELD`/`WITHHELD`/`NOT AUTHORIZED` triplet, confirmed still present and unmodified this turn.
9. **Interaction with OD-006?** Only a scope-boundary mention ("OD-006 is out of scope") found in the plan; no substantive OD-006 content is read, cited, or altered by the OPT-005-B proposal. `Coverage_c`/`CoverAndValid_c` formulas (OD-006's subject matter) independently confirmed unchanged (INV-10).
10. **Interaction with OD-015?** No mention found anywhere in the four planning artifacts or this review's sources. No interaction exists.
11. **Risk that retirement hides an alternative metric?** Checked: retirement does not select or promote any alternative metric; OPT-005-A (`AbsBias_c`) remains exactly as evidenced (`EVIDENCE_SUFFICIENT_FOR_REVIEW`, unchanged, NL-03), not silently substituted for OPT-005-B.
12. **Risk that the recommendation rests only on absence of specification?** Checked per instruction §15's own standard: the recommendation additionally rests on (a) the pre-existing `silent_default_risk=high` evidence-matrix flag, (b) nonduplication with the already-rejected `RelBias at n_c=0` option, (c) the ten-question retirement test, and (d) full requirement/test-obligation nonloss — not on absence of specification alone.

**No blocking adversarial finding identified.**

## 11. Decision-rule application (instruction §10)

All twelve qualifying conditions for `APPROVED_WITH_LIMITATIONS_TO_RETIRE` are checked against this turn's independent findings:

| Condition | Result |
|---|---|
| 15/15 RETIRE criteria reviewed | YES (§8) |
| 0 RETIRE criterion NOT_CONFIRMED | YES (§8: 15/15 CONFIRMED) |
| every REQUIRES_CLARIFICATION nonblocking and covered by a limitation | N/A — 0 REQUIRES_CLARIFICATION found |
| mathematical invariance passes for all required objects | YES (§4: 13/13 IDENTICAL) |
| requirement nonloss passes | YES (§7) |
| test-obligation nonloss passes | YES (§7) |
| identifier preservation passes | YES (§5) |
| provenance chain complete | YES (§8, K12) |
| amendment surface narrow and additive | YES (8 rows, all within the 7-value vocabulary, no deletion semantic) |
| no new numeric decision | YES (0 numeric values found) |
| no implementation/calibration evidence required for retirement semantics | YES (§9.2) |
| no substantive effect on OD-006, OD-015, or any other OD | YES (§10 items 9-10) |

**All twelve conditions satisfied → `APPROVED_WITH_LIMITATIONS_TO_RETIRE` is the correct outcome.**

## 12. Outcome

```text
Recommendation review = APPROVED_WITH_LIMITATIONS_TO_RETIRE
Amendment execution = NOT AUTHORIZED
Ledger modification = NOT AUTHORIZED
```

This outcome approves the draft recommendation for a future, separately authorized amendment-execution turn. It does not itself retire `OPT-005-B`, does not modify the ledger, and does not modify the validator, specification, or any frozen artifact.

---

See `WAVE_2_OD_005_RETIREMENT_REVIEW_DECISION_DRAFT.md` for the formal 16-point decision draft.
