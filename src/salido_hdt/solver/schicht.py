"""Typed schicht (shift) domain -- v0.1.3/v0.1.4 fix
(SOLVER_V0_1_3_SCHICHT_PLAN.md, SOLVER_V0_1_4_THREE_SHIFT_METADATA_PLAN.md).

The CP-SAT model keeps using integer schicht indices internally (`s` in
`x[h,j,l,s,t]`) -- nothing about variable construction or constraint
grouping changes here. This module is a resolution layer applied AFTER
solving: it maps each internal integer index to a controlled, public
`SchichtId` string plus its evidentiary basis, so a downstream reader of
any public output can never mistake "internal bookkeeping index
`schicht_index_internal = 0`" for "the historical claim that this was an
unspecified/day/night/three-shift-unspecified shift" -- these are two
different statements, resolved independently. `schicht_index_internal` is
diagnostic-only: it must never appear in end-user-facing output (see
`schicht_label_to_public_dict()`).

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

Three-shift source statements (v0.1.4): a document stating an operation
ran in three schichten, without identifying who was on which shift, is
represented as METADATA on the SAME single internal index -- never as
three separate indices, never as SCHICHT-1/SCHICHT-2/SCHICHT-3 identities,
and never by tripling x-variables, personnel, or aggregate-group
headcounts. `SchichtSourceEvidence.source_schicht_count` carries the
archivally-stated count (e.g. 3); `individual_shift_assignment_known`
records whether per-person/per-group allocation evidence exists (almost
always False for this kind of statement). Neither field is ever read by
`variables.build_variables()` -- that function's `schicht_count` parameter
is sourced only from `config.DEFAULT_SCHICHT_COUNT`, entirely decoupled
from this module, which only ever runs AFTER variable construction.
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
    evidence so the mechanism is ready the moment such a column exists.

    `source_schicht_count`/`individual_shift_assignment_known` exist for
    the "document says three schichten, personnel unknown" case: set
    `schicht_id=SchichtId.THREE_SHIFT_UNSPECIFIED`,
    `source_schicht_count=3`, `individual_shift_assignment_known=False`.
    This is pure metadata -- it never changes how many CP-SAT variables,
    entities, or group headcounts exist."""

    schicht_id: SchichtId
    source_document_id: str
    source_passage_id: str
    source_schicht_count: int | None = None
    individual_shift_assignment_known: bool = False


@dataclass(frozen=True)
class SchichtScenarioAssumption:
    """An explicit, caller-declared modelling assumption -- never silent.
    Distinct from SchichtSourceEvidence: this is NOT an archival
    statement, it is a hypothesis the caller chose to test for one run."""

    schicht_id: SchichtId
    assumption_id: str


@dataclass(frozen=True)
class SchichtLabel:
    """The full, diagnostic-ready resolution for one internal schicht
    index. `schicht_index_internal` is kept for internal traceability
    only -- it must never be read as the historical schicht identifier
    and must never appear in end-user-facing output (use
    `schicht_label_to_public_dict()` there); `schicht_id` is the actual
    historical claim (or explicit absence of one)."""

    schicht_index_internal: int
    schicht_id: SchichtId
    schicht_evidence_status: str  # "unspecified" | "explicit_source" | "scenario_assumption"
    schicht_source_document_id: str = ""
    schicht_source_passage_id: str = ""
    schicht_assumption_id: str = ""
    schicht_warning: str = ""
    source_schicht_count: int | None = None
    individual_shift_assignment_known: bool = False


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
    assumption); absent both, an index always resolves to UNSPECIFIED.

    This function is called strictly AFTER variables.build_variables() in
    every caller -- it never influences, and is never called by, variable
    construction. schicht_count here is the INTERNAL slot count (from
    SolverVariables.schicht_count), never a source_schicht_count value."""
    source_evidence = source_evidence or {}
    scenario_assumptions = scenario_assumptions or {}

    labels: dict[int, SchichtLabel] = {}
    for index in range(schicht_count):
        evidence = source_evidence.get(index)
        assumption = scenario_assumptions.get(index)

        if evidence is not None:
            labels[index] = SchichtLabel(
                schicht_index_internal=index,
                schicht_id=evidence.schicht_id,
                schicht_evidence_status="explicit_source",
                schicht_source_document_id=evidence.source_document_id,
                schicht_source_passage_id=evidence.source_passage_id,
                source_schicht_count=evidence.source_schicht_count,
                individual_shift_assignment_known=evidence.individual_shift_assignment_known,
            )
        elif assumption is not None:
            labels[index] = SchichtLabel(
                schicht_index_internal=index,
                schicht_id=assumption.schicht_id,
                schicht_evidence_status="scenario_assumption",
                schicht_assumption_id=assumption.assumption_id,
                schicht_warning=_ASSUMPTION_WARNING,
            )
        else:
            labels[index] = SchichtLabel(
                schicht_index_internal=index,
                schicht_id=SchichtId.UNSPECIFIED,
                schicht_evidence_status="unspecified",
                schicht_warning=_UNSPECIFIED_WARNING_TEMPLATE.format(index=index),
            )
    return labels


def schicht_label_to_dict(label: SchichtLabel) -> dict:
    """Full, diagnostic dict -- includes schicht_index_internal. Use only
    for diagnostic/audit output (e.g. validation_summary.json), never for
    end-user-facing artifacts -- see schicht_label_to_public_dict()."""
    return {
        "schicht_index_internal": label.schicht_index_internal,
        "schicht_id": label.schicht_id.value,
        "schicht_evidence_status": label.schicht_evidence_status,
        "schicht_source_document_id": label.schicht_source_document_id,
        "schicht_source_passage_id": label.schicht_source_passage_id,
        "schicht_assumption_id": label.schicht_assumption_id,
        "schicht_warning": label.schicht_warning,
        "source_schicht_count": label.source_schicht_count,
        "individual_shift_assignment_known": label.individual_shift_assignment_known,
    }


def schicht_label_to_public_dict(label: SchichtLabel) -> dict:
    """End-user-facing dict -- excludes schicht_index_internal (v0.1.4:
    the internal bookkeeping index must never appear in a public-facing
    dataset, only in diagnostic output). Use for scenario_NN.json
    active_assignments and equipment_capacity.csv."""
    d = schicht_label_to_dict(label)
    del d["schicht_index_internal"]
    return d
