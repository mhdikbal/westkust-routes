# Model 3B — M0 Interval-Coverage Audit (Phase B)

> **Diagnostic audit only. No tournament rerun at scale. No historical data. Nothing staged/committed/pushed.**
> **Current admissible status carried forward from the pilot facts (not re-derived, not drifted):** `M0_INFERENCE_INTERVAL_IMPLEMENTATION_REQUIRES_REVIEW`

---

## 1. Reconstructed from executed code

Source: `docs/thesis/colab/model3b_tournament_harness/run_recovery_m0.py` (the actual driver executed for the pilot; `m0_baseline.py::fit_m0_poisson` was NOT the code path used for the dispersion-axis cells — the driver adds an inline NB fit, `fit_nb`, documented explicitly in its own docstring as "does not modify m0_baseline.py").

| Item | Value |
|---|---|
| Distribution | Negative Binomial, mean-dispersion parameterization (`phi`=size); `phi=None` branch reduces to Poisson (`poisson_limit` dispersion setting) |
| Likelihood | `neg_loglik_nb`: `gammaln(k+phi) - gammaln(phi) - gammaln(k+1) + phi*log(p) + k*log(1-p)`, `p = phi/(phi+mean)`, `mean = exp(theta0 + theta1*x_CD)` |
| Parameter vector/order | `[theta0, theta1, log_phi]` (3-vector passed to `scipy.optimize.minimize`) |
| Link function | log-link on the mean: `log(mean_t) = theta0 + theta1 * x_CD(year)` |
| Dispersion (`phi`) convention | `log_phi` unconstrained, clamped `[-20, 20]` inside the likelihood (`min(max(log_phi,-20),20)`) before `phi = exp(log_phi)` — this clamp is what fixed the earlier `OverflowError` crash (pilot fact §3.1); it does not otherwise affect the CI question here |
| Optimizer | `scipy.optimize.minimize`, `method="L-BFGS-B"`, `bounds=[(None,None),(None,None),(-20,20)]` |
| Initialization | `x0 = (log(mean_count), 0.0, log(3.0))` for the poisson_limit cells (explicit `x0` passed in `run_cell`); default `(log(mean_c), 0.0, log(3.0))` otherwise |
| Restart policy | None — single L-BFGS-B call per replicate, no multi-start |
| Interval construction | **Numeric, central finite-difference, diagonal-only** — see §2 |
| Finite-difference step | `eps = 1e-3` (fixed, not adaptive to parameter scale) |
| Covariance construction | `se0 = sqrt(1/f00)`, `se1 = sqrt(1/f11)` where `f00`, `f11` are the diagonal second partials of the NLL — **no off-diagonal (cross) term is ever computed** |
| Final interval | `abs(est - true) <= 1.96 * se` (this is coverage-checking code, not literally an interval object, but mathematically equivalent to a symmetric Wald interval `[est - 1.96*se, est + 1.96*se]`) |

## 2. Hessian convention audit

The instruction's governing convention (§4.2 of the master instruction): for a function that is **minimized** (the NLL, as here), `Cov(θ̂) = [H_NLL(θ̂)]^{-1}`, where `H_NLL` is the **full** Hessian matrix of the negative log-likelihood.

The executed code (`run_recovery_m0.py::run_cell`, lines ~122–134):

```python
eps = 1e-3
def nll2(t0v, t1v):
    return neg_loglik_nb([t0v, t1v, math.log(max(est_phi, 1e-6))], counts, YEAR_COV)
f00 = (nll2(est_t0+eps, est_t1) - 2*nll2(est_t0, est_t1) + nll2(est_t0-eps, est_t1)) / eps**2
f11 = (nll2(est_t0, est_t1+eps) - 2*nll2(est_t0, est_t1) + nll2(est_t0, est_t1-eps)) / eps**2
se0 = sqrt(1/f00) if f00 > 1e-9 else nan
se1 = sqrt(1/f11) if f11 > 1e-9 else nan
```

- **Sign**: correct for the minimize convention — `f00`/`f11` are second derivatives of the NLL itself (not the log-likelihood), and `1/f00` is taken directly without an extra negation, matching `[H_NLL]^{-1}` on the diagonal.
- **Parameter order / scale**: consistent, no transformation-back issue (theta0/theta1 are used directly, not on a further-transformed scale).
- **Conditioning / positive definiteness**: only checked per-diagonal-element (`f00 > 1e-9`), never for the full matrix, because the full matrix is never assembled.
- **Inversion fallback**: none needed because no matrix is ever inverted — only two independent scalar reciprocals are taken.
- **The defect**: `phi` is treated as a plug-in nuisance parameter (fixed at `est_phi`) when computing `f00`/`f11`, which is a defensible simplification (profiled-out nuisance), but **the off-diagonal term between `theta0` and `theta1`, `∂²NLL/∂theta0∂theta1`, is never computed at all.** The code effectively assumes `Cov(theta0, theta1) = 0` — that the joint 2×2 Fisher information matrix is diagonal. For a GLM where `theta1` multiplies a covariate `x_CD(year)` and `theta0` is the intercept on the same log-link, this assumption is generically false; intercept and slope estimates in this kind of model are correlated by construction (they are jointly estimated from the same likelihood surface, and `x_CD` is not mean-centered).

## 3. Small synthetic oracle (diagnostic-only, not staged)

