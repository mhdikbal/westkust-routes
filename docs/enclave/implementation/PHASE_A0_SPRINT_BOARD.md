# Phase A0 Sprint Board — Required Audits (Enclave 1682 Critical Model)

Companion to `ENCLAVE_1682_CRITICAL_MODEL_PLAN.md` (commit `4ff7dff`), §15 "Phase A0 — Required audits (new, gates Phase A)".
Status: **planning only — no ticket below has been started or executed by this board's setup.**

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
| A0-2 | Obtain archival scan/folio image access for the relevant folios | **Blocked** | External: Nationaal Archief scan access | `docs/enclave/scans/` does not exist in this repository (confirmed while setting up this board — the directory is `.gitignore`d for when populated, but is currently absent). This ticket cannot be completed by repository-local work; it requires the research owner to source the scans (Nationaal Archief, Den Haag — Access 1.04.02, Inventory 7964, per `docs/SOURCE_PROVENANCE.md`) before image verification (A0-3) can start. **No ticket in this workstream should be marked Done past this point without the scan actually having been viewed.** |
| A0-3 | Image-verify both passages against the original folio | **Blocked on A0-2** | A0-2 | `SP-01267` and `SP-01344` both move from `image_verified=not_checked` to `image_verified=confirmed` (or a documented rejection) in a reviewer's notes — per `docs/SOURCE_PROVENANCE.md`'s existing verification fields. This is the step that turns "researcher-transcribed DOCX text" into archivally-verified fact; skipping it and proceeding on DOCX text alone is exactly the shortcut Correction 1 was raised to prevent. |
| A0-4 | Populate `restraint_device_review.csv` seed rows (critical layer, not canonical) | **Backlog** | A0-1 (schema-ready regardless of A0-2/3 outcome) | Two rows per plan §5 schema, `source_passage_id` filled in from A0-1 (`SP-01267`, `SP-01344`), `canonical_extraction_status=missing_from_canonical_csv`, `extraction_audit_required=true` until A0-3 completes, `actual_use_status`/`target_person_status`/`date_of_use_status` all `not_recorded` (schema-enforced — see plan §14 item 5). **This ticket can start before A0-2/A0-3 resolve**, since it only records the audit's current state, not its conclusion. |
| A0-5 | Draft `RESTRAINT_DEVICE_EXTRACTION_AUDIT.md` | **Blocked on A0-3** | A0-3, A0-4 | Documents the audit outcome per plan §18; explicitly states whether/how a future canonical-CSV addition will be proposed (a separate MIG-NNN-style proposal, out of scope for this document itself, per plan §17); does **not** modify any canonical CSV. |
| A0-6 | Reviewer sign-off, Workstream 1 | **Blocked on A0-5** | A0-5 | A named reviewer (not the plan's author) confirms A0-5's findings; `restraint_device_review.csv`'s `extraction_audit_required` flips to `false` only after this sign-off, never automatically. |

---

## Workstream 2 — Cross-document temporal-overlap review

Traces to plan §15 Phase A0, bullet 2; §8 tier 6; §5 `group_hierarchy_review.csv`.

| ID | Ticket | Status | Depends on | Acceptance criteria |
|---|---|---|---|---|
| A0-7 | Enumerate all documents in the corpus with a time window overlapping the 1682-01-09 personnel register | **Backlog** | — | Query `01_documents.csv` for any `document_id` whose date range intersects `DOC-PERSONNEL-1682-01-09`'s period; list is exhaustive over the current corpus (not a sample), with each candidate document's relationship to the personnel register stated explicitly (same register / distinct register / inventory-only / correspondence). |
| A0-8 | Check candidate documents for population overlap with the Beneden-Pagger and Madagascar-arrival cohorts | **Backlog** | A0-7 | For each candidate document from A0-7, state explicitly whether it names or counts any of the same people/groups as `06_human_groups.csv`'s 17 records — with a citation (`source_document_id` + `source_passage_id`) for every "yes," not just a summary judgement. |
| A0-9 | Confirm (or revise) the `group_hierarchy_review.csv` parent/child de-duplication decision | **Backlog** | A0-8 | Reviewer confirms the plan's recommended assignment (`counts_toward_unique_person_estimate=true` on `G-MADA-64` parent, `false` on its 5 children) still holds after A0-8, or documents why it should change — either way, `SUM(record_person_count WHERE counts_toward_unique_person_estimate)` across the Madagascar rows must equal 64, never 128 (the direct regression condition from plan §16). |
| A0-10 | Document findings and update the tier-6 status in `archival_visibility.csv`/`uncertainty_critical.csv` scaffolding | **Backlog** | A0-8, A0-9 | States plainly whether 308 (tier 5, provisional single-document estimate) still stands as the best available *provisional* figure after cross-document review, or whether A0-8 surfaced overlap requiring a different provisional figure. **In neither case does this ticket produce a tier-6 "verified" number** — per the approval qualification, tier 6 (`unique_person_verified_count`) can only move off "unresolved" through a separate, explicit future decision, not as a byproduct of this review. |
| A0-11 | Reviewer sign-off, Workstream 2 | **Blocked on A0-10** | A0-10 | A named reviewer confirms A0-10's findings; `group_hierarchy_review.csv`'s `cross_document_temporal_overlap_checked` flips to `true` only after this sign-off. |

---

## Sprint sequencing note

A0-1 and A0-4 have no blocking dependency and can be picked up immediately. A0-7/A0-8 (Workstream 2) are corpus queries against data already in the repository and do not depend on external scan access, so they can also proceed in parallel with Workstream 1. **A0-2 (scan access) is the single external dependency on this entire board** — everything downstream of it in Workstream 1 (A0-3, A0-5, A0-6) is blocked until the research owner sources the archival images; this should be flagged to the research owner as the first action item, since it is the only ticket here this repository's contents cannot resolve on their own.

## Explicitly not on this board

- No Phase A (schema/derivation layer) tickets — blocked entirely until both workstreams reach sign-off (A0-6, A0-11), per the gate condition above.
- No ticket authorizes writing to any canonical dataset, solver snapshot, or Docker configuration — consistent with every prior approval in this project.
- No estimate/story-point/velocity fields — this board tracks archival-review dependencies and gate status, not delivery-date forecasting, since the binding constraint here is scan access and reviewer availability, not engineering capacity.

---

*This board is planning only. No ticket has been started. No canonical dataset, solver snapshot, or Docker configuration was touched while setting it up — only read access to `00_source_passages.csv` and a directory-existence check on `docs/enclave/scans/`.*
