"""
R2: bootstrap calibration of the marginal residual statistic, restricted to
the approved finite submanifest (5 arms x 1 prespecified parent replication
x B=499 bootstrap refits = 2495 total). Frozen algorithm per the approved
manifest/contract. hash() is never used for seeding.
"""
import json, hashlib
import numpy as np
from scipy.stats import kstest
from v2a_validation_engine import (
    T_HORIZON, DESIGN_SEED_OFFSET, design_seed, time_rescaling_residuals,
    cd_density_at, fit_hawkes,
)
from v2a_designs import DESIGNS, gen_D10_latent, gen_D10_observed, assign_precision_classes
from v2a_validation_engine import simulate_exp_hawkes

T = T_HORIZON
B_BOOT = 499
PARENT_REP = 0
SEED_DERIVATION_VERSION = "bootstrap_seed_v1"
ENGINE_HASH = hashlib.md5(open("v2a_validation_engine.py","rb").read()).hexdigest()
DESIGNS_HASH = hashlib.md5(open("v2a_designs.py","rb").read()).hexdigest()

ARM_OFFSET = {"primary": 0, "correct_cd_modulated": 1, "misspecified_constant_mu": 2}

ARMS = [
    ("D7", "primary"),
    ("D8", "primary"),
    ("D9", "correct_cd_modulated"),
    ("D9", "misspecified_constant_mu"),
    ("D10", "primary"),
]

def bootstrap_seed(design_id, arm, parent_rep, b):
    return design_seed(design_id, parent_rep) * 10000 + ARM_OFFSET[arm] * 1000 + b

def h(x):
    return hashlib.md5(x).hexdigest()

def arr_hash(a):
    return h(np.asarray(a, dtype=float).tobytes())

def regen_parent_events(design_id, rep):
    rng = np.random.default_rng(design_seed(design_id, rep))
    if design_id == "D10":
        latent = gen_D10_latent(rng)
        classes = assign_precision_classes(latent, rng)
        return gen_D10_observed(latent, classes, rng)
    return DESIGNS[design_id]["generator"](rng)

def mu_of_t_for(design_id, arm):
    if design_id == "D9" and arm == "correct_cd_modulated":
        return lambda t: cd_density_at(np.atleast_1d(t))
    return None

def simulate_bootstrap(design_id, arm, params, rng):
    mu_hat, alpha_hat, beta_hat = params
    if design_id == "D9" and arm == "correct_cd_modulated":
        mu_fn = lambda t: mu_hat * cd_density_at(np.atleast_1d(t))
        return simulate_exp_hawkes(mu_fn, alpha_hat, beta_hat, T, rng)
    mu_fn = lambda t: np.full_like(np.atleast_1d(t), mu_hat, dtype=float)
    latent = simulate_exp_hawkes(mu_fn, alpha_hat, beta_hat, T, rng)
    if design_id == "D10":
        classes = assign_precision_classes(latent, rng)
        return gen_D10_observed(latent, classes, rng)
    return latent

rec = json.load(open("v2a_full_study_recovery_rows.json"))
by = {}
for r in rec:
    by.setdefault((r["design"], r.get("arm", "primary")), []).append(r)

arm_summaries = []
row_records = []

