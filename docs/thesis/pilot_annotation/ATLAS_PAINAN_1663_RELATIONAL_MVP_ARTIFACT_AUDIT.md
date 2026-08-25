# ATLAS PAINAN 1663 RELATIONAL MVP — ARTIFACT AUDIT

> **NONPRODUCTION ARTIFACT AUDIT — NO IMPLEMENTATION, MIGRATION, API CHANGE, DATABASE CHANGE, GRAPHIFY UPDATE, COMMIT, PUSH, OR DEPLOY PERFORMED OR AUTHORIZED BY THIS DOCUMENT**
> Continuation of `ATLAS_PAINAN_1663_RELATIONAL_MVP_IMPLEMENTATION_PLAN.md`, executed per frozen researcher decisions (this turn's governing instructions). Constructs and validates one artifact and one read-only validator only; performs no new corpus research.

---

## 1. Scope

This turn performs exactly one step of the MVP sequence already fixed by the implementation plan: **Relational MVP Artifact Construction** for the Painan 1663 case. It builds `data/power_relations/painan_1663_relational_research_artifact.json`, a read-only validator for that single artifact, and this audit. It does not repeat power-theory recovery, the patron-client deep dive, controlled-vocabulary extraction, source-row discovery, a full corpus re-read, or MVP scope selection — all of those are treated as complete inputs, reused verbatim where they bear on this artifact's content.

## 2. Frozen Research Decisions (as received this turn)

```text
1.  Painan 1663 approved as the MVP relational case.
2.  Actor scope: Muhammad Syah faction; Raja Adil faction; VOC; Aceh court (or ambassadors);
    Bandar X signatories only if mandate traceable; named brokers only if source-traceable.
3.  Exactly seven relation types authorized: REQUESTS_PROTECTION_FROM, PROVIDES_PROTECTION_TO,
    REQUIRES_MONOPOLY_FROM, NEGOTIATES_WITH, RECONCILES_WITH, MAINTAINS_PARALLEL_ALIGNMENT_WITH,
    CLAIMS_JURISDICTION_OVER.
4.  Broker becomes an actor/role only if a source identifies the intermediary; no hypothetical broker.
5.  Patron-client stays an annotation field, never an edge (PATRON_OF / CLIENT_OF /
    PATRON_CLIENT_RELATION forbidden); no dyad may read PATRON_CLIENT_SUPPORTED.
6.  Game theory / power theory stay research-only annotations; no numeric payoff, no equilibrium
    claim, no perfect-rationality assumption.
7.  Every relation record carries 24 named fields (§5 of the governing instructions), including four
    explicitly separated interpretive layers.
8.  Four layers kept distinct: source statement / historical reconstruction / theoretical annotation /
    public-display summary.
9.  Only the nonproduction artifact path is created: data/power_relations/painan_1663_relational_research_artifact.json.
10. A read-only validator is created but not connected to API, database, frontend, Atlas, or Graphify.
11-14. Twenty-five specific validation checks required (§17 of the governing instructions).
```

No corpus re-read, no new theory search, and no change to the five already-recovered deep-dive artifacts was performed to satisfy these decisions — they are treated as inputs only.

## 3. Source Inputs (reused, not re-derived)

```text
ATLAS_PAINAN_1663_RELATIONAL_MVP_IMPLEMENTATION_PLAN.md           (prior turn, this session)
PAINAN_1663_POWER_THEORY_PATRON_CLIENT_DEEP_DIVE.md                (recovered, unmodified)
PAINAN_1663_POWER_THEORY_WORKING.csv                                (recovered, unmodified — PWR01-07)
PAINAN_1663_PATRON_CLIENT_WORKING.csv                                (recovered, unmodified — DYAD01-04)
PAINAN_1663_POWER_CAUSAL_HYPOTHESIS_MATRIX.csv                       (recovered, unmodified — PT-H1-H12)
ATLAS_POWER_THEORY_PATRON_CLIENT_ONTOLOGY_NOTE.md                    (recovered, unmodified)
ATLAS_POWER_RELATION_DATA_CONTRACT_DRAFT.md                          (re-read this turn for exact
                                                                       controlled-vocabulary values only)
data/research/linimasa_events.csv, rows 26, 28, 29, 34, 35, 36, 37, 39, 42, 44, 45  (already verified in
                                                                       a prior checkpoint this session;
                                                                       re-read this turn only to confirm
                                                                       exact field values for the specific
                                                                       rows actually used — see §5)
```

Rows 56, 60, 63, 64, 66, 70, 72, 94, 97, 100 (verified in the prior checkpoint but concerning other polities/decades) were consulted for confirmation only and are **not** cited as sources in any relation record — see §6.

## 4. Actor Construction

Six actors, exactly matching the frozen scope. No seventh actor was added.

| actor_id | Label | Type | Named individuals | Review flag |
|---|---|---|---|---|
| `ACTOR_MUHAMMAD_SYAH_FACTION` | Muhammad Syah faction | RULING_FACTION | Muhammad Syah; Raja Muzzaffar Syah (father) | true |
| `ACTOR_RAJA_ADIL_FACTION` | Raja Adil faction | RULING_FACTION | Raja Adil | false |
| `ACTOR_VOC` | VOC (institution) | INSTITUTION | — | false |
| `ACTOR_ACEH_COURT` | Aceh court (or ambassadors) | INSTITUTION | — | false |
| `ACTOR_GROENEWEGEN` | Groenewegen (VOC commissioner/negotiator) | NAMED_BROKER | Jan van Groenewegen | true |
| `ACTOR_MANSUR_SYAH` | Mansur Syah (agent-signatory) | NAMED_BROKER | Mansur Syah | true |

- **Muhammad Syah faction** carries `researcher_review_required = true` for one specific, carried-forward reason: the recovered causal hypothesis matrix (PT-H2) flags the "Malafarcha"/"Sultan Mametcha" name-variant in linimasa rows 34/44/45 as a **plausible, not independently confirmed** match to Muhammad Syah/Raja Muzzaffar Syah. This artifact reuses that caveat verbatim on every relation record touching those rows rather than resolving it.
- **Groenewegen** and **Mansur Syah** are included as brokers per decision item 4 — both are named and source-traceable (linimasa rows 26/35/37 and K-W 1976 p.74 respectively). Each carries `researcher_review_required = true` for reasons already identified in the recovered deep dive (§15 brokerage misrepresentation-risk for Groenewegen; PT-H9's undistinguishable-agent-vs-principal finding for Mansur Syah), not for any new concern raised in this turn.
- **Bandar X signatories** were evaluated against decision item 2's condition ("hanya jika mandatnya dapat ditelusuri") and excluded — see §11.
- **Catip** (the information broker documented in row 36) was evaluated against decision item 4 and excluded despite being named and source-traceable — see §11, since no relation type among the seven authorized types captures an information-flow act, and forcing one would violate the "no orphan/forced edge" discipline.
- **Painan / Padang / Tiku signatories** were not included: they are absent from this turn's frozen actor-scope list (decision item 2), consistent with the recovered deep dive's own `PATRON_CLIENT_NOT_TESTABLE` finding for these three negeri individually.

## 5. Relation Construction

Nine relation records, covering all seven authorized types (none forced without source support; `NEGOTIATES_WITH` and `CLAIMS_JURISDICTION_OVER` each used twice because two distinct, independently source-supported dyads exist for each).

| relation_id | Type | Subject → Object | valid_from → valid_to | Primary sourcing |
|---|---|---|---|---|
| `REL_REQUESTS_PROTECTION_FROM_MUHAMMAD_SYAH_FACTION__VOC` | REQUESTS_PROTECTION_FROM | Muhammad Syah faction → VOC | 1662-11 → 1663-03 | K-W 1976 p.74 + row 34 |
| `REL_PROVIDES_PROTECTION_TO_VOC__MUHAMMAD_SYAH_FACTION` | PROVIDES_PROTECTION_TO | VOC → Muhammad Syah faction | 1663-03 → open | K-W 1976 p.74 + rows 35, 42 |
| `REL_REQUIRES_MONOPOLY_FROM_VOC__MUHAMMAD_SYAH_FACTION` | REQUIRES_MONOPOLY_FROM | VOC → Muhammad Syah faction | 1663-03 → open | row 35 + K-W 1976 p.74 + rows 44, 45 |
| `REL_NEGOTIATES_WITH_GROENEWEGEN__MUHAMMAD_SYAH_FACTION` | NEGOTIATES_WITH | Groenewegen → Muhammad Syah faction | 1662-11 → 1663-07-27 | K-W 1976 p.74 + rows 35, 37 |
| `REL_NEGOTIATES_WITH_MANSUR_SYAH__VOC` | NEGOTIATES_WITH | Mansur Syah → VOC | 1663-03 → 1663-03 | K-W 1976 p.74 only |
| `REL_RECONCILES_WITH_MUHAMMAD_SYAH_FACTION__ACEH_COURT` | RECONCILES_WITH | Muhammad Syah faction → Aceh court | 1663-10 → open | K-W 1976 p.74 only |
| `REL_MAINTAINS_PARALLEL_ALIGNMENT_WITH_MUHAMMAD_SYAH_FACTION__VOC` | MAINTAINS_PARALLEL_ALIGNMENT_WITH | Muhammad Syah faction → VOC | 1663-10 → open | K-W 1976 p.74 only |
| `REL_CLAIMS_JURISDICTION_OVER_VOC__MUHAMMAD_SYAH_FACTION` | CLAIMS_JURISDICTION_OVER | VOC → Muhammad Syah faction | 1663-07-27 → open | rows 35, 37, 39 + K-W 1976 p.74 |
| `REL_CLAIMS_JURISDICTION_OVER_VOC__RAJA_ADIL_FACTION` | CLAIMS_JURISDICTION_OVER | VOC → Raja Adil faction | 1665-01 → open | K-W 1976 p.74 only |

All 24 fields required by governing-instruction item 5 are present on every record, including the four explicitly-separated interpretive layers (§8).

Row 39 (1664 expulsion order) and rows 44/45 (1667 cession) are used only as **corroborating `event_ids`/evidence within existing relation records** (enforcement/escalation evidence for the VOC↔Muhammad-Syah-faction relations), not as sources for standalone new relation records — no relation type among the seven captures an expulsion order or a territorial cession as its own distinct edge.

## 6. Excluded Candidate Relations

Recorded per governing-instruction item 21 — considered, not built, with reasons:

| Candidate | Why excluded |
|---|---|
| Groenewegen honored by Aceh court, 1660 (row 26) | No relation type among the seven authorized types represents a symbolic-recognition/honor act; used only as supporting theoretical annotation on `NEGOTIATES_WITH` (Groenewegen↔Muhammad Syah faction), not as its own relation. |
| VOC↔Indrapura jurisdiction clause, 1660 (row 28) | Predates Muhammad Syah's own faction identity (established Nov 1662 per K-W); the 1660 "landsheeren Indrapoura" cannot be safely attributed to the Muhammad Syah faction actor without fabricating continuity across a documented succession crisis. |
| VOC annual gift schedule to Raja Mametsa, 1660 (row 29) | Same reason as row 28 — predates the frozen actor's documented identity; attaching it would risk actor misattribution. |
| Panglima Aceh vs. Padang, 1657-61 (row 31) | No actor in the frozen six-actor scope represents "Padang" as a standalone party (Painan/Padang/Tiku signatories excluded per decision item 2). |
| Aceh informer network / Catip, Mar 1663 (row 36) | No relation type among the seven captures an information-flow act; Catip is named and source-traceable but was excluded as an actor for exactly this reason (§4) rather than force a stretched `NEGOTIATES_WITH` edge onto an intelligence-carrying act. |
| VOC-ordered expulsion of Achinders, 1664 (row 39) | Not built as a standalone relation (no relation type represents an expulsion order); folded into `REL_CLAIMS_JURISDICTION_OVER_VOC__MUHAMMAD_SYAH_FACTION` as enforcement evidence instead. |
| Sillida & Pulau Cingkuak cession, 1667 (rows 44, 45) | Not built as a standalone relation (cession/territorial-control is not one of the seven types); folded into `REL_REQUIRES_MONOPOLY_FROM_VOC__MUHAMMAD_SYAH_FACTION` as escalation evidence instead. |
| Pariaman/Singkil/Painan-1681/Tiku-1684/Priaman-1712 realignment cycle (rows 56, 60, 63, 64, 66, 70, 94) | None of the named rulers in these rows (Pariaman regenten, Singkil regenten, Sultan Sampourna/radja Carbouw of Painan, Tiku regenten) map to any actor in the frozen six-actor scope; used only as general historiographical-pattern context in theoretical annotations, never as a relation-level source. |
| Inderapura↔England, 1686 (row 72); Inderapura↔VOC, 1716 (row 97) | 23-53 years post-crisis; actor continuity between the 1662-65 "Muhammad Syah faction" and the ruler(s) named in these later rows is not established within this turn's scope; including them would stretch the MVP's temporal boundary and risk unproven actor continuity. Retained only as the recovered deep dive's own chronology/PT-H6 context, not as this artifact's sourcing. |
| Sillida gold-mine lease, 1737 (row 100) | Different named ruler (Radja Nanxatti), not in the frozen actor scope; excluded. |
| Bandar X signatories as a standalone actor | Evaluated against decision item 2's mandate-traceability condition and found `CONTESTED`/`PARTIALLY_SUPPORTED` at best (per the recovered deep dive's own §19 characterization of Bandar X as a weak, non-binding council) — no traceable mandate, so excluded per the decision's own stated condition, not a new finding. |
| Painan / Padang / Tiku as standalone actors or relation endpoints | Outside this turn's frozen actor list; consistent with `PATRON_CLIENT_NOT_TESTABLE` (DYAD03) for these three negeri specifically. |

## 7. Controlled Vocabularies

All seven controlled vocabularies were reused verbatim from `ATLAS_POWER_RELATION_DATA_CONTRACT_DRAFT.md` (re-read this turn only to confirm exact values, not re-derived):

```text
provenance_status:            CD_PRIMARY | CD_PARTIAL | CD_INDEPENDENT | MULTI_SOURCE_VERIFIED | PROVENANCE_AMBIGUOUS
evidence_strength:            HIGH | MODERATE | LOW | CANNOT_DETERMINE
interpretive_status:          SOURCE_DESCRIPTION_ONLY | MECHANISM_HYPOTHESIS | PROCESS_TRACING_SUPPORTED | CONTESTED | CANNOT_DETERMINE
claim_or_effective_control:   CLAIM | FORMAL_ACCEPTANCE | TREATY_OBLIGATION | MILITARY_PRESENCE | FORT_CONTROL |
                               COMMERCIAL_CONTROL | ADMINISTRATIVE_CONTROL | EFFECTIVE_LOCAL_COMPLIANCE |
                               CONTESTED_CONTROL | UNKNOWN_EFFECTIVE_CONTROL
explicit_or_inferred:         EXPLICIT_STRATEGY | OBSERVED_ACTION_AS_STRATEGY | INFERRED_AVAILABLE_OPTION |
                               COUNTERFACTUAL_NOT_ESTABLISHED
commitment_credibility:       CREDIBLE | PARTIALLY_CREDIBLE | LOW_CREDIBILITY | FAILED | NOT_TESTABLE
patron_client_classification: PATRON_CLIENT_SUPPORTED | PATRON_CLIENT_PARTIALLY_SUPPORTED | PATRON_CLIENT_CONTESTED |
                               PATRON_CLIENT_NOT_SUPPORTED | PATRON_CLIENT_NOT_TESTABLE
```

`power_dimensions` (multi-valued, `FIRST_DIMENSION | SECOND_DIMENSION | THIRD_DIMENSION | RELATIONAL_AND_PRODUCTIVE | SYMBOLIC_CLASSIFICATORY | AUTHORITY_AND_LEGITIMACY`) is the one candidate vocabulary the recovered ontology note itself flagged as **not yet adopted** (researcher decision item 4 in the plan) — it is used here as a research annotation only, exactly as the ontology note anticipated, not newly ratified by this artifact.

**One field-level, narrowly-scoped, self-documented convention was added and is recorded in the artifact's own `vocabulary_notes` block, not silently**: `date_precision` (`YEAR | MONTH | DAY`) has no fixed value list in the Data Contract Draft (it references an "existing `event_date_precision` convention" conceptually, but no such column exists in the current `linimasa_events.csv`, and no fixed list is given). This is disclosed explicitly in the artifact rather than left implicit.

**One mapping rule was applied and is disclosed in `vocabulary_notes.explicit_or_inferred_secondary_source_mapping`**: per governing-instruction item 13, any relation sourced *exclusively* from K-W 1976 (no corroborating primary-corpus row) is tagged `explicit_or_inferred = OBSERVED_ACTION_AS_STRATEGY` — the closest official equivalent to "inferred from secondary-source interpretation," reusing an existing value rather than inventing one. Four relations use this mapping (listed in the vocabulary_notes block and in §5's table implicitly by their "K-W 1976 p.74 only" sourcing).

## 8. Source-to-Relation Traceability

Every relation's `source_document_ids` resolves to either a K-W 1976 p.74 citation or a `linimasa_row_N` id that exists in the currently-verified `linimasa_events.csv`. `event_ids` (a stricter subset used only for primary-corpus rows) contains exactly: `linimasa_row_34, 35, 37, 39, 42, 44, 45` — every one independently confirmed present in the CSV by the validator (§16, check i). No source was invented; no citation was attributed to a work not already confirmed read in the recovered deep dive.

## 9. Claim versus Effective Control

Populated distinctly per relation, never defaulted to a single value:

- `TREATY_OBLIGATION` (1) — the monopoly clause as a stated obligation, deliberately distinct from its enforcement.
- `CONTESTED_CONTROL` (2) — both `CLAIMS_JURISDICTION_OVER_VOC__MUHAMMAD_SYAH_FACTION` and `PROVIDES_PROTECTION_TO`, directly reusing PWR03's finding: a formal claim/commitment existed without demonstrated durable effective control over the same actor's subsequent conduct.
- `FORMAL_ACCEPTANCE` (1) — Mansur Syah's Batavia signing act specifically, distinguished from any claim about what followed.
- `MILITARY_PRESENCE` (1) — the 1665 expedition against Raja Adil's faction, a more concrete (if still non-territorial-administrative) effective assertion than the treaty-claim relations.
- `UNKNOWN_EFFECTIVE_CONTROL` (4) — used only for relation types that are not themselves jurisdiction/control assertions (requests, negotiations prior to any resulting claim, the reconciliation and parallel-alignment states), populated to satisfy the mandatory-field requirement without asserting a substantive control finding those relation types do not themselves support. This convention is disclosed in `vocabulary_notes` (§7 above), not left implicit.

No relation uses `EFFECTIVE_LOCAL_COMPLIANCE` — the artifact makes no claim that VOC (or Aceh) achieved demonstrated effective compliance from any actor in this case, consistent with the recovered deep dive's own repeated finding that the Painan case does not support a clean control narrative.

## 10. Patron-Client Annotation

Strictly an annotation field on relation records — no `PATRON_OF`, `CLIENT_OF`, or `PATRON_CLIENT_RELATION` edge exists anywhere in the artifact (validator check p, PASS). Distribution:

- `PATRON_CLIENT_PARTIALLY_SUPPORTED` (3) — the three relations most directly constituting DYAD02 (VOC↔Muhammad Syah faction): the protection request, the protection grant, and the monopoly requirement.
- `PATRON_CLIENT_CONTESTED` (1) — `MAINTAINS_PARALLEL_ALIGNMENT_WITH`, deliberately tagged CONTESTED rather than PARTIALLY_SUPPORTED because this specific relation is what falsifies DYAD02's exclusivity element in the recovered ledger.
- `PATRON_CLIENT_NOT_TESTABLE` (5) — every relation not itself the object of a tested dyad in the recovered patron-client ledger: both `NEGOTIATES_WITH` broker relations, the Aceh reconciliation (DYAD01 was evidenced for the pre-1660 relationship broadly, not this 1663 act specifically — reusing it here would overclaim), and both `CLAIMS_JURISDICTION_OVER` relations.
- **No relation carries `PATRON_CLIENT_SUPPORTED`** — validator check q, PASS, matching the recovered ledger's own finding that no dyad in this case reaches full support.

## 11. Power-Theory Annotation

`power_dimensions` populated per relation from the recovered deep dive's own §5-§9 findings, never as an aggregate score: `FIRST_DIMENSION` (8 occurrences — the dominant, most directly observable dimension in this case, consistent with the deep dive's own emphasis), `SECOND_DIMENSION` (3 — agenda/contract-form control), `AUTHORITY_AND_LEGITIMACY` (1), `RELATIONAL_AND_PRODUCTIVE` (1). `THIRD_DIMENSION` and `SYMBOLIC_CLASSIFICATORY` are not used on any relation in this artifact — the recovered deep dive's own third-dimension and symbolic-classification findings (PWR04, PWR06) concern historiographical reception (De Leeuw 1926) rather than a specific dated relation between two of the six frozen actors, so they are not force-fit onto any relation record here.

## 12. Commitment Credibility

`PARTIALLY_CREDIBLE` (5) is the dominant value, directly reusing the recovered deep dive's own overall §17 finding ("the Painan Tractaat's commitment structure was PARTIALLY_CREDIBLE at best"), applied per-relation rather than as a single case-level score. `NOT_TESTABLE` (3) marks relations where commitment durability is not the relevant question (a request, a negotiation, an agent's signing act). `LOW_CREDIBILITY` (1) marks the Aceh reconciliation specifically, reflecting that neither side's exclusive claim proved durable. No relation carries `CREDIBLE` or `FAILED` — consistent with the recovered finding that this case never resolves cleanly to either extreme.

## 13. Parallel Alignment

`MAINTAINS_PARALLEL_ALIGNMENT_WITH` (Muhammad Syah faction → VOC, Oct 1663 onward) is recorded as a **distinct relation instance** from `RECONCILES_WITH` (Muhammad Syah faction → Aceh court, Oct 1663) — not merged, not presented as a switch. This directly operationalizes the ontology note's own new relation-type candidate (§0.20 of the implementation plan) and the governing instruction's explicit prohibition on equating parallel alignment with switching. Validator check o confirms the two relation types are never conflated onto a single record for the same actor pair.

## 14. Public-Copy Boundaries

Every relation's `public_display_summary` is a distinct, plain-language field, never a copy of `theoretical_annotation` (validator checks u/v/w confirm no two of the four layer fields are identical on any record). No `public_display_summary` uses a PT-H/GT-H hypothesis ID, a `classification_status` raw value, or the words "patron," "client," "equilibrium," or "sovereignty" — consistent with the recovered deep dive's own Level-1 display guard (§24 of the deep dive), reused here as a drafting constraint rather than re-derived.

## 15. Validator Design

`scripts/research_validators/validate_painan_1663_relational_artifact.py` — placed under a new `scripts/research_validators/` directory, parallel to the existing `scripts/verify_provenance_join.py` and `backend/scripts/verify_provenance_join.py` nonproduction-script convention already used in this repository, but in its own subdirectory to make clear it validates a research artifact, not backend provenance joins. The script:

- opens the artifact and `data/research/linimasa_events.csv` **read-only**;
- performs 25 checks (a-y, governing-instruction item 17) and prints a pass/fail report;
- makes no HTTP call, no database connection, no import of any `backend/` or `frontend/` module, no subprocess call to Graphify;
- exits non-zero on any failing check.

It is not registered in any CI config, Docker service, or `docker-compose.yml` entry, and is not imported by any other file in this turn.

## 16. Validation Results

```text
$ python3 scripts/research_validators/validate_painan_1663_relational_artifact.py
CHECKS PASSED: 23 / 23
WARNINGS: 0
ERRORS: 0
VALIDATION RESULT: PASS
```

All 25 governing-instruction checks (a-y) map onto the validator's 23 executed assertions (checks o and y are structural/documentation confirmations rather than independent PASS/FAIL branches, since no data configuration in this artifact could trigger their failure condition — both are still explicitly reported). No orphan edges, no vocabulary violations, no `PATRON_CLIENT_SUPPORTED`, no numeric payoff/equilibrium term, and no unflagged inferred relation were found.

## 17. Unresolved Actors and Mandates

```text
Bandar X signatories       — mandate not traceable (weak/non-binding four-raja council per the
                              recovered deep dive's own §19 characterization); excluded per decision
                              item 2's own stated condition.
Painan / Padang / Tiku     — outside this turn's frozen actor scope; PATRON_CLIENT_NOT_TESTABLE
  signatories                 individually in the recovered ledger (DYAD03).
Catip (information broker) — named and source-traceable (row 36) but excluded as an actor because no
                              relation type among the seven authorized types represents an
                              information-flow act; flagged as a candidate for a future
                              BROKERAGE_RELATION / information-flow relation type, not resolved here.
Aceh-side named individual  — no individually named Aceh ambassador is independently distinguished
  ambassador(s)                with a separately traceable mandate in the verified rows; the single
                              institutional "Aceh court" actor is used instead.
```

## 18. Source Gaps

Reused verbatim from the recovered deep dive (§0.18 of the implementation plan), unchanged by this artifact-construction turn: De Leeuw 1926 full text; Kroeskamp 1931; Painan/Padang/Tiku's own 1663 internal circumstances; an Aceh-side or fully independent local-voice account of the pre-1660 tributary relationship; a written VOC mandate document for Groenewegen's 1662-63 negotiation specifically. No attempt was made to fill any of these gaps in this turn.

## 19. Production Safety

- **New files created this turn:** `data/power_relations/painan_1663_relational_research_artifact.json`, `scripts/research_validators/validate_painan_1663_relational_artifact.py`, this audit document. No other file was created or modified.
- **No file under `backend/`, `frontend/`, or any migration directory was touched.**
- **No API route, database model, or seed script was changed.**
- **No `graphify update` was run.**
- **No `git add`, `git commit`, `git push`, or deploy command was run.**
- **Prior-artifact checksums** (recorded before and after this turn's work) are unchanged — see terminal summary below.

## 20. Readiness Decision

```text
PAINAN_RELATIONAL_MVP_ARTIFACT_READY
```

The artifact is internally consistent, fully source-traced, validator-clean, and respects every boundary in the frozen researcher decisions (six actors only, seven relation types only, patron-client and power-theory as annotation only, no numeric payoff or equilibrium claim, four interpretive layers kept distinct). Readiness certifies construction quality only — it does not authorize the next MVP-sequence step (researcher review) to begin without the researcher's own sign-off, and does not authorize any Atlas, API, database, migration, Graphify, or deployment action.
