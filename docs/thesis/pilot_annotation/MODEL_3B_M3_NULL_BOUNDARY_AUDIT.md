# Model 3B — M3 Null-Boundary Audit (Phase D)

> **Diagnostic audit only. No full tournament rerun. No historical data. Nothing staged/committed/pushed.**
> **Current admissible status carried forward from the pilot facts (not re-derived, not drifted):**
> `M3_NULL_BOUNDARY_PARAMETERIZATION_DEFECT_SUSPECTED`, `M3_CURRENT_VERDICT_NOT_INTERPRETABLE`
> **Note:** this is Phase D of the *diagnostic audit* (§8 of the governing instruction) — unrelated to, and not to be confused with, the project's separate "Phase D" (the 9-arm/90,000-simulation residual-clustering test, already `COMPLETED_VALID_NEGATIVE_RESULT` and explicitly not rerun anywhere in this turn).

---

## 1. Exact null support — direct code inspection

Source: `docs/thesis/colab/model3b_tournament_harness/m3_bayesian_discrete.py`, `_from_unconstrained`:

```python
def _from_unconstrained(u: np.ndarray) -> tuple[float, float, float, float]:
    theta0, theta1, logit_n, log_beta = u
    n_branch = 1.0 / (1.0 + math.exp(-logit_n))
    ...
```

This is the standard logistic (expit) transform. For **any finite** `logit_n` — and the unconstrained-space random-walk Metropolis-Hastings sampler (`fit_m3_mcmc`) only ever proposes and evaluates finite real numbers — `n_branch` is **strictly** in the open interval `(0, 1)`. `n_branch = 0` requires `logit_n = -infinity`, which has probability zero of ever being proposed or accepted by a random-walk sampler on the unconstrained scale.

**Per the governing instruction's own §8.1 formula**: "If `n = logit^{-1}(η)`, then finite `η` implies `0 < n < 1`. Therefore exact `n=0` is absent unless the model has an explicit null component." Direct inspection confirms: **M3 has no explicit null component.** `n=0` is not in the parameter support of this sampler, full stop.

- **Transform**: `expit`, as above — confirmed.
- **Epsilon clipping**: none found in `_from_unconstrained`; no additional clamp is applied to `n_branch` itself (unlike `log_phi` in M0's driver, which IS clamped `[-20,20]` — M3's `logit_n` has no equivalent explicit range clamp, but the expit transform itself already guarantees `(0,1)` regardless).
- **Prior support**: `log_prior` (read in full) places weakly-informative priors on the unconstrained parameters, not directly on `n` in a way that would exclude any part of `(0,1)` — the prior does not itself force positivity beyond what the transform already guarantees structurally.
- **Initialization**: MCMC chains are initialized via `_to_unconstrained` applied to a starting point, which itself passes through the same one-way `logit`/`expit` pairing — initialization cannot start the chain at `n=0` either.
- **Sampler**: random-walk Metropolis-Hastings on the unconstrained 4-vector `(theta0, theta1, logit_n, log_beta)` — proposals are Gaussian perturbations of finite reals, so all proposed states remain in the finite-`logit_n` regime, hence `n∈(0,1)` always.
- **Posterior summary / decision rule**: see §2 — this is where the structural gap becomes a *scored* failure.

## 2. Does the decision rule mechanically force excitation? (§13 question 9)

Source: `docs/thesis/colab/model3b_tournament_harness/run_recovery_m3.py`, `run_cell`:

```python
lo, hi = np.percentile(post.samples[k], [2.5, 97.5])
covered[k].append(lo <= true_v <= hi)
if k == "n" and n_true == 0.0:
    n_positive_flags.append(lo > 0.0)
```

The false-positive decision rule for the `n_true = 0` cell (`S1-equiv-n0`) is: **flag a false positive if the 95% credible interval's lower bound exceeds exactly 0.0.**

Given §1's finding — every single posterior draw of `n` is strictly greater than 0 by construction — the 2.5th percentile of *any* finite MCMC sample of `n` will also be strictly greater than 0 (a sample of continuous values, all > 0, has a 2.5th percentile that is itself > 0, essentially without exception at any practical posterior concentration). **The decision rule `lo > 0.0` is therefore true by construction, independent of the true data-generating process, independent of the data actually observed, and independent of whether the model correctly infers "no real excitation."**

**Confirmed observed result**: `false_positive_excitation_rate = 1.0` at the `S1-equiv-n0` cell (`m3_summary.csv`), exactly as this mechanical analysis predicts, with 200/200 replicates all producing `lo > 0.0`.

