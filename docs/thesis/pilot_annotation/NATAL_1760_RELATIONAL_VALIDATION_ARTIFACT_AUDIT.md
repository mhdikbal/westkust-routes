# NATAL 1760 RELATIONAL VALIDATION ARTIFACT — AUDIT

> **RESEARCH-ONLY NONPRODUCTION AUDIT.** Documents the construction and validation of the first of four planned ontology validation cases (V1: Natal 1760), per `CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md`. This audit does not modify `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md`, the Painan artifact, or any prior artifact.

## 1. Scope

This turn builds and validates exactly one artifact set: the Natal 1760 relational validation artifact, its dedicated validator, an ontology stress-test ledger, and this audit. Its purpose is to test whether the frozen `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` (V2 Draft) can represent Natal 1760's own documented complexity — not to adjust the Draft so Natal fits it. No new historical research was performed; all source material is restricted to what Batch I9 already approved (CD6 traktat MXXVI p.210, CD6 traktat MXXXI p.223, the already-verified GM Deel13 corroboration, and `docs/cd_resistance_signal_candidates.csv` row 21). V2 (Koto Tangah), multi-case prototyping, and any commit/push/deploy action are explicitly out of scope for this turn.

## 2. Frozen Ontology Target

The validation target is `docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` (162 lines), unmodified throughout this turn (checksum verified unchanged before and after, see §3). Its entity set (10 KEEP_AS_FIRST_CLASS_ENTITY, 9 KEEP_AS_ROLE_OR_ATTRIBUTE, 3 KEEP_RESEARCH_ONLY, 1 REQUIRES_MORE_EVIDENCE), relation set (14 MVP_CORE_RELATION, 2 EXTENDED_RESEARCH_RELATION, 2 CASE_SPECIFIC_ONLY, 2 REQUIRES_MORE_EVIDENCE, 1 ANNOTATION_NOT_RELATION), 17-item frozen annotation list, 10-value claim/control vocabulary, and identity/temporal rules were treated as fixed constraints, not adjustable parameters.

## 3. Inputs and Integrity

Eleven frozen/protected files were checksummed (SHA-256) before this turn's construction work began and reverified identical afterward:

| File | Status |
|---|---|
| `data/power_relations/painan_1663_relational_research_artifact.json` | unchanged |
| `research_prototypes/painan_1663_relational/index.html` | unchanged |
| `research_prototypes/painan_1663_relational/prototype.js` | unchanged |
| `research_prototypes/painan_1663_relational/prototype.css` | unchanged |
| `docs/thesis/colab/MODEL_3B_COLONIAL_CATEGORY_AND_RESISTANCE_INTERPRETIVE_WORKING.csv` | unchanged |
| `docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md` | unchanged |
| `docs/thesis/pilot_annotation/CROSS_CASE_POWER_ONTOLOGY_VALIDATION_PLAN.md` | unchanged |
| `docs/thesis/pilot_annotation/CROSS_CASE_POWER_ONTOLOGY_REVIEW.md` | unchanged |
| `docs/thesis/colab/CROSS_CASE_ENTITY_DECISION_LEDGER.csv` | unchanged |
| `docs/thesis/colab/CROSS_CASE_RELATION_DECISION_LEDGER.csv` | unchanged |
| `docs/thesis/colab/CROSS_CASE_ANNOTATION_DECISION_LEDGER.csv` | unchanged |

The dedicated validator (`scripts/research_validators/validate_natal_1760_relational_artifact.py`, check 25) re-verifies the Painan artifact and its 3 prototype files against these baseline checksums on every run, so this guarantee is machine-enforced going forward, not only asserted here.

## 4. Natal Actor Construction

