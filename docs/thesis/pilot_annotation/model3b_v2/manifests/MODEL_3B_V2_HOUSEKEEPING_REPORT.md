# Model 3B V2 — Repository Organization and Housekeeping Report

**Authoritative baseline:** `9da3d9fec04341e5fb71ecb934b8acdc59f7d044`
**Scope:** repository hygiene only — inventory, reorganization, cache cleanup, path-reference updates. No amendment, no adjudication, no code/model work, no staging/commit.

## 1. What was inventoried

153 artifacts matching the instruction's inventory criteria (filename contains `MODEL_3B`/`WAVE_1`/`WAVE_2`/`NUM-DEC`, or resides in a Model3B validator/code folder, or is one of the enumerated frozen/Wave1/Wave2/evidence/adjudication artifact sets):

- 42 V2-milestone Markdown/CSV artifacts (moved this turn)
- 51 pre-V2 historical-archive Markdown/CSV documents (kept in place)
- 14 Wave 1 validator package files (`.py` + fixture `.csv`, kept in place)
- 12 M0/M2/M3 estimation-code files (kept in place)
- 34 CD-era simulator code files (kept in place)

Full detail: `MODEL_3B_V2_ARTIFACT_INVENTORY.csv`.

## 2. What moved and why

The 42 V2-milestone Markdown/CSV artifacts — the 5 frozen V2 specs, 8 NUM-DEC adjudications, 2 reconciliation artifacts, 3 numerical-consistency outputs, 10 Wave 2 planning contracts, the open-decision adjudication map + batch matrix, the 5-file OD-005/006/015 literature-evidence package, the 4 adjudication drafts, and the 3 specification-clarification-review artifacts — moved from flat placement in `docs/thesis/pilot_annotation/` into a classified subfolder structure under `docs/thesis/pilot_annotation/model3b_v2/` (`specifications/`, `numerical_decisions/`, `reconciliation/`, `planning/`, `evidence/`, `adjudication/`). This is the complete, currently-active V2 milestone corpus — everything the ongoing OD-005/006/015 adjudication work actively references.

Every move used a plain filesystem `mv` (not `git mv`, to avoid staging). Every file's SHA-256, byte size, and (for CSVs) row/column count were captured before the move and reverified identical after. **0 of 42 mismatches** — full detail in `MODEL_3B_V2_MOVE_MANIFEST.csv`. No file was renamed; only its directory changed.

## 3. What was deliberately excluded, and why

- **Wave 1 validator Python package** (`docs/thesis/colab/model3b_spec_validator/`, 14 files including test fixtures): NOT relocated. It is a runtime-imported Python package; moving it would break its own import path, the narrow `.gitignore` whitelist keyed to its current location, and the test suite's relative fixture paths. Moving it risked exactly the failure mode the governing instruction's stop-conditions warn against ("validator tidak dapat menemukan source setelah path update plan"). It stays at its current path as one unit. The `model3b_v2/validators/` subfolder was created per the target structure but is intentionally left empty this turn.
- **M0/M2/M3 estimation code** (`docs/thesis/colab/model3b_tournament_harness/`, 12 files): protected estimation code, explicitly out of scope for a documentation reorganization.
- **CD-era simulator code** (`docs/thesis/colab/model3b_cd_simulator/`, 34 files): pre-V2 historical archive, out of scope.
- **51 pre-V2 historical Model3B documents** still in `docs/thesis/pilot_annotation/` (the `MODEL_3B_AMENDMENT_*`, `MODEL_3B_CD_*`, `MODEL_3B_PHASE0_*`, the original — non-V2 — `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv`, and similar): inventoried but not relocated, per the instruction's own principle "jangan memindahkan ... arsip sejarah." These remain fully accessible at their existing paths; nothing about them changed.

## 4. Cache and temporary-artifact cleanup

Deleted 55 `__pycache__` files across 6 directories, all within Model3B-relevant code paths and all matching the housekeeping allowlist (`__pycache__/`, `*.pyc`):

