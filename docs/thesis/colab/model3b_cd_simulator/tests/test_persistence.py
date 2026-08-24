"""Tests for persistence.py -- event_times storage, checksum, legacy
detection (never reconstructed), and instrumentation compatibility.
"""

from __future__ import annotations

import hashlib

import numpy as np
import pytest

from model3b_cd_simulator import persistence as p
from model3b_cd_simulator.density import DEFAULT_CSV_PATH, DEFAULT_WINDOW, build_x_cd_lookup, build_year_covariates, load_spec_a_density
from model3b_cd_simulator.gamma_cluster_simulator import simulate_gamma_cluster_m3b_cd
from model3b_cd_simulator.inference import fit_m1_with_inference, fit_m2_with_inference, fit_m3b_cd_with_inference
from model3b_cd_simulator.rng import make_rng
from model3b_cd_simulator.simulate import simulate_m3b_cd

T0, T1 = 1600.0, 1650.0
TRUTH = {"theta0": -1.357513, "theta1": 0.1, "alpha": 0.4207, "beta": 0.6215}


def _make_result(event_times, **overrides):
    defaults = dict(
        cell_id="TEST-CELL", replicate_id=1, base_seed=1000, replicate_seed=1001,
        simulator_commit="2ec1def", instrumentation_commit="2ec1def", density_checksum="deadbeef",
        simulation_kernel="exponential", fitted_kernel="exponential", truth_parameters=TRUTH,
        event_times=event_times, t0=T0, t1=T1,
        fit_status="ok", fit_success=True, fit_params=dict(TRUTH), fit_loglik=-42.0, runtime_seconds=0.05,
    )
    defaults.update(overrides)
    return p.make_new_replicate_result(**defaults)


# --------------------------------------------------------------------------
# 1/2/3/4. Storage, round-trip, length, ordering
# --------------------------------------------------------------------------


def test_event_times_stored_and_readable_back():
    events = np.array([1601.5, 1605.2, 1610.0])
    r = _make_result(events)
    loaded = p.load_result(p.serialize_result(r), t0=T0, t1=T1)
    assert isinstance(loaded, p.NewReplicateResult)
    assert np.array_equal(loaded.event_times, events)


def test_event_times_length_matches_n_events():
    events = np.array([1601.5, 1605.2, 1610.0, 1620.1])
    r = _make_result(events)
    assert r.n_events == 4
    assert r.event_times.size == r.n_events


def test_event_times_must_be_sorted():
    with pytest.raises(ValueError):
        p.validate_event_times(np.array([1610.0, 1601.5]), T0, T1, 2)


def test_event_times_within_window_required():
    p.validate_event_times(np.array([1600.0, 1649.999]), T0, T1, 2)  # ok, boundary-inclusive lower / exclusive upper
    with pytest.raises(ValueError):
        p.validate_event_times(np.array([1599.9]), T0, T1, 1)  # below t0
    with pytest.raises(ValueError):
        p.validate_event_times(np.array([1650.0]), T0, T1, 1)  # at/above t1 (window is [t0, t1))


# --------------------------------------------------------------------------
# 5/6. Nonfinite and out-of-window rejected
# --------------------------------------------------------------------------


def test_nonfinite_event_times_rejected():
    with pytest.raises(ValueError):
        p.validate_event_times(np.array([1601.0, np.nan]), T0, T1, 2)
    with pytest.raises(ValueError):
        p.validate_event_times(np.array([1601.0, np.inf]), T0, T1, 2)


def test_out_of_window_event_rejected_at_construction():
    with pytest.raises(ValueError):
        _make_result(np.array([1601.0, 1700.0]))  # 1700 outside [1600,1650)


# --------------------------------------------------------------------------
# 7/8. Checksum round-trip and sensitivity
# --------------------------------------------------------------------------


def test_checksum_matches_after_roundtrip():
    events = np.array([1601.5, 1605.2, 1610.0])
    r = _make_result(events)
    d = p.serialize_result(r)
    loaded = p.load_result(d, t0=T0, t1=T1)
    assert loaded.event_times_sha256 == r.event_times_sha256
    assert loaded.event_times_sha256 == p.event_times_checksum(events)


def test_single_event_change_changes_checksum():
    events_a = np.array([1601.5, 1605.2, 1610.0])
    events_b = np.array([1601.5, 1605.2, 1610.000001])
    assert p.event_times_checksum(events_a) != p.event_times_checksum(events_b)


def test_tampered_checksum_detected_on_load():
    events = np.array([1601.5, 1605.2, 1610.0])
    r = _make_result(events)
    d = p.serialize_result(r)
    d["event_times_sha256"] = "0" * 64  # tampered
    with pytest.raises(ValueError, match="checksum mismatch"):
        p.load_result(d, t0=T0, t1=T1)


# --------------------------------------------------------------------------
# 9/10. Legacy detection, no reconstruction
# --------------------------------------------------------------------------


