# Phase A0 Sprint Board — Required Audits (Enclave 1682 Critical Model)

Companion to `ENCLAVE_1682_CRITICAL_MODEL_PLAN.md` (commit `4ff7dff`), §15 "Phase A0 — Required audits (new, gates Phase A)".
Status: **Workstream 2 (A0-7…A0-11) complete and signed off. Workstream 1: A0-1/A0-2/A0-5 done, A0-3 in review, A0-4 rejected (moot), A0-6 rejected (no migration required). Overall Phase A0 gate (`S1-03`) not yet open, pending only A0-3's remaining fields or an explicit reviewer waiver.**

**Correction, this revision — the extraction-gap premise is formally withdrawn.** `A0-5`'s read-only diagnosis found, via direct row-level verification, that `SP-01267` and `SP-01344` already exist as canonical rows: `SP-01267 -> INV-0343` (Ammunitie van oorlogh, `military_inventory`, `L-SALIDO`), `SP-01344 -> INV-0401` (Waker transfer Beneden-Pagger, `transferred_military_inventory`, `L-BENEDEN-PAGGER`), both in `docs/enclave/salido_hdt_model_v0_4_1/10_inventory_items.csv`, sourced from `DOC-INVENTORY-1682-01-04`. There was no parser omission, no section filter, no vocabulary filter, no range truncation, and no deduplication defect — the rows were never missing. `evidence_status`/`review_status` are blank on both rows, matching every other row in the 403-row file; this is the pre-existing corpus-wide metadata-population gap (`REVIEW_QUEUE.md` §A), not evidence of absence. Full correction history in `A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md`.

## 0. Evidence-retention policy (correction, this revision)

**Local image retention is not required by this project.** The prior framing of `docs/enclave/scans/`'s absence as an external blocker conflated "scan access obtained" with "scan duplicated into this repository" — `docs/SOURCE_PROVENANCE.md` requires neither; it requires only that a reviewer examined the source and can cite repository/access/inventory/folio/quoted text. The research workflow deliberately does not copy Nationaal Archief folio images into this repository, and no ticket on this board authorizes creating `docs/enclave/scans/` or downloading/committing archival images.

Absence of a local image is **not** evidence that philological review did not occur. The evidence model distinguishes:

```text
source_examined_externally    — true (set by researcher, not inferred)
image_retained_locally        — false (standing default for this project)
image_retention_status        — not_retained_by_policy
verification_method           — external_archive_viewer
verified_against_local_image  — false (never set true under this policy)
canonical_extraction_status   — present (SP-01267 -> INV-0343, SP-01344 -> INV-0401 — see A0-5)
researcher_attestation_status — researcher_attested
```

The gate for `A0-3` is **researcher attestation completion** (`A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md` filled and reviewer-confirmed), not local image possession. Object identity and recorded quantities are now attested (committed `f98cfb0`) — `A0-3` is therefore **Review**, not yet **Done**: exact original Dutch spelling, folio number, viewer scan sequence, and IVdNT lemma remain unrecorded, and closing A0-3 fully requires either recording those or an explicit reviewer decision that object-and-count attestation alone is sufficient.

**Formerly-stated "remaining P0 issue" — withdrawn.** Earlier revisions of this board stated that `SP-01267`/`SP-01344` existed in `00_source_passages.csv` but were absent from `10_inventory_items.csv`. That claim was never re-verified by a direct row-level check and is false: `A0-5` confirmed both rows exist (`INV-0343`, `INV-0401`). No canonical-CSV work is required for these two records.

## Gate condition (repeated from the approved plan, not new)

Phase A (schema/derivation layer) may not begin, and no count above §8 tier 4 ("parent-child duplicated count") may be treated as more resolved than **provisional**, until both workstreams below reach reviewer sign-off. This is a hard prerequisite, not a target — if a sprint ends with open items in either workstream, Phase A stays blocked, full stop.

## Board conventions

