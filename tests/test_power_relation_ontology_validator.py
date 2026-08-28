"""Deterministic test harness for the generalized power-relation ontology
validator (scripts/research_validators/validate_power_relation_ontology.py).

Governing baseline: commit b54c8a6c05b13d75db864d0731105fe276fdce6d.
Read-only against synthetic fixtures under
tests/fixtures/power_relation_ontology/ -- no fixture is ever modified by
these tests, and none of the fixtures contains real archival data.
"""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "research_validators" / "validate_power_relation_ontology.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "power_relation_ontology"

POSITIVE_FIXTURES = sorted(FIXTURES.glob("positive_*.json"))
NEGATIVE_FIXTURES = sorted(FIXTURES.glob("negative_*.json"))

EXPECTED_NEGATIVE_ERROR_CODES = {
    "negative_01_unknown_version.json": "UNKNOWN_ONTOLOGY_VERSION",
    "negative_02_missing_provenance.json": "MISSING_PROVENANCE",
    "negative_03_invalid_reference.json": "ORPHAN_RIGHT_MODIFICATION_REFERENCE",
    "negative_04_invalid_cardinality.json": "INVALID_NON_IDENTITY_CARDINALITY",
    "negative_05_unapproved_relation_type.json": "UNAPPROVED_RELATION_TYPE",
    "negative_06_research_only_marked_public.json": "RESEARCH_ONLY_BOUNDARY_VIOLATION",
    "negative_07_research_only_marked_graphify.json": "RESEARCH_ONLY_BOUNDARY_VIOLATION",
    "negative_08_deferred_ch04.json": "DEFERRED_STRUCTURE_NOT_AUTHORIZED",
    "negative_09_rejected_ch05.json": "REJECTED_STRUCTURE_NOT_AUTHORIZED",
    "negative_10_deferred_ch08.json": "DEFERRED_STRUCTURE_NOT_AUTHORIZED",
    "negative_11_automatic_identity_merge.json": "INVALID_NON_IDENTITY_REFERENCE",
    "negative_12_unbounded_continuity.json": "UNBOUNDED_MANDATE_FIELD",
    "negative_13_resistance_as_factual_edge.json": "RESEARCH_ONLY_BOUNDARY_VIOLATION",
    "negative_14_patron_client_as_factual_edge.json": "UNAPPROVED_RELATION_TYPE",
    "negative_15_malformed_json.json": "MALFORMED_JSON",
    "negative_16_unknown_field_value.json": "INVALID_COERCION_STATUS",
    "negative_17_invalid_temporal_range.json": "INVALID_TEMPORAL_RANGE",
    "negative_18_unauthorized_extra_field.json": "UNAUTHORIZED_EXTRA_FIELD",
}


def run_validator(path: Path, as_json: bool = True):
    args = [sys.executable, str(VALIDATOR), str(path)]
    if as_json:
        args.append("--json")
    proc = subprocess.run(args, capture_output=True, text=True)
    return proc


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="module", autouse=True)
def fixtures_present():
    assert len(POSITIVE_FIXTURES) == 10, f"expected 10 positive fixtures, found {len(POSITIVE_FIXTURES)}"
    assert len(NEGATIVE_FIXTURES) == 18, f"expected 18 negative fixtures, found {len(NEGATIVE_FIXTURES)}"


@pytest.mark.parametrize("fixture", POSITIVE_FIXTURES, ids=lambda p: p.name)
def test_positive_fixtures_pass(fixture):
    proc = run_validator(fixture)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    data = json.loads(proc.stdout)
    assert data["passed"] is True
    assert data["counts"]["CRITICAL"] == 0
    assert data["counts"]["ERROR"] == 0


@pytest.mark.parametrize("fixture", NEGATIVE_FIXTURES, ids=lambda p: p.name)
def test_negative_fixtures_fail_with_expected_code(fixture):
    proc = run_validator(fixture)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    data = json.loads(proc.stdout)
    assert data["passed"] is False
    expected = EXPECTED_NEGATIVE_ERROR_CODES[fixture.name]
    codes = {f["error_code"] for f in data["findings"] if f["error_code"]}
    assert expected in codes, f"expected {expected} in {codes}"


@pytest.mark.parametrize("fixture", POSITIVE_FIXTURES + NEGATIVE_FIXTURES, ids=lambda p: p.name)
def test_fixture_not_modified_by_validation(fixture):
    if fixture.name == "negative_15_malformed_json.json":
        before = fixture.read_bytes()
    else:
        before = _file_hash(fixture)
    run_validator(fixture)
    run_validator(fixture, as_json=False)
    if fixture.name == "negative_15_malformed_json.json":
        assert fixture.read_bytes() == before
    else:
        assert _file_hash(fixture) == before


@pytest.mark.parametrize("fixture", POSITIVE_FIXTURES + NEGATIVE_FIXTURES, ids=lambda p: p.name)
def test_deterministic_repeated_execution(fixture):
    first = run_validator(fixture)
    second = run_validator(fixture)
    assert first.returncode == second.returncode
    assert first.stdout == second.stdout


