"""
Unit test for create_aceh_fort.py — fort Aceh (id=17) sebelumnya dibuat
manual via SQL, ketahuan hilang total di production saat deploy 2026-07-13.

Pure content test -- no DB.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from create_aceh_fort import ACEH_FORT_ID, DESCRIPTION


class TestAcehFortConstants:
    def test_fort_id_matches_voyage_scripts(self):
        """Semua add_atjeh_*.py hardcode ACEH_FORT_ID=17 -- harus konsisten,
        beda id berarti voyage lama nyasar ke fort yg salah."""
        assert ACEH_FORT_ID == 17

    def test_description_not_empty(self):
        assert len(DESCRIPTION) > 50

    def test_description_mentions_comptoir_and_structured_voyages(self):
        """Regresi 2026-07-13: deskripsi lama bilang 'tidak pernah jadi comptoir
        VOC' & 'bukan data terstruktur' -- SALAH setelah sisir 5 volume. Versi
        baru harus menyebut comptoir 1625 & jumlah voyage terstruktur."""
        assert "comptoir" in DESCRIPTION.lower()
        assert "terstruktur" in DESCRIPTION.lower()
