# WAVE 2 — OD-005 E1 Documentation Amendment Audit (OPT-005-B Retirement)

Status: **NARROW ADDITIVITY REVIEW COMPLETE — E1 CLEARED FOR LOCAL FREEZE AUTHORIZATION**. This audit covers only the E1 documentation-tier subwave (OP-02, OP-03, OP-04, OP-05, OP-07). E2, E3, and E4 are not authorized and were not touched. §13 below records a follow-up narrow additivity review triggered by the `1 deletion` reported in the initial `git diff --stat`.

Authoritative baseline for this turn: `6a8a400ee1c7752f99957c36649f58e32307b642` (local HEAD = origin/main, verified clean before amendment).

Execution inputs (all pre-frozen, unmodified by this turn): `WAVE_2_OD_005_EXACT_AMENDMENT_EXECUTION_SPECIFICATION.md`, `WAVE_2_OD_005_EXACT_AMENDMENT_OPERATIONS.csv`, `WAVE_2_OD_005_EXACT_ADDITIVE_TEXT_CATALOG.csv`, `WAVE_2_OD_005_EXACT_TEST_OBLIGATIONS.csv`, `WAVE_2_OD_005_EXACT_CHECKSUM_AND_ROLLBACK_PLAN.md`, `WAVE_2_OD_005_EXECUTION_SPEC_CONSISTENCY_AUDIT.md`.

---

## 1. E1 operation IDs and targets

| Operation | Target path | Pre-amendment SHA-256 | Post-amendment SHA-256 |
|---|---|---|---|
| OP-02 | `evidence/WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv` | `80f6a8c8b9d11497ffb817eb4a573d0c435a71d4263d5041809ffdc9391d3efd` | `99146a3b07afcf89e9fffa25e3c2e520943e3c53d50ac2d2b05502523fa8eb3d` |
| OP-03 | `adjudication/WAVE_2_OD_005_DRAFT_ADJUDICATION.md` | `762f1a5c2a75b237f5016557f3a5222ce887cd4ebe40b83407ce6e40f8fd4d3b` | `82c357943309b5d239173e93a62f61425cc2203e69f955c3525037364dd21ce9` |
| OP-04 | `adjudication/WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md` | `f3a395ffd0b8f8a5867de19ebb677b517f06934de417880ef40d72221866c8f0` | `049c4d13b7469fbe96747668b20d85468fa44d26811f9e0b134dd04fda5cb788` |
| OP-05 | `planning/WAVE_2_MATHEMATICAL_CONTRACT.md` | `4df948ad08b15d8be381927c66e52856fc31fdb564a5d2ffbe775e52e818a043` | `15701b6152cd4ed40f9a23a2fb1aa9a33ffd5f479b05d87cd0478a4c16ed679e` |
| OP-07 | `adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_PLAN.md` | `887db2a1ae72207faeae8a204badec8dd0611bf78132f27de710dc772c576791` | `f758486eba436bc96e412ee0104f7cdd0a64b3961fcb5ea213645eaac14ade25` |

All five pre-amendment hashes matched the frozen execution specification's historical table exactly before any edit. All five post-amendment hashes changed from their pre-amendment values. The historical checksum manifest (`WAVE_2_OD_005_EXACT_CHECKSUM_AND_ROLLBACK_PLAN.md`) was not overwritten; the values above are recorded only in this new audit artifact.

## 2. Insertion-anchor verification

All 5 insertion anchors were grep-confirmed to resolve to exactly one occurrence in their target file before insertion. OP-02's anchor matched the specification's literal ASCII text directly. OP-05's anchor required matching the source's actual Unicode em dash (`—`) and section-sign (`§`) characters rather than the specification's ASCII paraphrase (`--`, `S21`) of the same sentence; once matched verbatim against the file it resolved uniquely. Result: 5/5 anchors uniquely resolved. See §13.4 for the dedicated Unicode-anchor re-verification.

## 3. Exact-text presence

5/5 authorized additive-text insertions (ATX-02, ATX-03, ATX-04, ATX-05, ATX-07) applied. Post-insertion occurrence count: exactly 1 per target (5/5). Duplicate insertions: 0. Missing insertions: 0.

## 4. Idempotency result

Pre-insertion check confirmed 0 prior occurrences of each additive text in its target. No idempotency conflict. `MODEL_3B_V2_OD_005_E1_IDEMPOTENCY_REQUIRES_REVIEW` was not triggered.

## 5. Mathematical-invariance result

