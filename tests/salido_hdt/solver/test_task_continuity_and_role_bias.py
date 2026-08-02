"""Regression guards for add_task_continuity_penalty's idle/switch fix (see
SOLVER_SCENARIO_INTERPRETATION_AUDIT.md / SOLVER_V0_1_1_FIX_PLAN.md F1).

v0.1's version mischarged idle<->idle transitions as a task switch. These
tests assert the fix removes that bias without introducing the opposite one
(idle must never be forced or preferred over a genuinely equal alternative
either).

Role-support/role-switch coverage (add_role_task_support_penalty,
add_role_switch_penalty) lives in test_role_task_support_and_switch.py.
"""
from ortools.sat.python import cp_model

from salido_hdt.solver.soft_constraints import add_task_continuity_penalty


def _solve(model, continuity):
    all_penalties = continuity.task_switch + continuity.location_switch + continuity.presence_transition
    model.Minimize(sum(all_penalties) if all_penalties else 0)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    return solver


def _total(solver, *pools):
    return sum(solver.Value(p) for pool in pools for p in pool)


def test_idle_idle_transition_costs_nothing():
    model = cp_model.CpModel()
    x = {
        ("H1", "J1", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "J2", "L1", 0, 0): model.NewBoolVar("x2"),
        ("H1", "J1", "L1", 0, 1): model.NewBoolVar("x3"),
        ("H1", "J2", "L1", 0, 1): model.NewBoolVar("x4"),
    }
    for v in x.values():
        model.Add(v == 0)
    continuity = add_task_continuity_penalty(
        model, x, ("H1",), ("J1", "J2"), 2, include_presence_transition_penalty=True
    )
    solver = _solve(model, continuity)
    assert _total(solver, continuity.task_switch) == 0
    assert _total(solver, continuity.location_switch) == 0
    assert _total(solver, continuity.presence_transition) == 0


def test_active_active_same_task_and_location_costs_nothing():
    model = cp_model.CpModel()
    x = {
        ("H1", "J1", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "J1", "L1", 0, 1): model.NewBoolVar("x2"),
    }
    model.Add(x[("H1", "J1", "L1", 0, 0)] == 1)
    model.Add(x[("H1", "J1", "L1", 0, 1)] == 1)
    continuity = add_task_continuity_penalty(
        model, x, ("H1",), ("J1",), 2, include_presence_transition_penalty=True
    )
    solver = _solve(model, continuity)
    assert _total(solver, continuity.task_switch) == 0
    assert _total(solver, continuity.location_switch) == 0
    assert _total(solver, continuity.presence_transition) == 0


def test_active_active_different_task_costs_task_switch_only():
    model = cp_model.CpModel()
    x = {
        ("H1", "J1", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "J2", "L1", 0, 0): model.NewBoolVar("x2"),
        ("H1", "J1", "L1", 0, 1): model.NewBoolVar("x3"),
        ("H1", "J2", "L1", 0, 1): model.NewBoolVar("x4"),
    }
    model.Add(x[("H1", "J1", "L1", 0, 0)] == 1)
    model.Add(x[("H1", "J2", "L1", 0, 0)] == 0)
    model.Add(x[("H1", "J1", "L1", 0, 1)] == 0)
    model.Add(x[("H1", "J2", "L1", 0, 1)] == 1)
    continuity = add_task_continuity_penalty(model, x, ("H1",), ("J1", "J2"), 2)
    solver = _solve(model, continuity)
    assert _total(solver, continuity.task_switch) == 1
    assert _total(solver, continuity.location_switch) == 0


def test_same_task_different_location_costs_location_switch_not_task_switch():
    model = cp_model.CpModel()
    x = {
        ("H1", "J1", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "J1", "L2", 0, 1): model.NewBoolVar("x2"),
    }
    model.Add(x[("H1", "J1", "L1", 0, 0)] == 1)
    model.Add(x[("H1", "J1", "L2", 0, 1)] == 1)
    continuity = add_task_continuity_penalty(model, x, ("H1",), ("J1",), 2)
    solver = _solve(model, continuity)
    assert _total(solver, continuity.task_switch) == 0
    assert _total(solver, continuity.location_switch) == 1


def test_active_idle_transition_costs_nothing_by_default_but_can_be_enabled():
    model = cp_model.CpModel()
    x = {
        ("H1", "J1", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "J1", "L1", 0, 1): model.NewBoolVar("x2"),
    }
    model.Add(x[("H1", "J1", "L1", 0, 0)] == 1)
    model.Add(x[("H1", "J1", "L1", 0, 1)] == 0)

    continuity_default = add_task_continuity_penalty(model, x, ("H1",), ("J1",), 2)
    assert continuity_default.presence_transition == []
    solver = _solve(model, continuity_default)
    assert _total(solver, continuity_default.task_switch) == 0
    assert _total(solver, continuity_default.location_switch) == 0

    model2 = cp_model.CpModel()
    x2 = {
        ("H1", "J1", "L1", 0, 0): model2.NewBoolVar("x1"),
        ("H1", "J1", "L1", 0, 1): model2.NewBoolVar("x2"),
    }
    model2.Add(x2[("H1", "J1", "L1", 0, 0)] == 1)
    model2.Add(x2[("H1", "J1", "L1", 0, 1)] == 0)
    continuity_opt_in = add_task_continuity_penalty(
        model2, x2, ("H1",), ("J1",), 2, include_presence_transition_penalty=True
    )
    solver2 = _solve(model2, continuity_opt_in)
    assert _total(solver2, continuity_opt_in.task_switch) == 0
    assert _total(solver2, continuity_opt_in.location_switch) == 0
    assert _total(solver2, continuity_opt_in.presence_transition) == 1


def test_idle_to_assigned_transition_costs_nothing_by_default_but_can_be_enabled():
    model = cp_model.CpModel()
    x = {
        ("H1", "J1", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "J1", "L1", 0, 1): model.NewBoolVar("x2"),
    }
    model.Add(x[("H1", "J1", "L1", 0, 0)] == 0)
    model.Add(x[("H1", "J1", "L1", 0, 1)] == 1)

    continuity_default = add_task_continuity_penalty(model, x, ("H1",), ("J1",), 2)
    solver = _solve(model, continuity_default)
    assert _total(solver, continuity_default.task_switch) == 0
    assert _total(solver, continuity_default.location_switch) == 0

    model2 = cp_model.CpModel()
    x2 = {
        ("H1", "J1", "L1", 0, 0): model2.NewBoolVar("x1"),
        ("H1", "J1", "L1", 0, 1): model2.NewBoolVar("x2"),
    }
    model2.Add(x2[("H1", "J1", "L1", 0, 0)] == 0)
    model2.Add(x2[("H1", "J1", "L1", 0, 1)] == 1)
    continuity_opt_in = add_task_continuity_penalty(
        model2, x2, ("H1",), ("J1",), 2, include_presence_transition_penalty=True
    )
    solver2 = _solve(model2, continuity_opt_in)
    assert _total(solver2, continuity_opt_in.presence_transition) == 1


def test_no_penalty_created_when_neither_period_has_any_variable():
    """'Do not create a penalty merely because no assignment variable is
    true' -- when there are literally no x-variables for h at either t or
    t+1, no penalty variables of any kind may be constructed."""
    model = cp_model.CpModel()
    x: dict = {}
    continuity = add_task_continuity_penalty(
        model, x, ("H1",), ("J1",), 2, include_presence_transition_penalty=True
    )
    assert continuity.task_switch == []
    assert continuity.location_switch == []
    assert continuity.presence_transition == []
