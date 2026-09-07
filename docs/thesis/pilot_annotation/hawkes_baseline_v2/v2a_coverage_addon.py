"""
Coverage_r addon: recompute Hessian-based 95% Wald CIs for every recovery-
family replication (D7,D8,D9x2 arms,D10) that already converged. This was
missing from the original v2a_full_study.py run -- an honest completion gap,
fixed here rather than silently omitted.
"""
import json
import numpy as np
from v2a_validation_engine import fit_hawkes, hawkes_hessian_se, T_HORIZON, cd_density_at, design_seed
from v2a_designs import DESIGNS, gen_D10_latent, gen_D10_observed, assign_precision_classes, MU0_D9

T = T_HORIZON
SEED_BASE = 20260906
Z95 = 1.959963984540054

def regen_events(design_id, rep):
    rng = np.random.default_rng(design_seed(design_id, rep))
    if design_id == "D10":
        latent = gen_D10_latent(rng)
        # must replicate the EXACT (post-fix) rng call sequence used in
        # v2a_full_study.py's run_family_recovery: ONE assign_precision_classes
        # draw shared by n_interval_observed and gen_D10_observed (checkpoint-5
        # reconciliation fix for the D10 double-draw defect).
        classes = assign_precision_classes(latent, rng)
        return gen_D10_observed(latent, classes, rng)
    return DESIGNS[design_id]["generator"](rng)

recovery = json.load(open("v2a_full_study_recovery_rows.json"))
out = []
n_processed = 0
for row in recovery:
    d, arm, rep = row["design"], row.get("arm", "primary"), row["rep"]
    if not row["converged"]:
        row["coverage_mu"] = None
        row["coverage_alpha"] = None
        row["coverage_beta"] = None
        out.append(row)
        continue
    events = regen_events(d, rep)
    params = [row["mu_hat"], row["alpha_hat"], row["beta_hat"]]
    if d == "D9":
        mu_of_t = (lambda t: cd_density_at(np.atleast_1d(t))) if arm == "correct_cd_modulated" else None
    else:
        mu_of_t = None
    se = hawkes_hessian_se(params, events, T, mu_of_t=mu_of_t)
    theta_true = [row["true_mu"], row["true_alpha"], row["true_beta"]]
    covered = []
    for k in range(3):
        if np.isnan(se[k]) or se[k] <= 0 or not np.isfinite(se[k]):
            covered.append(None)
            continue
        lo, hi = params[k] - Z95 * se[k], params[k] + Z95 * se[k]
        covered.append(bool(lo <= theta_true[k] <= hi))
    row["coverage_mu"], row["coverage_alpha"], row["coverage_beta"] = covered
    row["se_mu"], row["se_alpha"], row["se_beta"] = [float(x) if np.isfinite(x) else None for x in se]
    out.append(row)
    n_processed += 1

json.dump(out, open("v2a_full_study_recovery_rows.json", "w"), default=str)
print(f"Coverage addon: processed {n_processed} converged replications with Hessian SE + Wald CI")
