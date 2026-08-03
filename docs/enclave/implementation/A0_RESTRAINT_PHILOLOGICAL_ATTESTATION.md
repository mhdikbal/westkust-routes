# Philological Attestation: Restraint Entries

## Researcher

Muhammad Ikbal

## Archive

- Repository: Nationaal Archief, Den Haag
- Access: 1.04.02
- Inventory: 7964
- Viewer method: external archive viewer
- Viewer URL:
- Viewer file or scan sequence:
- Folio number, if explicitly available:
- Date accessed:
- Image retained locally: no
- Retention reason: source consulted externally; local duplication not
  required by project policy
- Researcher attestation status: researcher_attested

## Methodological statement

The archival image was consulted through the Nationaal Archief external viewer. The image is not retained locally by project policy. Absence of a local JPG is not equivalent to absence of philological examination.

## Evidence state

```text
source_examined_externally: true
image_retained_locally: false
image_retention_status: not_retained_by_policy
verification_method: external_archive_viewer
verified_against_local_image: false
canonical_extraction_status: present
canonical_inventory_row_present: true
structured_migration_authorized: false
```

The researcher has completed and approved the attested object identity and recorded counts below. `canonical_extraction_status` is **`present`** — direct row-level verification by `A0-5` (read-only) confirmed both entries already exist as structured rows in `10_inventory_items.csv`; see "Canonical inventory mapping" below. `structured_migration_authorized` remains `false` because none is needed: no canonical row is missing, so no migration proposal, no candidate correction, and no new row creation is authorized or required by this document.

## Canonical inventory mapping

```text
SP-01267 -> INV-0343  (Ammunitie van oorlogh, category=military_inventory, location=L-SALIDO)
SP-01344 -> INV-0401  (Waker transfer, Beneden-Pagger, category=transferred_military_inventory, location=L-BENEDEN-PAGGER)
```

Both rows are sourced from `DOC-INVENTORY-1682-01-04` and their `source_translation_full` field matches the corresponding source passage exactly. `evidence_status` and `review_status` are blank on both rows — this is the pre-existing, corpus-wide metadata-population gap documented in `REVIEW_QUEUE.md` §A (affecting all 403 rows of `10_inventory_items.csv` uniformly, not something specific to these two entries). **A blank `evidence_status`/`review_status` is not absence of evidence** — the row, its category, its location, and its source passage are all explicit and present; only the separate evidence-status/review-status metadata fields await the corpus-wide population pass.

## Lexicographical resource

- IVdNT
- relevant lemma or search terms:

## Entry 1

- source passage: SP-01267
- canonical inventory row: INV-0343
- document section: Ammunitie van oorlogh
- folio number:
- inventory examination date: 1682-01-04
- later collation date: 1682-04-22
- reading:
- normalized reading:
- Indonesian translation:
- object count: 1
- ring count: 5
- key count: 1
- confidence:
- notes:

## Entry 2

- source passage: SP-01344
- canonical inventory row: INV-0401
- document section: Waker transfer, Beneden-Pagger
- folio number:
- inventory examination date: 1682-01-06
- later collation date: 1682-04-22
- reading:
- normalized reading:
- Indonesian translation:
- object count: 1
- ring count: 3
- key count: 1
- confidence:
- notes:

## Consolidated documentary count

```text
restraint-device entries: 2
restraint devices: 2
rings: 8
keys: 2
```

This is a count of what the attestation documents about the two entries themselves (object identity and recorded quantities), corresponding directly to the existing canonical rows `INV-0343` and `INV-0401` — it does not create, migrate, or duplicate anything in `10_inventory_items.csv`. `structured_migration_authorized: false` applies here too, because no migration is needed: both rows already exist.

## Epistemic limits

The entries establish the recorded presence of restraint devices.

The entries do not establish:

- use against any specific person;
- date of actual use;
- frequency of use;
- exclusive use against enslaved workers.

The recorded `inventory examination date` and `later collation date` for each entry are documentary/administrative dates (when the object was counted or re-verified in an inventory pass) — they are not, and must not be read as, a date of use. This distinction is deliberate and unchanged by recording these dates.

## Correction history

**The passage-to-structured-row extraction-gap premise stated in earlier versions of this document is formally withdrawn.** `A0-5` (read-only diagnosis) found, via direct row-level verification against `10_inventory_items.csv`, that both entries already exist as canonical rows (`INV-0343`, `INV-0401`) — there was never a missing row, a parser omission, a section filter, a vocabulary filter, a range truncation, or a deduplication defect to find.

Root cause of the false premise: an earlier investigation searched `10_inventory_items.csv` for a list of restraint-related terms (`boei`, `ketting`, `slot`, `sleutel`, `gevangenis`, `rantai`, `gembok`, `borgol`, `kurungan`, `handboei`, `voetboei`, `iron ring`, `shackle`, `chain`) but the search omitted the literal Indonesian term actually used in this corpus's translated text: **"belenggu"**. "Belenggu" was subsequently found only via a raw DOCX text extraction, at which point the absence-from-canonical-CSV claim was carried forward and stated as fact without a direct re-check of `10_inventory_items.csv` for that specific term. That unverified assumption then propagated through the critical model plan, the Phase A0 board, the master sprint board, the backlog, and this attestation's earlier `canonical_extraction_status: missing` value — across several commits — until `A0-5`'s direct row-level verification corrected it.
