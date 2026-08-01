"""Plan decision #5 / ETHICAL_MODELING.md: aggregate groups (coerced-labour
headcounts, e.g. G-SLAVIN-68) may be ASSIGNED (present/absent per the HRLT
tensor) but must never be SCORED for productivity by group size. This is
asserted by construction here, not by convention: by inspecting the actual
variable set built from the real dataset, and by inspecting objective.py's
and soft_constraints.py's source for any reference to HumanGroup.count.
"""
import inspect
import re
from pathlib import Path

from salido_hdt.solver import config, hard_constraints, objective, soft_constraints
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.domain import EntityType
from salido_hdt.solver.variables import build_variables


def _dataset():
    return load_dataset(config.V0_4_1_ROOT)


def test_dataset_contains_at_least_one_aggregate_group():
    dataset = _dataset()
    group_hrlt = [
        h for h in dataset.hrlt_records.values()
        if h.entity_type == EntityType.AGGREGATE_GROUP
    ]
    assert group_hrlt, "expected at least one aggregate_group HRLT record in v0.4.1"


def test_aggregate_group_gets_exactly_one_boolvar_per_j_l_s_t_not_scaled_by_count():
    """An aggregate group's x variables must have the identical shape as an
    individual's: one BoolVar per (task, location, schicht, time) tuple it
    is attested present at -- never `count` variables, never a variable
    whose name or count depends on HumanGroup.count."""
    dataset = _dataset()
    solver_vars = build_variables(dataset)

    group_ids = {
        h.human_or_group_id
        for h in dataset.hrlt_records.values()
        if h.entity_type == EntityType.AGGREGATE_GROUP
    }
    group_entities_with_vars = group_ids & set(solver_vars.entities)
    assert group_entities_with_vars, "no aggregate group survived hard-eligible pruning to check"

    for h in group_entities_with_vars:
        attested = solver_vars.presence.get(h, set())
        expected_keys = {
            (h, j, l, s, t)
            for j in dataset.task_requirements
            for (l, t_from, t_to) in attested
            for s in range(solver_vars.schicht_count)
            for t in range(t_from, t_to + 1)
        }
        actual_keys = {k for k in solver_vars.x if k[0] == h}
        assert actual_keys == expected_keys
        # Exactly one BoolVar per key -- no per-member fan-out.
        assert len(actual_keys) == len(expected_keys)


def _function_bodies(module):
    """Source of every top-level function in module, docstring stripped --
    so explanatory prose ABOUT the guard (e.g. this module's own comments
    naming 'HumanGroup.count') can't trip a check meant for executable code."""
    for _, fn in inspect.getmembers(module, inspect.isfunction):
        if fn.__module__ != module.__name__:
            continue
        src = inspect.getsource(fn)
        doc = inspect.getdoc(fn) or ""
        if doc:
            src = src.replace(doc, "")
        yield fn.__name__, src


def test_no_solver_module_references_human_group_count():
    """Static guard: grep the executable body (not docstrings/comments) of
    every constraint/objective function for a HumanGroup.count reference. A
    future edit that tries to weight an aggregate group's penalty/objective
    contribution by its headcount must fail this test."""
    modules = [hard_constraints, soft_constraints, objective]
    pattern = re.compile(r"\.count\b|human_groups\[.*?\]\.count|group\.count")
    for module in modules:
        for name, body in _function_bodies(module):
            body = "\n".join(
                line for line in body.splitlines() if not line.strip().startswith("#")
            )
            assert not pattern.search(body), (
                f"{module.__name__}.{name} references a group-size/count-weighted "
                "term, violating the ethical guard (plan decision #5)"
            )


def test_variables_module_does_not_reference_human_group_count():
    from salido_hdt.solver import variables

    pattern = re.compile(r"\.count\b|human_groups\[.*?\]\.count|group\.count")
    for name, body in _function_bodies(variables):
        body = "\n".join(
            line for line in body.splitlines() if not line.strip().startswith("#")
        )
        assert not pattern.search(body), (
            f"variables.{name} must never branch on HumanGroup.count when "
            "building x/y/m/q/z"
        )


def test_objective_signature_has_no_group_or_count_parameter():
    sig = inspect.signature(objective.build_objective)
    for name in sig.parameters:
        assert "group" not in name.lower()
        assert "count" not in name.lower()
