"""
Targeted cross-process reproducibility check (verification only, NOT counted
toward the 2,495 bootstrap rows). Designated sentinel seed = 999999999.
Designated parent arm = D8/primary, parent_rep=0 (the arm already used for
the earlier generator-only sentinel check).

Prespecified numerical tolerance (declared BEFORE running, not chosen after
seeing results): absolute tolerance 1e-9 for fitted parameters, eta, and the
KS diagnostic statistic; exact byte-hash equality required for the event
array, code hashes, and seed-map hash (these are deterministic integer/RNG
outputs with no floating-point accumulation-order sensitivity across
processes, since the same numpy PCG64 generator with the same seed produces
bit-identical draws in any process on the same numpy build).
"""
import json, hashlib
import numpy as np
from v2a_validation_engine import (
    T_HORIZON, DESIGN_SEED_OFFSET, design_seed, time_rescaling_residuals, fit_hawkes,
)
from v2a_designs import DESIGNS
from scipy.stats import kstest

T = T_HORIZON
SENTINEL_SEED = 999999999
DESIGN_ID, ARM = "D8", "primary"
ABS_TOL = 1e-9

def h(x):
    return hashlib.md5(x).hexdigest()

def arr_hash(a):
    return h(np.asarray(a, dtype=float).tobytes())

rec = json.load(open("v2a_full_study_recovery_rows.json"))
parent_row = next(r for r in rec if r["design"] == DESIGN_ID and r.get("arm","primary") == ARM and r["rep"] == 0)
params = (parent_row["mu_hat"], parent_row["alpha_hat"], parent_row["beta_hat"])

def full_pipeline(seed, params, design_id="D8"):
    from v2a_validation_engine import simulate_exp_hawkes
    mu_hat, alpha_hat, beta_hat = params
    rng = np.random.default_rng(seed)
    mu_fn = lambda t: np.full_like(np.atleast_1d(t), mu_hat, dtype=float)
    X = simulate_exp_hawkes(mu_fn, alpha_hat, beta_hat, T, rng)
    res = fit_hawkes(X, T, mu_of_t=None)
    v = time_rescaling_residuals(res.x, X, T, mu_of_t=None)
    D = kstest(v, "uniform").statistic
    out = {
        "n_events": len(X),
        "event_hash": arr_hash(X),
        "mu": float(res.x[0]), "alpha": float(res.x[1]), "beta": float(res.x[2]),
        "eta": float(res.x[1]/res.x[2]),
        "residual_hash": arr_hash(v),
        "D_stat": float(D),
        "output_hash": h(f"{res.x.tolist()}|{D}".encode()),
    }
    return out

out_inprocess = full_pipeline(SENTINEL_SEED, params, DESIGN_ID)
json.dump(out_inprocess, open("/tmp/_xcheck_inprocess.json","w"))
print("IN-PROCESS:", out_inprocess)
