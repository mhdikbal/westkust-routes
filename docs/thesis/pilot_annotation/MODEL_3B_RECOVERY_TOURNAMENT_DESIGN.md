# Model 3B — Recovery Tournament Design

> **DESIGN ONLY. Not executed. No V2 implemented. No V1/Phase D rerun. No historical data fitted. No data file changed. Nothing staged, committed, pushed, or deployed.**
> **Builds directly on**: `MODEL_3B_ROOT_CAUSE_AND_LITERATURE_COMPATIBILITY_AUDIT.md` (root-cause classification `RECOVERY_OBSERVATION_REGIME_MISMATCH`, §5 initial candidate sketch — this document supersedes that sketch in structure and completeness per the researcher's more detailed specification, while reusing every substantive finding from it rather than re-deriving).
> **Authoritative root cause (not re-litigated here):** V1's recovery study validated a continuous-time, no-tie synthetic regime; the real 141-event corpus is year-only precision with extensive same-year ties requiring a fabricated deterministic jitter (`model3_hawkes_kaskade_event.py::jitter_ties`) to be fit at all. **Corrected conclusion**: the estimator failed a recovery test that does not represent the real data — not "Hawkes cannot be implemented." V1 remains `MODEL_VALIDATION_FAILURE` / `INFERENCE_NOT_AUTHORIZED`. The Hawkes family itself is `NOT_RULED_OUT`.

---

## 0. Do-Not List (binding for this document and any future execution turn)

```text
Do NOT rerun the old (V1) recovery study.
Do NOT tune V1's existing parameterization until it passes.
Do NOT change any historical timestamp or the linimasa_events source data.
Do NOT select a new excitation kernel before the observation-regime fix is validated.
Do NOT fit any candidate (M0-M4) to the real 141-event corpus.
Do NOT deploy any model.
```

---

## 1. Candidates

Exactly five slots, four mandatory, one conditional.

### M0 — Exposure-adjusted count baseline (Poisson / Negative Binomial)

Non-Hawkes floor. Period-binned (annual, matching real data's actual grain exactly) count model, `log(1+CD_t)` density covariate optional as an exposure or rate term (tested both ways — see §4, CD-1 vs CD-2). No self-excitation term. Purpose: if a model with **no clustering mechanism at all** matches or beats the Hawkes candidates on real-data-realistic synthetic scenarios, that is independent evidence the excitation term is not earning its parameter cost — directly probing audit root causes #7 (complexity vs. effective n) and #10/#12 (is any excitation justified at this resolution/sample size at all).

### M1 — Current V1, non-authoritative benchmark

**Not a candidate for adoption.** V1's existing `model3b_cd_simulator` (M1/M2/M3B-CD as already implemented) is carried into this tournament unchanged, run through the *same* corrected observation-regime pipeline (§ below, in `MODEL_3B_OBSERVATION_REGIME_SIMULATION_SPEC.md`) that M2/M3/M4 will use, purely as a reference point. Its purpose is diagnostic, not competitive: if V1's own specification recovers acceptably once the synthetic generator is corrected to match the real censoring/tie regime, that is strong evidence the root cause was **entirely** observation-regime mismatch (audit #4/#11), not the Hawkes family or V1's specific parameterization. If V1 still fails to recover even under a corrected regime, that shifts weight toward #2 (parameterization), #10 (non-identifiability), or #12 (family incompatibility) as additional, non-eliminated causes. M1 is explicitly excluded from "eligible to touch real data" status regardless of its recovery outcome — it remains the benchmark artifact of a model already classified `MODEL_VALIDATION_FAILURE`; a passing recovery result for M1 under the corrected pipeline would justify a *new*, separately-numbered model version, not reinstatement of V1 itself.

### M2 — MBPP interval-censored Hawkes (Rizoiu et al. 2022, JMLR)

Reuses this project's own partial implementation (`docs/thesis/colab/model3_mbpp_full.py`, `model3_mbpp_eval.py`; Eq. 9/10/18 of Rizoiu et al.). Treats each calendar year as a censoring interval over a continuous latent intensity — the literature-native answer to the confirmed temporal-resolution mismatch, as opposed to either fabricating sub-year points (V1's actual mistake) or discarding all sub-year information via coarse binning (M0/M3's approach). Directly targets root causes #3, #4, #11, and provides a cleaner identifiability test of #10 than V1 could, since MBPP's censoring is correctly specified rather than confounded by a fabricated variable.

### M3 — Bayesian discrete-time Hawkes (period-binned, prior-informed)

A discrete self-exciting count process (e.g. INGARCH-family or discrete Hawkes) on annual bins, fit with weakly informative priors on excitation/branching-ratio parameters — chosen specifically because V1's Wald/MLE approach demonstrably miscalibrates at this n (postmortem: CI coverage 60-84% vs. 92.5-97.5% target for alpha/beta). No sub-year timestamp is ever required, so root causes #3/#4/#11 cannot recur by construction. Addresses #7 directly via informative priors rather than asymptotic intervals.

### M4 — Continuous-time Hawkes on a verified exact-date subset (CONDITIONALLY_ELIGIBLE)

**Status: `CONDITIONALLY_ELIGIBLE`.** M4 is not "included" outright — it is eligible only after Guard A (§1a below) is satisfied. Any prior wording in this project's Model 3B documents describing M4 as simply "included" is superseded by this status.

**Precision audit performed as part of this design turn** (read-only, against `data/research/linimasa_events.csv`'s `event_date_raw` field — no model-fitting code run, no data modified):

```text
n = 141 total events, first-pass regex classification of event_date_raw:
  single exact day precision ("17 Januari 1607" shape):        75  (53.2%)
  multi-day range / multiple-date entries ("10-12 Maret 1637",
    "6 & 9 November 1649", or explicit "lapor"/reported-date
    variants):                                                 18  (12.8%)
  month-only precision:                                        11  ( 7.8%)
  year-only precision:                                         10  ( 7.1%)
  unclassified by this first-pass regex (needs manual review,
    likely a mix of qualified/approximate phrasing not yet
    seen by this pattern set):                                 27  (19.1%)
```

**This is candidate identification only. It is NOT final exact-event-date classification.** The 75-event figure tells us how many events are *worth manually reviewing* for M4 eligibility — it is not itself the M4-eligible count, and must never be treated as such by any future implementation turn. See Guard A immediately below for the required manual classification step and its hard prohibitions.

If, after Guard A's dedicated manual audit, the genuinely-precise subset (`EXACT_EVENT_DATE` class only) falls below roughly 30-40 events, M4's own recovery test becomes underpowered by construction — which the recovery-tournament framework treats as **a finding about M4's eligibility, not a design flaw**: M4 would then be recorded as `EXCLUDED_INSUFFICIENT_PRECISE_SUBSET` rather than silently run underpowered.

**Root causes tested**: #4, #11 in isolation (does continuous-time Hawkes recover cleanly when its precision assumption is actually met?), and indirectly #10 by elimination.

---

### 1a. Guard A — Phase-0 Date Precision Guard (pre-execution, binding on M4)

```text
GUARD STATUS: ACTIVE. M4 remains CONDITIONALLY_ELIGIBLE until this guard
is satisfied by a completed, documented Phase-0 audit.
```

The regex first pass above (75/141 events, "apparent single exact day precision") is **candidate identification only** — it is not, and must never be represented as, final exact-event-date classification. It does not yet distinguish event-date from report-date, does not parse the 27 unclassified rows, and does not verify that "single exact day" entries are free of qualifying language (circa, approximately) that a stricter audit might reclassify.

**Before M4 implementation, every one of the 75 candidate events must be manually classified as exactly one of the following eight classes:**

```text
EXACT_EVENT_DATE            -- the date is the event's own occurrence date,
                                stated to single-day precision, with no
                                qualifying/approximate language.
EXACT_REPORT_DATE           -- the date is when the event was reported/
                                recorded, not when it occurred.
DOCUMENT_DATE                -- the date is the date of the source document
                                itself (e.g. a letter's dateline), not
                                necessarily the event's occurrence date.
ARRIVAL_OR_DEPARTURE_DATE   -- the date marks an arrival/departure distinct
                                from the substantive event being dated.
DATE_RANGE_BOUNDARY         -- the "single day" reading is one boundary of
                                what is actually a multi-day range.
MULTIPLE_DATES_AMBIGUOUS    -- more than one date is present and the source
                                does not unambiguously indicate which one is
                                the event date.
INFERRED_DATE                -- the day-level precision was inferred/
                                calculated rather than stated directly in
                                the source.
CANNOT_DETERMINE             -- the source review does not resolve the
                                classification.
```

**Only events classified `EXACT_EVENT_DATE` may enter M4's synthetic-generator design or any future M4 implementation.**

**Explicit prohibitions on this classification pass:**

```text
Do NOT alter the original date (event_date_raw or any other source field).
Do NOT replace uncertainty with a precise date.
Do NOT select the first date automatically when multiple dates are present.
Do NOT treat a document date as an event date.
Do NOT resolve multiple dates without source review (i.e. never guess).
```

This classification pass is manual source review, not automated pattern-matching — the regex first pass exists only to identify which 75 events are worth that manual review, nothing more. Completing Guard A is a separate, small, non-model-fitting, separately-authorizable task (Phase 0 in §6's sequencing), not performed by this design document.

---

## 2. Governing Simulation Pipeline

Full specification in `MODEL_3B_OBSERVATION_REGIME_SIMULATION_SPEC.md`. Every candidate's synthetic recovery test **must** pass its ground-truth-generated events through the full chain below — no stage may be skipped, and no candidate may be tested against a synthetic regime more favorable than what its own real-data application would face (this is the precise discipline V1's recovery study violated):

```text
latent event process
  -> source-observation process
  -> year-level interval censoring
  -> same-year ties
  -> parent-child episode structure
  -> missing and duplicate reporting
  -> candidate-specific preprocessing
  -> estimator
  -> recovery metrics
```

M0/M2/M3 apply the full chain at annual/interval-censored resolution (matching real data exactly). M4 applies the full chain but restricts the "source-observation process" and "year-level interval censoring" stages to the precise-subset regime (near-zero censoring width, by construction, for the events that qualify) — this is not a shortcut, it is the correct application of the same pipeline to a differently-precise data-generating scenario, and is exactly what makes M4 a valid test of root cause #4 in isolation.

---

## 3. Recovery-Factor Grid

Every factor below appears somewhere in the design; levels are illustrative starting points, not fixed as of this document (an implementer would refine within the ranges given, subject to compute budget):

| Factor | Levels tested | Rationale |
|---|---|---|
| Event count (n) | 50, 100, 141 (real n), 200 | 141 matches the real corpus exactly (primary); 50/100 stress-test the small-n regime the postmortem already flagged as marginal; 200 checks whether recovery improves materially with more data, informing whether n itself (vs. resolution) is the binding constraint |
| Effective episode count | 1 episode = all events; ~5 episodes (matching the real corpus's rough parent/child clustering, per Phase D's Sas-expedition finding); fully flat (no episodes, V1's implicit assumption) | Isolates root cause #6 — tests whether ignoring episode structure (the flat assumption) specifically degrades recovery relative to an episode-aware generator |
| Date precision | Year-only (real data's dominant regime, 7-19% by the count above depending on classification confidence); mixed (matching the actual 53/13/8/7/19 split found above); day-exact (M4's regime only) | Directly operationalizes the confirmed root cause; "mixed" is the single most externally-valid setting since it matches the real corpus's actual heterogeneity, not an idealized uniform regime |
| Tie rate | 0% (M4's precise subset); ~30-40% (estimated real year-only tie rate, to be confirmed by the precision audit); high-tie stress case (60%+) | Ties are the specific mechanism that forced V1's fabricated jitter; must be varied to confirm which candidates handle ties without fabrication |
| Source concentration | Low (one source per event); moderate; high (single-source-dominated, matching Phase B's 59.6% CD-dependency finding) | Probes root cause #5 interaction with recovery, even though source confounding's *resolution* is out of this tournament's scope (see §6) |
| CD dependence | CD-0 (excluded), CD-1 (intensity covariate), CD-2 (exposure covariate) | Full crossing required — see `MODEL_3B_VARIABLE_ROLE_DECISION_MATRIX.csv` |
| Parent-child rate | 0% (fully independent events); ~30% (rough estimate matching Sas-expedition-scale clustering); 50%+ (stress case) | Directly targets root cause #6 |
| Missing-event rate | 0%; 10%; 25% | Archival record loss is a real, undocumented risk not tested by V1 at all; 0% is the null/optimistic case already implicitly assumed by V1 |
| Duplicate-report rate | 0%; 5%; 15% | The corpus already shows explicit dual-reporting language ("lapor" entries) — a nonzero rate is empirically motivated, not speculative |
| Branching ratio (n = alpha/beta) | 0 (pure baseline, false-positive-excitation test); 0.3; 0.68 (V1's production point estimate); 0.9 (near-explosive stress case) | 0.68 anchors to V1's own fitted value; 0 and 0.9 bracket the range needed to test both false-positive and boundary-collapse behavior |
| Decay (beta) | Fixed/grid: {0.3, 0.62 (V1's production estimate), 1.2} per-year; jointly estimated (free parameter) | Directly implements the researcher's stationarity-safe parameterization requirement (§4) |
| Exogenous shocks | None; single shock (one exogenous burst mid-series); periodic (matching plausible institutional-cycle patterns, e.g. treaty-renewal years) | Tests whether candidates can distinguish self-excitation from exogenous covariate-driven bursts — relevant to disentangling CD-1 vs. genuine clustering |

Not a full factorial (12 factors at 3-4 levels each would be computationally intractable and scientifically unnecessary). A reduced design — e.g. a fractional factorial or one-factor-at-a-time sweep anchored at a realistic "baseline" setting (n=141, mixed precision, moderate ties, CD-1, ~30% parent-child, 10% missing, 5% duplicate, branching ratio 0.68, jointly estimated decay) with targeted stress cells varying one or two factors at a time (mirroring V1's own S1-S8 cell design, blueprint §8) — is the intended structure. Full cell enumeration is a separate, future implementation-planning step, not performed by this design document.

---

## 4. CD Variable Requirement

Full detail in `MODEL_3B_VARIABLE_ROLE_DECISION_MATRIX.csv`. Summary: CD-1 (V1's assumption — density as an *event-intensity* covariate, i.e. more documents → genuinely more events happening) is not assumed correct. CD-2 (density as an *observation/exposure* covariate — more documents → higher probability of *observing* events that occur at a constant underlying rate, a detection-probability reframing) is at least as plausible given Phase B's confound finding, and CD-0 (excluded entirely) is the null comparator. All three interpretations must be tested against at least the Hawkes-family candidates (M1-M4); M0 (baseline) tests CD-1 vs. CD-2 in their simplest, most interpretable form (a GLM offset for CD-2 vs. a GLM predictor for CD-1) and is therefore the cleanest place to *first* distinguish the two before carrying the distinction into the more complex Hawkes candidates.

---

## 5. Stationarity-Safe Parameterization Requirement (Hawkes candidates: M1, M2, M3, M4)

```text
n (branching ratio) = alpha / beta,   constrained  0 <= n < 1
alpha = n * beta   (n is the free/estimated parameter, not alpha directly)
```

Each Hawkes candidate must be evaluated under **both**:
1. **Fixed/grid decay**: beta swept over a small fixed grid (e.g. {0.3, 0.62, 1.2} per year, anchored at V1's production estimate), n estimated freely within [0, 1) at each grid point, best-fitting beta selected by likelihood/marginal-likelihood comparison.
2. **Jointly estimated decay**: beta itself a free parameter alongside n, fit simultaneously.

This directly targets the audit's identifiability finding (§1 row 10: alpha/beta trading off, low theta1-alpha correlation but severe branching-ratio undercoverage) — the n/beta reparameterization changes what is estimated without changing the model's mathematical content, and comparing fixed vs. jointly-estimated decay isolates whether decay-rate non-identifiability specifically (rather than the alpha/beta split generally) is the dominant driver of V1's boundary-collapse behavior.

---

## 6. Sequencing and Stopping Rule

```text
Phase 0 (prerequisite, small, non-model-fitting):
  Dedicated event_date_raw precision-parsing audit of all 141 events
  (confirms/refines the M4 eligibility count above). Separately
  authorizable on its own, cheap, does not require building any candidate.

Phase 1 (cheapest, run first, informs all subsequent phases):
  M0 (baseline count model) recovery test.
  Rationale: trivial compute cost; directly resolves whether ANY
  excitation mechanism is justified at all, informing how much
  weight to put on M2-M4 succeeding vs. M0 alone being sufficient.

Phase 2 (parallel, moderate cost):
  M1 (V1 benchmark, corrected pipeline) and M2 (MBPP) recovery tests,
  run in parallel -- no dependency between them. M1 diagnoses whether
  the corrected observation regime alone rescues V1's specification;
  M2 tests the literature-native resolution-matched alternative.

Phase 3 (conditional on Phase 0):
  M4 (precise-subset continuous Hawkes) recovery test, ONLY if Phase 0's
  dedicated audit confirms a sufficient precise-event subset (informal
  floor: >=30-40 genuinely single-exact-day, non-report-date-confused
  events). If insufficient, M4 is marked EXCLUDED_INSUFFICIENT_PRECISE_
  SUBSET and the tournament proceeds with M0/M1/M2/M3 only.

Phase 4 (most expensive, run last, only if warranted):
  M3 (Bayesian discrete-time) recovery test. Placed last because it is
  the highest-cost candidate (MCMC); if M0 alone already resolves the
  complexity-vs-sample-size question in M0's favor (i.e., no excitation
  term earns its cost at any tested setting), M3's Bayesian machinery
  may not be worth the compute investment, and that determination can
  only be made after Phase 1's results are in hand.

STOPPING CONDITION: the tournament stops when every phase above has
either run to completion or been explicitly marked excluded/deferred by
researcher decision. It does not stop early merely because one candidate
passes -- multiple candidates may legitimately pass (see gate below).
```

---

## 7. Go/No-Go Gate to Real Data (fully operational)

```text
GOVERNING RULE (restated from the audit, made fully operational here):
  Only a candidate that independently passes its own pre-registered
  recovery test, per the numeric thresholds in
  MODEL_3B_RECOVERY_GATE_SPECIFICATION.csv, may be fit against the 141
  real historical events.

WHAT "TOUCHING REAL DATA" MEANS AS A NEXT STEP:
  Fitting a passing candidate to the real corpus is a SEPARATE, further
  action requiring its own explicit researcher authorization -- passing
  a recovery test does not auto-authorize a real-data fit. This mirrors
  the discipline already applied throughout this session (decision !=
  implementation; e.g. DEC-19 was decided in one turn, implemented only
  after separate explicit authorization in a later turn).

IF ZERO CANDIDATES PASS:
  This is itself a valid, reportable scientific outcome -- it would mean
  root causes #10 (intrinsic non-identifiability) or #12 (Hawkes-family
  incompatibility) are confirmed at a stronger evidentiary level than
  this audit currently supports, and M0's baseline-only conclusion would
  become the operative finding pending any further, differently-designed
  candidate.

IF EXACTLY ONE CANDIDATE PASSES:
  It becomes the sole eligible candidate for a future, separately
  authorized real-data fit. No further tie-breaking needed.

IF MULTIPLE CANDIDATES PASS:
  Tie-breaking, in this priority order:
    1. Prefer the candidate whose recovery test used the resolution
       regime that most closely matches the real data's ACTUAL,
       audited precision distribution (per Phase 0's findings) --
       i.e., prefer M2/M3 (which use the true year/interval-censored
       regime for the full n=141) over M4 (which by construction only
       validates a subset) unless M4's subset-specific claim is exactly
       what a future research question needs.
    2. Among remaining ties, prefer the candidate with the SIMPLER
       parameterization (fewer free parameters) at comparable recovery
       quality -- consistent with root cause #7's own finding that V1
       was likely over-parameterized for its effective sample size.
    3. If still tied, this becomes an explicit researcher decision, not
       an automated resolution -- multiple valid candidates with
       different substantive interpretations (e.g. CD-1 vs CD-2) may
       legitimately coexist and require a scientific judgment call, not
       a numeric tiebreaker.
  Multiple passing candidates may also legitimately be reported together
  as a robustness/triangulation result rather than forcing a single
  winner, if their substantive conclusions agree.
```

---

## Final Status

```text
MODEL_3B_RECOVERY_TOURNAMENT_READY_FOR_RESEARCHER_DECISION
```

Nothing in this document authorizes execution of Phase 0 through Phase 4 above. Each phase requires its own separate, explicit researcher authorization before any code is written or run, per this session's standing discipline.
