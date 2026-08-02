# Phase A0 Sprint Board — Required Audits (Enclave 1682 Critical Model)

Companion to `ENCLAVE_1682_CRITICAL_MODEL_PLAN.md` (commit `4ff7dff`), §15 "Phase A0 — Required audits (new, gates Phase A)".
Status: **Workstream 2 (A0-7…A0-11) complete and signed off. Workstream 1 (A0-2…A0-6) is no longer externally blocked — evidence-retention policy corrected (see §0 below); the gate is now researcher attestation completion, tracked in `A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md` (currently `draft_awaiting_researcher_completion`). Overall Phase A0 gate (`S1-03`) not yet open.**

## 0. Evidence-retention policy (correction, this revision)

**Local image retention is not required by this project.** The prior framing of `docs/enclave/scans/`'s absence as an external blocker conflated "scan access obtained" with "scan duplicated into this repository" — `docs/SOURCE_PROVENANCE.md` requires neither; it requires only that a reviewer examined the source and can cite repository/access/inventory/folio/quoted text. The research workflow deliberately does not copy Nationaal Archief folio images into this repository, and no ticket on this board authorizes creating `docs/enclave/scans/` or downloading/committing archival images.

Absence of a local image is **not** evidence that philological review did not occur. The evidence model distinguishes:

```text
source_examined_externally    — pending_researcher_attestation | true (set by researcher, not inferred)
image_retained_locally        — false (standing default for this project)
image_retention_status        — not_retained_by_policy
verification_method           — external_archive_viewer
verified_against_local_image  — false (never set true under this policy)
canonical_extraction_status   — missing (until A0-4/A0-5 resolve — see remaining P0 below)
researcher_attestation_status — draft_awaiting_researcher_completion | researcher_attested
```

The gate for `A0-3` is **researcher attestation completion** (`A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md` filled and reviewer-confirmed), not local image possession.

