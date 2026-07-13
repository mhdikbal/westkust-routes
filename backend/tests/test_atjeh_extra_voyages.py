"""
Unit tests for add_atjeh_extra_voyages.py — 7 tambahan voyage Atjeh<->Batavia
yang sudah terdokumentasi di riset (atjeh_trade_records) tapi belum pernah
dipromosikan ke tabel voyages publik. Tujuan: /atlas hanya punya 2 voyage
Atjeh (Buijren + jacht Sluys) meski sumber punya lebih banyak pergerakan
kapal nyata -- keluhan user "yang masuk dan keluar masih sedikit".

Setiap entri HARUS punya jejak sumber jelas (tanggal + halaman + kutipan
konteks di notes/all_products) -- tak ada tanggal/kargo karangan utk baris
yg sumbernya blank (mis. cargasoen Swarten Arent keberangkatan tak diisi
angkanya di sumber -- main_product/total_gulden tetap None).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_extra_voyages import build_voyage_records

ACEH_FORT_ID = 17
BATAVIA_FORT_ID = 9


class TestBuildVoyageRecords:
    def test_returns_seven_records(self):
        recs = build_voyage_records()
        assert len(recs) == 7

    def test_all_touch_aceh_and_batavia_only(self):
        for r in build_voyage_records():
            ids = {r["origin_id"], r["destination_id"]}
            assert ids == {ACEH_FORT_ID, BATAVIA_FORT_ID}

    def test_all_source_daghregister_batavia(self):
        for r in build_voyage_records():
            assert r["source"] == "daghregister_batavia"

    def test_masuk_and_keluar_both_represented(self):
        """masuk Aceh (destination=Aceh) dan keluar Aceh (origin=Aceh) dua-duanya
        harus ada -- keluhan user: sebelumnya cuma 'keluar', 0 'masuk'."""
        recs = build_voyage_records()
        masuk = [r for r in recs if r["destination_id"] == ACEH_FORT_ID]
        keluar = [r for r in recs if r["origin_id"] == ACEH_FORT_ID]
        assert len(masuk) >= 3
        assert len(keluar) >= 3

    def test_no_fabricated_cargo_for_blank_source(self):
        """Swarten Arent keberangkatan (16 Juni 1633): sumber cargasoen 'f....(1)'
        (blank, tak diisi penulis asli) -- main_product/total_gulden HARUS None,
        bukan ditebak dari cargo retour-nya."""
        recs = build_voyage_records()
        outbound = next(r for r in recs if r["ship_name"] == "Swarten Arent" and r["destination_id"] == ACEH_FORT_ID)
        assert outbound["main_product"] is None
        assert outbound["total_gulden"] is None

    def test_ship_names_not_fabricated_for_unnamed_vessels(self):
        """gillion (p87) & contingh (p77) tak disebut namanya di sumber --
        ship_name harus mengaku tak diketahui, bukan nama karangan."""
        recs = build_voyage_records()
        unnamed = [r for r in recs if "tak tercatat" in r["ship_name"].lower() or "onbekend" in r["ship_name"].lower()]
        assert len(unnamed) >= 2

    def test_every_record_has_dated_leg(self):
        """Tiap baris wajib py departure_date ATAU arrival_date -- jangan
        keduanya None (tak ada jejak waktu sama sekali)."""
        for r in build_voyage_records():
            assert r["departure_date"] or r["arrival_date"], f"{r['ship_name']} tanpa tanggal sama sekali"
