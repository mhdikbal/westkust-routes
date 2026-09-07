# HAWKES BASELINE V2 — DIVERGENT ONTOLOGY AND OBSERVATION REMEDIATION — MASTER REPORT (CORRECTED, CHECKPOINT 1C)

**Checkpoint 1C correction note:** this document is corrected per
`docs/CLAUDE_CHECKPOINT1_NARROW_CORRECTION_INSTRUCTION.md` (CR-1, CR-1b,
CR-3, CR-5, CR-6 below) following the read-only evidence audit conducted
under `docs/CLAUDE_CHECKPOINT1_EVIDENCE_AUDIT_AND_SUPPLEMENT_REQUEST.md`.
No new computation, fitting, or source retrieval was performed to produce
this correction — it repairs miscounts, a CSV-quoting defect, a denominator
label, a graph node-set omission, and an unstructured dialectic section in
the prior version. See Section 0 below for the full before/after ledger.

Governing instruction: `docs/CLAUDE_HAWKES_V2_DIVERGENT_ONTOLOGY_OBSERVATION_REMEDIATION.md`
Authoritative baseline: `f7b26bb`
Entry decision (unchanged by this operation): `CONTINUE_F3_REMEDIATION_INCOMPLETE`
Entry gate distribution (unchanged by this operation): `0 PASS / 1 FAIL / 9 NOT_EVALUABLE`

No Hawkes fitting, forecasting, simulation, bootstrap, calibration, or
visualization was performed. The 141-row corpus and frozen AS86 primary set
were read only, never modified. DEDUP-06 was not resolved. No git operation
(stage/commit/push/sync) was performed. This report is a reasoning-process
document, not a new evidentiary layer.

---

## 0. Checkpoint 1C correction ledger (before / after)

| ID | Item | Before (Checkpoint 1) | After (Checkpoint 1C) | File(s) touched |
|---|---|---|---|---|
| CR-1 | Unresolved-item denominator | `N_unresolved_items = 11` (miscounted) | `N_unresolved_items = 12`, confirmed by strict `csv` parsing of all substantive rows in the uncertainty ledger | This report only (ledger CSV itself was already correct at 12 rows) |
| CR-1b | Additional-edge count | "6 additional edges" (miscounted) | `N_minimum = 12`, `N_additional = 5`, `\|E_R\| = 17` (machine-counted) | This report only (dependency-graph CSV was already correct at 17 rows) |
| CR-2 | Mechanism-register CSV malformation | MEC-02, MEC-08, MEC-15 each parsed to 11 raw fields against a 10-column header (unquoted comma inside `identification_status`) | All 15 rows now parse to exactly 10 fields; substantive statuses unchanged | `HAWKES_BASELINE_V2_DIVERGENT_MECHANISM_REGISTER.csv` |
| CR-3 | Epistemic denominator shift | Reported as `P_typed = 15/15 = 1.00` without the `DENOMINATOR_SHIFT` label | Explicitly labeled `DENOMINATOR_SHIFT`; proposition-level coverage stated as `NOT_EVALUABLE` | This report only |
| CR-4 | DEDUP-06 matrix row order | `A, B, STOP_RULE_RESULT, C` | `A, B, C, STOP_RULE_RESULT` — content unchanged, DEDUP-06 not resolved | `HAWKES_BASELINE_V2_DEDUP06_ABDUCTIVE_MATRIX.csv` |
| CR-5 | Graph node-set specification gap | `G_reconsider` used as an edge target but absent from the documented node set | `G_reconsider` explicitly added to the documented node set (15 nodes total); labeled as correcting an inherited specification gap in the governing instruction, not new evidence | This report only |
| CR-6 | WP-D9 structured dialectic | Framing-circularity and ontology-scaffold challenges given in prose only | Both given full structured form (thesis/antithesis/favoring/disfavoring/rival/discriminating-observation); neither adjudicated closed | This report only |
| (unlisted, in-scope) | Additional CSV malformations found during Section 6 machine-parsing validation | `HAWKES_BASELINE_V2_EPISTEMIC_OBJECT_LEDGER.csv` (4 rows, unquoted commas in `scope_of_typing`/`dominant_epistemic_object_type`); `HAWKES_BASELINE_V2_DEDUP06_ABDUCTIVE_MATRIX.csv` (2 rows, unquoted comma inside the literal string `'Corpus III, nr. D'`); `HAWKES_BASELINE_V2_EXPOSURE_INFORMATION_REQUIREMENTS.csv` (1 row); `HAWKES_BASELINE_V2_COMPARATOR_PREREQUISITE_MAP.csv` (3 rows) — 10 malformed rows total across 4 files, none previously identified by name in either the evidence audit or the narrow-correction instruction | All 10 rows re-quoted; zero content changed; every one of the 8 CSVs among the ten outputs now parses to exactly its header's field count on every row (verified with Python's `csv` module) | `HAWKES_BASELINE_V2_EPISTEMIC_OBJECT_LEDGER.csv`, `HAWKES_BASELINE_V2_DEDUP06_ABDUCTIVE_MATRIX.csv`, `HAWKES_BASELINE_V2_EXPOSURE_INFORMATION_REQUIREMENTS.csv`, `HAWKES_BASELINE_V2_COMPARATOR_PREREQUISITE_MAP.csv` |

