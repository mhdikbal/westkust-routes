"""
HAWKES BASELINE V2-A -- VALIDATION-ONLY SYNTHETIC ENGINE
==========================================================
Structurally distinct from Phase D (model3_hawkes_kaskade_event.py), per the
approved HAWKES_BASELINE_V2_RECOVERY_DISTINCTION_MATRIX.csv:
  - estimand is parameter-level bias/RMSE/coverage, not model-selection accuracy
  - direct thinning simulation at the M2 exponential-kernel level (no multi-family simulator)
  - per-precision-class date perturbation (not uniform jitter_ties)
  - exposure covariate arm using real CD document-density series
  - comparator selection via MODEL_COMPARISON_WITHOUT_ASYMPTOTIC_P_VALUE (no LR p-value)

Uses SYNTHETIC data only. Never reads, fits, or interprets the 86-event
historical primary analysis set or any historical corpus content.

No Phase D code, simulator, or result is imported, reused, or modified.
"""
import numpy as np
from scipy.optimize import minimize
from scipy.stats import kstest, norm
import csv
import time
import json

RNG_SEED_BASE = 20260906  # fixed, documented seed base for reproducibility

# DEFECT FIX (checkpoint-5 reconciliation): the seed formula previously used
# hash(design_id) % 100000, but Python randomizes str hash() per process by
# default (no PYTHONHASHSEED pinned), so a later process (e.g. the coverage
# addon) regenerates DIFFERENT synthetic events than the ones actually fit in
# the original run_family_recovery process. Fixed, order-independent integer
# offsets replace hash() so every process derives the identical rng stream.
DESIGN_SEED_OFFSET = {
    "D1": 1, "D2": 2, "D3": 3, "D4": 4, "D5": 5,
    "D6": 6, "D7": 7, "D8": 8, "D9": 9, "D10": 10,
}

def design_seed(design_id, rep):
    return RNG_SEED_BASE * 100000 + DESIGN_SEED_OFFSET[design_id] * 1000 + rep

# ---------------------------------------------------------------------------
# Real CD exposure covariate (read-only; used as a design input, not fitted)
# ---------------------------------------------------------------------------
def load_cd_exposure(path="/home/naro/westkust-routes/docs/thesis/colab/CD_ANNUAL_DOCUMENT_DENSITY_WORKING.csv"):
    years, counts = [], []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                years.append(int(row["year"]))
                counts.append(float(row["cd_documents_all_accepted"]))
            except (ValueError, KeyError):
                continue
    years = np.array(years)
    counts = np.array(counts)
    # normalize to [0,1] density multiplier around mean 1.0 (design covariate, not a fitted model)
    dens = counts / counts.mean()
    return years, dens

CD_YEARS, CD_DENSITY = load_cd_exposure()
T_HORIZON = 184.0  # years, matches CD observed range 1600-1784 (exposure contract EXP-CD)
T0 = 1600.0

def cd_density_at(t):
    """Piecewise-constant density lookup for absolute year t0+t."""
    year = np.clip(np.floor(T0 + t).astype(int), CD_YEARS.min(), CD_YEARS.max())
    idx = year - int(CD_YEARS.min())
    return CD_DENSITY[idx]

# ---------------------------------------------------------------------------
# Simulators (Ogata thinning for Hawkes; direct sampling for Poisson)
# ---------------------------------------------------------------------------
def simulate_exp_hawkes(mu_fn, alpha, beta, T, rng, mu_bar=None):
    """Ogata's modified thinning algorithm for exponential-kernel Hawkes.
    mu_fn: callable t -> baseline intensity (allows nonstationary baseline).
    Uses a global supremum of mu_fn as a conservative constant upper-bound
    component (always valid for thinning, if slightly less efficient).
    """
    if mu_bar is None:
        ts = np.linspace(0, T, 2000)
        mu_bar = max(mu_fn(ts).max(), 1e-6)
    t = 0.0
    events = []
    S = 0.0  # excitation sum evaluated exactly at time t (post-decay, pre-jump)
    while t < T:
        M = mu_bar + S  # valid upper bound: mu_fn<=mu_bar always, excitation only decays until next jump
        if M <= 0:
            M = 1e-6
        w = rng.exponential(1.0 / M)
        t_candidate = t + w
        if t_candidate > T:
            break
        S_decayed = S * np.exp(-beta * w)
        lam_candidate = mu_fn(np.array([t_candidate]))[0] + S_decayed
        u = rng.uniform(0.0, 1.0)
        if u <= lam_candidate / M:
            events.append(t_candidate)
            S = S_decayed + alpha
        else:
            S = S_decayed
        t = t_candidate
    return np.array(events)

