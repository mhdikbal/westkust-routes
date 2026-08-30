# WAVE 2 Mathematical Contract — Model 3B V2 (M0, M2, M3)

> **Status: PLANNING-ONLY.** Baseline `979eaeb0d9b5d8dcd90faebd75a5dff5cd26d055`. This document defines mathematical objects, formulas, and future acceptance criteria. It authorizes no code, no execution, no numeric threshold, no tau value, no ROPE value. M0 final PASS is not established. M2 recovery/coverage is not validated. M3 model selection is not run. Historical inference remains `NOT_AUTHORIZED`.

## S0. Symbol Disambiguation (W2-P0 gate condition 4)

Two tokens are overloaded in the frozen corpus and must be read by context, never assumed:

```text
M0  (a) M0-IMPLEMENTATION-VALIDATION -- the model-validation/gate stage applied to every candidate's
        point-process likelihood machinery (this document's §S1)
    (b) M3-NULL-MODEL -- the M3 exact-null submodel n=0 (this document's §S3.1)

M1  (a) V1-BENCHMARK-NONAUTHORITATIVE -- the original V1 Hawkes benchmark, MODEL_VALIDATION_FAILURE /
        INFERENCE_NOT_AUTHORIZED (MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md lines 80, 401)
    (b) M3-EXCITATION-MODEL -- the M3 alternative 0<n<1 (this document's §S3.2)
```

Both disambiguation labels are `PROPOSED_INTERNAL_LABEL` (documentation convention only, per instruction §6.4). The five frozen V2 specification files are not renamed or edited. This document uses "M0-gate" for referent (a) and "M0-null"/"M1-excitation" for the M3 model tokens throughout, to avoid collision.

Full field-level dependency mapping and symbol table live in the companion CSVs:
`WAVE_2_REQUIREMENT_DEPENDENCY_MATRIX.csv` (37 requirements, 0 broken references, 0 cycles — verified in `WAVE_2_CROSS_DOCUMENT_CONSISTENCY_AUDIT.md`) and `WAVE_2_FORMULA_SYMBOL_REGISTRY.csv` (38 symbols).

---

## S1. M0-Gate Mathematical Contract (W2-P1)

### S1.1 Data and event history

```math
0 < t_1 < t_2 < \cdots < t_N \leq T, \qquad \mathcal H_t = \{t_i : t_i < t\}.
```

### S1.2 Conditional intensity (exponential-kernel Hawkes)

```math
\lambda(t \mid \mathcal H_t) = \mu + \sum_{t_j<t}\alpha\exp\{-\beta(t-t_j)\}, \qquad \mu>0,\ \alpha\geq0,\ \beta>0.
```

Branching ratio `n = alpha/beta`. Excitation regime `0<n<1`; exact null `n=0`.

### S1.3 Log-likelihood and compensator — OPEN

```math
\ell(\theta;Y) = \sum_{i=1}^{N}\log\lambda(t_i\mid\mathcal H_{t_i};\theta) - \int_0^T \lambda(t\mid\mathcal H_t;\theta)\,dt.
```

Candidate closed-form compensator for the exponential kernel (must be verified before adoption, not assumed):

```math
\int_0^T \lambda(t)\,dt = \mu T + \frac{\alpha}{\beta}\sum_{t_j<T}\left[1-\exp\{-\beta(T-t_j)\}\right].
```

**Open before this form is final** (REQ-M0-002, OD-004 for the n=0 boundary case specifically): definition of history at boundary ties; event-on-boundary treatment; initial-condition/presample-history convention; observation-window convention (does the M2/M3 annual-interval-count convention require a fundamentally different — interval-censored, not point-process — likelihood entirely? See cross-reference to M2's MBPP interval-censored likelihood, which is a *different* likelihood family from this continuous-time point-process form. This contract documents the continuous-time M0-gate form per the instruction's own S7; whether M0-gate validation runs against the continuous-time form or the interval-censored M2 form actually used downstream is itself flagged `OPEN_REQUIRES_ADJUDICATION` — no NUM-DEC decision in the frozen ledger settles which likelihood the M0-gate checks apply to).

### S1.4 Score

```math
s(\theta)=\nabla_\theta\ell(\theta), \qquad \lVert s(\widehat\theta)\rVert_\infty \leq \varepsilon_s \ \text{(interior-solution acceptance criterion, candidate)}.
```

`epsilon_s` = `OD-001`, `OPEN_REQUIRES_ADJUDICATION`.

