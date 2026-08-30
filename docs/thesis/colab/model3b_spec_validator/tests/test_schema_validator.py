"""Software-contract tests for schema_validator.py using minimal synthetic
fixtures. Confirms duplicate-ID detection and ledger-shape checks work on
small, controlled inputs -- not a claim about the real frozen spec."""
from pathlib import Path

from ..parser import parse_gate_spec_v2, parse_ledger
from ..schema_validator import validate_gate_spec, validate_ledger

FIXTURES = Path(__file__).parent / "fixtures"


def test_validate_gate_spec_flags_duplicate_gate_id():
    doc = parse_gate_spec_v2(FIXTURES / "broken_gate_spec_duplicate_id.csv")
    result = validate_gate_spec(doc)
    assert not result.ok
    assert any("duplicate gate_id" in f for f in result.findings)


def test_validate_gate_spec_minimal_fixture_has_no_duplicate_finding():
    doc = parse_gate_spec_v2(FIXTURES / "minimal_gate_spec.csv")
    result = validate_gate_spec(doc)
    assert not any("duplicate gate_id" in f for f in result.findings)


def test_validate_ledger_reports_distribution_mismatch_on_small_fixture():
    # The minimal fixture has 2 rows, not the frozen baseline's 8 -- the
    # validator must report this mismatch rather than silently pass.
    doc = parse_ledger(FIXTURES / "minimal_ledger.csv")
    result = validate_ledger(doc)
    assert not result.ok
    assert any("row count" in f for f in result.findings)


def test_validate_ledger_detects_no_duplicate_ids_in_minimal_fixture():
    doc = parse_ledger(FIXTURES / "minimal_ledger.csv")
    result = validate_ledger(doc)
    assert not any("duplicate decision_id" in f for f in result.findings)
