# HAWKES V2 — WAVE 3A: PROSPECTIVE GRANULARITY RULE, PARENT-EPISODE RULE, NON-MUTATING TEST, AND ACT-07 DESIGN

```
Authoritative HEAD (unchanged throughout) = 3184e14e8183f9a93a34496f0bf3e4ebea568e58
Operation date (UTC) = 2026-09-09
Wave 1 and Wave 2 are not reopened or edited by this operation.
```

## 0. Revision note (2026-09-09) — researcher adjudication

The original Wave 3A package is accepted as a useful design draft but was
**not** accepted as an operational prospective rule. Researcher decisions:

```
GRANULARITY_RULE_DECISION              = REVISE_PROSPECTIVELY
PARENT_EPISODE_RULE_DECISION           = REVISE_PROSPECTIVELY
ACT07_EXECUTION_DECISION               = DEFER
TEST03_EPISODE_AUDIT                   = DEFER_PENDING_ACCEPTED_RULE
MULTI_SOURCE_VERIFIED_PROJECT_WIDE_REVIEW = REQUIRED_BUT_NOT_EXECUTED
```
`REVISE_PROSPECTIVELY` is not rejection of the design — the successful
uncertainty-retention behavior (all five original cases correctly avoided
premature closure) is preserved below, alongside a genuine operational
extension (Sections 0.1–0.5) that separates evidence from authorization and
adds three further non-mutating stress tests.

### 0.1 Four-state component logic (replaces binary 0/1)

Each `Γ_i` component now takes:
```
X_ik ∈ {SATISFIED, FAILED, CONFLICTING, NOT_EVALUABLE}
```
A component is never reduced to binary zero when its true state is
`CONFLICTING` or `NOT_EVALUABLE` — STRESS-02 below is the clearest
demonstration of why this distinction matters.

### 0.2 Evidence gates, separated from authorization

```
G_sep,ij^evidence    = 1[I_i≠I_j ∧ P_i=P_j=1 ∧ (A_i≠A_j ∨ J_i≠J_j) ∧ T_i,T_j,S_i,S_j explicitly assessed]
G_parent,ij^evidence = 1[G_sep,ij^evidence=1 ∧ T_ij=1 ∧ S_ij=1 ∧ K_ij=1 ∧ H_ij=1 ∧ P_ij=1]
G_single,ij^evidence = 1[I_i=I_j ∧ A_i=A_j ∧ J_i=J_j ∧ T_i=T_j ∧ S_i=S_j ∧ P_i=P_j=1 ∧ X_distinct=0]

G_sep,ij^authorized    = G_sep,ij^evidence    × A_gran
G_parent,ij^authorized = G_parent,ij^evidence × A_parent
G_single,ij^authorized = G_single,ij^evidence × A_gran

A_gran = A_parent = 0 throughout this revision — no corpus action is
authorized even where an evidence gate equals 1.
```

**Decision output, per case, now reports two separate fields:**
```
EVIDENCE_CLASSIFICATION ∈ {EVIDENCE_SUPPORTS_SEPARATE_CHILDREN,
  EVIDENCE_SUPPORTS_SEPARATE_CHILDREN_SHARED_PARENT,
  EVIDENCE_SUPPORTS_SINGLE_EVENT, EVIDENCE_UNRESOLVED}
AUTHORIZED_CORPUS_ACTION = NO_CORPUS_ACTION_AUTHORIZED   (always, this revision)
```
This separation exists precisely so that a case is not forced to
`EVIDENCE_UNRESOLVED` merely because researcher acceptance is pending — see
STRESS-03 below, the one case where evidence and authorization now visibly
diverge.

### 0.3 Original five cases — re-expressed, evidence unchanged

TEST-01 through TEST-05's underlying evidence is **not re-derived**. Under
the four-state/evidence-authorization framing:
```
TEST-01  EVIDENCE_UNRESOLVED   (I_CodedRow=FAILED, A_CodedRow=FAILED; G_split,^evidence blocked on missing R_split acceptance test, not an evidence gap)
TEST-02  EVIDENCE_UNRESOLVED   (A,J genuinely differ Vogel vs EIC letter — same finding, now labeled EVIDENCE_UNRESOLVED rather than UNRESOLVED_GRANULARITY)
TEST-03  EVIDENCE_UNRESOLVED   (rule_e=FAILED for all 7 members; provenance_e=CONFLICTING, not simply 0 — the ledger's own "mechanically derived" note is itself conflicting evidence about whether provenance is source-grounded)
TEST-04  EVIDENCE_UNRESOLVED   (T_i=CONFLICTING — dispatch-date and event-date are both attested, in genuine conflict, not merely absent)
TEST-05  EVIDENCE_UNRESOLVED   (I_i=NOT_EVALUABLE — no CD6 folio located; four-state NOT_EVALUABLE, never FAILED, per the non-absence-of-evidence principle)
```
All five: `AUTHORIZED_CORPUS_ACTION = NO_CORPUS_ACTION_AUTHORIZED`.

### 0.4 Stress-test amendment (N_stress = 3, N_all = 8)

Full pre-application selection provenance, evidence application, and all
required disclosures (actor normalization, colonial-category audit,
selection-risk statements) are in
`HAWKES_V2_GRANULARITY_RULE_NONMUTATING_TEST_LEDGER.csv`, rows STRESS-01
through STRESS-03. Summary:

