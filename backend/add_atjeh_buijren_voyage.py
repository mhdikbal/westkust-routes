"""
add_atjeh_buijren_voyage.py

Menambahkan SATU baris voyage nyata: schip Buijren, Atjeh -> Batavia,
10 Desember 1632 (docs/Dagh-register ... 1631-1634, PDF hlm. 139 / cetak 128).
Kapal ini membawa pulang kapten Dirck Statlander, yang dikirim sbg legaet
(utusan) ke Raja Atjeh, dengan 796 bahar peper.

total_gulden SENGAJA None: sumber mencatat "f 69929:6:1" (gulden:stuiver:
penning), bukan desimal -- konversi 1 gulden=20 stuiver=16 penning tak
eksplisit dilakukan sumber, jadi nilai asli disimpan sbg teks di all_products
saja drpd menebak pembulatan.

Idempotent: skip bila baris (source, origin_id, destination_id, year, ship_name)
yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_buijren_voyage.py
"""
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

ACEH_FORT_ID = 17
BATAVIA_FORT_ID = 9


def build_voyage_record():
    return {
        "voyage_ref": None,
        "origin_id": ACEH_FORT_ID,
        "destination_id": BATAVIA_FORT_ID,
        "origin_name_raw": "Atchijn",
        "destination_name_raw": "Batavia",
        "ship_name": "Buijren",
        "captain": "kapt. Dirck Statlander (kembali dari misi legaet ke Coninck van Atchijn)",
        "tonnage": None,
        "year": 1632,
        "departure_date": None,
        "arrival_date": "1632-12-10",
        "total_gulden": None,
        "main_product": "peper",
        "all_products": "796 bhaaren peper, costende als per factuijre f 69929:6:1 (gulden:stuiver:penning, tak dikonversi desimal).",
        "cargo_count": 1,
        "destination": "Batavia",
        "duration_days": None,
        "direction": "outbound",
        "source_url": None,
        "source": "daghregister_batavia",
    }


def main():
    rec = build_voyage_record()

    engine = create_engine(DATABASE_SYNC_URL, future=True)
    from models import Voyage

    with Session(engine) as session:
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

    print(f"Voyage baru ditambahkan: id={new_id} (Atjeh -> Batavia, 1632, schip Buijren)")

    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:voyages")
        print(f"cache voyages di-invalidate: {flushed} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
