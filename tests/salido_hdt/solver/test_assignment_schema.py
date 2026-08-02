"""Regression guards for the extended per-assignment evidence schema in
cli.run()'s scenario_NN.json output, and for constraint_strength's wiring
into _hard_task_preferred_roles / _task_preferred_roles."""
import json

from salido_hdt.solver import config
from salido_hdt.solver.cli import (
    _assignment_evidence,
    _blocked_constraint_strength_tasks,
    _hard_task_preferred_roles,
    _task_preferred_roles,
    run,
)
from salido_hdt.solver.constraint_strength import AxisValue, parse_constraint_strength
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.domain import ProvenanceLevel
from salido_hdt.solver.variables import build_variables

_REQUIRED_ASSIGNMENT_KEYS = {
    "scenario_id", "entity_id", "entity_type", "task_id", "location_id",
    "schicht_id", "time_bucket", "assignment_state", "evidence_status",
    "source_document_id", "source_passage_id", "evidence_quote",
    "constraint_ids", "supporting_inventory_item_ids", "supporting_role_ids",
    "provenance_precision", "reconstruction_warning",
}


def _dataset():
    return load_dataset(config.V0_4_1_ROOT)


# --- _assignment_evidence: real-data-grounded -----------------------------


def test_assignment_evidence_for_real_hrlt_backed_assignment():
    """P-HESSE's presence at L-SALIDO is backed by HRLT-0003 -- verify
    every evidence field traces back to that real record."""
    dataset = _dataset()
    sv = build_variables(dataset)
    rec = dataset.hrlt_records["HRLT-0003"]
    assert rec.human_or_group_id == "P-HESSE" and rec.location_id == "L-SALIDO"

    evidence = _assignment_evidence(dataset, sv, {}, "P-HESSE", "T-RECORD", "L-SALIDO", 5)

    assert evidence["entity_type"] == "individual"
    assert evidence["assignment_state"] == "solver_reconstructed"
    assert evidence["evidence_status"] == "reconstructed"
    assert evidence["reconstruction_warning"] == "not an archival statement"
    assert evidence["source_document_id"] == rec.source_document_id
    assert evidence["evidence_quote"] == rec.source_quote
    assert evidence["constraint_ids"] == ["HRLT-0003"]
    assert evidence["provenance_precision"] in {p.value for p in ProvenanceLevel}
    assert "R-BERGHSCHRIJVER" in evidence["supporting_role_ids"]


def test_assignment_evidence_for_aggregate_group():
    dataset = _dataset()
    sv = build_variables(dataset)
    evidence = _assignment_evidence(dataset, sv, {}, "G-MS-121", "T-DRILL", "L-BENEDEN-PAGGER", 5)
    assert evidence["entity_type"] == "aggregate_group"
    assert evidence["assignment_state"] == "solver_reconstructed"
    assert evidence["evidence_status"] == "reconstructed"


def test_assignment_evidence_reconstruction_warning_is_always_present_and_fixed():
    """Every solver assignment is a reconstruction -- these three fields
    must be constant, never varying by entity or record quality."""
    dataset = _dataset()
    sv = build_variables(dataset)
    for h, l, t in [("P-HESSE", "L-SALIDO", 3), ("G-SLAVIN-68", "L-BENEDEN-PAGGER", 10)]:
        evidence = _assignment_evidence(dataset, sv, {}, h, "T-X", l, t)
        assert evidence["assignment_state"] == "solver_reconstructed"
        assert evidence["evidence_status"] == "reconstructed"
        assert evidence["reconstruction_warning"] == "not an archival statement"


def test_assignment_evidence_supporting_inventory_item_ids_from_capacity_map():
    dataset = _dataset()
    sv = build_variables(dataset)
    capacity_map = {("T-DRILL", "L-ORTEN"): ("INV-0001", "INV-0002")}
    evidence = _assignment_evidence(dataset, sv, capacity_map, "P-HESSE", "T-DRILL", "L-ORTEN", 0)
    assert evidence["supporting_inventory_item_ids"] == ["INV-0001", "INV-0002"]


