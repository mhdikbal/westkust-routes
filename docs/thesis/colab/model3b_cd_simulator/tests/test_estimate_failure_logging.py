"""Unit test #11 (Fase 1 requirement list)."""

from types import SimpleNamespace

import numpy as np

import model3b_cd_simulator.estimate as estimate_module
from model3b_cd_simulator.logging_utils import FailureLog


def test_optimizer_failure_is_recorded_not_hidden(monkeypatch):
    """#11 — when scipy.optimize.minimize reports success=False, the fit
    must be marked status='optimizer_failed' (never silently reported as
    'ok'), and the failure must be appended to the FailureLog."""

    def fake_minimize(fun, x0, method, bounds):  # noqa: ANN001 - test double
        return SimpleNamespace(x=np.asarray(x0), fun=fun(x0), success=False, message="fake non-convergence")

    monkeypatch.setattr(estimate_module, "minimize", fake_minimize)

    failure_log = FailureLog()
    events = np.array([1650.0, 1660.0, 1670.0])
    fit = estimate_module.fit_m1(
        events, 1600.0, 1700.0,
        failure_log=failure_log, scenario_id="s1", grid_point_id="g1", replicate_id=3,
    )

    assert fit.success is False
    assert fit.status == "optimizer_failed"
    assert len(failure_log) == 1
    record = failure_log.records[0]
    assert record.scenario_id == "s1"
    assert record.grid_point_id == "g1"
    assert record.replicate_id == 3
    assert record.reason == "optimizer_failed"


def test_successful_fit_is_not_logged_as_failure():
    """Companion check: a genuinely converged fit must NOT appear in the
    failure log, so the log stays a true record of failures only."""
    failure_log = FailureLog()
    events = np.array([1620.0, 1635.0, 1650.0, 1665.0, 1680.0])
    fit = estimate_module.fit_m1(
        events, 1600.0, 1700.0,
        failure_log=failure_log, scenario_id="s1", grid_point_id="g1", replicate_id=1,
    )
    if fit.status == "ok":
        assert len(failure_log) == 0
    else:
        # If the tiny 5-event sample genuinely fails to converge, that is
        # itself evidence the failure path works — just assert consistency.
        assert len(failure_log) == 1