Per §6.3, a small fixed-seed comparison was run to test whether coverage improves under a valid alternative interval construction, using the identical simulate → fit pipeline as the pilot, one representative cell (`S3-equiv`, `theta0=-1.357513, theta1=0.1, phi=5.0`, moderate overdispersion), reduced replicate count for tractability (`n=60`, not the pilot's 1,000 — this is explicitly a small oracle, not a re-run of the pilot at scale).

**Script**: `/tmp/model3b_diag/m0_ci_diagnostic.py` — `DIAGNOSTIC_ONLY`, fixed seeds (`rng_base=900000`, replicate `i` uses seed `900000+i`), never staged, saved outside `recovery_results/`, no historical data, uses only the identical synthetic NB generator and `neg_loglik_nb`/`fit_nb` functions already in the pilot's own driver (imported logic reproduced inline for isolation, not modified).

**Compared**:
1. **Pilot's actual method** — diagonal-only finite-difference Hessian (reproduced exactly).
2. **Corrected** — full 2×2 finite-difference Hessian (adds the cross term `f01 = ∂²NLL/∂theta0∂theta1` via a 4-point central-difference stencil), inverted as a matrix (`np.linalg.inv`), diagonal of the inverse gives `Var(theta0)`, `Var(theta1)`.
3. **Small parametric bootstrap** — `R=50` per replicate, evaluated on every 15th replicate only (n=4 replicates get a bootstrap CI, for cost reasons within a small-oracle budget) — refit the NB model on data simulated from each replicate's own MLE, form a percentile interval.

**Result** (theta1 coverage, target band `[0.925, 0.975]`):

```text
n_valid_replicates=60
PILOT METHOD (diagonal-only Hessian) theta1 coverage: 0.450  (n=60)
CORRECTED (full 2x2 Hessian inverse) theta1 coverage: 0.933  (n=60)
Parametric bootstrap (R=50/replicate, every 15th)     theta1 coverage: 1.000  (n=4, too few to be conclusive alone)
mean SE(theta1) diagonal-only: 0.07713
mean SE(theta1) full-Hessian:  0.18478
ratio (full/diag): 2.396
```

The diagonal-only SE is **2.4× too small** relative to the full-Hessian SE. This single correction moves theta1 coverage from 0.450 (consistent in direction and rough magnitude with the pilot's own reported 0.544–0.615 range, and well outside it is not surprising given this is a different cell and a much smaller n=60 sample) into the target band (0.933, inside `[0.925, 0.975]`). The bootstrap result (n=4) points the same direction but is too small a sample to be independently conclusive — reported for transparency, not as confirming evidence on its own.

**This directly answers instruction §13 question 3** ("Does M0 coverage improve under a valid alternative interval on a small oracle?"): **YES**, substantially and in the direction and rough magnitude predicted by the code-level defect identified in §2.

## 4. Primary classification

```text
STANDARD_ERROR_IMPLEMENTATION
```

Selected over the alternatives because:
- **Not** `MODEL_MISSPECIFICATION` — GATE-001 and GATE-004 (invalid-estimate rate, point-estimate bias) both pass across all 15 cells; the generative NB/Poisson model and its point estimator are sound.
- **Not** `FINITE_DIFFERENCE_INSTABILITY` — the fixed `eps=1e-3` step is a secondary, smaller concern (not tested in isolation here, since the oracle already isolates and confirms the larger, structural cause); the diagonal-only omission is sufficient by itself to explain the observed undercoverage direction and rough magnitude.
- **Not** `HESSIAN_SIGN_OR_SCALE_ERROR` — the sign convention (§2) is verified correct for the minimize case; there is no sign or scale bug, only a missing term.
- **Not** `DELTA_METHOD_ERROR` — no parameter transformation is being back-transformed incorrectly here (theta0/theta1 are used on their native scale).
- **Not** `BOUNDARY_EFFECT` — GATE-007's failure is uniform across all 15 cells including ones far from any parameter boundary (e.g. `S1-G3` at `theta0=-0.665532`), not concentrated near boundaries.
- **Not** `SMALL_SAMPLE_APPROXIMATION` — the pilot's own scale (1,000 replicates/cell, ~184 annual bins per replicate) is not small in the sense this classification would imply; the oracle's smaller n=60 was a deliberate diagnostic choice, not evidence the pilot itself was underpowered for this question.
- **Not** `DISPERSION_CONVENTION_MISMATCH` — the mean-dispersion NB convention (§4.3 of the master instruction) is used consistently in `simulate_nb_counts` (generator) and `neg_loglik_nb` (estimator); both use `p = phi/(phi+mean)` with the same `phi`/`mean` roles, so generator and estimator agree.

## 5. A valid point estimator with an invalid CI is not a substantive model failure

Per the instruction's own §6.4 closing principle: GATE-001, GATE-004, and GATE-037 (invalid-estimate rate, point-estimate bias, convergence rate) all pass cleanly across every one of the 15 pilot cells. The failure is entirely confined to GATE-007 (interval coverage), and the oracle in §3 traces that failure to a specific, correctable line of code (the missing off-diagonal Hessian term), not to the NB/Poisson model class, the link function, the dispersion convention, or the optimizer. **M0 as a model is not falsified by this pilot; M0's interval-construction code, as executed, is.**

## 6. What this does not authorize

- Does not authorize adopting the corrected CI construction into the pilot codebase (that is an amendment requiring researcher approval — see `MODEL_3B_GATE_AMENDMENT_PROPOSAL.md`).
- Does not authorize re-running M0 at the full 1,000-replicate/cell scale with a corrected CI (a separate execution authorization).
- Does not change GATE-007's frozen `[0.925, 0.975]` threshold — the target itself is not in question, only the implementation that is supposed to meet it.
