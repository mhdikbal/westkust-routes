# SALIDO-HDT Solver v0.1.2 — Interpretability Fix Plan

Patch target: **Solver v0.1.2**. Baseline: commit `93b05a4`
("fix(salido-hdt): enforce equipment capacity and atomic constraint
strength"), itself built on `1cb16df` ("feat(salido-hdt): add
validation-first historical reconstruction solver"). **Neither commit is
amended by this patch** — this is a new, separate commit on top of
`93b05a4`.

Canonical research inputs remain read-only, unchanged by this patch:
`docs/enclave/salido_hdt_model_v0_3/`, `salido_hdt_model_v0_4/`,
`salido_hdt_model_v0_4_1/`.

This plan covers four items, all interpretability/correctness gaps
identified while re-reading the shipped v0.1.1 code against
`docs/enclave/salido_hdt_model_v0_4_1/docs/CONSTRAINT_SOLVER.md`'s own
specification — none were flagged in `SOLVER_SCENARIO_INTERPRETATION_
AUDIT.md` or `SOLVER_V0_1_1_FIX_PLAN.md`, so this is a new, independent
finding set, not a re-litigation of F1-F10.

---

## Item 1 — F6: schicht semantics (equipment capacity is schicht-blind)

**Current behaviour.** `CONSTRAINT_SOLVER.md` defines the decision
variable as `x[h,j,l,s,t]` — schicht `s` is a first-class axis alongside
time `t`. `hard_constraints.add_equipment_capacity()` groups candidate
variables by `t` only:

```python
by_time: dict[int, list[cp_model.IntVar]] = defaultdict(list)
for (h, j, l, s, t), var in x_vars.items():
    if j == task_id and l == location_id:
        by_time[t].append(var)
for t, vs in by_time.items():
    model.Add(sum(vs) <= capacity)
```

This silently sums across **every** schicht value within a time bucket as
if they shared one capacity pool. It is dormant and invisible today only
because `config.DEFAULT_SCHICHT_COUNT = 1`, so `s` is always `0` and the
grouping is accidentally correct. It is a latent correctness defect: if
`DEFAULT_SCHICHT_COUNT` were ever raised (e.g. day/night shifts), this
function would under-count available capacity by pooling schicht-disjoint
equipment as if it were schicht-shared, or over-count if equipment is
meant to be schicht-exclusive — the function does not express either
policy, it just ignores the axis.

`docs/CONSTRAINT_SOLVER.md`'s own hard-constraint list separately states
"one location per schicht" (`sum_l x[h,j,l,s,t] <= 1`, already correctly
per-`(h,s,t)` in `add_one_location_per_schicht`) but says nothing about
whether equipment capacity is meant to be per-schicht or shared across
schicht within a time bucket — the source spec is silent on this, so this
patch cannot resolve the POLICY question by invention. What it CAN and
must fix is that the current code has no policy at all, just an
unexamined bug.

**Intended behaviour.** `add_equipment_capacity()` groups by `(s, t)`
instead of `t` alone — i.e. **per-schicht** capacity, the more
conservative reading (never allows two schicht to silently share one
capacity pool unless the caller explicitly pools them). This is the
minimal, non-inventive fix: it makes the function actually respect the
axis CONSTRAINT_SOLVER.md defines, without asserting a specific real-world
staffing policy the archive doesn't state. Behaviourally identical to
today at `DEFAULT_SCHICHT_COUNT=1` (verified: with a single schicht value,
grouping by `(s,t)` and by `t` alone produce identical partitions) —
this patch is a no-behaviour-change-today, correctness-for-the-future fix,
verified by a dedicated regression test using a synthetic 2-schicht model
(which the real dataset cannot exercise, since it never uses more than one
schicht).

**Affected modules.** `src/salido_hdt/solver/hard_constraints.py`
(`add_equipment_capacity`). No caller-side change needed in `cli.py` --
it already passes the full `sv.x` dict, unaffected by the grouping key
change internal to the function.

**Mathematical formulation.**

Before: `∀t: Σ_{h,j,l fixed, s any} x[h,j,l,s,t] ≤ capacity`

After: `∀(s,t): Σ_{h,j,l fixed} x[h,j,l,s,t] ≤ capacity`

**Output-schema changes.** None. `equipment_capacity.csv`'s columns are
unchanged; the fix is purely inside constraint construction.

**Regression tests.** New test in
`tests/salido_hdt/solver/test_equipment_capacity_cli_wiring.py` (or a new
file `test_schicht_capacity.py`):
- `test_equipment_capacity_is_per_schicht_not_pooled_across_schicht` --
  synthetic model with `DEFAULT_SCHICHT_COUNT`-independent 2 schicht
  values at the same `(task, location, time)`, capacity=1 each; assert
  both schicht can be simultaneously at their own cap of 1 (2 total
  active), which the OLD pooled-by-`t`-only code would have forbidden
  (it would have capped the sum across both schicht at 1, not 2).
- `test_equipment_capacity_behaviour_unchanged_at_schicht_count_one` --
  same real-dataset capacity report driving the constraint at
  `schicht_count=1`; solved bound must be identical before/after (this is
  the "no behaviour change today" claim, verified not just asserted).

**Acceptance criterion.** Both new tests pass; the full existing suite
(161 tests as of `93b05a4`) still passes unchanged; a real `cli.run()`
still reports exactly 7 equipment-capacity constraints instantiated
(unchanged, since real data never exercises `s != 0`).

---

## Item 2 — F7: objective and penalty accounting (structural vs. live categories are indistinguishable in output)

**Current behaviour.** `penalty_breakdown` in every `scenario_NN.json`
reports six numbers: `archival_contradictions, unsupported_assignments,
temporal_violations, topological_violations, role_location_penalties,
over_assignment` (plus diagnostic sub-breakdowns). Two of these --
`temporal_violations` and `topological_violations` -- are **structurally
always zero**: `objective.py`'s own docstring already states they are
"hard-enforced... structurally zero," because `add_temporal_presence()`
and `add_topological_feasibility()` are wired as absolute HARD exclusions
(`model.Add(var == 0)`), never as soft penalty terms. A reader of a single
`scenario_NN.json` cannot tell the difference between "this run happened
to have zero temporal violations" (a real, contingent finding) and "this
objective category can never be anything but zero given how this solver
is wired" (a structural fact about the code, true for every possible
scenario forever) -- both currently render identically as `0`.

