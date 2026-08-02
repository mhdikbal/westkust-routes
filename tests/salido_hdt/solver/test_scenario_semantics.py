"""Regression guards for v0.1.2 Item 4 (SOLVER_V0_1_2_FIX_PLAN.md):
scenario_semantics classification and bounded degenerate diversification.
"""
from ortools.sat.python import cp_model

from salido_hdt.solver import config
from salido_hdt.solver.cli import run
from salido_hdt.solver.scenario_collector import ScenarioCollection, collect_scenarios


def test_unique_optimum_label_when_no_alternative_exists():
    model = cp_model.CpModel()
    a = model.NewBoolVar("a")
    model.Add(a == 1)
    expr = 1 * a

    scenarios = collect_scenarios(model, expr, decision_vars={"a": a}, max_scenarios=5)
    assert isinstance(scenarios, ScenarioCollection)
    assert scenarios.scenario_semantics == "unique_optimum"
    assert len(scenarios) == 1


def test_infeasible_model_labeled_infeasible():
    model = cp_model.CpModel()
    a = model.NewBoolVar("a")
    model.Add(a == 1)
    model.Add(a == 0)
    expr = 1 * a

    scenarios = collect_scenarios(model, expr, decision_vars={"a": a})
    assert scenarios == []
    assert scenarios.scenario_semantics == "infeasible"


def test_degenerate_tied_optimum_label_and_extra_scenario_found():
    """All-idle-cheapest optimum where forcing a different variable to 1
    remains feasible at equal cost (0) -- must find it and label the
    collection as a degenerate partial sample, not silently stop at 1."""
    model = cp_model.CpModel()
    a = model.NewBoolVar("a")
    b = model.NewBoolVar("b")
    # No constraint links a/b -- both free, objective only counts a (b is
    # free real-value with zero cost either way), so the pure optimum is
    # a=0 (cost 0), with b=0 or b=1 both equally valid/free.
    expr = 1 * a
    model.Minimize(expr)

    scenarios = collect_scenarios(
        model, expr, decision_vars={"a": a, "b": b}, max_scenarios=3, tolerance=0.0,
    )
    assert scenarios.scenario_semantics == "degenerate_tied_optimum_partial_sample"
    assert len(scenarios) > 1
    assert scenarios[0].assignment == {"a": 0, "b": 0}
    # the forced-alternative scenario must show a genuinely different assignment
    assert any(s.assignment != scenarios[0].assignment for s in scenarios[1:])


def test_multiple_scenarios_label_unchanged_for_existing_true_variable_case():
    """Regression guard: the pre-existing, already-working no-good-cut
    path (a genuine tied optimum WITH true variables) must still be
    labeled 'multiple_scenarios', unchanged by the new degenerate branch."""
    model = cp_model.CpModel()
    a = model.NewBoolVar("a")
    b = model.NewBoolVar("b")
    model.Add(a + b == 1)
    expr = 1 * a + 1 * b
    model.Minimize(expr)

    scenarios = collect_scenarios(
        model, expr, decision_vars={"a": a, "b": b}, max_scenarios=5, tolerance=0.0,
    )
    assert len(scenarios) == 2
    assert scenarios.scenario_semantics == "multiple_scenarios"


def test_degenerate_round_respects_max_scenarios_budget():
    model = cp_model.CpModel()
    vars_ = {name: model.NewBoolVar(name) for name in "abcd"}
    expr = sum(vars_.values())
    model.Minimize(expr)  # optimum: all zero, every single var forceable to 1 at equal marginal cost within tolerance

    scenarios = collect_scenarios(
        model, expr, decision_vars=vars_, max_scenarios=3, tolerance=1.0,
    )
    assert len(scenarios) <= 3


# --- real dataset -----------------------------------------------------------


def test_real_dataset_run_reports_degenerate_label_and_more_than_one_scenario(tmp_path):
    """Direct closing verification: the real dataset's previously-silent
    n_scenarios=1 gap (verified during this patch's planning) is now both
    fixed (more than one scenario found) and disclosed (scenario_semantics
    field present and correctly labeled)."""
    import json

    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=5)
    summary = json.loads((output_dir / "validation_summary.json").read_text(encoding="utf-8"))

    assert summary["scenario_semantics"] == "degenerate_tied_optimum_partial_sample"
    assert summary["n_scenarios"] > 1
    scenario_files = sorted(output_dir.glob("scenario_*.json"))
    assert len(scenario_files) == summary["n_scenarios"]
