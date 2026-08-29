"""Shared observation-regime pipeline (Stages 2-6 of the 9-stage chain in
docs/thesis/pilot_annotation/MODEL_3B_OBSERVATION_REGIME_SIMULATION_SPEC.md).

Stage 1 (latent event process) and Stage 8 (estimator) are candidate-
specific and live in m0_baseline.py / m2_mbpp.py / m3_bayesian_discrete.py.
Stage 7 (candidate-specific preprocessing) is also candidate-specific.
Stage 9 (recovery metrics) lives in recovery_metrics.py.

This module exists because V1's own recovery study (model3b_cd_simulator/
simulate.py) implements ONLY Stage 1 and feeds it directly to the
estimator -- the confirmed mechanism of root cause #11
(RECOVERY_OBSERVATION_REGIME_MISMATCH). Every tournament candidate's
synthetic ground truth must pass through Stages 2-6 below before Stage 7,
exactly as the design doc requires.

All randomness routes through an `np.random.Generator` passed in by the
caller (matching model3b_cd_simulator/rng.py's `make_rng` convention) --
no other entropy source is used anywhere in this module.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal

import numpy as np

CdMode = Literal["CD1_no_thinning", "CD2_exposure_thinning"]
PrecisionMode = Literal["year_only", "mixed", "day_exact"]
SourceConcentration = Literal["low", "moderate", "high"]

# Real corpus's own audited first-pass precision mixture (Design doc §1,
# M4 section) -- used as the default "mixed" regime weights. This is
# descriptive of the ~141-event corpus's actual heterogeneity, not a
# tunable model parameter.
DEFAULT_MIXED_PRECISION_WEIGHTS: dict[str, float] = {
    "day_exact": 0.532,
    "range_or_multi": 0.128,
    "month": 0.078,
    "year_only": 0.071,
    "unclassified": 0.191,  # treated as year_only for synthetic-generation
                            # purposes: the audit's own Phase-0 finding was
                            # that this bucket resolves mostly to non-exact
                            # classes (DOCUMENT_DATE/EXACT_REPORT_DATE/etc,
                            # never day-exact) -- see MODEL_3B_PHASE0_AUDIT_SUMMARY.md.
}

_SOURCE_CONCENTRATION_STEEPNESS = {"low": 0.5, "moderate": 1.5, "high": 4.0}


@dataclass(frozen=True)
class CensoredEvent:
    """One event after Stages 2-4: an observation interval, not a point."""

    t_true: float          # ground truth (never fed to any estimator; recovery-metric use only)
    t_lower: float
    t_upper: float
    tie_group_id: int      # events sharing an identical (t_lower, t_upper) share this id
    source_id: int         # synthetic source-of-origin, for Stage-removal-stability tests (recovery_metrics.py)
    episode_id: int        # -1 if generated under the "flat" (no-episode) regime


@dataclass
class PipelineResult:
    events: list[CensoredEvent] = field(default_factory=list)
    n_missing_dropped: int = 0
    n_duplicated: int = 0


# ---------------------------------------------------------------------------
# Stage 2 -- Source-Observation Process
# ---------------------------------------------------------------------------

def observe_events(
    latent_event_times: np.ndarray,
    year_covariates: dict[int, float],
    mode: CdMode,
    source_concentration: SourceConcentration,
    rng: np.random.Generator,
) -> np.ndarray:
    """Stage 2. Returns the subset of latent_event_times that are 'observed'.

    mode="CD1_no_thinning": CD density already entered the latent
    intensity at Stage 1 (as V1's simulate_m3b_cd already does) -- this
    stage is a structural no-op under CD-1, by design (not an oversight),
    matching the Variable Role Decision Matrix's CD-1 specification.

    mode="CD2_exposure_thinning": CD density modulates the *probability
    of observing* an event occurring at a constant true rate. p(t) is a
    logistic function of the year's CD covariate, steepness controlled
    by source_concentration (higher concentration -> observation depends
    more sharply on a few dominant-source years, operationalizing Phase
    B's 59.6% CD-dependency finding as a synthetic knob).
    """
    latent_event_times = np.asarray(latent_event_times, dtype=float)
    if mode == "CD1_no_thinning":
        return latent_event_times.copy()
    if mode != "CD2_exposure_thinning":
        raise ValueError(f"unknown CD mode: {mode!r}")

    steepness = _SOURCE_CONCENTRATION_STEEPNESS[source_concentration]
    mean_x = np.mean(list(year_covariates.values())) if year_covariates else 0.0
    kept = []
    for t in latent_event_times:
        year = int(math.floor(t))
        x = year_covariates.get(year, mean_x)
        p = 1.0 / (1.0 + math.exp(-steepness * (x - mean_x)))
        if rng.uniform() <= p:
            kept.append(t)
    return np.array(sorted(kept))


# ---------------------------------------------------------------------------
# Stages 3+4 -- Year-Level Interval Censoring + Same-Year Ties
# ---------------------------------------------------------------------------

def censor_events(
    observed_event_times: np.ndarray,
    precision_mode: PrecisionMode,
    rng: np.random.Generator,
    *,
    day_width: float = 1.0 / 365.0,
    mixed_weights: dict[str, float] | None = None,
) -> list[CensoredEvent]:
    """Stages 3-4 combined. Assigns each observed event a [t_lower, t_upper)
    interval per the target precision regime, and tags same-interval
    events with a shared tie_group_id (Stage 4).

    precision_mode="year_only": every event -> [floor(t), floor(t)+1).
    This is the dominant real regime once M4's day-exact subset is
    excluded (12/141 HIGH-confidence exact dates per the frozen Phase-0
    ledger) -- the primary regime M0/M2/M3 must be tested against.

    precision_mode="day_exact": near-zero-width interval [t, t+day_width).
    Used only for M4-style sensitivity comparisons; M4 itself is
    EXCLUDED_INSUFFICIENT_PRECISE_SUBSET and not built by this harness,
    but the pipeline still supports this mode for M0/M2/M3's own
    "day_exact" factor-grid cells (Design doc §3).

    precision_mode="mixed": draws a per-event precision tier from
    DEFAULT_MIXED_PRECISION_WEIGHTS (or an override), matching the real
    corpus's actual heterogeneity -- the single most externally-valid
    setting per the Design doc's own note.

    Output interval width NEVER collapses to a fabricated point estimate
    -- this is the crux fix for the confirmed root cause. Only day_exact
    events get a near-zero (not exactly zero, to keep bin math well
    defined) width.
    """
    weights = mixed_weights or DEFAULT_MIXED_PRECISION_WEIGHTS
    observed_event_times = np.asarray(sorted(observed_event_times), dtype=float)
    intervals: list[tuple[float, float]] = []
    for t in observed_event_times:
        tier = precision_mode
        if precision_mode == "mixed":
            tier = _draw_precision_tier(weights, rng)
        if tier in ("day_exact",):
            lo, hi = t, t + day_width
        elif tier in ("month",):
            month_start = math.floor(t * 12.0) / 12.0
            lo, hi = month_start, month_start + (1.0 / 12.0)
        elif tier in ("range_or_multi",):
            # A multi-day range: width drawn 2-9 days, matching the audit's
            # own DATE_RANGE_BOUNDARY examples ("10-12 Maret", "6 & 9 November").
            width_days = rng.integers(2, 10)
            lo = t
            hi = t + width_days / 365.0
        else:  # "year_only" or "unclassified" (treated as year_only, see module docstring)
            lo, hi = math.floor(t), math.floor(t) + 1.0
        intervals.append((lo, hi))

    tie_groups: dict[tuple[float, float], int] = {}
    censored: list[CensoredEvent] = []
    for t, (lo, hi) in zip(observed_event_times, intervals):
        key = (round(lo, 9), round(hi, 9))
        if key not in tie_groups:
            tie_groups[key] = len(tie_groups)
        censored.append(
            CensoredEvent(
                t_true=float(t), t_lower=float(lo), t_upper=float(hi),
                tie_group_id=tie_groups[key], source_id=-1, episode_id=-1,
            )
        )
    return censored


def _draw_precision_tier(weights: dict[str, float], rng: np.random.Generator) -> str:
    tiers = list(weights.keys())
    probs = np.array([weights[k] for k in tiers], dtype=float)
    probs = probs / probs.sum()
    return tiers[rng.choice(len(tiers), p=probs)]


def tie_rate(censored_events: list[CensoredEvent]) -> float:
    """Fraction of events that share a tie_group_id with >=1 other event."""
    if not censored_events:
        return 0.0
    from collections import Counter

    counts = Counter(e.tie_group_id for e in censored_events)
    tied = sum(1 for e in censored_events if counts[e.tie_group_id] > 1)
    return tied / len(censored_events)


# ---------------------------------------------------------------------------
# Stage 5 -- Parent-Child Episode Structure
# ---------------------------------------------------------------------------

def generate_episode_structured_latent_events(
    n_episodes: int,
    episode_window: tuple[float, float],
    child_rate: float,
    child_cluster_beta: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Stage 5. Draws n_episodes 'parent' arrival times uniformly across
    the window, then generates children per episode via a tight,
    episode-internal exponential-decay burst (child_cluster_beta, a much
    faster decay than the between-episode Hawkes excitation being
    estimated -- e.g. days-to-weeks scale vs. the production beta~0.62
    /year scale). Returns (event_times, episode_ids), both sorted by time.

    Directly operationalizes root cause #6: Phase D's own diagnostic
    found the Sas expedition alone contributes 47.2% of all observed
    90-day event pairs -- this generator lets the tournament measure how
    much apparent between-event excitation is actually a within-episode
    artifact when the estimator is NOT given episode labels (Design
    doc's Stage-5 (b) comparison).
    """
    t0, t1 = episode_window
    parent_times = np.sort(rng.uniform(t0, t1, size=n_episodes))
    event_times: list[float] = []
    episode_ids: list[int] = []
    for ep_id, parent_t in enumerate(parent_times):
        event_times.append(parent_t)
        episode_ids.append(ep_id)
        n_children = rng.poisson(child_rate)
        for _ in range(n_children):
            offset = rng.exponential(1.0 / child_cluster_beta)
            child_t = parent_t + offset
            if child_t < t1:
                event_times.append(child_t)
                episode_ids.append(ep_id)
    order = np.argsort(event_times)
    return np.array(event_times)[order], np.array(episode_ids)[order]


# ---------------------------------------------------------------------------
# Stage 6 -- Missing and Duplicate Reporting
# ---------------------------------------------------------------------------

def apply_missing_and_duplicate_reporting(
    censored_events: list[CensoredEvent],
    missing_rate: float,
    duplicate_rate: float,
    rng: np.random.Generator,
    *,
    duplicate_report_lag_years: float = 0.05,
) -> PipelineResult:
    """Stage 6. Independently (a) drops each event with probability
    missing_rate (total archival loss, distinct from Stage 2's
    non-observation), and (b) duplicates each surviving event with
    probability duplicate_rate, jittering the duplicate's interval
    slightly later -- matching the real corpus's explicit dual-reporting
    pattern (e.g. "24 Sep 1636 (lapor 12 Okt 1636)") -- to test whether a
    Hawkes-family candidate mistakes the duplicate for genuine excitation
    (a direct false-positive-excitation risk).
    """
    if not (0.0 <= missing_rate <= 1.0):
        raise ValueError(f"missing_rate must be in [0,1], got {missing_rate}")
    if not (0.0 <= duplicate_rate <= 1.0):
        raise ValueError(f"duplicate_rate must be in [0,1], got {duplicate_rate}")

    kept = [e for e in censored_events if rng.uniform() > missing_rate]
    n_dropped = len(censored_events) - len(kept)

    out = list(kept)
    n_dup = 0
    next_tie_id = (max((e.tie_group_id for e in censored_events), default=-1) + 1)
    for e in kept:
        if rng.uniform() <= duplicate_rate:
            lag = rng.exponential(duplicate_report_lag_years)
            dup = CensoredEvent(
                t_true=e.t_true, t_lower=e.t_lower + lag, t_upper=e.t_upper + lag,
                tie_group_id=next_tie_id, source_id=e.source_id, episode_id=e.episode_id,
            )
            next_tie_id += 1
            out.append(dup)
            n_dup += 1

    out.sort(key=lambda e: e.t_lower)
    return PipelineResult(events=out, n_missing_dropped=n_dropped, n_duplicated=n_dup)


def assign_synthetic_sources(
    censored_events: list[CensoredEvent],
    n_sources: int,
    rng: np.random.Generator,
) -> list[CensoredEvent]:
    """Tags each event with a synthetic source_id in [0, n_sources), for
    Stage-9's source_removal_stability metric (leave-one-source-out
    refitting). Uniform-random assignment is the simplest defensible
    default; source-concentration-weighted assignment is a future
    refinement not required for this harness's smoke-test scope."""
    return [
        CensoredEvent(
            t_true=e.t_true, t_lower=e.t_lower, t_upper=e.t_upper,
            tie_group_id=e.tie_group_id, source_id=int(rng.integers(0, n_sources)),
            episode_id=e.episode_id,
        )
        for e in censored_events
    ]
