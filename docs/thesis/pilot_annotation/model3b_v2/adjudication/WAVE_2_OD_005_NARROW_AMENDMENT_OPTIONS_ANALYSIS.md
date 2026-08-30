# WAVE 2 — OD-005 Narrow Additive Nonnumerical Amendment: Options Analysis

Status: PLANNING-ONLY. No amendment has been executed. No frozen artifact has been modified. This document analyzes, but does not decide, whether `OPT-005-B` should be retired or concretized.

Baseline: local HEAD = origin/main = `ce7abcea459c50b36b40e827772c90d70141ca5c`.

---

## 1. Source chain (provenance)

| Claim | Source path | Location | Statement |
|---|---|---|---|
| OD-005 candidate options (verbatim) | `planning/WAVE_2_OPEN_DECISION_LEDGER.csv` | OD-005 row, `candidate_options` field | "AbsBias_c as proposed; a different exact-null-specific metric; RelBias with a regularized denominator (rejected in spec S8.4 discussion)" |
| OPT-005-A = AbsBias_c, fully specified | `evidence/WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv` | OD-005/OPT-005-A row | `adjudication_readiness=EVIDENCE_SUFFICIENT_FOR_REVIEW` |
| OPT-005-B = unnamed placeholder | `evidence/WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv` | OD-005/OPT-005-B row | `adjudication_readiness=SPECIFICATION_CLARIFICATION_REQUIRED`, `silent_default_risk=high`, `provenance_risk=high`, `decidable_without_execution=NO` |
| Same framing repeated | `adjudication/WAVE_2_OD_005_DRAFT_ADJUDICATION.md` | lines 21-81 | OPT-005-A = `DRAFT_CANDIDATE_SET_FOR_REVIEW`; OPT-005-B "flagged for retirement-or-concretization" |
| Ambiguity first classified | `adjudication/WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md` | lines 13-98 | Classified `ADDITIVE_NONNUMERICAL_AMENDMENT_REQUIRED`; recommends choosing explicitly between retire (a) or concretize with a named formula (b) |
| AbsBias_c formula (frozen) | `planning/WAVE_2_MATHEMATICAL_CONTRACT.md` | §S2.3 | `AbsBias_c = (1/R_valid,c) * sum_{r in V_c} |n_hat_cr - n_c|`, exact-null substitute for `n_c=0` |
| AC-M2-03 registry row | `planning/WAVE_2_MATHEMATICAL_CONTRACT.md` | §S2.4 acceptance-criterion registry | `threshold_status=OPEN_REQUIRES_ADJUDICATION`, `threshold_value=NULL`, `mathematical_object=AbsBias_c at exact null`, source=`S2.3`, dependency=`none (OD-005)` |
| NUM-DEC-02 future gate list names AbsBias, not a second metric | `numerical_decisions/MODEL_3B_NUM_DEC_02_M2_UNCERTAINTY_ADJUDICATION.md` | line 154 | Future gate family (1) = "absolute bias of `n`" — consistent with OPT-005-A only; no second exact-null-specific metric is named anywhere in this document |
| NUM-DEC-01 denominator invariant (must not be redefined) | `numerical_decisions/MODEL_3B_NUM_DEC_01_M2_REPLICATION_DENOMINATOR_ADJUDICATION.md` | lines 48, 79-93 | `R_attempt = R_valid + R_failed + R_invalid`; `R_metric <= R_valid <= R_attempt` — AbsBias_c's `1/R_valid,c` denominator is compatible; no alternate denominator convention is introduced or implied for a hypothetical OPT-005-B |
| NUM-DEC-03 nested-null structure | `numerical_decisions/MODEL_3B_NUM_DEC_03_M2_EXACT_NULL_ADJUDICATION.md` | lines 33-101, 256-297 | Governs *existence* testing (`H0: n=0` vs `H1`) via likelihood-ratio, not the *magnitude*-bias metric that OD-005 governs; explicitly a different quantity ("these are different quantities requiring different machinery," line 256-260) — confirms OD-005/AbsBias_c is not duplicative of NUM-DEC-03's LR statistic and that NUM-DEC-03 supplies no formula for a second OD-005 candidate either |

**Cross-source consistency check (stop-condition §16 item 1):** OPT-005-B's exact wording — "a different exact-null-specific metric" — is identical, verbatim, everywhere it appears (ledger, evidence matrix; the two adjudication-stage documents paraphrase but do not contradict it). **No inconsistency found. Stop condition does not trigger.**

