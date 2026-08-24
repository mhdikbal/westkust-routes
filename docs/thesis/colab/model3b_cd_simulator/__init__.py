"""Model 3B-CD simulation/recovery framework (Fase 1 skeleton).

Implements the M1 / M2 / M3B-CD simulators, exponential Hawkes kernel,
MLE estimators, and recovery metrics specified in
docs/thesis/pilot_annotation/MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md.

Scope of this module (Fase 1): framework + unit tests + one 2-replicate
smoke test. It does NOT run the pilot (100 replicates/cell) or final
(1000 replicates/cell) study, and does NOT fit real linimasa_events.
"""

from . import (
    density,
    estimate,
    gamma_cluster_simulator,
    hessian,
    inference,
    kernel,
    likelihood,
    logging_utils,
    metrics,
    persistence,
    rng,
    schema,
    simulate,
    validation,
)

__all__ = [
    "density",
    "estimate",
    "gamma_cluster_simulator",
    "hessian",
    "inference",
    "kernel",
    "likelihood",
    "logging_utils",
    "metrics",
    "persistence",
    "rng",
    "schema",
    "simulate",
    "validation",
]
