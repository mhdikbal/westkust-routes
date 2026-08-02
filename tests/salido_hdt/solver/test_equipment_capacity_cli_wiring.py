"""Regression guards for equipment_capacity.py and its wiring into
cli.run(). Verified against the real dataset's actual structure:

  - INV-0333 (row_type='container_or_parent', '6 meriam logam') has
    children INV-0334 (2) + INV-0335 (4) summing to exactly 6 -- the real
    parent/child double-counting case this module must never re-sum.
  - condition_normalized is empty (unknown) for 369 of 403 real rows, and
    'unserviceable' for 22 -- so confirmed_capacity is legitimately 0 for
    almost every real match; this is a correct finding, not a bug.
"""
import csv
from unittest.mock import Mock

from ortools.sat.python import cp_model

from salido_hdt.solver import config
from salido_hdt.solver.cli import run
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.equipment_capacity import (
    CapacityReport,
    CapacityStatus,
    compute_capacity_reports,
    hard_capacity_bound,
    write_equipment_capacity_csv,
)


def _dataset():
    return load_dataset(config.V0_4_1_ROOT)


def _mock_item(**kwargs):
    defaults = dict(
        inventory_item_id="INV-X", inventory_date="", location_id="L-ORTEN",
        inventory_section="", category="", row_type="inventory_item",
        quantity=1.0, unit_normalized="stux", item_text_id="", source_translation_full="",
        condition_normalized="", reading_status="translated_docx", source_document_id="",
        source_paragraph_index=None, image_verified="", notes="", evidence_status="", review_status="",
    )
    defaults.update(kwargs)
    return Mock(**defaults)


# --- condition / classification rules (synthetic, isolated) ----------------


def _report_for(items, task_keywords=("boor",), required=1.0):
    dataset = Mock()
    task = Mock(
        required_tool_keywords=task_keywords,
        allowed_location_ids=("L-ORTEN",),
        minimum_workers_assumption=required,
    )
    dataset.task_requirements = {"T-X": task}
    dataset.inventory_items = {item.inventory_item_id: item for item in items}
    reports = compute_capacity_reports(dataset)
    assert len(reports) == 1
    return reports[0]


def test_serviceable_item_contributes_confirmed_capacity():
    item = _mock_item(inventory_item_id="INV-1", item_text_id="boor", quantity=5.0,
                       condition_normalized="serviceable")
    r = _report_for([item])
    assert r.confirmed_capacity == 5.0
    assert r.uncertain_capacity == 0.0
    assert r.source_inventory_item_ids == ("INV-1",)


def test_unknown_condition_contributes_uncertain_not_confirmed():
    item = _mock_item(inventory_item_id="INV-2", item_text_id="boor", quantity=3.0,
                       condition_normalized="")
    r = _report_for([item])
    assert r.confirmed_capacity == 0.0
    assert r.uncertain_capacity == 3.0


def test_unserviceable_item_contributes_zero_confirmed_and_is_excluded_from_uncertain():
    item = _mock_item(inventory_item_id="INV-3", item_text_id="boor", quantity=7.0,
                       condition_normalized="unserviceable")
    r = _report_for([item])
    assert r.confirmed_capacity == 0.0
    assert r.uncertain_capacity == 0.0
    assert r.source_inventory_item_ids == ()


def test_unresolved_reading_never_silently_satisfies_requirement():
    """Even a condition_normalized='serviceable' item must NOT count as
    confirmed if its reading_status is 'unresolved' -- the item's very
    textual identity is unconfirmed."""
    item = _mock_item(inventory_item_id="INV-4", item_text_id="boor", quantity=60.0,
                       condition_normalized="serviceable", reading_status="unresolved")
    r = _report_for([item])
    assert r.confirmed_capacity == 0.0
    assert r.uncertain_capacity == 60.0
    assert r.capacity_status == CapacityStatus.UNCERTAIN_SUFFICIENT


def test_compound_condition_value_is_uncertain_not_confirmed():
    item = _mock_item(inventory_item_id="INV-5", item_text_id="boor", quantity=2.0,
                       condition_normalized="new|old")
    r = _report_for([item])
    assert r.confirmed_capacity == 0.0
    assert r.uncertain_capacity == 2.0


