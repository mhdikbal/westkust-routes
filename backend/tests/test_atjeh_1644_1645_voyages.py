"""
Unit test for add_atjeh_1644_1645_voyages.py — 2 voyage ditemukan sisir volume
docs/Dagh-register ... 1644-1645 (schip Maestricht Indrapoura->Batavia 5 Sep
1645 PDF hlm.63/cetak47; jacht Aquersloot Atchijn->Batavia via Westcust 26 Okt
1645 PDF hlm.66/cetak50).

Pure function test -- no DB.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_1644_1645_voyages import build_voyage_records


class TestBuildVoyageRecords:
    def test_two_records(self):
        recs = build_voyage_records()
        assert len(recs) == 2

    def test_maestricht_leg(self):
        recs = build_voyage_records()
        maestricht = recs[0]
        assert maestricht["origin_id"] == 16   # Inderapura
        assert maestricht["destination_id"] == 9  # Batavia
        assert maestricht["arrival_date"] == "1645-09-05"
        assert maestricht["departure_date"] is None
        assert maestricht["year"] == 1645
        assert maestricht["ship_name"] == "schip Maestricht"

    def test_aquersloot_leg(self):
        recs = build_voyage_records()
        aquersloot = recs[1]
        assert aquersloot["origin_id"] == 17   # Aceh
        assert aquersloot["destination_id"] == 9  # Batavia
        assert aquersloot["arrival_date"] == "1645-10-26"
        assert aquersloot["departure_date"] is None
        assert aquersloot["year"] == 1645

    def test_westcust_route_noted(self):
        """Rute pulang Atchijn->Batavia eksplisit lewat pantai barat, bukan
        Malacca -- fakta ini harus tercatat, bukan didiamkan."""
        recs = build_voyage_records()
        assert "westcust" in recs[1]["all_products"].lower()

    def test_both_use_daghregister_source(self):
        recs = build_voyage_records()
        for r in recs:
            assert r["source"] == "daghregister_batavia"

    def test_no_cargo_claimed(self):
        """Tak ada kargo dagang tercatat di sumber utk kedua voyage -- jangan
        mengarang main_product/total_gulden yg tak ada bukti."""
        recs = build_voyage_records()
        for r in recs:
            assert r["main_product"] is None
            assert r["total_gulden"] is None
            assert r["cargo_count"] == 0
