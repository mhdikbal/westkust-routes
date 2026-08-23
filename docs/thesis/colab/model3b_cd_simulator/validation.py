"""Parameter validation and numeric guards.

Enforces plan §0/§1 constraints (`alpha >= 0`, `beta > 0`) and the §9 Gate A
prerequisite that intensities are always finite and nonnegative. Every
simulator/likelihood/estimator entry point routes parameters through these
checks — invalid parameters raise immediately rather than silently
producing nonsense output.
"""

from __future__ import annotations

import math


def validate_mu(mu: float) -> None:
    if not math.isfinite(mu) or mu <= 0:
        raise ValueError(f"mu must be finite and > 0, got {mu}")


def validate_alpha(alpha: float) -> None:
    if not math.isfinite(alpha) or alpha < 0:
        raise ValueError(f"alpha must be finite and >= 0, got {alpha}")


def validate_beta(beta: float) -> None:
    if not math.isfinite(beta) or beta <= 0:
        raise ValueError(f"beta must be finite and > 0, got {beta}")


def validate_hawkes_params(mu: float, alpha: float, beta: float) -> None:
    validate_mu(mu)
    validate_alpha(alpha)
    validate_beta(beta)


def validate_density_params(theta0: float, theta1: float) -> None:
    if not math.isfinite(theta0):
        raise ValueError(f"theta0 must be finite, got {theta0}")
    if not math.isfinite(theta1):
        raise ValueError(f"theta1 must be finite, got {theta1}")


def validate_window(t0: float, t1: float) -> None:
    if not (math.isfinite(t0) and math.isfinite(t1)):
        raise ValueError("window bounds must be finite")
    if t1 <= t0:
        raise ValueError(f"require t1 > t0, got t0={t0}, t1={t1}")


def validate_event_times_in_window(event_times, t0: float, t1: float) -> None:
    for ti in event_times:
        if not (t0 <= ti <= t1):
            raise ValueError(f"event time {ti} outside observation window [{t0}, {t1}]")


def validate_intensity(value: float, *, where: str = "") -> float:
    """Guard: intensity must always be finite and nonnegative (plan §9 Gate A)."""
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"intensity must be finite and >= 0 ({where}): got {value}")
    return value


def branching_ratio(alpha: float, beta: float) -> float:
    validate_alpha(alpha)
    validate_beta(beta)
    return alpha / beta
