"""Validation-first provenance classification.

This module re-derives, from the actual loaded records, exactly the
granularity/hard-soft classification SOLVER_INPUT_READINESS.md worked out
by hand -- it does not trust that report as a frozen answer key. Where a
finding genuinely cannot be re-derived mechanically (it required reading
the surrounding archival passages, or the row's own free-text
`evidence_basis` declaring itself unresolved), it is looked up in
config.MANUAL_PROVENANCE_OVERRIDES / MANUAL_AMBIGUOUS_RECORD_IDS -- a small,
explicitly-cited registry, not a silent hardcoded answer.

hard_constraints.py / soft_constraints.py MUST run every record through
classify_hard_soft() before using it. A record classified AMBIGUOUS or
MISSING (composition-level) is never eligible for a hard constraint.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from salido_hdt.solver import config
from salido_hdt.solver.domain import (
    AdjacencyEdge,
    CompatibilityRule,
    Dataset,
    HardSoftLabel,
    HrltRecord,
    ProvenanceLevel,
    TaskRequirement,
)

#: Values that self-signal an unresolved disjunction or unresolved status.
#: "_or_" catches explicit_or_structural / explicit_or_translated /
#: approaches_or_audibly_connected. The other two are single tokens that
#: do not follow the "_or_" pattern but were established as ambiguous in
#: SOLVER_INPUT_READINESS.md §1.1/§1.5/§7 (uncertain -> relation/evidence
#: explicitly unknown; strong_interpretation -> a strength claim with no
#: field to verify it against).
_AMBIGUOUS_SINGLE_VALUES = {"uncertain", "strong_interpretation"}


def _is_ambiguous_value(value: str | None) -> bool:
    if not value:
        return False
    if "_or_" in value:
        return True
    return value in _AMBIGUOUS_SINGLE_VALUES


def _record_id(record) -> str:
    for attr in (
        "hrlt_id",
        "person_role_id",
        "compatibility_id",
        "edge_id",
        "task_id",
        "group_id",
        "inventory_item_id",
    ):
        value = getattr(record, attr, None)
        if value:
            return value
    return "<unknown>"


def classify_provenance(record, dataset: Dataset) -> ProvenanceLevel:
    """Re-derive provenance granularity for any domain record."""
    # 1. Ambiguity is checked first -- it overrides document/claim-level
    #    citation, because an unresolved evidence value means the citation
    #    itself does not settle what is being claimed.
    for attr in ("evidence_status", "relation_type", "constraint_type"):
        value = getattr(record, attr, None)
        if _is_ambiguous_value(value):
            return ProvenanceLevel.AMBIGUOUS

    record_id = _record_id(record)
    if record_id in config.MANUAL_AMBIGUOUS_RECORD_IDS:
        return ProvenanceLevel.AMBIGUOUS

    # 2. Inventory items: source_paragraph_index -> 00_source_passages join
    #    (SOLVER_INPUT_READINESS.md §8) -- the pre-existing v0.3 column, a
    #    different (and stronger) mechanism than the v0.4 source_passage_id
    #    column other tables use.
    paragraph_index = getattr(record, "source_paragraph_index", None)
    if paragraph_index is not None:
        passage = dataset.source_passages_by_paragraph_index.get(paragraph_index)
        if passage is not None:
            override = config.MANUAL_PROVENANCE_OVERRIDES.get(passage.source_passage_id)
            if override:
                return ProvenanceLevel(override)
            return ProvenanceLevel.CLAIM_LEVEL

    # 3. Tables with a source_passage_id column (00/02/04/06/07/09/10/11/05).
    passage_id = getattr(record, "source_passage_id", "")
    if passage_id:
        override = config.MANUAL_PROVENANCE_OVERRIDES.get(passage_id)
        if override:
            return ProvenanceLevel(override)
        return ProvenanceLevel.CLAIM_LEVEL

    # 4. Fall back to document-level citation.
    document_id = getattr(record, "source_document_id", "")
    if document_id:
        return ProvenanceLevel.DOCUMENT_LEVEL

    # 5. 14/15/16 have no source_document_id/source_passage_id column at
    #    all (SOLVER_INPUT_READINESS.md §5-7) -- structurally missing.
    return ProvenanceLevel.MISSING


def classify_hard_soft(record, level: ProvenanceLevel, dataset: Dataset) -> HardSoftLabel:
    """Per SOLVER_INPUT_READINESS.md §9's loadability rules."""
    if level == ProvenanceLevel.AMBIGUOUS:
        return HardSoftLabel.SOFT

    if level in (ProvenanceLevel.CLAIM_LEVEL, ProvenanceLevel.DOCUMENT_LEVEL):
        return HardSoftLabel.HARD

    if level == ProvenanceLevel.SECTION_LEVEL:
        # Section-level provenance is sufficient for entity grouping
        # (presence) but not for a detailed quantity/role assignment --
        # the exact distinction the SP-01236 investigation established.
        if isinstance(record, HrltRecord) and not record.role_id:
            return HardSoftLabel.HARD
        return HardSoftLabel.CONTEXT_ONLY

    # level == MISSING: 14/15/16 carry no citation column at all. Their own
    # declared strength is provisionally honoured here; hard_constraints.py
    # additionally re-verifies corroboration against 04/07 before actually
    # building a constraint from one of these (SOLVER_INPUT_READINESS.md's
    # own recommendation -- "resolve the corroboration join explicitly").
    if isinstance(record, CompatibilityRule):
        return HardSoftLabel.HARD if record.constraint_type.startswith("hard") else HardSoftLabel.SOFT
    if isinstance(record, AdjacencyEdge):
        clean = {"explicit", "explicit_route"}
        return HardSoftLabel.HARD if record.evidence_status in clean else HardSoftLabel.SOFT
    if isinstance(record, TaskRequirement):
        return HardSoftLabel.HARD if record.constraint_strength.startswith("hard") else HardSoftLabel.SOFT
    return HardSoftLabel.SOFT


