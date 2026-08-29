# Model 3B — Observation-Regime Simulation Pipeline Specification

> **DESIGN SPEC ONLY. Not executed. No code in this document is runnable as-is; it specifies what a future, separately-authorized implementation turn would build. No V2 implemented, no data changed, nothing staged/committed/pushed/deployed.**
> **Companion to**: `MODEL_3B_RECOVERY_TOURNAMENT_DESIGN.md` §2. This document is the technical detail behind that design's governing pipeline: `latent event process -> source-observation process -> year-level interval censoring -> same-year ties -> parent-child episode structure -> missing and duplicate reporting -> candidate-specific preprocessing -> estimator -> recovery metrics`.

---

## Why this pipeline exists

V1's recovery study (`docs/thesis/colab/model3b_cd_simulator/simulate.py`) implements only the first stage of this chain — a latent Hawkes/Poisson event process via Ogata thinning — and feeds its output directly to the estimator, with no intervening observation model at all. The real data undergoes at minimum the censoring and tie-generation stages before it ever reaches `model3_hawkes_kaskade_event.py`'s fitting routine. **This is the exact, confirmed mechanism of root cause #11**: the recovery study is missing pipeline stages that the real application cannot avoid. Every candidate in the tournament must pass synthetic ground truth through the full chain, not just stage 1.

---

## Stage 1 — Latent Event Process

**Purpose**: generate ground-truth event times from a known generative model, at full continuous-time precision, exactly as V1's existing `simulate.py` already does.

**Reusable as-is**: `simulate_m1`, `simulate_m2`, `simulate_m3b_cd` (`model3b_cd_simulator/simulate.py`) and their shared closed-form compensator (`kernel.py::excitation_compensator`). No changes needed to this stage for M1/M2/M4 (which are Hawkes-family and share V1's generative form). M0 (baseline count) and M3 (discrete-time) need a period-binned generative process instead of continuous Ogata thinning — see Stage 8 note below; conceptually this is still "Stage 1" for those candidates, just discrete from the start.

**Parameters**: mu/theta0/theta1 (baseline), alpha/beta or n/beta (excitation, per §5 of the Design doc), observation window [t0, t1) — reuse V1's [1600, 1784) window (blueprint-matched) as the default, with the reduced-n sensitivity settings from the Design doc's factor grid (§3) as alternates.

**Output**: a set of exact, continuous-time event coordinates with known ground-truth parameters — the "true" world before any observation process degrades it.

---

## Stage 2 — Source-Observation Process

**Purpose**: model the fact that not every latent event in the true world produces a surviving archival record, and that a record's existence/content is itself a function of source concentration and CD-density-as-exposure (if CD-2 interpretation is being tested — see the Variable Role Decision Matrix).

**What it does**: for each Stage-1 event, draw a "recorded" indicator with probability that may depend on:
- The CD-density covariate for that event's year, under the **CD-2 (exposure)** interpretation specifically — i.e., under CD-2, `x_CD(t)` modulates the *probability of observing* an event that occurs at a constant true rate, rather than the *true rate itself* (which is CD-1's interpretation, tested by NOT applying this stage's CD-dependent thinning and instead letting `x_CD` enter Stage 1's intensity directly, as V1 already does).
- A source-concentration parameter (Design doc §3): low/moderate/high, controlling what fraction of recorded events derive from a small number of dominant sources (operationalizing Phase B's 59.6% CD-dependency finding as a synthetic knob, not a real-data value to be estimated by this stage).

**Interaction with Stage 6 (missing/duplicate reporting)**: this stage handles *whether an event enters the archival record at all*; Stage 6 handles *distortions to events that did* enter the record (missed entirely after being recorded, or double-counted). Keeping these separate avoids conflating two different failure mechanisms into one nuisance parameter.

**New implementation needed**: no existing code in this repo does source-observation thinning. A new, small function (e.g. `observe_events(latent_events, cd_density_by_year, mode, source_concentration) -> observed_events`) would be net-new, parameterized by `mode in {"CD1_no_thinning", "CD2_exposure_thinning"}` so the same function serves both CD interpretations by branching internally rather than duplicating the whole pipeline per interpretation.

---

## Stage 3 — Year-Level Interval Censoring

**Purpose**: this is the crux fix for the confirmed root cause. Once an event is "observed" (Stage 2), its recorded date resolution is NOT the exact Stage-1 timestamp — it is whatever precision the archival source actually preserved, per the real corpus's own audited distribution (Design doc §1, M4 section: roughly 53% single-day, 13% range/multiple, 8% month, 7% year-only, 19% unclassified, pending Phase 0's dedicated audit).

