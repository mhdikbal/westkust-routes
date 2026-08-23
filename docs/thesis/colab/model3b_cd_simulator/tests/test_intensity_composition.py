"""Unit tests #3, #4, #5 (Fase 1 requirement list).

Tested at the level of the intensity functions (analytic), not via
statistical comparison of simulated counts — this keeps the tests
deterministic rather than relying on random-seed luck.
"""

import math

import numpy as np

from model3b_cd_simulator.simulate import intensity_m1, intensity_m2, intensity_m3b_cd

THETA0, THETA1 = math.log(0.2573), 0.1
ALPHA, BETA = 0.4207, 0.6215


def _x_cd(t: float) -> float:
    return 1.5  # fixed covariate value for this test module


def test_density_only_alpha_zero_matches_m2_intensity():
    """#3 — M3B-CD with alpha=0 must equal the pure density-only (M2) intensity."""
    past = np.array([])
    lam_m3b = intensity_m3b_cd(1650.0, past, THETA0, THETA1, 0.0, BETA, _x_cd)
    lam_m2 = intensity_m2(1650.0, THETA0, THETA1, _x_cd)
    assert math.isclose(lam_m3b, lam_m2, rel_tol=1e-12)


def test_excitation_only_theta1_zero_matches_m1_intensity():
    """#4 — M3B-CD with theta1=0 must equal the pure self-excitation (M1) intensity,
    with mu = exp(theta0)."""
    past = np.array([1620.0, 1630.0])
    mu = math.exp(THETA0)
    lam_m3b = intensity_m3b_cd(1650.0, past, THETA0, 0.0, ALPHA, BETA, _x_cd)
    lam_m1 = intensity_m1(1650.0, past, mu, ALPHA, BETA)
    assert math.isclose(lam_m3b, lam_m1, rel_tol=1e-12)


def test_combined_intensity_is_sum_of_components():
    """#5 — M3B-CD intensity must equal density-component + excitation-component,
    exactly (no interaction term)."""
    past = np.array([1610.0, 1640.0, 1645.0])
    lam_m3b = intensity_m3b_cd(1650.0, past, THETA0, THETA1, ALPHA, BETA, _x_cd)
    density_component = math.exp(THETA0 + THETA1 * _x_cd(1650.0))
    # mu=0 is invalid for intensity_m1 (validate_mu requires mu>0), so the
    # excitation-only piece is computed directly here instead of reusing it.
    excitation_component = sum(ALPHA * math.exp(-BETA * (1650.0 - ti)) for ti in past)
    assert math.isclose(lam_m3b, density_component + excitation_component, rel_tol=1e-12)
