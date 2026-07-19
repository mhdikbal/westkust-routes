"""
Unit tests for seed_linimasa_events.py logic + CSV integrity.

Pure function tests (no DB) — mirrors backend/tests/test_atjeh_trade.py pattern.
Source: data/research/linimasa_events.csv (101 peristiwa suksesi/politik Atjeh,
1600-1775 -- distilasi atjeh_trade_records + docs/thesis/dr/korpus_tema_slim.csv
+ docs/CD1.pdf + docs/CD2.pdf + docs/CD3.pdf + docs/CD4.pdf + docs/CD5.pdf +
docs/CD6.pdf/Corpus Diplomaticum). Sejak Fase 1
(docs/prd/prd-linimasa-kronik-pantai-barat.md) tiap baris juga punya era_slug
(babak naratif) -- lihat ALLOWED_ERAS.
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
        """Fase 1 /linimasa (docs/prd/prd-linimasa-kronik-pantai-barat.md): tiap event
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

    def test_cd1_treaties_present(self, rows):
        """"tim DBA sisir CD1.pdf" (2026-07-14): Corpus Diplomaticum Neerlando-
        Indicum jilid I -- 6 peristiwa baru, SUMBER KETIGA (beda dari 9 volume
        Dagh-register kami sendiri MAUPUN korpus_tema_slim.csv). Harus ada &
        dari OCR pipeline kami sendiri (bukan tag 'SUMBER BEDA PIPELINE' yg
        reserved utk korpus_tema_slim.csv)."""
        cd1_rows = [r for r in rows if r["source_document"] == "CD1"]
        assert len(cd1_rows) >= 6
        for r in cd1_rows:
            assert "SUMBER BEDA PIPELINE" not in (r["notes"] or ""), \
                f"baris p{r['source_page']} (CD1) salah ditandai beda pipeline -- CD1 tetap OCR kami sendiri"

    def test_1600_is_new_earliest_year(self, rows):
        """Traktat dagang lada pertama VOC-Atjeh (CD1, Des 1600) memundurkan
        titik AWAL linimasa dari klaim yurisdiksi 1625 -- sebelumnya event
        tertua di seluruh korpus (lihat test_1625_earliest_jurisdiction_claim_present)."""
        years = [r["year"] for r in rows if r["year"] is not None]
        assert min(years) == 1600
        y1600 = [r for r in rows if r["year"] == 1600]
        assert all(r["source_document"] == "CD1" for r in y1600)

    def test_iskandar_thani_now_sourced(self, rows):
        """Traktat CD1 Feb-Mar 1641 adalah SUMBER PRIMER PERTAMA di seluruh
        korpus riset utk identitas 'Iskander Tsani' (Iskandar Thani) sbg
        pendahulu/suami Ratu Atjeh -- sebelumnya EKSPLISIT ditolak masuk data
        krn tak tersitasi (docs/prd/prd-linimasa-kronik-pantai-barat.md §2). Baris
        yg sumbernya cuma catatan kaki editor (bukan kutipan traktat periode
        VOC langsung) wajib ditandai eksplisit di notes, bukan didiamkan
        seolah setara kutipan primer lain."""
        thani_rows = [r for r in rows if "Tsani" in r["text_asli"] or "Thani" in r["title"]]
        assert len(thani_rows) >= 1
        for r in thani_rows:
            notes = (r["notes"] or "")
            assert "CATATAN" in notes and "editor" in notes.lower(), \
                f"baris p{r['source_page']} soal Iskandar Thani wajib tandai eksplisit bahwa sumbernya catatan kaki editor"

    def test_cd2_treaties_present(self, rows):
        """"tim MLOPS dan DBA sisir CD2.pdf" (2026-07-15): Corpus Diplomaticum
        jilid II (~1655-1673), lensa tol/pajak & hadiah diplomasi -- 14
        peristiwa baru, harus tetap dari OCR pipeline kami sendiri (bukan tag
        'SUMBER BEDA PIPELINE' yg reserved utk korpus_tema_slim.csv)."""
        cd2_rows = [r for r in rows if r["source_document"] == "CD2"]
        assert len(cd2_rows) >= 14
        for r in cd2_rows:
            assert "SUMBER BEDA PIPELINE" not in (r["notes"] or ""), \
                f"baris p{r['source_page']} (CD2) salah ditandai beda pipeline -- CD2 tetap OCR kami sendiri"

    def test_cd2_complements_not_duplicates_existing_events(self, rows):
        """Baris CD2 yg berkaitan dgn event yg sudah ada dari source_document
        lain (mis. Traktat Painan 1663 dari korpus_tema_slim.csv, Sillida 1667)
        wajib ditandai eksplisit 'MELENGKAPI' di notes -- bukan didiamkan
        seolah event baru yg tak berkaitan/duplikat."""
        painan_cd2 = [r for r in rows if r["source_document"] == "CD2" and r["year"] == 1663]
        assert len(painan_cd2) >= 1
        for r in painan_cd2:
            assert "MELENGKAPI" in (r["notes"] or ""), \
                f"baris p{r['source_page']} (CD2, 1663) wajib tandai eksplisit MELENGKAPI event Traktat Painan yg sudah ada"

    def test_cd2_barus_1668_predates_1681_treaty(self, rows):
        """Traktat Barus 29 April 1668 (CD2) adalah bukti Aceh-Barus PERTAMA yg
        sesungguhnya -- 13 tahun lebih awal dari traktat Barus 1681
        (korpus_tema_slim.csv) yg sebelumnya diklaim 'bukti pertama'. Kedua
        baris harus tetap ada (bukan salah satu dihapus), tapi baris 1668
        wajib menandai eksplisit bahwa ia mendahului 1681."""
        barus_1668 = [r for r in rows if r["source_document"] == "CD2" and r["year"] == 1668
                      and "Barus" in r["title"]]
        barus_1681 = [r for r in rows if r["source_document"] == "1681"]
        assert len(barus_1668) >= 1
        assert len(barus_1681) >= 1, "baris traktat Barus 1681 (korpus_tema_slim.csv) harus tetap ada, bukan dihapus"
        assert any("1681" in (r["notes"] or "") for r in barus_1668), \
            "baris Barus 1668 wajib eksplisit sebut ia mendahului traktat 1681"

    def test_perang_damai_era_extended_to_1655(self, rows):
        """Traktat damai Perak 7 Des 1655 (CD2) masuk babak 'perang-damai' --
        era ini diperluas dari 1656 ke 1655 utk menampungnya, non-overlap dgn
        'ratu-puncak' (berakhir 1650) tetap terjaga."""
        y1655 = [r for r in rows if r["year"] == 1655]
        assert len(y1655) >= 1
        assert all(r["era_slug"] == "perang-damai" for r in y1655)

    def test_cd3_treaties_present(self, rows):
        """"tim MLOPS dan DBA sisir CD3.pdf" (2026-07-15): Corpus Diplomaticum
        jilid III (~1678-1690), volume PALING PADAT -- 18 peristiwa baru,
        harus tetap dari OCR pipeline kami sendiri (bukan tag 'SUMBER BEDA
        PIPELINE' yg reserved utk korpus_tema_slim.csv)."""
        cd3_rows = [r for r in rows if r["source_document"] == "CD3"]
        assert len(cd3_rows) >= 18
        for r in cd3_rows:
            assert "SUMBER BEDA PIPELINE" not in (r["notes"] or ""), \
                f"baris p{r['source_page']} (CD3) salah ditandai beda pipeline -- CD3 tetap OCR kami sendiri"

    def test_1690_superseded_as_latest_year_by_cd4(self, rows):
        """Suksesi radja d'Ilhier Barus (CD3, 18 Okt 1690) SEMPAT jadi titik
        AKHIR linimasa, tapi CD4 (1693-1716) memajukannya lagi -- 1690 harus
        tetap ada sbg event CD3, tapi bukan lagi tahun terbaru di korpus."""
        y1690 = [r for r in rows if r["year"] == 1690]
        assert len(y1690) >= 1
        assert all(r["source_document"] == "CD3" for r in y1690)
        years = [r["year"] for r in rows if r["year"] is not None]
        assert max(years) > 1690

    def test_pengusiran_penataan_era_extended_to_1690(self, rows):
        """Era 'pengusiran-penataan' diperluas dari 1664-1681 ke 1664-1690 utk
        menampung 18 event CD3 (1678-1690), non-overlap dgn era lain tetap
        terjaga (retak-painan berakhir 1663)."""
        y1682_1690 = [r for r in rows if r["year"] is not None and 1682 <= r["year"] <= 1690]
        assert len(y1682_1690) >= 1
        assert all(r["era_slug"] == "pengusiran-penataan" for r in y1682_1690)

    def test_cd3_grand_alliance_1680_present(self, rows):
        """Traktat aliansi umum 29 Agustus 1680 (CD3) -- temuan terbesar sesi
        CD3, menyatukan Indrapoura/Padang/Kottatenga/Sillida dalam satu
        traktat pertama kalinya -- harus tercatat eksplisit."""
        y1680 = [r for r in rows if r["source_document"] == "CD3" and r["year"] == 1680]
        assert any("Seblat" in r["title"] or "seluruh pantai barat" in r["title"] for r in y1680)

    def test_cd4_treaties_present(self, rows):
        """"tim MLOPS dan DBA sisir CD4.pdf" (2026-07-15): Corpus Diplomaticum
        jilid IV (~1693-1716), rentang & jumlah event TERBESAR sejauh ini --
        20 peristiwa baru, harus tetap dari OCR pipeline kami sendiri (bukan
        tag 'SUMBER BEDA PIPELINE' yg reserved utk korpus_tema_slim.csv)."""
        cd4_rows = [r for r in rows if r["source_document"] == "CD4"]
        assert len(cd4_rows) >= 20
        for r in cd4_rows:
            assert "SUMBER BEDA PIPELINE" not in (r["notes"] or ""), \
                f"baris p{r['source_page']} (CD4) salah ditandai beda pipeline -- CD4 tetap OCR kami sendiri"

    def test_1716_superseded_as_latest_year_by_cd5(self, rows):
        """Pembaruan traktat Indrapoera (CD4, Maret 1716) SEMPAT jadi titik
        AKHIR linimasa, tapi CD5 (1727-1741) memajukannya lagi -- 1716 harus
        tetap ada sbg event CD4, tapi bukan lagi tahun terbaru di korpus."""
        y1716 = [r for r in rows if r["year"] == 1716]
        assert len(y1716) >= 1
        assert all(r["source_document"] == "CD4" for r in y1716)
        years = [r["year"] for r in rows if r["year"] is not None]
        assert max(years) > 1716

    def test_1741_superseded_as_latest_year_by_cd6(self, rows):
        """Pembaruan aliansi Tigablas & Doeapoeloeh-Kotta (CD5, 21 Okt 1741)
        SEMPAT jadi titik AKHIR linimasa, tapi CD6 (1755-1775) memajukannya
        lagi -- 1741 harus tetap ada sbg event CD5, tapi bukan lagi tahun
        terbaru di korpus."""
        y1741 = [r for r in rows if r["year"] == 1741]
        assert len(y1741) >= 1
        assert all(r["source_document"] == "CD5" for r in y1741)
        years = [r["year"] for r in rows if r["year"] is not None]
        assert max(years) > 1741

    def test_pengusiran_penataan_era_extended_to_1716(self, rows):
        """Era 'pengusiran-penataan' diperluas lagi dari 1664-1690 ke 1664-1716
        utk menampung 20 event CD4 (1693-1716), non-overlap dgn era lain tetap
        terjaga."""
        y1691_1716 = [r for r in rows if r["year"] is not None and 1691 <= r["year"] <= 1716]
        assert len(y1691_1716) >= 1
        assert all(r["era_slug"] == "pengusiran-penataan" for r in y1691_1716)

    def test_cd4_nias_expedition_present(self, rows):
        """Ekspedisi vaandrig Johannes Sas (1693) MELUAS ke pulau Nias -- 7
        traktat aliansi terpisah, jangkauan geografis terjauh utara di
        seluruh korpus kami -- harus tercatat eksplisit."""
        nias_rows = [r for r in rows if r["source_document"] == "CD4" and "Nias" in r["title"] + (r["ruler_actor"] or "")]
        assert len(nias_rows) >= 5

    def test_cd4_priaman_longest_relapse_present(self, rows):
        """Priaman dkk relaps ke Aceh ~20 tahun sebelum ditundukkan ulang 1712
        (CD4) -- jeda relaps terlama tercatat dlm seluruh siklus westkust,
        harus tercatat eksplisit di notes."""
        priaman_1712 = [r for r in rows if r["source_document"] == "CD4" and r["year"] == 1712]
        assert len(priaman_1712) >= 1
        assert any("Atchin" in r["text_asli"] or "Aetchin" in r["text_asli"] for r in priaman_1712)

    def test_cd5_treaties_present(self, rows):
        """"tim MLOPS dan DBA sisir CD5.pdf" (2026-07-15): Corpus Diplomaticum
        jilid V (~1727-1741), volume PALING SEDIKIT konten westkust/Aceh
        sejauh ini -- 4 peristiwa baru, harus tetap dari OCR pipeline kami
        sendiri (bukan tag 'SUMBER BEDA PIPELINE' yg reserved utk
        korpus_tema_slim.csv)."""
        cd5_rows = [r for r in rows if r["source_document"] == "CD5"]
        assert len(cd5_rows) >= 4
        for r in cd5_rows:
            assert "SUMBER BEDA PIPELINE" not in (r["notes"] or ""), \
                f"baris p{r['source_page']} (CD5) salah ditandai beda pipeline -- CD5 tetap OCR kami sendiri"

    def test_pengusiran_penataan_era_extended_to_1741(self, rows):
        """Era 'pengusiran-penataan' diperluas lagi dari 1664-1716 ke 1664-1741
        utk menampung 4 event CD5 (1727-1741), non-overlap dgn era lain tetap
        terjaga."""
        y1717_1741 = [r for r in rows if r["year"] is not None and 1717 <= r["year"] <= 1741]
        assert len(y1717_1741) >= 1
        assert all(r["era_slug"] == "pengusiran-penataan" for r in y1717_1741)

    def test_cd5_1740_rebellion_context_present(self, rows):
        """Pemberontakan besar 1740 (Paoeh/Kotta-Tengah/Priaman di bawah Abdul
        Jalil, VOC lepas benteng Priaman) adalah konteks traktat CD5 21 Okt
        1741 -- harus tercatat eksplisit di notes."""
        y1741 = [r for r in rows if r["source_document"] == "CD5" and r["year"] == 1741]
        assert len(y1741) >= 1
        assert any("Abdul Jalil" in (r["notes"] or "") for r in y1741)

    def test_cd6_treaties_present(self, rows):
        """"tim MLOPS dan DBA sisir CD6.pdf" (2026-07-15): Corpus Diplomaticum
        jilid VI (~1755-1775) -- 8 peristiwa baru, harus tetap dari OCR
        pipeline kami sendiri (bukan tag 'SUMBER BEDA PIPELINE' yg reserved
        utk korpus_tema_slim.csv)."""
        cd6_rows = [r for r in rows if r["source_document"] == "CD6"]
        assert len(cd6_rows) >= 8
        for r in cd6_rows:
            assert "SUMBER BEDA PIPELINE" not in (r["notes"] or ""), \
                f"baris p{r['source_page']} (CD6) salah ditandai beda pipeline -- CD6 tetap OCR kami sendiri"

    def test_1775_is_new_latest_year(self, rows):
        """Penutupan loge Baros (CD6, 23 Jan 1775) memajukan titik AKHIR
        linimasa dari 1741 ke 1775 -- peristiwa TERBARU di seluruh korpus."""
        years = [r["year"] for r in rows if r["year"] is not None]
        assert max(years) == 1775
        y1775 = [r for r in rows if r["year"] == 1775]
        assert all(r["source_document"] == "CD6" for r in y1775)

    def test_pengusiran_penataan_era_extended_to_1775(self, rows):
        """Era 'pengusiran-penataan' diperluas lagi dari 1664-1741 ke 1664-1775
        utk menampung 8 event CD6 (1755-1775), non-overlap dgn era lain tetap
        terjaga."""
        y1742_1775 = [r for r in rows if r["year"] is not None and 1742 <= r["year"] <= 1775]
        assert len(y1742_1775) >= 1
        assert all(r["era_slug"] == "pengusiran-penataan" for r in y1742_1775)

    def test_cd6_1755_renewal_campaign_present(self, rows):
        """Rangkaian renovasi besar Feb 1755-Jan 1756 (~30 negeri westkust,
        dipicu kekhawatiran aktivitas Inggris) adalah temuan pembuka CD6 --
        harus tercatat eksplisit di notes."""
        y1755 = [r for r in rows if r["source_document"] == "CD6" and r["year"] == 1755]
        assert len(y1755) >= 3
        assert any("RENOVASI BESAR" in (r["notes"] or "") for r in y1755)
