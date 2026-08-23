"""Synthetic event simulators for M1, M2, M3B-CD (plan §1).

M1 (Hawkes baseline) and M3B-CD (density + self-excitation) use Ogata's
thinning algorithm with the intensity upper bound recomputed at the start
of each attempt and at every calendar-year boundary (the base rate is
piecewise-constant per year; the excitation term is monotonically
decreasing between events, so the bound is valid until either the next
accepted event or the next year boundary).

M2 (density-only Poisson) is simulated exactly: within each year the
intensity is constant, so event counts are Poisson and event times are
uniform on the year segment.

All randomness goes through `rng.make_rng` — no other entropy source is
used, so a given seed reproduces a given realization exactly (plan §9).
"""

from __future__ import annotations

import math
from typing import Callable

import numpy as np

from .kernel import excitation_intensity
from .validation import (
    validate_alpha,
    validate_beta,
    validate_density_params,
    validate_hawkes_params,
    validate_intensity,
    validate_window,
)


def _year_boundary(t: float) -> float:
    return math.floor(t) + 1.0


def simulate_m1(mu: float, alpha: float, beta: float, t0: float, t1: float, rng: np.random.Generator) -> np.ndarray:
    """M1 — Hawkes baseline: lambda(t) = mu + sum_{ti<t} alpha*exp(-beta(t-ti))."""
    validate_hawkes_params(mu, alpha, beta)
    validate_window(t0, t1)
    events: list[float] = []
    t = t0
    while t < t1:
        excite = excitation_intensity(t, np.array(events), alpha, beta)
        lam_upper = mu + excite
        t_candidate = t + rng.exponential(1.0 / lam_upper)
        if t_candidate >= t1:
            break
        excite_c = excitation_intensity(t_candidate, np.array(events), alpha, beta)
        lam_actual = validate_intensity(mu + excite_c, where="simulate_m1")
        if rng.uniform() <= lam_actual / lam_upper:
            events.append(t_candidate)
        t = t_candidate
    return np.array(sorted(events))


def simulate_m2(
    theta0: float,
    theta1: float,
    x_cd: Callable[[float], float],
    t0: float,
    t1: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """M2 — CD-density-only Poisson: lambda(t) = exp(theta0 + theta1*x_CD(t)).

    Exact simulation (no thinning needed): intensity is piecewise-constant
    per calendar year.
    """
    validate_density_params(theta0, theta1)
    validate_window(t0, t1)
    events: list[float] = []
    year = math.floor(t0)
    while year < t1:
        seg_lo = max(t0, float(year))
        seg_hi = min(t1, float(year) + 1.0)
        if seg_hi > seg_lo:
            lam = validate_intensity(math.exp(theta0 + theta1 * x_cd(seg_lo)), where="simulate_m2")
            n = rng.poisson(lam * (seg_hi - seg_lo))
            if n > 0:
                events.extend(rng.uniform(seg_lo, seg_hi, size=n).tolist())
        year += 1
    return np.array(sorted(events))


def simulate_m3b_cd(
    theta0: float,
    theta1: float,
    alpha: float,
    beta: float,
    x_cd: Callable[[float], float],
    t0: float,
    t1: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """M3B-CD — density + self-excitation combined:
    lambda(t) = exp(theta0 + theta1*x_CD(t)) + sum_{ti<t} alpha*exp(-beta(t-ti)).
    """
    validate_density_params(theta0, theta1)
    validate_alpha(alpha)
    validate_beta(beta)
    validate_window(t0, t1)
    events: list[float] = []
    t = t0
    while t < t1:
        boundary = min(_year_boundary(t), t1)
        base = math.exp(theta0 + theta1 * x_cd(t))
        excite = excitation_intensity(t, np.array(events), alpha, beta)
        lam_upper = base + excite
        t_candidate = t + rng.exponential(1.0 / lam_upper)
        if t_candidate >= boundary:
            t = boundary
            continue
        base_c = math.exp(theta0 + theta1 * x_cd(t_candidate))
        excite_c = excitation_intensity(t_candidate, np.array(events), alpha, beta)
        lam_actual = validate_intensity(base_c + excite_c, where="simulate_m3b_cd")
        if rng.uniform() <= lam_actual / lam_upper:
            events.append(t_candidate)
        t = t_candidate
    return np.array(sorted(events))


def intensity_m1(t: float, past_event_times: np.ndarray, mu: float, alpha: float, beta: float) -> float:
    validate_hawkes_params(mu, alpha, beta)
    return validate_intensity(mu + excitation_intensity(t, past_event_times, alpha, beta), where="intensity_m1")


def intensity_m2(t: float, theta0: float, theta1: float, x_cd: Callable[[float], float]) -> float:
    validate_density_params(theta0, theta1)
    return validate_intensity(math.exp(theta0 + theta1 * x_cd(t)), where="intensity_m2")


def intensity_m3b_cd(
    t: float,
    past_event_times: np.ndarray,
    theta0: float,
    theta1: float,
    alpha: float,
    beta: float,
    x_cd: Callable[[float], float],
) -> float:
    validate_density_params(theta0, theta1)
    validate_alpha(alpha)
    validate_beta(beta)
    base = math.exp(theta0 + theta1 * x_cd(t))
    excite = excitation_intensity(t, past_event_times, alpha, beta)
    return validate_intensity(base + excite, where="intensity_m3b_cd")
