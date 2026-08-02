"""Multi-scenario collection per docs/CONSTRAINT_SOLVER.md: "return all
optimal or near-optimal scenarios ... do not collapse equally plausible
histories into one answer."

Solves once for the best objective value, then repeatedly re-solves with
(a) an objective bound requiring the new solution stay within `tolerance`
of the best found so far, and (b) a "no-good" cut excluding every exact
combination of true decision variables seen in a previous scenario -- so
each additional scenario is a genuinely different assignment, not the
solver re-finding the same optimum.

`objective_expr` MUST already have purely integer coefficients (see
objective.py's int() casts) -- CP-SAT's model.Add() rejects float
coefficients even though model.Minimize() accepts them, so the bounding
constraint built here would raise on a float expression.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ortools.sat.python import cp_model

from salido_hdt.solver import config


@dataclass(frozen=True)
class Scenario:
    index: int
    status: str
    objective_value: int
    assignment: dict = field(default_factory=dict)
    #: v0.1.1 F7: {category_name: solved sum of that category's raw,
    #: unweighted penalty variables}. Diagnostic only -- never affects what
    #: is minimized, only what is reported. Empty when collect_scenarios()
    #: is called without `penalty_terms` (backward compatible).
    penalty_breakdown: dict = field(default_factory=dict)


#: v0.1.2 fix (SOLVER_V0_1_2_FIX_PLAN.md Item 4): classifies the WHOLE
#: collection, not any single scenario. One of:
#:   "unique_optimum" -- proven no other tied/near-tied solution exists
#:     (the tolerance-bounded re-solve, or every degenerate forcing
#:     attempt, was infeasible).
#:   "degenerate_tied_optimum_partial_sample" -- the optimal solution had
#:     no true decision variables to build a no-good cut from (e.g. an
#:     all-idle optimum), but at least one alternative was found via
#:     bounded forcing; almost certainly more tied solutions exist beyond
#:     this small sample.
#:   "multiple_scenarios" -- the standard no-good-cut loop found more than
#:     one distinct scenario via true-variable exclusion.
class ScenarioCollection(list):
    """A list[Scenario] carrying an additional `scenario_semantics`
    classification for the collection as a whole. Subclasses list (not a
    wrapper dataclass) so every existing caller that does `len(...)`,
    `[...]`, or `for s in ...` keeps working unchanged."""

    scenario_semantics: str = "unique_optimum"


def collect_scenarios(
    model: cp_model.CpModel,
    objective_expr,
    decision_vars: dict,
    max_scenarios: int | None = None,
    tolerance: float | None = None,
    time_limit_seconds: float | None = None,
    penalty_terms: dict[str, list[cp_model.IntVar]] | None = None,
) -> ScenarioCollection:
    """decision_vars: {key: BoolVar} -- the variables a no-good cut should
    diversify over (typically the x[h,j,l,s,t] presence/assignment vars).
    penalty_terms: optional {category_name: [IntVar, ...]} -- when given,
    each returned Scenario carries a penalty_breakdown with that category's
    solved sum (v0.1.1 F7; see SOLVER_V0_1_1_FIX_PLAN.md).
    Returns an empty ScenarioCollection if the model is infeasible on the
    first solve. See ScenarioCollection.scenario_semantics (v0.1.2 Item 4,
    SOLVER_V0_1_2_FIX_PLAN.md) for the collection-level classification."""
    max_scenarios = max_scenarios or config.MAX_SCENARIOS
    tolerance = config.SCENARIO_OBJECTIVE_TOLERANCE if tolerance is None else tolerance
    time_limit_seconds = time_limit_seconds or config.SOLVE_TIME_LIMIT_SECONDS
    penalty_terms = penalty_terms or {}

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds

    status = solver.Solve(model)
    scenarios = ScenarioCollection()
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        scenarios.scenario_semantics = "infeasible"
        return scenarios

    best = int(round(solver.ObjectiveValue()))
    bound = best + int(round(abs(best) * tolerance)) + 1

    def _snapshot(idx: int, sv: cp_model.CpSolver, st) -> Scenario:
        return Scenario(
            index=idx,
            status=sv.StatusName(st),
            objective_value=int(round(sv.ObjectiveValue())),
            assignment={k: sv.Value(v) for k, v in decision_vars.items()},
            penalty_breakdown={
                name: sum(sv.Value(v) for v in terms)
                for name, terms in penalty_terms.items()
            },
        )

    scenarios.append(_snapshot(0, solver, status))
    model.Add(objective_expr <= bound)

    first_true_keys = [k for k, v in decision_vars.items() if solver.Value(v) == 1]

    if first_true_keys:
        # Standard path: diversify by excluding the exact combination of
        # true variables seen in each previously-found scenario.
        for idx in range(1, max_scenarios):
            true_keys = [k for k, v in decision_vars.items() if solver.Value(v) == 1]
            if not true_keys:
                break
            model.Add(sum(decision_vars[k] for k in true_keys) <= len(true_keys) - 1)

            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = time_limit_seconds
            status = solver.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                break
            scenarios.append(_snapshot(idx, solver, status))
        scenarios.scenario_semantics = "multiple_scenarios" if len(scenarios) > 1 else "unique_optimum"
    else:
        # Degenerate path (SOLVER_V0_1_2_FIX_PLAN.md Item 4): the optimal
        # solution has no true variable to build a no-good cut from (e.g.
        # an all-idle optimum). Rather than silently stopping at 1
        # scenario, attempt a bounded round of forcing individual,
        # not-yet-tried decision variables to 1 via CP-SAT assumptions
        # (AddAssumptions/ClearAssumptions -- tests a hypothesis for one
        # solve without permanently modifying the model), keeping any that
        # remain feasible within the existing tolerance bound. This is an
        # honestly-labeled PARTIAL sample, not exhaustive enumeration --
        # see the fix plan's "Remaining limitations".
        tried_keys: set = set()
        for idx in range(1, max_scenarios):
            candidate_key = next((k for k in decision_vars if k not in tried_keys), None)
            if candidate_key is None:
                break
            tried_keys.add(candidate_key)

            model.AddAssumptions([decision_vars[candidate_key]])
            probe_solver = cp_model.CpSolver()
            probe_solver.parameters.max_time_in_seconds = time_limit_seconds
            probe_status = probe_solver.Solve(model)
            model.ClearAssumptions()

            if probe_status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                scenarios.append(_snapshot(idx, probe_solver, probe_status))
        scenarios.scenario_semantics = (
            "degenerate_tied_optimum_partial_sample" if len(scenarios) > 1 else "unique_optimum"
        )

    return scenarios
