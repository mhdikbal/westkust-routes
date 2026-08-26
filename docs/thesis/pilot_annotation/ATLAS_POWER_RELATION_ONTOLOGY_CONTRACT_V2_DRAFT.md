# ATLAS POWER-RELATION ONTOLOGY CONTRACT — V2 DRAFT

> **DESIGN DRAFT ONLY — NO SCHEMA, MIGRATION, OR API CHANGE AUTHORIZED**
> Supersedes nothing; extends `ATLAS_POWER_RELATION_DATA_CONTRACT_DRAFT.md` (V1) with the findings of the twelve-case cross-case review (`CROSS_CASE_POWER_ONTOLOGY_REVIEW.md`). V1's own controlled vocabularies (`provenance_status`, `evidence_strength`, `interpretive_status`, `claim_or_effective_control`, `explicit_or_inferred`) are reused verbatim throughout — none is redefined here.

## 1. Entity Definitions

Reused from V1's own 21-entity list plus this review's own decisions (`CROSS_CASE_ENTITY_DECISION_LEDGER.csv`, 23 classes reviewed):

```text
KEEP_AS_FIRST_CLASS_ENTITY (candidate V2 tables):
  Actor, Institution, IndividualOfficeHolder, Location, Treaty, HistoricalEvent,
  ParentEpisode, Claim, PowerRelation, EffectiveControlObservation

KEEP_AS_ROLE_OR_ATTRIBUTE (fields on the above, not separate tables):
  ActorFaction (attribute of Actor, with an optional persistent faction_id per §11 of the review),
  PoliticalOffice (source_term + normalized_label pair, attached to IndividualOfficeHolder),
  Broker (boolean/role flag on a NEGOTIATES_WITH relation, with an evidence_type sub-field),
  Port / Fort / Mine (Location subtype attribute), Commodity (attribute of monopoly/toll relations),
  Obligation / BreachAllegation (paired free-text fields on a PowerRelation or Treaty)

KEEP_RESEARCH_ONLY (not exposed at Level 1/2):
  NamedCollective, DocumentaryReport, StrategicInteraction

REQUIRES_MORE_EVIDENCE (not modeled in V2 pending further case work):
  Community
```

## 2. Relation Definitions

Per the cross-case relation ledger (`CROSS_CASE_RELATION_DECISION_LEDGER.csv`, 21 types reviewed):

```text
MVP_CORE_RELATION (candidate V2 relation_type controlled vocabulary, 14 values):
  REQUESTS_PROTECTION_FROM, PROVIDES_PROTECTION_TO, REQUIRES_MONOPOLY_FROM, NEGOTIATES_WITH,
  RECONCILES_WITH, SWITCHES_ALIGNMENT_TO, CLAIMS_JURISDICTION_OVER, CLAIMS_COMMODITY_MONOPOLY,
  CONTESTS_SUCCESSION_WITH, CONTESTS_RESOURCE_WITH, RECOGNIZES_OFFICE_HOLDER,
  COLLECTS_TOLL_FROM, LEASES_RESOURCE_TO, USES_MILITARY_FORCE_AGAINST

EXTENDED_RESEARCH_RELATION (available, not MVP):
  EXERCISES_EFFECTIVE_CONTROL_OVER, CONTROLS_FORT

CASE_SPECIFIC_ONLY (not generalized without further evidence):
  CONTROLS_PORT, DISMISSES_OFFICE_HOLDER (subject-type correction needed -- evidenced instances
  in this review's case set are LOCALLY-initiated, not institution-initiated)

REQUIRES_MORE_EVIDENCE:
  MAINTAINS_PARALLEL_ALIGNMENT_WITH (confirmed PAINAN_SPECIFIC, not cross-case stable, per the
  review's own §16 finding -- retained for Painan's own use, not extended elsewhere without new
  evidence), APPOINTS_OFFICE_HOLDER (zero clear instances across 12 cases)

ANNOTATION_NOT_RELATION (demoted):
  IMPOSES_PUNITIVE_CLASSIFICATION_ON (source-specific rhetoric, not a stable directed relation --
  see the review's own §18 finding)
```

