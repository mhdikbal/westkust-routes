"""Regression guards for the add_unsupported_role_switching_penalty fix.

The old function conflated two different claims under one misleading name:
it never compared across time (despite being named "switching"), and it
penalized single-assignment role-documentation gaps using naive presence-
in-04_person_roles.csv as the sole signal -- which is why v0.1.1 had to
blanket-exempt every aggregate group (absence from a table that
structurally never has group rows is not evidence about the group).

This revision splits the concern into two functions and five distinguished
cases, per the request that authored this file:

  1. named person, explicit documented role            -> SUPPORTED
  2. named person, no documented role                   -> UNDOCUMENTED
  3. aggregate group, plain source category (no match)   -> UNDOCUMENTED
  4. aggregate group, explicit supervisory function match -> SUPPORTED
  5. entity genuinely contradicting a required role       -> CONTRADICTED

add_role_task_support_penalty(): single-assignment classification of cases
1-5 (except case 5's temporal form).
add_role_switch_penalty(): the real, ACROSS-TIME "role switching" concept
-- penalizes only when an entity's assignment sequence implies two
genuinely incompatible roles, independent of whether the entity's own
identity is documented at all (so it cannot reintroduce the old aggregate-
group bias -- it never looks at person_roles/group identity).
"""
from ortools.sat.python import cp_model

from salido_hdt.solver import config
from salido_hdt.solver.cli import _group_declared_roles
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.soft_constraints import (
    add_role_switch_penalty,
    add_role_task_support_penalty,
)


# --- add_role_task_support_penalty: the five cases -------------------------


def test_case1_named_person_explicit_role_is_supported_no_penalty():
    x = {("P-KNOWN", "T-ASSAY", "L1", 0, 0): cp_model.CpModel().NewBoolVar("x")}
    result = add_role_task_support_penalty(
        x,
        task_preferred_roles={"T-ASSAY": {"R-ASSAIJEUR"}},
        person_roles={"P-KNOWN": {"R-ASSAIJEUR"}},
    )
    assert result.undocumented == []
    assert result.contradicted == []


def test_case2_named_person_no_documented_role_is_undocumented():
    x = {("P-UNKNOWN", "T-ASSAY", "L1", 0, 0): cp_model.CpModel().NewBoolVar("x")}
    result = add_role_task_support_penalty(
        x,
        task_preferred_roles={"T-ASSAY": {"R-ASSAIJEUR"}},
        person_roles={},  # P-UNKNOWN absent -- must not itself imply contradiction
    )
    assert len(result.undocumented) == 1
    assert result.contradicted == []


def test_case3_aggregate_group_plain_category_is_undocumented_not_exempted():
    """A group absent from BOTH person_roles and group_declared_roles must
    receive the SAME treatment as an undocumented named individual -- not a
    blanket exemption (the old, over-corrected v0.1.1 behaviour) and not a
    harsher penalty either."""
    x = {("G-PLAIN", "T-ASSAY", "L1", 0, 0): cp_model.CpModel().NewBoolVar("x")}
    result = add_role_task_support_penalty(
        x,
        task_preferred_roles={"T-ASSAY": {"R-ASSAIJEUR"}},
        person_roles={},  # groups never appear here, by schema
        group_declared_roles={},  # this group's category has no role match
    )
    assert len(result.undocumented) == 1
    assert result.contradicted == []


def test_case4_aggregate_group_supervisory_function_is_supported_no_penalty():
    """A group whose OWN category label names the required role (e.g. the
    real G-MANDOOR-8 -> R-MANDOOR match) must be treated as SUPPORTED, not
    undocumented and not automatically-compatible-because-it's-a-group --
    the support comes from the specific role match, verified below to be
    exactly as narrow as the real data supports."""
    x = {("G-MANDOOR-8", "T-SUPERVISE", "L1", 0, 0): cp_model.CpModel().NewBoolVar("x")}
    result = add_role_task_support_penalty(
        x,
        task_preferred_roles={"T-SUPERVISE": {"R-MANDOOR", "R-MANDORESS", "R-VOORSLAGER"}},
        person_roles={},
        group_declared_roles={"G-MANDOOR-8": {"R-MANDOOR"}},
    )
    assert result.undocumented == []
    assert result.contradicted == []