for design_id, arm in ARMS:
    parent_row = next(r for r in by[(design_id, arm)] if r["rep"] == PARENT_REP)
    params = (parent_row["mu_hat"], parent_row["alpha_hat"], parent_row["beta_hat"])
    mu_of_t = mu_of_t_for(design_id, arm)

    parent_events = regen_parent_events(design_id, PARENT_REP)
    cross_process_ok = (len(parent_events) == parent_row["n_events"])
    parent_input_hash = arr_hash(parent_events)

    v_obs = time_rescaling_residuals(params, parent_events, T, mu_of_t=mu_of_t)
    D_obs = kstest(v_obs, "uniform").statistic if len(v_obs) >= 3 else np.nan

    N_requested = B_BOOT
    N_simulated = 0
    N_simulation_failed = 0
    N_refit_attempted = 0
    N_refit_converged = 0
    N_refit_failed = 0
    N_finite_residual_vector = 0
    N_nonfinite_residual_vector = 0
    N_finite_statistic = 0
    N_nonfinite_statistic = 0
    D_boot_finite = []

    for j in range(B_BOOT):
        seed = bootstrap_seed(design_id, arm, PARENT_REP, j)
        rng = np.random.default_rng(seed)
        try:
            X_boot = simulate_bootstrap(design_id, arm, params, rng)
            N_simulated += 1
        except Exception:
            N_simulation_failed += 1
            row_records.append(dict(design=design_id, arm=arm, parent_rep=PARENT_REP, b=j,
                seed_integer=seed, seed_derivation_version=SEED_DERIVATION_VERSION,
                engine_hash=ENGINE_HASH, parent_input_hash=parent_input_hash,
                bootstrap_input_hash=None, bootstrap_output_hash=None,
                n_boot_events=None, refit_converged=None, D_boot=None, status="SIMULATION_FAILED"))
            continue
        bootstrap_input_hash = arr_hash(X_boot)
        N_refit_attempted += 1
        res_boot = fit_hawkes(X_boot, T, mu_of_t=mu_of_t)
        ok = bool(res_boot.success) and len(X_boot) > 3
        if not ok:
            N_refit_failed += 1
            row_records.append(dict(design=design_id, arm=arm, parent_rep=PARENT_REP, b=j,
                seed_integer=seed, seed_derivation_version=SEED_DERIVATION_VERSION,
                engine_hash=ENGINE_HASH, parent_input_hash=parent_input_hash,
                bootstrap_input_hash=bootstrap_input_hash, bootstrap_output_hash=None,
                n_boot_events=len(X_boot), refit_converged=False, D_boot=None, status="REFIT_FAILED"))
            continue
        N_refit_converged += 1
        v_boot = time_rescaling_residuals(res_boot.x, X_boot, T, mu_of_t=mu_of_t)
        if len(v_boot) == 0 or not np.isfinite(v_boot).all():
            N_nonfinite_residual_vector += 1
            N_nonfinite_statistic += 1
            row_records.append(dict(design=design_id, arm=arm, parent_rep=PARENT_REP, b=j,
                seed_integer=seed, seed_derivation_version=SEED_DERIVATION_VERSION,
                engine_hash=ENGINE_HASH, parent_input_hash=parent_input_hash,
                bootstrap_input_hash=bootstrap_input_hash, bootstrap_output_hash=None,
                n_boot_events=len(X_boot), refit_converged=True, D_boot=None, status="NONFINITE_RESIDUAL"))
            continue
        N_finite_residual_vector += 1
        D_b = kstest(v_boot, "uniform").statistic
        if not np.isfinite(D_b):
            N_nonfinite_statistic += 1
            status = "NONFINITE_STATISTIC"
            bootstrap_output_hash = None
        else:
            N_finite_statistic += 1
            D_boot_finite.append(D_b)
            status = "OK"
            bootstrap_output_hash = h(f"{res_boot.x.tolist()}|{D_b}".encode())
        row_records.append(dict(design=design_id, arm=arm, parent_rep=PARENT_REP, b=j,
            seed_integer=seed, seed_derivation_version=SEED_DERIVATION_VERSION,
            engine_hash=ENGINE_HASH, parent_input_hash=parent_input_hash,
            bootstrap_input_hash=bootstrap_input_hash, bootstrap_output_hash=bootstrap_output_hash,
            n_boot_events=len(X_boot), refit_converged=True, D_boot=(D_b if np.isfinite(D_b) else None), status=status))

    D_boot_arr = np.array(D_boot_finite)
    exceed_count = int(np.sum(D_boot_arr >= D_obs)) if len(D_boot_arr) else 0
    p_exceed = exceed_count / B_BOOT  # literal formula: denominator is fixed B_boot=499
    p_boot_corrected = (1 + exceed_count) / (B_BOOT + 1)
    mcse_boot = float(np.sqrt(p_exceed * (1 - p_exceed) / B_BOOT))

    complete = (N_requested == B_BOOT and N_simulation_failed == 0 and
                N_refit_failed == 0 and N_nonfinite_statistic == 0)
    r2_status = "R2_TERMINAL_COMPLETE" if complete else "R2_COMPLETE_WITH_FAILURES_REQUIRES_REVIEW"

    summary = dict(
        design=design_id, arm=arm, parent_replication_id=PARENT_REP,
        cross_process_reproducibility_ok=cross_process_ok,
        D_obs=D_obs,
        N_requested=N_requested, N_simulated=N_simulated, N_simulation_failed=N_simulation_failed,
        N_refit_attempted=N_refit_attempted, N_refit_converged=N_refit_converged, N_refit_failed=N_refit_failed,
        N_finite_residual_vector=N_finite_residual_vector, N_nonfinite_residual_vector=N_nonfinite_residual_vector,
        N_finite_statistic=N_finite_statistic, N_nonfinite_statistic=N_nonfinite_statistic,
        D_boot_mean=float(np.mean(D_boot_arr)) if len(D_boot_arr) else None,
        D_boot_sd=float(np.std(D_boot_arr, ddof=1)) if len(D_boot_arr) > 1 else None,
        D_boot_min=float(np.min(D_boot_arr)) if len(D_boot_arr) else None,
        D_boot_q025=float(np.quantile(D_boot_arr, 0.025)) if len(D_boot_arr) else None,
        D_boot_median=float(np.median(D_boot_arr)) if len(D_boot_arr) else None,
        D_boot_q975=float(np.quantile(D_boot_arr, 0.975)) if len(D_boot_arr) else None,
        D_boot_max=float(np.max(D_boot_arr)) if len(D_boot_arr) else None,
        N_bootstrap_exceedance=exceed_count,
        p_exceed_raw=p_exceed,
        p_boot_corrected=p_boot_corrected,
        MCSE_boot=mcse_boot,
        F_sim=N_simulation_failed / B_BOOT,
        F_refit=N_refit_failed / B_BOOT,
        F_stat=N_nonfinite_statistic / B_BOOT,
        R2_arm_status=r2_status,
        engine_hash=ENGINE_HASH, designs_hash=DESIGNS_HASH, parent_input_hash=parent_input_hash,
    )
    arm_summaries.append(summary)
    print(f"{design_id}/{arm}: D_obs={D_obs:.4f} N_conv={N_refit_converged}/{B_BOOT} "
          f"N_finite_stat={N_finite_statistic} exceed={exceed_count} "
          f"p_exceed={p_exceed:.4f} p_boot={p_boot_corrected:.4f} MCSE={mcse_boot:.4f} status={r2_status}")

import csv
with open("HAWKES_BASELINE_V2A_BOOTSTRAP_CALIBRATION_RESULTS.csv", "w", newline="") as f:
    fieldnames = list(arm_summaries[0].keys())
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for s in arm_summaries:
        w.writerow(s)

with open("HAWKES_BASELINE_V2A_BOOTSTRAP_CALIBRATION_ROWS.csv", "w", newline="") as f:
    fieldnames = list(row_records[0].keys())
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in row_records:
        w.writerow(r)

print("\nwrote", len(arm_summaries), "arm summaries and", len(row_records), "per-bootstrap rows")
