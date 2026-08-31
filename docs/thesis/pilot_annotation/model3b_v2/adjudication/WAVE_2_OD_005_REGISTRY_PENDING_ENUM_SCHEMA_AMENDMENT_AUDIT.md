# WAVE 2 — OD-005 Registry Pending-Enum Schema Amendment — Audit

Status: **SCHEMA AMENDMENT APPLIED IN WORKING TREE, NOT STAGED, NOT COMMITTED**.

Authoritative baseline: `a2d2e71ee682bf39ca5fd9257cad3bbdf7628d59`.

---

## 1. Target

```text
Target schema path: docs/thesis/pilot_annotation/model3b_v2/adjudication/WAVE_2_OD_005_OPERATION_REGISTRY_SCHEMA.csv
Target row: column_name = historical_status (column_order = 11)
```

## 2. Hash before/after

```text
Pre-amendment SHA-256:  4554e409dfc3e6b5ea53ddc6c358e770b66d2a38f68a8efda55b7b8a1c1cb7bd
Post-amendment SHA-256: c1464dd94b9a87bf1f1c81beb8e7f03762eebbc59c23c48ce8b1d6ef6c8811e9
```

## 3. Schema shape before/after

```text
Columns:            10 -> 10 (unchanged)
Data rows:           16 -> 16 (unchanged)
Unique column_order: 16 -> 16 (unchanged)
Unique column_name:  16 -> 16 (unchanged)
```

## 4. historical_status row — old vs new

**Old `allowed_values`:**
```text
FROZEN (only value expected for OP-01..09)
```

**New `allowed_values`:**
```text
FROZEN, PENDING_FREEZE (OP-10 and any future operation's registry row, applied in the working tree before push/server sync; see WAVE_2_OD_005_OP10_ENUM_CONTRACT_DECISION_DRAFT.md)
```

**Old `validation_rule`:**
```text
must equal FROZEN for any operation whose defining record has been committed; a PROPOSED value would mean the operation is not yet real
```

**New `validation_rule`:**
```text
must equal FROZEN for any operation whose defining record has been committed, pushed, and server-synced; must equal PENDING_FREEZE only in the interval between working-tree registry-row application and push/server sync (Model A: PENDING_FREEZE -> FROZEN, no intermediate token, per WAVE_2_OD_005_OP10_ENUM_CONTRACT_DECISION_DRAFT.md); a PROPOSED value would mean the operation is not yet real
```

All other fields of the `historical_status` row (`column_order`, `column_name`, `data_type`, `required`, `unique`, `foreign_reference`, `semantic_definition`, `source_basis`) are byte-identical to baseline.

## 5. Additivity accounting

```text
Enum token additions:              1  (PENDING_FREEZE)
Enum token deletions:              0
Existing schema-field deletions:   0
Schema-row mutations outside historical_status: 0
Schema-column mutations:           0
Unaffected rows:                   15 / 16 (all rows except historical_status)
```

**Strict reconstruction check:** removing `PENDING_FREEZE` from the new allowed-values string and its accompanying parenthetical yields `FROZEN` — matches the baseline value exactly. Result: `PASS`.

## 6. Machine-readable validation

```text
Parser:                       csv.DictReader, quoting-aware
historical_status row resolution: PASS (resolved by column_name)
allowed_values exact tokens:  {FROZEN, PENDING_FREEZE}  -- PASS
Duplicate allowed token count: 0
Blank allowed token count:     0
Malformed row count:           0
Shifted-field row count:       0
Extra-column artifact count:   0
Forbidden wording scan (or equivalent / TBD / future token / appropriate value): 0 matches
```

## 7. Registry immutability

```text
MODEL_3B_V2_OD005_OPERATION_REGISTRY.csv hash before: 39eb7a7b5e76812d491048daa0218a38ceedd8039dfafa8abb02bfa9f9668897
MODEL_3B_V2_OD005_OPERATION_REGISTRY.csv hash after:  39eb7a7b5e76812d491048daa0218a38ceedd8039dfafa8abb02bfa9f9668897
Registry rows: 9 (OP-01..OP-09), unchanged
OP-10 registry row count: 0
OP-10 authoritative registry assignment count: 0
Existing rows changed to PENDING_FREEZE: 0
```

## 8. Successor / protected-artifact preservation

```text
Successor-specification change count: 0
Successor readiness status: READY_WITH_OPERATION_ID_PENDING (unchanged)
Successor actual file (reconciliation): ABSENT (unchanged)
id_assignment_status AUTHORITATIVELY_ASSIGNED applied: NO
Readiness tokens (OPERATION_ID_ASSIGNED_*) applied: NO
ART-016 / README changes: 0
Numerical/amendment/canonical-test inventory changes: 0
Ledger changes: 0
Validator / Python code changes: 0
E3: NOT AUTHORIZED
E4: NOT AUTHORIZED
Executed-test count: 0
```

## 9. Secret scan

```text
Scope: amended schema diff + this audit file
Result: CLEAN (one incidental match on the substring "token" inside the prose
"no intermediate token" — not a credential, dismissed as false positive)
```

## 10. Rollback readiness

```text
Recorded pre-amendment SHA-256: 4554e409dfc3e6b5ea53ddc6c358e770b66d2a38f68a8efda55b7b8a1c1cb7bd
Rollback method (if needed): git checkout a2d2e71ee682bf39ca5fd9257cad3bbdf7628d59 -- <schema path>; rm this audit file
Rollback exercised this turn: NO (all verifications passed)
```

## 11. Final working-tree status

```text
Modified (unstaged): WAVE_2_OD_005_OPERATION_REGISTRY_SCHEMA.csv
New (untracked):      WAVE_2_OD_005_REGISTRY_PENDING_ENUM_SCHEMA_AMENDMENT_AUDIT.md
Staged paths: 0
Committed: NO
Pushed: NO
Server-synced: NO
```

---

**Decision outcome:** `MODEL_3B_V2_OD_005_REGISTRY_PENDING_ENUM_SCHEMA_AMENDMENT_READY_FOR_REVIEW`

**Required semantic status:**

```text
Registry schema:            PENDING_FREEZE ENUM ADDED IN WORKING TREE
Canonical registry:         UNCHANGED, OP-01 THROUGH OP-09 ONLY
OP-10 registry row:         NOT YET ADDED
Successor specification:    NOT YET UPDATED
Successor reconciliation:   NOT CREATED
Operation execution:        NOT AUTHORIZED
E3:                         NOT AUTHORIZED
E4:                         NOT AUTHORIZED
Executed tests:             0
```