| Directory | Files removed |
|---|---|
| `docs/thesis/colab/model3b_spec_validator/__pycache__/` | 5 |
| `docs/thesis/colab/model3b_spec_validator/tests/__pycache__/` | 4 |
| `docs/thesis/colab/model3b_tournament_harness/__pycache__/` | 9 |
| `docs/thesis/colab/model3b_cd_simulator/__pycache__/` | 19 |
| `docs/thesis/colab/model3b_cd_simulator/tests/__pycache__/` | 16 |
| `docs/thesis/colab/__pycache__/` | 2 |

Pre-deletion safety check confirmed: none of these files were git-tracked, none were symlinks, all are mechanically rebuildable (`.pyc` bytecode), none are evidence/dataset/manifest/dependency-lock/source-code, and deletion does not affect any research result. All 55 `.py` source files across the three code directories were verified present and untouched after cleanup.

**Zone.Identifier sidecar files**: 19 exist in the repository, but **0 are inside Model3B-relevant paths** (`docs/thesis/pilot_annotation/` or `docs/thesis/colab/`) — they are scattered at the repository root and `docs/` root, paired with unrelated Atlas/ontology/other-project documents. Per the instruction's own scope boundary and to avoid unilateral deletion outside this task's authorized Model3B-V2 scope, **none were deleted**. They are noted here for a possible separate, explicitly-authorized repo-wide cleanup pass.

## 5. Path-reference updates

Searched the full repository for literal full-path references (`docs/thesis/pilot_annotation/<old-filename>`) to the 42 moved files, distinct from informal bare-filename mentions in prose (which remain valid citations regardless of file location and were not touched):

- **0 full-path cross-references found among the 42 moved files themselves** — every internal Model3B document that cites another Model3B document does so by bare filename, not a literal path, so no content edit was needed inside the moved corpus.
- **`.gitignore`**: required a real update. Removed 39 individual per-filename whitelist lines. Of the 42 moved files, 39 were already committed to `HEAD` (`9da3d9f`) and therefore had an existing per-file whitelist entry to remove; the remaining 3 (`WAVE_2_OD_005_SPECIFICATION_CLARIFICATION_REVIEW.md`, `WAVE_2_OD_006_SPECIFICATION_CLARIFICATION_REVIEW.md`, `WAVE_2_OD_005_006_CLARIFICATION_RECONCILIATION.md`) were genuinely **uncommitted working-tree files** carried over from the most recent specification-clarification-review turn (that turn was explicitly review-only and prohibited staging/commit; no freeze turn followed it before this housekeeping task began) — they had no prior whitelist entry to remove, confirmed via `git ls-tree -r HEAD --name-only` (39/42 present in the tree, these 3 absent). All 3 are still handled correctly by this reorganization: content-hash-verified on move like every other file, and now covered by the new block-structured whitelist below. Added one narrow whitelist section for `docs/thesis/pilot_annotation/model3b_v2/` mirroring this repository's own established convention elsewhere in `.gitignore` (block-by-default + per-subfolder `!dir/` + extension-scoped `!dir/*.md`/`!dir/*.csv` whitelisting, the same pattern already used for `model3b_spec_validator/`, `model3b_tournament_harness/`, and `model3b_cd_simulator/`). No recursive (`**`) glob was introduced. Verified mechanically: all 42 moved files now show as `??` (visible/untracked, stageable in a future turn) and 0 remain `!!` (ignored) inside `model3b_v2/`. `git diff --stat` against `HEAD` shows 39 files as deletions-at-old-path (the previously-committed ones) plus `.gitignore` modified — consistent with 39 tracked + 3 never-committed.
- **5 literal full-path references found in one file outside the Model3B artifact corpus**: `CLAUDE_MODEL_3B_MATHEMATICAL_SPECIFICATION_V2_INSTRUCTIONS.md` (repository root — a governing instruction/prompt-history document from an earlier turn, not one of the 42 V2-milestone artifacts or any other tracked/frozen artifact set this housekeeping task governs). These 5 references (to the 5 frozen V2 specs, by old path) were **deliberately left unmodified** — editing a historical instruction document is outside this task's narrow scope (path-reference updates are authorized only for artifacts within the reorganization's own governed corpus, not arbitrary repository-root instruction files), and doing so would risk altering a record of what instruction was actually given at the time. Flagged here for a possible future, separately-authorized reference-update pass if desired.
- No checksum was overwritten. Two genuine historical-checksum citations were found and cross-verified rather than modified: `MODEL_3B_NUM_DEC_03_M2_EXACT_NULL_ADJUDICATION.md`'s checksum (`a7e8ad2c...`, cited in `MODEL_3B_COMPLETE_NUMERICAL_DECISION_CONSISTENCY_AUDIT.md`) still matches its content at the new path exactly; `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv`'s original checksum (`d4d4d3f5...`, cited in `MODEL_3B_RECOVERY_PROTOCOL_V2.md`) is for a file that was not moved and remains valid unchanged. See `MODEL_3B_V2_CHECKSUM_MANIFEST.csv`.