`MAINTAINS_PARALLEL_ALIGNMENT_WITH` MUST NOT be applied to any case in V2 without the same double-instantiation evidence bar Painan met (two independently-dated, concurrently-valid relations to different patrons) — inferring it from sequential contacts alone is explicitly prohibited, per the review's own §16.

## 3. Annotation Definitions

All 17 items reviewed in `CROSS_CASE_ANNOTATION_DECISION_LEDGER.csv` are **KEEP_AS_ANNOTATION**, none promoted:

```text
PATRON_CLIENT_CLASSIFICATION, POWER_DIMENSION, IEMP_POWER_SOURCE, COMMITMENT_CREDIBILITY,
RESISTANCE_CANDIDATE, EVIDENCE_STRENGTH, PROVENANCE_STATUS, INTERPRETIVE_STATUS,
SOURCE_ASYMMETRY, CLAIM_OR_EFFECTIVE_CONTROL, REPEATED_COERCION, FAILED_DETERRENCE,
PROTECTION_BARGAIN, VOC_JURISDICTIONAL_EXPANSION, LOCAL_AUTONOMY_DEFENSE,
COMMERCIAL_STRATEGY, FACTIONAL_CONFLICT
```

Promotion criteria (unchanged from the governing plan §22, reused verbatim): identifiable subject, identifiable object, direction, temporal range, source locator, observable historical action, cross-case usefulness — ALL SEVEN required simultaneously. No annotation in this V2 draft meets all seven; each fails on at least one (most commonly: no independent temporal range distinct from the relation it describes, or no cross-case usefulness demonstrated beyond a single case).

## 4. Identity Rules

```text
Actor:            requires >=1 named individual OR an explicitly bounded, source-described group
                  (e.g. "12 desa pongelous"); a bare place name is never sufficient (Actor-vs-Location
                  guard, review §8 -- Pariaman is the confirmed failure-mode case to avoid repeating)
ActorFaction:     persistent faction_id only if membership/leadership traceable, temporal scope
                  boundable, not a retrospective label, source basis recorded (2 of 6 tested
                  candidates in the review meet this; see review §9)
Broker:           evidence_type required from the 8-item list in the governing plan §12; repeated
                  appearance alone is explicitly insufficient
PoliticalOffice:  original source term ALWAYS preserved alongside any normalized label; VOC-period
                  terms never equated with 19th-century statutory offices
```

## 5. Temporal Rules

```text
Every PowerRelation candidate carries: valid_from, valid_to, date_precision, open_ended,
  observed_at, superseded_by, contradicted_by (per the governing plan §26, reused verbatim)
Overlapping relations for the same subject/object pair are PERMITTED and, per CASE-01/CASE-03,
  EXPECTED -- never forced to one relation per actor/location per year
A DocumentaryReport's own date (e.g. a retrospective memoir passage) is always kept distinct from
  the HistoricalEvent date(s) it describes -- CASE-04's Vogel-only rows are the model illustration
  of why this separation is load-bearing, not cosmetic
```

## 6. Evidence Contract

Reused verbatim from V1 and the Painan artifact's own already-validated schema, extended with `parent_episode_ids` (present in the 79-row interpretive ledger, not yet in the artifact-level schema):

```text
source_document_ids, source_passage_locator, event_ids, parent_episode_ids, provenance_status,
evidence_strength, interpretive_status, explicit_or_inferred, researcher_review_required
```

