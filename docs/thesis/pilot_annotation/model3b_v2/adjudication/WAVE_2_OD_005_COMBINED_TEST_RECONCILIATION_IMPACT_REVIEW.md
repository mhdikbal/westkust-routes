# WAVE 2 — OD-005 Combined Test Reconciliation Impact Review

Status: **REVIEW-ONLY**. This document analyzes the impact of the canonical OD-005 test inventory (`OP-09`, committed and server-synced at `ce372eb`) on the existing combined test reconciliation. It authorizes no change to any reconciliation, inventory, ledger, or validator artifact.

Authoritative baseline: `ce372ebd75814ceb48f9c8458cd84eac30d71349`.

---

## 1. Mathematical contract (re-verified this turn)

```text
|T_N| = 194, |T_A| = 121, |T_OD005| = 8
T_N ∩ T_A = ∅, T_N ∩ T_OD005 = ∅, T_A ∩ T_OD005 = ∅
|T_N ∪ T_A ∪ T_OD005| = 323
D = (194+121+8) − |unique(ID_N ∪ ID_A ∪ ID_OD005)| = 0
|T_executed| = 0
```

All values match the OP-09 audit exactly; nothing has changed since that commit.

## 2. Answers to the twelve review questions

**1. Which existing artifact is the authoritative source for the count 315?**
`docs/thesis/pilot_annotation/model3b_v2/reconciliation/MODEL_3B_COMPLETE_NUMERICAL_DECISION_CONSISTENCY_AUDIT.md`, §19 "Future Test Inventory" (line 127: `Combined future-test count: 194 + 121 = 315`). This is the single point of origin; every other 315-reference in the repository cites or re-confirms this computation rather than deriving it independently.

**2. Is that artifact frozen?**
Yes. It is `ART-016` in `MODEL_3B_V2_ARTIFACT_INVENTORY.csv`, type `RECONCILIATION_OR_CONSISTENCY`, classification `FROZEN_V2_MILESTONE`, and its content hash is tracked in `MODEL_3B_V2_CHECKSUM_MANIFEST.csv`.

**3. Does its current schema assume exactly two inventories?**
Effectively yes, though informally: the document is narrative Markdown, not a formal N-inventory schema. Its §19 code block hard-writes a two-term sum (`Numerical-decision test count` + `Existing amendment test count` → `Combined future-test count`), with no generalized "list of inventory files" structure that a third term could be inserted into without prose surgery.

**4. Can a third inventory be added through a purely additive update?**
Yes, in principle — a new paragraph could be appended after the existing §19 block, stating the OD-005 canonical inventory and the new `194+121+8=323` sum, without deleting or rewriting the original sentence. This is additive at the file level.

**5. Would modifying the existing reconciliation overwrite historical state?**
Only if the edit touches the existing `194+121=315` sentence itself (e.g., replacing `315` with `323` in place). A correctly-scoped append that leaves that sentence untouched would not. The risk is in execution discipline, not in principle — and per §3's finding, this file's editing surface also cascades into the checksum manifest, widening the risk (see §3 of the option matrix, `OPT-A`).

**6. Would an additive successor artifact preserve provenance more safely?**
Yes. A new, separately named file that cites `ART-016` as the historical baseline — without editing it — touches zero frozen bytes and forces zero checksum-manifest update. This is strictly safer than any in-place edit, additive or not.

**7. Is a new reconciliation operation required?**
Yes. Whichever of Option A or Option B is eventually authorized, it constitutes a new class of write (reconciliation update or creation) distinct from `OP-01` (ledger), `OP-06` (validator), `OP-08` (eligibility-only zero-edit record), and `OP-09` (canonical-inventory creation). See §4 below — `NEW_RECONCILIATION_OPERATION_REQUIRED`.

**8. Does any validator or documentation currently hard-code 315?**
No functional dependency was found. `grep` across `docs/thesis/colab/model3b_spec_validator/` for `315`, `194`, `121` found exactly one hit: a docstring comment in `validate_frozen_baseline.py` ("Not a substantive future test (the 315-item PLANNED_ONLY inventory)"). Inspection of the surrounding code confirms this is descriptive prose only — no runtime assertion, comparison, or count check reads or depends on the literal value 315 anywhere in the Wave 1 tooling.

**9. Would changing 315 to 323 silently imply test execution?**
Only if done carelessly. Several existing 315-references are phrased as "None of the 315 tests were executed" — a like-for-like substitution to "None of the 323 tests were executed" preserves the correct meaning. The risk is a bare, unqualified restatement of the number without the "obligations, not executed" qualifier reappearing nearby, which is why §10's terminology distinction matters.

