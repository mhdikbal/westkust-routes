"""Soft constraints per docs/enclave/.../docs/CONSTRAINT_SOLVER.md.

Every function returns a list of penalty BoolVars/expressions -- it never
calls model.Add(... == 0) the way hard_constraints.py does. objective.py
sums and weights these; nothing here forbids an assignment outright.
"""
from __future__ import annotations

from ortools.sat.python import cp_model


def add_role_location_preference_penalty(
    model: cp_model.CpModel,
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    person_roles: dict[str, set[str]],
    soft_compatible_locations: dict[str, set[str]],
) -> list[cp_model.IntVar]:
    """CONSTRAINT_SOLVER.md soft list: 'role-location compatibility'.

    For roles that have SOFT (not HARD) compatibility rules only, penalize
    -- but do not forbid -- an assignment outside the soft-preferred set.
    """
    penalties: list[cp_model.IntVar] = []
    for (h, j, l, s, t), var in x_vars.items():
        h_roles = person_roles.get(h)
        if not h_roles:
            continue
        for role in h_roles:
            preferred = soft_compatible_locations.get(role)
            if preferred is not None and l not in preferred:
                penalties.append(var)
    return penalties


def add_task_continuity_penalty(
    model: cp_model.CpModel,
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    entities: tuple[str, ...],
    task_ids: tuple[str, ...],
    n_time_buckets: int,
) -> list[cp_model.IntVar]:
    """CONSTRAINT_SOLVER.md soft list: 'task continuity'.

    Penalize an entity switching task between two consecutive time buckets.
    Returns one penalty BoolVar per (h, t) pair where a switch is possible;
    the BoolVar is 1 iff the entity's active task at t differs from t+1.
    """
    penalties: list[cp_model.IntVar] = []
    for h in entities:
        for t in range(n_time_buckets - 1):
            vars_t = {j: x_vars[(h, j, l, s, t)]
                      for (hh, j, l, s, tt) in x_vars
                      if hh == h and tt == t}
            vars_t1 = {j: x_vars[(h, j, l, s, t + 1)]
                       for (hh, j, l, s, tt) in x_vars
                       if hh == h and tt == t + 1}
            if not vars_t or not vars_t1:
                continue
            switch = model.NewBoolVar(f"switch_{h}_{t}")
            same_task_indicators = []
            for j in set(vars_t) & set(vars_t1):
                both = model.NewBoolVar(f"both_{h}_{j}_{t}")
                model.AddMultiplicationEquality(both, [vars_t[j], vars_t1[j]])
                same_task_indicators.append(both)
            # switch is a MINIMIZATION penalty (objective.py sums these with
            # a positive weight): forcing switch=1 whenever no same-task
            # indicator fired is enough of a lower bound, since a
            # minimizing solver will never pay for switch=1 when it could
            # legally set it to 0.
            if same_task_indicators:
                model.Add(sum(same_task_indicators) + switch >= 1)
            else:
                model.Add(switch == 1)
            penalties.append(switch)
    return penalties


def add_explicit_location_preference_penalty(
    model: cp_model.CpModel,
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    non_explicit_location_ids: set[str],
) -> list[cp_model.IntVar]:
    """CONSTRAINT_SOLVER.md soft list: 'preference for explicit over
    interpreted locations'. Penalize any assignment to a location whose
    own evidence_status (05_locations.csv) is not 'explicit'."""
    return [
        var
        for (h, j, l, s, t), var in x_vars.items()
        if l in non_explicit_location_ids
    ]


def add_unsupported_role_switching_penalty(
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    task_preferred_roles: dict[str, set[str]],
    person_roles: dict[str, set[str]],
) -> list[cp_model.IntVar]:
    """CONSTRAINT_SOLVER.md soft list: 'avoidance of unsupported role
    switching'.

    hard_constraints.add_role_task_compatibility() already forbids a
    *known*-role entity from being assigned to a task requiring a role it
    does not hold. This function covers the complementary case: an entity
    with NO HARD-documented role at all (person_roles.get(h) is None --
    every aggregate group, since 04_person_roles.csv only covers named
    individuals) assigned to a task that DOES declare a role preference.
    That assignment is not blocked (there is no role to check), but it is
    also not evidentially supported -- soft-penalized, not forbidden.
    """
    return [
        var
        for (h, j, l, s, t), var in x_vars.items()
        if task_preferred_roles.get(j) and person_roles.get(h) is None
    ]


def add_serviceable_equipment_preference_penalty(
    y_vars: dict[tuple[str, str, str, int], cp_model.IntVar],
    unserviceable_item_ids: set[str],
) -> list[cp_model.IntVar]:
    """CONSTRAINT_SOLVER.md soft list: 'preference for serviceable
    equipment'. Penalize use of an inventory item whose condition_normalized
    is not 'serviceable' (e.g. UNRESOLVED_READINGS.md items marked
    unserviceable). variables.py's build_variables() leaves y empty by
    default (equipment-use variables are out of this task's build scope --
    see variables.py's module docstring), so this returns [] against the
    real dataset today; it exists so the mechanism is ready once y is
    populated for a specific equipment-capacity scenario."""
    return [
        var
        for (e, j, l, t), var in y_vars.items()
        if e in unserviceable_item_ids
    ]


def add_minimum_movement_penalty(
    m_vars: dict[tuple[str, str, str, int], cp_model.IntVar],
) -> list[cp_model.IntVar]:
    """CONSTRAINT_SOLVER.md soft list: 'minimum movement between periods'.
    Every active movement variable is itself a penalty unit."""
    return list(m_vars.values())
