# SALIDO-HDT Solver v0.1.1 — Formulation & Interpretability Fix Plan

Patch target: **Solver v0.1.1**. Baseline: **Solver v0.1**, commit `1cb16df`
(`feat(salido-hdt): add validation-first historical reconstruction solver`),
which remains the recorded baseline in git history — this codebase is
software, not a dataset snapshot, so "v0.1 remains the baseline" is honored
via git history (`git show 1cb16df`), not a duplicated source tree, unlike
the `salido_hdt_model_v0_*` dataset directories. No dataset directory is
touched by this patch. `docs/enclave/salido_hdt_model_v0_4_1/` remains the
sole, read-only canonical input; `v0.3`/`v0.4`/`v0.4.1` are not modified.

This plan responds point-by-point to
`docs/enclave/implementation/SOLVER_SCENARIO_INTERPRETATION_AUDIT.md`
(not rewritten, not deleted — it stays as the frozen record of what v0.1
produced and why it was unsafe to read as-is).

**Guardrails restated for this patch specifically** (from the task
instructions, binding on every fix below):
- Do not optimize ore output, labour use, or group utilization — no fix may
  add a term that *rewards* assignment/utilization.
- Do not force any aggregate group to receive an assignment — no fix may
  add a term or constraint that *requires* assignment either.
- The patch removes formulation **bias**; it must not replace one bias
  (idle-favoring... or rather, in v0.1, idle-forced-by-accident) with
  another (assignment-favoring). The correct target state is
  **indifference** between idle and assigned where the archive itself is
  silent — i.e. historical underdetermination, preserved, not resolved by
  the objective function.

---

## F1 — CRITICAL: aggregate groups structurally erased via two compounding penalty bugs

**Root cause (mechanism 1 of 2).**
`soft_constraints.add_task_continuity_penalty` builds a `switch` BoolVar for
every consecutive `(h,t),(h,t+1)` pair for which *any* `x`-variable exists,
regardless of whether those variables are true. The lower-bound constraint
`sum(same_task_indicators) + switch >= 1` has no term expressing "both
periods idle" as a legitimate, zero-cost third state — idle is implicitly
treated as a task that never matches itself, so idle→idle is
indistinguishable from a genuine task-to-task change and is forced to
`switch = 1`.

**Root cause (mechanism 2 of 2).**
`soft_constraints.add_unsupported_role_switching_penalty` penalizes every
assignment of an entity absent from `person_roles` (i.e. `person_roles.get(h)
is None`) to a role-declaring task. All 18 rows of
`14_task_requirements.csv` declare a preferred role, so every aggregate
group — which can *never* appear in `04_person_roles.csv` by schema, not by
evidentiary gap, since that table only has rows for named individuals —
pays this penalty on every period it is assigned anything. The function
does not distinguish "this entity's role is undocumented" (a real
evidentiary gap, correctly soft-penalized for a *named individual*) from
"this entity is a class of record for which `04` conceptually cannot ever
apply" (a schema fact about aggregate groups, not a gap).

**Affected module / functions.**
`src/salido_hdt/solver/soft_constraints.py`:
`add_task_continuity_penalty`, `add_unsupported_role_switching_penalty`.
Call sites in `src/salido_hdt/solver/cli.py::run()`.

**Current mathematical behaviour.**
For an entity present across `N` consecutive weekly buckets with zero legal
task assignments in all of them: continuity penalty = `N-1` (one "switch"
per idle→idle pair). For the same entity assigned to one consistent
role-undocumented-relative task across all `N` buckets: unsupported-role
penalty = `N`. Verified on real data: `N=17` for the 10 aggregate groups
present at `L-BENEDEN-PAGGER` → idle costs 16, uniform-assignment costs 17.
The 1-unit margin is what pushes every group to idle in every scenario
(objective 160 ≈ 10 × 16).

**Intended behaviour.**
- A genuine task-to-task change while continuously present costs 1 (soft
  "continuity" signal — unchanged intent from `CONSTRAINT_SOLVER.md`).
- Idle→idle costs 0. Idle↔active transitions cost 0 (this function is about
  task continuity, not presence/absence, which is governed elsewhere by
  `add_temporal_presence`).
