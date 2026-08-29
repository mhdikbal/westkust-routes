"""Model 3B recovery-tournament harness for candidates M0, M2, M3.

Implements the observation-regime pipeline (Stages 2-6) and per-candidate
Stage 1/7/8 generators+estimators specified in
docs/thesis/pilot_annotation/MODEL_3B_OBSERVATION_REGIME_SIMULATION_SPEC.md,
plus shared Stage-9 recovery metrics matching
docs/thesis/pilot_annotation/MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv.

M1 (V1's own model, run as a non-authoritative benchmark) and M4
(EXCLUDED_INSUFFICIENT_PRECISE_SUBSET, frozen researcher decision) are
NOT implemented here -- M1 already exists as model3b_cd_simulator; M4 is
excluded and not built.

Scope of this module: harness IMPLEMENTATION and smoke tests only (tiny
n, few iterations -- confirms the code runs end-to-end without crashing,
NOT a scientific result). It does NOT run the pre-registered synthetic
recovery study (real sample sizes/replication counts from
MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md) and does NOT fit any
real historical data -- both are separate, not-yet-authorized steps.
"""

from . import m0_baseline, m2_mbpp, m3_bayesian_discrete, observation_pipeline, recovery_metrics

__all__ = ["m0_baseline", "m2_mbpp", "m3_bayesian_discrete", "observation_pipeline", "recovery_metrics"]
