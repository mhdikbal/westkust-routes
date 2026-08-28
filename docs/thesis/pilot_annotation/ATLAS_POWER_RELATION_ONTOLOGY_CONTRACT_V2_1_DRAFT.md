# ATLAS POWER-RELATION ONTOLOGY CONTRACT — V2.1 DRAFT

> **DESIGN DRAFT ONLY — NO SCHEMA, MIGRATION, OR API CHANGE AUTHORIZED**
> Supersedes nothing. `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` (Draft V2, sha256 `f43b1f9fcee75e7a7271994905b676616470271f89dd99d62a6758f1c4b3cd37`) remains the frozen baseline, unmodified by this document. Draft V2.1 extends it with the 18-decision researcher adjudication recorded in `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv` (0 PENDING) and its closing audit, `POST_V1_V4_COMPLETE_RESEARCHER_DECISION_AUDIT.md`. **PACKAGE: BALANCED** (per DEC-14). This document preserves Draft V2's own 14 section numbers and headers unchanged — every prior document that cites "Draft V2 §N" continues to resolve correctly against this draft. Every addition below is additive and optional; nothing here renames, removes, or redefines any Draft V2 component.

## 0. Schema-Authorship Note

The researcher decision ledger approved, per decision, **a direction — not a copy-paste-ready schema fragment** (audit §21). Two things below are quoted **verbatim** from `researcher_notes` and must not be altered without reopening the underlying decision: the `RightModification` action vocabulary (`GRANTS, WAIVES, RELEASES, REVOKES, RENEWS, EXEMPTS`, DEC-04) and the constrained-agency field *names* (`dependency_status, coercion_status, ability_to_refuse, voice_availability, political_intent, constrained_agency`, DEC-10). Everything else at field/cardinality level — `CommercialRight`'s exact field list, `CommandObservation`/`OperationParticipation`'s exact field list, the internal shape of `mandate_status`/`mandate_scope` — is this document's own first-pass construction, built by direct analogy to Draft V2's own already-frozen patterns (§5 Temporal Rules, §6 Evidence Contract, reused verbatim rather than reinvented). These are flagged here for researcher review specifically, separately from the already-decided DEC items they implement.

## 1. Entity Definitions

Unchanged from Draft V2 except `KEEP_RESEARCH_ONLY`, which grows from 3 to 7:

```text
KEEP_AS_FIRST_CLASS_ENTITY (unchanged, 10 classes):
  Actor, Institution, IndividualOfficeHolder, Location, Treaty, HistoricalEvent,
  ParentEpisode, Claim, PowerRelation, EffectiveControlObservation

KEEP_AS_ROLE_OR_ATTRIBUTE (unchanged from Draft V2 §1)

KEEP_RESEARCH_ONLY (extended, 3 -> 7):
  NamedCollective, DocumentaryReport, StrategicInteraction                  [Draft V2, unchanged]
  CommercialRight, RightModification                                       [NEW -- DEC-04]
  CommandObservation, OperationParticipation                                [NEW -- DEC-09/DEC-10]

REQUIRES_MORE_EVIDENCE (unchanged, 1 class):
  Community
```

No entity is promoted out of `KEEP_RESEARCH_ONLY` by this draft. See §16 for entities explicitly considered and **not** added.

## 2. Relation Definitions

**UNCHANGED IN FULL.** Zero new `relation_type` values in either `MVP_CORE_RELATION` (14) or `EXTENDED_RESEARCH_RELATION` (2). This is a decided fact, not an omission: DEC-04 explicitly rejects "one new relation type per privilege," and DEC-09 explicitly rejects encoding `ALLY_OF`, `VOLUNTARILY_SUPPORTS`, loyalty, or political consent as any relation type. Both CH-03 and CH-07 land as entities/fields (§4 below), never as new directed relations, specifically to avoid a relation type being read as implying consent or voluntary alliance.

## 3. Annotation Definitions

The 17-type list from Draft V2 §3 is **unchanged** — no new annotation type is added. `resistance_candidate` gains one new optional field (§4 below); this is a field-level extension of an existing type, not a new type, and does not change the count of 17.

## 4. Identity Rules

