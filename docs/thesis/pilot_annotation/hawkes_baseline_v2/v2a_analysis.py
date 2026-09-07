import json, csv
import numpy as np

fpr = json.load(open("v2a_full_study_fpr_rows.json"))
rec = json.load(open("v2a_full_study_recovery_rows.json"))
DELTA_GRID = [0, 2, 6, 10]
B = 278

def jackknife_rmse(errors):
    """errors = theta_hat - theta array (finite only); jackknife SE of RMSE."""
    errors = np.asarray(errors, dtype=float)
    errors = errors[np.isfinite(errors)]
    n = len(errors)
    if n < 3:
        return np.nan, np.nan
    rmse_full = np.sqrt(np.mean(errors**2))
    jk_vals = []
    for i in range(n):
        e_i = np.delete(errors, i)
        jk_vals.append(np.sqrt(np.mean(e_i**2)))
    jk_vals = np.array(jk_vals)
    jk_mean = jk_vals.mean()
    se_jk = np.sqrt((n-1)/n * np.sum((jk_vals - jk_mean)**2))
    return rmse_full, se_jk

# ---------------------------------------------------------------------------
# Part 1: D1-D6 FPR/PR summary + continuous delta-AIC/BIC + threshold grid
# ---------------------------------------------------------------------------
by_design = {}
for row in fpr:
    by_design.setdefault(row["design"], []).append(row)

summary_rows = []
for d, rows in by_design.items():
    n = len(rows)
    n_conv = sum(1 for r in rows if r["hawkes_converged"])
    if d != "D5":
        dAIC = [r["aic_comparator"] - r["aic_hawkes"] for r in rows if r["hawkes_converged"]]  # positive = Hawkes better
        dBIC = [r["bic_comparator"] - r["bic_hawkes"] for r in rows if r["hawkes_converged"]]
        comparator_specified = rows[0]["comparator_specified"]
        rate_label = "FALSE_SELECTION_RATE" if comparator_specified else (
            "HAWKES_PREFERENCE_RATE_UNDER_NAIVE_POINT_SUBSTITUTION" if d == "D4" else "PREFERENCE_RATE_MISSPECIFIED_COMPARATOR")
        threshold_rates = {f"delta{th}": float(np.mean([1 if x > th else 0 for x in dAIC])) for th in DELTA_GRID}
        mcse_threshold = {f"delta{th}_mcse": float(np.sqrt(max(threshold_rates[f'delta{th}'],1e-9)*(1-min(threshold_rates[f'delta{th}'],1-1e-9))/n)) for th in DELTA_GRID}
        summary_rows.append({
            "design": d, "n_reps": n, "n_converged": n_conv,
            "rate_label": rate_label,
            "mean_deltaAIC": float(np.mean(dAIC)), "median_deltaAIC": float(np.median(dAIC)),
            "q10_deltaAIC": float(np.quantile(dAIC, 0.10)), "q90_deltaAIC": float(np.quantile(dAIC, 0.90)),
            "mean_deltaBIC": float(np.mean(dBIC)), "median_deltaBIC": float(np.median(dBIC)),
            **threshold_rates, **mcse_threshold,
            "comparator_specified": comparator_specified,
        })
    else:
        dAIC_naive = [r["aic_comparator_naive"] - r["aic_hawkes"] for r in rows if r["hawkes_converged"]]
        dAIC_correct = [r["aic_comparator_correct"] - r["aic_hawkes"] for r in rows if r["hawkes_converged"]]
        dBIC_naive = [r["bic_comparator_naive"] - r["bic_hawkes"] for r in rows if r["hawkes_converged"]]
        dBIC_correct = [r["bic_comparator_correct"] - r["bic_hawkes"] for r in rows if r["hawkes_converged"]]
        thr_correct = {f"delta{th}": float(np.mean([1 if x > th else 0 for x in dAIC_correct])) for th in DELTA_GRID}
        thr_naive = {f"delta{th}_naive": float(np.mean([1 if x > th else 0 for x in dAIC_naive])) for th in DELTA_GRID}
        summary_rows.append({
            "design": "D5_vs_correct_density_comparator", "n_reps": n, "n_converged": n_conv,
            "rate_label": "FALSE_SELECTION_RATE",
            "mean_deltaAIC": float(np.mean(dAIC_correct)), "median_deltaAIC": float(np.median(dAIC_correct)),
            "q10_deltaAIC": float(np.quantile(dAIC_correct,0.10)), "q90_deltaAIC": float(np.quantile(dAIC_correct,0.90)),
            "mean_deltaBIC": float(np.mean(dBIC_correct)), "median_deltaBIC": float(np.median(dBIC_correct)),
            **thr_correct, "comparator_specified": True,
        })
        summary_rows.append({
            "design": "D5_vs_naive_homogeneous_comparator", "n_reps": n, "n_converged": n_conv,
            "rate_label": "PREFERENCE_RATE",
            "mean_deltaAIC": float(np.mean(dAIC_naive)), "median_deltaAIC": float(np.median(dAIC_naive)),
            "q10_deltaAIC": float(np.quantile(dAIC_naive,0.10)), "q90_deltaAIC": float(np.quantile(dAIC_naive,0.90)),
            "mean_deltaBIC": float(np.mean(dBIC_naive)), "median_deltaBIC": float(np.median(dBIC_naive)),
            **thr_naive, "comparator_specified": False,
        })

with open("v2a_summary_fpr.csv", "w", newline="") as f:
    allkeys = sorted(set(k for r in summary_rows for k in r.keys()))
    w = csv.DictWriter(f, fieldnames=allkeys)
    w.writeheader()
    for r in summary_rows:
        w.writerow(r)

