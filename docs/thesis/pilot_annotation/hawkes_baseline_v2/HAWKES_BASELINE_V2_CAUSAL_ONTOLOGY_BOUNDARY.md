# HAWKES BASELINE V2 — CAUSAL AND ONTOLOGICAL BOUNDARY

Baseline: `f228b4a74d90234061b21c3d5969f5820955ab65`. This document formalizes the
observation/ontology and causal boundaries required by the governing
instruction (`docs/CLAUDE_HAWKES_V2_NEXT_DIALECTICAL_GOVERNANCE_AND_MODEL_FUTURE_DECISION.md`,
Sections 6-7, 12) applied to this corpus. It performs no fitting, simulation,
or new computation.

## 1. Observation decomposition

```
N_corpus(t) = O{ H(t), O(t), S(t), A(t), C(t) }
```

- `H(t)` — latent historical occurrence process (unobservable directly).
- `O(t)` — contemporary observation/recording process (what VOC-era actors
  chose to document).
- `S(t)` — archival survival and selection process.
- `A(t)` — present-day accessibility process (which surviving documents this
  project has actually digitized/scanned, e.g. GM Deel additions, CD5/CD6).
- `C(t)` — coding and corpus-construction process (this project's own
  extraction, deduplication, and field-mapping decisions).

**Prohibited identity:** `N_corpus(t) = H(t)`. Nothing produced anywhere in
this workstream treats the coded event stream as equal to the historical
occurrence process. This prohibition is REPOSITORY_FACT, not a new decision
of this operation.

`A(t)` in particular is empirically demonstrated to be uneven in this
project: corpus size grew from n=113 to n=141 across sessions as GM Deel
01-08 and CD5/CD6 were incorporated (SOURCE_SUPPORTED_CLAIM,
`project_markov_hawkes_models` memory). Any within-corpus intensity
comparison must treat `A(t)` as a live confound, not a constant.

## 2. Seven-entity event ontology (maintained separately, not collapsed)

```
LATENT_HISTORICAL_EVENT      — an occurrence in the past, never directly observed
DOCUMENTED_OR_REPORTED_EVENT — a period source's account of an occurrence
CORPUS_CODED_EVENT           — a row in this project's extracted dataset
PARENT_EPISODE                — a single historical episode that may correspond
                                to >1 CORPUS_CODED_EVENT (see A6/C6, register)
SYNTHETIC_GENERATED_EVENT     — a simulator-produced event used for
                                identifiability/recovery testing (V2-A, Model
                                3B-CD V1), never treated as a historical claim
OBSERVED_SYNTHETIC_EVENT      — the subset of a synthetic event stream an
                                estimator actually receives (e.g. after
                                censoring/jitter), used only for recovery
                                diagnostics
ESTIMATOR_INPUT_EVENT         — whatever event representation is actually
                                passed to the point-process likelihood
                                (jittered CORPUS_CODED_EVENT rows for the
                                production fit; OBSERVED_SYNTHETIC_EVENT rows
                                for V2-A recovery testing)
```

For each type, the required audit fields per the governing instruction
(identity rule, start/end boundary, source evidence, report-event
distinction, parent-episode relation, duplicate-report relation, date
interval, actor ontology, action ontology, outcome ontology, coding
uncertainty) are **not** completed for any of the seven entities in this
operation — completing them is new ontology-construction work, out of scope
here per the "no new research artifact beyond the seven listed deliverables"
constraint and explicitly gated below.

```
G_ontology^future = 1[ M_event=M_report=M_episode=M_source=M_coding=M_date=1 ]
```

Current state, unchanged by this operation:

```
G_ontology = 0
```

## 3. Causal layer

No causal claim may be inferred from temporal self-excitation alone. A
future causal estimand, if one is ever pursued, would require a defined
intervention:

```
tau(Delta) = E[ N^do(E=1)(t, t+Delta] ] - E[ N^do(E=0)(t, t+Delta] ]
```

where `E` is a defined historical exposure/intervention, `N^do(E=e)` is the
counterfactual event count under intervention state `e`, and `Delta` is a
prespecified follow-up horizon. **This document does not assert this
estimand is identifiable in this corpus.**

```
G_causal^future = 1[ I_intervention=I_counterfactual=I_confounding=
                      I_observation=I_positivity=I_consistency=
                      I_identification = 1 ]
```

None of the seven indicators is currently established. Current state,
unchanged:

```
G_causal = 0
```

Three distinct concepts must remain separate and are not interchangeable in
any future document in this workstream:

1. **Granger-type history dependence** — a statement about predictive
   information content of past events for future intensity, estimable from
   data alone.
