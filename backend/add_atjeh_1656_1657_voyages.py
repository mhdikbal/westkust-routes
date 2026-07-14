"""
add_atjeh_1656_1657_voyages.py

1 voyage ditemukan saat sisir volume docs/"Dagh-register gehouden int casteel
Batavia ... 1656-1657" (384 hlm.). Volume ini mengungkap PERANG TERBUKA
VOC-Atjeh 1656-57 (6 tahun sebelum pemberontakan Painan 1662-63) -- lihat
data/research/atjeh_trade.csv baris source_document='1656-1657' & halaman
/linimasa utk detail lengkap: komisaris Johan Treuijtman membuka perang, ratu
Atjeh balas perintahkan panglima westcust (Sillida/Ticco/Priaman) tangkap &
siksa semua personel VOC, ekspedisi hukuman van Voorst berhasil bebaskan 9
tawanan di Sillida tapi gagal di Priaman (10 tawanan tetap, ~2000 penjaga).

Sumber:
  jacht de Tortelduijf, Sillida & Priaman -> Batavia, tiba 28 Januari 1657
  [PDF hlm.101, cetak 87]: "comt alhier behouden ter reede 't jacht de
  Tortelduijf van Sumatra's westcust, van Sillidaende Priaman, medebrengende
  den coopman Anthonij van Voorst nevens noch 17 Comp dienaren daer aen landt
  met hem van Voorst gelegen" -- kapal yg membawa kabar pertama ke Batavia
  soal serangan panglima westcust atas perintah ratu Atjeh, mengangkut
  coopman Anthonij van Voorst (nanti memimpin ekspedisi hukuman) + 17
  penyintas.

Idempotent: skip per-baris bila (source, origin_id, destination_id, ship_name,
departure_date, arrival_date) yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_1656_1657_voyages.py
"""
import os

from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

BATAVIA_FORT_ID = 9
SALIDO_FORT_ID = 12


def build_voyage_records():
    return [
        {
            "voyage_ref": None,
            "origin_id": SALIDO_FORT_ID, "destination_id": BATAVIA_FORT_ID,
            "origin_name_raw": "Sillida ende Priaman", "destination_name_raw": "Battavia",
            "ship_name": "jacht de Tortelduijf",
            "captain": None,
            "tonnage": None, "year": 1657,
            "departure_date": None, "arrival_date": "1657-01-28",
            "total_gulden": None, "main_product": None,
            "all_products": (
                "Tak ada kargo dagang tercatat -- kapal ini membawa kabar pertama ke Batavia soal "
                "serangan panglima westcust (Sillida, Ticco, Priaman) atas perintah ratu Atjeh thd "
                "personel VOC (menyusul komisaris Treuijtman membuka perang dgn Atjeh), mengangkut "
                "coopman Anthonij van Voorst + 17 pegawai VOC penyintas. Origin dicatat Salido "
                "(fort_id=12) krn Sillida disebut lebih dulu di sumber 'van Sillidaende Priaman' "
                "(2 pelabuhan, 1 kapal, sama ambiguitas spt voyage volume 1647-1648)."
            ),
            "cargo_count": 0, "destination": "Battavia", "duration_days": None,
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
