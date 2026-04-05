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
    # ── Westkust Sumatra Ports ─────────────────────────────
    {
        "name": "Barus",
        "latitude":  2.0144566458864355,
        "longitude": 98.39931988670789,
        "color": "#16a085",
        "port_type": "departure",
        "description": "Barus (Fansur) adalah pelabuhan historis kamfer dan benzoin.",
    },
    {
        "name": "Air Bangis",
        "latitude":  0.1974875340994538,
        "longitude": 99.37555542252645,
        "color": "#2980b9",
        "port_type": "departure",
        "description": "Air Bangis adalah pos pengumpulan hasil bumi di wilayah Pasaman.",
    },
    {
        "name": "Padang",
        "latitude": -0.9655545283543475,
        "longitude": 100.35388946846183,
        "color": "#c0392b",
        "port_type": "both",
        "description": "Fort de Goede Hoop di Padang adalah pusat administrasi VOC di Westkust.",
    },
    {
        "name": "Pulau Cingkuak",
        "latitude": -1.3528370592631371,
        "longitude": 100.5599951812238,
        "color": "#e67e22",
        "port_type": "departure",
        "description": "Pulau Cingkuak adalah pos perdagangan lada utama dekat Painan.",
    },
    {
        "name": "Air Haji",
        "latitude": -1.9339388926360865,
        "longitude": 100.86698214155489,
        "color": "#27ae60",
        "port_type": "departure",
        "description": "Air Haji merupakan pos perdagangan VOC di wilayah selatan Sumatera Barat.",
    },
    # ── Destination Center ──────────────────────────────────────────────
    {
        "name": "Batavia",
        "latitude": -6.116501909271064,
        "longitude": 106.81651216615884,
        "color": "#2c3e50",
        "port_type": "arrival",
        "description": "Batavia adalah pusat kekuasaan dan perdagangan VOC di Asia.",
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

    with Session(engine) as session:
        # ---------- Seed forts ----------
        fort_map: dict[str, Fort] = {}

        for meta in FORTS_META:
            existing = session.execute(
                select(Fort).where(Fort.name == meta["name"])
            ).scalar_one_or_none()

            if existing:
                existing.port_type = meta["port_type"]
                existing.color = meta["color"]
                fort_map[meta["name"]] = existing
                continue

            fort = Fort(
                name=meta["name"],
                latitude=meta["latitude"],
                longitude=meta["longitude"],
                color=meta["color"],
                description=meta["description"],
                port_type=meta["port_type"],
            )
            session.add(fort)
            session.flush()
            fort_map[meta["name"]] = fort
            print(f"  ✔ Fort added: {meta['name']}")

        session.commit()

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

            # Check directional logic
            direction = None
            if origin_name in sumatra_ports:
                direction = "outbound"
            elif dest_name in sumatra_ports:
                direction = "inbound"

            # We only seed if at least one port is recognized in our system
            if not origin_fort and not dest_fort:
                skipped += 1
                continue

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

