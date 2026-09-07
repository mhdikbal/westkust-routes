# HAWKES V2 — DIVERGENT EVIDENCE ACQUISITION AND MECHANISM DISCRIMINATION — MASTER REPORT (CHECKPOINT 1C, CORRECTED)

**Checkpoint 1C correction note:** this document is corrected per
`docs/CLAUDE_HAWKES_V2_EVIDENCE_ACQUISITION_NARROW_CORRECTION.md` (CR-1
through CR-8), following the read-only audit conducted under
`docs/CLAUDE_HAWKES_V2_EVIDENCE_ACQUISITION_CHECKPOINT1_AUDIT.md`. The
audit's central finding — an unsupported MEC-13 live-to-nonlive transition
— is corrected here. The audit trail showing the defect occurred is
preserved, not erased (Sections 9, 16, 19 below).

Governing instruction: `docs/CLAUDE_HAWKES_V2_DIVERGENT_EVIDENCE_ACQUISITION_AND_DISCRIMINATION_PLAN.md`
Authoritative HEAD: `38137fe0ad923488ffbedc4d4fc640c096acf0b5`

No Hawkes fitting, forecasting, predictive-likelihood calculation, simulation,
bootstrap, calibration, or visualization was performed. AS86 and the 141-row
corpus were not mutated. No sensitivity corpus was created. DEDUP-06 was not
resolved. V2-B was not executed. Phase D was not rerun. No working-tree
disposition, housekeeping, or unrelated Git action occurred.

---

## 1. Repository state and protected values

```
local HEAD  = 38137fe0ad923488ffbedc4d4fc640c096acf0b5   -- MATCH
origin/main = 38137fe0ad923488ffbedc4d4fc640c096acf0b5   -- MATCH (fresh fetch)
N_staged = 0
N_tracked_modified = 0
```
The twelve new outputs under `evidence_acquisition/` are **not merely
untracked — they are Git-ignored** by the existing repository rule
`.gitignore:163: docs/thesis/pilot_annotation/hawkes_baseline_v2/*`,
confirmed via `git check-ignore -v` on each. This is the same rule that
covered the ten divergent-remediation outputs before they were explicitly
force-added in Checkpoint 2 — explicit `git add <path>` still works on an
ignored path; only wildcard adds are blocked by it. This is a more precise
statement than "untracked" and is recorded here because the governing
instruction's Section 12 asks for exact tracked/staged/untracked status.

**Live Git-visible untracked count (fact only, no census rerun):** 704.
This is fully explained by two additions since the last audited baseline
(703, itself already reflecting the prior turn's self-referential
adjudication-file drift): this operation's own governing instruction file,
`docs/CLAUDE_HAWKES_V2_DIVERGENT_EVIDENCE_ACQUISITION_AND_DISCRIMINATION_PLAN.md`
(+1). The twelve new evidence-acquisition outputs contribute **zero** to
this count, being Git-ignored. No other path changed. Per the governing
instruction's Section 13 and the prior adjudication's `G_stop_recursion`
precedent, this is reported as a fact, not re-audited.

```
Frozen state (restated, unchanged):
V2-A = MIXED_VALIDATION_RESULT
Hawkes family = EXPLORATORY_CANDIDATE / NOT_RULED_OUT
F3 = SUSPEND_PENDING_ONTOLOGY_AND_OBSERVATION_MODEL_REMEDIATION
Hawkes fitting = SUSPENDED
Hawkes visualization = SUSPENDED
H-05 = H05_NOT_EVALUABLE_REQUIRES_RESEARCHER_REVIEW
G_artifact_verification = 1
D1 = NOT_EVALUABLE
G_divergent = NOT_EVALUABLE
G_ontology = 0
G_causal = 0
G_reconsider_future = 0
V2-B = BLOCKED
DEDUP-06 = UNRESOLVED
AS86 = FROZEN_UNCHANGED
R-O = 0 PASS / 1 FAIL / 9 NOT_EVALUABLE
G_sync = NOT_EVALUABLE
Phase D = CLOSED / MUST NOT BE RERUN
```

## 2. Exact output paths, hashes, byte sizes

All twelve outputs are under `docs/thesis/pilot_annotation/hawkes_baseline_v2/evidence_acquisition/` — see Section 12 of this report for the computed table (hashes are computed after all twelve files are finalized, in the terminal evidence accompanying this Checkpoint-1 response).

## 3. WP-E1 — Material-claim denominator and coverage