**Exhaustive formula search result:** across all 9 sources read (ledger, evidence-to-option matrix, draft adjudication, clarification review, mathematical contract §S2.3/§S2.4, NUM-DEC-01, NUM-DEC-02, NUM-DEC-03), **zero formulas, zero named methods, and zero citations** are associated with OPT-005-B anywhere in the frozen corpus. The only concrete mathematical object ever attached to "exact-null-specific metric" in this corpus is `AbsBias_c` itself (OPT-005-A).

---

## 2. Branch A — RETIRE OPT-005-B

### 2.1 Ten-question retirement-candidate test

1. **Does OPT-005-B have a named formula anywhere in frozen sources?** No (see §1 exhaustive search).
2. **Does any frozen source promise one is forthcoming?** No — the clarification review (line ~57-70) treats it as an open gap requiring a *researcher* decision, not a pending literature delivery.
3. **Is OPT-005-B duplicative of a rejected option?** No — `options_rejected` in the ledger names only `RelBias at n_c=0`, a distinct (and already-rejected) idea. OPT-005-B is a separate, never-specified placeholder, not a restatement of the rejected option.
4. **Would retiring it strand any dependency?** `downstream_impact` = `REQ-M2-008 (acceptance-criterion registry)`, specifically `AC-M2-03`. AC-M2-03 already has `threshold_status=OPEN_REQUIRES_ADJUDICATION` regardless of which OD-005 option is chosen; retiring OPT-005-B does not change AC-M2-03's status, only shrinks the candidate set feeding it.
5. **Is OPT-005-A alone sufficient to keep OD-005 open for adjudication?** Yes — OPT-005-A already carries `adjudication_readiness=EVIDENCE_SUFFICIENT_FOR_REVIEW`; a one-candidate ledger is not a stop condition (the ledger's own `required_evidence` field never mandated a minimum of two live candidates).
6. **Does retirement erase any identifier?** No — per the identifier contract, retirement is `MARK_OPTION_RETIRED_WITH_RATIONALE`; `OPT-005-B` remains a valid, citable, historically-preserved identifier, only its `current_status` changes.
7. **Is the rationale for retirement traceable without new evidence?** Yes — the rationale is purely the absence of a specification in the already-frozen corpus, not a new empirical or literature claim.
8. **Does retirement require any numeric choice?** No.
9. **Does retirement conflict with any NUM-DEC (01/02/03) commitment?** No — checked directly above; none of the three decisions name or depend on OPT-005-B.
10. **Is retirement reversible?** Yes — a future researcher could re-open/re-concretize OPT-005-B later if a formula is ever proposed; nothing about retirement forecloses that path structurally (the identifier is preserved, not deleted).

### 2.2 Retirement-candidate criteria (§6.1) — result: **ALL SATISFIED**

---

## 3. Branch B — CONCRETIZE OPT-005-B

### 3.1 Minimum-contract fillability test (16 required fields, tested against frozen sources only)

| # | Required field | Fillable from frozen sources? | Basis |
|---|---|---|---|
| 1 | Explicit mathematical formula | **NO** | Zero formula found anywhere (§1) |
| 2 | Named estimator/statistic | **NO** | No name given beyond the generic descriptor already in the ledger |
| 3 | Domain of applicability (which cells) | Partially (exact-null cells only, by definition) | Inherited from the ledger's own framing, not new |
| 4 | Denominator convention | **NO** — cannot be fixed without a formula to attach it to | — |
| 5 | Relationship to `AbsBias_c` (distinct? nested? alternative?) | **NO** | No source states whether it is a variant of AbsBias or something structurally different |
| 6-16 | (units, boundary behavior, failure-transparency interaction, validator representability, evidence citation, etc.) | **NO** for all remaining fields that presuppose a formula exists | Each downstream field is formula-dependent |

**Result: 1/16 fields fillable (weakly), 15/16 NOT fillable from frozen sources without inventing new mathematical content.**

Concretizing OPT-005-B under this instruction's constraints (no new numbers, no new evidence, no implementation-dependent claims, no literature search) would require **authoring** a formula from nothing — which is not an additive nonnumerical clarification of an existing specification, it is the creation of new mathematical content. That is explicitly out of scope for this planning turn and, per the instruction's own prohibitions, not authorized.

### 3.2 Concretization-candidate criteria (§6.2) — result: **NOT SATISFIED** (fails at field 1 of 16, cascades to fields 4-16)

---

## 4. K1-K15 criterion rubric

| # | Criterion | Branch A (RETIRE) | Branch B (CONCRETIZE) |
|---|---|---|---|
| K1 | Source explicitness | SATISFIED — rationale cites only frozen, already-read sources | NOT_SATISFIED — no source explicitly states a formula |
| K2 | Mathematical completeness | NOT_APPLICABLE — retirement removes the object, does not define one | NOT_SATISFIED — cannot be completed |
| K3 | Operational testability | SATISFIED — "retired" is a binary, testable status | NOT_SATISFIED — no operational content exists to test |
| K4 | Nonduplication | SATISFIED — does not touch OPT-005-A or the rejected RelBias option | NOT_SATISFIED — cannot even confirm nonduplication with OPT-005-A without a formula |
| K5 | Denominator safety | SATISFIED — no denominator introduced | NOT_SATISFIED — denominator undefined |
| K6 | Failure transparency | SATISFIED — unaffected; `FailureRate_c` reporting requirement (S2.3) is untouched | NOT_SATISFIED — cannot state how failed replications interact with an undefined metric |
| K7 | Compatibility with frozen estimand (`n=alpha/beta`) | SATISFIED — retirement makes no estimand claim | NOT_SATISFIED — cannot verify compatibility of an unspecified formula |
| K8 | Compatibility with NUM-DEC-01/02/03 | SATISFIED — verified directly in §1 | NOT_SATISFIED — cannot verify against decisions that were never asked to accommodate this metric |
| K9 | Validator representability | SATISFIED — a retired-option schema field is trivially representable (Wave-1 validator already enforces only structural/schema validity, not semantic concreteness) | NOT_SATISFIED — nothing to represent |
| K10 | No new numerical choice | SATISFIED | NOT_SATISFIED — any concretization attempt would force an implicit numerical/structural choice |
| K11 | No implementation evidence required | SATISFIED | NOT_SATISFIED |
| K12 | Provenance completeness | SATISFIED — full chain shown in §1 | NOT_SATISFIED — provenance chain terminates at "unnamed" |
| K13 | Minimal amendment surface | SATISFIED — one option-status flip + rationale note | NOT_SATISFIED — would require inventing and threading a new formula through §S2.3/§S2.4, the evidence matrix, and AC-M2-03 |
| K14 | Reversibility | SATISFIED — see §2.1 item 10 | NOT_APPLICABLE — branch does not reach a defined state to reverse |
| K15 | Risk of silent default | SATISFIED (LOW) — explicit retirement with rationale is the opposite of a silent default | NOT_SATISFIED (HIGH) — matches the evidence matrix's own pre-existing `silent_default_risk=high` flag; inventing content here would realize that exact risk |

**Score summary:** Branch A (RETIRE) — SATISFIED=14, PARTIALLY_SATISFIED=0, NOT_SATISFIED=0, NOT_APPLICABLE=1, TOTAL=15. Branch B (CONCRETIZE) — SATISFIED=0, PARTIALLY_SATISFIED=0, NOT_SATISFIED=14, NOT_APPLICABLE=1, TOTAL=15.

---

## 5. Recommendation determination (§8 rule)

Applying the instruction's recommendation rule: Branch A meets every qualifying condition for `DRAFT_RECOMMEND_RETIRE_FOR_REVIEW` (all K-criteria satisfied or not-applicable, zero not-satisfied, ten-question test fully passed, minimum-contract test not applicable since nothing is being defined). Branch B fails the qualifying conditions for `DRAFT_RECOMMEND_CONCRETIZE_FOR_REVIEW` (14 of 16 contract fields unfillable, 13 of 15 applicable K-criteria not satisfied).

**Draft recommendation: `DRAFT_RECOMMEND_RETIRE_FOR_REVIEW`.**

This is a draft recommendation for a future adjudication turn. It is **not** a final adjudication. `OD-005` and `OPT-005-B`'s final disposition remain **WITHHELD** pending researcher review, per the closing statement of `WAVE_2_OD_005_NARROW_AMENDMENT_PLAN.md`.
