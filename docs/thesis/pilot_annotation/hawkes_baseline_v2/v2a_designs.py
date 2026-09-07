"""
V2-A design generators D1-D10 and per-replication evaluation.
Synthetic data only. See HAWKES_BASELINE_V2A_DESIGN_REGISTRY.csv for the
frozen specification each function implements.
"""
import numpy as np
from v2a_validation_engine import (
    T_HORIZON, T0, CD_YEARS, CD_DENSITY, cd_density_at,
    simulate_exp_hawkes, simulate_poisson,
    fit_hawkes, fit_homogeneous_poisson, fit_inhomogeneous_poisson_cd,
    aic, bic, assign_precision_classes, impute_d10, impute_d4,
    time_rescaling_residuals, ks_uniform_pvalue,
)

T = T_HORIZON

# ---- calibration constants (frozen at checkpoint 3, from real-data statics) ----
MU0_D1 = 86.0 / T                      # 0.46739
MU_LATENT_D5 = 86.0 / 35.62779922779922  # 2.41385, from integral of p_obs
MU_PARENT_D6 = 86.0 / (T * 3.0)         # 0.155797, c=2, parents+offspring both observed
C_D6 = 2

def _density_normalized():
    # mean-1-normalized CD density already computed as CD_DENSITY in engine
    return CD_DENSITY

def cd_density_norm_at(t):
    return cd_density_at(t)  # already mean-1-normalized in load_cd_exposure()

def p_obs_at(t):
    """Detection probability for D5: density / max(density over 1600-1784)."""
    year = np.clip(np.floor(T0 + np.atleast_1d(t)).astype(int), CD_YEARS.min(), CD_YEARS.max())
    idx = year - int(CD_YEARS.min())
    raw = CD_DENSITY[idx] * CD_DENSITY.mean()  # undo mean-normalization -> raw counts proxy
    return np.clip(raw / raw.max(), 0.0, 1.0)

# ---------------------------------------------------------------------------
# D1: homogeneous Poisson, eta N/A (true generator has no excitation)
# ---------------------------------------------------------------------------
def gen_D1(rng):
    mu_fn = lambda t: np.full_like(np.atleast_1d(t), MU0_D1, dtype=float)
    return simulate_poisson(mu_fn, T, rng, mu_bar=MU0_D1 * 1.05)

# ---------------------------------------------------------------------------
# D2: inhomogeneous Poisson (smooth sinusoidal baseline)
# ---------------------------------------------------------------------------
def gen_D2(rng):
    mu_fn = lambda t: MU0_D1 * (1 + 0.5 * np.sin(2 * np.pi * np.atleast_1d(t) / T))
    return simulate_poisson(mu_fn, T, rng, mu_bar=MU0_D1 * 1.6)

# ---------------------------------------------------------------------------
# D3: exposure-varying non-Hawkes (real CD density as covariate)
# ---------------------------------------------------------------------------
B0_D3, B1_D3 = 0.2, 0.3
def gen_D3(rng):
    mu_fn = lambda t: B0_D3 + B1_D3 * cd_density_norm_at(np.atleast_1d(t))
    return simulate_poisson(mu_fn, T, rng, mu_bar=B0_D3 + B1_D3 * CD_DENSITY.max() * 1.1)

# ---------------------------------------------------------------------------
# D4: NAIVE_POINT_SUBSTITUTION_STRESS_TEST (latent homogeneous Poisson)
# ---------------------------------------------------------------------------
def gen_D4(rng):
    latent = gen_D1(rng)
    classes = assign_precision_classes(latent, rng)
    observed = impute_d4(latent, classes)
    return observed

# ---------------------------------------------------------------------------
# D5: density-thinning non-Hawkes (replaces degenerate volume-mask design)
# ---------------------------------------------------------------------------
def gen_D5(rng):
    mu_fn = lambda t: np.full_like(np.atleast_1d(t), MU_LATENT_D5, dtype=float)
    latent = simulate_poisson(mu_fn, T, rng, mu_bar=MU_LATENT_D5 * 1.05)
    if len(latent) == 0:
        return latent
    p = p_obs_at(latent)
    keep = rng.uniform(0, 1, len(latent)) <= p
    return latent[keep]

# ---------------------------------------------------------------------------
# D6: Neyman-Scott temporal cluster process (parents+offspring both observed)
# ---------------------------------------------------------------------------
def gen_D6(rng):
    mu_fn = lambda t: np.full_like(np.atleast_1d(t), MU_PARENT_D6, dtype=float)
    parents = simulate_poisson(mu_fn, T, rng, mu_bar=MU_PARENT_D6 * 1.05)
    all_events = list(parents)
    for p in parents:
        n_off = rng.poisson(C_D6)
        disp = rng.uniform(-0.5, 0.5, n_off)
        off = p + disp
        off = off[(off >= 0) & (off <= T)]
        all_events.extend(off.tolist())
    return np.sort(np.array(all_events))

