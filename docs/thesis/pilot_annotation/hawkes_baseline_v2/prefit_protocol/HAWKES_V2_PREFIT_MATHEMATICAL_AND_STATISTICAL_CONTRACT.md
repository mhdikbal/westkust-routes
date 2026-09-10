# HAWKES V2 — PRE-FIT MATHEMATICAL AND STATISTICAL CONTRACT

```
Authoritative HEAD = 2e12f68dbac609c9e50145ad86e7fb6051c11080
Operation date (UTC) = 2026-09-10
Current execution mode = READ-ONLY REPOSITORY AUDIT AND PROTOCOL CREATION ONLY
No model was fit. No likelihood was computed from historical data. No forecast,
simulation, bootstrap, calibration, or plot was produced in this operation.
```

Governing hierarchy: DIVERGENCE BEFORE CONVERGENCE · ONTOLOGY BEFORE
ESTIMATION · SOURCE CRITICISM BEFORE MODEL INPUT · OBSERVATION PROCESS
BEFORE SELF-EXCITATION · COMPARATOR FAMILY BEFORE HAWKES PREFERENCE ·
OUT-OF-SAMPLE PERFORMANCE BEFORE IN-SAMPLE CELEBRATION · UNCERTAINTY TYPING
BEFORE QUANTIFICATION · NO CAUSAL CLAIM FROM MODEL FIT ALONE.

## 0. Corpus-denominator distinction (load-bearing, applies to every section below)

```
AS86                        = 86 primary events (the primary analysis set)
Provenance-audit table      = 141 rows (docs/.../HAWKES_BASELINE_V2_EVENT_PROVENANCE_AUDIT.csv,
                               confirmed 141 data rows this operation)
AS86 != 141.                AS86 is a labeled SUBSET of the 141-row table, not the whole table.
```
Every coverage proportion in this contract states explicitly which of the
following denominators it uses: **86 primary events**, **141
provenance-audit rows**, **9 identified source objects**, **a separately
enumerated subset**, **parent episodes**, **report pairs**, or **temporal
units**. No proportion in this document treats 141 as if it were AS86, and
none treats all 141 rows as one homogeneous denominator without saying so.

```
G_corpus,v = 0
```
because no new immutable model-input corpus has been created after
applying the accepted prospective rules (`G_gran_accepted=G_parent_accepted=
G_same_accepted=1`, Wave 3B). **AS86 remains frozen and unchanged** — it
must not be used as though the new prospective rules had already been
applied to it.

## 1. Epistemic and observation-process contract

```
N_obs(t) = O{H(t), R(t), S(t), A(t), K(t)}
  H(t): latent historical-event process
  R(t): contemporary recording/reporting process
  S(t): archival survival/selection process
  A(t): present-day access/digitization process
  K(t): coding, normalization, deduplication, corpus-construction process
  N_obs(t): observed coded-event process available to any future model

Prohibited identity: N_obs(t) = H(t)

Causal estimand (unidentified):
  tau(Delta) = E[ N^do(E=1)(t,t+Delta) - N^do(E=0)(t,t+Delta) ]

Therefore: G_causal = 0
```
No likelihood, p-value, Bayes factor, information criterion, residual
diagnostic, or forecast score computed under any future authorized fit may
promote `G_causal`.

**Formula contract (complete structural contract, not an estimator):**
domain = historical time `t in [T_0,T_1]` (window declared §10); purpose =
epistemic decomposition of the observed coded-event process; estimand =
`NOT_APPLICABLE_WITH_REASON` (this is a process relation, not itself an
estimator); denominator = `NOT_APPLICABLE_WITH_REASON` (a structural
identity, not a count-based ratio); gate = `G_observation` (currently 1 at
accepted-design level only — this decomposition is designed and named, nothing
more); stop condition = stop any causal or self-excitation interpretation
that treats the observed corpus `N_obs(t)` as the latent historical process
`H(t)` itself.

## 2. Corpus-version and analysis-unit contract

A future model-ready corpus version *v* requires: immutable version
identifier; external SHA-256; exact row count; explicit inclusion/exclusion
rules; event-unit definition; date-role policy; unresolved-case policy;
source-family coverage statement; parent-episode representation policy;
report-to-occurrence mapping policy; provenance path per included row.

