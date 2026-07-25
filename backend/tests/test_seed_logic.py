"""
Unit tests for seed_data.py logic functions.
Tests clean_name() and classify_direction() independently of the database.

These are pure function tests — no DB, no async, no mocking needed.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from seed_data import clean_name, classify_direction, FORTS_META


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: FORTS_META -- Fase 2 roster (docs/prd/prd-atlas-power-model-fase2-roster.md)
# ═══════════════════════════════════════════════════════════════════════════════

class TestFase2RosterForts:
    """Koto Tangah & Pauh ditambahkan sbg 2 fort terpisah (bukan digabung
    'Paoeh/Kotta-tengah') utk isi 15 linimasa_events yg selama ini
    fort_id=NULL -- lihat memory project_padang_hinterland_gaps &
    project_nias_1693_gap_evidence."""

    def test_koto_tangah_present(self):
        koto_tangah = next((f for f in FORTS_META if f["name"] == "Koto Tangah"), None)
        assert koto_tangah is not None
        assert koto_tangah["port_type"] == "departure"
        assert isinstance(koto_tangah["latitude"], float)
        assert isinstance(koto_tangah["longitude"], float)

    def test_pauh_present(self):
        pauh = next((f for f in FORTS_META if f["name"] == "Pauh"), None)
        assert pauh is not None
        assert pauh["port_type"] == "departure"
        assert isinstance(pauh["latitude"], float)
        assert isinstance(pauh["longitude"], float)

    def test_koto_tangah_pauh_distinct_coordinates(self):
        """Dua nagari berbeda (buku 'Padang Abad XVII-XVIII' hlm 237: Koto
        Tangah = portal pesisir, Pauh = lebih jauh ke timur/pedalaman) --
        koordinat harus beda, bukan titik yg sama disalin 2x."""
        koto_tangah = next(f for f in FORTS_META if f["name"] == "Koto Tangah")
        pauh = next(f for f in FORTS_META if f["name"] == "Pauh")
        assert (koto_tangah["latitude"], koto_tangah["longitude"]) != (pauh["latitude"], pauh["longitude"])

    def test_koto_tangah_pauh_names_unique_in_roster(self):
        names = [f["name"] for f in FORTS_META]
        assert names.count("Koto Tangah") == 1
        assert names.count("Pauh") == 1

    @pytest.mark.parametrize("name", ["Nias", "Natal", "Singkil", "Sorkam"])
    def test_sisa_fase2_fort_present(self, name):
        """Sisa 4 entitas Fase 2 (PRD §2): Nias (1 titik agregat per §3 Opsi
        A), Natal, Singkil, Sorkam -- semua entitas geografis riil/modern,
        beda dari Koto Tangah/Pauh yg butuh estimasi toponimi VOC-era."""
        fort = next((f for f in FORTS_META if f["name"] == name), None)
        assert fort is not None
        assert fort["port_type"] == "departure"
        assert isinstance(fort["latitude"], float)
        assert isinstance(fort["longitude"], float)

    def test_all_fase2_forts_have_unique_coordinates(self):
        """6 fort Fase 2 (Koto Tangah, Pauh, Nias, Natal, Singkil, Sorkam)
        harus py 6 koordinat berbeda -- tak ada yg tersalin dari fort lain."""
        names = ["Koto Tangah", "Pauh", "Nias", "Natal", "Singkil", "Sorkam"]
        coords = [(f["latitude"], f["longitude"])
                  for n in names for f in FORTS_META if f["name"] == n]
        assert len(coords) == 6
        assert len(set(coords)) == 6


class TestFortYork:
    """Fort York (Bengkulu/Bencoolen) -- pos EIC (Inggris), BUKAN pos VOC,
    di luar cakupan geografis inti 'westkust' (selatan Silebar). Ditambahkan
    krn arsip BL_IOR_G_35_198 (British Library IOR, via AmDigital) -- surat
    dari York Fort 18/22 Sept 1686 soal konsesi 'Raja Manacabo (Minangkabau)'
    Barus-Silebar ke Inggris & kehilangan pos Batang Capas -- cross-validasi
    independen thd row Painan/1686/buku-vogel-1690 yg sudah ada. Lihat
    project_vogel_full_survey_sillida_mine / user request 2026-07-24."""

    def test_fort_york_present(self):
        fort = next((f for f in FORTS_META if f["name"] == "Fort York"), None)
        assert fort is not None
        assert isinstance(fort["latitude"], float)
        assert isinstance(fort["longitude"], float)

    def test_fort_york_coordinates_match_user_supplied_point(self):
        """Koordinat persis yg diberikan user (Bengkulu), bukan estimasi."""
        fort = next(f for f in FORTS_META if f["name"] == "Fort York")
        assert round(fort["latitude"], 6) == round(-3.7766925254615944, 6)
        assert round(fort["longitude"], 6) == round(102.26424897116361, 6)

    def test_fort_york_name_unique_in_roster(self):
        names = [f["name"] for f in FORTS_META]
        assert names.count("Fort York") == 1


class TestFortMarlborough:
    """Fort Marlborough (Bengkulu) -- pengganti York Fort 1714, Presidency EIC
    1761-1785. Sumber: Kathirithamby (1965) thesis + surat Henry Botham 1781."""

    def test_fort_marlborough_present(self):
        fort = next((f for f in FORTS_META if f["name"] == "Fort Marlborough"), None)
        assert fort is not None
        assert isinstance(fort["latitude"], float)
        assert isinstance(fort["longitude"], float)

    def test_fort_marlborough_coordinates_match_user_supplied_point(self):
        fort = next(f for f in FORTS_META if f["name"] == "Fort Marlborough")
        assert round(fort["latitude"], 6) == round(-3.7870018339628033, 6)
        assert round(fort["longitude"], 6) == round(102.25174006960465, 6)

    def test_fort_marlborough_name_unique_in_roster(self):
        names = [f["name"] for f in FORTS_META]
        assert names.count("Fort Marlborough") == 1


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: clean_name()
# ═══════════════════════════════════════════════════════════════════════════════

class TestCleanName:
    """Tests for port name normalization."""

    def test_simple_name(self):
        """Simple name should pass through unchanged."""
        assert clean_name("Padang") == "Padang"

    def test_comma_separated_name(self):
        """'Batavia,Batavia' should return 'Batavia'."""
        assert clean_name("Batavia,Batavia") == "Batavia"

    def test_comma_with_region(self):
        """'Padang,Sumatra's Westkust' should return 'Padang'."""
        assert clean_name("Padang,Sumatra's Westkust") == "Padang"

    def test_baros_to_barus(self):
        """Historical spelling 'Baros' should map to 'Barus'."""
        assert clean_name("Baros") == "Barus"

    def test_airbangis_variants(self):
        """Multiple Air Bangis spellings should normalize."""
        assert clean_name("Airbangis") == "Air Bangis"
        assert clean_name("Aijer Bangis") == "Air Bangis"

    def test_djambi_passthrough_after_east_removal(self):
        """rev.11: mapping pelabuhan timur DIHAPUS — 'Djambi' tidak lagi dipetakan."""
        assert clean_name("Djambi") == "Djambi"

    def test_dash_prefix(self):
        """'-,Bengalen' should return 'Bengalen' (second part)."""
        assert clean_name("-,Bengalen") == "Bengalen"

    def test_empty_input(self):
        """Empty string should return empty string."""
        assert clean_name("") == ""
        assert clean_name(None) == ""

    def test_whitespace(self):
        """Whitespace should be stripped."""
        assert clean_name("  Padang  ") == "Padang"

    def test_palembang_comma(self):
        """'Palembang,Palembang' should return 'Palembang'."""
        assert clean_name("Palembang,Palembang") == "Palembang"

    def test_lampung_variants_passthrough_after_east_removal(self):
        """rev.11: mapping pelabuhan timur DIHAPUS — varian Lampung tidak dipetakan."""
        assert clean_name("Lampongs") == "Lampongs"
        assert clean_name("Lampong") == "Lampong"

    def test_unknown_name_passthrough(self):
        """Unknown names should pass through unchanged."""
        assert clean_name("SomeRandomPort") == "SomeRandomPort"


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: classify_direction()
# ═══════════════════════════════════════════════════════════════════════════════