def test_case5_entity_with_declared_role_contradicting_task_is_contradicted():
    """An entity WITH a positively declared role that does not match the
    task's requirement is a stronger, distinct claim from 'undocumented' --
    kept in its own pool."""
    x = {("P-SMITH", "T-ASSAY", "L1", 0, 0): cp_model.CpModel().NewBoolVar("x")}
    result = add_role_task_support_penalty(
        x,
        task_preferred_roles={"T-ASSAY": {"R-ASSAIJEUR"}},
        person_roles={"P-SMITH": {"R-SMIT"}},  # documented, but not R-ASSAIJEUR
    )
    assert result.undocumented == []
    assert len(result.contradicted) == 1


def test_case5_aggregate_group_with_mismatched_declared_function_is_contradicted():
    """Symmetric case-5 check for a group: G-MANDOOR-8's own declared
    function (R-MANDOOR) does not intersect an unrelated task's
    requirement -- contradicted, not merely undocumented, and NOT silently
    treated as compatible because it's a group."""
    x = {("G-MANDOOR-8", "T-ASSAY", "L1", 0, 0): cp_model.CpModel().NewBoolVar("x")}
    result = add_role_task_support_penalty(
        x,
        task_preferred_roles={"T-ASSAY": {"R-ASSAIJEUR"}},
        person_roles={},
        group_declared_roles={"G-MANDOOR-8": {"R-MANDOOR"}},
    )
    assert result.undocumented == []
    assert len(result.contradicted) == 1


def test_task_with_no_declared_role_requirement_is_never_penalized():
    x = {("P-ANYONE", "T-NO-ROLE", "L1", 0, 0): cp_model.CpModel().NewBoolVar("x")}
    result = add_role_task_support_penalty(
        x, task_preferred_roles={}, person_roles={},
    )
    assert result.undocumented == []
    assert result.contradicted == []


def test_absence_from_person_roles_is_not_treated_as_negative_evidence():
    """Structural guard: an entity absent from person_roles must be
    UNDOCUMENTED, never CONTRADICTED -- absence is not itself a claim of
    incompatibility."""
    x = {("P-GHOST", "T-ASSAY", "L1", 0, 0): cp_model.CpModel().NewBoolVar("x")}
    result = add_role_task_support_penalty(
        x, task_preferred_roles={"T-ASSAY": {"R-ASSAIJEUR"}}, person_roles={},
    )
    assert len(result.undocumented) == 1
    assert result.contradicted == []


# --- _group_declared_roles: verified against the real dataset --------------


def test_group_declared_roles_matches_only_the_three_real_supervisory_groups():
    """Verified textual match, not invented: exactly G-MANDOOR-8,
    G-MANDORESS-3, G-VOORSLAGER-1 match a role_original; every other of the
    17 real groups (e.g. G-MS-121's purely demographic 'volwassen
    mansslaven') has no match and must not be assigned one."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    declared = _group_declared_roles(dataset)

    assert declared.get("G-MANDOOR-8") == {"R-MANDOOR"}
    assert declared.get("G-MANDORESS-3") == {"R-MANDORESS"}
    assert declared.get("G-VOORSLAGER-1") == {"R-VOORSLAGER"}
    assert "G-MS-121" not in declared
    assert "G-SLAVIN-68" not in declared
    assert len(declared) == 3


def test_group_declared_roles_never_expands_to_individual_entries():
    """Structural guard: the returned mapping is keyed by group_id (never
    by a synthesized per-member individual id) -- group-level evidence
    stays group-level."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    declared = _group_declared_roles(dataset)
    real_group_ids = {g.group_id for g in dataset.human_groups.values()}
    assert set(declared) <= real_group_ids


# --- add_role_switch_penalty: the real, across-time mechanism --------------


def test_role_switch_idle_idle_costs_nothing():
    model = cp_model.CpModel()
    x = {
        ("H1", "T-A", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "T-B", "L1", 0, 1): model.NewBoolVar("x2"),
    }
    model.Add(x[("H1", "T-A", "L1", 0, 0)] == 0)
    model.Add(x[("H1", "T-B", "L1", 0, 1)] == 0)
    penalties = add_role_switch_penalty(
        model, x, ("H1",), {"T-A": {"R-X"}, "T-B": {"R-Y"}}, 2
    )
    solver = cp_model.CpSolver()
    solver.Solve(model)
    assert sum(solver.Value(p) for p in penalties) == 0