```
E_v = event set of corpus version v;  N_v = |E_v|
G_corpus,v = 1[Exists_v=1 AND Version_v=1 AND Hash_v=1 AND Denom_v=1
               AND Prov_v=1 AND Schema_v=1]
  Exists_v:  a materialized version-tagged corpus file exists
  Version_v: it carries an explicit immutable version identifier
  Hash_v:    an external SHA-256 is registered for it
  Denom_v:   its row-count denominator and inclusion/exclusion rule are explicit
  Prov_v:    every included row has a provenance path
  Schema_v:  event-unit/date-role/unresolved-case/source-family/parent-episode/
             report-mapping policies are all declared (per this section's
             opening paragraph)
Current: G_corpus,v = 0  (no such version exists yet)
```

## 3. Granularity and report-to-occurrence readiness (accepted rule, not yet applied)

```
Gamma_i = (I_i, A_i, J_i, T_i, S_i, C_i, P_i)   [instrument identity, actor set,
  juridical act, time/date-role, spatial status, source context, provenance]
X_ik in {SATISFIED, FAILED, CONFLICTING, NOT_EVALUABLE}

Omega_ij = (A_ij, J_ij, T_ij, S_ij, X_ij^dep, D_ij^distinct, P_ij)
X_ij^dep in {INDEPENDENT, PARTIALLY_DEPENDENT, TEXTUALLY_DEPENDENT, DEPENDENCE_NOT_EVALUABLE}
D_ij^distinct: distinctness marker between events i and j — whether i and j
  are asserted as the same underlying occurrence, distinct occurrences, or
  undetermined; separate from X_ij^dep (textual/reporting dependence), since
  two reports can be dependent in text while still describing distinct events
Compatibility is not independent corroboration.

P_gran     = N_{included rows with explicit prospective granularity assessment} / N_{rows included under the declared assessment rule}
P_gran_open = N_{included rows retained as unresolved granularity} / N_{rows assessed}
```
**Current state:** the accepted prospective rule (Wave 3B, `G_gran_accepted=
G_parent_accepted=1`) has been tested on 5 hand-selected repository cases
(TEST-01..05) plus 3 stress/holdout cases (STRESS-01, HOLDOUT-01,
HOLDOUT-02) — **not applied to any of the 86 or 141 corpus rows as a
corpus-wide pass.** `P_gran` and `P_gran_open` are therefore **NOT
COMPUTABLE** against either the 86- or 141-row denominator today; a
corpus-wide application is a separate, not-yet-authorized future operation.
No threshold for either proportion may be invented after seeing results.

## 4. Date-role and temporal-precision contract

```
D_i = (v_i, r_i, p_i, l_i, u_i, s_i, b_i)
  v: recorded date value   r: date role   p: precision
  l,u: lower/upper time bounds   s: source/locator   b: evidentiary basis

Allowed roles: EVENT_DATE, REPORT_DATE, DISPATCH_DATE, RECEIPT_DATE,
  RESOLUTION_DATE, COMPILATION_DATE, PUBLICATION_DATE, PROXY_DATE,
  BOUNDED_INTERVAL, UNRESOLVED_DATE_ROLE

G_date,i = 1[r_i != UNRESOLVED_DATE_ROLE AND l_i<=u_i AND s_i=1 AND b_i=1]
P_date = sum_i G_date,i / N_{events assessed}
```
Do not impute day-level dates from month-only or dispatch dates merely to
satisfy point-process input requirements. Future temporal representations
must be predeclared separately: (1) exact-day subset; (2) bounded-interval
treatment; (3) multiple-imputation, only with a defensible imputation law;
(4) lower/upper-bound sensitivity; (5) exclusion of unresolved-role cases.
No one representation may be silently designated authoritative.

**Current corpus-wide precision distribution** (denominator = **141
provenance-audit rows**, `HAWKES_BASELINE_V2_DATE_UNCERTAINTY_LEDGER.csv`,
re-confirmed Wave 1, not recomputed here): EXACT_DAY 72 (51.1%), MONTH_ONLY
10 (7.1%), YEAR_ONLY 16 (11.3%), INTERVAL 21 (14.9%), UNRESOLVED 22 (15.6%).
**This is precision, not date role** — the 10-role taxonomy above has not
been applied to assign an explicit `r_i` to any of the 141 rows; `G_date,i`
is therefore `NOT_EVALUABLE` for all 141 rows today, not computably 0 or 1.

## 5. Binomial and proportion-based validation

Binomial methods are permitted **only** for explicitly binary, bounded
audit outcomes — never as a test of Hawkes self-excitation.

