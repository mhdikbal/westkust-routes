"""M3 -- Bayesian discrete-time Hawkes (period-binned, prior-informed).

No existing project code reuses directly (V1 is frequentist point-
estimate MLE; M3 is a genuinely different model class -- Design doc §1,
Candidate Implementation Review's M3 section). This module implements:

1. A discrete self-exciting count process: an INGARCH-family
   specification where annual count_t ~ Poisson(lambda_t), with
       lambda_t = exp(theta0 + theta1*x_CD(t))
                  + alpha * sum_{s<t} exp(-beta*(t-s)) * count_s
   i.e. past COUNTS (not point events) excite future intensity via the
   same exponential-decay kernel shape as the continuous-time candidates,
   discretized to annual lag. This directly addresses root causes #3/#4/
   #11 by construction: no sub-year timestamp is ever required or
   fabricated.

2. A hand-rolled Bayesian fitting routine (random-walk Metropolis-
   Hastings on an unconstrained reparameterization), because neither
   PyMC nor numpyro is installed in this environment (checked via import
   attempt, not assumed) and the project's own stated convention favors
   hand-rolled scipy/numpy-based methods over adding a new heavyweight
   statistical-library dependency (matching model3b_cd_simulator's own
   scipy.optimize.minimize pattern, extended here to sampling rather than
   optimization). This is a scoped, explicit substitution -- if a future
   turn authorizes installing PyMC/numpyro, this module's `log_posterior`
   function is directly reusable as the target density for either.

Stationarity-safe parameterization (Design doc §5): n = alpha/beta,
constrained 0 <= n < 1, alpha = n*beta. Sampling happens on n directly
(not alpha), exactly as required.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
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

_EPS = 1e-9


@dataclass
class M3PosteriorResult:
    samples: dict[str, np.ndarray]   # {"theta0": array, "theta1": array, "n": array, "beta": array}
    acceptance_rate: float
    n_draws: int
    n_burnin: int
    status: str                       # "ok" | "degenerate" (acceptance_rate near 0 or 1)
    pointwise_loglik: np.ndarray = field(default_factory=lambda: np.empty((0, 0)))  # [n_draws, n_bins], for WAIC/LOO

    def posterior_mean(self) -> dict[str, float]:
        return {k: float(np.mean(v)) for k, v in self.samples.items()}

    def credible_interval(self, name: str, level: float = 0.95) -> tuple[float, float]:
        lo_q, hi_q = (1 - level) / 2, 1 - (1 - level) / 2
        vals = self.samples[name]
        return float(np.quantile(vals, lo_q)), float(np.quantile(vals, hi_q))


def simulate_m3(
    theta0: float, theta1: float, n_branch: float, beta: float,
    year_covariates: dict[int, float], t0: int, t1: int, rng: np.random.Generator,
) -> np.ndarray:
    """Stage 1 for M3: discrete annual counts (not a point-event array --
    M3's own Stage-1 output is already in its native discrete form, per
    the Simulation Spec's note that M0/M3 are 'discrete from the start').
    n_branch = branching ratio (n = alpha/beta); alpha = n_branch*beta
    internally, per the stationarity-safe reparameterization."""
    alpha = n_branch * beta
    years = list(range(t0, t1))
    counts = np.zeros(len(years), dtype=int)
    for i, year in enumerate(years):
        x = year_covariates.get(year, 0.0)
        base = math.exp(theta0 + theta1 * x)
        excite = 0.0
        for j in range(i):
            lag = i - j
            excite += alpha * math.exp(-beta * lag) * counts[j]
        lam = max(base + excite, _EPS)
        counts[i] = rng.poisson(lam)
    return counts


def _lambda_series(theta0: float, theta1: float, n_branch: float, beta: float,
                    counts: np.ndarray, year_covariates_ordered: np.ndarray) -> np.ndarray:
    alpha = n_branch * beta
    n_bins = counts.size
    lam = np.empty(n_bins)
    for i in range(n_bins):
        base = math.exp(theta0 + theta1 * year_covariates_ordered[i])
        if i == 0:
            excite = 0.0
        else:
            lags = np.arange(i, 0, -1)
            excite = alpha * np.sum(np.exp(-beta * lags) * counts[:i])
        lam[i] = max(base + excite, _EPS)
    return lam


def loglik_m3(theta0: float, theta1: float, n_branch: float, beta: float,
              counts: np.ndarray, year_covariates_ordered: np.ndarray) -> float:
    if not (0.0 <= n_branch < 1.0) or beta <= 0:
        return -math.inf
    lam = _lambda_series(theta0, theta1, n_branch, beta, counts, year_covariates_ordered)
    ll = np.sum(counts * np.log(lam) - lam - gammaln(counts + 1))
    return float(ll) if math.isfinite(ll) else -math.inf


def pointwise_loglik_m3(theta0: float, theta1: float, n_branch: float, beta: float,
                          counts: np.ndarray, year_covariates_ordered: np.ndarray) -> np.ndarray:
    """Per-bin log-likelihood contributions, for WAIC/LOO (GATE-*39/53/60
    model-selection analogue, motivated by the audit's independent
    finding that AIC/BIC's failure mode held under both correct
    specification and deliberate kernel misspecification)."""
    lam = _lambda_series(theta0, theta1, n_branch, beta, counts, year_covariates_ordered)
    return counts * np.log(lam) - lam - gammaln(counts + 1)


def log_prior(theta0: float, theta1: float, n_branch: float, beta: float) -> float:
    """Weakly informative priors (Design doc §1 M3 rationale: 'fit with
    weakly informative priors on excitation/branching-ratio parameters',
    motivated by V1's postmortem-documented CI miscalibration 60-84% vs
    92.5-97.5% target for alpha/beta under the Wald/MLE approach)."""
    if not (0.0 <= n_branch < 1.0) or beta <= 0:
        return -math.inf
    lp = 0.0
    lp += -0.5 * (theta0 ** 2) / 4.0            # theta0 ~ N(0, 2^2)
    lp += -0.5 * (theta1 ** 2) / 1.0             # theta1 ~ N(0, 1)
    lp += (2 - 1) * math.log(n_branch + _EPS) + (2 - 1) * math.log(1 - n_branch + _EPS)  # n ~ Beta(2,2)
    lp += (2 - 1) * math.log(beta) - beta        # beta ~ Gamma(2,1)
    return lp


def log_posterior(theta0: float, theta1: float, n_branch: float, beta: float,
                   counts: np.ndarray, year_covariates_ordered: np.ndarray) -> float:
    lp = log_prior(theta0, theta1, n_branch, beta)
    if not math.isfinite(lp):
        return -math.inf
    return lp + loglik_m3(theta0, theta1, n_branch, beta, counts, year_covariates_ordered)


def _to_unconstrained(theta0: float, theta1: float, n_branch: float, beta: float) -> np.ndarray:
    n_clamped = min(max(n_branch, _EPS), 1 - _EPS)
    return np.array([theta0, theta1, math.log(n_clamped / (1 - n_clamped)), math.log(beta)])


def _from_unconstrained(u: np.ndarray) -> tuple[float, float, float, float]:
    theta0, theta1, logit_n, log_beta = u
    n_branch = 1.0 / (1.0 + math.exp(-logit_n))
    beta = math.exp(log_beta)
    return theta0, theta1, n_branch, beta


def fit_m3_mcmc(
    counts: np.ndarray,
    year_covariates_ordered: np.ndarray,
    n_draws: int = 500,
    n_burnin: int = 200,
    step_size: float = 0.15,
    x0: tuple[float, float, float, float] | None = None,
    rng: np.random.Generator | None = None,
) -> M3PosteriorResult:
    """Random-walk Metropolis-Hastings on the unconstrained
    reparameterization (theta0, theta1, logit(n), log(beta)) -- a simple,
    hand-rolled, numpy/scipy-only sampler (see module docstring for why
    PyMC/numpyro are not used). Smoke-test-scale defaults (500 draws, 200
    burn-in); the pre-registered recovery study would use far more draws
    and multiple chains with R-hat convergence diagnostics -- neither is
    implemented here, since running that study is a separate,
    not-yet-authorized step."""
    rng = rng or np.random.default_rng(0)
    if x0 is None:
        mean_count = max(float(np.mean(counts)), _EPS)
        x0 = (math.log(mean_count), 0.0, 0.3, 0.6)
    u = _to_unconstrained(*x0)
    lp_current = log_posterior(*_from_unconstrained(u), counts, year_covariates_ordered)

    n_total = n_burnin + n_draws
    kept = {"theta0": [], "theta1": [], "n": [], "beta": []}
    pointwise = []
    n_accept = 0
    for it in range(n_total):
        proposal = u + rng.normal(0, step_size, size=4)
        theta0_p, theta1_p, n_p, beta_p = _from_unconstrained(proposal)
        lp_proposal = log_posterior(theta0_p, theta1_p, n_p, beta_p, counts, year_covariates_ordered)
        log_accept_ratio = lp_proposal - lp_current
        if math.log(rng.uniform() + _EPS) <= log_accept_ratio:
            u = proposal
            lp_current = lp_proposal
            n_accept += 1
        if it >= n_burnin:
            theta0_c, theta1_c, n_c, beta_c = _from_unconstrained(u)
            kept["theta0"].append(theta0_c)
            kept["theta1"].append(theta1_c)
            kept["n"].append(n_c)
            kept["beta"].append(beta_c)
            pointwise.append(pointwise_loglik_m3(theta0_c, theta1_c, n_c, beta_c, counts, year_covariates_ordered))

    acceptance_rate = n_accept / n_total
    status = "ok" if 0.05 < acceptance_rate < 0.95 else "degenerate"
    samples = {k: np.array(v) for k, v in kept.items()}
    return M3PosteriorResult(
        samples=samples, acceptance_rate=acceptance_rate, n_draws=n_draws, n_burnin=n_burnin,
        status=status, pointwise_loglik=np.array(pointwise),
    )


def waic(pointwise_loglik: np.ndarray) -> float:
    """Watanabe-Akaike Information Criterion from posterior draws of
    per-bin log-likelihood (pointwise_loglik: [n_draws, n_bins]). Lower
    is better, matching the AIC/BIC convention this replaces (GATE-*39/
    53/60's own motivation: AIC/BIC's failure mode was confirmed under
    both correct and deliberately-misspecified kernels in the audit)."""
    lppd = np.sum(np.log(np.mean(np.exp(pointwise_loglik - pointwise_loglik.max(axis=0)), axis=0)) + pointwise_loglik.max(axis=0))
    p_waic = np.sum(np.var(pointwise_loglik, axis=0, ddof=1))
    return float(-2 * (lppd - p_waic))


def run_full_pipeline_m3(
    theta0: float, theta1: float, n_branch: float, beta: float,
    year_covariates: dict[int, float], cd_mode: str, precision_mode: str,
    t0: float, t1: float, rng: np.random.Generator,
    *,
    n_episodes: int | None = None, child_rate: float = 1.5, child_cluster_beta: float = 20.0,
    missing_rate: float = 0.0, duplicate_rate: float = 0.0, n_sources: int = 5,
) -> list[CensoredEvent]:
    """M3's own Stage 1 is already discrete (simulate_m3 above); this
    function instead runs the FULL Stages 2-6 pipeline starting from a
    continuous-time proxy generator (episode-structured, if requested)
    so M3 is exercised under the same observation-regime distortions as
    M0/M2 for factor-grid settings that require it (e.g. episode
    structure, missing/duplicate reporting) -- M3's Stage-7 aggregation
    (in fit terms via _annual_counts_from_censored below) then converts
    back to its native discrete count representation."""
    if n_episodes is not None:
        latent, _episode_ids = generate_episode_structured_latent_events(
            n_episodes, (t0, t1), child_rate, child_cluster_beta, rng
        )
    else:
        # Discrete-native path: simulate_m3 directly produces annual counts,
        # then expand to a synthetic within-year uniform timestamp ONLY for
        # feeding the shared Stages 2/6 (which operate on event times) --
        # this expansion is discarded before Stage 7 (M3 never sees it).
        annual_counts = simulate_m3(theta0, theta1, n_branch, beta, year_covariates, int(t0), int(t1), rng)
        latent = []
        for i, c in enumerate(annual_counts):
            year = int(t0) + i
            latent.extend(rng.uniform(year, year + 1, size=int(c)).tolist())
        latent = np.array(sorted(latent))

    observed = observe_events(latent, year_covariates, cd_mode, "moderate", rng)
    censored = censor_events(observed, precision_mode, rng)
    censored = assign_synthetic_sources(censored, n_sources, rng)
    result = apply_missing_and_duplicate_reporting(censored, missing_rate, duplicate_rate, rng)
    return result.events


def annual_counts_from_censored(events: list[CensoredEvent], t0: float, t1: float) -> tuple[np.ndarray, np.ndarray]:
    """Stage 7 for M3: aggregate to the discrete time grid by interval
    midpoint's year, RETAINING the self-exciting count structure (not
    collapsed to a single GLM count, unlike M0 -- M3's estimator needs
    the ordered count SEQUENCE, not just a total)."""
    years = np.arange(int(math.floor(t0)), int(math.ceil(t1)))
    counts = np.zeros(len(years), dtype=int)
    for e in events:
        mid = 0.5 * (e.t_lower + e.t_upper)
        year = int(math.floor(mid))
        idx = year - years[0]
        if 0 <= idx < len(counts):
            counts[idx] += 1
    return years, counts
