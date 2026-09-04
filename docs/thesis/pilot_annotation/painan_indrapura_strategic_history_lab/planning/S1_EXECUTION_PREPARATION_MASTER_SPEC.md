# S1 — Retrieval and Indexing Execution Preparation Master Spec

**Status:** PLANNING AND AUTHORIZATION-SURFACE REVIEW ONLY. No retrieval, download, OCR, extraction, transcription, indexing, or claim entry is performed by this document or by any artifact accompanying it. No source file is opened. No source class or verification status is changed.

**Authoritative baseline:** `477182ea120331f2667c0eead2e7dea58bed477a`

---

## 1. Purpose

This spec turns the frozen S1 source-readiness plan (5 artifacts, committed and server-synced) into a deterministic execution surface: exactly which of the 18 retrieval/indexing targets need what kind of access (local metadata only, local content, external lookup, external retrieval, or a user-supplied source), grouped into batches that can each be separately authorized, with output schemas, gates, checksums, stop conditions, and rollback actions defined in advance. No batch is executed this turn.

---

## 2. Audit of Frozen S1 Inputs

```text
work-package registry      = 12 columns x 12 rows, 12/12 unique, 12/12 PLANNED_ONLY
retrieval/indexing plan     = 12 columns x 18 rows, 18/18 unique, 18/18 PLANNED_ONLY
content_extraction_authorized = 0/18
claim_entry_authorized        = 0/18
UNRESOLVED_BY_VERIFICATION_STATUS_SOURCE_ID_COUNT = 6
UNVERIFIED_REFERENCE_SOURCE_CLASS_ID_COUNT        = 12
UNIQUE_UNRESOLVED_BIBLIOGRAPHIC_TARGET_COUNT       = 11
UNIQUE_UNRESOLVED_RETRIEVAL_TARGET_COUNT           = 11
G0_SOURCE_GAP_ENTRY_COUNT                          = 5
```

All confirmed unchanged from the frozen, server-synced S1 planning artifacts. No discrepancy found.

---

## 3. Execution Classes (8 allowed, all used except `WITHHELD_REQUIRES_REVIEW`)

```text
LOCAL_METADATA_ONLY
LOCAL_FILE_IDENTITY_REVIEW
LOCAL_CONTENT_INDEXING_REQUIRES_AUTHORIZATION
EXTERNAL_BIBLIOGRAPHIC_LOOKUP_REQUIRES_AUTHORIZATION
EXTERNAL_SOURCE_RETRIEVAL_REQUIRES_AUTHORIZATION
USER_SUPPLIED_SOURCE_REQUIRED
METHOD_TASK_NO_SOURCE_ACCESS
WITHHELD_REQUIRES_REVIEW
```

**Distribution across the 18 frozen retrieval targets (full detail in `S1_EXECUTION_TARGET_REGISTRY.csv`):**

```text
LOCAL_CONTENT_INDEXING_REQUIRES_AUTHORIZATION        = 12  (ET-03..ET-09, ET-14..ET-18)
EXTERNAL_BIBLIOGRAPHIC_LOOKUP_REQUIRES_AUTHORIZATION = 4   (ET-01, ET-02, ET-10, ET-13)
LOCAL_FILE_IDENTITY_REVIEW                            = 1   (ET-12)
EXTERNAL_SOURCE_RETRIEVAL_REQUIRES_AUTHORIZATION      = 1   (ET-11)
```

`PATH_VERIFIED` did not authorize content opening for any target: the 6 CD volumes and the Kathirithamby-Wells 1976 article are `PATH_VERIFIED` but were classified `LOCAL_CONTENT_INDEXING_REQUIRES_AUTHORIZATION`, not `LOCAL_METADATA_ONLY`, because their planned action requires reading the file's content. `CITED_ONLY_NOT_YET_LOCATED` did not authorize internet retrieval for Veevers, Fort York, Vogel, or the Kathirithamby thesis: each remains `REQUIRES_AUTHORIZATION`, not executed. No `UNVERIFIED_REFERENCE` source was promoted.

---

## 4. Batches (6, mechanically derived — see §6 for why the original 5-scope sketch became 6 target-mapped batches)

```text
S1-B0  Metadata reconciliation                          — all 18 targets, content_access=NO, network=NO
S1-B1  Bibliographic identity review                     — 10 targets, content_access=NO, network=YES
S1-B2  Local source-position indexing                    — 8 targets,  content_access=YES, network=NO
S1-B3  External source retrieval                         — 5 targets,  content_access=NO, network=YES
S1-B4  Repository-derived artifact provenance audit       — 5 targets,  content_access=YES, network=NO
S1-B5  Methodology gates                                  — 0 retrieval targets (operates on S1-WP10/11/12), content_access=NO, network=NO
```

