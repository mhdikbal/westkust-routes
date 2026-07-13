"""
Unit test for add_atjeh_buijren_voyage.py — ship Buijren, Atjeh -> Batavia,
10 Desember 1632 (docs/Dagh-register ... 1631-1634, PDF hlm. 139 / cetak 128).
Returning legate ship carrying capt. Dirck Statlander back from the King of
Atjeh, 796 bahar pepper. Pure function test — no DB.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_buijren_voyage import build_voyage_record


class TestBuildVoyageRecord:
    def test_fort_ids(self):
        rec = build_voyage_record()
        assert rec["origin_id"] == 17      # Aceh
        assert rec["destination_id"] == 9  # Batavia

    def test_direction_matches_existing_aceh_convention(self):
        rec = build_voyage_record()
        assert rec["direction"] == "outbound"

    def test_source_and_year(self):
        rec = build_voyage_record()
        assert rec["source"] == "daghregister_batavia"
        assert rec["year"] == 1632

    def test_cargo_matches_source_not_fabricated(self):
        """796 bahar peper -- angka dari sumber, bukan tebakan; total_gulden
        TIDAK dikonversi dari format gulden:stuiver:penning (f 69929:6:1) krn
        itu perlu asumsi konversi yg tak eksplisit di sumber."""
        rec = build_voyage_record()
        assert rec["main_product"] == "peper"
        assert "796" in rec["all_products"]
        assert rec["total_gulden"] is None

    def test_captain_notes_legate_context(self):
        rec = build_voyage_record()
        assert "statlander" in (rec["captain"] or "").lower()
