"""
add_atjeh_1659_voyages.py

2 voyage ditemukan saat sisir volume docs/"Dagh-register gehouden int casteel
Batavia ... 1659" (288 hlm.). Volume ini melanjutkan cerita perang VOC-Atjeh
1656-57 (lihat data/research/atjeh_trade.csv source_document='1656-1657') --
Maret 1659 perang masih berjalan (6 tawanan Belanda, panglima pantai barat
terbelah), lalu 26 Mei 1659 perdamaian resmi tercapai lewat kedutaan ratu
Atjeh yg diterima penuh upacara di Batavia.

Sumber:
  1. jacht de Cabeljauw, dari "de Aetchinsebesettinge" (via Malacca) ke
     Batavia, tiba 24 Mei 1659 [PDF hlm.110-111, cetak 102-103]: membawa 2
     duta Atjeh + surat perdamaian ratu, plus singgah Malacca ambil 1643
     picol peper (kargo Malacca, bukan Atjeh).

  2. jacht Weesp (berlayar bersama jacht de Cabeljauw), Batavia -> Atchijn
     (via Malacca), berangkat 28-29 Juli 1659 [PDF hlm.159, cetak 151]:
     mengantar pulang 2 duta Atjeh sehabis ~2 bulan di Batavia.

Idempotent: skip per-baris bila (source, origin_id, destination_id, ship_name,
departure_date, arrival_date) yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_1659_voyages.py
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
            "origin_id": ACEH_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Aetchinsebesettinge (via Malacca)", "destination_name_raw": "Battavia",
            "ship_name": "jacht de Cabeljauw",
            "captain": None,
            "tonnage": None, "year": 1659,
            "departure_date": None, "arrival_date": "1659-05-24",
            "total_gulden": None, "main_product": None,
            "all_products": (
                "Tak ada kargo dagang Atjeh tercatat -- kapal ini membawa 2 duta Atjeh (Siry Bidsy Indra "
                "& Oupaduta Tchittra Siry Nara Wangsa) beserta surat perdamaian resmi ratu Atjeh, "
                "mengakhiri perang VOC-Atjeh 1656-57. Singgah Malacca mengambil 1643 picol peper (kargo "
                "comptoir Malacca, bukan dari Atjeh, tak dihitung sbg produk voyage ini)."
            ),
            "cargo_count": 0, "destination": "Battavia", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": BATAVIA_FORT_ID, "destination_id": ACEH_FORT_ID,
            "origin_name_raw": "Battavia", "destination_name_raw": "Atchijn (via Malacca)",
            "ship_name": "jacht Weesp",
            "captain": None,
            "tonnage": None, "year": 1659,
            "departure_date": "1659-07-29", "arrival_date": None,
            "total_gulden": None, "main_product": None,
            "all_products": (
                "Tak ada kargo dagang tercatat -- mengantar pulang 2 duta Atjeh sehabis ~2 bulan di "
                "Batavia, berlayar berkompi dgn jacht de Cabeljauw."
            ),
            "cargo_count": 0, "destination": "Atchijn", "duration_days": None,
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
