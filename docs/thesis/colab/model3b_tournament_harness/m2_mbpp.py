"""M2 -- MBPP interval-censored Hawkes (Rizoiu et al. 2022, JMLR vol 23 no
338, "Interval-censored Hawkes processes"), extended from
docs/thesis/colab/model3_mbpp_full.py's constant-baseline (s(t)=mu) form
to the M3B-CD combined form (density-covariate baseline + excitation).

Reuses model3_mbpp_full.py's xi_closed_form / Xi_closed_form (Eq. 9/10)
and neg_ic_ll (Eq. 18) DIRECTLY (imported, not reimplemented) for the
constant-baseline special case; this module's own
xi_closed_form_density_baseline / Xi_closed_form_density_baseline extend
the same closed-form derivation to a piecewise-constant-per-year baseline
s(t) = exp(theta0 + theta1 * x_CD(year(t))) instead of a single constant
mu, since M3B-CD's own generative form (model3b_cd_simulator/kernel.py,
likelihood.py) already uses exactly this piecewise-constant density
baseline and M2 is meant to test the SAME density+excitation combination
under year-level interval censoring rather than V1's fabricated point
timestamps.

Derivation note (new work, not in the original paper or model3_mbpp_full.py):
Eq (9)'s self-consistent ODE for xi(t), xi'(t) = s(t) - (beta-alpha)*xi(t)
+ ... [see model3_mbpp_full.py docstring for the constant-s(t) derivation],
does NOT have a single closed form when s(t) is itself piecewise-constant
across year boundaries. This module instead solves it PIECEWISE: within
each year segment, s(t) is locally constant, so the SAME closed-form
solution from model3_mbpp_full.py applies on that segment, with the
initial condition carried forward from the end of the previous segment
(continuity of xi(t) across boundaries, matching the ODE's own
first-order continuity requirement). This is an exact, closed-form
piecewise solution -- no numerical ODE integration is used anywhere.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

_THIS_DIR = Path(__file__).resolve().parent
_COLAB_DIR = _THIS_DIR.parent
sys.path.insert(0, str(_THIS_DIR))
sys.path.insert(0, str(_COLAB_DIR))
from model3_mbpp_full import Xi_closed_form, xi_closed_form  # noqa: E402  (reused as-is for the constant-segment building block)
from observation_pipeline import (  # noqa: E402
    CensoredEvent,
    apply_missing_and_duplicate_reporting,
    assign_synthetic_sources,
    censor_events,
    generate_episode_structured_latent_events,
    observe_events,
)
from model3b_cd_simulator.simulate import simulate_m3b_cd  # noqa: E402  (Stage 1, reused as-is per the spec)

_EPS = 1e-6
_BOUNDARY_TOL = 1e-3


@dataclass
class M2FitResult:
    params: dict[str, float]  # theta0, theta1, alpha, beta
    success: bool
    status: str
    loglik: float
    n_events: int
    boundary_flags: dict[str, bool]
    optimizer_message: str = ""

    @property
    def is_valid(self) -> bool:
        return self.status == "ok"

    @property
    def any_boundary_flag(self) -> bool:
        return any(self.boundary_flags.values())


def _xi_general(local_t: float, xi0: float, mu_seg: float, alpha: float, beta: float) -> float:
    """General solution of the ODE xi'(tau) = -(beta-alpha)*xi(tau) + beta*mu_seg
    with initial condition xi(0)=xi0 (derived by hand from Eq 9's linear
    ODE form; verified against model3_mbpp_full.xi_closed_form, which is
    the special case xi0=mu_seg -- i.e. 'process turns on fresh here with
    no carried-forward history'):
        xi(tau) = xi_closed_form(tau, mu_seg, alpha, beta) + (xi0 - mu_seg)*exp(-(beta-alpha)*tau)
    Verified by direct differentiation (see module docstring derivation
    note) and by a constant-baseline regression check
    (docs/thesis/colab/model3b_tournament_harness/m2_smoke_test.py) against
    model3_mbpp_full.Xi_closed_form when theta1=0 (single segment, so this
    reduces to xi0=mu exactly and the two must match to numerical precision)."""
    k = beta - alpha
    decay = math.exp(-k * local_t) if abs(k) > 1e-9 else 1.0
    return xi_closed_form(local_t, mu_seg, alpha, beta) + (xi0 - mu_seg) * decay


def xi_closed_form_density_baseline(
    t_points: np.ndarray, theta0: float, theta1: float, alpha: float, beta: float,
    year_covariates: dict[int, float], t0: float,
) -> np.ndarray:
    """Piecewise-exact xi(t) for a year-piecewise-constant baseline
    s(year) = exp(theta0 + theta1*x_CD(year)), evaluated at each of
    t_points (must be sorted, all >= t0). Solved segment-by-segment via
    _xi_general above, carrying the boundary value (not zero) forward for
    continuity across year boundaries -- xi(t) must be continuous even
    though s(t) jumps discontinuously at each year boundary, since xi(t)
    is defined by an integral equation (Eq 9), not a memoryless reset."""
    t_points = np.asarray(sorted(t_points), dtype=float)
    out = np.empty_like(t_points)
    seg_start = t0
    year = int(math.floor(t0))
    idx = 0
    max_year = int(math.floor(t_points[-1])) + 2 if t_points.size else year + 1
    x0 = year_covariates.get(year, 0.0)
    xi_at_seg_start = math.exp(theta0 + theta1 * x0)  # xi(t0) = mu(t0): fresh start, no prior history
    while idx < t_points.size and year <= max_year:
        seg_end = float(year) + 1.0
        x = year_covariates.get(year, 0.0)
        mu_seg = math.exp(theta0 + theta1 * x)
        while idx < t_points.size and t_points[idx] < seg_end:
            local_t = t_points[idx] - seg_start
            out[idx] = _xi_general(local_t, xi_at_seg_start, mu_seg, alpha, beta)
            idx += 1
        local_seg_width = seg_end - seg_start
        xi_at_seg_start = _xi_general(local_seg_width, xi_at_seg_start, mu_seg, alpha, beta)
        seg_start = seg_end
        year += 1
    return out


def Xi_closed_form_density_baseline(
    bin_edges: np.ndarray, theta0: float, theta1: float, alpha: float, beta: float,
    year_covariates: dict[int, float], t0: float,
) -> np.ndarray:
    """Cumulative Xi(t) at bin_edges via numerically integrating the
    piecewise-exact xi(t) above using a fine trapezoid grid WITHIN each
    year segment (the segment-level xi(t) itself remains closed-form; the
    within-segment cumulative integral uses a fine deterministic grid
    since Eq(10)'s own closed form assumes a single constant baseline
    across the whole integration range, which no longer holds once the
    baseline is piecewise). This is the one place this module departs
    from a fully closed-form solution, and is flagged explicitly: it
    trades a small, controllable (grid-resolution-bounded) numerical
    error for tractability, rather than a full ODE solver."""
    bin_edges = np.asarray(sorted(bin_edges), dtype=float)
    fine_grid = np.linspace(t0, bin_edges[-1], max(2000, 20 * int(bin_edges[-1] - t0)))
    xi_fine = xi_closed_form_density_baseline(fine_grid, theta0, theta1, alpha, beta, year_covariates, t0)
    Xi_fine = np.concatenate([[0.0], np.cumsum(0.5 * (xi_fine[1:] + xi_fine[:-1]) * np.diff(fine_grid))])
    return np.interp(bin_edges, fine_grid, Xi_fine)


def neg_ic_ll_density_baseline(
    params: np.ndarray, bin_edges: np.ndarray, counts: np.ndarray,
    year_covariates: dict[int, float], t0: float,
) -> float:
    """Eq (18)/Proposition 4 IC-LL, negative, for the density-baseline
    extension. Structurally identical to model3_mbpp_full.neg_ic_ll,
    substituting Xi_closed_form_density_baseline for Xi_closed_form."""
    theta0, theta1, alpha, beta = params
    if alpha < 0 or beta <= 0 or beta <= alpha:
        return 1e10
    Xi_vals = Xi_closed_form_density_baseline(bin_edges, theta0, theta1, alpha, beta, year_covariates, t0)
    bin_Xi = np.diff(Xi_vals)
    bin_Xi = np.clip(bin_Xi, 1e-12, None)
    from scipy.special import gammaln

    ll = np.sum(counts * np.log(bin_Xi) - bin_Xi - gammaln(counts + 1))
    return -ll if math.isfinite(ll) else 1e10


def simulate_m2_candidate(
    theta0: float, theta1: float, alpha: float, beta: float,
    year_covariates: dict[int, float], t0: float, t1: float, rng: np.random.Generator,
) -> np.ndarray:
    """Stage 1 for M2: reuses model3b_cd_simulator.simulate.simulate_m3b_cd
    as-is (per the Simulation Spec's Stage 1 reuse note) -- M2's own
    contribution is Stages 3+ (interval censoring), not the latent
    generator."""
    def x_cd(t: float) -> float:
        return year_covariates.get(int(math.floor(t)), 0.0)

    return simulate_m3b_cd(theta0, theta1, alpha, beta, x_cd, t0, t1, rng)


def run_full_pipeline_m2(
    theta0: float, theta1: float, alpha: float, beta: float,
    year_covariates: dict[int, float], cd_mode: str, precision_mode: str,
    t0: float, t1: float, rng: np.random.Generator,
    *,
    n_episodes: int | None = None, child_rate: float = 1.5, child_cluster_beta: float = 20.0,
    missing_rate: float = 0.0, duplicate_rate: float = 0.0, n_sources: int = 5,
) -> list[CensoredEvent]:
    if n_episodes is not None:
        latent, _episode_ids = generate_episode_structured_latent_events(
            n_episodes, (t0, t1), child_rate, child_cluster_beta, rng
        )
    else:
        latent = simulate_m2_candidate(theta0, theta1, alpha, beta, year_covariates, t0, t1, rng)

    observed = observe_events(latent, year_covariates, cd_mode, "moderate", rng)
    censored = censor_events(observed, precision_mode, rng)
    censored = assign_synthetic_sources(censored, n_sources, rng)
    result = apply_missing_and_duplicate_reporting(censored, missing_rate, duplicate_rate, rng)
    return result.events


def _bin_counts(events: list[CensoredEvent], t0: float, t1: float) -> tuple[np.ndarray, np.ndarray]:
    """Stage 7 for M2: bin_edges at year boundaries, counts by interval
    midpoint's year -- MBPP's interval-censored likelihood consumes bin
    counts directly, never a fabricated point timestamp."""
    bin_edges = np.arange(math.floor(t0), math.ceil(t1) + 1, 1.0)
    mids = np.array([0.5 * (e.t_lower + e.t_upper) for e in events])
    counts, _ = np.histogram(mids, bins=bin_edges)
    return bin_edges, counts


def fit_m2(
    events: list[CensoredEvent], year_covariates: dict[int, float], t0: float, t1: float,
    x0: tuple[float, float, float, float] | None = None,
) -> M2FitResult:
    bin_edges, counts = _bin_counts(events, t0, t1)
    names = ["theta0", "theta1", "alpha", "beta"]
    bounds = [(None, None), (None, None), (0.0, None), (_EPS, None)]
    if x0 is None:
        mean_count = max(np.mean(counts) if counts.size else _EPS, _EPS)
        x0 = (math.log(mean_count), 0.0, 0.1, 1.0)

    def neg_ll(x: np.ndarray) -> float:
        try:
            return neg_ic_ll_density_baseline(x, bin_edges, counts, year_covariates, t0)
        except (ValueError, OverflowError):
            return 1e10

    res = minimize(neg_ll, x0=np.array(x0, dtype=float), method="L-BFGS-B", bounds=bounds)
    return _build_result(names, res, bounds, len(events))


def _build_result(names: list[str], res, bounds: list[tuple], n_events: int) -> M2FitResult:
    params = dict(zip(names, np.atleast_1d(res.x).tolist()))
    fun_finite = math.isfinite(res.fun)
    params_finite = all(math.isfinite(v) for v in params.values())
    status = "optimizer_failed" if not res.success else ("invalid" if not (fun_finite and params_finite) else "ok")
    boundary_flags = {}
    for name, value, (lo, hi) in zip(names, np.atleast_1d(res.x), bounds):
        near_lo = lo is not None and abs(value - lo) <= _BOUNDARY_TOL
        near_hi = hi is not None and math.isfinite(hi) and abs(value - hi) <= _BOUNDARY_TOL
        boundary_flags[name] = bool(near_lo or near_hi)
    return M2FitResult(
        params=params, success=bool(res.success), status=status,
        loglik=float(-res.fun) if fun_finite else float("nan"),
        n_events=n_events, boundary_flags=boundary_flags,
        optimizer_message=str(getattr(res, "message", "")),
    )