```
STRESS-01 = EVIDENCE_UNRESOLVED
  Selected via query: provenance_status=MULTI_SOURCE_VERIFIED, excluding
  TEST-02's event -- 2 results; Cingkuak (this case) chosen because its 3
  sources agree exactly on date (Padang's differ by 1 day).
  FORMAL RULE DEFECT recorded: G_single,ij requires I_i=I_j; independent
  reports of one occurrence normally have I_i≠I_j by construction, so
  G_single cannot affirm a single occurrence across distinct reports no
  matter how well they agree.
  G_single_cross_report = NOT_EVALUABLE_PENDING_REVISED_REPORT_TO_OCCURRENCE_MAPPING_RULE
  -- NOT silently repaired in this write. The Cingkuak reports are NOT
  classified as one occurrence merely because the three dates agree.
  STRESS01_SELECTION_RISK = TARGET_CONGRUENT_SELECTION_DISCLOSED
  STRESS01_INDEPENDENT_VALIDATION_VALUE = LIMITED
  This is NOT a blind test and NOT independent confirmation of a
  single-event rule.

STRESS-02 = EVIDENCE_UNRESOLVED
  Selected via query: rule_explicit_R_i=1 across all 141
  PARENT_EPISODE_MEMBERSHIP.csv rows -- ZERO results; and STANDALONE_EVENT
  rows with possible_shared_parent_episode_note_present=YES -- ZERO
  results. Fell back to the sole DISTINCT_HISTORICAL_EVENTS verdict in
  HAWKES_BASELINE_V2_DEDUP_ADJUDICATION.csv (DEDUP-02).
  I_Pouti = NOT_EVALUABLE, not FAILED -- the Pouti execution has a source
  locator (docs/bsb10468472.txt) but no independent corpus event_id or
  granularity vector of its own. Absence of an independent corpus object is
  NOT treated as evidence that no distinct occurrence existed.

STRESS-03 = EVIDENCE_SUPPORTS_SEPARATE_CHILDREN_SHARED_PARENT
  Selected as the pair from the same MULTI_SOURCE_VERIFIED query (Cingkuak +
  Padang, both parent_episode_id=EP-1781-EIC-CAPTURE-PADANG-WESTKUST).
  G_sep,ij^evidence=1 and G_parent,ij^evidence=1 -- K_ij grounded directly in
  Botham's own primary letter ("Since the Capture of Padang I have taken
  Possession of its Subordinates..."). THE SOLE non-unresolved evidence
  classification among all 8 cases. Support is limited to documentary and
  episode mapping only -- NOT promoted to a validated universal
  parent-episode rule, an authorized corpus grouping, causal continuity, or
  permission to mutate parent_episode_id.

  Actor normalization (required disclosure):
    diplomatic form            = the exact form in Botham's primary letter (Governor unnamed in the quoted excerpt)
    normalized form             = "Heerskerch"
    normalized-form source      = Kathirithamby 1965 secondary thesis, p.314
    primary-document cross-verification = NOT_AVAILABLE
    collision risk               = UNRESOLVED
    alternative readings         = RETAINED
  The secondary normalized form is NOT used as an authoritative actor identity.

  Colonial-category finding (required disclosure):
    event_type = "konflik"  ->  category class = PROJECT_NORMALIZED_LABEL
    Botham's primary text uses "surrender", "summoned", "expedition" --
    never "konflik". "Konflik" is NOT promoted into a source-native term or
    a neutral historical ontology.
```

### 0.5 Revised estimands

```
N_original = 5, N_stress = 3, N_all = 8

P_unresolved^original = 5/5 = 1

P_evidence_applicable = N_{non-EVIDENCE_UNRESOLVED} / N_all = 1/8 = 0.125
  (numerator: STRESS-03 only)

P_authorized_action = 0 / N_all = 0/8 = 0   (required, and preserved)

P_open = N_{insufficient-evidence cases correctly EVIDENCE_UNRESOLVED} / N_{insufficient-evidence cases}
       = 2/2 = 1
  (denominator: TEST-05 and STRESS-02, the two cases whose blocking
  component is NOT_EVALUABLE due to a missing/unestablished documentary
  object, not a resolved conflict)

N_unsupported = Σ_k 1[E_k≠EVIDENCE_UNRESOLVED ∧ G_k^evidence=0] = 0
  (the only non-unresolved case, STRESS-03, has G_parent,ij^evidence=1 --
  fully evidence-supported)

G_demonstration = 1[N_{nonunresolved evidence classes}≥1(=1) ∧ N_{unresolved preserved}≥1(=7) ∧ N_unsupported=0] = 1
```
**`G_demonstration = 1` is qualified as `LIMITED_OPERATIONAL_DEMONSTRATION`.**
It shows only that the revised framework CAN produce at least one
non-unresolved evidence classification while preserving at least one
unresolved case and producing no unsupported decisive classification.

**`G_demonstration = 1` does NOT imply:**
```
G_gran_accepted = 1
G_parent_accepted = 1
G_ontology = 1
G_causal = 1
G_reconsider_future = 1
CORPUS_MUTATION_AUTHORIZED
```

`OVERFIT_TO_DEDUP06_EXAMPLE = PARTIAL_MITIGATION_NOT_PROOF` — **preserved,
not promoted to PASS.** The expanded evidence (one rule defect exposed in
STRESS-01, one disclosed selection-risk in STRESS-01, one honest
NOT_EVALUABLE in STRESS-02, one genuine positive finding in STRESS-03) does
not justify a more permissive status either.

## 0-B. Wave 3B revision (2026-09-09) — corrected report-to-occurrence gate and final holdout audit

