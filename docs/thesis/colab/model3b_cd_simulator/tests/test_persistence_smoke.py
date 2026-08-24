"""Pytest wrapper for the one-cell, one-replicate persistence smoke test.
See persistence_smoke_test.py for the "not a pilot, not final" disclaimer.
"""

from model3b_cd_simulator.persistence_smoke_test import run_smoke_test


def test_persistence_smoke_one_cell_one_replicate():
    result = run_smoke_test()
    assert result["event_times_stored"] is True
    assert result["checksum_match_after_roundtrip"] is True
    assert result["boundary_test_m2_vs_m3b_cd"]["label_correct"] is True
    assert result["aic_bic_available"] is True
    assert result["not_pilot_10x10"] is True
    assert result["not_final_1000"] is True
