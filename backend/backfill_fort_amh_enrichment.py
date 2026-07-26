"""
backfill_fort_amh_enrichment.py

Isi kolom enrichment AMH (nama_historis, designasi_voc, fungsi_historis) --
Alembic 001 (Sprint ATM US-06) cuma nambah kolomnya, TIDAK pernah mengisi
nilainya lewat script yang bisa diulang. Nilainya sempat terisi manual di 1
DB (dev lokal) tapi tidak pernah tercatat sebagai seed -- ketahuan pas fitur
is_fortified (backend/routers/forts.py) butuh designasi_voc dan production
ternyata NULL semua utk 4 fort ini. Idempotent (UPDATE per nama, aman
dijalankan ulang), sama pola seed_fort_model_metrics.py.

Jalankan: docker compose exec backend python backfill_fort_amh_enrichment.py
"""
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

# Hanya 4 fort yang genuinely berbenteng VOC fisik (garnisun) sudah
# ter-enrich AMH -- Fort York/Marlborough (EIC) msh nunggu enrichment
# terpisah, lihat _KNOWN_FORTIFIED_WITHOUT_AMH di routers/forts.py.
AMH_ENRICHMENT = {
    "Air Bangis": {
        "nama_historis": "Airbangis",
        "designasi_voc": "Sumatras Westcust (VOC-gebied)",
        "fungsi_historis": (
            "Pos dagang VOC di bagian utara Pantai Barat Sumatra. Titik "
            "pengumpulan lada dan hasil hutan dari pedalaman Pasaman "
            "sebelum dikirim ke Padang dan Batavia."
        ),
    },
    "Barus": {
        "nama_historis": "Baros",
        "designasi_voc": "Sumatras Westcust (VOC-gebied)",
        "fungsi_historis": (
            "Pelabuhan kuno bersejarah yang terkenal sejak abad ke-9 "
            "sebagai penghasil kamfer (kapur Barus) berkualitas tinggi. "
            "Pada era VOC menjadi pos pengumpul kamfer dan kemenyan dari "
            "pedalaman Tapanuli."
        ),
    },
    "Padang": {
        "nama_historis": "Padangh",
        "designasi_voc": "Sumatras Westcust (VOC-gebied)",
        "fungsi_historis": (
            "Pusat komando perdagangan Pantai Barat Sumatra. VOC mendirikan "
            "pos dagang dengan fasilitas hospital, gereja, dan mahkamah "
            "kecil untuk melayani pos-pos dagang di sekitarnya. Komoditi "
            "utama: lada, garam, kamfer, dan kemenyan (benzoin) yang "
            "diangkut ke Batavia."
        ),
    },
    "Pulau Cingkuak": {
        "nama_historis": "Pulau Tjinkuk",
        "designasi_voc": "Sumatras Westcust (VOC-gebied)",
        "fungsi_historis": (
            "Pulau kecil di lepas pantai Painan yang berfungsi sebagai "
            "benteng pertahanan dan pos transit VOC. Mengontrol jalur "
            "masuk ke perairan Pantai Barat Sumatra bagian selatan."
        ),
    },
}


def main():
    engine = create_engine(DATABASE_SYNC_URL)
    with Session(engine) as session:
        updated = 0
        for name, fields in AMH_ENRICHMENT.items():
            result = session.execute(
                text(
                    "UPDATE forts SET nama_historis = :nama_historis, "
                    "designasi_voc = :designasi_voc, "
                    "fungsi_historis = :fungsi_historis "
                    "WHERE name = :name"
                ),
                {"name": name, **fields},
            )
            if result.rowcount:
                updated += result.rowcount
            else:
                print(f"  ⚠ Fort '{name}' tidak ditemukan di tabel forts -- dilewati.")
        session.commit()
        print(f"  ✔ AMH enrichment backfill: {updated} fort di-update.")


if __name__ == "__main__":
    main()
