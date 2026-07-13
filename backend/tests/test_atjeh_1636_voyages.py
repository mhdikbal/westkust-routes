"""
Unit test for add_atjeh_1636_voyages.py — jacht Sardam (Indrapoura->Batavia,
12 Okt 1636) & schip de Revengie (Atchijn->Batavia, 21 Des 1636), docs/
Dagh-register ... 1636, PDF hlm.264/cetak251 & PDF hlm.309/cetak296.

Pure function test -- no DB.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_1636_voyages import build_voyage_records


class TestBuildVoyageRecords:
    def test_two_records(self):
        recs = build_voyage_records()
        assert len(recs) == 2

    def test_sardam_indrapura_leg(self):
        recs = build_voyage_records()
        sardam = recs[0]
        assert sardam["origin_id"] == 16   # Indrapura
        assert sardam["destination_id"] == 9  # Batavia
        assert sardam["arrival_date"] == "1636-10-12"
        assert sardam["ship_name"] == "jacht Sardam"
        assert "Indrapura" in sardam["all_products"]

    def test_revengie_aceh_leg(self):
        recs = build_voyage_records()
        revengie = recs[1]
        assert revengie["origin_id"] == 17   # Aceh
        assert revengie["destination_id"] == 9  # Batavia
        assert revengie["arrival_date"] == "1636-12-21"
        assert revengie["total_gulden"] == 36216.12

    def test_royal_gift_noted(self):
        """4 bhaar peper khusus hadiah raja HARUS tercatat terpisah dari
        kargo dagang biasa, bukan digabung diam-diam."""
        recs = build_voyage_records()
        assert "hadiah" in recs[1]["all_products"].lower()

    def test_both_use_daghregister_source(self):
        recs = build_voyage_records()
        for r in recs:
            assert r["source"] == "daghregister_batavia"
            assert r["year"] == 1636
