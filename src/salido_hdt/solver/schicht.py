"""Typed schicht (shift) domain -- v0.1.3 fix (SOLVER_V0_1_3_SCHICHT_PLAN.md).

The CP-SAT model keeps using integer schicht indices internally (`s` in
`x[h,j,l,s,t]`) -- nothing about variable construction or constraint
grouping changes here. This module is a resolution layer applied AFTER
solving: it maps each internal integer index to a controlled, public
`SchichtId` string plus its evidentiary basis, so a downstream reader of
any public output can never mistake "internal bookkeeping index 0" for
"the historical claim that this was an unspecified/day/night shift" --
these are two different statements. `schicht_index = 0` is bookkeeping;
`schicht_id = SchichtId.UNSPECIFIED` (or DAY/NIGHT/THREE_SHIFT_UNSPECIFIED)
is the historical claim, resolved independently.

Evidence gating: DAY / NIGHT / THREE_SHIFT_UNSPECIFIED are reachable only
via an explicit SchichtSourceEvidence (a real archival record) or an
explicit SchichtScenarioAssumption (a caller-declared modelling
assumption, never silent). No CSV column in
docs/enclave/salido_hdt_model_v0_4_1/ currently encodes shift identity --
verified in SOLVER_V0_1_2_F6_F7_ACCEPTANCE_AUDIT.md -- so the
explicit_source path exists and is tested (mirroring hard_constraints.
add_health_exclusion()'s "documented no-op" discipline) but cannot be
exercised by the real dataset today. Absent either input, an index always
resolves to UNSPECIFIED with a warning explaining why -- never inferred
from modern working-hour conventions.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass


class SchichtId(enum.Enum):
    UNSPECIFIED = "SCHICHT-UNSPECIFIED"
    DAY = "SCHICHT-DAY"
    NIGHT = "SCHICHT-NIGHT"
    THREE_SHIFT_UNSPECIFIED = "SCHICHT-THREE-SHIFT-UNSPECIFIED"


@dataclass(frozen=True)
class SchichtSourceEvidence:
    """An explicit archival record asserting a schicht identity for a
    given internal index. Not reachable from the real v0.4.1 dataset
    today (no source column exists) -- built and tested against synthetic
    evidence so the mechanism is ready the moment such a column exists."""

    schicht_id: SchichtId
    source_document_id: str
    source_passage_id: str


@dataclass(frozen=True)
class SchichtScenarioAssumption:
    """An explicit, caller-declared modelling assumption -- never silent.
    Distinct from SchichtSourceEvidence: this is NOT an archival
    statement, it is a hypothesis the caller chose to test for one run."""

    schicht_id: SchichtId
    assumption_id: str


@dataclass(frozen=True)
class SchichtLabel:
    """The full, public-output-ready resolution for one internal schicht
    index. `schicht_index` is kept for internal traceability only -- it
    must never be read as the historical schicht identifier; `schicht_id`
    is the actual historical claim (or explicit absence of one)."""

    schicht_index: int
    schicht_id: SchichtId
    schicht_evidence_status: str  # "unspecified" | "explicit_source" | "scenario_assumption"
    schicht_source_document_id: str = ""
    schicht_source_passage_id: str = ""
    schicht_assumption_id: str = ""
    schicht_warning: str = ""


_UNSPECIFIED_WARNING_TEMPLATE = (
    "no source evidence or scenario assumption for schicht index {index}; "
    "defaulting to SCHICHT-UNSPECIFIED -- never inferred from modern "
    "working-hour conventions"
)
_ASSUMPTION_WARNING = (
    "scenario assumption, not an archival statement -- this schicht_id "
    "reflects a modelling choice the caller explicitly declared, not "
    "documented shift evidence"
)


def resolve_schicht_labels(
    schicht_count: int,
    source_evidence: dict[int, SchichtSourceEvidence] | None = None,
    scenario_assumptions: dict[int, SchichtScenarioAssumption] | None = None,
) -> dict[int, SchichtLabel]:
    """One SchichtLabel per index in range(schicht_count). Explicit source
    evidence takes precedence over a scenario assumption for the same
    index (real archival evidence outranks a caller's modelling
    assumption); absent both, an index always resolves to UNSPECIFIED."""
    source_evidence = source_evidence or {}
    scenario_assumptions = scenario_assumptions or {}

    labels: dict[int, SchichtLabel] = {}
    for index in range(schicht_count):
        evidence = source_evidence.get(index)
        assumption = scenario_assumptions.get(index)

        if evidence is not None:
            labels[index] = SchichtLabel(
                schicht_index=index,
                schicht_id=evidence.schicht_id,
                schicht_evidence_status="explicit_source",
                schicht_source_document_id=evidence.source_document_id,
                schicht_source_passage_id=evidence.source_passage_id,
            )
        elif assumption is not None:
            labels[index] = SchichtLabel(
                schicht_index=index,
                schicht_id=assumption.schicht_id,
                schicht_evidence_status="scenario_assumption",
                schicht_assumption_id=assumption.assumption_id,
                schicht_warning=_ASSUMPTION_WARNING,
            )
        else:
            labels[index] = SchichtLabel(
                schicht_index=index,
                schicht_id=SchichtId.UNSPECIFIED,
                schicht_evidence_status="unspecified",
                schicht_warning=_UNSPECIFIED_WARNING_TEMPLATE.format(index=index),
            )
    return labels


def schicht_label_to_dict(label: SchichtLabel) -> dict:
    return {
        "schicht_index": label.schicht_index,
        "schicht_id": label.schicht_id.value,
        "schicht_evidence_status": label.schicht_evidence_status,
        "schicht_source_document_id": label.schicht_source_document_id,
        "schicht_source_passage_id": label.schicht_source_passage_id,
        "schicht_assumption_id": label.schicht_assumption_id,
        "schicht_warning": label.schicht_warning,
    }
