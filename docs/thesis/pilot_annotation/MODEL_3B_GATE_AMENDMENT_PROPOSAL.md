# Model 3B — Gate Amendment Proposal

> **Proposal only. No amendment is adopted by this document. `MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv` (the original 70-row, frozen gate specification) is NOT modified by this audit — checksum unchanged, verified in the parent audit document. Every amendment below requires explicit researcher approval before it may govern any future gate evaluation.**

Each proposal below follows the required structure: original gate; observed issue; evidence; proposed amendment; scientific consequence; risk of post-hoc relaxation; whether the amendment tightens, relaxes, or changes the estimand; researcher decision required.

---

## Proposal 1 — M0 interval-coverage gate (GATE-007): fix implementation, do not change the target

**Original gate**: `ci_coverage_95pct`, target band `[0.925, 0.975]`, MANDATORY.

**Observed issue**: 0.544–0.615 coverage across all 15 pilot cells, traced (`MODEL_3B_M0_INTERVAL_COVERAGE_AUDIT.md` §2) to a diagonal-only finite-difference Hessian in `run_recovery_m0.py::run_cell`, omitting the `theta0`/`theta1` covariance term.

**Evidence**: small oracle (n=60, `S3-equiv`-moderate cell, fixed seed 900000): diagonal-only method coverage 0.450; full 2×2 Hessian-inverse method coverage 0.933 (inside target band); mean SE(theta1) ratio full/diagonal = 2.40.

**Proposed amendment**: NOT a change to GATE-007's threshold or band. Propose only an **implementation fix**: replace the diagonal-only SE construction with a full 2×2 (or larger, if `phi` is later un-profiled) finite-difference Hessian, inverted as a matrix, before any future M0 recovery run is scored against GATE-007.

**Scientific consequence**: none to the estimand or the target — this restores the gate to testing what it was always meant to test. The point estimator (already passing GATE-001/004/037) is unaffected.