## 1. Protected state (restated, not re-derived)

```
Hawkes family        = EXPLORATORY_CANDIDATE, NOT_RULED_OUT
V2-A                  = MIXED_VALIDATION_RESULT
H-05                  = H05_NOT_EVALUABLE_REQUIRES_RESEARCHER_REVIEW
DEDUP-06              = UNRESOLVED (candidate B referent class = UNRESOLVED_REFERENT)
AS86                  = FROZEN_UNCHANGED
G_causal              = 0
G_ontology            = 0
G_reconsider_future   = 0
A_Hawkes_historical_fit = 0
A_Hawkes_visualization  = 0
A_V2B                   = 0
```

## 2. WP-D1 — Epistemic typing coverage

Full ledger: `HAWKES_BASELINE_V2_EPISTEMIC_OBJECT_LEDGER.csv`.

```
N_outputs_typed (bounded scope: the 15 existing deliverables, typed at
  file/row level as already structured by each file) = 15
N_outputs_assessed = 15
P_typed^(file-level) = 15/15 = 1.00 (at the file/row-level scope defined below)
```

**CR-3 correction (denominator shift, explicit):** the figure above is a
file/row-level coverage statistic, not the proposition-level estimand the
governing instruction's Section 3/4 define. The present ledger uses
deliverable-level units, and for four files (claim matrix, mechanism
register, model-future options, observation process register) their
pre-existing sub-file row units — never an atomic-proposition
segmentation. No atomic-proposition segmentation rule was prespecified in
this or any prior operation. Therefore:

```
P_type^(proposition) = N_propositions_typed / N_propositions_assessed = NOT_EVALUABLE
  (N_propositions_assessed is undefined; no segmentation rule exists)
```

This is `DENOMINATOR_SHIFT`, not a zero score and not a failed ontology —
the file/row-level figure above (1.00) remains accurate for the unit it
actually measures, and is reported alongside, not in place of, the
proposition-level `NOT_EVALUABLE`. No atomic propositions were invented
retrospectively to close this gap.

No file required a silent type promotion. Four files are `MIXED_LEDGER`
(claim matrix, mechanism register, model-future options, observation
process register) because they are themselves dialectical or multi-row
registers, not single-type documents — their existing per-row type columns
were preserved, not collapsed.

## 3. WP-D2 — Uncertainty-type distribution

Full ledger: `HAWKES_BASELINE_V2_UNCERTAINTY_TYPE_LEDGER.csv`.

```
N_unresolved_items = 12 (R-O1,2,3,5,6,7,8,9,10; R-O4_DEDUP06; G_sourcecrit; G_ontology_future)
  [CR-1 correction: the prior version of this report stated 11, an
   arithmetic miscount against its own listed item set, which already
   summed to 12. Confirmed by strict csv-module parsing of
   HAWKES_BASELINE_V2_UNCERTAINTY_TYPE_LEDGER.csv: 12 substantive rows,
   excluding header.]
N_vectorized = 12 (every row has a complete, non-blank U1-U12 vector; 0 missing)
P_uncertainty = N_vectorized / N_unresolved = 12/12 = 1.00
```

Distribution of dominant non-quantifiable types across the 12 items:

```
U5  ONTOLOGICAL_UNCERTAINTY                  : R-O1, R-O2, R-O3, R-O4/DEDUP-06, R-O6, G_ontology_future   (6)
U6  SOURCE_SURVIVAL_UNCERTAINTY              : R-O4/DEDUP-06, R-O8, R-O9                                   (3)
U7  SOURCE_ACCESS_UNCERTAINTY                : R-O8                                                        (1)
U8  SOURCE_INTENT_OR_CATEGORY_UNCERTAINTY    : R-O7, G_sourcecrit                                          (2)
U9  CODING_UNCERTAINTY                       : R-O1, R-O3, R-O4/DEDUP-06, R-O9                             (4)
U11 MECHANISM_UNDERDETERMINATION             : R-O2, R-O3, R-O4/DEDUP-06, R-O10, G_ontology_future         (5)
U12 GOVERNANCE_OR_DECISION_RULE_UNCERTAINTY  : G_sourcecrit                                                 (1)
```