def test_assignment_evidence_missing_provenance_when_no_presence_record():
    """An (h, l, t) combination outside any attested window must yield
    provenance_precision=missing, not a fabricated claim."""
    dataset = _dataset()
    sv = build_variables(dataset)
    evidence = _assignment_evidence(dataset, sv, {}, "P-HESSE", "T-X", "L-NOWHERE", 0)
    assert evidence["provenance_precision"] == ProvenanceLevel.MISSING.value
    assert evidence["source_document_id"] == ""
    assert evidence["constraint_ids"] == []


# --- full scenario JSON schema, end-to-end ---------------------------------


def test_scenario_json_active_assignments_have_all_required_keys(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    payload = json.loads((output_dir / "scenario_00.json").read_text(encoding="utf-8"))
    assert "scenario_id" in payload
    for a in payload["active_assignments"]:
        assert _REQUIRED_ASSIGNMENT_KEYS <= set(a.keys())
        assert a["provenance_precision"] in {p.value for p in ProvenanceLevel}
        assert a["assignment_state"] == "solver_reconstructed"
        assert a["evidence_status"] == "reconstructed"
        assert a["reconstruction_warning"] == "not an archival statement"


def test_scenario_json_active_assignments_have_all_required_keys_even_with_forced_assignment(tmp_path):
    """Force at least one real assignment to exist (the current unbiased
    optimum is all-idle) so the schema is exercised on non-empty output
    too, not just verified structurally to be an empty list."""
    from ortools.sat.python import cp_model

    from salido_hdt.solver.cli import _aggregate_group_ids, _assignment_evidence
    from salido_hdt.solver.hard_constraints import add_one_location_per_schicht, add_temporal_presence
    from salido_hdt.solver.variables import build_variables as bv

    dataset = _dataset()
    sv = bv(dataset)
    model = sv.model
    add_temporal_presence(model, sv.x, sv.presence)
    add_one_location_per_schicht(model, sv.x)

    h_vars = {k: v for k, v in sv.x.items() if k[0] == "P-HESSE"}
    assert h_vars
    some_key = next(iter(h_vars))
    for k, v in h_vars.items():
        model.Add(v == (1 if k == some_key else 0))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    assert solver.Value(h_vars[some_key]) == 1

    evidence = _assignment_evidence(dataset, sv, {}, some_key[0], some_key[1], some_key[2], some_key[4])
    row = {
        "scenario_id": "scenario_00", "entity_id": some_key[0], "task_id": some_key[1],
        "location_id": some_key[2], "schicht_id": some_key[3], "time_bucket": some_key[4],
        **evidence,
    }
    assert _REQUIRED_ASSIGNMENT_KEYS <= set(row.keys())
    assert row["entity_id"] == "P-HESSE"
    assert row["provenance_precision"] != ""


# --- constraint_strength wiring into cli.py --------------------------------


def test_hard_task_preferred_roles_uses_parser_role_axis_not_free_text():
    dataset = _dataset()
    hard = _hard_task_preferred_roles(dataset)
    for task_id in hard:
        t = dataset.task_requirements[task_id]
        parsed = parse_constraint_strength(t)
        assert parsed.parsed_constraint_axes.role_constraint_type == AxisValue.HARD


def test_t_assay_is_included_since_role_constraint_type_is_hard():
    """T-ASSAY's constraint_strength is plain 'hard', which the
    authoritative table resolves to role=HARD, location=HARD."""
    dataset = _dataset()
    hard = _hard_task_preferred_roles(dataset)
    assert "T-ASSAY" in hard


def test_blocked_constraint_strength_tasks_empty_on_real_dataset():
    dataset = _dataset()
    assert _blocked_constraint_strength_tasks(dataset) == []


def test_task_preferred_roles_excludes_blocked_unknown_tasks():
    import dataclasses
    from unittest.mock import Mock

    dataset = _dataset()
    fake_task = Mock(
        task_id="T-FAKE", preferred_role_ids=("R-X",), constraint_strength="totally_unrecognized",
        allowed_location_ids=("L-X",), required_tool_keywords=(), minimum_workers_assumption=1.0,
    )
    new_task_requirements = dict(dataset.task_requirements)
    new_task_requirements["T-FAKE"] = fake_task
    dataset = dataclasses.replace(dataset, task_requirements=new_task_requirements)

    assert "T-FAKE" not in _task_preferred_roles(dataset)
    assert "T-FAKE" not in _hard_task_preferred_roles(dataset)
    blocked = _blocked_constraint_strength_tasks(dataset)
    assert any(b["task_id"] == "T-FAKE" for b in blocked)
