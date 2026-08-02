"""Equipment-capacity classification, wired into hard_constraints.
add_equipment_capacity() from cli.run() whenever real inventory data
resolves a task's required_tool_keywords to actual 10_inventory_items.csv
rows at one of that task's allowed_location_ids.

Linkage (real, not invented): 14_task_requirements.csv's own
`required_tool_keywords` column (pipe-delimited Dutch tool terms, e.g.
T-DRILL's 'boor|boorens|boorers') is matched, case-insensitively, as a
substring against each candidate inventory row's `category`,
`item_text_id`, and `source_translation_full` fields, restricted to rows
whose `location_id` is one of the task's own `allowed_location_ids`
(inventory `location_id` values are real 05_locations.csv ids -- verified,
e.g. 'L-SMITSWINCKEL', 'L-ORTEN'). No task-specific inventory linkage table
is hand-authored; the match is purely textual and dataset-driven, so a gap
in the underlying vocabulary (e.g. a Dutch keyword vs. an Indonesian-
translated inventory description) surfaces as a real, visible
NO_INVENTORY_MATCH status rather than being papered over with a fuzzy/
invented translation.

Only `unit_normalized == 'stux'` (piece-count) rows are ever counted --
weight ('lb'), volume, or barrel-count rows do not represent discrete,
simultaneously-usable equipment units and would misrepresent worker
capacity if summed as if they did.

Confirmed vs. uncertain classification rules (verbatim from the request
that authored this module):

    - only serviceable equipment contributes to confirmed capacity
    - unknown condition contributes to uncertain capacity, not confirmed
    - unserviceable equipment contributes zero confirmed capacity (and is
      also excluded from uncertain -- it is a definite negative fact, not
      an ambiguous one, so it must not inflate the "might work out" pool
      either)
    - unresolved equipment terms (reading_status == 'unresolved') must
      never silently satisfy a tool requirement -- they are always routed
      to uncertain_capacity, regardless of their own condition_normalized
      value, since the item's very textual identity is unconfirmed

Parent/child double-counting (verified against the real dataset): every
row_type == 'container_or_parent' row is an aggregate summary whose
breakdown is fully itemized by the row_type == 'inventory_item' rows that
immediately follow it (e.g. INV-0333 'container_or_parent' = 6 meriam
logam; its children INV-0334 (2) + INV-0335 (4) sum to exactly 6). Only
row_type == 'inventory_item' rows are ever counted; container_or_parent
rows never contribute, so the same equipment can never be counted twice.
"""
from __future__ import annotations

import csv
import enum
from dataclasses import dataclass, field
from pathlib import Path


class CapacityStatus(enum.Enum):
    NO_REQUIREMENT_DECLARED = "no_requirement_declared"
    NO_INVENTORY_MATCH = "no_inventory_match"
    SUFFICIENT = "sufficient"
    UNCERTAIN_SUFFICIENT = "uncertain_sufficient"
    INSUFFICIENT = "insufficient"


_CONFIRMED_TOKENS = {"serviceable", "new"}
_UNSERVICEABLE_TOKENS = {"unserviceable"}
_COUNTABLE_UNIT = "stux"


def _condition_class(condition_normalized: str) -> str:
    """'confirmed' / 'unserviceable' / 'uncertain' for a single row.
    A compound value ('a|b') is always 'uncertain' -- '|' is this
    dataset's established marker for an unresolved reading disjunction
    (the same convention validation.py already treats as ambiguous for
    evidence_status/relation_type/constraint_type), never a confirmed
    single state."""
    value = (condition_normalized or "").strip().lower()
    if not value:
        return "uncertain"  # unknown condition -> uncertain, never confirmed
    if "|" in value:
        return "uncertain"
    if value in _UNSERVICEABLE_TOKENS:
        return "unserviceable"
    if value in _CONFIRMED_TOKENS:
        return "confirmed"
    return "uncertain"  # e.g. 'old' / 'worn' / 'unopened' -- not proof of serviceability


