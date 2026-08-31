# WAVE 2 — OD-005 Operation-ID Allocation Rule (Specification)

Status: **SPECIFICATION-ONLY**. Specifies the rule; does not apply it. `OP-10` is not assigned by this document.

Authoritative baseline: `8f106c4626255cc0e2a857fd75700661db601379`.

---

## 1. Namespace owner

`OD-005`, within the `docs/thesis/pilot_annotation/model3b_v2/` (and cross-referenced `docs/thesis/colab/model3b_spec_validator/`) documentation set. Explicitly **not** shared with `docs/enclave/`'s unrelated `OP-0NN` (3-digit) historical-operations series (see `WAVE_2_OD_005_OPERATION_NAMESPACE_REVIEW.md` §3–4).

## 2. Numeric width and formatting

`OP-NN`, two digits, zero-padded to two digits for `01`–`99` (`OP-01` … `OP-99`), extending to three digits only if `OP-99` is ever exhausted (`OP-100`). No other separator, prefix, or suffix.

## 3. Monotonic allocation

New IDs are allocated as the next unused integer in strictly ascending order. No ID is ever assigned out of order, and none is ever skipped except via an explicit, documented reservation (§5).

## 4. Collision scan across repository

Before any new ID is allocated, a full-repository `grep` for the exact candidate string (e.g. `\bOP-10\b`) must return zero matches outside this registry's own future entry, **and** a review of any differently-formatted `OP-*`-shaped series (per §1's exclusion) must confirm no ambiguity. This is a repeatable, mechanical precondition, not a one-time check.

## 5. Reserved IDs

None exist today (0 `reserved_reason` entries across both source files). If a future turn needs to reserve an ID ahead of its definition (e.g. to lock in a number for a not-yet-designed operation), it must record `reserved_reason` explicitly in the registry rather than silently skip a number.

## 6. Abandoned candidate IDs

None exist today. If a candidate ID is ever proposed and then abandoned before being frozen, the registry must record it with `historical_status=ABANDONED_CANDIDATE` rather than making the number available for reuse by a different operation — abandoned numbers are retired, not recycled, to keep every ID a permanent, unambiguous pointer.

## 7. Retired operations

None exist today. A retired operation retains its row in the registry (never deleted) with `historical_status` updated to record retirement and a `notes` explanation; its `operation_id` is never reused (this mirrors the `OPT-005-B` retirement pattern already established in this OD-005 workstream — retired, not deleted).

## 8. Superseded operations

None exist today (`supersedes_operation_id=NONE` for all 9). A future supersession must set the superseding operation's `supersedes_operation_id` field to the older ID; the superseded row remains in the registry, unmodified, forever.

## 9. Prohibition on ID reuse

An `operation_id`, once frozen (`historical_status=FROZEN`), is permanently retired from reuse even if the operation it names is later retired or superseded. This matches property `NEVER REUSED` required of the `operation_id` column in `WAVE_2_OD_005_OPERATION_REGISTRY_SCHEMA.csv`.

## 10. Registry write and freeze precondition

A new ID may be written into the registry only after: (a) the §4 collision scan returns clean, (b) the operation's `owner_decision`, `operation_type`, `target_path`, and `predecessor_operation_id` are all specified (not blank, not guessed), and (c) the registry write is itself committed as its own frozen turn before the ID is treated as authoritative for any subsequent execution.

## 11. Allocation audit

Every allocation of a new ID must be accompanied by a mechanical audit re-stating: existing ID count before, existing ID count after (+1), collision count (0 required), and the exact commit hash under which the new row was frozen — following the same audit pattern already used for `OP-09`'s own creation (`WAVE_2_OD_005_OP09_CANONICAL_TEST_INVENTORY_CREATION_AUDIT.md`).

## 12. Next-ID derivation formula

```math
k_{next} = 1 + \max\{k : \mathrm{OP}\text{-}k \in \mathcal O_{confirmed}\}
```

**This formula is valid only when all of the following hold simultaneously** (per this turn's own instruction, and per the namespace review's finding):

- single `OD-005` namespace proven — **partially proven**: OD-005-internal uniqueness is clean, but repository-wide exclusivity of the `OP-*` prefix is not yet formally documented (see `WAVE_2_OD_005_OPERATION_NAMESPACE_REVIEW.md`);
- `OP-01`–`OP-09` unique — **proven** (9/9 unique, 0 collisions);
- no other `OP-*` namespace exists — **not proven** (the `docs/enclave/` `OP-0NN` series exists, though non-colliding by format);
- no reserved or hidden ID — **proven** (0 found);
- source-schema differences do not mark a subnamespace — **proven** (`OP-09`'s differing 15-column schema is a versioning artifact, not a competing namespace, per its own explicit `predecessor_operation_id=OP-08`);
- no conflicting registry rule exists — **proven** (no registry rule existed at all before this specification).

**Because one of the six conditions is not yet fully proven, this formula cannot yet be applied to assign `OP-10` as an authoritative ID.** It can, however, be recorded now as the formula this registry will apply once (a) the registry is frozen with the disambiguation note from `WAVE_2_OD_005_OPERATION_NAMESPACE_REVIEW.md` §4, and (b) the repository-wide collision scan in §4 above is re-run clean at that time.
