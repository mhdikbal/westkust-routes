# SALIDO-HDT Solver v0.1.3 — Typed Schicht Domain Plan

Patch target: **Solver v0.1.3**. Baseline: commit `53f906f` ("docs:
audit F6 and F7 acceptance status"), on top of `ad8dc6b4` ("solver
v0.1.2"), `93b05a4`, and `1cb16df`. **None of `1cb16df`, `93b05a4`, or
`ad8dc6b4` are amended by this patch** — this is a new, separate commit.

Canonical research inputs remain read-only, unchanged by this patch:
`docs/enclave/salido_hdt_model_v0_3/`, `salido_hdt_model_v0_4/`,
`salido_hdt_model_v0_4_1/`.

This plan closes the two schicht-specific gaps identified as
`partially_complete` in `SOLVER_V0_1_2_F6_F7_ACCEPTANCE_AUDIT.md`
(checks 3 and 5): no controlled schicht domain exists, and no
evidence-gating mechanism exists for a labeled shift concept.

---

## Current behaviour

`s` (schicht) is a bare Python `int` everywhere in the codebase — the
CP-SAT decision variable key component, `SolverVariables.schicht_count`,
and the public `active_assignments[].schicht_id` field in
`scenario_NN.json` (added in commit `93b05a4`) are all raw integers.
`config.DEFAULT_SCHICHT_COUNT = 1` means the only value ever produced is
`0`. Nothing in the dataset (`docs/enclave/salido_hdt_model_v0_4_1/`)
carries a shift-identity column at all — verified in the acceptance
audit via header inspection of `07_human_role_location_time.csv` and
`08_weekly_operations.csv`. There is no enum, no controlled vocabulary,
and no mechanism to distinguish "internal bookkeeping index 0" from "the
historical claim that this was an unspecified/day/night shift" — the two
are currently the same undifferentiated integer.

## Intended behaviour

A new typed domain, `SchichtId`, with exactly the four controlled string
values specified:

```python
class SchichtId(enum.Enum):
    UNSPECIFIED = "SCHICHT-UNSPECIFIED"
    DAY = "SCHICHT-DAY"
    NIGHT = "SCHICHT-NIGHT"
    THREE_SHIFT_UNSPECIFIED = "SCHICHT-THREE-SHIFT-UNSPECIFIED"
```

The CP-SAT model keeps using integer schicht indices internally (`s` in
`x[h,j,l,s,t]`) — **no change to variable construction, no change to any
existing hard/soft constraint's grouping key**. A new resolution layer
maps each internal index to a `SchichtLabel` carrying the controlled
`schicht_id` plus its evidentiary basis, and every PUBLIC output field
that currently emits the raw int is changed to emit `schicht_id.value`
(a controlled string) instead. The raw internal index is not deleted from
output — it is kept as a clearly-separate `schicht_index` field
(mirroring how `time_bucket` is already an internal integer index
exposed as such) so the two claims stay visibly distinct: `schicht_index
= 0` is bookkeeping; `schicht_id = "SCHICHT-UNSPECIFIED"` is the
historical claim (or lack of one). They are never the same statement.

**Default mapping.** With no source evidence and no scenario assumption
for a given index, that index resolves to `SchichtId.UNSPECIFIED` --
`schicht_index = 0` maps to `schicht_id = "SCHICHT-UNSPECIFIED"` under
the current default configuration (`DEFAULT_SCHICHT_COUNT = 1`). This is
the only mapping the real dataset can ever produce today, since no CSV
column supplies schicht evidence.

**Evidence gating.** `SchichtId.DAY` / `SchichtId.NIGHT` /
`SchichtId.THREE_SHIFT_UNSPECIFIED` may only be resolved for an index
when the caller supplies one of:
1. `SchichtSourceEvidence` (an explicit source record: the asserted
   `SchichtId` plus `source_document_id`/`source_passage_id`) -- not
   reachable from the real dataset today (no such column exists), but the
   mechanism must exist and be tested against synthetic evidence, the
   same discipline already used for `hard_constraints.add_health_
   exclusion()` (a documented, tested, currently-dormant no-op).
2. `SchichtScenarioAssumption` (an explicit, caller-supplied modelling
   assumption, carrying its own `assumption_id`) -- reachable via a new
   `--schicht-assumption INDEX=SCHICHT_ID` CLI flag, or directly via
   `cli.run(schicht_scenario_assumptions=...)`.

Absent either, the index resolves to `UNSPECIFIED` with a `schicht_
warning` explaining why -- never a guess based on modern working-hours
conventions.

## Affected modules

- **`src/salido_hdt/solver/schicht.py`** (new). `SchichtId` enum,
  `SchichtLabel` / `SchichtSourceEvidence` / `SchichtScenarioAssumption`
  dataclasses, `resolve_schicht_labels(schicht_count, source_evidence=None,
  scenario_assumptions=None) -> dict[int, SchichtLabel]`.
- **`src/salido_hdt/solver/cli.py`**. `run()` gains two new optional
  parameters (`schicht_source_evidence`, `schicht_scenario_assumptions`,
  both `None` by default -- no behaviour change for existing callers).
  `active_assignments` entries gain `schicht_id` (replacing the raw int
  previously there) plus `schicht_evidence_status`, `schicht_source_
  document_id`, `schicht_source_passage_id`, `schicht_assumption_id`,
  `schicht_warning`; `schicht_index` (the old raw int) is kept as a
  separate, clearly-internal field. `validation_summary.json`'s
  `run_metadata` gains `schicht_labels` (the resolved label for every
  index in scope). `equipment_capacity.csv` gains a `schicht_id` column
  (each row already applies its capacity bound to every `(schicht, time)`
  pair uniformly per `ad8dc6b4`'s Item 1 fix; the new column makes
  explicit which schicht identifier that uniform bound is asserted for).
  `main()` gains an optional, repeatable `--schicht-assumption
  INDEX=SCHICHT_ID` CLI argument.
- **No change** to `variables.py`, `hard_constraints.py`,
  `soft_constraints.py`, `objective.py`, `scenario_collector.py` --
  schicht's role in CP-SAT variable construction and constraint grouping
  is entirely unaffected; this patch only changes what is DISCLOSED about
  an already-computed integer index, not how the model is built or solved.

## Mathematical formulation

No change. `x[h,j,l,s,t]` is unchanged; `s` remains an integer in
`range(schicht_count)` throughout the CP-SAT model. This patch is a pure
output-labelling layer applied after solving, exactly like
`_citations_for`/`_assignment_evidence` already do for HRLT presence
evidence.

## Output-schema changes

`scenario_NN.json.active_assignments[]` -- before:
```json
{"schicht_id": 0, ...}
```
after:
```json
{
  "schicht_index": 0,
  "schicht_id": "SCHICHT-UNSPECIFIED",
  "schicht_evidence_status": "unspecified",
  "schicht_source_document_id": "",
  "schicht_source_passage_id": "",
  "schicht_assumption_id": "",
  "schicht_warning": "no source evidence or scenario assumption for schicht index 0; defaulting to SCHICHT-UNSPECIFIED -- never inferred from modern working-hour conventions",
  ...
}
```

`validation_summary.json.run_metadata` gains:
```json
"schicht_labels": [
  {"schicht_index": 0, "schicht_id": "SCHICHT-UNSPECIFIED", "schicht_evidence_status": "unspecified", ...}
]
```

`equipment_capacity.csv` gains one column: `schicht_id` (controlled
string, e.g. `SCHICHT-UNSPECIFIED` on every real-dataset row today).

`entity_presence.csv` / `candidate_entities.csv` / `excluded_entities.csv`
-- **unchanged, explicitly out of scope**: these operate at HRLT-presence
or register-presence granularity, coarser than schicht, and never carried
a schicht field before this patch either. Adding one would require
inventing a schicht claim these reports do not make; not done.

## Regression tests

New file `tests/salido_hdt/solver/test_schicht.py`:
- `test_schicht_id_enum_has_exactly_the_four_controlled_values`.
- `test_default_resolution_with_no_evidence_is_unspecified` -- index 0,
  no evidence/assumption -> `SchichtId.UNSPECIFIED`, `evidence_status ==
  "unspecified"`, empty document/passage/assumption ids, non-empty
  warning.
- `test_scenario_assumption_resolves_to_asserted_schicht_id` -- index 0
  with a `SchichtScenarioAssumption(DAY, assumption_id=...)` ->
  `SchichtId.DAY`, `evidence_status == "scenario_assumption"`,
  `schicht_assumption_id` populated, warning states it is a modelling
  assumption, not an archival statement.
- `test_source_evidence_resolves_to_asserted_schicht_id` -- synthetic
  `SchichtSourceEvidence(NIGHT, doc, passage)` -> `SchichtId.NIGHT`,
  `evidence_status == "explicit_source"`, document/passage ids populated,
  `schicht_assumption_id` empty.
- `test_source_evidence_takes_precedence_over_scenario_assumption` --
  both supplied for the same index -> explicit source wins (real
  archival evidence outranks a caller's modelling assumption).
- `test_real_dataset_default_run_never_emits_raw_int_schicht_id` -- real
  `cli.run()`, no assumption/evidence supplied: every `active_
  assignments[].schicht_id` is the string `"SCHICHT-UNSPECIFIED"`, never
  the integer `0`; `schicht_index` (separately) is `0`.
- `test_real_dataset_run_with_cli_assumption_emits_asserted_schicht_id`
  -- force at least one real assignment to exist (reusing the established
  "pin P-HESSE" pattern from prior test files), pass a
  `schicht_scenario_assumptions={0: SchichtScenarioAssumption(DAY, ...)}`
  through `cli.run()`, assert the resulting assignment's `schicht_id ==
  "SCHICHT-DAY"` and carries a non-empty `schicht_warning` and populated
  `schicht_assumption_id`.
- `test_equipment_capacity_csv_has_schicht_id_column` -- real run,
  `equipment_capacity.csv` every row's `schicht_id ==
  "SCHICHT-UNSPECIFIED"`.
- `test_validation_summary_run_metadata_includes_schicht_labels`.
- `test_cli_schicht_assumption_flag_parses_index_and_schicht_id` -- unit
  test of the new argparse flag's parsing helper, isolated from a full
  subprocess invocation.

## Acceptance criteria

1. `SchichtId` has exactly the four specified members with the exact
   specified string values.
2. The raw integer `0` never appears as the value of any `schicht_id`
   field in `scenario_NN.json`, `validation_summary.json`, or
   `equipment_capacity.csv` produced by a real `cli.run()` -- verified by
   a live check against real output, not just unit-level.
3. `SchichtId.DAY`/`NIGHT`/`THREE_SHIFT_UNSPECIFIED` are reachable only
   via `SchichtSourceEvidence` or `SchichtScenarioAssumption` -- verified
   by a test asserting the default (no-evidence, no-assumption) path can
   only ever produce `UNSPECIFIED`.
4. All new and pre-existing tests pass (176 existing + new schicht tests).
5. A real `cli.run()` with no schicht arguments is byte-for-byte
   unaffected in every other field (F1-F10/Items 1-4 behaviour
   unchanged) -- only the schicht-related fields differ from `ad8dc6b4`'s
   output shape.
6. SHA-256 immutability of `salido_hdt_model_v0_3/`, `_v0_4/`, `_v0_4_1/`
   re-verified before and after implementation.

## Remaining limitations (explicitly out of scope)

- **No source column in the real dataset can ever populate
  `SchichtSourceEvidence`** -- this patch builds and tests the mechanism,
  but the real v0.4.1 dataset structurally cannot exercise the
  `explicit_source` evidence path (no schicht/shift column exists
  anywhere in `docs/enclave/salido_hdt_model_v0_4_1/`). This mirrors
  `add_health_exclusion()`'s existing "documented no-op" pattern -- ready
  machinery, dormant today, not a defect.
- **`equipment_capacity.csv`'s `schicht_id` column reports the schicht
  the uniform capacity bound is asserted for, not a per-schicht-
  partitioned capacity number** -- unchanged from `ad8dc6b4`'s Item 1
  policy (schicht-exclusive replication, not partition); this patch only
  labels that policy's scope explicitly, it does not change the
  underlying capacity arithmetic.
- **`entity_presence.csv`/`candidate_entities.csv`/`excluded_entities.csv`
  remain schicht-blind by design** -- adding a schicht dimension to
  HRLT/register-presence reporting is a larger, separate extension not
  undertaken here.
- **The `--schicht-assumption` CLI flag accepts one assumption per index
  per invocation** -- no batch-file or multi-scenario-comparison
  interface for exploring several competing schicht assumptions at once;
  a future extension, not built here.
