"""Unit test #10 (Fase 1 requirement list)."""

import math

import pytest

from model3b_cd_simulator.schema import FitResult, ReplicateResult


def test_fit_result_schema_consistency():
    """#10 — FitResult fields/types must be well-formed for every status."""
    ok = FitResult(
        model="m1",
        params={"mu": 0.25, "alpha": 0.4, "beta": 0.6},
        success=True,
        status="ok",
        loglik=-123.4,
        n_events=141,
        boundary_flags={"mu": False, "alpha": False, "beta": False},
    )
    assert ok.is_valid is True
    assert ok.any_boundary_flag is False

    failed = FitResult(
        model="m1",
        params={"mu": 1e-6, "alpha": 0.0, "beta": 1e-6},
        success=False,
        status="optimizer_failed",
        loglik=math.nan,
        n_events=0,
        boundary_flags={"mu": True, "alpha": False, "beta": True},
    )
    assert failed.is_valid is False
    assert failed.any_boundary_flag is True

    with pytest.raises(ValueError):
        FitResult(
            model="m1", params={}, success=True, status="not_a_real_status",
            loglik=0.0, n_events=0, boundary_flags={},
        )


def test_replicate_result_keeps_truth_separate_from_estimate():
    """#10 (and §9 guard) — ReplicateResult.true_params and .fit.params must
    be distinct fields, never merged into one dict."""
    fit = FitResult(
        model="m3b_cd",
        params={"theta0": -1.3, "theta1": 0.05, "alpha": 0.38, "beta": 0.60},
        success=True,
        status="ok",
        loglik=-99.0,
        n_events=140,
        boundary_flags={"theta0": False, "theta1": False, "alpha": False, "beta": False},
    )
    replicate = ReplicateResult(
        scenario_id="scenario_3",
        grid_point_id="grid_0",
        replicate_id=1,
        seed=1001,
        true_params={"theta0": -1.36, "theta1": 0.1, "alpha": 0.4207, "beta": 0.6215},
        n_simulated_events=140,
        fit=fit,
    )
    assert replicate.true_params is not replicate.fit.params
    assert replicate.true_params["alpha"] != replicate.fit.params["alpha"]
    assert set(replicate.true_params) == set(replicate.fit.params)
