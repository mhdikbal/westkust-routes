# CROSS-CASE POWER ONTOLOGY REVIEW

> **READ-ONLY CROSS-CASE SYNTHESIS — NO ATLAS PRODUCTION INTEGRATION, GRAPHIFY, MIGRATION, MODEL RUN, COMMIT, PUSH, OR DEPLOYMENT AUTHORIZED**
> Executed per `CROSS_CASE_POWER_ONTOLOGY_REVIEW_PLAN.md` (repository root). Synthesizes the already-completed interpretive program (Batches I1-I11, 79 ledger rows), the Painan 1663 relational artifact and local prototype, and their supporting audit trail. No prior artifact is modified; no new primary-source research was performed. This document does not freeze the ontology — it prepares the ground for a researcher decision.

---

## 1. Executive Summary

Twelve cases were reviewed. The single most repeated, cross-case-stable finding is that **claim and effective control must never be conflated** — Painan 1663, Natal 1760, the Koto Tangah destruction cycle, and Tiku's own 1641/1684 material each independently demonstrate the same gap via different mechanisms (a contested treaty clause, a documented VOC-side institutional hesitation, a repeated-destruction-without-durable-compliance pattern, and an unlocalized administrative claim, respectively). **No dyad in the case set reaches `PATRON_CLIENT_SUPPORTED`.** **`MAINTAINS_PARALLEL_ALIGNMENT_WITH` does not generalize beyond Painan** — every other multi-patron case in this review is sequential switching, not concurrent alignment. **Resistance remains entirely research-only**: zero of 79 ledger rows reach `SUPPORTED`. The clearest actor-vs-location failure mode is Pariaman (CASE-10), where a place-name/collective-label repeatedly substitutes for a demonstrated-mandate actor across 10 rows and 120 years. The review recommends a narrow, evidence-anchored MVP relation set (7-9 types), a large annotation-only set (17 items, none promoted), and explicitly defers Atlas/Graphify/production integration pending four additional non-Painan case artifacts and a multi-case prototype — none of which this review authorizes or builds.

## 2. Scope

This review covers exactly the read-only synthesis specified in `CROSS_CASE_POWER_ONTOLOGY_REVIEW_PLAN.md`: a comparative case matrix, entity/relation/annotation decision ledgers, an ontology contract draft, and a validation plan for future (not current) case artifacts. It does not re-derive, re-verify, or alter any finding from Batches I1-I11, the Painan artifact, or the Painan prototype. Two ledger rows (`EVT-1687-buku-vogel-1690-545-3f44`, the Sapoelo Boabandaars alliance-switching case, and `EVT-1687-buku-vogel-1690-477-154b`, the Batoe Bannaw/Songy Abou resource dispute) fall outside the 12 required cases and are cross-referenced where directly relevant (§17, §19) but not separately case-matrixed, per the plan's own "additional cases only when required" instruction.

## 3. Frozen Research Status

Reused verbatim from the governing plan §2 — not modified:

```text
MODEL_3: RETAINED_AS_POOLED_EXPLORATORY_BASELINE
MODEL_3B_CD_V1: CLOSED_AFTER_FAILED_RECOVERY_VALIDATION
PHASE_B_PROVENANCE_AUDIT: COMPLETE, 141/141 EVENTS
PHASE_C_LEAVE_SOURCE_OUT: COMPLETE
PARENT_EPISODE_REVIEW: COMPLETE
PHASE_D_CONDITIONAL_CLUSTERING: COMPLETE
PHASE_D_PRIMARY_RESULT: RESIDUAL_CLUSTERING_NOT_SUPPORTED IN ALL 9 ARMS
INTERPRETIVE_BATCHES_I1_I11: COMPLETE
INTERPRETIVE_LEDGER_ROWS: 79 (confirmed this turn)
RESISTANCE_CANDIDATE_SUPPORTED: 0 (confirmed this turn)
PAINAN_1663_RELATIONAL_ARTIFACT: COMPLETE, VALIDATED, PUSHED, SERVER-SYNCED
PAINAN_1663_LOCAL_PROTOTYPE: COMPLETE, VALIDATED, VISUALLY REVIEWED, PUSHED, SERVER-SYNCED
ATLAS_PRODUCTION_INTEGRATION: NOT AUTHORIZED
GRAPHIFY_UPDATE: DEFERRED
MODEL_V2: NOT AUTHORIZED
```

## 4. Inputs and Integrity

All 24 input paths listed in the governing plan §4 were located (none missing). Preflight results:

```text
1. SHA-256 recorded for all 24 inputs before analysis began — see §31 (Checksums Before and After).
2. linimasa_events.csv unchanged: ebca46d1...5278b (confirmed).
3. Painan artifact validator: 23/23 PASS, 0 warnings, 0 errors.
4. Painan prototype validator: 30/30 PASS.
5. Interpretive ledger row count: 79 (confirmed by fresh count this turn).
6. Fixed-vocabulary validation (evidence_strength, source_asymmetry, resistance_candidate,
   interpretive_status) across all 79 rows: 0 violations.
7. No prior artifact was written during this task (only the 7 new cross-case outputs were created).
8. No production file change existed before starting (git status confirmed clean of production paths).
```

No integrity guard failed. `CROSS_CASE_POWER_ONTOLOGY_REVIEW_BLOCKED_BY_INTEGRITY_FAILURE` is NOT invoked.

## 5. Comparative Method

Each of the 12 required cases (§6 of the governing plan) was reconstructed by grouping the 79-row interpretive ledger's own `episode_or_event_id`/`locations` fields, cross-referencing the already-completed Batch I1-I11 audit sections and, for Painan specifically, the separately-reviewed relational artifact (which is not itself a ledger-row case, since its own 9 relations were built and validated outside the 43-column interpretive schema). No case was assembled by re-reading primary sources; every fact in the resulting matrix (`CROSS_CASE_POWER_ONTOLOGY_MATRIX.csv`) traces to an already-existing ledger row, artifact field, or audit-section finding. The 20 comparative questions in the governing plan §8 are answered per-case in the matrix's own columns and synthesized thematically in Part B-E of this document below, not repeated as a 12×20 grid (which would substantially duplicate the matrix CSV without adding new information).

## 6. Case Matrix

Full 31-field matrix: `docs/thesis/colab/CROSS_CASE_POWER_ONTOLOGY_MATRIX.csv` (12 rows). Summary:

```text
CASE-01 PAINAN_1663                          -- 1662-1687 -- LOCAL_VOICE_PRESENT/VOC_ONLY -- HIGH-adjacent evidence -- concurrent parallel alignment (unique in set)
CASE-02 INDRAPURA_1662_1686                  -- 1636-1755 -- VOC_ONLY/VOC_DOMINANT        -- sequential alignment cycling (Aceh->VOC->England->VOC)
CASE-03 NATAL_1760                           -- 1760       -- VOC_DOMINANT                -- HIGH evidence, cleanest claim-vs-control gap (VOC's own hesitation documented)
CASE-04 KOTO_TANGAH_1670_1686                -- 1660-1755 -- VOC_DOMINANT/VOC_ONLY        -- repeated coercion / failed deterrence primary test case
CASE-05 TIKU_1625_1740                       -- 1625-1740 -- VOC_ONLY/VOC_DOMINANT/MIXED  -- richest local-voice row (Soureradja, 1662); patron-client explicit non-finding
CASE-06 SILLIDA_RESOURCE_GOVERNANCE          -- 1648-1755 -- VOC_DOMINANT/VOC_ONLY        -- primary resource-governance case; constrained-agency cross-reference
CASE-07 BATANG_CAPAS_1686                    -- 1686       -- MIXED                       -- HIGH evidence, EIC-VOC confrontation, linked to CASE-02's own 1686 defection
CASE-08 PADANG_OFFICE_AND_SUCCESSION         -- 1671-1782 -- VOC_ONLY/VOC_DOMINANT        -- panglima-office continuity test; boundary-spans CASE-04
CASE-09 BARUS_FACTIONAL_AND_COMMERCIAL       -- 1668-1775 -- VOC_DOMINANT/VOC_ONLY        -- longest single-location case (107 years); resistance-to-Aceh not VOC
CASE-10 PARIAMAN_ACTOR_AGGREGATION           -- 1661-1781 -- VOC_ONLY/VOC_DOMINANT        -- primary Actor-vs-Location failure-mode test case
CASE-11 SAS_EXPEDITION_1693                  -- 1693-1695 -- VOC_ONLY/VOC_DOMINANT        -- broker-continuity cross-reference (Sas, parallel to Groenewegen)
CASE-12 VOC_ACEH_WAR_1656_1657               -- 1656-1659 -- VOC_ONLY                     -- root episode for at least 4 other cases
```

## 7. Entity Review

Full 23-class ledger: `docs/thesis/colab/CROSS_CASE_ENTITY_DECISION_LEDGER.csv`. Decision distribution:

