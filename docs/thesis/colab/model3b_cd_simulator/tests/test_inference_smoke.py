"""The one instrumentation smoke test, run via pytest. See
inference_smoke_test.py for the standalone-runnable version and the
"not used for gate evaluation" disclaimer.
"""

from model3b_cd_simulator.inference_smoke_test import run_smoke_test


def test_instrumentation_smoke_all_three_models_complete():
    result = run_smoke_test()
    assert result["gate_evaluation_performed"] is False
    assert set(result["models"]) == {"m1", "m2", "m3b_cd"}
    for name, m in result["models"].items():
        assert m["fit_status"] in ("ok", "optimizer_failed", "invalid")
        assert m["covariance_status"] in ("valid", "regularized", "singular", "non_positive_definite", "unavailable")
        assert isinstance(m["aic"], float)
        assert isinstance(m["bic"], float)
        assert "standard_errors" in m and "wald_ci_95" in m
    assert result["model_selection"]["best_model_by_AIC"] in {"m1", "m2", "m3b_cd"}
    assert result["model_selection"]["best_model_by_BIC"] in {"m1", "m2", "m3b_cd"}