## 6. Verification summary

All items from the instruction's §19 mechanical-verification checklist were checked directly (not assumed):

- 42/42 target artifacts located under `model3b_v2/`
- 0 duplicate artifacts, 0 filename collisions, 0 missing artifacts
- 0 content-hash mismatches, 0 size mismatches, 0 CSV row/column-count mismatches
- 0 broken internal cross-references (none existed to begin with — bare-filename citation style throughout)
- 0 research identifiers removed or changed (decision_id/evidence_id/gate_id/requirement_id/NUM-DEC IDs untouched — content byte-identical)
- 0 checksum history overwritten
- All 55 deleted files belong to the housekeeping allowlist (`__pycache__`/`.pyc`)
- 0 cache or Zone.Identifier artifact remains inside the Model3B target paths
- 0 source code deleted (55 `.py` files across validator/harness/simulator confirmed present)
- 0 research data or evidence deleted
- 0 staged paths (`git diff --cached` empty; moved files show as untracked, per plan)

## 7. Epistemic boundaries — unchanged, verified directly against source files

```
Model 3B-CD V1 = MODEL_VALIDATION_FAILURE
Historical inference = NOT_AUTHORIZED
Hawkes family = NOT_RULED_OUT
Phase D = COMPLETED_VALID_NEGATIVE_RESULT / DO NOT RERUN
NUM-DEC-07 = DEFERRED
tau final = UNSET
ROPE = DEFERRED (NUM-DEC-07 and open-decision OD-016 both)
M3 blockers = 8 OPEN
315 substantive tests = NOT EXECUTED
OD-005 final decision = WITHHELD
OD-006 final decision = WITHHELD
OD-015 final decision = WITHHELD
```

Open-decision ledger distribution reverified directly: 16 `OPEN_REQUIRES_ADJUDICATION`, 1 `DEFERRED` (**OD-016**, ROPE epsilon_n — not "OD-07," which does not exist in the Wave 2 open-decision ledger; that ID belongs to the separate, earlier NUM-DEC numerical-decision ledger), 1 `NONBLOCKING_CLARIFICATION`.

## 8. Substantive next step (not begun this turn)

Per the housekeeping instruction's explicit separation requirement, this turn did **not** create an OD-005 amendment, did not decide retire-vs-concretize for `OPT-005-B`, did not modify any adjudication draft, and did not change OD-006's status. The next substantive step, separately authorized, is:

```
OD-005 NARROW ADDITIVE NONNUMERICAL AMENDMENT PLAN
```

OD-006 does not require a separate amendment for its procedural sub-question (already resolvable by cross-document reconciliation, per the specification-clarification review), but its substantive final choice (`Coverage_c` vs. `CoverAndValid_c`) remains `IMPLEMENTATION_DEPENDENT_FINAL_DECISION`, unchanged by this housekeeping pass.

## 9. Git state

Working tree after this turn: 42 files moved (shown as deleted-at-old-path + untracked-new-at-new-path), `.gitignore` modified in place, 55 cache files deleted (were untracked/ignored, so their removal produces no git status change), 5 new manifest/README files created (untracked). **Nothing staged.** No commit, push, sync, or deploy performed.