class TestClassifyDirection:
    """Tests for voyage direction classification."""

    def test_outbound_padang_to_batavia(self):
        """Padang → Batavia should be outbound."""
        assert classify_direction("Padang", "Batavia") == "outbound"

    def test_outbound_barus_to_batavia(self):
        """Barus → Batavia should be outbound."""
        assert classify_direction("Barus", "Batavia") == "outbound"

    def test_outbound_air_bangis_to_batavia(self):
        """Air Bangis → Batavia should be outbound."""
        assert classify_direction("Air Bangis", "Batavia") == "outbound"

    def test_outbound_pulau_cingkuak_to_batavia(self):
        """Pulau Cingkuak → Batavia should be outbound."""
        assert classify_direction("Pulau Cingkuak", "Batavia") == "outbound"

    def test_outbound_air_haji_to_batavia(self):
        """Air Haji → Batavia should be outbound."""
        assert classify_direction("Air Haji", "Batavia") == "outbound"

    def test_inbound_batavia_to_padang(self):
        """Batavia → Padang should be inbound."""
        assert classify_direction("Batavia", "Padang") == "inbound"

    def test_inbound_jambi_to_padang(self):
        """Jambi → Padang should be inbound."""
        assert classify_direction("Jambi", "Padang") == "inbound"

    def test_transit_palembang_to_batavia(self):
        """Palembang → Batavia: neither is Westkust → transit."""
        assert classify_direction("Palembang", "Batavia") == "transit"

    def test_transit_jambi_to_batavia(self):
        """Jambi → Batavia: neither is Westkust → transit."""
        assert classify_direction("Jambi", "Batavia") == "transit"

    def test_internal_westkust(self):
        """Padang → Barus: both Westkust → treat as outbound."""
        assert classify_direction("Padang", "Barus") == "outbound"

    def test_unknown_ports(self):
        """Unknown ports at both ends → transit."""
        assert classify_direction("Bengalen", "Malabar") == "transit"

    def test_outbound_to_unknown(self):
        """Westkust port → unknown destination → outbound."""
        assert classify_direction("Padang", "Bengalen") == "outbound"

    def test_unknown_to_westkust(self):
        """Unknown origin → Westkust destination → inbound."""
        assert classify_direction("Bengalen", "Padang") == "inbound"


