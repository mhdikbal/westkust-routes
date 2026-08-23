"""Recovery metrics matching the frozen §9 gate definitions in
docs/thesis/pilot_annotation/MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md.

NOTE (Fase 1 scope): these functions compute metrics from whatever
estimates they are given. They do NOT decide PASS/FAIL against the §9
thresholds, and this module must not be used to declare simulation
recovery results until the pilot (100/cell) and final (1000/cell)
replicate runs described in the plan have actually been executed.
"""

from __future__ import annotations

import numpy as np


def bias(estimates: np.ndarray, true_value: float) -> float:
    estimates = np.asarray(estimates, dtype=float)
    return float(np.mean(estimates) - true_value)


def rmse(estimates: np.ndarray, true_value: float) -> float:
    estimates = np.asarray(estimates, dtype=float)
    return float(np.sqrt(np.mean((estimates - true_value) ** 2)))


def normalized_rmse(estimates: np.ndarray, true_value: float) -> float:
    """§9 Gate D: normalized RMSE <= 0.20."""
    denom = abs(true_value) if true_value != 0 else 1.0
    return rmse(estimates, true_value) / denom


def absolute_relative_bias(estimates: np.ndarray, true_value: float) -> float:
    """§9 Gate B: |mean(estimate) - true| / |true|, for theta1/alpha/beta (theta0 excluded — see normalized_absolute_bias)."""
    if true_value == 0:
        raise ValueError("relative bias undefined for true_value == 0; use normalized_absolute_bias for theta0")
    return abs(bias(estimates, true_value)) / abs(true_value)


def normalized_absolute_bias(estimates: np.ndarray, true_value: float, scale: float | None = None) -> float:
    """§9 Gate B: theta0 uses normalized absolute bias (<= 0.25), not relative
    bias, because theta0 can be near zero and relative bias is undefined
    there. `scale` defaults to max(|true_value|, 1.0)."""
    denom = scale if scale is not None else max(abs(true_value), 1.0)
    return abs(bias(estimates, true_value)) / denom


def branching_ratio_bias(alpha_estimates: np.ndarray, beta_estimates: np.ndarray, true_alpha: float, true_beta: float) -> tuple[float, float]:
    """§9 Gate B: branching-ratio absolute bias <= 0.05 AND relative bias <= 0.10."""
    alpha_estimates = np.asarray(alpha_estimates, dtype=float)
    beta_estimates = np.asarray(beta_estimates, dtype=float)
    br_true = true_alpha / true_beta
    br_est = alpha_estimates / beta_estimates
    absolute_bias = float(np.mean(br_est) - br_true)
    relative_bias = abs(absolute_bias) / abs(br_true) if br_true != 0 else float("nan")
    return absolute_bias, relative_bias


def sign_recovery_rate(estimates: np.ndarray, true_value: float) -> float:
    """§9 Gate B: sign recovery >= 0.95."""
    estimates = np.asarray(estimates, dtype=float)
    if true_value == 0:
        raise ValueError("sign recovery undefined for true_value == 0")
    return float(np.mean(np.sign(estimates) == np.sign(true_value)))


def false_positive_excitation_rate(alpha_significant_flags: np.ndarray) -> float:
    """§9 Gate B: proportion of alpha_true=0 replicates where alpha is
    (falsely) flagged significant. The significance test itself (LR-test,
    CI-based, etc.) is decided at pilot/final implementation stage (plan
    §8 poin 3) — this only aggregates pre-computed boolean flags."""
    flags = np.asarray(alpha_significant_flags, dtype=bool)
    return float(np.mean(flags))


def ci_coverage_rate(covered_flags: np.ndarray) -> float:
    """§9 Gate B: nominal 95% CI coverage empirik in [0.925, 0.975]."""
    flags = np.asarray(covered_flags, dtype=bool)
    return float(np.mean(flags))


def convergence_rate(success_flags: np.ndarray) -> float:
    """§9 Gate A: convergence rate PASS >= 0.95, FAIL < 0.90."""
    flags = np.asarray(success_flags, dtype=bool)
    return float(np.mean(flags))


def invalid_estimate_rate(invalid_flags: np.ndarray) -> float:
    """§9 Gate A: invalid estimate rate <= 0.05."""
    flags = np.asarray(invalid_flags, dtype=bool)
    return float(np.mean(flags))