0 of the 13 mathematical objects (conditional intensity, `n=alpha/beta`, exact null, log-likelihood, full Hessian, `J`, `Var`, `R_attempted,c=1000`, accounting invariant, `Coverage_c`, profile likelihood, plus AC-M2-03's `threshold_status`/`threshold_value`) changed. ATX-05 (inserted into `WAVE_2_MATHEMATICAL_CONTRACT.md`) is a prohibited-interpretation clause that restates these objects by name without redefining any of them; `threshold_value` remains `NULL` and `threshold_status` remains `OPEN_REQUIRES_ADJUDICATION` in the S6 registry row, unchanged. Mathematical-change count: 0.

## 6. Requirement-nonloss result

0 existing requirements or test obligations removed. All 5 postconditions from the Operations CSV (target retains 100% of pre-amendment content, append-only) verified by inspection of the diffs applied. `MODEL_3B_NUMERICAL_TEST_INVENTORY.csv` and `MODEL_3B_AMENDMENT_TEST_INVENTORY.csv` (the 315-test inventory) were not touched. Existing-test-loss count: 0.

## 7. Identifier-preservation and provenance result

`OPT-005-B` appears in the newly inserted text in OP-02, OP-03, OP-04, and OP-05's targets as a preserved historical identifier — never deleted, never reused, never renamed. `OD-005` is unchanged. Identifier-deletion count: 0. No `decision_id`, `option_id`, `requirement_id`, `gate_id`, `test_id`, `evidence_id`, `blocker_id`, DOI, checksum, or commit hash was deleted or reused anywhere in this turn.

## 8. E2/E3/E4 exclusion result

`docs/thesis/pilot_annotation/model3b_v2/planning/WAVE_2_OPEN_DECISION_LEDGER.csv` (OP-01/E4), `docs/thesis/colab/model3b_spec_validator/schema_validator.py` (OP-06/E3), and `docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_TEST_IMPACT.csv` (OP-08/E2) show 0 changes in `git diff --stat` against baseline `6a8a400`. OP-01 executed: NO. OP-06 executed: NO. OP-08 executed: NO.

## 9. Rollback readiness

Each of the 5 modified targets can be restored individually via `git checkout 6a8a400ee1c7752f99957c36649f58e32307b642 -- <path>`, verified against the pre-amendment SHA-256 values in §1. No global reset, broad checkout, or `git clean` was used or is required. Rollback readiness: CONFIRMED, not exercised (no stop condition was triggered).

## 10. Protected-artifact verification

`git diff --stat` against baseline confirms exactly 5 tracked files modified (the 5 E1 targets) plus 1 new untracked audit artifact (this file). The open-decision ledger, the 315-test inventory, the validator, all Python files, the frozen execution-specification artifacts, the retirement review artifacts, the amendment planning artifacts other than the 5 authorized targets, the evidence package's other rows, numerical-decision documents, Atlas application code, Phase D artifacts, and `.gitignore` show 0 changes. Protected-artifact change count: 0.

## 11. Secret scan

Grep for credential/secret/password/token/bearer/PEM-header patterns across the 5 modified targets returned 3 matches, all pre-existing (not part of the inserted text) and all non-secret: 2 uses of "token" in `WAVE_2_MATHEMATICAL_CONTRACT.md` referring to model-notation disambiguation labels (`M0-gate`, `M0-null`), and 1 use of "token" in `WAVE_2_OD_005_NARROW_AMENDMENT_PLAN.md` referring to a prior turn's own secret-scan description. 0 real secrets found. No rollback triggered.

## 12. Final E1 status (pre-additivity-review, superseded by §13)

`MODEL_3B_V2_OD_005_E1_DOCUMENTATION_AMENDMENT_READY_FOR_REVIEW`

---

## 13. Narrow additivity review (follow-up turn, `MODEL_3B_V2_OD_005_E1_REQUIRES_NARROW_ADDITIVITY_REVIEW`)

Trigger: initial `git diff --stat` reported `5 files changed, 9 insertions(+), 1 deletion(-)` against baseline `6a8a400ee1c7752f99957c36649f58e32307b642`, apparently in tension with E1's additive-only contract.

### 13.1 Locate the deletion (Audit A)

`git diff --numstat` against baseline, per target:

| Target | Hunks | Lines added | Lines deleted |
|---|---|---|---|
| OP-02 (`WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv`) | 1 | 1 | 1 |
| OP-03 (`WAVE_2_OD_005_DRAFT_ADJUDICATION.md`) | 1 | 2 | 0 |
| OP-04 (`WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md`) | 1 | 2 | 0 |
| OP-05 (`WAVE_2_MATHEMATICAL_CONTRACT.md`) | 1 | 2 | 0 |
| OP-07 (`WAVE_2_OD_005_NARROW_AMENDMENT_PLAN.md`) | 1 | 2 | 0 |

All 1 deletion is confined to OP-02's target. The deleted line is nonblank. The deleted line contains an identifier (`OPT-005-B`'s row key). The deleted line contains no formula. The deleted line contains a status/requirement field (`SPECIFICATION_CLARIFICATION_REQUIRED`, end-of-row). An equivalent line remains present after amendment — the inserted line is the deleted line's full text plus the authorized additive text appended within the same CSV field, unmodified otherwise.

### 13.2 Classification (Audit B)