**Intended behaviour.** Every `scenario_NN.json` and
`validation_summary.json` explicitly lists which of the six objective
categories are **structural-zero** (cannot vary, by construction) vs.
**live** (can genuinely vary run to run). This is a pure reporting
addition -- it changes no weighting, no minimization behaviour, nothing
about what is computed, only what is disclosed about what was computed.

**Affected modules.** `src/salido_hdt/solver/objective.py` (expose the
structural-zero category names as a module-level constant, since the
docstring already states this as a hardcoded fact of this implementation),
`src/salido_hdt/solver/cli.py` (write the constant into both output
locations).

**Mathematical formulation.** No formula changes. Documentation-only:

```
STRUCTURAL_ZERO_CATEGORIES = {"temporal_violations", "topological_violations"}
```

is true precisely because, in `cli.run()`'s wiring,
`penalty_terms["temporal_violations"] = []` and
`penalty_terms["topological_violations"] = []` are passed as empty lists
unconditionally (not because no violations happened to occur this run --
because no violation-tracking variable for these two categories is ever
constructed at all).

**Output-schema changes.** Add `"structural_zero_categories":
["temporal_violations", "topological_violations"]` to
`validation_summary.json`, and add the same list (or a boolean per-key
`"is_structural_zero"` map alongside `penalty_breakdown`) to every
`scenario_NN.json`.