Four-layer text contract (reused verbatim, already validated in the Painan artifact's own prototype):

```text
source_statement_summary, historical_reconstruction, theoretical_annotation, public_display_summary
```

No layer may be auto-generated into another without explicit review — zero violations of this rule were found anywhere in the material examined by this review.

## 7. Claim/Control Model

Reused verbatim from V1 (10-value `claim_or_effective_control` vocabulary): `CLAIM | FORMAL_ACCEPTANCE | TREATY_OBLIGATION | MILITARY_PRESENCE | FORT_CONTROL | COMMERCIAL_CONTROL | ADMINISTRATIVE_CONTROL | EFFECTIVE_LOCAL_COMPLIANCE | CONTESTED_CONTROL | UNKNOWN_EFFECTIVE_CONTROL`. Never derived from treaty signing alone (enforced across all 12 cases reviewed, §14 of the review). A future implementation must never render a `CLAIM`-type relation with the same visual weight as an `EFFECTIVE_LOCAL_COMPLIANCE`-type relation without an explicit distinguishing indicator, per V1's own §6 enforcement principle, reused unchanged.

## 8. Contradiction Handling

Reused from the review's own §26 draft policy: retain competing source readings side by side (never average or pick a winner); give retrospective multi-event summaries per-member evidence assessment, not a uniform inherited confidence; mark contested mandate `CANNOT_DETERMINE` explicitly with competing hypotheses in notes. **Contradictions are never resolved by majority vote.** Independent corroboration upgrades only the specifically-corroborated layer (existence/mechanism), never the uncorroborated layer (exact date, named actor) by association.

## 9. Public-Display Mappings

Candidate public vocabulary (per the governing plan §30, not yet researcher-approved):

```text
Perlindungan               <- REQUESTS_PROTECTION_FROM, PROVIDES_PROTECTION_TO
Negosiasi                  <- NEGOTIATES_WITH
Perjanjian dan kewajiban   <- Treaty, Obligation, RECOGNIZES_OFFICE_HOLDER
Klaim yurisdiksi           <- CLAIMS_JURISDICTION_OVER
Kehadiran militer          <- USES_MILITARY_FORCE_AGAINST
Kontrol benteng            <- CONTROLS_FORT, FORT_CONTROL-valued claim/control observations
Penguasaan dagang          <- REQUIRES_MONOPOLY_FROM, CLAIMS_COMMODITY_MONOPOLY, COLLECTS_TOLL_FROM,
                               LEASES_RESOURCE_TO
Aliansi atau perubahan hubungan <- SWITCHES_ALIGNMENT_TO, RECONCILES_WITH
Hubungan yang masih diperdebatkan <- CONTESTED_CONTROL-valued relations; interpretive_status=CONTESTED
```

No raw theoretical label (`PT-H*`, `GT-H*`, `classification_status` value, mechanism-annotation name) may appear at this public layer under any future implementation — reused verbatim from the Painan artifact's own already-enforced Level-1 guard.

## 10. Research-Only Fields

All 17 annotation types in §3 above; `StrategicInteraction`, `DocumentaryReport`, `NamedCollective` entities; the full patron-client and power-theory finding sets for every case; `MAINTAINS_PARALLEL_ALIGNMENT_WITH`'s own intentionality question (deliberate hedging vs. reactive improvisation, unresolved for Painan itself); the Sire-Narra/Gouverneur-Pouti and Sulthan-Bagindo/hoofdregent-Baginda identity hypotheses.

## 11. Validation Requirements

A future generalized relation validator (not built by this review) should, at minimum, replicate every check already proven in `validate_painan_1663_relational_artifact.py` (unique actor/relation IDs, no orphan endpoints, relation_type restricted to the frozen MVP set, controlled-vocabulary conformance, no `PATRON_OF`/`CLIENT_OF` edges, no numeric payoff/equilibrium language, four-layer separation, inferred-relation review-flagging) generalized across an arbitrary case rather than hardcoded to Painan's 6 actors and 9 relations.

## 12. Migration Non-Authorization

No migration is authorized by this draft, this review, or any prior artifact it reuses. `linimasa_events.csv` and all Phase B/C/D artifacts remain unmodified and are not proposed for modification here.

## 13. Graphify Non-Authorization

No Graphify execution is authorized by this draft. Per the review's own §28, Graphify readiness requires reviewed relation types (proposed, not frozen, by this draft), source-linked temporal edges beyond Painan alone, and explicit uncertainty fields extended to at least the 4 cases named in the accompanying Validation Plan — none of which exist yet.

## 14. Production Gate

Reused verbatim from the review's own §29: 8 items, 0 currently passing in full, 1 partially addressed (public-copy category proposal, §9 above, not yet researcher-approved). Production integration remains fully blocked pending researcher action on all 8 items.
