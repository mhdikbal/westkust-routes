"""Deterministic RNG helper. All stochastic draws in this package MUST route
through `make_rng` so replicate results are reproducible from a seed alone
(plan §9 replicate design; unit test requirement #1/#2)."""

from __future__ import annotations

import numpy as np


def make_rng(seed: int) -> np.random.Generator:
    if not isinstance(seed, (int, np.integer)) or isinstance(seed, bool):
        raise TypeError(f"seed must be an int for reproducibility, got {type(seed)}")
    return np.random.default_rng(seed)
