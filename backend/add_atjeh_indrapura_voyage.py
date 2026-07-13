"""
add_atjeh_indrapura_voyage.py

Menambahkan SATU baris voyage yang benar-benar terdokumentasi sbg pergerakan
kapal (bukan cuma disebut-sebut) yang menghubungkan Atjeh ke atlas Sumatra
Westkust: PDF hal. 33 (docs/Dagh-register ... 1643-1644), 22 Januari 1644 --
galleon KOSONG dari Indrapura, MILIK duta besar Atjeh, tiba di Batavia.

SENGAJA bukan "Atjeh -> Inderapura" -- sumber tidak mendokumentasikan pelayaran
kaki itu, hanya kapal tsb berlayar Indrapura -> Batavia. Kepemilikan oleh duta
Atjeh dicatat di kolom captain/all_products, BUKAN diperlakukan sbg rute
Atjeh->Inderapura yg tak ada buktinya (lihat project_atjeh_trade_1643_1644.md
soal Barus/Tiku/Pariaman -- bukti terlalu tipis utk digambar sbg rute).

Idempotent: skip bila baris dgn (source, origin_id, destination_id, year,
ship_name) yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_indrapura_voyage.py
"""
import os
from datetime import datetime, timezone

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

BATAVIA_FORT_ID = 9
# GOTCHA 2026-07-13: id fort Inderapura TERNYATA beda antar environment (16 di
# dev, 15 di production -- dibuat manual di masing2 tanpa script, drift diam2).
# Resolve via nama saat runtime, bukan hardcode, spy tak patah lagi di env baru.


def build_voyage_record(inderapura_fort_id):
    return {
        "voyage_ref": None,
        "origin_id": inderapura_fort_id,
        "destination_id": BATAVIA_FORT_ID,
        "origin_name_raw": "Indrapoura",
        "destination_name_raw": "Batavia",
        "ship_name": "gilioen (nama tak tercatat)",
        "captain": "milik ambassadeur van Atchin (duta besar Atjeh, nama tak tercatat)",
        "tonnage": None,
        "year": 1644,
        "departure_date": None,
        "arrival_date": "1644-01-22",
        "total_gulden": None,
        "main_product": None,
        "all_products": "Kargo kosong ('ledigh') -- kapal duta besar Atjeh singgah Batavia dlm perjalanan dari Indrapura.",
        "cargo_count": 0,
        "destination": "Batavia",
        "duration_days": None,
        "direction": "outbound",
        "source_url": None,
        "source": "daghregister_batavia",
    }


def main():
    engine = create_engine(DATABASE_SYNC_URL, future=True)
    from models import Fort, Voyage

    with Session(engine) as session:
        inderapura_fort_id = session.execute(
            select(Fort.id).where(Fort.name == "Inderapura")
        ).scalar_one()

        rec = build_voyage_record(inderapura_fort_id)

        existing = session.execute(
            select(Voyage.id).where(
                Voyage.source == rec["source"],
                Voyage.origin_id == rec["origin_id"],
                Voyage.destination_id == rec["destination_id"],
                Voyage.year == rec["year"],
                Voyage.ship_name == rec["ship_name"],
            )
        ).scalar_one_or_none()

        if existing is not None:
            print(f"Sudah ada (voyage id={existing}) -- dilewati (idempotent).")
            return

        session.execute(Voyage.__table__.insert(), [rec])
        session.commit()
        new_id = session.execute(
            select(Voyage.id).where(
                Voyage.source == rec["source"],
                Voyage.origin_id == rec["origin_id"],
                Voyage.destination_id == rec["destination_id"],
                Voyage.year == rec["year"],
                Voyage.ship_name == rec["ship_name"],
            )
        ).scalar_one()

    print(f"Voyage baru ditambahkan: id={new_id} (Inderapura -> Batavia, 1644)")

    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:voyages")
        print(f"cache voyages di-invalidate: {flushed} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