This is the final planned methodology stress-test pass. `G_demonstration=1`
from Wave 3B remains `LIMITED_OPERATIONAL_DEMONSTRATION` — this revision is
accepted as demonstrating corrected rule *behavior*, not as an accepted
granularity or parent-episode rule.

### 0-B.1 Formal correction

The original `G_single,ij` required documentary identity (`I_i=I_j`),
which independent reports of one occurrence normally never satisfy. This is
replaced by two separated levels:
```
I_r^doc = (source, document, locator, reporting context)   -- documentary identity, per report
Omega_ij = (A_ij, J_ij, T_ij, S_ij, X_ij, D_ij, P_ij)       -- report-to-occurrence compatibility
  A: actor-set compatibility        J: act/process compatibility
  T: event-time compatibility (post date-role separation)   S: spatial compatibility
  X: cross-report independence / textual-relation           D: explicit distinctness-marker state
  P: provenance sufficiency
Each component ∈ {MATCH, COMPATIBLE, CONFLICTING, NOT_EVALUABLE}
```
Documentary-identity equality is **not** restored as a requirement for
multiple reports of one candidate occurrence.
```
G_same,ij^evidence = 1[A,J,T,S ∈ {MATCH,COMPATIBLE} ∧ X≠CONFLICTING ∧ D≠CONFLICTING ∧ P=MATCH]
G_contradiction,ij = 1[all 6 conflict dimensions explicitly assessed]
E_same,ij = 1[G_same,ij^evidence=1 ∧ G_contradiction,ij=1]
Allowed outputs: EVIDENCE_SUPPORTS_SAME_OCCURRENCE_MAPPING |
  EVIDENCE_CONFLICTS_WITH_SAME_OCCURRENCE_MAPPING |
  EVIDENCE_UNRESOLVED_FOR_SAME_OCCURRENCE
"SAME_HISTORICAL_EVENT_PROVEN" is never used.
```

### 0-B.2 STRESS-01 (corrected) — Cingkuak, 3 report pairs

```
(Kathirithamby, Harries)   A,J,T,S=MATCH/COMPATIBLE, X=COMPATIBLE, D=COMPATIBLE, P=MATCH
(Kathirithamby, van Kempen) same result
(Harries, van Kempen)      same result
-> all 3 pairs: EVIDENCE_SUPPORTS_SAME_OCCURRENCE_MAPPING
```
This is a report-to-occurrence **compatibility** classification only.
Selection-risk qualification is **not erased**:
`STRESS01_SELECTION_RISK=TARGET_CONGRUENT_SELECTION_DISCLOSED`,
`STRESS01_INDEPENDENT_VALIDATION_VALUE=LIMITED` — the Cingkuak bundle was
originally chosen because its dates agreed; the corrected gate demonstrates
behavior, it does not retroactively make the selection blind.

### 0-B.3 HOLDOUT-01 — Padang, mandatory adverse holdout, 3 report pairs (CORRECTED — narrow semantic fix applied)

Documentary identity `I_r^doc` is separated from report-to-occurrence
compatibility `Ω_ij`, and within `Ω_ij`, textual dependence `X_dep` is
scored **separately** from occurrence compatibility rather than being
encoded as a `T`/`X` conflict:
```
X_dep ∈ {INDEPENDENT, PARTIALLY_DEPENDENT, TEXTUALLY_DEPENDENT, DEPENDENCE_NOT_EVALUABLE}
G_compat,ij^evidence = 1[A,J,T,S ∈ {MATCH,COMPATIBLE} ∧ D≠CONFLICTING ∧ P=MATCH]
G_corroboration,ij^evidence = G_compat,ij^evidence × 1[X_dep=INDEPENDENT]
  -- compatibility with one occurrence is NOT independent corroboration
```
```
(Botham, Harries)      A,J,T,S=MATCH/COMPATIBLE (both state 17 Aug), D=COMPATIBLE, P=MATCH
                        -> G_compat=1; X_dep=TEXTUALLY_DEPENDENT (Harries quotes Botham's separate letter)
                        -> EVIDENCE_COMPATIBLE_WITH_SAME_OCCURRENCE_BUT_TEXTUALLY_DEPENDENT
                        (CORRECTED from an earlier pass that wrongly classified this pair CONFLICTS
                        by encoding textual dependence as an occurrence conflict)

(Botham, van Kempen)    J audited explicitly: "surrender" and "Padang jatuh" (Padang fell) are
                        compatible descriptions of the same capitulation act -> J=COMPATIBLE
                        T=CONFLICTING (17 Aug vs 18 Aug ONLY — 19 Aug excluded, see below)
                        X_dep=INDEPENDENT -> EVIDENCE_CONFLICTS_WITH_SAME_OCCURRENCE_MAPPING

(Harries, van Kempen)   Same J/T finding as above; X_dep=PARTIALLY_DEPENDENT (Harries' figure
                        derives from Botham) -> EVIDENCE_CONFLICTS_WITH_SAME_OCCURRENCE_MAPPING
```
**19 August is never a third surrender-date candidate.** Van Kempen's "19
August" is explicitly `J_19Aug=FLEET_ARRIVAL` — the main fleet's arrival, a
distinct act from the surrender — and is excluded from the surrender/fall
date vector, which is **17 vs. 18 August only**. Textual dependence
(Harries quoting Botham) is scored as `X_dep=TEXTUALLY_DEPENDENT`/
`PARTIALLY_DEPENDENT`, never smuggled into a `T` or occurrence-level
conflict, and is never converted into independent corroboration.

