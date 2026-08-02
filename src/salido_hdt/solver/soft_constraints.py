"""Soft constraints per docs/enclave/.../docs/CONSTRAINT_SOLVER.md.

Every function returns a list of penalty BoolVars/expressions -- it never
calls model.Add(... == 0) the way hard_constraints.py does. objective.py
sums and weights these; nothing here forbids an assignment outright.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ortools.sat.python import cp_model


@dataclass(frozen=True)
class ContinuityPenalties:
    """add_task_continuity_penalty()'s three distinct transition-penalty
    pools -- kept separate because they are different evidentiary claims
    (task changed vs. location changed vs. presence started/stopped), not
    three names for the same thing."""

    task_switch: list[cp_model.IntVar] = field(default_factory=list)
    location_switch: list[cp_model.IntVar] = field(default_factory=list)
    presence_transition: list[cp_model.IntVar] = field(default_factory=list)


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
    include_presence_transition_penalty: bool = False,
) -> ContinuityPenalties:
    """CONSTRAINT_SOLVER.md soft list: 'task continuity'.

    Compares entity h's ACTUAL assignment state (task, location) between
    consecutive time buckets t and t+1 and classifies the transition into
    exactly one of the categories below, per SOLVER_V0_1_1_FIX_PLAN.md's
    task-continuity truth table:

        idle -> idle                        : no penalty
        (task, location) -> same (task, loc): no penalty
        assigned -> idle / idle -> assigned : optional presence_transition
                                               penalty (off by default)
        task A -> different task B          : task_switch penalty
        task A -> task A, different location: location_switch penalty,
                                               NEVER task_switch

    Returns a ContinuityPenalties with the three pools kept separate -- a
    caller decides how (or whether) to weight each into an objective;
    nothing here presumes they belong in the same bucket.

    v0.1.1 fix (SOLVER_SCENARIO_INTERPRETATION_AUDIT.md F1 /
    SOLVER_V0_1_1_FIX_PLAN.md F1): the prior version (a) grouped candidate
    variables by task only, discarding location, so "same task, different
    location" was silently invisible -- it could only ever look like "same
    task" (zero penalty) or, if the (task) key didn't even match, an
    undifferentiated "switch"; and (b) had no explicit idle state, so an
    entity idle in both t and t+1 was mischarged a full task_switch penalty
    identical to an actual task change. This version tracks (task,
    location) pairs explicitly and never creates a penalty variable for a
    (h, t) pair with no assignment variables in either period at all.
    """
    task_switch: list[cp_model.IntVar] = []
    location_switch: list[cp_model.IntVar] = []
    presence_transition: list[cp_model.IntVar] = []

    for h in entities:
        for t in range(n_time_buckets - 1):
            vars_t = {(j, l): x_vars[(h, j, l, s, t)]
                      for (hh, j, l, s, tt) in x_vars
                      if hh == h and tt == t}
            vars_t1 = {(j, l): x_vars[(h, j, l, s, t + 1)]
                       for (hh, j, l, s, tt) in x_vars
                       if hh == h and tt == t + 1}
            if not vars_t and not vars_t1:
                # No assignment variable exists in either period -- there is
                # nothing to compare, and creating a penalty here would be
                # exactly the "penalty merely because no variable is true"
                # mistake this fix removes. Skip entirely.
                continue

            active_t = model.NewBoolVar(f"active_{h}_{t}")
            if vars_t:
                model.AddMaxEquality(active_t, list(vars_t.values()))
            else:
                model.Add(active_t == 0)

            active_t1 = model.NewBoolVar(f"active_{h}_{t + 1}")
            if vars_t1:
                model.AddMaxEquality(active_t1, list(vars_t1.values()))
            else:
                model.Add(active_t1 == 0)

            # Exact (task, location) continuation -- the true "no change" case.
            exact_same_indicators = []
            for key in set(vars_t) & set(vars_t1):
                both = model.NewBoolVar(f"same_state_{h}_{key[0]}_{key[1]}_{t}")
                model.AddMultiplicationEquality(both, [vars_t[key], vars_t1[key]])
                exact_same_indicators.append(both)
            same_state = model.NewBoolVar(f"same_state_any_{h}_{t}")
            if exact_same_indicators:
                model.AddMaxEquality(same_state, exact_same_indicators)
            else:
                model.Add(same_state == 0)

            # Same task, any location -- task continuation regardless of a
            # possible location change.
            tasks_t = {j for (j, l) in vars_t}
            tasks_t1 = {j for (j, l) in vars_t1}
            same_task_indicators = []
            for j in tasks_t & tasks_t1:
                task_active_t = model.NewBoolVar(f"task_active_{h}_{j}_{t}")
                model.AddMaxEquality(
                    task_active_t, [v for (jj, l), v in vars_t.items() if jj == j]
                )
                task_active_t1 = model.NewBoolVar(f"task_active_{h}_{j}_{t + 1}")
                model.AddMaxEquality(
                    task_active_t1, [v for (jj, l), v in vars_t1.items() if jj == j]
                )
                both_task = model.NewBoolVar(f"same_task_{h}_{j}_{t}")
                model.AddMultiplicationEquality(both_task, [task_active_t, task_active_t1])
                same_task_indicators.append(both_task)
            same_task = model.NewBoolVar(f"same_task_any_{h}_{t}")
            if same_task_indicators:
                model.AddMaxEquality(same_task, same_task_indicators)
            else:
                model.Add(same_task == 0)

            # task_switch: both periods active, but no task carried over.
            switch = model.NewBoolVar(f"task_switch_{h}_{t}")
            model.Add(switch >= active_t + active_t1 - 1 - same_task)
            task_switch.append(switch)

            # location_switch: the task carried over, but not the exact
            # (task, location) pair -- i.e. same task, different location.
            # Never overlaps with task_switch: same_task=1 forces switch's
            # lower bound to <=0 above, so switch and moved cannot both be
            # forced to 1 for the same (h, t) transition.
            moved = model.NewBoolVar(f"location_switch_{h}_{t}")
            model.Add(moved >= same_task - same_state)
            location_switch.append(moved)

            if include_presence_transition_penalty:
                transition = model.NewBoolVar(f"presence_transition_{h}_{t}")
                model.Add(transition >= active_t - active_t1)
                model.Add(transition >= active_t1 - active_t)
                presence_transition.append(transition)

    return ContinuityPenalties(
        task_switch=task_switch,
        location_switch=location_switch,
        presence_transition=presence_transition,
    )


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


@dataclass(frozen=True)
class RoleTaskSupportPenalties:
    """add_role_task_support_penalty()'s two pools -- kept separate because
    "no positive evidence either way" and "positive evidence pointing
    somewhere else" are different evidentiary claims about the same
    assignment, not degrees of the same one."""

    undocumented: list[cp_model.IntVar] = field(default_factory=list)
    contradicted: list[cp_model.IntVar] = field(default_factory=list)


def add_role_task_support_penalty(
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    task_preferred_roles: dict[str, set[str]],
    person_roles: dict[str, set[str]],
    group_declared_roles: dict[str, set[str]] = {},
) -> RoleTaskSupportPenalties:
    """CONSTRAINT_SOLVER.md soft list: 'preference for documented role
    support' -- a single-assignment, no-time-dimension check of whether a
    given (h, j) pairing is positively attested, undocumented, or actively
    contradicted. hard_constraints.add_role_task_compatibility() already
    hard-forbids a *known*-role individual from a HARD-classified task
    requiring a role they do not hold; this function is what remains
    reachable (SOFT-classified task rows, and entities without a hard
    person_roles.csv entry at all) and classifies it rather than either
    blanket-penalizing or blanket-exempting it.

    Fix (this revision -- see the request that replaced v0.1.1's blanket
    aggregate-group exemption): absence of h from `person_roles` is never,
    by itself, treated as evidence against h -- it only means "check the
    next available evidence source." Two positive-evidence sources are
    checked, in order:

      1. `person_roles.get(h)` -- a named individual's HARD-documented
         04_person_roles.csv role(s).
      2. `group_declared_roles.get(h)` -- an aggregate group whose OWN
         06_human_groups.csv `source_category_original` textually names a
         role from 03_roles.csv (verified, not invented: e.g. G-MANDOOR-8's
         category 'mandoors' matches R-MANDOOR's role_original 'Mandoor';
         G-VOORSLAGER-1/'voorslager'->R-VOORSLAGER;
         G-MANDORESS-3/'mandoressen'->R-MANDORESS -- an explicit
         supervisory function, distinct from a purely demographic/labour
         category like G-MS-121's 'volwassen mansslaven', which has no
         match and is never synthesized one).

    Per (h, j) pairing where j declares a preferred role:
      - h's declared set (from whichever source applies) intersects j's
        required roles  -> SUPPORTED, no penalty at all (covers both a
        role-documented individual on their own task, and a supervisory
        group like G-MANDOOR-8 on T-SUPERVISE).
      - h has no declared set from EITHER source                -> UNDOCUMENTED
        (soft penalty; covers a role-undocumented individual, and an
        ordinary-category group like G-MS-121 on any role-declaring task --
        never a "must not assign" forbid, and never inferred as evidence
        the assignment did NOT happen).
      - h HAS a declared set, but it does not intersect j's required roles
        -> CONTRADICTED (soft penalty, kept in its own pool since this is a
        stronger claim than mere absence of documentation -- h is
        positively attested as something else).

    This function never invents an individual role for an aggregate group
    and never expands a group beyond its own recorded category label; it
    only ever checks group-level textual evidence against group-level
    assignments, exactly like it does for individuals.
    """
    undocumented: list[cp_model.IntVar] = []
    contradicted: list[cp_model.IntVar] = []
    for (h, j, l, s, t), var in x_vars.items():
        required = task_preferred_roles.get(j)
        if not required:
            continue
        declared = person_roles.get(h)
        if declared is None:
            declared = group_declared_roles.get(h)
        if declared is None:
            undocumented.append(var)
        elif not (declared & required):
            contradicted.append(var)
        # else: declared & required is non-empty -> SUPPORTED, no penalty.
    return RoleTaskSupportPenalties(undocumented=undocumented, contradicted=contradicted)


def add_role_switch_penalty(
    model: cp_model.CpModel,
    x_vars: dict[tuple[str, str, str, int, int], cp_model.IntVar],
    entities: tuple[str, ...],
    task_preferred_roles: dict[str, set[str]],
    n_time_buckets: int,
) -> list[cp_model.IntVar]:
    """CONSTRAINT_SOLVER.md soft list: 'avoidance of unsupported role
    switching' -- the actual, ACROSS-TIME meaning of that name (fixing the
    prior version, which despite the name never compared t to t+1 at all
    and instead penalized single-assignment documentation gaps -- that
    concept now lives in add_role_task_support_penalty()).

    Compares the ROLE(S) implied by whichever task is active at t against
    those implied at t+1, for every entity -- individual or aggregate group
    alike; this mechanism never consults person_roles/group category
    identity, only each task's own declared preferred_role_ids, so it
    cannot reintroduce the v0.1.1 F1 bias (nothing here is affected by
    whether h has a documented role or not).

    A transition is only penalized when it is a genuine, structurally
    unavoidable role incompatibility: BOTH periods are active, and there is
    NO pair of (task active at t, task active at t+1) whose declared roles
    overlap (or where either task declares no role requirement at all --
    an unconstrained task is never treated as contradicting anything).
    Idle<->idle, idle<->active, same-task, or different-tasks-that-share-a-
    role (e.g. T-INSPECT-MINE and T-SUPERVISE both admit R-OPPERSTEIJGER)
    are never penalized here -- switching TASKS is add_task_continuity_
    penalty's concern; this is only about switching ROLES.
    """
    penalties: list[cp_model.IntVar] = []
    for h in entities:
        for t in range(n_time_buckets - 1):
            vars_t = {(j, l): x_vars[(h, j, l, s, t)]
                      for (hh, j, l, s, tt) in x_vars
                      if hh == h and tt == t}
            vars_t1 = {(j, l): x_vars[(h, j, l, s, t + 1)]
                       for (hh, j, l, s, tt) in x_vars
                       if hh == h and tt == t + 1}
            if not vars_t and not vars_t1:
                continue

            active_t = model.NewBoolVar(f"role_active_{h}_{t}")
            if vars_t:
                model.AddMaxEquality(active_t, list(vars_t.values()))
            else:
                model.Add(active_t == 0)

            active_t1 = model.NewBoolVar(f"role_active_{h}_{t + 1}")
            if vars_t1:
                model.AddMaxEquality(active_t1, list(vars_t1.values()))
            else:
                model.Add(active_t1 == 0)

            tasks_t = {j for (j, l) in vars_t}
            tasks_t1 = {j for (j, l) in vars_t1}
            task_active_t_cache: dict[str, cp_model.IntVar] = {}
            task_active_t1_cache: dict[str, cp_model.IntVar] = {}

            def _task_active(j, period_vars, cache, tag):
                if j in cache:
                    return cache[j]
                var = model.NewBoolVar(f"role_task_active_{h}_{tag}_{j}")
                model.AddMaxEquality(var, [v for (jj, l), v in period_vars.items() if jj == j])
                cache[j] = var
                return var

            compatible_indicators = []
            for j in tasks_t:
                roles_j = task_preferred_roles.get(j)
                for j1 in tasks_t1:
                    roles_j1 = task_preferred_roles.get(j1)
                    if roles_j and roles_j1 and not (roles_j & roles_j1):
                        continue  # both declare roles, and they don't overlap -- incompatible
                    task_at_t = _task_active(j, vars_t, task_active_t_cache, t)
                    task_at_t1 = _task_active(j1, vars_t1, task_active_t1_cache, t + 1)
                    both = model.NewBoolVar(f"role_compatible_{h}_{j}_{j1}_{t}")
                    model.AddMultiplicationEquality(both, [task_at_t, task_at_t1])
                    compatible_indicators.append(both)

            compatible_any = model.NewBoolVar(f"role_compatible_any_{h}_{t}")
            if compatible_indicators:
                model.AddMaxEquality(compatible_any, compatible_indicators)
            else:
                model.Add(compatible_any == 0)

            switch = model.NewBoolVar(f"role_switch_{h}_{t}")
            model.Add(switch >= active_t + active_t1 - 1 - compatible_any)
            penalties.append(switch)
    return penalties


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