```
Y_i in {0,1};  X = sum_i Y_i;  X ~ Binomial(n,p);  p_hat = X/n
p-value (exact, two-sided, vs. prespecified p_0):
  p = P_p0{ P_p0(X=x) <= P_p0(X=x_obs) }
```
`p_0` must derive from a prespecified requirement or justified external
benchmark — never invented post hoc.

### 5.1 Clopper-Pearson exact interval
```
p_L = B^-1(alpha/2 ; X, n-X+1)
p_U = B^-1(1-alpha/2 ; X+1, n-X)
```
(boundary conventions apply at X=0 or X=n)

### 5.2 Wilson interval
```
z = z_{1-alpha/2}
p_tilde = (p_hat + z^2/(2n)) / (1 + z^2/n)
h = z/(1+z^2/n) * sqrt( p_hat(1-p_hat)/n + z^2/(4n^2) )
Interval = [p_tilde - h, p_tilde + h]
```
For small denominators, report exact and Wilson intervals as descriptive
sensitivity, never as competing "truth" estimates.

### 5.3 Permitted audit applications
Date-ready rows; provenance-complete rows; actor-normalization-complete
rows; source-family coverage units; granularity-assessed rows;
contradiction-audited pairs; diagnostic simulations meeting a prespecified
recovery criterion. **Never** used to infer that historical events are
independent and identically distributed.

### 5.4 Exchangeability gate
```
G_binomial = 1[binary_estimand=1 AND denominator_declared=1
               AND exchangeability_defensible=1 AND p0_justified_if_tested=1]
```
If `G_binomial=0`: report counts and proportions only — no inferential
binomial p-value.

## 6. Beta-binomial and overdispersion boundary

```
p_i ~ Beta(alpha,beta);  X|p_i ~ Binomial(n,p_i);  X ~ BetaBinomial(n,alpha,beta)
E[X] = n*alpha/(alpha+beta)
Var(X) = n*mu*(1-mu)*[1+(n-1)*rho],  mu=alpha/(alpha+beta), rho=1/(alpha+beta+1)
```
Use only if group structure, repeated units, and exchangeability are
substantively defensible. Not a generic container for deep historical
uncertainty.

## 7. Count-process comparator family (design only — none registered/executed)

### 7.1 Homogeneous Poisson
```
N(t,t+Delta) ~ Poisson(mu*Delta);  lambda(t)=mu
ell(mu) = n*log(mu) - mu*T;  mu_hat = n/T
```
### 7.2 Inhomogeneous Poisson
```
lambda(t) = exp{beta_0 + beta^T x(t)}
ell(beta) = sum_i log(lambda(t_i)) - integral_0^T lambda(s) ds
```
Covariates: external, prespecified, non-outcome-derived only. ACT-07
circular candidates (Wave 3A candidates 4–5, `DESCRIPTIVE_ONLY_CIRCULAR`)
are **prohibited** as covariates or offsets.
### 7.3 Piecewise-constant Poisson
```
lambda(t) = mu_k for t in I_k (prespecified intervals)
```
Do not choose breakpoints by inspecting event peaks and treat the result as
confirmatory.
### 7.4 Renewal comparator
```
W_i = t_i - t_{i-1};  W_i ~ F_W(theta)
```
Candidate families (exponential, Weibull, gamma) must be prespecified.
Tests duration dependence without event-triggered offspring interpretation.

## 8. Hawkes model registry (design only — none fit)

```
lambda(t | H_t) = mu(t) + sum_{t_i<t} g(t-t_i)
```
### 8.1 Exponential kernel
```
g(u) = eta*beta*e^(-beta*u) * 1[u>0]
  eta >= 0: branching ratio under the normalized kernel
  beta > 0: decay rate; 1/beta: characteristic memory timescale
integral_0^inf g(u) du = eta
Stationarity (constant baseline): 0 <= eta < 1
```
`eta` is **never** interpreted as a historically causal fraction of
resistance events.
### 8.2 Alternative kernels
Only prespecified: exponential; sum-of-exponentials; power-law;
nonparametric (only with prespecified data support/regularization). Each
additional kernel increases researcher degrees of freedom and requires
explicit scientific rationale.
### 8.3 Multitype/marked Hawkes
```
lambda_k(t) = mu_k(t) + sum_j sum_{t_i^(j)<t} g_kj(t - t_i^(j))
```
**Blocked in this corpus today:** type labels must be source-critical,
prospectively defined, sufficiently supported, and not merely colonial
categories or project-normalized labels. `event_type="konflik"` is
`PROJECT_NORMALIZED_LABEL` (Wave 3B category-origin audit) — not a valid
type label for a multitype specification without a separate, source-critical
re-derivation (R-O7, still `NOT_EVALUABLE`).

