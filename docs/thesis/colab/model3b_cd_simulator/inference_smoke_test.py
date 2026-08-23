"""One deterministic instrumentation smoke test: ONE hardcoded synthetic
event sequence, fit M1, M2, M3B-CD via the *_with_inference functions,
confirm every instrumentation field is present and well-formed.

No simulate_* call anywhere in this module. Mirrors Fase 1's
smoke_test.py pattern (standalone runnable + pytest wrapper).

This ONLY verifies the instrumentation pipeline runs end-to-end. Its
output must NOT be used to assess any plan §9 decision gate, evaluate
recovery, or authorize real-data fitting.

Run directly: python inference_smoke_test.py
"""

from __future__ import annotations

import json

import numpy as np

from .density import DEFAULT_WINDOW
from . import inference as inf

T0, T1 = float(DEFAULT_WINDOW[0]), float(DEFAULT_WINDOW[1])
YEAR_COVARIATES = {y: 0.05 * ((y - 1600) % 7) for y in range(1600, 1784)}

# One hardcoded, moderately clustered synthetic sequence (not from simulate_*).
SMOKE_EVENTS = np.array([
    1601.5, 1601.7, 1601.9, 1602.3, 1603.1, 1603.4, 1605.9, 1606.1, 1606.3, 1608.1,
    1608.3, 1610.4, 1610.6, 1610.8, 1615.3, 1615.5, 1620.7, 1620.9, 1622.1, 1625.0,
])


def _report_to_dict(report: inf.ModelFitReport) -> dict:
    return {
        "model": report.model,
        "params": report.fit.params,
        "fit_status": report.fit.status,
        "loglik": report.fit.loglik,
        "n_params": len(report.param_names),
        "n_bic": report.n_bic,
        "covariance_status": report.covariance.status,
        "standard_errors": report.standard_errors,
        "wald_ci_95": {k: list(v) for k, v in report.wald_ci_95.items()},
        "aic": report.aic,
        "bic": report.bic,
        "boundary_alpha_test": (
            {
                # restricted/unrestricted model names printed explicitly so this
                # label can never silently drift (e.g. m1's own test uses a
                # closed-form homogeneous-Poisson restricted model, NOT m2 --
                # only m3b_cd's test is genuinely "m2 vs m3b_cd").
                "restricted_model": report.boundary_alpha_test.restricted_model,
                "unrestricted_model": report.boundary_alpha_test.unrestricted_model,
                "loglik_restricted": report.boundary_alpha_test.loglik_restricted,
                "loglik_unrestricted": report.boundary_alpha_test.loglik_unrestricted,
                "lr": report.boundary_alpha_test.test_statistic_lr,
                "p_value": report.boundary_alpha_test.p_value,
                "decision": report.boundary_alpha_test.decision_alpha_0p05,
            }
            if report.boundary_alpha_test is not None else None
        ),
        "branching_ratio": (
            {
                "estimate": report.branching_ratio.branching_ratio,
                "se": report.branching_ratio.branching_ratio_standard_error,
                "ci_95": (
                    list(report.branching_ratio.branching_ratio_ci_95)
                    if isinstance(report.branching_ratio.branching_ratio_ci_95, tuple) else report.branching_ratio.branching_ratio_ci_95
                ),
                "status": report.branching_ratio.delta_method_status,
            }
            if report.branching_ratio is not None else None
        ),
    }


def run_smoke_test() -> dict:
    r_m1 = inf.fit_m1_with_inference(SMOKE_EVENTS, T0, T1)
    r_m2 = inf.fit_m2_with_inference(SMOKE_EVENTS, YEAR_COVARIATES, T0, T1)
    r_m3b = inf.fit_m3b_cd_with_inference(SMOKE_EVENTS, YEAR_COVARIATES, T0, T1)
    selection = inf.select_best_model({"m1": r_m1, "m2": r_m2, "m3b_cd": r_m3b})

    return {
        "n_events": int(SMOKE_EVENTS.size),
        "models": {"m1": _report_to_dict(r_m1), "m2": _report_to_dict(r_m2), "m3b_cd": _report_to_dict(r_m3b)},
        "model_selection": {
            "best_model_by_AIC": selection.best_model_by_AIC,
            "best_model_by_BIC": selection.best_model_by_BIC,
            "delta_AIC": selection.delta_AIC,
            "delta_BIC": selection.delta_BIC,
            "caveat": selection.caveat,
        },
        "gate_evaluation_performed": False,
    }


if __name__ == "__main__":
    result = run_smoke_test()
    print(json.dumps(result, indent=2, default=str))