- An aggregate group being assigned to a role-declaring task costs 0 extra
  for "lacking a role" specifically, because "lacking a role" is not a
  meaningful evidentiary statement about a group — `04_person_roles.csv`
  structurally never has group rows. A *named individual* lacking a
  documented role assigned to a role-declaring task should still cost 1 per
  period (unchanged: that is a real, informative evidentiary gap for an
  individual).
- Net effect: for a group, idle and assigned-with-no-other-penalty become
  cost-equal (0 vs 0) — the solver has no formulation-driven reason to
  prefer either. Any remaining preference must come from genuine evidence
  (e.g. `add_role_location_preference_penalty`, `add_explicit_location_preference_penalty`),
  not from an artifact of these two functions.

**Proposed code change.**

1. `add_task_continuity_penalty`: introduce two auxiliary `BoolVar`s per
   `(h,t)` group, `active_t`/`active_t1`, each tied to the OR of that
   period's task variables via `model.AddMaxEquality(active, list(vars.values()))`.
   Replace the unconditional `switch >= 1 - sum(same_task_indicators)` /
   `switch == 1` logic with:
   `model.Add(switch >= active_t + active_t1 - 1 - sum(same_task_indicators))`.
   This is 0 whenever either period is inactive (idle), and forces
   `switch=1` only when both periods are active and no matching task fired.
   Skip the `(h,t)` pair entirely (no `active`/`switch` vars at all) if
   neither period has any variable — nothing to compare.

2. `add_unsupported_role_switching_penalty`: add a parameter
   `aggregate_group_ids: frozenset[str] = frozenset()`. Skip any `h in
   aggregate_group_ids` before adding its penalty var — group assignments
   are never penalized for "unsupported role" by this function. Named
   individuals absent from `person_roles` are unaffected and keep the
   existing soft penalty.

3. `cli.py`: add `_aggregate_group_ids(dataset) -> frozenset[str]`, built
   from `{h.human_or_group_id for h in dataset.hrlt_records.values() if
   h.entity_type == EntityType.AGGREGATE_GROUP}` — the same set that
   actually receives `x`-variables (not `06_human_groups.csv`'s full
   17-row id set, 7 of which never appear in `07` at all and therefore
   never reach this function regardless). Pass it into
   `add_unsupported_role_switching_penalty`.

**Required regression tests.**
New file `tests/salido_hdt/solver/test_task_continuity_and_role_bias.py`:
- `test_idle_idle_transition_costs_nothing` — two periods, all vars 0,
  `switch` must solve to 0 (was 1 in v0.1; this is the direct regression
  guard for the bug).
