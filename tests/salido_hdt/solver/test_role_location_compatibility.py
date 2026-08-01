from ortools.sat.python import cp_model

from salido_hdt.solver.hard_constraints import add_role_location_compatibility


def _solve(model):
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    return solver


def test_role_restricted_to_hard_compatible_locations():
    """R-SMIT is HARD-compatible only with L-SMITSWINCKEL (RLC-0016)."""
    model = cp_model.CpModel()
    x = {("P-SMIT", "T-SMITH", "L-SALIDO", 0, 0): model.NewBoolVar("x1")}
    person_roles = {"P-SMIT": {"R-SMIT"}}
    hard_compatible_locations = {"R-SMIT": {"L-SMITSWINCKEL"}}

    n = add_role_location_compatibility(model, x, person_roles, hard_compatible_locations)
    assert n == 1
    solver = _solve(model)
    assert solver.Value(x[("P-SMIT", "T-SMITH", "L-SALIDO", 0, 0)]) == 0


def test_role_at_its_compatible_location_left_free():
    model = cp_model.CpModel()
    var = model.NewBoolVar("x1")
    model.Add(var == 1)
    x = {("P-SMIT", "T-SMITH", "L-SMITSWINCKEL", 0, 0): var}
    person_roles = {"P-SMIT": {"R-SMIT"}}
    hard_compatible_locations = {"R-SMIT": {"L-SMITSWINCKEL"}}

    n = add_role_location_compatibility(model, x, person_roles, hard_compatible_locations)
    assert n == 0
    solver = _solve(model)
    assert solver.Value(var) == 1


def test_role_with_no_recorded_rule_is_unrestricted():
    """Absence of a rule in 15_role_location_compatibility.csv must not be
    treated as evidence of incompatibility (UNCERTAINTY_POLICY.md)."""
    model = cp_model.CpModel()
    var = model.NewBoolVar("x1")
    model.Add(var == 1)
    x = {("P-X", "T-Y", "L-ANYWHERE", 0, 0): var}
    person_roles = {"P-X": {"R-VOERMAN"}}
    hard_compatible_locations = {}  # R-VOERMAN has no HARD rule at all

    n = add_role_location_compatibility(model, x, person_roles, hard_compatible_locations)
    assert n == 0
    solver = _solve(model)
    assert solver.Value(var) == 1
