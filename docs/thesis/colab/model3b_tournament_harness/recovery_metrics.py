"""Shared Stage-9 recovery-metric implementations, matching every metric
named in docs/thesis/pilot_annotation/MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv.

Reuses model3b_cd_simulator/metrics.py's definitions verbatim (bias, rmse,
normalized_absolute_bias, absolute_relative_bias, branching_ratio_bias,
sign_recovery_rate, false_positive_excitation_rate, ci_coverage_rate,
convergence_rate, invalid_estimate_rate) rather than reimplementing them --
those are the SAME metrics under the SAME names in the gate spec, and V1's
own smoke-tested implementation is the one source of truth. This module
adds only the metrics the gate spec requires that V1's metrics.py does not
already have: false_negative_excitation_rate, boundary_solution_rate,
held_out_predictive_score, source_removal_stability,
episode_removal_stability, calibration.

NOTE (same discipline as V1's metrics.py): these functions compute metric
VALUES from whatever estimates/replicates they are given. They do NOT
themselves decide PASS/FAIL against MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv's
thresholds, and must not be used to declare a tournament result until the
pre-registered recovery study (a separate, not-yet-authorized execution
step) has actually been run.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model3b_cd_simulator.metrics import (  # noqa: E402
    absolute_relative_bias,
    bias,
    branching_ratio_bias,
    ci_coverage_rate,
    convergence_rate,
    false_positive_excitation_rate,
    invalid_estimate_rate,
    normalized_absolute_bias,
    normalized_rmse,
    rmse,
    sign_recovery_rate,
)

__all__ = [
    "absolute_relative_bias", "bias", "branching_ratio_bias", "ci_coverage_rate",
    "convergence_rate", "false_positive_excitation_rate", "invalid_estimate_rate",
    "normalized_absolute_bias", "normalized_rmse", "rmse", "sign_recovery_rate",
    "false_negative_excitation_rate", "boundary_solution_rate",
    "held_out_predictive_score", "source_removal_stability",
    "episode_removal_stability", "calibration_pit",
]


def false_negative_excitation_rate(alpha_true_positive_flags_not_flagged_significant: np.ndarray) -> float:
    """GATE-*36/50/57: proportion of alpha_true>0 replicates where the
    estimator FAILS to flag alpha as significant (the mirror image of
    false_positive_excitation_rate, which covers alpha_true=0 cells).
    Input: boolean array, True where alpha_true>0 but was NOT flagged
    significant (i.e. a missed real excitation signal)."""
    flags = np.asarray(alpha_true_positive_flags_not_flagged_significant, dtype=bool)
    return float(np.mean(flags))


def boundary_solution_rate(boundary_flags: np.ndarray) -> float:
    """GATE-*38/38/59: fraction of replicates whose fit landed on (or
    within tolerance of) a parameter-space boundary. For frequentist
    candidates (M0, M2) this is `FitResult.any_boundary_flag` across
    replicates. For M3 (Bayesian), per GATE-038's own notes, 'boundary'
    is reinterpreted as posterior mass concentrated at the prior's edge
    (n approaching 1, or beta approaching the prior's bounds) -- callers
    pass the appropriately-reinterpreted boolean array either way; this
    function itself is agnostic to which definition produced the flags."""
    flags = np.asarray(boundary_flags, dtype=bool)
    return float(np.mean(flags))


def held_out_predictive_score(loglik_held_out: np.ndarray) -> float:
    """GATE-*39/53/60: mean held-out log-likelihood across replicates, on
    a temporal train/test split WITHIN each synthetic replicate (e.g.
    final 20% of the observation window) -- never a real-data split.
    Gate direction is `relative_to_M0`: the CALLER is responsible for
    comparing this candidate's score against M0's own score at matched
    settings; this function only computes the raw per-candidate value."""
    vals = np.asarray(loglik_held_out, dtype=float)
    finite = vals[np.isfinite(vals)]
    if finite.size == 0:
        return float("nan")
    return float(np.mean(finite))


def source_removal_stability(
    full_fit_params: dict[str, float],
    leave_one_source_out_params: list[dict[str, float]],
) -> float:
    """GATE-*40/54/61: max relative parameter-estimate shift across all
    leave-one-(synthetic)-source-out refits, relative to the full-data
    fit. <=0.20 is the gate threshold (checked by the caller against the
    gate spec, not here)."""
    shifts = []
    for loo_params in leave_one_source_out_params:
        for name, full_val in full_fit_params.items():
            loo_val = loo_params.get(name)
            if loo_val is None or not np.isfinite(full_val) or full_val == 0:
                continue
            shifts.append(abs(loo_val - full_val) / abs(full_val))
    if not shifts:
        return float("nan")
    return float(np.max(shifts))


def episode_removal_stability(
    full_fit_params: dict[str, float],
    leave_one_episode_out_params: list[dict[str, float]],
) -> float:
    """GATE-*41/55/62: identical construction to source_removal_stability,
    but over leave-one-episode-out refits. N/A (return NaN, per the gate
    spec's own notes) under the flat (no-episode) synthetic regime --
    callers should not invoke this for flat-regime replicates at all."""
    return source_removal_stability(full_fit_params, leave_one_episode_out_params)


def calibration_pit(pit_values: np.ndarray, n_deciles: int = 10) -> float:
    """GATE-*42/56/63: max absolute deviation of the PIT (probability
    integral transform) histogram from the nominal uniform decile
    frequency (1/n_deciles each). <=0.05 is the gate threshold (checked
    by the caller). `pit_values` are the per-replicate/per-held-out-point
    PIT values in [0,1] -- for frequentist candidates (M0, M2), computed
    via a parametric-bootstrap or asymptotic-approximation PIT check per
    GATE-042's own notes; for M3 (Bayesian), via posterior-predictive PIT.
    This function only aggregates already-computed PIT values into the
    calibration statistic; it does not compute PIT itself, since that
    computation is candidate-specific."""
    pit_values = np.asarray(pit_values, dtype=float)
    pit_values = pit_values[np.isfinite(pit_values)]
    if pit_values.size == 0:
        return float("nan")
    edges = np.linspace(0.0, 1.0, n_deciles + 1)
    observed_freq, _ = np.histogram(pit_values, bins=edges)
    observed_freq = observed_freq / pit_values.size
    nominal_freq = 1.0 / n_deciles
    return float(np.max(np.abs(observed_freq - nominal_freq)))
