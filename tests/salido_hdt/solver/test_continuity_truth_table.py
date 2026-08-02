"""Isolated truth-table test for add_task_continuity_penalty, per the exact
transition rules specified for the fix (see SOLVER_V0_1_1_FIX_PLAN.md /
SOLVER_SCENARIO_INTERPRETATION_AUDIT.md F1-followup):

    idle -> idle                         : no penalty
    (task, loc) -> same (task, loc)      : no penalty
    assigned -> idle                     : optional presence_transition only
    idle -> assigned                     : optional presence_transition only
    task A -> different task B           : task_switch penalty
    task A -> task A, different location : location_switch penalty, NEVER
                                            task_switch

Every row uses the same three candidate (task, location) slots per period
-- (J1, L1), (J2, L1), (J1, L2) -- with exactly zero or one forced to 1 at
t=0 and t=1 (all others forced to 0), so each row is a genuinely isolated,
minimal reproduction rather than a re-used shared fixture.
"""
import pytest
from ortools.sat.python import cp_model

from salido_hdt.solver.soft_constraints import add_task_continuity_penalty

_SLOTS = [("J1", "L1"), ("J2", "L1"), ("J1", "L2")]

TRUTH_TABLE = [
    pytest.param(None, None, 0, 0, 0, id="idle_to_idle"),
    pytest.param(("J1", "L1"), ("J1", "L1"), 0, 0, 0, id="same_task_same_location"),
    pytest.param(("J1", "L1"), None, 0, 0, 1, id="assigned_to_idle"),
    pytest.param(None, ("J1", "L1"), 0, 0, 1, id="idle_to_assigned"),
    pytest.param(("J1", "L1"), ("J2", "L1"), 1, 0, 0, id="task_switch_same_location"),
    pytest.param(("J1", "L1"), ("J1", "L2"), 0, 1, 0, id="same_task_location_switch"),
]


@pytest.mark.parametrize(
    "slot_t0, slot_t1, expected_task_switch, expected_location_switch, expected_presence_transition",
    TRUTH_TABLE,
)
def test_continuity_truth_table(
    slot_t0, slot_t1, expected_task_switch, expected_location_switch, expected_presence_transition
):
    model = cp_model.CpModel()
    x = {}
    for (j, l) in _SLOTS:
        var0 = model.NewBoolVar(f"x_{j}_{l}_t0")
        model.Add(var0 == (1 if (j, l) == slot_t0 else 0))
        x[("H1", j, l, 0, 0)] = var0

        var1 = model.NewBoolVar(f"x_{j}_{l}_t1")
        model.Add(var1 == (1 if (j, l) == slot_t1 else 0))
        x[("H1", j, l, 0, 1)] = var1

    continuity = add_task_continuity_penalty(
        model, x, ("H1",), ("J1", "J2"), 2, include_presence_transition_penalty=True
    )

    solver = cp_model.CpSolver()
    # No objective needed: every candidate penalty var's value is pinned by
    # the lower-bound constraints plus the forced x-values above, regardless
    # of solve direction. Solve as a plain feasibility problem.
    status = solver.Solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)

    task_switch_total = sum(solver.Value(v) for v in continuity.task_switch)
    location_switch_total = sum(solver.Value(v) for v in continuity.location_switch)
    presence_transition_total = sum(solver.Value(v) for v in continuity.presence_transition)

    assert task_switch_total == expected_task_switch
    assert location_switch_total == expected_location_switch
    assert presence_transition_total == expected_presence_transition


def test_truth_table_covers_all_six_required_transitions():
    """Guard against silently dropping a row from the table above."""
    ids = {p.id for p in TRUTH_TABLE}
    assert ids == {
        "idle_to_idle",
        "same_task_same_location",
        "assigned_to_idle",
        "idle_to_assigned",
        "task_switch_same_location",
        "same_task_location_switch",
    }
