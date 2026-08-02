"""End-to-end entry point: load -> validate -> build -> solve -> write.

    python -m salido_hdt.solver.cli [--scenarios N] [--output DIR]

Never opens anything under the canonical dataset root in write mode --
load_dataset() is read-only by construction (see data_loader.py), and every
write this module performs targets `output_dir`, which defaults OUTSIDE the
canonical tree (config.DEFAULT_OUTPUT_ROOT). test_no_source_mutation.py's
test_full_cli_run_does_not_mutate_v0_4_1 hashes v0.3/v0.4/v0.4.1 before and
after a full run() call to enforce this.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from salido_hdt.solver import config
from salido_hdt.solver.candidate_universe import (
    write_candidate_entities_csv,
    write_entity_presence_csv,
    write_excluded_entities_csv,
)
from salido_hdt.solver.constraint_strength import AxisValue, parse_constraint_strength
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.domain import EntityType, HardSoftLabel, ProvenanceLevel
from salido_hdt.solver.equipment_capacity import (
    CapacityStatus,
    compute_capacity_reports,
    hard_capacity_bound,
    write_equipment_capacity_csv,
)
from salido_hdt.solver.hard_constraints import (
    add_equipment_capacity,
    add_health_exclusion,
    add_one_location_per_schicht,
    add_role_location_compatibility,
    add_role_task_compatibility,
    add_temporal_presence,
    add_topological_feasibility,
)
from salido_hdt.solver.objective import build_objective
from salido_hdt.solver.scenario_collector import collect_scenarios
from salido_hdt.solver.soft_constraints import (
    add_explicit_location_preference_penalty,
    add_minimum_movement_penalty,
    add_role_location_preference_penalty,
    add_role_switch_penalty,
    add_role_task_support_penalty,
    add_task_continuity_penalty,
)
from salido_hdt.solver.validation import classify_hard_soft, classify_provenance, validate_dataset
from salido_hdt.solver.variables import _bucket_index_for, _parse_date, build_variables

#: v0.1.1 F6: fixed, non-invented explanation attached to every run's output
#: so a reader of validation_summary.json alone (not the source) knows how
#: to correctly scope scenario-to-scenario comparisons.
_RUN_METADATA_NOTE = (
    "schicht_count is a documented minimal assumption (config.DEFAULT_SCHICHT_COUNT), "
    "not derived from any CSV column. Scenario-to-scenario diversity reflects task "
    "choice only, within an already HARD-fixed (entity, location, time-window) "
    "presence set resolved before variable construction -- it never represents "
    "alternate presence, location, or arrival/departure histories."
)

#: F3 follow-up: hard_constraints.add_equipment_capacity() is now wired
#: into run() for every (task, location) pair where equipment_capacity.py's
#: keyword+location match against 10_inventory_items.csv finds real
#: candidate rows -- see equipment_capacity.py's module docstring for the
#: matching mechanism and hard_capacity_bound()'s docstring for why the
#: HARD cap uses confirmed+uncertain (never confirmed alone: condition_
#: normalized is empty/unknown for the large majority of real rows, so
#: confirmed-only would hard-forbid tasks the archive does not actually
#: forbid). (task, location) pairs with NO matching inventory data are
#: left unconstrained -- absence of a keyword/vocabulary match is not
#: itself evidence of zero equipment.
_EQUIPMENT_CAPACITY_NOTE = (
    "hard_constraints.add_equipment_capacity() is wired for every (task, location) "
    "pair with at least one matching 10_inventory_items.csv row (see "
    "equipment_capacity.csv for the full per-pair report: confirmed_capacity, "
    "uncertain_capacity, required_capacity, capacity_status, "
    "source_inventory_item_ids). The wired HARD bound is confirmed_capacity + "
    "uncertain_capacity, not confirmed_capacity alone -- see "
    "equipment_capacity.hard_capacity_bound()'s docstring."
)


def _hard_soft_location_maps(dataset) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """role_id -> {location_id}, split into HARD-only and everything-else
    (SOFT/CONTEXT_ONLY/AMBIGUOUS), per SOLVER_INPUT_READINESS.md §6."""
    hard: dict[str, set[str]] = {}
    soft: dict[str, set[str]] = {}
    for rule in dataset.compatibility_rules.values():
        level = classify_provenance(rule, dataset)
        label = classify_hard_soft(rule, level, dataset)
        target = hard if label == HardSoftLabel.HARD else soft
        target.setdefault(rule.role_id, set()).add(rule.location_id)
    return hard, soft


def _hard_adjacent_pairs(dataset) -> set[tuple[str, str]]:
    """The clean-`explicit` 16_location_adjacency.csv rows only
    (SOLVER_INPUT_READINESS.md §7) -- expanding bidirectional edges."""
    pairs: set[tuple[str, str]] = set()
    for edge in dataset.adjacency_edges.values():
        level = classify_provenance(edge, dataset)
        if classify_hard_soft(edge, level, dataset) != HardSoftLabel.HARD:
            continue
        pairs.add((edge.from_location_id, edge.to_location_id))
        if edge.bidirectional:
            pairs.add((edge.to_location_id, edge.from_location_id))
    return pairs


def _task_preferred_roles(dataset) -> dict[str, set[str]]:
    """Every task's declared preferred_role_ids, EXCLUDING only tasks whose
    constraint_strength is blocked_unknown (rule 7 of the constraint_
    strength parser: a blocked record must never silently enter the
    solver as either hard or soft). Used as input to the SOFT
    add_role_task_support_penalty() and add_role_switch_penalty() -- for
    the HARD gate, see _hard_task_preferred_roles()."""
    result: dict[str, set[str]] = {}
    for task_id, t in dataset.task_requirements.items():
        if not t.preferred_role_ids:
            continue
        if parse_constraint_strength(t).status == "blocked":
            continue
        result[task_id] = set(t.preferred_role_ids)
    return result


def _group_declared_roles(dataset) -> dict[str, set[str]]:
    """A small number of aggregate groups' own 06_human_groups.csv
    `source_category_original` textually NAMES a role from 03_roles.csv --
    an explicit supervisory function, verified, not invented. Matched via a
    case-insensitive prefix check in either direction (Dutch plural
    suffixes: 'mandoors'/'mandoressen'/'voorslager' vs
    'Mandoor'/'Mandores'/'Voorslager'). Verified against the real dataset:
    matches exactly G-MANDOOR-8->R-MANDOOR, G-MANDORESS-3->R-MANDORESS,
    G-VOORSLAGER-1->R-VOORSLAGER, and nothing else -- every other group's
    category (e.g. G-MS-121's 'volwassen mansslaven') is a purely
    demographic/labour descriptor with no role match. See
    add_role_task_support_penalty()'s docstring for how this is used."""
    declared: dict[str, set[str]] = {}
    for group in dataset.human_groups.values():
        category = (group.source_category_original or "").strip().lower()
        if not category:
            continue
        matches = {
            role.role_id
            for role in dataset.roles.values()
            if role.role_original.strip()
            and (
                category.startswith(role.role_original.strip().lower())
                or role.role_original.strip().lower().startswith(category)
            )
        }
        if matches:
            declared[group.group_id] = matches
    return declared


def _hard_task_preferred_roles(dataset) -> dict[str, set[str]]:
    """Like _task_preferred_roles(), but restricted to task requirement
    rows whose constraint_strength.constraint_strength PARSES to
    role_constraint_type == HARD via the controlled
    constraint_strength.parse_constraint_strength() parser -- never a
    free-text `.startswith("hard")` comparison. In v0.1, ALL 18 task rows
    were fed to add_role_task_compatibility as an absolute hard exclusion
    regardless of each row's own constraint_strength -- a task requirement
    row self-declared 'soft' was still hard-forbidding role-undocumented
    entities. A task whose constraint_strength is blocked_unknown is
    excluded here too (never silently hard). Use this function's output
    (not _task_preferred_roles()'s) as input to
    hard_constraints.add_role_task_compatibility()."""
    hard: dict[str, set[str]] = {}
    for task_id, t in dataset.task_requirements.items():
        if not t.preferred_role_ids:
            continue
        parsed = parse_constraint_strength(t)
        if parsed.parsed_constraint_axes.role_constraint_type == AxisValue.HARD:
            hard[task_id] = set(t.preferred_role_ids)
    return hard


def _blocked_constraint_strength_tasks(dataset) -> list[dict]:
    """Diagnostic visibility for rule 7: every task whose constraint_
    strength failed to parse (blocked_unknown), so its exclusion from both
    the hard role-task gate and the soft role-support signal is traceable
    rather than silent. Empty against the real v0.4.1 dataset today (all 7
    real constraint_strength values are among the 8 controlled tokens) --
    exists for when a future task row carries an unreviewed value."""
    blocked = []
    for task_id, t in sorted(dataset.task_requirements.items()):
        parsed = parse_constraint_strength(t)
        if parsed.status == "blocked":
            blocked.append({
                "task_id": task_id,
                "constraint_strength_original": parsed.constraint_strength_original,
                "reason": parsed.reason,
            })
    return blocked


def _non_explicit_location_ids(dataset) -> set[str]:
    return {
        loc_id for loc_id, loc in dataset.locations.items()
        if loc.evidence_status != "explicit"
    }


def _aggregate_group_ids(dataset) -> frozenset[str]:
    """v0.1.1 F1: the entity ids that actually receive x-variables as
    aggregate groups -- derived from 07_human_role_location_time.csv's own
    entity_type column, NOT from 06_human_groups.csv's full id set (7 of
    that table's 17 rows never appear in 07 at all and so never reach
    variables.py regardless)."""
    return frozenset(
        h.human_or_group_id
        for h in dataset.hrlt_records.values()
        if h.entity_type == EntityType.AGGREGATE_GROUP
    )


def _entity_coverage(dataset, sv) -> list[dict]:
    """v0.1.1 F2: per-entity visibility into why an entity does or does not
    have CP-SAT variables at all, so a scenario's silence about an entity
    is never misread as an evidentiary claim (SOLVER_V0_1_1_FIX_PLAN.md
    F2)."""
    group_ids = _aggregate_group_ids(dataset)
    known_ids = set(dataset.persons) | group_ids
    coverage = []
    for entity_id in sorted(known_ids):
        has_hard_role = entity_id in sv.person_roles
        has_hard_presence = entity_id in sv.presence
        coverage.append({
            "entity_id": entity_id,
            "entity_type": "aggregate_group" if entity_id in group_ids else "individual",
            "has_hard_role": has_hard_role,
            "has_hard_presence": has_hard_presence,
            "included_in_variables": entity_id in sv.entities and has_hard_presence,
        })
    return coverage


def _presence_records_for(dataset, sv, h: str, l: str, t: int) -> list:
    """The HARD-classified HRLT record(s) whose (location_id, time window)
    covers this assignment -- the raw records backing _citations_for() and
    the richer per-assignment evidence fields below. Re-derives each
    candidate record's own time-bucket window (rather than trusting the
    (h,l) pair alone) so a record is only returned when its window
    actually covers t."""
    windows = sv.presence.get(h, ())
    if not any(loc == l and t_from <= t <= t_to for (loc, t_from, t_to) in windows):
        return []

    buckets = sv.time_buckets
    records = []
    for rec in dataset.hrlt_records.values():
        if rec.human_or_group_id != h or rec.location_id != l:
            continue
        level = classify_provenance(rec, dataset)
        if classify_hard_soft(rec, level, dataset) != HardSoftLabel.HARD:
            continue
        rec_from = _bucket_index_for(buckets, _parse_date(rec.valid_from)) or 0
        rec_to = _bucket_index_for(buckets, _parse_date(rec.valid_to))
        if rec_to is None:
            rec_to = buckets[-1].index
        if rec_from <= t <= rec_to:
            records.append(rec)
    return sorted(records, key=lambda r: r.hrlt_id)


def _citations_for(dataset, sv, h: str, l: str, t: int) -> list[str]:
    """The hrlt_id(s) of _presence_records_for()'s records -- kept as a
    thin wrapper so a scenario's active_assignments entries can be traced
    back to the archival record(s) that licensed them without re-running
    validation.py by hand."""
    return [rec.hrlt_id for rec in _presence_records_for(dataset, sv, h, l, t)]


def _assignment_evidence(
    dataset, sv, capacity_reports_by_task_location, h: str, j: str, l: str, t: int
) -> dict:
    """Builds the full evidence block for one assignment entry, per the
    required output schema. Every field here is traceable to a specific
    real record; nothing is invented. Since every assignment this solver
    ever emits is a COMBINATORIAL RECONSTRUCTION (no single archival
    record ever states "entity h performed task j at location l at time
    t" directly -- it is inferred from combining separately-attested
    presence/role/task feasibility), assignment_state / evidence_status /
    reconstruction_warning are fixed constants for every assignment cli.run()
    produces -- never claimed as a direct archival statement."""
    records = _presence_records_for(dataset, sv, h, l, t)
    primary = records[0] if records else None

    if primary is not None:
        provenance_precision = classify_provenance(primary, dataset).value
        source_document_id = primary.source_document_id
        source_passage_id = primary.source_passage_id
        evidence_quote = primary.source_quote
    else:
        provenance_precision = ProvenanceLevel.MISSING.value
        source_document_id = ""
        source_passage_id = ""
        evidence_quote = ""

    group_ids = _aggregate_group_ids(dataset)
    supporting_role_ids = sorted(
        sv.person_roles.get(h) or _group_declared_roles(dataset).get(h) or set()
    )

    return {
        "entity_type": "aggregate_group" if h in group_ids else "individual",
        "assignment_state": "solver_reconstructed",
        "evidence_status": "reconstructed",
        "source_document_id": source_document_id,
        "source_passage_id": source_passage_id,
        "evidence_quote": evidence_quote,
        "constraint_ids": [rec.hrlt_id for rec in records],
        "supporting_inventory_item_ids": list(
            capacity_reports_by_task_location.get((j, l), ())
        ),
        "supporting_role_ids": supporting_role_ids,
        "provenance_precision": provenance_precision,
        "reconstruction_warning": "not an archival statement",
    }


def run(root: Path, output_dir: Path, max_scenarios: int | None = None) -> Path:
    """Runs the full pipeline once and writes scenario_*.json +
    validation_summary.json under output_dir. Returns output_dir."""
    max_scenarios = max_scenarios or config.MAX_SCENARIOS
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset(root)
    report = validate_dataset(dataset)

    sv = build_variables(dataset)
    model = sv.model

    task_preferred_roles = _task_preferred_roles(dataset)
    hard_task_preferred_roles = _hard_task_preferred_roles(dataset)  # v0.1.1 F4
    hard_locations, soft_locations = _hard_soft_location_maps(dataset)
    hard_adjacent_pairs = _hard_adjacent_pairs(dataset)
    non_explicit_location_ids = _non_explicit_location_ids(dataset)

    add_temporal_presence(model, sv.x, sv.presence)
    add_role_task_compatibility(model, sv.x, sv.person_roles, hard_task_preferred_roles)  # v0.1.1 F4
    add_role_location_compatibility(model, sv.x, sv.person_roles, hard_locations)
    add_one_location_per_schicht(model, sv.x)
    add_topological_feasibility(model, sv.m, hard_adjacent_pairs)  # sv.m is empty by design -> no-op today
    add_health_exclusion(model, sv.x, released_ill=set())  # documented no-op: no health column exists

    # Equipment capacity: instantiate a HARD add_equipment_capacity() bound
    # for every (task, location) pair equipment_capacity.py finds real
    # inventory rows for -- pairs with no matching data are left
    # unconstrained (absence of a keyword/vocabulary match is not itself
    # evidence of zero equipment). See _EQUIPMENT_CAPACITY_NOTE and
    # equipment_capacity.hard_capacity_bound() for why the bound uses
    # confirmed+uncertain rather than confirmed alone.
    capacity_reports = compute_capacity_reports(dataset)
    _unmatched_statuses = (CapacityStatus.NO_INVENTORY_MATCH, CapacityStatus.NO_REQUIREMENT_DECLARED)
    n_equipment_constraints = 0
    for cap_report in capacity_reports:
        if cap_report.capacity_status in _unmatched_statuses:
            continue
        add_equipment_capacity(
            model, sv.x, task_id=cap_report.task_id, location_id=cap_report.location_id,
            capacity=hard_capacity_bound(cap_report),
        )
        n_equipment_constraints += 1
    capacity_reports_by_task_location = {
        (r.task_id, r.location_id): r.source_inventory_item_ids for r in capacity_reports
    }

    archival_contradictions = add_explicit_location_preference_penalty(
        model, sv.x, non_explicit_location_ids
    )
    group_declared_roles = _group_declared_roles(dataset)
    role_support = add_role_task_support_penalty(
        sv.x, task_preferred_roles, sv.person_roles, group_declared_roles
    )
    # role_task_support's two pools (undocumented / contradicted) both feed
    # "unsupported_assignments" -- the single-assignment "documented role
    # support" objective category -- but stay individually visible in
    # penalty_terms below (F7) since "no evidence either way" and "evidence
    # points elsewhere" are different claims worth telling apart in a
    # scenario's breakdown, even though they're weighted the same here.
    unsupported_assignments = role_support.undocumented + role_support.contradicted
    role_location_penalties = add_role_location_preference_penalty(
        model, sv.x, sv.person_roles, soft_locations
    )
    # v0.1.1 F1-followup: task_switch and location_switch are distinct
    # evidentiary claims (task changed vs. only location changed) -- see
    # soft_constraints.ContinuityPenalties. All three of task_switch,
    # location_switch, and role_switch feed the existing "over_assignment"
    # objective category (build_objective()'s six categories are fixed;
    # all three are temporal churn/inconsistency signals), but are also
    # kept visible as their own penalty_terms keys below (F7) so a reader
    # can tell which kind of churn drove a scenario's score without
    # re-deriving it from source. presence_transition is left disabled
    # (include_presence_transition_penalty defaults False): enabling it by
    # default would reintroduce an idle-vs-assigned pressure of exactly the
    # kind F1 removed for the live pipeline.
    continuity = add_task_continuity_penalty(
        model, sv.x, sv.entities, tuple(dataset.task_requirements), len(sv.time_buckets)
    )
    role_switch = add_role_switch_penalty(
        model, sv.x, sv.entities, task_preferred_roles, len(sv.time_buckets)
    )
    over_assignment = continuity.task_switch + continuity.location_switch + role_switch
    add_minimum_movement_penalty(sv.m)  # sv.m empty by design -> []

    penalty_terms = {  # v0.1.1 F7: named so collect_scenarios can report each category's solved sum
        "archival_contradictions": archival_contradictions,
        "unsupported_assignments": unsupported_assignments,
        "temporal_violations": [],  # hard-enforced by add_temporal_presence -> structurally zero
        "topological_violations": [],  # hard-enforced by add_topological_feasibility -> structurally zero
        "role_location_penalties": role_location_penalties,
        "over_assignment": over_assignment,
        "task_switch": continuity.task_switch,  # diagnostic breakdown of over_assignment
        "location_switch": continuity.location_switch,  # diagnostic breakdown of over_assignment
        "role_switch": role_switch,  # diagnostic breakdown of over_assignment
        "role_undocumented": role_support.undocumented,  # diagnostic breakdown of unsupported_assignments
        "role_contradicted": role_support.contradicted,  # diagnostic breakdown of unsupported_assignments
    }
    _diagnostic_only_keys = (
        "task_switch", "location_switch", "role_switch", "role_undocumented", "role_contradicted",
    )
    objective_terms = {k: v for k, v in penalty_terms.items() if k not in _diagnostic_only_keys}
    expr = build_objective(model, **objective_terms)

    scenarios = collect_scenarios(
        model, expr, decision_vars=sv.x, max_scenarios=max_scenarios, penalty_terms=penalty_terms,
    )

    for scenario in scenarios:
        scenario_id = f"scenario_{scenario.index:02d}"
        path = output_dir / f"{scenario_id}.json"
        active_assignments = []
        for k, v in scenario.assignment.items():
            if v != 1:
                continue
            h, j, l, s, t = k
            evidence = _assignment_evidence(dataset, sv, capacity_reports_by_task_location, h, j, l, t)
            active_assignments.append({
                "scenario_id": scenario_id,
                "entity_id": h,
                "entity_type": evidence["entity_type"],
                "task_id": j,
                "location_id": l,
                "schicht_id": s,
                "time_bucket": t,
                "assignment_state": evidence["assignment_state"],
                "evidence_status": evidence["evidence_status"],
                "source_document_id": evidence["source_document_id"],
                "source_passage_id": evidence["source_passage_id"],
                "evidence_quote": evidence["evidence_quote"],
                "constraint_ids": evidence["constraint_ids"],
                "supporting_inventory_item_ids": evidence["supporting_inventory_item_ids"],
                "supporting_role_ids": evidence["supporting_role_ids"],
                "provenance_precision": evidence["provenance_precision"],
                "reconstruction_warning": evidence["reconstruction_warning"],
                # retained for backward compatibility with existing readers:
                "human_or_group_id": h,
                "presence_hrlt_ids": evidence["constraint_ids"],
            })
        payload = {
            "index": scenario.index,
            "scenario_id": scenario_id,
            "status": scenario.status,
            "objective_value": scenario.objective_value,
            "penalty_breakdown": scenario.penalty_breakdown,  # v0.1.1 F7
            "active_assignments": active_assignments,
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Candidate-universe reporting (read-only; does not add x-variables --
    # see candidate_universe.py's module docstring for the scope decision).
    # assigned_entity_ids comes from scenario 0 (the primary/optimal
    # scenario) when at least one scenario was solved, splitting eligible
    # entities into ASSIGNED / PRESENT_BUT_UNASSIGNED; None (no scenario
    # solved at all) is kept distinct from an empty-but-solved scenario.
    assigned_entity_ids = (
        frozenset(k[0] for k, v in scenarios[0].assignment.items() if v == 1)
        if scenarios else None
    )
    write_entity_presence_csv(dataset, sv, output_dir / "entity_presence.csv")
    write_candidate_entities_csv(dataset, sv, output_dir / "candidate_entities.csv", assigned_entity_ids)
    write_excluded_entities_csv(dataset, sv, output_dir / "excluded_entities.csv", assigned_entity_ids)
    write_equipment_capacity_csv(capacity_reports, output_dir / "equipment_capacity.csv")

    capacity_status_counts = Counter(r.capacity_status.value for r in capacity_reports)

    summary = {
        "root": str(root),
        "total_records_validated": report.total_records,
        "hard_eligible": len(report.hard_eligible),
        "excluded_from_hard": len(report.excluded_from_hard),
        "n_scenarios": len(scenarios),
        "n_time_buckets": len(sv.time_buckets),
        "n_entities": len(sv.entities),
        "n_x_variables": len(sv.x),
        "entity_coverage": _entity_coverage(dataset, sv),  # v0.1.1 F2
        "equipment_capacity_enforced": n_equipment_constraints > 0,
        "equipment_capacity_constraints_instantiated": n_equipment_constraints,
        "equipment_capacity_status_counts": dict(capacity_status_counts),
        "equipment_capacity_note": _EQUIPMENT_CAPACITY_NOTE,
        "blocked_constraint_strength_tasks": _blocked_constraint_strength_tasks(dataset),
        "run_metadata": {  # v0.1.1 F6
            "schicht_count": sv.schicht_count,
            "time_bucket_width_days": 7,
            "note": _RUN_METADATA_NOTE,
        },
        "file_hashes": dataset.file_hashes,
    }
    (output_dir / "validation_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="SALIDO-HDT validation-first CP-SAT solver")
    parser.add_argument("--scenarios", type=int, default=config.MAX_SCENARIOS)
    parser.add_argument("--output", type=Path, default=config.DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--root", type=Path, default=config.V0_4_1_ROOT)
    args = parser.parse_args()

    output_dir = run(root=args.root, output_dir=args.output, max_scenarios=args.scenarios)
    print(f"Wrote solver run output to {output_dir}")


if __name__ == "__main__":
    main()