def simulate_poisson(mu_fn, T, rng, mu_bar=None):
    if mu_bar is None:
        ts = np.linspace(0, T, 2000)
        mu_bar = max(mu_fn(ts).max() * 1.2, 1e-6)
    n_upper = rng.poisson(mu_bar * T)
    cand = np.sort(rng.uniform(0, T, n_upper))
    keep = rng.uniform(0, 1, n_upper) <= mu_fn(cand) / mu_bar
    return cand[keep]

# ---------------------------------------------------------------------------
# Exponential-Hawkes exact log-likelihood (F-02) and MLE (recursive O(n))
# ---------------------------------------------------------------------------
def hawkes_negloglik(params, t_events, T, mu_shape=None):
    """mu_shape: optional callable s(t) (design covariate, e.g. normalized CD
    density) such that the baseline is mu*s(t). mu itself remains the free,
    estimated parameter in all cases -- s(t) only supplies the SHAPE, never
    replaces mu (fixed: an earlier version let mu_of_t ignore mu entirely,
    making mu unidentified for nonstationary-baseline designs)."""
    mu, alpha, beta = params
    if mu <= 0 or alpha < 0 or beta <= 0 or alpha >= beta:  # enforce subcriticality-friendly domain
        return 1e10
    n = len(t_events)
    baseline = (lambda t: np.full_like(np.atleast_1d(t), mu, dtype=float)) if mu_shape is None else (lambda t: mu * mu_shape(np.atleast_1d(t)))
    if n == 0:
        grid = np.linspace(0, T, 500)
        return np.trapezoid(baseline(grid), grid)
    A = 0.0  # recursive excitation sum
    loglik = 0.0
    prev_t = 0.0
    for i, ti in enumerate(t_events):
        A *= np.exp(-beta * (ti - prev_t))
        lam_i = baseline(np.array([ti]))[0] + alpha * A
        if lam_i <= 0:
            return 1e10
        loglik += np.log(lam_i)
        A += 1.0
        prev_t = ti
    grid = np.linspace(0, T, 500)
    int_mu = np.trapezoid(baseline(grid), grid)
    # compensator integral of excitation term: sum alpha/beta * (1-exp(-beta*(T-ti)))
    int_exc = np.sum((alpha / beta) * (1 - np.exp(-beta * (T - t_events))))
    loglik -= (int_mu + int_exc)
    return -loglik

def fit_hawkes(t_events, T, mu_of_t=None, x0=(0.3, 0.3, 0.6)):
    res = minimize(hawkes_negloglik, x0=np.array(x0), args=(t_events, T, mu_of_t),
                    method="Nelder-Mead",
                    options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 2000})
    return res

def hawkes_hessian_se(params, t_events, T, mu_of_t=None, eps=1e-4):
    """Finite-difference Hessian of negloglik at MLE -> asymptotic SE."""
    k = len(params)
    H = np.zeros((k, k))
    f0 = hawkes_negloglik(params, t_events, T, mu_of_t)
    for i in range(k):
        for j in range(k):
            pi = np.array(params, dtype=float)
            pj = np.array(params, dtype=float)
            pij = np.array(params, dtype=float)
            pi[i] += eps
            pj[j] += eps
            pij[i] += eps
            pij[j] += eps
            fi = hawkes_negloglik(pi, t_events, T, mu_of_t)
            fj = hawkes_negloglik(pj, t_events, T, mu_of_t)
            fij = hawkes_negloglik(pij, t_events, T, mu_of_t)
            H[i, j] = (fij - fi - fj + f0) / (eps * eps)
    try:
        cov = np.linalg.inv(H)
        se = np.sqrt(np.diag(np.abs(cov)))
    except np.linalg.LinAlgError:
        se = np.array([np.nan] * k)
    return se

# ---------------------------------------------------------------------------
# Poisson comparators (closed-form / simple numerical MLE)
# ---------------------------------------------------------------------------
def fit_homogeneous_poisson(t_events, T):
    n = len(t_events)
    mu_hat = n / T
    loglik = n * np.log(mu_hat) - mu_hat * T if mu_hat > 0 else -1e10
    return mu_hat, loglik

def fit_inhomogeneous_poisson_cd(t_events, T):
    """lambda(t) = b0 + b1*cd_density(t), fit by MLE (b0,b1>=0)."""
    def negloglik(params):
        b0, b1 = params
        if b0 < 0 or b1 < 0:
            return 1e10
        grid = np.linspace(0, T, 500)
        lam_grid = b0 + b1 * cd_density_at(grid)
        integral = np.trapezoid(lam_grid, grid)
        if len(t_events) == 0:
            return integral
        lam_events = b0 + b1 * cd_density_at(t_events)
        if np.any(lam_events <= 0):
            return 1e10
        return integral - np.sum(np.log(lam_events))
    res = minimize(negloglik, x0=[0.3, 0.1], method="Nelder-Mead",
                    options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 1000})
    b0, b1 = res.x
    return (b0, b1), -res.fun

