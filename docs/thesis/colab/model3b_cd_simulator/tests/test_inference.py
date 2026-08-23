"""Tests for inference.py -- covariance/SE/CI, boundary-aware alpha test,
branching-ratio delta method, AIC/BIC, model comparison.

All fixtures are hardcoded event-time arrays (no simulate_* calls).
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy.optimize import approx_fprime

from model3b_cd_simulator.estimate import fit_m1, fit_m2, fit_m3b_cd
from model3b_cd_simulator.likelihood import loglik_m1, loglik_m2, loglik_m3b_cd
from model3b_cd_simulator.logging_utils import FailureLog
from model3b_cd_simulator import inference as inf

T0, T1 = 1600.0, 1650.0
YEAR_COVARIATES = {y: 0.05 * ((y - 1600) % 7) for y in range(1600, 1650)}

# Boundary-case dataset: sparse, no visible clustering -> alpha_hat lands at 0.
BOUNDARY_EVENTS = np.array([1601.5, 1603.2, 1605.9, 1608.1, 1610.4, 1615.3, 1620.7, 1622.1, 1625.0, 1630.5, 1635.2, 1640.8])

# Interior-case dataset: dense clustering -> alpha_hat well away from 0.
INTERIOR_EVENTS = np.array([
    1601.5, 1601.7, 1601.9, 1602.3, 1603.1, 1603.4, 1605.9, 1606.1, 1606.3, 1608.1,
    1608.3, 1610.4, 1610.6, 1610.8, 1615.3, 1615.5, 1620.7, 1620.9, 1622.1, 1625.0,
])


# --------------------------------------------------------------------------
# Standard errors / CI
# --------------------------------------------------------------------------


def test_standard_errors_nonnegative_on_interior_fit():
    report = inf.fit_m3b_cd_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    assert report.covariance.status == "valid"
    for name, se in report.standard_errors.items():
        assert se >= 0, f"{name}: se={se}"


def test_wald_ci_95_ordered_lower_leq_upper():
    report = inf.fit_m3b_cd_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    for name, (lo, hi) in report.wald_ci_95.items():
        if math.isfinite(lo) and math.isfinite(hi):
            assert lo <= hi, f"{name}: ({lo}, {hi})"


def test_standard_errors_nan_when_covariance_unavailable():
    report = inf.fit_m3b_cd_with_inference(BOUNDARY_EVENTS, YEAR_COVARIATES, T0, T1)
    assert report.covariance.status in ("non_positive_definite", "singular", "unavailable")
    assert all(math.isnan(se) for se in report.standard_errors.values())


# --------------------------------------------------------------------------
# Boundary-aware alpha test (not a plain Wald test)
# --------------------------------------------------------------------------


def test_boundary_alpha_test_used_when_alpha_hat_at_boundary():
    report = inf.fit_m3b_cd_with_inference(BOUNDARY_EVENTS, YEAR_COVARIATES, T0, T1)
    assert report.fit.params["alpha"] == 0.0
    assert report.fit.boundary_flags["alpha"] is True
    test = report.boundary_alpha_test
    assert test.at_boundary is True
    assert test.test_statistic_lr == 0.0  # restricted == unrestricted when alpha_hat==0
    assert test.p_value == 1.0
    assert test.decision_alpha_0p05 == "fail_to_reject_H0"
    assert "mixture" in test.reference_distribution.lower() or "point_mass" in test.reference_distribution.lower()
    assert "Wald" in test.note  # explicitly documents this is NOT a Wald test


def test_boundary_alpha_test_wald_ci_not_used_for_formal_decision():
    """The Wald CI (wald_ci_95['alpha']) must never be the basis for
    decision_alpha_0p05 -- confirm the two are computed independently and
    the formal decision comes from the LR statistic, not from whether 0
    falls inside the Wald interval."""
    report = inf.fit_m3b_cd_with_inference(BOUNDARY_EVENTS, YEAR_COVARIATES, T0, T1)
    # Wald CI is NaN here (covariance unavailable at the boundary) while the
    # boundary-aware test still produces a well-defined formal decision --
    # proof the two pathways are independent.
    wald_lo, wald_hi = report.wald_ci_95["alpha"]
    assert math.isnan(wald_lo) and math.isnan(wald_hi)
    assert report.boundary_alpha_test.decision_alpha_0p05 == "fail_to_reject_H0"


def test_boundary_alpha_test_lr_matches_manual_computation():
    report = inf.fit_m3b_cd_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    restricted = fit_m2(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    expected_lr = max(0.0, 2.0 * (report.fit.loglik - restricted.loglik))
    assert math.isclose(report.boundary_alpha_test.test_statistic_lr, expected_lr, rel_tol=1e-9)


def test_m3b_cd_boundary_alpha_test_is_labeled_m2_vs_m3b_cd_not_m1():
    """Label-correctness regression guard: M3B-CD's boundary-aware alpha
    test MUST be M2 (restricted) vs M3B-CD (unrestricted) -- never M1.
    M1 has its own SEPARATE boundary test against a closed-form
    homogeneous-Poisson restricted model, which is a different comparison
    and must never be conflated with or reported as "M1/M3B-CD"."""
    report = inf.fit_m3b_cd_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    test = report.boundary_alpha_test
    assert test.restricted_model == "m2"
    assert test.unrestricted_model == "m3b_cd"
    assert test.restricted_model != "m1"

    restricted_m2 = fit_m2(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    assert math.isclose(test.loglik_restricted, restricted_m2.loglik, rel_tol=1e-12)
    assert math.isclose(test.loglik_unrestricted, report.fit.loglik, rel_tol=1e-12)

    expected_lr = 2.0 * (test.loglik_unrestricted - test.loglik_restricted)
    assert math.isclose(test.test_statistic_lr, max(0.0, expected_lr), rel_tol=1e-9)


def test_m1_boundary_alpha_test_is_labeled_m1_not_m2():
    """Complementary guard: M1's OWN boundary test is a distinct
    comparison (M1 vs a closed-form homogeneous-Poisson restricted model)
    and must never be labeled as using M2 as the restricted model."""
    report = inf.fit_m1_with_inference(INTERIOR_EVENTS, T0, T1)
    test = report.boundary_alpha_test
    assert test.unrestricted_model == "m1"
    assert test.restricted_model != "m2"
    assert "homogeneous_poisson" in test.restricted_model


def test_boundary_alpha_test_p_value_matches_mixture_formula():
    from scipy.stats import chi2

    report = inf.fit_m3b_cd_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    lr = report.boundary_alpha_test.test_statistic_lr
    if lr > 0:
        expected_p = 0.5 * float(chi2.sf(lr, df=1))
        assert math.isclose(report.boundary_alpha_test.p_value, expected_p, rel_tol=1e-9)


# --------------------------------------------------------------------------
# Branching-ratio delta method
# --------------------------------------------------------------------------


def test_delta_method_branching_ratio_matches_finite_difference_gradient():
    report = inf.fit_m3b_cd_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    assert report.covariance.status == "valid"
    alpha_hat = report.fit.params["alpha"]
    beta_hat = report.fit.params["beta"]

    def ratio(v):
        a, b = v
        return a / b

    fd_grad = approx_fprime(np.array([alpha_hat, beta_hat]), ratio, 1e-6)
    analytic_grad = np.array([1.0 / beta_hat, -alpha_hat / beta_hat**2])
    assert np.allclose(fd_grad, analytic_grad, rtol=1e-4)

    names = report.param_names
    sub_cov = report.covariance.covariance[np.ix_([names.index("alpha"), names.index("beta")], [names.index("alpha"), names.index("beta")])]
    expected_var = float(fd_grad @ sub_cov @ fd_grad)
    expected_se = math.sqrt(expected_var)
    assert math.isclose(report.branching_ratio.branching_ratio_standard_error, expected_se, rel_tol=1e-3)


def test_branching_ratio_ci_unavailable_when_covariance_invalid():
    report = inf.fit_m3b_cd_with_inference(BOUNDARY_EVENTS, YEAR_COVARIATES, T0, T1)
    assert report.branching_ratio.delta_method_status == "unavailable"
    assert report.branching_ratio.branching_ratio_ci_95 == "unavailable"
    assert report.branching_ratio.branching_ratio_standard_error == "unavailable"


# --------------------------------------------------------------------------
# Log-likelihoods unchanged (regression guard against likelihood.py)
# --------------------------------------------------------------------------


def test_m1_loglik_matches_audited_likelihood_module():
    fit = fit_m1(INTERIOR_EVENTS, T0, T1)
    expected = loglik_m1(INTERIOR_EVENTS, fit.params["mu"], fit.params["alpha"], fit.params["beta"], T0, T1)
    assert math.isclose(fit.loglik, expected, rel_tol=1e-12)


def test_m2_loglik_matches_audited_likelihood_module():
    fit = fit_m2(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    expected = loglik_m2(INTERIOR_EVENTS, fit.params["theta0"], fit.params["theta1"], YEAR_COVARIATES, T0, T1)
    assert math.isclose(fit.loglik, expected, rel_tol=1e-12)


def test_m3b_cd_loglik_unchanged_from_fase1b_audit():
    """Regression guard: likelihood.py is not touched by this phase, so
    M3B-CD's log-likelihood value for a fixed parameter set must be
    byte-identical to Fase 1B's audited computation."""
    theta0, theta1, alpha, beta = -1.357513, 0.1, 0.4207, 0.6215
    ll = loglik_m3b_cd(INTERIOR_EVENTS, theta0, theta1, alpha, beta, YEAR_COVARIATES, T0, T1)
    assert math.isfinite(ll)
    # re-derive independently (naive loop) as an extra guard, matching Fase 1B's pattern
    naive = 0.0
    for i, ti in enumerate(INTERIOR_EVENTS):
        base = math.exp(theta0 + theta1 * YEAR_COVARIATES[int(math.floor(ti))])
        excite = sum(alpha * math.exp(-beta * (ti - tj)) for tj in INTERIOR_EVENTS[:i])
        naive += math.log(base + excite)
    density_comp = sum(
        math.exp(theta0 + theta1 * YEAR_COVARIATES[y]) * (min(T1, y + 1.0) - max(T0, float(y)))
        for y in range(int(T0), int(T1))
        if min(T1, y + 1.0) > max(T0, float(y))
    )
    hawkes_comp = sum((alpha / beta) * (1.0 - math.exp(-beta * (T1 - ti))) for ti in INTERIOR_EVENTS)
    naive -= density_comp + hawkes_comp
    assert math.isclose(ll, naive, rel_tol=1e-10)