def test_legacy_output_recognized_as_missing_event_sequence():
    legacy_record = {
        "replicate_id": 1, "seed": 20260824, "n_events": 133, "fit_status": "ok",
        "fit_success": True, "fit_params": {"theta0": -1.0}, "fit_loglik": -100.0,
    }
    result = p.load_result(legacy_record)
    assert isinstance(result, p.LegacyReplicateResult)
    assert result.status == p.MISSING_EVENT_SEQUENCE_STATUS
    assert result.result_kind == p.RESULT_KIND_LEGACY


def test_legacy_output_not_reconstructed():
    """A legacy record with a `seed` present must NOT have event_times
    silently derived from it -- LegacyReplicateResult carries no
    event_times attribute at all."""
    legacy_record = {"seed": 20260824, "n_events": 5, "fit_params": {}}
    result = p.load_result(legacy_record)
    assert not hasattr(result, "event_times")
    assert result.raw == legacy_record  # untouched, exactly as read


# --------------------------------------------------------------------------
# 11/12. Seed/provenance stored; truth separate from fitted params
# --------------------------------------------------------------------------


def test_seed_and_provenance_stored():
    r = _make_result(np.array([1601.0, 1602.0]))
    d = p.serialize_result(r)
    for key in ("base_seed", "replicate_seed", "simulator_commit", "instrumentation_commit", "density_checksum"):
        assert key in d


def test_truth_parameters_separate_from_fit_params():
    r = _make_result(np.array([1601.0, 1602.0]), fit_params={"theta0": -9.9, "theta1": 9.9, "alpha": 9.9, "beta": 9.9})
    assert r.truth_parameters != r.fit_params
    assert r.truth_parameters is not r.fit_params


# --------------------------------------------------------------------------
# 13/14. Exponential and Gamma-cluster simulator outputs both valid
# --------------------------------------------------------------------------


def test_exponential_simulator_output_valid():
    events = simulate_m3b_cd(TRUTH["theta0"], TRUTH["theta1"], TRUTH["alpha"], TRUTH["beta"], lambda t: 0.0, T0, T1, make_rng(42))
    r = _make_result(events, simulation_kernel="exponential")
    assert r.event_times.size == events.size
    assert r.simulation_kernel == "exponential"


def test_gamma_cluster_simulator_output_valid():
    events = simulate_gamma_cluster_m3b_cd(
        TRUTH["theta0"], TRUTH["theta1"], 0.6769, 2.0, 2.38095, lambda t: 0.0, T0, T1, make_rng(7)
    )
    r = _make_result(events, simulation_kernel="gamma", fitted_kernel="exponential")
    assert r.event_times.size == events.size
    assert r.simulation_kernel == "gamma"


# --------------------------------------------------------------------------
# 15. Density checksum unchanged by this module
# --------------------------------------------------------------------------


def test_density_source_untouched_by_persistence_module():
    before = hashlib.sha256(DEFAULT_CSV_PATH.read_bytes()).hexdigest()
    events = simulate_m3b_cd(TRUTH["theta0"], TRUTH["theta1"], TRUTH["alpha"], TRUTH["beta"], lambda t: 0.0, T0, T1, make_rng(1))
    _make_result(events)
    after = hashlib.sha256(DEFAULT_CSV_PATH.read_bytes()).hexdigest()
    assert before == after


# --------------------------------------------------------------------------
# 16. Instrumentation can read event sequence from a round trip
# --------------------------------------------------------------------------


def test_instrumentation_reads_roundtripped_event_sequence():
    series = load_spec_a_density(window=DEFAULT_WINDOW)
    x_cd = build_x_cd_lookup(series)
    year_covariates = build_year_covariates(series)
    t0, t1 = float(DEFAULT_WINDOW[0]), float(DEFAULT_WINDOW[1])

    events = simulate_m3b_cd(TRUTH["theta0"], TRUTH["theta1"], TRUTH["alpha"], TRUTH["beta"], x_cd, t0, t1, make_rng(99))
    d = p.serialize_result(p.make_new_replicate_result(
        cell_id="TEST", replicate_id=1, base_seed=1, replicate_seed=2, simulator_commit="c", instrumentation_commit="c",
        density_checksum="x", simulation_kernel="exponential", fitted_kernel="exponential", truth_parameters=TRUTH,
        event_times=events, t0=t0, t1=t1, fit_status="ok", fit_success=True, fit_params=TRUTH, fit_loglik=0.0, runtime_seconds=0.1,
    ))
    loaded = p.load_result(d, t0=t0, t1=t1)

    report = fit_m3b_cd_with_inference(loaded.event_times, year_covariates, t0, t1)
    assert report.fit.status in ("ok", "optimizer_failed", "invalid")
    assert report.covariance.status in ("valid", "regularized", "singular", "non_positive_definite", "unavailable")


# --------------------------------------------------------------------------
# 17. Structured failure status preserved in the schema
# --------------------------------------------------------------------------


def test_structured_failure_status_preserved():
    r = _make_result(np.array([1601.0]), fit_status="optimizer_failed", fit_success=False)
    d = p.serialize_result(r)
    loaded = p.load_result(d, t0=T0, t1=T1)
    assert loaded.fit_status == "optimizer_failed"
    assert loaded.fit_success is False
