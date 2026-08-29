"""M0 -- Exposure-adjusted count baseline (Poisson / Negative Binomial).

Non-Hawkes floor candidate (Design doc §1). Period-binned (annual) count
model, `log(1+CD_t)` density covariate entering either as a CD-1 rate
predictor or a CD-2 exposure offset. No self-excitation term.

Estimator implemented by hand via scipy.optimize.minimize on the direct
Poisson/NB log-likelihood, matching model3b_cd_simulator/estimate.py's
existing hand-rolled-MLE convention -- NOT via statsmodels, even though
statsmodels happens to already be installed in this environment, to avoid
a stylistic inconsistency with every other estimator in this project (a
deliberate choice, not an oversight: see MODEL_3B_CANDIDATE_IMPLEMENTATION_REVIEW.md's
own note on this exact tradeoff).
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln

sys.path.insert(0, str(Path(__file__).resolve().parent))
from observation_pipeline import (  # noqa: E402
    CensoredEvent,
    apply_missing_and_duplicate_reporting,
    assign_synthetic_sources,
    censor_events,
    generate_episode_structured_latent_events,
    observe_events,
)

_EPS = 1e-6
_BOUNDARY_TOL = 1e-3


@dataclass
class M0FitResult:
    params: dict[str, float]      # {"theta0": ..., "theta1": ..., "dispersion": ... (NB only)}
    success: bool
    status: str                    # "ok" | "optimizer_failed" | "invalid"
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


def simulate_m0(
    theta0: float,
    theta1: float,
    year_covariates: dict[int, float],
    cd_mode: str,
    t0: float,
    t1: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Stage 1 for M0: period-binned (annual) Poisson generative process.

    cd_mode="CD1_no_thinning" (really "CD-1 rate mode" here, reusing the
    pipeline's mode vocabulary): CD density enters the RATE directly,
    log(lambda_year) = theta0 + theta1 * x_CD(year).
    cd_mode="CD2_exposure_thinning": true rate is exp(theta0) constant;
    CD density instead modulates an offset added post-hoc via
    observation_pipeline.observe_events (Stage 2), so this function
    simulates the CONSTANT-rate process and the caller applies Stage 2
    exposure-thinning afterward -- kept as two separate calls (not fused
    here) so M0's CD-1-vs-CD-2 test reuses the exact same Stage-2
    function every other candidate uses, per the Simulation Spec's own
    intent that Stage 2 serve both interpretations by branching
    internally rather than duplicating pipeline logic per candidate.
    """
    events: list[float] = []
    year = int(math.floor(t0))
    while year < t1:
        seg_lo, seg_hi = max(t0, float(year)), min(t1, float(year) + 1.0)
        if seg_hi > seg_lo:
            x = year_covariates.get(year, 0.0)
            if cd_mode == "CD1_no_thinning":
                log_lam = theta0 + theta1 * x
            else:
                log_lam = theta0  # constant true rate; CD-2 exposure applied at Stage 2
            lam = math.exp(log_lam)
            n = rng.poisson(lam * (seg_hi - seg_lo))
            if n > 0:
                events.extend(rng.uniform(seg_lo, seg_hi, size=n).tolist())
        year += 1
    return np.array(sorted(events))


def run_full_pipeline_m0(
    theta0: float,
    theta1: float,
    year_covariates: dict[int, float],
    cd_mode: str,
    precision_mode: str,
    t0: float,
    t1: float,
    rng: np.random.Generator,
    *,
    n_episodes: int | None = None,
    child_rate: float = 1.5,
    child_cluster_beta: float = 20.0,
    missing_rate: float = 0.0,
    duplicate_rate: float = 0.0,
    n_sources: int = 5,
) -> list[CensoredEvent]:
    """Runs Stages 1-6 for M0 and returns the pipeline output (Stage 7
    aggregation happens in fit_m0, not here, matching the Design doc's
    Stage-7 boundary)."""
    if n_episodes is not None:
        latent, _episode_ids = generate_episode_structured_latent_events(
            n_episodes, (t0, t1), child_rate, child_cluster_beta, rng
        )
    else:
        latent = simulate_m0(theta0, theta1, year_covariates, cd_mode, t0, t1, rng)

    observed = observe_events(latent, year_covariates, cd_mode, "moderate", rng)
    censored = censor_events(observed, precision_mode, rng)
    censored = assign_synthetic_sources(censored, n_sources, rng)
    result = apply_missing_and_duplicate_reporting(censored, missing_rate, duplicate_rate, rng)
    return result.events


def _annual_counts(events: list[CensoredEvent], t0: float, t1: float) -> dict[int, int]:
    """Stage 7 for M0: aggregate censored events to annual counts by their
    interval midpoint's year (a year-only-censored event's interval IS
    already exactly one calendar year, so this is exact for the primary
    real-data regime; for finer intervals it assigns by midpoint)."""
    counts: dict[int, int] = {y: 0 for y in range(int(math.floor(t0)), int(math.ceil(t1)))}
    for e in events:
        mid = 0.5 * (e.t_lower + e.t_upper)
        year = int(math.floor(mid))
        if year in counts:
            counts[year] += 1
    return counts


def _neg_loglik_poisson(theta0: float, theta1: float, counts: dict[int, int], year_covariates: dict[int, float]) -> float:
    ll = 0.0
    for year, c in counts.items():
        x = year_covariates.get(year, 0.0)
        log_lam = theta0 + theta1 * x
        lam = math.exp(min(log_lam, 50.0))
        ll += c * log_lam - lam - float(gammaln(c + 1))
    return -ll


def fit_m0_poisson(
    events: list[CensoredEvent],
    year_covariates: dict[int, float],
    t0: float,
    t1: float,
    x0: tuple[float, float] | None = None,
) -> M0FitResult:
    """Stage 8 for M0: Poisson GLM MLE via hand-rolled scipy.optimize."""
    counts = _annual_counts(events, t0, t1)
    names = ["theta0", "theta1"]
    bounds = [(None, None), (None, None)]
    if x0 is None:
        mean_count = max(np.mean(list(counts.values())) if counts else _EPS, _EPS)
        x0 = (math.log(mean_count), 0.0)

    def neg_ll(x: np.ndarray) -> float:
        theta0, theta1 = x
        try:
            return _neg_loglik_poisson(theta0, theta1, counts, year_covariates)
        except (ValueError, OverflowError):
            return math.inf

    res = minimize(neg_ll, x0=np.array(x0, dtype=float), method="L-BFGS-B", bounds=bounds)
    return _build_result(names, res, bounds, len(events))


def _build_result(names: list[str], res, bounds: list[tuple], n_events: int) -> M0FitResult:
    params = dict(zip(names, np.atleast_1d(res.x).tolist()))
    fun_finite = math.isfinite(res.fun)
    params_finite = all(math.isfinite(v) for v in params.values())
    if not res.success:
        status = "optimizer_failed"
    elif not (fun_finite and params_finite):
        status = "invalid"
    else:
        status = "ok"
    boundary_flags = {}
    for name, value, (lo, hi) in zip(names, np.atleast_1d(res.x), bounds):
        near_lo = lo is not None and abs(value - lo) <= _BOUNDARY_TOL
        near_hi = hi is not None and math.isfinite(hi) and abs(value - hi) <= _BOUNDARY_TOL
        boundary_flags[name] = bool(near_lo or near_hi)
    return M0FitResult(
        params=params, success=bool(res.success), status=status,
        loglik=float(-res.fun) if fun_finite else float("nan"),
        n_events=n_events, boundary_flags=boundary_flags,
        optimizer_message=str(getattr(res, "message", "")),
    )