```
CORRECTED per CR-1 (prior value was N_material_claims=23, P_claim=23/23=1.00,
which omitted two compound gates already cited as dependency targets):

N_material_claims_identified = 25   (C1-C12; R-O1..R-O10; SCENARIO-S-CURRENT;
  G_sourcecrit; G_ontology_future)
N_material_claims_represented = 25  (the two omitted claims were added using
  existing repository evidence -- HAWKES_BASELINE_V2_RO1_RO10_GATE_MATRIX.csv
  rows G_sourcecrit and G_ontology_future -- no new source retrieval)
P_claim = 25/25 = 1.00   (pre-correction value: 23/25 = 0.92, retained in the
  reproducibility manifest for the audit trail)
```
Full ledger: `HAWKES_V2_CLAIM_EVIDENCE_DEPENDENCY_LEDGER.csv` (now 25 rows).
**Estimand clarified per CR-1:** this is representation coverage in the
dependency ledger, not truth, validity, ontology readiness, or historical
completeness. Not every proposition in every committed file was retyped —
per WP-E1's explicit scope, only claims already identified as material by
the governing artifacts were included. `R-O` rows remain compound decision
objects (construct + numerator/denominator + terminal status + blocking
condition), not bare claims at the same analytical level as `C1`-`C12` —
this is an inherited convention from the committed gate matrix, not
introduced here.

## 4. WP-E2 — Research-question decomposition

Ten questions (Q1–Q10), full table in
`HAWKES_V2_RESEARCH_QUESTION_DECOMPOSITION.csv`. Each is recorded as
`(object, domain, evidence, alternatives, uncertainty_types, decision_rule)`.
Summary: Q1 (event unit) and Q6 (exposure) remain the most evidentially
starved; Q10 (irreducibly not evaluable) is explicitly non-empty (R_record/
R_survival components of R-O8).

## 5. WP-E3 — Source-family denominator and coverage

```
CORRECTED per CR-2 -- relabeled estimand:

N_identified_source_objects = 9
N_with_metadata_record      = 9
IDENTIFIED_SOURCE_OBJECT_METADATA_COVERAGE = 9/9 = 1.00
  (domain: this repository's 9 identified objects ONLY -- NOT source
  comparability, NOT archival-opportunity coverage, NOT historical-source
  completeness)

Object-class sets (added column `object_class_set`):
S_primary   = {EIC correspondence, Vogel memoir}                    (2)
S_edited    = {CD, GM, Daghregister}                                 (3)
S_apparatus = {RGP editorial cross-reference apparatus}               (1)
S_secondary = {Kathirithamby thesis, Hakluyt/Lancaster edition}       (2)
UNCLASSIFIABLE (INFERENCE_ONLY) = {NL-HaNA archival scan}             (1)
2+3+1+2+1 = 9
```
Full map: `HAWKES_V2_SOURCE_FAMILY_OPPORTUNITY_MAP.csv` (now 14 columns,
including `object_class_set` and `metadata_coverage_label`). The nine items
span four structurally different object classes plus one unclassifiable
item — `9/9` never implies uniform comparability across them. Two families
(CD, GM) lack a documented lawful access route in repository evidence; the
NL-HaNA entry retains explicit `INFERENCE_ONLY` status per the prior
provenance audit — its very relevance to this project is unconfirmed, not
merely its access route.

## 6. WP-E4 / WP-E5 — Event-unit and date-semantics protocol summaries

`HAWKES_V2_EVENT_UNIT_ADJUDICATION_PROTOCOL.md`: defines
`E_i^unit = 1[I=B=G=P=1]` over six entity classes, with three worked
hypothetical examples (none scoring `E^unit=1`, illustrating that the
instrument is discriminating, not automatically permissive). No AS86 row
was scored.

`HAWKES_V2_DATE_SEMANTICS_PROTOCOL.md`: defines a 10-role date taxonomy and
a `D_i=(value,role,precision,lower,upper,source,confidence_basis)` record
structure with a categorical (never numeric) `confidence_basis`. No
interval bounds were constructed for any actual corpus row.

## 7. WP-E6 — DEDUP-06 retrieval-dossier status

```
DEDUP-06 = UNRESOLVED (unchanged)
D_primary_unresolved = 1, K_primary_unresolved = 1
G_DEDUP06 = 1[R=1 ∧ Q=1 ∧ C=1 ∧ A=1] = 0
  R = source object retrieved
  Q = referent readable and locatable
  C = competing hypotheses discriminable
  A = researcher accepts the adjudication
```
Full dossier: `HAWKES_V2_DEDUP06_RETRIEVAL_DOSSIER.md`. Specifies the known
row, citation string, decomposed locator components, missing object,
retrieval route (specification only, not executed), required philological
checks, the three live hypotheses restated, and a blank researcher
adjudication form. Nothing was retrieved.

**CORRECTED per CR-4:** retrieval alone establishes at most `R=1`; it does
not imply `Q`, `C`, or `A`, and does not by itself resolve DEDUP-06,
correct AS86, or convert R-O4 to PASS. **`ACT-01` is labeled
`MAY_ENABLE_ADJUDICATION`, not `WILL_RESOLVE_FAIL`.**

## 8. WP-E7 — External-exposure feasibility map