**Remaining P0 issue, unaffected by this correction**: `SP-01267` and `SP-01344` exist in `00_source_passages.csv` but their entries are absent from `10_inventory_items.csv` — a passage-to-structured-row extraction gap, not a source-access problem. This is what `A0-4`/`A0-5` must still resolve.

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
| A0-2 | Document external-viewer philological attestation | **Ready — template created, `docs/enclave/implementation/A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md`, status `draft_awaiting_researcher_completion`** | — | Researcher reads the relevant folio(s) directly in the Nationaal Archief viewer (Access 1.04.02, Inventory 7964), cross-checks archaic vocabulary via IVdNT, and fills the attestation's blank fields — Viewer URL, viewer file/scan sequence, folio number *if explicitly available* (not required when the viewer only provides a stable file sequence), reading, normalized reading, Indonesian translation, quantity, confidence. **No local JPG required or permitted by this ticket** — `docs/enclave/scans/` must not be created. |
| A0-3 | Reviewer confirms the philological attestation | **Blocked on A0-2** | A0-2 (researcher-completed and reviewer-confirmed attestation — not local JPG availability) | `SP-01267` and `SP-01344` both move from `source_examined_externally=pending_researcher_attestation` to `source_examined_externally=true` with `researcher_attestation_status=researcher_attested`, recorded in the attestation document by a reviewer — **not automatically**, and **not** `verified_against_local_image=true`, which is never set under this policy. This is the step that turns "researcher-transcribed DOCX text" into philologically-reviewed fact; skipping it and proceeding on unreviewed DOCX text alone is exactly the shortcut Correction 1 was raised to prevent — the fix is reviewed attestation, not a locally-stored image. |
| A0-4 | Populate `restraint_device_review.csv` seed rows (critical layer, not canonical) | **Backlog** | A0-1 (schema-ready regardless of A0-2/3 outcome) | Two rows per plan §5 schema, `source_passage_id` filled in from A0-1 (`SP-01267`, `SP-01344`), `canonical_extraction_status=missing_from_canonical_csv`, `extraction_audit_required=true` until A0-3 completes, `actual_use_status`/`target_person_status`/`date_of_use_status` all `not_recorded` (schema-enforced — see plan §14 item 5). **This ticket can start before A0-2/A0-3 resolve**, since it only records the audit's current state, not its conclusion. |
| A0-5 | Draft `RESTRAINT_DEVICE_EXTRACTION_AUDIT.md` | **Blocked on A0-3** | A0-3, A0-4 | Documents the audit outcome per plan §18; explicitly states whether/how a future canonical-CSV addition will be proposed (a separate MIG-NNN-style proposal, out of scope for this document itself, per plan §17); does **not** modify any canonical CSV. |
| A0-6 | Reviewer sign-off, Workstream 1 | **Blocked on A0-5** | A0-5 | A named reviewer (not the plan's author) confirms A0-5's findings; `restraint_device_review.csv`'s `extraction_audit_required` flips to `false` only after this sign-off, never automatically. |

---

## Workstream 2 — Cross-document temporal-overlap review

Traces to plan §15 Phase A0, bullet 2; §8 tier 6; §5 `group_hierarchy_review.csv`.

| ID | Ticket | Status | Depends on | Acceptance criteria |
|---|---|---|---|---|
| A0-7 | Enumerate all documents in the corpus with a time window overlapping the 1682-01-09 personnel register | **Done** | — | All 5 corpus documents enumerated and checked (exhaustive — the corpus contains only 5 documents total); findings in `CROSS_DOCUMENT_OVERLAP_FINDINGS.md` §2. Discrepancy flagged (archive catalogue period vs. two documents' internal dates), not resolved. |
| A0-8 | Check candidate documents for population overlap with the Beneden-Pagger and Madagascar-arrival cohorts | **Done** | A0-7 | Findings in `CROSS_DOCUMENT_OVERLAP_FINDINGS.md` §3: `DOC-PROTOCOL-1682` and `DOC-INVENTORY-1682-01-04` show structural overlap (cited by HRLT/claims row IDs); `DOC-ASSAY-1682-03-12` and `DOC-OLITSCH-1682-04-30` show none in currently-linked tables. Exhaustiveness limitation explicitly recorded: `00_source_passages.csv`'s `source_document_id` is empty for all 1488 rows, so "no overlap" for those two documents is bounded by that gap, not an absolute claim. |
| A0-9 | Confirm (or revise) the `group_hierarchy_review.csv` parent/child de-duplication decision | **Done** | A0-8 | Reviewer (Muhammad Ikbal) confirmed the plan's recommended assignment (`counts_toward_unique_person_estimate=true` on `G-MADA-64` parent, `false` on its 5 children) — no cross-document evidence found in A0-8 contradicts it; the only other reference to the cohort (`DOC-PROTOCOL-1682` claim `CL-003`) re-attests the same `group_id`, not a second count. `SUM(record_person_count WHERE counts_toward_unique_person_estimate)` across the Madagascar rows remains 64, never 128. |
| A0-10 | Document findings and update the tier-6 status in `archival_visibility.csv`/`uncertainty_critical.csv` scaffolding | **Done** | A0-8, A0-9 | `CROSS_DOCUMENT_OVERLAP_FINDINGS.md` written. States plainly that 308 (tier 5) still stands as the best available *provisional* figure. Tier 6 (`unique_person_verified_count`) explicitly recorded as remaining **unresolved** — this ticket did not and could not promote it, per the approval qualification. Tier-6 status recorded in prose (§5 of that document) pending Sprint 2 creating the actual `uncertainty_critical.csv` file to hold it. |
| A0-11 | Reviewer sign-off, Workstream 2 | **Done — signed off by Muhammad Ikbal** | A0-10 | Reviewer confirmed `CROSS_DOCUMENT_OVERLAP_FINDINGS.md`'s findings. `group_hierarchy_review.csv`'s `cross_document_temporal_overlap_checked` field is authorized to flip to `true` once Sprint 2 creates that file (the file does not exist yet — this sign-off pre-authorizes that specific field value for when it does). This sign-off closes **Workstream 2 only** — Workstream 1 (`A0-2`…`A0-6`) is no longer externally blocked (see §0) but is not yet complete: it awaits researcher attestation completion and reviewer confirmation; the overall Phase A0 gate (`S1-03`) stays blocked until Workstream 1 also reaches sign-off. |

---

## Sprint sequencing note

A0-1, A0-2, and A0-4 have no blocking dependency and can be picked up immediately. **No ticket in this workstream depends on external scan access any longer** — A0-2 depends only on the researcher completing the attestation document; A0-3 depends on reviewer confirmation of that attestation, not on any repository-local artifact.

## Explicitly not on this board

- No Phase A (schema/derivation layer) tickets — blocked entirely until both workstreams reach sign-off. **A0-11 signed off; A0-6 still outstanding** (pending A0-2 researcher attestation completion + A0-3/A0-5 review chain — no longer an external blocker) — per the gate condition above, Phase A stays blocked until A0-6 closes too.
- No ticket authorizes writing to any canonical dataset, solver snapshot, or Docker configuration — consistent with every prior approval in this project.
- **No ticket authorizes creating `docs/enclave/scans/` or downloading/committing archival images** — local image retention is not required by this project's evidence policy (`docs/SOURCE_PROVENANCE.md`).
- No estimate/story-point/velocity fields — this board tracks archival-review dependencies and gate status, not delivery-date forecasting, since the binding constraint here is attestation completion and reviewer availability, not engineering capacity.
- Preserved unchanged: actual restraint-device *use* and *target person* remain `not_recorded` and must never be inferred (P6) — this correction changes how presence is verified, not what may be claimed about use. Canonical `v0.4.1` remains immutable throughout.

---

*Workstream 2 (A0-7…A0-11) executed and signed off via direct, read-only queries against the canonical v0.4.1 CSVs — full findings in `CROSS_DOCUMENT_OVERLAP_FINDINGS.md`. Workstream 1's evidence-retention policy corrected this revision — no local scan required or permitted; verification proceeds via `A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md`. No canonical dataset, solver snapshot, application code, or Docker configuration was modified at any point.*