Only one item (R-O5) has a presumptively quantifiable component (`U4`),
and only conditionally — the parsing-rule step that would make it
quantifiable is deliberately deferred, not completed. `G_i^quant=0` for
every other item; no probability distribution was assigned anywhere in
this operation to U5/U6/U8/U10/U11/U12-typed uncertainty.

## 4. WP-D3 — R-O dependency graph and cycles

**CR-5 correction (node-set specification gap):** the governing
divergent-remediation instruction's Section 5 declares
`V_R = {R-O1..R-O10, G_sourcecrit, G_ontology, G_observation, G_comparator}`
but its own minimum edge list requires `G_reconsider` as an edge target
twice, without ever declaring it in `V_R`. This is an inherited
specification gap in the governing instruction itself, not new scientific
evidence produced by this operation. It is corrected here by explicit
declaration:

```
V_R (corrected, complete node set, 15 nodes) =
  { R-O1, R-O2, R-O3, R-O4, R-O5, R-O6, R-O7, R-O8, R-O9, R-O10,
    G_sourcecrit, G_ontology, G_observation, G_comparator, G_reconsider }
```

`G_observation` and `G_comparator` remain isolated (0 in-degree, 0
out-degree) under the minimum + additional edge sets below; this is
recorded as an explicit incompleteness of the minimum specification, not
silently resolved by inventing edges for them.

Full edge list: `HAWKES_BASELINE_V2_RO_DEPENDENCY_GRAPH.csv`.

```
N_minimum = 12 instruction-minimum edges
N_additional = 5 additional edges grounded in existing repository artifacts
|E_R| = 17 total
  [CR-1b correction: the prior version of this report stated "6 additional
   edges." Machine count (csv rows minus header) is 5 additional edges;
   17 total is unchanged and was already correct.]
```

```
In-degree (instruction-minimum edges only):
  R-O1  = 4  (from R-O2, R-O3, R-O4, R-O5)
  R-O10 = 4  (from R-O1, R-O5, R-O8, R-O9)
  R-O6  = 1, R-O9 = 1, G_reconsider = 2
  all others = 0

In-degree (including additional grounded edges, independently re-verified
by DFS and by direct edge-count with Python's csv module):
  R-O1 = 4, R-O10 = 4 (CONFIRMED unchanged — no additional edge targets
                        either node)
  R-O7 = 2, R-O3 = 1, R-O2 = 1, R-O6 = 1, R-O9 = 1, G_reconsider = 3
  G_observation = 0, G_comparator = 0
```

**Bottlenecks (not importance):** R-O1 and R-O10 are tied for highest
in-degree under both edge sets. Per the governing instruction, this is read
only as "most remediation paths pass through these two nodes," not as a
claim that event-unit ontology or comparator feasibility is historically
more important than the others.

**Cycles:** none detected in either edge set, independently re-verified by
two methods (DFS with white/gray/black back-edge detection, and Kahn's
topological-sort algorithm — both return a full 15/15-node ordering,
confirming a DAG). The graph as constructed is acyclic; this is reported as
a fact about the graph as built in this operation, not a claim that no
feedback exists in principle between, e.g., R-O3 (episode membership) and
R-O4 (dedup cleanliness) — the added `R-O4 -> R-O3` edge already captures
that specific directional dependency without closing a cycle back to R-O4.

## 5. WP-D4 — Divergent mechanism register

Full register: `HAWKES_BASELINE_V2_DIVERGENT_MECHANISM_REGISTER.csv`, 15
entries (MEC-01 through MEC-15), mapped against the prior A1–A12 register
with two new entries (MEC-13 administrative-period effects, MEC-14
editorial compilation effects) and one explicit closure-prevention
placeholder (MEC-15).

**CR-2 correction (CSV malformation repaired):** the prior version of this
file had unquoted commas inside the `identification_status` field for
MEC-02, MEC-08, and MEC-15, causing each of those three rows to parse to 11
raw fields against the 10-column header — `current_status` and
`legacy_cross_reference` were consequently misaligned for those three rows
under strict machine parsing. The three fields have been re-quoted; no
substantive status was changed by the repair. Verified by Python's `csv`
module: all 15 rows now parse to exactly 10 fields.

