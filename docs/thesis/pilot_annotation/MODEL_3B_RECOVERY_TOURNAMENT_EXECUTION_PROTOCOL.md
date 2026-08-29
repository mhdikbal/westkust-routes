# Model 3B — Recovery Tournament Execution Protocol

> **DESIGN ONLY. NOT AUTHORIZED FOR EXECUTION.** No Model V2 implemented. No model-fitting or simulation code written or run. No V1 or Phase D rerun. No data file touched. Nothing staged, committed, pushed, or deployed.
> **Extends** `MODEL_3B_ROOT_CAUSE_AND_LITERATURE_COMPATIBILITY_AUDIT.md` §5 (design sketch) into an operational, step-by-step protocol a future, separately-authorized turn could follow without re-deriving anything. Read that audit first — this document assumes its findings (temporal resolution mismatch = strongest confirmed root cause; simulator/estimator equivalence held; kernel misspecification ruled out; source confounding and episode dependence confirmed as independent structural risks).

---

## 0. Governing Rule (repeated verbatim, binding)

```text
Only a candidate that independently passes its own pre-registered
simulation-recovery test, on synthetic data whose generating mechanism is
known, may ever be fit against the 141 real historical events.

"Touching real data" means: running any candidate's estimator against
linimasa_events.csv (or any derived real-event table) with the intent of
producing a parameter estimate, confidence/credible interval, or model-
selection verdict about the actual archive. This is a SEPARATE, further
authorization, granted (if ever) only after recovery results are reviewed
and a specific candidate is chosen -- never automatic, never bundled with
the recovery-test authorization itself.
```

Every phase below is marked with an explicit authorization checkpoint. As of this document, **zero phases are authorized**. This document only makes each phase concrete enough to authorize individually later.

---

## 1. Sequencing and Stopping Rule

**Phase order is not arbitrary — it is chosen to spend the least compute before the most informative result.**

```text
STEP 0  (prerequisite, blocks Candidate 2 only):
        Precision-distribution audit of linimasa_events.csv's
        event_date_raw field across all 141 rows.
        Cost: trivial (a read-only pandas groupby, no fitting).
        [AUTHORIZATION CHECKPOINT A]

STEP 1  Candidate 1 (baseline count model) recovery test.
        Cheapest, fastest, and its result reframes how to read every
        other candidate's model-selection comparison.
        [AUTHORIZATION CHECKPOINT B]

STEP 2  Candidate 3 (MBPP interval-censored) recovery test.
        Second-cheapest (closed-form), directly targets the strongest
        confirmed root cause (#4/#11), and has the most existing code
        to reuse (model3_mbpp_full.py). Run before Candidate 2 because
        its result does not depend on Step 0's outcome.
        [AUTHORIZATION CHECKPOINT C]

STEP 3  Candidate 2 (continuous Hawkes, precision-verified subset) --
        ONLY IF Step 0 finds a subset of usable size (see §3, minimum-n
        rule below). If Step 0 finds the subset too small, Candidate 2
        is marked NOT_TESTABLE and the tournament proceeds without it --
        this is itself a finding (the archive lacks enough continuously-
        precise events to ever legitimately run continuous-time Hawkes),
        not a gap to route around.
        [AUTHORIZATION CHECKPOINT D]

STEP 4  Candidate 4 (Bayesian discrete-time Hawkes) recovery test.
        Run last: most expensive (MCMC), and its main comparative value
        is highest when Candidates 1 and 3's results are already known
        (it sits conceptually between them -- discrete-time like
        Candidate 1, still self-exciting like Candidate 3).
        [AUTHORIZATION CHECKPOINT E]

STOPPING CONDITION: the tournament stops after Step 4 regardless of how
many candidates pass or fail up to that point -- it is NOT a "stop at
first pass" design. Rationale: a candidate passing recovery is necessary
but not sufficient for real-data authorization (§6); comparing ALL
candidates that pass is itself required to make an informed selection
if more than one does (see §6 tie-breaking). Do not stop early even if
Candidate 1 or 3 passes cleanly.
```

Each STEP's authorization checkpoint is independent — passing Checkpoint B does not imply Checkpoint C is pre-approved. This mirrors the DEC-19 decision→implementation and Graphify authorization→build pattern already established this session: each execution step gets its own explicit go-ahead, never inherited from a prior one.

---

## 2. Candidate 1 — Baseline Count Model

