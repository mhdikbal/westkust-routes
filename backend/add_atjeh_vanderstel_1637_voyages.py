"""
add_atjeh_vanderstel_1637_voyages.py

2 voyage vrijburger (free merchant) Adriaen vander Stel, Batavia<->Atchijn,
1637 -- ditemukan saat sisir volume docs/"Dagh-register gehouden int casteel
Batavia ... 1637" (331 hlm.) utk menjawab pertanyaan user soal pelayaran
Aceh-pantai barat.

Sumber:
  1. Outbound, 28-29 April 1637 [PDF hlm.173, cetak 160]: "vertrecktvan hier
     onder behoorlijckecomissij den vrijcoopman Adrijaenvander Stel met sijn
     jacht den Sluijmerenden Leeuw naerAtchieenende voortsnaerBengalaende
     Aracquan met omtrent8000 p. grofen fijnposteleijn, 500 p. boeckspiegels,
     eenighe sijdestoffen ende andre cleijnicheeden meer" -- OCR ambigu
     apakah "Sluijmer ende den Leeuw" nama SATU kapal (majemuk) atau DUA
     kapal terpisah; dicatat literal sesuai sumber, caveat di all_products.
     Tujuan akhir voyage ini Bengala/Arakan, Atchijn cuma singgah -- dicatat
     tetap sbg leg Batavia->Atchijn krn itu yg relevan westkust/thesis.

  2. Inbound, 23 Mei 1637 [PDF hlm.56, cetak 43]: "Den vrijburgerAdriaenvander
     Stelwas den 23enMaij passadomet zijn opgeboijdebootvan Atchijnaldaer
     aengecomen mede brenghendeomtrent7 a8 barenpeper hem van dien coninck
     (soo bijseijde) vereert, partijesolpher, tin en sandelhout" -- kembali
     dgn kapal BERBEDA ("opgeboijde boot", bukan jacht) drpd keberangkatan;
     kargo hadiah pribadi dari Raja Atjeh, bukan kargo dagang comptoir biasa.

Idempotent: skip per-baris bila (source, origin_id, destination_id, ship_name,
departure_date, arrival_date) yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_vanderstel_1637_voyages.py
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
            "origin_name_raw": "Batavia", "destination_name_raw": "Atchieen",
            "ship_name": "jacht Sluijmer ende den Leeuw (vrijcoopman Adrijaen vander Stel)",
            "captain": "vrijcoopman Adrijaen vander Stel",
            "tonnage": None, "year": 1637,
            "departure_date": "1637-04-29", "arrival_date": None,
            "total_gulden": None, "main_product": "porceleijn",
            "all_products": (
                "8000 p. grof en fijn posteleijn, 500 p. boeckspiegels, eenighe sijdestoffen "
                "ende andre cleijnicheeden. CAVEAT: OCR ambigu apakah 'Sluijmer ende den Leeuw' "
                "nama SATU kapal majemuk atau DUA kapal terpisah -- dicatat literal sesuai "
                "sumber. Tujuan akhir voyage ini Bengala & Aracquan (Atchijn cuma transit), "
                "dicatat sbg leg Batavia->Atchijn krn itu yg relevan westkust."
            ),
            "cargo_count": 3, "destination": "Atchieen", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": ACEH_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Atchijn", "destination_name_raw": "Batavia",
            "ship_name": "opgeboijde boot (vrijburger Adriaen vander Stel)",
            "captain": "vrijburger Adriaen vander Stel",
            "tonnage": None, "year": 1637,
            "departure_date": None, "arrival_date": "1637-05-23",
            "total_gulden": None, "main_product": "peper",
            "all_products": (
                "7 a 8 baren peper (hadiah pribadi dari Raja Atjeh, kata vander Stel), "
                "partije solpher, tin en sandelhout. Kembali dgn kapal BERBEDA drpd "
                "keberangkatan (opgeboijde boot, bukan jacht Sluijmer ende den Leeuw) -- "
                "kemungkinan berpindah kapal di Atchijn atau kargo pribadi terpisah dari "
                "misi comptoir. Pada tanggal sama, kapal terpisah milik pedagang Moor "
                "Mangelis juga tiba dari Atchijn dgn ~90 bhaaren peper (tidak dicatat "
                "sbg voyage terpisah di sini)."
            ),
            "cargo_count": 3, "destination": "Batavia", "duration_days": None,
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