- `test_active_active_same_task_costs_nothing` (unchanged behaviour,
  re-asserted so the rewrite didn't regress it).
- `test_active_active_different_task_still_costs_one` (unchanged intent,
  re-asserted).
- `test_active_idle_transition_costs_nothing` — one period active, the
  other idle; must not be forced to `switch=1`.
- `test_aggregate_group_not_penalized_for_missing_role` —
  `add_unsupported_role_switching_penalty` with `h` in
  `aggregate_group_ids`: returns no penalty var for that entity even though
  the task declares a preferred role.
- `test_named_individual_without_role_still_penalized` — same task, `h` a
  named individual not in `aggregate_group_ids` and absent from
  `person_roles`: still penalized (regression guard that F1's fix did not
  over-correct into "never penalize anyone").
- `test_group_idle_vs_assigned_are_cost_equal_on_real_presence_window` —
  integration-level, built from `G-MS-121`'s real 17-week presence window:
  solve the model twice (once forcing all-idle, once forcing one consistent
  role-declaring task across the window) with both fixed functions wired
  exactly as `cli.run()` wires them; assert the two objective values are
  **equal**, not that either is preferred. This is the direct test of "bias
  removed, underdetermination preserved" — it must never assert that
  assignment is forced or preferred.

**Ethical implication.**
This is the load-bearing fix for the whole patch. Before it, `scenario_*.json`
could be read as "the archive shows coerced-labor groups did nothing while
Dutch officials performed the mine labor" — a formulation artifact standing
in for, and contradicting, the archive. After it, the solver has no
structural preference either way for a group; if a scenario shows a group
idle, that must trace to an actual absence of favorable evidence elsewhere
in the model, not to this bug. This directly implements
`ETHICAL_MODELING.md`'s requirement that aggregate groups be assignable
without being either scored for productivity (already true, `[[project_causal... ]]`
not relevant here — see original ethical guard, unchanged) or structurally
punished into invisibility (the new requirement this patch adds).

**Data-model implication.** None — no CSV, no domain dataclass, no
provenance classification changes. This is purely an objective-formulation
fix; `validation.py`'s HARD/SOFT classification of every record is
untouched.

**Acceptance criterion.** On the real v0.4.1 dataset, re-running
`cli.run()`: (a) `test_group_idle_vs_assigned_are_cost_equal_on_real_presence_window`
passes; (b) the total objective value no longer decomposes as
`~16 × (number of idle groups)` (verified by inspecting the new
per-category `penalty_breakdown`, F7); (c) no test anywhere asserts a group
must appear in `active_assignments` — presence or absence of a group in a
given scenario after this patch must be a legitimate tied/untied outcome,
never a required one.

---

## F2 — HIGH: entity exclusion from variable construction is invisible in output

**Root cause.** `variables.build_variables()` only creates `x`-variables
for an entity `h` if `presence.get(h)` is truthy. An entity can have a full
HARD-classified role in `04_person_roles.csv` and still receive zero
variables because it has no HARD-eligible HRLT presence record. Verified:
42 of 47 role-documented individuals (e.g. `P-BRETSNIJDER`, role
`R-BERGWERKER`) fall into this set. Nothing in `cli.py`'s output records
this; a reader sees only silence.

**Affected module / functions.** `src/salido_hdt/solver/cli.py::run()`
(output assembly only — no change to `variables.py`'s pruning logic itself,
which is correct and deliberate, see `variables.py`'s own docstring on
plan decision #3).

**Current mathematical behaviour.** N/A — this is a reporting gap, not a
formulation error. The pruning itself (only build variables for
HARD-attested presence) is correct and intentional; the problem is purely
that its consequence is undocumented in the artifact a reader actually
opens.

**Intended behaviour.** `validation_summary.json` enumerates, per known
entity id (union of `02_persons.csv` and the HRLT-derived aggregate-group
id set), a coverage record: `has_hard_role`, `has_hard_presence`,
`included_in_variables`. A reader can then distinguish "this entity is
absent from every scenario because the archive is silent about their
presence here" from "absent because the archive says they weren't here" —
the audit's core F2 risk.

**Proposed code change.** Add `cli._entity_coverage(dataset, sv) ->
list[dict]` and include its output under a new `"entity_coverage"` key in
`validation_summary.json`. Pure read/aggregate over already-computed
`sv.presence` / `sv.person_roles` plus `dataset.persons` /
`_aggregate_group_ids(dataset)` — no new classification logic.

**Required regression tests.** In `tests/salido_hdt/solver/test_cli_pipeline.py`:
- `test_entity_coverage_flags_role_documented_presence_excluded_individual`
  — asserts `P-BRETSNIJDER` appears with `has_hard_role=True`,
  `has_hard_presence=False`, `included_in_variables=False`.
- `test_entity_coverage_flags_fully_included_entity` — asserts one of the
  five presence+role individuals (e.g. `P-HESSE`) shows both flags `True`.
- `test_entity_coverage_covers_all_known_persons_and_groups` — count check
  against `dataset.persons` ∪ aggregate-group ids.

**Ethical implication.** Prevents "absence from scenario" from being
silently misread as "absence from the archive" for the 89% of
role-documented individuals this affects — a milder but real version of the
F1 misreading risk, this time about scope rather than the objective.

**Data-model implication.** None.

**Acceptance criterion.** `validation_summary.json` produced by a real
`cli.run()` contains an `entity_coverage` array whose length equals
`len(dataset.persons) + len(aggregate_group_ids)`, and the three tests
above pass against the real dataset.

---

## F3 — MEDIUM: equipment_capacity implemented but not enforced, and not declared

**Root cause.** `hard_constraints.add_equipment_capacity()` requires a
`(task_id, location_id, capacity)` triple that this codebase does not
derive automatically from `10_inventory_items.csv`, because doing so
generically would require inferring which task an inventory row's quantity
caps — a linkage the CSVs do not state as a foreign key, and inventing it
would violate this project's "do not invent archival evidence" discipline
that has governed every prior task in this dataset's lineage. The one
concrete case this session's own research identified by manual reading
(`INV-0232`, "60 bor tambang", `SOLVER_INPUT_READINESS.md` §8–9) ties to
drilling capacity, but not to a *specific* `location_id` the CSV states —
`SOLVER_INPUT_READINESS.md`'s own worked example used a placeholder
location for illustration, not a verified real one. Wiring it against an
unverified location would itself be an invention.

**Decision for this patch.** Do not fabricate the linkage. Instead, make
the gap **explicit and non-silent** in the run's own output, which is what
turns this from a silent risk into a documented, auditable limitation —
consistent with this patch's "interpretability" half.

**Affected module / functions.** `src/salido_hdt/solver/cli.py::run()`
(declaration only — `hard_constraints.add_equipment_capacity` itself is
unchanged and remains available, tested, and ready to wire once a verified
linkage is established in a future, separate task).

**Current mathematical behaviour.** No equipment cap is enforced anywhere
in `cli.run()`'s live pipeline; nothing in the objective or constraints
references `10_inventory_items.csv` at all today.

**Intended behaviour.** Unchanged solver behaviour (still not enforced —
this patch does not invent the linkage), but `validation_summary.json`
must say so explicitly: `"equipment_capacity_enforced": false` plus a
`"equipment_capacity_note"` string citing this decision and
`SOLVER_INPUT_READINESS.md` §8–9, so a reader of the output alone (not the
source code) knows this hard constraint category is not live.

**Proposed code change.** Add two fixed keys to the `summary` dict built in
`cli.run()`. No new function needed.

**Required regression tests.** In `test_cli_pipeline.py`:
- `test_validation_summary_declares_equipment_capacity_not_enforced` —
  asserts both keys are present with the documented values.

**Ethical implication.** None directly (equipment capacity is a physical
logistics constraint, not a labor-productivity term — wiring it would not
violate the "no group utilization objective" guardrail even if it were
wired), but leaving it silently absent risks a reader trusting a capacity
guarantee that isn't actually running.

**Data-model implication.** None — no CSV column is read differently.

**Acceptance criterion.** The two new keys are present and correctly
valued in a real `cli.run()` output; the audit's F3 risk (silent absence)
is closed by declaration, not by an invented linkage.

---

## F4 — MEDIUM: role-task compatibility ignores the task requirement's own evidentiary strength

**Root cause.** `cli._task_preferred_roles()` builds
`{task_id: set(preferred_role_ids)}` from every row of
`14_task_requirements.csv` unconditionally. `add_role_task_compatibility`
then treats this as an absolute HARD exclusion. A task requirement row
whose own `constraint_strength` is `"soft"`/interpreted still hard-forbids
every role-undocumented entity — the requirement row's own self-declared
evidentiary weakness is discarded before it reaches the HARD constraint
builder.

**Affected module / functions.** `src/salido_hdt/solver/cli.py`.
`hard_constraints.add_role_task_compatibility` itself is correct and
unchanged — it faithfully hard-enforces whatever it is given; the bug is
entirely in what `cli.py` gives it.

**Current mathematical behaviour.** Every one of the 18 task rows (all 18
declare a `preferred_role_ids`) is treated as HARD regardless of
`constraint_strength`.

**Intended behaviour.** Only task-requirement rows that
`validation.classify_hard_soft()` itself classifies `HARD` feed the HARD
constraint. Rows it classifies otherwise (`SOFT`/`CONTEXT_ONLY`) are
excluded from the HARD role-task gate — an entity is not hard-blocked from
a softly-attested task preference. (Soft task-role signal is not separately
re-added as a new soft penalty in this patch — the guardrail against
optimizing labour allocation makes adding a new soft "prefer the declared
role" term here unnecessary scope creep; the existing
`add_unsupported_role_switching_penalty` already covers the adjacent soft
signal for role-undocumented entities generally.)

**Proposed code change.** Add
`_hard_task_preferred_roles(dataset) -> dict[str, set[str]]` in `cli.py`,
identical to `_task_preferred_roles()` but filtered by
`classify_hard_soft(task_requirement, classify_provenance(task_requirement,
dataset), dataset) == HardSoftLabel.HARD`. Use this new function (not the
old one) as the input to `add_role_task_compatibility`. Keep
`_task_preferred_roles()` (all 18, unfiltered) as-is for
`add_unsupported_role_switching_penalty`'s input, since that function is
soft by construction and the audit did not flag its own input as needing
this gate.

**Required regression tests.** In `test_cli_pipeline.py`:
- `test_hard_task_preferred_roles_excludes_non_hard_requirement_rows` —
  run `_hard_task_preferred_roles` against the real dataset and cross-check
  every included `task_id` independently classifies `HARD` via
  `validation.classify_hard_soft`.
- `test_hard_task_preferred_roles_subset_of_all_task_preferred_roles` —
  structural invariant, guards against the two functions diverging in
  unexpected ways later.

**Ethical implication.** None specific to labor representation; this is a
provenance-discipline fix in the same family as the rest of this dataset's
migration history (not over-claiming hardness for a softly-attested
constraint).

**Data-model implication.** None.

**Acceptance criterion.** `_hard_task_preferred_roles(dataset)`'s output,
run against the real v0.4.1 dataset, is a (possibly proper) subset of
`_task_preferred_roles(dataset)`'s output, and the regression tests above
pass.

---

## F5 — MEDIUM: scenario output carries no evidence citation per assignment

**Root cause.** `cli.run()`'s scenario-writing loop emits
`{human_or_group_id, task_id, location_id, schicht, time_bucket}` per
active assignment with no back-reference to the HRLT record(s) that
established the entity's presence at that location/time, breaking this
dataset lineage's citation-traceability discipline the moment output
leaves the pipeline.

**Affected module / functions.** `src/salido_hdt/solver/cli.py::run()`.

**Current mathematical behaviour.** N/A — output formatting only.

**Intended behaviour.** Each `active_assignments` entry additionally
carries `"presence_hrlt_ids"`: the `hrlt_id`(s) of the HARD-classified
`07_human_role_location_time.csv` record(s) whose `(location_id,
valid_from..valid_to)` window covers this assignment's `(location_id,
time_bucket)`. This is a pure lookup against already-loaded data — no new
evidence is inferred, only cited.

**Proposed code change.** Add
`cli._citations_for(dataset, sv, h, l, t) -> list[str]`, iterating
`dataset.hrlt_records` for records matching `human_or_group_id == h`,
`location_id == l`, HARD-classified, whose bucket-index window contains
`t` (reusing `variables._parse_date`/`_bucket_index_for` via
`sv.presence`'s already-computed windows — simplest correct approach:
match against `sv.presence[h]`'s `(location_id, t_from, t_to)` tuples
directly, then map back to the originating `hrlt_id`s by re-scanning
`dataset.hrlt_records` for the same `(h, l)` pair. Call this per assignment
when writing `scenario_NN.json`.

**Required regression tests.** In `test_cli_pipeline.py`:
- `test_scenario_output_assignments_carry_presence_citations` — run
  `cli.run()` for real, assert every `active_assignments` entry has a
  non-empty `presence_hrlt_ids` list, and that each cited `hrlt_id` is a
  real key in `dataset.hrlt_records` whose `human_or_group_id`/
  `location_id` match the assignment.

**Ethical implication.** Restores auditability: a reader can now trace any
assignment (including one involving an aggregate group, once F1 no longer
suppresses them) back to the specific archival record that licensed its
presence claim, without re-running the pipeline.

**Data-model implication.** None — no CSV or dataclass change; this reads
existing loaded data.

**Acceptance criterion.** The regression test above passes against a real
`cli.run()` output.

---

## F6 — LOW: schicht flatness and scenario-diversity scope are undocumented in output

**Root cause.** `DEFAULT_SCHICHT_COUNT=1` (documented in `config.py`, but
only there). A reader of `scenario_NN.json` alone has no way to know
scenario-to-scenario diversity is task-choice-only (location and time
window are fixed pre-solve by the HARD presence pruning) without reading
`variables.py`'s source.

**Affected module / functions.** `src/salido_hdt/solver/cli.py::run()`.

**Intended behaviour.** `validation_summary.json` gains a `"run_metadata"`
object stating the modeling assumptions a reader needs to correctly scope
their interpretation: `schicht_count`, `time_bucket_width_days`, and a
short fixed string explaining that scenario diversity reflects task choice
within an already HARD-fixed (entity, location, time-window) presence set,
not alternate presence histories.

**Proposed code change.** Add a `run_metadata` dict, sourced directly from
`config.DEFAULT_SCHICHT_COUNT` / `sv.schicht_count` and a fixed
explanatory string constant, to the `summary` dict.

**Required regression tests.** In `test_cli_pipeline.py`:
- `test_validation_summary_includes_run_metadata` — key presence and
  correct `schicht_count` value check.

**Ethical implication.** None beyond the general interpretability goal of
this patch.

**Data-model implication.** None.

**Acceptance criterion.** `run_metadata.schicht_count == 1` in a real run's
`validation_summary.json`, and the test passes.

---

## F7 — LOW: no per-category penalty breakdown, so F1-style dominance is invisible without reading source

**Root cause.** `cli.run()` builds six penalty-term lists and calls
`objective.build_objective()`, which returns a single aggregated
`LinearExpr`. `scenario_collector.collect_scenarios()` records only the
scalar `objective_value` per scenario; the six categories' individual
solved sums are discarded.

**Affected module / functions.**
`src/salido_hdt/solver/scenario_collector.py` (`Scenario` dataclass,
`collect_scenarios`), `src/salido_hdt/solver/cli.py::run()`.

**Current mathematical behaviour.** N/A — reporting gap.

**Intended behaviour.** Each `Scenario` (and therefore each
`scenario_NN.json`) carries a `penalty_breakdown` dict: one key per
objective category (`archival_contradictions`, `unsupported_assignments`,
`temporal_violations`, `topological_violations`, `role_location_penalties`,
`over_assignment`), each value the solved sum of that category's raw
(unweighted) penalty variables at that scenario's solution. This is
diagnostic only — it does not change what is minimized, only what is
reported.

**Proposed code change.**
`collect_scenarios()` gains an optional parameter
`penalty_terms: dict[str, list[cp_model.IntVar]] | None = None`. When
given, each captured `Scenario` additionally stores
`{name: sum(solver.Value(v) for v in terms) for name, terms in
penalty_terms.items()}`. `cli.run()` passes the same six lists it already
built for `build_objective()` under their category names, and writes
`penalty_breakdown` into each `scenario_NN.json`.

**Required regression tests.** In `test_multiple_scenarios.py`:
- `test_scenario_penalty_breakdown_matches_named_terms` — synthetic model
  with two named penalty categories, assert the returned `Scenario.penalty_breakdown`
  matches hand-computed values for a forced solution.
- `test_penalty_breakdown_defaults_to_empty_when_not_provided` — backward
  compatibility: omitting `penalty_terms` still returns scenarios (all
  existing calls/tests keep working unchanged).

In `test_cli_pipeline.py`:
- `test_scenario_output_includes_penalty_breakdown_with_six_categories` —
  run `cli.run()` for real, assert every `scenario_NN.json` has a
  `penalty_breakdown` with exactly the six expected keys.

**Ethical implication.** This is what would have made F1 visible from the
output alone, without needing this audit's manual instrumentation — the
core interpretability goal of this whole patch.

**Data-model implication.** None.

**Acceptance criterion.** All three tests above pass; a real `cli.run()`'s
`scenario_00.json` shows `penalty_breakdown["over_assignment"]` no longer
dominated by idle-miscounted-as-switch cost (cross-checked against F1's
fix — this is the closing verification that F1 actually worked, visible
from the artifact itself).

---

## Cross-cutting acceptance check (all seven findings together)

After all seven fixes: re-run `cli.run()` against the real v0.4.1 dataset
with `--scenarios 3`. Required, in one pass:

1. `validation_summary.json` contains `entity_coverage` (F2),
   `equipment_capacity_enforced`/`equipment_capacity_note` (F3), and
   `run_metadata` (F6).
2. Every `scenario_NN.json` assignment carries `presence_hrlt_ids` (F5) and
   every scenario file carries `penalty_breakdown` with six keys (F7).
3. No aggregate group is forced into or out of `active_assignments` by any
   new constraint — only F1's bias-removal is present.
4. Full test suite (v0.1's original 51 + this patch's new tests) passes.
5. SHA-256 immutability re-verified for `salido_hdt_model_v0_3/`,
   `salido_hdt_model_v0_4/`, `salido_hdt_model_v0_4_1/` — unchanged.
6. This document and `SOLVER_SCENARIO_INTERPRETATION_AUDIT.md` are both
   still present, unedited in their findings text.
