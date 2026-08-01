# SALIDO-HDT v0.4 → v0.4.1 — Comparative Validation Report

Date: 2026-08-01
Scope: `docs/enclave/salido_hdt_model_v0_4_1/`, validated against `docs/enclave/salido_hdt_model_v0_4/`.
`docs/enclave/salido_hdt_model_v0_3/` was not touched by this task and is re-verified untouched below as part of the full immutability chain.

---

## 1. What was applied

Exactly **one** column, in exactly **one** file, received an automated backfill: `07_human_role_location_time.csv.source_passage_id`, for **10 of its 15 rows**. This is the only rule `docs/enclave/implementation/V0_4_SEMANTIC_QA.md` verified as safe to apply without semantic interpretation — every other candidate examined in that report (source_document_id lookups, unit/condition extraction, evidence_status/review_status assignment) was explicitly found non-deterministic and excluded. No other field, in any of the 17 canonical CSVs, was populated.

**Derivation rule applied**: for each row, `source_quote` was tested as an exact substring of `00_source_passages.csv.text`. Where exactly one passage matched, `source_passage_id` was set to that passage's ID. Where zero or more than one passage matched, the field was left empty. `semantic_interpretation_required = false` for all 10 applied rows — the rule is a mechanical string-containment test with a uniqueness gate, not a judgement call.

| hrlt_id | source_quote | Unique match? | Result |
|---|---|---|---|
| HRLT-0001 | "Johan Willem Vogel Assaijeur" | No (0 matches — paraphrase, not verbatim) | left empty |
| HRLT-0002 | "Johan Pleijtner Marckscheijder" | No (0 matches) | left empty |
| HRLT-0003 | "Elias Hesse Berghschrijver" | No (0 matches) | left empty |
| HRLT-0004 | "Johan Hoffman Assaijeur" | No (0 matches) | left empty |
| HRLT-0005 | "Op Poulo Chinco onder den Assaijeur Willem Roeling..." | No (0 matches) | left empty |
| HRLT-0006 – HRLT-0015 (10 rows) | "Lijfeijgenen in de mijns Beneden-Pagger" | Yes — exactly 1 match, `SP-01236` | **backfilled** |

---

## 2. `PROVENANCE_BACKFILL_LOG.csv`

10 rows, `backfill_id` `BF-0001`–`BF-0010`, one per populated field. All required columns present: `backfill_id, file, record_id, field, old_value, new_value, derivation_rule, input_fields, semantic_interpretation_required, review_status`. `semantic_interpretation_required` is `false` for all 10 rows — verified by inspecting the file directly, not assumed. `review_status` is set to `auto_applied_deterministic_unreviewed` for every entry: this documents that the derivation is mechanical and traceable, but — consistent with `docs/DOCUMENTATION.md`'s status vocabulary ("No record becomes `verified` solely because it was extracted automatically") — a human has not yet signed off on it, and this log does not claim otherwise.

---

## 3. Cell-level comparative diff, v0.4 → v0.4.1

Every one of the 17 canonical CSVs was loaded from both releases and compared field-by-field, keyed by primary identifier (`(file, column)` pair for `13_data_dictionary.csv`, the file's own `_id` column elsewhere).

**Result: exactly 10 cell-level differences across the entire dataset, and they are exactly the 10 backfills logged above — no more, no fewer.**

```
07_human_role_location_time.csv  HRLT-0006  source_passage_id  '' -> 'SP-01236'
07_human_role_location_time.csv  HRLT-0007  source_passage_id  '' -> 'SP-01236'
07_human_role_location_time.csv  HRLT-0008  source_passage_id  '' -> 'SP-01236'
07_human_role_location_time.csv  HRLT-0009  source_passage_id  '' -> 'SP-01236'
07_human_role_location_time.csv  HRLT-0010  source_passage_id  '' -> 'SP-01236'
07_human_role_location_time.csv  HRLT-0011  source_passage_id  '' -> 'SP-01236'
07_human_role_location_time.csv  HRLT-0012  source_passage_id  '' -> 'SP-01236'
07_human_role_location_time.csv  HRLT-0013  source_passage_id  '' -> 'SP-01236'
07_human_role_location_time.csv  HRLT-0014  source_passage_id  '' -> 'SP-01236'
07_human_role_location_time.csv  HRLT-0015  source_passage_id  '' -> 'SP-01236'
```

No row count changed in any file. No column was added or removed in any of the 17 canonical CSVs (`PROVENANCE_BACKFILL_LOG.csv` is a new *file*, not a new column in an existing one). **No existing non-empty value was altered anywhere** — every one of the 10 changed cells had `old_value = ''` (confirmed empty before the backfill, both in the diff above and independently in the backfill log).

The remaining 29 columns added empty in v0.4 (4,932 of the original 4,942 empty cells — 4,942 minus the 10 now filled) are **unchanged and still empty** in v0.4.1, exactly as `V0_4_SEMANTIC_QA.md` classified them (`source_review_required`).

---

## 4. Referential integrity of the new values

`07_human_role_location_time.csv.source_passage_id` is a new foreign key surface (the column did not previously hold data to validate). Checked: all 10 populated values resolve to an existing `00_source_passages.csv.source_passage_id` — 0 unresolved, confirmed by direct lookup (trivially expected, since the values were derived *from* that table, but verified rather than assumed). Primary-key uniqueness and non-emptiness across all 17 files was re-checked in v0.4.1 using the same method as the v0.4 migration's MIG-008 — unchanged, still clean, since no primary-key column was touched by this task.

---

## 5. Immutability chain

| Release | Check | Result |
|---|---|---|
| `salido_hdt_model_v0_3/` | SHA-256 of every file, compared against the baseline snapshot taken before the v0.4 migration began (two tasks ago) | **Unchanged** |
| `salido_hdt_model_v0_4/` | SHA-256 of every file, compared against a snapshot taken immediately before this task started | **Unchanged** |
| `salido_hdt_model_v0_4_1/` | Cell-level diff against v0.4 | **Exactly the 10 approved backfills, nothing else** |

---

## 6. Statement

No file under `salido_hdt_model_v0_3/` or `salido_hdt_model_v0_4/` was modified during this task — confirmed by hash comparison, not assumed. Within `salido_hdt_model_v0_4_1/`, the only data change applied was the single deterministic rule described in §1, to the 10 rows it verifiably resolves; the 5 rows it could not uniquely resolve were left empty rather than guessed. `docs/DATA_DICTIONARY.md`, `README.md`, and `MANIFEST.csv` were updated to describe the new file and the backfill (documentation only, no archival data touched). No archival evidence, name, quantity, folio reference, or image coordinate was invented. This report and `PROVENANCE_BACKFILL_LOG.csv` are both reproducible by re-running the same read-only substring-match query against `salido_hdt_model_v0_4/`.
