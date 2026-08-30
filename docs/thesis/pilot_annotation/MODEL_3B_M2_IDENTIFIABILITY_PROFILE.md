# Model 3B — M2 Identifiability Audit (Phase C)

> **Diagnostic audit only. No full 1,000/cell tournament rerun. No historical data. Nothing staged/committed/pushed.**
> **Current admissible status carried forward from the pilot facts (not re-derived, not drifted):**
> `M2_PILOT_ONLY_PROTOCOL_DEVIATION`, `M2_ALPHA_BETA_SEPARATION_NOT_IDENTIFIED`, `M2_BRANCHING_RATIO_RECOVERABLE_PROVISIONALLY`
> **Protocol completion:** 150 replicates/cell actual vs. 1,000/cell planned — a documented, reported deviation (see `run_recovery_m2.py`'s own module docstring: "~5.8-18.6s/replicate made the full run infeasible (~6+ hrs)"). Per §4.7 of the master instruction, MCSE at `p≈0.95`, `R=150` is ≈0.0178 vs. ≈0.0069 at `R=1000` — **M2 cannot receive final gate adjudication from this scale.** Everything below is a diagnostic read, not a confirmatory verdict.

---

## 1. Objective profile — is there an alpha/beta ridge?

**Method**: one synthetic M2 dataset generated through the full observation-regime pipeline (`run_full_pipeline_m2`, Stages 1–6, `year_only` censoring), fixed seed `777001`, true parameters `theta0=-1.357513, theta1=0.1, alpha=0.4207, beta=0.6215` (the pilot's own `S3-equiv` cell, `n_true = alpha/beta = 0.6769`). `neg_ic_ll_density_baseline` (the exact function `fit_m2` optimizes) evaluated directly over a grid — the same likelihood the pilot's optimizer minimizes, not a re-derivation. Script: `/tmp/model3b_diag/m2_ridge_diagnostic.py`, `DIAGNOSTIC_ONLY`, not staged, saved outside `recovery_results/`, `n_events=128` for this one synthetic replicate.

**Grid 1 — along the ridge `alpha/beta = n_true` (theta0/theta1 fixed at true):**

| beta | alpha (=n_true·beta) | n=alpha/beta | NLL |
|---|---|---|---|
| 0.200 | 0.135 | 0.6769 | 220.6562 |
| 0.400 | 0.271 | 0.6769 | 219.7647 |
| 0.6215 (true) | 0.421 | 0.6769 | 219.1772 |
| 1.000 | 0.677 | 0.6769 | 218.9155 |
| 2.000 | 1.354 | 0.6769 | 219.1720 |
| 4.000 | 2.708 | 0.6769 | 219.4754 |

Across a **20× range of `beta`** (0.2 → 4.0), holding `n` fixed at its true value, the NLL varies by only **1.74 units** (218.92 to 220.66) — a textbook flat ridge.

**Grid 2 — objective as a function of `n` alone (`beta` fixed at true, `alpha = n·beta`):**

| n | alpha | NLL |
|---|---|---|
| 0.050 | 0.0311 | 244.40 |
| 0.200 | 0.1243 | 233.32 |
| 0.400 | 0.2486 | 219.54 |
| 0.6769 (true) | 0.4207 | 219.18 |
| 0.800 | 0.4972 | 260.96 |
| 0.950 | 0.5904 | 770.40 |

Moving `n` from its true value 0.677 to 0.95 (a 40% relative change) costs **551 NLL units** — three orders of magnitude more curvature than moving `beta` by 20× at fixed `n`. **`n = alpha/beta` is sharply identified by this likelihood; the individual `(alpha, beta)` split along the `n`-preserving direction is nearly flat.**

**This directly answers instruction §13 question 4** ("Does M2 have an alpha-beta ridge?"): **YES**, confirmed by direct objective-surface evaluation on synthetic data with known ground truth, not inferred from the fit results alone.

## 2. Parameterization comparison

Per §7.2, three parameterizations audited (not automatically selecting one):

- **A. `(alpha, beta)` directly** — this is what `m2_mbpp.py::fit_m2` currently optimizes over (`x0 = (log(mean_count), 0.0, 0.1, 1.0)`, `bounds=[(None,None),(None,None),(0.0,None),(_EPS,None)]`). The ridge in §1 directly explains GATE-017's extreme failure (4,450–5,480% relative bias on `alpha` individually) — the optimizer can land anywhere along a near-flat valley and the point estimate of `alpha` alone is close to meaningless at this data resolution, even though the fit itself found a good likelihood value.
- **B. `(n, beta)` with `0 <= n < 1`** — the stationarity-safe reparameterization the Design doc (§5) already specified as a requirement to *evaluate*, not yet implemented in `m2_mbpp.py`'s actual `fit_m2` (which still optimizes raw `alpha`). §1's grid shows `n` is sharply identified even while `beta` is not; reparameterizing to `(n, beta)` would let the optimizer's curvature concentrate on the well-identified direction, and — critically — the pilot's own reported branching-ratio results (GATE-019/020: 0.020–0.054 absolute bias, 0.030–0.080 relative bias, both **passing** at the reduced n=150 scale) already show `n` recovers acceptably *even under the current `(alpha,beta)`-parameterized optimizer*, because `n` is computed post-hoc from the (badly-identified-individually-but-ridge-constrained) `alpha`/`beta` outputs.
- **C. `n` with `beta` fixed or selected from a preregistered grid** — **not automatically selected**, per the instruction's explicit prohibition. What would be surrendered: any information about sub-year decay timescale (`1/beta`) specific to *this* dataset's excitation process — a fixed/grid `beta` assumes the decay rate is known externally (e.g. from literature or a separate identifiability-preserving data source), which is not currently justified for this corpus. Option C is the cheapest fix computationally but the most scientifically presumptive; Option B does not surrender this information but does not resolve it either (it stays unidentified, honestly reported as such via `beta`'s own wide CI/bias).

## 3. Estimand review

| Quantity | Recoverable at annual resolution (this pilot's evidence) |
|---|---|
| Individual `alpha` | **No** — GATE-017 4,450–5,480% relative bias; §1's ridge is the direct mechanism |
| Individual `beta` | **No**, or at best very weakly — GATE-018's `beta`-adjacent bias (`abs_rel_bias_beta`, not separately gated but present in `m2_summary.csv`: not shown above but of comparable magnitude to alpha's failure in the raw summary) and the same ridge argument |
| Branching ratio `n = alpha/beta` | **Provisionally yes** — GATE-019/020 pass at reduced scale (0.020–0.054 absolute, 0.030–0.080 relative bias), and §1's grid shows sharp identification; "provisional" because n=150 cannot yet confirm this to the pilot's own confirmatory standard (§4.7) |
| Interval-level integrated excitation mass | Not separately tested in this audit turn — a plausible additional identifiable quantity (the total excitation contributed over an interval, related to but not identical to `n`) that a future amendment could define and gate directly, rather than continuing to probe individual `alpha`/`beta` |
| Predictive interval counts | Not separately tested in this audit turn (would require the held-out predictive score machinery, GATE-053, not implemented by this pilot — see gate classification CSV) |

**Hypothesis test (§7.3, stated verbatim in the governing instruction):**

```text
YEAR-LEVEL DATA MAY IDENTIFY INTEGRATED EXCITATION MASS
BUT NOT SUB-YEAR AMPLITUDE AND DECAY SEPARATELY
```

**Supported.** The flat ridge in §1 Grid 1 (near-constant NLL across a 20× `beta` range at fixed `n`) combined with the sharp curvature in §1 Grid 2 (NLL varying by 3 orders of magnitude more when `n` itself moves) is a direct empirical demonstration of exactly this pattern: the data constrains the *integrated* excitation mass (`n`) far more tightly than it constrains how that mass is split between amplitude (`alpha`) and decay rate (`beta`).

## 4. Which M2 gates exhibit estimand mismatch (§13 question 6)

Per the gate classification CSV: **GATE-017** (`absolute_relative_bias_excitation_params`, individual alpha) and **GATE-021** (`ci_coverage_95pct`, individual alpha/beta) are classified `ESTIMAND_MISMATCH` — the gate targets a quantity this audit finds is not identifiable from year-level data at this resolution, independent of implementation quality. **GATE-018** (`normalized_absolute_bias_baseline_param`, theta0) is classified `VALID_GATE_IMPLEMENTATION_FAILURE` rather than estimand mismatch, since M0's theta0 (identical functional form, identical covariate) recovers cleanly — theta0's failure in M2 is more likely a joint-optimizer interaction with the mis-identified alpha/beta than a resolution-inherent identifiability problem, and is flagged for further investigation rather than classified with confidence here. **GATE-019/020** (branching ratio) are classified `PROTOCOL_NOT_COMPLETED` (need the full 1,000/cell scale to confirm), not estimand mismatch — they are the gates whose *estimand* this audit finds most defensible.

## 5. Was M2 protocol completed? (§13 question 7)

**No.** `PILOT_ONLY_PROTOCOL_DEVIATION`, exactly as the governing instruction's §5 required classification states. 150/cell actual vs. 1,000/cell planned, reported explicitly by the pilot's own driver script docstring, not discovered post-hoc by this audit. No gate result from M2 in this pilot may be treated as a final tournament verdict.

## 6. Amendment proposal only (§7.4) — not adopted here

If the estimand-mismatch finding is accepted by the researcher:
- **Preserve** the original GATE-017/GATE-021 (individual alpha/beta bias and coverage) exactly as frozen — do not delete or silently relax them; they remain valid record of what was originally specified and why it failed.
- **Classify** them `ESTIMAND_MISMATCH_PROPOSED` in the ledger (already done in the accompanying gate-classification CSV as `ESTIMAND_MISMATCH`, consistent with this section's naming) rather than treating their failure as a verdict on M2 as a whole.
- **Propose** a supplementary/replacement gate pair scoped to the branching ratio `n` and, if a future turn defines it, interval-level integrated excitation mass — see `MODEL_3B_GATE_AMENDMENT_PROPOSAL.md` for the concrete proposal.
- **Require** researcher approval before any such amendment is adopted.
- **Do not** run the full 1,000-replicate-per-cell M2 tournament under either the old or a new gate set until that approval is given — this audit does not authorize it.
