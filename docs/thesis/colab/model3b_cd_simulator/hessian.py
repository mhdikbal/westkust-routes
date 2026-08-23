"""Finite-difference Hessian of a scalar function, with explicit numerical
diagnostics (symmetry, positive-definiteness, condition number).

No analytic gradients exist anywhere in this package (consistent with
`estimate.py`'s style: `scipy.optimize.minimize` is always called without
`jac`), so the Hessian used for covariance estimation (`inference.py`) is
computed numerically here, via a central-difference stencil, evaluated
at a caller-supplied point (typically the MLE).

Bound-aware stepping: if a central-difference step for dimension i would
push x[i] outside [lower_bounds[i], upper_bounds[i]], that dimension
falls back to a one-sided (forward or backward) difference instead of
evaluating the function outside the feasible region. This matters in
practice: `beta_hat` can sit very close to its optimizer lower bound
(observed directly in the Fase 2B S4-G1 pilot), where a naive
symmetric step would evaluate the negative log-likelihood at an invalid
(non-positive) beta.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np

_MACHINE_EPS = np.finfo(float).eps
_STEP_EXPONENT = 0.25  # h ~ eps^(1/4), standard finite-difference Hessian heuristic
_SINGULAR_CONDITION_CEILING = 1e10
_PD_NOISE_TOLERANCE_FACTOR = 1e-6  # relative to max|eigenvalue|


@dataclass
class HessianDiagnostics:
    hessian_raw: np.ndarray
    hessian_symmetrized: np.ndarray
    symmetry_discrepancy: float
    eigenvalues: np.ndarray
    min_eigenvalue: float
    max_eigenvalue: float
    condition_number: float
    is_positive_definite: bool
    boundary_adjusted_dims: list[int]
    step_sizes: np.ndarray


def _default_step_sizes(x: np.ndarray) -> np.ndarray:
    return (_MACHINE_EPS ** _STEP_EXPONENT) * np.maximum(np.abs(x), 1.0)


def _offset_pair(
    x: np.ndarray, i: int, h: float, lower: np.ndarray | None, upper: np.ndarray | None
) -> tuple[float, float, bool]:
    """Return (offset_lo, offset_hi, boundary_adjusted) for dimension i.

    Two-sided (interior) dimension: (-h, +h), boundary_adjusted=False.
    One-sided dimension (a symmetric step would leave the feasible
    region on one side): (0, +h) or (-h, 0) -- i.e. the baseline point x
    itself is reused as one corner, and every other evaluation for this
    dimension stays on the feasible side. boundary_adjusted=True.

    This same (offset_lo, offset_hi) pair is used consistently for BOTH
    the diagonal term and every mixed-partial (off-diagonal) term
    involving dimension i, so a boundary-adjusted dimension never has
    the objective evaluated outside its feasible bound anywhere in the
    Hessian -- the earlier version of this function only protected the
    diagonal term, which let mixed-partial terms evaluate at infeasible
    points (e.g. alpha<0) whenever one dimension was at its boundary.
    """
    lo = lower[i] if lower is not None else -np.inf
    hi = upper[i] if upper is not None else np.inf
    forward_ok = (x[i] + h) <= hi
    backward_ok = (x[i] - h) >= lo
    if forward_ok and backward_ok:
        return -h, h, False
    if forward_ok and not backward_ok:
        return 0.0, h, True  # one-sided forward only
    if backward_ok and not forward_ok:
        return -h, 0.0, True  # one-sided backward only
    raise ValueError(f"dimension {i}: neither x+h nor x-h is feasible within [{lo}, {hi}] at h={h}")


def finite_difference_hessian(
    f: Callable[[np.ndarray], float],
    x: np.ndarray,
    *,
    lower_bounds: np.ndarray | None = None,
    upper_bounds: np.ndarray | None = None,
    step_sizes: np.ndarray | None = None,
) -> HessianDiagnostics:
    """Central-difference Hessian of scalar function f at point x.

    Diagonal: H[i,i] ~= (f(x+h_i) - 2f(x) + f(x-h_i)) / h_i^2
    Off-diagonal: standard 4-point mixed-partial stencil.

    When a bound would be crossed, that dimension's diagonal term falls
    back to a one-sided second-difference, and mixed partials involving
    that dimension use the feasible one-sided step in place of the
    infeasible side (documented via `boundary_adjusted_dims`).
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    h = step_sizes if step_sizes is not None else _default_step_sizes(x)

    boundary_adjusted: list[int] = []
    offset_lo = np.empty(n)
    offset_hi = np.empty(n)
    for i in range(n):
        lo_i, hi_i, adjusted = _offset_pair(x, i, h[i], lower_bounds, upper_bounds)
        offset_lo[i], offset_hi[i] = lo_i, hi_i
        if adjusted:
            boundary_adjusted.append(i)

    def evaluate(offsets: dict[int, float]) -> float:
        """f at x shifted by `offsets` (dimension -> signed shift); 0.0 shifts are free (reuse x)."""
        if not offsets or all(v == 0.0 for v in offsets.values()):
            return f0
        xi = x.copy()
        for dim, shift in offsets.items():
            xi[dim] += shift
        return f(xi)

    f0 = f(x)
    H = np.zeros((n, n))

    for i in range(n):
        if i in boundary_adjusted:
            # one-sided: f0 sits at the (feasible-side) baseline; step twice
            # further in the single feasible direction for a 3-point one-sided
            # second difference, never evaluating the infeasible side.
            s = offset_hi[i] if offset_hi[i] != 0 else offset_lo[i]
            f1 = evaluate({i: s})
            f2 = evaluate({i: 2 * s})
            H[i, i] = (f2 - 2 * f1 + f0) / (s * s)
        else:
            f_lo = evaluate({i: offset_lo[i]})
            f_hi = evaluate({i: offset_hi[i]})
            h_i = offset_hi[i]  # == -offset_lo[i] for two-sided dims
            H[i, i] = (f_hi - 2 * f0 + f_lo) / (h_i * h_i)

    for i in range(n):
        for j in range(i + 1, n):
            f_hi_hi = evaluate({i: offset_hi[i], j: offset_hi[j]})
            f_hi_lo = evaluate({i: offset_hi[i], j: offset_lo[j]})
            f_lo_hi = evaluate({i: offset_lo[i], j: offset_hi[j]})
            f_lo_lo = evaluate({i: offset_lo[i], j: offset_lo[j]})
            width_i = offset_hi[i] - offset_lo[i]
            width_j = offset_hi[j] - offset_lo[j]
            value = (f_hi_hi - f_hi_lo - f_lo_hi + f_lo_lo) / (width_i * width_j)
            H[i, j] = value
            H[j, i] = value

    symmetry_discrepancy = float(np.max(np.abs(H - H.T))) if n > 1 else 0.0
    H_sym = (H + H.T) / 2.0

    eigenvalues = np.linalg.eigvalsh(H_sym)
    min_eig = float(eigenvalues.min())
    max_eig = float(eigenvalues.max())
    condition_number = float(abs(max_eig) / abs(min_eig)) if min_eig != 0 else math.inf
    is_pd = bool(min_eig > _PD_NOISE_TOLERANCE_FACTOR * max(abs(max_eig), 1.0))

    return HessianDiagnostics(
        hessian_raw=H,
        hessian_symmetrized=H_sym,
        symmetry_discrepancy=symmetry_discrepancy,
        eigenvalues=eigenvalues,
        min_eigenvalue=min_eig,
        max_eigenvalue=max_eig,
        condition_number=condition_number,
        is_positive_definite=is_pd,
        boundary_adjusted_dims=boundary_adjusted,
        step_sizes=h,
    )
