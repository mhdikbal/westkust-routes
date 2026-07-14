"""
Unit test for add_atjeh_1647_1648_voyages.py — 7 voyage ditemukan sisir volume
docs/Dagh-register ... 1647-1648 (jacht de Zeerobbe Batavia->Atchijn; fluijt de
Noortstarre & schip Wesel Batavia<->Salida/Indrapoura Jul-Aug 1648, pulang
kosong krn sengketa harga; fluijtschip de Wolff & fluijt den Swarten Beer dari
Ticco/Priaman->Batavia).

Pure function test -- no DB.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_1647_1648_voyages import build_voyage_records


class TestBuildVoyageRecords:
    def test_seven_records(self):
        recs = build_voyage_records()
        assert len(recs) == 7

    def test_zeerobbe_leg(self):
        recs = build_voyage_records()
        z = recs[0]
        assert z["origin_id"] == 9    # Batavia
        assert z["destination_id"] == 17  # Aceh
        assert z["departure_date"] == "1648-04-28"
        assert z["year"] == 1648

    def test_noortstarre_roundtrip(self):
        recs = build_voyage_records()
        out, back = recs[1], recs[2]
        assert out["origin_id"] == 9 and out["destination_id"] == 12   # Batavia -> Salido
        assert back["origin_id"] == 12 and back["destination_id"] == 9  # Salido -> Batavia
        assert out["ship_name"] == back["ship_name"] == "fluijt de Noortstarre"
        assert out["departure_date"] == "1648-07-03"
        assert back["arrival_date"] == "1648-08-09"

    def test_wesel_roundtrip(self):
        recs = build_voyage_records()
        out, back = recs[3], recs[4]
        assert out["origin_id"] == 9 and out["destination_id"] == 16   # Batavia -> Inderapura
        assert back["origin_id"] == 16 and back["destination_id"] == 9  # Inderapura -> Batavia
        assert out["ship_name"] == back["ship_name"] == "schip Wesel"

    def test_empty_handed_return_legs_no_cargo(self):
        """Noortstarre & Wesel pulang TANPA peper krn sengketa harga -- jangan
        mengarang main_product/cargo_count yg tak ada bukti."""
        recs = build_voyage_records()
        for r in (recs[2], recs[4]):
            assert r["main_product"] is None
            assert r["cargo_count"] == 0

    def test_wolff_and_swarten_beer_from_tiku(self):
        recs = build_voyage_records()
        wolff, swarten_beer = recs[5], recs[6]
        assert wolff["origin_id"] == 10   # Tiku
        assert wolff["destination_id"] == 9
        assert wolff["main_product"] == "peper"
        assert swarten_beer["origin_id"] == 10
        assert swarten_beer["captain"] == "coopman Hendrick Craijer"

    def test_ambiguous_tiku_priaman_origin_noted(self):
        """Sumber sebut 'Ticco ende Priaman' bersamaan utk satu kapal -- caveat
        ambiguitas harus eksplisit di all_products, bukan didiamkan."""
        recs = build_voyage_records()
        assert "ambigu" in recs[5]["all_products"].lower()
        assert "ambigu" in recs[6]["all_products"].lower()

    def test_all_use_daghregister_source(self):
        recs = build_voyage_records()
        for r in recs:
            assert r["source"] == "daghregister_batavia"
