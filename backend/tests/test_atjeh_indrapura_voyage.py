"""
Unit test for add_atjeh_indrapura_voyage.py — the single hand-verified voyage
leg connecting Atjeh to the Sumatra Westkust atlas (p33, Dagh-register 1643-1644:
empty galleon from Indrapura belonging to the Atjeh ambassador, arrived
Batavia 22 Jan 1644). Pure function test — no DB.

GOTCHA 2026-07-13: fort id Inderapura BEDA antar environment (16 di dev,
15 di production, dibuat manual tanpa script di masing2 -- drift diam2).
build_voyage_record() sekarang terima inderapura_fort_id sbg parameter
(diresolve via nama saat runtime di main()), bukan hardcode -- test pakai
angka arbitrer utk buktikan fungsinya cuma nerusin nilai, bukan hardcode ulang.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_indrapura_voyage import build_voyage_record

TEST_INDERAPURA_ID = 999  # angka arbitrer -- buktikan fungsi terusin parameter, bukan hardcode


class TestBuildVoyageRecord:
    def test_fort_ids(self):
        rec = build_voyage_record(TEST_INDERAPURA_ID)
        assert rec["origin_id"] == TEST_INDERAPURA_ID
        assert rec["destination_id"] == 9   # Batavia

    def test_direction_matches_existing_aceh_convention(self):
        """Konsisten dgn 1 voyage Aceh->Batavia yg sudah ada (source=daghregister_batavia):
        'outbound' = menuju Batavia, terlepas dari klasifikasi SUMATRA_WESTKUST_PORTS
        (Inderapura tak masuk set itu di seed_data.py, tapi konvensi baris tangan
        utk daghregister_batavia sumbernya beda dari pipeline bgb_huygens)."""
        rec = build_voyage_record(TEST_INDERAPURA_ID)
        assert rec["direction"] == "outbound"

    def test_source_and_year(self):
        rec = build_voyage_record(TEST_INDERAPURA_ID)
        assert rec["source"] == "daghregister_batavia"
        assert rec["year"] == 1644

    def test_empty_cargo_no_fabricated_product(self):
        """Kargo tercatat 'ledigh' (kosong) di sumber -- main_product HARUS None,
        bukan ditebak/di-null-safe-default jadi string kosong."""
        rec = build_voyage_record(TEST_INDERAPURA_ID)
        assert rec["main_product"] is None

    def test_notes_flag_aceh_ambassador_ownership(self):
        """Provenance wajib jelas: ini BUKAN rute niaga Atjeh->Inderapura yg
        terdokumentasi, tapi kapal MILIK duta besar Atjeh yg tiba dari Inderapura."""
        rec = build_voyage_record(TEST_INDERAPURA_ID)
        assert "duta" in (rec["captain"] or "").lower() or "duta" in (rec["all_products"] or "").lower()

    def test_ship_name_not_fabricated(self):
        """Sumber tak menyebut nama kapal ('een gilioen') -- ship_name harus
        mengaku tak diketahui, bukan nama karangan."""
        rec = build_voyage_record(TEST_INDERAPURA_ID)
        assert "tak" in rec["ship_name"].lower() or "onbekend" in rec["ship_name"].lower()
