"""Reference audit for Fase 3A statistical instrumentation.

Cross-checks hessian.py's Hessian, standard errors, AIC/BIC, and the
branching-ratio delta-method SE against independently hand-coded
reference computations, on one small HARDCODED event sequence (no
simulate_* calls). Reports maximum discrepancy explicitly, mirroring
Fase 1B's `test_mathematical_audit.py` pattern.
"""

from __future__ import annotations

import math

import numpy as np

from model3b_cd_simulator import inference as inf
from model3b_cd_simulator.likelihood import loglik_m3b_cd

T0, T1 = 1600.0, 1650.0
YEAR_COVARIATES = {y: 0.05 * ((y - 1600) % 7) for y in range(1600, 1650)}
INTERIOR_EVENTS = np.array([
    1601.5, 1601.7, 1601.9, 1602.3, 1603.1, 1603.4, 1605.9, 1606.1, 1606.3, 1608.1,
    1608.3, 1610.4, 1610.6, 1610.8, 1615.3, 1615.5, 1620.7, 1620.9, 1622.1, 1625.0,
])


def _independent_central_hessian(f, x: np.ndarray, h: float = 1e-4) -> np.ndarray:
    """Independent reference implementation: fixed step size, plain central
    4-point mixed-partial stencil, no bound-awareness, no shared code path
    with hessian.py."""
    n = x.size
    f0 = f(x)
    H = np.zeros((n, n))
    for i in range(n):
        xp, xm = x.copy(), x.copy()
        xp[i] += h
        xm[i] -= h
        H[i, i] = (f(xp) - 2 * f0 + f(xm)) / (h * h)
    for i in range(n):
        for j in range(i + 1, n):
            xpp, xpm, xmp, xmm = x.copy(), x.copy(), x.copy(), x.copy()
            xpp[i] += h; xpp[j] += h
            xpm[i] += h; xpm[j] -= h
            xmp[i] -= h; xmp[j] += h
            xmm[i] -= h; xmm[j] -= h
            v = (f(xpp) - f(xpm) - f(xmp) + f(xmm)) / (4 * h * h)
            H[i, j] = v
            H[j, i] = v
    return (H + H.T) / 2.0


def test_reference_audit_hessian_se_aic_bic_branching_ratio():
    report = inf.fit_m3b_cd_with_inference(INTERIOR_EVENTS, YEAR_COVARIATES, T0, T1)
    assert report.covariance.status == "valid", "reference audit requires an interior (well-conditioned) fit"

    theta0, theta1, alpha, beta = (report.fit.params[k] for k in ("theta0", "theta1", "alpha", "beta"))

    def neg_ll(x):
        t0_, t1_, a_, b_ = x
        try:
            return -loglik_m3b_cd(INTERIOR_EVENTS, t0_, t1_, a_, b_, YEAR_COVARIATES, T0, T1)
        except ValueError:
            return math.inf

    x_hat = np.array([theta0, theta1, alpha, beta])
    H_reference = _independent_central_hessian(neg_ll, x_hat)
    H_implementation = report.covariance.diagnostics.hessian_symmetrized

    hessian_discrepancy = float(np.max(np.abs(H_reference - H_implementation)))
    # relative comparison too, since raw entries vary widely in magnitude
    scale = float(np.max(np.abs(H_reference))) or 1.0
    relative_hessian_discrepancy = hessian_discrepancy / scale

    cov_reference = np.linalg.inv(H_reference)
    se_reference = {name: math.sqrt(cov_reference[i, i]) for i, name in enumerate(report.param_names)}
    se_discrepancies = {name: abs(se_reference[name] - report.standard_errors[name]) for name in report.param_names}
    max_se_discrepancy = max(se_discrepancies.values())

    aic_reference = 2 * 4 - 2 * report.fit.loglik
    bic_reference = 4 * math.log(INTERIOR_EVENTS.size) - 2 * report.fit.loglik
    aic_discrepancy = abs(aic_reference - report.aic)
    bic_discrepancy = abs(bic_reference - report.bic)

    g_reference = np.array([1.0 / beta, -alpha / beta**2])
    idx = {name: i for i, name in enumerate(report.param_names)}
    sub_cov_reference = cov_reference[np.ix_([idx["alpha"], idx["beta"]], [idx["alpha"], idx["beta"]])]
    se_br_reference = math.sqrt(float(g_reference @ sub_cov_reference @ g_reference))
    se_br_discrepancy = abs(se_br_reference - report.branching_ratio.branching_ratio_standard_error)

    max_discrepancy = max(relative_hessian_discrepancy, max_se_discrepancy, aic_discrepancy, bic_discrepancy, se_br_discrepancy)

    print(f"[reference audit] relative_hessian_discrepancy={relative_hessian_discrepancy:.3e}")
    print(f"[reference audit] max_se_discrepancy={max_se_discrepancy:.3e} ({se_discrepancies})")
    print(f"[reference audit] aic_discrepancy={aic_discrepancy:.3e} bic_discrepancy={bic_discrepancy:.3e}")
    print(f"[reference audit] branching_ratio_se_discrepancy={se_br_discrepancy:.3e}")
    print(f"[reference audit] MAX_DISCREPANCY={max_discrepancy:.3e}")

    assert relative_hessian_discrepancy < 1e-2
    assert max_se_discrepancy < 1e-2
    assert aic_discrepancy < 1e-8
    assert bic_discrepancy < 1e-8
    assert se_br_discrepancy < 1e-2
