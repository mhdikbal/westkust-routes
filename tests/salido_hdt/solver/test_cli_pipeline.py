"""v0.1.1 interpretability-fix regression tests (F2, F3, F4, F5, F6, F7) --
see SOLVER_SCENARIO_INTERPRETATION_AUDIT.md / SOLVER_V0_1_1_FIX_PLAN.md.

F1's own dedicated tests live in test_task_continuity_and_role_bias.py.
"""
import json

from salido_hdt.solver import config
from salido_hdt.solver.cli import (
    _EQUIPMENT_CAPACITY_NOTE,
    _RUN_METADATA_NOTE,
    _citations_for,
    _entity_coverage,
    _hard_task_preferred_roles,
    _task_preferred_roles,
    run,
)
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.domain import HardSoftLabel
from salido_hdt.solver.validation import classify_hard_soft, classify_provenance
from salido_hdt.solver.variables import build_variables


def _dataset():
    return load_dataset(config.V0_4_1_ROOT)


# --- F2: entity_coverage --------------------------------------------------


def test_entity_coverage_flags_role_documented_presence_excluded_individual():
    """P-BRETSNIJDER holds a HARD role (R-BERGWERKER) but has no
    HARD-eligible HRLT presence record -- must show up as excluded from
    variables, not silently absent."""
    dataset = _dataset()
    sv = build_variables(dataset)
    coverage = {c["entity_id"]: c for c in _entity_coverage(dataset, sv)}

    assert "P-BRETSNIJDER" in coverage
    row = coverage["P-BRETSNIJDER"]
    assert row["has_hard_role"] is True
    assert row["has_hard_presence"] is False
    assert row["included_in_variables"] is False


def test_entity_coverage_flags_fully_included_entity():
    dataset = _dataset()
    sv = build_variables(dataset)
    coverage = {c["entity_id"]: c for c in _entity_coverage(dataset, sv)}

    row = coverage["P-HESSE"]
    assert row["has_hard_role"] is True
    assert row["has_hard_presence"] is True
    assert row["included_in_variables"] is True


def test_entity_coverage_covers_all_known_persons_and_groups():
    dataset = _dataset()
    sv = build_variables(dataset)
    coverage = _entity_coverage(dataset, sv)

    from salido_hdt.solver.cli import _aggregate_group_ids
    expected = len(dataset.persons) + len(_aggregate_group_ids(dataset))
    assert len(coverage) == expected


# --- F3-followup: equipment capacity wired, not fabricated -----------------


def test_validation_summary_reports_equipment_capacity_wiring(tmp_path):
    """Superseded by the equipment-capacity wiring fix: it is now enforced
    for every (task, location) pair with real inventory matches. See
    test_equipment_capacity_cli_wiring.py for the detailed report checks."""
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    summary = json.loads((output_dir / "validation_summary.json").read_text(encoding="utf-8"))

    assert summary["equipment_capacity_enforced"] is True
    assert summary["equipment_capacity_constraints_instantiated"] > 0
    assert summary["equipment_capacity_note"] == _EQUIPMENT_CAPACITY_NOTE
    assert (output_dir / "equipment_capacity.csv").exists()


# --- F4: hard role-task gate respects constraint_strength -----------------


def test_hard_task_preferred_roles_excludes_non_hard_requirement_rows():
    dataset = _dataset()
    hard = _hard_task_preferred_roles(dataset)
    for task_id in hard:
        t = dataset.task_requirements[task_id]
        level = classify_provenance(t, dataset)
        assert classify_hard_soft(t, level, dataset) == HardSoftLabel.HARD


def test_hard_task_preferred_roles_subset_of_all_task_preferred_roles():
    dataset = _dataset()
    hard = _hard_task_preferred_roles(dataset)
    all_roles = _task_preferred_roles(dataset)
    assert set(hard) <= set(all_roles)
    for task_id, roles in hard.items():
        assert roles == all_roles[task_id]


# --- F5: evidence citations attached to assignments ------------------------


def test_citations_for_returns_backing_hrlt_id_for_real_record():
    dataset = _dataset()
    sv = build_variables(dataset)
    # P-HESSE's presence window is (L-SALIDO, 0, 17), backed by HRLT-0003.
    citations = _citations_for(dataset, sv, "P-HESSE", "L-SALIDO", 5)
    assert citations == ["HRLT-0003"]


def test_citations_for_returns_empty_outside_presence_window():
    dataset = _dataset()
    sv = build_variables(dataset)
    citations = _citations_for(dataset, sv, "P-HESSE", "L-SOME-OTHER-PLACE", 5)
    assert citations == []


def test_scenario_output_assignments_carry_presence_citations(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=3)
    dataset = _dataset()

    scenario_files = sorted(output_dir.glob("scenario_*.json"))
    assert scenario_files
    for path in scenario_files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for a in payload["active_assignments"]:
            assert "presence_hrlt_ids" in a
            for hrlt_id in a["presence_hrlt_ids"]:
                rec = dataset.hrlt_records[hrlt_id]
                assert rec.human_or_group_id == a["human_or_group_id"]
                assert rec.location_id == a["location_id"]


# --- F6: run metadata ------------------------------------------------------


def test_validation_summary_includes_run_metadata(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    summary = json.loads((output_dir / "validation_summary.json").read_text(encoding="utf-8"))

    assert summary["run_metadata"]["schicht_count"] == 1
    assert summary["run_metadata"]["note"] == _RUN_METADATA_NOTE


# --- F7: penalty breakdown in scenario output ------------------------------


def test_scenario_output_includes_penalty_breakdown_with_six_categories(tmp_path):
    """The six objective.py categories must be present; task_switch/
    location_switch/role_switch/role_undocumented/role_contradicted are
    additional diagnostic-only keys (breakdowns of over_assignment and
    unsupported_assignments respectively) and may also appear."""
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=3)
    required_keys = {
        "archival_contradictions", "unsupported_assignments", "temporal_violations",
        "topological_violations", "role_location_penalties", "over_assignment",
    }
    for path in sorted(output_dir.glob("scenario_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert required_keys <= set(payload["penalty_breakdown"])
        breakdown = payload["penalty_breakdown"]
        assert (
            breakdown["task_switch"] + breakdown["location_switch"] + breakdown["role_switch"]
            == breakdown["over_assignment"]
        )
        assert (
            breakdown["role_undocumented"] + breakdown["role_contradicted"]
            == breakdown["unsupported_assignments"]
        )


def test_real_run_no_longer_dominated_by_idle_penalty(tmp_path):
    """Direct closing check for F1, visible from the artifact itself (per
    SOLVER_V0_1_1_FIX_PLAN.md's cross-cutting acceptance check #2): the
    real dataset's objective must no longer decompose as ~16 per idle
    aggregate group. v0.1 produced objective ~160; after the fix nothing
    in the model rewards assignment, so the true optimum is <= v0.1's."""
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    payload = json.loads((output_dir / "scenario_00.json").read_text(encoding="utf-8"))
    assert payload["objective_value"] < 160
    assert payload["penalty_breakdown"]["over_assignment"] < 160