@dataclass(frozen=True)
class ClassifiedRecord:
    record_id: str
    table: str
    provenance: ProvenanceLevel
    label: HardSoftLabel


@dataclass(frozen=True)
class ValidationReport:
    total_records: int
    classified: tuple[ClassifiedRecord, ...] = field(default_factory=tuple)

    @property
    def excluded_from_hard(self) -> tuple[ClassifiedRecord, ...]:
        return tuple(c for c in self.classified if c.label != HardSoftLabel.HARD)

    @property
    def hard_eligible(self) -> tuple[ClassifiedRecord, ...]:
        return tuple(c for c in self.classified if c.label == HardSoftLabel.HARD)


def _classify_table(records: dict, table: str, dataset: Dataset) -> list[ClassifiedRecord]:
    out = []
    for record_id, record in records.items():
        level = classify_provenance(record, dataset)
        label = classify_hard_soft(record, level, dataset)
        out.append(ClassifiedRecord(record_id, table, level, label))
    return out


def validate_dataset(dataset: Dataset) -> ValidationReport:
    """Run provenance + hard/soft classification over every solver-input
    candidate table. This MUST run before variables.py/hard_constraints.py
    build anything -- that is what makes this solver 'validation-first'."""
    classified: list[ClassifiedRecord] = []
    classified += _classify_table(dataset.person_roles, "04_person_roles", dataset)
    classified += _classify_table(dataset.hrlt_records, "07_hrlt", dataset)
    classified += _classify_table(dataset.inventory_items, "10_inventory_items", dataset)
    classified += _classify_table(dataset.task_requirements, "14_task_requirements", dataset)
    classified += _classify_table(
        dataset.compatibility_rules, "15_role_location_compatibility", dataset
    )
    classified += _classify_table(dataset.adjacency_edges, "16_location_adjacency", dataset)

    return ValidationReport(total_records=len(classified), classified=tuple(classified))
