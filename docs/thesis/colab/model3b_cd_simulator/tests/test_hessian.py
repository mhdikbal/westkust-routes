"""Tests for hessian.py -- finite-difference Hessian + diagnostics.

All fixtures are hardcoded (no simulate_* calls anywhere in this file).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from model3b_cd_simulator.hessian import finite_difference_hessian

# --------------------------------------------------------------------------
# Simple closed-form quadratic: f(x,y) = a*x^2 + b*y^2 + c*x*y
# Hessian is exactly [[2a, c], [c, 2b]] everywhere -- independent of the
# Hawkes/point-process framework entirely, a clean ground-truth check.
# --------------------------------------------------------------------------

A, B, C = 3.0, 5.0, 1.5


def _quadratic(v: np.ndarray) -> float:
    x, y = v
    return A * x**2 + B * y**2 + C * x * y


def test_hessian_matches_analytic_on_simple_quadratic():
    diag = finite_difference_hessian(_quadratic, np.array([1.3, -0.7]))
    analytic = np.array([[2 * A, C], [C, 2 * B]])
    discrepancy = float(np.max(np.abs(diag.hessian_symmetrized - analytic)))
    assert discrepancy < 1e-4, f"discrepancy={discrepancy}"


def test_hessian_symmetric_within_tolerance():
    diag = finite_difference_hessian(_quadratic, np.array([2.0, 3.0]))
    assert diag.symmetry_discrepancy < 1e-6


def test_covariance_finite_at_interior_solution():
    """A well-conditioned interior quadratic minimum: eigenvalues finite,
    positive, condition number finite."""
    diag = finite_difference_hessian(_quadratic, np.array([0.0, 0.0]))
    assert np.all(np.isfinite(diag.eigenvalues))
    assert diag.is_positive_definite
    assert diag.min_eigenvalue > 0
    assert math.isfinite(diag.condition_number)


def test_singular_hessian_is_reported_not_hidden():
    """f(x,y) = x^2 (no y-dependence at all): rank-deficient Hessian
    [[2,0],[0,0]] -- min eigenvalue exactly 0, must NOT be reported as
    positive-definite."""

    def rank_deficient(v: np.ndarray) -> float:
        x, y = v
        return x**2

    diag = finite_difference_hessian(rank_deficient, np.array([0.5, 0.5]))
    assert diag.min_eigenvalue <= 1e-6
    assert not diag.is_positive_definite


def test_boundary_adjusted_one_sided_stepping_near_lower_bound():
    """A dimension pinned at its lower bound must use a one-sided step
    (no evaluation below the bound), and this must be reflected in
    boundary_adjusted_dims."""

    def f(v: np.ndarray) -> float:
        x, y = v
        if x < 0:
            raise ValueError("infeasible: x < 0")
        return A * x**2 + B * y**2 + C * x * y

    diag = finite_difference_hessian(
        f, np.array([0.0, 1.0]), lower_bounds=np.array([0.0, -np.inf]), upper_bounds=np.array([np.inf, np.inf])
    )
    assert 0 in diag.boundary_adjusted_dims
    assert 1 not in diag.boundary_adjusted_dims
    assert np.all(np.isfinite(diag.hessian_raw))


def test_boundary_adjusted_mixed_partial_never_evaluates_infeasible_point():
    """Regression test for the bug found during Fase 3A implementation:
    the FIRST version of this module only made the diagonal term
    bound-aware, letting mixed-partial (off-diagonal) terms evaluate the
    objective at an infeasible point (e.g. x<0) whenever one dimension
    was boundary-adjusted -- producing inf/nan and a Hessian whose
    eigenvalues failed to converge. This must no longer happen."""

    def f(v: np.ndarray) -> float:
        x, y = v
        if x < 0:
            raise ValueError("infeasible: x < 0")
        return A * x**2 + B * y**2 + C * x * y

    diag = finite_difference_hessian(
        f, np.array([0.0, 1.0]), lower_bounds=np.array([0.0, -np.inf]), upper_bounds=np.array([np.inf, np.inf])
    )
    assert np.all(np.isfinite(diag.hessian_raw))
    assert np.all(np.isfinite(diag.eigenvalues))


def test_infeasible_starting_point_raises():
    def f(v: np.ndarray) -> float:
        return float(v[0] ** 2)

    with pytest.raises(ValueError):
        finite_difference_hessian(f, np.array([1e-10]), lower_bounds=np.array([0.0]), upper_bounds=np.array([1e-11]))