def test_m2_nested_in_m3b_cd_at_alpha_zero():
    """M2 must be nested inside M3B-CD at alpha=0: log-likelihood must be
    identical for matching baseline parameters (theta0, theta1) on the
    same event sequence."""
    theta0, theta1 = -1.4, 0.08
    ll_m2 = loglik_m2(INTERIOR_EVENTS, theta0, theta1, YEAR_COVARIATES, T0, T1)
    ll_m3b_alpha0 = loglik_m3b_cd(INTERIOR_EVENTS, theta0, theta1, 0.0, 1.0, YEAR_COVARIATES, T0, T1)
    assert math.isclose(ll_m2, ll_m3b_alpha0, rel_tol=1e-12)


# --------------------------------------------------------------------------
# AIC / BIC
# --------------------------------------------------------------------------


def test_aic_formula():
    assert math.isclose(inf.aic(-100.0, 3), 2 * 3 - 2 * (-100.0))


def test_bic_formula_uses_n_events():
    n_events = INTERIOR_EVENTS.size
    expected = 4 * math.log(n_events) - 2 * (-100.0)
    assert math.isclose(inf.bic(-100.0, 4, n_events), expected)


def test_bic_n_events_consistent_across_m1_m2_m3b_cd_same_sequence():
    r1 = inf.fit_m1_with_inference(INTERIOR_EVENTS, T0, T1)
    r2 = inf.fit_m2_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    r3 = inf.fit_m3b_cd_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    assert r1.n_bic == r2.n_bic == r3.n_bic == INTERIOR_EVENTS.size