**Meaning:** the current report bundle does not satisfy the
same-occurrence *compatibility* gate for 2 of its 3 pairs — this is a
gate-failure finding about evidence-bundle consistency, restated precisely
as: **event-date and act-date reconciliation remains unresolved across
reports** — **not** proof of multiple historical occurrences, and not a
claim forced at the "total occurrence" level merely from a date conflict.

### 0-B.4 HOLDOUT-02 — full parent-episode boundary audit, N_children=4

```
Cingkuak  B_ie=1  (act identity=1, actor identity assessed=1, date role assessed=1, provenance=1)
Padang    B_ie=0  (EVENT-DATE AND ACT-DATE RECONCILIATION REMAINS UNRESOLVED ACROSS REPORTS, per corrected 0-B.3 — 19 Aug fleet arrival is not counted as a third surrender date)
Pariaman  B_ie=0  (Oct 1781 value is Botham's dispatch/letter date, not an independently established event date)
Air Haji  B_ie=0  (location identity itself "diduga"/suspected, unconfirmed — in addition to the same date-proxy problem)

P_boundary = 1/4 = 0.25
G_parent,e^evidence = 1[N_children≥2(yes) ∧ ∀i:B_ie=1(NO — 3 of 4 fail) ∧ ...] = 0
```
Episodes are **not** validated merely because dates are close, it is one
expedition, places are sequential, or the colonial actor is the same. Every
child must clear its own boundary; one failing child is sufficient to leave
the parent episode not evidence-ready.

**This does NOT mean:** the episode definitely did not exist; the four
entries are historically unrelated; `parent_episode_id` must be deleted; or
every child must become a standalone event. Status:
`EXISTING_PARENT_EPISODE_NOT_EVIDENCE_READY_UNDER_PROSPECTIVE_RULE`.

### 0-B.5 Revised estimands (CORRECTED — final pair-level distribution)

```
N_reevaluation_objects = 3   (STRESS-01, HOLDOUT-01, HOLDOUT-02)
N_pairs_assessed = 6   (3 Cingkuak + 3 Padang)

N_supports_same_occurrence_mapping        = 3   (all 3 Cingkuak pairs)
N_compatible_but_textually_dependent      = 1   ((Botham,Harries))
N_conflicts_with_same_occurrence_mapping  = 2   ((Botham,vanKempen), (Harries,vanKempen))
N_unresolved_for_same_occurrence_mapping  = 0
  3 + 1 + 2 + 0 = 6  (reconciles)

P_support             = 3/6 = 0.500
P_dependent_compatible = 1/6 ≈ 0.1667
P_conflict             = 2/6 ≈ 0.3333
P_unresolved           = 0/6 = 0.000

P_same_nonunresolved = 6/6 = 1.00
  (retained validly: 0 of 6 pairs are unresolved, so all 6 reached a
  decisive category — support, dependent-compatible, or conflict. This is
  NOT described as universal same-occurrence support; the disaggregation
  above is the correct reading.)

P_conflict_preservation = 1/1 = 1.00
  (the one pre-identified known conflict — Padang's date — was preserved
  as CONFLICTING for 2 of 3 Padang pairs, not smoothed to MATCH; the third
  pair's apparent date agreement was correctly attributed to textual
  dependence, not independent confirmation)

P_boundary = 1/4 = 0.25

N_unsupported = Σ 1[classification≠EVIDENCE_UNRESOLVED ∧ evidence_gate=0] = 0
  (all 6 pair classifications, including the dependent-compatible one, are
  evidence-backed: G_compat=1 for the dependent pair, X_dep assessed
  separately; T=CONFLICTING is explicit assessed evidence for the two
  conflicting pairs, not an unsupported claim)

G_closure_demo = 1[STRESS01 evaluated=1 ∧ HOLDOUT01 evaluated=1 ∧ HOLDOUT02 evaluated=1
                    ∧ N_unsupported=0 ∧ conflict_preservation=1
                    ∧ textual_dependence_not_misrepresented_as_conflict=1] = 1
```
**`G_closure_demo=1` is qualified `LIMITED_RULE_BEHAVIOR_DEMONSTRATION`.** It
means: all three re-evaluation objects were assessed; the known adverse
conflict was retained, not normalized away; no non-unresolved
classification was assigned with an unsatisfied evidence gate. **It does
NOT imply** ontology validity, historical truth, corpus readiness, model
readiness, or researcher acceptance.

### 0-B.6 Actor normalization and category origin (carried forward, re-confirmed)

```
Diplomatic actor form (Botham's primary letter) = unnamed
Normalized form                                  = "Heerskerch"
Normalization source                             = Kathirithamby 1965 secondary thesis, p.314
Primary cross-verification                       = NOT_AVAILABLE
Collision risk                                    = UNRESOLVED
Authoritative actor identity                      = NOT_ESTABLISHED

event_type = "konflik"  ->  category origin = PROJECT_NORMALIZED_LABEL
  Botham's primary wording: "surrender", "summoned", "expedition" -- not "konflik".
```
"Heerskerch" is not promoted to a primary-source identity. "Konflik" is not
treated as a source-native category or neutral historical ontology.

### 0-B.7 Design and acceptance gates — ACCEPTED 2026-09-09 (final validation pass)

