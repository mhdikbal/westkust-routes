"""Hard constraints per docs/enclave/.../docs/CONSTRAINT_SOLVER.md.

Every function here takes plain, explicit data structures (not the whole
Dataset) so each is unit-testable in isolation with a handful of synthetic
BoolVars -- see tests/salido_hdt/solver/test_temporal_presence.py etc.

Each function's docstring states exactly which HARD-classified records it
is meant to be fed -- callers (cli.py) are responsible for running
validation.classify_hard_soft() first and only passing HARD-eligible data
in. A caller that passes ambiguous/section-level-composition data here is
misusing the API; these functions do not re-validate provenance themselves
(that would duplicate validation.py, the single source of truth for it).
"""
from __future__ import annotations

from collections import defaultdict

from ortools.sat.python import cp_model


def add_temporal_presence(
    model: cp_model.CpModel,
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    presence: dict[str, set[tuple[str, int, int]]],
) -> int:
    """No assignment before arrival or after documented departure.

    presence: entity_id -> {(location_id, from_time_bucket, to_time_bucket)},
    built from HARD-classified 04/07 records only (validation.py).
    Forces x[h,j,l,s,t] = 0 for any (h,l,t) combination not covered by an
    attested presence window. Returns the number of variables constrained.
    """
    constrained = 0
    for (h, j, l, s, t), var in x_vars.items():
        windows = presence.get(h, ())
        in_window = any(
            loc == l and t_from <= t <= t_to for (loc, t_from, t_to) in windows
        )
        if not in_window:
            model.Add(var == 0)
            constrained += 1
    return constrained


def add_role_task_compatibility(
    model: cp_model.CpModel,
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    person_roles: dict[str, set[str]],
    task_preferred_roles: dict[str, set[str]],
) -> int:
    """An assignment to a task requiring role R is only legal for an entity
    holding R (per HARD-classified 04 records), UNLESS the task declares no
    role preference at all -- absence of a requirement is not itself a
    requirement. Aggregate groups (absent from person_roles, since 04 only
    covers named individuals) are never restricted by this function; role
    compatibility for groups is out of scope here (no group-level role data
    exists at HARD provenance -- see SOLVER_INPUT_READINESS.md §4).
    """
    constrained = 0
    for (h, j, l, s, t), var in x_vars.items():
        required = task_preferred_roles.get(j)
        if not required:
            continue
        h_roles = person_roles.get(h)
        if h_roles is None:
            continue
        if not (h_roles & required):
            model.Add(var == 0)
            constrained += 1
    return constrained


def add_role_location_compatibility(
    model: cp_model.CpModel,
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    person_roles: dict[str, set[str]],
    hard_compatible_locations: dict[str, set[str]],
) -> int:
    """Restrict a role to its HARD-classified compatible locations -- but
    ONLY for roles that have at least one HARD compatibility rule.

    A role with zero rows in 15_role_location_compatibility.csv is left
    unrestricted here: absence of a recorded rule is not evidence of
    incompatibility (docs/.../UNCERTAINTY_POLICY.md's "Prohibited
    practice" explicitly forbids treating absence of evidence as evidence
    of absence).
    """
    constrained = 0
    for (h, j, l, s, t), var in x_vars.items():
        h_roles = person_roles.get(h)
        if not h_roles:
            continue
        for role in h_roles:
            allowed = hard_compatible_locations.get(role)
            if allowed is not None and l not in allowed:
                model.Add(var == 0)
                constrained += 1
                break
    return constrained


def add_one_location_per_schicht(
    model: cp_model.CpModel,
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
) -> int:
    """sum_l x[h,j,l,s,t] <= 1 -- purely structural, no data dependency."""
    grouped: dict[tuple[str, int, int], list[cp_model.IntVar]] = defaultdict(list)
    for (h, j, l, s, t), var in x_vars.items():
        grouped[(h, s, t)].append(var)
    for group_vars in grouped.values():
        if len(group_vars) > 1:
            model.Add(sum(group_vars) <= 1)
    return len(grouped)


def add_equipment_capacity(
    model: cp_model.CpModel,
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    task_id: str,
    location_id: str,
    capacity: int,
) -> int:
    """Simultaneous assignments to `task_id` at `location_id` cannot exceed
    `capacity` within any single (schicht, time bucket) pair.

    `capacity` should already reflect the SOLVER_INPUT_READINESS.md §8/§9
    widening rule: if the source InventoryItem's reading_status is
    `unresolved` (e.g. INV-0232, "60 bor tambang, kemungkinan terbaca
    berghborers"), the caller must pass a widened bound, not the raw
    quantity, to avoid treating an uncertain reading as an exact cap.

    v0.1.2 fix (SOLVER_V0_1_2_FIX_PLAN.md Item 1): grouped by (s, t), not
    by t alone. CONSTRAINT_SOLVER.md defines the decision variable as
    x[h,j,l,s,t] -- schicht is a first-class axis. Grouping by t alone
    silently pooled every schicht's candidates into one shared capacity
    check, which is dormant and invisible today only because
    config.DEFAULT_SCHICHT_COUNT == 1 (so s is always 0); it would
    under/over-count the moment more than one schicht value is ever used.
    This is the more conservative reading (equipment is never assumed
    shared across schicht) absent any archival statement either way -- see
    the fix plan's "Remaining limitations" for why the underlying policy
    question itself is not resolved here.
    """
    by_schicht_time: dict[tuple[int, int], list[cp_model.IntVar]] = defaultdict(list)
    for (h, j, l, s, t), var in x_vars.items():
        if j == task_id and l == location_id:
            by_schicht_time[(s, t)].append(var)
    for (s, t), vs in by_schicht_time.items():
        model.Add(sum(vs) <= capacity)
    return len(by_schicht_time)


def add_topological_feasibility(
    model: cp_model.CpModel,
    m_vars: dict[tuple[str, str, str, int], cp_model.IntVar],
    hard_adjacent_pairs: set[tuple[str, str]],
) -> int:
    """Movement m[h,l1,l2,t] is only legal through a HARD-classified
    adjacency edge (the 9 clean-`explicit` rows of 16_location_adjacency.csv
    per SOLVER_INPUT_READINESS.md §7/§9) or its reverse if bidirectional --
    the caller is responsible for expanding bidirectional pairs before
    calling this. The 12 `ambiguous` edges must never appear in
    hard_adjacent_pairs; that exclusion is validation.py's job upstream.
    """
    constrained = 0
    for (h, l1, l2, t), var in m_vars.items():
        if (l1, l2) not in hard_adjacent_pairs:
            model.Add(var == 0)
            constrained += 1
    return constrained


def add_health_exclusion(
    model: cp_model.CpModel,
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    released_ill: set[tuple[str, int]],
) -> int:
    """A person documented as released due to illness cannot be assigned
    afterwards without evidence of return.

    Documented no-op on v0.4.1: no CSV column in this dataset carries
    health-state data (HRLT_TENSOR.md names a conceptual `Health[h,t]`
    companion tensor, but it has no corresponding CSV -- confirmed absent
    during the SOLVER_INPUT_READINESS.md review). `released_ill` will
    therefore be empty when called against the real dataset; this function
    still exists and is exercised by tests so the mechanism is ready the
    moment health data is added, without fabricating any today.
    """
    constrained = 0
    for (h, t_released) in released_ill:
        for (hh, j, l, s, t), var in x_vars.items():
            if hh == h and t >= t_released:
                model.Add(var == 0)
                constrained += 1
    return constrained
