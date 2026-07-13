"""
add_atjeh_1636_voyages.py

2 voyage ditemukan sisir volume docs/"Dagh-register gehouden int Casteel
Batavia ... 1636" (328 hlm.):

  1. Indrapoura->Batavia, 12 Oktober 1636 [PDF hlm.264, cetak 251]: "arriveert
     vande Sumatrase Westcust volladen met 928 bhaar Indrapurasepeper,
     tjacht Sardam medebrengende neffens 14 packen ongetrocken cleeden een
     missive vanden coopman Jacob Schooff uit Indrapura, gedateert 24
     September passado" -- jacht Sardam, pepper eksplisit disebut "Indrapurase"
     (dari Indrapura), plus surat coopman VOC Jacob Schooff yg berkedudukan
     DI Indrapura (bukti comptoir/pos dagang VOC sendiri ada di sana).

  2. Atchijn->Batavia, 21 Desember 1636 [PDF hlm.309, cetak 296]: "arriveert
     hier vande Sumatrase Westcust van Atchijn weder op rheede t schip de
     Revengie met den oppercoopman Jacob Compostel, medebrengende 314 bhaar,
     50 cattij peper, ende 4 bhaar wegens den coninck tot vereeringh aenden
     Generael. Item 40 bhaar, 197 cattij peras tin, 32 bhaar, 22 cattij
     solpher, 100 buffelshuijden, 225 doshoorns, ende twee cattij gout" --
     total f 36216.12; 2 hari kemudian (23 Des) hadiah raja diarak ke darat
     dgn kehormatan militer (3 tembakan musket, 3 tembakan meriam).

Idempotent: skip per-baris bila (source, origin_id, destination_id, ship_name,
departure_date, arrival_date) yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_1636_voyages.py
"""
import os

from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

ACEH_FORT_ID = 17
BATAVIA_FORT_ID = 9
INDRAPURA_FORT_ID = 16


def build_voyage_records():
    return [
        {
            "voyage_ref": None,
            "origin_id": INDRAPURA_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Indrapoura", "destination_name_raw": "Batavia",
            "ship_name": "jacht Sardam",
            "captain": None,
            "tonnage": None, "year": 1636,
            "departure_date": None, "arrival_date": "1636-10-12",
            "total_gulden": None, "main_product": "peper",
            "all_products": (
                "928 bhaar Indrapurase peper, 14 packen ongetrocken cleeden. Membawa surat "
                "coopman VOC Jacob Schooff (berkedudukan di Indrapura, tertanggal 24 September "
                "1636) yg mengeluhkan pejabat pungut-tol Raja Atjeh masih menghambat dagang "
                "cleeden-tegen-peper di sana."
            ),
            "cargo_count": 2, "destination": "Batavia", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": ACEH_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Atchijn", "destination_name_raw": "Batavia",
            "ship_name": "schip de Revengie",
            "captain": "oppercoopman Jacob Compostel",
            "tonnage": None, "year": 1636,
            "departure_date": None, "arrival_date": "1636-12-21",
            "total_gulden": 36216.12, "main_product": "peper",
            "all_products": (
                "314 bhaar + 50 cattij peper, ditambah 4 bhaar peper KHUSUS hadiah Raja Atjeh "
                "utk Gouverneur Generael. 40 bhaar 197 cattij peras tin, 32 bhaar 22 cattij "
                "solpher, 100 buffelshuijden, 225 doshoorns, 2 cattij gout. Total f 36216.12. "
                "2 hari kemudian (23 Des) hadiah raja diarak ke darat dgn kehormatan militer "
                "(3 tembakan musket, 3 tembakan meriam)."
            ),
            "cargo_count": 6, "destination": "Batavia", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
    ]


def main():
    records = build_voyage_records()

    engine = create_engine(DATABASE_SYNC_URL, future=True)
    from models import Voyage

    added, skipped = 0, 0
    with Session(engine) as session:
        for rec in records:
            existing = session.execute(
                select(Voyage.id).where(and_(
                    Voyage.source == rec["source"],
                    Voyage.origin_id == rec["origin_id"],
                    Voyage.destination_id == rec["destination_id"],
                    Voyage.ship_name == rec["ship_name"],
                    Voyage.departure_date.is_(rec["departure_date"]) if rec["departure_date"] is None
                        else Voyage.departure_date == rec["departure_date"],
                    Voyage.arrival_date.is_(rec["arrival_date"]) if rec["arrival_date"] is None
                        else Voyage.arrival_date == rec["arrival_date"],
                ))
            ).scalar_one_or_none()

            if existing is not None:
                print(f"Sudah ada (id={existing}): {rec['ship_name']} {rec['origin_name_raw']}->{rec['destination_name_raw']} -- dilewati")
                skipped += 1
                continue

            session.execute(Voyage.__table__.insert(), [rec])
            added += 1
            print(f"Ditambahkan: {rec['ship_name']} {rec['origin_name_raw']}->{rec['destination_name_raw']} ({rec['departure_date'] or rec['arrival_date']})")

        session.commit()

    print("=" * 60)
    print(f"{added} baris baru, {skipped} dilewati (idempotent)")
    print("=" * 60)

    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:voyages")
        print(f"cache voyages di-invalidate: {flushed} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
