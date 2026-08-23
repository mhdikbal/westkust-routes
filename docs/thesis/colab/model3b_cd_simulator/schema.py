"""Result schemas.

Kept small and explicit so recovery metrics never rely on an implicit
shape: `FitResult.status` distinguishes a converged, valid fit ("ok")
from an optimizer failure ("optimizer_failed") from a fit that converged
but produced a nonfinite/invalid estimate ("invalid") — plan §9 Gate A.
`ReplicateResult.true_params` and `.fit` are kept as separate fields so
simulation ground truth is never confused with an estimate (plan §9
guard: "simulation truth dipisahkan dari estimate").
"""

from __future__ import annotations

from dataclasses import dataclass, field

VALID_STATUSES = ("ok", "optimizer_failed", "invalid")


@dataclass
class FitResult:
    model: str
    params: dict[str, float]
    success: bool
    status: str
    loglik: float
    n_events: int
    boundary_flags: dict[str, bool]
    optimizer_message: str = ""

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}, got {self.status!r}")

    @property
    def is_valid(self) -> bool:
        return self.status == "ok"

    @property
    def any_boundary_flag(self) -> bool:
        return any(self.boundary_flags.values())


@dataclass
class ReplicateResult:
    scenario_id: str
    grid_point_id: str
    replicate_id: int
    seed: int
    true_params: dict[str, float]
    n_simulated_events: int
    fit: FitResult
    metrics: dict[str, float] = field(default_factory=dict)
