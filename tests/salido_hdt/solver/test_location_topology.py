from ortools.sat.python import cp_model

from salido_hdt.solver.hard_constraints import add_topological_feasibility


def _solve(model):
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    return solver


def test_movement_through_non_adjacent_pair_forced_to_zero():
    model = cp_model.CpModel()
    m = {("P-A", "L-SALIDO", "L-MADAGASCAR", 0): model.NewBoolVar("m1")}
    # LE clean-explicit edges (SOLVER_INPUT_READINESS.md §7/§9) do not
    # include Salido->Madagascar directly.
    hard_adjacent_pairs = {("L-SALIDO", "L-BOVEN-PAGGER"), ("L-SALIDO", "L-BENEDEN-PAGGER")}

    n = add_topological_feasibility(model, m, hard_adjacent_pairs)
    assert n == 1
    solver = _solve(model)
    assert solver.Value(m[("P-A", "L-SALIDO", "L-MADAGASCAR", 0)]) == 0


def test_movement_through_adjacent_pair_left_free():
    model = cp_model.CpModel()
    var = model.NewBoolVar("m1")
    model.Add(var == 1)
    m = {("P-A", "L-SALIDO", "L-BOVEN-PAGGER", 0): var}
    hard_adjacent_pairs = {("L-SALIDO", "L-BOVEN-PAGGER")}

    n = add_topological_feasibility(model, m, hard_adjacent_pairs)
    assert n == 0
    solver = _solve(model)
    assert solver.Value(var) == 1


def test_ambiguous_edges_must_not_be_passed_as_hard_adjacent():
    """SOLVER_INPUT_READINESS.md §7: the 12 ambiguous 16_location_adjacency
    rows (e.g. LE-0018 Princestolle<->Zuijder-Schacht, relation_type
    'topological_relation_unknown') must never appear in
    hard_adjacent_pairs. This test documents the exclusion is enforced by
    the CALLER (validation.py's classification), not re-checked here --
    passing an ambiguous pair in would incorrectly legalize it, which is
    exactly why cli.py must build hard_adjacent_pairs only from
    HARD-classified edges."""
    model = cp_model.CpModel()
    var = model.NewBoolVar("m1")
    m = {("P-A", "L-PRINCESTOLLE", "L-ZUIJDER-SCHACHT", 0): var}
    # Simulating a caller that correctly excluded the ambiguous LE-0018 pair:
    hard_adjacent_pairs: set[tuple[str, str]] = set()

    n = add_topological_feasibility(model, m, hard_adjacent_pairs)
    assert n == 1
    solver = _solve(model)
    assert solver.Value(m[("P-A", "L-PRINCESTOLLE", "L-ZUIJDER-SCHACHT", 0)]) == 0