Draft V2's four existing identity rules (`Actor`, `ActorFaction`, `Broker`, `PoliticalOffice`) are unchanged. Four new subsections follow.

### 4a. Actor — Identity Continuity and Mandate (DEC-01/DEC-02/DEC-03)

```text
Actor gains 4 OPTIONAL fields:
  mandate_status              semi-structured guided-text, NOT a closed enum (DEC-03 -- avoids
                               overfitting mandate categories to only the 4 cases examined so far);
                               valid values include CANNOT_DETERMINE / NOT_TESTABLE, never forced
                               into a category
  mandate_scope                same guided-text discipline as mandate_status; must remain bounded
                               by both scope and time
  identity_continuity_status   semi-structured guided-text; CANNOT_DETERMINE / NOT_TESTABLE remain
                               valid values
  explicit_non_identity_with   list of {actor_id, rationale}; symmetric (A non-identical-to B implies
                               B non-identical-to A); an actor MUST NOT list itself; doubles as the
                               mechanism for "tested and explicitly judged non-identical" (DEC-02,
                               folded into this single field rather than a separate schema element)
```

Safeguards (verbatim discipline from DEC-01/02/03, non-negotiable): no automatic actor merge under any circumstance; actor merge requires manual researcher approval; `explicit_non_identity_with` must prevent silent merging, never permit it; unknown continuity/mandate remains unknown, never inferred; no in-place rewriting of any frozen V1–V4 artifact. Rejected explicitly by the ledger: a new first-class `ActorContinuityClaim` entity (over-engineered); a closed `mandate_status` enum (overfitting risk); separate `possible_predecessor_actor_ids`/`possible_successor_actor_ids` fields (describes a different relationship — temporal succession — than non-identity; Sillida's own office-succession test passed without them, kept as a future, separately-evaluated candidate only if a genuine succession-chain failure is found).

### 4b. CommercialRight / RightModification (DEC-04)

Researcher-selected direction: a structured object pair, not the changeset draft's own original Option A recommendation (a single `right_status` field on existing toll/monopoly relations). Explicit boundaries carried verbatim from DEC-04: never one new relation type per right-action; never reverse `COLLECTS_TOLL_FROM` to represent an exemption; never equate a trade privilege with sovereignty or effective control (§7 stays untouched — a `CommercialRight` is never a `claim_or_effective_control` value).

```text
CommercialRight (KEEP_RESEARCH_ONLY entity):
  right_id                    unique identifier
  holder_actor_id              the Actor holding the right
  granting_actor_id            the Actor/Institution recognizing or granting the right, if evidenced
  concerns_relation_type        which existing MVP_CORE_RELATION this right concerns (e.g.
                               COLLECTS_TOLL_FROM, CLAIMS_COMMODITY_MONOPOLY, LEASES_RESOURCE_TO) --
                               a reference into Draft V2 section 2's own frozen vocabulary, not a new
                               vocabulary of its own
  commodity                   reuses the existing Commodity attribute (Draft V2 section 1), not
                               redefined here
  <evidence contract fields>  source_document_ids, source_passage_locator, event_ids,
                               parent_episode_ids, provenance_status, evidence_strength,
                               interpretive_status, explicit_or_inferred, researcher_review_required
                               -- reused verbatim from Draft V2 section 6, no new vocabulary
  valid_from, valid_to, date_precision, open_ended  -- reused verbatim from Draft V2 section 5

RightModification (KEEP_RESEARCH_ONLY entity):
  modification_id              unique identifier
  right_id                     references the CommercialRight this modification acts upon
  action                       ENUM, exactly 6 values, quoted VERBATIM from DEC-04's own
                               researcher_notes: GRANTS | WAIVES | RELEASES | REVOKES | RENEWS |
                               EXEMPTS
  acting_actor_id               the Actor/Institution performing the action
  affected_actor_id             the Actor whose right this action affects (usually, not always, the
                               same as CommercialRight.holder_actor_id -- modeled separately to leave
                               room for a mediated/third-party modification without forcing one)
  modification_date, date_precision  reused verbatim from Draft V2 section 5
  <evidence contract fields>   reused verbatim from Draft V2 section 6, same as CommercialRight
```

Rejected explicitly by the ledger: a new relation type per right-action (proliferation, directly violates the plan's own hard rule); no-change (leaves a 3x-cross-case-corroborated gap unaddressed). Sillida's own third-party fine (1679) is explicitly NOT modeled here — see §16, it belongs to the deferred `DisputeSettlement` family (DEC-11), not to `RightModification`, because a punitive arbitration outcome is not the same historical shape as a voluntary rights-release.

### 4c. CommandObservation / OperationParticipation (DEC-09/DEC-10)

Researcher-selected direction: a structured object pair, not the changeset draft's own original recommendation (fields added directly onto the existing `EffectiveControlObservation` entity). The core safety rationale is unchanged regardless of which shape was chosen: **no directed relation type may ever imply consent or voluntary alliance for a coerced actor.**

```text
CommandObservation (KEEP_RESEARCH_ONLY entity):
  observation_id                unique identifier
  commanding_actor_id            the Actor/Institution issuing command
  commanded_actor_id             the Actor/NamedCollective subject to command
  coercion_status                ENUM: FREE | COERCED | CANNOT_DETERMINE
  ability_to_refuse              ENUM: YES | NO | CANNOT_DETERMINE
  dependency_status               semi-structured guided-text (DEC-10 -- same overfitting-avoidance
                                  discipline as mandate_status/mandate_scope; not a closed enum,
                                  since this field's exact value space is not yet evidenced beyond
                                  one case)
  voice_availability              ENUM: DOCUMENTED | ABSENT | CANNOT_DETERMINE
  constrained_agency               ENUM: CONFIRMED | SUSPECTED | NOT_APPLICABLE | CANNOT_DETERMINE
                                  (summary assessment field, distinct from coercion_status --
                                  DEC-10 lists it as its own named field)
  political_intent                 FREE TEXT ONLY -- explicitly, per DEC-10, NEVER a controlled
                                  vocabulary; must allow explicit CANNOT_DETERMINE as a value; exists
                                  so the model can never force a premature loyalty/resistance
                                  classification the sources do not support
  <evidence contract + temporal fields>  reused verbatim from Draft V2 sections 5/6

OperationParticipation (KEEP_RESEARCH_ONLY entity):
  participation_id               unique identifier
  command_observation_id          references the governing CommandObservation
  participant_actor_id            the Actor/NamedCollective member participating
  event_id or parent_episode_id   the HistoricalEvent/ParentEpisode this participation concerns
                                  (Draft V2's own entities, not redefined)
  role_as_written                 free text, original source term preserved (per Draft V2 section 4
                                  PoliticalOffice discipline: source term never silently normalized
                                  away)
  <evidence contract fields>      reused verbatim from Draft V2 section 6
```

**Non-negotiable safety rule** (carried forward from the changeset draft's own CH-07 rationale, retargeted at this entity pair): a `commanding_actor_id`/`commanded_actor_id` pair recorded in a `CommandObservation` must **never** simultaneously appear as the subject/object of any `relation_type` in `PowerRelation`. Without this check enforced, the entire safety rationale for choosing an observation entity over a directed relation type is unenforced. See §11.

Rejected explicitly by the ledger: encoding `ALLY_OF`, `VOLUNTARILY_SUPPORTS`, loyalty, or political consent in any form; `DIRECTS_OPERATION_BY`/`DEPLOYS_GROUP_IN`/`COMMANDS_UNIT` as new relation types (the changeset draft's single most consequential rejection — any directed relation type between a commanding institution and a coerced group risks being read, or later reused, as implying a normal command-and-compliance relationship structurally similar to a voluntary one); a closed `political_intent` enum.

### 4d. resistance_candidate — Target Extension (DEC-08)

```text
resistance_candidate (existing annotation, Draft V2 section 3) gains 1 OPTIONAL field:
  resistance_target_actor_id     single actor_id (not a list -- no case yet demonstrates a need
                                 beyond one target-actor reference), used ONLY when the resistance
                                 target differs from the relation's own object
```

Safeguards: field remains optional, never required; `resistance_candidate` remains Research-Only throughout (Draft V2 §3/§9, unchanged) — this field does not promote resistance to a public category; no automatic inference of a target where the source is ambiguous, `CANNOT_DETERMINE` remains valid. Rejected explicitly by the ledger: `resistance_target_relation_type` or `resistance_scope` (no case in the four validation artifacts demonstrates a need beyond a single target-actor reference; deferred to `REQUIRES_MORE_EVIDENCE`).

## 5. Temporal Rules

**UNCHANGED.** All new entities (§4b, §4c) and the extended `Actor`/`resistance_candidate` fields (§4a, §4d) reuse Draft V2 §5's `valid_from`/`valid_to`/`date_precision`/`open_ended`/`observed_at`/`superseded_by`/`contradicted_by` contract verbatim. No new temporal vocabulary is introduced.

## 6. Evidence Contract

**UNCHANGED.** Every new entity in §4 reuses the Draft V2 §6 evidence fields (`source_document_ids, source_passage_locator, event_ids, parent_episode_ids, provenance_status, evidence_strength, interpretive_status, explicit_or_inferred, researcher_review_required`) and the four-layer text contract (`source_statement_summary, historical_reconstruction, theoretical_annotation, public_display_summary`) verbatim. No new evidence vocabulary is introduced.

## 7. Claim/Control Model

**UNCHANGED.** The 10-value `claim_or_effective_control` vocabulary is untouched. `CommercialRight` (§4b) is explicitly and deliberately kept outside this vocabulary — per DEC-04, a trade privilege must never be equated with sovereignty or effective control.

## 8. Contradiction Handling

**UNCHANGED.** All new entities inherit Draft V2 §8's contradiction-handling policy verbatim (competing source readings retained side by side, never averaged; independent corroboration upgrades only the specifically-corroborated layer).

## 9. Public-Display Mappings

**UNCHANGED.** DEC-12 confirms none of the 8 proposed changes introduces a new public-facing category. No entry in §4 above appears in this mapping.

## 10. Research-Only Fields

Extended (per DEC-16, which explicitly binds these exact elements). All items below remain Research-Only until independently re-evaluated for public-display promotion under the existing 7-simultaneous-criteria discipline (Draft V2 §3) — a review this draft does not itself perform:

```text
All items already listed in Draft V2 section 10, unchanged, PLUS:
  CommercialRight, RightModification                                         (DEC-04)
  CommandObservation, OperationParticipation                                  (DEC-09/DEC-10)
  Actor.mandate_status, Actor.mandate_scope, Actor.identity_continuity_status,
    Actor.explicit_non_identity_with                                         (DEC-01/02/03)
  resistance_candidate.resistance_target_actor_id                            (DEC-08)
```

No automatic promotion occurs on adoption of this draft; no promotion merely because an entity is structurally well-formed or already implemented; promotion requires re-evaluation against all 7 criteria simultaneously, not a subset; manual researcher review required for any future promotion attempt.

## 11. Validation Requirements

Extended. A future generalized relation validator (not built by this draft) should, at minimum, replicate every check already listed in Draft V2 §11, **plus**:

```text
NEW CHECK (DEC-01/02): explicit_non_identity_with pairs are symmetric (A lists B implies B lists A)
  and no actor_id lists itself.
NEW CHECK (DEC-09/10, SAFETY-CRITICAL): no relation_type in PowerRelation ever references the same
  actor_id pair as a CommandObservation's commanding_actor_id/commanded_actor_id. Without this
  check, CommandObservation's entire safety rationale (foreclosing consent-implying misuse) is
  unenforced.
```

## 12. Migration Non-Authorization

**Reaffirmed, unchanged.** No migration is authorized by this draft. `linimasa_events.csv` and all Phase B/C/D artifacts remain unmodified. Per DEC-14: original V1–V4 artifacts remain immutable; any future migrated artifact will be written as a new file, never an in-place rewrite of a frozen artifact.

## 13. Graphify Non-Authorization

**Reaffirmed, unchanged (DEC-17).** No Graphify execution is authorized by this draft. None of the changes in §4 alters Draft V2 §13's own readiness requirements (reviewed, frozen relation types across ≥4 cases) — this draft proposes zero new relation types (§2), so Graphify readiness is, if anything, unaffected in either direction.

## 14. Production Gate

**Reaffirmed, unchanged (DEC-18).** The 8-item Production Gate from Draft V2 §14 is unaffected by this draft. Production integration remains fully blocked.

## 15. Change Provenance

Every new element in this draft, traced to its exact decision:

| Element | Decision(s) | Disposition |
|---|---|---|
| `Actor.mandate_status`, `Actor.mandate_scope` | DEC-01, DEC-03 | APPROVED_WITH_LIMITATIONS |
| `Actor.identity_continuity_status`, `Actor.explicit_non_identity_with` | DEC-01, DEC-02 | APPROVED_WITH_LIMITATIONS |
| `CommercialRight`, `RightModification` | DEC-04 | APPROVED_WITH_LIMITATIONS (structured object selected) |
| `resistance_candidate.resistance_target_actor_id` | DEC-08 | APPROVED_WITH_LIMITATIONS |
| `CommandObservation`, `OperationParticipation` | DEC-09 | APPROVED_WITH_LIMITATIONS (structured object pair selected) |
| `coercion_status`, `ability_to_refuse`, `voice_availability`, `dependency_status`, `constrained_agency`, `political_intent` | DEC-10 | APPROVED_WITH_LIMITATIONS |
| No new public category (§9 unchanged) | DEC-12 | APPROVED |
| Additive/optional-only design (§17 backward compatibility, unchanged from Draft V2 pattern) | DEC-13 | APPROVED |
| Version name: V2.1, not V3 | DEC-14 | DRAFT_V2_1 |
| Revalidation scope: all 5 artifacts, Painan as clean baseline | DEC-15 | APPROVED |
| Research-only boundary on all 4 new entities | DEC-16 | APPROVED_WITH_LIMITATIONS |
| Graphify deferral continues (§13) | DEC-17 | APPROVED |
| Production gate continues (§14) | DEC-18 | APPROVED |

## 16. Explicitly Excluded

Three change families considered by the changeset draft do **not** appear anywhere above. Their absence is a decision, not an oversight:

```text
CH-04 (institutional state and presence)  -- DEC-05/DEC-06: DEFERRED.
  No InstitutionalObservation model, unified or split, is proposed. A future, separate
  design-exploration turn is required before any specific change is proposed here.

CH-05 (ambiguous spatial feature)         -- DEC-07: REJECTED.
  No source_place_expression / feature_type_confidence / spatial_scope_status field is added to
  Location. Sillida V4's own successful 6-location model, using only the existing Location entity,
  is direct evidence the existing model already suffices. A non-ontology source re-check of Vogel's
  "Refort" usage was authorized instead, entirely outside this draft's own scope.

CH-08 (dispute settlement)                -- DEC-11: DEFERRED (explicit researcher override,
  provenance preserved in the decision ledger).
  No DisputeSettlement entity is added. Evidence rests on one principal case (Sillida V4's own 1679
  Bayang-Sillida fine); the proposed object has the highest schema-to-evidence ratio of any change
  considered; a second, sufficiently independent case is required before reconsideration. The 1679
  fine detail remains representable only as free-text relation notes. Deferral does not reject the
  historical phenomenon itself.
```

## 17. Backward Compatibility

**Reaffirmed (DEC-13).** All changes in §4 are additive/optional. All 5 existing validated artifacts (Painan, Natal, Koto Tangah, Tiku, Sillida) remain valid without modification under this draft. No existing entity, relation type, annotation, or field is renamed, removed, or redefined. This draft is a new file; `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` is not edited and its checksum is unchanged.

## 18. Remaining Preconditions Before Any Implementation

None of the following is authorized or begun by this draft (per the decision audit's own §21, still applicable):

```text
[ ] generalized-validator implementation (currently PLANNED_ONLY, no executable exists)
[ ] artifact migration plan execution for the 5 V1-V4 artifacts as new, separate files
[ ] multi-case prototype (does not currently exist)
[ ] revalidation-matrix execution (10 planned in ATLAS_POWER_RELATION_V2_1_REVALIDATION_MATRIX.csv,
    0 executed)
[ ] Graphify activation
[ ] any Atlas/backend/frontend/API/database/production change
```

This draft authorizes construction of the contract document itself — nothing more. Implementation, migration, Graphify, and production integration all remain `NOT_AUTHORIZED`.