### S1.5 Full Hessian (mandatory: never diagonal-only)

```math
H(\theta)=\nabla_\theta^2\ell(\theta) \quad\text{(all 9 entries of the 3x3 }(\mu,\alpha,\beta)\text{ matrix, including cross-derivatives)}.
```

```math
J(\widehat\theta)=-H(\widehat\theta), \qquad \widehat{\operatorname{Var}}(\widehat\theta)=J(\widehat\theta)^{-1}.
```

`H_diag = diag{H(theta)}` substitution is **prohibited** (`RESOLVED_BY_FROZEN_SPEC`, REQ-M0-004) — this is the correction already approved in a prior amendment; Wave 2 does not reopen it, only carries it forward as a binding contract term.

### S1.6 Symmetry / numerical-reference comparison

```math
E_{\mathrm{sym}} = \frac{\lVert H-H^\top\rVert_F}{\max(1,\lVert H\rVert_F)}, \qquad E_H = \frac{\lVert H_{\mathrm{candidate}}-H_{\mathrm{reference}}\rVert_F}{\max(1,\lVert H_{\mathrm{reference}}\rVert_F)}.
```

Tolerances = `OD-002`, `OPEN_REQUIRES_ADJUDICATION` — must not be set by trial-and-error against final results.

### S1.7 Parameter transformation — 8 open sub-questions (Package A)

Candidate transforms: `mu=exp(eta_mu)`, `beta=exp(eta_beta)`, `n=logit^-1(eta_n)`, `alpha=n*beta`. Delta-method covariance transform: `Var(theta_hat) = G(eta_hat) Var(eta_hat) G(eta_hat)^T`, `G(eta) = d g(eta)/d eta^T`.

All 8 sub-questions listed in the governing instruction (optimization space vs. reporting space; `n=0` representability under logit; frequentist vs. Bayesian Jacobian use; covariance transform; `alpha`/`beta` identifiability given `n` is primary) are `OD-003`/`OD-004`, `OPEN_REQUIRES_ADJUDICATION`. **Critical finding**: a naive `n=logit^-1(eta_n)` transform structurally excludes exact `n=0` for any finite `eta_n` — this is the *identical defect class* already confirmed in the current M3 sampler as `M3-BLOCK-01`. Any M0/M2/M3 implementation reusing this transform inherits the same defect unless a nested-null design (§S3.1) is used instead of a single continuous reparameterization.

### S1.8 Future M0-Gate checklist (REQ-M0-008, 11 sub-checks, none executed)

```text
1. point-estimate agreement            7. transformed-covariance check
2. score check                         8. boundary behavior
3. full-Hessian check                  9. deterministic reproducibility
4. cross-derivative check             10. failure reporting
5. Hessian symmetry check
6. covariance finiteness / SE finiteness
```

Point-estimate agreement alone is explicitly insufficient for PASS (`RESOLVED_BY_FROZEN_SPEC`). M0 final PASS status: **not established** by this document.

---

## S2. M2 Mathematical Contract (W2-P2)

### S2.1 Primary estimand vs. diagnostic parameters (RESOLVED_BY_FROZEN_SPEC, NUM-DEC-02)

```text
PRIMARY ESTIMAND:      n = alpha / beta
DIAGNOSTIC PARAMETERS: alpha, beta   (never a primary acceptance quantity)
```

Every future M2 output schema must separate these two categories explicitly (REQ-M2-001).

### S2.2 Attempted-replication accounting (RESOLVED_BY_FROZEN_SPEC, NUM-DEC-01)

```math
R_{\mathrm{attempted},c}=1000, \qquad R_{\mathrm{attempted},c} = R_{\mathrm{valid},c} + \sum_k R_{\mathrm{failure},c,k}.
```

```math
\widehat{\operatorname{FailureRate}}_c = 1-\frac{R_{\mathrm{valid},c}}{R_{\mathrm{attempted},c}}.
```

`R_generated`, `R_completed`, `R_converged`, `R_valid` are a strictly ordered refinement chain (each a subset of the previous, per §8.2). The denominator may never silently narrow to successful replications only.

### S2.3 Bias, relative bias, absolute bias

```math
\widehat{\operatorname{Bias}}_c(\widehat n) = \frac{1}{R_{\mathrm{valid},c}}\sum_{r\in\mathcal V_c}(\widehat n_{cr}-n_c), \qquad \widehat{\operatorname{RelBias}}_c(\widehat n) = \frac{\widehat{\operatorname{Bias}}_c(\widehat n)}{n_c}\ (n_c>0\text{ only}).
```

