# Model 3B V2 — Gate Status Explanation & Numerical Decision Digest

Status: PRE-FREEZE WORKING DOCUMENT. No researcher decision is recorded here.
No numerical value is selected here. Nothing in this document authorizes
implementation, tournament execution, or historical-data fitting.

Companion file: `MODEL_3B_GATE_V1_TO_V2_RECONCILIATION.csv` (Phase 1, produced
alongside this document).

---

## Phase 2 — Complete `mandatory_advisory_status` Distribution (V2 Gate Spec, 51 rows)

Mechanically recomputed via `csv.DictReader` against
`MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv` (verification snippet run twice,
independently, with identical results):

| Value (verbatim, incl. free text) | Count |
|---|---|
| `MANDATORY` | 24 |
| `ADVISORY` | 17 |
| `N/A` | 7 |
| `MANDATORY (historical; retired for future amended M3 only)` | 1 |
| `MANDATORY (historical benchmark; not eligible for inferential authorization)` | 1 |
| `MIXED (see original: GATE-044 MANDATORY; others ADVISORY)` | 1 |
| **Total** | **51** |

No blank values. No duplicate `gate_id` values (51 unique IDs for 51 rows).

### Correcting the premise in the researcher's message

The researcher's message assumed `MANDATORY = 17`, `ADVISORY = 17`, with 17
rows unexplained. The mechanical count does not match that assumption:
`MANDATORY = 24`, `ADVISORY = 17` (unchanged from the prior consistency-audit
correction of 19→17), leaving **10** rows outside the two clean enum values,
not 17. Those 10 are fully accounted for below — none are unexplained.

### Explaining the 10 non-`MANDATORY`/non-`ADVISORY` rows

1. **`N/A` — 7 rows.** `GATE-002-V2, GATE-003-V2, GATE-005-V2, GATE-006-V2,
   GATE-036-V2` (M0 excitation-domain gates, undefined on M0's parameter
   space per the Mathematical Domain Applicability Rule) plus
   `GATE-022-V2-THROUGH-028-V2` and `GATE-064-V2-THROUGH-070-V2` (M4,
   candidate excluded entirely: `EXCLUDED_INSUFFICIENT_PRECISE_SUBSET`). This
   is by design, not a defect — these gates are outside the parameter space
   of the candidate they're nominally attached to (`A(g,m)=0`).

2. **`MANDATORY (historical; retired for future amended M3 only)` — 1 row.**
   `GATE-031-V2-RETIRED`. This is GATE-031's own disposition: it remains
   `MANDATORY` in the historical pilot record (its original tier is
   preserved, not erased) while being prospectively retired for the future
   amended M3 only (Proposal 7). This is a deliberate dual-state
   representation, not a clean enum value, because the row simultaneously
   describes two time-scoped facts (historical tier + future retirement).

3. **`MANDATORY (historical benchmark; not eligible for inferential
   authorization)` — 1 row.** `GATE-008-V2-THROUGH-014-V2` (M1). M1 is a
   frozen benchmark candidate, out of scope for Proposals 1–7. The text
   preserves that GATE-008–014 were originally `MANDATORY` while flagging
   that M1 results are not eligible for the same inferential authorization
   pathway as M0/M2/M3 (M1 was never a deployment candidate).

4. **`MIXED (see original: GATE-044 MANDATORY; others ADVISORY)` — 1 row.**
   `GATE-043-V2-THROUGH-049-V2` (M1). This single V2 row condenses 7 original
   gates (GATE-043 through GATE-049) of which only GATE-044
   (`convergence_rate`) was `MANDATORY`; the remaining six were `ADVISORY`.
   The merged row cannot honestly carry one uniform tier, so it says so
   explicitly rather than picking one value and losing information.

### Structural finding on this sub-representation (reported, not auto-corrected)

Rows 2–4 above use free-text values inside `mandatory_advisory_status`
rather than a closed enum. This is defensible as a compression choice (M1
and GATE-031 are condensed/dual-state cases that a two-value enum cannot
represent without an added column), but it does mean the column is not
strictly machine-parseable as a controlled vocabulary in its current form.
**This is flagged as a structural improvement candidate for a future
revision of the V2 gate-spec schema** (e.g., splitting into
`mandatory_advisory_status_current` + `mandatory_advisory_status_scope_note`
columns) — **not acted on here**, since Phase 6 constraints prohibit
modifying the five existing V2 outputs absent an actual factual
contradiction, and this is a representational-clarity observation, not a
contradiction.