**Regression tests.** New assertions in `test_cli_pipeline.py` or a new
`test_objective_accounting.py`:
- `test_structural_zero_categories_reported_in_validation_summary`.
- `test_structural_zero_categories_reported_in_scenario_json`.
- `test_structural_zero_categories_are_actually_always_zero_in_practice`
  -- run the real pipeline and assert every reported structural-zero
  category's `penalty_breakdown` value is `0` (a live check that the
  documentation constant hasn't drifted out of sync with the actual
  wiring, which a plain docstring claim cannot self-verify).

**Acceptance criterion.** The three tests above pass; a real `cli.run()`'s
`validation_summary.json` and every `scenario_NN.json` carry the new
field with the correct two-element list.

---

## Item 3 — Capacity-bound interpretation (required_capacity is an archival floor, not a simultaneous-use demand estimate; bound rationale is undocumented in the report itself)

**Current behaviour.** `equipment_capacity.CapacityReport.required_capacity`
is sourced from `TaskRequirement.minimum_workers_assumption`, which is
**always `1.0`** for all 18 real task rows (verified in
`SOLVER_V0_1_1_FIX_PLAN.md`'s and this session's own data dump). This
field genuinely means "the archivally-assumed minimum crew size to run
this task at all" -- it does NOT mean "the maximum number of workers who
might simultaneously want this equipment," which is what
`capacity_status` (`sufficient` / `uncertain_sufficient` / `insufficient`)
is actually being compared against as if it were a realistic demand
ceiling. Separately, `hard_capacity_bound()`'s choice to wire
`confirmed_capacity + uncertain_capacity` (not confirmed alone) as the
HARD cap is justified in a docstring, but that rationale is not visible
in `equipment_capacity.csv` itself -- a reader of the CSV alone sees only
the two numbers and the final status, not why the wired bound is their
sum.

**Intended behaviour.**
1. Rename the reported field's semantics explicitly in output (not the
   CSV column name, to avoid an unnecessary schema break -- add a
   sibling column) -- `equipment_capacity.csv` gains a
   `required_capacity_semantics` column with the fixed string
   `"archival_minimum_crew_size"`, so `required_capacity=1.0` is never
   misread as "this task never needs more than one unit of equipment."
2. `equipment_capacity.csv` gains a `hard_bound_rationale` column stating,
   per row, which quantity was actually wired into
   `add_equipment_capacity()` and why -- e.g.
   `"confirmed_capacity + uncertain_capacity (condition data mostly
   unknown in the real archive; confirmed-only would hard-forbid tasks
   the archive does not actually forbid)"` for a matched row, or `"no
   constraint instantiated (no_inventory_match / no_requirement_declared)"`
   for an unmatched one.

**Affected modules.** `src/salido_hdt/solver/equipment_capacity.py`
(`CapacityReport` gains two fields, `write_equipment_capacity_csv` gains
two columns).

**Mathematical formulation.** None changed -- `hard_capacity_bound()`'s
formula (`confirmed + uncertain`) is unchanged; this item is purely about
making the existing formula's rationale legible in the artifact itself
rather than only in source-code docstrings.

**Output-schema changes.** `equipment_capacity.csv` gains two columns:
`required_capacity_semantics`, `hard_bound_rationale`. `CapacityReport`
dataclass gains matching fields with sensible defaults so existing
callers of `compute_capacity_reports()` are not broken.

**Regression tests.** New tests in `test_equipment_capacity_cli_wiring.py`:
- `test_required_capacity_semantics_is_reported`.
- `test_hard_bound_rationale_distinguishes_matched_and_unmatched_pairs`.
- `test_real_run_equipment_capacity_csv_has_new_columns` -- real
  `cli.run()`, read `equipment_capacity.csv`, assert both new columns
  present and non-empty for all 45 real (task, location) rows.

**Acceptance criterion.** The three tests above pass; a real
`equipment_capacity.csv` shows `required_capacity_semantics=
archival_minimum_crew_size` on every row and a non-empty
`hard_bound_rationale` on every row (matched or not).

