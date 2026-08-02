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


def collect_scenarios(
    model: cp_model.CpModel,
    objective_expr,
    decision_vars: dict,
    max_scenarios: int | None = None,
    tolerance: float | None = None,
    time_limit_seconds: float | None = None,
    penalty_terms: dict[str, list[cp_model.IntVar]] | None = None,
) -> list[Scenario]:
    """decision_vars: {key: BoolVar} -- the variables a no-good cut should
    diversify over (typically the x[h,j,l,s,t] presence/assignment vars).
    penalty_terms: optional {category_name: [IntVar, ...]} -- when given,
    each returned Scenario carries a penalty_breakdown with that category's
    solved sum (v0.1.1 F7; see SOLVER_V0_1_1_FIX_PLAN.md).
    Returns an empty list if the model is infeasible on the first solve."""
    max_scenarios = max_scenarios or config.MAX_SCENARIOS
    tolerance = config.SCENARIO_OBJECTIVE_TOLERANCE if tolerance is None else tolerance
    time_limit_seconds = time_limit_seconds or config.SOLVE_TIME_LIMIT_SECONDS
    penalty_terms = penalty_terms or {}

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds

    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return []

    best = int(round(solver.ObjectiveValue()))
    bound = best + int(round(abs(best) * tolerance)) + 1

    scenarios: list[Scenario] = []

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

    for idx in range(1, max_scenarios):
        true_keys = [k for k, v in decision_vars.items() if solver.Value(v) == 1]
        if not true_keys:
            # Nothing to diversify against (degenerate all-zero solution) --
            # further re-solves would just repeat it.
            break
        # No-good cut: forbid the exact same set of true assignments again.
        model.Add(sum(decision_vars[k] for k in true_keys) <= len(true_keys) - 1)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit_seconds
        status = solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break
        scenarios.append(_snapshot(idx, solver, status))

    return scenarios