---

## Phase 3 — Digest of NUM-DEC-01 through NUM-DEC-08

No decision is recorded. This is preparation material only, drawn from
`MODEL_3B_V2_NUMERICAL_DECISION_LEDGER.csv`.

### NUM-DEC-01 — M2 replication denominator
- **Mathematical question:** what does "1,000 replications per cell" mean as
  a denominator — attempted replications, or only replications valid for
  metric calculation (i.e., excluding failed optimizations)?
- **Model affected:** M2.
- **Options:** `ATTEMPTED_REPLICATIONS_PER_CELL`;
  `VALID_FOR_METRIC_CALCULATION_REPLICATIONS_PER_CELL`;
  `BOTH_REPORTED_SEPARATELY_NO_SINGLE_DENOMINATOR_ADOPTED`.
- **Formula affected:** every M2 gate's per-cell rate/bias metric (denominator
  term of `invalid_estimate_rate`, `false_positive_excitation_rate`,
  bias/CI-coverage metrics).
- **Evidence available:** Proposal 3 SS8/SS9 — denominator ambiguity flagged;
  failed optimizations must never be silently substituted regardless of
  which option is chosen.
- **Evidence missing:** the tournament execution protocol's own original
  wording has not been re-read specifically for disambiguating context.
- **Consequence per option:** `ATTEMPTED` is conservative (penalizes
  non-convergence into every rate); `VALID_FOR_METRIC_CALCULATION` isolates
  estimator behavior conditional on convergence but can mask a high
  non-convergence problem if reported alone; `BOTH_REPORTED_SEPARATELY`
  avoids the choice but requires every downstream gate to carry two numbers.
- **Risk of deciding too early:** picking a denominator before re-reading the
  original protocol wording risks silently overriding a decision the
  protocol may have already made, reopening a settled document without
  cause.
- **Blocking status:** `implementation_blocking = YES`,
  `execution_blocking = YES`, `historical_fit_blocking = NO`.
- **Recommendation:** none offered — re-read
  `MODEL_3B_RECOVERY_TOURNAMENT_EXECUTION_PROTOCOL.md` first; if silent, this
  is a fresh preregistration decision, not a re-derivation.
- **Literature review required:** no.
- **Synthetic calibration required:** no (documentation re-read, not a
  simulation question).

### NUM-DEC-02 — M2 uncertainty method for n
- **Mathematical question:** what standard-error/CI construction should be
  used for `n = alpha/beta` under the stationarity-safe reparameterization?
- **Model affected:** M2.
- **Options:** `PROFILE_LIKELIHOOD_FOR_N`; `PARAMETRIC_BOOTSTRAP`;
  `LIKELIHOOD_BASED_INTERVAL_UNDER_N_BETA_PARAMETERIZATION`;
  `BAYESIAN_POSTERIOR_INTERVAL_IF_M2_BECOMES_BAYESIAN`.
- **Formula affected:** `GATE-021-V2` (`ci_coverage_95pct` for M2), directly.
- **Evidence available:** Proposal 2 SS15 flags the method as unresolved
  alongside the estimand switch to `n=alpha/beta`.
- **Evidence missing:** no small-scale coverage comparison across candidate
  methods on the `(n, beta)` reparameterization has been run yet.
- **Consequence per option:** profile likelihood and the likelihood-based
  interval are computationally cheaper but may mis-cover near the `n→0`
  boundary; bootstrap is more robust to non-normality but expensive at full
  scale; the Bayesian option only applies if M2 itself is reformulated as
  Bayesian, which is out of current scope.
- **Risk of deciding too early:** an uncalibrated method choice could
  silently reproduce the diagonal-Hessian-style coverage failure already
  found and corrected for M0 (Proposal 1) — coverage near a parameter
  boundary is exactly where naive interval methods misbehave.
- **Blocking status:** `implementation_blocking = YES`,
  `execution_blocking = YES`, `historical_fit_blocking = NO`.
  `GATE-021-V2` cannot be computed until this is resolved.
