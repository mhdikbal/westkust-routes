"""
Unit tests for seed_atjeh_trade.py logic + CSV integrity.

Pure function tests (no DB) — mirrors backend/tests/test_seed_logic.py pattern.
Source: "Dagh-register gehouden int casteel Batavia ... 1643-1644" (docs/).
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from seed_atjeh_trade import parse_row, ALLOWED_DIRECTIONS, CSV_FILE


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: parse_row()
# ═══════════════════════════════════════════════════════════════════════════════

class TestParseRow:
    def test_minimal_row_with_price(self):
        row = {
            "source_document": "1643-1644",
            "source_page": "137", "book_page": "", "entry_date_raw": "9 Mei 1644",
            "direction": "in_atjeh", "commodity_raw": "peper", "quantity_raw": "22",
            "unit_raw": "bahar", "price_value": "7", "price_unit_raw": "taijl/bhaer",
            "actor_raw": "ondercoopman Jan Lucassen Levendich",
            "text_asli": "22 bhaer peeper ende 18 catti tegens 7 theijl de bhaer genegotieert",
            "notes": "",
        }
        rec = parse_row(row)
        assert rec["source_page"] == 137
        assert rec["source_document"] == "1643-1644"
        assert rec["direction"] == "in_atjeh"
        assert rec["commodity_raw"] == "peper"
        assert rec["price_value"] == 7.0

    def test_empty_cargo_row(self):
        """'ledigh' (empty) ships: commodity_raw/unit_raw/price stay NULL, not '0'."""
        row = {
            "source_document": "1643-1644",
            "source_page": "33", "book_page": "16", "entry_date_raw": "22 Januari 1644",
            "direction": "van_atjeh", "commodity_raw": "", "quantity_raw": "",
            "unit_raw": "", "price_value": "", "price_unit_raw": "",
            "actor_raw": "gilioen ambassadeur van Atchin (via Indrapoura)",
            "text_asli": "een gilioen van Indrapoura toebehorende den ambassadeur van Atchin ledigh",
            "notes": "kargo kosong (ledigh)",
        }
        rec = parse_row(row)
        assert rec["commodity_raw"] is None
        assert rec["price_value"] is None

    def test_invalid_direction_rejected(self):
        row = {
            "source_document": "1643-1644",
            "source_page": "1", "book_page": "", "entry_date_raw": "",
            "direction": "sideways", "commodity_raw": "peper", "quantity_raw": "1",
            "unit_raw": "bahar", "price_value": "", "price_unit_raw": "",
            "actor_raw": "", "text_asli": "x", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)

    def test_missing_source_page_rejected(self):
        row = {
            "source_document": "1643-1644",
            "source_page": "", "book_page": "", "entry_date_raw": "",
            "direction": "naar_atjeh", "commodity_raw": "peper", "quantity_raw": "1",
            "unit_raw": "bahar", "price_value": "", "price_unit_raw": "",
            "actor_raw": "", "text_asli": "x", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)

    def test_missing_source_document_rejected(self):
        """Tiga volume PDF sekarang jadi sumber -- source_document wajib ada
        supaya source_page tak ambigu antar volume (mis. p164 beda isi di
        1643-1644 vs 1631-1634 vs 1637)."""
        row = {
            "source_document": "",
            "source_page": "1", "book_page": "", "entry_date_raw": "",
            "direction": "naar_atjeh", "commodity_raw": "peper", "quantity_raw": "1",
            "unit_raw": "bahar", "price_value": "", "price_unit_raw": "",
            "actor_raw": "", "text_asli": "x", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: CSV integrity — every curated row must be well-formed and traceable
# ═══════════════════════════════════════════════════════════════════════════════

class TestCsvIntegrity:
    @pytest.fixture(scope="class")
    def rows(self):
        assert CSV_FILE is not None and CSV_FILE.exists(), f"CSV tidak ditemukan: {CSV_FILE}"
        with CSV_FILE.open(newline="", encoding="utf-8") as f:
            return [parse_row(r) for r in csv.DictReader(f)]

    def test_has_minimum_rows(self, rows):
        assert len(rows) >= 8

    def test_all_directions_allowed(self, rows):
        for r in rows:
            assert r["direction"] in ALLOWED_DIRECTIONS

    def test_every_row_has_source_excerpt(self, rows):
        """text_asli wajib ada -- jejak verifikasi ke sumber OCR (anti klaim tanpa bukti)."""
        for r in rows:
            assert r["text_asli"] and len(r["text_asli"]) > 10

    def test_every_row_unverified_by_default(self, rows):
        for r in rows:
            assert r["confidence_flag"] == "unverified"

    def test_both_directions_represented(self, rows):
        """Permintaan user: laporan dagang DARI dan KE Atjeh -- bukan cuma satu arah."""
        directions = {r["direction"] for r in rows}
        assert "van_atjeh" in directions
        assert "naar_atjeh" in directions

    def test_all_volumes_represented(self, rows):
        """Empat volume Dagh-register sudah disisir (1643-1644, 1631-1634, 1637, 1636)."""
        docs = {r["source_document"] for r in rows}
        assert "1643-1644" in docs
        assert "1631-1634" in docs
        assert "1637" in docs
        assert "1636" in docs

    def test_political_facts_marked_not_trade(self, rows):
        """Baris fakta politik/administratif (klaim yurisdiksi, penegakan tol,
        suksesi raja -- bukan transaksi dagang) harus ditandai eksplisit "BUKAN
        transaksi" di notes, supaya tak salah dijumlah sbg volume dagang.
        Regresi 2026-07-13 (re-sisir setelah perbaikan regex)."""
        political = [r for r in rows if "BUKAN transaksi" in (r["notes"] or "")]
        assert len(political) >= 5
        for r in political:
            assert r["price_value"] is None, \
                f"baris p{r['source_page']} ditandai bukan-transaksi tapi punya price_value"

    def test_every_row_has_source_document(self, rows):
        for r in rows:
            assert r["source_document"], f"baris p{r['source_page']} tanpa source_document"

    def test_no_translated_commodity_terms(self, rows):
        """Jangan pakai istilah Indonesia hasil terjemahan (mis. 'sendawa') --
        harus ejaan asli sumber (mis. 'salpeter'). Regresi utk feedback user."""
        banned = {"sendawa", "lada", "timah"}
        for r in rows:
            c = (r["commodity_raw"] or "").strip().lower()
            assert c not in banned, f"commodity_raw='{c}' adalah terjemahan, bukan istilah asli (p{r['source_page']})"
