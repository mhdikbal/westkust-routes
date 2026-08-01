from ortools.sat.python import cp_model

from salido_hdt.solver.hard_constraints import add_role_task_compatibility


def _solve(model):
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    return solver


def test_incompatible_role_forced_to_zero():
    """P-A only holds R-BERGWERKER; task T-ASSAY needs R-ASSAIJEUR."""
    model = cp_model.CpModel()
    x = {("P-A", "T-ASSAY", "L-ASSAY-LAB", 0, 0): model.NewBoolVar("x1")}
    person_roles = {"P-A": {"R-BERGWERKER"}}
    task_preferred_roles = {"T-ASSAY": {"R-ASSAIJEUR"}}

    n = add_role_task_compatibility(model, x, person_roles, task_preferred_roles)
    assert n == 1
    solver = _solve(model)
    assert solver.Value(x[("P-A", "T-ASSAY", "L-ASSAY-LAB", 0, 0)]) == 0


def test_compatible_role_left_free():
    model = cp_model.CpModel()
    var = model.NewBoolVar("x1")
    model.Add(var == 1)
    x = {("P-VOGEL", "T-ASSAY", "L-ASSAY-LAB", 0, 0): var}
    person_roles = {"P-VOGEL": {"R-ASSAIJEUR"}}
    task_preferred_roles = {"T-ASSAY": {"R-ASSAIJEUR"}}

    n = add_role_task_compatibility(model, x, person_roles, task_preferred_roles)
    assert n == 0
    solver = _solve(model)
    assert solver.Value(var) == 1


def test_task_with_no_declared_role_preference_is_unrestricted():
    """Absence of a requirement must not become a requirement."""
    model = cp_model.CpModel()
    var = model.NewBoolVar("x1")
    model.Add(var == 1)
    x = {("P-A", "T-WASH", "L-SCHEIJDEBANCK", 0, 0): var}
    person_roles = {"P-A": {"R-BERGWERKER"}}
    task_preferred_roles = {}  # T-WASH has constraint_strength=soft, no roles

    n = add_role_task_compatibility(model, x, person_roles, task_preferred_roles)
    assert n == 0
    solver = _solve(model)
    assert solver.Value(var) == 1


def test_aggregate_group_with_unknown_roles_is_unrestricted():
    """Groups are absent from person_roles (04 covers named individuals
    only) -- role-task compatibility does not restrict them here."""
    model = cp_model.CpModel()
    var = model.NewBoolVar("x1")
    model.Add(var == 1)
    x = {("G-MANDOOR-8", "T-ASSAY", "L-ASSAY-LAB", 0, 0): var}
    person_roles = {}  # group not present
    task_preferred_roles = {"T-ASSAY": {"R-ASSAIJEUR"}}

    n = add_role_task_compatibility(model, x, person_roles, task_preferred_roles)
    assert n == 0
    solver = _solve(model)
    assert solver.Value(var) == 1
