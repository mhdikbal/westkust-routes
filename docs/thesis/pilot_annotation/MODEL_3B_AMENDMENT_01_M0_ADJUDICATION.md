# Amendment Adjudication — Proposal 1: M0 Full-Hessian and Covariance Correction

> **Decision record only. No M0 source code modified. No correction implemented. No M0 recovery rerun. No gate specification changed. No historical data fitted. Nothing staged, committed, pushed, or deployed.**

---

## Authoritative Baseline

```text
Model 3B pilot diagnostic audit commit:     4b94cd689c995765102b4ca4c63e2636334432bb
Authoritative status:                       MODEL_3B_PILOT_DIAGNOSTIC_AUDIT_PUSHED_AND_SERVER_SYNCED
Tournament verdict:                         NOT_AVAILABLE
Historical-data fitting:                    NOT_AUTHORIZED
Original amendment proposals:               7 PROPOSED_ONLY, 0 ADOPTED
```

## Proposal Subject

Correct the M0 uncertainty-estimation implementation by replacing the diagonal-only finite-difference Hessian treatment with a validated full Hessian and covariance calculation.

## Researcher Adjudication

```text
Proposal 1: APPROVED_WITH_LIMITATIONS
```

This decision approves the **methodological correction direction only**. It does **not** authorize: editing M0 source code in this turn; running the full M0 recovery tournament; changing the original recovery gates; fitting historical data; selecting M0 as the winning candidate; production deployment.

---

## Scientific Basis

```text
M0 execution scale:              15 cells x 1,000 replications/cell = 15,000 total
Point-estimate relative bias:    ~0.7-3.4%
Original interval coverage:      ~54.4-61.5%
Frozen target:                   92.5-97.5%
```

**Confirmed defect** (verified directly against `docs/thesis/colab/model3b_tournament_harness/run_recovery_m0.py::run_cell`, lines ~123-130, not asserted from prose):

```python
# (numeric Hessian at the MLE, 2x2 for theta0/theta1, phi treated nuisance)
def nll2(t0v, t1v):
    return neg_loglik_nb([t0v, t1v, math.log(max(est_phi, 1e-6))], counts, YEAR_COV)
f00 = (nll2(est_t0 + eps, est_t1) - 2 * nll2(est_t0, est_t1) + nll2(est_t0 - eps, est_t1)) / eps**2
f11 = (nll2(est_t0, est_t1 + eps) - 2 * nll2(est_t0, est_t1) + nll2(est_t0, est_t1 - eps)) / eps**2
se0 = math.sqrt(1.0 / f00) if f00 > 1e-9 else float("nan")
se1 = math.sqrt(1.0 / f11) if f11 > 1e-9 else float("nan")
```

The executed code computes only `f00` and `f11` (the diagonal), never the cross-partial `f01 = ∂²NLL/∂θ0∂θ1`, and inverts each diagonal element independently (`1/f00`, `1/f11`) rather than inverting the full 2×2 matrix. **Additionally confirmed, beyond the originally-flagged cross-term gap**: the code's own comment states `phi treated nuisance` — `phi` (the NB dispersion parameter, jointly estimated by the same optimizer) is excluded from the covariance calculation entirely, not merely from the cross-term. This directly evidences Limitation #3 below (`"the correction must use the complete parameter vector, not only theta0/theta1 if M0 also estimates dispersion"`) as an actual, present gap in the executed code — not a hypothetical one.

**Mathematical formulation:**

The old approximation effectively used:

```text
H_diagonal = diag( d2NLL/dtheta0^2, d2NLL/dtheta1^2 )
```

instead of the full Hessian (extended here to the actually-estimated 3-parameter vector `(theta0, theta1, log_phi)`, per the confirmed gap above):

```text
H_full =
[ d2NLL/dtheta0^2,           d2NLL/dtheta0 dtheta1,      d2NLL/dtheta0 dlogphi ]
[ d2NLL/dtheta1 dtheta0,     d2NLL/dtheta1^2,             d2NLL/dtheta1 dlogphi ]
[ d2NLL/dlogphi dtheta0,     d2NLL/dlogphi dtheta1,       d2NLL/dlogphi^2       ]
```

