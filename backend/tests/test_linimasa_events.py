"""
Unit tests for seed_linimasa_events.py logic + CSV integrity.

Pure function tests (no DB) — mirrors backend/tests/test_atjeh_trade.py pattern.
Source: data/research/linimasa_events.csv (9 peristiwa suksesi/politik Atjeh,
1632-1663 -- distilasi atjeh_trade_records + docs/thesis/dr/korpus_tema_slim.csv).
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from seed_linimasa_events import parse_row, ALLOWED_EVENT_TYPES, ALLOWED_SOURCE_DOCUMENTS, CSV_FILE


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: parse_row()
# ═══════════════════════════════════════════════════════════════════════════════

class TestParseRow:
    def test_minimal_row(self):
        row = {
            "source_document": "1637", "source_page": "99", "book_page": "86",
            "event_date_raw": "10-12 Maret 1637", "year": "1637", "event_type": "suksesi",
            "ruler_actor": "Coninck van Atchijn", "title": "Raja Atjeh wafat",
            "text_asli": "de anachoda van de joncgen rapporteert dat den coninck van Atchijn overleden is",
            "notes": "",
        }
        rec = parse_row(row)
        assert rec["source_page"] == 99
        assert rec["year"] == 1637
        assert rec["event_type"] == "suksesi"
        assert rec["title"] == "Raja Atjeh wafat"

    def test_invalid_event_type_rejected(self):
        row = {
            "source_document": "1637", "source_page": "1", "book_page": "", "event_date_raw": "",
            "year": "", "event_type": "sideways", "ruler_actor": "", "title": "x",
            "text_asli": "x", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)

    def test_invalid_source_document_rejected(self):
        row = {
            "source_document": "9999", "source_page": "1", "book_page": "", "event_date_raw": "",
            "year": "", "event_type": "suksesi", "ruler_actor": "", "title": "x",
            "text_asli": "x", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)

    def test_missing_title_rejected(self):
        row = {
            "source_document": "1637", "source_page": "1", "book_page": "", "event_date_raw": "",
            "year": "", "event_type": "suksesi", "ruler_actor": "", "title": "",
            "text_asli": "x", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)

    def test_missing_text_asli_rejected(self):
        row = {
            "source_document": "1637", "source_page": "1", "book_page": "", "event_date_raw": "",
            "year": "", "event_type": "suksesi", "ruler_actor": "", "title": "x",
            "text_asli": "", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)

    def test_year_optional(self):
        row = {
            "source_document": "1647-1648", "source_page": "94", "book_page": "80-81",
            "event_date_raw": "sebelum Mei 1648", "year": "", "event_type": "administratif",
            "ruler_actor": "panglima van Cillida", "title": "x", "text_asli": "x", "notes": "",
        }
        rec = parse_row(row)
        assert rec["year"] is None


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: CSV integrity
# ═══════════════════════════════════════════════════════════════════════════════

class TestCsvIntegrity:
    @pytest.fixture(scope="class")
    def rows(self):
        assert CSV_FILE is not None and CSV_FILE.exists(), f"CSV tidak ditemukan: {CSV_FILE}"
        with CSV_FILE.open(newline="", encoding="utf-8") as f:
            return [parse_row(r) for r in csv.DictReader(f)]

    def test_has_minimum_rows(self, rows):
        assert len(rows) >= 8

    def test_all_event_types_allowed(self, rows):
        for r in rows:
            assert r["event_type"] in ALLOWED_EVENT_TYPES

    def test_all_source_documents_allowed(self, rows):
        for r in rows:
            assert r["source_document"] in ALLOWED_SOURCE_DOCUMENTS

    def test_every_row_has_source_excerpt(self, rows):
        """text_asli wajib ada -- jejak verifikasi ke sumber, tak boleh klaim tanpa bukti."""
        for r in rows:
            assert r["text_asli"] and len(r["text_asli"]) > 10

    def test_every_row_unverified_by_default(self, rows):
        for r in rows:
            assert r["confidence_flag"] == "unverified"

    def test_every_row_has_title(self, rows):
        for r in rows:
            assert r["title"], f"baris p{r['source_page']} tanpa title"

    def test_succession_arc_represented(self, rows):
        """Linimasa harus mencakup arc utama: suksesi (wafat/ratu) DAN perjanjian
        (Traktat Painan) -- bukan cuma satu jenis peristiwa."""
        types = {r["event_type"] for r in rows}
        assert "suksesi" in types
        assert "perjanjian" in types

    def test_painan_treaty_present(self, rows):
        """Traktat Painan 1663 adalah anchor event linimasa -- wajib ada, sourced
        dari source_document='1663' (corpus terpisah korpus_tema_slim.csv)."""
        painan = [r for r in rows if r["source_document"] == "1663"]
        assert len(painan) >= 3
        for r in painan:
            assert r["year"] in (1662, 1663)

    def test_1663_rows_flag_different_pipeline(self, rows):
        """Baris source_document='1663' sumbernya BEDA pipeline (korpus_tema_slim.csv,
        terjemahan Indonesia) -- notes wajib menyebut ini eksplisit, jangan didiamkan
        seolah sama dgn OCR Belanda baris lain."""
        painan = [r for r in rows if r["source_document"] == "1663"]
        for r in painan:
            assert "SUMBER BEDA PIPELINE" in (r["notes"] or ""), \
                f"baris p{r['source_page']} (1663) tak menandai provenance beda pipeline"

    def test_years_ascending_or_covers_range(self, rows):
        years = [r["year"] for r in rows if r["year"] is not None]
        assert min(years) <= 1637
        assert max(years) >= 1663
