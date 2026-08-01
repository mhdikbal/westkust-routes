# SALIDO-HDT CSV Bundle v0.4.1

Source working file: `enklave-salido.docx`

Archive identity recorded in the working document: Nationaal Archief, access 1.04.02, inventory 7964.

## Scope

This is a first structured extraction for the Human-Role-Location-Time and mine-operation model. It is intentionally conservative. Records marked `needs_folio_link`, `needs_image_review`, `interpreted`, or `parallel_reading` are not final archival readings.

## Important rules

- UTF-8 CSV files include BOM for Excel compatibility.
- Empty means unknown or not yet extracted, not zero.
- Original historical categories are preserved.
- Aggregate groups are not expanded into invented persons.
- Marginalia and source-image coordinates are not yet available in this DOCX-first bundle.
- `10_inventory_items.csv` contains the full translated inventory blocks currently available in the DOCX, at line-item level.
- Multi-valued ID columns (e.g. `14_task_requirements.allowed_location_ids`) use `|` as the separator — see `docs/DATA_DICTIONARY.md` (added v0.4).

## Files

- `00_source_passages.csv`
- `01_documents.csv`
- `02_persons.csv`
- `03_roles.csv`
- `04_person_roles.csv`
- `05_locations.csv`
- `06_human_groups.csv`
- `07_human_role_location_time.csv`
- `08_weekly_operations.csv`
- `09_assay_results.csv`
- `10_inventory_items.csv`
- `11_claims.csv`
- `12_numeric_anomalies.csv`
- `13_data_dictionary.csv`
- `14_task_requirements.csv`
- `15_role_location_compatibility.csv`
- `16_location_adjacency.csv`
- `MANIFEST.csv`

## Next pass

1. Complete full inventory extraction.
2. Link every row to DOCX paragraph IDs.
3. Add folio and scan references.
4. Review unresolved names and tools.
5. Build CP-SAT constraint input tables and Petri-net YAML from verified CSVs.
6. Populate the schema-only columns added in v0.4 (see `docs/enclave/implementation/REVIEW_QUEUE.md`) — these were added empty and require human review to fill in, not automated inference.

## Documented in v0.3 (renamed from "Added in v0.3" — see note below)

- Full documentation set (`DOCUMENTATION.md` and the 16-file `docs/` directory).
- Expanded release manifest (`MANIFEST.csv`) covering the documentation files.

**Note (added v0.4, MIG-003):** a byte-for-byte comparison of every CSV data file between this release lineage and `salido_hdt_csv_v0_2/` shows that `00_source_passages.csv` through `16_location_adjacency.csv` — including the inventory, task-requirements, role-location-compatibility, and location-adjacency tables — are identical in both releases. The v0.3 README previously stated these were "added in v0.3"; that phrasing was inaccurate as far as the CSV data is concerned. v0.3's actual addition, verified by this comparison, was the documentation layer listed above. This note corrects the record without altering any historical release file — `salido_hdt_csv_v0_2/` and `salido_hdt_model_v0_3/` remain untouched.

## Added in v0.4

- Schema requirements enforced and verified: primary-key uniqueness/non-emptiness, complete foreign-key resolution (including the two checks v0.3's audit had deferred), empty-string semantics reviewed.
- Structural schema additions (all left empty for pre-existing rows — no value is inferred or invented): evidence-bearing quadruple (`source_document_id`, `source_passage_id`, `evidence_status`, `review_status`) completed across ten files that were missing one or more; normalization triad (`normalization_status`, `normalization_reason`, `normalization_confidence`) added for four existing normalized fields; `unit_original`/`condition_original` added to `10_inventory_items.csv` to pair with their existing `_normalized` counterparts.
- Documentation fixes: corrected `MANIFEST.csv` row count, extended identifier-convention list, corrected this file list, documented the `|`-delimiter convention, extended the evidence-status vocabulary with five compound terms already in use but previously undocumented.
- Full migration rationale, including what was deliberately **not** auto-applied: `docs/enclave/implementation/V0_4_MIGRATION_PLAN.md`. Deferred/open items requiring human judgement: `docs/enclave/implementation/REVIEW_QUEUE.md`.

## Added in v0.4.1

- **Deterministic provenance backfill only** — per `docs/enclave/implementation/V0_4_SEMANTIC_QA.md` Task 2, exactly one column qualified: `07_human_role_location_time.csv.source_passage_id`, backfilled for 10 of its 15 rows via an exact-substring match of `source_quote` against `00_source_passages.text`, applied only where the match was unique. The remaining 5 rows of that column, and every other empty field introduced in v0.4, were left untouched — the QA report found no other deterministic rule.
- `PROVENANCE_BACKFILL_LOG.csv` — one row per populated field (10 rows), with the exact derivation rule and source fields for each.
- Full validation: `docs/enclave/implementation/V0_4_1_VALIDATION_REPORT.md`.

## Documentation v0.4.1

See `DOCUMENTATION.md` and the `docs/` directory for the complete modelling specification. Unchanged from v0.4 except for the backfill described above.