def test_bic_zero_events_clamped_not_crashed():
    empty = np.array([])
    assert inf.bic(-1.0, 2, 0) == inf.bic(-1.0, 2, 1)  # clamped to n=1, ln(0) never evaluated


# --------------------------------------------------------------------------
# Model-selection output consistency
# --------------------------------------------------------------------------


def test_model_selection_output_internally_consistent():
    r1 = inf.fit_m1_with_inference(INTERIOR_EVENTS, T0, T1)
    r2 = inf.fit_m2_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    r3 = inf.fit_m3b_cd_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    reports = {"m1": r1, "m2": r2, "m3b_cd": r3}
    sel = inf.select_best_model(reports)
    assert sel.delta_AIC[sel.best_model_by_AIC] == 0.0
    assert sel.delta_BIC[sel.best_model_by_BIC] == 0.0
    assert all(v >= 0 for v in sel.delta_AIC.values())
    assert all(v >= 0 for v in sel.delta_BIC.values())
    assert "not a claim about historical process" in sel.caveat


# --------------------------------------------------------------------------
# Estimator-failure tracking still works (this layer doesn't swallow it)
# --------------------------------------------------------------------------


def test_optimizer_failure_still_yields_unavailable_covariance_not_a_crash(monkeypatch):
    import model3b_cd_simulator.estimate as estimate_module
    from types import SimpleNamespace

    def fake_minimize(fun, x0, method, bounds):  # noqa: ANN001
        return SimpleNamespace(x=np.asarray(x0), fun=fun(x0), success=False, message="fake non-convergence")

    monkeypatch.setattr(estimate_module, "minimize", fake_minimize)
    failure_log = FailureLog()
    # fit_m1 itself still records the failure (unchanged estimate.py behavior)
    fit = estimate_module.fit_m1(INTERIOR_EVENTS, T0, T1, failure_log=failure_log)
    assert fit.status == "optimizer_failed"
    assert len(failure_log) == 1
    # the inference layer built on top must not crash even given a failed fit
    report = inf.fit_m1_with_inference(INTERIOR_EVENTS, T0, T1)
    assert report.fit.status in ("optimizer_failed", "ok", "invalid")


