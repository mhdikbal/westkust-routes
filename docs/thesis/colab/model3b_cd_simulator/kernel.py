"""Exponential Hawkes excitation kernel and its closed-form compensator.

lambda_excite(t) = sum_{ti < t} alpha * exp(-beta * (t - ti))   (plan §1, M1/M3B-CD)
"""

from __future__ import annotations

import numpy as np

from .validation import validate_alpha, validate_beta


def excitation_intensity(t: float, past_event_times: np.ndarray, alpha: float, beta: float) -> float:
    """sum_{ti < t} alpha * exp(-beta * (t - ti))."""
    validate_alpha(alpha)
    validate_beta(beta)
    past = np.asarray(past_event_times, dtype=float)
    past = past[past < t]
    if past.size == 0:
        return 0.0
    return float(alpha * np.sum(np.exp(-beta * (t - past))))


def excitation_compensator(event_times: np.ndarray, alpha: float, beta: float, t0: float, t1: float) -> float:
    """integral_{t0}^{t1} sum_{ti<t} alpha*exp(-beta(t-ti)) dt for ti in [t0, t1].

    Closed form per event: (alpha/beta) * (1 - exp(-beta*(t1 - ti))).
    """
    validate_alpha(alpha)
    validate_beta(beta)
    events = np.asarray(event_times, dtype=float)
    if events.size == 0:
        return 0.0
    return float(np.sum((alpha / beta) * (1.0 - np.exp(-beta * (t1 - events)))))
