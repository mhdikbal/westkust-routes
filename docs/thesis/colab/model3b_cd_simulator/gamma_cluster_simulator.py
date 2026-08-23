"""Exact cluster (immigration-birth) simulator for a Hawkes process with a
Gamma-density offspring kernel and a piecewise-constant (per-calendar-year)
immigrant intensity.

This is the M3B-CD kernel-misspecification STRESS-TEST simulation path
(plan §2 row 8 / manifest S8-G1). Ground truth is simulated here with a
Gamma offspring-lag kernel; `estimate.fit_m3b_cd` (exponential kernel,
unmodified by this module) is used downstream to fit it — that
mismatch is the deliberate misspecification under test.

Why exact-cluster instead of Ogata thinning: `simulate.py`'s Ogata
thinning relies on a kernel-derived upper bound that is monotonically
valid within a segment for the *exponential* kernel (monotonically
decreasing after each event). A Gamma(shape=2) kernel is unimodal, not
monotone, so a correct Ogata bound must be a global per-event constant
(amplitude × kernel peak). That bound does not decay with elapsed time
since each past event, so as events accumulate the acceptance
probability collapses and thinning becomes combinatorially slow (this
was observed directly: a 100-replicate pilot attempt of this scenario
did not complete a single replicate in 17+ minutes before being
terminated).

The exact-cluster / branching representation (Hawkes & Oakes 1974)
avoids rejection sampling entirely: generation-0 ("immigrant") events
arrive as an inhomogeneous Poisson process at the baseline rate;
each event (immigrant or offspring) independently spawns
`K ~ Poisson(branching_ratio)` offspring, each offspring's lag since
its parent drawn directly from the (normalized) Gamma lag distribution.
Because `branching_ratio < 1` (subcritical), the process terminates
almost surely — each generation's event times strictly increase, so
offspring eventually fall outside the observation window and stop
propagating. Total work scales with the (finite, expected) total event
count, not with a collapsing acceptance rate.
"""

from __future__ import annotations

import math
from typing import Callable

import numpy as np

from .validation import validate_density_params, validate_window

_DEFAULT_MAX_TOTAL_EVENTS = 20_000


def validate_gamma_kernel_params(branching_ratio: float, gamma_shape: float, gamma_rate: float) -> None:
    """Subcriticality (branching_ratio < 1) is required for the cluster
    process to terminate almost surely — this is a stronger requirement
    than `validate_alpha`'s `>= 0` (which permits the boundary/explosive
    values that the exponential-kernel Ogata simulator can still
    represent as a finite-horizon draw)."""
    if not math.isfinite(branching_ratio) or not (0.0 <= branching_ratio < 1.0):
        raise ValueError(f"branching_ratio must be finite and in [0, 1) for a.s. termination, got {branching_ratio}")
    if not math.isfinite(gamma_shape) or gamma_shape <= 0:
        raise ValueError(f"gamma_shape must be finite and > 0, got {gamma_shape}")
    if not math.isfinite(gamma_rate) or gamma_rate <= 0:
        raise ValueError(f"gamma_rate must be finite and > 0, got {gamma_rate}")


def spawn_offspring(
    parent_t: float,
    branching_ratio: float,
    gamma_shape: float,
    gamma_rate: float,
    t1: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """K ~ Poisson(branching_ratio) offspring of one parent event; each
    offspring's lag ~ Gamma(shape=gamma_shape, rate=gamma_rate); children
    with `t_child >= t1` are discarded. Exposed as a standalone function
    so the Poisson-offspring-count and Gamma-lag mechanisms are each
    independently unit-testable without running a full cluster."""
    k = int(rng.poisson(branching_ratio))
    if k == 0:
        return np.empty(0, dtype=float)
    lags = rng.gamma(shape=gamma_shape, scale=1.0 / gamma_rate, size=k)
    children = parent_t + lags
    return children[children < t1]


def simulate_gamma_cluster_m3b_cd(
    theta0: float,
    theta1: float,
    branching_ratio: float,
    gamma_shape: float,
    gamma_rate: float,
    x_cd: Callable[[float], float],
    t0: float,
    t1: float,
    rng: np.random.Generator,
    *,
    max_total_events: int = _DEFAULT_MAX_TOTAL_EVENTS,
) -> np.ndarray:
    """Exact M3B-CD simulation with a Gamma offspring kernel (see module
    docstring). `branching_ratio` plays the role `alpha/beta` plays for
    the exponential-kernel simulator in `simulate.py` — it is NOT the
    exponential `alpha=0.4207` reused as a Gamma amplitude; the Gamma
    lag density already integrates to 1, so `branching_ratio` alone is
    both the amplitude and the expected offspring count per parent.
    """
    validate_density_params(theta0, theta1)
    validate_gamma_kernel_params(branching_ratio, gamma_shape, gamma_rate)
    validate_window(t0, t1)

    # --- generation 0: immigrants from the piecewise-constant baseline ---
    events: list[float] = []
    queue: list[float] = []
    year = math.floor(t0)
    while year < t1:
        seg_lo = max(t0, float(year))
        seg_hi = min(t1, float(year) + 1.0)
        if seg_hi > seg_lo:
            mu_y = math.exp(theta0 + theta1 * x_cd(seg_lo))
            if not math.isfinite(mu_y) or mu_y < 0:
                raise ValueError(f"immigrant intensity nonfinite/negative for year {year}: {mu_y}")
            n_y = int(rng.poisson(mu_y * (seg_hi - seg_lo)))
            if n_y > 0:
                immigrants = rng.uniform(seg_lo, seg_hi, size=n_y)
                events.extend(immigrants.tolist())
                queue.extend(immigrants.tolist())
        year += 1

    # --- generations 1..N: offspring, processed iteratively (no recursion) ---
    total_events = len(events)
    while queue:
        parent_t = queue.pop()
        children = spawn_offspring(parent_t, branching_ratio, gamma_shape, gamma_rate, t1, rng)
        if children.size:
            total_events += children.size
            if total_events > max_total_events:
                raise ValueError(
                    f"total simulated events exceeded max_total_events={max_total_events} "
                    f"(branching_ratio={branching_ratio}) -- aborting as a defensive guard, "
                    "not expected for a subcritical process; investigate before retrying"
                )
            events.extend(children.tolist())
            queue.extend(children.tolist())

    result = np.array(sorted(events))
    if result.size:
        if result.min() < t0 or result.max() >= t1:
            raise ValueError(f"simulated event outside window [{t0}, {t1}): min={result.min()}, max={result.max()}")
    return result
