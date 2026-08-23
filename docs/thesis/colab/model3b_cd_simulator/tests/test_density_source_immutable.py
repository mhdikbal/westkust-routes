"""Unit test #12 (Fase 1 requirement list)."""

import hashlib

from model3b_cd_simulator.density import DEFAULT_CSV_PATH, build_x_cd_lookup, load_spec_a_density
from model3b_cd_simulator.rng import make_rng
from model3b_cd_simulator.simulate import simulate_m2


def _hash_file(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_source_density_csv_is_never_modified():
    """#12 — reading/using the Spec A working CSV must never mutate it
    (docs/thesis/pilot_annotation/MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md
    §0 treats it as read-only; CLAUDE.md: data historis adalah sumber
    kebenaran, jangan diedit langsung)."""
    before_hash = _hash_file(DEFAULT_CSV_PATH)

    series = load_spec_a_density()
    x_cd = build_x_cd_lookup(series)
    simulate_m2(-1.3, 0.1, x_cd, 1600.0, 1650.0, make_rng(11))  # exercise the reader

    after_hash = _hash_file(DEFAULT_CSV_PATH)
    assert before_hash == after_hash