**This directly answers instruction §13 question 9**: **Yes — the decision rule mechanically forces excitation-detection at the null cell, confirmed by direct inspection of the transform code (§1) and the decision-rule code (§2), not inferred from the 100% rate alone (a 100% rate is consistent with, but does not by itself prove, a structural cause — the code-level proof is what makes this conclusive rather than merely suggestive).**

## 3. Candidate null designs (§8.2 — analyzed, not implemented)

| Design | Mechanism | Would fix the boundary artifact? |
|---|---|---|
| **Explicit `H0: n=0` vs `H1: 0<n<1` comparison** | A discrete model-comparison step (e.g. Bayes factor, or a two-stage fit: fit the `n=0`-constrained model and the free model separately, compare via WAIC/LOO) | Yes — `n=0` becomes a genuinely reachable, explicitly tested hypothesis rather than a limit the continuous parameterization can only approach |
| **Spike-and-slab** (`z ~ Bernoulli(π)`, `n = 0` if `z=0` else `ñ`) | Adds a discrete latent indicator; posterior `P(z=0 \| data)` is the natural false-positive-rate statistic, replacing `lo > 0.0` | Yes — directly gives `P(\text{no excitation} \| data)` as a first-class quantity |
| **Hurdle model** | Separates "does excitation exist at all" (a Bernoulli/logistic sub-model) from "how much, given it exists" (the continuous `n>0` magnitude) | Yes — same structural fix as spike-and-slab, framed as two linked sub-models rather than one mixture |
| **Region of practical equivalence (ROPE)**, `0 <= n <= epsilon_n` | Keep the current continuous parameterization; redefine "false positive" as `lo > epsilon_n` for a preregistered, non-zero `epsilon_n` | Partially — avoids the exact-zero impossibility, but **`epsilon_n` must not be chosen automatically** (governing instruction §8.2 explicit prohibition) — it requires either literature support (e.g. a domain-specific "negligible excitation" threshold) or an explicit researcher policy decision, and picking it post-hoc after seeing this result would risk the exact "post-hoc relaxation" pattern §9 of the instruction requires flagging |

No design is selected or implemented here. All four remain researcher-decision items — see `MODEL_3B_GATE_AMENDMENT_PROPOSAL.md`.

## 4. Primary classification

```text
NULL_NOT_IN_PARAMETER_SUPPORT
```

with `DECISION_RULE_INVALID` recorded as the direct, confirmed downstream mechanism (not a competing alternative — both are true and causally linked: the parameter-support gap in §1 is *why* the decision rule in §2 is invalid, not two independent findings).

Explicitly **not** classified `GENUINE_FALSE_POSITIVE_MODEL_FAILURE`: per the governing instruction's own closing line in §8.3, "the 100 percent FPR is not interpretable as substantive failure until exact-null support and the decision rule are valid" — and this audit has now directly demonstrated (not merely asserted) that neither is currently valid, via code inspection of both the transform (§1) and the decision rule (§2). There is no evidence in this audit that M3, if paired with a null design that actually admits `n=0`, would exhibit a genuine excessive false-positive tendency — that question remains open and untested, not answered negatively either.

## 5. Secondary finding — branching-ratio bias at non-null cells

GATE-033/034 (branching-ratio bias) fail even at the three non-null cells (`S3/S5/S6-equiv`, true `n=0.6769`): absolute bias 0.134–0.135, relative bias 0.198–0.199 — roughly double the GATE-033 threshold (0.05) and double the GATE-034 threshold (0.10). This is **not** explained by the null-boundary mechanism above (these cells have `n_true > 0`, comfortably away from the `n=0` boundary), so it is recorded separately in the gate classification CSV as `VALID_GATE_VALID_FAILURE`, not re-attributed to the boundary artifact. It is milder than M2's raw individual-alpha failure (M2: 4,450–5,480% relative bias on alpha; M3: ~20% relative bias on `n` directly) — consistent with M3's discrete-time, direct-`n`-parameterization design intentionally avoiding M2's continuous-time alpha/beta split, even though it does not yet clear the gate outright.

## 6. What this does not authorize

- Does not authorize implementing any of the four candidate null designs in §3.
- Does not authorize re-running M3 at any scale, reduced or full.
- Does not change GATE-030's frozen `<=0.05` threshold or GATE-035's frozen `[0.925, 0.975]` band.
- Does not conclude the Hawkes/self-exciting family is falsified by this result — the finding is specific to this parameterization-and-decision-rule pairing, not to the underlying discrete self-exciting count-process model class.
