"""
V2-A FULL STUDY. B=278 per design, N_full_study_plan=2780.
Frozen per checkpoints 3-4. Synthetic data only.
"""
import numpy as np
import time
import json
import csv
from v2a_validation_engine import (
    fit_hawkes, fit_homogeneous_poisson, fit_inhomogeneous_poisson_cd,
    aic, bic, T_HORIZON, time_rescaling_residuals, ks_uniform_pvalue,
    cd_density_at, design_seed,
)
from v2a_designs import (
    DESIGNS, gen_D10_latent, gen_D10_observed, assign_precision_classes,
    p_obs_at, MU0_D9, ALPHA_D9, BETA_D9, ETA_D9,
)

T = T_HORIZON
B = 278
SEED_BASE = 20260906
DELTA_GRID = [0, 2, 6, 10]

def fisher_se(res, t_events, T, mu_of_t=None, eps=1e-4):
    from v2a_validation_engine import hawkes_hessian_se
    return hawkes_hessian_se(res.x, t_events, T, mu_of_t)

def hawkes_fit_and_diag(events, mu_of_t=None):
    res = fit_hawkes(events, T, mu_of_t=mu_of_t)
    ok = bool(res.success) and len(events) > 3
    ll = -res.fun
    return res, ok, ll

def run_family_FPR_or_PR(design_id, rep, n_success, rows_out):
    """D1,D2,D3,D4,D5,D6: Hawkes vs comparator(s), AIC/BIC continuous + threshold grid."""
    rng = np.random.default_rng(design_seed(design_id, rep))
    gen = DESIGNS[design_id]["generator"]
    events = gen(rng) if design_id != "D4" else DESIGNS["D4"]["generator"](rng)
    n_events = len(events)

    res_h, ok_h, ll_h = hawkes_fit_and_diag(events)
    aic_h = aic(ll_h, 3) if ok_h else np.nan
    bic_h = bic(ll_h, 3, n_events) if ok_h else np.nan

    row = {"design": design_id, "rep": rep, "n_events": n_events,
           "hawkes_converged": ok_h, "aic_hawkes": aic_h, "bic_hawkes": bic_h}

    if design_id in ("D1", "D2", "D4"):
        mu_hat, ll_p = fit_homogeneous_poisson(events, T)
        aic_p, bic_p = aic(ll_p, 1), bic(ll_p, 1, n_events)
        row.update({"aic_comparator": aic_p, "bic_comparator": bic_p,
                    "comparator": "homogeneous_poisson", "comparator_specified": design_id != "D4" and design_id != "D2"})
        # D1: correctly specified; D2: comparator is homogeneous but truth is smooth-inhomog -> misspecified;
        # D4: latent generator is homog Poisson but observed process has heaped ties -> comparator NOT_AVAILABLE per correction
        if design_id == "D1":
            row["comparator_specified"] = True
        elif design_id == "D2":
            row["comparator_specified"] = False  # homogeneous comparator is misspecified vs smooth-inhomogeneous truth; still reported as best available
        elif design_id == "D4":
            row["comparator_specified"] = False  # NOT_AVAILABLE_IN_CURRENT_DESIGN per correction; homogeneous fit used only as nominal reference
    elif design_id == "D3":
        (b0, b1), ll_p = fit_inhomogeneous_poisson_cd(events, T)
        aic_p, bic_p = aic(ll_p, 2), bic(ll_p, 2, n_events)
        row.update({"aic_comparator": aic_p, "bic_comparator": bic_p,
                    "comparator": "cd_covariate_poisson", "comparator_specified": True})
    elif design_id == "D5":
        mu_hat, ll_naive = fit_homogeneous_poisson(events, T)
        aic_naive, bic_naive = aic(ll_naive, 1), bic(ll_naive, 1, n_events)
        (b0, b1), ll_correct = fit_inhomogeneous_poisson_cd(events, T)
        aic_correct, bic_correct = aic(ll_correct, 2), bic(ll_correct, 2, n_events)
        row.update({"aic_comparator_naive": aic_naive, "bic_comparator_naive": bic_naive,
                    "aic_comparator_correct": aic_correct, "bic_comparator_correct": bic_correct})
    elif design_id == "D6":
        mu_hat, ll_p = fit_homogeneous_poisson(events, T)
        aic_p, bic_p = aic(ll_p, 1), bic(ll_p, 1, n_events)
        row.update({"aic_comparator": aic_p, "bic_comparator": bic_p,
                    "comparator": "homogeneous_poisson_misspecified_vs_cluster", "comparator_specified": False})
    rows_out.append(row)

