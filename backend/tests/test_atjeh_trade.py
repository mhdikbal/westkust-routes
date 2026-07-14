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
        """Sembilan volume Dagh-register sudah disisir (1643-1644, 1631-1634, 1637, 1636, 1624-1629, 1644-1645, 1647-1648, 1656-1657, 1659)."""
        docs = {r["source_document"] for r in rows}
        assert "1643-1644" in docs
        assert "1631-1634" in docs
        assert "1637" in docs
        assert "1636" in docs
        assert "1624-1629" in docs
        assert "1644-1645" in docs
        assert "1647-1648" in docs
        assert "1656-1657" in docs
        assert "1659" in docs

    def test_1656_1657_war_documented(self, rows):
        """Volume 1656-1657 mengungkap perang terbuka VOC-Atjeh, 6 tahun sebelum
        Traktat Painan -- harus ada baris politik dgn bukti perang eksplisit."""
        war_rows = [r for r in rows if r["source_document"] == "1656-1657"]
        assert len(war_rows) >= 5
        assert any("oorlo" in (r["text_asli"] or "").lower() for r in war_rows)

    def test_1659_peace_ends_the_war(self, rows):
        """Volume 1659 mengungkap perdamaian resmi yg mengakhiri perang 1656-57
        -- harus ada baris politik dgn bukti perdamaian eksplisit."""
        peace_rows = [r for r in rows if r["source_document"] == "1659"]
        assert len(peace_rows) >= 3
        assert any("vrede" in (r["text_asli"] or "").lower() for r in peace_rows)

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

    def test_political_facts_use_politik_direction(self, rows):
        """direction='politik' (kategori ke-4, ditambah 2026-07-13 atas permintaan
        user) HARUS dipakai utk semua baris fakta politik/administratif -- 'in_atjeh'
        jangan lagi jadi bucket ganda dagang+politik. Setiap baris 'BUKAN transaksi'
        harus direction='politik', dan sebaliknya."""
        for r in rows:
            is_political_note = "BUKAN transaksi" in (r["notes"] or "")
            is_politik_direction = r["direction"] == "politik"
            assert is_political_note == is_politik_direction, (
                f"baris p{r['source_page']}: notes bukan-transaksi={is_political_note} "
                f"tapi direction={r['direction']!r} tidak konsisten"
            )

    def test_every_row_has_source_document(self, rows):
        for r in rows:
            assert r["source_document"], f"baris p{r['source_page']} tanpa source_document"

    def test_cd1_treaties_documented(self, rows):
        """"tim DBA sisir CD1.pdf" (2026-07-14): Corpus Diplomaticum
        Neerlando-Indicum jilid I (traktat/kontrak VOC, ed. J.E. Heeres) --
        5 traktat baru, direction='politik', mundurkan titik awal korpus dari
        1631 ke 1600 (kontrak lada pertama VOC-Atjeh)."""
        cd1_rows = [r for r in rows if r["source_document"] == "CD1"]
        assert len(cd1_rows) >= 5
        for r in cd1_rows:
            assert r["direction"] == "politik"
            assert "Corpus Diplomaticum" in (r["notes"] or "")

    def test_cd2_treaties_documented(self, rows):
        """"tim MLOPS dan DBA sisir CD2.pdf" (2026-07-15): Corpus Diplomaticum
        Neerlando-Indicum jilid II (~1655-1673), lensa tol/pajak & hadiah
        diplomasi -- 14 traktat baru, direction='politik'."""
        cd2_rows = [r for r in rows if r["source_document"] == "CD2"]
        assert len(cd2_rows) >= 14
        for r in cd2_rows:
            assert r["direction"] == "politik"
            assert "Corpus Diplomaticum" in (r["notes"] or "")

    def test_cd3_treaties_documented(self, rows):
        """"tim MLOPS dan DBA sisir CD3.pdf" (2026-07-15): Corpus Diplomaticum
        Neerlando-Indicum jilid III (~1678-1690), volume paling padat --
        18 traktat baru, direction='politik'."""
        cd3_rows = [r for r in rows if r["source_document"] == "CD3"]
        assert len(cd3_rows) >= 18
        for r in cd3_rows:
            assert r["direction"] == "politik"
            assert "Corpus Diplomaticum" in (r["notes"] or "")

    def test_cd2_barus_treaty_predates_1681(self, rows):
        """Traktat Barus 29 April 1668 (CD2) ditemukan MENDAHULUI traktat Barus
        1681 (korpus_tema_slim.csv) 13 tahun -- caveat lama 'Barus nihil sampai
        1681' sudah usang, harus ada bukti Aceh-Barus dari CD2 juga."""
        barus_cd2 = [r for r in rows if r["source_document"] == "CD2" and "Barus" in (r["actor_raw"] or r["notes"] or "")]
        assert any("1668" in (r["notes"] or "") for r in barus_cd2)

    def test_no_translated_commodity_terms(self, rows):
        """Jangan pakai istilah Indonesia hasil terjemahan (mis. 'sendawa') --
        harus ejaan asli sumber (mis. 'salpeter'). Regresi utk feedback user."""
        banned = {"sendawa", "lada", "timah"}
        for r in rows:
            c = (r["commodity_raw"] or "").strip().lower()
            assert c not in banned, f"commodity_raw='{c}' adalah terjemahan, bukan istilah asli (p{r['source_page']})"
