"""Unit tests #8, #9 (Fase 1 requirement list)."""

import math

import pytest

from model3b_cd_simulator.validation import (
    branching_ratio,
    validate_alpha,
    validate_beta,
    validate_density_params,
    validate_intensity,
    validate_mu,
    validate_window,
)


def test_branching_ratio_calculation():
    """#8 — branching ratio must equal alpha/beta, matching production Model 3
    (alpha=0.4207, beta=0.6215 -> ~0.677, plan §0)."""
    assert math.isclose(branching_ratio(0.4207, 0.6215), 0.4207 / 0.6215, rel_tol=1e-12)
    assert branching_ratio(0.0, 1.0) == 0.0


@pytest.mark.parametrize(
    "fn, bad_args",
    [
        (validate_mu, (0.0,)),
        (validate_mu, (-1.0,)),
        (validate_mu, (math.inf,)),
        (validate_alpha, (-0.01,)),
        (validate_alpha, (math.nan,)),
        (validate_beta, (0.0,)),
        (validate_beta, (-1.0,)),
        (validate_window, (1700.0, 1600.0)),
        (validate_window, (1600.0, 1600.0)),
        (validate_intensity, (-0.5,)),
        (validate_intensity, (math.inf,)),
        (validate_intensity, (math.nan,)),
    ],
)
def test_invalid_parameter_rejection(fn, bad_args):
    """#9 — invalid parameters must raise, never be silently accepted."""
    with pytest.raises(ValueError):
        fn(*bad_args)


def test_valid_density_params_accepted():
    validate_density_params(0.0, 0.0)  # must not raise
    with pytest.raises(ValueError):
        validate_density_params(math.nan, 0.0)