# ---------------------------------------------------------------------------
# AIC / BIC (F-09 / F-10)
# ---------------------------------------------------------------------------
def aic(loglik, k):
    return 2 * k - 2 * loglik

def bic(loglik, k, n):
    return k * np.log(max(n, 1)) - 2 * loglik

# ---------------------------------------------------------------------------
# Date coarsening (D_T mechanism): class probabilities ONLY (not per-class
# semantics) drawn from the real 141-event precision distribution.
# ---------------------------------------------------------------------------
PRECISION_PROPORTIONS = {
    "exact_day": 72/141, "range": 21/141, "year": 16/141,
    "month": 10/141, "unresolved": 22/141,
}

def assign_precision_classes(t_events, rng):
    return rng.choice(list(PRECISION_PROPORTIONS.keys()), size=len(t_events),
                       p=list(PRECISION_PROPORTIONS.values()))

def generate_bounds(t_events, classes):
    """Stage-3 (D10/D4 shared): calendar-aligned [L_i,U_i] synthetic generated
    bounds -- NOT 'recorded bounds'. Absolute year alignment uses T0=1600."""
    L = np.array(t_events, dtype=float)
    U = np.array(t_events, dtype=float)
    for i, c in enumerate(classes):
        ti = t_events[i]
        if c == "exact_day":
            L[i], U[i] = ti, ti
        elif c == "month":
            m0 = np.floor((T0 + ti) * 12) / 12 - T0
            L[i], U[i] = m0, m0 + 1/12
        elif c == "range":
            m0 = np.floor((T0 + ti) * 12) / 12 - T0
            L[i], U[i] = m0 - 0.25, m0 + 1/12 + 0.25
        elif c == "year":
            y0 = np.floor(T0 + ti) - T0
            L[i], U[i] = y0, y0 + 1.0
        else:  # unresolved
            L[i], U[i] = np.nan, np.nan
    return L, U

def impute_d10(t_events, classes, rng):
    """Stage-4/5 for D10: single random-within-bounds imputation; unresolved dropped."""
    L, U = generate_bounds(t_events, classes)
    observed = np.array(t_events, dtype=float)
    needs_draw = (classes != "exact_day") & (classes != "unresolved")
    if needs_draw.any():
        observed[needs_draw] = rng.uniform(L[needs_draw], U[needs_draw])
    keep = ~np.isnan(L)
    return np.sort(observed[keep])

def impute_d4(t_events, classes):
    """Stage-4' for D4: deterministic point substitution (naive malpractice stress test)."""
    L, U = generate_bounds(t_events, classes)
    observed = np.array(t_events, dtype=float)
    for i, c in enumerate(classes):
        if c == "exact_day":
            observed[i] = t_events[i]
        elif c in ("month", "year"):
            observed[i] = L[i]
        elif c == "range":
            observed[i] = (L[i] + U[i]) / 2.0
        else:
            observed[i] = np.nan
    keep = ~np.isnan(observed)
    return np.sort(observed[keep])

# ---------------------------------------------------------------------------
# Time-rescaling residual diagnostics (F-08, now resolved)
# ---------------------------------------------------------------------------
def time_rescaling_residuals(params, t_events, T, mu_of_t=None):
    mu, alpha, beta = params
    n = len(t_events)
    if n == 0:
        return np.array([])
    A = 0.0
    prev_t = 0.0
    L_vals = []
    L_cum = 0.0
    for ti in t_events:
        # integral of mu*shape(t) term over (prev_t, ti] -- mu is always the free parameter
        if mu_of_t is None:
            int_mu = mu * (ti - prev_t)
        else:
            grid = np.linspace(prev_t, ti, 20)
            int_mu = mu * np.trapezoid(mu_of_t(grid), grid) if len(grid) > 1 else 0.0
        int_exc = (alpha / beta) * A * (1 - np.exp(-beta * (ti - prev_t)))
        L_cum += int_mu + int_exc
        L_vals.append(L_cum)
        A = A * np.exp(-beta * (ti - prev_t)) + 1.0
        prev_t = ti
        L_cum = 0.0
        # reset cumulative tracker since we recompute increments below
    z = np.array(L_vals)  # z_i = L(u_i)-L(u_{i-1}) increments, already per-interval (eq. 2.16, Brown et al. 2002)
    z = np.clip(z, 1e-12, None)
    v = 1 - np.exp(-z)  # v_i uniform residual (project notation, eq. 2.17 analogue)
    return v

def ks_uniform_pvalue(v):
    if len(v) < 3:
        return np.nan
    stat, p = kstest(v, "uniform")
    return p
