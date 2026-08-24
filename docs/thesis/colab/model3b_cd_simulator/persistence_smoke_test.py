"""ONE cell, ONE replicate smoke test for event_times persistence + the
Fase 3A instrumentation layer, end to end: simulate -> persist -> read
back -> verify checksum -> fit M1/M2/M3B-CD from the ROUND-TRIPPED
sequence -> confirm the M2-vs-M3B-CD boundary test and AIC/BIC.

This is explicitly NOT the 10x10 instrumentation pilot and NOT the final
1000-replicate run. Its output must not be used for any recovery-gate
assessment. Uses the already-frozen S3-G1 cell (exponential kernel,
production-calibrated) from
docs/thesis/pilot_annotation/MODEL_3B_CD_SIMULATION_CELL_MANIFEST.md.

Run directly: python -m model3b_cd_simulator.persistence_smoke_test
"""

from __future__ import annotations

import json
import subprocess

from . import persistence as p
from .density import DEFAULT_WINDOW, build_x_cd_lookup, build_year_covariates, load_spec_a_density
from .inference import fit_m1_with_inference, fit_m2_with_inference, fit_m3b_cd_with_inference
from .rng import make_rng
from .simulate import simulate_m3b_cd

CELL_ID = "S3-G1"
TRUTH = {"theta0": -1.357513, "theta1": 0.1, "alpha": 0.4207, "beta": 0.6215}
BASE_SEED = 20260823  # same convention as the manifest's S3-G1 pilot cell
REPLICATE_ID = 1
REPLICATE_SEED = BASE_SEED + REPLICATE_ID
T0, T1 = float(DEFAULT_WINDOW[0]), float(DEFAULT_WINDOW[1])


def _git_commit() -> str:
    return subprocess.check_output(
        ["git", "-C", "/home/naro/westkust-routes", "rev-parse", "--short", "HEAD"], text=True
    ).strip()


def run_smoke_test() -> dict:
    commit = _git_commit()
    series = load_spec_a_density(window=DEFAULT_WINDOW)
    x_cd = build_x_cd_lookup(series)
    year_covariates = build_year_covariates(series)

    # --- simulate exactly ONE replicate ---
    rng = make_rng(REPLICATE_SEED)
    events = simulate_m3b_cd(TRUTH["theta0"], TRUTH["theta1"], TRUTH["alpha"], TRUTH["beta"], x_cd, T0, T1, rng)

    # --- fit once, for the persisted point-estimate fields ---
    point_fit = fit_m3b_cd_with_inference(events, year_covariates, T0, T1)

    # --- persist (event_times required, validated, checksummed) ---
    result = p.make_new_replicate_result(
        cell_id=CELL_ID, replicate_id=REPLICATE_ID, base_seed=BASE_SEED, replicate_seed=REPLICATE_SEED,
        simulator_commit=commit, instrumentation_commit=commit, density_checksum="n/a-smoke-test",
        simulation_kernel="exponential", fitted_kernel="exponential", truth_parameters=TRUTH,
        event_times=events, t0=T0, t1=T1,
        fit_status=point_fit.fit.status, fit_success=point_fit.fit.success,
        fit_params=point_fit.fit.params, fit_loglik=point_fit.fit.loglik, runtime_seconds=0.0,
    )
    serialized = p.serialize_result(result)

    # --- round trip through a JSON string, exactly like a real file would ---
    roundtripped_dict = json.loads(json.dumps(serialized))
    loaded = p.load_result(roundtripped_dict, t0=T0, t1=T1)
    checksum_ok = isinstance(loaded, p.NewReplicateResult) and loaded.event_times_sha256 == result.event_times_sha256

    # --- re-fit M1, M2, M3B-CD from the ROUND-TRIPPED event_times ---
    r_m1 = fit_m1_with_inference(loaded.event_times, T0, T1)
    r_m2 = fit_m2_with_inference(loaded.event_times, year_covariates, T0, T1)
    r_m3b = fit_m3b_cd_with_inference(loaded.event_times, year_covariates, T0, T1)

    boundary = r_m3b.boundary_alpha_test
    boundary_label_correct = boundary is not None and boundary.restricted_model == "m2" and boundary.unrestricted_model == "m3b_cd"

    return {
        "cell_id": CELL_ID,
        "replicate_id": REPLICATE_ID,
        "n_events": int(events.size),
        "event_times_stored": True,
        "event_times_sha256": result.event_times_sha256,
        "checksum_match_after_roundtrip": checksum_ok,
        "fits": {
            "m1": {"status": r_m1.fit.status, "aic": r_m1.aic, "bic": r_m1.bic},
            "m2": {"status": r_m2.fit.status, "aic": r_m2.aic, "bic": r_m2.bic},
            "m3b_cd": {"status": r_m3b.fit.status, "aic": r_m3b.aic, "bic": r_m3b.bic},
        },
        "boundary_test_m2_vs_m3b_cd": {
            "restricted_model": boundary.restricted_model if boundary else None,
            "unrestricted_model": boundary.unrestricted_model if boundary else None,
            "label_correct": boundary_label_correct,
            "lr": boundary.test_statistic_lr if boundary else None,
            "p_value": boundary.p_value if boundary else None,
        },
        "aic_bic_available": all(r.aic is not None and r.bic is not None for r in (r_m1, r_m2, r_m3b)),
        "not_pilot_10x10": True,
        "not_final_1000": True,
        "not_used_for_recovery_assessment": True,
    }


if __name__ == "__main__":
    result = run_smoke_test()
    print(json.dumps(result, indent=2, default=str))