```text
KEEP_AS_FIRST_CLASS_ENTITY:   Actor, Institution, IndividualOfficeHolder, Location, Treaty,
                                HistoricalEvent, ParentEpisode, Claim, PowerRelation,
                                EffectiveControlObservation  (10)
KEEP_AS_ROLE_OR_ATTRIBUTE:    ActorFaction, PoliticalOffice, Broker, Port, Fort, Mine,
                                Commodity, Obligation, BreachAllegation  (9)
KEEP_RESEARCH_ONLY:           NamedCollective, DocumentaryReport, StrategicInteraction  (3)
REQUIRES_MORE_EVIDENCE:       Community  (1)
MERGE_WITH_ANOTHER_ENTITY:    none
REJECT_FROM_ONTOLOGY:         none
```

No entity class was rejected outright; the case set is too early-stage for confident rejection, but `Community` is the one class this review cannot yet recommend past `REQUIRES_MORE_EVIDENCE` — only CASE-04 and CASE-05 supply even borderline sufficient collective-action evidence, and both are thin (office-holders acting nominally on the community's behalf, not the community itself documented as an acting body).

## 8. Actor and Location Distinction

The governing plan's own §10 guard (`Pariaman as location != Priamanners as source category != named local rulers != community with demonstrated mandate`) was applied to all 8 named places:

```text
Painan     -- location confirmed distinct from actor; CASE-01's own 6 actors are individually named, never "Painan" itself
Padang     -- location confirmed distinct; Panglima Padang is an OFFICE, tested separately from the place (CASE-08)
Tiku       -- location confirmed distinct; CASE-05's own §5 finding (Batch I11) explicitly separates Tiku-as-port/trade-region
              from Tiku-as-political-community (Soureradja + 12 desa) from Tiku-as-mere-killing-site (row 126)
Natal      -- location confirmed distinct; CASE-03's 6 actors are individually named signatories, never "Natal" as a bloc
Sillida    -- location confirmed distinct, though CASE-06's own actor detail is the thinnest in the review (see §7's
              REQUIRES_MORE_EVIDENCE finding for Community)
Barus      -- location confirmed distinct; landsheeren/Grooten van Baros and named radja are the actors, not "Barus" itself
Koto Tangah -- location confirmed distinct; CASE-04's own explicit refusal (Batch I10) to merge "Bergvolkeren te Koto
              Tangah" (1738) with the 1660-1712 coastal polity is this review's strongest single illustration
Indrapura  -- location confirmed distinct; named rulers (Sulthan Mamet-chia, Malafarcha) carry the actor identity across
              CASE-02's own 80-year span, not the place name itself
```

**FAILURE MODE IDENTIFIED, not a place on the above list but the single clearest counter-illustration in the case set: CASE-10, Pariaman.** Across 10 ledger rows spanning 120 years, "Pariaman"/"(regenten) Priaman dkk" functions predominantly as a SOURCE CATEGORY — a VOC-side collective label — not as an entity with demonstrated continuous mandate. Only 1 of the 10 rows (the 1661 panglima poisoning) names an individual, and even that individual is unnamed ("an unnamed panglima"). This review's explicit finding: **no persistent Actor or ActorFaction ID should be minted for "Pariaman" as a whole.** Per-instance actor identification would be required first, and the underlying ledger rows do not supply it.

## 9. Faction Review

Tested against the 6 minimum candidates in the governing plan §11:

```text
Muhammad Syah faction (CASE-01):      MEETS persistent-ID bar -- membership implied via the 9-of-20 loyal
                                        menteri count, leadership named, temporal scope bounded (1662-1665)
Raja Adil faction (CASE-01):          MEETS persistent-ID bar -- 11-of-20 menteri count explicit, leadership
                                        named, temporal scope bounded
Eleven-minister faction:              same as Raja Adil faction above (the two are the same referent in this
                                        project's own material)
Pro-Aceh faction at Tiku (CASE-04):   DOES NOT meet the bar -- no membership, leadership, or count documented
                                        for the 1684 rebellion; remains a narrative attribute of that single event
Hoeloe/Ilir factions at Barus (CASE-09): not independently re-tested by this review (already-completed Batch
                                        I1/I2 material); flagged for a future pass, not resolved here
Local elite alignments, Pariaman/Padang: DOES NOT meet the bar in either case -- see §8's Pariaman finding above;
                                        Padang's own office-succession disruptions (1676, 1782) name no faction
                                        membership either
```

**Decision: `ActorFaction` requires persistent IDs only where membership/leadership is explicitly counted or named AND temporal scope is bounded — 2 of 6 tested candidates meet this bar.** A blanket persistent-ID policy would create mostly-empty faction records for the other 4; a blanket refusal would lose CASE-01's own genuinely well-evidenced two-faction succession contest. Recommendation: case-by-case faction IDs, not a default.

## 10. Broker Review

Tested against Groenewegen (primary candidate) and Sas (secondary candidate), per §12:

```text
Groenewegen: evidence of negotiation transmission (CASE-01, CASE-05) AND representation claim/both-sides
              standing (honored at Aceh's own court 1660, then VOC's lead negotiator against Aceh's interest
              1662-63) -- MEETS the evidentiary bar with TWO of the eight required evidence types, across
              THREE cases (CASE-01, CASE-04's own 1665 row, CASE-05)
Sas:          evidence of negotiation transmission across 3 sites in one 1693 tour (CASE-11) -- MEETS the bar
              with ONE evidence type; no both-sides-standing evidence documented
Carpentier, Senff, van Leene, Boudens: single-case command/negotiation roles only -- repeated appearance
              WITHIN one case, not across cases, and no broker-specific evidence type (translation, information
              control, commodity brokerage) documented for any of them
```

**Decision: `Broker` remains a role/attribute on individual relations (e.g. a flag on `NEGOTIATES_WITH`), not a first-class entity table.** Groenewegen and Sas differ in kind (both-sides-standing vs. single-direction multi-site transmission) — collapsing them into one entity table would flatten a real distinction the evidence itself supports keeping separate. Repeated appearance alone (true of van Leene across CASE-04/CASE-05/CASE-10) is explicitly NOT sufficient, per §12's own instruction, and this review does not treat it as such.

## 11. Political Office Review

Nine office terms occur across the case set: panglima, pongoulon/penghulu, regent/regenten, hoofdregent, governor, dato, radja, sultan, plus VOC titles (commandeur, resident, commissaris) and one EIC reference (CASE-08's cross-referenced material). **Decision: normalized label PLUS original term** (§13's fourth option), not a fixed cross-case office ontology. Justification: the same underlying function (local headman/ruler) is rendered panglima (Aceh-administered, CASE-05), penghulu/penghulu kepala (CASE-05's own Tiku material, 1740), regent/regenten (CASE-03/04/10, Dutch-administrative usage), hoofdregent (CASE-03, seemingly a senior regent), dato (CASE-03), radja (nearly every case), and sultan (CASE-01/02) — collapsing these into one normalized "local ruler" category would erase genuine source-vocabulary distinctions the project's own terminology-test discipline (established since Batch I2) requires preserving. VOC-period terms are explicitly NOT equated with any 19th-century statutory office in any case reviewed.

## 12. Constrained Agency Review

Primary test case: the armed, enslaved companies drawn from the Sillida mine's own labor force (documented in the Vogel-sourced 1687 material, cross-referenced from Batch I2/I3, not re-ledgered by CASE-06's own I-review rows). The existing ledger's own already-completed treatment (reused, not re-derived) records:

```text
group existence:            documented (a company of "commandirte Sclaven" / mustered armed slaves)
legal/coercive status:       explicit and diplomatically preserved as written ("Sclaven," not softened to
                              "workers" or hardened to "soldiers")
command relationship:        unnamed VOC officers ("commandirte" = commanded/ordered)
action performed:            deployed in at least 2 documented operations (a rebel-capture operation and a
                              trade-route-security military expedition)
absent political voice:      explicit -- the company's own political interest is NOT FOUND IN THE CORPUS
                              EXAMINED, per the existing ledger's own already-completed finding
constrained agency:          recruitment source, refusal possibility, compensation, and own political interest
                              are all explicitly recorded as NOT FOUND, not inferred either way
inability to infer loyalty
  or resistance:              explicit -- the existing ledger record treats this as CANNOT_DETERMINE, strictly
                              separated from the SEPARATELY-tested resistance-candidate status of the named
                              individual (Radja doa Selas) captured in the same operation
```

**No voluntary alliance relation is created for this group by this review, and none should be created without new evidence, per §14's own explicit instruction.** This is this project's clearest and most carefully already-modeled instance of the constrained-agency problem; this review recommends preserving it exactly as-is, not extending or generalizing it into a template applied elsewhere without equivalent evidence.

## 13. Relation-Type Review

Full 21-type ledger (the governing plan's own §15 heading says "20" but its enumerated list contains 21 items, the same off-by-one pattern flagged in the plan's own §45 for the required-outputs list — this review resolves it the same way, by reviewing the fuller, explicit enumerated set): `docs/thesis/colab/CROSS_CASE_RELATION_DECISION_LEDGER.csv`. Decision distribution:

```text
MVP_CORE_RELATION:            REQUESTS_PROTECTION_FROM, PROVIDES_PROTECTION_TO, REQUIRES_MONOPOLY_FROM,
                                NEGOTIATES_WITH, RECONCILES_WITH, SWITCHES_ALIGNMENT_TO,
                                CLAIMS_JURISDICTION_OVER, CLAIMS_COMMODITY_MONOPOLY,
                                CONTESTS_SUCCESSION_WITH, CONTESTS_RESOURCE_WITH,
                                RECOGNIZES_OFFICE_HOLDER, COLLECTS_TOLL_FROM, LEASES_RESOURCE_TO,
                                USES_MILITARY_FORCE_AGAINST   (14)
EXTENDED_RESEARCH_RELATION:    EXERCISES_EFFECTIVE_CONTROL_OVER, CONTROLS_FORT   (2)
CASE_SPECIFIC_ONLY:            CONTROLS_PORT, DISMISSES_OFFICE_HOLDER   (2)
REQUIRES_MORE_EVIDENCE:        MAINTAINS_PARALLEL_ALIGNMENT_WITH, APPOINTS_OFFICE_HOLDER   (2)
ANNOTATION_NOT_RELATION:       IMPOSES_PUNITIVE_CLASSIFICATION_ON   (1)
REJECT:                        none
```

## 14. Claim versus Effective Control

The 10-value vocabulary was tested per-case where instantiated:

```text
CASE-01: CONTESTED_CONTROL (PWR03, VOC's formal claim without demonstrated control over subsequent conduct)
CASE-03: CLAIM/FORMAL_ACCEPTANCE (Mar 1760, no effective control -- VOC's own Padang hesitation, deferred to
         Batavia) -> MILITARY_PRESENCE/effective presence (Oct 1760, Senff's independently-confirmed posting)
         -- a ~7-month, source-documented gap between claim and control
CASE-04: repeated CLAIM/punitive-classification (1670-1738) with NO row supplying a clean, distinct effective-
         control observation -- the clearest case in the whole review where claim is repeatedly reasserted
         without ever being followed by an independently-confirmed control observation
CASE-05: CLAIM only (1641, Aceh's own toll policy) with no documented on-the-ground Aceh official at Tiku
CASE-06: CLAIM (sovereignty retained, 1737 lease text) vs. COMMERCIAL_CONTROL (the lease itself) recorded as
         two distinct fields on the same instrument -- this review's cleanest textual separation of the two
```

**Never derived from treaty signing alone, in any case reviewed** — every instance above required a SEPARATE, independently-dated piece of evidence (a hesitation record, a posted commandant, a repeated destruction, an absent local official, an explicit lease clause) to assess control, distinct from the claim's own date.

## 15. Protection Relations

`REQUESTS_PROTECTION_FROM`/`PROVIDES_PROTECTION_TO` remain distinct relations; `PROTECTION_BARGAIN` remains an annotation describing the bundle (§22 decision, reused). Tested across CASE-01 (fully instantiated, 3 relations in the reviewed artifact), CASE-05 (Soureradja's own explicit request, 1662, not yet promoted to a full relation record by this review), and CASE-03/CASE-11 (protection language not independently re-confirmed in this synthesis, flagged not assumed). **Protection does not imply submission or sovereignty in any case reviewed** — CASE-01's own artifact explicitly guards against this reading (§11 of the artifact's audit), and this review finds no case that contradicts it.

## 16. Alignment Relations

`ALLY_OF`, `SWITCHES_ALIGNMENT_TO`, `MAINTAINS_PARALLEL_ALIGNMENT_WITH`, `RECONCILES_WITH` were tested for cross-case stability. **`MAINTAINS_PARALLEL_ALIGNMENT_WITH` is `PAINAN_SPECIFIC`, not `CROSS_CASE_STABLE`** (§13 of the relation ledger; direct answer to the governing plan's own §18 question) — every other multi-patron case reviewed (CASE-02, CASE-03, CASE-10) is sequential switching. No case in this review infers parallel alignment merely from sequential contacts; CASE-01's own classification rests on two independently-dated, concurrently-valid relations (the standing VOC protection tie plus the Oct 1663 Aceh reconciliation), not mere proximity in time.

## 17. Coercion and Punitive Action

`USES_MILITARY_FORCE_AGAINST` is confirmed `MVP_CORE_RELATION`, evidenced explicitly in at least 8 of 12 cases (§13 above). `REPEATED_COERCION` and `FAILED_DETERRENCE` remain mechanism annotations (§22), never promoted to relations, per the governing plan's own §19 instruction. CASE-04/Koto Tangah is the primary test case; compared against CASE-06/Sillida (coercive content present but not the episode's own primary subject), CASE-07/Batang Capas (a single high-evidence recapture, not a repeated cycle), CASE-05/Tiku (one subduing, 1684, not a repeated cycle at the same site), CASE-10/Pariaman (a repeated relapse-and-resubduing cycle structurally PARALLEL to Koto Tangah's own, via alignment-switching rather than destruction), and CASE-09/Barus (repeated RENEWAL, not repeated coercion — the episode's own already-completed characterization is voluntary-appearing, not punitive). **Repeated destruction is never treated as effective-control evidence in any case reviewed — the opposite finding is what every repeated-coercion case in this review actually supports.**

## 18. Administrative and Symbolic Relations

`RECOGNIZES_OFFICE_HOLDER` is well-evidenced (CASE-03, CASE-05) and kept as `MVP_CORE_RELATION`; `APPOINTS_OFFICE_HOLDER` is NOT evidenced in any of the 12 cases as a directed VOC/Aceh-selects-the-individual action (`REQUIRES_MORE_EVIDENCE`); `DISMISSES_OFFICE_HOLDER`'s one clear instance (CASE-08, Panglima Jelel 1782) is LOCALLY-initiated, not a colonial-power action, complicating the relation type's own implicit subject assumption (`CASE_SPECIFIC_ONLY`, flagged for a possible subject-type correction). `IMPOSES_PUNITIVE_CLASSIFICATION_ON` is demoted to annotation-only: CASE-03's own Oct 1760 treaty explicitly declines to impose a punitive frame on a structurally similar alignment-shift that CASE-04 and CASE-09 (cross-ref) DO frame punitively — direct evidence this is source-specific rhetoric, not a stable relation. `ADMINISTRATIVE_RECLASSIFICATION` and `SYMBOLIC_RECLASSIFICATION` remain annotations per the governing plan's own §20 default; no case reviewed supplies a clear enough subject/object/dated-action triple to promote either.

## 19. Resource-Governance Relations

CASE-06/Sillida is the primary case. `CONTESTS_RESOURCE_WITH` (CASE-05's Raja Ibrahim/Raja Kinali rivalry; the cross-referenced Batoe Bannaw/Songy Abou dispute), `LEASES_RESOURCE_TO` (CASE-06's 1737 gold lease), and `CLAIMS_COMMODITY_MONOPOLY` (pepper/gold/camphor across multiple cases) are all `MVP_CORE_RELATION`. `COLLECTS_TOLL_FROM` is likewise core (CASE-03's own explicit reciprocal clause is the model instance). `GRANTS_TRADE_ACCESS_TO` was not independently instantiated in any of the 79 rows reviewed this turn (`REQUIRES_MORE_EVIDENCE`, not separately tabled in the relation ledger given zero supporting cases). **`RESOURCE_GOVERNANCE_CONFLICT` is best treated as a PARENT CATEGORY / mechanism-bundle label** (not a single relation, not merely a synonym for `COMMERCIAL_STRATEGY`) — CASE-05's Raja Ibrahim case explicitly demonstrates resource governance is NOT reducible to commercial strategy alone, since a local political rivalry (Raja Kinali) is the actual resolving mechanism, not a VOC commercial decision.

## 20. Annotation Review

Full 17-item ledger: `docs/thesis/colab/CROSS_CASE_ANNOTATION_DECISION_LEDGER.csv`. **All 17 items are `KEEP_AS_ANNOTATION` — none is promoted to a relation by this review.** No candidate met the full promotion bar (identifiable subject, object, direction, temporal range, source locator, observable historical action, cross-case usefulness) simultaneously; several (e.g. `CLAIM_OR_EFFECTIVE_CONTROL`) are structurally FIELDS on relations, not separable actions, by design.

## 21. Patron-Client Review

No dyad across any of the 12 cases reaches `PATRON_CLIENT_SUPPORTED`. CASE-01's best dyad (VOC↔Muhammad Syah faction) and CASE-03's whole relationship (VOC↔Natal regents) both reach only `PATRON_CLIENT_PARTIALLY_SUPPORTED`, for different reasons (CASE-01: exclusivity directly falsified by the Oct 1663 reconciliation; CASE-03: exclusivity broke down externally, via inter-European war, not local choice). CASE-05/Tiku is an explicit non-finding — the evidentiary basis across 115 years is too fragmented (no single continuous relationship meets the 9-10 element bar). **The evidentiary bar is not lowered anywhere in this review.** Recommendation: `PATRON_CLIENT_CLASSIFICATION` remains annotation-only permanently, pending a case that reaches full `SUPPORTED` — none has, across 12 cases and 79 ledger rows.

## 22. Resistance Review

```text
SUPPORTED:            0
PARTIALLY_SUPPORTED:  7
NOT_SUPPORTED:        11
NOT_TESTABLE:         61
```

`RESISTANCE_CANDIDATE` must remain research-only. This review finds every case in the set consistent with the governing plan's own §24 prohibition: no ledger row promotes violence, treaty breach, alliance switching, trade evasion, refusal, or a colonial punitive label into a resistance finding by itself — each of the 7 `PARTIALLY_SUPPORTED` rows carries an explicit, source-supported local political target or demand distinct from the bare fact of conflict (e.g. CASE-05's Soureradja row targets ACEH specifically, not VOC, and is kept analytically separate from any VOC-resistance claim).

## 23. Power-Theory Review

First-dimensional, agenda-setting, relational/productive, and symbolic/classificatory power are all evidenced somewhere in the case set (concentrated in CASE-01 and CASE-04); preference-shaping (third-dimensional) evidence is the thinnest, confined to CASE-01's own historiographical-reception finding (the De Leeuw `aanvaarding`→`inbezitneming` shift). IEMP dimensions are fully worked only for CASE-01. **Default recommendation confirmed: research detail only.** No simpler public explanation is proposed or approved by this review; that decision is reserved for the researcher (see §30, item 16).

## 24. Temporal Model

Every case reviewed requires `valid_from`/`valid_to`/`date_precision`/`open_ended` at minimum; `superseded_by` is directly needed for CASE-03 (October instrument superseding March's claim-only status) and CASE-04 (each destruction year superseded by the next treaty renewal); `contradicted_by` is directly needed for CASE-01 (Oct 1663 reconciliation contradicting the standing VOC protection tie) and CASE-04 (Vogel's retrospective "vielfältigen Meineydes" contradicting the individual 1670 source's own silence on repetition). Overlapping relations are REQUIRED, not exceptional — CASE-01's own concurrent alignment and CASE-03's claim/control gap both depend on it. Retrospective source dates (Vogel's single 1690 sentence covering 1670-1686) must NOT be treated as four equally-precise event dates — this review reuses Batch I10's own explicit per-year evidence-strength differentiation as the model.

## 25. Evidence Contract

The Painan artifact's own already-validated contract (`source_document_ids`, `source_passage_locator`, `event_ids`, `provenance_status`, `evidence_strength`, `interpretive_status`, `explicit_or_inferred`, `researcher_review_required`) is recommended as the base for any future relation record, extended with `parent_episode_ids` (present in the interpretive ledger but not yet in the artifact schema) per the governing plan's own §27. The four-layer text contract (source statement / historical reconstruction / theoretical annotation / public-display summary) is likewise already validated in the Painan artifact and recommended unchanged. No layer should be auto-generated into another — this review finds zero violations of this rule anywhere in the 79-row ledger or the artifact (already confirmed by both validators, §4).

## 26. Contradiction Handling

Draft policy, informed by 3 directly-observed contradiction types in the case set:

```text
Sources disagreeing on mechanism/framing (CASE-03's CD6 "voluntary" language vs. GM's "regained from the
  hands of the regents" language, per Batch I9's own already-flagged tonal tension): retain BOTH readings
  as separate source_statement_summary entries, do not average or pick a winner.
Retrospective summaries covering multiple events (CASE-04's Vogel sentence, 4 years in one clause):
  retain the summary as its own DocumentaryReport, and give each event its own independently-assessed
  evidence_strength -- do not inherit the summary's own aggregate confidence uniformly across all members.
Contested mandate (CASE-01's Muhammad-Syah-vs-Raja-Adil succession; CASE-04's Sire-Narra/Gouverneur-Pouti
  identity question): mark CANNOT_DETERMINE explicitly, carry the competing hypotheses in notes, never
  silently pick the better-documented side as "the" answer.
```

**Contradictions are never resolved by majority vote** — where 2 independent sources corroborate mechanism but not detail (e.g. CASE-03's GM/CD6 pairing), only the CORROBORATED layer (existence/mechanism) is upgraded; the uncorroborated layer (exact date, named actor) remains at its original, single-source evidence tier, exactly as Batch I9 already modeled it.

## 27. Atlas Implications

The proposed opt-in layer (actor relations, relation timeline, claim/control toggle, source/evidence drawer, research-detail theory drawer) directly matches the ALREADY-BUILT and visually-reviewed Painan local prototype's own 6-view design. This review's own finding is that the prototype's design generalizes STRUCTURALLY (the same 6 views could render any case's relation set) but the UNDERLYING DATA does not yet exist for any other case — no relation artifact comparable to the Painan JSON has been built for Natal, Koto Tangah, Tiku, Sillida, or Batang Capas. **This review does not implement any Atlas layer and does not authorize doing so.** The legacy territorial layer is unaffected and untouched by this entire review.

## 28. Graphify Timing

Graphify readiness requires, per the governing plan §31: reviewed actor IDs (not yet frozen, per §7-11 above), reviewed first-class relation types (14 of 21 candidates decided `MVP_CORE_RELATION` in this review, but not yet formally frozen by researcher sign-off), source-linked temporal edges (only CASE-01 has these fully instantiated), and explicit uncertainty fields (already modeled in the Painan artifact, not yet extended elsewhere). **This review does not authorize Graphify execution.** Recommendation: Graphify remains appropriately `DEFERRED` until at least the 4 additional case artifacts in §29's production gate item 3 exist and pass their own validators.

## 29. Production Integration Gate

Status against the governing plan's own 8-item gate (§32):

```text
1. ontology categories frozen:                    NOT YET (this review proposes, does not freeze)
2. relation validator generalized:                 NOT YET (only the Painan-specific validator exists)
3. >=4 non-Painan cases encoded as test artifacts:  NOT YET (0 exist; Natal/Koto-Tangah/Tiku/Sillida
                                                     are the recommended 4, per §39 below)
4. cross-case validation passes:                    NOT APPLICABLE (no cross-case validator exists yet)
5. public-copy categories reviewed:                 PARTIALLY (a candidate 9-category vocabulary is
                                                     proposed in §30 below, not yet researcher-approved)
6. local multi-case prototype passes visual review: NOT YET (not built; explicitly not authorized this turn)
7. legacy compatibility tested:                     NOT APPLICABLE (nothing new has been built to test)
8. deployment and rollback plan approved:            NOT YET
```

**Production integration remains fully blocked.** This review does not move any of the 8 gate items to a passing status; it only clarifies what each item would require.

## 30. Researcher Decisions Required

Reused verbatim from the governing plan §42, with this review's own recommendation appended in brackets where one is offered:

```text
1.  frozen entity set [this review's own 10-item KEEP_AS_FIRST_CLASS_ENTITY list, §7, is offered as a
    starting proposal, not a freeze]
2.  frozen MVP relation set [this review's own 14-item list, §13]
3.  extended research relation set [EXERCISES_EFFECTIVE_CONTROL_OVER, CONTROLS_FORT]
4.  rejected relation set [none rejected outright by this review -- researcher may choose to reject
    CONTROLS_PORT given its zero independent instantiation]
5.  annotation-only set [this review's own 17-item list, §20, all confirmed annotation-only]
6.  persistent faction IDs [recommend case-by-case: yes for CASE-01's two factions, no by default elsewhere]
7.  Broker as role or first-class entity [this review recommends role/attribute, §10]
8.  treatment of political offices [this review recommends normalized label + original term, §11]
9.  representation of coerced groups [this review recommends preserving the existing Sillida-armed-
    company model exactly as-is, §12, not generalizing it without equivalent evidence elsewhere]
10. MAINTAINS_PARALLEL_ALIGNMENT_WITH cross-case status [this review finds PAINAN_SPECIFIC, §16]
11. patron-client permanent status [this review recommends permanent annotation-only, §21]
12. resistance public-display prohibition [this review recommends maintaining the prohibition, §22]
13. claim/control public labels [not resolved by this review -- see the candidate vocabulary in §30
    of the Ontology Contract Draft V2 for options]
14. treatment of repeated coercion and failed deterrence [this review recommends permanent
    annotation-only, §17]
15. resource-governance representation [this review recommends PARENT CATEGORY, §19]
16. public versus research theory layers [this review recommends research-detail-only as the
    continuing default, §23]
17. Graphify timing [this review recommends continued deferral, §28]
18. four cases selected for future nonproduction artifacts [this review recommends Natal 1760,
    Koto Tangah cycle, Tiku, and Sillida -- see the Validation Plan]
19. conditions for local multi-case prototype [not resolved by this review; requires the 4 case
    artifacts in item 18 to exist first]
20. conditions for production integration [not resolved by this review; the full 8-item gate in
    §29 must clear first]
```

## 31. Final Readiness Decision

All required outputs were created (§33-39 of the governing plan; 7 files, confirmed by explicit count in the terminal summary). All integrity guards passed (§4). No stop condition (§41 of the governing plan) was triggered: no input checksum changed, the ledger remained at 79 rows throughout, every case traced to source-linked ledger entries or the already-reviewed Painan artifact, no entity identity was invented, no relation endpoint was fabricated, no mandate was assumed where the source did not supply one, and no category required modifying a prior artifact to resolve.

```text
CROSS_CASE_POWER_ONTOLOGY_REVIEW_READY_FOR_RESEARCHER_DECISION
```

Readiness does not authorize implementation, Atlas integration, Graphify, or any new case artifact. See the accompanying terminal summary for the full 40-item QC result and checksum confirmation.