```
G_gran_design=1, G_parent_design=1, G_same_design=1, G_closure_demo=1
A_gran=1, A_parent=1, A_same=1   (ACCEPT_PROSPECTIVELY_WITH_LIMITS, researcher decision 2026-09-09)
G_gran_accepted=1, G_parent_accepted=1, G_same_accepted=1
```
**Acceptance scope:** authorizes future prospective use of the rule only.
It does **not** authorize corpus mutation, retrospective recoding,
`DEDUP-06` closure, `R-O4` promotion, Hawkes fitting, ACT-07 execution,
ontology validation, or causal inference. `DEDUP-06` remains open; ACT-07
remains deferred; every actual corpus mutation requires a new, separately
authorized operation.

### 0-B.8 ACT-07 (unchanged, re-confirmed)

```
ACT07_EXECUTION_DECISION = DEFER
G_ACT07_design = 1
G_ACT07_execute = 0
```
Not expanded or executed. No Corpus Diplomaticum search. No
archival-opportunity data retrieved.

### 0-B.9 Final status

```
RULE_PACKAGE_READY_FOR_RESEARCHER_ACCEPTANCE_DECISION
```
This is the final planned methodology stress-test pass. No further stress
test or example is proposed after this checkpoint.

## 1. Epistemic objects (kept separate)

```
LATENT_HISTORICAL_EVENT, DOCUMENTED_OR_REPORTED_EVENT,
LEGAL_OR_ADMINISTRATIVE_INSTRUMENT, CORPUS_CODED_EVENT, PARENT_EPISODE,
SOURCE_CITATION_TARGET, EDITORIAL_ASSERTION, PROJECT_CODING_DECISION,
UNRESOLVED_REFERENT
```
No two objects are collapsed merely because date, commissioner, location, or
narrative is shared. This principle is applied throughout Section 5.

## 2. Prospective granularity rule (design)

For candidate documentary occurrence *i*:
```
Γ_i = (I_i, A_i, J_i, T_i, S_i, C_i, P_i)
  I: instrument/documentary-object identity explicit and distinct
  A: actor/party set explicitly enumerated from the document itself
  J: juridical/administrative act explicitly named
  T: temporal interval AND date role both explicit
  S: spatial scope explicit
  C: source-context/reporting relation established (primary/secondary, indep/derivative)
  P: provenance sufficiency (locator distinct from the object's own self-citation)

G_atomic,i = 1[I=A=J=T=S=P=1]
```
`G_atomic,i=1` identifies an atomic coding candidate. **It does not prove a
latent historical event.**

**Split eligibility:**
```
G_split,ij = 1[I_i≠I_j ∧ (A_i≠A_j ∨ J_i≠J_j) ∧ P_i=P_j=1 ∧ R_split=1]
R_split = 0   (not yet accepted by researcher — no split is authorized)
```

**Keep-as-one eligibility:**
```
G_single,ij = 1[I_i=I_j ∧ A_i=A_j ∧ J_i=J_j ∧ B_ij=1]
```
`B_ij` (bridging condition) requires an explicit source statement that two
representations denote the *same* literal instrument (e.g. the same
document/treaty number), not merely a shared date. **Shared date alone
never satisfies `G_single,ij`.**

## 3. Prospective parent-episode rule (design)

```
M_ie = 1[T_ie ∧ S_ie ∧ K_ie ∧ H_ie ∧ P_ie]
  T: time-window relation explicitly bounded
  S: spatial/administrative setting relation documented
  K: common process/mission/conflict/negotiation/administrative sequence is source-grounded
  H: heterogeneity among child instruments/events remains represented, not erased
  P: provenance supports membership

G_episode,e = 1[N_children,e≥2 ∧ rule_e=1 ∧ provenance_e=1 ∧ contradiction_audit_e=1 ∧ researcher_acceptance_e=1]
```
**Necessary prohibitions** — parent-episode membership must NOT be inferred
solely from: same calendar date; same commissioner; same broad region;
adjacent pages; one editorial footnote; convenience for Hawkes estimation;
desire to resolve duplication.

## 4. Three-way (four-token) prospective decision

Allowed: `SEPARATE_CHILD_EVENTS_WITHOUT_PARENT`,
`SEPARATE_CHILD_EVENTS_WITH_SHARED_PARENT`, `SINGLE_CODED_EVENT`,
`UNRESOLVED_GRANULARITY`. If decisive evidence or an accepted rule is
absent, use `UNRESOLVED_GRANULARITY`.

## 5. Non-mutating test set (N_test = 5) — ORIGINAL DESIGN RECORD, evidence preserved unchanged

**Note (2026-09-09 revision):** the `UNRESOLVED_GRANULARITY` labels below are
the original design-phase terminal labels. Section 0.3 re-expresses these
same five cases' unchanged underlying evidence using the revised
`EVIDENCE_CLASSIFICATION` / `AUTHORIZED_CORPUS_ACTION` separation and
four-state components. Nothing about the five cases' evidence was
re-derived; only the reporting vocabulary was extended.

No corpus file, `AS86`, or coded row was altered by any test below. Full
per-case detail (objects, epistemic types, granularity vectors, satisfied/
unsatisfied components, contradicting evidence, uncertainty vectors) is in
`HAWKES_V2_GRANULARITY_RULE_NONMUTATING_TEST_LEDGER.csv`. This section
gives the interpretive summary.

**All five results are `UNRESOLVED_GRANULARITY`. This is not one repeated
reason — each case fails a different, explicitly identified rule
component, and the common terminal label must not be read as evidence that
the rule collapses every case identically.**

