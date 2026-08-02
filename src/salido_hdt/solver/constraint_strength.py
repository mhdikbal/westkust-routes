"""Controlled parser for 14_task_requirements.csv's `constraint_strength`
column into four INDEPENDENT, atomic axis fields -- replacing every
`.startswith("hard")`-style free-text comparison against that column
anywhere in solver logic.

Real values observed in the dataset (7 of the 8 controlled literals; the
8th, 'hard_for_assay', is not currently used by any row but is still part
of the controlled mapping): hard, hard_role, hard_location,
hard_location_soft_staffing, hard_role_soft_tools, hard_role_soft_location,
soft.

The per-token -> per-axis table below is the authoritative, explicitly
reviewed mapping (not derived from a generic "does the token contain this
axis name" heuristic -- 'hard' and 'soft' resolve asymmetrically: bare
'hard' names role+location specifically but leaves equipment/staffing
unspecified, while bare 'soft' resolves all four axes to soft; this
asymmetry is why a controlled table, not a combinator parser, is used).

Rules:

  1. An explicitly named axis receives the explicitly named value.
  2. An axis not mentioned by the source token receives: unspecified.
  3-5. unspecified != soft, != hard, != not_applicable -- three distinct,
       never-conflated atomic values.
  6. An unknown or syntactically invalid token causes: blocked_unknown
     (on all four axes -- the whole record fails to parse).
  7. A record with blocked_unknown must not silently enter the solver as
     either a hard or soft constraint.
  8. constraint_strength_original is preserved unchanged for provenance.
  9. Both constraint_strength_original and parsed_constraint_axes are
     stored on the result -- never overwriting the source field.
  10. This module never modifies the canonical v0.4.1 CSV; parsing exists
      purely in this in-memory domain model.

`hard_for_assay` additionally carries `scope="assay"` and
`parse_status="legacy_ambiguous"` -- it is a recognized (not
blocked_unknown), but flagged-as-legacy token: none of its four axes
resolve to hard/soft, so any solver logic that needs a hard/soft decision
for a task carrying this token gets `unspecified` on every axis, same as
if constraint_strength had said nothing about any axis at all.

Structural `not_applicable` (an axis whose underlying task field is itself
empty, e.g. equipment_constraint_type for a task with no
required_tool_keywords) is computed independently of the token and takes
precedence over whatever the token's table entry says -- a requirement
that does not exist cannot be "hard" or "soft" no matter what the string
claims.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass


class AxisValue(enum.Enum):
    HARD = "hard"
    SOFT = "soft"
    UNSPECIFIED = "unspecified"
    NOT_APPLICABLE = "not_applicable"
    BLOCKED_UNKNOWN = "blocked_unknown"


@dataclass(frozen=True)
class ConstraintAxes:
    role_constraint_type: AxisValue
    location_constraint_type: AxisValue
    equipment_constraint_type: AxisValue
    staffing_constraint_type: AxisValue


@dataclass(frozen=True)
class ParsedConstraintStrength:
    constraint_strength_original: str
    parsed_constraint_axes: ConstraintAxes
    status: str  # "ok" | "blocked"
    reason: str = ""
    scope: str | None = None
    parse_status: str = "resolved"


_AXES = ("role", "location", "equipment", "staffing")
_H, _S, _U = AxisValue.HARD, AxisValue.SOFT, AxisValue.UNSPECIFIED

#: Controlled mapping: EXACT literal strings only, each entry explicitly
#: reviewed and authoritative -- deliberately not a generic grammar/
#: combinator parser over '_'-separated segments (which would silently
#: accept a syntactically-similar-but-uncontrolled string, and could not
#: represent 'hard' vs 'soft''s asymmetric propagation below).
_KNOWN_TOKENS: dict[str, dict] = {
    "hard": {"role": _H, "location": _H, "equipment": _U, "staffing": _U},
    "soft": {"role": _S, "location": _S, "equipment": _S, "staffing": _S},
    "hard_role": {"role": _H, "location": _U, "equipment": _U, "staffing": _U},
    "hard_location": {"role": _U, "location": _H, "equipment": _U, "staffing": _U},
    "hard_for_assay": {
        "role": _U, "location": _U, "equipment": _U, "staffing": _U,
        "scope": "assay", "parse_status": "legacy_ambiguous",
    },
    "hard_role_soft_tools": {"role": _H, "location": _U, "equipment": _S, "staffing": _U},
    "hard_location_soft_staffing": {"role": _U, "location": _H, "equipment": _U, "staffing": _S},
    "hard_role_soft_location": {"role": _H, "location": _S, "equipment": _U, "staffing": _U},
}


def _structural_not_applicable(task) -> dict[str, bool]:
    """An axis is not_applicable when the TASK ITSELF (independent of what
    constraint_strength says) declares no relevant requirement at all --
    this structural fact takes precedence over the token's own table
    entry, since a requirement that does not exist cannot be "hard"/"soft"
    no matter what the string claims."""
    return {
        "role": not task.preferred_role_ids,
        "location": not task.allowed_location_ids,
        "equipment": not task.required_tool_keywords,
        "staffing": task.minimum_workers_assumption is None,
    }


def parse_constraint_strength(task) -> ParsedConstraintStrength:
    """task: a domain.TaskRequirement. Never mutates `task` or any CSV --
    read-only, in-memory parsing per rule 10."""
    original = task.constraint_strength
    not_applicable = _structural_not_applicable(task)

    if original not in _KNOWN_TOKENS:
        blocked = ConstraintAxes(*(AxisValue.BLOCKED_UNKNOWN for _ in _AXES))
        return ParsedConstraintStrength(
            constraint_strength_original=original,
            parsed_constraint_axes=blocked,
            status="blocked",
            reason="unknown_constraint_strength",
        )

    entry = _KNOWN_TOKENS[original]
    resolved: dict[str, AxisValue] = {}
    for axis in _AXES:
        resolved[axis] = AxisValue.NOT_APPLICABLE if not_applicable[axis] else entry[axis]

    return ParsedConstraintStrength(
        constraint_strength_original=original,
        parsed_constraint_axes=ConstraintAxes(
            role_constraint_type=resolved["role"],
            location_constraint_type=resolved["location"],
            equipment_constraint_type=resolved["equipment"],
            staffing_constraint_type=resolved["staffing"],
        ),
        status="ok",
        scope=entry.get("scope"),
        parse_status=entry.get("parse_status", "resolved"),
    )
