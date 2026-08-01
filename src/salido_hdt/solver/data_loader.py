"""Read-only loader for the SALIDO-HDT v0.4.1 canonical dataset.

Every file this module touches is opened via `open(path, "r", ...)`
(csv.DictReader's default) -- never "w"/"a"/"x". This is the single choke
point all solver code goes through to read the dataset, which is what
test_no_source_mutation.py verifies at the builtins.open() level.
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Optional

from salido_hdt.solver.domain import (
    AdjacencyEdge,
    CompatibilityRule,
    Dataset,
    Document,
    EntityType,
    HrltRecord,
    HumanGroup,
    InventoryItem,
    Location,
    Person,
    PersonRole,
    Role,
    SourcePassage,
    TaskRequirement,
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _hash_file(path: Path) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _opt_float(value: str) -> Optional[float]:
    value = (value or "").strip()
    return float(value) if value else None


def _opt_int(value: str) -> Optional[int]:
    value = (value or "").strip()
    return int(value) if value else None


def _pipe_list(value: str) -> tuple[str, ...]:
    value = (value or "").strip()
    return tuple(v.strip() for v in value.split("|") if v.strip())


def load_dataset(root: Path) -> Dataset:
    """Load every canonical table this solver needs from `root` (v0.4.1),
    read-only, returning an immutable Dataset."""
    root = Path(root)
    file_hashes: dict[str, str] = {}

    def load(filename: str) -> list[dict[str, str]]:
        path = root / filename
        file_hashes[filename] = _hash_file(path)
        return _read_csv(path)

    source_passages: dict[str, SourcePassage] = {}
    source_passages_by_paragraph_index: dict[int, SourcePassage] = {}
    for r in load("00_source_passages.csv"):
        sp = SourcePassage(
            source_passage_id=r["source_passage_id"],
            docx_file=r["docx_file"],
            source_document_id=r.get("source_document_id", ""),
            paragraph_index=int(r["paragraph_index"]),
            style=r["style"],
            text=r["text"],
            review_status=r["review_status"],
            image_verified=r["image_verified"],
        )
        source_passages[sp.source_passage_id] = sp
        source_passages_by_paragraph_index[sp.paragraph_index] = sp

    documents = {
        r["document_id"]: Document(
            document_id=r["document_id"],
            title=r["title"],
            date_original=r["date_original"],
            date_iso=r["date_iso"],
            archive_repository=r["archive_repository"],
            archive_access=r["archive_access"],
            inventory_number=r["inventory_number"],
            source_file=r["source_file"],
            document_type=r["document_type"],
            status=r["status"],
        )
        for r in load("01_documents.csv")
    }

    roles = {
        r["role_id"]: Role(
            role_id=r["role_id"],
            role_original=r["role_original"],
            role_description_id=r["role_description_id"],
            role_family=r["role_family"],
        )
        for r in load("03_roles.csv")
    }

    persons = {
        r["person_id"]: Person(
            person_id=r["person_id"],
            name_canonical=r["name_canonical"],
            entity_level=r["entity_level"],
            source_status=r["source_status"],
            identity_confidence=_opt_float(r["identity_confidence"]),
            notes=r["notes"],
        )
        for r in load("02_persons.csv")
    }

    person_roles = {
        r["person_role_id"]: PersonRole(
            person_role_id=r["person_role_id"],
            person_id=r["person_id"],
            role_id=r["role_id"],
            role_original=r["role_original"],
            valid_from=r["valid_from"],
            valid_to=r["valid_to"],
            evidence_status=r["evidence_status"],
            source_document_id=r["source_document_id"],
            confidence=_opt_float(r["confidence"]),
            review_status=r.get("review_status", ""),
            source_passage_id=r.get("source_passage_id", ""),
        )
        for r in load("04_person_roles.csv")
    }

    locations = {
        r["location_id"]: Location(
            location_id=r["location_id"],
            name_original=r["name_original"],
            name_normalized_id=r["name_normalized_id"],
            location_type=r["location_type"],
            parent_location_id=r["parent_location_id"],
            evidence_status=r["evidence_status"],
        )
        for r in load("05_locations.csv")
    }

    human_groups = {
        r["group_id"]: HumanGroup(
            group_id=r["group_id"],
            source_category_original=r["source_category_original"],
            count=int(r["count"]),
            status_category=r["status_category"],
            growth_category_original=r["growth_category_original"],
            sex_category_original=r["sex_category_original"],
            location_id=r["location_id"],
            evidence_status=r["evidence_status"],
            source_document_id=r["source_document_id"],
            source_passage_id=r.get("source_passage_id", ""),
            review_status=r.get("review_status", ""),
        )
        for r in load("06_human_groups.csv")
    }

    hrlt_records = {
        r["hrlt_id"]: HrltRecord(
            hrlt_id=r["hrlt_id"],
            human_or_group_id=r["human_or_group_id"],
            entity_type=(
                EntityType.AGGREGATE_GROUP
                if r["entity_type"] == "aggregate_group"
                else EntityType.INDIVIDUAL
            ),
            role_id=r.get("role_id", ""),
            location_id=r["location_id"],
            valid_from=r["valid_from"],
            valid_to=r["valid_to"],
            assignment_value=_opt_float(r["assignment_value"]),
            evidence_status=r["evidence_status"],
            source_quote=r["source_quote"],
            source_document_id=r["source_document_id"],
            confidence=_opt_float(r["confidence"]),
            review_status=r["review_status"],
            source_passage_id=r.get("source_passage_id", ""),
        )
        for r in load("07_human_role_location_time.csv")
    }

    inventory_items = {
        r["inventory_item_id"]: InventoryItem(
            inventory_item_id=r["inventory_item_id"],
            inventory_date=r["inventory_date"],
            location_id=r["location_id"],
            inventory_section=r["inventory_section"],
            category=r["category"],
            row_type=r["row_type"],
            quantity=_opt_float(r["quantity"]),
            unit_normalized=r["unit_normalized"],
            item_text_id=r["item_text_id"],
            source_translation_full=r["source_translation_full"],
            condition_normalized=r["condition_normalized"],
            reading_status=r["reading_status"],
            source_document_id=r["source_document_id"],
            source_paragraph_index=_opt_int(r["source_paragraph_index"]),
            image_verified=r["image_verified"],
            notes=r["notes"],
            evidence_status=r.get("evidence_status", ""),
            review_status=r.get("review_status", ""),
        )
        for r in load("10_inventory_items.csv")
    }

    task_requirements = {
        r["task_id"]: TaskRequirement(
            task_id=r["task_id"],
            task_name=r["task_name"],
            task_family=r["task_family"],
            allowed_location_ids=_pipe_list(r["allowed_location_ids"]),
            required_skill_ids=_pipe_list(r["required_skill_ids"]),
            preferred_role_ids=_pipe_list(r["preferred_role_ids"]),
            required_tool_keywords=_pipe_list(r["required_tool_keywords"]),
            minimum_workers_assumption=_opt_float(r["minimum_workers_assumption"]),
            constraint_strength=r["constraint_strength"],
            evidence_basis=r["evidence_basis"],
            review_status=r["review_status"],
        )
        for r in load("14_task_requirements.csv")
    }

    compatibility_rules = {
        r["compatibility_id"]: CompatibilityRule(
            compatibility_id=r["compatibility_id"],
            role_id=r["role_id"],
            location_id=r["location_id"],
            compatibility_score=_opt_float(r["compatibility_score"]),
            constraint_type=r["constraint_type"],
            evidence_basis=r["evidence_basis"],
            review_status=r["review_status"],
        )
        for r in load("15_role_location_compatibility.csv")
    }

    adjacency_edges = {
        r["edge_id"]: AdjacencyEdge(
            edge_id=r["edge_id"],
            from_location_id=r["from_location_id"],
            to_location_id=r["to_location_id"],
            relation_type=r["relation_type"],
            bidirectional=r["bidirectional"].strip().lower() == "true",
            evidence_status=r["evidence_status"],
            evidence_basis=r["evidence_basis"],
            distance_original=r["distance_original"],
            distance_normalized=_opt_float(r["distance_normalized"]),
            review_status=r["review_status"],
        )
        for r in load("16_location_adjacency.csv")
    }

    return Dataset(
        source_passages=source_passages,
        source_passages_by_paragraph_index=source_passages_by_paragraph_index,
        documents=documents,
        roles=roles,
        persons=persons,
        person_roles=person_roles,
        locations=locations,
        human_groups=human_groups,
        hrlt_records=hrlt_records,
        inventory_items=inventory_items,
        task_requirements=task_requirements,
        compatibility_rules=compatibility_rules,
        adjacency_edges=adjacency_edges,
        file_hashes=file_hashes,
        root=str(root),
    )
