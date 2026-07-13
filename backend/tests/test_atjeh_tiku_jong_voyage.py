"""
Unit test for add_atjeh_tiku_jong_voyage.py — jong Atjeh diamati di Tiku,
dikirim Raja Atjeh dgn utusan, 400 bhaer peper (docs/Dagh-register ...
1631-1634, PDF hlm. 121 / cetak 110, entri "31 OCTOBER - 4 NOVEMBER" 1633).

Baris ini SENGAJA bukti-lemah dibanding voyage Aceh<->Batavia lain: sumber
tak menyebut tanggal berangkat dari Aceh maupun tanggal tiba pasti di Tiku,
cuma "lach in Ticouw" (sedang berada di Tiku) pada tanggal catatan kronik.
User eksplisit setuju tetap ditambahkan dgn caveat tegas drpd didiamkan.
Pure function test -- no DB.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from add_atjeh_tiku_jong_voyage import build_voyage_record


class TestBuildVoyageRecord:
    def test_fort_ids(self):
        rec = build_voyage_record()
        assert rec["origin_id"] == 17   # Aceh
        assert rec["destination_id"] == 10  # Tiku

    def test_no_fabricated_dates(self):
        """Sumber tak menyebut tanggal berangkat/tiba pasti -- HARUS None,
        bukan diisi tanggal observasi kronik (31 Okt-4 Nov) sbg tanggal tiba
        yg seolah pasti."""
        rec = build_voyage_record()
        assert rec["departure_date"] is None
        assert rec["arrival_date"] is None

    def test_year_still_set_for_filtering(self):
        rec = build_voyage_record()
        assert rec["year"] == 1633

    def test_ship_name_not_fabricated(self):
        rec = build_voyage_record()
        assert "tak tercatat" in rec["ship_name"].lower()

    def test_caveat_present_in_notes(self):
        """Catatan wajib bilang eksplisit ini blm dikonfirmasi berangkat/tiba,
        bukan cuma diam soal itu."""
        rec = build_voyage_record()
        notes = (rec["all_products"] or "").lower()
        assert "belum" in notes or "tak" in notes or "rencana" in notes

    def test_main_product_matches_source_quantity(self):
        rec = build_voyage_record()
        assert rec["main_product"] == "peper"
        assert "400" in rec["all_products"]