**1. Synthetic data-generating process.** Simulate `count_y ~ NegativeBinomial(mean = exp(theta0 + theta1 * x_CD(y)), dispersion = phi)` per calendar year `y` in `[1600, 1784)`, using the real `x_CD(y)` series from `CD_ANNUAL_DOCUMENT_DENSITY_WORKING.csv` (not a synthetic density series — the real covariate is fully observed, no reason to simulate it). Parameter grid: reuse the blueprint's own `theta0`/`theta1` true-value grid from cells S1/S3/S4 (blueprint §8) rather than inventing a new one — those values are already calibrated to production Model 3's actual fitted range. Sweep `phi` (dispersion) across at least {Poisson limit (phi→∞), moderate overdispersion, high overdispersion} — 3 settings, since V1 never tested for overdispersion at all and this is a new axis Candidate 1 introduces.

**2. Recovery metric and pass/fail threshold.** Reuse the blueprint §9 gates verbatim for `theta0`/`theta1` only (no alpha/beta exist in this candidate): `absolute relative bias theta1 <= 0.10`, `normalized absolute bias theta0 <= 0.25`, `95% CI coverage between 0.925 and 0.975`, `sign recovery >= 0.95`. Add one new gate specific to this candidate: `dispersion parameter relative bias <= 0.15` (a threshold consistent in strictness with the existing theta1 gate, not arbitrarily looser).

**3. Sample size / replication count.** 1,000 replicates per (theta0, theta1, phi) grid cell, matching V1's per-cell replicate count (blueprint §13) so results are comparable on the same statistical footing. 3 dispersion settings x the existing theta-grid (blueprint §8 already enumerates S1/S3/S4's theta combinations) — smaller total cell count than V1's 10 cells since there is no alpha/beta axis to cross.

**4. Reuse vs. new code.** Reuse: `density.py::x_cd` (annual covariate lookup, unchanged), `CD_ANNUAL_DOCUMENT_DENSITY_WORKING.csv` (no new density data). New: a NegativeBinomial/Poisson GLM simulate+fit pair (`statsmodels.discrete.discrete_model.NegativeBinomial` or `scipy.optimize` MLE — either is standard, off-the-shelf; this is the one candidate needing genuinely new, but trivial, code, not adapted from `model3b_cd_simulator`).

**5. Root-cause attribution.** If Candidate 1 achieves comparable or better AIC/BIC than M3B-CD on production-calibrated synthetic scenarios (S3-equivalent), that independently corroborates root cause #7/#10 (the excitation term is not earning its parameter cost at this n) — it does NOT by itself prove #12 (Hawkes incompatibility), since Candidates 3/4 test resolution-matched Hawkes reformulations separately. If Candidate 1 fits noticeably worse than M3B-CD even under M3B-CD-generating conditions, that is evidence excitation IS informative at this scale, weakening #7/#10/#12 as explanations and further isolating #4/#11 (resolution mismatch) as the dominant, near-sole driver.

**6. Cost.** Trivial — closed-form or near-instant GLM fits; full sweep completes in minutes on CPU, no cluster/GPU needed.

**[AUTHORIZATION CHECKPOINT B — required before writing or running any Candidate 1 code.]**

---

## 3. Candidate 2 — Continuous-Time Hawkes, Precision-Verified Subset