```
G_CSV = 1[N_malformed=0 AND N_columns,row=10 for all rows] = 1[0=0 AND True] = 1
```

```
Status distribution (live/open indicator in parentheses):
  SUPPORTED_FOR_CORPUS             : MEC-02, MEC-09, MEC-11, MEC-12          (4, all LIVE)
  PARTIALLY_SUPPORTED_FOR_CORPUS   : MEC-01, MEC-05, MEC-06, MEC-07, MEC-08  (5, all LIVE)
  PLAUSIBLE_MODEL_RISK             : MEC-13, MEC-14                          (2, all LIVE)
  NOT_TESTABLE                     : MEC-03, MEC-04, MEC-10                  (3, all NONLIVE)
  NOT_SUPPORTED                    : MEC-15                                  (1, NONLIVE)

N_live    = 4 + 5 + 2 = 11
N_nonlive = 3 + 1     = 4
N_mechanisms = N_live + N_nonlive = 11 + 4 = 15   -- identity confirmed, mutually
  exclusive and exhaustive status accounting.
```

MEC-15 is explicitly recorded `NOT_SUPPORTED` and `NONLIVE` (a
closure-prevention placeholder, not a substantive hypothesis) — this
reconciles the prior version's ambiguous phrasing ("11 live mechanisms
(MEC-01…14 minus 3 structurally NOT_TESTABLE)"), which left MEC-15
unaccounted for in that sentence even though the ledger itself already
recorded it correctly. The eleven-live-mechanism set is otherwise preserved
unchanged; no other inconsistency was found in this correction pass.

No mechanism reached `SUPPORTED_FOR_CORPUS` on synthetic evidence alone —
every `SUPPORTED_FOR_CORPUS` entry cites corpus-historical or in-corpus
repository evidence, consistent with the synthetic-promotion ceiling
(`PLAUSIBLE_MODEL_RISK` maximum for synthetic-only evidence).

For observation `y` = "the corpus shows temporal concentration of coded
events," the live mechanism set is `|M_y| = {MEC-01, MEC-02, MEC-05,
MEC-06, MEC-07, MEC-08, MEC-09, MEC-11, MEC-12, MEC-13, MEC-14}` — 11
live, non-excluded alternatives. `MEC-03/MEC-04/MEC-10` are `NOT_TESTABLE`
(structurally, not evidentially, excluded); `MEC-15` is a placeholder.
With 11 live alternatives and no comparator architecture built to
discriminate between them, this observation cannot currently converge on
one mechanism (Section 17 stop-rule; see Section 9 below).

## 6. WP-D5 — DEDUP-06 abductive result

Full matrix: `HAWKES_BASELINE_V2_DEDUP06_ABDUCTIVE_MATRIX.csv`. Three live
hypotheses (H-DEDUP06-A same-event corroboration, H-DEDUP06-B second
uncoded event, H-DEDUP06-C citation/editorial artifact only). For all
three, the one discriminating observation identified (direct retrieval and
reading of the "Corpus III, nr. D" source location) does not currently
exist in-repository, and this operation is not authorized to perform new
source retrieval (Section 18).

**CR-4 correction (row order):** the prior version of this file ordered its
rows `A, B, STOP_RULE_RESULT, C` (an artifact of an in-place edit). Rows
are now ordered `A, B, C, STOP_RULE_RESULT` — content of every row is
unchanged, and DEDUP-06 remains unresolved.

```
G_c^converge (DEDUP-06) = 0   (|M_c^live|=3 != 1, and D_c^available-and-observed=0)
DECISION_STATUS = RETAIN_AS_OPEN
```

Permitted conclusion only:
`PRIMARY_SET_MEMBERSHIP_IS_EPISTEMICALLY_CONTAMINATED_BY_ONE_UNRESOLVED_DEDUP_CASE`.
No inference is drawn that the referent is a second event, a duplicate, or
that exactly one historical occurrence exists.

## 7. WP-D6 — Exposure information requirements

Full map: `HAWKES_BASELINE_V2_EXPOSURE_INFORMATION_REQUIREMENTS.csv`.

```
N_candidates_defined = 6
N_assessed = 2 (both ASSESSED_CIRCULAR_PROHIBITED_AS_MODEL_INPUT)
N_open_information_requirement = 4
```

Both assessed candidates remain restricted to `DESCRIPTIVE_USE =
ALLOWED_WITH_LIMITATIONS`; `MODEL_OFFSET_USE`, `MODEL_COVARIATE_USE`, and
`CAUSAL_ADJUSTMENT_USE` are `PROHIBITED` for both. No circular exposure
candidate was promoted to a model role anywhere in this operation
(`D6` gate, Section 11 below).

## 8. WP-D7 — Comparator prerequisite map

Full map: `HAWKES_BASELINE_V2_COMPARATOR_PREREQUISITE_MAP.csv`.

```
M1: R_m^now = 0  (O=0, T=0, E=0, I=0; only P=1)
M3: R_m^now = 0  (same profile, plus one additional uncharacterized
                   mu(t)-vs-kernel identifiability tradeoff)
