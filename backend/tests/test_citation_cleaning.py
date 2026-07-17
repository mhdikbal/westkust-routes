"""
test_citation_cleaning.py — TDD utk citation_cleaning.py (CD1-CD6).

Masalah: kolom `notes` linimasa_events/atjeh_trade_records menyimpan literal
nama file scan "(CD1.pdf)".."(CD6.pdf)" yang bocor apa adanya ke /linimasa
dan /riset/atjeh-dagang. Juga kolom `source_document` (nilai mentah "CD1"..
"CD6") ditampilkan langsung sbg "vol. CD1" alih-alih judul buku sebenarnya.

Semua sampel di bawah adalah string NYATA dari data/research/linimasa_events.csv
dan atjeh_trade.csv (per disiplin proyek: uji regex thd sampel asli dulu).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from citation_cleaning import CD_JILID, clean_cd_citation, cd_source_label


# ─── cd_source_label ─────────────────────────────────────────────────────────

def test_cd_source_label_maps_all_six_volumes():
    assert cd_source_label("CD1") == "Corpus Diplomaticum Neerlando-Indicum, Jilid I"
    assert cd_source_label("CD2") == "Corpus Diplomaticum Neerlando-Indicum, Jilid II"
    assert cd_source_label("CD3") == "Corpus Diplomaticum Neerlando-Indicum, Jilid III"
    assert cd_source_label("CD4") == "Corpus Diplomaticum Neerlando-Indicum, Jilid IV"
    assert cd_source_label("CD5") == "Corpus Diplomaticum Neerlando-Indicum, Jilid V"
    assert cd_source_label("CD6") == "Corpus Diplomaticum Neerlando-Indicum, Jilid VI"


def test_cd_source_label_passthrough_non_cd_codes():
    """Baris Dagh-register pakai source_document spt '1624-1629', '1659' -- BUKAN
    kode CD, harus dibiarkan apa adanya (label sudah benar, bukan nama file)."""
    assert cd_source_label("1624-1629") == "1624-1629"
    assert cd_source_label("1659") == "1659"


def test_cd_jilid_dict_has_six_entries():
    assert len(CD_JILID) == 6
    assert set(CD_JILID) == {"CD1", "CD2", "CD3", "CD4", "CD5", "CD6"}


# ─── clean_cd_citation (kolom notes) ────────────────────────────────────────

def test_clean_cd1_missing_jilid_label():
    """CD1 SATU-SATUNYA yang di data mentah tak menyertakan 'jilid I' sama sekali."""
    raw = ("SUMBER: Corpus Diplomaticum (CD1.pdf), traktat IX 'Atjeh'. Kontrak dagang "
           "PERTAMA VOC-Atjeh tercatat di seluruh korpus riset ini.")
    out = clean_cd_citation(raw)
    assert ".pdf" not in out
    assert "CD1" not in out
    assert "Corpus Diplomaticum Neerlando-Indicum, Jilid I" in out
    assert "traktat IX 'Atjeh'" in out  # sisa kalimat tak boleh rusak


def test_clean_cd2_already_has_jilid_label():
    raw = ("SUMBER: Corpus Diplomaticum jilid II (CD2.pdf), traktat CCXVI 'Malaka-Atjeh'. "
           "Perjanjian damai mengakhiri konflik Perak.")
    out = clean_cd_citation(raw)
    assert ".pdf" not in out
    assert "CD2" not in out
    assert "Corpus Diplomaticum Neerlando-Indicum, Jilid II" in out
    # tak boleh dobel "jilid II ... Jilid II"
    assert out.count("Jilid II") == 1


def test_clean_cd_citation_no_trailing_treaty_number():
    """Baris tanpa nomor traktat setelah tanda kurung (titik langsung)."""
    raw = "SUMBER: Corpus Diplomaticum jilid II (CD2.pdf). Klausul yurisdiksi VOC-Indrapoura."
    out = clean_cd_citation(raw)
    assert ".pdf" not in out
    assert "Corpus Diplomaticum Neerlando-Indicum, Jilid II" in out


def test_clean_cd_citation_all_six_volumes_real_samples():
    samples = {
        1: "SUMBER: Corpus Diplomaticum (CD1.pdf), traktat XXI 'Atjeh'.",
        2: "SUMBER: Corpus Diplomaticum jilid II (CD2.pdf), traktat CCXXXVIII 'Atjeh'.",
        3: "SUMBER: Corpus Diplomaticum jilid III (CD3.pdf), traktat CCCLXXX.",
        4: "SUMBER: Corpus Diplomaticum jilid IV (CD4.pdf), traktat DXCVIII.",
        5: "SUMBER: Corpus Diplomaticum jilid V (CD5.pdf), traktat DCCXVI.",
        6: "SUMBER: Corpus Diplomaticum jilid VI (CD6.pdf), traktat MXCIX.",
    }
    roman = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}
    for n, raw in samples.items():
        out = clean_cd_citation(raw)
        assert ".pdf" not in out, f"CD{n}: .pdf masih bocor -> {out!r}"
        assert f"CD{n}" not in out, f"CD{n}: kode mentah masih bocor -> {out!r}"
        assert f"Corpus Diplomaticum Neerlando-Indicum, Jilid {roman[n]}" in out


def test_clean_cd_citation_passthrough_no_cd_mention():
    """Baris tanpa mention CD sama sekali (mis. Dagh-register) tak boleh berubah."""
    raw = "SUMBER: Dagh-register Batavia vol. 1656-1657, hlm. 214."
    assert clean_cd_citation(raw) == raw


def test_clean_cd_citation_empty_and_none():
    assert clean_cd_citation("") == ""
    assert clean_cd_citation(None) == ""
