"""Unit tests #1, #2, #6, #7 (Fase 1 requirement list)."""

import numpy as np

from model3b_cd_simulator.rng import make_rng
from model3b_cd_simulator.simulate import simulate_m1

T0, T1 = 1600.0, 1700.0
MU, ALPHA, BETA = 0.2573, 0.4207, 0.6215


def test_reproducibility_same_seed():
    """#1 — same seed must produce an identical event realization."""
    events_a = simulate_m1(MU, ALPHA, BETA, T0, T1, make_rng(42))
    events_b = simulate_m1(MU, ALPHA, BETA, T0, T1, make_rng(42))
    assert np.array_equal(events_a, events_b)


def test_different_seed_different_realization():
    """#2 — different seeds must (with overwhelming probability) differ."""
    events_a = simulate_m1(MU, ALPHA, BETA, T0, T1, make_rng(1))
    events_b = simulate_m1(MU, ALPHA, BETA, T0, T1, make_rng(2))
    assert not np.array_equal(events_a, events_b)


def test_event_times_are_sorted():
    """#6 — simulator output must be chronologically ordered."""
    events = simulate_m1(MU, ALPHA, BETA, T0, T1, make_rng(7))
    assert events.size > 0
    assert np.all(np.diff(events) >= 0)


def test_no_events_outside_observation_window():
    """#7 — no simulated event may fall outside [t0, t1]."""
    events = simulate_m1(MU, ALPHA, BETA, T0, T1, make_rng(7))
    assert np.all(events >= T0)
    assert np.all(events <= T1)