## 9. Hawkes likelihood and parameter constraints

```
ell(theta) = sum_i log(lambda(t_i|H_{t_i};theta)) - integral_0^T lambda(s|H_s;theta) ds
```
Requirements: `lambda(t)>0` throughout; `mu(t)>=0`; kernel non-negativity
unless inhibition is separately modeled/justified; `0<=eta<1` for stationary
exponential Hawkes; declared initialization, optimizer, tolerance,
parameter bounds, multiple starting values, convergence diagnostics.
**Optimization success alone is not scientific validity.**

## 10. Observation window and edge effects

Declare `[T_0,T_1]` with: why it begins/ends there; left/right-censoring
risk; missing prehistory; treatment of source-free/access-poor periods;
whether burn-in is simulation-only; whether likelihood conditions on
observed prehistory. Absence of coded events near a boundary is **never**
treated as absence of historical activity.

## 11. Exposure and opportunity contract

```
lambda_obs(t) = E(t) * lambda_latent_proxy(t)   [future offset model, only if E(t) qualifies]
R_E(m) = 1[A_m=1 AND X_m=1 AND C_m=1 AND T_m=1 AND P_m=1]
  A: data exist/accessible  X: external to coded-outcome  C: coverage domain defined
  T: temporal comparability established  P: provenance complete
Current: G_ACT07^execute = 0  ->  no exposure-adjusted model may be fitted now
```

## 12. Train/test logic for point processes

Random row-wise splitting is **prohibited** (destroys temporal order). Use
`[T_0,T_train], (T_train,T_test]`. Permitted: rolling-origin evaluation;
blocked temporal CV; leave-period-out; leave-source-family-out sensitivity;
episode-level sensitivity under the accepted prospective rule.
```
LS_k = sum_{t_i in Test_k} log(lambda_hat_{-k}(t_i)) - integral_{Test_k} lambda_hat_{-k}(s) ds
LS_bar = (1/K) sum_k LS_k
```
No superiority claim from in-sample likelihood alone.

## 13. Information criteria (secondary diagnostics only)

```
AIC = 2k - 2*ell(theta_hat)
BIC = k*log(n) - 2*ell(theta_hat)
```
Not substitutes for temporal out-of-sample scores, residual diagnostics, or
source-sensitivity analysis. If effective sample size is ambiguous due to
dependent event times, that limitation must be reported explicitly.

## 14. Time-rescaling diagnostics

```
z_i = integral_{t_{i-1}}^{t_i} lambda_hat(s) ds;  under correct specification z_i ~approx~ Exponential(1)
u_i = 1 - e^(-z_i);  u_i ~approx~ Uniform(0,1)
```
Required: exponential QQ; uniform QQ; KS statistic with stated limitations;
autocorrelation of transformed residuals; cumulative residual plot;
residual checks by period and source family. **No single p-value may accept
the model.**

## 15. Dispersion and count diagnostics

```
Y_bar = (1/B) sum_b Y_b;  S_Y^2 = (1/(B-1)) sum_b (Y_b - Y_bar)^2
D_disp = S_Y^2 / Y_bar
```
`D_disp` (renamed from bare `D` to avoid collision with `D_ij^distinct`,
`D_q^denom`, and `N_dup,f` elsewhere in this document family). `D_disp>1` may indicate clustering, nonstationarity, exposure variation, or
observation-process heterogeneity — it does **not** uniquely imply
self-excitation. Fano-factor comparisons require prespecified bin widths
plus multiple-width sensitivity.

## 16. Pair-correlation and inter-event diagnostics

```
W_i = t_i - t_{i-1}
B_burst = (sigma_W - mu_W) / (sigma_W + mu_W)
```
`B_burst` (renamed from bare `B` for the same collision-avoidance reason as
`D_disp` above). Report: empirical survival function; coefficient of variation; burstiness
(with limitations); comparison with exponential/renewal alternatives;
sensitivity to tied/interval-censored dates. `B_burst>0` is **not** proof of
Hawkes excitation.

## 17. Calibration and count-forecast diagnostics (future authorized use only — forecasting prohibited now)

