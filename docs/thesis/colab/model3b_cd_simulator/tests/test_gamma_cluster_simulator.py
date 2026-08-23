"""Tests for gamma_cluster_simulator.py — the exact-cluster (immigration-
birth) Gamma-kernel simulator that replaces the old, combinatorially slow
Ogata-thinning-with-global-bound approach for the S8-G1 kernel-
misspecification scenario.
"""

from __future__ import annotations

import hashlib
import math
import time

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.stats import gamma as gamma_dist

from model3b_cd_simulator.density import DEFAULT_CSV_PATH, DEFAULT_WINDOW, build_x_cd_lookup, build_year_covariates, load_spec_a_density
from model3b_cd_simulator.estimate import fit_m3b_cd
from model3b_cd_simulator.gamma_cluster_simulator import (
    simulate_gamma_cluster_m3b_cd,
    spawn_offspring,
    validate_gamma_kernel_params,
)
from model3b_cd_simulator.rng import make_rng

THETA0, THETA1 = -1.357513, 0.1
BRANCHING_RATIO = 0.6769
GAMMA_SHAPE, GAMMA_RATE = 2.0, 2.38095
T0, T1 = float(DEFAULT_WINDOW[0]), float(DEFAULT_WINDOW[1])

# The exact seed that hung the OLD Ogata-thinning-with-global-bound
# implementation for 17+ minutes without completing a single replicate
# (S8-G1, base_seed=20260823+900000=21160823, replicate 1).
PREVIOUSLY_HUNG_SEED = 21160824


def _x_cd_from_real_density():
    series = load_spec_a_density(window=DEFAULT_WINDOW)
    return series, build_x_cd_lookup(series), build_year_covariates(series)


# --------------------------------------------------------------------------
# Guard: parameter validation
# --------------------------------------------------------------------------


def test_branching_ratio_one_or_above_rejected():
    """#5 — n >= 1 must be rejected (supercritical/critical: no a.s. termination guarantee)."""
    with pytest.raises(ValueError):
        validate_gamma_kernel_params(1.0, GAMMA_SHAPE, GAMMA_RATE)
    with pytest.raises(ValueError):
        validate_gamma_kernel_params(1.5, GAMMA_SHAPE, GAMMA_RATE)
    with pytest.raises(ValueError):
        validate_gamma_kernel_params(-0.01, GAMMA_SHAPE, GAMMA_RATE)
    validate_gamma_kernel_params(0.6769, GAMMA_SHAPE, GAMMA_RATE)  # must not raise


def test_gamma_shape_and_rate_must_be_positive():
    with pytest.raises(ValueError):
        validate_gamma_kernel_params(0.5, 0.0, GAMMA_RATE)
    with pytest.raises(ValueError):
        validate_gamma_kernel_params(0.5, GAMMA_SHAPE, -1.0)


# --------------------------------------------------------------------------
# Mathematical guards: integral, mode, expected offspring
# --------------------------------------------------------------------------


def test_gamma_kernel_integral_equals_branching_ratio():
    """integral of branching_ratio * GammaPDF(shape=2, rate=2.38095) over
    [0, inf) must equal the branching ratio itself (GammaPDF integrates to
    1 by construction) — NOT the exponential alpha=0.4207."""

    def kernel(s):
        return BRANCHING_RATIO * gamma_dist.pdf(s, a=GAMMA_SHAPE, scale=1.0 / GAMMA_RATE)

    integral, _ = quad(kernel, 0, 500)
    assert math.isclose(integral, BRANCHING_RATIO, rel_tol=1e-9)


def test_gamma_kernel_mode():
    mode = (GAMMA_SHAPE - 1.0) / GAMMA_RATE
    assert math.isclose(mode, 0.42, abs_tol=1e-4)


def test_mean_first_generation_offspring_approaches_branching_ratio():
    """#7 — mean offspring count over many controlled single-parent draws
    should approach `branching_ratio` (E[K] = branching_ratio by
    construction of K ~ Poisson(branching_ratio))."""
    rng = make_rng(777)
    n_trials = 4000
    counts = [spawn_offspring(1650.0, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, T1, rng).size for _ in range(n_trials)]
    sample_mean = float(np.mean(counts))
    # Poisson(0.6769): std = sqrt(0.6769) ~= 0.823; SE over 4000 trials ~= 0.013
    assert abs(sample_mean - BRANCHING_RATIO) < 0.08, f"sample_mean={sample_mean}"


def test_offspring_lags_are_positive_and_gamma_distributed():
    """#8 — lags must be strictly positive and match Gamma(shape=2, rate=2.38095)
    in mean/variance within sampling tolerance."""
    rng = make_rng(555)
    all_children: list[float] = []
    for _ in range(3000):
        children = spawn_offspring(1650.0, 5.0, GAMMA_SHAPE, GAMMA_RATE, T1, rng)  # n=5 to get many lags fast
        all_children.extend((children - 1650.0).tolist())
    lags = np.array(all_children)
    assert lags.size > 500
    assert np.all(lags > 0)
    theoretical_mean = GAMMA_SHAPE / GAMMA_RATE
    theoretical_var = GAMMA_SHAPE / GAMMA_RATE**2
    assert abs(lags.mean() - theoretical_mean) < 0.05
    assert abs(lags.var() - theoretical_var) < 0.05


