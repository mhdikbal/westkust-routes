# WAVE 2 — OD-005 New Canonical Test Inventory — Rollback Plan (Specified, Not Exercised)

Status: **SPECIFICATION-ONLY**. Nothing described here has been executed. No inventory file exists at the target path as of this turn. This plan applies only to a future, separately authorized turn that actually runs `OP-09`.

Authoritative baseline: `47525d62404ba0a3b0bf72e4436c98b07a967dbd`.

---

## 1. Pre-creation baseline facts (verified this turn)

```text
target_path_exists_at_baseline: NO
MODEL_3B_NUMERICAL_TEST_INVENTORY.csv:  194 data rows (unchanged)
MODEL_3B_AMENDMENT_TEST_INVENTORY.csv:  121 data rows (unchanged)
OP-08: ELIGIBILITY_ONLY_ZERO_EDIT_RECORD (unchanged)
proposed IDs present in either existing file: 0
```

## 2. Rollback preconditions (for a future creation turn)

Before any future turn runs `OP-09`, it must record:

1. confirmation the target path does not exist immediately before creation;
2. the baseline commit hash it is executing against;
3. the pre-creation SHA-256 of both existing inventories (for byte-identity verification after creation).

## 3. Rollback procedure (if a future creation turn fails its own postcondition checks)

1. Verify the file did not exist at the baseline that future turn recorded (per §2.1).
2. Remove only the newly created canonical inventory file (`MODEL_3B_OD005_AMENDMENT_TEST_INVENTORY.csv`) — a single, explicit path deletion, never a wildcard or directory-level removal.
3. Remove only that future turn's own creation-audit artifact (its equivalent of this session's `WAVE_2_OD_005_NEW_CANONICAL_TEST_INVENTORY_SPEC_AUDIT.md`, if a further "applied" audit was produced) — never this specification-stage document, which records intent, not execution.
4. Verify both paths are absent (`ls` / `git status` shows neither as tracked or untracked-pending).
5. Verify the two existing inventories are byte-identical to their pre-creation SHA-256 (per §2.3).
6. Verify no ledger, validator, E1-artifact, or test-execution change occurred as a side effect.
7. Do not use `git clean`, a broad `git checkout .`, or any recursive deletion — only the two named paths above may be touched.

## 4. Explicit non-execution statement

No step in §3 has been run. This turn created 6 specification/review artifacts only; it did not create, modify, or delete the canonical inventory file, either existing inventory, `OP-08`, the ledger, the validator, or any E1 artifact.
