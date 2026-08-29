"""One deterministic end-to-end smoke test for M3: 1 scenario, TINY window
(20 years, not the real [1600,1784) window), TINY MCMC (300 draws / 150
burn-in, not the pre-registered study's multi-chain, thousands-of-draws
design). Exercises: discrete-Hawkes simulation -> full observation-regime
pipeline (Stages 2-6) -> annual aggregation (Stage 7) -> hand-rolled MCMC
(Stage 8) -> WAIC (Stage 9's model-selection metric).

Output MUST NOT be used to evaluate MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv's
thresholds or claim any tournament recovery result -- that requires the
pre-registered recovery study (a separate, not-yet-authorized execution
step per MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md).

Run directly: python3 m3_smoke_test.py
"""

from __future__ import annotations

import numpy as np

from m3_bayesian_discrete import (
    annual_counts_from_censored,
    fit_m3_mcmc,
    run_full_pipeline_m3,
    simulate_m3,
    waic,
)

SMOKE_TRUE_PARAMS = {"theta0": 1.0, "theta1": 0.2, "n_branch": 0.3, "beta": 0.6}
SMOKE_WINDOW = (1600.0, 1620.0)  # 20 years -- smoke scale only
SMOKE_MCMC = {"n_draws": 300, "n_burnin": 150}


def run_smoke_test() -> dict:
    t0, t1 = SMOKE_WINDOW
    year_covariates = {y: 0.3 * np.sin(y / 10.0) for y in range(int(t0), int(t1))}

    # Direct discrete-native path (simulate_m3 -> annual counts directly).
    rng = np.random.default_rng(7001)
    counts_direct = simulate_m3(
        SMOKE_TRUE_PARAMS["theta0"], SMOKE_TRUE_PARAMS["theta1"],
        SMOKE_TRUE_PARAMS["n_branch"], SMOKE_TRUE_PARAMS["beta"],
        year_covariates, int(t0), int(t1), rng,
    )

    # Full-pipeline path (Stages 2-6 applied, then re-aggregated to counts).
    rng2 = np.random.default_rng(7002)
    events = run_full_pipeline_m3(
        SMOKE_TRUE_PARAMS["theta0"], SMOKE_TRUE_PARAMS["theta1"],
        SMOKE_TRUE_PARAMS["n_branch"], SMOKE_TRUE_PARAMS["beta"],
        year_covariates, "CD1_no_thinning", "year_only", t0, t1, rng2,
    )
    years, counts_pipeline = annual_counts_from_censored(events, t0, t1)
    x_ordered = np.array([year_covariates[y] for y in years])

    post = fit_m3_mcmc(counts_pipeline, x_ordered, rng=np.random.default_rng(7003), **SMOKE_MCMC)
    waic_val = waic(post.pointwise_loglik) if post.pointwise_loglik.size else float("nan")

    return {
        "counts_direct": counts_direct, "n_pipeline_events": len(events),
        "counts_pipeline": counts_pipeline, "posterior": post, "waic": waic_val,
        "gate_evaluation_performed": False,
    }


if __name__ == "__main__":
    result = run_smoke_test()
    print(f"direct discrete-native counts: {result['counts_direct'].tolist()}")
    print(f"full-pipeline n_events={result['n_pipeline_events']} counts={result['counts_pipeline'].tolist()}")
    post = result["posterior"]
    print(f"MCMC: n_draws={post.n_draws} n_burnin={post.n_burnin} acceptance_rate={post.acceptance_rate:.3f} status={post.status}")
    print(f"posterior_mean={post.posterior_mean()}")
    print(f"credible_interval(n, 95%)={post.credible_interval('n')}")
    print(f"WAIC={result['waic']:.3f}")
    print("gate_evaluation_performed=False (smoke test only -- not a pilot/final run)")
