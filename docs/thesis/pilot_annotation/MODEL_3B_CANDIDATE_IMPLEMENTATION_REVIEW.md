# Model 3B — Candidate Implementation Review

> **DESIGN/PLANNING ONLY. Nothing built, run, or fitted. No V2 implemented, no V1/Phase D rerun, no data changed, nothing staged/committed/pushed/deployed.**
> **Companion to**: `MODEL_3B_RECOVERY_TOURNAMENT_DESIGN.md`. For each candidate: reusable code, net-new work, complexity class, and the specific root-cause hypothesis a pass/fail result would confirm or rule out.

---

## M0 — Exposure-adjusted count baseline (Poisson / Negative Binomial)

**Reusable**: none of the project's existing model code — M0 is a standard GLM, structurally simpler than anything currently implemented. `data/thesis/.../CD_ANNUAL_DOCUMENT_DENSITY_WORKING.csv` (or equivalent annual CD-count series, referenced in the audit's Candidate 1 sketch) is directly reusable as the covariate input without modification.

**Net-new**: (1) a period-binned synthetic generator producing annual counts under known Poisson/NB parameters with a CD covariate entering either as a rate predictor (CD-1) or an offset (CD-2); (2) a GLM fitting wrapper (`scipy.optimize`/`statsmodels` — statsmodels is not currently a listed dependency of the `model3b_cd_simulator` package and would need to be added, or the fit implemented directly via `scipy.optimize.minimize` on the Poisson/NB log-likelihood, consistent with the rest of the codebase's existing pattern of hand-rolled `scipy`-based MLE rather than a statistics-library dependency).

**Complexity/runtime**: trivial. Closed-form or near-instant GLM fits; a full recovery study of several thousand replicates across the factor grid is minutes, not hours, on CPU.

**Root-cause hypothesis tested**: primarily #7 (model complexity vs. effective sample size) and, as the comparison floor, #10/#12 (is any excitation term justified at all, at this resolution and n). A pass for M0 alone, combined with M2/M3/M4 all failing or showing no material improvement over M0, would be strong evidence that the Hawkes excitation mechanism itself is not supportable by this corpus regardless of resolution fix — sharpening #12 from "possible" to "likely." A clear M0-vs-Hawkes-candidate separation (Hawkes candidates recovering meaningfully better) would instead support the audit's primary finding that resolution mismatch, not model-family unsuitability, was V1's dominant problem.

---

## M1 — Current V1, non-authoritative benchmark

**Reusable**: the entire `model3b_cd_simulator` package as-is — `likelihood.py` (`loglik_m1`/`loglik_m2`/`loglik_m3b_cd`), `kernel.py` (`excitation_intensity`/`excitation_compensator`), `density.py`, `estimate.py`, `metrics.py`. No changes to V1's own specification are made; what changes is the synthetic-data pipeline feeding it (Simulation Spec §1-7), not V1 itself.

**Net-new**: none for the model itself. The only new work is on the pipeline side (shared with M2-M4): the observation/censoring/tie/episode/missing-duplicate stages (Simulation Spec §2-6), which M1 consumes but does not require any code change to accommodate — the diagnostic value of M1's run comes precisely from feeding it data it cannot cleanly consume without its existing `jitter_ties`-style fabrication, per the Design doc's own note that M1 either (a) needs the fabrication step re-applied (diagnostic) or (b) fails outright without it (also diagnostic).

**Complexity/runtime**: identical to V1's existing recovery study — same order of magnitude as the original 10-cell × 1,000-replicate design (blueprint §8-9), though this tournament's factor grid (Design doc §3) may warrant a reduced replicate count per cell given the larger number of factors now being varied (a tradeoff to be made explicit, not hidden, in any future execution plan).

**Root-cause hypothesis tested**: this is the single most informative candidate for distinguishing "resolution mismatch was the whole story" (#4/#11) from "V1's parameterization/architecture has additional problems beyond resolution" (#2/#10). If M1 recovers acceptably once fed a correctly-censored synthetic regime (without needing fabrication), that isolates resolution mismatch as sufficient explanation. If M1 still fails even under a corrected regime, that confirms at least one additional root cause beyond #4/#11 is independently operating.

---

## M2 — MBPP interval-censored Hawkes (Rizoiu et al. 2022)

**Reusable**: `docs/thesis/colab/model3_mbpp_full.py` — `xi_closed_form`/`Xi_closed_form` (closed-form Eq. 9/10 intensity and cumulative-intensity integrals for constant baseline + exponential kernel) and `neg_ic_ll` (Eq. 18 interval-censored negative log-likelihood) are directly reusable as the estimator core. `model3_mbpp_eval.py`'s `build_bins`/`neg_log_lik_mbpp_lite` are reusable for the lighter-weight population-mean variant already exercised for the existing (narrow, non-transferable per the status addendum's own scoping) branching-ratio robustness check — useful as a secondary, cheaper sanity check alongside the full recovery study, not a replacement for it.

**Net-new**: (1) extending the existing MBPP implementation from its current simple-Hawkes form to the M3B-CD form (density + excitation combined) — the existing code compares only Model 3's plain Hawkes branching ratio, not the density-covariate combined model; (2) the year-level censoring stage of the synthetic pipeline (Simulation Spec §3) generating properly censored ground truth to fit against, since the existing `model3_mbpp_full.py` work was evaluated against the real data's own censoring, not a synthetic recovery study with known ground truth at all — this candidate's recovery test is fully novel even though its estimator core is not.

**Complexity/runtime**: moderate. Closed-form ODE-based intensity/compensator terms (per the existing implementation's own header) mean per-fit cost is comparable to V1's continuous-time MLE, likely cheaper than a numerical-integration alternative would be. A full recovery study at comparable scale to V1's original design is feasible on the same compute budget.

**Root-cause hypothesis tested**: the most direct test of #3/#4/#11 as a class — MBPP is the literature-native reformulation that eliminates the fabricated-timestamp mechanism entirely by construction, not as a workaround. A pass for M2 combined with a fail for M1 (under the same corrected pipeline) would be the cleanest possible confirmation that resolution mismatch alone (not deeper non-identifiability) explains V1's failure. If M2 also fails to recover cleanly, that shifts substantial weight toward #10 (intrinsic non-identifiability of the density+excitation combination, independent of resolution) since M2 removes the resolution confound that clouded V1's own result.

---

## M3 — Bayesian discrete-time Hawkes (period-binned, prior-informed)

**Reusable**: none of the existing estimation code — V1's entire architecture is a frequentist point-estimate MLE via `scipy.optimize.minimize`/L-BFGS-B, structurally incompatible with a Bayesian posterior-sampling approach. The annual CD-density covariate series and the general concept of the M3B-CD combined intensity form (baseline + excitation, reparameterized for discrete time) are conceptually reusable, but no code transfers directly.

**Net-new**: (1) a discrete-time self-exciting count process specification (e.g. INGARCH-family or a discrete Hawkes formulation with a geometric/negative-binomial offspring kernel analogue) — genuinely new model-specification work, not merely new code for an existing specification; (2) a Bayesian fitting routine, requiring a new dependency decision (`PyMC` or `numpyro` are the standard choices for this problem class; neither is currently listed as a project dependency — a decision for a future implementation turn, not made here); (3) posterior-interval coverage, posterior-predictive false-positive-excitation check, and a WAIC/LOO-based model-selection analogue replacing V1's AIC/BIC comparison (motivated specifically because AIC/BIC's failure mode was independently confirmed under both correct specification and deliberate kernel misspecification, per the audit §1 rows 6/8 — a like-for-like Bayesian analogue is a substantive methodological response to a documented failure, not an arbitrary swap).

**Complexity/runtime**: highest of the four mandatory candidates. MCMC fitting per synthetic replicate is materially more expensive than L-BFGS-B point estimation. A full recovery study at V1's original scale (10 cells × 1,000 replicates) is likely infeasible at that replicate count without either a much-reduced replicate count per cell (explicit power/precision tradeoff to be disclosed, not hidden) or a faster approximate-Bayesian method (variational inference), which would itself require its own validation before being trusted as a stand-in for full MCMC.

**Root-cause hypothesis tested**: #4 (sidesteps entirely by construction — no sub-year timestamp is ever consumed), #7 (directly, via informative priors replacing the asymptotic Wald intervals the postmortem already showed miscalibrate at this n: 60-84% coverage vs. 92.5-97.5% target for alpha/beta), and #10 (via the coverage/prior mechanism — a well-calibrated Bayesian posterior interval at this small n is a different, arguably more appropriate identifiability diagnostic than the frequentist CI coverage V1 relied on).

---

## M4 — Continuous-time Hawkes on a verified exact-date subset (EXCLUDED_INSUFFICIENT_PRECISE_SUBSET)

**Status: `EXCLUDED_INSUFFICIENT_PRECISE_SUBSET`**, resolved by researcher decision (2026-08-29) — superseding the earlier `CONDITIONALLY_ELIGIBLE` status. Guard A's manual audit (Design doc §1a) completed: 96/96 candidate rows classified and QA-verified against full `text_asli` (`MODEL_3B_PHASE0_DATE_PRECISION_LEDGER.csv`). Result: `EXACT_EVENT_DATE` = 69 total, but only 12 at HIGH confidence (57 MEDIUM, resting on genre-level inference). Applying the prespecified HIGH-only threshold, 12 falls below the ~30-40 floor, so **M4 does not proceed for the current dataset**. HIGH and MEDIUM rows were deliberately not combined to reach the floor. The 57 MEDIUM rows are recorded `SENSITIVITY_ONLY_NOT_PRIMARY_M4` — reconsiderable only under a future uncertainty-aware temporal model, never folded into M4's primary recovery test. Everything below in this section (reusable code, net-new work, complexity) describes what M4's implementation *would have* required and remains historically informative, but is not scoped for near-term execution given the exclusion.

**Reusable**: identical to M1 — `model3b_cd_simulator`'s existing `likelihood.py`/`kernel.py`/`simulate.py`, applied unchanged to a filtered subset of events rather than the full 141.

**Net-new**: (1) the dedicated precision-parsing audit of `event_date_raw` (Design doc's Phase 0 prerequisite, = Guard A) — manually classifying each of the 75 candidate events into exactly one of the eight classes above, distinguishing genuine single-exact-day events from ranges, multiple-date entries, and event-date/report-date confusion (a small, well-scoped, non-model-fitting data-engineering task, not yet performed by any existing script in this repo); (2) a filtering step selecting the `EXACT_EVENT_DATE`-only subset for both the synthetic recovery test's target sample size and, if M4 ever passes and is separately authorized for real-data use, the actual real-data input.

**Complexity/runtime**: same order as V1's existing recovery study, but on a smaller synthetic n (matching whatever the Phase 0 audit confirms as the real precise-subset size — first-pass estimate 75/141, likely somewhat lower after excluding report-date confusion and qualified language) — cheaper in absolute compute, though a smaller n also means the recovery test itself has less statistical power, a tradeoff the Design doc's tournament framework treats as a reportable finding (`EXCLUDED_INSUFFICIENT_PRECISE_SUBSET`) if the subset proves too small, not a flaw to be patched around.

**Root-cause hypothesis tested**: #4 and #11 in the cleanest possible isolation — since M4's subset is chosen specifically to eliminate the temporal-resolution confound by construction (real exact-date events, not synthetic idealization), a pass for M4 is the single most direct confirmation that continuous-time Hawkes recovers correctly when its precision assumption is genuinely met. A fail for M4 despite the resolution confound being removed would be strong evidence for #10 (non-identifiability) or #12 (Hawkes-family incompatibility) independent of the resolution issue.

---

## Cross-candidate note: shared pipeline infrastructure

Stages 2 (source-observation), 4 (same-year ties), 5 (parent-child structure), and 6 (missing/duplicate reporting) of the Simulation Spec are genuinely new, shared infrastructure — none of the four candidates' own estimator code needs to change to consume their output, but all four (M0/M2/M3 fully, M1/M4 as diagnostic edge cases) depend on this shared pipeline existing before any candidate-specific recovery test can run. Building this shared infrastructure once, rather than per-candidate, is the single highest-leverage net-new implementation task if/when this tournament is authorized to proceed — it is not itself a "candidate," but every candidate's validity depends on it being built correctly and used identically across all four/five recovery tests (the same discipline violation — an inconsistent or partial pipeline — is exactly what made V1's original recovery study unrepresentative).
