"""Software-contract tests for parser.py. Uses only minimal synthetic
fixtures (never the real frozen V2 files, never historical data)."""
from pathlib import Path

import pytest

from ..parser import SpecParseError, parse_gate_spec_v2, parse_ledger

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_gate_spec_minimal_ok():
    doc = parse_gate_spec_v2(FIXTURES / "minimal_gate_spec.csv")
    assert len(doc.rows) == 2
    assert doc.rows[0]["gate_id"] == "GATE-SYN-001"


def test_parse_gate_spec_round_trips_tau_procedure_token_unchanged():
    doc = parse_gate_spec_v2(FIXTURES / "minimal_gate_spec.csv")
    row = next(r for r in doc.rows if r["gate_id"] == "GATE-SYN-002")
    assert row["threshold_status"] == "PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION"


def test_parse_gate_spec_rejects_blank_required_field():
    with pytest.raises(SpecParseError, match="mandatory_advisory_status"):
        parse_gate_spec_v2(FIXTURES / "broken_gate_spec_blank_field.csv")


def test_parse_gate_spec_does_not_silently_default_blank_field():
    # Explicit companion to the above: confirm the failure mode is a raised
    # exception, not a silently-substituted default value anywhere in rows.
    try:
        parse_gate_spec_v2(FIXTURES / "broken_gate_spec_blank_field.csv")
        assert False, "expected SpecParseError"
    except SpecParseError:
        pass


def test_parse_ledger_minimal_ok():
    doc = parse_ledger(FIXTURES / "minimal_ledger.csv")
    assert len(doc.rows) == 2
    assert {r["current_status"] for r in doc.rows} == {"APPROVED_WITH_LIMITATIONS", "DEFERRED"}


def test_parse_ledger_rejects_unrecognized_status_enum():
    with pytest.raises(SpecParseError, match="unrecognized current_status"):
        parse_ledger(FIXTURES / "broken_ledger_bad_status.csv")


def test_parse_ledger_wrong_column_set_raises():
    with pytest.raises(SpecParseError, match="column set/order"):
        # gate spec fixture has the wrong header for a ledger
        parse_ledger(FIXTURES / "minimal_gate_spec.csv")