def test_role_switch_same_task_costs_nothing():
    model = cp_model.CpModel()
    x = {
        ("H1", "T-A", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "T-A", "L1", 0, 1): model.NewBoolVar("x2"),
    }
    model.Add(x[("H1", "T-A", "L1", 0, 0)] == 1)
    model.Add(x[("H1", "T-A", "L1", 0, 1)] == 1)
    penalties = add_role_switch_penalty(model, x, ("H1",), {"T-A": {"R-X"}}, 2)
    solver = cp_model.CpSolver()
    solver.Solve(model)
    assert sum(solver.Value(p) for p in penalties) == 0


def test_role_switch_different_tasks_sharing_a_role_costs_nothing():
    """T-INSPECT-MINE-like and T-SUPERVISE-like tasks both admit
    R-OPPERSTEIJGER in the real dataset -- moving between them is not a
    role switch."""
    model = cp_model.CpModel()
    x = {
        ("H1", "T-A", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "T-B", "L1", 0, 1): model.NewBoolVar("x2"),
    }
    model.Add(x[("H1", "T-A", "L1", 0, 0)] == 1)
    model.Add(x[("H1", "T-B", "L1", 0, 1)] == 1)
    penalties = add_role_switch_penalty(
        model, x, ("H1",),
        {"T-A": {"R-OPPERSTEIJGER", "R-BERGWERKER"}, "T-B": {"R-OPPERSTEIJGER", "R-MANDOOR"}},
        2,
    )
    solver = cp_model.CpSolver()
    solver.Solve(model)
    assert sum(solver.Value(p) for p in penalties) == 0


def test_role_switch_disjoint_roles_is_penalized():
    model = cp_model.CpModel()
    x = {
        ("H1", "T-A", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "T-B", "L1", 0, 1): model.NewBoolVar("x2"),
    }
    model.Add(x[("H1", "T-A", "L1", 0, 0)] == 1)
    model.Add(x[("H1", "T-B", "L1", 0, 1)] == 1)
    penalties = add_role_switch_penalty(
        model, x, ("H1",), {"T-A": {"R-ASSAIJEUR"}, "T-B": {"R-SMIT"}}, 2
    )
    solver = cp_model.CpSolver()
    solver.Solve(model)
    assert sum(solver.Value(p) for p in penalties) == 1


def test_role_switch_unconstrained_task_never_contradicts_anything():
    """A task with no declared preferred_role_ids has nothing to
    contradict -- must never trigger a role_switch penalty."""
    model = cp_model.CpModel()
    x = {
        ("H1", "T-A", "L1", 0, 0): model.NewBoolVar("x1"),
        ("H1", "T-NOROLE", "L1", 0, 1): model.NewBoolVar("x2"),
    }
    model.Add(x[("H1", "T-A", "L1", 0, 0)] == 1)
    model.Add(x[("H1", "T-NOROLE", "L1", 0, 1)] == 1)
    penalties = add_role_switch_penalty(
        model, x, ("H1",), {"T-A": {"R-ASSAIJEUR"}}, 2  # T-NOROLE absent -> no requirement
    )
    solver = cp_model.CpSolver()
    solver.Solve(model)
    assert sum(solver.Value(p) for p in penalties) == 0


def test_role_switch_applies_symmetrically_to_aggregate_groups():
    """add_role_switch_penalty never consults person_roles/group identity
    -- an aggregate group's disjoint-role switch must be penalized exactly
    like a named individual's, with no special-casing either way."""
    model = cp_model.CpModel()
    x = {
        ("G-GROUP", "T-A", "L1", 0, 0): model.NewBoolVar("x1"),
        ("G-GROUP", "T-B", "L1", 0, 1): model.NewBoolVar("x2"),
    }
    model.Add(x[("G-GROUP", "T-A", "L1", 0, 0)] == 1)
    model.Add(x[("G-GROUP", "T-B", "L1", 0, 1)] == 1)
    penalties = add_role_switch_penalty(
        model, x, ("G-GROUP",), {"T-A": {"R-ASSAIJEUR"}, "T-B": {"R-SMIT"}}, 2
    )
    solver = cp_model.CpSolver()
    solver.Solve(model)
    assert sum(solver.Value(p) for p in penalties) == 1


def test_role_switch_no_penalty_created_when_neither_period_has_any_variable():
    model = cp_model.CpModel()
    penalties = add_role_switch_penalty(model, {}, ("H1",), {"T-A": {"R-X"}}, 2)
    assert penalties == []