**Convention, confirmed from source (not assumed):** `run_recovery_m0.py::neg_loglik_nb` is passed directly to `scipy.optimize.minimize` (line ~89: `minimize(lambda p: neg_loglik_nb(p, counts, year_cov), ...)`) — the code **minimizes the negative log-likelihood**. The applicable convention is therefore:

```text
Cov(theta_hat) = inverse( H_NLL(theta_hat) )
```

not the maximized-log-likelihood form (`inverse(-H_loglik)`) — both reduce to the same matrix here since `H_NLL = -H_loglik`, but the sign path actually exercised by the code is the NLL-minimization one, confirmed by reading the `minimize()` call site directly.

---

## Diagnostic Oracle

```text
Fixed-seed oracle:          n = 60
Observed full-Hessian coverage: 93.3%
```

**Interpretation:**
- The oracle result lies within the frozen target band `[92.5%, 97.5%]`.
- The result supports the implementation-defect diagnosis.
- The oracle does **not** constitute a full tournament rerun.
- The oracle does **not** establish final M0 PASS.

---

## Final M0 Status After This Adjudication

```text
M0_HESSIAN_COVARIANCE_CORRECTION_APPROVED_WITH_LIMITATIONS
M0_FINAL_GATE_PENDING_CORRECTED_RERUN
```

Explicitly **not** used: `M0_FINAL_PASS`, `M0_MODEL_VALIDATED`, `M0_SELECTED_FOR_HISTORICAL_FIT`, `M0_PRODUCTION_READY`.

---

## Limitations (all recorded)

