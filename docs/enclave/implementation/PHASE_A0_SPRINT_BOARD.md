# Phase A0 Sprint Board — Required Audits (Enclave 1682 Critical Model)

Companion to `ENCLAVE_1682_CRITICAL_MODEL_PLAN.md` (commit `4ff7dff`), §15 "Phase A0 — Required audits (new, gates Phase A)".
Status: **Workstream 2 (A0-7…A0-11) complete and signed off. Workstream 1: A0-1/A0-2 done (attestation committed `f98cfb0`), A0-3 in review (object identity and counts attested; exact original Dutch spelling, folio, viewer scan sequence, and IVdNT lemma not yet recorded), A0-5 ready to start (read-only diagnosis of the passage-to-structured-row gap), A0-4/A0-6 still blocked on their own dependencies. Overall Phase A0 gate (`S1-03`) not yet open.**

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

The gate for `A0-3` is **researcher attestation completion** (`A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md` filled and reviewer-confirmed), not local image possession. Object identity and recorded quantities are now attested (committed `f98cfb0`) — `A0-3` is therefore **Review**, not yet **Done**: exact original Dutch spelling, folio number, viewer scan sequence, and IVdNT lemma remain unrecorded, and closing A0-3 fully requires either recording those or an explicit reviewer decision that object-and-count attestation alone is sufficient.

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
| A0-2 | Document external-viewer philological attestation | **Done — `A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md` committed `f98cfb090aa41b3939a77bf33417dafd946724f7`** | — | Researcher attested object identity and recorded quantities for both entries (object/ring/key counts, inventory examination date, later collation date, `researcher_attestation_status=researcher_attested`, `source_examined_externally=true`). **No local JPG was used or required** — `docs/enclave/scans/` remains absent, as intended. |
| A0-3 | Reviewer confirms the philological attestation | **Review** | A0-2 (done) — no longer blocked on A0-2 or on local JPG availability | Object identity and recorded quantities are attested and reviewer-acknowledged. **Not yet closable to Done**: exact original Dutch spelling, folio number, viewer scan sequence, and IVdNT lemma are not recorded in the current attestation artifact (`A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md` leaves `reading`, `normalized reading`, `relevant lemma or search terms`, and `folio number` blank by design — nothing was invented to fill them). `verified_against_local_image` remains `false`, never set `true` under this policy. Closing A0-3 to Done requires either those fields being recorded, or an explicit reviewer decision that object-identity-and-count attestation alone is sufficient — not decided here. |
| A0-4 | Populate `restraint_device_review.csv` seed rows (critical layer, not canonical) | **Backlog** | A0-1 (schema-ready regardless of A0-3 outcome) | Two rows per plan §5 schema, `source_passage_id` filled in from A0-1 (`SP-01267`, `SP-01344`), `canonical_extraction_status=missing_from_canonical_csv`, `extraction_audit_required=true` until A0-3 fully closes, `actual_use_status`/`target_person_status`/`date_of_use_status` all `not_recorded` (schema-enforced — see plan §14 item 5). **This ticket can start before A0-3 fully resolves**, since it only records the audit's current state, not its conclusion. |
| A0-5 | Draft `RESTRAINT_DEVICE_EXTRACTION_AUDIT.md` | **Ready** | A0-1, A0-2 (both done) | `SP-01267`/`SP-01344` exist and the object/counts are researcher-attested, so the passage-to-structured-row omission can now be investigated. **Scoped to read-only diagnosis only**: trace why both rows were dropped during structured extraction into `10_inventory_items.csv`; document the audit outcome per plan §18; explicitly state whether/how a future canonical-CSV addition will be proposed (a separate MIG-NNN-style proposal, out of scope for this document itself, per plan §17). **Must not modify `v0.4.1`, must not invent an exact original Dutch reading, folio, or viewer sequence, and must not infer restraint use or a target person** — A0-3 being in Review, not Done, does not block this read-only investigation. No migration is authorized by this ticket. |
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
| A0-11 | Reviewer sign-off, Workstream 2 | **Done — signed off by Muhammad Ikbal** | A0-10 | Reviewer confirmed `CROSS_DOCUMENT_OVERLAP_FINDINGS.md`'s findings. `group_hierarchy_review.csv`'s `cross_document_temporal_overlap_checked` field is authorized to flip to `true` once Sprint 2 creates that file (the file does not exist yet — this sign-off pre-authorizes that specific field value for when it does). This sign-off closes **Workstream 2 only** — Workstream 1 is now A0-1/A0-2 done, A0-3 in review, A0-5 ready, A0-4/A0-6 still blocked on their own dependencies; the overall Phase A0 gate (`S1-03`) stays blocked until A0-3 fully closes and A0-6 signs off. |

---

## Sprint sequencing note

A0-1, A0-2 are done. A0-4 and A0-5 have no remaining blocking dependency and can be picked up immediately — A0-5 specifically as a **read-only diagnosis only**. A0-3 is in Review, not blocking A0-4 or A0-5. **No ticket in this workstream depends on external scan access any longer.**

## Explicitly not on this board

- No Phase A (schema/derivation layer) tickets — blocked entirely until both workstreams reach sign-off. **A0-11 signed off; A0-3 in Review and A0-6 still outstanding** (A0-3 needs original reading/folio/lemma recorded or an explicit reviewer decision that object-and-count attestation alone suffices; A0-6 needs A0-5's findings) — per the gate condition above, Phase A stays blocked until A0-6 closes.
- No ticket authorizes writing to any canonical dataset, solver snapshot, or Docker configuration — consistent with every prior approval in this project.
- **No ticket authorizes creating `docs/enclave/scans/` or downloading/committing archival images** — local image retention is not required by this project's evidence policy (`docs/SOURCE_PROVENANCE.md`).
- No estimate/story-point/velocity fields — this board tracks archival-review dependencies and gate status, not delivery-date forecasting, since the binding constraint here is attestation completion and reviewer availability, not engineering capacity.
- Preserved unchanged: actual restraint-device *use* and *target person* remain `not_recorded` and must never be inferred (P6) — this correction changes how presence is verified, not what may be claimed about use. Canonical `v0.4.1` remains immutable throughout.

---

*Workstream 2 (A0-7…A0-11) executed and signed off via direct, read-only queries against the canonical v0.4.1 CSVs — full findings in `CROSS_DOCUMENT_OVERLAP_FINDINGS.md`. Workstream 1's evidence-retention policy corrected this revision — no local scan required or permitted; A0-1/A0-2 done, attestation committed `f98cfb0`, A0-3 in review, A0-5 ready for read-only diagnosis. No canonical dataset, solver snapshot, application code, or Docker configuration was modified at any point.*
