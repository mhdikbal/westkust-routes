from ortools.sat.python import cp_model

from salido_hdt.solver.hard_constraints import (
    add_health_exclusion,
    add_one_location_per_schicht,
    add_temporal_presence,
)


def _solve(model):
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    return solver


def test_assignment_outside_presence_window_forced_to_zero():
    model = cp_model.CpModel()
    x = {
        ("P-A", "T-DIG", "L-SALIDO", 0, 5): model.NewBoolVar("x1"),
    }
    presence = {"P-A": {("L-SALIDO", 0, 3)}}  # attested only weeks 0..3

    n = add_temporal_presence(model, x, presence)
    assert n == 1
    solver = _solve(model)
    assert solver.Value(x[("P-A", "T-DIG", "L-SALIDO", 0, 5)]) == 0


def test_assignment_inside_presence_window_left_free():
    model = cp_model.CpModel()
    var = model.NewBoolVar("x1")
    model.Add(var == 1)  # force it True to prove add_temporal_presence didn't zero it
    x = {("P-A", "T-DIG", "L-SALIDO", 0, 2): var}
    presence = {"P-A": {("L-SALIDO", 0, 3)}}

    n = add_temporal_presence(model, x, presence)
    assert n == 0
    solver = _solve(model)
    assert solver.Value(var) == 1


def test_wrong_location_forced_to_zero_even_if_time_matches():
    model = cp_model.CpModel()
    x = {("P-A", "T-DIG", "L-OTHER", 0, 1): model.NewBoolVar("x1")}
    presence = {"P-A": {("L-SALIDO", 0, 3)}}

    add_temporal_presence(model, x, presence)
    solver = _solve(model)
    assert solver.Value(x[("P-A", "T-DIG", "L-OTHER", 0, 1)]) == 0


def test_entity_with_no_presence_record_fully_excluded():
    model = cp_model.CpModel()
    x = {("P-UNKNOWN", "T-DIG", "L-SALIDO", 0, 1): model.NewBoolVar("x1")}
    n = add_temporal_presence(model, x, presence={})
    assert n == 1
    solver = _solve(model)
    assert solver.Value(x[("P-UNKNOWN", "T-DIG", "L-SALIDO", 0, 1)]) == 0


# --- one_location_per_schicht -------------------------------------------


def test_one_location_per_schicht_forbids_two_simultaneous_locations():
    model = cp_model.CpModel()
    x = {
        ("P-A", "T-DIG", "L-SALIDO", 0, 0): model.NewBoolVar("x1"),
        ("P-A", "T-DIG", "L-BOVEN-PAGGER", 0, 0): model.NewBoolVar("x2"),
    }
    n = add_one_location_per_schicht(model, x)
    assert n == 1  # one (h,s,t) group
    model.Maximize(sum(x.values()))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status == cp_model.OPTIMAL
    assert sum(solver.Value(v) for v in x.values()) == 1


def test_one_location_per_schicht_different_time_buckets_are_independent():
    model = cp_model.CpModel()
    x = {
        ("P-A", "T-DIG", "L-SALIDO", 0, 0): model.NewBoolVar("x1"),
        ("P-A", "T-DIG", "L-BOVEN-PAGGER", 0, 1): model.NewBoolVar("x2"),
    }
    add_one_location_per_schicht(model, x)
    model.Maximize(sum(x.values()))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status == cp_model.OPTIMAL
    assert sum(solver.Value(v) for v in x.values()) == 2  # different t -> both allowed


# --- health_exclusion (documented no-op on v0.4.1, machinery still tested) --


def test_health_exclusion_blocks_assignment_after_release_time():
    model = cp_model.CpModel()
    x = {
        ("P-A", "T-DIG", "L-SALIDO", 0, 3): model.NewBoolVar("x1"),
        ("P-A", "T-DIG", "L-SALIDO", 0, 1): model.NewBoolVar("x2"),
    }
    released_ill = {("P-A", 2)}  # released at time bucket 2
    n = add_health_exclusion(model, x, released_ill)
    assert n == 1  # only the t=3 assignment (after release) is constrained
    solver = _solve(model)
    assert solver.Value(x[("P-A", "T-DIG", "L-SALIDO", 0, 3)]) == 0


def test_health_exclusion_is_a_documented_noop_with_empty_input():
    """v0.4.1 has no health-state column anywhere -- the real caller passes
    an empty released_ill set, so this must add zero constraints, not
    fabricate any."""
    model = cp_model.CpModel()
    var = model.NewBoolVar("x1")
    model.Add(var == 1)
    x = {("P-A", "T-DIG", "L-SALIDO", 0, 0): var}
    n = add_health_exclusion(model, x, released_ill=set())
    assert n == 0
    solver = _solve(model)
    assert solver.Value(var) == 1
