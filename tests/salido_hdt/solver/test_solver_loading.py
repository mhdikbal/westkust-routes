"""data_loader must load v0.4.1 read-only and produce a consistent Dataset."""
import csv

from salido_hdt.solver import config
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.domain import EntityType


def _real_csv_row_count(filename: str) -> int:
    path = config.V0_4_1_ROOT / filename
    with open(path, encoding="utf-8-sig", newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


def test_loads_real_v0_4_1_dataset():
    dataset = load_dataset(config.V0_4_1_ROOT)
    assert dataset.root == str(config.V0_4_1_ROOT)


def test_row_counts_match_actual_csvs():
    dataset = load_dataset(config.V0_4_1_ROOT)
    assert len(dataset.persons) == _real_csv_row_count("02_persons.csv")
    assert len(dataset.roles) == _real_csv_row_count("03_roles.csv")
    assert len(dataset.person_roles) == _real_csv_row_count("04_person_roles.csv")
    assert len(dataset.locations) == _real_csv_row_count("05_locations.csv")
    assert len(dataset.human_groups) == _real_csv_row_count("06_human_groups.csv")
    assert len(dataset.hrlt_records) == _real_csv_row_count(
        "07_human_role_location_time.csv"
    )
    assert len(dataset.inventory_items) == _real_csv_row_count("10_inventory_items.csv")
    assert len(dataset.task_requirements) == _real_csv_row_count(
        "14_task_requirements.csv"
    )
    assert len(dataset.compatibility_rules) == _real_csv_row_count(
        "15_role_location_compatibility.csv"
    )
    assert len(dataset.adjacency_edges) == _real_csv_row_count(
        "16_location_adjacency.csv"
    )
    assert len(dataset.source_passages) == _real_csv_row_count("00_source_passages.csv")


def test_person_role_has_review_status_and_source_passage_id_fields():
    """04_person_roles.csv gained source_passage_id/review_status in v0.4
    (MIG-013) -- both present as columns, empty for all 47 rows per
    SOLVER_INPUT_READINESS.md §3. Regression guard: domain.PersonRole must
    expose both fields, not silently drop the column."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    pr = dataset.person_roles["PR-OLITSCH"]
    assert pr.source_passage_id == ""
    assert pr.review_status == ""


def test_hrlt_entity_type_parsed_as_enum():
    dataset = load_dataset(config.V0_4_1_ROOT)
    hrlt0006 = dataset.hrlt_records["HRLT-0006"]
    assert hrlt0006.entity_type == EntityType.AGGREGATE_GROUP
    assert hrlt0006.human_or_group_id == "G-MS-121"

    hrlt0001 = dataset.hrlt_records["HRLT-0001"]
    assert hrlt0001.entity_type == EntityType.INDIVIDUAL
    assert hrlt0001.human_or_group_id == "P-VOGEL"


def test_v0_4_1_backfilled_source_passage_id_loaded_correctly():
    """Sanity check on the v0.4.1 backfill this whole chain produced."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    assert dataset.hrlt_records["HRLT-0006"].source_passage_id == "SP-01236"
    assert dataset.hrlt_records["HRLT-0015"].source_passage_id == "SP-01236"
    # HRLT-0001..0005 were deliberately left empty by the v0.4.1 backfill
    # (no unique passage match) -- must still be empty, not guessed.
    assert dataset.hrlt_records["HRLT-0001"].source_passage_id == ""


def test_source_paragraph_index_join_resolves_for_inventory():
    """10_inventory_items.source_paragraph_index -> 00_source_passages join,
    the mechanism SOLVER_INPUT_READINESS.md §8 relies on for claim_level
    equipment provenance (INV-0232, 60 bor tambang)."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    inv_0232 = dataset.inventory_items["INV-0232"]
    assert inv_0232.source_paragraph_index == 1108
    passage = dataset.source_passages_by_paragraph_index[1108]
    assert passage.source_passage_id == "SP-01108"
    assert "bor tambang" in passage.text
    assert inv_0232.quantity == 60


def test_load_never_opens_files_in_write_mode(monkeypatch):
    """Guard the read-only promise at the builtins.open() level."""
    import builtins

    real_open = builtins.open
    seen_modes = []

    def spying_open(file, mode="r", *args, **kwargs):
        seen_modes.append(mode)
        return real_open(file, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", spying_open)
    load_dataset(config.V0_4_1_ROOT)
    forbidden = {"w", "a", "x", "w+", "a+", "x+", "r+"}
    for mode in seen_modes:
        normalized = mode.replace("b", "").replace("t", "")
        assert normalized not in forbidden, f"data_loader opened a file with mode={mode!r}"