### TEST-01 — Corpus III D/Dl + `EVT-1687-gm-vol04-05-162-a6b1`
```
Blockers: G_split blocked because R_split=0; G_episode blocked because
researcher_acceptance_e=0. Wave 2's H-F and H-G remain frozen at
RETAIN_AS_OPEN and are NOT reopened or reinterpreted here — this test
applies the new general rule to the same facts and finds it produces the
same non-closure, which is a consistency check, not a new finding.
```

### TEST-02 — `EVT-1686-buku-vogel-1690-458-fa01` (Batang Capas recapture, 1 Sept 1686)
```
Objects: Vogel's memoir account (docs/bsb10468472.txt) of the VOC military
recapture of the English fort at Batang Capas, 1 Sept 1686; EIC letter
docs/BL_IOR_G_35_198.txt (18-22 Sept 1686) discussing a "Raja Manacabo"
trading-concession dispute, in which the loss of the Batang Capas post is
cited as established context.

Blockers: A (actor set) and J (juridical/administrative act) differ
substantially — Vogel's account concerns a military assault by named VOC
forces; the EIC letter concerns an administrative correspondence dispute
among English officials (Bloome/Potts/Stobbs) about a trading concession,
written roughly three weeks later. This is a PROSPECTIVE RULE-DIAGNOSTIC
FINDING, not a correction to the corpus: the existing
`provenance_status=MULTI_SOURCE_VERIFIED` / `source_count_unique=2` tag on
this row may conflate "two sources touching one broader episode" with "two
independent reports of one occurrence" — the same class of ambiguity found
in the D/Dl case, surfaced independently. The corpus tag is NOT corrected
or reopened by this finding.
```

### TEST-03 — `EP-1668-1681-BARUS-SECESSION-AND-CONSOLIDATION` (7-member parent episode, 1668-1690)
```
Objects: EVT-1668-CD2-399-dc97, EVT-1673-CD2-498-f351, EVT-1679-CD3-208-e635,
EVT-1681-1681-971-dae1, EVT-1681-CD3-239-27a2, EVT-1681-CD3-244-1165,
EVT-1690-CD3-547-cce7 — all sharing parent_episode_id
EP-1668-1681-BARUS-SECESSION-AND-CONSOLIDATION per
HAWKES_BASELINE_V2_PARENT_EPISODE_MEMBERSHIP.csv.

Blockers: rule_explicit_R_i=0 for all seven members (confirmed directly
from the ledger's own `rule_explicit_R_i` column); the grouping's own notes
field states it is "mechanically derived from parent_episode_id ...
columns," not from a source-grounded episode rule. G_episode,e=0.
**This finding neither dissolves nor affirms the existing grouping** — it
records that a 7-member, 22-year-span grouping has never been tested
against an explicit prospective rule, which the new rule now makes visible
rather than hides.
```

### TEST-04 — `EVT-1694-gm-vol04-05-599-ac7e` (death of Sas, Nias)
```
Objects: docs/thesis/GM/xml/05/p0599.xml; coded row event_date_raw =
"~1693-1695 (tak presisi, catatan editorial RGP)"; document_date =
"14 Maret 1693 (tanggal surat); pembunuhan Sas sendiri tak presisi".

Blockers: T_i=0 — atomicity fails specifically on the temporal/date-role
component. The 14 March 1693 value is a DISPATCH_DATE-type value (the date
of the letter reporting the killing), not a resolved EVENT_DATE for the
killing itself, which the source itself states imprecisely as "~1693-1695."
**No date role is selected by convenience** — the row is left with T_i=0
and the case classified UNRESOLVED_GRANULARITY rather than defaulting the
proxy date into the event-date slot.
```

### TEST-05 — DEDUP-05 (`EVT-1755-buku-padang-1718-238-0727` vs. CD6 Koto Tangah)
```
Objects: coded row EVT-1755-buku-padang-1718-238-0727 vs. the CD6
~30-negeri renewal list (row 104, EP-1755-WESTKUST-RENEWAL-CAMPAIGN), per
HAWKES_BASELINE_V2_DEDUP_ADJUDICATION.csv row DEDUP-05.

Blockers: I_i=0 — no individual CD6 treaty folio for Koto Tangah has been
located in this repository ("belum ada nomor traktat individual ... yg bisa
dicek langsung batch ini," quoted verbatim from the existing adjudication
row). **Repository absence is not treated as historical absence** — the
case is retained as UNRESOLVED_GRANULARITY, not as evidence the
Koto Tangah instrument does not exist.
```

## 6. Reading the five UNRESOLVED results correctly

These five results are **not a rule failure** — they show the protocol did
not perform a forced classification:
```
N_premature = Σ_{k=1}^{5} 1[D_k≠UNRESOLVED ∧ G_k^decision=0] = 0
```
**But this must not be read as validating the rule either.** Every example
resolving to `UNRESOLVED_GRANULARITY` could equally indicate the rule (or
its decision gates) is too strict, or not yet operational enough to close
any case — that judgment belongs to the researcher reviewing the four
outputs, not to this operation.

## 7. Estimands and denominators (enumerated, not shortcut) — SUPERSEDED BY SECTION 0.5

**Note (2026-09-09 revision):** the estimands below reflect the original
5-case design test only. Section 0.5 recomputes all estimands across the
full 8-case set (`N_all=8`) and is authoritative going forward. This
section is retained as the historical record of the pre-revision
computation, not deleted.

