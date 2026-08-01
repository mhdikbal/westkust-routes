"""Frozen domain model for the SALIDO-HDT solver.

Every dataclass here is immutable (frozen=True) on purpose: nothing in this
package should ever construct a mutable view of the canonical v0.4.1 CSVs.
Field names mirror the CSV column names 1:1 so a record's provenance can be
re-derived directly from its own attributes (see validation.py) without a
separate lookup table.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Optional


class ProvenanceLevel(enum.Enum):
    """How granular a record's citation is, per SOLVER_INPUT_READINESS.md §2."""

    CLAIM_LEVEL = "claim_level"
    SECTION_LEVEL = "section_level"
    DOCUMENT_LEVEL = "document_level"
    MISSING = "missing"
    AMBIGUOUS = "ambiguous"


class HardSoftLabel(enum.Enum):
    """Where a record may be loaded, per SOLVER_INPUT_READINESS.md §9."""

    HARD = "hard"
    SOFT = "soft"
    CONTEXT_ONLY = "context_only"


class EntityType(enum.Enum):
    INDIVIDUAL = "individual"
    AGGREGATE_GROUP = "aggregate_group"


@dataclass(frozen=True)
class SourcePassage:
    source_passage_id: str
    docx_file: str
    source_document_id: str
    paragraph_index: int
    style: str
    text: str
    review_status: str
    image_verified: str


@dataclass(frozen=True)
class Document:
    document_id: str
    title: str
    date_original: str
    date_iso: str
    archive_repository: str
    archive_access: str
    inventory_number: str
    source_file: str
    document_type: str
    status: str


@dataclass(frozen=True)
class Role:
    role_id: str
    role_original: str
    role_description_id: str
    role_family: str


@dataclass(frozen=True)
class Person:
    person_id: str
    name_canonical: str
    entity_level: str
    source_status: str
    identity_confidence: Optional[float]
    notes: str


@dataclass(frozen=True)
class PersonRole:
    person_role_id: str
    person_id: str
    role_id: str
    role_original: str
    valid_from: str
    valid_to: str
    evidence_status: str
    source_document_id: str
    confidence: Optional[float]
    review_status: str = ""
    source_passage_id: str = ""


@dataclass(frozen=True)
class Location:
    location_id: str
    name_original: str
    name_normalized_id: str
    location_type: str
    parent_location_id: str
    evidence_status: str


@dataclass(frozen=True)
class HumanGroup:
    group_id: str
    source_category_original: str
    count: int
    status_category: str
    growth_category_original: str
    sex_category_original: str
    location_id: str
    evidence_status: str
    source_document_id: str
    source_passage_id: str = ""
    review_status: str = ""


@dataclass(frozen=True)
class HrltRecord:
    """A row of 07_human_role_location_time.csv -- the sparse HRLT tensor."""

    hrlt_id: str
    human_or_group_id: str
    entity_type: EntityType
    role_id: str
    location_id: str
    valid_from: str
    valid_to: str
    assignment_value: Optional[float]
    evidence_status: str
    source_quote: str
    source_document_id: str
    confidence: Optional[float]
    review_status: str
    source_passage_id: str = ""


@dataclass(frozen=True)
class InventoryItem:
    inventory_item_id: str
    inventory_date: str
    location_id: str
    inventory_section: str
    category: str
    row_type: str
    quantity: Optional[float]
    unit_normalized: str
    item_text_id: str
    source_translation_full: str
    condition_normalized: str
    reading_status: str
    source_document_id: str
    source_paragraph_index: Optional[int]
    image_verified: str
    notes: str
    evidence_status: str = ""
    review_status: str = ""


@dataclass(frozen=True)
class TaskRequirement:
    task_id: str
    task_name: str
    task_family: str
    allowed_location_ids: tuple[str, ...]
    required_skill_ids: tuple[str, ...]
    preferred_role_ids: tuple[str, ...]
    required_tool_keywords: tuple[str, ...]
    minimum_workers_assumption: Optional[float]
    constraint_strength: str
    evidence_basis: str
    review_status: str


@dataclass(frozen=True)
class CompatibilityRule:
    compatibility_id: str
    role_id: str
    location_id: str
    compatibility_score: Optional[float]
    constraint_type: str
    evidence_basis: str
    review_status: str


@dataclass(frozen=True)
class AdjacencyEdge:
    edge_id: str
    from_location_id: str
    to_location_id: str
    relation_type: str
    bidirectional: bool
    evidence_status: str
    evidence_basis: str
    distance_original: str
    distance_normalized: Optional[float]
    review_status: str


@dataclass(frozen=True)
class Dataset:
    """Everything load_dataset() reads from v0.4.1, plus its own read-only proof."""

    source_passages: dict[str, SourcePassage]
    source_passages_by_paragraph_index: dict[int, SourcePassage]
    documents: dict[str, Document]
    roles: dict[str, Role]
    persons: dict[str, Person]
    person_roles: dict[str, PersonRole]
    locations: dict[str, Location]
    human_groups: dict[str, HumanGroup]
    hrlt_records: dict[str, HrltRecord]
    inventory_items: dict[str, InventoryItem]
    task_requirements: dict[str, TaskRequirement]
    compatibility_rules: dict[str, CompatibilityRule]
    adjacency_edges: dict[str, AdjacencyEdge]
    file_hashes: dict[str, str] = field(default_factory=dict)
    root: str = ""