**Prerequisite (Step 0, its own checkpoint).** Query `linimasa_events` for the actual precision of `event_date_raw` across all 141 rows (e.g., does the raw string carry a day, a month, a season, or only a year — the same `date_precision`-style classification already used natively in this session's power-relations artifacts, §3 of the audit notes Model 3B-CD has no equivalent field today). Output: a precision histogram and the count of events with genuine sub-year precision (`n_precise`).

**Minimum-n rule (decision criterion, not yet met/unmet — determined by Step 0's result):** if `n_precise < 40` (roughly matching the smallest per-cell n the blueprint's own gates were calibrated to detect reliably — blueprint §9's power target of `>= 0.80` was set against V1's full-141 cells, not a subset; a subset materially smaller than that has no calibrated precedent in this project and should be treated as underpowered by default unless a fresh power calculation says otherwise), mark Candidate 2 `NOT_TESTABLE_INSUFFICIENT_PRECISE_SUBSET` and stop this candidate's protocol — do not attempt a recovery test on a subset with no power justification.

**1. Synthetic data-generating process (only if `n_precise >= 40`).** Reuse `simulate.py::simulate_m3b_cd` unchanged (it already generates exactly the continuous-time process this candidate needs) at `n = n_precise` (not 141), over the same `[t0, t1]` window, at the same theta/alpha/beta true-value grid as blueprint cells S3/S5/S6 (production-calibrated and stress cells — reuse, do not re-derive).

**2. Recovery metric and pass/fail threshold.** Blueprint §9 gates verbatim, unmodified — this candidate is not proposing a new estimator, only a smaller, precision-honest input, so there is no principled reason to relax the existing thresholds.

**3. Sample size / replication count.** 1,000 replicates per cell, 3 cells (S3/S5/S6-equivalent only — S1/S2/S4/S7/S8 test axes, like false-positive rate and kernel misspecification, that are not specific to this candidate's resolution question and do not need re-running at smaller n).

**4. Reuse vs. new code.** Reuse essentially everything: `simulate.py`, `likelihood.py`, `kernel.py`, `estimate.py::fit_m3b_cd`, `validation.py` — unchanged. New: only the Step 0 precision-audit script and a subset-selection filter feeding the existing pipeline a smaller `n`.

**5. Root-cause attribution.** If this candidate passes recovery at `n_precise`, that is the cleanest possible confirmation that root cause #4 (temporal resolution mismatch), not the Hawkes family itself, was the dominant driver of V1's failure — the identical code that failed at n=141-with-fabricated-precision succeeds once given data whose precision it can honestly support. If it still fails even on genuinely precise data, weight shifts toward #7 (small-n, now doubly true since the subset is smaller than 141) and #10 (intrinsic non-identifiability, now harder to attribute to resolution alone).

**6. Cost.** Low-to-moderate — same per-replicate cost as V1's existing pipeline, but fewer cells and (likely) smaller n means materially less total compute than the original 10-cell/1,000-replicate study.

**[AUTHORIZATION CHECKPOINT A — Step 0 precision audit — required first, and is cheap/low-risk enough to reasonably request separately from Checkpoint D — the full Candidate 2 recovery test.]**

---

## 4. Candidate 3 — MBPP Interval-Censored (Rizoiu et al. 2022)

**Design note carried forward from the existing code, not invented here:** `model3_mbpp_full.py`'s own header states explicitly that its closed-form `xi(t)`/`Xi(t)` under constant background `s(t)=mu` answers a **population-mean** question (the average intensity over all possible Hawkes realizations at those parameters), not "does this fit the one observed sequence of 5 historical peaks." This is a real scope difference from V1's conditional-MLE, single-realization fit, and the protocol below is designed around it explicitly rather than glossing over it.

**1. Synthetic data-generating process.** Reuse `simulate.py::simulate_m3b_cd` (continuous-time ground truth, same as Candidate 2) to generate synthetic event times at the FULL real precision regime (n=141-equivalent, real window). Then — this is the step V1's own recovery study never performed and whose absence the audit (§4) identifies as the core design flaw — **year-bin/censor the synthetic events into annual counts**, exactly as `model3_hawkes_kaskade_event.py` would represent the real archive (i.e., discard the continuous timestamps entirely after generation, keep only per-year counts, matching how MBPP's `neg_ic_ll` already expects `bin_edges, counts` — reuse that exact input contract, do not invent a new one). Fit via `neg_ic_ll` against `xi_closed_form`/`Xi_closed_form`, minimizing over `(mu, alpha, beta)`.

**2. Recovery metric and pass/fail threshold.** Blueprint §9 gates for `alpha`, `beta`, and `branching_ratio` (bias, CI coverage — note MBPP's optimizer returns a point estimate + Hessian-based SE via `scipy.optimize.minimize`, from which a Wald CI can be constructed the same way V1's does, so the existing coverage-gate machinery applies without modification). **Explicitly do NOT apply the theta0/theta1 gates here** unless a density-covariate term is added to the MBPP formulation first (the existing `model3_mbpp_full.py` implements the pure-Hawkes case only, per its own scope note — extending it to include `x_CD(t)` in `s(t)` is new work this protocol flags as a prerequisite sub-step, not assumed already done).

**3. Sample size / replication count.** 1,000 replicates, same cell structure as Candidate 2 (S3/S5/S6-equivalent theta/alpha/beta grid) — full n=141-equivalent this time, since censoring (not subsetting) is the fix being tested.

**4. Reuse vs. new code.** Reuse: `simulate.py` (ground-truth generator), `model3_mbpp_full.py::xi_closed_form/Xi_closed_form/neg_ic_ll` (the closed-form MBPP machinery, already implemented and already exercised once on production parameters). New, and this is the real implementation cost of this candidate: (a) extending `neg_ic_ll`'s `s(t)` term to include `theta0 + theta1*x_CD(t)` rather than constant `mu` alone, since M3B-CD's whole point is the density covariate and the existing MBPP code does not yet have it; (b) a recovery-test harness (parameter sweep, replicate loop, gate evaluation) analogous to `model3b_cd_simulator`'s existing harness but wired to the MBPP fit function instead of `estimate.py::fit_m3b_cd`.

**5. Root-cause attribution.** If this candidate passes recovery, that is strong, literature-grounded evidence that root causes #3/#4/#11 (wrong variable representation / resolution mismatch / unrepresentative recovery design) were the correctable problem, and that a properly resolution-matched Hawkes-family model CAN be identified from this archive — directly informative for root cause #12 (ruling out "Hawkes family is categorically wrong," at least for this specific reformulation). If it still fails to separate alpha/beta from theta0/theta1 even with correct censoring, that is materially stronger evidence for #10 (intrinsic non-identifiability) than V1's result, since the resolution confound is removed.

**6. Cost.** Moderate — closed-form intensity/compensator (no numerical integration), so per-replicate cost is comparable to or cheaper than V1's own MLE fits; the density-covariate extension (item 4a above) is the main new-development cost, not the recovery study itself.

**[AUTHORIZATION CHECKPOINT C — required before extending `model3_mbpp_full.py` or running any Candidate 3 recovery test.]**

---

## 5. Candidate 4 — Bayesian Discrete-Time Hawkes

**1. Synthetic data-generating process.** Simulate discrete annual (or, if annual proves too sparse per-bin, 3-year-binned — a fallback explicitly noted, not assumed) count sequences from a known discrete self-exciting process (e.g., a log-linear Hawkes-INGARCH form: `log(lambda_y) = theta0 + theta1*x_CD(y) + sum_{k>=1} alpha*beta^k * count_{y-k}`, a direct discrete-time analogue of the continuous kernel already in `kernel.py`, chosen for structural continuity with the rest of this project's model family rather than importing an unrelated discrete-process formulation). Same theta/alpha/beta grid as Candidates 2/3, same `[1600, 1784)` window at annual grain.

**2. Recovery metric and pass/fail threshold.** Bayesian analogues of the blueprint §9 gates, explicitly mapped (not a different standard, a translated one): `95% CI coverage` → `95% posterior-credible-interval coverage`, same `[0.925, 0.975]` band; `false-positive excitation <= 0.05` → posterior probability `P(alpha > 0 | data) <= 0.05` under `alpha_true = 0` simulations (S1-equivalent); `correct-model-selection rate >= 0.80` → WAIC/LOO correctly favors the true generating model (M3B-CD-discrete vs. density-only-discrete) in `>= 0.80` of production-calibrated (S3-equivalent) replicates — WAIC/LOO chosen specifically because §1 row 10 of the audit found AIC/BIC's specific failure mode holds even under correct and misspecified kernel form, so carrying AIC/BIC forward unchanged into this candidate would import a known-bad instrument rather than test the candidate fairly.

**3. Sample size / replication count.** Full V1-scale replication (1,000/cell) is not proposed as the default here given MCMC cost — protocol default: **200 replicates/cell** for an initial pass, with an explicit note that this is a **reduced-power diagnostic run**, not a confirmatory study on Phase D's own standard (9 arms x 10,000 sims). If the reduced run shows a candidate clearly failing or clearly passing all gates with room to spare, that is sufficient for a go/no-go read without the full 1,000. If results are borderline (near any gate's threshold), a follow-up authorization to scale to 1,000 replicates would be a separate, explicitly justified request — not silently assumed.

**4. Reuse vs. new code.** Reuse: `density.py::x_cd`, the theta/alpha/beta grid definitions, the gate-evaluation harness structure (conceptually, not literally — the pass/fail logic pattern from `estimate.py`/`validation.py` is a template, not directly importable since the estimator itself is fully new). New: the entire discrete Hawkes-INGARCH generative model, and a Bayesian fitting routine (PyMC or Stan via `cmdstanpy`/`pymc`, neither currently a project dependency — a new dependency this protocol flags explicitly, not silently assumed available). This is the candidate with the largest genuinely-new implementation surface of the four.

**5. Root-cause attribution.** Passing recovery here would demonstrate that (a) discrete-time binning alone (independent of MBPP's censored-likelihood machinery) resolves the resolution mismatch, and (b) informative priors resolve the small-n CI-undercoverage problem V1's Wald intervals showed (postmortem §5) — jointly addressing #4 and #7/#10 through a different mechanism than Candidate 3. If Candidates 3 and 4 both pass, their comparison (§6) becomes informative about whether censored-likelihood or discretization is the more parsimonious fix; if only one passes, that is a direct answer.

**6. Cost.** Highest of the four — MCMC per replicate is materially more expensive than L-BFGS-B point estimation; even the reduced 200-replicate/cell run should be expected to be the single most compute-intensive step in this tournament, and a full 1,000-replicate scale-up (if ever authorized) substantially more so.

**[AUTHORIZATION CHECKPOINT E — required before adding any new Bayesian-fitting dependency or writing/running any Candidate 4 code.]**

---

## 6. Go/No-Go to Real Data — Operationalized

```text
IF zero candidates pass their own recovery test:
    No candidate is authorized to touch real data. Report findings,
    stop. This would itself be informative -- it would mean the
    identified root causes (resolution mismatch, source confounding,
    episode dependence, small-n complexity) are not fixable by any of
    the four reformulations tried, strengthening #12 (Hawkes-family
    incompatibility) as the leading remaining explanation.

IF exactly one candidate passes:
    That candidate becomes eligible for a SEPARATE, explicit real-data
    fitting authorization request -- passing recovery is necessary, not
    sufficient. The real-data request must additionally address root
    cause #5 (source-observation confounding, 59.6% CD-dependency,
    Phase B) and #6 (parent/child episode dependence, Sas expedition =
    47.2% of pairs, Phase D) BEFORE fitting, since neither is resolved
    by any of the four candidates as scoped in this protocol -- both
    remain independent blockers per audit §1 rows 5-6, regardless of
    which candidate (if any) passes its recovery test.

IF more than one candidate passes:
    Tie-breaking order, most-to-least preferred, and NOT decided
    automatically -- presented to the researcher as a recommendation
    template only:
      1. Prefer the candidate with the narrowest, most literature-
         grounded scope match to the actual research question (per
         audit §1 row 12's framing: "self-excitation tetap diperlukan
         setelah mengontrol densitas CD" -- a candidate that answers
         exactly this question, not a broader or narrower one, is
         preferred over one that answers an adjacent question, e.g.
         MBPP's population-mean scope note in §4 above).
      2. Prefer the candidate requiring the smaller number of new,
         unverified implementation components (Candidate 1 < Candidate
         3 < Candidate 2 (if testable) < Candidate 4, per the "reuse
         vs. new code" sections above).
      3. Prefer the candidate whose recovery-test margins (how far
         inside each gate's threshold it landed, not merely pass/fail)
         are largest -- a candidate that barely clears every gate is a
         weaker basis for real-data claims than one with comfortable
         margins, even though both formally "pass."
    This ordering is a DEFAULT to propose, not a rule the researcher is
    bound by -- final selection remains a researcher decision.

IN ALL CASES: authorization to fit real data is a distinct future
request, never implied by a recovery-test pass, and must explicitly
re-confirm the source-confounding and episode-dependence blockers are
either resolved or explicitly and separately waived before proceeding.
```

---

## 7. Summary Table (execution view, complements audit §5's design view)

| Candidate | Step | Prerequisite | Est. cost | New deps | Checkpoint |
|---|---|---|---|---|---|
| 1. Baseline count | 1 | none | trivial | statsmodels NB/Poisson (likely already available) | B |
| 3. MBPP interval-censored | 2 | none | moderate | none (extends existing `model3_mbpp_full.py`) | C |
| 2. Continuous Hawkes, precise subset | 3 | Step 0 precision audit, `n_precise >= 40` | low-moderate (if testable) | none | A then D |
| 4. Bayesian discrete-time | 4 | none | highest (MCMC) | PyMC or cmdstanpy (new) | E |

---

## 8. What This Protocol Does and Does Not Authorize

```text
AUTHORIZES (by writing this document): nothing. This is a plan.

DOES NOT AUTHORIZE: writing simulation or estimation code for any
candidate; running any recovery test; the Step 0 precision audit itself
(cheap and low-risk, but still a new script touching real data read-only
-- requires Checkpoint A explicitly, not bundled with this document);
adding new dependencies (PyMC/cmdstanpy for Candidate 4); fitting any
candidate against real data under any circumstance; rerunning V1 or
Phase D; modifying any existing file in model3b_cd_simulator/ or
model3_mbpp_full.py in place (any extension, e.g. the density-covariate
addition for Candidate 3, would be new code alongside the existing
files, not an in-place rewrite of frozen research code, consistent with
this project's standing "no in-place rewriting of frozen artifacts"
discipline applied elsewhere this session).
```

**STOP** — protocol complete. No Model V2 implemented, no recovery test run, no V1 or Phase D rerun, no data changed, nothing staged, committed, pushed, or deployed.