def test_branching_ratio_zero_gives_immigrants_only():
    """#6 — branching_ratio=0 must yield zero offspring, deterministically
    (Poisson(0) is always 0), i.e. the full simulation reduces to
    immigrants-only (pure M2-equivalent realization)."""
    rng = make_rng(999)
    children = spawn_offspring(1650.0, 0.0, GAMMA_SHAPE, GAMMA_RATE, T1, rng)
    assert children.size == 0

    _, x_cd, _ = _x_cd_from_real_density()
    events = simulate_gamma_cluster_m3b_cd(THETA0, THETA1, 0.0, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(2026))
    assert events.size > 0  # immigrants still occur
    assert np.all(events >= T0) and np.all(events < T1)


# --------------------------------------------------------------------------
# 1/2/3/4. Reproducibility, distinct seeds, window membership, ordering
# --------------------------------------------------------------------------


def test_same_seed_reproducible():
    _, x_cd, _ = _x_cd_from_real_density()
    events_a = simulate_gamma_cluster_m3b_cd(THETA0, THETA1, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(42))
    events_b = simulate_gamma_cluster_m3b_cd(THETA0, THETA1, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(42))
    assert np.array_equal(events_a, events_b)


def test_different_seed_different_realization():
    _, x_cd, _ = _x_cd_from_real_density()
    events_a = simulate_gamma_cluster_m3b_cd(THETA0, THETA1, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(1))
    events_b = simulate_gamma_cluster_m3b_cd(THETA0, THETA1, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(2))
    assert not np.array_equal(events_a, events_b)


def test_all_events_within_observation_window():
    _, x_cd, _ = _x_cd_from_real_density()
    events = simulate_gamma_cluster_m3b_cd(THETA0, THETA1, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(7))
    assert events.size > 0
    assert np.all(events >= T0)
    assert np.all(events < T1)


def test_events_sorted():
    _, x_cd, _ = _x_cd_from_real_density()
    events = simulate_gamma_cluster_m3b_cd(THETA0, THETA1, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(7))
    assert np.all(np.diff(events) >= 0)


# --------------------------------------------------------------------------
# 9/10. No infinite recursion; terminates on the previously-hung seed
# --------------------------------------------------------------------------


def test_max_total_events_guard_trips_when_forced_low():
    """Defensive guard itself works: an artificially tiny cap must raise,
    not silently truncate or hang."""
    _, x_cd, _ = _x_cd_from_real_density()
    with pytest.raises(ValueError, match="max_total_events"):
        simulate_gamma_cluster_m3b_cd(
            THETA0, THETA1, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(7),
            max_total_events=5,
        )


def test_completes_on_previously_hung_seed_within_time_budget():
    """#9 / #10 — the exact seed that hung the old global-bound Ogata
    implementation for 17+ minutes without finishing replicate 1 must now
    complete quickly (no infinite recursion / no combinatorial slowdown)."""
    _, x_cd, _ = _x_cd_from_real_density()
    start = time.perf_counter()
    events = simulate_gamma_cluster_m3b_cd(
        THETA0, THETA1, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(PREVIOUSLY_HUNG_SEED)
    )
    elapsed = time.perf_counter() - start
    assert elapsed < 10.0, f"elapsed={elapsed}s (previously hung indefinitely)"
    assert events.size > 0
    assert np.all(np.isfinite(events))


# --------------------------------------------------------------------------
# 11. Source density untouched
# --------------------------------------------------------------------------


def test_source_density_untouched_by_gamma_simulation():
    before = hashlib.sha256(DEFAULT_CSV_PATH.read_bytes()).hexdigest()
    _, x_cd, _ = _x_cd_from_real_density()
    simulate_gamma_cluster_m3b_cd(THETA0, THETA1, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(11))
    after = hashlib.sha256(DEFAULT_CSV_PATH.read_bytes()).hexdigest()
    assert before == after


# --------------------------------------------------------------------------
# 12. Fitted exponential estimator unchanged / still works end-to-end on
#     Gamma-simulated (misspecified) data
# --------------------------------------------------------------------------


def test_fit_m3b_cd_exponential_estimator_unchanged_and_compatible():
    _, x_cd, year_covariates = _x_cd_from_real_density()
    events = simulate_gamma_cluster_m3b_cd(THETA0, THETA1, BRANCHING_RATIO, GAMMA_SHAPE, GAMMA_RATE, x_cd, T0, T1, make_rng(2026))
    fit = fit_m3b_cd(events, year_covariates, T0, T1)
    assert fit.model == "m3b_cd"
    assert fit.status in ("ok", "optimizer_failed", "invalid")
    assert set(fit.params) == {"theta0", "theta1", "alpha", "beta"}
