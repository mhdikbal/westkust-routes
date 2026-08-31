# WAVE 2 — OD-005 Operation Namespace Review

Status: **REVIEW-ONLY**. Determines the scope of the `OP-*` namespace used by OD-005 operations. Changes no existing file.

Authoritative baseline: `8f106c4626255cc0e2a857fd75700661db601379`.

---

## 1. Existing operation inventory

9 operation records found, across two source files:

```text
WAVE_2_OD_005_EXACT_AMENDMENT_OPERATIONS.csv (17 columns): OP-01, OP-02, OP-03, OP-04, OP-05, OP-06, OP-07, OP-08
WAVE_2_OD_005_NEW_E2_OPERATION_SPECIFICATION.csv (15 columns): OP-09
```

Record count = 9. Unique ID count = 9. Collision count = 0. Missing-numeric-sequence count = 0 (`01`–`09` contiguous, no gap). Full per-operation detail in `WAVE_2_OD_005_OPERATION_SOURCE_MAP.csv`.

## 2. Condition-by-condition namespace check

Per this turn's own rule — namespace may be called linear only if **every** condition holds:

| Condition | Result |
|---|---|
| All 9 IDs owned by OD-005 | PASS — every source row's context is OD-005-scoped |
| No other `OP-xx` in the repository with a different owner | **FAIL** — see §3 |
| No reserved ID | PASS — 0 `reserved_reason` entries found in either source file |
| No deprecated-but-hidden ID | PASS — 0 deprecation markers found |
| No duplicate ID on another schema | PASS — the two source schemas' `operation_id` sets are disjoint by construction (OP-01..08 vs. OP-09 only) and jointly unique |
| `OP-09` continues `OP-01`–`08` intentionally and documented | PASS — `WAVE_2_OD_005_NEW_E2_OPERATION_SPECIFICATION.csv` row 1 explicitly sets `predecessor_operation_id=OP-08` |
| Source-schema differences do not form a separate namespace | PASS-WITH-NOTE — `OP-09`'s source file uses a 15-column schema, distinct from `OP-01`–`08`'s 17-column schema, but this is a **schema-version** difference (both files exist to define the same `OP-*` ID series, `OP-09` explicitly declares its predecessor as `OP-08`), not evidence of two competing numbering authorities |

## 3. Other `OP-xx`-shaped namespace found (repository-wide scan)

A repository-wide `grep` (not limited to `docs/thesis/pilot_annotation/`) found a second, unrelated series: **`OP-001` through `OP-042`** (3-digit, zero-padded) in `docs/enclave/salido_hdt_model_v0_3/08_weekly_operations.csv` and its sibling versioned copies (`v0_4`, `v0_4_1`, `salido_hdt_csv_v0_2`). Inspection confirms these are **weekly historical-ore-shipment operation records** for the 17th-century Salido mining economy (e.g. `OP-001,1682-01-04,1682-01-10,L-ZZW-DAGGANG,...`) — an entirely different research workstream (`docs/enclave/`, the Salido historical-mining-economy dataset), unrelated to Model 3B, OD-005, or any statistical-validation decision.

This series does not lexically collide with OD-005's `OP-01`–`OP-09` (3-digit zero-padded vs. 2-digit, e.g. `OP-001` ≠ `OP-01`), and a human or script that is aware of both formats would not confuse them. However, it **does** falsify the strict repository-wide condition "no other `OP-xx` in the repository with a different owner" as literally stated. The two series have never been documented as formally disjoint namespaces (no cross-reference, no shared registry, no stated digit-width convention distinguishing them).

## 4. Outcome

**`PROJECT_WIDE_NAMESPACE_REQUIRES_REVIEW`.**

Within OD-005's own scope, the 9 existing IDs are a clean, contiguous, collision-free, non-reserved, non-deprecated linear sequence (all conditions in §2 pass except the one in §3). But because a formally identical-looking prefix (`OP-`) is independently used elsewhere in the repository for a wholly unrelated purpose, this review cannot certify that `OP-*` is *globally* reserved for OD-005 without an explicit disambiguation statement. This is not a collision risk today (different digit-padding, different domain, different directory) — it is a documentation gap that a future registry should close explicitly, rather than silently assume away.

**Recommended registry-freeze content to resolve this**: the future unified `MODEL_3B_V2_OD005_OPERATION_REGISTRY.csv` (see `WAVE_2_OD_005_OPERATION_REGISTRY_SCHEMA.csv`) should state, in its own header comment or an accompanying specification note, that its `operation_id` namespace is `OP-NN` (2-digit, unpadded beyond two digits, OD-005-scoped) and is explicitly distinct from `docs/enclave/`'s unrelated `OP-0NN` (3-digit) historical-operations series. This one sentence, once frozen, closes the gap found in §3.
