# SALIDO-HDT Solver — F6 / F7 Acceptance Audit

Read-only audit. No code or data was changed to produce this report.
Baseline: commit `ad8dc6b4` ("solver v0.1.2"), itself built on `93b05a4`
and `1cb16df`. **None of the three commits are modified or amended by
this audit.** All findings below are reproduced directly against the real
`docs/enclave/salido_hdt_model_v0_4_1/` dataset via `git grep`/`grep`
against the committed source, direct Python inspection of the loaded
domain objects, the existing test suite (176 tests, all passing at
`ad8dc6b4`), and fresh `python -m salido_hdt.solver.cli` runs whose output
was inspected and then discarded (nothing written under the canonical
dataset tree).

---

## F6 — schicht semantics

### 1. Every distinct schicht value appearing in each layer

| Layer | Distinct schicht values found | Evidence |
|---|---|---|
| Solver domain objects (`SolverVariables.x` keys, index `[3]`) | `{0}` | `build_variables(load_dataset(...))` against the real dataset: `sorted(set(k[3] for k in sv.x)) == [0]`; `sv.schicht_count == 1` |
| Active assignments (`scenario_NN.json` → `active_assignments[].schicht_id`) | `{0}` | Fresh `cli.run(..., max_scenarios=3)`: every `schicht_id` across all returned scenarios' `active_assignments` is `0` |
| Scenario JSON (top-level / `penalty_breakdown` / any other field) | N/A — schicht does not appear anywhere in scenario JSON except inside each `active_assignments` entry's `schicht_id` | Direct inspection of a real `scenario_NN.json`'s key set |
| `validation_summary.json` | `run_metadata.schicht_count = 1` (a count, not a value); no other top-level or nested key contains "schicht" | `[k for k in summary if 'schicht' in k.lower()]` on a real run → `[]` (only the nested `run_metadata.schicht_count` field, found by direct key lookup, not the top-level scan) |
| `equipment_capacity.csv` | none — the CSV has no schicht column at all | Real header: `task_id,location_id,confirmed_capacity,uncertain_capacity,required_capacity,capacity_status,source_inventory_item_ids,required_capacity_semantics,hard_bound_rationale` |
| `entity_presence.csv` / `candidate_entities.csv` / `excluded_entities.csv` | none — no schicht column in any of the three candidate-universe CSVs | Real headers inspected directly; schicht is not a concept these reports operate at (HRLT presence windows and register presence are both coarser than schicht) |

**Finding:** the only place a schicht value is ever materialized in
output is `scenario_NN.json`'s per-assignment `schicht_id` field, and it
is always `0` in the current dataset. `equipment_capacity.csv` reports
capacity per `(task_id, location_id)` only — it does not expose the
per-`(schicht, time)` constraint structure that the underlying CP-SAT
model actually enforces (see item 7).

### 2. Does numeric schicht `0` appear anywhere in public output?

