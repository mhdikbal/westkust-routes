# WAVE 2 — OD-005 Exact Checksum and Rollback Plan for Retirement of OPT-005-B

Status: **SPECIFICATION-ONLY**. No hash in this document has been computed for a post-amendment state, because no amendment has been executed. No rollback has been run.

Baseline: local HEAD = origin/main = `81af816e7d8691ae515ab22dc671499ddfa36aee`.

---

## 1. Hash formula

```math
h_f = \operatorname{SHA256}(\operatorname{bytes}(f))
```

Computed via `sha256sum <path>` against the working-tree file, matching the committed blob content at the stated commit (verified via `git show <commit>:<path> | sha256sum`, not shown here to avoid full-content leakage — only the resulting hash is recorded).

## 2. Historical hash table (8 targets, computed this turn at baseline `81af816e7d8691ae515ab22dc671499ddfa36aee`)

| operation_id | historical_path | historical_commit | historical_sha256 |
|---|---|---|---|
| OP-01 | `docs/thesis/pilot_annotation/model3b_v2/planning/WAVE_2_OPEN_DECISION_LEDGER.csv` | `81af816e7d8691ae515ab22dc671499ddfa36aee` | `023b273e49013c2bedf0f237579f961a7a506c7d2e265ca5e8615d73efe67fa5` |
| OP-02 | `docs/thesis/pilot_annotation/model3b_v2/evidence/WAVE_2_OD_005_006_015_EVIDENCE_TO_OPTION_MATRIX.csv` | `81af816e7d8691ae515ab22dc671499ddfa36aee` | `80f6a8c8b9d11497ffb817eb4a573d0c435a71d4263d5041809ffdc9391d3efd` |
| OP-03 | `docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_DRAFT_ADJUDICATION.md` | `81af816e7d8691ae515ab22dc671499ddfa36aee` | `762f1a5c2a75b237f5016557f3a5222ce887cd4ebe40b83407ce6e40f8fd4d3b` |
| OP-04 | `docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md` | `81af816e7d8691ae515ab22dc671499ddfa36aee` | `f3a395ffd0b8f8a5867de19ebb677b517f06934de417880ef40d72221866c8f0` |
| OP-05 | `docs/thesis/pilot_annotation/model3b_v2/planning/WAVE_2_MATHEMATICAL_CONTRACT.md` | `81af816e7d8691ae515ab22dc671499ddfa36aee` | `4df948ad08b15d8be381927c66e52856fc31fdb564a5d2ffbe775e52e818a043` |
| OP-06 | `docs/thesis/colab/model3b_spec_validator/schema_validator.py` | `81af816e7d8691ae515ab22dc671499ddfa36aee` | `bdf6d5be403295b77ba36df4dc0c6f087afba404bf26d15e902266ae8212dbfe` |
| OP-07 | `docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_PLAN.md` | `81af816e7d8691ae515ab22dc671499ddfa36aee` | `887db2a1ae72207faeae8a204badec8dd0611bf78132f27de710dc772c576791` |
| OP-08 | `docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_NARROW_AMENDMENT_TEST_IMPACT.csv` | `81af816e7d8691ae515ab22dc671499ddfa36aee` | `a3f2c7e5df983387885307bcccb87a39b610ac6de001127374aca2029118ecd9` |

All 8 hashes computed directly from the working tree this turn (`sha256sum`), with the working tree confirmed identical to commit `81af816e7d8691ae515ab22dc671499ddfa36aee` (`git status --short` clean, `git diff --stat` empty at the time of computation).

**None of these 8 historical hashes is overwritten by this specification.** No file listed above has been modified this turn.

## 3. Post-amendment hash procedure (future, not run)

For each operation, once (and only once) its owning subwave is separately authorized and the exact additive text from `WAVE_2_OD_005_EXACT_ADDITIVE_TEXT_CATALOG.csv` is actually applied:

```text
post_amendment_path            = historical_path (unchanged path)
post_amendment_commit_future   = the commit hash of the future freeze that includes this edit (not yet created)
post_amendment_sha256_future   = SHA256(bytes(f)) computed AFTER the edit, recorded as a NEW additive row
                                  in a future WAVE_2_OD_005_AMENDMENT_EXECUTION_AUDIT.md (not yet created)
operation_id                   = OP-01 through OP-08 (this table's key)
review_decision_reference      = WAVE_2_OD_005_RETIREMENT_REVIEW_DECISION_DRAFT.md (APPROVED_WITH_LIMITATIONS_TO_RETIRE)
```

Each post-amendment hash is an **additive provenance record**, appended alongside — never in place of — the historical hash in this table. This table itself, once execution is authorized, is expected to gain 8 new columns or a companion table recording the post-amendment values; this specification does not pre-populate those values, since no edit has occurred.

## 4. Rollback plan

### 4.1 Pre-amendment baseline

```text
pre_amendment_baseline_hash = 81af816e7d8691ae515ab22dc671499ddfa36aee
```

### 4.2 Exact affected paths (identical to §2's 8 rows)

Listed in §2 above — 8 paths, 8 operation IDs, 1:1.

### 4.3 Per-file rollback command

For any operation `OP-nn` that has been executed and must be reverted:

```text
git checkout 81af816e7d8691ae515ab22dc671499ddfa36aee -- <historical_path>
```

using the exact `historical_path` value from §2's row for that `operation_id`.

### 4.4 Abort-before-staging rule

If any post-application audit check (§9 of `WAVE_2_OD_005_EXECUTION_SPEC_CONSISTENCY_AUDIT.md`, once re-run against an actually-amended tree) fails, the amendment execution turn must stop before running `git add` on any of the 8 paths. No partial staging is permitted.

### 4.5 Working-tree restoration method if audit fails

1. For every one of the 8 paths whose current SHA-256 does not equal its §2 historical value, run the §4.3 rollback command for that path.
2. Re-compute SHA-256 for each restored path.
3. Confirm every restored hash equals its §2 historical value exactly (byte-for-byte match, not a semantic/approximate match).
4. Confirm `git status --short` shows 0 modified tracked paths for the 8 target paths after restoration.
5. Do not delete any newly-created file (e.g. a draft audit report) — move it aside or leave it untracked; only tracked-file content reverts via `git checkout`.

### 4.6 Prohibition on overwriting historical records

No rollback command in this plan ever uses `git commit --amend`, `git rebase`, `git push --force`, or any other history-rewriting operation. Rollback is always a forward-moving `git checkout <historical_commit> -- <path>` on the working tree, never a rewrite of `81af816` or any earlier commit.

### 4.7 Verification that restored hashes match

Mandatory before declaring rollback complete: re-run `sha256sum` on all 8 paths and diff the result against §2's table. 0 mismatches required.

### 4.8 No partial amendment state

If fewer than all operations in a given subwave (E1, E2, E3, or E4) can be completed and verified, the entire subwave must be rolled back via §4.3-§4.7 — a subwave is atomic; there is no state where, for example, 3 of E1's 5 operations remain applied while 2 are reverted.

### 4.9 No server rollback

Server synchronization is out of scope for any future amendment-execution turn until a local freeze of that execution has been reviewed and separately authorized, per this session's established provenance-splitting pattern (local freeze → separate push+sync authorization). This plan defines no server-side rollback procedure because no server-side change is authorized to occur before that separate freeze.

## 5. Explicit non-execution statement

No SHA-256 in §3 has been computed. No `git checkout` command in §4 has been run. This document is a plan for a future, separately authorized amendment-execution turn.