```
N_test = 5

P_applicable = N_{cases receiving a NON-UNRESOLVED rule-based classification} / N_test
             = 0 / 5 = 0
  (Denominator members: TEST-01..TEST-05, all 5 counted. Numerator members:
  NONE — every case terminated UNRESOLVED_GRANULARITY.)

P_open = N_{cases correctly retained unresolved under missing evidence} / N_{cases designed to test missing evidence}
       = 1 / 1 = 1
  (Denominator: {TEST-05} only — the sole case explicitly designed as the
  insufficient-evidence preservation test. TEST-01/03/04 also terminated
  UNRESOLVED but for rule-acceptance-gap, episode-rule-gap, and
  date-role-gap reasons respectively, not raw evidentiary absence, and are
  excluded from this denominator by design category, not convenience.
  Numerator: {TEST-05} — correctly retained unresolved.)

P_contradiction = N_{test cases with explicit contradicting-evidence assessment} / 5
                = 5 / 5 = 1
  (Denominator/numerator members: TEST-01, TEST-02, TEST-03, TEST-04,
  TEST-05 — each has an explicit contradicting-evidence field in the test
  ledger, even where the entry is "NONE IDENTIFIED.")

P_provenance = N_{test cases with exact repository provenance} / 5
             = 5 / 5 = 1
  (All five cases cite exact file paths and row/page locators — see
  Section 5 and the test ledger.)

N_premature = 0   (Section 6)
```
No percentage threshold automatically validates the rule (per governing
instruction Section 8).

## 8. Red-team / blue-team — ORIGINAL PASS, see also Section 0.4/0.5 for revision-round findings

**Revision-round red-team additions (2026-09-09):**
```
Do the new evidence gates merely encode expected outcomes?
  PARTIALLY -- STRESS-03's positive result was not guaranteed by
  construction (G_parent,ij^evidence required 5 independently-checked
  components, K_ij in particular; a weaker source base would have failed
  it), but the case was selected FROM a query already known to involve a
  shared parent_episode_id, so the selection itself is not blind to the
  parent-episode question.

Is STRESS-01/02/03 selection cherry-picked?
  STRESS-01's selection criterion (3-source date agreement) is explicitly
  disclosed as TARGET_CONGRUENT_SELECTION_DISCLOSED, not blind.
  STRESS-02 and STRESS-03 were selected by objective query with disclosed
  zero-result fallbacks, not by outcome preference.

Does actor normalization create false identity?
  Not resolved either way -- STRESS-03 explicitly retains "Heerskerch" as
  UNRESOLVED collision risk rather than adopting it as ground truth.

Does J_i naturalize colonial classifications?
  STRESS-03 demonstrates the 5-way protocol catches at least one instance
  ("konflik" = PROJECT_NORMALIZED_LABEL) but the protocol itself remains
  otherwise unapplied project-wide (R-O7 still NOT_EVALUABLE).

Do parent episodes absorb meaningful heterogeneity?
  STRESS-03's H_ij=1 finding keeps Cingkuak and Padang analytically
  distinct even while grouping them -- the opposite failure mode (silent
  absorption) is not demonstrated in this revision.

Are missing-source cases (STRESS-02, TEST-05) unfairly treated as separate?
  No -- both resolved to EVIDENCE_UNRESOLVED via NOT_EVALUABLE, not to
  EVIDENCE_SUPPORTS_SEPARATE_CHILDREN.

Is the rule optimized for future Hawkes estimation?
  No reference to model fit, likelihood, or estimation convenience appears
  anywhere in this revision's gates or components.
```

## 8-original. Red-team / blue-team

**Blue team:** the componentized `Γ_i` vector preserves documentary
distinctions (TEST-01 keeps D≠Dl distinct); supports reproducible future
coding (an explicit checklist, not ad hoc judgment); can represent both
child events and shared parents (`G_split`/`G_episode` are separate
gates); and caught silent conflation independently in TEST-02 (A/J
mismatch) and TEST-04 (T failure) — cases not designed around D/Dl.

**Red team, against each named risk:**
```
Colonial-category naturalization in J_i        : UNRESOLVED (inherited from R-O7; not fixed here)
False atomicity (G_atomic=1 read as historical) : mitigated by explicit non-implication statement (Section 2), not eliminated
False aggregation                                : ACTIVELY EXPOSED, not fixed — TEST-03 shows a 7-member grouping with rule_e=0 already exists in the corpus
Documentary survival bias                        : OUTSIDE the five-case test domain (belongs to R-O8/R-O9)
Editorial-structure leakage                      : TEST-01 (Stapel's footnote) and TEST-02 (EIC letter's retrospective framing) both show this risk is real; I_i/A_i force per-document assessment as a partial countermeasure
Date-role conflation                             : DIRECTLY DEMONSTRATED by TEST-04, an independently selected case
Actor-name normalization                         : UNTESTED by any of the five cases — disclosed gap, not silently omitted
Retrospective rule fitting to D/Dl               : see OVERFIT finding below
Rule construction to improve Hawkes behavior     : ABSENT BY CONSTRUCTION — no reference to model fit, likelihood, or estimation convenience appears anywhere in Γ_i, G_split, G_single, M_ie, or G_episode
Hidden corpus mutation                           : NONE — confirmed via git status (Section 12)
```

```
OVERFIT_TO_DEDUP06_EXAMPLE = PARTIAL_MITIGATION_NOT_PROOF
```
TEST-02, TEST-03, and TEST-04 are independent stress cases — selected from
existing repository evidence, not designed around D/Dl — and the
unmodified rule produced non-trivial, non-flattering findings in each
(Section 5). This reduces, but does not eliminate, the risk that the rule
is tailored to the DEDUP-06 example. **This is not recorded as a clean
PASS.**

