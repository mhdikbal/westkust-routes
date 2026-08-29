"""One deterministic end-to-end smoke test for M0: 1 scenario, 2
replicates, TINY window (10 years, not the real [1600,1784) window).

This module only proves the M0 pipeline (Stage 1-6 -> annual aggregation
-> Poisson MLE) runs without error and produces well-formed results. Its
output MUST NOT be used to evaluate MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv's
thresholds or claim any tournament recovery result -- that requires the
pre-registered recovery study (a separate, not-yet-authorized execution
step per MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md).

Run directly: python3 m0_smoke_test.py
"""

from __future__ import annotations

import numpy as np

from m0_baseline import fit_m0_poisson, run_full_pipeline_m0

SMOKE_TRUE_PARAMS = {"theta0": 1.0, "theta1": 0.3}
SMOKE_SEEDS = (2001, 2002)
SMOKE_WINDOW = (1600.0, 1610.0)  # 10 years -- smoke scale only, NOT the real [1600,1784) window


def run_smoke_test() -> dict:
    t0, t1 = SMOKE_WINDOW
    year_covariates = {y: 0.5 * np.sin(y / 10.0) for y in range(int(t0), int(t1))}
    results = []
    for seed in SMOKE_SEEDS:
        rng = np.random.default_rng(seed)
        events = run_full_pipeline_m0(
            SMOKE_TRUE_PARAMS["theta0"], SMOKE_TRUE_PARAMS["theta1"],
            year_covariates, "CD1_no_thinning", "year_only", t0, t1, rng,
        )
        fit = fit_m0_poisson(events, year_covariates, t0, t1)
        results.append({"seed": seed, "n_events": len(events), "fit": fit})
    return {
        "n_scenarios": 1, "n_replicates": len(SMOKE_SEEDS),
        "results": results, "gate_evaluation_performed": False,
    }


if __name__ == "__main__":
    result = run_smoke_test()
    print(f"n_scenarios={result['n_scenarios']} n_replicates={result['n_replicates']}")
    for r in result["results"]:
        print(f"  seed={r['seed']} n_events={r['n_events']} fit_status={r['fit'].status} fit_params={r['fit'].params}")
    print("gate_evaluation_performed=False (smoke test only -- not a pilot/final run)")
