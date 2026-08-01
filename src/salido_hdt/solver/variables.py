"""CP-SAT decision variables per docs/enclave/.../docs/CONSTRAINT_SOLVER.md.

    x[h,j,l,s,t]  human/group h performs task j at location l, schicht s, time t
    y[e,j,l,t]    equipment e is used for task j at location l, time t
    m[h,l1,l2,t]  human/group h moves from l1 to l2 at time t
    q[h,t]        health state of h at time t
    z[j,l,t]      task j is active at location l, time t

Pruning (plan decision #3): x is only instantiated for (h, l) pairs the
dataset actually attests h present at, via HARD-eligible HRLT records --
never the full h x l cross-product. This means the solver never even
considers an assignment the archive gives no evidence for; it is not an
optimization, it is the "validation-first" promise applied to variable
construction itself. Role-task and role-location *legality* (as opposed to
existence-pruning) is enforced by hard_constraints.py, not silently baked
in here, so those rules stay independently testable and auditable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

from ortools.sat.python import cp_model

from salido_hdt.solver import config
from salido_hdt.solver.domain import Dataset, HardSoftLabel
from salido_hdt.solver.validation import classify_hard_soft, classify_provenance


@dataclass(frozen=True)
class TimeBucket:
    index: int
    start: date
    end: date
    label: str


def _parse_date(value: str) -> Optional[date]:
    value = (value or "").strip()
    if not value:
        return None
    # Dataset dates are ISO "YYYY-MM-DD"; a few valid_from values are
    # "YYYY-MM" (month precision only) -- treat those as the 1st of month.
    try:
        return date.fromisoformat(value)
    except ValueError:
        pass
    try:
        year, month = value.split("-")
        return date(int(year), int(month), 1)
    except (ValueError, IndexError):
        return None


def derive_time_buckets(dataset: Dataset, bucket_days: int = 7) -> tuple[TimeBucket, ...]:
    """Weekly buckets spanning every valid_from/valid_to in 04/07 -- the
    only two tables in this dataset that carry temporal-validity fields.
    Bounds come from the data itself, never a hardcoded date range."""
    candidates: list[date] = []
    for pr in dataset.person_roles.values():
        candidates += [_parse_date(pr.valid_from), _parse_date(pr.valid_to)]
    for h in dataset.hrlt_records.values():
        candidates += [_parse_date(h.valid_from), _parse_date(h.valid_to)]
    known = sorted(d for d in candidates if d is not None)
    if not known:
        raise ValueError("dataset has no parseable valid_from/valid_to dates")

    start, end = known[0], known[-1]
    buckets = []
    cursor = start
    idx = 0
    while cursor <= end:
        bucket_end = min(cursor + timedelta(days=bucket_days - 1), end)
        buckets.append(TimeBucket(idx, cursor, bucket_end, f"W{idx:02d}"))
        cursor = bucket_end + timedelta(days=1)
        idx += 1
    return tuple(buckets)


def _bucket_index_for(buckets: tuple[TimeBucket, ...], d: Optional[date]) -> Optional[int]:
    if d is None:
        return None
    for b in buckets:
        if b.start <= d <= b.end:
            return b.index
    if d < buckets[0].start:
        return 0
    if d > buckets[-1].end:
        return buckets[-1].index
    return None


def hard_eligible_presence(dataset: Dataset) -> dict[str, set[tuple[str, int, int]]]:
    """entity_id -> {(location_id, from_bucket, to_bucket)} attested by a
    HARD-classified HRLT or person_role record. This is the pruning basis
    for x[h,j,l,s,t]."""
    buckets = derive_time_buckets(dataset)
    presence: dict[str, set[tuple[str, int, int]]] = {}

    for h in dataset.hrlt_records.values():
        level = classify_provenance(h, dataset)
        if classify_hard_soft(h, level, dataset) != HardSoftLabel.HARD:
            continue
        t_from = _bucket_index_for(buckets, _parse_date(h.valid_from)) or 0
        t_to = _bucket_index_for(buckets, _parse_date(h.valid_to))
        if t_to is None:
            t_to = buckets[-1].index
        presence.setdefault(h.human_or_group_id, set()).add((h.location_id, t_from, t_to))

    return presence


def hard_eligible_person_roles(dataset: Dataset) -> dict[str, set[str]]:
    """person_id -> {role_id} attested by a HARD-classified 04 record."""
    roles: dict[str, set[str]] = {}
    for pr in dataset.person_roles.values():
        level = classify_provenance(pr, dataset)
        if classify_hard_soft(pr, level, dataset) != HardSoftLabel.HARD:
            continue
        roles.setdefault(pr.person_id, set()).add(pr.role_id)
    return roles


@dataclass(frozen=True)
class SolverVariables:
    model: cp_model.CpModel
    time_buckets: tuple[TimeBucket, ...]
    schicht_count: int
    entities: tuple[str, ...]
    x: dict[tuple[str, str, str, int, int], cp_model.IntVar] = field(default_factory=dict)
    y: dict[tuple[str, str, str, int], cp_model.IntVar] = field(default_factory=dict)
    m: dict[tuple[str, str, str, int], cp_model.IntVar] = field(default_factory=dict)
    q: dict[tuple[str, int], cp_model.IntVar] = field(default_factory=dict)
    z: dict[tuple[str, str, int], cp_model.IntVar] = field(default_factory=dict)
    presence: dict[str, set[tuple[str, int, int]]] = field(default_factory=dict)
    person_roles: dict[str, set[str]] = field(default_factory=dict)


def build_variables(
    dataset: Dataset,
    schicht_count: Optional[int] = None,
) -> SolverVariables:
    schicht_count = schicht_count or config.DEFAULT_SCHICHT_COUNT
    time_buckets = derive_time_buckets(dataset)
    presence = hard_eligible_presence(dataset)
    person_roles = hard_eligible_person_roles(dataset)

    entities = tuple(sorted(set(presence) | set(person_roles)))
    model = cp_model.CpModel()

    x: dict[tuple[str, str, str, int, int], cp_model.IntVar] = {}
    for h in entities:
        attested = presence.get(h)
        if not attested:
            # Person has a role but no attested location presence in this
            # snapshot -- nothing to prune from, no x variables for them.
            continue
        for j in dataset.task_requirements:
            for (l, t_from, t_to) in attested:
                for s in range(schicht_count):
                    for t in range(t_from, t_to + 1):
                        x[(h, j, l, s, t)] = model.NewBoolVar(f"x_{h}_{j}_{l}_{s}_{t}")

    z: dict[tuple[str, str, int], cp_model.IntVar] = {}
    for j in dataset.task_requirements:
        for l in dataset.locations:
            for t in range(len(time_buckets)):
                z[(j, l, t)] = model.NewBoolVar(f"z_{j}_{l}_{t}")

    q: dict[tuple[str, int], cp_model.IntVar] = {}
    for h in entities:
        for t in range(len(time_buckets)):
            q[(h, t)] = model.NewBoolVar(f"q_{h}_{t}")  # 1 = healthy/available

    return SolverVariables(
        model=model,
        time_buckets=time_buckets,
        schicht_count=schicht_count,
        entities=entities,
        x=x,
        y={},
        m={},
        z=z,
        q=q,
        presence=presence,
        person_roles=person_roles,
    )
