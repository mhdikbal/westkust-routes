"""Regression guards for the controlled constraint_strength parser --
every one of the 8 known tokens, per the authoritative per-axis table, plus
the blocked_unknown / not_applicable / provenance-preservation rules.
"""
from unittest.mock import Mock

from salido_hdt.solver import config
from salido_hdt.solver.constraint_strength import AxisValue, parse_constraint_strength
from salido_hdt.solver.data_loader import load_dataset

_H, _S, _U, _NA, _BU = (
    AxisValue.HARD, AxisValue.SOFT, AxisValue.UNSPECIFIED,
    AxisValue.NOT_APPLICABLE, AxisValue.BLOCKED_UNKNOWN,
)


def _task(constraint_strength, preferred_role_ids=("R-X",), allowed_location_ids=("L-X",),
          required_tool_keywords=("kw",), minimum_workers_assumption=1.0):
    return Mock(
        constraint_strength=constraint_strength,
        preferred_role_ids=preferred_role_ids,
        allowed_location_ids=allowed_location_ids,
        required_tool_keywords=required_tool_keywords,
        minimum_workers_assumption=minimum_workers_assumption,
    )


def _axes(constraint_strength, **task_kwargs):
    return parse_constraint_strength(_task(constraint_strength, **task_kwargs)).parsed_constraint_axes


# --- the 8 known tokens, per the authoritative table ------------------------


def test_hard_token():
    ax = _axes("hard")
    assert ax.role_constraint_type == _H
    assert ax.location_constraint_type == _H
    assert ax.equipment_constraint_type == _U
    assert ax.staffing_constraint_type == _U


def test_soft_token():
    ax = _axes("soft")
    assert ax.role_constraint_type == _S
    assert ax.location_constraint_type == _S
    assert ax.equipment_constraint_type == _S
    assert ax.staffing_constraint_type == _S


def test_hard_role_token():
    ax = _axes("hard_role")
    assert ax.role_constraint_type == _H
    assert ax.location_constraint_type == _U
    assert ax.equipment_constraint_type == _U
    assert ax.staffing_constraint_type == _U


def test_hard_location_token():
    ax = _axes("hard_location")
    assert ax.role_constraint_type == _U
    assert ax.location_constraint_type == _H
    assert ax.equipment_constraint_type == _U
    assert ax.staffing_constraint_type == _U


def test_hard_for_assay_token_all_unspecified_plus_legacy_metadata():
    task = _task("hard_for_assay")
    parsed = parse_constraint_strength(task)
    ax = parsed.parsed_constraint_axes
    assert ax.role_constraint_type == _U
    assert ax.location_constraint_type == _U
    assert ax.equipment_constraint_type == _U
    assert ax.staffing_constraint_type == _U
    assert parsed.scope == "assay"
    assert parsed.parse_status == "legacy_ambiguous"
    assert parsed.status == "ok"  # recognized, not blocked


def test_hard_location_soft_staffing_token():
    ax = _axes("hard_location_soft_staffing")
    assert ax.role_constraint_type == _U
    assert ax.location_constraint_type == _H
    assert ax.equipment_constraint_type == _U
    assert ax.staffing_constraint_type == _S


def test_hard_role_soft_tools_token():
    ax = _axes("hard_role_soft_tools")
    assert ax.role_constraint_type == _H
    assert ax.location_constraint_type == _U
    assert ax.equipment_constraint_type == _S
    assert ax.staffing_constraint_type == _U


def test_hard_role_soft_location_token():
    ax = _axes("hard_role_soft_location")
    assert ax.role_constraint_type == _H
    assert ax.location_constraint_type == _S
    assert ax.equipment_constraint_type == _U
    assert ax.staffing_constraint_type == _U


# --- blocked_unknown ----------------------------------------------------------


def test_unrecognized_token_is_blocked_unknown_on_all_axes():
    task = _task("hard_maybe_kind_of")
    parsed = parse_constraint_strength(task)
    ax = parsed.parsed_constraint_axes
    assert ax.role_constraint_type == _BU
    assert ax.location_constraint_type == _BU
    assert ax.equipment_constraint_type == _BU
    assert ax.staffing_constraint_type == _BU
    assert parsed.status == "blocked"
    assert parsed.reason == "unknown_constraint_strength"


def test_empty_string_is_blocked_unknown():
    parsed = parse_constraint_strength(_task(""))
    assert parsed.status == "blocked"
    assert parsed.reason == "unknown_constraint_strength"


def test_similar_but_uncontrolled_token_is_blocked_not_silently_matched():
    """A syntactically-similar-but-not-in-the-controlled-8 string must not
    be silently accepted by any generic combinator logic."""
    parsed = parse_constraint_strength(_task("hard_role_soft_staffing_and_location"))
    assert parsed.status == "blocked"


# --- structural not_applicable overrides the token table ----------------------


def test_not_applicable_overrides_token_for_missing_role_requirement():
    ax = _axes("hard_role", preferred_role_ids=())
    assert ax.role_constraint_type == _NA  # not HARD, despite the token saying hard_role


def test_not_applicable_overrides_token_for_missing_tool_requirement():
    ax = _axes("hard_role_soft_tools", required_tool_keywords=())
    assert ax.equipment_constraint_type == _NA  # not SOFT, despite the token saying soft_tools


def test_not_applicable_overrides_token_for_missing_location_requirement():
    ax = _axes("hard_location", allowed_location_ids=())
    assert ax.location_constraint_type == _NA


def test_not_applicable_overrides_token_for_missing_staffing_assumption():
    ax = _axes("hard_location_soft_staffing", minimum_workers_assumption=None)
    assert ax.staffing_constraint_type == _NA


# --- provenance preservation ---------------------------------------------------


def test_original_string_preserved_verbatim():
    parsed = parse_constraint_strength(_task("hard_role_soft_tools"))
    assert parsed.constraint_strength_original == "hard_role_soft_tools"


def test_task_object_itself_is_never_mutated():
    task = _task("hard_role")
    original_value = task.constraint_strength
    parse_constraint_strength(task)
    assert task.constraint_strength == original_value


# --- real dataset ---------------------------------------------------------------


def test_real_dataset_every_task_parses_without_blocked_unknown():
    """All 7 real constraint_strength values in the actual v0.4.1 dataset
    are among the 8 controlled tokens -- none should ever be blocked."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    for task in dataset.task_requirements.values():
        parsed = parse_constraint_strength(task)
        assert parsed.status == "ok", f"{task.task_id}: {task.constraint_strength}"


def test_real_dataset_t_assay_is_hard_role_and_hard_location():
    dataset = load_dataset(config.V0_4_1_ROOT)
    parsed = parse_constraint_strength(dataset.task_requirements["T-ASSAY"])
    assert parsed.parsed_constraint_axes.role_constraint_type == _H
    assert parsed.parsed_constraint_axes.location_constraint_type == _H