**What it does**: for each observed event with true continuous time `t`, replace it with an interval `[t_lower, t_upper]` (or, for the day-precision subset, a near-zero-width interval) drawn according to the target precision-mixture being tested (Design doc §3, "date precision" factor). For the **year-only** regime specifically (the dominant real regime once M4's subset is excluded): `t_lower = floor(t)`, `t_upper = floor(t) + 1` — the event is known only to have occurred sometime within its calendar year, exactly matching what `linimasa_events.year` actually encodes and what MBPP's interval-censored likelihood (Eq. 18, `model3_mbpp_full.py`) is designed to consume directly.

**Critical constraint carried from the audit**: this stage's output must NEVER be a fabricated point estimate. M0's period-binned counts, M2's interval-censored likelihood, and M3's discrete-time formulation all consume the *interval* `[t_lower, t_upper]` or its implied bin directly — none of them require collapsing it back to a single fictitious timestamp. **Only M1 (V1's own specification, run here purely as a benchmark) and M4 (on its precision-verified subset only) require a point timestamp** — and M1, run under this corrected pipeline, must NOT silently re-apply `jitter_ties`-style fabrication; if V1's estimator structurally requires a point estimate and the synthetic event only has an interval, that is itself diagnostic information (V1's architecture cannot consume the data's true resolution without fabrication, confirming root cause #3 independent of any particular jitter implementation).

**Reusable**: `model3_mbpp_full.py`'s `xi_closed_form`/`Xi_closed_form` (the closed-form Eq. 9/10 intensity and cumulative-intensity integrals MBPP already implements) and `neg_ic_ll` (Eq. 18 interval-censored likelihood) are the estimator-side counterpart to this stage and should be reused, not reimplemented, for M2.

---

## Stage 4 — Same-Year Ties

**Purpose**: multiple Stage-3 intervals may share the exact same year (the real corpus's dominant tie mechanism, per the audit's §2 finding — "many events share the exact same year"). This stage is conceptually a special case of Stage 3 (both events get the identical `[y, y+1)` interval) but is broken out separately because it is the stage whose mishandling (V1's `jitter_ties`) is the confirmed proximate cause of root cause #3.

**What it does**: for the year-only precision tier specifically, tag events sharing a year with an explicit tie-group identifier. This tag is consumed differently per candidate:
- M0: ties simply co-contribute to the same annual count bin — no special handling needed, this is the natural behavior of a count model.
- M2 (MBPP): ties within the same censoring interval are naturally handled by the interval-censored likelihood, which integrates over within-interval ordering rather than requiring it as an input — this is precisely why MBPP is the literature-native answer rather than a workaround.
- M3 (discrete-time): identical to M0's handling — ties simply increment the same period's count.
- M1 (benchmark) and M4 (precise subset): M4 should have near-zero ties by construction (its precision floor excludes year-only events); M1, run on the full corrected pipeline, WILL encounter ties and must be observed to either (a) require a fabrication step to proceed (diagnostic finding, confirming #3) or (b) genuinely fail to converge/fit at all when given tied interval data without a jitter escape hatch (also diagnostic, confirming #3 at the architecture level).

**New implementation needed**: tie-group tagging is a small utility function alongside Stage 3's censoring logic; no existing code implements this (V1's `jitter_ties` is the thing being tested, not reused, for M1's benchmark run).

---

## Stage 5 — Parent-Child Episode Structure

**Purpose**: directly operationalizes root cause #6. Phase D's own diagnostic found the Sas expedition alone (one episode, 11 members) contributes 47.2% of all observed 90-day event pairs — meaning a flat, unordered event array (V1's assumption) is likely absorbing genuine within-episode dependence and misattributing it to between-episode contagion (the very thing the Hawkes excitation term is meant to measure).

**What it does**: Stage 1's latent generator is extended (for the "non-flat" episode-count settings in the Design doc's factor grid) to first draw a smaller number of "parent episodes," then generate 1-N child events per episode via a tighter, episode-internal clustering mechanism (e.g. a short-lag, high-intensity burst) distinct from the between-episode Hawkes excitation being estimated. The estimator then either (a) is given episode labels and can condition on them (a natural extension for M3's discrete-time formulation, noted in the Design doc as a future extension point, not implemented in this tournament) or (b) is NOT given episode labels, and recovery quality is compared against the "flat" (no-episode) setting to measure how much apparent excitation is actually within-episode artifact.

**New implementation needed**: entirely new — no existing code in this project generates episode-structured synthetic event sequences. This is the most novel piece of the pipeline; budget accordingly (Design doc §6 sequencing places episode-aware testing as a secondary sensitivity check within each candidate's cell grid, not a separate model to build from scratch this turn).

---

## Stage 6 — Missing and Duplicate Reporting

**Purpose**: models two further real-world distortions distinct from Stage 2's source-observation thinning:
- **Missing-event rate**: an event survives to Stage 5 but is then dropped entirely (simulating total archival loss, not just non-observation at the source) — a real, previously-untested risk (Design doc §3: 0%/10%/25% levels).
- **Duplicate-report rate**: an event is recorded more than once under what looks like a distinct entry (the real corpus already shows explicit dual-reporting language — e.g. `"24 Sep 1636 (lapor 12 Okt 1636)"` — where an event date and a separate report date could plausibly generate two rows if not carefully deduplicated upstream of any model).

**What it does**: after Stage 5, independently (a) drop each event with the missing-rate probability, and (b) duplicate each surviving event with the duplicate-rate probability, optionally jittering the duplicate's recorded interval slightly later (matching the real corpus's "lapor" pattern of a later report date) to test whether candidates mistake a duplicate for a genuine second, closely-following event (a direct false-positive-excitation risk for any Hawkes-family candidate).

**New implementation needed**: small, new utility functions; straightforward Bernoulli thinning/duplication, not a modeling innovation.

---

## Stage 7 — Candidate-Specific Preprocessing

**Purpose**: the point where the shared synthetic pipeline output (a set of censored, tied, episode-structured, possibly-missing-or-duplicated observations) is transformed into whatever input format each candidate's estimator actually consumes.

- M0: aggregate to annual (or coarser) counts + annual CD covariate.
- M1 (benchmark): must produce point timestamps — either by requiring the same fabrication V1 currently uses (in which case this stage IS the diagnostic, per Stage 4 above) or by being unable to proceed on interval data at all without modification.
- M2: pass censoring intervals directly to the interval-censored likelihood — no point-estimate fabrication at any point.
- M3: aggregate to the discrete time grid (annual, matching the count model) but retain the self-exciting count structure (not collapsed to a single GLM count, unlike M0).
- M4: filter to the precision-verified subset only (events whose Stage 3 interval width is below the "genuinely exact" threshold established by Phase 0's dedicated precision audit), discard the rest, then proceed as continuous-time point data — the ONLY candidate for which discarding data is the correct move, since M4's entire purpose is testing the subset where fabrication is unnecessary.

---

## Stage 8 — Estimator

Existing, reusable code per candidate:
- M0: standard GLM (Poisson/NB) — `scipy`/`statsmodels`, no project-specific code exists yet; trivial to write new.
- M1: `model3b_cd_simulator/likelihood.py::loglik_m1`/`loglik_m2`/`loglik_m3b_cd`, unchanged.
- M2: `model3_mbpp_full.py::neg_ic_ll` (Eq. 18), reused; `model3_mbpp_eval.py::neg_log_lik_mbpp_lite`/`build_bins` for the lighter-weight population-mean variant already used for the existing (narrow, non-transferable) branching-ratio robustness check.
- M3: new — no existing Bayesian discrete-time Hawkes implementation in this repo; would need a new MCMC/variational fitting routine (e.g. via `PyMC`/`numpyro`, neither currently a project dependency — a new-dependency decision for a future implementation turn, not made here).
- M4: `model3b_cd_simulator/likelihood.py::loglik_m1`/`loglik_m3b_cd`, unchanged, applied only to the filtered precise subset.

---

## Stage 9 — Recovery Metrics

See `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` for the full numeric threshold table. This stage computes, per synthetic replicate and aggregated per cell: parameter bias, RMSE, interval/credible-interval coverage, branching-ratio recovery, false-positive/false-negative excitation rate, convergence rate, boundary-solution rate, held-out predictive score, source-removal and episode-removal stability (leave-one-source-out / leave-one-episode-out refitting, checking parameter stability — a new diagnostic not present in V1's existing recovery study, directly motivated by root causes #5/#6), and calibration (posterior-predictive or frequentist calibration curve, candidate-appropriate).

---

## Summary: Reuse Map

```text
STAGE                          REUSABLE FROM              NEW WORK NEEDED
1. Latent event process        simulate.py (M1/M2/M4)     period-binned generator (M0/M3)
2. Source-observation          --                          new: observe_events()
3. Year-level censoring        model3_mbpp_full.py         new: censoring-interval generator
   (estimator side only)       (xi_closed_form, neg_ic_ll)
4. Same-year ties              --                          new: tie-group tagging
5. Parent-child structure      --                          new: episode-structured generator
6. Missing/duplicate           --                          new: Bernoulli thin/duplicate
7. Candidate preprocessing     --                          new, per candidate (mostly small)
8. Estimator                   likelihood.py (M1/M4),      new: GLM (M0), Bayesian discrete-
                                model3_mbpp_full.py (M2)    time MCMC/VI (M3)
9. Recovery metrics            metrics.py (partial, if     new: source/episode-removal
                                extending V1's existing     stability checks
                                gate logic)
```

Nothing in this document has been executed. It specifies scope for a future, separately-authorized implementation turn.
