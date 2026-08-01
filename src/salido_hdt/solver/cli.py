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
from pathlib import Path

from salido_hdt.solver import config
from salido_hdt.solver.data_loader import load_dataset
from salido_hdt.solver.domain import HardSoftLabel
from salido_hdt.solver.hard_constraints import (
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
    add_task_continuity_penalty,
    add_unsupported_role_switching_penalty,
)
from salido_hdt.solver.validation import classify_hard_soft, classify_provenance, validate_dataset
from salido_hdt.solver.variables import build_variables


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
    return {
        task_id: set(t.preferred_role_ids)
        for task_id, t in dataset.task_requirements.items()
        if t.preferred_role_ids
    }


def _non_explicit_location_ids(dataset) -> set[str]:
    return {
        loc_id for loc_id, loc in dataset.locations.items()
        if loc.evidence_status != "explicit"
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
    hard_locations, soft_locations = _hard_soft_location_maps(dataset)
    hard_adjacent_pairs = _hard_adjacent_pairs(dataset)
    non_explicit_location_ids = _non_explicit_location_ids(dataset)

    add_temporal_presence(model, sv.x, sv.presence)
    add_role_task_compatibility(model, sv.x, sv.person_roles, task_preferred_roles)
    add_role_location_compatibility(model, sv.x, sv.person_roles, hard_locations)
    add_one_location_per_schicht(model, sv.x)
    add_topological_feasibility(model, sv.m, hard_adjacent_pairs)  # sv.m is empty by design -> no-op today
    add_health_exclusion(model, sv.x, released_ill=set())  # documented no-op: no health column exists

    archival_contradictions = add_explicit_location_preference_penalty(
        model, sv.x, non_explicit_location_ids
    )
    unsupported_assignments = add_unsupported_role_switching_penalty(
        sv.x, task_preferred_roles, sv.person_roles
    )
    role_location_penalties = add_role_location_preference_penalty(
        model, sv.x, sv.person_roles, soft_locations
    )
    over_assignment = add_task_continuity_penalty(
        model, sv.x, sv.entities, tuple(dataset.task_requirements), len(sv.time_buckets)
    )
    add_minimum_movement_penalty(sv.m)  # sv.m empty by design -> []

    expr = build_objective(
        model,
        archival_contradictions=archival_contradictions,
        unsupported_assignments=unsupported_assignments,
        temporal_violations=[],  # hard-enforced by add_temporal_presence -> structurally zero
        topological_violations=[],  # hard-enforced by add_topological_feasibility -> structurally zero
        role_location_penalties=role_location_penalties,
        over_assignment=over_assignment,
    )

    scenarios = collect_scenarios(
        model, expr, decision_vars=sv.x, max_scenarios=max_scenarios
    )

    for scenario in scenarios:
        path = output_dir / f"scenario_{scenario.index:02d}.json"
        payload = {
            "index": scenario.index,
            "status": scenario.status,
            "objective_value": scenario.objective_value,
            "active_assignments": [
                {"human_or_group_id": k[0], "task_id": k[1], "location_id": k[2],
                 "schicht": k[3], "time_bucket": k[4]}
                for k, v in scenario.assignment.items() if v == 1
            ],
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = {
        "root": str(root),
        "total_records_validated": report.total_records,
        "hard_eligible": len(report.hard_eligible),
        "excluded_from_hard": len(report.excluded_from_hard),
        "n_scenarios": len(scenarios),
        "n_time_buckets": len(sv.time_buckets),
        "n_entities": len(sv.entities),
        "n_x_variables": len(sv.x),
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
