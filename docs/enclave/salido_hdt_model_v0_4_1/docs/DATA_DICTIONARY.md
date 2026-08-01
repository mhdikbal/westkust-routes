# Data Dictionary

## File-level dictionary

### `00_source_passages.csv`

Rows: **1488**

Columns: `source_passage_id`, `docx_file`, `source_document_id`, `paragraph_index`, `style`, `text`, `review_status`, `image_verified`

### `01_documents.csv`

Rows: **5**

Columns: `document_id`, `title`, `date_original`, `date_iso`, `archive_repository`, `archive_access`, `inventory_number`, `source_file`, `document_type`, `status`

### `02_persons.csv`

Rows: **50**

Columns: `person_id`, `name_canonical`, `entity_level`, `source_status`, `identity_confidence`, `notes`, `source_document_id`, `source_passage_id`, `evidence_status`, `review_status`

### `03_roles.csv`

Rows: **22**

Columns: `role_id`, `role_original`, `role_description_id`, `role_family`

### `04_person_roles.csv`

Rows: **47**

Columns: `person_role_id`, `person_id`, `role_id`, `role_original`, `valid_from`, `valid_to`, `evidence_status`, `review_status`, `source_document_id`, `source_passage_id`, `confidence`

### `05_locations.csv`

Rows: **23**

Columns: `location_id`, `name_original`, `name_normalized_id`, `normalization_status`, `normalization_reason`, `normalization_confidence`, `location_type`, `parent_location_id`, `evidence_status`, `source_document_id`, `source_passage_id`, `review_status`

### `06_human_groups.csv`

Rows: **17**

Columns: `group_id`, `source_category_original`, `count`, `status_category`, `growth_category_original`, `sex_category_original`, `location_id`, `evidence_status`, `source_document_id`, `source_passage_id`, `review_status`

### `07_human_role_location_time.csv`

Rows: **15**

Columns: `hrlt_id`, `human_or_group_id`, `entity_type`, `role_id`, `location_id`, `valid_from`, `valid_to`, `assignment_value`, `evidence_status`, `source_quote`, `source_document_id`, `source_passage_id`, `confidence`, `review_status`

### `08_weekly_operations.csv`

Rows: **42**

Columns: `operation_id`, `period_start`, `period_end`, `location_id`, `schoten`, `ore_weight_lb`, `notes`, `source_document_id`, `source_passage_id`, `evidence_status`, `review_status`

### `09_assay_results.csv`

Rows: **19**

Columns: `assay_id`, `period_or_batch`, `ore_weight_lb`, `assayer`, `mark`, `lood`, `grein`, `gulden`, `stuiver`, `penning`, `assay_type`, `evidence_status`, `source_document_id`, `source_passage_id`, `review_status`

### `10_inventory_items.csv`

Rows: **403**

Columns: `inventory_item_id`, `inventory_date`, `location_id`, `inventory_section`, `category`, `row_type`, `quantity`, `unit_original`, `unit_normalized`, `normalization_status`, `normalization_reason`, `normalization_confidence`, `item_text_id`, `source_translation_full`, `condition_normalized`, `condition_original`, `reading_status`, `evidence_status`, `review_status`, `source_document_id`, `source_paragraph_index`, `image_verified`, `notes`

### `11_claims.csv`

Rows: **6**

Columns: `claim_id`, `subject_id`, `predicate`, `object_or_value`, `evidence_status`, `evidence_quote`, `source_document_id`, `source_passage_id`, `review_status`

### `12_numeric_anomalies.csv`

Rows: **5**

Columns: `anomaly_id`, `metric`, `source_value`, `validation_result`, `difference`, `status`, `source_file`

### `13_data_dictionary.csv`

Rows: **176**

Columns: `file`, `column`, `description`, `required`, `notes`

### `14_task_requirements.csv`

Rows: **18**

