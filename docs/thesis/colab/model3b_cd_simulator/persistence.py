"""Replicate-result persistence with explicit event_times storage.

This module exists because the earlier Pilot 100 output
(`data/model3b_working/pilot_100/`) recorded only point estimates and
event *counts* (`n_events`), never the event *times* themselves —
making the Fase 3A statistical instrumentation (`hessian.py`,
`inference.py`) impossible to apply to it legitimately (see
`docs/thesis/pilot_annotation/MODEL_3B_CD_INSTRUMENTATION_PILOT_BLOCKER.md`).
Every function here either (a) constructs/validates a "new-format"
result that always carries `event_times`, or (b) reads a result back
and explicitly classifies it as `new_result_with_event_times` or
`legacy_result_without_event_times` — never silently reconstructing
missing data.

This module does not run any simulation or fit itself; callers (a
future pilot driver) supply an already-simulated `event_times` array
and an already-computed fit.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from .density import DEFAULT_WINDOW

RESULT_KIND_NEW = "new_result_with_event_times"
RESULT_KIND_LEGACY = "legacy_result_without_event_times"
MISSING_EVENT_SEQUENCE_STATUS = "MISSING_EVENT_SEQUENCE"


# --------------------------------------------------------------------------
# event_times validation and checksum
# --------------------------------------------------------------------------


def validate_event_times(event_times: Any, t0: float, t1: float, n_events: int) -> np.ndarray:
    """Enforce every rule required of a persisted event_times array:
    explicit numeric array, ascending order, all values in [t0, t1),
    length == n_events, all finite. Returns the validated float64 array
    (no destructive rounding -- values pass through as float64, the same
    precision the simulator and likelihood functions already use).
    """
    arr = np.asarray(event_times, dtype=np.float64)
    if arr.ndim != 1:
        raise ValueError(f"event_times must be 1-D, got shape {arr.shape}")
    if arr.size != n_events:
        raise ValueError(f"len(event_times)={arr.size} does not match n_events={n_events}")
    if arr.size and not np.all(np.isfinite(arr)):
        raise ValueError("event_times contains nonfinite value(s)")
    if arr.size > 1 and not np.all(np.diff(arr) >= 0):
        raise ValueError("event_times is not sorted ascending")
    if arr.size and (arr.min() < t0 or arr.max() >= t1):
        raise ValueError(f"event_times contains value(s) outside window [{t0}, {t1}): min={arr.min()}, max={arr.max()}")
    return arr


def event_times_checksum(event_times: Any) -> str:
    """Canonical checksum: event_times cast to little-endian float64
    (platform-independent byte order, not just 'native'), then SHA-256
    of the raw bytes. Documented explicitly so a round-trip check is
    reproducible across machines, not just within one process."""
    arr = np.asarray(event_times, dtype=np.float64).astype("<f8", copy=False)
    return hashlib.sha256(arr.tobytes()).hexdigest()


# --------------------------------------------------------------------------
# Result dataclasses
# --------------------------------------------------------------------------


@dataclass
class NewReplicateResult:
    """A replicate result that always carries its event_times. Truth
    parameters (`truth_parameters`) and fitted parameters (`fit_params`)
    are kept as separate fields -- never merged -- matching the
    simulation-truth-vs-estimate guard already enforced in schema.py's
    ReplicateResult (Fase 1)."""

    cell_id: str
    replicate_id: int
    base_seed: int
    replicate_seed: int
    simulator_commit: str
    instrumentation_commit: str
    density_checksum: str
    simulation_kernel: str
    fitted_kernel: str
    truth_parameters: dict[str, float]
    event_times: np.ndarray
    n_events: int
    fit_status: str
    fit_success: bool
    fit_params: dict[str, float]
    fit_loglik: float
    runtime_seconds: float
    event_times_sha256: str
    result_kind: str = RESULT_KIND_NEW

    def __post_init__(self) -> None:
        if self.result_kind != RESULT_KIND_NEW:
            raise ValueError(f"result_kind must be {RESULT_KIND_NEW!r}, got {self.result_kind!r}")


@dataclass
class LegacyReplicateResult:
    """A result read back that has no event_times field at all (e.g. any
    record from data/model3b_working/pilot_100/). Carries the raw dict
    for inspection but deliberately exposes NO event_times attribute and
    performs NO reconstruction."""

    raw: dict[str, Any]
    status: str = MISSING_EVENT_SEQUENCE_STATUS
    result_kind: str = RESULT_KIND_LEGACY

    def __post_init__(self) -> None:
        if self.result_kind != RESULT_KIND_LEGACY:
            raise ValueError(f"result_kind must be {RESULT_KIND_LEGACY!r}, got {self.result_kind!r}")


def make_new_replicate_result(
    *,
    cell_id: str,
    replicate_id: int,
    base_seed: int,
    replicate_seed: int,
    simulator_commit: str,
    instrumentation_commit: str,
    density_checksum: str,
    simulation_kernel: str,
    fitted_kernel: str,
    truth_parameters: dict[str, float],
    event_times: Any,
    t0: float,
    t1: float,
    fit_status: str,
    fit_success: bool,
    fit_params: dict[str, float],
    fit_loglik: float,
    runtime_seconds: float,
) -> NewReplicateResult:
    """The only constructor for a new-format result. event_times must be
    the actual realization from `simulate_m1`/`simulate_m2`/
    `simulate_m3b_cd`/`gamma_cluster_simulator.simulate_gamma_cluster_m3b_cd`
    for THIS replicate -- never reconstructed from n_events or fit_params."""
    n_events = int(np.asarray(event_times).size)
    validated = validate_event_times(event_times, t0, t1, n_events)
    checksum = event_times_checksum(validated)
    return NewReplicateResult(
        cell_id=cell_id, replicate_id=replicate_id, base_seed=base_seed, replicate_seed=replicate_seed,
        simulator_commit=simulator_commit, instrumentation_commit=instrumentation_commit,
        density_checksum=density_checksum, simulation_kernel=simulation_kernel, fitted_kernel=fitted_kernel,
        truth_parameters=dict(truth_parameters), event_times=validated, n_events=n_events,
        fit_status=fit_status, fit_success=fit_success, fit_params=dict(fit_params), fit_loglik=fit_loglik,
        runtime_seconds=runtime_seconds, event_times_sha256=checksum,
    )


# --------------------------------------------------------------------------
# Serialization (full float64 precision via Python's round-trip-safe
# float repr, used automatically by json.dumps)
# --------------------------------------------------------------------------


def serialize_result(result: NewReplicateResult) -> dict:
    return {
        "result_kind": RESULT_KIND_NEW,
        "cell_id": result.cell_id,
        "replicate_id": result.replicate_id,
        "base_seed": result.base_seed,
        "replicate_seed": result.replicate_seed,
        "simulator_commit": result.simulator_commit,
        "instrumentation_commit": result.instrumentation_commit,
        "density_checksum": result.density_checksum,
        "simulation_kernel": result.simulation_kernel,
        "fitted_kernel": result.fitted_kernel,
        "truth_parameters": result.truth_parameters,
        "event_times": result.event_times.tolist(),
        "n_events": result.n_events,
        "fit_status": result.fit_status,
        "fit_success": result.fit_success,
        "fit_params": result.fit_params,
        "fit_loglik": result.fit_loglik,
        "runtime_seconds": result.runtime_seconds,
        "event_times_sha256": result.event_times_sha256,
    }


def load_result(
    d: dict, *, t0: float = float(DEFAULT_WINDOW[0]), t1: float = float(DEFAULT_WINDOW[1])
) -> NewReplicateResult | LegacyReplicateResult:
    """Reader that classifies the record instead of guessing. A record
    missing `event_times` is ALWAYS returned as LegacyReplicateResult
    (status MISSING_EVENT_SEQUENCE) -- never reconstructed, regardless of
    whether `seed`/`base_seed` happen to be present (as they are in the
    old Pilot 100 output).

    `t0`/`t1` default to the project's standard observation window
    (`density.DEFAULT_WINDOW`, 1600-1784) -- the window bound is a fixed,
    externally-known constant, never inferred from the event_times being
    validated (inferring the window from the data itself would make the
    in-window check circular and unable to catch a genuinely
    out-of-window value)."""
    if "event_times" not in d or d["event_times"] is None:
        return LegacyReplicateResult(raw=d)

    arr = validate_event_times(d["event_times"], t0, t1, d["n_events"])

    recomputed = event_times_checksum(arr)
    stored = d.get("event_times_sha256")
    if stored != recomputed:
        raise ValueError(f"event_times checksum mismatch: stored={stored!r} recomputed={recomputed!r}")

    return NewReplicateResult(
        cell_id=d["cell_id"], replicate_id=d["replicate_id"], base_seed=d["base_seed"],
        replicate_seed=d["replicate_seed"], simulator_commit=d["simulator_commit"],
        instrumentation_commit=d["instrumentation_commit"], density_checksum=d["density_checksum"],
        simulation_kernel=d["simulation_kernel"], fitted_kernel=d["fitted_kernel"],
        truth_parameters=d["truth_parameters"], event_times=arr, n_events=d["n_events"],
        fit_status=d["fit_status"], fit_success=d["fit_success"], fit_params=d["fit_params"],
        fit_loglik=d["fit_loglik"], runtime_seconds=d["runtime_seconds"], event_times_sha256=recomputed,
    )


# --------------------------------------------------------------------------
# Thin JSONL file helpers (for the future 10x10 pilot driver)
# --------------------------------------------------------------------------


def write_jsonl(path: Path | str, results: list[NewReplicateResult]) -> None:
    with Path(path).open("w", encoding="utf-8") as fh:
        for r in results:
            fh.write(json.dumps(serialize_result(r)) + "\n")


def read_jsonl(path: Path | str) -> list[NewReplicateResult | LegacyReplicateResult]:
    out: list[NewReplicateResult | LegacyReplicateResult] = []
    with Path(path).open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(load_result(json.loads(line)))
    return out
