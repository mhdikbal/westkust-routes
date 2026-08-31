# WAVE 2 — OD-005 OP-10 Assignment Enum Contract Review

Status: **REVIEW-AND-SPECIFICATION ONLY**. Establishes exact fixed enum tokens closing the gap found in the prior turn's stop condition (`MODEL_3B_V2_OD_005_OP10_ASSIGNMENT_ENUM_REQUIRES_REVIEW`). Does not add `OP-10` to the registry, does not amend the registry schema, and does not edit any successor-specification artifact.

Authoritative baseline: `e165e6fefae1316794a238589703220a5e1dafca`.

---

## 1. Three status dimensions (kept strictly separate)

```text
A. Identifier assignment state   -- has OP-10 been decided/applied as an ID?
B. Artifact freeze/provenance    -- has the artifact record been committed/synced?
C. Operation execution state     -- has the operation actually run?
```

`historical_status` (registry) belongs to dimension B only. `id_assignment_status` (successor operation draft) belongs to dimension A only. Successor-specification "readiness" is a distinct fourth axis — artifact-set freeze/provenance for the six specification files themselves, tracked separately from the registry's own dimension B. None of the four selected tokens below implies execution or successor creation.

## 2. Registry `historical_status` — pending token selection

Candidates evaluated against 9 criteria (semantic precision, separation from execution, compatibility with existing `FROZEN`, lifecycle clarity, machine readability, transition determinism, rollback clarity, risk of implying commit/sync, risk of implying execution):

| Candidate | Assessment |
|---|---|
| `PENDING_FREEZE` | High precision; parallels `FROZEN` directly (`PENDING_FREEZE → FROZEN`); no execution/commit/sync implication; clean rollback (delete row, no state to unwind) |
| `ASSIGNED_PENDING_FREEZE` | Conflates dimension A (assignment) into a dimension-B field, violating the separation principle in §5 of the governing instructions; rejected on those grounds alone |
| `CURRENT_UNFROZEN` | "Current" is ambiguous (current relative to what reference point?); lower semantic precision |
| `NOT_YET_FROZEN` | Acceptable but stylistically inconsistent with the existing affirmative-adjective convention (`FROZEN`, not `NOT_UNFROZEN`); no advantage over `PENDING_FREEZE` |

**Selected: `PENDING_FREEZE`.** Means exactly: *the record has assignment authority and may be applied to the working tree, but is not yet committed, pushed, or server-synced.* Does not mean executed, frozen, synced, or successor-created.

## 3. Registry lifecycle model

**Model A selected**: `PENDING_FREEZE → FROZEN` (transitioning directly upon push/server sync, with no intermediate registry-level token).

Justification: inspecting all 9 existing rows' `historical_status` values, `FROZEN` has only ever been recorded once each operation's *underlying source specification file* (not the registry row itself) was committed — e.g. `OP-09`'s `historical_status=FROZEN` reflects `WAVE_2_OD_005_NEW_E2_OPERATION_SPECIFICATION.csv` being committed, independent of when the registry document that cites it was itself committed. No existing row has ever needed or used an intermediate "committed locally, not yet synced" registry-level state — every prior local-commit-then-push pair for this session's operation-specification files happened within the same reviewed batch, leaving no precedent for a `FROZEN_LOCALLY` registry value. Model B (`PENDING_FREEZE → FROZEN_LOCALLY → FROZEN`) would introduce a second new enum value with zero supporting precedent and would duplicate work already covered by the *successor-specification* readiness lifecycle (§4 below), which does need a local-commit stage because it tracks the specification-artifact files' own git state directly, not an operation's provenance record. Model A avoids that duplication.

## 4. Registry schema amendment requirement

**`ADD_PENDING_ENUM_TO_REGISTRY_SCHEMA`.** Only `PENDING_FREEZE` needs to be added to `WAVE_2_OD_005_OPERATION_REGISTRY_SCHEMA.csv`'s `historical_status` `allowed_values` (currently `FROZEN (only value expected for OP-01..09)`); `NO_SCHEMA_CHANGE_REQUIRED_WITH_JUSTIFICATION` is correctly disallowed here, since `OP-10` genuinely requires a non-`FROZEN` value at working-tree-application stage.

**Timing:** the schema amendment must occur in its own explicit, separately-authorized write (it modifies a frozen schema catalog file, which this review does not touch), and it must precede `OP-10`'s actual registry-row application — a row citing an enum value the schema doesn't yet permit would itself be a schema violation. It may be bundled into the same future commit that freezes these enum-contract artifacts (both are specification-tier writes with no execution implication), or done as a fully separate turn; either is acceptable, but it cannot happen simultaneously with or after the `OP-10` row write.

## 5. Successor `id_assignment_status` — post-application token selection

Inventory of values/candidates found across successor-specification and allocation-review artifacts, classified:

