"""
add_atjeh_extra_voyages.py

7 voyage tambahan Atjeh<->Batavia, sudah terdokumentasi di riset
(atjeh_trade_records, lihat data/research/atjeh_trade.csv) tapi belum pernah
dipromosikan ke tabel voyages publik -- keluhan user: "yang masuk dan keluar
sepertinya masih sedikit" (sebelumnya cuma 2: Buijren + jacht Sluys, 0 masuk).

Sumber tiap baris (docs/Dagh-register gehouden int casteel Batavia ...):
  1. gillion (tak bernama) Batavia->Atjeh via Malacca, 7 Mei 1644 [1643-1644 p87]
  2. jacht Grol Batavia->Atjeh, 27 Mei 1644 -- komisaris Vlamingh + oppercoopman
     Jan Harmanssen dikirim mendirikan comptoir Atjeh permanen [1643-1644 p102]
  3. contingh (tak bernama) Atjeh->Batavia, 17 April 1644, kosong (ledigh)
     [1643-1644 p77]
  4-5. schip Swarten Arent, pp Batavia->Atjeh (berangkat 16 Juni 1633,
     cargasoen tak diisi di sumber) & Atjeh->Batavia (tiba 6 Feb 1634, retour
     200 bhaer thin) [1631-1634 p247-248]
  6-7. schip Wassenaer, pp Batavia->Atjeh (tiba di rede Atjeh 29 Sep 1633) &
     Atjeh->Batavia (tiba ~10 Des 1633 via Malacca) [1631-1634 p464-465]

Idempotent: skip per-baris bila (source, origin_id, destination_id, ship_name,
departure_date, arrival_date) yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_extra_voyages.py
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
            "origin_name_raw": "Batavia", "destination_name_raw": "Atchin",
            "ship_name": "gillion (nama tak tercatat)",
            "captain": None,
            "tonnage": None, "year": 1644,
            "departure_date": "1644-05-07", "arrival_date": None,
            "total_gulden": None, "main_product": "Chinese waren",
            "all_products": "1000 realen (nilai) Chinese waren; kapal transit lewat Malacca dulu ('na Malacca ende voort na Atchin').",
            "cargo_count": 1, "destination": "Atchin", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": BATAVIA_FORT_ID, "destination_id": ACEH_FORT_ID,
            "origin_name_raw": "Batavia", "destination_name_raw": "Atchin",
            "ship_name": "jacht Grol",
            "captain": "komisaris Arnout de Vlamingh (mengantar oppercoopman Jan Harmanssen sbg opperhoofd comptoir Atchin baru)",
            "tonnage": None, "year": 1644,
            "departure_date": "1644-05-27", "arrival_date": None,
            "total_gulden": 11183.17, "main_product": None,
            "all_products": "Modal awal comptoir Atchin permanen: guld. 11183.168 (gulden:stuiver:penning, ditulis 11183.17 desimal). Via Malacca; jacht Grol lalu balik lewat Sumatrase Westcust.",
            "cargo_count": 0, "destination": "Atchin", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": ACEH_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Atchin", "destination_name_raw": "Batavia",
            "ship_name": "contingh (nama tak tercatat)",
            "captain": None,
            "tonnage": None, "year": 1644,
            "departure_date": None, "arrival_date": "1644-04-17",
            "total_gulden": None, "main_product": None,
            "all_products": "Kargo KOSONG (ledich) -- kapal hanya singgah mengurus surat jalan (pascedul) ke Grissie/Gresik.",
            "cargo_count": 0, "destination": "Batavia", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": BATAVIA_FORT_ID, "destination_id": ACEH_FORT_ID,
            "origin_name_raw": "Batavia", "destination_name_raw": "Atchijn",
            "ship_name": "Swarten Arent",
            "captain": None,
            "tonnage": None, "year": 1633,
            "departure_date": "1633-06-16", "arrival_date": None,
            "total_gulden": None, "main_product": None,
            "all_products": "Tot procure van peper en vervolch vanden Atchijnsen handel als mede tot bevorderinghe van des coninckx voorgenomen expeditie op Mallacca. Nilai cargasoen TAK diisi di sumber ('f....(1)') -- tak ditebak.",
            "cargo_count": 0, "destination": "Atchijn", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": ACEH_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Atchijn", "destination_name_raw": "Batavia",
            "ship_name": "Swarten Arent",
            "captain": None,
            "tonnage": None, "year": 1634,
            "departure_date": None, "arrival_date": "1634-02-06",
            "total_gulden": None, "main_product": "thin",
            "all_products": "Retour: 200 bhaer thin a 18 taijl (f36720), kain f7177:17:8, tunai Atchijnse munte f20427:17:8. Modal awal terbelanja rendah krn Raja monopoli beli (195 bhaer ijser a 5 taijl + 4 stucken geschut + juwelen, total f55186:10) -- dagang 1633 mengecewakan.",
            "cargo_count": 3, "destination": "Batavia", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": BATAVIA_FORT_ID, "destination_id": ACEH_FORT_ID,
            "origin_name_raw": "Batavia", "destination_name_raw": "Atchijn",
            "ship_name": "Wassenaer",
            "captain": "coopman Gerrit Corsen",
            "tonnage": None, "year": 1633,
            "departure_date": None, "arrival_date": "1633-09-29",
            "total_gulden": None, "main_product": "cleden",
            "all_products": "Tiba di rede Atjeh; Raja beli hampir semua kain dgn margin 75-80% utk VOC. Modal/kargo berangkat tak dirinci angka di sumber yg tersedia.",
            "cargo_count": 1, "destination": "Atchijn", "duration_days": None,
            "direction": "outbound", "source_url": None, "source": "daghregister_batavia",
        },
        {
            "voyage_ref": None,
            "origin_id": ACEH_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Atchijn", "destination_name_raw": "Batavia",
            "ship_name": "Wassenaer",
            "captain": "coopman Gerrit Corsen",
            "tonnage": None, "year": 1633,
            "departure_date": None, "arrival_date": "1633-12-10",
            "total_gulden": None, "main_product": "peper",
            "all_products": "Via Malacca. ~300 bhaer peper blm sepenuhnya diambil saat laporan ditulis; Raja pesan 400-500 bhaer solpher (blm jadi) + 4 kuda Surat + hadiah balasan 8 bhaer peper utk Gouverneur Generael.",
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