def _matches_tool_keywords(item, keywords: tuple[str, ...]) -> bool:
    haystacks = (
        (item.category or "").lower(),
        (item.item_text_id or "").lower(),
        (item.source_translation_full or "").lower(),
    )
    return any(kw.lower() in haystack for kw in keywords for haystack in haystacks)


#: v0.1.2 fix (SOLVER_V0_1_2_FIX_PLAN.md Item 3): required_capacity is
#: sourced from TaskRequirement.minimum_workers_assumption, which means
#: "the archivally-assumed minimum crew size to run this task at all" --
#: NOT "the maximum number of workers who might simultaneously want this
#: equipment." No data source in this dataset states an actual
#: simultaneous-demand estimate, so this fixed label is attached to every
#: report rather than leaving the number's meaning to be inferred.
REQUIRED_CAPACITY_SEMANTICS = "archival_minimum_crew_size"

_UNMATCHED_BOUND_RATIONALE = "no constraint instantiated (no_inventory_match / no_requirement_declared)"


def _hard_bound_rationale(status: CapacityStatus) -> str:
    if status in (CapacityStatus.NO_INVENTORY_MATCH, CapacityStatus.NO_REQUIREMENT_DECLARED):
        return _UNMATCHED_BOUND_RATIONALE
    return (
        "confirmed_capacity + uncertain_capacity (condition data mostly unknown "
        "in the real archive; confirmed-only would hard-forbid tasks the archive "
        "does not actually forbid -- see hard_capacity_bound())"
    )


@dataclass(frozen=True)
class CapacityReport:
    task_id: str
    location_id: str
    confirmed_capacity: float
    uncertain_capacity: float
    required_capacity: float | None
    capacity_status: CapacityStatus
    source_inventory_item_ids: tuple[str, ...] = field(default_factory=tuple)
    required_capacity_semantics: str = REQUIRED_CAPACITY_SEMANTICS
    hard_bound_rationale: str = ""


def compute_capacity_reports(dataset) -> list[CapacityReport]:
    """One CapacityReport per (task, location) pair for every task that
    declares required_tool_keywords, across every one of its
    allowed_location_ids -- emitted even when no inventory matches, so a
    gap in the underlying data is visible rather than silently absent from
    the output (the "instantiate and validate whenever inputs are
    available" requirement)."""
    reports: list[CapacityReport] = []
    for task_id, task in sorted(dataset.task_requirements.items()):
        keywords = tuple(k for k in task.required_tool_keywords if k)
        required = task.minimum_workers_assumption

        if not keywords:
            for location_id in task.allowed_location_ids:
                reports.append(CapacityReport(
                    task_id=task_id, location_id=location_id,
                    confirmed_capacity=0.0, uncertain_capacity=0.0,
                    required_capacity=required,
                    capacity_status=CapacityStatus.NO_REQUIREMENT_DECLARED,
                    hard_bound_rationale=_hard_bound_rationale(CapacityStatus.NO_REQUIREMENT_DECLARED),
                ))
            continue

        for location_id in task.allowed_location_ids:
            candidates = [
                item for item in dataset.inventory_items.values()
                if item.row_type == "inventory_item"
                and item.location_id == location_id
                and item.unit_normalized == _COUNTABLE_UNIT
                and _matches_tool_keywords(item, keywords)
            ]

            confirmed = 0.0
            uncertain = 0.0
            source_ids: list[str] = []
            for item in candidates:
                qty = item.quantity if item.quantity is not None else 0.0
                if item.reading_status == "unresolved":
                    uncertain += qty
                    source_ids.append(item.inventory_item_id)
                    continue
                cond = _condition_class(item.condition_normalized)
                if cond == "confirmed":
                    confirmed += qty
                    source_ids.append(item.inventory_item_id)
                elif cond == "uncertain":
                    uncertain += qty
                    source_ids.append(item.inventory_item_id)
                # cond == "unserviceable" -> zero contribution, excluded
                # from source_inventory_item_ids (a definite negative, not
                # a source backing either capacity number).

            if not candidates:
                status = CapacityStatus.NO_INVENTORY_MATCH
            elif required is not None and confirmed >= required:
                status = CapacityStatus.SUFFICIENT
            elif required is not None and (confirmed + uncertain) >= required:
                status = CapacityStatus.UNCERTAIN_SUFFICIENT
            else:
                status = CapacityStatus.INSUFFICIENT

            reports.append(CapacityReport(
                task_id=task_id, location_id=location_id,
                confirmed_capacity=confirmed, uncertain_capacity=uncertain,
                required_capacity=required, capacity_status=status,
                source_inventory_item_ids=tuple(sorted(source_ids)),
                hard_bound_rationale=_hard_bound_rationale(status),
            ))
    return reports