```math
\widehat{\operatorname{AbsBias}}_c = \frac{1}{R_{\mathrm{valid},c}}\sum_{r\in\mathcal V_c}\left|\widehat n_{cr}-n_c\right| \quad (\text{exact-null substitute}, n_c=0).
```

`RelBias` is undefined at `n_c=0` by construction (division by zero) — `AbsBias` is a *candidate*, not yet adopted (`OD-005`, `OPEN_REQUIRES_ADJUDICATION`). Every bias metric must be reported alongside `FailureRate_c` (attempted-denominator), never in isolation.

### S2.4 RMSE

```math
\widehat{\operatorname{RMSE}}_c(\widehat n) = \sqrt{\frac{1}{R_{\mathrm{valid},c}}\sum_{r\in\mathcal V_c}(\widehat n_{cr}-n_c)^2}.
```

### S2.5 Profile likelihood (RESOLVED_BY_FROZEN_SPEC as *primary method*, NUM-DEC-02; design details OPEN, Package C)

```math
\ell_p(n)=\sup_\psi\ell(n,\psi), \qquad D(n)=2\left[\ell_p(\widehat n)-\ell_p(n)\right], \qquad C_{1-\gamma}=\{n:D(n)\leq c_{1-\gamma}\}.
```

Ten design sub-decisions (grid, adaptive refinement, nuisance optimization, warm-start policy, endpoint search, disconnected confidence sets, boundary at `n=0`, upper boundary near `n=1`, profile-failure classification, interpolation/monotonicity assumptions) are `OD-007`, `OPEN_REQUIRES_ADJUDICATION`.

### S2.6 Coverage

```math
\widehat{\operatorname{Coverage}}_c = \frac{1}{R_{\mathrm{valid},c}}\sum_{r\in\mathcal V_c}\mathbf 1\{n_c\in C_{cr}\}, \qquad \widehat{\operatorname{CoverAndValid}}_c = \frac{1}{R_{\mathrm{attempted},c}}\sum_{r=1}^{R_{\mathrm{attempted},c}}\mathbf 1\{\text{valid interval and }n_c\in C_{cr}\}.
```

Which is primary = `OD-006`, `OPEN_REQUIRES_ADJUDICATION` — no new primary metric may be adopted without an explicit NUM-DEC/spec cross-check (S8.7 of the governing instruction).

### S2.7 Monte Carlo standard error

```math
\operatorname{MCSE}(\widehat p) = \sqrt{\widehat p(1-\widehat p)/R}.
```

