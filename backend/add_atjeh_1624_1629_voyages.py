"""
add_atjeh_1624_1629_voyages.py

2 voyage ditemukan sisir volume docs/"Dagh_register_gehouden_int_casteel_
Batavia-1624-1629" (434 hlm., Google Books scan) -- volume PALING AWAL yg
sudah disisir sejauh ini, mendokumentasikan periode konflik Atjeh-Jambi
(Sultan Iskandar Muda) & dagang pepper VOC di Atjeh sebelum titah 1633.

  1. Batavia->Atchyn, 6 April 1624 [PDF hlm.55, cetak 42]: "vertreckt van
     hier naer Atchyn tot bevorderinge van den peperhandel aldaer t schip
     Wapen van Hoorn met een cargasoen van cleeden als andersints
     monterende f 71046.4.6."

  2. Atchin->Batavia, 23 Februari 1627 [PDF hlm.315, cetak 302]: "arriveert
     alhier van Atchin t'schip Haerlem inhebbende 802 bh' peper."

Tahun dipin via header "DACHREGISTER vant geene hier in Battavia t'sedert
Pmo January [tahun] gepasseert is" -- pdf hlm.14=1624, 134=1625, 236=1626,
312=1627 (offset cetak-ke-pdf = 13, konsisten dgn volume lain).

Idempotent: skip per-baris bila (source, origin_id, destination_id, ship_name,
departure_date, arrival_date) yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_1624_1629_voyages.py
"""
import os

from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

ACEH_FORT_ID = 17
BATAVIA_FORT_ID = 9


def build_voyage_records():
    return [
        {
            "voyage_ref": None,
            "origin_id": BATAVIA_FORT_ID, "destination_id": ACEH_FORT_ID,
            "origin_name_raw": "Batavia", "destination_name_raw": "Atchyn",
            "ship_name": "schip Wapen van Hoorn",
            "captain": None,
            "tonnage": None, "year": 1624,
            "departure_date": "1624-04-06", "arrival_date": None,
            "total_gulden": 71046.4, "main_product": None,
            "all_products": (
                "Cargasoen van cleeden als andersints (kain & lainnya), \"tot bevorderinge "
                "van den peperhandel aldaer\" -- modal awal utk dagang pepper di Atjeh, "
                "bukan retour peper. Volume paling awal yg disisir (1624-1629), 9 tahun "
                "sebelum titah pembatasan dagang 1633."
            ),
            "cargo_count": 1, "destination": "Atchyn", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": ACEH_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Atchin", "destination_name_raw": "Batavia",
            "ship_name": "schip Haerlem",
            "captain": None,
            "tonnage": None, "year": 1627,
            "departure_date": None, "arrival_date": "1627-02-23",
            "total_gulden": None, "main_product": "peper",
            "all_products": "802 bhaar peper.",
            "cargo_count": 1, "destination": "Batavia", "duration_days": None,
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