def hard_capacity_bound(report: CapacityReport) -> int:
    """The value actually wired into hard_constraints.add_equipment_
    capacity()'s `capacity` parameter for a report with real inventory
    matches: confirmed_capacity + uncertain_capacity (never confirmed
    alone). Rationale: condition_normalized is empty/unknown for the large
    majority of real inventory rows, so confirmed_capacity is frequently 0
    even where matching equipment clearly exists in the archive --
    hard-capping at 0 would use ABSENCE of recorded condition as if it
    were evidence of true zero capacity, exactly the "absence of evidence
    is not evidence of absence" mistake UNCERTAINTY_POLICY.md prohibits.
    confirmed_capacity + uncertain_capacity already excludes definitively
    unserviceable items (a real negative fact, correctly subtracted); the
    remainder is the honest physical count of items not known to be
    broken, matching the same "widen for reading uncertainty, never
    silently narrow" precedent already established for INV-0232 in
    SOLVER_INPUT_READINESS.md §8-9."""
    return int(round(report.confirmed_capacity + report.uncertain_capacity))


def write_equipment_capacity_csv(reports: list[CapacityReport], path: Path, schicht_labels=None) -> None:
    """v0.1.3/v0.1.4 fix: one row per (report, schicht index in scope) --
    the capacity bound `add_equipment_capacity` wires is asserted
    independently per (schicht, time) pair (see hard_constraints.
    add_equipment_capacity, fixed in ad8dc6b4), so this report makes
    explicit which controlled schicht_id each uniform bound applies to,
    plus that schicht's own evidentiary basis (source_schicht_count,
    schicht_evidence_status). `schicht_labels`: optional
    {index: schicht.SchichtLabel} -- when omitted, defaults to the single
    SCHICHT-UNSPECIFIED index, matching the real dataset's only possible
    value today. This is an end-user-facing report, so it uses the PUBLIC
    dict -- schicht_index_internal is never written here (v0.1.4)."""
    from salido_hdt.solver.schicht import resolve_schicht_labels, schicht_label_to_public_dict

    if schicht_labels is None:
        schicht_labels = resolve_schicht_labels(1)

    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "task_id", "location_id", "schicht_id", "source_schicht_count", "schicht_evidence_status",
            "confirmed_capacity", "uncertain_capacity",
            "required_capacity", "capacity_status", "source_inventory_item_ids",
            "required_capacity_semantics", "hard_bound_rationale",
        ])
        for r in reports:
            for index in sorted(schicht_labels):
                public = schicht_label_to_public_dict(schicht_labels[index])
                writer.writerow([
                    r.task_id, r.location_id, public["schicht_id"],
                    public["source_schicht_count"] if public["source_schicht_count"] is not None else "",
                    public["schicht_evidence_status"],
                    r.confirmed_capacity, r.uncertain_capacity,
                    r.required_capacity if r.required_capacity is not None else "",
                    r.capacity_status.value, "|".join(r.source_inventory_item_ids),
                    r.required_capacity_semantics, r.hard_bound_rationale,
                ])