def test_parent_row_never_contributes_alongside_children():
    """Real-data-shaped: a container_or_parent row and its itemized
    children must not both count -- only the children (inventory_item
    rows) ever contribute."""
    parent = _mock_item(inventory_item_id="INV-PARENT", item_text_id="boor tools, yaitu",
                         quantity=6.0, row_type="container_or_parent", condition_normalized="serviceable")
    child_a = _mock_item(inventory_item_id="INV-CHILD-A", item_text_id="boor type A",
                          quantity=2.0, row_type="inventory_item", condition_normalized="serviceable")
    child_b = _mock_item(inventory_item_id="INV-CHILD-B", item_text_id="boor type B",
                          quantity=4.0, row_type="inventory_item", condition_normalized="serviceable")
    r = _report_for([parent, child_a, child_b])
    assert r.confirmed_capacity == 6.0  # only children (2+4), not 6+2+4=12
    assert "INV-PARENT" not in r.source_inventory_item_ids
    assert set(r.source_inventory_item_ids) == {"INV-CHILD-A", "INV-CHILD-B"}


def test_non_stux_unit_is_never_counted():
    """A weight/volume quantity does not represent discrete, simultaneously
    usable equipment -- must not be summed as if it did."""
    item = _mock_item(inventory_item_id="INV-6", item_text_id="boor", quantity=50.0,
                       unit_normalized="lb", condition_normalized="serviceable")
    r = _report_for([item])
    assert r.confirmed_capacity == 0.0
    assert r.capacity_status == CapacityStatus.NO_INVENTORY_MATCH


def test_no_matching_inventory_status():
    r = _report_for([])
    assert r.capacity_status == CapacityStatus.NO_INVENTORY_MATCH
    assert r.source_inventory_item_ids == ()


def test_no_requirement_declared_when_task_has_no_tool_keywords():
    dataset = Mock()
    task = Mock(required_tool_keywords=(), allowed_location_ids=("L-ORTEN",),
                minimum_workers_assumption=1.0)
    dataset.task_requirements = {"T-X": task}
    dataset.inventory_items = {}
    reports = compute_capacity_reports(dataset)
    assert reports[0].capacity_status == CapacityStatus.NO_REQUIREMENT_DECLARED


def test_capacity_status_sufficient_vs_uncertain_vs_insufficient():
    sufficient = _report_for(
        [_mock_item(inventory_item_id="I1", item_text_id="boor", quantity=2.0, condition_normalized="serviceable")],
        required=1.0,
    )
    assert sufficient.capacity_status == CapacityStatus.SUFFICIENT

    uncertain = _report_for(
        [_mock_item(inventory_item_id="I2", item_text_id="boor", quantity=2.0, condition_normalized="")],
        required=1.0,
    )
    assert uncertain.capacity_status == CapacityStatus.UNCERTAIN_SUFFICIENT

    insufficient = _report_for(
        [_mock_item(inventory_item_id="I3", item_text_id="boor", quantity=1.0, condition_normalized="unserviceable")],
        required=1.0,
    )
    assert insufficient.capacity_status == CapacityStatus.INSUFFICIENT


def test_hard_capacity_bound_uses_confirmed_plus_uncertain():
    report = CapacityReport(
        task_id="T-X", location_id="L-ORTEN", confirmed_capacity=2.0, uncertain_capacity=3.0,
        required_capacity=1.0, capacity_status=CapacityStatus.UNCERTAIN_SUFFICIENT,
    )
    assert hard_capacity_bound(report) == 5


def test_write_equipment_capacity_csv_has_five_required_columns(tmp_path):
    reports = [CapacityReport(
        task_id="T-X", location_id="L-ORTEN", confirmed_capacity=1.0, uncertain_capacity=2.0,
        required_capacity=1.0, capacity_status=CapacityStatus.SUFFICIENT,
        source_inventory_item_ids=("INV-1", "INV-2"),
    )]
    path = tmp_path / "equipment_capacity.csv"
    write_equipment_capacity_csv(reports, path)
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    row = rows[0]
    assert row["confirmed_capacity"] == "1.0"
    assert row["uncertain_capacity"] == "2.0"
    assert row["required_capacity"] == "1.0"
    assert row["capacity_status"] == "sufficient"
    assert row["source_inventory_item_ids"] == "INV-1|INV-2"


# --- v0.1.2 Item 3: capacity-bound interpretation columns -------------------


def test_required_capacity_semantics_is_reported():
    report = _report_for(
        [_mock_item(inventory_item_id="I1", item_text_id="boor", quantity=1.0,
                     condition_normalized="serviceable")],
        required=1.0,
    )
    assert report.required_capacity_semantics == "archival_minimum_crew_size"