G_RO10_now = 0, G_RO10_conditional = 1  (restated, not changed)
```

`FEASIBLE_CONDITIONALLY` status (formula specified, inputs exist) is kept
explicitly distinct from `R_m^now=1` readiness throughout this map.
Forecasting performance was not used anywhere to substitute for an unmet
readiness condition.

## 9. WP-D9 — Red-team / blue-team challenge of F3 continuation

**Claim under test:** the decision to continue F3 (suspend Hawkes pending
ontology/observation remediation) rather than move to
`HAWKES_RECONSIDERATION_REVIEW_READY_NOT_AUTHORIZED`,
`RETIRE_HAWKES_FROM_CURRENT_CORPUS_RECOMMENDED`, or
`REQUIRES_RESEARCHER_REVIEW`.

**Blue team (strongest case for continuing F3 as currently scoped):**
The gate matrix is unambiguous at 0 PASS / 1 FAIL / 9 NOT_EVALUABLE; the
one FAIL (R-O4/DEDUP-06) is a demonstrated contradiction, not a close call;
none of the nine NOT_EVALUABLE items are contested judgment calls — each
traces to a concrete, named schema gap (no atomic report ID, no source-term
column, no external exposure ledger, no actor/outcome columns) or an
explicit current/conditional distinction (R-O10). This is not a borderline
case warranting `REQUIRES_RESEARCHER_REVIEW`, and nothing in this operation
constitutes a positive falsification warranting retirement. Continuing F3
with a now-more-structured divergent backlog (this operation's WP-D1–D8
outputs) is the most honest available label.

**Red team (strongest challenge):**
1. *Category error risk:* treating "9 of 10 NOT_EVALUABLE" as self-evidently
   meaning "dominated by unresolved ontology" (Section 1 of the governing
   instruction) risks circularity — the instruction that commissioned this
   operation already assumed that interpretation before this operation
   tested it. This report does not independently verify that ontology
   remediation (rather than, e.g., simple schema extension effort) is the
   binding constraint; it restates the instruction's framing.
2. *Evidence leakage:* several `SUPPORTED_FOR_CORPUS` mechanism entries
   (MEC-02, MEC-09, MEC-11) draw on the same underlying memory records
   (`project_markov_hawkes_models`) cited repeatedly across this whole
   multi-session workstream — apparent convergence across documents may
   partly reflect shared-source reuse rather than independent
   corroboration.
3. *Denominator shift:* R-O1's two figures (84.4% metadata availability vs.
   `NOT_COMPUTABLE` original construct) use different, non-comparable
   denominators in spirit even though both nominally divide by 141; a
   reader skimming only the percentage risks the exact shortcut Section 2
   item 7 prohibits.
4. *Hidden ontology assumption:* the five-process decomposition `H,O,S,A,C`
   (causal-ontology-boundary document) is itself this project's own
   analytic scaffold, not verified against an independent historiographic
   framework for VOC-era archival epistemology — it could be missing a
   sixth process or conflating two of the five.
5. *Post hoc rule risk:* SR-01 through SR-04 (prior operation's semantic
   corrections) were all applied reactively, after an initial version
   overstated readiness — a pattern of correction-after-the-fact that,
   while transparently documented, warrants continued scrutiny of whether
   this operation's own new constructs (the dependency graph, the MEC-13/14
   additions) will survive a similar future correction pass.

**CR-6 correction — structured form for the two unresolved challenges**
(added; neither is adjudicated closed by adding structure):

| | Challenge 1: framing circularity | Challenge 2: unverified ontology scaffold |
|---|---|---|
| Thesis | "9 of 10 `NOT_EVALUABLE`" self-evidently means "dominated by unresolved ontology" (Section 1 of the governing instruction) | The `H,O,S,A,C` five-process decomposition (`HAWKES_BASELINE_V2_CAUSAL_ONTOLOGY_BOUNDARY.md`) correctly captures the relevant observation-process structure |
| Antithesis | The governing instruction assumed this interpretation before this operation tested it; this operation restates rather than independently verifies the framing | The decomposition is this project's own analytic scaffold, never checked against an external historiographic/archival-science framework |
| Favoring evidence | The gate matrix's own concrete, named schema gaps (no atomic report ID, no source-term column, no external exposure ledger, no actor/outcome columns) are consistent with an ontology-dominated reading | The decomposition has been used consistently and without internal contradiction across multiple sessions and documents in this workstream |
| Disfavoring evidence | An alternative framing (e.g. "dominated by unresolved data-collection scope," not ontology per se) has never been tested against the same evidence | No independent second framework was ever consulted to check for a missing or conflated process |
| Rival explanation | Simple schema-extension effort (R-O2's atomic report_id table, R-O6's actor/outcome columns), not deep ontological remediation, could resolve several `NOT_EVALUABLE` items without touching the harder R-O1/R-O9/R-O10 cluster | A sixth process, or a merge of two of the five, could be equally defensible without any of this project's existing evidence distinguishing between them |
| Discriminating observation | Whether R-O2/R-O6 resolve via straightforward schema extension without requiring R-O1/R-O9/R-O10 to move | Independent review by a historian/archivist specializing in VOC-era archival epistemology |
| Observation currently exists? | NO — not attempted in this or the audit operation | NO |

Neither team cited the other team's conclusion as evidence in constructing
either challenge above.

**Synthesis:** The red-team challenges do not overturn the blue-team case,
but they are not resolved by it either. Challenge 1 (circularity of
framing) and challenge 4 (unverified ontology scaffold) remain genuinely
open — this operation cannot adjudicate them from repository evidence
alone, since doing so would require independent historiographic or
archival-science input not available in this corpus. Per the Section 17
stop-rule, this is recorded as `RETAIN_AS_OPEN` rather than resolved in
either direction: continuing F3 is the decision under the evidence as
structured, while acknowledging the structuring itself has not been
independently audited.

```
False-convergence check for this synthesis:
  |M_c^live| = 2 (the red-team framing-circularity challenge remains live
                  alongside the blue-team case) -> G_c^converge = 0
  DECISION_STATUS (for the framing question itself) = RETAIN_AS_OPEN
  DECISION_STATUS (for the F3-vs-alternatives decision) = CONTINUE_F3
    -- this is NOT a convergence on a contested mechanism claim; it is a
       governance choice under Section 15's robust-decision logic, which
       does not require G_c^converge=1 to select an action.
