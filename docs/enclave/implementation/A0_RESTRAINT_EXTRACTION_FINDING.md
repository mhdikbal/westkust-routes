# A0-5 Finding: No Passage-to-Structured-Row Extraction Defect Exists

Status: **read-only finding, accepted**. Formally withdraws the "canonical-extraction gap" premise stated in earlier revisions of the critical model plan, the Phase A0 board, the master sprint board, the backlog, and the philological attestation.

## Task

`A0-5` — diagnose why `SP-01267` and `SP-01344` exist in `00_source_passages.csv` but allegedly do not produce structured rows in `10_inventory_items.csv`.

## Method

Direct row-level query against `docs/enclave/salido_hdt_model_v0_4_1/10_inventory_items.csv` (read-only; no file modified):

```
grep -n "belenggu" 10_inventory_items.csv
```

Cross-checked against `source_paragraph_index` values immediately surrounding 1267 and 1344, to confirm the rows sit in the correct position relative to their known neighbors (musket balls, powder timer, spears — already-confirmed canonical rows).

## Finding

**Both entries already exist as canonical rows. There is no extraction defect.**

| Passage | Canonical row | `source_paragraph_index` | `inventory_section` | `category` | `location_id` | `source_document_id` |
|---|---|---|---|---|---|---|
| `SP-01267` | `INV-0343` | 1267 | Ammunitie van oorlogh | `military_inventory` | `L-SALIDO` | `DOC-INVENTORY-1682-01-04` |
| `SP-01344` | `INV-0401` | 1344 | Van Lieutenant Waker overgelevert | `transferred_military_inventory` | `L-BENEDEN-PAGGER` | `DOC-INVENTORY-1682-01-04` |

`source_translation_full` on both rows matches the corresponding source passage exactly. Both rows carry blank `evidence_status`/`review_status`, identical to their immediate neighbors (`INV-0342`, `INV-0344`, `INV-0400`, `INV-0402`) — this is the pre-existing, corpus-wide metadata-population gap documented in `REVIEW_QUEUE.md` §A (affecting all 403 rows uniformly), not a defect unique to these two.

Checked against every failure mode named in the task's evidence requirements:

| Candidate defect | Found? |
|---|---|
| Parser omission | No — both rows present, correctly formed |
| Section filtering | No — both rows carry the correct `inventory_section` |
| Vocabulary filtering | No — both rows carry a valid, existing `category` value (`military_inventory`, `transferred_military_inventory`) |
| Range truncation | No — both rows sit at the correct `source_paragraph_index`, among correctly-captured neighbors |
| Deduplication | No — one row per passage, no merge or drop |

## Root cause of the false premise (not an extraction defect — an earlier analysis error)

An earlier investigation in this project's history searched `10_inventory_items.csv` for a list of restraint-related terms (`boei`, `ketting`, `slot`, `sleutel`, `gevangenis`, `rantai`, `gembok`, `borgol`, `kurungan`, `handboei`, `voetboei`, `iron ring`, `shackle`, `chain`) but the list omitted the literal Indonesian term this corpus actually uses: **"belenggu"**. "Belenggu" was subsequently found only via a raw DOCX text extraction, and the "absent from canonical CSV" claim was then stated as fact without a direct re-check of `10_inventory_items.csv` for that specific term. That unverified assumption propagated through the critical model plan (`C10`, §4, §5, §15), the Phase A0 board (`A0-2`…`A0-6`), the master sprint board, the backlog, and the attestation's `canonical_extraction_status: missing` value, across several commits, until this diagnosis corrected it by direct row-level verification.

## What is not affected by this correction

- Object identity and presence: unchanged, remains explicit (`presence_status=explicit`).
- Actual use, target person, and date of use: unchanged, remain `not_recorded` and must never be inferred (P6).
- No-local-JPG evidence-retention policy: unchanged.
- Canonical dataset `v0.4.1`: unchanged, read-only throughout this diagnosis and this correction.

## What changes

- `canonical_extraction_status` moves from `missing` to `present` everywhere it is recorded.
- No canonical-CSV migration, candidate correction, or new canonical version is proposed, needed, or authorized for these two records.
- Phase A0 tickets `A0-4` and `A0-6` (Workstream 1), which were scoped around the now-withdrawn extraction-gap premise, are closed as rejected/moot rather than completed.
- `A0-3` remains open, but only for a narrower, unrelated reason: exact original Dutch spelling, folio number, viewer scan sequence, and IVdNT lemma are not yet recorded in `A0_RESTRAINT_PHILOLOGICAL_ATTESTATION.md`.

---

*No canonical dataset, solver snapshot, application code, or Docker configuration was modified in the course of this diagnosis or this finding record. No migration proposed. Not committed.*
