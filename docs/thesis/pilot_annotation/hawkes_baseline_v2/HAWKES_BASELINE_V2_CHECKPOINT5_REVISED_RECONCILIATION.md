# HAWKES BASELINE V2-A — CHECKPOINT 5, REVISED (RECONCILIATION PASS)

Status: **NOT APPROVED — awaiting manual researcher sign-off.**
Scope: deterministic inspection of the existing 2,780-replication full-study
output (`v2a_full_study_meta.json`: N_full_study_plan=2780, N_attempted=2780,
N_errors=0, elapsed_sec=182.4), plus two targeted reruns limited to the
designs where a verified defect required it. **The FPR family (D1–D6, 1,668
of 2,780 replications) was never rerun** — it does not depend on either
defect found below.

---

## 1. KS / TIME-RESCALING RESIDUAL AUDIT

**Implementation facts, read directly from
`v2a_validation_engine.py`/`v2a_full_study.py`:**

- **Granularity:** KS is run **once per replication**, not once per pooled
  design. `run_family_recovery()` calls `ks_uniform_pvalue(v)` inside the
  per-`rep` loop for D7, D8, D9 (both arms), D10 — 278 independent KS tests
  per design/arm, never one pooled test on concatenated residuals.
- **Residual vector:** the time-rescaling residuals `v` from that single
  replication's own fitted model (`time_rescaling_residuals(res.x, events, T,
  mu_of_t=...)`), tested against Uniform(0,1) via `scipy.stats.kstest`.
- **Fitted vs. true parameters:** **fitted** (MLE `res.x`), not the design's
  true `(mu, alpha, beta)`. This is standard practice for a GOF residual
  check, but it means the test is conservative — see calibration finding
  below.
- **Compensator:** `time_rescaling_residuals()` recursively integrates
  baseline + excitation between consecutive events: `int_mu = mu*(ti-prev_t)`
  (or a covariate-shape integral for D9's correct arm) plus
  `int_exc = (alpha/beta)*A*(1-exp(-beta*(ti-prev_t)))`, matching the same
  recursive excitation sum `A` used in the log-likelihood. Algebraically
  consistent with the fitting code.
- **Observation window start/end:** the recursion starts at `prev_t=0.0` for
  the first event and stops at the **last observed event**, not at `T`. The
  right-censored tail interval `(t_last, T]` is never converted into a
  residual or tested. This is a common simplification (n residuals for n
  events) but it means the tail of the observation window is untested by
  design — a genuine, if minor, coverage gap in the GOF check, not a defect.
- **NaN handling:** `ks_uniform_pvalue` returns `NaN` when `len(v) < 3`;
  `v2a_analysis.py` then **filters NaNs out** before computing
  `ks_pvalue_mean` / `ks_pvalue_frac_below_0.05` (`N_ks_computed` records the
  finite count). In this run `N_ks_computed == 278` for every
  design/arm — no replication was ever excluded.
- **Duplication check:** for every design/arm, `n_unique(p) == n_finite(p)
  == 278`. No duplicated p-values across replications.

**Post-fix numbers** (D7/D8/D9/D10 rerun under the corrected seeding, see §6):

| design/arm | N | N_finite | N_below_0.05 | min p | median p | max p |
|---|---|---|---|---|---|---|
| D7 primary | 278 | 278 | 0 | 0.2276 | 0.8525 | 0.9999 |
| D8 primary | 278 | 278 | 0 | 0.1050 | 0.7942 | 0.9999 |
| D9 correct_cd_modulated | 278 | 278 | 0 | 0.1045 | 0.7679 | 0.9997 |
| D9 misspecified_constant_mu | 278 | 278 | 1 | 0.0297 | 0.7791 | 0.9972 |
| D10 primary | 278 | 278 | 0 | 0.1179 | 0.8153 | 0.9999 |

**Diagnostic verdict:**

```
MARGINAL_KS_DIAGNOSTIC_IMPLEMENTATION_OR_CALIBRATION_REQUIRES_AUDIT
```

`frac_below_0.05 ≈ 0` is **not** treated as a pass. The p-value distributions
are not remotely Uniform(0,1) under the null they are supposed to test —
medians run 0.77–0.85, far above the 0.5 expected of a well-calibrated KS
test, and even the deliberately-misspecified D9 arm only pushes the rate
below 0.05 in 1/278 replications. This pattern (systematically inflated
p-values, near-zero rejection even under known misspecification) is the
textbook signature of **fit-then-test-on-the-same-data bias**: residuals
built from MLE parameters estimated on the very data being tested are
mechanically closer to the target distribution than residuals from the true
parameters, so the test loses power. This is a known, expected property of
in-sample time-rescaling residual checks, not evidence that the fitted
Hawkes model is correctly specified. It means the near-zero false-positive
rate reported for the residual GOF check cannot, by itself, be read as
validating model fit.

Independence diagnostics (e.g., autocorrelation of the rescaled residuals,
Ljung–Box, or a second-order/Q-Q check on inter-residual spacing) were never
implemented — only the marginal-uniformity KS test exists. Therefore:

```
V_T = NOT_COMPLETE
```

**Residual validation is not complete.** The marginal KS result is an
input to, not a substitute for, GOF completion.

---

## 2. D2 MANIFEST RECONCILIATION

**No standalone frozen design-registry document was found in the repository**
(`v2a_designs.py`'s docstring references
`HAWKES_BASELINE_V2A_DESIGN_REGISTRY.csv`, which does not exist under that
name anywhere in `docs/thesis/`). The only recoverable specification of D2's
intent is the code itself and its inline comments.

**Exact comparator actually fit for D2:** `fit_homogeneous_poisson()` — a
constant-rate Poisson MLE (`mu_hat = n/T`), **not** an inhomogeneous-Poisson
comparator. The generator (`gen_D2`) simulates from a smooth sinusoidal
baseline `mu0*(1+0.5*sin(2πt/T))`.

**Classification, per the code's own inline annotation**
(`v2a_full_study.py:57-58`):

```
row["comparator_specified"] = False  # homogeneous comparator is
# misspecified vs smooth-inhomogeneous truth; still reported as best available
```

and `v2a_analysis.py` labels the resulting rate `PREFERENCE_RATE_MISSPECIFIED_COMPARATOR`
(delta2 = 0.327, mean ΔAIC = 0.848), **not** `FALSE_SELECTION_RATE` / FPR.
So at the level of the code that actually exists and ran, **D2 was never
reported as an FPR result** — the analysis pipeline already refuses to call
this a false-positive rate. What cannot be confirmed, in the absence of the
referenced registry file, is whether the *original frozen manifest*
specified an inhomogeneous-Poisson comparator for D2 and the implementation
silently substituted a homogeneous one, or whether "deliberately-misspecified
comparator, reported as a preference-rate robustness arm" was the frozen
design all along. Recording both possibilities:

```
D2_DESIGN_EXECUTION_STATUS = UNRECONCILABLE_AGAINST_MISSING_MANIFEST
D2_AS_EXECUTED = PREFERENCE_RATE_MISSPECIFIED_COMPARATOR (NOT reported as FPR)
```

No rerun performed for D2 — the implementation is internally consistent with
its own inline documentation, and the analysis layer already withholds the
FPR label. This is a **documentation gap** (missing/unfindable frozen
manifest), not a demonstrated code defect, and should be closed by the
researcher confirming which of the two readings above was actually approved
at checkpoint 3/4, not by further code changes.

---

## 3. D3 COUNT CALIBRATION RECONCILIATION

- **Intensity formula:** `mu(t) = B0 + B1 * cd_density_norm(t)`, `B0=0.2`,
  `B1=0.3`, where `cd_density_norm(t)` is the real CD annual-document-density
  series, mean-normalized to 1.0 over 1600–1784 (`CD_DENSITY = counts /
  counts.mean()`).
- **Exposure normalization:** density is a **mean-1** normalization (not
  max-1), so `mean(cd_density_norm) = 1.0` exactly over the empirical year
  range but `max(cd_density_norm) = 5.386`.
- **Integral of intensity over [0,T] (T=184 yr):** computed directly —
  `∫μ(t)dt ≈ 94.56` on a 20,000-point grid (`≈95.23` on the coarser 500-point
  grid used internally by the fitting/likelihood code — a ~0.7 discretization
  difference, immaterial at this sample size).
- **Theoretical E[N] = 94.6–95.2**, not 86.
- **Implemented calibration constants:** `B0=0.2, B1=0.3`, documented in
  `v2a_designs.py` as "frozen at checkpoint 3, from real-data statics" — i.e.
  chosen to match some real-data feature of the CD density shape, with no
  documented step that also targets a total count of 86.
- **Achieved mean N and MCSE:** `mean_n = 94.014`, `sd_n = 9.212`,
  `MCSE = sd/√278 = 0.5535`.

**Why achieved (94.01) differs from "intended" 86:** it doesn't, relative to
the actual implemented model — 94.01 sits within 1 discretization unit of the
model's own theoretical expectation (94.56–95.2) and well inside its MCSE.
**There is no calibration defect in D3.** The discrepancy is between the
achieved count and an *assumed* target of 86 (the D1 baseline count) that was
never built into B0/B1 for D3. D3 was calibrated to reproduce the **shape**
of real document density, not the **total historical event count** — those
are two different calibration targets, and only the first was actually
implemented. **No rerun performed** — the simulator is correctly implementing
the frozen `(B0, B1)` constants; what needs researcher resolution is whether
D3 was *also* supposed to target N≈86, which would require different
`(B0,B1)`, not a bug fix.

---

## 4. D10 EVENT-COUNT RECONCILIATION

**Verified implementation defect (fixed and rerun — see §6, Defect D10-A).**

Pre-fix, checking `N_estimator_input <= N_interval_observed <= N_latent` for
every one of the 278 D10 replications:

```
violations = 132 / 278   (47.5%)
```

**Root cause:** `run_family_recovery()` drew `classes =
assign_precision_classes(latent, rng)` once (to compute `n_interval_observed
= n_latent - n_unresolved`), then called `gen_D10_observed(latent, rng)`,
which **re-drew** `classes = assign_precision_classes(latent, rng)`
**internally**, consuming the same `rng` stream a second time with a fresh,
independent random assignment. The count used for `n_interval_observed` and
the count of "unresolved" actually dropped inside `impute_d10()` therefore
came from **two different random realizations** of the same 15.6%-probability
"unresolved" draw over ~145 latent events (binomial sd ≈ 4.35 each,
difference sd ≈ 6.15) — which side came out larger was close to a coin flip,
exactly matching the observed ~47.5% violation rate.

This explains the previously reported means exactly:
`N_interval_observed = 122.0`, `N_estimator_input = 122.4` — both are
"`n_latent` minus an unresolved-count" but from two uncorrelated draws, so
their means are close (same underlying probability) while their **per-
replication** values routinely disagree, some times in the invariant-
violating direction.

**Fix:** `gen_D10_observed` now takes the already-drawn `classes` as an
explicit parameter and no longer redraws (`v2a_designs.py`, function
`gen_D10_observed`). The caller passes the single `classes` draw through.

**Post-fix (D10 rerun, 278/278 replications, same B=278 plan):**

```
N_interval_observed mean = 121.40   (sd = 29.01)
N_estimator_input   mean = 121.40   (sd = 29.01, IDENTICAL — same draw)
violations = 0 / 278
N_latent mean = 144.13   (sd = 34.73)
```

The invariant now holds with equality for every replication
(`N_estimator_input == N_interval_observed` exactly, since D10's stress test
only tests single-imputation *within* known bounds, never dropping further
resolved events at the estimator stage — a stronger invariant than the
`<=` originally specified, and correctly so).

---

## 5. OPTIMIZER vs. UNCERTAINTY-RECOVERY ACCOUNTING (RECOVERY FAMILY)

**Second verified defect found during this reconciliation (Defect
COVERAGE-B, §6):** the original coverage/Hessian/CI columns (`se_mu`,
`se_alpha`, `se_beta`, `coverage_mu/alpha/beta`) were computed by
`v2a_coverage_addon.py` running as a **separate Python process** from
`v2a_full_study.py`. Both derived their per-replication RNG seed from
`SEED_BASE*100000 + hash(design_id)%100000 + rep`. Python randomizes
`str.__hash__` per process by default (no `PYTHONHASHSEED` pinned anywhere in
this pipeline), so `hash("D7")` (etc.) differs between the two process
invocations. The addon therefore regenerated a **different synthetic event
set** than the one that actually produced the stored `mu_hat/alpha_hat/
beta_hat`, and evaluated the Hessian/Wald CI at the reported MLE against
mismatched data. This invalidated every `se_*`/`coverage_*` value for **all**
recovery-family designs (D7, D8, D9 both arms, D10) — not a D10-specific
issue. `mu_hat/alpha_hat/beta_hat`, bias, RMSE, `F_opt`, and the KS
diagnostics in §1 were unaffected (computed entirely inside the single
original `v2a_full_study.py` process).

**Fix:** replaced `hash(design_id)` with a fixed, explicit
`DESIGN_SEED_OFFSET` integer map in `v2a_validation_engine.py`
(`design_seed(design_id, rep)`), used identically by `v2a_full_study.py` and
`v2a_coverage_addon.py`. Verified post-fix: an independent, freshly-seeded
regeneration of D7 rep 5 now reproduces the exact same `n_events` (71) as the
original fit — cross-process consistency confirmed.

**Rerun performed:** the full RECOVERY family (D7, D8, D9, D10 — 1,390 rows,
not the full 2,780) was rerun end-to-end (fit + KS + Hessian/CI) under the
corrected deterministic seeding, since the original per-design seeds were
themselves process-salt-dependent and unrecoverable. **D1–D6 (FPR family,
1,668 replications) were not rerun** — they never call the coverage addon and
were unaffected by this defect.

**Post-fix accounting, per design/arm/parameter (N=278 each):**

| design/arm | param | N_opt_conv | F_opt | N_valid_hessian | F_CI (nonfinite) | N_covered | Coverage_cond | Coverage_uncond |
|---|---|---|---|---|---|---|---|---|
| D7 | mu | 278 | 0.0000 | 278 | 0.0000 | 265 | 0.9532 | 0.9532 |
| D7 | alpha | 278 | 0.0000 | 278 | 0.0000 | 233 | 0.8381 | 0.8381 |
| D7 | beta | 278 | 0.0000 | 278 | 0.0000 | 251 | 0.9029 | 0.9029 |
| D8 | mu | 278 | 0.0000 | 278 | 0.0000 | 258 | 0.9281 | 0.9281 |
| D8 | alpha | 278 | 0.0000 | 278 | 0.0000 | 257 | 0.9245 | 0.9245 |
| D8 | beta | 278 | 0.0000 | 278 | 0.0000 | 259 | 0.9317 | 0.9317 |
| D9 correct | mu | 278 | 0.0000 | 278 | 0.0000 | 256 | 0.9209 | 0.9209 |
| D9 correct | alpha | 278 | 0.0000 | 278 | 0.0000 | 251 | 0.9029 | 0.9029 |
| D9 correct | beta | 278 | 0.0000 | 278 | 0.0000 | 251 | 0.9029 | 0.9029 |
| D9 misspec. | mu | 278 | 0.0000 | 278 | 0.0000 | 187 | 0.6727 | 0.6727 |
| D9 misspec. | alpha | 278 | 0.0000 | 278 | 0.0000 | 247 | 0.8885 | 0.8885 |
| D9 misspec. | beta | 278 | 0.0000 | 278 | 0.0000 | 211 | 0.7590 | 0.7590 |
| D10 | mu | 278 | 0.0000 | 278 | 0.0000 | 258 | 0.9281 | 0.9281 |
| D10 | alpha | 278 | 0.0000 | 278 | 0.0000 | 252 | 0.9065 | 0.9065 |
| D10 | beta | 278 | 0.0000 | 278 | 0.0000 | 260 | 0.9353 | 0.9353 |

`F_opt = 0` and `F_CI = 0` (finite Hessian in every single replication)
across the board — a real property of this run, not an artifact: Nelder-Mead
converged (`res.success`) and produced an invertible finite-difference
Hessian in all 1,390 replications, so `Coverage_conditional ==
Coverage_unconditional` here.

**Because F_opt and F_CI are both exactly 0, 278 optimizer convergences here
does equal 278 usable CIs** — that specific failure mode the checkpoint asked
to guard against (claiming full uncertainty recovery when finite-CI counts
are smaller) does not occur in this run. What **does** remain a live
finding: for the correctly-specified arms (D7, D8, D9-correct, D10), nominal
95% Wald coverage is achieved for some parameters (D7-mu 95.3%, D8 all three
92.8–93.2%) but sits meaningfully below nominal for others (D7-alpha 83.8%,
D9-correct alpha/beta 90.3% each, D10-alpha 90.7%) — consistent with known
finite-difference-Hessian Wald-CI under-coverage at these sample sizes
(n≈85–146 events), not with a coding defect. D9's misspecified-constant-mu
arm shows the expected large under-coverage on mu (67.3%) from ignoring the
true covariate-modulated baseline — correctly excluded from H-05 evidence
(`counted_toward_H05: False` in the row data).

---

## 6. IMPLEMENTATION DEFECTS — LEDGER

| Field | Defect D10-A | Defect COVERAGE-B |
|---|---|---|
| Affected design | D10 only | D7, D8, D9 (both arms), D10 |
| Affected replications | all 278 D10 reps, pre-fix | all 1,390 recovery-family rows, pre-fix |
| Pre-fix code hash | `v2a_designs.py` = `51a14e586778437e217b62b4d40223d4` | `v2a_full_study.py` = `2d418999c4d492c34e89d997c3606d6e`; `v2a_coverage_addon.py` (pre-fix, unhashed — superseded in place, no snapshot retained) |
| Pre-fix output status | `N_estimator_input`/`N_interval_observed` computed from two independent RNG draws of "unresolved" class; invariant violated in 132/278 (47.5%) reps | `se_mu/alpha/beta`, `coverage_mu/alpha/beta` computed against synthetic events regenerated with a *different* `hash(design_id)` salt than the original fitting process; values not tied to the reported `mu_hat/alpha_hat/beta_hat` |
| Correction | `gen_D10_observed` now takes `classes` as an explicit argument instead of redrawing internally; caller passes its single draw through | `hash(design_id)` replaced by a fixed `DESIGN_SEED_OFFSET` map + `design_seed()` helper in `v2a_validation_engine.py`, used identically by both scripts |
| Post-fix code hash | `v2a_designs.py` = `40ce5d8c8b4c8ff4cf496b3e98d9fc6b` | `v2a_full_study.py` = `aab9479769fc8497ca060e69a9131ba8`; `v2a_coverage_addon.py` = `abe65cbb47fda7adaa85bc69bf9e9781`; `v2a_validation_engine.py` = `81857728b78095013779b4d61403f621` |
| Targeted rerun status | superseded by the COVERAGE-B rerun below (same 278 reps, rerun once, correctly) | RECOVERY family only rerun (D7/D8/D9/D10, 1,390 rows via `v2a_full_study.py` + `v2a_coverage_addon.py`); FPR family (D1–D6, 1,668 rows) **not rerun**, unaffected |
| Old/new rows coexist? | No — `v2a_full_study_recovery_rows.json` fully replaced for D7/D8/D9/D10; pre-fix snapshot preserved separately as `v2a_full_study_recovery_rows_PRE_D10_CLASSES_DEFECT_SUPERSEDED.json` | Same file/same replacement; the superseded snapshot above also carries the pre-COVERAGE-B (mismatched) SE/coverage columns for D7/D8/D9, retained for audit only |
| Does any summary mix versions? | No — `v2a_summary_recovery.csv` and `v2a_d10_pipeline.csv` were regenerated from the post-fix `v2a_full_study_recovery_rows.json` after both fixes landed | Same regeneration covers this |

**No superseded result entered `v2a_summary_recovery.csv`, `v2a_summary_fpr.csv`,
or `v2a_d10_pipeline.csv`** — all three were regenerated from the corrected
`v2a_full_study_recovery_rows.json` (1,390 rows, post both fixes) and the
untouched, still-valid `v2a_full_study_fpr_rows.json` (1,668 rows, D1–D6,
never affected by either defect).

A third, non-code finding worth carrying forward without a "fix": `D4`
(FPR family) shows `n_converged = 274/278` — the only design in the whole
2,780-replication study with any recorded Hawkes-fit non-convergence
(`F_opt ≈ 1.4%`). This was not investigated further under this checkpoint's
scope (D4 is a stress-test design, not part of H-05 evidence), but should be
listed as an open item.

---

## 7. H-05 — PRESERVED AS PROVISIONAL

```
H05_PROVISIONAL = H05_NOT_EVALUABLE_REQUIRES_RESEARCHER_REVIEW
```

**Reason A:** the authoritative "≥0.80" acceptance criterion referenced for
H-05 has no operational metric or aggregation rule on file in this directory
(no document defines whether ≥0.80 applies to per-parameter coverage, to a
pooled coverage across D7/D8/D9-correct/D10, to `1 - frac_below_0.05` on the
KS check, or to some other quantity). Absent that definition, none of the
numbers in §5 or §1 can be mechanically compared against a pass/fail bound.

**Reason B:** validation-package completion remains pending — the marginal
KS check is confirmed conservative/self-fit-biased (§1), independence
diagnostics were never implemented (`V_T = NOT_COMPLETE`), the D2 frozen
manifest cannot be located to confirm intended comparator specification
(§2), and D4's 4 non-convergent replications are unexplained.

H-05 is **not** converted to PASS or FAIL by this reconciliation pass.

---

## 8. REVISED CHECKPOINT 5 — STATUS SUMMARY

| Design | Family | Status | Rerun this pass? |
|---|---|---|---|
| D1 | FPR | Terminal, valid (unaffected by either defect) | No |
| D2 | FPR (misspecified-comparator arm) | Terminal as executed; frozen-manifest comparison **unreconcilable** (registry file not found) — see §2 | No |
| D3 | FPR | Terminal, valid; achieved N=94.01 matches the design's own theoretical E[N]≈94.6–95.2, not the assumed 86 target — see §3 | No |
| D4 | PR (naive substitution stress test) | Terminal but flags 4/278 non-convergent fits, unexplained — open item | No |
| D5 | FPR_DUAL | Terminal, valid | No |
| D6 | PR (Neyman–Scott) | Terminal, valid | No |
| D7 | RECOVERY | Terminal, valid **post-fix** (COVERAGE-B) | Yes |
| D8 | RECOVERY | Terminal, valid **post-fix** (COVERAGE-B) | Yes |
| D9 | RECOVERY (2 arms) | Terminal, valid **post-fix** (COVERAGE-B) | Yes |
| D10 | RECOVERY_INTERVAL | Terminal, valid **post-fix** (D10-A + COVERAGE-B) | Yes |

**Original vs. corrected targeted results:** see §4 (D10 counts:
122.0/122.4 pre-fix with 132/278 invariant violations → 121.4/121.4 post-fix
with 0/278 violations) and §5 (coverage table now computed against the
correct matched synthetic data for all 1,390 recovery-family rows, rather
than cross-process-mismatched data).

**Residual calibration audit:** §1 — conservative/self-fit-biased KS,
recorded as `MARGINAL_KS_DIAGNOSTIC_IMPLEMENTATION_OR_CALIBRATION_REQUIRES_AUDIT`.

**Residual-independence gap:** `V_T = NOT_COMPLETE` — no independence
diagnostic exists in the codebase.

**D2 manifest compliance:** unreconcilable — frozen manifest file not
located; current execution reports a misspecified-comparator preference
rate, never an FPR.

**D3 theoretical vs. achieved:** theoretical E[N] ≈ 94.6–95.2; achieved
94.01 ± 0.55 MCSE — consistent, no defect; open question is whether the
frozen calibration target for D3 was ever intended to be N≈86.

**D10 count invariants:** 0/278 violations post-fix (was 132/278).

**Optimizer/Hessian/CI accounting:** F_opt=0, F_CI=0 across all 1,390
recovery-family rows post-fix; per-parameter Wald coverage 67.3–95.3%,
below nominal 95% for several parameters even in correctly-specified arms —
flagged, not treated as a defect.

**Achieved MCSEs:** reported per design in §3/§5 tables and in
`v2a_summary_fpr.csv` / `v2a_summary_recovery.csv`.

**Exact unreconciled issues carried forward:**
1. D2's frozen manifest cannot be located to confirm the originally-approved
   comparator specification (§2).
2. Whether D3's calibration constants were ever intended to also hit
   N≈86 (§3).
3. D4's 4/278 non-convergent Hawkes fits, cause not investigated (§6).
4. No operational ≥0.80 metric/aggregation rule exists for H-05 (§7).
5. No residual-independence diagnostic exists; KS alone cannot close
   out validation (§1).
6. D7's beta recovery shows large bias (+0.99 against true beta=0.6) and
   D9-correct shows beta bias (+0.50 against true beta=0.6) — plausible
   weak identifiability of the decay parameter under low/moderate
   excitation, noted here but not investigated further under this
   checkpoint's scope.

**Do not proceed to checkpoint 6 or V2-B readiness until this revised
checkpoint 5 is manually approved by the researcher.**
