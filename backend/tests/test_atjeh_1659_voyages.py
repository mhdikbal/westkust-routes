"""
Unit test for add_atjeh_1659_voyages.py — 2 voyage ditemukan sisir volume
docs/Dagh-register ... 1659 (jacht de Cabeljauw membawa duta perdamaian
Atjeh ke Batavia 24 Mei 1659; jacht Weesp mengantar pulang 29 Juli 1659,
mengakhiri perang VOC-Atjeh 1656-57).

Pure function test -- no DB.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_1659_voyages import build_voyage_records


class TestBuildVoyageRecords:
    def test_two_records(self):
        recs = build_voyage_records()
        assert len(recs) == 2

    def test_cabeljauw_leg(self):
        recs = build_voyage_records()
        r = recs[0]
        assert r["origin_id"] == 17   # Aceh
        assert r["destination_id"] == 9   # Batavia
        assert r["arrival_date"] == "1659-05-24"
        assert r["ship_name"] == "jacht de Cabeljauw"

    def test_weesp_leg(self):
        recs = build_voyage_records()
        r = recs[1]
        assert r["origin_id"] == 9   # Batavia
        assert r["destination_id"] == 17   # Aceh
        assert r["departure_date"] == "1659-07-29"
        assert r["ship_name"] == "jacht Weesp"

    def test_no_cargo_claimed(self):
        """Voyage diplomatik, bukan dagang -- jangan mengarang kargo."""
        recs = build_voyage_records()
        for r in recs:
            assert r["main_product"] is None
            assert r["cargo_count"] == 0

    def test_uses_daghregister_source(self):
        recs = build_voyage_records()
        for r in recs:
            assert r["source"] == "daghregister_batavia"