13 actors were instantiated: the 5 mandatory granular local units (Dato's-bazaer Radja-putti-katy, Sulthan Bagindo Maharadja-Lelo, hoofdregent Baginda Maharadja Lello, radja Darat, 7 ponghoulous Natal — each a separate `actor_id`, none merged into a single "Natal" actor), one additional `NamedCollective` actor (`ACTOR_NATAL_REGENTS_COLLECTIVE_1693_1760`, carrying the October treaty's own retrospective collective narrative voice, explicitly disclosed as not asserted identical to any individually-named actor), 3 institutions (VOC, English, French), and 4 individually-named office holders (d'Estaing, Carpentier, van Moschel, Senff). Every actor carries `actor_id`, `actor_type`, `label`, `source_label_as_written`, `temporal_scope`, `source_document_ids`, `source_passage_locator`, `identity_confidence`, `researcher_review_required`, and `notes`, per the task's own required field list. Candidate actors were not included automatically: the actor list was built only from individuals/groups the frozen Batch I9 material actually names or bounds.

## 5. March 1760 State

Represented as: `REL_CONTROLS_FORT_ENGLISH_NATAL` (English prior control, undated start), `REL_CONTROLS_FORT_FRENCH_NATAL` (French capture, `MILITARY_PRESENCE`, explicitly transitional per the source's own account), two `RECOGNIZES_OFFICE_HOLDER` relations (French recognizing the two local signatories separately), `REL_CLAIMS_JURISDICTION_VOC_MARCH` (`claim_or_effective_control=CLAIM` only), and `ANNOTATION_VOC_HESITATION_MARCH` (VOC's own documented institutional hesitation). No relation dated March 1760 carries a control-implying `claim_or_effective_control` value.

## 6. English Relapse

Represented as `REL_SWITCH_REGENTS_TO_ENGLISH`, subject `ACTOR_NATAL_REGENTS_COLLECTIVE_1693_1760`, undated (bounded only by `valid_to=1760-02`, per the source's own lack of a precise date), `interpretive_status=CONTESTED`, preserving the source's own compound "gedeeltelijk door persuatiën en gedeeltelijk door drygementen" (partly persuasion, partly threats) account without collapsing it to a single consent-or-coercion label. This relation is never merged into, or used to extend, the March or October relations — it stands as its own dated (bounded) record between them.

## 7. October 1760 State

Represented as: `REL_CONTROLS_FORT_VOC_OCTOBER` (`claim_or_effective_control=FORT_CONTROL`, `evidence_strength=HIGH`, independently GM-corroborated), `REL_SWITCH_REGENTS_TO_VOC_OCTOBER` (restoration, `contradicted_by` pointing at the relapse relation so the disruption remains visible), and three `RECOGNIZES_OFFICE_HOLDER` relations (hoofdregent, radja Darat, 7 ponghoulous, kept as 3 separate records).

## 8. Formal Cession versus Control

The March cession/claim (`CLAIM`) and the October fort posting (`FORT_CONTROL`) are two structurally distinct relations, never merged into one span. The validator's checks 11 and 13 enforce this distinction mechanically (`validate_natal_1760_relational_artifact.py`, checks 11/13, both PASS). No relation in this artifact asserts "VOC controls Natal from March 1760."

## 9. Fort, Port, Territory, and Population

Every control-type relation in this artifact targets `LOCATION_FORT_NATAL` specifically, a `Location` entity of subtype Fort. No relation targets a port, a wider territorial unit, or a population entity. `EXERCISES_EFFECTIVE_CONTROL_OVER` (the broader, territory-scale relation type available in Draft V2's EXTENDED_RESEARCH_RELATION set) was deliberately never instantiated, even for the October state where its strongest available evidence (Senff's posting) might have seemed to justify a broader claim — see stress-test test T-15.

## 10. Local Actor Granularity

All 5 mandatory local actors remain separate records. The Sulthan Bagindo Maharadja-Lelo (March) / hoofdregent Baginda Maharadja Lello (October) name-and-title similarity was handled per the task's explicit instruction: two separate actor records, each carrying a `possible_same_actor` cross-reference note and `researcher_review_required=true`, with no merge and no assertion of definite non-identity either. This directly operationalizes Draft V2 §10's own already-anticipated open question about this exact pair.

## 11. Consent, Persuasion, and Force

The relapse relation (`REL_SWITCH_REGENTS_TO_ENGLISH`) is the artifact's operationalization of this axis: `interpretive_status=CONTESTED`, `explicit_or_inferred=OBSERVED_ACTION_AS_STRATEGY` (secondary/retrospective-clause-only sourcing, per the Batch I9 mapping convention), and a `source_statement_summary` that preserves the source's own mixed persuasion/force account rather than resolving it into a single mechanism.

## 12. Patron-Client Annotation

`patron_client_classification=PATRON_CLIENT_PARTIALLY_SUPPORTED` is carried onto the October relations (`REL_CONTROLS_FORT_VOC_OCTOBER`, `REL_SWITCH_REGENTS_TO_VOC_OCTOBER`), directly reusing Batch I9's own already-completed joint test for the VOC-Natal-regents relationship (1693-1760), not re-derived. It appears only as an annotation field value on existing relations — no `PATRON_OF`/`CLIENT_OF` edge or dedicated patron-client relation exists anywhere in this artifact (validator check 19, PASS).

## 13. Resistance Annotation

No `resistance_candidate` field is populated anywhere in this artifact. Per Batch I9's own already-completed analysis, no Natal row met even a `NOT_TESTABLE` threshold for a resistance mechanism distinct from the alignment-switch relation already modeled, so the field is omitted rather than populated with an unexamined default value. This is logged as a schema-completeness question for future researcher decision (stress-test test T-18), not resolved unilaterally here, and does not affect the hard rule that resistance stays research-only (validator check 20, PASS).

## 14. Relation to Project Status and Readiness Decision

```text
CROSS_CASE DRAFT V2:        PUSHED_AND_SERVER_SYNCED
V1 NATAL VALIDATION:        COMPLETE (this turn) -- artifact + validator + stress-test ledger + audit built;
                             commit/push/server-sync NOT performed this turn, pending a separate researcher-gated turn
V2 KOTO TANGAH:              NOT AUTHORIZED
MULTI-CASE PROTOTYPE:        NOT AUTHORIZED
PRODUCTION INTEGRATION:      BLOCKED
```

**Artifact:** `data/power_relations/natal_1760_relational_validation_artifact.json` — 13 actors, 1 location, 2 treaties, 12 relations. SHA-256 recorded at construction: `afafe9f2985ef5e326514fcb8634d304f39a59c6f729abf1582d5221638ab07a` (post-correction, see §3 of the stress-test ledger, test T-05, for the one compound-vocabulary fix made during validation).

**Validator:** `scripts/research_validators/validate_natal_1760_relational_artifact.py` — 28/28 checks PASS (the 25 required checks plus 2 required-field-completeness sub-checks and one duplicate-numbered check retained from the task's own check list). The Painan artifact's own validator (`validate_painan_1663_relational_artifact.py`) was re-run independently and still reports 23/23 PASS, confirming no cross-contamination.

**Ontology stress test:** `docs/thesis/colab/NATAL_1760_ONTOLOGY_STRESS_TEST.csv` — 19 tests: 10 PASS, 1 FAIL (T-06: no Draft V2 relation_type represents an institution's own internal hesitation about a claim it has already nominally received — logged as a genuine `ONTOLOGY_GAP`, not repaired by changing the Draft, not papered over by inventing new controlled vocabulary; this artifact's own workaround, a self-referential subject=object annotation record excluded from relation-type validation, is disclosed as non-standard rather than presented as if Draft V2 already supports it), 4 EXCLUDED_BY_RESTRAINT (NEGOTIATES_WITH, PROVIDES/REQUESTS_PROTECTION_FROM, CONTROLS_PORT, EXERCISES_EFFECTIVE_CONTROL_OVER — each a deliberate, source-supported non-inclusion rather than an oversight, recorded so the exclusion itself is auditable), plus 4 additional disclosure/confirmation-type test rows covering identity-rule operation, NamedCollective usage, and structural checks.

**Readiness decision:** V1 Natal validation is judged COMPLETE for this turn's scope: Draft V2 successfully represented 18 of 19 tested ontology components without any vocabulary change, relation-type extension, or silent field addition; the 1 failure is logged as an explicit ontology gap awaiting a future researcher-gated Draft revision decision, not resolved here. No artifact, validator, or Draft file outside this turn's declared outputs was modified. Per the explicit stop condition governing this task: proceeding to V2 (Koto Tangah), building a multi-case prototype, touching Atlas/API/database/Graphify, or staging/committing/pushing any of this turn's outputs are all NOT authorized by this turn and are deferred to separate, future, researcher-gated turns.

Ketiadaan ledger interpretif di server adalah expected behavior, bukan ketidaksesuaian — validasi 79 baris (termasuk kedua baris Natal yang menjadi basis artefak ini) tetap dilakukan lokal, tempat artefak kerja itu memang dirancang untuk berada; ini tidak memengaruhi status COMPLETE V1 di atas, yang seluruhnya adalah pekerjaan lokal nonproduksi.
