"""One deterministic end-to-end smoke test: 1 scenario, 1 grid point, 2
replicates (plan Fase 1 hard limit — NOT the pilot, NOT the final study).

This module only proves the pipeline (density -> simulate -> fit ->
metrics) runs without error and produces well-formed results. Its output
MUST NOT be used to evaluate the §9 decision gates, change the parameter
grid, change any numerical threshold, or claim simulation recovery
passed/failed — those require the pilot (100/cell) and final (1000/cell)
replicate runs described in the plan.

Run directly:  python smoke_test.py
"""

from __future__ import annotations

import time

import numpy as np

from .density import DEFAULT_WINDOW, build_x_cd_lookup, build_year_covariates, load_spec_a_density
from .estimate import fit_m3b_cd
from .logging_utils import FailureLog
from .rng import make_rng
from .schema import ReplicateResult
from .simulate import simulate_m3b_cd

# Production-calibrated ground truth for M1 component (plan §0, from
# HAWKES_MODEL_AUDIT.md): mu=0.2573, alpha=0.4207, beta=0.6215.
# theta0 calibrated so exp(theta0) ~= mu at x_CD=0 (plan §3); theta1 is a
# placeholder "moderate" value for pipeline-exercise purposes only — it is
# NOT a pilot/final grid value (plan §3: "nilai eksak grid ditentukan saat
# implementasi").
SMOKE_TRUE_PARAMS = {
    "theta0": float(np.log(0.2573)),
    "theta1": 0.1,
    "alpha": 0.4207,
    "beta": 0.6215,
}
SMOKE_SEEDS = (1001, 1002)
SMOKE_SCENARIO_ID = "smoke_scenario_3_density_plus_excitation"
SMOKE_GRID_POINT_ID = "smoke_grid_point_production_calibrated"


def run_smoke_test() -> dict:
    t0, t1 = float(DEFAULT_WINDOW[0]), float(DEFAULT_WINDOW[1])
    density_before = load_spec_a_density(window=DEFAULT_WINDOW)
    series = density_before
    x_cd = build_x_cd_lookup(series)
    year_covariates = build_year_covariates(series)

    failure_log = FailureLog()
    replicate_results: list[ReplicateResult] = []
    start = time.perf_counter()
    for replicate_id, seed in enumerate(SMOKE_SEEDS, start=1):
        rng = make_rng(seed)
        events = simulate_m3b_cd(
            SMOKE_TRUE_PARAMS["theta0"],
            SMOKE_TRUE_PARAMS["theta1"],
            SMOKE_TRUE_PARAMS["alpha"],
            SMOKE_TRUE_PARAMS["beta"],
            x_cd,
            t0,
            t1,
            rng,
        )
        fit = fit_m3b_cd(
            events,
            year_covariates,
            t0,
            t1,
            failure_log=failure_log,
            scenario_id=SMOKE_SCENARIO_ID,
            grid_point_id=SMOKE_GRID_POINT_ID,
            replicate_id=replicate_id,
        )
        replicate_results.append(
            ReplicateResult(
                scenario_id=SMOKE_SCENARIO_ID,
                grid_point_id=SMOKE_GRID_POINT_ID,
                replicate_id=replicate_id,
                seed=seed,
                true_params=dict(SMOKE_TRUE_PARAMS),
                n_simulated_events=int(events.size),
                fit=fit,
            )
        )
    runtime_seconds = time.perf_counter() - start

    density_after = load_spec_a_density(window=DEFAULT_WINDOW)
    source_unchanged = (
        density_before.years.tolist() == density_after.years.tolist()
        and density_before.counts.tolist() == density_after.counts.tolist()
    )

    return {
        "n_scenarios": 1,
        "n_grid_points": 1,
        "n_replicates": len(SMOKE_SEEDS),
        "runtime_seconds": runtime_seconds,
        "replicate_results": replicate_results,
        "failure_log": failure_log,
        "source_density_unchanged": source_unchanged,
        "gate_evaluation_performed": False,
    }


if __name__ == "__main__":
    result = run_smoke_test()
    print(f"n_scenarios={result['n_scenarios']} n_grid_points={result['n_grid_points']} n_replicates={result['n_replicates']}")
    print(f"runtime_seconds={result['runtime_seconds']:.4f}")
    print(f"source_density_unchanged={result['source_density_unchanged']}")
    print(f"failures_logged={len(result['failure_log'])}")
    for rr in result["replicate_results"]:
        print(
            f"  replicate={rr.replicate_id} seed={rr.seed} n_events={rr.n_simulated_events} "
            f"fit_status={rr.fit.status} fit_params={rr.fit.params}"
        )
    print("gate_evaluation_performed=False (smoke test only — not a pilot/final run)")
