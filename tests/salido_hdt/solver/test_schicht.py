"""Regression guards for v0.1.3 (SOLVER_V0_1_3_SCHICHT_PLAN.md) and v0.1.4
(SOLVER_V0_1_4_THREE_SHIFT_METADATA_PLAN.md): typed schicht domain,
evidence gating, three-shift source-count metadata, and diagnostic-vs-
public output disclosure.
"""
import csv
import inspect
import json

from salido_hdt.solver import config
from salido_hdt.solver.cli import parse_schicht_assumption_arg, run
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.domain import EntityType
from salido_hdt.solver.schicht import (
    SchichtId,
    SchichtLabel,
    SchichtScenarioAssumption,
    SchichtSourceEvidence,
    resolve_schicht_labels,
    schicht_label_to_dict,
    schicht_label_to_public_dict,
)
from salido_hdt.solver.variables import build_variables


def test_schicht_id_enum_has_exactly_the_four_controlled_values():
    assert {member.value for member in SchichtId} == {
        "SCHICHT-UNSPECIFIED", "SCHICHT-DAY", "SCHICHT-NIGHT",
        "SCHICHT-THREE-SHIFT-UNSPECIFIED",
    }


def test_no_schicht_1_2_3_identities_exist():
    values = {member.value for member in SchichtId}
    assert "SCHICHT-1" not in values
    assert "SCHICHT-2" not in values
    assert "SCHICHT-3" not in values
    assert len(SchichtId) == 4


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
    assert label.source_schicht_count is None
    assert label.individual_shift_assignment_known is False


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
        schicht_index_internal=0, schicht_id=SchichtId.UNSPECIFIED, schicht_evidence_status="unspecified",
        schicht_warning="w",
    )
    d = schicht_label_to_dict(label)
    assert set(d) == {
        "schicht_index_internal", "schicht_id", "schicht_evidence_status", "schicht_source_document_id",
        "schicht_source_passage_id", "schicht_assumption_id", "schicht_warning",
        "source_schicht_count", "individual_shift_assignment_known",
    }
    assert d["schicht_id"] == "SCHICHT-UNSPECIFIED"
    assert isinstance(d["schicht_index_internal"], int)


def test_schicht_label_to_public_dict_excludes_internal_index():
    label = SchichtLabel(
        schicht_index_internal=0, schicht_id=SchichtId.UNSPECIFIED, schicht_evidence_status="unspecified",
    )
    d = schicht_label_to_public_dict(label)
    assert "schicht_index_internal" not in d
    assert set(d) == {
        "schicht_id", "schicht_evidence_status", "schicht_source_document_id",
        "schicht_source_passage_id", "schicht_assumption_id", "schicht_warning",
        "source_schicht_count", "individual_shift_assignment_known",
    }


# --- v0.1.4: three-shift source-count metadata ------------------------------


def test_three_shift_evidence_carries_source_count_and_unknown_allocation():
    """The exact 'dokumen menyebut tiga schichten, personel tak
    teridentifikasi' case."""
    evidence = SchichtSourceEvidence(
        schicht_id=SchichtId.THREE_SHIFT_UNSPECIFIED,
        source_document_id="DOC-EVENT-X",
        source_passage_id="SP-EVENT-X",
        source_schicht_count=3,
        individual_shift_assignment_known=False,
    )
    labels = resolve_schicht_labels(1, source_evidence={0: evidence})
    label = labels[0]
    assert label.schicht_id == SchichtId.THREE_SHIFT_UNSPECIFIED
    assert label.source_schicht_count == 3
    assert label.individual_shift_assignment_known is False
    assert label.schicht_evidence_status == "explicit_source"
    # never inflated into per-shift identities:
    assert label.schicht_id.value not in {"SCHICHT-1", "SCHICHT-2", "SCHICHT-3"}


