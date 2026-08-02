from ortools.sat.python import cp_model

from salido_hdt.solver.scenario_collector import Scenario, collect_scenarios


def test_two_equally_plausible_optima_are_not_collapsed_into_one():
    """A model with two BoolVars, exactly one of which must be true, and an
    objective that scores both identically: two genuinely distinct optima
    exist. The collector must not silently return only one."""
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
    assignments = {frozenset(k for k, v in s.assignment.items() if v == 1) for s in scenarios}
    assert assignments == {frozenset({"a"}), frozenset({"b"})}
    for s in scenarios:
        assert isinstance(s, Scenario)
        assert s.objective_value == 1


def test_single_unique_optimum_returns_exactly_one_scenario():
    model = cp_model.CpModel()
    a = model.NewBoolVar("a")
    model.Add(a == 1)
    expr = 1 * a
    model.Minimize(expr)

    scenarios = collect_scenarios(model, expr, decision_vars={"a": a}, max_scenarios=5)
    assert len(scenarios) == 1
    assert scenarios[0].assignment == {"a": 1}


def test_respects_max_scenarios_cap():
    """Four mutually exclusive equally-good singleton choices, but capped
    at 2 -- must not exceed the cap even though 4 optima exist."""
    model = cp_model.CpModel()
    vars_ = {name: model.NewBoolVar(name) for name in "abcd"}
    model.Add(sum(vars_.values()) == 1)
    expr = sum(vars_.values())
    model.Minimize(expr)

    scenarios = collect_scenarios(model, expr, decision_vars=vars_, max_scenarios=2, tolerance=0.0)
    assert len(scenarios) == 2


def test_infeasible_model_returns_empty_list():
    model = cp_model.CpModel()
    a = model.NewBoolVar("a")
    model.Add(a == 1)
    model.Add(a == 0)
    expr = 1 * a

    scenarios = collect_scenarios(model, expr, decision_vars={"a": a})
    assert scenarios == []


def test_scenario_penalty_breakdown_matches_named_terms():
    """v0.1.1 F7: collect_scenarios(penalty_terms=...) must report each
    category's solved sum, independent of how the terms were weighted into
    the objective itself."""
    model = cp_model.CpModel()
    a = model.NewBoolVar("a")
    b = model.NewBoolVar("b")
    c = model.NewBoolVar("c")
    model.Add(a == 1)
    model.Add(b == 1)
    model.Add(c == 0)
    expr = 1 * a + 1 * b + 1 * c
    model.Minimize(expr)

    scenarios = collect_scenarios(
        model, expr, decision_vars={"a": a, "b": b, "c": c},
        penalty_terms={"cat_x": [a, c], "cat_y": [b]},
    )
    assert len(scenarios) == 1
    assert scenarios[0].penalty_breakdown == {"cat_x": 1, "cat_y": 1}


def test_penalty_breakdown_defaults_to_empty_when_not_provided():
    model = cp_model.CpModel()
    a = model.NewBoolVar("a")
    model.Add(a == 1)
    expr = 1 * a

    scenarios = collect_scenarios(model, expr, decision_vars={"a": a})
    assert scenarios[0].penalty_breakdown == {}


def test_tolerance_zero_excludes_strictly_worse_solutions():
    """Two options: one costs 1, the other costs 5. With tolerance=0 only
    the cost-1 optimum should be collectable -- the cost-5 alternative must
    not appear even if max_scenarios allows more solves."""
    model = cp_model.CpModel()
    a = model.NewBoolVar("a")
    b = model.NewBoolVar("b")
    model.Add(a + b == 1)
    expr = 1 * a + 5 * b
    model.Minimize(expr)

    scenarios = collect_scenarios(
        model, expr, decision_vars={"a": a, "b": b}, max_scenarios=5, tolerance=0.0,
    )
    assert len(scenarios) == 1
    assert scenarios[0].assignment == {"a": 1, "b": 0}