- **Recommendation:** none offered — coverage behavior differs by method
  near a boundary and must be checked, not assumed.
- **Literature review required:** implicit (interval-construction methods
  for ratio parameters near a boundary) — not explicitly requested in the
  ledger, but relevant.
- **Synthetic calibration required:** yes — small-scale coverage comparison
  before committing at full scale.

### NUM-DEC-03 — M2 exact-null implementation
- **Mathematical question:** how should `H0: n=0` be represented inside M2's
  interval-censored MBPP likelihood estimator specifically (not inherited
  automatically from M3's solution)?
- **Model affected:** M2.
- **Options:** `ADAPT_M3_NULL_A_STYLE_TWO_MODEL_COMPARISON`;
  `ADAPT_M3_NULL_B_STYLE_HURDLE_INDICATOR`;
  `M2_SPECIFIC_BOUNDARY_REPARAMETERIZATION_NOT_YET_DESIGNED`;
  `OTHER_M2_SPECIFIC_DESIGN`.
- **Formula affected:** `GATE-016-V2` (`false_positive_excitation_rate` for
  M2), directly; conceptually parallels the M3 exact-null defect (Proposal
  4) but is explicitly a **separate dependency**, not an automatic
  inheritance.
- **Evidence available:** Proposal 2 SS13 and Proposal 4 SS17 both flag this
  as `SEPARATE_DEPENDENCY`.
- **Evidence missing:** no review of `m2_mbpp.py`'s actual closed-form
  likelihood at `n=0` has been performed (the M3 exact-null defect was
  diagnosed from M3's `logit_n` parameterization, which is architecturally
  different from M2's).
- **Consequence per option:** adapting M3's two-model comparison or hurdle
  design gives consistency across candidates but may not fit M2's
  closed-form intensity structure; a from-scratch M2-specific boundary
  reparameterization is more work but more faithful to M2's actual
  likelihood.
- **Risk of deciding too early:** assuming the M3 solution transfers without
  checking M2's own likelihood form at `n=0` could reproduce a
  representability defect analogous to the one just found and fixed for M3.
- **Blocking status:** `implementation_blocking = YES`,
  `execution_blocking = YES`, `historical_fit_blocking = NO`.
  `GATE-016-V2` cannot be meaningfully computed until this is resolved.
- **Recommendation:** none offered — requires a dedicated M2-specific
  exact-null review examining `m2_mbpp.py`'s actual likelihood form at
  `n=0`, structurally analogous to Proposal 4 but not assumed to reach the
  same answer.
- **Literature review required:** not explicitly stated; implicitly
  relevant (interval-censored Hawkes null-boundary literature, per Rizoiu et
  al. 2022 already cited for M2's core method).
- **Synthetic calibration required:** not stated as a precondition, but
  likely needed once a design is chosen, symmetric to NUM-DEC-04's grid
  calibration.

### NUM-DEC-04 — M3 threshold tau
- **Mathematical question:** what decision threshold on `P(M1|Y)` declares
  excitation present?
- **Model affected:** M3.
- **Options:** `TAU_0_50`; `TAU_0_75`; `TAU_0_90`; `TAU_0_95`; `TAU_0_975`;
  `TAU_0_99`; `OTHER_VALUE_FROM_PROSPECTIVE_CALIBRATION_GRID`.
- **Formula affected:** `GATE-030-V2` (`FPR_hat(tau)`), `GATE-031-V2-REPL-B`
  (`posterior_probability_calibration`), `GATE-031-V2-REPL-C`
  (`FPR_hat(tau)`), `GATE-031-V2-REPL-D` (`FNR_hat(tau)`) — four gates
  directly blocked.
- **Evidence available:** Proposal 5 SS9 specifies a five-step prospective
  calibration procedure; explicitly rejects a universal `tau=0.95`
  assumption and forbids choosing tau by eliminating detection power.
- **Evidence missing:** the calibration grid has not been run (no synthetic
  calibration-seed evaluation of `FPR`/`FNR`/power across the mandatory
  null-scenario set yet).
- **Consequence per option:** a low tau (0.50–0.75) raises detection power
  but risks unacceptable FPR; a high tau (0.95–0.99) controls FPR but may
  push FNR/power outside acceptable bounds — the correct value is an
  empirical joint-optimization outcome, not a default.
- **Risk of deciding too early — dependency note (per Phase 4):**
  `P(M1|Y)/P(M0|Y) = BF_10(Y) · P(M1)/P(M0)`. Tau operates on `P(M1|Y)`,
  which is itself a function of the prior odds `P(M1)/P(M0)` (NUM-DEC-05)
  and the Bayes-factor/marginal-likelihood computation method (NUM-DEC-06).
  Calibrating tau before those two are fixed means recalibrating tau again
  the moment either changes — the calibration would not be reusable.
- **Blocking status:** `implementation_blocking = YES`,
  `execution_blocking = YES`, `historical_fit_blocking = NO`.
- **Recommendation:** none offered — must come from the Proposal 5 SS9
  five-step prospective calibration procedure, run only after NUM-DEC-05 and
  NUM-DEC-06 are fixed.
- **Literature review required:** not explicitly stated as a precondition
  (this is a simulation-design decision, not a literature-derived
  threshold).
- **Synthetic calibration required:** yes — mandatory, on a separate
  calibration-seed set, jointly evaluating FPR/FNR/power.

### NUM-DEC-05 — M3 prior model odds
- **Mathematical question:** what are `P(M0)` and `P(M1)`, the prior
  probabilities of the null vs. excitation model?
- **Model affected:** M3.
- **Options:** `EQUAL_ODDS_0_5_0_5_AS_ONE_CANDIDATE_ONLY`;
  `RESEARCHER_SPECIFIED_INFORMATIVE_ODDS`;
  `SENSITIVITY_ANALYSIS_ACROSS_A_GRID_NO_SINGLE_VALUE_ADOPTED`.
- **Formula affected:** the posterior odds equation directly
  (`P(M1|Y)/P(M0|Y) = BF_10(Y)·P(M1)/P(M0)`), and transitively every gate
  that depends on `P(M1|Y)` (see NUM-DEC-04's blocked-gate list).
- **Evidence available:** Proposal 5 SS14 — equal odds (0.5/0.5) may be
  *evaluated* as one candidate but is explicitly **not adopted** by any
  adjudicated document; no default has been assumed anywhere in the frozen
  record.
- **Evidence missing:** a prior-sensitivity analysis showing how the
  posterior model probability and downstream FPR/FNR shift across a grid of
  candidate prior odds has not been produced.
- **Consequence per option:** equal odds is the least assumption-laden
  choice but is still a substantive commitment (it says the researcher has
  no prior belief that excitation is more or less likely than not, which is
  itself a claim); informative odds require an explicit, defensible
  justification; a sensitivity analysis avoids commitment at the cost of not
  producing a single operational number for tau calibration.
- **Risk of deciding too early:** prior odds interact multiplicatively with
  the Bayes factor — an unexamined prior can dominate or be dominated by the
  likelihood evidence in ways that are opaque unless the sensitivity has
  been mapped first.
- **Blocking status:** `implementation_blocking = YES`,
  `execution_blocking = YES`, `historical_fit_blocking = NO`.
- **Recommendation:** none offered — ledger explicitly withholds a default,
  including equal odds.
- **Literature review required:** not stated; plausibly relevant background
  (Bayesian model-selection prior-elicitation practice) but not flagged as
  required in the frozen record.
- **Synthetic calibration required:** yes — prior-sensitivity analysis
  across a grid, before any single value is adopted.

### NUM-DEC-06 — M3 marginal-likelihood / Bayes-factor method
- **Mathematical question:** what estimator computes `p(Y|M0)`, `p(Y|M1)`,
  and (if used as a secondary diagnostic) `BF_10`?
- **Model affected:** M3.
- **Options:** `BRIDGE_SAMPLING`; `IMPORTANCE_SAMPLING`;
  `SAVAGE_DICKEY_DENSITY_RATIO_WHERE_APPLICABLE`; `REVERSIBLE_JUMP_MCMC`;
  `NO_BAYES_FACTOR_POSTERIOR_PROBABILITY_ONLY`.
- **Formula affected:** the marginal-likelihood terms feeding `BF_10(Y)` in
  the posterior-odds equation; also required for `P(M1|Y)` itself if a
  direct posterior-probability route (rather than a BF-based route) is used.
- **Evidence available:** Proposal 5 SS15 — Bayes factor is explicitly a
  **secondary diagnostic only**, never the sole primary decision rule; no
  universal `BF>3`/`>10`/`>100` interpretive category is assumed without
  calibration.
- **Evidence missing:** no numerical-stability or prior-sensitivity
  comparison of candidate estimators on synthetic exact-null vs.
  positive-excitation data has been run.
- **Consequence per option:** bridge/importance sampling and RJMCMC are
  general but can be numerically unstable near the null boundary (exactly
  where this model needs precision, per NUM-DEC-03/04's boundary concerns);
  Savage-Dickey is efficient but only applicable under nested-model
  conditions that must be verified for M3's structure;
  `NO_BAYES_FACTOR_POSTERIOR_PROBABILITY_ONLY` sidesteps marginal-likelihood
  estimation entirely by computing `P(M1|Y)` directly, if that route is
  numerically preferable.
- **Risk of deciding too early:** an unstable estimator near `n_d=0` could
  reintroduce a version of the exact-null representability problem at the
  computational level even after the mathematical definition (NUM-DEC-03/
  Proposal 4) is fixed.
- **Blocking status:** `implementation_blocking = YES`,
  `execution_blocking = NO`, `historical_fit_blocking = NO`. Not
  execution-blocking on its own since `P(M1|Y)` (NUM-DEC-04's target) is the
  primary decision quantity — but it does block any Bayes-factor-based
  reporting, and by the posterior-odds identity it is a precondition for a
  reusable NUM-DEC-04 calibration.
- **Recommendation:** none offered.
- **Literature review required:** not explicitly stated; implicit
  (marginal-likelihood estimator stability literature).
- **Synthetic calibration required:** yes — numerical-stability and
  prior-sensitivity comparison on synthetic exact-null and
  positive-excitation data before adoption.

### NUM-DEC-07 — M3 ROPE epsilon_n
- **Mathematical question:** what half-width `epsilon_n` (if any) defines a
  region of practical equivalence for magnitude interpretation of `n_d`?
- **Model affected:** M3.
- **Options:** `NO_ROPE_RETAINED`; `LITERATURE_DERIVED_EPSILON_N`;
  `SIMULATION_DESIGN_REQUIREMENT_EPSILON_N`; `COMPARATIVE_BENCHMARK_EPSILON_N`;
  `EXPLICIT_RESEARCHER_POLICY_EPSILON_N`.
- **Formula affected:** none of the mandatory gates directly; ROPE is
  explicitly supplementary magnitude interpretation, not a replacement for
  the exact-null-vs-excitation model comparison.
- **Evidence available:** Proposal 4 SS10 / Proposal 5 SS16 — ROPE role is
  scoped as supplementary only.
- **Evidence missing:** no threshold-provenance justification (from any of
  the six provenance classes) has been produced for any candidate
  `epsilon_n` value.
- **Consequence per option:** `NO_ROPE_RETAINED` avoids the question
  entirely; each provenance-class option carries the same
  literature/simulation/benchmark/policy justification burden as any other
  gate threshold in this framework — none may be derived from the
  historical fit.
- **Risk of deciding too early:** an ungrounded `epsilon_n` could quietly
  reintroduce a historical-fit-derived threshold in violation of the
  no-fitting-until-authorized rule, since ROPE width is intuitively easy to
  "eyeball" from prior results.
- **Blocking status:** `implementation_blocking = NO`,
  `execution_blocking = NO`, `historical_fit_blocking = NO`. Not blocking on
  its own since ROPE is optional — but if adopted, must not be silently
  derived from historical data.
- **Recommendation:** none offered — no evidence currently supports any
  single option, including `NO_ROPE_RETAINED`.
- **Literature review required:** yes, if `LITERATURE_DERIVED_EPSILON_N` is
  the eventual choice (conditional on that branch).
- **Synthetic calibration required:** yes, if
  `SIMULATION_DESIGN_REQUIREMENT_EPSILON_N` is the eventual choice
  (conditional on that branch).

### NUM-DEC-08 — operational resource ceiling
- **Mathematical question:** what is the maximum CPU time / wall-clock time /
  memory / storage budget for a full future execution across all candidates
  and cells?
- **Model affected:** M0, M2, M3 (jointly).
- **Options:**
  `ESTIMATE_FROM_OBSERVED_PILOT_TIMING_THEN_SET_CEILING` (M2 pilot observed
  ~5.8–18.6 s/replicate); `RESEARCHER_SPECIFIED_HARD_CEILING_INDEPENDENT_OF_PILOT_TIMING`.
- **Formula affected:** none of the mathematical gates directly — this is an
  operational/resourcing decision, not a statistical one — but it gates
  whether NUM-DEC-01's full-scale replication count (and by extension every
  gate depending on that scale, per Proposal 3) is executable at all.
- **Evidence available:** Proposal 3 SS13 — replication count must not be
  lowered solely because execution is expensive; infeasibility must return
  to researcher review rather than being silently downgraded.
- **Evidence missing:** the actual resource estimate — `(observed
  s/replicate) × (planned replications/cell) × (number of cells)` per
  candidate — has not yet been computed and reported.
- **Consequence per option:** estimating from observed pilot timing gives a
  data-grounded ceiling but risks anchoring too tightly to pilot-scale
  behavior (150/cell) rather than full-scale (1,000/cell) behavior, which
  may not scale linearly (e.g., convergence retries, memory growth);
  a hard ceiling independent of pilot timing is simpler but risks being set
  either impractically low or arbitrarily high without empirical grounding.
- **Risk of deciding too early:** setting a ceiling before the
  observed-timing × planned-scale arithmetic is actually computed risks
  either blocking a feasible run or silently authorizing a run whose true
  cost was never checked.
- **Blocking status:** `implementation_blocking = NO`,
  `execution_blocking = YES`, `historical_fit_blocking = NO`.
- **Recommendation:** none offered — ledger specifies the exact arithmetic
  to compute and report to the researcher before any execution commitment;
  no ceiling value is proposed here.
- **Literature review required:** no.
- **Synthetic calibration required:** no (arithmetic on already-observed
  pilot timing, not a new simulation).

---

## Phase 4 — Decision Order

Dependency order used, exactly as specified by the researcher (no silent
reordering):

1. NUM-DEC-01 — M2 replication denominator
2. NUM-DEC-02 — M2 uncertainty method for n
3. NUM-DEC-03 — M2 exact-null implementation
4. NUM-DEC-05 — M3 prior model odds
5. NUM-DEC-06 — M3 marginal-likelihood/Bayes-factor method
6. NUM-DEC-04 — M3 threshold tau
7. NUM-DEC-07 — M3 ROPE epsilon_n
8. NUM-DEC-08 — operational resource ceiling

**Dependency justification for placing NUM-DEC-04 after NUM-DEC-05/06** (per
researcher's explicit instruction, verified against the ledger's own
`notes` field for NUM-DEC-04, NUM-DEC-05, and NUM-DEC-06 — all three
independently reference this relationship):

```
P(M1 | Y) / P(M0 | Y)  =  BF_10(Y) · P(M1) / P(M0)
```

Tau is a threshold applied to `P(M1|Y)` (equivalently, to the posterior odds
above some transform). The right-hand side shows `P(M1|Y)` is a product of
the Bayes factor `BF_10(Y)` (NUM-DEC-06's estimator choice) and the prior
odds `P(M1)/P(M0)` (NUM-DEC-05's choice). A tau calibrated against one
prior-odds/BF-method combination is not transferable to a different
combination — recalibration would be required every time either upstream
choice changed. Fixing NUM-DEC-05 and NUM-DEC-06 first makes the NUM-DEC-04
calibration run (Proposal 5 SS9) a one-time cost rather than a repeated one.

No change to this order is proposed. M2-block decisions (01–03) precede the
M3-block decisions (05, 06, 04, 07) because M2 and M3 are independent
candidates with no cross-candidate mathematical dependency in the ledger;
the M2 block is simply listed first by the researcher's own ordering and
nothing in the evidence contradicts that sequencing. NUM-DEC-08 (resource
ceiling) is last because it is computed *from* the scale implied by
NUM-DEC-01 and cannot be meaningfully estimated before that denominator
question is settled.

---

## Phase 5 — Formula Completeness Check

Checked columns per V2 gate-spec row (51 rows × 10 required fields = 510
cells): `model_equation_id`, `parameter_space`, `estimand`,
`null_definition`, `applicability`, `metric_formula`, `denominator`,
`threshold_status`, `threshold_provenance`, `failure_meaning`.

| Column | Blank count |
|---|---|
| model_equation_id | 0 |
| parameter_space | 0 |
| estimand | 0 |
| null_definition | 0 |
| applicability | 0 |
| metric_formula | 0 |
| denominator | 0 |
| threshold_status | 0 |
| threshold_provenance | 0 |
| failure_meaning | 0 |

**Result: 0 blank required fields, out of 510 checked cells.** Matches the
expected target exactly.

### Finding: pending-decision placeholders do not use the literal `PENDING_NUM_DEC_0X` token format

The instruction anticipated pending fields would carry a literal placeholder
like `PENDING_NUM_DEC_04`. In practice, `MODEL_3B_RECOVERY_GATE_SPECIFICATION_V2.csv`
represents pending-numerical-decision status through the `threshold_status`
column using descriptive enum values instead:

| gate_id | threshold_status | Numerical decision it depends on |
|---|---|---|
| GATE-016-V2 | `FROZEN_UNCHANGED_METHOD_UNRESOLVED` | NUM-DEC-03 |
| GATE-021-V2 | `FROZEN_BAND_METHOD_UNRESOLVED` | NUM-DEC-02 |
| GATE-030-V2 | `UNRESOLVED_REQUIRES_TAU` | NUM-DEC-04 (transitively 05, 06) |
| GATE-031-V2-REPL-A | `UNRESOLVED_REQUIRES_IMPLEMENTATION` | NUM-DEC-03 |
| GATE-031-V2-REPL-B | `UNRESOLVED_REQUIRES_TAU` | NUM-DEC-05, 06 |
| GATE-031-V2-REPL-C | `UNRESOLVED_REQUIRES_TAU` | NUM-DEC-04 |
| GATE-031-V2-REPL-D | `UNRESOLVED_REQUIRES_TAU` | NUM-DEC-04 |

This is **not a blank-field defect** — every cell is populated, and the
semantic content correctly identifies which gates are numerically
unresolved and why. It is a **format deviation** from the instruction's
suggested literal-token convention: the spec identifies the *kind* of
pending dependency (method / tau / implementation) rather than citing the
specific `NUM-DEC-0X` ID inline. Reported here as a minor structural
observation for a possible future schema revision (e.g., adding a
`blocking_decision_id` column). **Not treated as a contradiction — no
auto-correction applied, five V2 files left untouched.**

---

## Summary

- Phase 1 reconciliation: all 70 original gates accounted for exactly once;
  all 51 V2 gates traced to a source (46 via direct/merged provenance, 5 via
  explicit `NEW_REPLACEMENT_GATE` marking sourced from GATE-031's
  retirement); disposition distribution RETAINED_UNCHANGED=28,
  NOT_APPLICABLE_TO_MODEL_DOMAIN=19, MERGED=14, REVISED_PROSPECTIVELY=5,
  DEFERRED_PENDING_NUMERICAL_DECISION=3, RETIRED_PROSPECTIVELY=1 (sums to
  70); plus 5 NEW_REPLACEMENT_GATE rows appended separately (75 total data
  rows in the CSV, 70 of them being the mandated original-gate accounting).
- Phase 2: full status distribution computed and explained; user's
  17/17/17 premise corrected to the mechanically verified 24/17/(7+1+1+1).
- Phase 3–4: all 8 numerical decisions digested with options, evidence,
  consequences, and blocking status; no value selected; dependency order
  preserved and justified via the posterior-odds identity.
- Phase 5: 0/510 required fields blank; one minor format-deviation finding
  reported (descriptive `threshold_status` enums used instead of literal
  `PENDING_NUM_DEC_0X` tokens) — not a contradiction, no file modified.
- No contradiction requiring a stop was found. The five existing V2 outputs
  were read but not modified.

**FINAL STATUS: MODEL_3B_V2_GATE_RECONCILIATION_AND_DECISION_DIGEST_READY**
