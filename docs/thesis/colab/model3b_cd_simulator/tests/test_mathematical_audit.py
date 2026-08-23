"""Fase 1B — mathematical audit tests.

Cross-checks the M1/M2/M3B-CD compensators, log-likelihoods, Ogata
thinning upper-bound property, x_CD(t) piecewise-constant lookup, and
model-equivalence special cases against independent numerical
computations (quadrature, naive reference reimplementations, finite
differences). Does NOT evaluate plan §9 decision gates, does NOT change
the parameter grid, and does NOT declare simulation recovery PASS/FAIL —
`test_deterministic_recovery_on_fixed_synthetic_dataset` below only
checks the pipeline reaches a converged, sane fit, not a §9 threshold.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.optimize import approx_fprime

from model3b_cd_simulator.estimate import fit_m3b_cd
from model3b_cd_simulator.kernel import excitation_compensator, excitation_intensity
from model3b_cd_simulator.likelihood import loglik_m1, loglik_m2, loglik_m3b_cd
from model3b_cd_simulator.rng import make_rng
from model3b_cd_simulator.simulate import intensity_m3b_cd, simulate_m3b_cd

# --------------------------------------------------------------------------
# Shared fixtures (deterministic, hand-picked, not drawn from real CD data)
# --------------------------------------------------------------------------

MU, ALPHA, BETA = 0.30, 0.50, 0.80
T0, T1 = 1600.0, 1650.0
EVENTS = np.array([1605.3, 1612.8, 1630.1, 1640.0])

# year_covariates: nonzero and non-constant across years, spans [1600, 1650)
YEAR_COVARIATES = {y: 0.05 * ((y - 1600) % 7) for y in range(1600, 1650)}
THETA0, THETA1 = math.log(0.3), 0.4


def _x_cd_from_year_covariates(t: float, year_covariates: dict[int, float] = YEAR_COVARIATES) -> float:
    return year_covariates[int(math.floor(t))]


# --------------------------------------------------------------------------
# 1/2. Compensators vs independent numeric integration; log-likelihood vs
#      independent reference implementation
# --------------------------------------------------------------------------


def test_m1_compensator_matches_numeric_quadrature():
    def intensity(t: float) -> float:
        return MU + excitation_intensity(t, EVENTS, ALPHA, BETA)

    numeric, _ = quad(intensity, T0, T1, points=sorted(EVENTS.tolist()), limit=200)
    analytic = MU * (T1 - T0) + excitation_compensator(EVENTS, ALPHA, BETA, T0, T1)
    discrepancy = abs(numeric - analytic)
    assert discrepancy < 1e-8, f"discrepancy={discrepancy}"


def test_m3b_cd_compensator_matches_numeric_quadrature():
    def intensity(t: float) -> float:
        base = math.exp(THETA0 + THETA1 * _x_cd_from_year_covariates(t))
        return base + excitation_intensity(t, EVENTS, ALPHA, BETA)

    year_boundaries = [float(y) for y in range(int(T0) + 1, int(T1))]
    numeric, _ = quad(intensity, T0, T1, points=sorted(EVENTS.tolist()) + year_boundaries, limit=400)

    from model3b_cd_simulator.likelihood import _density_compensator  # noqa: PLC0415

    analytic = _density_compensator(THETA0, THETA1, YEAR_COVARIATES, T0, T1) + excitation_compensator(
        EVENTS, ALPHA, BETA, T0, T1
    )
    discrepancy = abs(numeric - analytic)
    assert discrepancy < 1e-6, f"discrepancy={discrepancy}"


def _naive_loglik_m1(events, mu, alpha, beta, t0, t1) -> float:
    """Independent, deliberately naive re-implementation (no shared helpers)."""
    ll = 0.0
    for i, ti in enumerate(events):
        lam = mu
        for tj in events[:i]:
            lam += alpha * math.exp(-beta * (ti - tj))
        ll += math.log(lam)
    compensator = mu * (t1 - t0)
    for ti in events:
        compensator += (alpha / beta) * (1.0 - math.exp(-beta * (t1 - ti)))
    return ll - compensator


def test_loglik_m1_matches_naive_reference_implementation():
    reference = _naive_loglik_m1(EVENTS, MU, ALPHA, BETA, T0, T1)
    implementation = loglik_m1(EVENTS, MU, ALPHA, BETA, T0, T1)
    discrepancy = abs(reference - implementation)
    assert discrepancy < 1e-10, f"discrepancy={discrepancy}"


def _naive_loglik_m2(events, theta0, theta1, year_covariates, t0, t1) -> float:
    ll = 0.0
    for ti in events:
        x = year_covariates[int(math.floor(ti))]
        ll += theta0 + theta1 * x  # log(exp(...)) == theta0 + theta1*x
    compensator = 0.0
    year = int(math.floor(t0))
    while year < t1:
        lo, hi = max(t0, float(year)), min(t1, float(year) + 1.0)
        if hi > lo:
            compensator += math.exp(theta0 + theta1 * year_covariates[year]) * (hi - lo)
        year += 1
    return ll - compensator


def test_loglik_m2_matches_naive_reference_implementation():
    reference = _naive_loglik_m2(EVENTS, THETA0, THETA1, YEAR_COVARIATES, T0, T1)
    implementation = loglik_m2(EVENTS, THETA0, THETA1, YEAR_COVARIATES, T0, T1)
    discrepancy = abs(reference - implementation)
    assert discrepancy < 1e-10, f"discrepancy={discrepancy}"


def _naive_loglik_m3b_cd(events, theta0, theta1, alpha, beta, year_covariates, t0, t1) -> float:
    ll = 0.0
    for i, ti in enumerate(events):
        base = math.exp(theta0 + theta1 * year_covariates[int(math.floor(ti))])
        excite = 0.0
        for tj in events[:i]:
            excite += alpha * math.exp(-beta * (ti - tj))
        ll += math.log(base + excite)
    density_comp = 0.0
    year = int(math.floor(t0))
    while year < t1:
        lo, hi = max(t0, float(year)), min(t1, float(year) + 1.0)
        if hi > lo:
            density_comp += math.exp(theta0 + theta1 * year_covariates[year]) * (hi - lo)
        year += 1
    hawkes_comp = sum((alpha / beta) * (1.0 - math.exp(-beta * (t1 - ti))) for ti in events)
    return ll - density_comp - hawkes_comp


def test_loglik_m3b_cd_matches_naive_reference_implementation():
    reference = _naive_loglik_m3b_cd(EVENTS, THETA0, THETA1, ALPHA, BETA, YEAR_COVARIATES, T0, T1)
    implementation = loglik_m3b_cd(EVENTS, THETA0, THETA1, ALPHA, BETA, YEAR_COVARIATES, T0, T1)
    discrepancy = abs(reference - implementation)
    assert discrepancy < 1e-10, f"discrepancy={discrepancy}"


# --------------------------------------------------------------------------
# 3. Ogata thinning upper-bound property at year boundaries
# --------------------------------------------------------------------------


def test_intensity_is_nonincreasing_within_a_year_segment():
    """The thinning bound lam_upper = intensity(segment_start) is only valid
    if intensity(t) <= intensity(segment_start) for all t in the segment
    (no new events added). Verify this directly on the analytic intensity,
    independent of any simulated realization."""
    past_events = np.array([1600.2, 1600.55, 1600.9])
    segment_start = 1601.0  # year boundary
    reference = intensity_m3b_cd(segment_start, past_events, THETA0, THETA1, ALPHA, BETA, _x_cd_from_year_covariates)
    for t in np.linspace(1601.0, 1601.999, 200):
        value = intensity_m3b_cd(t, past_events, THETA0, THETA1, ALPHA, BETA, _x_cd_from_year_covariates)
        assert value <= reference + 1e-12, f"upper bound violated at t={t}: {value} > {reference}"


def test_intensity_jumps_up_immediately_after_new_event_recompute():
    """Complementary check: right after an event is accepted, the bound must
    be recomputed (it is, every loop iteration in simulate_m3b_cd) because
    intensity strictly increases at that instant."""
    past_before = np.array([1600.2])
    past_after = np.array([1600.2, 1601.3])
    before = intensity_m3b_cd(1601.3 + 1e-9, past_before, THETA0, THETA1, ALPHA, BETA, _x_cd_from_year_covariates)
    after = intensity_m3b_cd(1601.3 + 1e-9, past_after, THETA0, THETA1, ALPHA, BETA, _x_cd_from_year_covariates)
    assert after > before


# --------------------------------------------------------------------------
# 4. Continuity / piecewise-constant x_CD(t) lookup
# --------------------------------------------------------------------------


def test_x_cd_lookup_constant_within_year_and_left_closed_at_boundary():
    year = 1620
    x_year = YEAR_COVARIATES[year]
    for offset in (0.0, 0.001, 0.5, 0.999):
        assert _x_cd_from_year_covariates(year + offset) == x_year
    # boundary convention: t == year belongs to `year`, not `year - 1`.
    assert _x_cd_from_year_covariates(float(year)) == YEAR_COVARIATES[year]
    assert _x_cd_from_year_covariates(float(year) - 1e-9) == YEAR_COVARIATES[year - 1]


def test_x_cd_lookup_matches_density_module_convention():
    from model3b_cd_simulator.density import CdDensitySeries, build_x_cd_lookup  # noqa: PLC0415

    years = np.arange(1600, 1610)
    counts = np.array([0, 1, 1, 5, 5, 0, 2, 2, 2, 9])
    series = CdDensitySeries(years=years, counts=counts, source_path=None)  # type: ignore[arg-type]
    x_cd = build_x_cd_lookup(series)
    for y, c in zip(years.tolist(), counts.tolist()):
        assert math.isclose(x_cd(y + 0.3), math.log1p(c))


# --------------------------------------------------------------------------
# density zero / constant, empty / single-event sequences
# --------------------------------------------------------------------------


def test_density_zero_everywhere_reduces_m2_to_homogeneous_poisson_at_exp_theta0():
    zero_covariates = {y: 0.0 for y in range(1600, 1610)}
    events = np.array([1602.5, 1605.1])
    ll = loglik_m2(events, THETA0, 1.7, zero_covariates, 1600.0, 1610.0)
    # theta1 has no effect when x_CD == 0 everywhere.
    ll_theta1_zero = loglik_m2(events, THETA0, 0.0, zero_covariates, 1600.0, 1610.0)
    assert math.isclose(ll, ll_theta1_zero, rel_tol=1e-12)


def test_density_constant_nonzero_matches_shifted_homogeneous_poisson():
    x_const = 2.0
    covariates = {y: x_const for y in range(1600, 1610)}
    events = np.array([1602.5, 1605.1, 1608.9])
    ll_m2 = loglik_m2(events, THETA0, THETA1, covariates, 1600.0, 1610.0)
    equivalent_mu = math.exp(THETA0 + THETA1 * x_const)
    ll_m1_equivalent = loglik_m1(events, equivalent_mu, 0.0, 1.0, 1600.0, 1610.0)
    assert math.isclose(ll_m2, ll_m1_equivalent, rel_tol=1e-10)


def test_empty_event_sequence_returns_negative_compensator_only():
    empty = np.array([])
    ll_m1 = loglik_m1(empty, MU, ALPHA, BETA, T0, T1)
    assert math.isclose(ll_m1, -(MU * (T1 - T0)), rel_tol=1e-12)

    ll_m2 = loglik_m2(empty, THETA0, THETA1, YEAR_COVARIATES, T0, T1)
    from model3b_cd_simulator.likelihood import _density_compensator  # noqa: PLC0415

    assert math.isclose(ll_m2, -_density_compensator(THETA0, THETA1, YEAR_COVARIATES, T0, T1), rel_tol=1e-12)

    ll_m3b = loglik_m3b_cd(empty, THETA0, THETA1, ALPHA, BETA, YEAR_COVARIATES, T0, T1)
    assert math.isclose(ll_m3b, ll_m2 - excitation_compensator(empty, ALPHA, BETA, T0, T1), rel_tol=1e-12)


def test_single_event_sequence():
    single = np.array([1620.0])
    ll = loglik_m3b_cd(single, THETA0, THETA1, ALPHA, BETA, YEAR_COVARIATES, T0, T1)
    base = math.exp(THETA0 + THETA1 * YEAR_COVARIATES[1620])
    from model3b_cd_simulator.likelihood import _density_compensator  # noqa: PLC0415

    expected = (
        math.log(base)
        - _density_compensator(THETA0, THETA1, YEAR_COVARIATES, T0, T1)
        - excitation_compensator(single, ALPHA, BETA, T0, T1)
    )
    assert math.isclose(ll, expected, rel_tol=1e-12)


# --------------------------------------------------------------------------
# 8. Event exactly at year boundary counted once, unambiguous covariate
# --------------------------------------------------------------------------


def test_event_exactly_at_year_boundary_assigned_to_starting_year_once():
    boundary_event = np.array([1620.0])
    # Perturb year_covariates so 1619 and 1620 are clearly distinguishable.
    covariates = dict(YEAR_COVARIATES)
    covariates[1619] = 0.11
    covariates[1620] = 0.99
    ll_boundary = loglik_m2(boundary_event, THETA0, THETA1, covariates, T0, T1)
    expected_log_intensity = math.log(math.exp(THETA0 + THETA1 * covariates[1620]))
    from model3b_cd_simulator.likelihood import _density_compensator  # noqa: PLC0415

    expected = expected_log_intensity - _density_compensator(THETA0, THETA1, covariates, T0, T1)
    assert math.isclose(ll_boundary, expected, rel_tol=1e-12)
    # Must NOT have used year 1619's covariate.
    wrong_log_intensity = math.log(math.exp(THETA0 + THETA1 * covariates[1619]))
    assert not math.isclose(expected_log_intensity, wrong_log_intensity)


# --------------------------------------------------------------------------
# 5/6/7. Parameterization ordering, alpha>=0/beta>0 constraint, branching ratio
#         (also exercised extensively in test_validation_and_branching_ratio.py)
# --------------------------------------------------------------------------


def test_alpha_zero_makes_m3b_cd_equal_m2():
    ll_m3b_alpha0 = loglik_m3b_cd(EVENTS, THETA0, THETA1, 0.0, BETA, YEAR_COVARIATES, T0, T1)
    ll_m2 = loglik_m2(EVENTS, THETA0, THETA1, YEAR_COVARIATES, T0, T1)
    assert math.isclose(ll_m3b_alpha0, ll_m2, rel_tol=1e-12)


def test_theta1_zero_makes_m3b_cd_baseline_constant_equal_m1():
    mu_equivalent = math.exp(THETA0)
    ll_m3b_theta1_0 = loglik_m3b_cd(EVENTS, THETA0, 0.0, ALPHA, BETA, YEAR_COVARIATES, T0, T1)
    ll_m1_equivalent = loglik_m1(EVENTS, mu_equivalent, ALPHA, BETA, T0, T1)
    assert math.isclose(ll_m3b_theta1_0, ll_m1_equivalent, rel_tol=1e-12)


# --------------------------------------------------------------------------
# 10. Optimizer compares likelihoods on the same constant/basis across models
# --------------------------------------------------------------------------


def test_m1_and_m2_agree_exactly_on_the_shared_homogeneous_poisson_submodel():
    """Item #10: if M1 and M2 disagreed on a constant term, this exact
    special-case equivalence (both reduce to the same homogeneous Poisson
    process) would fail even though each model's own likelihood is
    self-consistent."""
    rate = 0.42
    events = np.array([1601.0, 1610.0, 1625.5, 1639.9])
    ll_m1 = loglik_m1(events, rate, 0.0, 1.0, T0, T1)
    covariates = {y: 0.0 for y in range(int(T0), int(T1))}
    ll_m2 = loglik_m2(events, math.log(rate), 0.0, covariates, T0, T1)
    discrepancy = abs(ll_m1 - ll_m2)
    assert discrepancy < 1e-10, f"discrepancy={discrepancy}"


# --------------------------------------------------------------------------
# 9. Observation window interval consistency
# --------------------------------------------------------------------------


def test_widening_window_increases_compensator_by_the_added_segment_exactly():
    from model3b_cd_simulator.likelihood import _density_compensator  # noqa: PLC0415

    comp_short = _density_compensator(THETA0, THETA1, YEAR_COVARIATES, T0, 1620.0)
    comp_long = _density_compensator(THETA0, THETA1, YEAR_COVARIATES, T0, 1621.0)
    added_segment = math.exp(THETA0 + THETA1 * YEAR_COVARIATES[1620]) * 1.0
    assert math.isclose(comp_long - comp_short, added_segment, rel_tol=1e-10)


def test_no_simulated_event_reaches_or_exceeds_t1():
    events = simulate_m3b_cd(THETA0, THETA1, ALPHA, BETA, _x_cd_from_year_covariates, T0, T1, make_rng(2024))
    assert events.size > 0
    assert np.all(events < T1)
    assert np.all(events >= T0)


# --------------------------------------------------------------------------
# Finite-difference gradient check
# --------------------------------------------------------------------------


def test_loglik_m3b_cd_finite_difference_gradient_is_stable():
    """No analytic gradient is implemented anywhere in this package (L-BFGS-B
    in estimate.py uses scipy's own internal finite-difference approximation
    since no `jac` is passed). This test independently re-derives a
    finite-difference gradient at two different step sizes and checks they
    agree — a smoke check that loglik_m3b_cd has no kinks/discontinuities at
    a generic interior point (away from year boundaries and event times)."""

    def f(x: np.ndarray) -> float:
        theta0, theta1, alpha, beta = x
        return loglik_m3b_cd(EVENTS, theta0, theta1, alpha, beta, YEAR_COVARIATES, T0, T1)

    x0 = np.array([THETA0, THETA1, ALPHA, BETA])
    grad_coarse = approx_fprime(x0, f, 1e-4)
    grad_fine = approx_fprime(x0, f, 1e-6)
    max_discrepancy = float(np.max(np.abs(grad_coarse - grad_fine)))
    assert np.all(np.isfinite(grad_coarse))
    assert np.all(np.isfinite(grad_fine))
    assert max_discrepancy < 1e-3, f"max_discrepancy={max_discrepancy}"


# --------------------------------------------------------------------------
# Deterministic recovery on one fixed synthetic dataset (pipeline check only
# — NOT a §9 gate evaluation; no pilot/final replicate run)
# --------------------------------------------------------------------------


def test_deterministic_recovery_on_fixed_synthetic_dataset():
    from model3b_cd_simulator.density import DEFAULT_WINDOW, build_x_cd_lookup, build_year_covariates, load_spec_a_density  # noqa: PLC0415

    t0, t1 = float(DEFAULT_WINDOW[0]), float(DEFAULT_WINDOW[1])
    series = load_spec_a_density(window=DEFAULT_WINDOW)
    x_cd = build_x_cd_lookup(series)
    year_covariates = build_year_covariates(series)

    true_params = {"theta0": math.log(0.2573), "theta1": 0.1, "alpha": 0.4207, "beta": 0.6215}
    events = simulate_m3b_cd(
        true_params["theta0"], true_params["theta1"], true_params["alpha"], true_params["beta"],
        x_cd, t0, t1, make_rng(20260823),
    )
    fit = fit_m3b_cd(events, year_covariates, t0, t1)

    assert fit.status == "ok"
    # Loose sanity bounds only (order-of-magnitude / correct sign), NOT the
    # plan §9 pilot/final decision-gate thresholds.
    assert fit.params["alpha"] >= 0.0
    assert fit.params["beta"] > 0.0
    assert 0.0 < fit.params["alpha"] / fit.params["beta"] < 3.0
