"""
create_aceh_fort.py

Fort Aceh (id=17) sebelumnya dibuat via SQL manual satu-kali (tak pernah
ada script, ketahuan 2026-07-13 saat deploy prod -- production ketinggalan
fort ini sama sekali walau voyage/riset Atjeh sudah live berbulan-bulan).
Script ini gantikan langkah manual itu, idempotent, aman dijalankan di env
manapun (dev atau prod) tanpa duplikasi.

id=17 SENGAJA eksplisit (bukan auto-increment) -- semua script add_atjeh_*.py
hardcode ACEH_FORT_ID=17, jadi id harus sama persis di semua environment.

Jalankan: docker compose exec backend python create_aceh_fort.py
"""
import os

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

ACEH_FORT_ID = 17

DESCRIPTION = (
    "Kesultanan Aceh -- kekuatan politik-dagang independen, bukan comptoir VOC "
    "permanen seperti pos pantai barat lainnya. VOC sempat punya pos dagang sendiri "
    "di Aceh (modal 60.000 real, ~1625) yang ditarik karena takut pembalasan politik. "
    "8 pelayaran terstruktur ditemukan dari narasi Dagh-register (1624-1644). Aceh "
    "berulang kali mengklaim yurisdiksi & penegakan tol atas pantai barat Sumatra "
    "(Tiku, Pariaman, Indrapura), bahkan disebut mencakup \"seluruh pantai timur & "
    "barat Sumatra\" (1625) -- lihat /riset/atjeh-dagang untuk detail & sumber."
)


def main():
    engine = create_engine(DATABASE_SYNC_URL, future=True)
    from models import Fort

    with Session(engine) as session:
        existing = session.execute(
            select(Fort.id).where(Fort.id == ACEH_FORT_ID)
        ).scalar_one_or_none()

        if existing is not None:
            print(f"Fort id={ACEH_FORT_ID} sudah ada -- dilewati (idempotent).")
            return

        session.execute(
            Fort.__table__.insert(),
            [{
                "id": ACEH_FORT_ID,
                "name": "Aceh",
                "latitude": 5.5577,
                "longitude": 95.3222,
                "color": "#8e44ad",
                "description": DESCRIPTION,
                "port_type": "both",
            }],
        )
        # Sinkronkan sequence supaya auto-increment berikutnya tak tabrakan
        # dgn id eksplisit yg baru saja dipakai.
        session.execute(text(
            "SELECT setval('forts_id_seq', GREATEST((SELECT MAX(id) FROM forts), 1), true)"
        ))
        session.commit()
        print(f"Fort Aceh ditambahkan (id={ACEH_FORT_ID}).")

    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:forts")
        print(f"cache forts di-invalidate: {flushed} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