- **Columns**: Backlog → In Progress → Blocked → Review → Done.
- All tickets start in **Backlog**. None are pre-assigned to In Progress by this setup.
- "Owner" is left blank throughout — this is a solo/small-team research project (no team-capacity or PTO planning applies, unlike a standard product sprint), so assignment is a manual step for whoever picks up the ticket, not a planning decision made here.
- Every acceptance criterion traces back to a specific section of the approved plan or a fact independently verified while setting up this board (marked **[refinement]** where it sharpens, but does not contradict, the approved plan's wording).

---

## Workstream 1 — Canonical-extraction audit for the two restraint rows

Traces to plan §15 Phase A0, bullet 1; §4 (P6, P7); §5 `restraint_device_review.csv`.

| ID | Ticket | Status | Depends on | Acceptance criteria |
|---|---|---|---|---|
| A0-1 | Confirm passage-level location of both entries in `00_source_passages.csv` | **Done (found during board setup)** | — | `SP-01267` ("1 belenggu dengan lima gelang dan satu kunci;", paragraph 1267) and `SP-01344` ("1 belenggu dengan tiga gelang dan satu kunci;", paragraph 1344) both confirmed present, both `review_status=researcher_docx`, both `image_verified=not_checked`. **[refinement]** — the plan's §15 language ("assign source_passage_ids") is slightly stronger than needed: the passage IDs already exist; what's missing is the link from passage → structured inventory row. |
| A0-2 | Document external-viewer philological attestation | **Done — `A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md` committed `f98cfb090aa41b3939a77bf33417dafd946724f7`** | — | Researcher attested object identity and recorded quantities for both entries (object/ring/key counts, inventory examination date, later collation date, `researcher_attestation_status=researcher_attested`, `source_examined_externally=true`). **No local JPG was used or required** — `docs/enclave/scans/` remains absent, as intended. |
| A0-3 | Reviewer confirms the philological attestation | **Review** | A0-2 (done) — no longer blocked on A0-2 or on local JPG availability | Object identity and recorded quantities are attested and reviewer-acknowledged. **Not yet closable to Done**: exact original Dutch spelling, folio number, viewer scan sequence, and IVdNT lemma are not recorded in the current attestation artifact (`A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md` leaves `reading`, `normalized reading`, `relevant lemma or search terms`, and `folio number` blank by design — nothing was invented to fill them). `verified_against_local_image` remains `false`, never set `true` under this policy. Closing A0-3 to Done requires either those fields being recorded, or an explicit reviewer decision that object-identity-and-count attestation alone is sufficient — not decided here. |
| A0-4 | Populate `restraint_device_review.csv` seed rows (critical layer, not canonical) | **Rejected — moot** | A0-1 | This ticket's scope was to seed audit rows tracking two *assumed-missing* canonical rows toward a future migration. `A0-5` found neither row is missing (`SP-01267 -> INV-0343`, `SP-01344 -> INV-0401`, both present in `10_inventory_items.csv`). There is nothing to audit toward a migration that isn't needed, so this ticket is rejected rather than completed — not because the work was done, but because its premise no longer exists. |
| A0-5 | Diagnose why the two entries produce no structured row | **Done** | A0-1, A0-2 | Read-only diagnosis complete: direct row-level verification against `10_inventory_items.csv` found both entries already exist as structured rows (`INV-0343`, `INV-0401`), sourced from `DOC-INVENTORY-1682-01-04`, `source_translation_full` matching the passage text exactly, positioned correctly among neighboring rows by `source_paragraph_index`. **No extraction defect of any kind exists** — no parser omission, section filter, vocabulary filter, range truncation, or deduplication issue. `evidence_status`/`review_status` blank on both rows matches the corpus-wide gap affecting all 403 rows, not a defect specific to these two. No migration proposed, none needed; `v0.4.1` was read-only throughout. Full finding and correction history in `A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md`. |
| A0-6 | Reviewer sign-off, Workstream 1 | **Rejected — no candidate correction or restraint-specific migration required** | A0-5 (done) | Originally scoped to sign off on a canonical-CSV correction proposal from `A0-5`. Since `A0-5` found no defect and no migration is needed, there is no correction to sign off on. `restraint_device_review.csv`'s `extraction_audit_required` concept is moot for these two rows for the same reason — nothing in the critical layer needs to track an extraction audit that found nothing wrong. |

---

## Workstream 2 — Cross-document temporal-overlap review

Traces to plan §15 Phase A0, bullet 2; §8 tier 6; §5 `group_hierarchy_review.csv`.

| ID | Ticket | Status | Depends on | Acceptance criteria |
|---|---|---|---|---|
| A0-7 | Enumerate all documents in the corpus with a time window overlapping the 1682-01-09 personnel register | **Done** | — | All 5 corpus documents enumerated and checked (exhaustive — the corpus contains only 5 documents total); findings in `CROSS_DOCUMENT_OVERLAP_FINDINGS.md` §2. Discrepancy flagged (archive catalogue period vs. two documents' internal dates), not resolved. |
| A0-8 | Check candidate documents for population overlap with the Beneden-Pagger and Madagascar-arrival cohorts | **Done** | A0-7 | Findings in `CROSS_DOCUMENT_OVERLAP_FINDINGS.md` §3: `DOC-PROTOCOL-1682` and `DOC-INVENTORY-1682-01-04` show structural overlap (cited by HRLT/claims row IDs); `DOC-ASSAY-1682-03-12` and `DOC-OLITSCH-1682-04-30` show none in currently-linked tables. Exhaustiveness limitation explicitly recorded: `00_source_passages.csv`'s `source_document_id` is empty for all 1488 rows, so "no overlap" for those two documents is bounded by that gap, not an absolute claim. |
| A0-9 | Confirm (or revise) the `group_hierarchy_review.csv` parent/child de-duplication decision | **Done** | A0-8 | Reviewer (Muhammad Ikbal) confirmed the plan's recommended assignment (`counts_toward_unique_person_estimate=true` on `G-MADA-64` parent, `false` on its 5 children) — no cross-document evidence found in A0-8 contradicts it; the only other reference to the cohort (`DOC-PROTOCOL-1682` claim `CL-003`) re-attests the same `group_id`, not a second count. `SUM(record_person_count WHERE counts_toward_unique_person_estimate)` across the Madagascar rows remains 64, never 128. |
| A0-10 | Document findings and update the tier-6 status in `archival_visibility.csv`/`uncertainty_critical.csv` scaffolding | **Done** | A0-8, A0-9 | `CROSS_DOCUMENT_OVERLAP_FINDINGS.md` written. States plainly that 308 (tier 5) still stands as the best available *provisional* figure. Tier 6 (`unique_person_verified_count`) explicitly recorded as remaining **unresolved** — this ticket did not and could not promote it, per the approval qualification. Tier-6 status recorded in prose (§5 of that document) pending Sprint 2 creating the actual `uncertainty_critical.csv` file to hold it. |
| A0-11 | Reviewer sign-off, Workstream 2 | **Done — signed off by Muhammad Ikbal** | A0-10 | Reviewer confirmed `CROSS_DOCUMENT_OVERLAP_FINDINGS.md`'s findings. `group_hierarchy_review.csv`'s `cross_document_temporal_overlap_checked` field is authorized to flip to `true` once Sprint 2 creates that file (the file does not exist yet — this sign-off pre-authorizes that specific field value for when it does). This sign-off closes **Workstream 2 only** — Workstream 1 is now A0-1/A0-2/A0-5 done, A0-3 in review, A0-4/A0-6 rejected (moot, no defect found); the overall Phase A0 gate (`S1-03`) stays blocked only on A0-3 closing (its remaining fields or an explicit reviewer waiver). |

---

## Sprint sequencing note

A0-1, A0-2, and A0-5 are done. A0-4 and A0-6 are rejected — both were scoped around an extraction-gap premise that A0-5 disproved. Only A0-3 remains open. **No ticket in this workstream depends on external scan access any longer.**

## Explicitly not on this board

- No Phase A (schema/derivation layer) tickets — blocked entirely until both workstreams reach sign-off. **A0-11 signed off; A0-3 in Review is the only Workstream 1 item still open** (A0-3 needs original reading/folio/lemma recorded or an explicit reviewer decision that object-and-count attestation alone suffices) — per the gate condition above, Phase A stays blocked until A0-3 closes. A0-4/A0-6 are rejected, not pending — they do not block anything further.
- No ticket authorizes writing to any canonical dataset, solver snapshot, or Docker configuration — consistent with every prior approval in this project.
- **No ticket authorizes creating `docs/enclave/scans/` or downloading/committing archival images** — local image retention is not required by this project's evidence policy (`docs/SOURCE_PROVENANCE.md`).
- No estimate/story-point/velocity fields — this board tracks archival-review dependencies and gate status, not delivery-date forecasting, since the binding constraint here is attestation completion and reviewer availability, not engineering capacity.
- Preserved unchanged: actual restraint-device *use* and *target person* remain `not_recorded` and must never be inferred (P6) — this correction changes how presence is verified, not what may be claimed about use. Canonical `v0.4.1` remains immutable throughout.

---

*Workstream 2 (A0-7…A0-11) executed and signed off via direct, read-only queries against the canonical v0.4.1 CSVs — full findings in `CROSS_DOCUMENT_OVERLAP_FINDINGS.md`. Workstream 1's evidence-retention policy corrected in an earlier revision — no local scan required or permitted; A0-1/A0-2/A0-5 done, A0-3 in review, A0-4/A0-6 rejected after A0-5's read-only diagnosis found no extraction defect and no missing canonical row. No canonical dataset, solver snapshot, application code, or Docker configuration was modified at any point.*
