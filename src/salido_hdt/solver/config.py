"""Configuration and explicitly-documented modelling assumptions.

Every constant here that is NOT directly derivable from the CSVs is called
out as such -- per the "do not invent" discipline this dataset's own docs
require (docs/enclave/salido_hdt_model_v0_4_1/docs/UNCERTAINTY_POLICY.md,
ETHICAL_MODELING.md). Nothing here is a silent default.
"""
from __future__ import annotations

from pathlib import Path

# --- Paths -------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[3]

#: Canonical input. READ-ONLY. Never opened in write mode anywhere in this
#: package -- see data_loader.py and test_no_source_mutation.py.
V0_4_1_ROOT = _REPO_ROOT / "docs" / "enclave" / "salido_hdt_model_v0_4_1"

#: Default output location for solver runs. Deliberately OUTSIDE the
#: canonical dataset tree.
DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "docs" / "enclave" / "implementation" / "solver_runs"
)

IMPLEMENTATION_DOCS_ROOT = _REPO_ROOT / "docs" / "enclave" / "implementation"


# --- Objective weights ---------------------------------------------------
# docs/CONSTRAINT_SOLVER.md: "lambda1 must dominate all other penalties."
# Enforced numerically (not just documented) by making LAMBDA_1 two orders
# of magnitude above every other term -- any single archival contradiction
# outweighs an unbounded combination of the other five penalties as long as
# their combined count stays below 100, which holds for a dataset this size
# (largest table is 403 rows; no scenario can rack up >=100 combined soft
# penalties without also being archivally absurd on its face).
LAMBDA_1_ARCHIVAL_CONTRADICTIONS = 100.0
LAMBDA_2_UNSUPPORTED_ASSIGNMENTS = 1.0
LAMBDA_3_TEMPORAL_VIOLATIONS = 1.0
LAMBDA_4_TOPOLOGICAL_VIOLATIONS = 1.0
LAMBDA_5_ROLE_LOCATION_PENALTIES = 1.0
LAMBDA_6_OVER_ASSIGNMENT = 1.0


# --- Modelling assumptions not given by any CSV column --------------------

#: "schicht" (shift) count. No file in the dataset defines how many shifts
#: existed per time period, or their boundaries -- CONSTRAINT_SOLVER.md
#: names the dimension but does not size it. Defaulting to a single generic
#: shift is the minimal assumption that does not invent an unstated fact;
#: "one location per schicht" still degenerates to a meaningful "one
#: location per time-bucket" constraint at S=1. Override only with a
#: documented reason if the underlying research adds real shift data.
DEFAULT_SCHICHT_COUNT = 1

#: Time axis bucket width. 08_weekly_operations.csv is the only table with
#: its own native time granularity, and it is weekly.
TIME_BUCKET = "W"  # pandas-style weekly bucket label, used by variables.py


# --- Scenario collection ---------------------------------------------------

MAX_SCENARIOS = 5
SOLVE_TIME_LIMIT_SECONDS = 30.0
#: Fractional tolerance above the best-found objective within which an
#: alternative solution is still considered "near-optimal" and collected.
SCENARIO_OBJECTIVE_TOLERANCE = 0.05


# --- Manual provenance overrides ------------------------------------------
# Findings from docs/enclave/implementation/SOLVER_INPUT_READINESS.md that
# required a human to actually read the surrounding archival passages and
# cannot be re-derived by validation.py's mechanical rules (empty-field
# checks, "_or_" pattern detection). Each entry cites the report section it
# came from. If v0.4.1 is ever superseded, re-verify these against the new
# release before trusting them -- they are frozen findings about a specific
# dataset snapshot, not a general algorithm.
MANUAL_PROVENANCE_OVERRIDES: dict[str, str] = {
    # SOLVER_INPUT_READINESS.md §1: SP-01236 is a pure section heading ("Lijfeijgenen
    # in de mijns Beneden-Pagger") with zero quantities/roles of its own --
    # confirmed only by reading the surrounding passages SP-01237..SP-01252.
    # Value is the ProvenanceLevel enum's .value string (kept as a plain str
    # here to avoid a domain.py <-> config.py import cycle).
    "SP-01236": "section_level",
}

#: SOLVER_INPUT_READINESS.md §6: these three 15_role_location_compatibility.csv
#: rows carry constraint_type="interpreted" whose own evidence_basis text
#: states the group identity is unknown ("identitas kelompok tidak
#: diketahui") -- a self-declared ambiguity that no "_or_"-style pattern
#: match can detect mechanically.
MANUAL_AMBIGUOUS_RECORD_IDS: frozenset[str] = frozenset(
    {"RLC-0027", "RLC-0029", "RLC-0031"}
)
