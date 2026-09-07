"""
R1: residual-independence diagnostics on EXISTING fitted replications.
No re-fitting. No new full recovery study. Regenerates only the event
sequence (deterministic, seed-map-based, no hash()) needed to recompute the
time-rescaling residual vector from the ALREADY-STORED fitted parameters,
then computes ACF(z_i), ACF(v_i), and the frozen Ljung-Box statistic at the
frozen lag set L={1,2,5,10}. Residuals are NEVER pooled across replications.
"""
import json
import numpy as np
from scipy.stats import chi2
from v2a_validation_engine import (
    T_HORIZON, design_seed, time_rescaling_residuals, cd_density_at,
)
from v2a_designs import DESIGNS, gen_D10_latent, gen_D10_observed, assign_precision_classes

T = T_HORIZON
LAGS = [1, 2, 5, 10]
MIN_N_FOR_LB = {m: m + 1 for m in LAGS}  # require n > m strictly

def regen_events(design_id, rep):
    rng = np.random.default_rng(design_seed(design_id, rep))
    if design_id == "D10":
        latent = gen_D10_latent(rng)
        classes = assign_precision_classes(latent, rng)
        return gen_D10_observed(latent, classes, rng)
    return DESIGNS[design_id]["generator"](rng)

def acf(x, lag):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n <= lag:
        return np.nan
    xm = x - x.mean()
    num = np.sum(xm[:n-lag] * xm[lag:])
    den = np.sum(xm ** 2)
    if den <= 0:
        return np.nan
    return num / den

def ljung_box_Q(x, m):
    """Q(m) = n(n+2) * sum_{k=1}^m rho_k^2/(n-k). Ljung & Box (1978), Biometrika 65(2):297-303."""
    n = len(x)
    if n <= m:
        return np.nan, np.nan, np.nan
    rhos = [acf(x, k) for k in range(1, m + 1)]
    if any(r is None or (isinstance(r, float) and np.isnan(r)) for r in rhos):
        return np.nan, np.nan, np.nan
    Q = n * (n + 2) * sum((rhos[k-1] ** 2) / (n - k) for k in range(1, m + 1))
    p = 1 - chi2.cdf(Q, df=m)
    return Q, p, rhos

rec = json.load(open("v2a_full_study_recovery_rows.json"))
by = {}
for r in rec:
    by.setdefault((r["design"], r.get("arm", "primary")), []).append(r)

rows_out = []
for (d, arm), rrows in sorted(by.items()):
    N_total = len(rrows)
    n_resid_constructed = 0
    n_nonfinite = 0
    short_excl = {m: 0 for m in LAGS}
    n_tests = {m: 0 for m in LAGS}
    n_reject = {m: 0 for m in LAGS}
    for row in rrows:
        rep = row["rep"]
        if str(row["converged"]) != "True":
            continue  # no fitted params to build residuals from
        events = regen_events(d, rep)
        if len(events) != row["n_events"]:
            raise RuntimeError(f"cross-process mismatch {d} {arm} rep {rep}")
        params = (row["mu_hat"], row["alpha_hat"], row["beta_hat"])
        if d == "D9":
            mu_of_t = (lambda t: cd_density_at(np.atleast_1d(t))) if arm == "correct_cd_modulated" else None
        else:
            mu_of_t = None
        v = time_rescaling_residuals(params, events, T, mu_of_t=mu_of_t)
        if len(v) == 0:
            continue
        n_resid_constructed += 1
        z = -np.log(np.clip(1 - v, 1e-300, 1.0))
        finite = np.isfinite(v).all() and np.isfinite(z).all()
        if not finite:
            n_nonfinite += 1
            continue
        n = len(v)
        for m in LAGS:
            if n <= m:
                short_excl[m] += 1
                continue
            Qv, pv, _ = ljung_box_Q(v, m)
            Qz, pz, _ = ljung_box_Q(z, m)
            if np.isnan(pv) or np.isnan(pz):
                short_excl[m] += 1
                continue
            n_tests[m] += 1
            # descriptive rejection counted on v_i series (the stored/primary residual)
            if pv < 0.05:
                n_reject[m] += 1
            acf_v = {k: acf(v, k) for k in LAGS if k <= n - 1}
            acf_z = {k: acf(z, k) for k in LAGS if k <= n - 1}
            rows_out.append({
                "design": d, "arm": arm, "rep": rep, "n_events": n, "lag_set_m": m,
                "Q_v": Qv, "p_v": pv, "Q_z": Qz, "p_z": pz,
                "acf_v_lag": acf_v.get(m), "acf_z_lag": acf_z.get(m),
                "reject_0.05_v": bool(pv < 0.05), "reject_0.05_z": bool(pz < 0.05),
            })
    for m in LAGS:
        print(f"{d}/{arm} m={m}: N_total={N_total} N_resid_constructed={n_resid_constructed} "
              f"N_nonfinite_excluded={n_nonfinite} N_short_excluded={short_excl[m]} "
              f"N_tests={n_tests[m]} N_reject={n_reject[m]} "
              f"R_hat={n_reject[m]/n_tests[m] if n_tests[m] else float('nan'):.4f}")

import csv
with open("HAWKES_BASELINE_V2A_RESIDUAL_INDEPENDENCE_RESULTS.csv", "w", newline="") as f:
    fieldnames = ["design","arm","rep","n_events","lag_set_m","Q_v","p_v","Q_z","p_z",
                  "acf_v_lag","acf_z_lag","reject_0.05_v","reject_0.05_z"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in rows_out:
        w.writerow(r)
print("\nwrote", len(rows_out), "rows to HAWKES_BASELINE_V2A_RESIDUAL_INDEPENDENCE_RESULTS.csv")
