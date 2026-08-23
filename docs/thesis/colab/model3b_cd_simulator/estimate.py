"""MLE estimators for M1, M2, M3B-CD.

Optimizer failures and boundary estimates are surfaced explicitly, never
hidden (plan §5 poin 6, §9 Gate A "kegagalan konvergensi... TIDAK boleh
disembunyikan"). `FitResult.status` is one of:
  - "ok"               : optimizer reported success and all params finite
  - "optimizer_failed"  : scipy.optimize.minimize reported success=False
  - "invalid"           : optimizer "succeeded" but produced a nonfinite
                           loglik or parameter (still reported, not dropped)

If a `FailureLog` is supplied, every non-"ok" fit is also appended there
as a structured record.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import minimize

from .likelihood import loglik_m1, loglik_m2, loglik_m3b_cd
from .logging_utils import FailureLog
from .schema import FitResult

_EPS = 1e-6
_BOUNDARY_TOL = 1e-3


def _boundary_flags(x: np.ndarray, bounds: list[tuple], names: list[str]) -> dict[str, bool]:
    flags = {}
    for name, value, (lo, hi) in zip(names, x, bounds):
        near_lo = lo is not None and abs(value - lo) <= _BOUNDARY_TOL
        near_hi = hi is not None and math.isfinite(hi) and abs(value - hi) <= _BOUNDARY_TOL
        flags[name] = bool(near_lo or near_hi)
    return flags


def _build_result(
    model: str,
    names: list[str],
    res,
    bounds: list[tuple],
    n_events: int,
    *,
    failure_log: FailureLog | None,
    scenario_id: str,
    grid_point_id: str,
    replicate_id: int,
) -> FitResult:
    params = dict(zip(names, np.atleast_1d(res.x).tolist()))
    fun_finite = math.isfinite(res.fun)
    params_finite = all(math.isfinite(v) for v in params.values())
    if not res.success:
        status = "optimizer_failed"
    elif not (fun_finite and params_finite):
        status = "invalid"
    else:
        status = "ok"
    result = FitResult(
        model=model,
        params=params,
        success=bool(res.success),
        status=status,
        loglik=float(-res.fun) if fun_finite else float("nan"),
        n_events=n_events,
        boundary_flags=_boundary_flags(np.atleast_1d(res.x), bounds, names),
        optimizer_message=str(getattr(res, "message", "")),
    )
    if status != "ok" and failure_log is not None:
        failure_log.log(scenario_id, grid_point_id, replicate_id, reason=status, detail=result.optimizer_message)
    return result


def fit_m1(
    events: np.ndarray,
    t0: float,
    t1: float,
    x0: tuple[float, float, float] | None = None,
    *,
    failure_log: FailureLog | None = None,
    scenario_id: str = "",
    grid_point_id: str = "",
    replicate_id: int = 0,
) -> FitResult:
    events = np.asarray(events, dtype=float)
    names = ["mu", "alpha", "beta"]
    bounds = [(_EPS, None), (0.0, None), (_EPS, None)]
    if x0 is None:
        mu0 = max(events.size / max(t1 - t0, _EPS), _EPS)
        x0 = (mu0, 0.1, 1.0)

    def neg_ll(x: np.ndarray) -> float:
        mu, alpha, beta = x
        try:
            return -loglik_m1(events, mu, alpha, beta, t0, t1)
        except ValueError:
            return math.inf

    res = minimize(neg_ll, x0=np.array(x0, dtype=float), method="L-BFGS-B", bounds=bounds)
    return _build_result(
        "m1", names, res, bounds, events.size,
        failure_log=failure_log, scenario_id=scenario_id, grid_point_id=grid_point_id, replicate_id=replicate_id,
    )


def fit_m2(
    events: np.ndarray,
    year_covariates: dict[int, float],
    t0: float,
    t1: float,
    x0: tuple[float, float] | None = None,
    *,
    failure_log: FailureLog | None = None,
    scenario_id: str = "",
    grid_point_id: str = "",
    replicate_id: int = 0,
) -> FitResult:
    events = np.asarray(events, dtype=float)
    names = ["theta0", "theta1"]
    bounds = [(None, None), (None, None)]
    if x0 is None:
        rate0 = max(events.size / max(t1 - t0, _EPS), _EPS)
        x0 = (math.log(rate0), 0.0)

    def neg_ll(x: np.ndarray) -> float:
        theta0, theta1 = x
        try:
            return -loglik_m2(events, theta0, theta1, year_covariates, t0, t1)
        except ValueError:
            return math.inf

    res = minimize(neg_ll, x0=np.array(x0, dtype=float), method="L-BFGS-B", bounds=bounds)
    return _build_result(
        "m2", names, res, bounds, events.size,
        failure_log=failure_log, scenario_id=scenario_id, grid_point_id=grid_point_id, replicate_id=replicate_id,
    )


def fit_m3b_cd(
    events: np.ndarray,
    year_covariates: dict[int, float],
    t0: float,
    t1: float,
    x0: tuple[float, float, float, float] | None = None,
    *,
    failure_log: FailureLog | None = None,
    scenario_id: str = "",
    grid_point_id: str = "",
    replicate_id: int = 0,
) -> FitResult:
    events = np.asarray(events, dtype=float)
    names = ["theta0", "theta1", "alpha", "beta"]
    bounds = [(None, None), (None, None), (0.0, None), (_EPS, None)]
    if x0 is None:
        rate0 = max(events.size / max(t1 - t0, _EPS), _EPS)
        x0 = (math.log(rate0), 0.0, 0.1, 1.0)

    def neg_ll(x: np.ndarray) -> float:
        theta0, theta1, alpha, beta = x
        try:
            return -loglik_m3b_cd(events, theta0, theta1, alpha, beta, year_covariates, t0, t1)
        except ValueError:
            return math.inf

    res = minimize(neg_ll, x0=np.array(x0, dtype=float), method="L-BFGS-B", bounds=bounds)
    return _build_result(
        "m3b_cd", names, res, bounds, events.size,
        failure_log=failure_log, scenario_id=scenario_id, grid_point_id=grid_point_id, replicate_id=replicate_id,
    )