The `R=1000, p=0.95 -> MCSE~0.0069` figure in the governing instruction is a worked *illustration only*, not an adopted acceptance band (`NONBLOCKING_CLARIFICATION` — see terminology flag reused from Wave 1's own audit output).

### S2.8 M2 exact-null test (RESOLVED_BY_FROZEN_SPEC structure, NUM-DEC-03; bootstrap design OPEN, Package D)

```math
H_0:n=0\ (\Rightarrow\alpha=0), \qquad H_1:0<n<1, \qquad \Lambda(Y)=2\left[\ell(\widehat\theta_1;Y)-\ell(\widehat\theta_0;Y)\right].
```

`Lambda(Y)` is the same statistic as NUM-DEC-03's `T_LR`, restated in this instruction's general point-process notation. Boundary null forbids automatic chi-square reference. Parametric-bootstrap calibration:

```math
Y^{*(b)}\sim p(Y\mid\widehat\theta_0,H_0), \qquad \Lambda^{*(b)}=2\left[\ell(\widehat\theta_1^{*(b)};Y^{*(b)})-\ell(\widehat\theta_0^{*(b)};Y^{*(b)})\right], \qquad \widehat p_{\mathrm{boot}}=\frac{1+\sum_b\mathbf 1\{\Lambda^{*(b)}\geq\Lambda_{\mathrm{obs}}\}}{B+1}.
```

Required order (`RESOLVED_BY_FROZEN_SPEC`, REQ-M2-012): exact-null test → excitation-existence decision → profile-likelihood magnitude uncertainty. Eleven bootstrap design sub-decisions (`B`, target MCSE, seed hierarchy, failed-fit policy, denominator policy, adaptive extension, critical-value estimation, exact-null generation contract, nonfinite/negative-LR treatment, calibration-validity criteria) are `OD-008`, `OPEN_REQUIRES_ADJUDICATION`.

---

## S3. M3 Exact-Null / Bayesian Model-Comparison Contract (W2-P3)

### S3.1 Exact null and S3.2 alternative (RESOLVED_BY_FROZEN_SPEC structure; M3-BLOCK-01 currently prevents representation)

```math
M_0:n=0\ (\Rightarrow\alpha=0,\ \lambda_0(t)=\mu), \qquad M_1:0<n<1.
```

Near-null substitutes (`n=epsilon`) are prohibited by the same rule already enforced for M2 (NUM-DEC-03) — independently required for M3, not automatically inherited (per NUM-DEC-03's own non-transfer note). **Currently blocked**: the live sampler clamps `n_branch` to `[EPS, 1-EPS]`, so `n=0` is unreachable (`M3-BLOCK-01`, status `OPEN`, not closed by this document — see `WAVE_2_M3_BLOCKER_CLOSURE_PROTOCOL.md`).

### S3.3 Prior model odds (RESOLVED_BY_FROZEN_SPEC, NUM-DEC-05)

```math
P(M_0)=P(M_1)=\tfrac12 \ \text{(primary)}, \qquad \text{mandatory sensitivity: }\{0.75/0.25,\ 0.50/0.50,\ 0.25/0.75\}.
```

### S3.4 Marginal likelihood, Bayes factor, posterior model probability (RESOLVED_BY_FROZEN_SPEC formulas, NUM-DEC-06; numeric computation NOT authorized)

```math
p(Y\mid M_k)=\int p(Y\mid\theta_k,M_k)\,p(\theta_k\mid M_k)\,d\theta_k, \qquad BF_{10}=\frac{p(Y\mid M_1)}{p(Y\mid M_0)}.
```

```math
\frac{P(M_1\mid Y)}{P(M_0\mid Y)}=BF_{10}\frac{P(M_1)}{P(M_0)}, \qquad P(M_1\mid Y)=\frac{BF_{10}P(M_1)}{BF_{10}P(M_1)+P(M_0)} \xrightarrow{\text{equal priors}} \frac{BF_{10}}{1+BF_{10}}.
```

**This formula is a contract term only.** It is never evaluated against historical data in Wave 2, and its numeric evaluation remains blocked by `M3-BLOCK-02` (unnormalized priors), `M3-BLOCK-03` (missing Jacobian), and `M3-BLOCK-06` (priors not frozen).

### S3.5 Prior contract (OPEN, Package E)

Priors `p(mu|M_k)`, `p(beta|M1)`, `p(n|M1)` must be proper, domain-consistent, not chosen for computational convenience alone, prior-predictively documented, sensitivity-prespecified, with explicit transform+Jacobian, checked for bridge-sampling compatibility, and (where shared parameters exist) consistent across `M0`/`M1`. `OD-009`, `OPEN_REQUIRES_ADJUDICATION`, blocked in part by `M3-BLOCK-06`.

### S3.6 Bridge sampling — primary marginal-likelihood method (RESOLVED_BY_FROZEN_SPEC as *method choice*, NUM-DEC-06; design OPEN, Package F)

```math
Z=p(Y)=\int q(\theta)\,d\theta,\ q(\theta)=p(Y\mid\theta)p(\theta), \qquad Z=\frac{\mathbb E_g[h(\theta)q(\theta)]}{\mathbb E_p[h(\theta)g(\theta)]}.
```

Fifteen design sub-decisions (sampling space, transform/Jacobian, proposal `g`, bridge function `h`, draw-count requirements, chain rules, convergence diagnostics, ESS requirements, repeated-run stability, overflow/underflow safeguards, log-scale computation, failure taxonomy, uncertainty estimate, reproducibility) are `OD-010`, `OPEN_REQUIRES_ADJUDICATION`, blocked by `M3-BLOCK-02/03/04/06`. No bridge sampling is run in this document.

### S3.7 Thermodynamic integration — secondary validation (RESOLVED_BY_FROZEN_SPEC as *method choice*, NUM-DEC-06; design OPEN)

```math
p_t(\theta\mid Y)\propto p(Y\mid\theta)^t p(\theta),\ 0\leq t\leq1, \qquad \log p(Y)=\int_0^1\mathbb E_t[\log p(Y\mid\theta)]\,dt.
```

```math
\Delta_{\mathrm{BTI}}=\left|\log\widehat Z_{\mathrm{bridge}}-\log\widehat Z_{\mathrm{TI}}\right|.
```

Ten design sub-decisions plus the escalation threshold are `OD-011`/`OD-012`, `OPEN_REQUIRES_ADJUDICATION`, blocked by `M3-BLOCK-05`. No temperature ladder, no TI run.

---

## S4. Cross-Reference: Model Comparison Required Order (RESOLVED_BY_FROZEN_SPEC, cross-document consistency)

```text
EXACT_NULL  ->  VALID_POSTERIOR_SAMPLING  ->  LOG_MARGINAL_LIKELIHOODS  ->
MODEL_EXISTENCE_PROBABILITY  ->  TAU_CALIBRATION  ->  INDEPENDENT_EVALUATION  ->  CONDITIONAL_MAGNITUDE_ESTIMATION
```

No step may be skipped or reordered by a future implementation. This is a binding contract term, not a preference.

---

## S5. Explicit Non-Claims

This document establishes contracts, not results. It does **not** claim: M0 final PASS; successful M2 recovery/coverage; successful M3 model selection; a selected tau value; a resolved ROPE; closure of any M3 blocker; execution of any of the 315 substantive future tests; authorization of historical inference; general failure of the Hawkes family (V1's `MODEL_VALIDATION_FAILURE` is candidate/implementation-specific — Hawkes family status remains `NOT_RULED_OUT`, per `MODEL_3B_FINAL_EPISTEMIC_STATUS.md` and `MODEL_3B_RECOVERY_TOURNAMENT_DESIGN.md`).

---

## S6. Acceptance-Criterion Registry (instruction §21)

| criterion_id | model_stage | quantity | formula_ref | threshold_status | threshold_value | threshold_source | denominator | failure_treatment | applicability | preregistered_before_execution |
|---|---|---|---|---|---|---|---|---|---|---|
| AC-M0-01 | M0-gate | score check | S1.4 | OPEN_REQUIRES_ADJUDICATION | NULL | none (OD-001) | n/a | SCORE_CHECK_FAILURE | all M0-gate runs | YES (required before any future run) |
| AC-M0-02 | M0-gate | Hessian symmetry | S1.6 | OPEN_REQUIRES_ADJUDICATION | NULL | none (OD-002) | n/a | HESSIAN_ASYMMETRY | all M0-gate runs | YES |
| AC-M0-03 | M0-gate | Hessian reference match | S1.6 | OPEN_REQUIRES_ADJUDICATION | NULL | none (OD-002) | n/a | HESSIAN_REFERENCE_MISMATCH | all M0-gate runs | YES |
| AC-M2-01 | M2 | RMSE(n) | S2.4 | OPEN_REQUIRES_ADJUDICATION | NULL | none | R_valid | n/a (diagnostic) | per cell | YES |
| AC-M2-02 | M2 | Coverage_c (or CoverAndValid_c, per OD-006) | S2.6 | OPEN_REQUIRES_ADJUDICATION | NULL | none (OD-006) | R_valid or R_attempted | n/a | per cell | YES |
| AC-M2-03 | M2 | AbsBias_c at exact null | S2.3 | OPEN_REQUIRES_ADJUDICATION | NULL | none (OD-005) | R_valid | n/a | n_c=0 cells only | YES |
| AC-M2-04 | M2 | exact-null bootstrap calibration validity | S2.8 | OPEN_REQUIRES_ADJUDICATION | NULL | none (OD-008) | B | LIKELIHOOD_RATIO_INVALID | exact-null cells | YES |
| AC-M3-01 | M3 | FSR_0(tau) | WAVE_2_TAU_CALIBRATION_PREREGISTRATION.md | OPEN_REQUIRES_ADJUDICATION | NULL | none (OD-013, NUM-DEC-04 pending) | R_0 | TAU_CALIBRATION_UNRESOLVED | exact-null replications | YES |
| AC-M3-02 | M3 | DP_j(tau) / power | WAVE_2_TAU_CALIBRATION_PREREGISTRATION.md | OPEN_REQUIRES_ADJUDICATION | NULL | none (OD-013) | R_j | TAU_CALIBRATION_UNRESOLVED | positive-excitation replications | YES |
| AC-M3-03 | M3 | Delta_BTI (bridge/TI agreement) | S3.7 | OPEN_REQUIRES_ADJUDICATION | NULL | none (OD-012) | n/a | MARGINAL_LIKELIHOOD_DISAGREEMENT | every model-comparison replication | YES |

No `threshold_value` is populated anywhere in this registry — every row is `NULL` with `threshold_status=OPEN_REQUIRES_ADJUDICATION`, per instruction §21's explicit prohibition on guessed thresholds.
