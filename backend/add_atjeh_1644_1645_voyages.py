"""
add_atjeh_1644_1645_voyages.py

2 voyage ditemukan saat sisir volume docs/"Dagh-register gehouden int casteel
Batavia ... 1644-1645" (404 hlm.) -- sesi ini isinya "Verbael Atjeh 1644-1645"
(PDF hlm.55-70, cetak 39-54) yg dedicated soal comptoir Atjeh, jauh lebih padat
dari volume2 sebelumnya. Lihat data/research/atjeh_trade.csv baris
source_document='1644-1645' utk 7 fakta politik/dagang terkait (termasuk temuan
kunci: transposisi pos dagang Indrapoura->Sillida/Cillida = Salido modern,
DITOLAK ratu Atjeh 2x).

Sumber:
  1. Outbound (arah data project, walau secara harfiah kapal DATANG ke Batavia),
     schip Maestricht, Indrapoura->Batavia, tiba 5 September 1645 [PDF hlm.63,
     cetak 47]: "Adij 5 September 1645 met de verschijningh van 't schip
     Maestricht van Indrapoura, becomen d'heeren Raden van India een missive
     van den oppercoopman Jan Hermansen uijt Atchin, geschreven 25 Februarij
     verleden" -- kapal ini mengangkut surat dari comptoir Atjeh (ditulis di
     Atjeh, dibawa fisik lewat Indrapoura), bukan kargo dagang tercatat.

  2. jacht Aquersloot, Atchijn->Batavia lewat rute pantai barat, tiba 26 Oktober
     1645 [PDF hlm.66, cetak 50]: "Adij 26 October verschijnt 't jacht
     Aquersloot met den oppercoopman Jan Hermansen over de Westcust, waermede
     becomen copiebrieff dato 12 April ... mitsgaders een missive van den
     commissaris Arnold de Vlamingh, getekent 12en Augustij" -- oppercoopman
     Jan Hermansen (kepala comptoir Atjeh) kembali ke Batavia via jalur pantai
     barat secara eksplisit ("over de Westcust"), bukan lewat Malacca spt rute
     komisaris Vlamingh di kapal lain. Konfirmasi primer rute kembali
     Atjeh->Batavia menyusuri pantai barat, bukan cuma rekonstruksi peta.

Idempotent: skip per-baris bila (source, origin_id, destination_id, ship_name,
departure_date, arrival_date) yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_1644_1645_voyages.py
"""
import os

from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

ACEH_FORT_ID = 17
BATAVIA_FORT_ID = 9
INDERAPURA_FORT_ID = 16


def build_voyage_records():
    return [
        {
            "voyage_ref": None,
            "origin_id": INDERAPURA_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Indrapoura", "destination_name_raw": "Batavia",
            "ship_name": "schip Maestricht",
            "captain": None,
            "tonnage": None, "year": 1645,
            "departure_date": None, "arrival_date": "1645-09-05",
            "total_gulden": None, "main_product": None,
            "all_products": (
                "Tak ada kargo dagang tercatat di sumber -- kapal ini mengangkut missive "
                "(surat) dari oppercoopman Jan Hermansen (kepala comptoir VOC di Atchijn) "
                "tertanggal 25 Februari 1645, dibawa fisik lewat Indrapoura ke Raden van "
                "India di Batavia."
            ),
            "cargo_count": 0, "destination": "Batavia", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": ACEH_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Atchijn", "destination_name_raw": "Batavia",
            "ship_name": "jacht Aquersloot (oppercoopman Jan Hermansen)",
            "captain": None,
            "tonnage": None, "year": 1645,
            "departure_date": None, "arrival_date": "1645-10-26",
            "total_gulden": None, "main_product": None,
            "all_products": (
                "Tak ada kargo dagang tercatat -- kapal mengangkut oppercoopman Jan "
                "Hermansen (kepala comptoir Atchijn) kembali ke Batavia, mitsgaders copie "
                "brief (12 April) & missive commissaris Arnold de Vlamingh (12 Augustus). "
                "Rute PULANG dari Atchijn eksplisit disebut 'over de Westcust' (menyusuri "
                "pantai barat Sumatra) -- bukan lewat Malacca spt rute komisaris Vlamingh "
                "di kapal terpisah."
            ),
            "cargo_count": 0, "destination": "Batavia", "duration_days": None,
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