---

## Item 4 — Scenario semantic differentiation (a degenerate all-idle optimum silently collapses "1 scenario returned" and "1 scenario exists" into the same output)

**Current behaviour.** Verified empirically against the real dataset:
`cli.run(..., max_scenarios=5)` on `docs/enclave/salido_hdt_model_v0_4_1/`
produces exactly **one** `scenario_NN.json` file, regardless of how many
were requested, because the current unbiased objective's optimum is the
fully-idle assignment (objective value `0`) and
`scenario_collector.collect_scenarios()`'s diversification loop reads:

```python
true_keys = [k for k, v in decision_vars.items() if solver.Value(v) == 1]
if not true_keys:
    break
```

With zero true decision variables in the optimal solution, there is
nothing to build a no-good cut from, so the loop stops immediately after
the first solve. `CONSTRAINT_SOLVER.md` explicitly requires: "Return all
optimal or near-optimal scenarios within a declared tolerance. Do not
collapse equally plausible histories into one answer." An all-idle
optimum is very likely NOT the only tied-optimal solution (many different
single-entity assignments cost exactly `0` too, e.g. assigning `P-HESSE`
to their own matching role/task costs nothing) -- but the current
mechanism cannot discover or report any of them, and nothing in the
output discloses that this happened. A reader sees `n_scenarios: 1` and
cannot tell "the solver proved this is the unique optimum" from "the
solver's diversification mechanism gave up because the first solution had
no true variables to cut against."

**Intended behaviour.** This patch does **not** attempt full combinatorial
enumeration of a potentially enormous tied-optimum equivalence class --
that is out of scope (see "Remaining limitations" below) and risks being
either too slow or producing an arbitrary, equally-uninformative sample of
an astronomically large tied set. Instead, `collect_scenarios()` is
extended to:
1. Attempt one bounded round of degenerate diversification when
   `true_keys` is empty: try forcing each of up to
   `config.MAX_SCENARIOS - 1` arbitrary, not-yet-tried decision variables
   to `1` (one at a time, each as its own re-solve under the existing
   tolerance bound), keeping any that remain feasible within tolerance as
   additional scenarios, until the scenario budget is reached or no more
   forcing attempts remain among the candidate variables.
2. Every returned scenario collection carries an explicit
   `scenario_semantics` classification, one of:
   - `"unique_optimum"` -- the tolerance-bounded re-solve after excluding
     the first solution's variables was infeasible (or, in the degenerate
     case, every attempted forcing was infeasible/out-of-tolerance) --
     genuinely no other tied/near-tied solution exists.
   - `"degenerate_tied_optimum_partial_sample"` -- the first solution had
     no true variables (nothing to cut against directly), and the bounded
     forcing round in step 1 found at least one more feasible
     within-tolerance alternative. The label makes explicit that
     additional tied solutions almost certainly exist beyond the small
     sample actually returned.
   - `"multiple_scenarios"` -- the existing, already-correct case: the
     original no-good-cut loop found and returned more than one distinct
     scenario via true-variable exclusion.

**Affected modules.** `src/salido_hdt/solver/scenario_collector.py`
(`collect_scenarios`, `Scenario` gains a module-level or per-collection
`scenario_semantics` field), `src/salido_hdt/solver/cli.py` (write the
classification into `validation_summary.json`).

**Mathematical formulation.** No change to the objective. The
diversification search, formalized:

```
best = solve(model)
if true_keys(best) != ∅:
    # existing no-good-cut loop, unchanged
    ...
else:
    for v in candidate_vars (bounded to MAX_SCENARIOS - 1 attempts):
        model' = model + [v == 1]
        s = solve(model')
        if s.status feasible and objective(s) <= tolerance_bound:
            keep s
        if len(kept) >= MAX_SCENARIOS - 1:
            break
```

