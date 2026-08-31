# G0 — Source Inventory and Claim-Source Ledger Schema Proposal

**Status:** PROPOSAL ONLY. No data row is populated in this document. Definitions only — this is not an accepted schema, not a migration, and not an API/data contract change to any existing system.

---

## 1. Design Principle

Both schemas below are built by reusing conventions already frozen elsewhere in the repository, rather than inventing a new vocabulary:

- the `source_id` / provenance-pointer discipline already used in `model3b_v2`'s `WAVE_2_OD_005_OPERATION_SOURCE_MAP.csv` pattern (a row never duplicates the cited file's content, only points at it with a locator);
- the "Evidence Contract" (§6) already frozen in `docs/thesis/pilot_annotation/ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_1_DRAFT.md`;
- the column set already proposed in the audited plan's own §11.2 (Relation ledger) and §11.4 (Contract-clause ledger).

Every ID field below is designed to be **cross-referenceable**, not to mint a competing ID space. Where `data/power_relations/painan_1663_relational_research_artifact.json` already assigns actor/treaty/relation IDs, this proposal's `existing_artifact_id` column is how a future row would point at that existing ID instead of creating a second one. Whether that cross-reference becomes the actual integration mechanism is exactly the question left open for the compatibility review in `G0_CANONICAL_LOCATION_RECOMMENDATION.md` §3 — this proposal is written so any of its four possible outcomes remains reachable from it.

Source authority is deliberately **not** asserted by either schema below: `source_class` and `verification_status` (source-inventory schema) exist precisely so that a repository-derived artifact, a working CSV, an unverified bibliographic reference, and a published document edition are never collapsed into a single undifferentiated "source."

---

## 2. Source Inventory Schema (11 columns, as implemented in the two accompanying CSVs)

Already implemented as data in:
`PAINAN_1662_1663_SOURCE_PATH_INVENTORY.csv`, `INDRAPURA_EIC_1680_1730_SOURCE_PATH_INVENTORY.csv`.

```text
source_id           -- primary key, e.g. PS-01 (Painan set) / IS-01 (Indrapura set)
title                -- source title as cited
author               -- author or compiling institution; "not yet identified" if unknown
path                 -- repository-relative path, or "NONE" if no local copy exists
format               -- PDF / CSV / JSON / Markdown / unknown
source_class         -- see allowed values below
coverage_period       -- date range the source covers
coverage_topic        -- what the source actually documents
already_used_in       -- other repository artifact(s) that already cite or derive from this source
verification_status   -- see allowed values below
notes                -- clarifies genre/edition ambiguity, verification method, or scope limits
```

**Allowed `source_class`:**
```text
PRIMARY_ARCHIVAL
PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION
SOURCE_FAITHFUL_TRANSCRIPTION
SECONDARY_SCHOLARSHIP
COLONIAL_SYNTHESIS
POPULAR_SUMMARY
REPOSITORY_DERIVED_ARTIFACT
WORKING_RESEARCH_DATA
UNVERIFIED_REFERENCE
```

**Allowed `verification_status`:**
```text
PATH_VERIFIED
FILE_VERIFIED
BIBLIOGRAPHIC_ONLY
CITED_ONLY_NOT_YET_LOCATED
MISSING_LOCAL_COPY
REQUIRES_FOLIO_OR_EDITION_CHECK
UNVERIFIED
```

File existence alone (`PATH_VERIFIED`) is never sufficient to imply historical or scholarly authority; that distinction is carried by `source_class`, and any residual genre ambiguity is carried in `notes` rather than silently resolved.

---

## 3. Claim-Source Ledger Schema (proposal, 12 columns, 0 rows populated)

```text
claim_id                       -- primary key for one claim (a single asserted
                                   fact, not a whole document)
case_id                        -- PAINAN_1663 | INDRAPURA_EIC_1680_1730
claim_text                     -- the specific factual assertion, stated
                                   narrowly (mirrors the audited plan's
                                   clause/relation-level granularity,
                                   §11.2/§11.4)
claim_type                     -- see allowed values below
source_id                      -- foreign key into the source inventory above
source_position                 -- specific locator within the source (page,
                                   folio, paragraph) -- must not be a vague
                                   file-level reference, matching the
                                   discipline already required by
                                   model3b_v2's registry schema for
                                   source_record_reference
source_relation                 -- see allowed values below
confidence_status               -- see allowed values below (no numeric
                                   confidence is used at G0 or any stage
                                   before a compatibility review authorizes
                                   otherwise)
colonial_classification_flag    -- whether the claim originates from a
                                   colonial archival label (VOC/EIC
                                   classification) as opposed to a
                                   source-independent observation, per
                                   audited plan §2.1
existing_artifact_id            -- OPTIONAL cross-reference to an actor_id /
                                   treaty_id / relation_id already present in
                                   data/power_relations/painan_1663_relational_research_artifact.json
                                   (or its V2.1-migrated counterpart); blank
                                   if no pre-existing counterpart exists
existing_ontology_entity        -- OPTIONAL cross-reference to the V2.1
                                   ontology entity this claim would
                                   instantiate under (Actor | Treaty |
                                   PowerRelation | Claim |
                                   StrategicInteraction | CommercialRight |
                                   RightModification | CommandObservation |
                                   OperationParticipation); left blank until
                                   the compatibility review determines
                                   whether this cross-reference is even the
                                   right mechanism
review_status                   -- DRAFT (no other value is valid before the
                                   compatibility review in
                                   G0_CANONICAL_LOCATION_RECOMMENDATION.md
                                   §3 completes)
```

**Allowed `claim_type`:**
```text
ACTOR_IDENTITY
REPRESENTATION_SCOPE
CONTRACT_CLAUSE
TRADE_RELATION
PROTECTION_RELATION
ALLIANCE_RELATION
FACTIONAL_RELATION
TERRITORIAL_CLAIM
COLONIAL_CLASSIFICATION
TEMPORAL_SEQUENCE
MECHANISM_HYPOTHESIS
OTHER_REQUIRES_REVIEW
```

**Allowed `source_relation`:**
```text
DIRECT_SUPPORT
PARTIAL_SUPPORT
CONTRADICTION
CONTEXT_ONLY
SOURCE_POSITION_ONLY
REQUIRES_REVIEW
```

**Allowed `confidence_status`:**
```text
HIGH_SOURCE_SUPPORT
MODERATE_SOURCE_SUPPORT
LOW_SOURCE_SUPPORT
NOT_YET_ASSESSED
NOT_IDENTIFIABLE
```

No numeric confidence value is used anywhere in this schema.

---

## 4. What This Document Does Not Do

- It does not populate a single claim row.
- It does not modify `ATLAS_POWER_RELATION_ONTOLOGY_CONTRACT_V2_1_DRAFT.md` or any other frozen ontology artifact.
- It does not modify `data/power_relations/painan_1663_relational_research_artifact.json`.
- It does not run the existing validators (`scripts/research_validators/validate_painan_1663_relational_artifact.py`, `validate_painan_1663_relational_prototype.py`).
- It does not decide the compatibility-review outcome.
- It does not assert source authority for any path listed in the accompanying source-path inventories; `source_class`/`verification_status` are the only carriers of that distinction.

## 5. Confirmation

This document contains no historical data filling, no modeling result, no simulation output, and no implementation. It is a column-and-enum definition proposal only.