## 9. Rule acceptance gates

```
G_gran^design   = 1[objects=1 ∧ rules=1 ∧ ambiguity=1 ∧ provenance=1 ∧ tests=1] = 1
G_parent^design = 1[membership=1 ∧ child_heterogeneity=1 ∧ contradiction_audit=1 ∧ tests=1] = 1

A_gran   = 0   (not yet obtained)
A_parent = 0   (not yet obtained)

G_gran^accepted   = G_gran^design   × A_gran   = 1 × 0 = 0
G_parent^accepted = G_parent^design × A_parent = 1 × 0 = 0
```
**Protocol design completion does not equal researcher acceptance.**

## 10. ACT-07 design (design only — no data retrieved)

Bounded question: *What external, outcome-independent information can
describe the changing opportunity for events to be recorded, survive, be
catalogued, be digitized, and enter the current corpus over time?*

Full per-candidate specification (bounded research question, target
institution/collection, metadata fields, date range, documentary unit,
coverage denominator, lawful access route, expected formats, provenance
fields, circularity test, missingness interpretation, stop condition,
result classification) is in
`HAWKES_V2_ACT07_ARCHIVAL_OPPORTUNITY_DESIGN.csv`. Summary:

```
Candidates 1-3 (annual surviving-document / folio-page / catalogue-record counts):
  NOT_EVALUABLE, A_m=0 (no lawfully-accessible source located in this repository)

Candidates 4-5 (annual active-source-family count / digitization-access coverage):
  DESCRIPTIVE_ONLY_CIRCULAR, C_m^overlap=1
  (reusing Wave 1's already-computed R-O9 finding, HAWKES_V2_EXPOSURE_INFORMATION_REQUIREMENTS.csv
  and HAWKES_BASELINE_V2_EXPOSURE_INFORMATION_REQUIREMENTS.csv -- NOT recomputed here)

Candidate 6 (administrative reporting-volume independent of coded resistance events,
  e.g. GM page-count per calendar year -- a NEW candidate, not previously assessed in Wave 1):
  NOT_EVALUABLE -- naming this example does NOT make it ready; A_m, T_m, and P_m
  are all unassessed pending a future, separately authorized ACT-07 execution

Candidate 7 (other, from existing repository metadata):
  NOT_EVALUABLE -- undefined until a concrete external measure is named
```
**Coded-event counts are never treated as an external archival-opportunity
measure** — this prohibition is preserved throughout.

```
G_ACT07^execute = 1[Q=1 ∧ D=1 ∧ L=1 ∧ F=1 ∧ C=1 ∧ B=1 ∧ A=1]
A = 0   (researcher authorization not given)
G_ACT07^execute = 0
```
No Corpus Diplomaticum search occurred. No ACT-07 data was retrieved.
ACT-05 was not executed.

## 11. Frozen state — confirmed unchanged

```
DEDUP-06 = UNRESOLVED, G_DEDUP06 = 0, R-O4 = FAIL, AS86 = FROZEN_UNCHANGED
D1_prior = NOT_EVALUABLE, G_seg_prospective = 1 (prospective only)
G_ontology = 0, G_causal = 0, G_reconsider_future = 0
Hawkes fitting = SUSPENDED, Hawkes visualization = SUSPENDED
V2-B = BLOCKED, Phase D = CLOSED / MUST NOT BE RERUN
Wave 2 remains frozen at (R,Q,C,A)=(1,1,0,1)
SERVER_SYNC = NOT_EXECUTED, PRODUCTION_DEPLOYMENT = NOT_EXECUTED, G_sync = NOT_EVALUABLE
```

## 12. Guardrail confirmation

No corpus file, `AS86`, coded row, Wave 1 output, or Wave 2 output was
edited. No Corpus Diplomaticum search or retrieval occurred (all five test
cases used only files already read/cited in Wave 1 or Wave 2, plus
`docs/bsb10468472.txt`, `docs/BL_IOR_G_35_198.txt`,
`HAWKES_BASELINE_V2_PARENT_EPISODE_MEMBERSHIP.csv`,
`HAWKES_BASELINE_V2_DATE_SEMANTICS.csv`, and
`docs/thesis/GM/xml/05/p0599.xml`, all already present in this repository).
No model execution, ontology/causal promotion, or Git/server/production
operation occurred at this checkpoint. Exactly four new files created,
under `.../evidence_acquisition/wave3a/`.

## 13. Final status (Wave 3A revision, 2026-09-09) — SUPERSEDED BY SECTION 0-B.9

**Note:** Section 0-B.9 (Wave 3B, same date) is the current authoritative
final status: `RULE_PACKAGE_READY_FOR_RESEARCHER_ACCEPTANCE_DECISION`. This
section is retained as the historical record of the Wave 3A revision
checkpoint.

```
WAVE3A_RULE_REVISION_OPERATIONALLY_DEMONSTRATED_RESEARCHER_ACCEPTANCE_REQUIRED
```
`G_demonstration=1` (`LIMITED_OPERATIONAL_DEMONSTRATION`) does not imply
`G_gran_accepted`, `G_parent_accepted`, `G_ontology`, `G_causal`,
`G_reconsider_future`, or corpus-mutation authorization — all remain 0/false.
`ACT07_EXECUTION_DECISION = DEFER`; `G_ACT07^execute = 0`. Neither this
status nor any gate value in this document authorizes corpus mutation,
ACT-07 execution, Hawkes estimation, or V2-B.

**Pausing for researcher adjudication.**
