# Cross-Document Temporal-Overlap Findings — Phase A0, Workstream 2 (A0-10)

Status: **findings documented, reviewer sign-off (A0-11) still outstanding**
Ticket: `A0-10` in `PHASE_A0_SPRINT_BOARD.md` — "Document findings and update the tier-6 status in `archival_visibility.csv`/`uncertainty_critical.csv` scaffolding"
Depends on: `A0-8`, `A0-9` (both addressed below)
Scope: `S1-02` in `ENCLAVE_1682_BACKLOG.csv`

This document is the A0-10 deliverable. It does **not** close `A0-9` or `A0-11` — both require an explicit decision by a named reviewer who is not the author of this analysis. It does not modify any canonical dataset, and it does not create `archival_visibility.csv` / `uncertainty_critical.csv` (those files do not exist yet — they are gated behind Sprint 2, itself gated behind Phase A0 sign-off, so "updating their tier-6 status" is not yet a file-level action this ticket can perform; the tier-6 status this ticket *can* set is recorded in prose here, to be transcribed into the actual CSV once Sprint 2 creates it).

---

## 1. Method

The entire canonical corpus (`docs/enclave/salido_hdt_model_v0_4_1/`) contains exactly **5 documents** (`01_documents.csv`). For each, every canonical table that carries a `source_document_id` column was queried directly — `06_human_groups.csv`, `04_person_roles.csv`, `07_human_role_location_time.csv`, `11_claims.csv`, `09_assay_results.csv`, `08_weekly_operations.csv`, `10_inventory_items.csv`, `12_numeric_anomalies.csv`, `00_source_passages.csv` — to find every row citing each document, then cross-checked whether the same `person_id`/`group_id` appears under more than one `document_id`. No sampling: this is a complete pass over every row in every source_document_id-bearing table in the corpus.

## 2. A0-7 — Document enumeration

| Document | `date_iso` | Type | Rows citing it (any table) |
|---|---|---|---|
| `DOC-PERSONNEL-1682-01-09` | 1682-01-09 | personnel register | baseline — source of all 50 persons + all 17 groups |
| `DOC-INVENTORY-1682-01-04` | 1682-01-04 | inventory | 403 (`10_inventory_items.csv`) + 1 (`07_human_role_location_time.csv`) |
| `DOC-PROTOCOL-1682` | 1682 (no specific day — original: *"beginne des 1682sten jaars"*) | mine protocol | 42 (`08_weekly_operations.csv`) + 19 (`09_assay_results.csv`) + 6 (`11_claims.csv`) + 2 (`07_human_role_location_time.csv`) |
| `DOC-ASSAY-1682-03-12` | 1682-03-12 | assay report | 0 |
| `DOC-OLITSCH-1682-04-30` | 1682-04-30 | letter | 0 |

All 5 fall within calendar year 1682 at the same enclave — every one qualifies as a temporal-overlap candidate against the personnel register; none was excluded from A0-8's check on date grounds alone.

**Discrepancy flagged, not resolved**: the archive's own catalogue statement (`00_source_passages.csv` row `SP-00002`: *"7964 1682 mrt. 12 - dec. 28"*) gives the inventory unit's period as starting 12 March, but `DOC-INVENTORY-1682-01-04` (4 Jan) and `DOC-PERSONNEL-1682-01-09` (9 Jan) both predate that. This is left for reviewer attention — it does not change any finding below, since both documents are already included as overlap candidates regardless.

## 3. A0-8 — Population overlap per document

| Document | Overlap with `DOC-PERSONNEL-1682-01-09`'s population? | Evidence |
|---|---|---|
| `DOC-PROTOCOL-1682` | **Yes** | `P-VOGEL` and `P-PLEIJTNER` (named individuals, role sourced from `DOC-PERSONNEL-1682-01-09` via `04_person_roles.csv`) reappear with an explicit validity window **1681-12-29 → 1682-04-30** (`HRLT-0001`, `HRLT-0002`, `07_human_role_location_time.csv`). Aggregate groups `G-MADA-64` and `G-HWJ-6` (sourced *only* from `DOC-PERSONNEL-1682-01-09` in `06_human_groups.csv`) are independently re-referenced by claims `CL-003` ("`G-MADA-64` arrived_from `L-MADAGASCAR`") and `CL-004` ("`G-HWJ-6` classified_as halfwasse cleene jongens") in `11_claims.csv`. |
| `DOC-INVENTORY-1682-01-04` | **Yes** | `P-ROELINGH` (Willem Roelingh, named individual from the personnel register) appears via `HRLT-0005` (role `R-ASSAIJEUR`, location `L-POULO-CHINCO`, `valid_from 1682-01-04`). This document is also the sole source of the two restraint-device passages (`SP-01267`, `SP-01344`) under audit in Workstream 1. |
| `DOC-ASSAY-1682-03-12` | No structural overlap found | Zero rows in any `source_document_id`-bearing table cite this document. |
| `DOC-OLITSCH-1682-04-30` | No structural overlap found | Zero rows cite this document, despite its author (`P-OLITSCH`) being a named person in the personnel register — the letter itself has no structured extraction linking back to it. |

