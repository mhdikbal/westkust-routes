# Multi-Case Prototype — Known-Gap Adjudication (Natal CH-04, Tiku Commodity-Endpoint)

**Date:** 2026-08-28
**Scope:** Langkah 2 of the post-freeze/post-sync roadmap for commit `77b79b68c0424f04289019687ad33d1976b023b5` (multi-case power-relations prototype). Adjudicates the three known migrated-artifact validation flags surfaced by the multi-case prototype's diagnostics and reproduced identically on both local and `westkust-prod`:

- Natal: 1 `UNAPPROVED_RELATION_TYPE` finding
- Tiku: 2 `ORPHAN_RELATION_ENDPOINT` findings
- Painan, Koto Tangah, Sillida: 0 (not adjudicated here — already clean)

This is an **adjudication-only** turn. No migrated artifact, validator, or Draft V2.1 contract file was modified. No graph projection, Atlas integration, or Graphify work was started.

## 1. Natal — `VOC_INSTITUTIONAL_HESITATION_ANNOTATION` (1 finding)

**Finding:** `relations[ANNOTATION_VOC_HESITATION_MARCH].relation_type='VOC_INSTITUTIONAL_HESITATION_ANNOTATION'` is outside the closed 18-value V2/V2.1 relation vocabulary (rule `R-VOC-06`).

**Adjudication: `EXPECTED_LEGACY_GAP`.**

This is the exact, already-anticipated signature of CH-04 (institutional state and presence), which Draft V2.1 §16 formally excludes: **DEC-05 = DEFERRED** — no concrete field or object was proposed; a future design-exploration turn was explicitly authorized instead of a premature unified/split model. Natal's `VOC_INSTITUTIONAL_HESITATION_ANNOTATION` is the artifact's own pre-existing, case-specific workaround for the concept CH-04 exists to eventually close. `REV-08` (revalidation implementation map) already records this mapping and needs no change.

**Confirmed by user (2026-08-28), option selected: `EXPECTED_LEGACY_GAP` (recommended).**

No ledger row added — DEC-05/REV-08 already cover this exactly; this adjudication reaffirms rather than reopens it.

## 2. Tiku — Commodity-as-endpoint (2 findings)

**Findings:**
- `relations[REL_1649_CLAIMS_COMMODITY_MONOPOLY].object_id='COMMODITY_PEPPER'` does not reference a known actor_id/location_id (rule `R-REF-05`)
- `relations[REL_1740_CLAIMS_MONOPOLY_SALT].object_id='COMMODITY_SALT'` does not reference a known actor_id/location_id (rule `R-REF-05`)

**Adjudication: `CONTRACT_EXCEPTION_REQUIRED`.**

Unlike CH-04, this gap had **no prior DEC-xx or CH-xx entry** — it surfaced only as a "Known Limitation" in the Phase V2.1-GV1 generalized-validator audit (§16), which explicitly flagged it as requiring researcher input rather than a settled deferral. Draft V2 §1 models Commodity as an **attribute** of monopoly/toll relations, not an independently ID-addressable entity a relation's `object_id` may reference. The Tiku artifact, however, already gives commodities their own `commodity_id` namespace (`COMMODITY_PEPPER`, `COMMODITY_SALT` in its own `commodities` array) and uses that ID as `object_id` on both relations — a genuine artifact/contract shape mismatch, not a migration defect (the artifact's structure predates this migration and was carried over unmodified, as authorized) and not a matter needing archival re-reading (the source content of both relations is not in question — only how to represent "commodity" structurally).

Two candidate resolutions remain open, deliberately not chosen here:
- **(a)** extend the Draft V2/V2.1 endpoint model to formally recognize Commodity as an addressable relation-object entity, on par with Actor/Location; or
- **(b)** remodel `REL_1649_CLAIMS_COMMODITY_MONOPOLY` and `REL_1740_CLAIMS_MONOPOLY_SALT` to carry the commodity as an attribute field instead of `object_id`, aligning the two relations with the contract's current attribute-only text.

**Confirmed by user (2026-08-28), option selected: `CONTRACT_EXCEPTION_REQUIRED` (recommended).**

**Recorded as `DEC-19`** in `docs/thesis/colab/POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv` (`researcher_decision=DEFERRED`) and **`REV-11`** in `docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_V2_1_REVALIDATION_IMPLEMENTATION_MAP.csv` (`implementation_status=DEFERRED`). DEC-19 defers the choice between (a)/(b) to a future design turn; it does not itself pick one. The Tiku migrated artifact and the two relations above remain byte-unmodified.

## 3. Non-actions (explicit)

Per this turn's own scope:

- No CH-xx row was added to the frozen `ATLAS_POWER_RELATION_ONTOLOGY_V2_1_CHANGESET_LEDGER.csv` — that file records the original Phase-level changeset proposal as proposed; DEC-19/REV-11 in the live decision/revalidation ledgers are the correct home for a gap surfaced after that changeset was frozen.
- Draft V2.1 contract (`ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_1_DRAFT.md`) was not edited.
- No migrated artifact under `data/power_relations/migrated_v2_1/` was modified; all five remain byte-identical to the checksums recorded at the `77b79b68` push/sync.
- No Graph Projection Readiness Review, Atlas integration, or Graphify work was started (Langkah 3/beyond, out of scope this turn).

## 4. Status

`GAP_ADJUDICATION_COMPLETE_LOCAL` — not committed, not pushed. Ready for the user to decide whether to commit these two ledger additions plus this note, before proceeding to Langkah 3 (Graph Projection Readiness Review).

## 5. Resolution (2026-08-29)

DEC-19's (a)/(b) choice has since been made: **option (b) selected** (remodel the two Tiku relations to carry commodity as an attribute, not as `object_id`). Full reasoning, evidence, and the exact scoped future change: `DEC19_TIKU_COMMODITY_ADJUDICATION_DECISION.md`. `POST_V1_V4_RESEARCHER_DECISION_LEDGER.csv` DEC-19 row and `ATLAS_POWER_RELATION_V2_1_REVALIDATION_IMPLEMENTATION_MAP.csv` REV-11 row updated accordingly. This section 2's text above (documenting the gap and both original candidate options) is left unmodified as the historical record of the open question; the decision itself lives in the new file, not as an edit here. Implementation of the remodeling remains NOT AUTHORIZED.