**Output-schema changes.** `validation_summary.json` gains
`"scenario_semantics": "<one of the three values above>"`. No change to
individual `scenario_NN.json` files' own schema (the classification
describes the COLLECTION, not a single scenario).

**Regression tests.** New file
`tests/salido_hdt/solver/test_scenario_semantics.py`:
- `test_unique_optimum_label_when_no_alternative_exists` -- synthetic
  model with a genuinely unique optimum (e.g. one variable forced) ->
  `scenario_semantics == "unique_optimum"`.
- `test_degenerate_tied_optimum_label_and_extra_scenario_found` --
  synthetic model with an all-idle-cheapest optimum where at least one
  other variable can also be forced to `1` at equal cost -> label
  `"degenerate_tied_optimum_partial_sample"` AND more than one scenario
  returned.
- `test_multiple_scenarios_label_unchanged_for_existing_true_variable_case`
  -- re-run of an EXISTING passing `test_multiple_scenarios.py` case,
  asserting the label is `"multiple_scenarios"` (regression guard: the new
  code path must not change behaviour for the already-working case).
- `test_real_dataset_run_reports_degenerate_label_and_more_than_one_scenario`
  -- real `cli.run(..., max_scenarios=5)`; assert
  `scenario_semantics == "degenerate_tied_optimum_partial_sample"` and
  `n_scenarios > 1` (this is the direct closing verification that the real
  dataset's previously-silent `n_scenarios: 1` gap is now both fixed and
  disclosed).

**Acceptance criterion.** All four tests above pass; a real
`cli.run(root=..., max_scenarios=5)` produces more than one
`scenario_NN.json` file (previously always exactly one) and
`validation_summary.json`'s `scenario_semantics` field is
`"degenerate_tied_optimum_partial_sample"`.

---

## Cross-cutting constraints (binding on every item above)

- No canonical dataset file is read in write mode or modified --
  unchanged from every prior patch's discipline; re-verified via
  `test_no_source_mutation.py` and a fresh SHA-256 check before and after
  implementation.
- No new objective term rewards assignment, labour, or group utilization
  -- items 1-3 are pure accounting/correctness fixes; item 4's bounded
  forcing round only ever tests EXISTING zero/near-zero-cost alternatives
  within the ALREADY-established tolerance band, it never changes what is
  minimized or adds an incentive to assign anyone.
- No aggregate group is forced into or out of any assignment by any of
  these four items.
- This is a separate commit from `1cb16df` and `93b05a4`; neither is
  amended.

## Remaining limitations (explicitly out of scope for this patch)

- **Full tied-optimum enumeration is not attempted.** Item 4's bounded
  forcing round returns a small, honestly-labeled PARTIAL sample of the
  degenerate tied-optimum set, not an exhaustive one -- the true
  equivalence class at objective value `0` on the real dataset is
  almost certainly far larger than `config.MAX_SCENARIOS` and is not
  practically enumerable without a fundamentally different search
  strategy (e.g. projected symmetry-breaking over the specific structure
  of the tied class), which is a substantially larger undertaking than an
  interpretability patch.
- **The schicht-per-equipment POLICY question is not resolved**, only the
  code defect (silently ignoring the axis) is fixed. `CONSTRAINT_SOLVER.md`
  does not state whether equipment is schicht-exclusive or schicht-shared
  in the underlying archive; this patch adopts the more conservative
  (schicht-exclusive/per-schicht) reading without archival justification
  for the alternative, because no real data currently exercises the
  choice either way.
- **`required_capacity`'s archival-floor-vs-demand-ceiling mismatch is
  documented, not resolved** -- there is no data source in
  `docs/enclave/salido_hdt_model_v0_4_1/` that states an actual
  simultaneous-worker demand estimate per task, so `capacity_status`
  continues to compare confirmed/uncertain capacity against
  `minimum_workers_assumption` for lack of any better-attested number;
  this patch only makes that comparison's limitations legible in the
  output rather than inventing a new demand estimate.