**A. `LINE_REPLACEMENT_WITH_BASELINE_CONTENT_PRESERVED`.** OP-02's target is a CSV with one logical row per physical line; a line-oriented diff necessarily represents any within-row edit as a full-line delete+insert pair even though the edit is a pure field-level append. Every baseline semantic element of that row is preserved byte-for-byte in the post-E1 line.

### 13.3 Baseline subsequence test (Audit C)

For each of the 5 targets, the exact authorized additive-text block was removed from the in-memory working-tree content (file not modified) and the result compared against the baseline blob (`git show 6a8a400:<path>`):

| Target | Result |
|---|---|
| OP-02 | `EXACT_BASELINE_RECOVERED` |
| OP-03 | `EXACT_BASELINE_RECOVERED` |
| OP-04 | `EXACT_BASELINE_RECOVERED` |
| OP-05 | `EXACT_BASELINE_RECOVERED` |
| OP-07 | `EXACT_BASELINE_RECOVERED` |

5/5 `EXACT_BASELINE_RECOVERED`. `reconstruct(post_E1) == baseline_content` holds for all 5 targets, byte-for-byte.

### 13.4 Unicode anchor check (Audit D)

OP-02: anchor discovery used the specification's literal ASCII text directly; no Unicode adaptation was needed; anchor resolved exactly once; unchanged; not normalized; recovered byte-identical after excluding the insertion (§13.3).

OP-05: the specification's anchor quote used ASCII paraphrase (`--`, `S21`); the repository source uses Unicode em dash (`—`) and section sign (`§`) at that location. The actual Unicode anchor was used for location matching only, resolves exactly once, was not changed, was not normalized, and was not replaced by the ASCII paraphrase in the file (the file still reads `—` and `§`, not `--`/`S21`). Recovered byte-identical after excluding the insertion (§13.3). Anchor-discovery adaptation is confirmed distinct from additive-text modification: the inserted text itself matches `WAVE_2_OD_005_EXACT_ADDITIVE_TEXT_CATALOG.csv`'s `ATX-05` value with no substitution of ASCII for Unicode or vice versa.

### 13.5 Semantic nonloss (Audit E)

Cross-checked against §13.3's byte-exact baseline recovery, which is a stronger guarantee than a semantic diff: since removing only the authorized insertion reproduces the baseline exactly, byte-for-byte, no baseline semantic element of any kind could have been altered.

- Baseline semantic element loss count: 0
- Identifier loss count: 0 (`OD-005`, `OPT-005-B`, all evidence/requirement/test IDs unaffected)
- Formula loss count: 0 (all S1-S4 objects, `AC-M2-03` fields unaffected)
- Status loss count: 0 (`SPECIFICATION_CLARIFICATION_REQUIRED`, `OPEN_REQUIRES_ADJUDICATION`, `threshold_status`, `DRAFT_CANDIDATE_SET_FOR_REVIEW`, `WITHHELD` triplet all unaffected)
- Reference loss count: 0 (all citations, source references, denominator/coverage rules, provenance statements, historical checksums unaffected)

### 13.6 Additivity decision (Audit F)

Condition 1 satisfied: all 5 targets return `EXACT_BASELINE_RECOVERED`. The reported `1 deletion` is a git line-diff artifact of a single-physical-line CSV field append (OP-02), not a rewrite or loss of baseline content. **No correction was required** — the `LINE_REPLACEMENT_WITH_BASELINE_CONTENT_PRESERVED` classification's exact-baseline-bytes condition is already met, so the correction rule's precondition ("if exact baseline bytes are not recoverable") does not apply.

### 13.7 Post-review verification

- Modified target count: 5 (unchanged)
- New audit artifact count: 1 (this file; no second artifact created)
- E1 operation set: exactly OP-02, OP-03, OP-04, OP-05, OP-07 (unchanged)
- Exact insertion count: 5/5 (unchanged)
- Duplicate insertion count: 0
- Insertion-anchor resolution: 5/5
- All 5 postconditions: PASS
- Post-E1 hashes: unchanged from §1 (no file was touched during this review)
- Mathematical-change count: 0
- Requirement-loss count: 0
- Existing-test-loss count: 0
- Identifier-deletion count: 0
- Unauthorized-operation count: 0
- OP-01 / OP-06 / OP-08: unexecuted (NO / NO / NO)
- Ledger, validator, 315-test inventory: unchanged
- `git diff --cached --stat`: empty
- Secret scan (this review): re-scanned same 5 targets, 0 new findings beyond §11's 3 pre-existing benign matches

### 13.8 Final E1 status

`MODEL_3B_V2_OD_005_E1_DOCUMENTATION_AMENDMENT_READY_FOR_REVIEW` — narrow additivity review complete, deletion explained and classified as `LINE_REPLACEMENT_WITH_BASELINE_CONTENT_PRESERVED` (Audit F condition 1 met), no correction applied, no target touched, working tree unchanged since §1. E1 is cleared to proceed to a separately authorized local commit freeze. E2, E3, E4, and the overall OD-005 ledger status remain unauthorized/open, unaffected by this review.
