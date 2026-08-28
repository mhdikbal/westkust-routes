# GET /api/forts/power-status — Publication Decision

> **Decision recording and implementation planning only. No source, API, or authentication modified. Nothing staged/committed/pushed/deployed.**

---

## 1. Endpoint

```text
GET /api/forts/power-status?year=...
File: backend/routers/forts.py:392
Router mount: /api/forts (backend/main.py:37), tag "Map" (not "Research")
```

## 2. Decision

```text
Decision status: APPROVED_WITH_LIMITATIONS
Current classification: PUBLIC_WITH_UNREVIEWED_RESEARCH_DETAIL
Target classification:  PUBLIC_MAP_SUMMARY_WITH_PROTECTED_RESEARCH_DETAIL
```

The public map layer is **retained** — this decision does not shut it down. The current full payload is **not** treated as the intended long-term public design; it is publicly exposed today only because no separation was ever built, not because it was reviewed and approved for publication as-is.

## 3. Researcher's Field Split (authoritative)

```text
PUBLIC:
  - fitur status kekuasaan pada peta (the map layer itself)
  - identitas benteng (fort_id, fort_name)
  - tahun (year)
  - status ringkas yang telah direview (dominion_status, once reviewed)
  - judul publik yang telah direview (a reviewed public title -- distinct
    from the current raw as_of_event.title, which has not been through a
    public-copy review pass)

PROTECTED:
  - kutipan text_asli
  - dokumen sumber (source_document)
  - provenance Phase B terperinci
  - cluster
  - p_self_current_status
  - dynamics_series
  - rmse
  - output Model 2/5/6
  - diagnostik dan ketidakpastian riset
```

## 4. Target Architecture

```text
PUBLIC MAP ENDPOINT (retained)
  GET /api/forts/power-status?year=...
  Purpose: support the public Atlas power-status map layer
  Candidate public fields: fort_id, fort_name, dominion_status, event.year,
    reviewed public event title (if approved)
  Candidate field list is NOT final until frontend dependencies (Phase 1)
  and public-copy review requirements are validated -- see § 6 below, which
  does exactly that validation.

PROTECTED RESEARCH ENDPOINT (candidate, not created)
  GET /api/research/forts/power-status-detail?year=...
  Purpose: serve research-only detail
  Candidate protected fields: event_date_raw, text_asli, source_document,
    Phase B provenance detail, cluster, p_self_current_status,
    dynamics_series, rmse, Model 2/5/6 output, diagnostic/uncertainty fields
  Authentication status: REQUIRES_RESEARCH_AUTHENTICATION
```

## 5. Implementation Status

```text
NOT_AUTHORIZED
```

This turn is decision recording and implementation planning only. Nothing was edited, created, staged, committed, pushed, or deployed. Full detail of what was and wasn't touched: § 10 of `FORT_POWER_STATUS_PUBLICATION_AUDIT.md`.

## 6. Required Statement (verbatim per instruction)

```text
MAP FEATURE: PUBLIC
PUBLIC SUMMARY: APPROVED_WITH_LIMITATIONS
FULL PROVENANCE AND MODEL DETAIL: REQUIRES_AUTHENTICATION
CURRENT PRODUCTION CHANGE: NOT_AUTHORIZED
```

## 7. Rationale (researcher's own words, recorded verbatim)

"Pendekatan ini mempertahankan peta sebagai produk publik, tetapi menghentikan asumsi bahwa semua data yang kebetulan dikirim oleh endpoint publik otomatis sudah disetujui untuk publikasi."

## 8. Cross-References

```text
Full field-by-field classification: FORT_POWER_STATUS_FIELD_CLASSIFICATION.csv
Public contract design:             FORT_POWER_STATUS_PUBLIC_SUMMARY_CONTRACT.md
Protected contract design:          FORT_POWER_STATUS_PROTECTED_RESEARCH_CONTRACT.md
Migration options:                  FORT_POWER_STATUS_ENDPOINT_MIGRATION_PLAN.md
Consolidated audit:                 FORT_POWER_STATUS_PUBLICATION_AUDIT.md
```

---

## Final Status

```text
FORT_POWER_STATUS_PUBLICATION_SPLIT_PLAN_READY_FOR_REVIEW
```