| Value found | Classification |
|---|---|
| `READY_WITH_OPERATION_ID_PENDING` | `ARTIFACT_READINESS_STATUS` (describes the six-file set's overall readiness, not this field) |
| `AWAITING_REGISTRY_FREEZE` | `ASSIGNMENT_APPLICATION_STATUS` (current, pre-application value of `id_assignment_status` itself) |
| `ASSIGNED` | `ASSIGNMENT_APPLICATION_STATUS` (candidate, from the frozen application plan's prose) |
| `AUTHORITATIVELY_ASSIGNED` | `ASSIGNMENT_APPLICATION_STATUS` (candidate; originally proposed for a nonexistent `assignment_status` field in an earlier, non-authoritative turn) |
| `APPROVED_FOR_APPLICATION` | `ASSIGNMENT_DECISION_STATUS` (describes the allocation *review's own decision*, a different artifact and a different moment, not this field) |

**Selected: `AUTHORITATIVELY_ASSIGNED`** — explicitly re-scoped to the real field name `id_assignment_status` (the earlier turn's error was inventing a field called `assignment_status`; the value itself remains sound once attached to the correct field). Chosen over the bare `ASSIGNED` because it unambiguously distinguishes a formally reviewed, provenance-backed assignment (per `WAVE_2_OD_005_AUTHORITATIVE_NEXT_ID_ALLOCATION_REVIEW.md`'s 12/12-precondition approval) from any of the 114 repository-wide nonauthoritative/candidate mentions of `OP-10` already on record — a distinction this whole workstream has repeatedly needed to make explicit. Means: *`OP-10` has been applied consistently to the registry and all authorized successor-specification targets, but has not been executed and the successor reconciliation has not been created.*

## 6. Successor-specification readiness — full four-stage lifecycle

| Stage | Token | Notes |
|---|---|---|
| Pre-application (current) | `READY_WITH_OPERATION_ID_PENDING` | Fixed, pre-existing, unchanged by this review |
| Post-application, working tree | `OPERATION_ID_ASSIGNED_PENDING_FREEZE` | Selected (§7 below) |
| Post-local-commit | `OPERATION_ID_ASSIGNED_FROZEN_LOCALLY` | Selected |
| Post-push/server-sync | `OPERATION_ID_ASSIGNED_FROZEN` | Selected |

All four tokens are distinct — none is reused across more than one stage, so no ambiguity-justification is required. Note this is a *different* lifecycle axis from the registry's `historical_status` (§2–3): the six successor-specification files are their own untracked artifact set with a real three-stage git history ahead of them (working tree → local commit → push/sync), unlike the registry's `historical_status`, which tracks an *operation's* underlying source-specification provenance rather than a document's own commit state. The two lifecycles are allowed to move independently.

## 7. Successor-specification readiness — post-application token detail

Candidates evaluated: `READY_FOR_ASSIGNMENT_FREEZE`, `OPERATION_ID_ASSIGNED_PENDING_FREEZE`, `READY_FOR_LOCAL_FREEZE`.

**Selected: `OPERATION_ID_ASSIGNED_PENDING_FREEZE`.** Most self-descriptive of the three (states both that the ID has been assigned and that freeze is pending, without a reader needing to infer either fact from context); already appears verbatim in this session's own prior semantic-status block (the `OP-10` assignment-application turn's required status list), so it introduces no net-new vocabulary; parallels the registry's `PENDING_FREEZE` naming without colliding with it (the two fields are visibly different strings, preventing cross-artifact confusion). Means: *all assignment-specific fields are internally consistent and ready to audit/freeze, but nothing has been committed, pushed, or synced.* Does not mean the successor reconciliation is ready for execution, `OP-10` is authorized for execution, or any artifact is already frozen.

## 8. Cross-field invariant (verified consistent)

```text
operation_id = OP-10
id_assignment_status = AUTHORITATIVELY_ASSIGNED
readiness = OPERATION_ID_ASSIGNED_PENDING_FREEZE
registry historical_status = PENDING_FREEZE
execution_status = SPECIFIED_NOT_AUTHORIZED
successor_actual_file = ABSENT
```

```math
\operatorname{Assigned}(OP\text{-}10)=1, \quad \operatorname{Executed}(OP\text{-}10)=0, \quad \operatorname{SuccessorExists}=0, \quad \operatorname{Frozen}(OP\text{-}10)=0.
```

All four selected tokens are mutually consistent with this invariant at the working-tree-application stage; none contradicts another.

## 9. Application surface (full detail in `WAVE_2_OD_005_OP10_ENUM_APPLICATION_SURFACE.csv`)

10 targets assessed. 5 `MUST_UPDATE` (registry schema catalog; canonical registry; successor operation draft; successor specification `.md`; the operation-ID-provenance-review and rollback-plan and spec-audit files — see the CSV for the exact per-file breakdown), 2 `NO_UPDATE_REQUIRED` (successor schema/source-map CSVs, which carry 0 `OP-10` mentions and no assignment/readiness field), 1 `NEW_AUDIT_ARTIFACT` (a future `OP-10` application audit). None modified by this review.

## 10. Decision

**`OP10_ASSIGNMENT_ENUM_CONTRACT_READY_FOR_SCHEMA_APPLICATION`.**

All required tokens are exact fixed strings with no "or equivalent" language; the registry-lifecycle model is explicitly selected (Model A); the schema-amendment requirement and its sequencing are stated. See `WAVE_2_OD_005_OP10_ENUM_CONTRACT_DECISION_DRAFT.md` for the formal decision record.
