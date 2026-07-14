"""
Unit tests for seed_linimasa_events.py logic + CSV integrity.

Pure function tests (no DB) — mirrors backend/tests/test_atjeh_trade.py pattern.
Source: data/research/linimasa_events.csv (30 peristiwa suksesi/politik Atjeh,
1625-1681 -- distilasi atjeh_trade_records + docs/thesis/dr/korpus_tema_slim.csv).
Sejak Fase 1 (docs/prd-linimasa-kronik-pantai-barat.md) tiap baris juga punya
era_slug (babak naratif) -- lihat ALLOWED_ERAS.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from seed_linimasa_events import parse_row, ALLOWED_EVENT_TYPES, ALLOWED_SOURCE_DOCUMENTS, ALLOWED_ERAS, CSV_FILE


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: parse_row()
# ═══════════════════════════════════════════════════════════════════════════════

class TestParseRow:
    def test_minimal_row(self):
        row = {
            "source_document": "1637", "source_page": "99", "book_page": "86",
            "event_date_raw": "10-12 Maret 1637", "year": "1637", "event_type": "suksesi",
            "ruler_actor": "Coninck van Atchijn", "title": "Raja Atjeh wafat",
            "era_slug": "klaim-awal",
            "text_asli": "de anachoda van de joncgen rapporteert dat den coninck van Atchijn overleden is",
            "notes": "",
        }
        rec = parse_row(row)
        assert rec["source_page"] == 99
        assert rec["year"] == 1637
        assert rec["event_type"] == "suksesi"
        assert rec["title"] == "Raja Atjeh wafat"
        assert rec["era_slug"] == "klaim-awal"

    def test_invalid_event_type_rejected(self):
        row = {
            "source_document": "1637", "source_page": "1", "book_page": "", "event_date_raw": "",
            "year": "", "event_type": "sideways", "ruler_actor": "", "title": "x",
            "era_slug": "klaim-awal", "text_asli": "x", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)

    def test_invalid_source_document_rejected(self):
        row = {
            "source_document": "9999", "source_page": "1", "book_page": "", "event_date_raw": "",
            "year": "", "event_type": "suksesi", "ruler_actor": "", "title": "x",
            "era_slug": "klaim-awal", "text_asli": "x", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)

    def test_missing_title_rejected(self):
        row = {
            "source_document": "1637", "source_page": "1", "book_page": "", "event_date_raw": "",
            "year": "", "event_type": "suksesi", "ruler_actor": "", "title": "",
            "era_slug": "klaim-awal", "text_asli": "x", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)

    def test_missing_text_asli_rejected(self):
        row = {
            "source_document": "1637", "source_page": "1", "book_page": "", "event_date_raw": "",
            "year": "", "event_type": "suksesi", "ruler_actor": "", "title": "x",
            "era_slug": "klaim-awal", "text_asli": "", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)

    def test_year_optional(self):
        row = {
            "source_document": "1647-1648", "source_page": "94", "book_page": "80-81",
            "event_date_raw": "sebelum Mei 1648", "year": "", "event_type": "administratif",
            "ruler_actor": "panglima van Cillida", "title": "x",
            "era_slug": "ratu-puncak", "text_asli": "x", "notes": "",
        }
        rec = parse_row(row)
        assert rec["year"] is None

    def test_invalid_era_slug_rejected(self):
        row = {
            "source_document": "1637", "source_page": "1", "book_page": "", "event_date_raw": "",
            "year": "", "event_type": "suksesi", "ruler_actor": "", "title": "x",
            "era_slug": "babak-yg-tak-ada", "text_asli": "x", "notes": "",
        }
        with pytest.raises(ValueError):
            parse_row(row)


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

    def test_korpus_tema_slim_rows_flag_different_pipeline(self, rows):
        """Baris source_document dari korpus_tema_slim.csv (1661/1663/1664/1665/1681)
        sumbernya BEDA pipeline (terjemahan Indonesia) -- notes wajib menyebut ini
        eksplisit, jangan didiamkan seolah sama dgn OCR Belanda baris lain."""
        corpus_sourced = [r for r in rows if r["source_document"] in ("1661", "1663", "1664", "1665", "1681")]
        assert len(corpus_sourced) >= 10
        for r in corpus_sourced:
            assert "SUMBER BEDA PIPELINE" in (r["notes"] or ""), \
                f"baris p{r['source_page']} ({r['source_document']}) tak menandai provenance beda pipeline"

    def test_years_ascending_or_covers_range(self, rows):
        years = [r["year"] for r in rows if r["year"] is not None]
        assert min(years) <= 1625
        assert max(years) >= 1681

    def test_1625_earliest_jurisdiction_claim_present(self, rows):
        """Klaim yurisdiksi Atjeh TERLUAS (VOC sendiri, vol.1624-1629) adalah
        event TERTUA linimasa -- sempat terlewat sesi awal, jangan lewat lagi."""
        y1625 = [r for r in rows if r["year"] == 1625]
        assert len(y1625) >= 2
        assert all(r["source_document"] == "1624-1629" for r in y1625)

    def test_barus_treaty_present(self, rows):
        """Ekstraksi 1661-1681 menemukan bukti Atjeh-Barus PERTAMA di seluruh korpus
        riset (traktat 1681) -- harus tercatat eksplisit di linimasa, bukan diabaikan."""
        barus_rows = [r for r in rows if "Barus" in r["title"] or "Barus" in (r["ruler_actor"] or "")]
        assert len(barus_rows) >= 1
        assert any(r["year"] == 1681 for r in barus_rows)

    def test_sillida_expulsion_arc_present(self, rows):
        """Arc pengusiran Atjeh dari Sillida (1664 kabur -> 1665 tuntas -> 1667
        penyerahan formal) harus lengkap, bukan cuma satu titik."""
        years_present = {r["year"] for r in rows if r["year"] is not None}
        assert 1664 in years_present
        assert 1665 in years_present
        assert 1667 in years_present

    def test_1656_1657_war_present_and_own_pipeline(self, rows):
        """Perang terbuka VOC-Atjeh 1656-57 (didistilasi dari atjeh_trade_records,
        BUKAN korpus_tema_slim.csv) harus ada, dan notes-nya TIDAK boleh salah
        ditandai 'SUMBER BEDA PIPELINE' krn ini dari pipeline OCR docs/ kita sendiri."""
        war_rows = [r for r in rows if r["source_document"] == "1656-1657"]
        assert len(war_rows) >= 5
        for r in war_rows:
            assert "SUMBER BEDA PIPELINE" not in (r["notes"] or ""), \
                f"baris p{r['source_page']} (1656-1657) salah ditandai beda pipeline -- ini dari OCR docs/ kita"

    def test_1659_peace_resolves_the_war(self, rows):
        """Perdamaian 1659 yg mengakhiri perang 1656-57 harus tercatat sbg event
        'perjanjian', bukan diam-diam hilang dari linimasa."""
        peace = [r for r in rows if r["source_document"] == "1659" and r["event_type"] == "perjanjian"]
        assert len(peace) >= 1
        assert peace[0]["year"] == 1659

    def test_all_rows_have_valid_era(self, rows):
        """Fase 1 /linimasa (docs/prd-linimasa-kronik-pantai-barat.md): tiap event
        wajib punya babak (era_slug), tak boleh NULL/di luar 5 babak yg didefinisikan."""
        for r in rows:
            assert r["era_slug"] in ALLOWED_ERAS, \
                f"baris p{r['source_page']} era_slug={r['era_slug']!r} tak valid"

    def test_all_five_eras_represented(self, rows):
        """Kelima babak harus punya minimal 1 event -- babak kosong artinya
        rentang tahunnya salah dipetakan atau perlu digabung dgn babak lain."""
        eras_present = {r["era_slug"] for r in rows}
        assert eras_present == ALLOWED_ERAS

    def test_era_year_ranges_non_overlapping(self, rows):
        """Tiap event hanya boleh masuk SATU babak berbasis tahun -- pastikan tak
        ada tahun yg sama muncul di dua era_slug berbeda (rentang tumpang tindih)."""
        year_to_eras = {}
        for r in rows:
            if r["year"] is None:
                continue
            year_to_eras.setdefault(r["year"], set()).add(r["era_slug"])
        for year, eras in year_to_eras.items():
            assert len(eras) == 1, f"tahun {year} muncul di >1 era: {eras}"