Columns: `task_id`, `task_name`, `task_family`, `allowed_location_ids`, `required_skill_ids`, `preferred_role_ids`, `required_tool_keywords`, `minimum_workers_assumption`, `constraint_strength`, `evidence_basis`, `review_status`

### `15_role_location_compatibility.csv`

Rows: **31**

Columns: `compatibility_id`, `role_id`, `location_id`, `compatibility_score`, `constraint_type`, `evidence_basis`, `review_status`

### `16_location_adjacency.csv`

Rows: **22**

Columns: `edge_id`, `from_location_id`, `to_location_id`, `relation_type`, `bidirectional`, `evidence_status`, `evidence_basis`, `distance_original`, `distance_normalized`, `normalization_status`, `normalization_reason`, `normalization_confidence`, `review_status`

### `MANIFEST.csv`

Rows: **38**

Columns: `file`, `sha256`, `bytes`

### `PROVENANCE_BACKFILL_LOG.csv` (added v0.4.1)

Rows: **10**

Columns: `backfill_id`, `file`, `record_id`, `field`, `old_value`, `new_value`, `derivation_rule`, `input_fields`, `semantic_interpretation_required`, `review_status`

One row per automatically-populated field. Every row in this log has `semantic_interpretation_required = false` by construction — this release applies no field for which that could not be guaranteed (see `docs/enclave/implementation/V0_4_1_VALIDATION_REPORT.md`).

_Corrected v0.4 (MIG-001): v0.3 documented this as 19 rows — a stale figure carried over from `salido_hdt_csv_v0_2/MANIFEST.csv`, which genuinely has 19 rows. v0.3's actual manifest, once `DOCUMENTATION.md` and the 16-file `docs/` directory are counted, has 37. This count is regenerated automatically each release (`MANIFEST.csv` is not hand-maintained) and will naturally stay in sync going forward._

## Null semantics

An empty value means unknown, unavailable, or not yet extracted. It does not mean zero, absent, or false.

## Identifier conventions

- `P-`: named person
- `G-`: aggregate human group
- `R-`: role
- `L-`: location
- `T-`: task
- `INV-`: inventory item
- `AS-`: assay observation
- `OP-`: operation record
- `CL-`: historical claim
- `AN-`: anomaly
- `HRLT-`: Human–Role–Location–Time assertion
- `DOC-`: document (`01_documents.csv`)
- `SP-`: source passage (`00_source_passages.csv`)
- `PR-`: person role assertion (`04_person_roles.csv`)
- `RLC-`: role-location compatibility rule (`15_role_location_compatibility.csv`)
- `LE-`: location edge / adjacency relation (`16_location_adjacency.csv`)

_Added v0.4 (MIG-002): these five prefixes were already in consistent use in v0.3 but were not listed here._

## Multi-valued ID columns (added v0.4, MIG-009 note)

Columns that hold more than one identifier per cell (`14_task_requirements.csv`: `allowed_location_ids`, `required_skill_ids`, `preferred_role_ids`) use **`|` (pipe) as the separator, not a comma**. This was not documented anywhere in v0.3 and caused an initial false-positive foreign-key-resolution failure during the v0.4 migration audit before the correct delimiter was identified. `required_skill_ids` does not resolve against any table in this bundle — there is no `06_skills.csv` or equivalent; skill identifiers are currently free-standing labels (`assay`, `weighing`, `blasting`, `drilling`, `carpentry`, `charcoal_burning`, `medical_care`, `ore_crushing`, `ore_removal`, `ore_sorting`, `mine_survey`, `underground_inspection`, and others), not foreign keys. This is noted, not changed, in v0.4.

## Note on `16_location_adjacency.csv.review_status` (added v0.4, MIG-004)

All 22 rows carry `review_status = model_input_v0.2`. This table is inherited unmodified from the v0.2 modelling cycle (confirmed byte-identical to `salido_hdt_csv_v0_2/16_location_adjacency.csv`) — the label is accurate provenance, not an error, and was not changed in v0.4.
