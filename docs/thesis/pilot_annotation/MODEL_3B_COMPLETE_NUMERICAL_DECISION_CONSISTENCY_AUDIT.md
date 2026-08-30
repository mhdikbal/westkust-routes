# Model 3B Complete Numerical-Decision Consistency Audit

> **Design/documentation alignment only.** No M0, M2, or M3 source file is modified or created. No estimator is created. No benchmark, bootstrap, bridge sampling, thermodynamic integration, calibration set, or tournament is executed. No historical data is fitted. Nothing is staged, committed, pushed, or deployed by this audit.

## 1. Scope

This audit covers all eight adjudicated numerical decisions (`NUM-DEC-01` through `NUM-DEC-08`) on `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv`, verifies their mutual mathematical and structural consistency, and records the additive integration of those decisions into the five V2 specification files. It does not authorize implementation, execution, or historical fitting.

## 2. Authoritative Inputs

Complete amendment commit: `da8c04d70f6ba107a14822fbd6da547f2f7f395d`. Five V2 working files (`MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md`, `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`, `MODEL_3B_RECOVERY_PROTOCOL_V2.md`, `MODEL_3B_FINAL_GATE_APPLICABILITY_MATRIX.csv`, `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv`); two supporting reconciliation files (`MODEL_3B_GATE_V1_TO_V2_RECONCILIATION.csv`, `MODEL_3B_V2_NUMERICAL_DECISION_DIGEST.md`); eight numerical adjudication documents (`MODEL_3B_NUM_DEC_01` through `_08`). All read in full before this audit.

## 3. Final Numerical Decision Distribution

Mechanically parsed from `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv` (8 data rows, unique IDs `NUM-DEC-01`–`08`, zero malformed rows, zero blank required fields):

```text
APPROVED_WITH_LIMITATIONS (7): NUM-DEC-01, NUM-DEC-02, NUM-DEC-03, NUM-DEC-04, NUM-DEC-05, NUM-DEC-06, NUM-DEC-08
DEFERRED (1):                  NUM-DEC-07
PENDING_RESEARCHER_DECISION (0)
```

All `implementation_blocking` / `execution_blocking` / `historical_fit_blocking` values across all 8 rows = `NO` (not authorized). No ledger row was found to contradict its governing adjudication document; no correction to the ledger was required.

## 4. Dependency Graph

Verified against `MODEL_3B_NUMERICAL_DECISION_DEPENDENCY_MATRIX.csv` (created by this audit, 8 rows, one per decision):

```text
NUM-DEC-01 -> M2 attempted-replication accounting                      (no upstream dependency)
NUM-DEC-02 -> M2 profile-likelihood uncertainty for n                  (depends on NUM-DEC-01's accounting)
NUM-DEC-03 -> M2 exact-null nested comparison                          (depends on NUM-DEC-01; informs NUM-DEC-02's boundary)
NUM-DEC-05 -> M3 model prior odds                                      (no upstream dependency)
NUM-DEC-06 -> M3 log marginal likelihood and log_BF_10                 (no upstream dependency)
NUM-DEC-04 -> M3 tau calibration procedure                             (depends on NUM-DEC-05 AND NUM-DEC-06)
NUM-DEC-07 -> ROPE deferred, not required for first tournament         (independent of exact-null existence question)
NUM-DEC-08 -> measured nonproduction resource envelope                 (depends on cost components from NUM-DEC-01/02/03/04/05/06/07)
```

