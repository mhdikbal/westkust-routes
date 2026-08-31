# S1 — Source Readiness Master Plan

**Status:** PLANNING ONLY. No source retrieval, indexing, extraction, OCR, claim entry, modeling, or simulation is performed by this document. No canonical artifact is modified.

**Authoritative baseline:** `4b0a6515d7dd976d101245817b3b81ab7d0c7257`
**Authoritative G0 path:** `docs/thesis/pilot_annotation/painan_indrapura_strategic_history_lab/`
**Sprint:** S1, Source Readiness

---

## 1. Purpose

S1 exists to close the source gaps identified in `G0_SOURCE_GAP_REPORT.md` and to establish the retrieval, indexing, and admissibility discipline required before any claim about Painan 1663 or Indrapura–EIC 1680–1730 may be entered into a claim-source ledger. S1 produces plans and rules only; it does not itself retrieve, transcribe, index, or interpret a single source.

---

## 2. Audit Summary of G0 Inputs

### 2.1 Painan 1662–1663 (17 source_ids, `PAINAN_1662_1663_SOURCE_PATH_INVENTORY.csv`)

```text
PATH_VERIFIED or FILE_VERIFIED = 15 (PS-01..PS-16)
UNVERIFIED                     = 1  (PS-17, Batangkapas antecedent)
REQUIRES_FOLIO_OR_EDITION_CHECK = 1 (PS-01, Het Painansch Contract)
```

Source-class distribution:

```text
PUBLISHED_PRIMARY_OR_DOCUMENT_EDITION = 1  (PS-01)
SECONDARY_SCHOLARSHIP                 = 1  (PS-02)
UNVERIFIED_REFERENCE                  = 7  (PS-03..PS-08, PS-17)
REPOSITORY_DERIVED_ARTIFACT           = 3  (PS-09, PS-10, PS-11)
WORKING_RESEARCH_DATA                 = 5  (PS-12..PS-16)
```

### 2.2 Indrapura–EIC 1680–1730 (8 source_ids, `INDRAPURA_EIC_1680_1730_SOURCE_PATH_INVENTORY.csv`)

```text
PATH_VERIFIED or FILE_VERIFIED  = 4  (IS-01, IS-02, IS-03, IS-07)
CITED_ONLY_NOT_YET_LOCATED       = 4  (IS-04, IS-05, IS-06, IS-08)
```

Source-class distribution:

```text
REPOSITORY_DERIVED_ARTIFACT = 1  (IS-01)
WORKING_RESEARCH_DATA       = 2  (IS-02, IS-03)
UNVERIFIED_REFERENCE        = 5  (IS-04, IS-05, IS-06, IS-07, IS-08)
```

### 2.3 Gap Report Summary (from `G0_SOURCE_GAP_REPORT.md`, tokens unchanged)

```text
Veevers (2021)                        = BIBLIOGRAPHIC_REFERENCE_ONLY
EIC Fort York / Batang Capas 1686      = LOCAL_FILE_MISSING
CD1-CD6 volume-topic index             = INDEXING_INCOMPLETE
Indrapura EIC-side primary material    = EIC_SIDE_COVERAGE_INSUFFICIENT
1662 Batangkapas antecedent            = PRIMARY_SOURCE_NOT_LOCATED
```

**No gap is filled by this plan.** These five findings are the direct origin of S1-WP02, S1-WP05, S1-WP03, S1-WP07, and S1-WP02 respectively (work packages defined in `S1_SOURCE_RESOLUTION_WORK_PACKAGE_REGISTRY.csv`).

---

## 3. S1 Work Packages (12, registered in full in the accompanying CSV)

```text
S1-WP01  Resolve bibliographic identity and edition status of Het Painansch Contract
S1-WP02  Locate and classify the 1662 Batangkapas antecedent source
S1-WP03  Index relevant CD1-CD6 volumes by document, date, place, actor, and folio/page position
S1-WP04  Resolve Kathirithamby-Wells citation and source-use boundary
S1-WP05  Locate or register a source-faithful local copy of Veevers
S1-WP06  Locate EIC Fort York / Batang Capas materials
S1-WP07  Audit EIC-side Indrapura coverage
S1-WP08  Audit the provenance of Painan relational JSON and working CSV files
S1-WP09  Audit the source coverage of INDERAPURA_EPISODE_DOSSIER_DRAFT.md
S1-WP10  Define source-position citation rules before claim entry
S1-WP11  Define primary-source and document-edition admissibility gates
S1-WP12  Prepare empty claim-source ledger instantiation plan
```

