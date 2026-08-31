# S1 — Source Admissibility and Promotion Rules

**Status:** PLANNING ONLY. No source is reclassified by this document. No claim is entered. These rules govern future retrieval, indexing, and claim-entry work; they are not applied to any source this turn.

**Governing principle, restated exactly:**

```text
PATH_EXISTS != BIBLIOGRAPHIC_IDENTITY_VERIFIED != SOURCE_AUTHORITY_ESTABLISHED != CLAIM_SUPPORTED
```

A file being present in the repository (`PATH_VERIFIED`) establishes nothing beyond its own presence. Every step to the right of `!=` above is a separate, harder condition that must be independently satisfied.

---

## 1. Source Classes (frozen at G0, unchanged here)

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

No source may be promoted out of `UNVERIFIED_REFERENCE` into any of `PRIMARY_ARCHIVAL`, `PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION`, or `SOURCE_FAITHFUL_TRANSCRIPTION` merely because a local file exists at its recorded path. Promotion requires passing the specific gate for that target class, below.

---

## 2. Twelve Admissibility Gates

### Gate 1 — File Existence
A path resolves to an actual file in the repository. This is the weakest gate and proves nothing beyond itself. Corresponds to `verification_status = PATH_VERIFIED` or `FILE_VERIFIED`.

### Gate 2 — Bibliographic Identity
The file's title, author, publisher/compiler, and date are confirmed against an external bibliographic record (library catalog, publisher record, DOI, or an already-verified secondary source that cites it correctly) — not merely inferred from the filename.

### Gate 3 — Edition Identity
For any published work, the specific edition, printing, or reprint is identified, distinguishing a first edition from a later reprint or translation, and distinguishing a document edition (a scholarly publication of an archival text) from a narrative work about that text.

### Gate 4 — Primary versus Published-Primary Status
A source is `PRIMARY_ARCHIVAL` only if it is the archival original or a source-faithful facsimile/transcription of it. A source that publishes, translates, or reproduces a primary document within a scholarly apparatus is `PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION` at most, never `PRIMARY_ARCHIVAL`, unless independently shown to be a facsimile.

### Gate 5 — Source-Faithful Transcription Status
A transcription is admitted as `SOURCE_FAITHFUL_TRANSCRIPTION` only when a verification method exists to compare it against the original (e.g., a stated transcription methodology, editorial apparatus, or cross-check against a second independent transcription). Absent that, it is capped at `PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION` or `COLONIAL_SYNTHESIS`.

### Gate 6 — Repository-Derived Artifact Status
Any file generated inside this repository (coded JSON, episode dossiers, working CSVs, prior analytical notes) is `REPOSITORY_DERIVED_ARTIFACT` or `WORKING_RESEARCH_DATA`, never a primary or secondary source class in its own right, regardless of how thorough its content appears. It may only be *cited as a pointer* to the primary/secondary sources it was itself derived from (see Gate 12).

### Gate 7 — Source-Position Resolution
A specific, checkable locator exists: page, folio, paragraph, or (for repository-derived artifacts) record ID. A file-level reference alone ("see this PDF") does not satisfy this gate.

### Gate 8 — Quotation/Transcription Verification
Any quoted or transcribed text attributed to a source is checked, at minimum, against the source's own pagination/structure so a reader could independently locate the same passage.

### Gate 9 — Claim-Support Relationship
The specific relationship between the source and the claim it is cited for is declared as one of `DIRECT_SUPPORT`, `PARTIAL_SUPPORT`, `CONTRADICTION`, `CONTEXT_ONLY`, `SOURCE_POSITION_ONLY`, or `REQUIRES_REVIEW` (per the claim-source ledger schema frozen at G0). A source being merely *cited elsewhere in the repository* does not by itself establish `DIRECT_SUPPORT`.

### Gate 10 — Colonial Classification Flag
Every claim sourced from a VOC or EIC institutional record is flagged for whether it originates from a colonial administrative/archival classification (e.g., a label such as "rebel," "loyal," or a treaty's own self-description) as opposed to an independent observation, per the audited plan's §2.1 principle.

### Gate 11 — Confidence-Status Assignment
Confidence is assigned only from the frozen enum (`HIGH_SOURCE_SUPPORT`, `MODERATE_SOURCE_SUPPORT`, `LOW_SOURCE_SUPPORT`, `NOT_YET_ASSESSED`, `NOT_IDENTIFIABLE`). No numeric confidence value is used at any stage before a separate authorization changes this rule.

### Gate 12 — Cross-Source Contradiction Handling
When two or more sources bearing on the same claim disagree, the contradiction is recorded explicitly (as a `CONTRADICTION` source-relation entry, per Gate 9) rather than silently resolved by preferring one source, and rather than averaged or blended into a composite narrative.

---

## 3. Worked Boundary Cases (illustrative, not a promotion decision)

- **Het Painansch Contract (PS-01):** currently `REQUIRES_FOLIO_OR_EDITION_CHECK`. Passing Gate 1 (file exists) does not pass Gates 2–4. It remains `PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION` at best until its edition is verified (S1-WP01); it must never be treated as `PRIMARY_ARCHIVAL`.
- **`data/power_relations/painan_1663_relational_research_artifact.json` (PS-09):** passes Gate 1 and Gate 6 only. It is `REPOSITORY_DERIVED_ARTIFACT`, and every actor/treaty/relation record inside it must itself point back to a source_id under Gate 12/S1-WP08 before it can support a claim.
- **`INDERAPURA_EPISODE_DOSSIER_DRAFT.md` (IS-01):** passes Gate 1 and Gate 6 only. It quotes Vogel and CD4, but neither Vogel (IS-06) nor CD4's own identity (IS-07/PS-06) currently passes Gate 2. The dossier itself is not primary evidence.
- **CD1–CD6 volumes (PS-03..PS-08, IS-07):** pass Gate 1 only. No volume passes Gate 2 (bibliographic identity of the compiler/edition) or Gate 7 (position resolution) until S1-WP03's indexing work is done.

---

## 4. Claim-Entry Gate (Composite)

No historical claim may enter the future claim-source ledger unless all of the following hold simultaneously:

```text
source_id resolves
source class is declared
source position is specified
source relation is declared
confidence status is declared
colonial classification flag is reviewed
claim text is distinguished from source wording
repository-derived artifacts point back to their source chain
```

**Required status for claim entry during this turn: `NOT AUTHORIZED`.**

---

## 5. Confirmation

This document defines rules only. It does not promote, demote, or reclassify any source_id in either G0 source-path inventory. It does not populate the claim-source ledger. It contains no historical claim, model result, or simulation output.
