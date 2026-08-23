"""The one deterministic smoke test: 1 scenario, 1 grid point, 2 replicates.

Verifies pipeline end-to-end only. Must NOT be used to evaluate the §9
decision gates, and asserts nothing about gate PASS/FAIL.
"""

from model3b_cd_simulator.schema import ReplicateResult
from model3b_cd_simulator.smoke_test import run_smoke_test


def test_smoke_pipeline_two_replicates_end_to_end():
    result = run_smoke_test()

    assert result["n_scenarios"] == 1
    assert result["n_grid_points"] == 1
    assert result["n_replicates"] == 2
    assert result["gate_evaluation_performed"] is False
    assert result["source_density_unchanged"] is True

    replicate_results = result["replicate_results"]
    assert len(replicate_results) == 2
    for rr in replicate_results:
        assert isinstance(rr, ReplicateResult)
        assert rr.fit.status in ("ok", "optimizer_failed", "invalid")
        assert rr.n_simulated_events >= 0
        assert set(rr.true_params) == {"theta0", "theta1", "alpha", "beta"}