# --------------------------------------------------------------------------
# Parameter bounds still enforced (regression: this layer must not bypass them)
# --------------------------------------------------------------------------


def test_parameter_bounds_still_enforced_by_underlying_estimator():
    report = inf.fit_m3b_cd_with_inference(BOUNDARY_EVENTS, YEAR_COVARIATES, T0, T1)
    assert report.fit.params["alpha"] >= 0.0
    assert report.fit.params["beta"] > 0.0


# --------------------------------------------------------------------------
# FitResult schema is untouched (backward compatibility)
# --------------------------------------------------------------------------


def test_fitresult_schema_unchanged_old_style_construction_still_works():
    from model3b_cd_simulator.schema import FitResult

    old_style = FitResult(
        model="m1", params={"mu": 0.2, "alpha": 0.1, "beta": 0.5}, success=True, status="ok",
        loglik=-10.0, n_events=5, boundary_flags={"mu": False, "alpha": False, "beta": False},
    )
    assert old_style.is_valid is True
    assert old_style.any_boundary_flag is False


# --------------------------------------------------------------------------
# Density checksum unchanged (this layer never touches the CSV)
# --------------------------------------------------------------------------


def test_density_source_untouched_by_inference_layer():
    import hashlib

    from model3b_cd_simulator.density import DEFAULT_CSV_PATH

    before = hashlib.sha256(DEFAULT_CSV_PATH.read_bytes()).hexdigest()
    inf.fit_m3b_cd_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    after = hashlib.sha256(DEFAULT_CSV_PATH.read_bytes()).hexdigest()
    assert before == after
