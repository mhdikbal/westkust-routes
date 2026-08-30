"""Structural schema validation for the parsed V2 specification set.

Checks shape, identifier uniqueness, and cross-file referential integrity
against the frozen 2572c19 baseline invariants. Does not interpret the
scientific meaning of any field (see applicability_validator.py for that).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .parser import CsvDocument, V2SpecificationSet

# Frozen baseline invariants as of commit 2572c19. A mismatch is reported,
# not silently tolerated -- these constants describe the milestone this
# validator was built against, not a moving target.
EXPECTED_GATE_SPEC_ROWS = 51
EXPECTED_GATE_SPEC_COLS = 20
EXPECTED_LEDGER_ROWS = 8
EXPECTED_LEDGER_IDS = tuple(f"NUM-DEC-{i:02d}" for i in range(1, 9))
EXPECTED_LEDGER_DISTRIBUTION = {
    "APPROVED_WITH_LIMITATIONS": 7,
    "DEFERRED": 1,
    "PENDING_RESEARCHER_DECISION": 0,
}
EXPECTED_SOLE_DEFERRED_ID = "NUM-DEC-07"


@dataclass
class ValidationResult:
    ok: bool
    findings: list = field(default_factory=list)  # list[str], empty if ok

    def add(self, msg: str):
        self.findings.append(msg)
        self.ok = False


def validate_gate_spec(doc: CsvDocument) -> ValidationResult:
    r = ValidationResult(ok=True)
    if len(doc.rows) != EXPECTED_GATE_SPEC_ROWS:
        r.add(f"gate spec row count {len(doc.rows)} != expected {EXPECTED_GATE_SPEC_ROWS}")
    if len(doc.columns) != EXPECTED_GATE_SPEC_COLS:
        r.add(f"gate spec column count {len(doc.columns)} != expected {EXPECTED_GATE_SPEC_COLS}")

    ids = [row["gate_id"] for row in doc.rows]
    dupes = sorted({g for g in ids if ids.count(g) > 1})
    if dupes:
        r.add(f"duplicate gate_id values: {dupes}")

    # M1 (original V1 benchmark, not amended by Proposals 1-7) and M4
    # (EXCLUDED_INSUFFICIENT_PRECISE_SUBSET) are legitimate historical/
    # excluded candidates in the frozen spec vocabulary, not typos.
    valid_candidates = {"M0", "M1", "M2", "M3", "M4"}
    for i, row in enumerate(doc.rows):
        if row["candidate"] not in valid_candidates:
            r.add(f"row {i} gate_id={row['gate_id']!r}: unrecognized candidate {row['candidate']!r}")
    return r


def validate_ledger(doc: CsvDocument) -> ValidationResult:
    r = ValidationResult(ok=True)
    if len(doc.rows) != EXPECTED_LEDGER_ROWS:
        r.add(f"ledger row count {len(doc.rows)} != expected {EXPECTED_LEDGER_ROWS}")

    ids = [row["decision_id"] for row in doc.rows]
    if sorted(ids) != sorted(EXPECTED_LEDGER_IDS):
        r.add(f"ledger decision_id set {sorted(ids)} != expected {sorted(EXPECTED_LEDGER_IDS)}")
    dupes = sorted({d for d in ids if ids.count(d) > 1})
    if dupes:
        r.add(f"duplicate decision_id values: {dupes}")

    from collections import Counter
    dist = Counter(row["current_status"] for row in doc.rows)
    for status, expected_count in EXPECTED_LEDGER_DISTRIBUTION.items():
        actual = dist.get(status, 0)
        if actual != expected_count:
            r.add(f"ledger status {status!r} count {actual} != expected {expected_count}")

    deferred_ids = [row["decision_id"] for row in doc.rows if row["current_status"] == "DEFERRED"]
    if deferred_ids != [EXPECTED_SOLE_DEFERRED_ID]:
        r.add(f"DEFERRED rows {deferred_ids} != expected [{EXPECTED_SOLE_DEFERRED_ID}]")

    return r


def validate_applicability_matrix(doc: CsvDocument, gate_spec: CsvDocument) -> ValidationResult:
    r = ValidationResult(ok=True)
    # M1 (original V1 benchmark, not amended by Proposals 1-7) and M4
    # (EXCLUDED_INSUFFICIENT_PRECISE_SUBSET) are legitimate historical/
    # excluded candidates in the frozen spec vocabulary, not typos.
    valid_candidates = {"M0", "M1", "M2", "M3", "M4"}
    for i, row in enumerate(doc.rows):
        if row["candidate"] not in valid_candidates:
            r.add(f"row {i} gate_id={row.get('gate_id')!r}: unrecognized candidate {row['candidate']!r}")

    # Referential integrity: mandatory_advisory_status vocabulary used in the
    # applicability matrix must be a subset of the vocabulary actually
    # present in the gate spec -- no invented tier not backed by the spec.
    gate_tiers = {row["mandatory_advisory_status"] for row in gate_spec.rows}
    matrix_tiers = {row["mandatory_advisory_status"] for row in doc.rows}
    unknown_tiers = matrix_tiers - gate_tiers
    if unknown_tiers:
        r.add(f"applicability matrix uses tier values absent from the gate spec: {sorted(unknown_tiers)}")
    return r


def validate_specification_set(spec: V2SpecificationSet) -> dict:
    """Run all schema checks and return a dict of {check_name: ValidationResult}."""
    return {
        "gate_spec": validate_gate_spec(spec.gate_spec),
        "ledger": validate_ledger(spec.ledger),
        "applicability_matrix": validate_applicability_matrix(spec.applicability_matrix, spec.gate_spec),
    }