**Nature of the overlap found**: in every case, the re-reference is a *qualitative re-attestation* of an entity whose identity/count already exists in `DOC-PERSONNEL-1682-01-09` — a role confirmation, a location assignment, a classification restatement, an arrival-origin claim. In no case does a second document supply an *independent count* of people that would need to be reconciled against `06_human_groups.csv`'s counts. This distinction matters directly for §4 below.

**Exhaustiveness limitation — must be carried forward, not glossed over**: `00_source_passages.csv`'s `source_document_id` column is empty for **all 1488 rows**, and `12_numeric_anomalies.csv`'s for all 5 rows (a pre-existing gap already logged in `REVIEW_QUEUE.md` §A, predating this review). The "no overlap found" verdicts for `DOC-ASSAY-1682-03-12` and `DOC-OLITSCH-1682-04-30` are exhaustive only over tables that already carry document linkage — they cannot rule out an un-linked passage in either document referencing the same population. **This review is exhaustive over currently-structured data, not exhaustive over the full corpus text.**

## 4. A0-9 — Parent/child de-duplication decision (informational input, not a closed decision)

No cross-document evidence found in this review contradicts the critical model plan's recommended assignment:
- `G-MADA-64` (parent, count 64) → `counts_toward_unique_person_estimate = true`
- Its 5 components (`G-MADA-VJ-10`, `G-MADA-HJ-8`, `G-MADA-VM-30`, `G-MADA-HM-10`, `G-MADA-K-6`) → `counts_toward_unique_person_estimate = false`

The only other document referencing the Madagascar cohort at all (`DOC-PROTOCOL-1682`, claim `CL-003`) re-attests the *same* `group_id` — not a second, independent count of a possibly-overlapping-but-distinct set of people. This is consistent with, but does **not by itself constitute**, reviewer confirmation of `A0-9`. A named reviewer still needs to make that determination explicitly.

## 5. Tier-6 status (§8 of `ENCLAVE_1682_CRITICAL_MODEL_PLAN.md`)

Per this review:

- **Tier 5 (unique-person estimate, 308)**: no cross-document evidence found that would revise this figure. It stands as the best available *provisional, single-document-derived* estimate, now additionally checked (not merely assumed) against every other document in the corpus for a competing count — none was found.
- **Tier 6 (unique-person verified count)**: **remains unresolved.** This review does not, and by its own design cannot, promote 308 to "verified" — per the approval qualification on this programme, that requires a separate, explicit decision, not an inference from absence of a contradicting count. Nothing in this document should be read as closing tier 6.

This is the tier-6 status to be transcribed into `uncertainty_critical.csv`'s `count_tier` field once that file exists (Sprint 2) — recorded here in the meantime since the file itself cannot yet hold it.

## 6. What this document does not do

- Does not confirm `A0-9` — that remains a reviewer decision.
- Does not record `A0-11` sign-off, and does not flip `group_hierarchy_review.csv`'s `cross_document_temporal_overlap_checked` field (that file does not exist yet).
- Does not change `PHASE_A0_SPRINT_BOARD.md`'s ticket statuses — `A0-7`/`A0-8`/`A0-9`/`A0-10` remain as currently recorded there unless and until the board is explicitly updated in a separate step.
- Does not modify any canonical dataset, solver snapshot, application code, or Docker configuration.

## 7. Recommended next step

`A0-11` (reviewer sign-off, Workstream 2) is now the only remaining ticket in Workstream 2 — its acceptance criterion ("a named reviewer confirms A0-10's findings") can be evaluated directly against this document. This is a decision point for you, not an automatic follow-on I should take.

---

*End of findings. Not committed — no commit was requested for this file.*