**10. Required terminology to distinguish four states:**
- **Inventory obligations**: a recorded future-test row with `status=PLANNED_ONLY` — exists as a specification, nothing more. 323 obligations exist today (194+121+8).
- **Implemented tests**: an obligation whose fixture/code has actually been written. 0 today.
- **Executed tests**: an implemented test that has actually been run (against synthetic or real data). 0 today (`|T_executed|=0`).
- **Passed tests**: an executed test whose outcome matched its `expected_behavior`. 0 today, since none has executed.

**11. Does any downstream dependency use 315 as a frozen baseline?**
Yes — eleven prose documents (REF-02 through REF-10, REF-12 in the accompanying CSV) cite 315 as a fixed comparison set from a specific past turn. All are correctly scoped as point-in-time attestations ("as of this turn, 0 collisions with the 315 existing IDs") and require no retroactive edit — they remain true statements about the past. One occurrence (REF-11, `model3b_v2/README.md` line 27) is framed as a present-tense project-status figure and is the one candidate for a future update.

**12. Can 315 remain the historical baseline while 323 becomes the current combined obligation count?**
Yes — this is the intended and recommended outcome, directly analogous to the pattern already used for `OPT-005-B` (retired but preserved for provenance) and for checksum handling throughout this session (historical hash never overwritten; a new hash is always an additive record). `315` = `HISTORICAL_BASELINE_COUNT` (ART-016, frozen, immutable). `323` = `CURRENT_COMBINED_OBLIGATION_COUNT` (established via `OP-09`, recorded in its audit, and now further reviewed in this document), coexisting without contradiction.

## 3. Option evaluation

Full nine-criterion assessment per option is in `WAVE_2_OD_005_RECONCILIATION_OPTION_MATRIX.csv`. Summary:

- **Option A** (`ADDITIVELY_UPDATE_EXISTING_RECONCILIATION`): technically additive at the paragraph level, but forces a cascading edit into the checksum manifest to keep `ART-016`'s tracked hash accurate, and raises the semantic risk of editing a document explicitly classified `FROZEN_V2_MILESTONE`. **Not recommended.**
- **Option B** (`CREATE_SUCCESSOR_RECONCILIATION_ARTIFACT`): touches zero frozen bytes, zero manifest cascading, smallest amendment surface, highest rollback clarity, and can be authored from scratch with correct obligation/implemented/executed/passed terminology. **Recommended.**
- **Option C** (`KEEP_EXISTING_RECONCILIATION_FROZEN_AND_USE_OP09_AUDIT_ONLY`): zero risk because zero action, but under-delivers on discoverability — the OP-09 audit is scoped to one operation, not catalogued as a general reconciliation artifact, and the gap between the frozen 315 and the true 323 would remain undocumented anywhere a future reader would think to look. **Viable but incomplete.**

## 4. New operation requirement

**`NEW_RECONCILIATION_OPERATION_REQUIRED`.** Neither `OP-08`, `OP-09`, `OP-06`, nor `OP-01` is reused or reinterpreted to cover this write. No operation ID is assigned in this turn: there is no frozen, generally-applicable identifier-allocation rule document in this repository (the `OP-01`..`OP-09` sequence was an ad hoc sequential convention observed across turns, not a codified rule), so assigning an ID now would not meet the instruction's bar of a deterministic, rule-authorized allocation. The next sequential, non-conflicting candidate would be `OP-10` (verified: no existing operation uses this ID), offered here only as the likely candidate for a future, separately authorized turn to formally adopt — not adopted by this review.

## 5. Recommendation

**Primary decision classification: `SUCCESSOR_RECONCILIATION_ARTIFACT_RECOMMENDED`.**

A future, separately authorized turn should: (1) formally assign a new operation ID (candidate `OP-10`) distinct from `OP-01`/`OP-06`/`OP-08`/`OP-09`; (2) create a new, explicitly-named successor reconciliation artifact that cites `ART-016` as the immutable historical baseline (315) and states the current combined obligation count (323) using the four-way terminology from §2 Q10; (3) leave `MODEL_3B_COMPLETE_NUMERICAL_DECISION_CONSISTENCY_AUDIT.md` and `MODEL_3B_V2_CHECKSUM_MANIFEST.csv` completely untouched. This review does not create that artifact, does not assign that operation, and does not modify any existing file. See `WAVE_2_OD_005_RECONCILIATION_REVIEW_DECISION_DRAFT.md` for the formal decision record.
