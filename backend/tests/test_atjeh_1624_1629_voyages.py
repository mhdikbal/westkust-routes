"""
Unit test for add_atjeh_1624_1629_voyages.py — schip Wapen van Hoorn
(Batavia->Atchyn, 6 Apr 1624) & schip Haerlem (Atchin->Batavia, 23 Feb 1627),
docs/Dagh_register...1624-1629, PDF hlm.55/cetak42 & PDF hlm.315/cetak302.

Pure function test -- no DB.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_1624_1629_voyages import build_voyage_records


class TestBuildVoyageRecords:
    def test_two_records(self):
        recs = build_voyage_records()
        assert len(recs) == 2

    def test_wapen_van_hoorn_outbound_leg(self):
        recs = build_voyage_records()
        wvh = recs[0]
        assert wvh["origin_id"] == 9    # Batavia
        assert wvh["destination_id"] == 17  # Aceh
        assert wvh["departure_date"] == "1624-04-06"
        assert wvh["year"] == 1624
        assert wvh["total_gulden"] == 71046.4

    def test_haerlem_inbound_leg(self):
        recs = build_voyage_records()
        haerlem = recs[1]
        assert haerlem["origin_id"] == 17   # Aceh
        assert haerlem["destination_id"] == 9  # Batavia
        assert haerlem["arrival_date"] == "1627-02-23"
        assert haerlem["year"] == 1627
        assert "802" in haerlem["all_products"]

    def test_this_is_earliest_volume_so_far(self):
        """1624 harus jadi tahun tertua di antara semua voyage Atjeh yg
        sudah dipromosikan (sebelumnya paling awal 1632, schip Buijren)."""
        recs = build_voyage_records()
        assert min(r["year"] for r in recs) == 1624

    def test_both_use_daghregister_source(self):
        recs = build_voyage_records()
        for r in recs:
            assert r["source"] == "daghregister_batavia"
