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
DATA_FILE = Path(__file__).parent.parent / "scrawling" / "Data_BGS_Sumatra_Full.json"
if not DATA_FILE.exists():
    DATA_FILE = Path("/app/scrawling/Data_BGS_Sumatra_Full.json")

FORTS_META = [
    # ── Departure ports (west coast Sumatra) ─────────────────────────────
    {
        "name": "Barus",
        "latitude":  2.0144566458864355,
        "longitude": 98.39931988670789,
        "color": "#16a085",
        "port_type": "departure",
        "description": (
            "Barus (Fansur/Baros) adalah salah satu pelabuhan tertua di Nusantara, "
            "terkenal sejak abad ke-7 sebagai penghasil kamfer (kapur barus) berkualitas "
            "tinggi yang diperdagangkan hingga ke Arab dan Cina. Pada era VOC, Barus "
            "menjadi pos pengumpulan kamfer dan benzoin dari pedalaman Sumatera Barat "
            "bagian utara sebelum dikirim ke Padang atau langsung ke Batavia."
        ),
    },
    {
        "name": "Air Bangis",
        "latitude":  0.1974875340994538,
        "longitude": 99.37555542252645,
        "color": "#2980b9",
        "port_type": "departure",
        "description": (
            "Air Bangis (Airbangis) adalah pelabuhan kecil di pantai barat Sumatera, "
            "terletak di antara Padang dan Barus. Pada masa VOC, Air Bangis berfungsi "
            "sebagai pos pengumpulan hasil bumi dari wilayah Pasaman dan sekitarnya, "
            "terutama kamfer, lada, dan hasil hutan. Kapal-kapal VOC singgah di sini "
            "dalam perjalanan antara Padang dan Barus."
        ),
    },
    {
        "name": "Padang",
        "latitude": -0.9655545283543475,
        "longitude": 100.35388946846183,
        "color": "#c0392b",
        "port_type": "both",
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
        "port_type": "departure",
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
        "port_type": "departure",
        "description": (
            "Air Haji merupakan pos perdagangan VOC di wilayah selatan Sumatera Barat. "
            "Terletak di kawasan yang kaya hasil hutan dan lada, pos ini berperan sebagai "
            "titik pengumpulan komoditi dari pedalaman Sumatera sebelum dikirim ke Padang "
            "atau langsung ke Batavia. Keberadaan benteng di Air Haji mencerminkan strategi "
            "VOC dalam mengontrol jalur perdagangan di sepanjang pantai barat Sumatera."
        ),
    },
    # ── Arrival / both ports ──────────────────────────────────────────────
    {
        "name": "Jambi",
        "latitude": -1.0984482519567516,
        "longitude": 104.1757178771618,
        "color": "#d35400",
        "port_type": "arrival",
        "description": (
            "Jambi adalah Kesultanan dan pelabuhan di pantai timur Sumatera. "
            "Kota ini merupakan penghasil utama lada hitam dan benzoin yang diperdagangkan "
            "melalui Selat Malaka dan Selat Bangka menuju Batavia. "
            "VOC memiliki loji (kantor dagang) di Jambi sejak abad ke-17."
        ),
    },
    {
        "name": "Palembang",
        "latitude": -3.002911966341772,
        "longitude": 104.78018903090859,
        "color": "#8e44ad",
        "port_type": "arrival",
        "description": (
            "Palembang adalah ibukota Kesultanan Palembang, salah satu pusat perdagangan "
            "terpenting di Sumatera Selatan. Kota ini menghasilkan lada, timah, damar, "
            "dan benjuang. VOC memiliki perjanjian dagang dengan Kesultanan Palembang "
            "dan kapal-kapalnya secara rutin singgah di Palembang dalam perjalanan "
            "antara Sumatera dan Batavia."
        ),
    },
    {
        "name": "Lampung",
        "latitude": -5.357800466943823,
        "longitude": 105.28038662236222,
        "color": "#7f8c8d",
        "port_type": "arrival",
        "description": (
            "Lampung (Lampong Toulang Bawang) adalah wilayah di ujung selatan Sumatera "
            "yang terkenal sebagai penghasil lada terbaik. Terletak dekat Selat Sunda, "
            "kapal-kapal VOC singgah di Lampung sebelum atau sesudah melewati Selat Sunda "
            "menuju Batavia. VOC bersaing keras dengan pedagang lokal dan Banten "
            "untuk menguasai perdagangan lada Lampung."
        ),
    },
    {
        "name": "Batavia",
        "latitude": -6.116501909271064,
        "longitude": 106.81651216615884,
        "color": "#2c3e50",
        "port_type": "arrival",
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

    # Ensure PostGIS and Schema
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    
    Base.metadata.create_all(engine)

    # Handle migration: add port_type column if it doesn't exist
    with engine.begin() as conn:
        try:
            conn.execute(text(
                "ALTER TABLE forts ADD COLUMN IF NOT EXISTS port_type VARCHAR(20) "
                "NOT NULL DEFAULT 'departure'"
            ))
        except Exception:
            pass  # Column already exists

    with Session(engine) as session:
        # ---------- Seed forts ----------
        fort_map: dict[str, Fort] = {}

        for meta in FORTS_META:
            existing = session.execute(
                select(Fort).where(Fort.name == meta["name"])
            ).scalar_one_or_none()

            if existing:
                # Update port_type if it changed
                existing.port_type = meta.get("port_type", "departure")
                existing.color     = meta.get("color", existing.color)
                fort_map[meta["name"]] = existing
                continue

            fort = Fort(
                name=meta["name"],
                latitude=meta["latitude"],
                longitude=meta["longitude"],
                color=meta["color"],
                description=meta["description"],
                port_type=meta.get("port_type", "departure"),
            )
            session.add(fort)
            session.flush()
            fort_map[meta["name"]] = fort
            print(f"  ✔ Fort added: {meta['name']} ({meta.get('port_type','departure')})")

        session.commit()


        # Re-fetch fort_map after commit
        for meta in FORTS_META:
            fort_map[meta["name"]] = session.execute(
                select(Fort).where(Fort.name == meta["name"])
            ).scalar_one()


        # ---------- Seed voyages ----------
        # Logic: Clean start for voyages to ensure directionality logic is applied correctly
        session.execute(text("TRUNCATE TABLE voyages RESTART IDENTITY"))
        
        if not DATA_FILE.exists():
            print(f"  ⚠️  Data file not found: {DATA_FILE}")
            return

        with open(DATA_FILE, encoding="utf-8") as f:
            records = json.load(f)

        added = 0
        skipped = 0
        
        # Ports that define our "Sumatra Westkust" region
        sumatra_ports = {"Barus", "Air Bangis", "Padang", "Pulau Cingkuak", "Air Haji"}

        for rec in records:
            origin_name = rec.get("Asal", "").strip()
            dest_name = rec.get("Tujuan", "").strip()

            origin_fort = fort_map.get(origin_name)
            dest_fort = fort_map.get(dest_name)

            # Skip if we don't have AT LEAST one Sumatra fort in the loop
            if not origin_fort and not dest_fort:
                skipped += 1
                continue

            # Check directional logic
            direction = None
            if origin_name in sumatra_ports:
                direction = "outbound"
            elif dest_name in sumatra_ports:
                direction = "inbound"

            voyage = Voyage(
                origin_id=origin_fort.id if origin_fort else None,
                destination_id=dest_fort.id if dest_fort else None,
                origin_name_raw=origin_name,
                destination_name_raw=dest_name,
                ship_name=rec.get("Nama_Kapal", "Unknown"),
                captain=rec.get("Kapten") or None,
                year=rec.get("Tahun"),
                total_gulden=rec.get("Total_Gulden_NL"),
                main_product=rec.get("Produk_Utama"),
                all_products=rec.get("Semua_Produk"),
                destination=dest_name, # Use cleaned dest_name
                duration_days=rec.get("Durasi_Hari"),
                direction=direction,
                source_url=rec.get("URL"),
            )
            session.add(voyage)
            added += 1

        session.commit()
        print(f"  ✔ Voyages seeded: {added} added (with direction logic), {skipped} skipped.")


if __name__ == "__main__":
    print("🌱 Waiting for database...")
    wait_for_db()
    print("🌱 Seeding database...")
    seed()
    print("✅ Done!")