**Risk of post-hoc relaxation**: low. The proposed fix tightens the interval (larger, more correct SEs), which is the opposite direction from a relaxation — a corrected implementation is *harder* to pass than the current buggy one only insofar as the current implementation was producing artificially narrow (miscalibrated) intervals that happened to fail coverage from below; a correctly-calibrated interval could in principle still fail if the true small-sample behavior departs from asymptotic normality, which the oracle does not fully rule out at n=1000/cell (only tested at the oracle's own n=60).

**Estimand**: unchanged — still `theta0`/`theta1` individual coverage.

**Researcher decision required**: YES — approve the fix, and separately authorize a re-run at the pilot's full 1,000-replicate/cell scale under the corrected code before GATE-007 is treated as adjudicated.

---

## Proposal 2 — M2 individual-alpha/beta gates (GATE-017, GATE-021): supplement, do not delete

**Original gates**: `absolute_relative_bias_excitation_params` (`<=0.10`, GATE-017) and `ci_coverage_95pct` for alpha/beta (`[0.925,0.975]`, GATE-021), both MANDATORY.

**Observed issue**: individual `alpha` bias 4,450–5,480%; alpha/beta coverage 3–20%. Traced (`MODEL_3B_M2_IDENTIFIABILITY_PROFILE.md` §1) to a confirmed, sharp objective ridge along `alpha/beta ≈ n_true`: NLL varies <2 units across a 20× range of `beta` at fixed `n`, but >500 units when `n` itself moves 40% at fixed `beta`.

**Proposed amendment**: **Preserve GATE-017/GATE-021 exactly as frozen** — do not delete, do not relax their thresholds. **Add** two new, supplementary gates specific to M2 (and any future Hawkes-family candidate sharing this parameterization):
- `branching_ratio_absolute_bias` / `branching_ratio_relative_bias` at the *mandatory* tier for M2 (currently these exist as GATE-019/020 but are worth explicitly re-affirming as the primary decision-relevant gates for M2 given this finding — they already show the most defensible pass/marginal-pass behavior even at reduced scale: 0.020–0.054 absolute, 0.030–0.080 relative).
- A new gate (not yet numbered — a future turn would need to extend the CSV with a new `gate_id` following the existing `GATE-0NN` convention) for **interval-level integrated excitation mass**, if a future design turn defines a concrete estimator for it — not specified further here, since this audit's scope is diagnosis, not new gate design beyond what's already implied by the branching-ratio finding.

**Scientific consequence**: this does not lower the bar for M2 — it redirects the *primary* pass/fail decision toward a quantity (`n`) the evidence shows is actually recoverable from this data, while keeping the original individual-parameter gates on record as a permanent, visible reminder that `alpha`/`beta` individually are not currently claimable. A future paper or report citing M2's results must not claim individual excitation-amplitude (`alpha`) or decay-rate (`beta`) values as reliable — only the branching ratio.

**Risk of post-hoc relaxation**: **moderate — this is the amendment most exposed to that risk**, since it was proposed *after* seeing GATE-017/021 fail badly. Mitigations already applied: (a) the ridge is demonstrated on **independent synthetic data with known ground truth**, not inferred from the failure pattern alone; (b) the original gates are preserved, not deleted, so the failure remains permanently visible; (c) the amendment is not self-adopted here — it requires the same researcher sign-off any other design change in this project has required.

**Estimand**: **changes** — from "is `alpha` individually unbiased/covered" to "is `n=alpha/beta` unbiased/covered." This is an explicit estimand narrowing, not a threshold relaxation on the same estimand.

**Researcher decision required**: YES — this is the single highest-stakes amendment in this proposal document and should not be treated as a formality.

---

## Proposal 3 — M2 theta0 gate (GATE-018): defer, do not amend yet

**Original gate**: `normalized_absolute_bias_baseline_param` (`<=0.25`, MANDATORY).

**Observed issue**: 1.36–1.59 bias across 4 cells — far outside tolerance, despite M0's theta0 (identical functional form and covariate) passing cleanly (0.007–0.034).

**Proposed amendment**: **None proposed yet.** This audit could not determine (§ M2 audit, GATE-018 row of the classification CSV) whether the theta0 failure is a joint-optimizer interaction with the mis-identified alpha/beta (plausible, unconfirmed) or something else. Proposing an amendment before root-causing this would be premature.

**Scientific consequence / risk / estimand**: N/A — no amendment proposed.

**Researcher decision required**: YES, but the decision requested is to **authorize further diagnostic work** (not an amendment) — specifically, profiling the joint `(theta0, alpha, beta)` objective surface the way §1 of the M2 audit profiled `(alpha, beta)` alone, to determine whether theta0's bias is downstream of the ridge or an independent defect.

---

## Proposal 4 — M3 null-boundary decision rule (GATE-030, GATE-035 at the null cell): fix decision rule, not the model

**Original gates**: `false_positive_excitation_rate` (`<=0.05`, GATE-030) and `credible_interval_coverage_95pct` (`[0.925,0.975]`, GATE-035), both MANDATORY.

**Observed issue**: 100% false-positive rate at the `n_true=0` cell; 0.0 coverage at the same cell. Traced (`MODEL_3B_M3_NULL_BOUNDARY_AUDIT.md` §1–2) directly to `_from_unconstrained`'s `expit(logit_n)` transform, which makes `n=0` structurally unreachable, combined with a decision rule (`lo > 0.0`) that treats any strictly-positive lower credible bound as a positive detection.

**Proposed amendment**: adopt one of four candidate null designs analyzed in the M3 audit §3 — explicit `H0:n=0` vs `H1` comparison, spike-and-slab, hurdle model, or a preregistered region-of-practical-equivalence (ROPE) threshold `epsilon_n`. **No design is selected here.** If ROPE is chosen, `epsilon_n` must be justified by literature or explicit researcher policy — **not chosen automatically or post-hoc to make the gate pass** (governing instruction's own explicit prohibition, §8.2).

**Scientific consequence**: whichever design is chosen changes *how* "no excitation" is tested, not whether it should be tested — the scientific question (does the null-cell data show spurious excitation-detection) remains open and legitimate; only the current instrument for answering it is broken.

**Risk of post-hoc relaxation**: **high, specifically for the ROPE option**, since a permissive `epsilon_n` chosen after seeing this failure would trivially "fix" the gate without addressing whether the model has a real false-positive tendency. The explicit-comparison and spike-and-slab/hurdle options carry much lower relaxation risk since they don't involve a tunable threshold at all — they give a first-class `P(\text{excitation}|data)` quantity.

**Estimand**: **changes**, from "is the current credible interval's lower bound distinguishable from exactly 0" to whichever design-specific quantity (posterior model probability, `P(z=1|data)`, or a ROPE-based test) is adopted.

**Researcher decision required**: YES — including the choice of which of the four designs to pursue, which this audit does not recommend among (per governing instruction §8.2, "do not choose automatically").

---

## Proposal 5 — M3 branching-ratio bias at non-null cells (GATE-033/034): no amendment proposed

**Observed issue**: 0.134–0.135 absolute bias, 0.198–0.199 relative bias at the three non-null cells — roughly 2× the respective thresholds, unrelated to the null-boundary mechanism (M3 audit §5).

**Proposed amendment**: none. This reads as a genuine, if moderate, recovery weakness in M3's discrete-time formulation at 200/cell reduced scale. Recommend re-running at full scale (with the null-boundary decision rule already fixed, so the two issues don't get conflated in a future run's diagnostics) before considering any gate amendment here.

**Researcher decision required**: NO amendment decision needed at this time; only the general re-run authorization already covered by Proposal 4's downstream consequence.

---

## Proposal 6 — advisory gates never computed by this pilot (GATE-038-042/050/053-057/059/061-063): scope gap, not a gate defect

**Observed issue**: 21 of the 42 pilot-applicable gates (all ADVISORY tier, plus GATE-032/031 discussed separately below) have no observed value at all — the pilot's run scripts never implemented `boundary_solution_rate` aggregation (M0/M3), `held_out_predictive_score`, `source_removal_stability`, `episode_removal_stability`, or `calibration`. **Correction (2026-08-30):** `GATE-036` (`false_negative_excitation_rate`, M0) is excluded from this list — it was reclassified `NOT_INTERPRETABLE`/`NOT_APPLICABLE_TO_MODEL_DOMAIN` (§11a of the main audit), since it is not merely uncomputed but mathematically undefined for M0 (no excitation process, no excitation decision rule). It is not a scope gap; no future run of this pilot's scripts would ever make it computable for M0.

**Proposed amendment**: none to the gates themselves — they remain correctly specified. Proposed **scope decision** for a future authorization: whether these advisory diagnostics are implemented before or after the mandatory-gate fixes above are validated. Recommend **after** — none of the mandatory-gate root causes found in this audit (§ M0/M2/M3) depend on these advisory metrics, so implementing them now would not change any current classification, only add cost.

**Researcher decision required**: NO immediate decision — noted for future scoping only.

---

## Proposal 7 — M3 excitation-parameter gate (GATE-031): retire for M3's own parameterization

**Original gate**: `absolute_relative_bias_excitation_params` (`<=0.10`, MANDATORY, M3).

**Observed issue**: M3 parameterizes directly in `(theta0, theta1, n, beta)` — there is no separate `alpha`-like amplitude parameter to which this gate's wording (assuming an "excitation params" plural, modeled on M0/M1/M2/M4's `alpha`) naturally applies.

**Proposed amendment**: for M3 specifically, retire this gate in favor of the branching-ratio gates it already reports directly (GATE-033/034), which cover the same underlying scientific question (how much excitation mass) without assuming a parameterization M3 doesn't use. Do not retire GATE-031 for M0/M1/M2/M4, which do have a distinct `alpha`.

**Scientific consequence**: closes a gate/model mismatch identified before it was ever meaningfully evaluable for M3, rather than silently reporting it as "not computed" indefinitely.

**Risk of post-hoc relaxation**: low — this was a parameterization mismatch present from the moment M3's design was specified (Design doc §5's own Option B/C), not a response to an unfavorable result.

**Estimand**: N/A for M3 (removes an inapplicable gate rather than changing what it measures).

**Researcher decision required**: YES — formal retirement of a mandatory gate for one candidate is not a decision this audit makes unilaterally.

---

## Summary table

| # | Gate(s) | Amendment type | Relaxation risk | Decision required |
|---|---|---|---|---|
| 1 | GATE-007 (M0) | Implementation fix, target unchanged | Low | YES |
| 2 | GATE-017/021 (M2) | Estimand narrowing + supplementary gate | Moderate | YES |
| 3 | GATE-018 (M2) | None (further diagnosis authorized) | N/A | YES (diagnosis only) |
| 4 | GATE-030/035 (M3, null cell) | Decision-rule redesign | High (ROPE variant only) | YES |
| 5 | GATE-033/034 (M3, non-null) | None | N/A | NO |
| 6 | 21 advisory gates | None (scope/sequencing) | N/A | NO (informational) |
| 7 | GATE-031 (M3) | Gate retirement for M3 only | Low | YES |

**None of these amendments are adopted by this document.** All require separate, explicit researcher review per the governing instruction's stop condition (§16).
