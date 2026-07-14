"""
Unit test for add_atjeh_1656_1657_voyages.py — 1 voyage ditemukan sisir volume
docs/Dagh-register ... 1656-1657 (jacht de Tortelduijf, Sillida/Priaman ->
Batavia, 28 Jan 1657 -- kabar pertama perang terbuka VOC-Atjeh sampai Batavia).

Pure function test -- no DB.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_1656_1657_voyages import build_voyage_records


class TestBuildVoyageRecords:
    def test_one_record(self):
        recs = build_voyage_records()
        assert len(recs) == 1

    def test_tortelduijf_leg(self):
        recs = build_voyage_records()
        r = recs[0]
        assert r["origin_id"] == 12   # Salido
        assert r["destination_id"] == 9   # Batavia
        assert r["arrival_date"] == "1657-01-28"
        assert r["departure_date"] is None
        assert r["year"] == 1657
        assert r["ship_name"] == "jacht de Tortelduijf"

    def test_no_cargo_claimed(self):
        """War/news voyage, bukan dagang -- jangan mengarang kargo."""
        recs = build_voyage_records()
        r = recs[0]
        assert r["main_product"] is None
        assert r["cargo_count"] == 0

    def test_uses_daghregister_source(self):
        recs = build_voyage_records()
        assert recs[0]["source"] == "daghregister_batavia"
