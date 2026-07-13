"""
Unit test for add_atjeh_vanderstel_1637_voyages.py — 2 voyage vrijburger
Adriaen vander Stel, Batavia<->Atchijn, 1637 (docs/Dagh-register ... 1637,
PDF hlm.173/cetak160 outbound & PDF hlm.56/cetak43 inbound).

Pure function test -- no DB.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_vanderstel_1637_voyages import build_voyage_records


class TestBuildVoyageRecords:
    def test_two_records(self):
        recs = build_voyage_records()
        assert len(recs) == 2

    def test_outbound_leg(self):
        recs = build_voyage_records()
        outbound = recs[0]
        assert outbound["origin_id"] == 9    # Batavia
        assert outbound["destination_id"] == 17  # Aceh
        assert outbound["departure_date"] == "1637-04-29"
        assert outbound["arrival_date"] is None
        assert outbound["year"] == 1637

    def test_inbound_leg(self):
        recs = build_voyage_records()
        inbound = recs[1]
        assert inbound["origin_id"] == 17   # Aceh
        assert inbound["destination_id"] == 9  # Batavia
        assert inbound["arrival_date"] == "1637-05-23"
        assert inbound["departure_date"] is None
        assert inbound["year"] == 1637

    def test_ship_name_caveat_present(self):
        """OCR ambigu apakah 'Sluijmer ende den Leeuw' satu kapal atau dua --
        caveat harus eksplisit di all_products, bukan didiamkan."""
        recs = build_voyage_records()
        assert "ambigu" in recs[0]["all_products"].lower()

    def test_both_use_daghregister_source(self):
        recs = build_voyage_records()
        for r in recs:
            assert r["source"] == "daghregister_batavia"

    def test_different_ship_on_return_leg_noted(self):
        """Kapal keberangkatan (jacht) beda dgn kapal kepulangan (opgeboijde
        boot) -- fakta ini harus tercatat, bukan disamakan begitu saja."""
        recs = build_voyage_records()
        assert "jacht" in recs[0]["ship_name"].lower()
        assert "boot" in recs[1]["ship_name"].lower()
        assert recs[0]["ship_name"] != recs[1]["ship_name"]
