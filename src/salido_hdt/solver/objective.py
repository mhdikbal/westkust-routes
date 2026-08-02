"""Objective function assembly.

    minimize:
      lambda1 * archival_contradictions
    + lambda2 * unsupported_assignments
    + lambda3 * temporal_violations
    + lambda4 * topological_violations
    + lambda5 * role_location_penalties
    + lambda6 * over_assignment

per docs/enclave/.../docs/CONSTRAINT_SOLVER.md, with lambda1 dominating.

Interpretive note (documented, not silent): CONSTRAINT_SOLVER.md's "Hard
constraints" section and its objective function both name
temporal/topological/role-location concerns. In this implementation,
hard_constraints.py enforces the HARD-eligible subset of those as absolute
exclusions (model.Add(var == 0)) -- so temporal_violations and
topological_violations are STRUCTURALLY ZERO in any feasible solution this
solver returns; they are still summed here (as an always-0 term) rather
than dropped, so the objective's shape matches the spec exactly and the
zero is visible/auditable rather than silently omitted.
`role_location_penalties` covers the SOFT (non-HARD) role-location
preference violations, since the HARD ones are, again, excluded outright.
`archival_contradictions` is reserved for the one thing this
implementation treats as the most severe: relying on an AMBIGUOUS-provenance
record for anything (soft_constraints callers should route ambiguous-record
penalties here specifically). `over_assignment` is interpreted as excess
movement between periods (add_minimum_movement_penalty) -- the closest
proxy available to "an entity is doing more, evidentially, than the record
supports" given this dataset does not carry a workload/quota field.

ETHICAL GUARD (plan decision #5): no term below is parameterized by
HumanGroup.count or any other group-size/composition value. Aggregate
groups contribute to every penalty list exactly the way an individual does
-- as a 0/1 presence indicator on an x/m/y var, never scaled by headcount.
test_aggregate_group_integrity.py asserts this by construction.
"""
from __future__ import annotations

from ortools.sat.python import cp_model

from salido_hdt.solver import config

#: v0.1.2 fix (SOLVER_V0_1_2_FIX_PLAN.md Item 2): the objective categories
#: that are STRUCTURALLY always zero given this implementation's wiring --
#: not a contingent finding of any particular run. temporal_violations and
#: topological_violations are hard-enforced (model.Add(var == 0) in
#: hard_constraints.add_temporal_presence / add_topological_feasibility),
#: never soft-penalized, so cli.py always passes them as [] and they can
#: never be anything but 0 in penalty_breakdown, forever, regardless of
#: dataset or scenario. Exposed here (not just in this docstring) so
#: cli.py can report it in output rather than leaving a reader unable to
#: tell "zero this run" from "structurally can never be nonzero."
STRUCTURAL_ZERO_CATEGORIES: frozenset[str] = frozenset({
    "temporal_violations", "topological_violations",
})


def build_objective(
    model: cp_model.CpModel,
    *,
    archival_contradictions: list[cp_model.IntVar],
    unsupported_assignments: list[cp_model.IntVar],
    temporal_violations: list[cp_model.IntVar],
    topological_violations: list[cp_model.IntVar],
    role_location_penalties: list[cp_model.IntVar],
    over_assignment: list[cp_model.IntVar],
) -> cp_model.LinearExpr:
    """Assemble and set the minimization objective. Returns the expression
    (also useful for scenario_collector.py's tolerance-bounded re-solves).

    Weights are cast with int() before use: every config.LAMBDA_* value is
    already integral (100.0, 1.0, ...) by design, and CP-SAT's model.Add()
    (used by scenario_collector.py to bound near-optimal re-solves) rejects
    float-coefficient linear expressions outright, even when Minimize()
    itself would have accepted them. Casting here keeps this expression
    identical in every solve path.
    """
    expr = (
        int(config.LAMBDA_1_ARCHIVAL_CONTRADICTIONS) * sum(archival_contradictions or [0])
        + int(config.LAMBDA_2_UNSUPPORTED_ASSIGNMENTS) * sum(unsupported_assignments or [0])
        + int(config.LAMBDA_3_TEMPORAL_VIOLATIONS) * sum(temporal_violations or [0])
        + int(config.LAMBDA_4_TOPOLOGICAL_VIOLATIONS) * sum(topological_violations or [0])
        + int(config.LAMBDA_5_ROLE_LOCATION_PENALTIES) * sum(role_location_penalties or [0])
        + int(config.LAMBDA_6_OVER_ASSIGNMENT) * sum(over_assignment or [0])
    )
    model.Minimize(expr)
    return expr
