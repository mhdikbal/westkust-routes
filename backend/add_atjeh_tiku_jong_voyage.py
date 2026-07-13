"""
add_atjeh_tiku_jong_voyage.py

Menambahkan SATU baris voyage Aceh->Tiku -- bukti PALING LEMAH dari semua
voyage Atjeh yg sudah ditambahkan sejauh ini, dimasukkan atas persetujuan
eksplisit user meski caveat-nya berat (docs/Dagh-register ... 1631-1634,
PDF hlm. 121 / cetak 110, entri "31 OCTOBER - 4 NOVEMBER" 1633):

  "Zeeckere Aetchijnse jonck geladen met wel 400 bhaaren peper lach in
  Ticouw gereet om met t'eerste van het Wester mouson herrewaerts aen te
  coomen. D° jonck expresselijck van den Coninck van Aetchijn aen den
  Generael met een gesant haffgeveerdicht; wat zyne commissie zij, zal den
  tijt leeren."

Sumber TIDAK menyebut tanggal berangkat dari Aceh maupun tanggal tiba pasti
di Tiku -- hanya bahwa jong itu "lach in Ticouw" (sedang berada di sana)
pada tanggal kronik Batavia mencatatnya. departure_date/arrival_date SENGAJA
None; caveat eksplisit di all_products.

Idempotent: skip bila baris (source, origin_id, destination_id, ship_name,
year) yg sama sudah ada.

Jalankan: docker compose exec backend python add_atjeh_tiku_jong_voyage.py
"""
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

ACEH_FORT_ID = 17
TIKU_FORT_ID = 10


def build_voyage_record():
    return {
        "voyage_ref": None,
        "origin_id": ACEH_FORT_ID,
        "destination_id": TIKU_FORT_ID,
        "origin_name_raw": "Atchijn",
        "destination_name_raw": "Ticouw",
        "ship_name": "jonck (nama tak tercatat)",
        "captain": "gesant Raja Atjeh (nama tak tercatat, dikirim Coninck van Aetchijn ke Gouverneur Generael)",
        "tonnage": None,
        "year": 1633,
        "departure_date": None,   # TAK diketahui -- sumber tak sebut tanggal berangkat dari Aceh
        "arrival_date": None,     # TAK diketahui -- sumber tak sebut tanggal tiba pasti di Tiku
        "total_gulden": None,
        "main_product": "peper",
        "all_products": (
            "400 bhaer peper. CAVEAT: bukti PALING LEMAH di antara voyage Atjeh -- "
            "sumber cuma catat jong 'lach in Ticouw' (sedang berada di sana) pada "
            "entri kronik 31 Okt-4 Nov 1633, BELUM ada tanggal berangkat dari Aceh "
            "maupun tanggal tiba pasti di Tiku yg dikonfirmasi. Kepergian onward ke "
            "Batavia masih RENCANA ('gereet om herrewaerts aen te coomen'), belum tentu terjadi."
        ),
        "cargo_count": 1,
        "destination": "Ticouw",
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
                Voyage.ship_name == rec["ship_name"],
                Voyage.year == rec["year"],
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
                Voyage.ship_name == rec["ship_name"],
                Voyage.year == rec["year"],
            )
        ).scalar_one()

    print(f"Voyage baru ditambahkan: id={new_id} (Atjeh -> Tiku, 1633, jonck tak bernama, CAVEAT bukti lemah)")

    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:voyages")
        print(f"cache voyages di-invalidate: {flushed} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
