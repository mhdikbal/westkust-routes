"""
Unit tests for seed_data.py logic functions.
Tests clean_name() and classify_direction() independently of the database.

These are pure function tests — no DB, no async, no mocking needed.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from seed_data import clean_name, classify_direction


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

    def test_djambi_to_jambi(self):
        """Dutch spelling 'Djambi' should map to 'Jambi'."""
        assert clean_name("Djambi") == "Jambi"

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

    def test_lampung_variants(self):
        """Lampung spelling variants."""
        assert clean_name("Lampongs") == "Lampung"
        assert clean_name("Lampong") == "Lampung"

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