# ═══════════════════════════════════════════════════════════════════════════════
# Tests: Integration — clean_name + classify_direction pipeline
# ═══════════════════════════════════════════════════════════════════════════════

class TestPipeline:
    """End-to-end tests: raw JSON names → direction classification."""

    def test_raw_padang_to_batavia(self):
        """Raw 'Padang' → 'Batavia,Batavia' should be outbound."""
        origin = clean_name("Padang")
        dest = clean_name("Batavia,Batavia")
        assert classify_direction(origin, dest) == "outbound"

    def test_raw_baros_to_batavia(self):
        """Raw 'Baros' → 'Batavia,Batavia' should be outbound."""
        origin = clean_name("Baros")
        dest = clean_name("Batavia,Batavia")
        assert classify_direction(origin, dest) == "outbound"

    def test_raw_palembang_to_batavia(self):
        """Raw 'Palembang' → 'Batavia,Batavia' should be transit."""
        origin = clean_name("Palembang,Palembang")
        dest = clean_name("Batavia,Batavia")
        assert classify_direction(origin, dest) == "transit"

    def test_raw_padang_to_bengalen(self):
        """'Padang' → '-,Bengalen' should be outbound."""
        origin = clean_name("Padang")
        dest = clean_name("-,Bengalen")
        assert classify_direction(origin, dest) == "outbound"

    def test_raw_djambi_to_batavia(self):
        """'Djambi' → 'Batavia,Batavia' should be transit (Jambi is NOT Westkust)."""
        origin = clean_name("Djambi")
        dest = clean_name("Batavia,Batavia")
        assert classify_direction(origin, dest) == "transit"