Result: `NO_CIRCULAR_DEPENDENCY` (mechanically verified — the dependency matrix's `circular` column is `NO` for all 8 rows); `NO_MISSING_GOVERNING_DECISION` (every M2/M3 quantity referenced across the V2 files traces to exactly one of the 8 decisions or to a pre-existing amendment); `NO_IMPLEMENTATION_BEFORE_SPECIFICATION` (all 8 `implementation_blocking` = NO, and no `.py` file was touched by any of the 8 adjudication turns or by this audit); `NO_HISTORICAL_FIT_AUTHORIZATION` (all 8 `historical_fit_blocking` = NO).

## 5. M2 Mathematical Consistency

Verified consistent across `MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md` and all three M2 adjudications: kernel `g(u) = alpha * exp(-beta*u)`; primary estimand `n = alpha/beta`; prospective reconstruction `alpha = n*beta`; parameter limits `0 <= n < 1, beta > 0`. No contradictory parameterization found in any V2 document.

## 6. M2 Replication Accounting

`NUM-DEC-01`: exactly 1,000 attempted replications per cell (not 1,000 successful); `R_attempt = R_valid + R_failed + R_invalid`; failed scientific runs never replaced; `R_attempt`, `R_valid`, `R_metric` remain distinct denominators throughout; infrastructure resume reuses the same replication ID and seed (never a new seed). Consistent with `NUM-DEC-02`'s bootstrap-coverage reporting and `NUM-DEC-03`'s bootstrap-calibration reporting, both of which explicitly inherit this accounting convention.

## 7. M2 Uncertainty

`NUM-DEC-02`: profile likelihood is the primary uncertainty method for `n`; parametric bootstrap validates coverage secondarily; Wald/inverse-Hessian interval is diagnostic-only, never primary; Bayesian posterior intervals are not selected for M2 (M2 remains likelihood-based). Interior candidate critical value `chi-square(1, 0.95) ~= 3.841`, explicitly not valid at the `n=0` boundary — boundary handling is deferred to `NUM-DEC-03`, consistent with that document's own explicit statement of the same deferral.

## 8. M2 Exact Null

`NUM-DEC-03` (completeness-corrected: verified exactly 30 sections, 30 `M2-NULL-001`–`030` tests, checksum `a7e8ad2cc058e8bb7e2b3ce6b920bfb09e372d420f9bc4c3bff3f2bb54af7aeb`, unchanged by this audit): `H0: n=0` represented as an explicit nested null submodel (never `epsilon`-clipping or a finite logit transform); `H1: 0<n<1`; nuisance parameters reoptimized independently under `H0` and `H1`; `T_LR = 2*(ell_1 - ell_0)`; boundary critical value calibrated by parametric bootstrap under the exact null, not the interior chi-square(1) reference (recorded only as a diagnostic). Calibration and evaluation sets remain separate. Required order verified present and unviolated in all three M2 documents: `EXACT_NULL_MODEL_COMPARISON -> EXCITATION_EXISTENCE_DECISION -> PROFILE_LIKELIHOOD_UNCERTAINTY_FOR_N_CONDITIONAL_ON_H1`. `PROFILE_INTERVAL_EXCLUDES_ZERO` is nowhere used as an automatic substitute for the exact-null test — `NUM-DEC-02` §16 and `NUM-DEC-03` §19 both explicitly label it diagnostic-only.

## 9. M3 Mathematical Consistency

Verified consistent across all four M3 adjudications and the mathematical specification: `M0: n=0`; `M1: 0<n<1`; primary decision quantity `P(M1|Y)`; posterior odds `P(M1|Y)/P(M0|Y) = BF_10(Y)*P(M1)/P(M0)`; numerically stable log form `logit[P(M1|Y)] = log_BF_10 + log[P(M1)/P(M0)]`. No contradictory formula found.

## 10. M3 Prior Model Odds

`NUM-DEC-05`: primary synthetic-calibration scenario `P(M0)=P(M1)=0.50` (prior odds = 1); mandatory sensitivity grid `{0.75/0.25 null-favoring, 0.50/0.50 equal, 0.25/0.75 excitation-favoring}`, explicitly synthetic calibration settings, not historical beliefs. `NUM-DEC-04` and `NUM-DEC-06` both correctly treat these as inputs rather than re-deriving or overriding them.

## 11. M3 Marginal Likelihood

`NUM-DEC-06` (compatibility classification `FEASIBLE_WITH_IMPLEMENTATION_WORK`, independently re-verified by the coordinator against `m3_bayesian_discrete.py` earlier this session): primary method bridge sampling; secondary validation thermodynamic integration on a prespecified subset; primary comparison `log_BF_10 = log_m1 - log_m0`. Proper normalized priors required; transformation Jacobians required; posterior diagnostics required before evidence estimation; harmonic-mean estimator rejected; Savage-Dickey not selected as primary; BIC confirmed not a marginal-likelihood substitute; WAIC/PSIS-LOO confirmed to remain predictive diagnostics only (consistent with the pre-existing `waic()` function's role in `m3_bayesian_discrete.py`, which the compatibility audit found already correctly scoped).

## 12. M3 Tau Calibration

`NUM-DEC-04`: candidate grid `{0.50, 0.75, 0.90, 0.95, 0.975, 0.99}` for future comparison only; final tau explicitly `NOT_SELECTED` — grep-verified no line in that document asserts a frozen numeric tau as final (the sole `tau=0.95` occurrence is inside "Prohibited Automatic Selection Rules", rejecting that shortcut). Required calibration: `max` over mandatory null scenarios of `FPR_hat_s(tau) <= 0.05` (worst-case rule, approved as default); FNR and power evaluation mandatory jointly; calibration and evaluation seed sets independent; outcome categories `EXCITATION_SUPPORTED / NO_EXCITATION_SUPPORTED / INCONCLUSIVE`. Correctly depends on `NUM-DEC-05` (prior odds) and `NUM-DEC-06` (comparison method) per the mathematical dependency `P(M1|Y)/P(M0|Y) = BF_10(Y)*P(M1)/P(M0)` — tau cannot be calibrated before both are fixed.

## 13. M3 ROPE Deferral

`NUM-DEC-07`: `epsilon_n` remains `UNSPECIFIED`; ROPE status `DEFERRED / OPTIONAL_SUPPLEMENTARY_MAGNITUDE_DIAGNOSTIC / NOT_REQUIRED_FOR_FIRST_TOURNAMENT`. Verified nowhere is `P(n<=epsilon_n | Y, M1)` represented as equivalent to `P(M0|Y)` — the two adjudication documents (`NUM-DEC-03` and `NUM-DEC-07`) both state this distinction independently and consistently. Required M3 order verified present: `EXACT_NULL -> VALID_POSTERIOR_SAMPLING -> LOG_MARGINAL_LIKELIHOODS -> MODEL_EXISTENCE_PROBABILITY -> TAU_CALIBRATION -> INDEPENDENT_EVALUATION -> CONDITIONAL_MAGNITUDE_ESTIMATION`.

## 14. Resource Envelope

`NUM-DEC-08`: execution environment `DEDICATED_NONPRODUCTION_RESEARCH_ENVIRONMENT`; production execution `PROHIBITED`; all 8 exact numerical ceilings (max concurrent workers, max wall-clock per wave, max total CPU-hours, max peak memory, max working disk, minimum free disk, max output size, checkpoint interval — plus retry count) remain `PENDING_MEASUREMENT`, grep-confirmed no arbitrary round number ("8 hours", "16 CPU", "32 GB", "100 GB") was adopted as a ceiling anywhere. Cost-model formulas (`T_serial_hat`, `T_parallel_hat`, `T_total_hat`, `T_budget`, `S_total_hat`, `M_peak_hat`) present and internally consistent. Explicitly built from existing pilot-log evidence only (M0: 15 cells × 1,000 attempted, 0.174–0.491 s/replication; M2: 4 cells × 150 attempted — pilot scale, point-fit only, excludes profile-likelihood/bootstrap cost mandated by `NUM-DEC-02`/`03`; M3: 4 cells × 200 attempted — single unconstrained-n MCMC only, excludes the cost of separate M0/M1 posteriors, bridge sampling, and thermodynamic integration mandated by `NUM-DEC-04`/`05`/`06`) — no new benchmark was run to produce it.

## 15. Confirmed Implementation Blockers

Preserved unresolved by this audit (none marked fixed): (1) `n_branch` clamped to `[EPS, 1-EPS]` in `_to_unconstrained()` — exact `n=0` structurally unreachable; (2) exact `n=0` absent from the current M3 implementation's support; (3) `log_prior()` omits normalization constants for the Beta(2,2) and Gamma(2,1) prior components; (4) the MCMC proposal in `fit_m3_mcmc()` is generated in unconstrained space; (5) the acceptance ratio is computed from the constrained-space `log_posterior` with no Jacobian correction for the unconstrained reparameterization; (6) bridge sampling does not exist in the codebase (grep-confirmed zero matches for "bridge"); (7) thermodynamic integration does not exist in the codebase (grep-confirmed zero matches for "thermodynamic"); (8) internal parameter priors are not yet versioned and frozen as a separate decision. All 8 independently re-confirmed present in `m3_bayesian_discrete.py` by the coordinator during the `NUM-DEC-06` turn; none touched by this audit.

## 16. Placeholder Standardization

Applied to `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`: exactly 4 cells changed, all in the `threshold_status` column: `GATE-030-V2`, `GATE-031-V2-REPL-B`, `GATE-031-V2-REPL-C`, `GATE-031-V2-REPL-D`, each from `UNRESOLVED_REQUIRES_TAU` to `PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION`. Full mapping applied (only the tokens actually present in the working files were found and changed; the other seven mapping entries in the researcher's instruction were checked and found not to literally occur elsewhere in the five V2 files as bare tokens, so no further cells required edits):

```text
UNRESOLVED_REQUIRES_REPLICATION_DENOMINATOR      -> RESOLVED_BY_NUM_DEC_01           (not found as a literal token; no edit needed)
UNRESOLVED_REQUIRES_N_UNCERTAINTY_METHOD         -> RESOLVED_BY_NUM_DEC_02           (not found as a literal token; no edit needed)
UNRESOLVED_REQUIRES_M2_EXACT_NULL                -> RESOLVED_BY_NUM_DEC_03           (not found as a literal token; no edit needed)
UNRESOLVED_REQUIRES_TAU                          -> PROCEDURE_RESOLVED_BY_NUM_DEC_04_VALUE_PENDING_CALIBRATION   (4 cells changed)
UNRESOLVED_REQUIRES_MODEL_PRIOR_ODDS             -> RESOLVED_BY_NUM_DEC_05           (not found as a literal token; no edit needed)
UNRESOLVED_REQUIRES_MARGINAL_LIKELIHOOD_METHOD   -> RESOLVED_BY_NUM_DEC_06           (not found as a literal token; no edit needed)
UNRESOLVED_REQUIRES_ROPE                         -> DEFERRED_BY_NUM_DEC_07           (not found as a literal token; no edit needed)
UNRESOLVED_REQUIRES_RESOURCE_CEILING             -> FRAMEWORK_RESOLVED_BY_NUM_DEC_08_VALUES_PENDING_MEASUREMENT (not found as a literal token; no edit needed)
```

One additional token was found and deliberately left unchanged, since it does not fall under the researcher's 8-item mapping: `GATE-031-V2-REPL-A.threshold_status = UNRESOLVED_REQUIRES_IMPLEMENTATION` — this gate concerns M3 exact-null representability in the parameter space, which is blocked on implementation-blocker #2 (§15 above), not on any pending NUM-DEC adjudication; it is correctly distinct from the tau-pending gates and was not altered. `MODEL_3B_MATHEMATICAL_SPECIFICATION_V2.md` §35 and `MODEL_3B_RECOVERY_PROTOCOL_V2.md` §21 (both newly added, additive, this turn) restate the full mapping and its rationale (a resolved procedure is not a resolved numerical value). `MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv` required no further edit — it already reflected the correct 7/1/0 distribution from the `NUM-DEC-08` turn.

## 17. Gate Formula Reconciliation

`MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`: 51 data rows, 20 columns, mechanically verified zero blank required fields both before and after the §16 edit. No bare `TBD`/`UNKNOWN`/`PENDING`-without-reference token found anywhere in the file (only `UNRESOLVED_REQUIRES_TAU` before the fix, and `UNRESOLVED_REQUIRES_IMPLEMENTATION` / `REQUIRES_PREIMPLEMENTATION_DECISION`, both of which are already decision-referenced in the sense required — they point to a specific named blocker, not a bare unexplained placeholder). No gate is marked executed (`implementation_status` values checked, none read `EXECUTED` or equivalent).

## 18. Original-to-V2 Gate Reconciliation

`MODEL_3B_GATE_V1_TO_V2_RECONCILIATION.csv` re-verified mechanically: 70 unique original `gate_id` values in the original 70-row spec, all 70 present exactly once in the reconciliation's `original_gate_id` column, zero missing, zero extra. 51 V2 gates all traceable. `GATE-031` → `RETIRED_PROSPECTIVELY` (historically preserved, retired for M3 only). `GATE-019`/`GATE-020` → `RETAINED_UNCHANGED`, confirmed still `MANDATORY` for M2 in the V2 spec. `GATE-036` → `NOT_APPLICABLE_TO_MODEL_DOMAIN`, confirmed still outside M0's model domain. No contradiction found; the reconciliation CSV was not modified by this audit.

## 19. Future Test Inventory

Mechanically recounted (regex over each adjudication document, not assumed):

```text
NUM-DEC-01: 0 tests    (confirmed: the document has no "Required Future Tests" section and no test-ID list at all — 21 sections total, ending at "21. Decision Summary")
NUM-DEC-02: 20 tests   (M2-UNC-001..020, table format, contiguous, unique)
NUM-DEC-03: 30 tests   (M2-NULL-001..030, contiguous, unique -- matches known-good completeness-corrected count)
NUM-DEC-04: 38 tests   (M3-TAU-001..038, contiguous, unique)
NUM-DEC-05: 20 tests   (M3-ODDS-001..020, contiguous, unique)
NUM-DEC-06: 40 tests   (M3-ML-001..040, contiguous, unique)
NUM-DEC-07: 16 tests   (M3-ROPE-001..016, contiguous, unique)
NUM-DEC-08: 30 tests   (M3B-RES-001..030, contiguous, unique)

Numerical-decision test count:  0+20+30+38+20+40+16+30 = 194
Existing amendment test count:  121  (MODEL_3B_AMENDMENT_TEST_INVENTORY.csv, re-verified 121 unique rows)
Combined future-test count:     194 + 121 = 315
Cross-family duplicate-test count: 0  (no test ID from any of the 8 numerical-decision families collides with any amendment-test ID)
```

`MODEL_3B_NUMERICAL_TEST_INVENTORY.csv` created with all 194 numerical-decision tests (10 columns: `test_id, source_decision, candidate, test_family, purpose, implementation_dependency, execution_dependency, historical_data_prohibited, status, notes`), every row `status=PLANNED_ONLY` — no test marked `PASS` merely because its governing decision was adjudicated.

## 20. Unresolved Measurements

Explicitly still open after this integration (none resolved by this audit, none should be):

```text
- M3 exact-null critical value c_0.05 (NUM-DEC-03)                      -- requires implementation + calibration run
- M3 posterior-probability threshold tau, final numeric value (NUM-DEC-04) -- requires calibration-set execution + separate researcher decision
- ROPE epsilon_n (NUM-DEC-07)                                            -- deferred, requires one of 5 reopening bases
- All 8 NUM-DEC-08 resource-ceiling numbers                              -- requires authorized profiling benchmark (not this turn, not the pilot logs alone)
- 8 confirmed M3 implementation blockers (SS15)                          -- requires future implementation work
```

## 21. Implementation Nonauthorization

```text
IMPLEMENTATION_AUTHORIZED: NO
```
No `.py` file was created or modified by this audit. No estimator was created.

## 22. Tournament Nonauthorization

```text
TOURNAMENT_EXECUTION_AUTHORIZED: NO
```
No calibration set, bootstrap, bridge sampling, thermodynamic integration, or tournament run occurred.

## 23. Historical-Fit Nonauthorization

```text
HISTORICAL_FIT_AUTHORIZED: NO
```
No historical data file was read, written, or referenced by this audit.

## 24. Production Isolation

No file under `backend/`, `frontend/`, or any Atlas/Graphify/production-configuration path was touched. All writes are confined to `docs/thesis/pilot_annotation/`. No Docker command, server action, or deployment step was executed.

## 25. Consistency Verdict

```text
NUMERICAL_DECISIONS_CONSISTENT_WITH_NONBLOCKING_CLARIFICATIONS
```

Rationale: all 8 decisions coexist mathematically without contradiction; the dependency graph is explicit and acyclic; formulas are coherent across every document that restates them; placeholders are now decision-linked (4 cells standardized, rest already compliant); implementation blockers remain fully visible and none is marked resolved. The "nonblocking clarifications" qualifier reflects two disclosed, non-contradictory findings that a future reader should be aware of but that do not block freezing this milestone: (a) `GATE-031-V2-REPL-A`'s placeholder is deliberately left outside the 8-token mapping since it tracks an implementation blocker rather than a NUM-DEC value (§16); (b) NUM-DEC-01 contributes zero mechanical future-tests, which is a structural asymmetry versus NUM-DEC-02–08, not a defect (§19). This verdict means only that the decisions are internally consistent as design documents — it is explicitly **not** `READY_FOR_IMPLEMENTATION`.

## 26. Final Status

```text
MODEL_3B_V2_NUMERICAL_DECISIONS_INTEGRATED_AND_READY_FOR_FREEZE
```