@pytest.mark.parametrize("fixture", POSITIVE_FIXTURES + NEGATIVE_FIXTURES, ids=lambda p: p.name)
def test_json_output_parses(fixture):
    proc = run_validator(fixture, as_json=True)
    data = json.loads(proc.stdout)
    assert "findings" in data and "passed" in data and "ontology_version" in data


@pytest.mark.parametrize("fixture", POSITIVE_FIXTURES + NEGATIVE_FIXTURES, ids=lambda p: p.name)
def test_human_readable_output_stable(fixture):
    first = run_validator(fixture, as_json=False)
    second = run_validator(fixture, as_json=False)
    assert first.stdout == second.stdout
    assert "VALIDATION RESULT:" in first.stdout


@pytest.mark.parametrize("fixture", POSITIVE_FIXTURES, ids=lambda p: p.name)
def test_positive_exit_code_zero(fixture):
    assert run_validator(fixture).returncode == 0


@pytest.mark.parametrize("fixture", NEGATIVE_FIXTURES, ids=lambda p: p.name)
def test_negative_exit_code_nonzero(fixture):
    assert run_validator(fixture).returncode != 0


def test_research_review_not_silently_converted_to_pass_or_fail():
    """positive_08 has a populated (non-CANNOT_DETERMINE) political_intent -- must
    surface as a REVIEW finding, must not be silently dropped, and must not by
    itself cause FAIL (REVIEW is not a failing severity)."""
    fixture = FIXTURES / "positive_08_constrained_agency_review.json"
    data = json.loads(run_validator(fixture).stdout)
    assert data["passed"] is True
    review_findings = [f for f in data["findings"] if f["severity"] == "REVIEW"]
    assert any(f["rule_id"] == "R-HRV-01" for f in review_findings)
    assert data["counts"]["REVIEW"] >= 1


def test_v2_backward_compatibility_no_v2_1_fields_required():
    fixture = FIXTURES / "positive_01_minimal_v2.json"
    data = json.loads(run_validator(fixture).stdout)
    assert data["ontology_version"] == "V2"
    assert data["passed"] is True


def test_v2_1_research_only_enforcement_blocks_all_promoted_values():
    base = json.loads((FIXTURES / "positive_04_commercial_right.json").read_text())
    promoted_values = ["PUBLIC", "PUBLIC_VOCABULARY", "PRODUCTION", "RUNTIME_APPROVED",
                        "GRAPHIFY_APPROVED", "FACTUAL_EDGE"]
    import tempfile
    for val in promoted_values:
        artifact = copy.deepcopy(base)
        artifact["commercial_rights"][0]["public_status"] = val
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
            json.dump(artifact, tf)
            tf_path = Path(tf.name)
        try:
            data = json.loads(run_validator(tf_path).stdout)
            assert data["passed"] is False, f"public_status={val} should have failed"
            assert any(f["error_code"] == "RESEARCH_ONLY_BOUNDARY_VIOLATION" for f in data["findings"])
        finally:
            tf_path.unlink()


def test_closed_relation_vocabulary_rejects_consent_implying_types():
    base = json.loads((FIXTURES / "positive_01_minimal_v2.json").read_text())
    forbidden = ["RESISTS", "PATRON_OF", "CLIENT_OF", "COMMANDS", "PARTICIPATES_IN",
                 "HOLDS_COMMERCIAL_RIGHT", "MODIFIES_RIGHT"]
    import tempfile
    for rt in forbidden:
        artifact = copy.deepcopy(base)
        artifact["relations"][0]["relation_type"] = rt
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
            json.dump(artifact, tf)
            tf_path = Path(tf.name)
        try:
            data = json.loads(run_validator(tf_path).stdout)
            assert data["passed"] is False, f"relation_type={rt} should have failed"
            assert any(f["error_code"] == "UNAPPROVED_RELATION_TYPE" for f in data["findings"])
        finally:
            tf_path.unlink()


def test_ch04_ch05_ch08_exclusions_enforced():
    ch04 = json.loads(run_validator(FIXTURES / "negative_08_deferred_ch04.json").stdout)
    ch05 = json.loads(run_validator(FIXTURES / "negative_09_rejected_ch05.json").stdout)
    ch08 = json.loads(run_validator(FIXTURES / "negative_10_deferred_ch08.json").stdout)
    assert ch04["passed"] is False and any(
        f["error_code"] == "DEFERRED_STRUCTURE_NOT_AUTHORIZED" for f in ch04["findings"])
    assert ch05["passed"] is False and any(
        f["error_code"] == "REJECTED_STRUCTURE_NOT_AUTHORIZED" for f in ch05["findings"])
    assert ch08["passed"] is False and any(
        f["error_code"] == "DEFERRED_STRUCTURE_NOT_AUTHORIZED" for f in ch08["findings"])


def test_no_graphify_or_production_authorization_introduced():
    """The validator's own source and rule registry must not reference any
    Graphify activation or production-authorization pathway."""
    validator_src = VALIDATOR.read_text(encoding="utf-8")
    assert "graphify_out" not in validator_src.lower()
    assert "import requests" not in validator_src
    assert "psycopg" not in validator_src
    assert "sqlalchemy" not in validator_src.lower()