Full specification: `HAWKES_V2_EXPOSURE_ACQUISITION_SPECIFICATION.csv`
(now includes a `readiness_zero_type` column per CR-5).
Of 6 candidate types: 2 (`ANNUAL_ACTIVE_SOURCE_FAMILY_COUNT`,
`ANNUAL_DIGITIZATION_OR_ACCESS_COVERAGE`) are already-assessed and circular
(`C_m^overlap=1`, all model roles prohibited except descriptive use) —
**`CONJUNCTION_ZERO`**: only `X_external_to_outcome=0`, while
`A=C=T=P=1`; 3 (`ANNUAL_SURVIVING_DOCUMENT_COUNT`,
`ANNUAL_FOLIO_OR_PAGE_COUNT`, `ANNUAL_CATALOGUE_RECORD_COUNT`) have a
concrete acquisition specification but **`ALL_COMPONENTS_ZERO`**
(`A=X=C=T=P=0` individually, not merely the conjunction); 1
(`OTHER_EXTERNAL_ARCHIVAL_OPPORTUNITY_MEASURE`) remains open by design
(`ALL_COMPONENTS_ZERO`, undefined until a candidate is named). **No
numerical exposure series was collected.**

## 9. WP-E8 — MEC-01 through MEC-15 discrimination status

Full matrix: `HAWKES_V2_MECHANISM_DISCRIMINATION_MATRIX.csv`.

**CR-3 CORRECTION — audit trail preserved, not erased:** the version of
this report first returned at Checkpoint 1 stated `LIVE (10) / NONLIVE (5)`,
moving `MEC-13` from live (`PLAUSIBLE_MODEL_RISK`, as recorded in the
committed baseline) to nonlive on the sole basis that its required join
(dominion_status × event corpus) is not yet built. The subsequent read-only
audit found this unsupported: applying
`G_drop,13 = 1[D_available=1 ∧ D_decisive=1 ∧ P=1 ∧ A=1]`, **no
discriminating evidence exists for MEC-13 at all** (`D_available=0`), so
`G_drop,13=0` and the transition should never have occurred — a blocked
prerequisite is absence of evidence, not disconfirming evidence. This was
reported as `FALSE_CONVERGENCE_DETECTED` for MEC-13 specifically.
**`MEC-13` is restored here to `LIVE / RETAIN_AS_OPEN`**, with its
assessment status corrected to `NOT_TESTABLE_BLOCKED_ON_JOIN` (not
historical exclusion).

```
CORRECTED (matches the original committed 11/4 split -- no net mechanism
transition should have occurred in this operation at all):

LIVE (11): MEC-01, MEC-02, MEC-05, MEC-06, MEC-07, MEC-08, MEC-09, MEC-11, MEC-12, MEC-13, MEC-14
NONLIVE (4): MEC-03 (structural), MEC-04 (structural), MEC-10 (blocked on R-O6 schema), MEC-15 (constructed placeholder)
11 + 4 = 15  ✓

FALSE_CONVERGENCE_DETECTED_PRECORRECTION = TRUE  (MEC-13, this operation's own prior pass)
FALSE_CONVERGENCE_REMEDIATED = TRUE  (MEC-13 now LIVE/RETAIN_AS_OPEN consistently
  in the mechanism matrix, the reproducibility manifest, and this report)
```
For MEC-03, MEC-04, MEC-10, and MEC-15: `NONLIVE` in every case means
structural non-testability or a blocked prerequisite/constructed
placeholder — **never** historical exclusion or mechanism disconfirmation;
none of the four was tested and found false.

Expected epistemic effect is drawn only from the five allowed tokens
(`MAY_NARROW_LIVE_SET`, `MAY_RECLASSIFY_UNCERTAINTY`,
`MAY_IMPROVE_OBSERVATION_MODEL`, `NONDISTINGUISHING`, `NOT_EVALUABLE`) —
`WILL_PROVE_MECHANISM` is never used, confirmed by direct grep of the file.

## 10. WP-E9 — Negative-control and comparator design status

Full design: `HAWKES_V2_NEGATIVE_CONTROL_COMPARATOR_DESIGN.csv`. 5 controls
designed (NC-01 through NC-05); only NC-02 and NC-05 reach
`G_NC,z=1` (design-admissible), and even NC-05 (the one control requiring
no new source access) has its *execution* explicitly marked `PROHIBITED`
in the evidence portfolio (`ACT-12`) because it would require refitting —
not authorized in this operation. **No statistical control or comparator
was executed.**

## 11. WP-E10 — Prospective proposition-segmentation gate