```
N_hat_j = integral_{I_j} lambda_hat(t) dt
MAE = (1/J) sum_j |N_j - N_hat_j|
RMSE = sqrt( (1/J) sum_j (N_j - N_hat_j)^2 )
Coverage_{1-alpha} = (1/J) sum_j 1[N_j in PI_{j,1-alpha}]
```
These evaluate prediction under the observed corpus, not historical truth.

## 18. Simulation-recovery contract for a future, genuinely new model family

**Phase D is closed and must not be rerun.** This section specifies formulas
only for a future, separately authorized, genuinely new model family:
```
Bias(theta_hat) = E[theta_hat - theta]
RMSE(theta_hat) = sqrt(E[(theta_hat-theta)^2])
Coverage_{1-alpha} = P{theta in CI_{1-alpha}(theta_hat)}
RBias(theta_hat) = E[theta_hat-theta] / theta
```
Recovery scenarios must vary: event count; observation window; baseline
nonstationarity; branching ratio; decay timescale; timestamp precision;
missingness; duplicate/report-bundle contamination; source-family exposure
heterogeneity. No recovery threshold chosen after seeing results.

## 19. Sensitivity-analysis registry (prospective, future arms only)

Minimum arms: exact-day subset; lower-bound dates; upper-bound dates;
interval-censored treatment; proxy-date exclusion; source-family leave-out;
parent-episode child representation; parent-episode earliest-date
representation; parent-episode latest-date representation;
unresolved-granularity exclusion; alternative baselines; alternative
kernels. **Closed Phase D arms are not rerun**; any new arm requires a new
purpose, estimand, and authorization.
```
S = (S_1, ..., S_A)   -- full vector reported, never only the most favorable arm
```

## 20. Multiple testing and researcher degrees of freedom

```
alpha* = alpha / M   (Bonferroni, M = number of formal tests)
```
Benjamini-Hochberg may be specified for exploratory false-discovery control
— it does **not** convert exploratory tests into confirmatory causal
evidence. Prefer a small set of primary estimands/diagnostics; do not
generate dozens of p-values from kernel/window/source/date/episode variants.

## 21. Primary and secondary estimands

**Primary (registered):**
```
Delta_LS = LS_bar_Hawkes - LS_bar_best_non_Hawkes_comparator
```
(temporal out-of-sample log-score difference — predictive adequacy for the
observed corpus, nothing more).

**Comparator-selection rule (leakage-safe, resolves the previously undefined
"best" comparator):**
```
M_C = {CMP-01, CMP-02, CMP-03, CMP-04}                    (frozen comparator set)
m*_k = argmax_{m in M_C} LS_{m,k}^validation                (inner-validation fold k)
Delta_LS_k = LS_{HWK01,k}^test - LS_{m*_k,k}^test            (held-out comparison only)
Delta_LS_bar = (1/K) sum_k Delta_LS_k
```
The comparator must never be selected on the same test interval used to
report Hawkes's advantage. If nested temporal validation proves infeasible
for a given fold structure, one comparator must be frozen before any
test-fold evaluation and the limitation disclosed alongside the estimand —
never chosen post hoc.

**Secondary:** branching ratio `eta`; decay timescale `1/beta`;
baseline-intensity parameters; time-rescaling residual statistics;
source-family sensitivity; date-representation sensitivity;
episode-representation sensitivity. No secondary estimand may replace the
primary estimand after results are seen.

## 22. Model-reconsideration gate

```
G_reconsider = 1[ G_corpus=1 AND G_gran_application=1 AND G_date=1 AND G_observation=1
                   AND G_exposure_decision=1 AND G_comparators^accepted=1
                   AND G_primary_model^accepted=1 AND G_estimands^accepted=1
                   AND G_diagnostics^accepted=1 AND G_sensitivity^accepted=1
                   AND G_stop^accepted=1 AND A_reconsider=1 ]
```
The `^accepted` superscript on the registry terms distinguishes *design-level
acceptance* (a registry has been reviewed and accepted as a design, but
nothing in it has been implemented or authorized to execute) from a
hypothetical fully execution-ready gate of the same name — these are not
interchangeable, and this formula uses only the design-accepted form.

**Current value:**
```
G_corpus=0  G_gran_application=0  G_date=0  G_observation=1
G_exposure_decision=0  G_comparators^accepted=1  G_primary_model^accepted=1
G_estimands^accepted=1  G_diagnostics^accepted=1  G_sensitivity^accepted=1
G_stop^accepted=1  A_reconsider=0
0 AND 0 AND 0 AND 1 AND 0 AND 1 AND 1 AND 1 AND 1 AND 1 AND 1 AND 0 = 0
G_reconsider = 0
```
Full component decomposition is in the readiness ledger (output 2). This
zero is a closed fit-admission gate, not an empirical rejection of any
model — every accepted-design term is 1; the closure comes entirely from
the corpus/granularity/date/exposure/researcher-authorization terms.