```

## 10. WP-D10 — Revised remediation backlog with discriminating-evidence actions

| Item | Concrete action | Discriminates between | Currently available? |
|---|---|---|---|
| R-O1 | Resolve 22 blank/unknown `event_date_precision` rows via source cross-check | EVENT_METADATA_MINIMUM_AVAILABILITY vs. true event-unit readiness | NO — requires source-text access |
| R-O2 | Design and populate an atomic per-document `report_id` table | MEC-06 (duplicate reports) vs. MEC-01 (genuine excitation) | NO — schema-extension task |
| R-O3 | Add source/audit locator + explicit assignment rule to `parent_episode_id` | MEC-07 (episode fragmentation) vs. MEC-01 | NO — requires source-text rereading |
| R-O4/DEDUP-06 | Retrieve and read "Corpus III, nr. D" | H-DEDUP06-A vs. -B vs. -C | NO — source retrieval outside this operation's authorization |
| R-O5 | Construct researcher-reviewed `L_i/U_i` interval bounds per precision class | MEC-08 (date heaping) kernel-shape claim vs. MEC-01 | PARTIALLY — parsing rule design is in-repository work, not new source access |
| R-O6 | Extend schema with actor-role/outcome columns | MEC-10 (event-type heterogeneity) vs. MEC-11 (already partly shown) | NO — requires source rereading |
| R-O7 | Extract literal source-language terms per `event_type` | G_sourcecrit unmarked-colonial-category risk | NO — requires source-text access |
| R-O8 | Systematic `source_chain_to_primary` audit (R_access only; R_record/R_survival likely permanently NOT_EVALUABLE) | MEC-03 (recording-density) vs. MEC-04 (survival/access), partially | PARTIALLY — audit is in-repository, structural ceiling remains |
| R-O9 | Search for an external, non-circular exposure ledger (4 open candidate types) | MEC-05 (reporting bursts) vs. MEC-01 | NO — requires external archival-ledger access |
| R-O10 | No independent remediation path — inherits R-O1, R-O5, R-O6, R-O9 | — | Derived, not separately actionable |

Every "NO" row above is recorded as an information requirement for a later,
separately authorized operation, per Section 18 of the governing
instruction — none is begun here.

## 11. Gates (Section 20), recomputed post-correction

| Gate | Value | Evidence |
|---|---|---|
| D0 (zero unauthorized execution) | **1** | `git diff --name-only HEAD` = 0 lines; `git diff --cached` empty; no fitting/staging/commit/push tool call in this or the prior two operations |
| D1 (all material propositions typed) | **NOT_EVALUABLE** | Per CR-3 (Section 2 above): no atomic-proposition segmentation rule was ever prespecified, and this correction pass does not invent one retrospectively (prohibited by the governing narrow-correction instruction, Section 4). Preserved as `NOT_EVALUABLE`, not forced to 1. |
| D2 (all unresolved blockers uncertainty-typed) | **1** | Corrected denominator N=12 (CR-1); 12/12 vectorized, 0 missing (Section 3 above) |
| D3 (dependency graph complete) | **1** | 17 edges (12 minimum + 5 additional, CR-1b), 0 cycles, independently re-verified by two algorithms (Section 4 above) |
| D4 (alternative mechanisms recorded) | **1** | Now demonstrably satisfied after CR-2 structural repair (`G_CSV=1`, all 15 rows parse to exactly 10 fields) and CR-2 status accounting (11 live + 4 nonlive = 15, identity confirmed, MEC-15 explicitly reconciled) — Section 5 above |
| D5 (DEDUP-06 not overresolved) | **1** | 3 hypotheses retained open, `RETAIN_AS_OPEN` preserved; only row order changed (CR-4) |
| D6 (circular exposure not promoted) | **1** | Unchanged from Checkpoint 1 — both assessed candidates remain `PROHIBITED` for offset/covariate/causal use |
| D7 (comparator readiness not inferred from implementability) | **1** | Unchanged — `R_m^now=0` for M1/M3, `FEASIBLE_CONDITIONALLY` kept distinct |
| D8 (causal and ontology gates remain zero) | **1** | `G_causal=0`, `G_ontology=0` restated, no tracked file changed |
| D9 (red-team contradictions retained) | **1** | Retained open; now in full structured form per CR-6 (Section 9 above) |
| D10 (false-convergence count zero) | **1** | Recomputed in Section 12 below; `N_false-convergence=0` |

```
G_divergent = 1[D0=D1=...=D10=1]
```
Because `D1 = NOT_EVALUABLE`, the strict conjunction cannot be asserted `=1`:

```
G_divergent = NOT_EVALUABLE
```

This is unchanged from the evidence-audit finding and is *not* an
adjudication failure — it is the correct, honest value given that
proposition-level typing was never attempted and this correction pass is
explicitly prohibited from inventing propositions retrospectively to force
`D1=1`.

Regardless of `G_divergent`'s value, the following remain true and are
restated per the governing instruction:
```
G_divergent = NOT_EVALUABLE (or 1)  ⇏  G_ontology = 1            (G_ontology = 0, unaffected)
G_divergent = NOT_EVALUABLE (or 1)  ⇏  G_causal = 1              (G_causal = 0, unaffected)
G_divergent = NOT_EVALUABLE (or 1)  ⇏  G_reconsider_future = 1   (G_reconsider_future = 0, unaffected)
```

## 12. False-convergence count, recomputed per-claim

Material claims with `DECISION_c ∈ {ADOPT, REJECT}` in
`HAWKES_BASELINE_V2_DIALECTICAL_CLAIM_MATRIX.csv`: C1, C2, C3, C4, C8, C9
(decisions `REJECT, REJECT, REJECT, ADOPT, REJECT, REJECT`); C11
(`REJECT_AS_CURRENT_ROLE`) is a distinct label, listed for completeness.

| claim | decision | `G_c^conv` | basis |
|---|---|---|---|
| C1 | REJECT | 1 | `D_available=1 ∧ D_decisive=1` — gate-matrix distribution (0 PASS/1 FAIL/9 NOT_EVALUABLE) is a settled repository fact, not a mechanism pick among live rivals |
| C2 | REJECT | 1 | H-05/coverage figures settled by repository fact |
| C3 | REJECT | 1 | Prior `RESEARCHER_DECISION`, not reopened |
| C4 | ADOPT | 1 | `\|M_c^live\|=1` — no live rival *mechanism* disputes materiality of a nonstationary baseline, only an estimation-power caveat |
| C8 | REJECT | 1 | Governing artifact (`HAWKES_BASELINE_V2A_H05_GOVERNANCE_AMENDMENT_PROPOSAL.md`) forecloses the reading directly |
| C9 | REJECT | 1 | `G_causal=0`, frozen across every session in this workstream |
| C11 | REJECT_AS_CURRENT_ROLE | 1 | Epistemic-safety argument settled by repository fact (`N_corpus(t) != H(t)` prohibition) |

```
N_false_convergence = Σ 1[DECISION_c ∈ {ADOPT,REJECT} ∧ G_c^conv=0] = 0
```

Also checked (not counted in the sum above, since none carries an
ADOPT/REJECT decision): the 11 live mechanisms under WP-D4 (retained open,
no forced selection); the 3 DEDUP-06 hypotheses (retained open,
`RETAIN_AS_OPEN`); the WP-D9 framing-circularity and ontology-scaffold
challenges (both retained open under `RETAIN_AS_OPEN`, per Section 9's
`G_c^converge=0` finding). **Required value `N_false_convergence=0` is
met.**

## 13. Ten required outputs and hashes

See `HAWKES_BASELINE_V2_DIVERGENT_REPRODUCIBILITY_MANIFEST.csv` for the
exact ten paths and SHA-256 hashes, computed after all ten files were
finalized.

## 14. Unchanged status (restated)

```
F3 decision           = UNCHANGED (CONTINUE_F3_REMEDIATION_INCOMPLETE)
G_reconsider_future    = UNCHANGED (0)
Hawkes family          = UNCHANGED (EXPLORATORY_CANDIDATE, NOT_RULED_OUT)
V2-A                   = UNCHANGED (MIXED_VALIDATION_RESULT)
```

## 15. Proposed next information-gathering actions

In priority order by dependency-graph bottleneck position (Section 4),
not by assumed historical importance:

1. Resolve DEDUP-06 via direct retrieval of "Corpus III, nr. D" (unblocks
   R-O4's unresolved referent and removes the sole FAIL from the gate
   matrix) — requires a separate source-access authorization.
2. Design the R-O5 interval-bound parsing rule (the one presumptively
   quantifiable R-O item) and bring it to researcher review before
   construction.
3. Scope a targeted source-text extraction pass for R-O7 (colonial
   category mapping) using the same filter-and-validate method already
   proven on `pelabuhan_disebut` (MEC-12 precedent).
4. Search named-institution catalogues for at least one of the four
   unassessed external exposure-candidate types (R-O9).
5. Only after 1–4: reassess R-O1/R-O2/R-O3/R-O6/R-O10 jointly, since none
   of them has an independent remediation path separate from source-text
   re-extraction work.

## 16. Checkpoint 1C decision

Per the narrow-correction instruction's Section 7 item 11, the
recommendation is limited to `REQUIRES_RESEARCHER_REVIEW` unless every
governing requirement is demonstrably satisfied. `G_divergent = NOT_EVALUABLE`
(Section 11 above), because `D1` remains `NOT_EVALUABLE` by design (no
proposition-level segmentation rule exists, and none may be invented
retrospectively). Every other gate (`D0, D2–D10`) is now `1`, including
`D4` which moved from an unverifiable claim to a demonstrably satisfied
gate after CR-2's structural repair. This is a real, substantial
improvement over the Checkpoint 1 evidence-audit state (which had two
`NOT_EVALUABLE` gates, `D1` and `D4`) — but it does not close the strict
conjunction, so:

```
CONTINUE_F3_WITH_DIVERGENT_REMEDIATION_BACKLOG   -- NOT selected (G_divergent != 1)
REQUIRES_RESEARCHER_REVIEW                       -- SELECTED
```

The frozen scientific and governance state (`F3`, `V2-A`, `H-05`,
`DEDUP-06`, `G_causal`, `G_ontology`, `AS86`) is unaffected by this
correction pass and remains exactly as adjudicated at the start of Section
1 of the narrow-correction instruction.

Final state (Section 25 of the original divergent-remediation instruction):

```
HAWKES_F3_DIVERGENT_REMEDIATION_REQUIRES_RESEARCHER_REVIEW
```

**Pausing for researcher adjudication.** No staging, commit, push, or
server-sync performed. The information-gathering backlog (Section 10
above) is not begun.
