"""One deterministic end-to-end smoke test for M2: 1 scenario, 2
replicates, TINY window (10 years, not the real [1600,1784) window).
Also runs a regression check against model3_mbpp_full.Xi_closed_form for
the theta1=0 (constant-baseline) special case, since this module's
density-baseline extension must reduce EXACTLY to the original
constant-baseline closed form when the covariate term is switched off --
this is the one non-negotiable correctness check for the new derivation
in m2_mbpp.py's Xi_closed_form_density_baseline.

Output MUST NOT be used to evaluate MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv's
thresholds or claim any tournament recovery result.

Run directly: python3 m2_smoke_test.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # colab/ for model3_mbpp_full
from m2_mbpp import Xi_closed_form_density_baseline, fit_m2, run_full_pipeline_m2  # noqa: E402
import model3_mbpp_full as mbpp_orig  # noqa: E402

SMOKE_TRUE_PARAMS = {"theta0": 1.0, "theta1": 0.3, "alpha": 0.3, "beta": 0.6}
SMOKE_SEEDS = (3001, 3002)
SMOKE_WINDOW = (1600.0, 1610.0)


def run_regression_check() -> float:
    """theta1=0 must reduce exactly to model3_mbpp_full's own Xi_closed_form."""
    year_covariates = {y: 0.0 for y in range(1600, 1610)}
    mu = np.exp(1.0)
    bin_edges = np.arange(1600, 1610, 1.0)
    Xi_new = Xi_closed_form_density_baseline(bin_edges, 1.0, 0.0, 0.3, 0.6, year_covariates, 1600.0)
    Xi_orig = mbpp_orig.Xi_closed_form(bin_edges - 1600.0, mu, 0.3, 0.6)
    return float(np.max(np.abs(Xi_new - Xi_orig)))


def run_smoke_test() -> dict:
    t0, t1 = SMOKE_WINDOW
    year_covariates = {y: 0.5 * np.sin(y / 10.0) for y in range(int(t0), int(t1))}
    regression_max_abs_diff = run_regression_check()
    results = []
    for seed in SMOKE_SEEDS:
        rng = np.random.default_rng(seed)
        events = run_full_pipeline_m2(
            SMOKE_TRUE_PARAMS["theta0"], SMOKE_TRUE_PARAMS["theta1"],
            SMOKE_TRUE_PARAMS["alpha"], SMOKE_TRUE_PARAMS["beta"],
            year_covariates, "CD1_no_thinning", "year_only", t0, t1, rng,
        )
        fit = fit_m2(events, year_covariates, t0, t1)
        results.append({"seed": seed, "n_events": len(events), "fit": fit})
    return {
        "n_scenarios": 1, "n_replicates": len(SMOKE_SEEDS),
        "regression_max_abs_diff_vs_mbpp_full": regression_max_abs_diff,
        "results": results, "gate_evaluation_performed": False,
    }


if __name__ == "__main__":
    result = run_smoke_test()
    print(f"regression check (theta1=0 vs model3_mbpp_full.Xi_closed_form): "
          f"max_abs_diff={result['regression_max_abs_diff_vs_mbpp_full']:.2e} "
          f"({'PASS' if result['regression_max_abs_diff_vs_mbpp_full'] < 1e-4 else 'FAIL'})")
    print(f"n_scenarios={result['n_scenarios']} n_replicates={result['n_replicates']}")
    for r in result["results"]:
        print(f"  seed={r['seed']} n_events={r['n_events']} fit_status={r['fit'].status} fit_params={r['fit'].params}")
    print("gate_evaluation_performed=False (smoke test only -- not a pilot/final run)")
