"""
Unit tests for corpus_cleaning.py — deteksi kebocoran scan (nomor halaman,
header tanggal, entri katalog arsip) pada kolom `text` di
data/research/korpus_tema_slim.csv (tabel research_theme_rows).

Pure function tests (no DB) — mirrors backend/tests/test_linimasa_events.py
pattern. Fixture di bawah adalah sampel NYATA dari korpus (bukan data
karangan) -- lihat docs/prd/prd-pembersihan-korpus-daghregister.md §1.2/§1.3.
Pelajaran dari insiden lama: regex korpus HARUS diuji dgn sampel nyata dulu
sebelum diterapkan, jangan asumsi satu pola lalu langsung jalan.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from corpus_cleaning import detect_leak, strip_header_leak


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: detect_leak() -- corpus_asal='daghregister'
# ═══════════════════════════════════════════════════════════════════════════════

class TestDetectLeakDaghregister:
    def test_page_number_plus_date_header_titlecase(self):
        text = "106\n31 Maret.\nCatatan kapal-kapal yang masuk pada bulan Maret:\nDari Palembang."
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_page_number_plus_date_header_allcaps(self):
        text = "230\n7 JUNI.\nGuillam Ferment,\nFredrik Tim,\nJurriaen de Graeff,"
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_compound_date_with_dan(self):
        text = "550\n13 DAN 14 DESEMBER.\nvan aluyn can oock niet voldaen worden om reden"
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_compound_date_with_dan_lowercase_variant(self):
        text = "696\n20 DAN 21 DESEMBER.\n…; dan, karena kapas itu adalah barang dagangan"
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_date_range_with_hyphen(self):
        text = "410\n27-30 Agustus.\nakan pergi mengelilingi sungai,"
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_single_digit_day_no_leading_zero(self):
        text = "634\n5 Desember.\nmenanyakan, apakah prerogatif,"
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_date_line_without_trailing_period(self):
        text = "302\n31 JULI\n7\n5 pikol hasil cucian;"
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_index_page_daftar_nama(self):
        text = "552\nDAFTAR NAMA ORANG DAN TEMPAT.\nSia-ko, 1.\nSiakol, 598.\nSiam, 25, 52, 55."
        assert detect_leak(text, corpus_asal="daghregister") == "non_narrative"

    def test_index_page_register_dari_nama_variant(self):
        # Ditemukan susulan (verifikasi DB pasca-P1): variasi lain "REGISTER
        # DARI NAMA..." dan "REGISTER VON PERSONEN..." (campuran Belanda).
        text = "REGISTER DARI NAMA ORANG DAN TEMPAT.\nSoekadana, 427, 441, 495.\nSoe-Ko, 229."
        assert detect_leak(text, corpus_asal="daghregister") == "non_narrative"

    def test_index_page_register_von_personen_variant(self):
        text = "REGISTER VON PERSONEN DAN NAMA-NAMA TEMPAT.\nOntong Java, 3, 11, 88, 181."
        assert detect_leak(text, corpus_asal="daghregister") == "non_narrative"

    def test_index_page_register_nama_no_leading_digit(self):
        # Ditemukan susulan: variasi "Register nama..." tanpa nomor halaman
        # di depan sama sekali (beda dari "DAFTAR NAMA" yg biasa didahului nomor).
        text = "Register nama orang dan tempat.\n513\nSabda Karti (kiai), 443.\nSablat, 52, 282."
        assert detect_leak(text, corpus_asal="daghregister") == "non_narrative"

    def test_reversed_order_date_then_page_number(self):
        # Ditemukan susulan (P0.2): urutan KEBALIK dari asumsi awal -- header
        # tanggal duluan, nomor halaman baru setelahnya, baru narasi.
        text = "30 dan 31 Januari.\n27\nbiaya-biaya harus diatur menurut ketentuan yang tetap."
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_date_header_alone_no_page_number_visible(self):
        text = "17 FEBRUARI.\n\n... akan dikirim untuk menjawab kepada Ratu."
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_same_line_combined_page_and_date(self):
        # Nomor halaman & header tanggal digabung 1 baris (bukan 2 baris terpisah).
        text = "146 30 Juni.\n\nKota Couchin dan tempat-tempat lain kembali hendak ditaklukkan."
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_same_line_with_inserted_word(self):
        text = "172 Pada 23 JULI.\n\ndan malam di Ambon, yang ditulis kepada mereka Yang Mulia."
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_archaic_month_spelling_juny(self):
        text = "163 24 JUNY,\n\ndiminta agar sekali gus memenuhi tuntutan yang diharapkan."
        assert detect_leak(text, corpus_asal="daghregister") == "header_leak"

    def test_clean_narrative_no_leading_digit(self):
        text = "de anachoda van de joncgen rapporteert dat den coninck van Atchijn overleden is"
        assert detect_leak(text, corpus_asal="daghregister") == "clean"

    def test_clean_narrative_starting_with_year_no_header_line(self):
        # Kutipan asli /linimasa -- diawali angka tahun tapi ini prosa mengalir,
        # BUKAN nomor halaman + baris header terpisah. Harus TIDAK terdeteksi.
        text = ("1600 jn December heefft den admiraell van Caerden met den sabander "
                "en andere in Achin voorkoop gemaeckt")
        assert detect_leak(text, corpus_asal="daghregister") == "clean"

    def test_false_positive_ordinal_enumeration(self):
        # "1º" adalah enumerasi klausul traktat yang sah, bukan nomor halaman.
        text = "1º [hak dagang VOC] diluaskan, dengan pengecualian atas semua bangsa lain"
        assert detect_leak(text, corpus_asal="daghregister") == "clean"

    def test_single_line_text_never_flagged(self):
        text = "Van Sillebar telah datang ke Bantam 10 kendaraan dengan 500 baris lada."
        assert detect_leak(text, corpus_asal="daghregister") == "clean"

    def test_leading_digit_without_date_stays_clean(self):
        # Nomor di baris pertama TANPA header tanggal di baris kedua -- bukan
        # kebocoran, jangan salah tangkap (mis. kuantitas dagang, bukan halaman).
        text = "20\nkapal-kapal berlayar menuju pelabuhan itu dengan muatan penuh."
        assert detect_leak(text, corpus_asal="daghregister") == "clean"


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: detect_leak() -- corpus_asal='globalise' (pola berbeda, lihat PRD §1.3)
# ═══════════════════════════════════════════════════════════════════════════════

class TestDetectLeakGlobalise:
    def test_register_alfabetis_catalog_entry(self):
        text = ("Register alfabetis dari catatan harian dan urusan yang ditangani "
                "antara Tuan Komandan Julius Valenthijn Stein van Goelenesse dan raja-raja")
        assert detect_leak(text, corpus_asal="globalise") == "non_narrative"

    def test_register_dari_semua_surat(self):
        text = ("Register dari semua surat dan tulisan yang tiba berturut-turut di "
                "Batavia, diterima mengenai wilayah Siam, Tonkin, Tiongkok, Jepang")
        assert detect_leak(text, corpus_asal="globalise") == "non_narrative"

    def test_inventaris_range_prefix(self):
        text = ("1607-1622/3.\nPaket kedua\nsalinan buku surat-surat oleh Hendrick Jansz "
                "dari Patanis berisi:")
        assert detect_leak(text, corpus_asal="globalise") == "non_narrative"

    def test_inventaris_page_range_dot(self):
        text = ("760 s.d. 765- 782.. . Salinan laporan oleh pemungut cukai Jacob bean "
                "tentang penangkapan fluit Montfoort di teluk Nielwelle")
        assert detect_leak(text, corpus_asal="globalise") == "non_narrative"

    def test_index_marker_applies_to_globalise_too(self):
        # Ditemukan susulan (verifikasi DB pasca-P1): penanda indeks generik
        # ("Daftar isi...") juga muncul di globalise, bukan cuma daghregister --
        # aturan indeks harus lintas corpus_asal, bukan cuma di cabang daghregister.
        text = "Daftar isi resolusi\nyang diambil dalam rapat Politie, di kantor utama Belanda"
        assert detect_leak(text, corpus_asal="globalise") == "non_narrative"

    def test_globalise_clean_case_no_catalog_marker(self):
        text = "Surat dari Malaka, tanggal 14 Februari 1737, membicarakan urusan dagang lada."
        assert detect_leak(text, corpus_asal="globalise") == "clean"

    def test_bare_folio_number_then_catalog_content(self):
        # Ditemukan susulan saat P0.2: nomor folio polos + baris kosong/konten
        # katalog -- 22/22 sampel dicek manual, semuanya deskripsi katalog,
        # bukan narasi (beda dari daghregister yg nomor halaman diikuti narasi).
        text = "1710\n\nLembar 2041 sampai 2056, rekening konsumsi dari kapal-kapal tersebut"
        assert detect_leak(text, corpus_asal="globalise") == "non_narrative"

    def test_bare_folio_number_directly_followed_by_salutation(self):
        text = "678\nKepada Yang Mulia Tuan Gubernur Ioan Tideon Loten\nKepada E. Hoofd administrateur"
        assert detect_leak(text, corpus_asal="globalise") == "non_narrative"


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: strip_header_leak() -- hanya utk kategori header_leak (daghregister)
# ═══════════════════════════════════════════════════════════════════════════════

class TestStripHeaderLeak:
    def test_strips_page_number_and_date_line(self):
        text = "106\n31 Maret.\nCatatan kapal-kapal yang masuk pada bulan Maret:\nDari Palembang."
        assert strip_header_leak(text) == "Catatan kapal-kapal yang masuk pada bulan Maret:\nDari Palembang."

    def test_strips_allcaps_header(self):
        text = "230\n7 JUNI.\nGuillam Ferment,\nFredrik Tim,"
        assert strip_header_leak(text) == "Guillam Ferment,\nFredrik Tim,"

    def test_does_not_over_strip_when_only_two_lines(self):
        text = "634\n5 Desember."
        # Tidak ada narasi tersisa setelah strip -- fungsi mengembalikan string kosong,
        # bukan error, supaya pemanggil bisa memutuskan (mis. exclude baris ini).
        assert strip_header_leak(text) == ""

    def test_strips_reversed_order_date_then_page_number(self):
        text = "30 dan 31 Januari.\n27\nbiaya-biaya harus diatur menurut ketentuan yang tetap."
        assert strip_header_leak(text) == "biaya-biaya harus diatur menurut ketentuan yang tetap."

    def test_strips_same_line_combined_header(self):
        text = "146 30 Juni.\n\nKota Couchin dan tempat-tempat lain kembali hendak ditaklukkan."
        assert strip_header_leak(text) == "Kota Couchin dan tempat-tempat lain kembali hendak ditaklukkan."