None of these twelve work packages is executed this turn. Each row in `S1_SOURCE_RESOLUTION_WORK_PACKAGE_REGISTRY.csv` carries `execution_status = PLANNED_ONLY`.

## 4. Dependency Graph (text form)

```text
S1-WP01 ──┐
S1-WP03 ──┼──> S1-WP08 (provenance trace needs edition + volume index)
S1-WP04 ──┘

S1-WP03 ──> S1-WP02 (Batangkapas search benefits from CD indexing)

S1-WP05 ──┐
S1-WP06 ──┼──> S1-WP07 (EIC-side coverage audit needs both located first)
          │
S1-WP03 ──┘ (CD4 identity feeds Indrapura coverage too)

S1-WP03 ──┐
S1-WP06 ──┼──> S1-WP09 (dossier citation cross-check needs CD index + Vogel/Fort York located)
          │

S1-WP10 ──┐
S1-WP11 ──┼──> S1-WP12 (ledger instantiation needs rules frozen first)
```

No cycle exists. S1-WP10 and S1-WP11 (the rules) have no upstream blocker and are drafted in full this turn as `S1_SOURCE_ADMISSIBILITY_AND_PROMOTION_RULES.md` — drafting the rules text is in scope for S1 planning; *applying* them to any actual source is not.

---

## 5. Retrieval and Indexing Plan (summary; full detail in the accompanying CSV)

18 retrieval/indexing targets are registered, covering every `UNVERIFIED_REFERENCE`, `CITED_ONLY_NOT_YET_LOCATED`, or `REQUIRES_FOLIO_OR_EDITION_CHECK` source_id from both inventories, plus a provenance-trace target for every `REPOSITORY_DERIVED_ARTIFACT`/`WORKING_RESEARCH_DATA` entry. Every row has `content_extraction_authorized = NO`, `claim_entry_authorized = NO`, `status = PLANNED_ONLY`. No URL, archive reference number, or folio position is fabricated; where such information is not yet known, the field states that it is to be determined by the retrieval action itself.

---

## 6. Claim-Entry Prerequisites

Restated from `S1_SOURCE_ADMISSIBILITY_AND_PROMOTION_RULES.md` §4:

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

**Claim entry status this turn: `NOT AUTHORIZED`.**

---

## 7. Painan Interpretive Boundary

All six competing explanations for the Painan treaty remain unadjudicated:

```text
ANTI_ACEH_LIBERATION        = HYPOTHESIS_ONLY_NOT_ADJUDICATED
COMMERCIAL_RENEGOTIATION    = HYPOTHESIS_ONLY_NOT_ADJUDICATED
FACTIONAL_COMPETITION       = HYPOTHESIS_ONLY_NOT_ADJUDICATED
STRATEGIC_HEDGING           = HYPOTHESIS_ONLY_NOT_ADJUDICATED
VOC_CONTRACTUAL_CAPTURE     = HYPOTHESIS_ONLY_NOT_ADJUDICATED
COMPOSITE_MECHANISM         = HYPOTHESIS_ONLY_NOT_ADJUDICATED
```

No preferred conclusion is selected by this plan or by any S1 work package.

## 8. Indrapura–EIC Research Questions

All six framings remain open research questions, not findings:

```text
ALTERNATIVE_COMMERCIAL_PARTNER                              = REQUIRES_SOURCE_AUDIT
HEDGE_AGAINST_VOC                                            = REQUIRES_SOURCE_AUDIT
FACTIONAL_PATRON                                             = REQUIRES_SOURCE_AUDIT
CLAIMANT_SUPPORTER                                           = REQUIRES_SOURCE_AUDIT
FORTIFIED_TERRITORIAL_ACTOR                                  = REQUIRES_SOURCE_AUDIT
TERRITORIAL_STRATEGY_CONSTRAINED_BY_MOBILITY_AND_NETWORKS    = REQUIRES_SOURCE_AUDIT
```

---

## 9. Explicit Non-Goals This Turn

```text
No source extraction
No OCR
No claim filling
No validator execution
No Hawkes execution
No game-theory model execution
No counterfactual simulation
No visualization
No S2, S3, S4, S5, S6, S7, or S8 start
No OP-10 continuation
No stage, commit, push, or server-sync
```

## 10. Confirmation

This plan contains no historical data filling, no modeling result, no simulation output, and no implementation. It audits G0 inputs, defines work packages and their dependencies, and points to the two accompanying rule/plan artifacts. It does not modify any of the seven G0 substantive deliverables, the canonical sprint board, `.gitignore`, or any protected artifact.