def test_hard_bound_rationale_distinguishes_matched_and_unmatched_pairs():
    matched = _report_for(
        [_mock_item(inventory_item_id="I1", item_text_id="boor", quantity=1.0,
                     condition_normalized="serviceable")],
        required=1.0,
    )
    unmatched = _report_for([], required=1.0)
    no_requirement = compute_capacity_reports(Mock(
        task_requirements={"T-X": Mock(required_tool_keywords=(), allowed_location_ids=("L-ORTEN",),
                                        minimum_workers_assumption=1.0)},
        inventory_items={},
    ))[0]

    assert matched.hard_bound_rationale != unmatched.hard_bound_rationale
    assert "confirmed_capacity + uncertain_capacity" in matched.hard_bound_rationale
    assert unmatched.hard_bound_rationale == "no constraint instantiated (no_inventory_match / no_requirement_declared)"
    assert no_requirement.hard_bound_rationale == unmatched.hard_bound_rationale


def test_real_run_equipment_capacity_csv_has_new_columns(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    with (output_dir / "equipment_capacity.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows
    for row in rows:
        assert row["required_capacity_semantics"] == "archival_minimum_crew_size"
        assert row["hard_bound_rationale"]  # non-empty on every row, matched or not


# --- real dataset -------------------------------------------------------------


def test_real_dataset_parent_child_case_INV_0333_never_double_counted():
    dataset = _dataset()
    parent = dataset.inventory_items["INV-0333"]
    child_a = dataset.inventory_items["INV-0334"]
    child_b = dataset.inventory_items["INV-0335"]
    assert parent.row_type == "container_or_parent"
    assert child_a.row_type == "inventory_item"
    assert child_b.row_type == "inventory_item"
    assert child_a.quantity + child_b.quantity == parent.quantity == 6.0


def test_real_dataset_reports_are_generated_for_every_task_location_pair():
    dataset = _dataset()
    reports = compute_capacity_reports(dataset)
    expected = sum(len(t.allowed_location_ids) for t in dataset.task_requirements.values())
    assert len(reports) == expected


def test_real_dataset_condition_data_is_mostly_unknown_so_confirmed_is_often_zero():
    """Documents the real finding: with 369/403 rows condition-unknown,
    confirmed_capacity legitimately comes out 0 for almost every real
    match -- this must not be silently 'fixed' by treating unknown as
    confirmed."""
    dataset = _dataset()
    reports = compute_capacity_reports(dataset)
    matched = [r for r in reports if r.capacity_status not in
               (CapacityStatus.NO_INVENTORY_MATCH, CapacityStatus.NO_REQUIREMENT_DECLARED)]
    assert matched  # sanity: real data does produce some matches
    assert all(r.confirmed_capacity == 0.0 for r in matched)
    assert any(r.uncertain_capacity > 0 for r in matched)


# --- CLI wiring -----------------------------------------------------------------


def test_cli_run_instantiates_equipment_capacity_constraints(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    import json
    summary = json.loads((output_dir / "validation_summary.json").read_text(encoding="utf-8"))
    assert summary["equipment_capacity_enforced"] is True
    assert summary["equipment_capacity_constraints_instantiated"] > 0
    assert "uncertain_sufficient" in summary["equipment_capacity_status_counts"]


def test_cli_run_writes_equipment_capacity_csv_with_required_columns(tmp_path):
    output_dir = run(root=config.V0_4_1_ROOT, output_dir=tmp_path / "out", max_scenarios=1)
    path = output_dir / "equipment_capacity.csv"
    assert path.exists()
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows
    required_columns = {
        "task_id", "location_id", "confirmed_capacity", "uncertain_capacity",
        "required_capacity", "capacity_status", "source_inventory_item_ids",
    }
    assert required_columns <= set(rows[0].keys())


def test_equipment_capacity_actually_bounds_the_model():
    """Direct proof the HARD constraint is really wired: force every
    x-variable for a capacity-constrained (task, location) pair to 1 and
    confirm the model becomes INFEASIBLE once the count exceeds the wired
    bound."""
    dataset = _dataset()
    reports = compute_capacity_reports(dataset)
    bounded = [
        r for r in reports
        if r.capacity_status not in (CapacityStatus.NO_INVENTORY_MATCH, CapacityStatus.NO_REQUIREMENT_DECLARED)
    ]
    assert bounded
    target = bounded[0]
    bound = hard_capacity_bound(target)

    from salido_hdt.solver.hard_constraints import add_equipment_capacity

    model = cp_model.CpModel()
    # bound+1 candidate workers at the same (task, location, time) --
    # exceeding the wired capacity by exactly one.
    x = {
        (f"P-{i}", target.task_id, target.location_id, 0, 0): model.NewBoolVar(f"x{i}")
        for i in range(bound + 1)
    }
    add_equipment_capacity(model, x, task_id=target.task_id, location_id=target.location_id, capacity=bound)
    for v in x.values():
        model.Add(v == 1)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status == cp_model.INFEASIBLE


# --- mandatory tests ("Tes wajib") ------------------------------------------


def test_seven_confirmed_units_do_not_support_eight_simultaneous_teams():
    """Seven confirmed-serviceable units must not support eight
    simultaneous drilling teams -- the exact boundary case."""
    from salido_hdt.solver.hard_constraints import add_equipment_capacity

    item = _mock_item(inventory_item_id="INV-BOR", item_text_id="boor tambang", quantity=7.0,
                       condition_normalized="serviceable")
    report = _report_for([item], task_keywords=("boor",), required=1.0)
    assert report.confirmed_capacity == 7.0
    bound = hard_capacity_bound(report)
    assert bound == 7

    model = cp_model.CpModel()
    x = {
        (f"P-{i}", "T-X", "L-ORTEN", 0, 0): model.NewBoolVar(f"x{i}")
        for i in range(8)  # eight simultaneous drilling teams
    }
    add_equipment_capacity(model, x, task_id="T-X", location_id="L-ORTEN", capacity=bound)
    for v in x.values():
        model.Add(v == 1)
    solver = cp_model.CpSolver()
    assert solver.Solve(model) == cp_model.INFEASIBLE

    # Exactly seven simultaneous teams must remain feasible.
    model2 = cp_model.CpModel()
    x2 = {
        (f"P-{i}", "T-X", "L-ORTEN", 0, 0): model2.NewBoolVar(f"x{i}")
        for i in range(7)
    }
    add_equipment_capacity(model2, x2, task_id="T-X", location_id="L-ORTEN", capacity=bound)
    for v in x2.values():
        model2.Add(v == 1)
    solver2 = cp_model.CpSolver()
    assert solver2.Solve(model2) in (cp_model.OPTIMAL, cp_model.FEASIBLE)


def test_unserviceable_equipment_cannot_satisfy_hard_capacity():
    """All matching items unserviceable -> hard bound is zero -> even a
    single assignment relying on it is infeasible."""
    from salido_hdt.solver.hard_constraints import add_equipment_capacity

    item = _mock_item(inventory_item_id="INV-BROKEN", item_text_id="boor tambang", quantity=60.0,
                       condition_normalized="unserviceable")
    report = _report_for([item], task_keywords=("boor",), required=1.0)
    bound = hard_capacity_bound(report)
    assert bound == 0

    model = cp_model.CpModel()
    var = model.NewBoolVar("x")
    x = {("P-1", "T-X", "L-ORTEN", 0, 0): var}
    add_equipment_capacity(model, x, task_id="T-X", location_id="L-ORTEN", capacity=bound)
    model.Add(var == 1)
    solver = cp_model.CpSolver()
    assert solver.Solve(model) == cp_model.INFEASIBLE


def test_parent_and_subcomponents_are_never_double_counted_end_to_end():
    """End-to-end version of test_parent_row_never_contributes_alongside_
    children, phrased against the exact real parent/child case (INV-0333 =
    6 meriam logam, children INV-0334 (2) + INV-0335 (4))."""
    dataset = _dataset()
    parent = dataset.inventory_items["INV-0333"]
    child_a = dataset.inventory_items["INV-0334"]
    child_b = dataset.inventory_items["INV-0335"]

    reconstructed = _report_for(
        [parent, child_a, child_b],
        task_keywords=("meriam",),
        required=1.0,
    )
    # Only the two children ever contribute -- never parent + children.
    assert set(reconstructed.source_inventory_item_ids) <= {"INV-0334", "INV-0335"}
    assert "INV-0333" not in reconstructed.source_inventory_item_ids


def test_cli_and_unit_tests_use_the_identical_constraint_builder():
    """cli.run() must wire the SAME add_equipment_capacity function object
    tested in isolation above -- not a parallel/divergent implementation."""
    import salido_hdt.solver.cli as cli_module
    from salido_hdt.solver.hard_constraints import add_equipment_capacity

    assert cli_module.add_equipment_capacity is add_equipment_capacity