print("=== D1-D6 SUMMARY ===")
for r in summary_rows:
    print(r["design"], r["rate_label"], "n_conv=", r["n_converged"], "delta2_rate=", r.get("delta2"), "delta2_naive=", r.get("delta2_naive"))

# ---------------------------------------------------------------------------
# Part 2: D7-D10 recovery metrics
# ---------------------------------------------------------------------------
by_design_rec = {}
for row in rec:
    key = (row["design"], row.get("arm", "primary"))
    by_design_rec.setdefault(key, []).append(row)

recovery_summary = []
for (d, arm), rows in by_design_rec.items():
    n = len(rows)
    n_conv = sum(1 for r in rows if r["converged"])
    n_failed = n - n_conv
    param_summary = {}
    for p in ["mu", "alpha", "beta", "eta"]:
        theta_true = rows[0][f"true_{p}"]
        # denominator stays at B=278 (failed fits count as non-recovered / excluded from point estimate but included in count)
        vals = [r[f"{p}_hat"] for r in rows]  # includes NaN for failed fits
        errors_all = np.array([ (v - theta_true) if (v is not None and not np.isnan(v)) else np.nan for v in vals ])
        finite_errors = errors_all[np.isfinite(errors_all)]
        bias = float(np.mean(finite_errors)) if len(finite_errors) else np.nan
        rb = float(np.mean(finite_errors / theta_true)) if (theta_true not in (0, None) and len(finite_errors)) else np.nan
        rmse, rmse_jk_se = jackknife_rmse(finite_errors) if len(finite_errors) >= 3 else (np.nan, np.nan)
        # Coverage via Wald CI from finite-diff Hessian SE (approx, using +-1.96*SE), computed per replication in main study? -- not stored; approximate here is NOT available per-rep SE, so report NaN and flag
        param_summary[p] = {
            "true": theta_true, "bias": bias, "rb": rb, "n_finite": int(len(finite_errors)),
            "rmse": rmse, "rmse_jackknife_se": rmse_jk_se,
            "mcse_bias": float(np.std(finite_errors, ddof=1)/np.sqrt(n)) if len(finite_errors) > 1 else np.nan,
        }
    fopt = n_failed / n
    mcse_fopt = float(np.sqrt(max(fopt,1e-9)*(1-min(fopt,1-1e-9))/n))
    row_out = {"design": d, "arm": arm, "n_reps": n, "n_converged": n_conv, "n_failed_fits": n_failed,
               "F_opt": fopt, "mcse_F_opt": mcse_fopt,
               "counted_toward_H05": rows[0].get("counted_toward_H05")}
    for p, s in param_summary.items():
        for k, v in s.items():
            row_out[f"{p}_{k}"] = v
    if d in ("D7", "D8", "D9", "D10"):
        ks_vals = [r.get("ks_pvalue_residuals") for r in rows if r.get("ks_pvalue_residuals") is not None and not np.isnan(r.get("ks_pvalue_residuals", np.nan))]
        row_out["ks_pvalue_mean"] = float(np.mean(ks_vals)) if ks_vals else np.nan
        row_out["ks_pvalue_frac_below_0.05"] = float(np.mean([1 if v < 0.05 else 0 for v in ks_vals])) if ks_vals else np.nan
        row_out["n_ks_computed"] = len(ks_vals)
    recovery_summary.append(row_out)

with open("v2a_summary_recovery.csv", "w", newline="") as f:
    allkeys = sorted(set(k for r in recovery_summary for k in r.keys()))
    w = csv.DictWriter(f, fieldnames=allkeys)
    w.writeheader()
    for r in recovery_summary:
        w.writerow(r)

print("\n=== D7-D10 RECOVERY SUMMARY ===")
for r in recovery_summary:
    print(r["design"], r["arm"], "F_opt=", round(r["F_opt"],4), "mu_bias=", r.get("mu_bias"), "alpha_bias=", r.get("alpha_bias"), "beta_bias=", r.get("beta_bias"), "ks_mean_p=", r.get("ks_pvalue_mean"))

# D10 N_latent/N_interval_observed/N_estimator_input distributions
d10_rows = by_design_rec[("D10", "primary")]
n_latent = [r["n_latent"] for r in d10_rows]
n_interval = [r["n_interval_observed"] for r in d10_rows]
n_est = [r["n_estimator_input"] for r in d10_rows]
print("\n=== D10 event-count pipeline ===")
print("N_latent: mean=", np.mean(n_latent), "sd=", np.std(n_latent))
print("N_interval_observed: mean=", np.mean(n_interval), "sd=", np.std(n_interval))
print("N_estimator_input: mean=", np.mean(n_est), "sd=", np.std(n_est))

with open("v2a_d10_pipeline.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rep", "n_latent", "n_interval_observed", "n_estimator_input"])
    for r in d10_rows:
        w.writerow([r["rep"], r["n_latent"], r["n_interval_observed"], r["n_estimator_input"]])

# event-count distributions for D1-D9 too
print("\n=== Achieved event-count distributions (all designs) ===")
achieved = {}
for d, rows in by_design.items():
    ns = [r["n_events"] for r in rows]
    achieved[d] = (np.mean(ns), np.std(ns))
    print(d, "mean_n=", round(np.mean(ns),1), "sd_n=", round(np.std(ns),1))
for (d,arm), rows in by_design_rec.items():
    ns = [r["n_events"] for r in rows]
    print(d, arm, "mean_n=", round(np.mean(ns),1), "sd_n=", round(np.std(ns),1))