# ---------------------------------------------------------------------------
# D7: subcritical Hawkes, low eta=0.2
# ---------------------------------------------------------------------------
BETA_D7 = 0.6
ETA_D7 = 0.2
ALPHA_D7 = ETA_D7 * BETA_D7
MU_D7 = (86.0 / T) * (1 - ETA_D7)  # long-run intensity F-07: lambda_bar=mu/(1-eta) -> mu=lambda_bar*(1-eta)

def gen_D7(rng):
    mu_fn = lambda t: np.full_like(np.atleast_1d(t), MU_D7, dtype=float)
    return simulate_exp_hawkes(mu_fn, ALPHA_D7, BETA_D7, T, rng)

# ---------------------------------------------------------------------------
# D8: subcritical Hawkes near published eta (mu_hat=0.2573, alpha_hat=0.4207, beta_hat=0.6215)
# ---------------------------------------------------------------------------
MU_D8, ALPHA_D8, BETA_D8 = 0.2573, 0.4207, 0.6215
ETA_D8 = ALPHA_D8 / BETA_D8

def gen_D8(rng):
    mu_fn = lambda t: np.full_like(np.atleast_1d(t), MU_D8, dtype=float)
    return simulate_exp_hawkes(mu_fn, ALPHA_D8, BETA_D8, T, rng)

# ---------------------------------------------------------------------------
# D9: Hawkes with nonstationary (CD-density-modulated) baseline, eta=0.4
# ---------------------------------------------------------------------------
BETA_D9 = 0.6
ETA_D9 = 0.4
ALPHA_D9 = ETA_D9 * BETA_D9
MU0_D9 = (86.0 / T) * (1 - ETA_D9)  # calibrated so time-average baseline matches D1-style target

def gen_D9(rng):
    mu_fn = lambda t: MU0_D9 * cd_density_norm_at(np.atleast_1d(t))  # mean-1-normalized -> preserves calibration
    return simulate_exp_hawkes(mu_fn, ALPHA_D9, BETA_D9, T, rng, mu_bar=MU0_D9 * CD_DENSITY.max() * 1.1 + ALPHA_D9 * 5)

# ---------------------------------------------------------------------------
# D10: SINGLE_IMPUTATION_INTERVAL_UNCERTAINTY_STRESS_TEST (same params as D8)
# ---------------------------------------------------------------------------
def gen_D10_latent(rng):
    mu_fn = lambda t: np.full_like(np.atleast_1d(t), MU_D8, dtype=float)
    return simulate_exp_hawkes(mu_fn, ALPHA_D8, BETA_D8, T, rng)

def gen_D10_observed(latent, classes, rng):
    """DEFECT FIX (checkpoint-5 reconciliation): must reuse the SAME classes
    draw the caller used to compute n_interval_observed. The previous version
    re-drew classes internally from the same rng stream, so n_interval_observed
    and n_estimator_input were computed from two different random 'unresolved'
    assignments, breaking the invariant N_estimator_input <= N_interval_observed
    <= N_latent (verified violation rate 132/278 replications pre-fix)."""
    return impute_d10(latent, classes, rng)

DESIGNS = {
    "D1": {"generator": gen_D1, "true": {"mu": MU0_D1, "alpha": 0.0, "beta": np.nan, "eta": 0.0}, "family": "FPR"},
    "D2": {"generator": gen_D2, "true": {"mu": MU0_D1, "alpha": 0.0, "beta": np.nan, "eta": 0.0}, "family": "FPR"},
    "D3": {"generator": gen_D3, "true": {"mu": np.nan, "alpha": 0.0, "beta": np.nan, "eta": 0.0}, "family": "FPR"},
    "D4": {"generator": gen_D4, "true": {"mu": MU0_D1, "alpha": 0.0, "beta": np.nan, "eta": 0.0}, "family": "PR_NAIVE_SUBSTITUTION"},
    "D5": {"generator": gen_D5, "true": {"mu": MU_LATENT_D5, "alpha": 0.0, "beta": np.nan, "eta": 0.0}, "family": "FPR_DUAL"},
    "D6": {"generator": gen_D6, "true": {"mu": MU_PARENT_D6, "alpha": np.nan, "beta": np.nan, "eta": np.nan}, "family": "PR_NEYMAN_SCOTT"},
    "D7": {"generator": gen_D7, "true": {"mu": MU_D7, "alpha": ALPHA_D7, "beta": BETA_D7, "eta": ETA_D7}, "family": "RECOVERY"},
    "D8": {"generator": gen_D8, "true": {"mu": MU_D8, "alpha": ALPHA_D8, "beta": BETA_D8, "eta": ETA_D8}, "family": "RECOVERY"},
    "D9": {"generator": gen_D9, "true": {"mu": MU0_D9, "alpha": ALPHA_D9, "beta": BETA_D9, "eta": ETA_D9}, "family": "RECOVERY"},
    "D10": {"generator": None, "true": {"mu": MU_D8, "alpha": ALPHA_D8, "beta": BETA_D8, "eta": ETA_D8}, "family": "RECOVERY_INTERVAL"},
}
