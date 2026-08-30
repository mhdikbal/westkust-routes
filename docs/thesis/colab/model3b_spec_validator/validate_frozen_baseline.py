"""Read-only validation report for the frozen V2 specification set at
commit 2572c19. Parses and validates docs/thesis/pilot_annotation/*, then
prints a summary. Does not modify any file. Not a substantive future test
(the 315-item PLANNED_ONLY inventory) -- this only checks that the design
documents are internally well-formed and readable by the Wave 1 tooling.

Usage: python -m docs.thesis.colab.model3b_spec_validator.validate_frozen_baseline
"""
from __future__ import annotations

import sys
from pathlib import Path

from .applicability_validator import (
    classify_gate_spec_tiers,
    get_m3_blockers,
    verify_tau_linked_gate_set,
)
from .parser import SpecParseError, parse_v2_specification_set
from .schema_validator import validate_specification_set

PILOT_ANNOTATION_DIR = Path(__file__).resolve().parents[2] / "pilot_annotation"


def main() -> int:
    print(f"Parsing V2 specification set from {PILOT_ANNOTATION_DIR}")
    try:
        spec = parse_v2_specification_set(PILOT_ANNOTATION_DIR)
    except SpecParseError as e:
        print(f"PARSE_FAILED: {e}")
        return 1
    print("Parse: OK (5/5 files read, no blank required fields, no unrecognized enum values)")

    results = validate_specification_set(spec)
    all_ok = True
    for name, r in results.items():
        status = "OK" if r.ok else "FINDINGS"
        print(f"Schema[{name}]: {status}")
        for f in r.findings:
            print(f"  - {f}")
        all_ok = all_ok and r.ok

    tiers = classify_gate_spec_tiers(spec.gate_spec)
    from collections import Counter
    tier_dist = Counter(t.tier_class.name for t in tiers)
    print(f"Gate tier distribution: {dict(tier_dist)}")

    tau_problems = verify_tau_linked_gate_set(spec.gate_spec)
    if tau_problems:
        print("Tau-linked gate check: FINDINGS")
        for p in tau_problems:
            print(f"  - {p}")
        all_ok = False
    else:
        print("Tau-linked gate check: OK (exactly the 4 expected gates carry "
              "PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION, "
              "recognized as procedure-resolved / value-not-selected)")

    blockers = get_m3_blockers()
    print(f"M3 implementation blockers: {len(blockers)} open (none closeable by this tooling)")
    for bid, desc in blockers.items():
        print(f"  - {bid}: {desc}")

    print(f"\nOVERALL: {'PASS' if all_ok else 'FINDINGS_PRESENT'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
