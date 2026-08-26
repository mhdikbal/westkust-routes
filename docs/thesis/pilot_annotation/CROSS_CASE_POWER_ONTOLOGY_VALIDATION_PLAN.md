# CROSS-CASE POWER ONTOLOGY VALIDATION PLAN

> **PLANNING DOCUMENT ONLY — NO TEST ARTIFACT CREATED BY THIS DOCUMENT, NO IMPLEMENTATION AUTHORIZED**
> Defines future nonproduction test artifacts for the four cases selected in `CROSS_CASE_POWER_ONTOLOGY_REVIEW.md` §30 item 18. Building any of these artifacts is explicitly deferred to a separate, future, researcher-authorized turn — none is created here.

## 1. Purpose

The Painan 1663 relational artifact and prototype remain this project's ONLY fully-instantiated, validated power-relation case. Before any ontology freeze or Atlas integration decision, the emerging V2 ontology (`ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_DRAFT.md`) must be tested against at least 4 structurally different cases, per the Production Integration Gate item 3. This plan defines what those 4 test artifacts would need to contain — it does not build them.

## 2. Selected Cases

Per the cross-case review's own §30 recommendation, chosen for maximum structural contrast with Painan and with each other:

```text
Natal 1760          -- imperial fort transfer via a third-party European broker (France); the
                        cleanest claim-vs-effective-control gap in the whole ledger, with an
                        independently-documented VOC-side institutional hesitation
Koto Tangah cycle    -- repeated destruction and possible failed deterrence; tests REPEATED_COERCION/
                        FAILED_DETERRENCE as annotations against a punitive (not protective) relation
                        pattern; four member years of sharply differing evidence strength
Tiku                 -- the richest single local-voice row in the whole project (Soureradja, 1662)
                        alongside the thinnest (the 1693-95 Sas killing); tests whether one case can
                        legitimately span both evidentiary extremes without merging them
Sillida (preferred over Batang Capas) -- resource-governance case; tests LEASES_RESOURCE_TO/
                        CLAIMS_COMMODITY_MONOPOLY and the constrained-agency (armed enslaved
                        company) representation question, neither of which Painan, Natal, or
                        Koto Tangah exercise
```

Batang Capas was considered but not selected as one of the 4: its own already-completed Batch I8 treatment was not re-opened by this review (per the review's own §6/§13 notes), so building a test artifact for it now would require re-deriving material this review deliberately left untouched. Sillida is recommended instead, as its resource-governance content is both well-attested across 10 ledger rows and structurally distinct from all 3 other selected cases.

## 3. What Each Future Test Artifact Must Contain

For each of the 4 cases, a future artifact-construction turn should produce a JSON file structurally parallel to `painan_1663_relational_research_artifact.json`, containing:

```text
schema_version, case_id, status (RESEARCH_ONLY_NONPRODUCTION), authorization_notice
actors[]        -- only actors already named in the 79-row interpretive ledger for that case;
                   no actor invented to fill a structural gap
treaties[]      -- only instruments already cited in the ledger
relations[]     -- restricted to the MVP_CORE_RELATION set frozen by researcher decision on this
                   review's §30 item 2 (14 candidates proposed, not yet frozen)
vocabulary_notes -- any case-specific mapping rule (e.g. Batch I9's own explicit_or_inferred
                   secondary-source-only mapping rule) disclosed exactly as done for Painan
```

## 4. Case-Specific Construction Notes (informational only, not instructions to build now)

```text
Natal:       2 ledger rows (EVT-1760-CD6-210-53b2, EVT-1760-CD6-223-cedc) map to at most 9 actors
             and an estimated 5-7 relations, closely mirroring Painan's own scale; the claim/control
             gap (March vs. October) should be the artifact's own centerpiece, exactly as this
             review's §14 already documents narratively.
Koto Tangah: 11 CORE_I10 ledger rows span 1660-1755; a future artifact must NOT collapse the 4
             Vogel-listed destruction years into one relation -- each requires its own evidence_
             strength (1670: LOW/independent-secondary; 1682: MODERATE/CD-primary; 1678/1686:
             LOW/Vogel-only), per Batch I10's own explicit, already-established discipline.
Tiku:        7 CORE_I11 ledger rows span 1625-1740; the 1662 Soureradja row (HIGH evidence, LOCAL_
             VOICE_PRESENT) and the 1693-95 Sas-killing row (LOW evidence, CANNOT_DETERMINE) must
             both be representable in the same artifact without the thin row being fabricated up
             to match the rich one's own evidentiary standard.
Sillida:     10 ledger rows span 1648-1755; the 1737 gold-mine lease's own CLAIM-vs-COMMERCIAL_
             CONTROL split (§6 of the review) should be the artifact's own model relation; the
             armed-enslaved-company material (cross-referenced from Batch I2/I3, not itself a
             CASE-06 ledger row) should be flagged as a KNOWN GAP in any future Sillida artifact,
             not silently included from a different case's own material without re-verification.
```

## 5. Validator Requirements for Future Artifacts

A future generalized validator (not built now) should verify, at minimum, the same 23+ checks already proven in `validate_painan_1663_relational_artifact.py`, generalized to accept a variable actor/relation count rather than Painan's hardcoded 6/9, plus 2 additional checks unique to the multi-case context:

```text
- no relation_type used outside the researcher-frozen MVP_CORE_RELATION set (§30 item 2 of the review)
- no case-specific actor ID collides with another case's actor ID (namespacing check, not required
  for Painan alone but necessary once >1 case artifact exists in the same directory)
```

## 6. What This Plan Does Not Authorize

```text
- creation of any of the 4 artifacts described above
- creation of a generalized validator
- creation of a multi-case prototype
- any change to the Painan artifact, prototype, or validators
- any Atlas, API, database, or Graphify change
- commit, push, or deploy
```

## 7. Sequencing

Per the review's own Production Integration Gate (§29): this validation plan's own artifacts (once authorized in a future turn) are gate item 3; a generalized validator passing against all 4 is gate item 4; only after both, plus the remaining 6 gate items, does production integration become eligible for researcher consideration. This plan does not shorten that sequence.