def test_three_shift_evidence_does_not_multiply_x_variables():
    """Structural proof, not a convention: resolving three-shift evidence
    (a post-hoc labeling step) must never change how many x-variables
    build_variables() constructed, because resolve_schicht_labels() is
    never consulted by build_variables() in the first place."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    sv_before = build_variables(dataset)
    n_x_before = len(sv_before.x)

    evidence = SchichtSourceEvidence(
        schicht_id=SchichtId.THREE_SHIFT_UNSPECIFIED,
        source_document_id="DOC-EVENT-X", source_passage_id="SP-EVENT-X",
        source_schicht_count=3, individual_shift_assignment_known=False,
    )
    # Resolve labels (metadata layer) -- must have zero effect on a freshly
    # rebuilt variable set.
    resolve_schicht_labels(sv_before.schicht_count, source_evidence={0: evidence})
    sv_after = build_variables(dataset)

    assert len(sv_after.x) == n_x_before
    assert sv_after.schicht_count == sv_before.schicht_count == 1


def test_three_shift_evidence_does_not_multiply_aggregate_group_variables():
    dataset = load_dataset(config.V0_4_1_ROOT)
    sv = build_variables(dataset)
    group_ids = {
        h.human_or_group_id for h in dataset.hrlt_records.values()
        if h.entity_type == EntityType.AGGREGATE_GROUP
    }
    group_vars_before = {k: v for k, v in sv.x.items() if k[0] in group_ids}
    assert group_vars_before  # sanity

    evidence = SchichtSourceEvidence(
        schicht_id=SchichtId.THREE_SHIFT_UNSPECIFIED,
        source_document_id="DOC-EVENT-X", source_passage_id="SP-EVENT-X",
        source_schicht_count=3, individual_shift_assignment_known=False,
    )
    resolve_schicht_labels(sv.schicht_count, source_evidence={0: evidence})

    sv_after = build_variables(dataset)
    group_vars_after = {k: v for k, v in sv_after.x.items() if k[0] in group_ids}
    assert len(group_vars_after) == len(group_vars_before)


def test_variables_module_never_references_source_schicht_count():
    """Static guard mirroring the existing HumanGroup.count guard
    (test_aggregate_group_integrity.py) -- proves the decoupling by
    construction, not convention."""
    from salido_hdt.solver import variables
    source = inspect.getsource(variables)
    assert "source_schicht_count" not in source
    assert "individual_shift_assignment_known" not in source


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


def test_schicht_index_internal_absent_from_end_user_outputs(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=3)

    for path in sorted(output_dir.glob("scenario_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for a in payload["active_assignments"]:
            assert "schicht_index_internal" not in a
            assert "schicht_index" not in a  # v0.1.3 name must also be gone

    with (output_dir / "equipment_capacity.csv").open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert "schicht_index_internal" not in reader.fieldnames
        assert "schicht_index" not in reader.fieldnames

    # ... but it IS present in the diagnostic output:
    summary = json.loads((output_dir / "validation_summary.json").read_text(encoding="utf-8"))
    assert "schicht_index_internal" in summary["run_metadata"]["schicht_labels"][0]


def test_equipment_capacity_csv_has_schicht_id_column(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    with (output_dir / "equipment_capacity.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows
    for row in rows:
        assert row["schicht_id"] == "SCHICHT-UNSPECIFIED"


def test_equipment_capacity_csv_has_source_schicht_count_and_evidence_status_columns(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    with (output_dir / "equipment_capacity.csv").open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert "source_schicht_count" in reader.fieldnames
        assert "schicht_evidence_status" in reader.fieldnames
        rows = list(reader)
    assert rows
    for row in rows:
        assert row["schicht_evidence_status"] == "unspecified"
        assert row["source_schicht_count"] == ""  # None -> empty string, never a fabricated count


def test_validation_summary_run_metadata_includes_schicht_labels(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    summary = json.loads((output_dir / "validation_summary.json").read_text(encoding="utf-8"))
    labels = summary["run_metadata"]["schicht_labels"]
    assert len(labels) == 1
    assert labels[0]["schicht_id"] == "SCHICHT-UNSPECIFIED"
    assert labels[0]["schicht_index_internal"] == 0


# --- equipment capacity remains grouped by (schicht, time) -- re-verification ---


def test_equipment_capacity_still_grouped_by_schicht_and_time():
    """Re-verification (not re-implementation) of ad8dc6b4's Item 1 fix --
    unaffected by this metadata-only patch."""
    from ortools.sat.python import cp_model

    from salido_hdt.solver.hard_constraints import add_equipment_capacity

    model = cp_model.CpModel()
    x = {
        ("P-A", "T-DRILL", "L-ORTEN", 0, 0): model.NewBoolVar("x_s0"),
        ("P-B", "T-DRILL", "L-ORTEN", 1, 0): model.NewBoolVar("x_s1"),
    }
    n = add_equipment_capacity(model, x, task_id="T-DRILL", location_id="L-ORTEN", capacity=1)
    assert n == 2