```
G_seg^prospective = 1[R=1 ∧ E=1 ∧ U=1 ∧ A=1]
(R,E,U,A) = (1,1,1,0)   -- rule, examples, ambiguity policy present; researcher acceptance pending
G_seg^prospective = 0   (blocked solely on researcher acceptance)
```
**CORRECTED per CR-6:** `E10` ("segmentation is prospective, not
retrospective") is relabeled `E10_PROCESS_COMPLETENESS = 1` — it certifies
only that a protocol was drafted with correct prospective scope, **not**
that the protocol passed its own researcher-acceptance gate. These are
different estimands, kept explicitly separate:
```
E10_PROCESS_COMPLETENESS = 1
G_seg^prospective          = 0
```
`D1^prior = NOT_EVALUABLE` is explicitly preserved regardless of either
value (`HAWKES_V2_PROSPECTIVE_PROPOSITION_SEGMENTATION_PROTOCOL.md`, Section 6).

## 12. WP-E11 — Evidence portfolio

Full portfolio: `HAWKES_V2_EVIDENCE_PORTFOLIO_AND_REPRODUCIBILITY_MANIFEST.csv`
(rows tagged `PORTFOLIO_ACTION`). Twelve actions (ACT-01 through ACT-12):

```
PROHIBITED               : 1  (ACT-12, would require refitting)
DO_NOW_READ_ONLY         : 2  (ACT-02, ACT-06)
DESIGN_ONLY              : 2  (ACT-03, ACT-08)
REQUEST_SOURCE_ACCESS    : 3  (ACT-01, ACT-07, ACT-09)
NOT_AUTHORIZED           : 1  (ACT-05 -- CORRECTED per CR-8: G_ACT05_design=0,
                                a five-way term-classification protocol
                                (SOURCE_NATIVE_TERM / SOURCE_REPORTED_CLASSIFICATION /
                                PROJECT_NORMALIZED_LABEL / HISTORIAN_INTERPRETATION /
                                UNRESOLVED_TRANSLATION_OR_CATEGORY) does not yet exist
                                or have researcher acceptance)
REQUIRES_RESEARCHER_REVIEW: 3 (ACT-04, ACT-10, ACT-11)
DEFER                    : 0
1+2+2+3+1+3 = 12  ✓
```
No numerical utility weights or probabilities were assigned to any action;
risk is recorded categorically (`LOW/MODERATE/HIGH`) per action-dimension,
never combined into a single score.

## 13. Uncertainty-type distribution (illustrative, per WP-E1/E8 material claims)

Reusing the U1–U12 taxonomy against the 23 material claims and 15
mechanisms surfaced in this operation (not a full re-tag of every
proposition — that remains gated by WP-E10's `researcher_acceptance=0`):

```
U5  ONTOLOGICAL_UNCERTAINTY                : dominant across R-O1,R-O2,R-O3,R-O4/DEDUP-06,R-O6 and MEC-07
U6  SOURCE_SURVIVAL_UNCERTAINTY            : R-O8, R-O9, MEC-03, MEC-04
U8  SOURCE_INTENT_OR_CATEGORY_UNCERTAINTY  : R-O7, G_sourcecrit, ACT-05 (colonial-category mapping)
U9  CODING_UNCERTAINTY                     : R-O1, MEC-06, MEC-12
U11 MECHANISM_UNDERDETERMINATION           : MEC-01,02,05,07,08,09,13,14 (the bulk of live mechanisms; MEC-10 is a schema-blocked NONLIVE item, U11 not applicable to it in the same sense)
U4  MEASUREMENT_OR_DATE_UNCERTAINTY        : R-O5, MEC-08 (the one presumptively quantifiable item, conditional on WP-E5 parsing-rule adoption)
```
No probability distribution was assigned to any U5/U6/U8/U11-typed item.

## 14. Red-team / Blue-team / Anti-compliance audit (WP-E12)

### 14.1 ACT-01 (retrieve "Corpus III, nr. D")

**Blue team:** This is the single highest-value action in the portfolio —
it `MAY_ENABLE_ADJUDICATION` of R-O4/DEDUP-06 (CORRECTED per CR-4; retrieval
alone does not itself resolve the FAIL — see Section 7), is fully
reversible (read-only retrieval), and has a specified route.

**Red team:** (a) *Category error risk:* the retrieval route in Section 6
of the dossier is itself speculative — "Corpus III" is matched to RGP/CD
conventions by pattern only, not confirmed; retrieval effort could be
spent against the wrong series entirely. (b) *Circularity risk:* if
retrieval finds nothing, that absence must not be read as favoring
H-DEDUP06-C (citation artifact) — absence of a found document is
`SOURCE_ACCESS_UNCERTAINTY` (U7), not evidence for any of the three
hypotheses. (c) *False-precision risk:* even a successful retrieval only
produces categorical discrimination among A/B/C, never a probability of
which is correct.

**Anti-compliance check:** No renaming detected — retrieval is described
as retrieval, not as "verification" or "closure."

### 14.2 ACT-05 (colonial-category source-term extraction)

**Blue team:** Directly unblocks `G_sourcecrit` and is the highest-leverage
single action for reclassifying U8-typed uncertainty across five
`event_type` categories at once; a proven method (the `pelabuhan_disebut`
precedent) already exists in this same corpus family.

**Red team:** (a) *Colonial-category-naturalization risk (flagged
explicitly by name in the governing instruction):* extracting a "literal
source term" is not itself neutral — the extractor's own translation and
categorization choices could re-import the same naturalization risk one
level down (e.g. deciding that a Dutch term "corresponds to" `konflik`
is itself an interpretive act). (b) *Denominator risk:* five categories
were named in R-O7, but extraction might reveal that the true source-native
category count is different (more granular or more coarse), silently
shifting the denominator if not flagged. (c) *Evidence-leakage risk:*
using this project's own prior translations (rather than independent
philological review) to interpret newly retrieved terms risks circularity.

**Anti-compliance check:** No renaming detected.

### 14.3 General anti-compliance scan across all twelve outputs

Checked specifically for the six named evasion patterns:

```
"diagnostic scoring" for fitting           -- NOT FOUND
"scenario projection" for forecasting      -- NOT FOUND (Section 8 of the deep-uncertainty
                                                scenario matrix in the prior operation already
                                                uses "scenario" correctly, as a categorical
                                                classification, not a forecast; not reused here
                                                as a forecast euphemism)
"synthetic stress exploration" for simulation -- NOT FOUND
"mechanism attribution" for causal inference  -- NOT FOUND (MEC discrimination matrix explicitly
                                                uses MAY_NARROW_LIVE_SET / MAY_RECLASSIFY_UNCERTAINTY,
                                                never a causal-sounding attribution verb)
"schema completion" for ontology validation   -- NOT FOUND (Section 4 explicit: "no AS86 row
                                                was scored"; WP-E4/E5 protocols are explicitly
                                                labeled design-only)
"temporary sensitivity preparation" for AS86 mutation -- NOT FOUND (no sensitivity corpus created;
                                                explicitly confirmed in Section 1)
```
```
REASONING_SHORTCUT_DETECTED = NOT TRIGGERED
PROHIBITED_OPERATION_RELABELED = NOT TRIGGERED
```

## 14.4 CR-8 completion — ACT-05 five-way term-classification protocol (design-only)

This section completes CR-8, previously left incomplete (only the five
class names were given, without assignment rules, ambiguity policy, or
provenance fields). **This is a design document only — no source is
retrieved, no term is classified, and ACT-05 remains unexecuted.**

**Classes:**
```
SNT = SOURCE_NATIVE_TERM
SRC = SOURCE_REPORTED_CLASSIFICATION
PNL = PROJECT_NORMALIZED_LABEL
HI  = HISTORIAN_INTERPRETATION
UTC = UNRESOLVED_TRANSLATION_OR_CATEGORY
```

**Assignment rules (positive inclusion and exclusion criteria per class):**

| Class | Positive inclusion criterion | Exclusion criterion |
|---|---|---|
| `SNT` | The exact lexical form is directly attested in the source text itself (a word or phrase actually written in the document), recorded without converting it into any analytical class | Excluded if the "term" is actually a project-assigned label, a translation, or an analyst's paraphrase rather than the attested source wording |
| `SRC` | The historical source (or its author) itself explicitly assigns a category to the item (e.g. the document itself calls something a "verbond" or labels an act as belonging to a named administrative category) | Excluded if the categorization is supplied by this project or by a later historian rather than by the source/author at the time of writing; a lexical form being present (`SNT`) does not by itself establish that the source also *categorized* it (per the governing instruction's explicit point: "a source-native term and a source-reported classification are not automatically identical") |
| `PNL` | The label was introduced by this project for retrieval, grouping, or coding purposes (e.g. `event_type` values `perjanjian`, `konflik`, `administratif`, `diplomasi`, `suksesi`) | Excluded if the label can be traced to source wording (`SNT`) or source categorization (`SRC`) rather than to project coding decisions |
| `HI` | The proposition is an interpretive claim introduced by a historian or analyst (this project's own agent interpretation, or a cited secondary-scholarship interpretation, e.g. Kathirithamby's thesis framing) about what a term or category means or implies | Excluded if the claim is a direct quotation (`SNT`), a source's own explicit categorization (`SRC`), or a project coding convention (`PNL`) rather than an interpretive addition |
| `UTC` | The reading, translation, or category boundary cannot currently be resolved to one of the other four classes, OR two or more classes remain simultaneously plausible | This is the residual/default class — an item is placed here precisely when no other class can be assigned without forcing a choice; it is never used as a first-choice convenience label |

**Ambiguity policy** (verbatim requirements, all satisfied by design):
```
1. No silent multi-class assignment -- every term instance gets exactly one T_j^category value,
   with any live alternative reading recorded in a separate `alternative_reading` field, not
   by assigning two classes.
2. No forced choice when two or more readings remain live -- such cases are assigned UTC,
   not the "most convenient" of the other four.
3. Unresolved cases enter UTC and an adjudication queue (structurally identical to the
   WP-E10 ambiguity-adjudication queue design: {document, locator, candidate_readings,
   reviewer_notes, researcher_decision}).
4. Original source form is preserved (the `diplomatic_form` provenance field, below,
   is never overwritten by a normalized or translated reading).
5. Normalized and interpretive fields remain separate (`normalized_reading` and
   `translation` are distinct provenance fields from `category_class` and from any
   historian-interpretation content).
6. Colonial administrative categories are not treated as neutral ontology -- an SRC or
   PNL classification of an administrative term does not by itself certify that the
   category is historically neutral; this remains an open question tracked via
   `classification_basis` and `ambiguity_status`, not resolved by classification alone.
7. Absence of a term is not evidence of absence of a historical phenomenon -- a term
   instance not found in a given source is recorded as SOURCE_ACCESS_UNCERTAINTY (U7)
   or SOURCE_SURVIVAL_UNCERTAINTY (U6) in the uncertainty taxonomy, never as SOURCE_SILENCE
   implying the underlying phenomenon did not occur (Section 2 item 8 prohibition,
   inherited from the divergent-remediation governing instruction).
```

**Provenance fields** (all 15 required fields, defined):

| Field | Definition |
|---|---|
| `term_instance_id` | Unique identifier for this specific occurrence of a term (not the term type — the same lexical form appearing in two documents gets two instance IDs) |
| `source_id` | Identifier of the source document the instance was found in (cross-references `HAWKES_V2_SOURCE_FAMILY_OPPORTUNITY_MAP.csv`) |
| `source_locator` | Page/folio/section locator within the source document |
| `source_image_or_text_reference` | Pointer to the actual image or transcribed text this instance was read from |
| `diplomatic_form` | The exact, unmodified transcription of the term as it appears in the source (preserved verbatim; never overwritten) |
| `normalized_reading` | A normalized spelling/form of the diplomatic form (e.g. resolving period orthographic variation), kept distinct from translation |
| `translation` | An English/Indonesian translation of the term, kept distinct from normalization and from interpretation |
| `category_class` | The assigned `T_j^category ∈ {SNT,SRC,PNL,HI,UTC}` |
| `classification_actor` | Who/what assigned `category_class` (e.g. "project coder," "cited secondary source," "this operation's design protocol") |
| `classification_basis` | The stated reason for the classification (links back to the assignment-rule table above) |
| `alternative_reading` | Any live alternative classification or translation not selected, preserved rather than discarded |
| `ambiguity_status` | `RESOLVED` or `UNRESOLVED_ENTERS_ADJUDICATION_QUEUE` |
| `reviewer` | Person/process that reviewed the classification |
| `researcher_decision` | Final researcher-level disposition, if adjudicated |
| `decision_date` | Date of researcher decision, if any |

**ACT-05 design gate:**
```
G_ACT05^design = 1[C=1 ∧ R=1 ∧ U=1 ∧ P=1 ∧ A=1]
C = 1 (five classes defined, above)
R = 1 (assignment + exclusion rules defined for all five classes, above)
U = 1 (seven-item ambiguity policy defined, above)
P = 1 (fifteen provenance fields defined, above)
A = 0 (researcher acceptance not yet obtained)

G_ACT05^design = 0
```
This is the correct value: **protocol completeness does not imply
researcher acceptance or execution authorization.** `ACT-05` remains
`NOT_AUTHORIZED`. No term was classified; no source was consulted beyond
what this repository already documents (the `pelabuhan_disebut` precedent
and the existing `event_type`/R-O7 category list).

## 15. False-convergence count

```
N_false_convergence^claim = Σ 1[DECISION_c ∈ {ADOPT,REJECT} ∧ G_c^conv=0]
```
Applied to the 25-claim ledger (Section 3): the only `ADOPT`/`REJECT`
decisions present (C1,C2,C3,C4,C8,C9,C11) were already verified
`G_c^conv=1` in the prior operation and are not reopened here; R-O4/DEDUP-06
is `FAIL` (a demonstrated fact, not a mechanism pick among live
alternatives, so it does not enter this sum); `G_sourcecrit` and
`G_ontology_future` carry no `ADOPT`/`REJECT` decision (both are
`NOT_EVALUABLE`/`MIXED` gate assessments); all `NOT_EVALUABLE` R-O items
and all `RETAIN_AS_OPEN` claims/mechanisms correctly avoid forced
decisions.
```
N_false_convergence^claim = 0   (strict claim-level formula; unchanged and correct)
```
**Kept explicitly separate per CR-7:** this zero claim-level count does
**not** paper over the mechanism-level defect found by the audit —
`FALSE_CONVERGENCE_DETECTED_PRECORRECTION = TRUE` for the MEC-13
live-to-nonlive transition in this operation's own first pass (Section 9),
now `FALSE_CONVERGENCE_REMEDIATED = TRUE` after restoration.

## 16. Program gates E0–E15

**Pre-correction values (audit trail, preserved per CR-7 — not erased):**
`E8=0` (MEC-13's unsupported transition), `E14=0` (that transition was an
undocumented, silent epistemic promotion from "unavailable evidence" to
"nonlive"), `G_E=0`.

**Post-correction values, recomputed from the corrected artifacts (not
forced to 1 merely because wording changed — each is checked against its
actual evidence condition):**

| Gate | Value | Concerns | Evidence path |
|---|---|---|---|
| E0 zero prohibited execution | 1 | production | Section 1; no fitting/retrieval/staging occurred in this correction pass |
| E1 baseline/protected-state fidelity | 1 | production | Section 1, HEAD/origin match |
| E2 material-claim denominator explicit | 1 | production | Section 3, corrected 25/25 — explicit, not merely asserted |
| E3 source-family map complete (relative to identified) | 1 | production | Section 5, 9/9 metadata coverage, relabeled per CR-2 |
| E4 event-unit protocol without corpus mutation | 1 | production | Section 6; no AS86 row scored |
| E5 date-semantics protocol without model use | 1 | production | Section 6; no bounds constructed |
| E6 DEDUP-06 dossier complete, status unresolved | 1 | production | Section 7; `G_DEDUP06=0` preserved |
| E7 exposure plans distinguish external from circular | 1 | production | Section 8; `CONJUNCTION_ZERO`/`ALL_COMPONENTS_ZERO` now explicit |
| **E8** all MEC-01..15 retain evidence-sensitive status | **1** | **scientific/evidentiary** | Section 9; MEC-13 restored to LIVE/RETAIN_AS_OPEN, verified consistent across the mechanism matrix, manifest, and this report — the actual evidence condition (no mechanism closed without `G_drop=1`) is now genuinely satisfied, not merely asserted |
| E9 comparator/negative-control designs unexecuted | 1 | production | Section 10; NC-05 execution remains PROHIBITED |
| E10 → **E10_PROCESS_COMPLETENESS** | 1 | production only | Section 11; explicitly does NOT mean `G_seg_prospective=1` |
| E11 action portfolio retains deep uncertainty | 1 | production | Section 12; no numeric weights |
| E12 red-team/blue-team/anti-compliance complete | 1 | production | Section 14 |
| E13 false-convergence count zero (claim-level) | 1 | scientific/evidentiary | Section 15; `N_false_convergence^claim=0`, kept separate from the remediated mechanism-level finding |
| **E14** all epistemic promotions documented | **1** | **scientific/evidentiary** | Section 9; the MEC-13 correction itself is now explicitly documented as a correction (this report, the manifest, the mechanism matrix), not a silent promotion — the defect that made E14=0 pre-correction is fixed by disclosure, not by erasure |
| E15 no working-tree disposition/unrelated Git action | 1 | production | Section 1; no housekeeping, no 13th file created |

```
G_E = 1[E0=E1=...=E15=1] = 1   (post-correction; G_E=0 pre-correction, per the audit trail above)
```

Explicit non-implications (restated per governing instruction Section 10):
```
G_E = 1  ⇏  G_seg_prospective = 1    (G_seg_prospective = 0, unaffected)
G_E = 1  ⇏  G_ontology = 1           (G_ontology = 0, unaffected)
G_E = 1  ⇏  G_causal = 1             (G_causal = 0, unaffected)
G_E = 1  ⇏  G_reconsider_future = 1  (G_reconsider_future = 0, unaffected)
```
`G_E=1` certifies only that the evidence-*acquisition-planning* process
completed without prohibited execution or false convergence — it is not a
readiness finding for Hawkes reconsideration.

## 17. Confirmation of unchanged frozen gates

All values listed in Section 1 were read, never recomputed or reinterpreted, in this operation. None changed.

## 18. Proposed next evidence-retrieval actions (bounded, not executed)

In descending order of portfolio priority (not asserted probability of success):
1. **ACT-01** — retrieve "Corpus III, nr. D" (`MAY_ENABLE_ADJUDICATION` of R-O4/DEDUP-06, not a guaranteed resolution; fully reversible)
2. **ACT-02** — re-verify existing dedup-adjudication coverage scope (DO_NOW_READ_ONLY, no new access needed)
3. **ACT-06** — audit Hawkes-relevant fields for the `pelabuhan_disebut`-analogous contamination pattern (DO_NOW_READ_ONLY)
4. **ACT-05** — `NOT_AUTHORIZED` until a five-way term-classification protocol (CR-8) is designed and researcher-accepted (`G_ACT05_design=0`); highest leverage but highest colonial-naturalization risk
5. **ACT-07** — search Nationaal Archief / British Library IOR for an external exposure ledger
6. **ACT-10** — obtain researcher acceptance of the WP-E10 segmentation protocol

None of these is executed in this operation. All require a separate, future authorization.

## 19. Recommendation

Given `G_E = 1` (post-correction, genuinely recomputed — see Section 16),
`N_false_convergence^claim = 0`, `FALSE_CONVERGENCE_REMEDIATED = TRUE` for
the MEC-13 defect, all 12 outputs corrected in place (no 13th file
created), and no prohibited execution detected in this correction pass:

```
CONTINUE_TO_BOUNDED_EVIDENCE_RETRIEVAL_REQUIRES_RESEARCHER_AUTHORIZATION
```

## 20. Git-ignore governance audit (Checkpoint 1D)

**Exact rule:** `.gitignore` line 163: `docs/thesis/pilot_annotation/hawkes_baseline_v2/*` — a broad directory-wildcard ignore, narrowed by re-include (`!`) exceptions on lines 164-166 and further specific exceptions later in the file (confirmed via `git show HEAD:.gitignore` and `git blame`).

**Predates HEAD?** YES. This line was introduced in commit `ee5fb4b0` (2026-09-06, authored by the repository owner), well before the current `HEAD=38137fe` (2026-09-07). It is not something this session introduced.

**Broad or exact-path?** The base rule (line 163) is **broad** (a full directory wildcard). It is narrowed by several **exact-pattern** re-includes: `!...HAWKES_BASELINE_V2_*.md`, `!...HAWKES_BASELINE_V2_*.csv`, `!...hawkes_v2_*.png`, plus many fully-exact-path `!` lines added across the V2-A workstream's history (e.g. `!...HAWKES_BASELINE_V2A_H05_FINAL_RESEARCHER_DECISION.md`).

**Root cause of contamination for these twelve outputs, identified:** the existing re-include patterns match filenames beginning `HAWKES_BASELINE_V2_` or `HAWKES_BASELINE_V2A_`. This evidence-acquisition package's twelve files are named `HAWKES_V2_*` (no "`BASELINE`") and additionally live one level deeper, in a `evidence_acquisition/` subdirectory that no existing re-include pattern addresses. **Neither the naming convention nor the subdirectory nesting was anticipated by the existing exceptions** — this is a naming/structure mismatch, not a deliberate concealment.

**Contamination scope if the base rule were narrowed:** 27 other paths currently rely on this same broad ignore within `hawkes_baseline_v2/` (verified via `git status --ignored`): 3 `__pycache__/*.pyc` files, 12 `v2a_*.py`/`.json`/`.csv` working files from the prior V2-A validation-engine workstream (including explicitly superseded/failed-attempt files like `v2a_full_study_meta_ATTEMPT1_FAILED_D3D5D9.json`), plus this operation's own 12 files. **Any change to the base rule or a new broad re-include would need to avoid re-exposing those 15 non-evidence-acquisition paths**, several of which are explicitly marked failed/superseded and are presumably meant to stay hidden.

```
N_ignored = 12
G_visible = 1[N_ignored=0] = 0
```

**Prospective options (none executed):**

| Option | Contamination risk if executed |
|---|---|
| 1. `NARROW_EXACT_PATH_GITIGNORE_EXCEPTION_REQUIRED` — add e.g. `!docs/thesis/pilot_annotation/hawkes_baseline_v2/evidence_acquisition/` (a subdirectory-scoped re-include) | **LOW** — matches only this operation's own subdirectory; the 15 sibling working/failed-attempt files sit directly in the parent directory, not inside `evidence_acquisition/`, so they would remain ignored |
| 2. `EXACT_PATH_FORCE_ADD_REQUIRES_RESEARCHER_AUTHORIZATION` — `git add` each of the twelve exact paths (as already done for the ten divergent-remediation outputs in Checkpoint 2) | **LOW** — touches no shared config file at all; identical precedent already exists in this repository's own history |
| 3. `OUTPUT_LOCATION_CHANGE_REQUIRES_RESEARCHER_AUTHORIZATION` — relocate the twelve files outside the ignored directory | **MODERATE-HIGH** — **prohibited by this instruction's own Section "Do not move the outputs"**; would also break every internal cross-reference among the twelve files that currently cites the `evidence_acquisition/` path, and is not evaluated further here |
| 4. `NO_GIT_FINALIZATION_REQUESTED` — leave as-is; Checkpoint review continues via terminal transcript only | **NONE** — status quo |

No option is executed. `.gitignore` is unmodified; no file is force-added.

## 21. `G_E_original` vs `G_correction_closure`

These are two distinct gates, not to be conflated:

```
G_E_original = 1[E0=E1=...=E15=1]
```
computed under the **original** E-component definitions from the governing
divergent-evidence-acquisition instruction. None of `E0`-`E15` was
originally defined to require ACT-05 protocol completeness — that
requirement belongs to CR-8, a correction-instruction addition, not an
original E-component. Recomputing each of the sixteen against their
original definitions (Section 16 above, post-Checkpoint-1C-correction
values) gives:
```
E0..E15 = 1 (all sixteen; see Section 16 table for individual evidence paths)
G_E_original = 1
```

```
G_correction_closure = 1[CR_1=CR_2=...=CR_8=1]
```
```
CR-1 (material-claim denominator)     = 1  (Section 3)
CR-2 (source-family semantics)        = 1  (Section 5)
CR-3 (MEC-13 restoration)             = 1  (Section 9)
CR-4 (DEDUP-06/ACT-01 wording)        = 1  (Section 7)
CR-5 (exposure readiness language)    = 1  (Section 8)
CR-6 (E10/segmentation separation)    = 1  (Section 11)
CR-7 (E8/E14/G_E audit-trail)         = 1  (Section 16)
CR-8 (ACT-05 five-way protocol)       = 1  (Section 14.4, completed this operation)

Before this operation: G_correction_closure = 0  (CR-8 was incomplete)
After this operation:  G_correction_closure = 1
```
Neither `G_E_original=1` nor `G_correction_closure=1` authorizes source
retrieval, portfolio-action execution, or any Git operation.

## 20. Final status boundary

```
HAWKES_V2_DIVERGENT_EVIDENCE_ACQUISITION_PLAN_COMPLETE_RETRIEVAL_REQUIRES_RESEARCHER_AUTHORIZATION
```
This does not authorize renewed Hawkes fitting, forecasting, visualization,
V2-B, ontology promotion, or causal inference.

**Pausing for researcher adjudication.** No staging, commit, push, or sync
performed.