Full detail, including exact `target_ids`, preconditions, success criteria, stop conditions, and rollback boundaries, is in `S1_EXECUTION_BATCH_REGISTRY.csv`. No batch is marked `AUTHORIZED` or `READY_TO_EXECUTE` — all six are `PLANNED_ONLY`.

Note on batch derivation: the instruction's own five illustrative scopes (B0–B4) already matched the frozen 18 targets one-for-one once De Leeuw (edition review, B1+B2), the CD volumes (identity then indexing, B1+B2), Kathirithamby-Wells 1976 (content crosscheck, B2 only — its identity is already known, unlike the PhD thesis), and Fort York (local git trace first, then conditional external escalation, B1 role reassigned to `LOCAL_FILE_IDENTITY_REVIEW` rather than a network lookup) were mapped precisely. The sixth batch, S1-B5 (methodology gates), was added because the instruction's own §12 scope ("source-position rules; admissibility gates; empty claim-ledger instantiation prerequisites") corresponds exactly to work packages S1-WP10/WP11/WP12, which carry no `retrieval_id` at all (they are the three intentional, non-retrieval orphans already confirmed in the frozen retrieval plan) — so this scope needed its own batch rather than being folded into a target-bearing one.

---

## 5. Future Output Artifact Contracts (schemas only, 0 rows populated by this turn)

```text
S1_SOURCE_IDENTITY_REVIEW.csv
  source_id,title,claimed_class,verified_publisher_or_compiler,verified_edition_or_identity,
  evidence_reference,source_class_before,source_class_after,verification_status_before,verification_status_after

S1_LOCAL_SOURCE_POSITION_INDEX.csv
  source_id,document_id,date,place,actor,folio_or_page,index_confidence

S1_EXTERNAL_RETRIEVAL_MANIFEST.csv
  source_id,title,acquisition_method,acquired_path,acquisition_date,doi_or_reference_match_verified,verification_status_after

S1_DERIVED_ARTIFACT_PROVENANCE_AUDIT.csv
  record_id,record_type,repository_derived_source_id,traced_source_id,traced_source_position,trace_confidence,unsourced_flag

S1_EXECUTION_AUDIT.md
  narrative audit log referencing the four CSVs above; no historical claim; records only what was checked, found, or left unresolved
```

Every future output must preserve: source ID; exact source path or bibliographic reference; source class before and after review; verification status before and after review; evidence for any promotion; position (page/folio/document/record) when available; checksum where a local file exists; no silent source-class promotion; no claim entry without a later, separately authorized gate.

---

## 6. Gates (restated from `S1_SOURCE_ADMISSIBILITY_AND_PROMOTION_RULES.md`, applied per-target in the registry)

```text
identity_gate       — Gate 2 (bibliographic identity) and, where relevant, Gate 3 (edition identity)
admissibility_gate  — Gates 4/6/7/8/9/12 as applicable per target (see registry column `admissibility_gate`)
checksum_required   — YES wherever a local file currently exists (recorded per target)
stop_condition      — per-target, e.g. "stop if no external catalog record confirms the edition"
rollback_action     — per-target; every rollback action is either "no file changes occur" or "delete only the newly acquired/derived artifact"
```

No source may be promoted to `PRIMARY_ARCHIVAL` merely because a local PDF exists. No repository-derived JSON, working CSV, or dossier may become primary evidence. No popular or secondary summary may establish actor motive by itself. These constraints are enforced per-row in `S1_EXECUTION_TARGET_REGISTRY.csv` via the `identity_gate` and `admissibility_gate` columns, and none of the 18 rows sets `execution_status` to anything other than `PLANNED_ONLY`.

---

## 7. Scientific and Workstream Boundaries (unchanged, restated)

```text
Painan hypotheses:            6/6 HYPOTHESIS_ONLY_NOT_ADJUDICATED
Indrapura-EIC research questions: 6/6 REQUIRES_SOURCE_AUDIT
Game-theory model:            NOT STARTED
Hawkes:                       DEFERRED_TO_G7
Counterfactual visualization: NOT IMPLEMENTED
```

No batch, target, or gate defined in this turn generates a finding, score, preference, payoff, or causal ranking.

---

## 8. Confirmation

This document, and the two accompanying CSVs, define an execution surface only. Zero source files were opened. Zero content was extracted, OCR'd, or transcribed. Zero claims were entered. Zero source classes or verification statuses were changed. Zero URLs, archive identifiers, folio numbers, page positions, local paths, document identities, or checksums were fabricated — every path cited above already appears in the frozen G0 source-path inventories or the frozen S1 retrieval/indexing plan.
