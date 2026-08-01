from ortools.sat.python import cp_model

from salido_hdt.solver.hard_constraints import add_equipment_capacity


def _solve_max(model, objective_vars):
    model.Maximize(sum(objective_vars))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status == cp_model.OPTIMAL
    return solver


def test_simultaneous_drilling_bounded_by_borer_capacity():
    """docs/CONSTRAINT_SOLVER.md: 'Simultaneous drilling teams cannot
    exceed available serviceable borers.' INV-0232 = 60 bor tambang."""
    model = cp_model.CpModel()
    x = {
        (f"P-{i}", "T-DRILL", "L-ORTEN", 0, 0): model.NewBoolVar(f"x{i}")
        for i in range(5)
    }
    n = add_equipment_capacity(model, x, task_id="T-DRILL", location_id="L-ORTEN", capacity=3)
    assert n == 1
    solver = _solve_max(model, list(x.values()))
    active = sum(solver.Value(v) for v in x.values())
    assert active <= 3
    assert active == 3  # maximized under the cap


def test_capacity_is_per_time_bucket_not_global():
    model = cp_model.CpModel()
    x = {
        ("P-A", "T-DRILL", "L-ORTEN", 0, 0): model.NewBoolVar("x_t0"),
        ("P-B", "T-DRILL", "L-ORTEN", 0, 0): model.NewBoolVar("x_t0b"),
        ("P-A", "T-DRILL", "L-ORTEN", 0, 1): model.NewBoolVar("x_t1"),
        ("P-B", "T-DRILL", "L-ORTEN", 0, 1): model.NewBoolVar("x_t1b"),
    }
    n = add_equipment_capacity(model, x, task_id="T-DRILL", location_id="L-ORTEN", capacity=1)
    assert n == 2  # two distinct time buckets
    solver = _solve_max(model, list(x.values()))
    total_active = sum(solver.Value(v) for v in x.values())
    assert total_active == 2  # one per bucket, not one total


def test_unrelated_task_or_location_untouched():
    model = cp_model.CpModel()
    var = model.NewBoolVar("x1")
    model.Add(var == 1)
    x = {("P-A", "T-WASH", "L-SCHEIJDEBANCK", 0, 0): var}
    n = add_equipment_capacity(model, x, task_id="T-DRILL", location_id="L-ORTEN", capacity=1)
    assert n == 0
    solver = cp_model.CpSolver()
    solver.Solve(model)
    assert solver.Value(var) == 1


def test_widened_bound_for_unresolved_reading_documented_by_caller():
    """SOLVER_INPUT_READINESS.md §9: INV-0232's reading_status=unresolved
    means the caller must pass a WIDENED bound, not the raw '60'. This test
    documents/asserts the widening is the CALLER's responsibility -- the
    function itself just enforces whatever capacity it is given."""
    model = cp_model.CpModel()
    raw_reading = 60
    widened_capacity = int(raw_reading * 1.2)  # example widening factor
    # more candidate workers than the widened capacity, so the cap actually binds
    x = {
        (f"P-{i}", "T-DRILL", "L-ORTEN", 0, 0): model.NewBoolVar(f"x{i}")
        for i in range(widened_capacity + 10)
    }
    add_equipment_capacity(model, x, task_id="T-DRILL", location_id="L-ORTEN", capacity=widened_capacity)
    solver = _solve_max(model, list(x.values()))
    active = sum(solver.Value(v) for v in x.values())
    assert active == widened_capacity
    assert active != raw_reading