def run_family_recovery(design_id, rep, rows_out):
    """D7,D8,D9(correct+misspecified arms),D10: Bias/RMSE/Coverage per parameter."""
    rng = np.random.default_rng(design_seed(design_id, rep))
    true = DESIGNS[design_id]["true"]

    if design_id == "D9":
        mu_fn_correct = lambda t: cd_density_at(np.atleast_1d(t))  # SHAPE only; mu itself is the free estimated parameter
        events = DESIGNS["D9"]["generator"](rng)
        n_events = len(events)
        res_c, ok_c, ll_c = hawkes_fit_and_diag(events, mu_of_t=mu_fn_correct)
        res_m, ok_m, ll_m = hawkes_fit_and_diag(events, mu_of_t=None)  # misspecified constant-mu arm
        v_c = time_rescaling_residuals(res_c.x, events, T, mu_of_t=mu_fn_correct) if ok_c else np.array([])
        ks_c = ks_uniform_pvalue(v_c) if len(v_c) >= 3 else np.nan
        v_m = time_rescaling_residuals(res_m.x, events, T, mu_of_t=None) if ok_m else np.array([])
        ks_m = ks_uniform_pvalue(v_m) if len(v_m) >= 3 else np.nan
        rows_out.append({
            "design": "D9", "rep": rep, "arm": "correct_cd_modulated", "n_events": n_events,
            "converged": ok_c, "mu_hat": res_c.x[0] if ok_c else np.nan,
            "alpha_hat": res_c.x[1] if ok_c else np.nan, "beta_hat": res_c.x[2] if ok_c else np.nan,
            "eta_hat": (res_c.x[1]/res_c.x[2]) if ok_c else np.nan,
            "true_mu": true["mu"], "true_alpha": true["alpha"], "true_beta": true["beta"], "true_eta": true["eta"],
            "ks_pvalue_residuals": ks_c, "counted_toward_H05": True,
        })
        rows_out.append({
            "design": "D9", "rep": rep, "arm": "misspecified_constant_mu", "n_events": n_events,
            "converged": ok_m, "mu_hat": res_m.x[0] if ok_m else np.nan,
            "alpha_hat": res_m.x[1] if ok_m else np.nan, "beta_hat": res_m.x[2] if ok_m else np.nan,
            "eta_hat": (res_m.x[1]/res_m.x[2]) if ok_m else np.nan,
            "true_mu": true["mu"], "true_alpha": true["alpha"], "true_beta": true["beta"], "true_eta": true["eta"],
            "ks_pvalue_residuals": ks_m,
            "counted_toward_H05": False,  # descriptive robustness illustration ONLY, excluded from H-05 evidence
        })
        return

    if design_id == "D10":
        latent = gen_D10_latent(rng)
        n_latent = len(latent)
        classes = assign_precision_classes(latent, rng)
        n_unresolved = int(np.sum(classes == "unresolved"))
        n_interval_observed = n_latent - n_unresolved
        observed = gen_D10_observed(latent, classes, rng)
        n_estimator_input = len(observed)
        events = observed
        n_events = n_estimator_input
        extra = {"n_latent": n_latent, "n_interval_observed": n_interval_observed, "n_estimator_input": n_estimator_input}
    else:
        events = DESIGNS[design_id]["generator"](rng)
        n_events = len(events)
        extra = {}

    res, ok, ll = hawkes_fit_and_diag(events)
    v = time_rescaling_residuals(res.x, events, T) if ok else np.array([])
    ks_p = ks_uniform_pvalue(v) if len(v) >= 3 else np.nan
    ks_mean_v = float(np.mean(v)) if len(v) > 0 else np.nan

    row = {"design": design_id, "rep": rep, "arm": "primary", "n_events": n_events,
           "converged": ok, "mu_hat": res.x[0] if ok else np.nan,
           "alpha_hat": res.x[1] if ok else np.nan, "beta_hat": res.x[2] if ok else np.nan,
           "eta_hat": (res.x[1]/res.x[2]) if ok else np.nan,
           "true_mu": true["mu"], "true_alpha": true["alpha"], "true_beta": true["beta"], "true_eta": true["eta"],
           "ks_pvalue_residuals": ks_p, "mean_v_residual": ks_mean_v,
           "counted_toward_H05": True}
    row.update(extra)
    rows_out.append(row)

def main():
    t0 = time.time()
    fpr_rows, recovery_rows = [], []
    n_attempted = 0
    errors = []
    for d in DESIGNS:
        family = DESIGNS[d]["family"]
        for r in range(B):
            n_attempted += 1
            try:
                if family in ("RECOVERY", "RECOVERY_INTERVAL"):
                    run_family_recovery(d, r, recovery_rows)
                else:
                    run_family_FPR_or_PR(d, r, n_attempted, fpr_rows)
            except Exception as e:
                errors.append({"design": d, "rep": r, "error": str(e)})
    elapsed = time.time() - t0

    with open("v2a_full_study_fpr_rows.json", "w") as f:
        json.dump(fpr_rows, f, default=str)
    with open("v2a_full_study_recovery_rows.json", "w") as f:
        json.dump(recovery_rows, f, default=str)
    with open("v2a_full_study_meta.json", "w") as f:
        json.dump({"N_full_study_plan": 10 * B, "N_attempted": n_attempted,
                    "N_errors": len(errors), "errors": errors, "elapsed_sec": elapsed}, f, indent=2, default=str)

    print(f"FULL STUDY DONE: {n_attempted} attempted, {len(errors)} errors, {elapsed:.1f}s")

if __name__ == "__main__":
    main()
