"""Software-contract tests for applicability_validator.py. Verifies the
core semantic guards: tiers are never collapsed, an approved calibration
procedure is never conflated with a resolved numeric value, and the eight
M3 blockers cannot be closed by any code path in this module."""
from pathlib import Path

import pytest

from ..applicability_validator import (
    TAU_PROCEDURE_TOKEN,
    TierClass,
    classify_tier,
    find_tau_linked_gates,
    get_m3_blockers,
    read_threshold_status,
    verify_all_blockers_open,
    verify_tau_linked_gate_set,
)
from ..parser import parse_gate_spec_v2

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("MANDATORY", TierClass.MANDATORY),
        ("ADVISORY", TierClass.ADVISORY),
        ("N/A", TierClass.NOT_APPLICABLE),
        ("MANDATORY (historical; retired for future amended M3 only)", TierClass.HISTORICAL_SPECIAL),
        ("MIXED (see original: GATE-044 MANDATORY; others ADVISORY)", TierClass.HISTORICAL_SPECIAL),
        ("SOMETHING_NEVER_SEEN_BEFORE", TierClass.UNRECOGNIZED),
    ],
)
def test_classify_tier_never_collapses_distinctions(raw, expected):
    result = classify_tier(raw)
    assert result.tier_class == expected
    assert result.raw_status == raw  # original string always preserved


def test_not_applicable_is_not_converted_to_pass_or_fail():
    result = classify_tier("N/A")
    # The classification carries no pass/fail field at all -- the dataclass
    # only has raw_status and tier_class, which is itself the guarantee.
    assert not hasattr(result, "passed")
    assert not hasattr(result, "failed")


def test_read_threshold_status_procedure_token_is_not_a_numeric_value():
    reading = read_threshold_status("GATE-SYN", TAU_PROCEDURE_TOKEN)
    assert reading.procedure_resolved is True
    assert reading.numeric_value_selected is False


def test_read_threshold_status_ordinary_value_has_no_procedure_flag():
    reading = read_threshold_status("GATE-SYN", "0.05")
    assert reading.procedure_resolved is False
    assert reading.numeric_value_selected is False


def test_find_tau_linked_gates_on_minimal_fixture():
    doc = parse_gate_spec_v2(FIXTURES / "minimal_gate_spec.csv")
    linked = find_tau_linked_gates(doc)
    assert [r.gate_id for r in linked] == ["GATE-SYN-002"]
    assert linked[0].numeric_value_selected is False


def test_verify_tau_linked_gate_set_reports_mismatch_on_minimal_fixture():
    # The minimal fixture only has 1 tau-linked gate, not the frozen
    # baseline's expected 4 -- the check must report this, not pass silently.
    doc = parse_gate_spec_v2(FIXTURES / "minimal_gate_spec.csv")
    problems = verify_tau_linked_gate_set(doc)
    assert problems  # non-empty: fixture deliberately deviates from the real spec


def test_m3_blockers_are_exactly_eight_and_all_open():
    blockers = get_m3_blockers()
    assert len(blockers) == 8
    assert verify_all_blockers_open() == sorted(blockers.keys())


def test_m3_blockers_mapping_is_immutable():
    blockers = get_m3_blockers()
    with pytest.raises(TypeError):
        blockers["M3-BLOCK-01"] = "attempting to close a blocker must fail"


def test_no_close_or_resolve_method_exists_on_applicability_validator_module():
    from .. import applicability_validator as mod
    forbidden_names = {"close_blocker", "resolve_blocker", "mark_resolved", "set_status"}
    assert forbidden_names.isdisjoint(dir(mod))