1. The original pilot result remains historically visible (this document does not retract or overwrite `MODEL_3B_PILOT_RECOVERY_DIAGNOSTIC_AUDIT.md`, `MODEL_3B_M0_INTERVAL_COVERAGE_AUDIT.md`, or the gate CSV).
2. The original gate specification (`MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv`, 70 rows) remains immutable.
3. **Confirmed present, not hypothetical** (see Scientific Basis above): the correction must use the complete parameter vector — `theta0`, `theta1`, **and `log_phi`**, since M0 as executed jointly estimates dispersion, not just `theta0`/`theta1`.
4. Hessian parameter order must match the optimizer parameter order (`x = [theta0, theta1, log_phi]` per `neg_loglik_nb`'s own signature).
5. Cross-partial symmetry (`∂²NLL/∂θ0∂θ1 = ∂²NLL/∂θ1∂θ0`, and the two additional cross-partials involving `log_phi`) must be checked numerically, not assumed.
6. Hessian sign must match the confirmed convention above (NLL-minimization; `Cov = inverse(H_NLL)`).
7. The Hessian must be checked for: finite values; symmetry; positive definiteness under the NLL convention; conditioning; invertibility.
8. Silent diagonal fallback is prohibited — if the full Hessian is non-invertible or ill-conditioned, this must surface as an explicit diagnostic flag, not a silent reversion to the old diagonal approximation.
9. Pseudoinverse use, if proposed as a fallback, must be disclosed and classified as a **degraded diagnostic result**, not an ordinary PASS.
10. `log_phi` is already a log-scale transform of `phi`; any reporting of `phi`'s own uncertainty (as opposed to `log_phi`'s) requires a documented Jacobian/delta-method transformation (`Var(phi_hat) ≈ phi_hat^2 * Var(log_phi_hat)`, per the master instruction's §4.3).
11. The dispersion parameter `phi` must use one consistent NB convention across simulator, likelihood, estimator, covariance, confidence interval, and recovery metrics — **verified consistent in the executed code** (see Negative Binomial Convention section below); this consistency must be preserved, not silently altered, by the future correction.
12. Corrected code requires synthetic unit tests before any full rerun (see Required Future Tests below).
13. A corrected full-scale M0 rerun requires separate authorization — not granted by this document.
14. Historical-data fitting remains separately gated — not granted by this document.

---

## Negative Binomial Convention (verified from source, not assumed)

Per the instruction's explicit requirement, the convention was read directly from `run_recovery_m0.py`, not assumed:

```python
def simulate_nb_counts(theta0, theta1, phi, rng):
    ...
    p = phi / (phi + mean)
    counts[y] = int(rng.negative_binomial(phi, p))

def neg_loglik_nb(params, counts, year_cov):
    theta0, theta1, log_phi = params
    log_phi = min(max(log_phi, -20.0), 20.0)
    phi = math.exp(log_phi)
    ...
    p = phi / (phi + mean)
    ll += gammaln(k + phi) - gammaln(phi) - gammaln(k + 1) + phi * math.log(p) + k * math.log(1 - p)
```

With `p = phi/(phi+mean)`: `mean = phi*(1-p)/p`, `Var = phi*(1-p)/p^2 = mean + mean^2/phi`. **This confirms the executed code uses exactly the convention the master instruction's §4.3 specifies**: `E[Y]=mu`, `Var[Y] = mu + mu^2/phi`, with `eta_phi = log(phi)` (confirmed: `log_phi` is the actual optimization variable, clamped to `[-20, 20]` before exponentiating) and `phi = exp(eta_phi)`. The simulator (`simulate_nb_counts`) and the estimator (`neg_loglik_nb`) both use the identical `p = phi/(phi+mean)` formula — **convention is consistent between simulator and estimator**, confirmed by direct comparison, not assumed. The covariance/CI/recovery-metric consumers of this convention are exactly the diagonal-only `f00`/`f11` construction audited above, which is what Proposal 1 addresses.

---

## Required Future Implementation Tests (recorded, NOT executed this turn)

```text
M0-HESS-001: Analytic or automatic-differentiation Hessian agrees with a
             trusted numerical full-Hessian implementation within a
             prespecified tolerance.
M0-HESS-002: Cross-partials are symmetric within numerical tolerance.
M0-HESS-003: Parameter order in the Hessian equals optimizer parameter order.
M0-HESS-004: Correct sign convention is used (NLL-minimization: Cov=inverse(H_NLL)).
M0-HESS-005: Covariance is finite and valid for an interior optimum.
M0-HESS-006: Near-singular Hessian produces an explicit diagnostic, not silent PASS.
M0-HESS-007: Log-scale parameters (log_phi) are transformed using a documented Jacobian.
M0-HESS-008: Fixed-seed oracle reproduces the corrected coverage result (this
             turn's n=60/93.3% oracle is the baseline to reproduce).
M0-HESS-009: Original point-estimate bias remains within the frozen gate
             (0.7-3.4% baseline, GATE-001/GATE-004).
M0-HESS-010: No raw pilot output or historical data is modified.
```

---

## Gate Consequences

The original 70-row gate specification is **not modified** by this adjudication.

**Remains applicable to M0** (unchanged from the diagnostic audit):
- point-estimate bias (GATE-001, GATE-004)
- RMSE
- interval coverage (GATE-007 — the gate this proposal targets)
- convergence (GATE-037)
- boundary-solution rate
- predictive calibration
- held-out predictive performance

**Remains not applicable to M0** (per the diagnostic audit's Mathematical Domain ruling, `NOT_APPLICABLE_TO_MODEL_DOMAIN`, unaffected by this proposal):
- excitation false-positive rate (GATE-002)
- excitation false-negative rate (GATE-036)
- alpha bias (GATE-003)
- beta bias (component of GATE-003/branching gates)
- branching-ratio bias (GATE-005/GATE-006)

---

## Approved Future Execution Order

This adjudication approves **only** the following future sequence, each step requiring its own further authorization where noted:

```text
1. Implement the full-Hessian correction in a separate turn.
2. Add targeted synthetic unit tests (M0-HESS-001 through 010).
3. Run a small fixed-seed implementation oracle.
4. Inspect Hessian conditioning and transformation behavior.
5. Freeze the corrected implementation.
6. Separately authorize the full M0 recovery rerun.
7. Evaluate M0 using the original applicable gates (list above).
8. Only after final recovery PASS, consider a separate historical-fit decision.
```

Nothing beyond step 0 (this adjudication) is authorized by this document.

---

## Final Status (this document)

```text
MODEL_3B_AMENDMENT_01_M0_ADJUDICATED
```
