"""
Seed script — inserts fort metadata and voyage data from JSON into PostgreSQL.
Safe to run multiple times (idempotent via upsert logic).
Includes retry logic so it waits for the DB to be ready.
"""
import json
import os
import sys
import time
from pathlib import Path

from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session

# Sync URL for seeding (psycopg2)
DATABASE_SYNC_URL = os.getenv(
    "DATABASE_SYNC_URL",
    "postgresql://vocuser:vocpassword@localhost:5432/vocdb"
)

# Resolve path to the JSON data file
DATA_FILE = Path(__file__).parent / "data" / "Data_Westkust_Map.json"
if not DATA_FILE.exists():
    DATA_FILE = Path("/app/data/Data_Westkust_Map.json")

FORTS_META = [
    {
        "name": "Padang",
        "latitude": -0.9655545283543475,
        "longitude": 100.35388946846183,
        "color": "#c0392b",
        "description": (
            "Fort de Goede Hoop (Benteng Paulus) di Padang adalah pos perdagangan utama VOC "
            "di pantai barat Sumatera. Didirikan sekitar tahun 1666, benteng ini menjadi pusat "
            "ekspor emas, lada, kamfer, dan benzoin dari pedalaman Minangkabau menuju Batavia. "
            "Selama lebih dari satu abad, Padang merupakan pelabuhan terpenting di sepanjang "
            "Sumatera Westkust dengan ratusan kapal VOC yang berlayar dari sini."
        ),
    },
    {
        "name": "Pulau Cingkuak",
        "latitude": -1.3528370592631371,
        "longitude": 100.5599951812238,
        "color": "#e67e22",
        "description": (
            "Pulau Cingkuak adalah pulau kecil di dekat Painan yang menjadi pos perdagangan lada VOC. "
            "Benteng VOC di Pulau Cingkuak (juga dikenal sebagai Fort van Indrapura) berfungsi "
            "sebagai titik pengumpulan lada dari wilayah Indrapura dan sekitarnya. "
            "Lokasi strategisnya di pesisir barat membuatnya penting dalam jaringan perdagangan "
            "maritime VOC di Sumatera."
        ),
    },
    {
        "name": "Air Haji",
        "latitude": -1.9339388926360865,
        "longitude": 100.86698214155489,
        "color": "#27ae60",
        "description": (
            "Air Haji merupakan pos perdagangan VOC di wilayah selatan Sumatera Barat. "
            "Terletak di kawasan yang kaya hasil hutan dan lada, pos ini berperan sebagai "
            "titik pengumpulan komoditi dari pedalaman Sumatera sebelum dikirim ke Padang "
            "atau langsung ke Batavia. Keberadaan benteng di Air Haji mencerminkan strategi "
            "VOC dalam mengontrol jalur perdagangan di sepanjang pantai barat Sumatera."
        ),
    },
    {
        "name": "Batavia",
        "latitude": -6.116501909271064,
        "longitude": 106.81651216615884,
        "color": "#8e44ad",
        "description": (
            "Batavia (kini Jakarta) adalah pusat kekuasaan dan perdagangan VOC di Asia. "
            "Didirikan pada tahun 1619 di atas reruntuhan kota Jayakarta, Batavia menjadi "
            "ibu kota Hindia Belanda dan tujuan utama kapal-kapal dari Sumatera Westkust. "
            "Emas, lada, kamfer, dan benzoin dari Padang, Pulau Cingkuak, dan Air Haji "
            "dikirim ke Batavia sebelum diperdagangkan ke pasar global. "
            "Kasteel Batavia menjadi simbol kekuatan kolonial VOC di Nusantara."
        ),
    },
]


def wait_for_db(max_retries: int = 30, delay: float = 2.0):
    """Wait until PostgreSQL is accepting connections."""
    from sqlalchemy import create_engine, text as sa_text
    engine = create_engine(DATABASE_SYNC_URL, echo=False)
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(sa_text("SELECT 1"))
            print(f"  ✅ Database ready (attempt {attempt})")
            engine.dispose()
            return
        except Exception as e:
            print(f"  ⏳ Waiting for DB... attempt {attempt}/{max_retries}: {e.__class__.__name__}")
            time.sleep(delay)
    engine.dispose()
    raise RuntimeError("❌ Database not available after max retries. Aborting seed.")


def seed():
    from models import Fort, Voyage, Base

    engine = create_engine(DATABASE_SYNC_URL, echo=False)

    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # ---------- Seed forts ----------
        fort_map: dict[str, Fort] = {}

        for meta in FORTS_META:
            existing = session.execute(
                select(Fort).where(Fort.name == meta["name"])
            ).scalar_one_or_none()

            if existing:
                fort_map[meta["name"]] = existing
                continue

            fort = Fort(
                name=meta["name"],
                latitude=meta["latitude"],
                longitude=meta["longitude"],
                color=meta["color"],
                description=meta["description"],
            )
            session.add(fort)
            session.flush()
            fort_map[meta["name"]] = fort
            print(f"  ✔ Fort added: {meta['name']}")

        session.commit()

        # Re-fetch fort_map after commit
        for meta in FORTS_META:
            fort_map[meta["name"]] = session.execute(
                select(Fort).where(Fort.name == meta["name"])
            ).scalar_one()

        # ---------- Seed voyages ----------
        existing_count = session.execute(
            text("SELECT COUNT(*) FROM voyages")
        ).scalar()

        if existing_count and existing_count > 0:
            print(f"  ℹ️  Voyages already seeded ({existing_count} records). Skipping.")
            return

        if not DATA_FILE.exists():
            print(f"  ⚠️  Data file not found: {DATA_FILE}")
            return

        with open(DATA_FILE, encoding="utf-8") as f:
            records = json.load(f)

        added = 0
        skipped = 0
        for rec in records:
            origin = rec.get("Asal", "").strip()
            fort = fort_map.get(origin)
            if not fort:
                skipped += 1
                continue

            voyage = Voyage(
                fort_id=fort.id,
                ship_name=rec.get("Nama_Kapal", "Unknown"),
                captain=rec.get("Kapten") or None,
                year=rec.get("Tahun"),
                total_gulden=rec.get("Total_Gulden_NL"),
                main_product=rec.get("Produk_Utama"),
                all_products=rec.get("Semua_Produk"),
                destination=rec.get("Tujuan"),
                duration_days=rec.get("Durasi_Hari"),
                source_url=rec.get("URL"),
            )
            session.add(voyage)
            added += 1

        session.commit()
        print(f"  ✔ Voyages seeded: {added} added, {skipped} skipped (unknown origin)")


if __name__ == "__main__":
    print("🌱 Waiting for database...")
    wait_for_db()
    print("🌱 Seeding database...")
    seed()
    print("✅ Done!")

