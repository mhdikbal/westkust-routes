# SALIDO-HDT Solver v0.1.4 — Three-Schichten Source-Count Metadata

Patch target: **Solver v0.1.4**. Baseline: commit `d4ddd07` ("typed
schicht domain with evidence-gated public identifiers"), on top of
`53f906f`, `ad8dc6b4`, `93b05a4`, `1cb16df`. **None of the five prior
commits are amended.** Canonical inputs remain read-only:
`docs/enclave/salido_hdt_model_v0_3/`, `_v0_4/`, `_v0_4_1/`.

## Problem

A source statement may say an operation ran in three schichten for a
specific event without identifying who was on which shift. The correct
model is a fact about the ARCHIVE (`source_schicht_count = 3`,
`schicht_id = SCHICHT-THREE-SHIFT-UNSPECIFIED`,
`individual_shift_assignment_known = false`), never a fact that changes
how many CP-SAT variables, entities, or aggregate-group headcounts exist.
The v0.1.3 domain (`schicht.py`) already defines `SchichtId.THREE_SHIFT_
UNSPECIFIED` but has no way to carry the archivally-stated count
(`source_schicht_count`) or the "do we know individual allocation"
distinction (`individual_shift_assignment_known`) -- and nothing enforces
that this count can never multiply x-variables, personnel, or group
headcounts. Forbidden: inventing `SCHICHT-1`/`SCHICHT-2`/`SCHICHT-3`
per-shift identities, and inferring DAY/NIGHT or a specific shift
assignment from a bare "three shifts" statement.

## Intended behaviour

1. `SchichtSourceEvidence` and `SchichtLabel` gain two new fields:
   `source_schicht_count: int | None` and `individual_shift_assignment_
   known: bool = False`. Both are pure metadata carried alongside the
   existing evidence-gating fields -- neither ever reaches
   `variables.build_variables()`'s `schicht_count` parameter (which stays
   sourced only from `config.DEFAULT_SCHICHT_COUNT`, unchanged). This
   decoupling already exists structurally (`resolve_schicht_labels()` is
   called AFTER `build_variables()`, never before); this patch adds an
   explicit static-analysis test proving `variables.py` never references
   `source_schicht_count`, the same discipline already used for
   `HumanGroup.count`.
2. Internal index naming is corrected to `schicht_index_internal`
   (renamed from v0.1.3's `schicht_index`) and is now **diagnostic-only**:
   it appears in `validation_summary.json`'s `run_metadata.schicht_labels`
   but is removed from every end-user-facing output (`scenario_NN.json`
   active_assignments, `equipment_capacity.csv`). Two dict builders are
   added: `schicht_label_to_dict()` (full, diagnostic, includes
   `schicht_index_internal`) and `schicht_label_to_public_dict()`
   (excludes it) -- callers writing end-user artifacts use the public
   variant.
3. `equipment_capacity.csv` gains `source_schicht_count` and
   `schicht_evidence_status` columns alongside the existing `schicht_id`
   (no `schicht_index_internal` column, per item 2).

## Affected modules

`src/salido_hdt/solver/schicht.py` (new fields, new
`schicht_label_to_public_dict()`, field rename), `src/salido_hdt/solver/
cli.py` (active_assignments uses the public dict variant;
`run_metadata.schicht_labels` keeps the full diagnostic variant),
`src/salido_hdt/solver/equipment_capacity.py` (CSV column changes). No
change to `variables.py`, `hard_constraints.py`, `soft_constraints.py`,
`objective.py`, `scenario_collector.py` -- this is metadata-only, same
discipline as v0.1.3.

## Mathematical formulation

None. No CP-SAT variable, constraint, or objective term changes.

## Output-schema changes

`scenario_NN.json.active_assignments[]`: `schicht_index_internal` field
removed (was added in v0.1.3); `schicht_id` unchanged; new fields
possible when three-shift evidence is supplied:
`source_schicht_count`, `individual_shift_assignment_known`.

`validation_summary.json.run_metadata.schicht_labels[]`: unchanged shape
plus the two new metadata fields; `schicht_index_internal` retained here
(this IS the diagnostic output).

`equipment_capacity.csv`: columns become `task_id, location_id,
schicht_id, source_schicht_count, schicht_evidence_status,
confirmed_capacity, uncertain_capacity, required_capacity,
capacity_status, source_inventory_item_ids, required_capacity_semantics,
hard_bound_rationale` -- no `schicht_index_internal` column.

## Regression tests

New tests in `tests/salido_hdt/solver/test_schicht.py`:
- `test_three_shift_evidence_carries_source_count_and_unknown_allocation`.
- `test_three_shift_evidence_does_not_multiply_x_variables` -- real
  dataset, compare `len(sv.x)` before/after resolving three-shift
  evidence (evidence never touches variable construction, so this must
  be a structural/architectural proof, not just "it happens to be equal
  today").
- `test_three_shift_evidence_does_not_multiply_aggregate_group_variables`
  -- same, scoped to an aggregate group's own variable count.
- `test_variables_module_never_references_source_schicht_count` (static
  grep guard, mirrors the existing `HumanGroup.count` guard).
- `test_schicht_index_internal_absent_from_end_user_outputs` -- real
  `cli.run()`, assert no key `schicht_index_internal` anywhere in
  `scenario_NN.json` or `equipment_capacity.csv`, but present in
  `validation_summary.json.run_metadata.schicht_labels`.
- `test_no_scicht_1_2_3_identities_exist` -- static guard: `SchichtId`
  has exactly 4 members, none named/valued `SCHICHT-1`/`SCHICHT-2`/
  `SCHICHT-3`.
- `test_equipment_capacity_csv_has_source_schicht_count_and_evidence_status_columns`.

## Acceptance criteria (verbatim from the request)

1. Numeric public schicht values: 0.
2. Default public value: `SCHICHT-UNSPECIFIED`.
3. Unsupported `SCHICHT-DAY` occurrences (no evidence/assumption): 0.
4. Unsupported `SCHICHT-NIGHT` occurrences (no evidence/assumption): 0.
5. Three-shift personnel multiplication: 0.
6. Three-shift aggregate-group multiplication: 0.
7. Equipment capacity remains grouped by `(schicht, time)` (unchanged
   from `ad8dc6b4`; re-verified, not re-implemented).
8. Existing tests remain green (189 baseline + new).
9. Canonical datasets remain unchanged (SHA-256 / `git status`
   re-verified before and after).

## Remaining limitations

- No CLI flag is added for supplying `SchichtSourceEvidence` (a
  three-shift or DAY/NIGHT source claim) -- the real dataset has no
  column that could supply one, so this remains a Python-API-level
  mechanism only (`cli.run(schicht_source_evidence=...)`), consistent
  with v0.1.3's existing scope decision for the `explicit_source` path.
- `individual_shift_assignment_known` is a boolean flag only; it does not
  yet drive any downstream solver behaviour (e.g. no partial-allocation
  constraint exists that activates when this becomes `True`) -- that
  would be a substantially larger extension (per-shift personnel
  attribution) not undertaken here.
