"""
update_aceh_fort_description.py

Fort.description utk Aceh (id=17) ketinggalan zaman -- ditulis sebelum sisir
5 volume Dagh-register (2026-07-13) yang menemukan: VOC SEMPAT punya comptoir
sendiri di Aceh (ditarik krn tensi politik Jambi), dan 8 voyage terstruktur
kini ada di tabel voyages (bukan lagi "cuma narasi, bukan data terstruktur"
spt klaim deskripsi lama). Deskripsi lama jadi salah/menyesatkan begitu
riset lanjut -- teks ini menggantikannya dgn ringkasan terkini.

Idempotent: UPDATE langsung by name, aman dijalankan berulang.

Jalankan: docker compose exec backend python update_aceh_fort_description.py
"""
import os

from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

NEW_DESCRIPTION = (
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
        result = session.execute(
            update(Fort).where(Fort.name == "Aceh").values(description=NEW_DESCRIPTION)
        )
        session.commit()
        print(f"Baris terupdate: {result.rowcount}")

    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:forts")
        print(f"cache forts di-invalidate: {flushed} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
