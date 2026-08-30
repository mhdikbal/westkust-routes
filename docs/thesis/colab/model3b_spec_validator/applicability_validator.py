"""Applicability semantics for the frozen V2 gate specification.

This module enforces meaning, not just shape: it classifies each gate's
mandatory/advisory tier without collapsing distinctions, refuses to treat
an approved calibration PROCEDURE as an already-resolved numeric VALUE,
and keeps the eight confirmed M3 implementation blockers visibly open.
No function in this module can mark a blocker resolved -- that is
deliberate: closing a blocker is a future, separately-authorized decision,
not a side effect of running a validator.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass
from types import MappingProxyType

from .parser import CsvDocument

TAU_PROCEDURE_TOKEN = "PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION"
EXPECTED_TAU_LINKED_GATE_IDS = frozenset(
    {"GATE-030-V2", "GATE-031-V2-REPL-B", "GATE-031-V2-REPL-C", "GATE-031-V2-REPL-D"}
)


class TierClass(enum.Enum):
    MANDATORY = "MANDATORY"
    ADVISORY = "ADVISORY"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    HISTORICAL_SPECIAL = "HISTORICAL_SPECIAL"  # the 3 mixed/historical-worded rows
    UNRECOGNIZED = "UNRECOGNIZED"


@dataclass(frozen=True)
class TierClassification:
    raw_status: str      # verbatim string from the gate spec, never rewritten
    tier_class: TierClass


def classify_tier(raw_status: str) -> TierClassification:
    """Classify a mandatory_advisory_status value. Never converts N/A into
    a pass/fail verdict, and never discards the original string."""
    if raw_status == "MANDATORY":
        return TierClassification(raw_status, TierClass.MANDATORY)
    if raw_status == "ADVISORY":
        return TierClassification(raw_status, TierClass.ADVISORY)
    if raw_status == "N/A":
        return TierClassification(raw_status, TierClass.NOT_APPLICABLE)
    if raw_status.startswith("MANDATORY (") or raw_status.startswith("MIXED ("):
        return TierClassification(raw_status, TierClass.HISTORICAL_SPECIAL)
    return TierClassification(raw_status, TierClass.UNRECOGNIZED)


def classify_gate_spec_tiers(gate_spec: CsvDocument) -> list:
    return [classify_tier(row["mandatory_advisory_status"]) for row in gate_spec.rows]


@dataclass(frozen=True)
class ThresholdStatusReading:
    gate_id: str
    raw_threshold_status: str
    procedure_resolved: bool       # a calibration/decision PROCEDURE exists
    numeric_value_selected: bool   # a concrete numeric VALUE has been chosen


def read_threshold_status(gate_id: str, raw_threshold_status: str) -> ThresholdStatusReading:
    """The core procedure-vs-value guard. A gate whose threshold_status is
    the tau placeholder token has an approved PROCEDURE but explicitly NOT
    a numeric value -- this function can never return
    (procedure_resolved=True, numeric_value_selected=True) for that token."""
    if raw_threshold_status == TAU_PROCEDURE_TOKEN:
        return ThresholdStatusReading(gate_id, raw_threshold_status, procedure_resolved=True, numeric_value_selected=False)
    return ThresholdStatusReading(gate_id, raw_threshold_status, procedure_resolved=False, numeric_value_selected=False)


def find_tau_linked_gates(gate_spec: CsvDocument) -> list:
    return [read_threshold_status(row["gate_id"], row["threshold_status"]) for row in gate_spec.rows
            if row["threshold_status"] == TAU_PROCEDURE_TOKEN]


def verify_tau_linked_gate_set(gate_spec: CsvDocument) -> list:
    """Returns a list of discrepancy strings (empty if the four expected
    tau-linked gates, and only those four, carry the procedure token)."""
    found = {r.gate_id for r in find_tau_linked_gates(gate_spec)}
    problems = []
    missing = EXPECTED_TAU_LINKED_GATE_IDS - found
    extra = found - EXPECTED_TAU_LINKED_GATE_IDS
    if missing:
        problems.append(f"expected tau-linked gates missing the procedure token: {sorted(missing)}")
    if extra:
        problems.append(f"unexpected gates carry the tau procedure token: {sorted(extra)}")
    return problems


# --- M3 implementation blockers -------------------------------------------
#
# Frozen finding set from NUM-DEC-06's compatibility audit of
# m3_bayesian_discrete.py (independently re-verified this session) plus
# NUM-DEC-04/06/08's own preconditions. Represented as an immutable mapping
# with no setter anywhere in this module -- there is no code path by which
# Wave 1 can mark one of these resolved.
_M3_BLOCKERS = MappingProxyType({
    "M3-BLOCK-01": "n_branch is clamped to [EPS, 1-EPS] in _to_unconstrained -- exact n=0 is unreachable",
    "M3-BLOCK-02": "log_prior omits normalization constants for the Beta(2,2)/Gamma(2,1) kernel priors",
    "M3-BLOCK-03": "MCMC proposal is generated in unconstrained space but the acceptance ratio uses the "
                   "constrained-space log_posterior with no transformation Jacobian",
    "M3-BLOCK-04": "no bridge-sampling implementation exists",
    "M3-BLOCK-05": "no thermodynamic-integration implementation exists",
    "M3-BLOCK-06": "internal parameter priors (n, beta, baseline, dispersion, CD, observation, episode) "
                   "are not yet versioned and frozen (NUM-DEC-06)",
    "M3-BLOCK-07": "calibration-set / evaluation-set seed-manifest separation is not implemented (NUM-DEC-04)",
    "M3-BLOCK-08": "the operational resource envelope is not measured; all ceilings remain "
                   "PENDING_MEASUREMENT (NUM-DEC-08)",
})


def get_m3_blockers() -> MappingProxyType:
    """Read-only view of the eight confirmed M3 blockers. Immutable: callers
    receive a MappingProxyType, not a dict, so accidental mutation raises
    TypeError rather than silently closing a blocker."""
    return _M3_BLOCKERS


def verify_all_blockers_open() -> list:
    """Sanity check used by tests and the terminal report: returns the
    sorted blocker IDs, always exactly the frozen eight. There is no
    'status' field to flip -- existence in this mapping IS the open state."""
    return sorted(_M3_BLOCKERS.keys())
