"""Point-process log-likelihoods for M1, M2, M3B-CD.

General form: LL = sum_i log(lambda(t_i)) - integral_{t0}^{t1} lambda(t) dt.
The compensator (integral term) is additive across the density and
excitation components, so M3B-CD's compensator is simply the sum of M2's
and M1's — no numerical integration needed anywhere in this module.
"""

from __future__ import annotations

import math

import numpy as np

from .kernel import excitation_compensator
from .validation import (
    validate_alpha,
    validate_beta,
    validate_density_params,
    validate_event_times_in_window,
    validate_hawkes_params,
    validate_intensity,
    validate_window,
)


def _density_compensator(theta0: float, theta1: float, year_covariates: dict[int, float], t0: float, t1: float) -> float:
    total = 0.0
    for year, x_year in year_covariates.items():
        seg_lo = max(t0, float(year))
        seg_hi = min(t1, float(year) + 1.0)
        if seg_hi > seg_lo:
            total += math.exp(theta0 + theta1 * x_year) * (seg_hi - seg_lo)
    return total


def _x_year(ti: float, year_covariates: dict[int, float]) -> float:
    year = int(math.floor(ti))
    if year not in year_covariates:
        raise ValueError(f"no CD density covariate available for year {year} (event at t={ti})")
    return year_covariates[year]


def loglik_m1(events: np.ndarray, mu: float, alpha: float, beta: float, t0: float, t1: float) -> float:
    validate_hawkes_params(mu, alpha, beta)
    validate_window(t0, t1)
    events = np.asarray(events, dtype=float)
    validate_event_times_in_window(events, t0, t1)
    log_intensity_sum = 0.0
    for i, ti in enumerate(events):
        past = events[:i]
        lam = mu + (alpha * np.sum(np.exp(-beta * (ti - past))) if past.size else 0.0)
        validate_intensity(lam, where="loglik_m1 event")
        log_intensity_sum += math.log(lam)
    compensator = mu * (t1 - t0) + excitation_compensator(events, alpha, beta, t0, t1)
    return float(log_intensity_sum - compensator)


def loglik_m2(events: np.ndarray, theta0: float, theta1: float, year_covariates: dict[int, float], t0: float, t1: float) -> float:
    validate_density_params(theta0, theta1)
    validate_window(t0, t1)
    events = np.asarray(events, dtype=float)
    validate_event_times_in_window(events, t0, t1)
    log_intensity_sum = 0.0
    for ti in events:
        lam = validate_intensity(math.exp(theta0 + theta1 * _x_year(ti, year_covariates)), where="loglik_m2 event")
        log_intensity_sum += math.log(lam)
    compensator = _density_compensator(theta0, theta1, year_covariates, t0, t1)
    return float(log_intensity_sum - compensator)


def loglik_m3b_cd(
    events: np.ndarray,
    theta0: float,
    theta1: float,
    alpha: float,
    beta: float,
    year_covariates: dict[int, float],
    t0: float,
    t1: float,
) -> float:
    validate_density_params(theta0, theta1)
    validate_alpha(alpha)
    validate_beta(beta)
    validate_window(t0, t1)
    events = np.asarray(events, dtype=float)
    validate_event_times_in_window(events, t0, t1)
    log_intensity_sum = 0.0
    for i, ti in enumerate(events):
        past = events[:i]
        base = math.exp(theta0 + theta1 * _x_year(ti, year_covariates))
        excite = alpha * np.sum(np.exp(-beta * (ti - past))) if past.size else 0.0
        lam = validate_intensity(base + excite, where="loglik_m3b_cd event")
        log_intensity_sum += math.log(lam)
    density_compensator = _density_compensator(theta0, theta1, year_covariates, t0, t1)
    hawkes_compensator = excitation_compensator(events, alpha, beta, t0, t1)
    return float(log_intensity_sum - density_compensator - hawkes_compensator)
