"""validation.py is the 'validation-first' gate: it must re-derive
provenance/hard-soft classification from the actual data (not trust a
frozen memo) and match every finding SOLVER_INPUT_READINESS.md recorded
for the real v0.4.1 dataset."""
from salido_hdt.solver import config
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.domain import HardSoftLabel, ProvenanceLevel
from salido_hdt.solver.validation import (
    classify_hard_soft,
    classify_provenance,
    validate_dataset,
)


def test_sp_01236_backfilled_hrlt_rows_are_section_level():
    """§1/§4 of SOLVER_INPUT_READINESS.md: all 10 HRLT-0006..0015 cite the
    section-heading passage SP-01236, via the config.py manual override."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    for hrlt_id in [f"HRLT-{i:04d}" for i in range(6, 16)]:
        record = dataset.hrlt_records[hrlt_id]
        assert record.source_passage_id == "SP-01236"
        level = classify_provenance(record, dataset)
        assert level == ProvenanceLevel.SECTION_LEVEL


def test_sp_01236_rows_are_hard_for_presence_not_for_composition():
    """§9: section-level supports the group-at-location claim these HRLT
    rows actually make (role_id is empty on all 10 -- presence only), so
    they may anchor HARD temporal/presence constraints. They must NOT be
    usable as a hard constraint on a specific composition count -- that
    distinction is what classify_hard_soft has to encode."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    record = dataset.hrlt_records["HRLT-0006"]
    assert record.role_id == ""
    level = classify_provenance(record, dataset)
    label = classify_hard_soft(record, level, dataset)
    assert label == HardSoftLabel.HARD  # presence claim only


def test_hrlt_0001_through_0005_are_document_level():
    """§4: named-individual rows whose source_quote does not uniquely match
    any passage (v0.4.1 correctly left them un-backfilled)."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    for hrlt_id in [f"HRLT-{i:04d}" for i in range(1, 6)]:
        record = dataset.hrlt_records[hrlt_id]
        assert record.source_passage_id == ""
        assert classify_provenance(record, dataset) == ProvenanceLevel.DOCUMENT_LEVEL


def test_person_roles_explicit_are_document_level_hard():
    dataset = load_dataset(config.V0_4_1_ROOT)
    pr = dataset.person_roles["PR-OLITSCH"]
    assert pr.evidence_status == "explicit"
    level = classify_provenance(pr, dataset)
    assert level == ProvenanceLevel.DOCUMENT_LEVEL
    assert classify_hard_soft(pr, level, dataset) == HardSoftLabel.HARD


def test_manual_ambiguous_compatibility_rules_never_hard():
    """§6: RLC-0027/0029/0031's own evidence_basis says group identity is
    unknown -- config.MANUAL_AMBIGUOUS_RECORD_IDS. Must classify AMBIGUOUS
    and must never be HARD."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    for rlc_id in config.MANUAL_AMBIGUOUS_RECORD_IDS:
        rule = dataset.compatibility_rules[rlc_id]
        level = classify_provenance(rule, dataset)
        assert level == ProvenanceLevel.AMBIGUOUS
        assert classify_hard_soft(rule, level, dataset) != HardSoftLabel.HARD


def test_compatibility_rule_hard_type_without_ambiguity_is_hard_eligible():
    dataset = load_dataset(config.V0_4_1_ROOT)
    rule = dataset.compatibility_rules["RLC-0011"]  # constraint_type=hard
    assert rule.constraint_type == "hard"
    level = classify_provenance(rule, dataset)
    label = classify_hard_soft(rule, level, dataset)
    assert label == HardSoftLabel.HARD


def test_adjacency_or_pattern_evidence_is_ambiguous():
    """§7: 9 rows with evidence_status='explicit_or_structural' plus
    LE-0017/0018/0019 -- 12 total ambiguous rows, none safe for hard
    topological-feasibility exclusion."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    ambiguous_ids = {
        "LE-0003", "LE-0004", "LE-0005", "LE-0006", "LE-0007",
        "LE-0008", "LE-0009", "LE-0010", "LE-0011",
        "LE-0017", "LE-0018", "LE-0019",
    }
    for edge_id in ambiguous_ids:
        edge = dataset.adjacency_edges[edge_id]
        level = classify_provenance(edge, dataset)
        assert level == ProvenanceLevel.AMBIGUOUS, f"{edge_id} should be ambiguous"
        assert classify_hard_soft(edge, level, dataset) != HardSoftLabel.HARD


def test_adjacency_clean_explicit_rows_are_hard_eligible():
    dataset = load_dataset(config.V0_4_1_ROOT)
    clean_ids = {
        "LE-0001", "LE-0002", "LE-0012", "LE-0013", "LE-0014",
        "LE-0015", "LE-0016", "LE-0020", "LE-0021",
    }
    for edge_id in clean_ids:
        edge = dataset.adjacency_edges[edge_id]
        level = classify_provenance(edge, dataset)
        assert level != ProvenanceLevel.AMBIGUOUS, f"{edge_id} should not be ambiguous"
        label = classify_hard_soft(edge, level, dataset)
        assert label == HardSoftLabel.HARD


def test_inventory_claim_level_via_paragraph_index_join():
    """§8: INV-0232 (60 bor tambang) is claim_level via the
    source_paragraph_index -> 00_source_passages join, but its
    reading_status=unresolved caveat must still surface."""
    dataset = load_dataset(config.V0_4_1_ROOT)
    item = dataset.inventory_items["INV-0232"]
    level = classify_provenance(item, dataset)
    assert level == ProvenanceLevel.CLAIM_LEVEL
    assert item.reading_status == "unresolved"


def test_validate_dataset_produces_full_report():
    dataset = load_dataset(config.V0_4_1_ROOT)
    report = validate_dataset(dataset)
    assert report.total_records > 0
    assert report.excluded_from_hard  # at least RLC-0027/29/31 + 12 LE rows
    excluded_ids = {r.record_id for r in report.excluded_from_hard}
    assert "RLC-0027" in excluded_ids
    assert "LE-0018" in excluded_ids