**Yes**, whenever `active_assignments` is non-empty:
`scenario_NN.json → active_assignments[].schicht_id == 0`. It is the
*only* schicht value that can ever appear, since
`config.DEFAULT_SCHICHT_COUNT = 1` bounds `range(schicht_count)` to
`{0}` everywhere `s` is generated (`variables.py`'s `for s in
range(schicht_count)`). If a given run's optimal/near-optimal scenarios
are all fully idle (no active assignments — the common case on the real
dataset today, see `SOLVER_SCENARIO_INTERPRETATION_AUDIT.md`), `0` does
not literally appear in any `active_assignments` entry that run, but
`run_metadata.schicht_count = 1` still discloses that schicht `0` is the
sole value in scope.

### 3. Does a controlled schicht domain exist?

**No.** `git grep -niE "SCHICHT-"` across `src/salido_hdt/solver/`,
`docs/enclave/salido_hdt_model_v0_4_1/*.csv`, and
`docs/enclave/salido_hdt_model_v0_4_1/docs/*.md` returns zero matches.
None of `SCHICHT-UNSPECIFIED`, `SCHICHT-DAY`, `SCHICHT-NIGHT`, or
`SCHICHT-THREE-SHIFT-UNSPECIFIED` exist anywhere in the codebase, the
canonical dataset, or its documentation. Schicht is represented purely as
a bare Python `int` (`s` in the `x[h,j,l,s,t]` tuple key), with no
symbolic/enum layer at all — contrast with, e.g.,
`domain.EntityType`/`domain.ProvenanceLevel`/
`constraint_strength.AxisValue`, which *are* controlled enums for their
respective concepts.

### 4. The actual default schicht value

`config.DEFAULT_SCHICHT_COUNT = 1` (`src/salido_hdt/solver/config.py`).
Because `variables.build_variables()` always iterates
`range(schicht_count)`, the one and only schicht value ever produced by
the default configuration is the integer `0`. There is no separate
"default schicht value" constant distinct from this — the count and the
resulting value space collapse to the same fact at `count = 1`.

### 5. Can DAY / NIGHT appear without source evidence or an explicit scenario assumption?

**Vacuously yes (they cannot appear at all, under any condition,
including with evidence).** Per item 3, no `DAY`/`NIGHT` concept exists
anywhere in the domain model. Confirmed the requirement is trivially
satisfied today (there is no code path capable of producing anything
other than integer schicht indices `0..DEFAULT_SCHICHT_COUNT-1`), but
this is a *structural absence*, not an enforced *guardrail*: no
evidence-gating mechanism exists because there is nothing yet to gate. If
a `DAY`/`NIGHT` (or any labeled-shift) concept is added in the future,
this audit found no existing validation hook, enum, or test that would
automatically require source evidence or an explicit scenario assumption
before such a value could enter the model — that enforcement would need
to be built at the same time as the concept itself. Flagged as a gap for
future work in the verdict below, not a defect in the current code (which
correctly invents nothing).

### 6. Does a source statement recording three schichten avoid fictional multiplication?

**Confirmed, by construction, via existing passing tests — not merely by
absence of a feature.**

- `data_loader.py` parses no shift-count field from any CSV — no column
  in any of the 17 real dataset files encodes a per-record schicht count
  (`grep` of `07_human_role_location_time.csv`'s and
  `08_weekly_operations.csv`'s headers confirms neither carries a schicht
  or shift-count column). `config.DEFAULT_SCHICHT_COUNT` is a hardcoded
  Python constant, entirely independent of any archival source statement,
  so no source text about "three schichten" is ever parsed into the
  model in the first place.
- `variables.build_variables()`'s x-variable construction loop
  (`for h in entities: ... for s in range(schicht_count): ...`) applies
  the *same* `schicht_count` to every entity uniformly — an aggregate
  group receives exactly as many `(j, l, s, t)` slots as an individual
  with the same presence window, never multiplied by `HumanGroup.count`.
  This is directly asserted by the existing, passing test
  `test_aggregate_group_gets_exactly_one_boolvar_per_j_l_s_t_not_scaled_
  by_count` (`tests/salido_hdt/solver/test_aggregate_group_integrity.py`),
  re-run for this audit: **PASSED**.
- `test_no_solver_module_references_human_group_count` and
  `test_variables_module_does_not_reference_human_group_count`
  (same file) statically grep `hard_constraints.py`, `soft_constraints.py`,
  `objective.py`, and `variables.py` for any reference to
  `HumanGroup.count`, asserting none exists — re-run for this audit:
  **PASSED** (both).
- Consequently, were `schicht_count` ever raised (e.g. to model a
  documented three-shift pattern), the multiplication would apply
  uniformly to the count of `(task, location, time)` slots per entity,
  never to the count of entities or to a group's headcount — no
  fictional personnel and no group multiplication is structurally
  possible via this code path.

### 7. Is equipment capacity constrained independently per (task, location, schicht, time)?

**Yes, at the constraint level — fixed in this same v0.1.2 patch
(`ad8dc6b4`, Item 1).** `hard_constraints.add_equipment_capacity()`
groups candidate variables by `(s, t)` (not by `t` alone, which was the
pre-`ad8dc6b4` defect):

```python
by_schicht_time: dict[tuple[int, int], list[cp_model.IntVar]] = defaultdict(list)
for (h, j, l, s, t), var in x_vars.items():
    if j == task_id and l == location_id:
        by_schicht_time[(s, t)].append(var)
for (s, t), vs in by_schicht_time.items():
    model.Add(sum(vs) <= capacity)
```

This produces one independent `sum(...) <= capacity` constraint per
distinct `(s, t)` pair for a given `(task_id, location_id)`. Verified via
the existing passing test
`test_equipment_capacity_is_per_schicht_not_pooled_across_schicht`
(`tests/salido_hdt/solver/test_equipment_capacity.py`), re-run for this
audit: **PASSED** (two schicht values at the same task/location/time each
get their own capacity=1 pool, 2 simultaneously active total — the
pre-fix code would have pooled both into a single `sum <= 1`).

**Caveat, precisely stated:** "independently constrained" means each
`(s, t)` pair gets its *own* constraint instance using the *same* numeric
`capacity` value — the bound is **replicated** across schicht, not
**partitioned** across schicht (there is no archival data giving a
per-schicht sub-quantity to partition by). This is the conservative,
schicht-exclusive reading `SOLVER_V0_1_2_FIX_PLAN.md`'s Item 1 explicitly
adopted and documented as a policy choice, not an archival fact — dormant
today since `schicht_count = 1` (only one `(s,t)` pair per `t` exists, so
replication vs. partition is unobservable in current output). Separately,
`equipment_capacity.csv`'s *report* (as opposed to the *constraint*) does
not break `confirmed_capacity`/`uncertain_capacity` out per schicht — it
reports one number per `(task_id, location_id)`, applied uniformly. This
is consistent (the report and the constraint use the same non-partitioned
number) but means a future reader cannot see per-schicht capacity
detail in the CSV even after `schicht_count` is raised, only in the
constraint structure itself.

### 8. F6 status: **partially_complete**

**What is fully resolved:**
- The schicht-blind equipment-capacity bug (checks 1, 7) is fixed and
  tested.
- No fictional personnel/group multiplication risk exists structurally
  (check 6), verified by existing passing tests.
- The current default behavior (checks 2, 4) is correct, consistent, and
  matches its own documentation everywhere it was checked.

**What remains incomplete:**
- **No controlled schicht domain exists** (check 3) — schicht is a bare
  `int`, not a validated enum. `SCHICHT-UNSPECIFIED` /
  `SCHICHT-DAY` / `SCHICHT-NIGHT` /
  `SCHICHT-THREE-SHIFT-UNSPECIFIED` do not exist as literals, types, or
  even documented conventions anywhere in this codebase.
- **No evidence-gating mechanism exists** for a labeled shift concept
  (check 5) — the requirement is met only because the concept it would
  govern has not been built yet, not because a guardrail was built and
  verified.
- **`equipment_capacity.csv` does not expose per-schicht granularity**
  even though the underlying constraint now respects the axis (check 7's
  caveat).

None of these three gaps affects correctness of the current, real
`schicht_count = 1` deployment — they are readiness gaps for a future
multi-schicht extension, not defects in what ships today.

---

## F7 — objective and penalty accounting

The request did not enumerate specific F7 checks (only F6's 8 items were
listed). The checks below are constructed by this audit, directly from
`SOLVER_V0_1_2_FIX_PLAN.md`'s own Item 2 acceptance criterion and
`docs/enclave/salido_hdt_model_v0_4_1/docs/CONSTRAINT_SOLVER.md`'s
six-category objective specification, so F7 is evaluated against a
concrete standard rather than left unaudited.

### F7.1 — Every objective category present in output

Real `scenario_NN.json.penalty_breakdown` (fresh run, this audit):

```json
{
  "archival_contradictions": 0, "unsupported_assignments": 0,
  "temporal_violations": 0, "topological_violations": 0,
  "role_location_penalties": 0, "over_assignment": 0,
  "task_switch": 0, "location_switch": 0, "role_switch": 0,
  "role_undocumented": 0, "role_contradicted": 0
}
```

All six `CONSTRAINT_SOLVER.md`-named categories are present, plus five
diagnostic sub-breakdown keys (not part of the spec, added in `93b05a4`
for interpretability). **Confirmed.**

### F7.2 — Structural-zero disclosure

`objective.STRUCTURAL_ZERO_CATEGORIES = frozenset({"temporal_violations",
"topological_violations"})`, surfaced as `structural_zero_categories` in
both `validation_summary.json` and every `scenario_NN.json` (added in
`ad8dc6b4`, this audit's baseline). Live-verified against a fresh run: the
two listed categories are indeed `0` in `penalty_breakdown`, matching
`test_structural_zero_categories_are_actually_always_zero_in_practice`
(re-run for this audit: **PASSED**). **Confirmed, and this is the exact
gap F6/F7's parent patch (`ad8dc6b4`) was scoped to close.**

### F7.3 — Lambda weights and dominance

`config.py`: `LAMBDA_1_ARCHIVAL_CONTRADICTIONS = 100.0`,
`LAMBDA_2` through `LAMBDA_6 = 1.0` each. `objective.build_objective()`
casts each via `int(...)` and sums them into a single `cp_model.Minimize`
call. Lambda1 is 100× every other weight — numerically dominant as
`CONSTRAINT_SOLVER.md` requires ("`lambda1` must dominate all other
penalties"), not merely asserted in a comment. **Confirmed**, unchanged
by this patch (pre-existing since `93b05a4`).

### F7.4 — Category-to-function mapping is documented, not silently reinterpreted

`objective.py`'s own module docstring states explicitly that
`archival_contradictions` and `over_assignment` are *interpretive*
reassignments of specific soft-penalty functions to
`CONSTRAINT_SOLVER.md`'s named categories (e.g. `over_assignment` is
mapped to task/location/role-switch penalties as "the closest proxy
available," not a literal spec term). This interpretive choice is
disclosed in-source but **is not itself disclosed in any JSON/CSV
output** — a reader of `scenario_NN.json` alone sees a category named
`over_assignment` with no indication that this label is this
implementation's interpretive stand-in rather than a literal
`CONSTRAINT_SOLVER.md` term with an unambiguous, spec-given definition.
**Not addressed by `ad8dc6b4`** — Item 2 of the v0.1.2 patch closed the
structural-zero gap but did not extend disclosure to this separate,
still-open interpretive-mapping gap.

### F7.5 — Sub-breakdown arithmetic consistency

`test_scenario_output_includes_penalty_breakdown_with_six_categories`
(`tests/salido_hdt/solver/test_cli_pipeline.py`) asserts, against a real
run: `task_switch + location_switch + role_switch == over_assignment` and
`role_undocumented + role_contradicted == unsupported_assignments`.
Re-run for this audit: **PASSED**. **Confirmed.**

### F7.6 — `penalty_breakdown` reflects the actual solved CP-SAT result

`scenario_collector._snapshot()` computes every `penalty_breakdown` entry
via `sum(solver.Value(v) for v in terms)` on the *same solved model
instance* used to populate `assignment`, not a separately-recomputed
estimate — the two cannot drift apart by construction. **Confirmed**,
unchanged by this patch.

### F7 status: **partially_complete**

**What is fully resolved:** all six spec categories present and correctly
computed (F7.1), lambda dominance enforced numerically (F7.3), structural-
zero disclosure now present (F7.2, this patch's direct contribution),
sub-breakdown arithmetic verified consistent (F7.5), and no drift between
reported and solved values is possible by construction (F7.6).

**What remains incomplete:** the interpretive category-to-function mapping
(F7.4) is documented in source but not disclosed in any output artifact —
a downstream reader of `scenario_NN.json` in isolation cannot tell that
`archival_contradictions`/`over_assignment` are this implementation's
interpretive stand-ins rather than literal `CONSTRAINT_SOLVER.md`
definitions, without reading `objective.py`'s source. This is the same
class of "documented in a docstring nobody reading the JSON sees" gap that
motivated F7.2's fix in `ad8dc6b4` — it was not extended to cover this
second instance of the same underlying problem.

---

## Summary

| Requirement | Status |
|---|---|
| F6 (schicht semantics) | **partially_complete** — core defect fixed and tested; controlled domain, evidence-gating for labeled shifts, and per-schicht capacity reporting remain unbuilt |
| F7 (objective and penalty accounting) | **partially_complete** — structural-zero disclosure now complete; category-to-function interpretive-mapping disclosure remains open |

No code or data was modified in the course of this audit. All cited test
results were reproduced by re-running the existing, already-committed
test suite (176 tests, `ad8dc6b4`) plus fresh, discarded `cli.run()`
output inspection — no new test files were added, since this task is
read-only per its own instructions.