2. **Model excitation** (`eta`, the fitted branching ratio) — a
   model-internal, model-conditional quantity: "expected fitted offspring
   ratio within the specified point-process model for the estimator-input
   event representation." Nothing more.
3. **Intervention-based causality** (`tau(Delta)` above) — requires
   identification assumptions never established in this corpus.

## 4. Colonial-narrative and source-critical boundary

VOC administrative categories (e.g. `dominion_status` labels such as
`voc_alliance`, `relapse_aceh`, `foreign_orbit`) are source categories
produced by the colonial administration's own record-keeping, not neutral
descriptions of historical actor intent. For every modeled event label, four
distinct layers must be kept distinguishable:

```
SOURCE_CATEGORY          — the label as the VOC-era document itself uses it
PROJECT_ANALYTIC_CATEGORY — this project's coding of that label into a field
HISTORIAN_INTERPRETATION  — a secondary-literature reading of the underlying
                            event (e.g. Vogel, Kathirithamby-Wells)
MODEL_INPUT_CATEGORY      — whatever category value is actually passed to a
                            fitted model (e.g. as a stratification arm)
```

A directly analogous coding-policy artifact was previously found and
corrected in this same corpus family: the `pelabuhan_disebut` field was
contaminated by archive-index pages and required filtering (76% of noise
removed) before it could support any downstream graph structure
(SOURCE_SUPPORTED_CLAIM, `feedback_register_page_contamination` memory).
This establishes precedent, not an assumption, that unmarked category
conflation is a live risk class in this corpus, independent of whether the
model in question is a Hawkes process.

```
G_sourcecrit = 1[ N_unmarked_colonial_categories=0
                   AND N_silent_category_normalizations=0
                   AND N_unsupported_resistance_labels=0 ]
```

This operation does not audit `G_sourcecrit` against the full corpus (that
would be new research work); it records the gate's definition and one
precedent finding as context for the future-role recommendation. No future
model authorization is possible while `G_sourcecrit=0` or unverified.

## 5. Checkpoint-1 researcher decision and remediation domain (added by correction)

The researcher adjudicated Checkpoint 1 and selected:

```
F3_SUSPEND_PENDING_ONTOLOGY_AND_OBSERVATION_MODEL_REMEDIATION
STATUS = ADOPTED_BY_RESEARCHER
DECISION_TYPE = RESEARCHER_DECISION
DECISION_SCOPE = CURRENT_CORPUS_AND_CURRENT_MODELING_WORKSTREAM
FAMILY_WIDE_REJECTION = NO
RETROSPECTIVE_MODEL_INVALIDATION = NO
```

This is a governance decision that the corpus is not presently ready for
either exploratory fitting or Hawkes-derived visualization — it is not a
finding that the Hawkes family failed.

F3 remains in force until a future operation evaluates at least:

```
R-O1  event identity and granularity
R-O2  report versus event distinction
R-O3  parent-episode membership
R-O4  duplicate and corroborating-report relations
R-O5  date intervals and unresolved precision
R-O6  actor/action/outcome ontology
R-O7  colonial source-category versus project analytic-category mapping
R-O8  observation, survival, access, and coding processes
R-O9  annual archival-exposure construction
R-O10 feasibility of nonstationary and exposure-adjusted comparators
```

```
R_O = { R-O1, ..., R-O10 }
Q_r in { PASS, FAIL, NOT_EVALUABLE }   for each r in R_O

G_reconsider^future = 1[ Q_R-O1 = ... = Q_R-O10 = PASS  AND  G_sourcecrit = 1 ]
```

This gate is **prospective only** and is **not evaluated in this
operation** — no `Q_r` value is assigned here.

Consequences of F3, in force now:

```
A_Hawkes_historical_fit = 0
A_Hawkes_visualization  = 0
A_V2B                    = 0
A_causal_interpretation  = 0
A_ontology_promotion     = 0

historical inference = NOT_AUTHORIZED
V2-B = BLOCKED
```

F3 does not change:

```
Hawkes family = EXPLORATORY_CANDIDATE, NOT_RULED_OUT
V2-A = MIXED_VALIDATION_RESULT
H-05 = H05_NOT_EVALUABLE_REQUIRES_RESEARCHER_REVIEW
F_SLR = 1
G_causal = 0
G_ontology = 0
```

## 6. What this document does not do

It does not authorize V2-B, historical fitting, causal interpretation,
ontology promotion, or source-category normalization. It does not alter any
frozen V2-A result. `G_causal=0` and `G_ontology=0` are preserved exactly as
they were before this operation.