## 23. Fit-admission gate

```
G_fit,m = 1[ G_reconsider=1 AND corpus_hash=registered AND model_m=registered
             AND optimizer_m=registered AND seed_m=registered
             AND output_path_m=registered AND stop_conditions_m=registered ]
Current: G_fit,m = 0 for all m
```
No code path may fit a model while this value is zero.

## 24. Stop conditions for future fitting

Stop if: fitted intensity becomes nonpositive; optimizer fails across
prespecified starts; branching ratio violates the registered stability
domain; parameter estimates remain on imposed bounds; Hessian/uncertainty
estimate is singular/unusable; time-rescaling diagnostics fail materially;
predictive score does not improve over the best comparator; conclusions
reverse under source-family or date-role sensitivity; exposure is circular
or provenance-incomplete; corpus hash differs from the registered input;
numerator/denominator shifts without disclosure; a prohibited model is
relabeled as a diagnostic; any causal language is inferred from fit alone.

Allowed terminal tokens: `FIT_COMPUTATION_FAILED`, `FIT_DIAGNOSTICS_FAILED`,
`FIT_NOT_BETTER_THAN_COMPARATOR`, `FIT_SENSITIVE_TO_CORPUS_CONSTRUCTION`,
`FIT_EXPLORATORY_ONLY`, `FIT_ACCEPTABLE_FOR_OBSERVED_CORPUS_PREDICTION`.
**`HAWKES_VALIDATED` is never used.**

## 25. UI and production boundary

`/atlas/riset/pemodelan/`, `/atlas/linimasa`, frontend routes, API
endpoints, Bokeh dashboards, and production files are **not modified** by
this or any future pre-fit operation without separate authorization. Model
outputs may appear on `/atlas/riset/pemodelan/` only after an authorized
fit, and must display corpus version, estimand, comparator, diagnostics,
and non-causal limitations. Timeline granularity caveats may appear only
through a separately authorized non-mutating metadata layer.

## 26. Read-only audit findings (this operation, repository evidence only)

Component-level findings are recorded in
`HAWKES_V2_PREFIT_READINESS_AND_DENOMINATOR_LEDGER.csv`, which separates
`object_type`, `design_status`, `acceptance_status`, `implementation_status`,
`data_status`, `authorization_status`, `execution_status`, `scientific_status`,
and per-axis gates for every component individually. A single collapsed
one-line-per-topic summary is deliberately not repeated here: doing so
previously conflated distinct ontological classes (e.g. a verified
source-object metadata result and an unaudited project-wide coverage claim
under one word, `READY`). Read the ledger for the current, disaggregated
findings; nothing in it authorizes fitting, and `G_corpus,v=0` throughout.

Graphify coverage of this package: `GRAPHIFY_VERIFIED_AVAILABLE_NOT_RUN_
STALE_GRAPH_ZERO_CURRENT_PACKAGE_COVERAGE` — the repository's Graphify graph
(`graphify-out/graph.json`) was built at a commit that predates this entire
pre-fit package and has zero node coverage of it (`P_graph_coverage=0/13`).
It was not rebuilt for this operation (`GRAPHIFY_REBUILD_DECISION=
DEFER_UNTIL_SCOPED_LOCAL_DETERMINISTIC_INGESTION_IS_AVAILABLE`); findings
above come from direct file reads and hash verification, not from the graph.

## 27. Frozen state — confirmed unchanged

```
Hawkes fitting = SUSPENDED, Hawkes visualization = SUSPENDED
G_reconsider_future = 0, G_ontology = 0, G_causal = 0
DEDUP-06 = UNRESOLVED, G_DEDUP06 = 0, R-O4 = FAIL, AS86 = FROZEN_UNCHANGED
ACT07_EXECUTION_DECISION = DEFER, G_ACT07_execute = 0
V2-B = BLOCKED, Phase D = CLOSED / MUST NOT BE RERUN
```

## 28. Final status

```
HAWKES_V2_PREFIT_MATHEMATICAL_PROTOCOL_COMPLETE_G_RECONSIDER_ZERO_FITTING_REMAINS_SUSPENDED
```
This status does not authorize fitting.

**Pausing for researcher adjudication.**
