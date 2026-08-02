"""Regression guards for v0.1.3 (SOLVER_V0_1_3_SCHICHT_PLAN.md): typed
schicht domain, evidence gating, and public-output disclosure.
"""
import csv
import json

from salido_hdt.solver import config
from salido_hdt.solver.cli import parse_schicht_assumption_arg, run
from salido_hdt.solver.schicht import (
    SchichtId,
    SchichtLabel,
    SchichtScenarioAssumption,
    SchichtSourceEvidence,
    resolve_schicht_labels,
    schicht_label_to_dict,
)


def test_schicht_id_enum_has_exactly_the_four_controlled_values():
    assert {member.value for member in SchichtId} == {
        "SCHICHT-UNSPECIFIED", "SCHICHT-DAY", "SCHICHT-NIGHT",
        "SCHICHT-THREE-SHIFT-UNSPECIFIED",
    }


def test_default_resolution_with_no_evidence_is_unspecified():
    labels = resolve_schicht_labels(1)
    label = labels[0]
    assert label.schicht_id == SchichtId.UNSPECIFIED
    assert label.schicht_evidence_status == "unspecified"
    assert label.schicht_source_document_id == ""
    assert label.schicht_source_passage_id == ""
    assert label.schicht_assumption_id == ""
    assert label.schicht_warning  # non-empty
    assert "SCHICHT-UNSPECIFIED" in label.schicht_warning


def test_scenario_assumption_resolves_to_asserted_schicht_id():
    assumption = SchichtScenarioAssumption(schicht_id=SchichtId.DAY, assumption_id="TEST-1")
    labels = resolve_schicht_labels(1, scenario_assumptions={0: assumption})
    label = labels[0]
    assert label.schicht_id == SchichtId.DAY
    assert label.schicht_evidence_status == "scenario_assumption"
    assert label.schicht_assumption_id == "TEST-1"
    assert "not an archival statement" in label.schicht_warning


def test_source_evidence_resolves_to_asserted_schicht_id():
    evidence = SchichtSourceEvidence(
        schicht_id=SchichtId.NIGHT, source_document_id="DOC-X", source_passage_id="SP-X",
    )
    labels = resolve_schicht_labels(1, source_evidence={0: evidence})
    label = labels[0]
    assert label.schicht_id == SchichtId.NIGHT
    assert label.schicht_evidence_status == "explicit_source"
    assert label.schicht_source_document_id == "DOC-X"
    assert label.schicht_source_passage_id == "SP-X"
    assert label.schicht_assumption_id == ""


def test_source_evidence_takes_precedence_over_scenario_assumption():
    evidence = SchichtSourceEvidence(
        schicht_id=SchichtId.NIGHT, source_document_id="DOC-X", source_passage_id="SP-X",
    )
    assumption = SchichtScenarioAssumption(schicht_id=SchichtId.DAY, assumption_id="TEST-1")
    labels = resolve_schicht_labels(1, source_evidence={0: evidence}, scenario_assumptions={0: assumption})
    label = labels[0]
    assert label.schicht_id == SchichtId.NIGHT
    assert label.schicht_evidence_status == "explicit_source"


def test_schicht_label_to_dict_has_all_required_fields():
    label = SchichtLabel(
        schicht_index=0, schicht_id=SchichtId.UNSPECIFIED, schicht_evidence_status="unspecified",
        schicht_warning="w",
    )
    d = schicht_label_to_dict(label)
    assert set(d) == {
        "schicht_index", "schicht_id", "schicht_evidence_status", "schicht_source_document_id",
        "schicht_source_passage_id", "schicht_assumption_id", "schicht_warning",
    }
    assert d["schicht_id"] == "SCHICHT-UNSPECIFIED"
    assert isinstance(d["schicht_index"], int)


# --- CLI argument parsing ---------------------------------------------------


def test_cli_schicht_assumption_flag_parses_index_and_schicht_id():
    index, assumption = parse_schicht_assumption_arg("0=SCHICHT-DAY")
    assert index == 0
    assert assumption.schicht_id == SchichtId.DAY
    assert assumption.assumption_id


def test_cli_schicht_assumption_flag_rejects_unrecognized_schicht_id():
    import pytest
    with pytest.raises(ValueError):
        parse_schicht_assumption_arg("0=SCHICHT-AFTERNOON")


def test_cli_schicht_assumption_flag_rejects_malformed_input():
    import pytest
    with pytest.raises(ValueError):
        parse_schicht_assumption_arg("not-a-valid-arg")


# --- real dataset, real cli.run() -------------------------------------------


def test_real_dataset_default_run_never_emits_raw_int_schicht_id(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=3)
    found_any_assignment = False
    for path in sorted(output_dir.glob("scenario_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for a in payload["active_assignments"]:
            found_any_assignment = True
            assert a["schicht_id"] == "SCHICHT-UNSPECIFIED"
            assert isinstance(a["schicht_id"], str)
            assert a["schicht_index"] == 0
            assert a["schicht_evidence_status"] == "unspecified"
            assert a["schicht_warning"]
    assert found_any_assignment  # sanity: the degenerate diversification round does produce assignments


def test_real_dataset_run_with_cli_assumption_emits_asserted_schicht_id(tmp_path):
    assumption = SchichtScenarioAssumption(schicht_id=SchichtId.DAY, assumption_id="TEST-RUN-1")
    output_dir = run(
        root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=3,
        schicht_scenario_assumptions={0: assumption},
    )
    found_any_assignment = False
    for path in sorted(output_dir.glob("scenario_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for a in payload["active_assignments"]:
            found_any_assignment = True
            assert a["schicht_id"] == "SCHICHT-DAY"
            assert a["schicht_evidence_status"] == "scenario_assumption"
            assert a["schicht_assumption_id"] == "TEST-RUN-1"
            assert "not an archival statement" in a["schicht_warning"]
    assert found_any_assignment


def test_equipment_capacity_csv_has_schicht_id_column(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    with (output_dir / "equipment_capacity.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows
    for row in rows:
        assert row["schicht_id"] == "SCHICHT-UNSPECIFIED"


def test_validation_summary_run_metadata_includes_schicht_labels(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    summary = json.loads((output_dir / "validation_summary.json").read_text(encoding="utf-8"))
    labels = summary["run_metadata"]["schicht_labels"]
    assert len(labels) == 1
    assert labels[0]["schicht_id"] == "SCHICHT-UNSPECIFIED"
    assert labels[0]["schicht_index"] == 0
