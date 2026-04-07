"""
Seed script — inserts fort metadata and voyage data from JSON into PostgreSQL.
Safe to run multiple times (idempotent via upsert logic).
Includes robust name cleaning for fuzzy JSON matches.
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
        "latitude":  2.0144566,
        "longitude": 98.3993198,
        "color": "#16a085",
        "port_type": "departure",
        "description": "Barus (Baros) adalah salah satu pelabuhan tertua di Nusantara, terkenal sebagai penghasil kamfer berkualitas tinggi."
    },
    {
        "name": "Air Bangis",
        "latitude":  0.1974875,
        "longitude": 99.3755554,
        "color": "#2980b9",
        "port_type": "departure",
        "description": "Air Bangis berfungsi sebagai pos pengumpulan hasil bumi terutama lada dan hasil hutan."
    },
    {
        "name": "Padang",
        "latitude": -0.9655545,
        "longitude": 100.3538894,
        "color": "#c0392b",
        "port_type": "both",
        "description": "Fort de Goede Hoop di Padang adalah pusat ekspor emas dan lada utama VOC di Sumatera Westkust."
    },
    {
        "name": "Pulau Cingkuak",
        "latitude": -1.3528370,
        "longitude": 100.5599951,
        "color": "#e67e22",
        "port_type": "departure",
        "description": "Pulau Cingkuak (Fort van Indrapura) adalah pos perdagangan lada vital di pesisir selatan."
    },
    {
        "name": "Air Haji",
        "latitude": -1.9339388,
        "longitude": 100.8669821,
        "color": "#27ae60",
        "port_type": "departure",
        "description": "Pos perdagangan VOC di wilayah selatan yang mengumpulkan lada dan hasil hutan."
    },
    # ── Arrival ports ─────────────────────────────────────────────────────
    {
        "name": "Jambi",
        "latitude": -1.0984482,
        "longitude": 104.1757178,
        "color": "#d35400",
        "port_type": "arrival",
        "description": "Kesultanan Jambi merupakan penghasil lada hitam dan benzoin."
    },
    {
        "name": "Palembang",
        "latitude": -3.0029119,
        "longitude": 104.7801890,
        "color": "#8e44ad",
        "port_type": "arrival",
        "description": "Pusat perdagangan timah dan lada di Sumatera Selatan."
    },
    {
        "name": "Lampung",
        "latitude": -5.3578004,
        "longitude": 105.2803866,
        "color": "#7f8c8d",
        "port_type": "arrival",
        "description": "Wilayah penghasil lada terbaik yang strategis dekat Selat Sunda."
    },
    {
        "name": "Batavia",
        "latitude": -6.1165019,
        "longitude": 106.8165121,
        "color": "#2c3e50",
        "port_type": "arrival",
        "description": "Pusat kekuasaan VOC di Asia; tujuan utama kapal-kapal dari Sumatera Westkust."
    },
]

def clean_name(raw_name: str) -> str:
    """Cleans names like 'Batavia,Batavia' or 'Baros' to match FORTS_META."""
    if not raw_name: return ""
    # Split by comma and take first part: "Padang,Sumatra's Westkust" -> "Padang"
    name = raw_name.split(',')[0].strip()
    
    # Manual Spell Mapping
    mapping = {
        "Baros":     "Barus",
        "Airbangis": "Air Bangis",
        "Aijer Bangis": "Air Bangis",
        "Djambi":    "Jambi",
    }
    return mapping.get(name, name)

def wait_for_db(max_retries: int = 30, delay: float = 2.0):
    engine = create_engine(DATABASE_SYNC_URL, echo=False)
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"  ✅ Database ready (attempt {attempt})")
            engine.dispose()
            return
        except Exception as e:
            print(f"  ⏳ Waiting for DB... attempt {attempt}/{max_retries}")
            time.sleep(delay)
    engine.dispose()
    raise RuntimeError("❌ Database not available.")

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
            existing = session.execute(select(Fort).where(Fort.name == meta["name"])).scalar_one_or_none()
            if existing:
                existing.port_type = meta["port_type"]
                existing.color = meta["color"]
                fort_map[meta["name"]] = existing
            else:
                f = Fort(**meta)
                session.add(f)
                session.flush()
                fort_map[meta["name"]] = f
        session.commit()

        # ---------- Seed voyages ----------
        session.execute(text("TRUNCATE TABLE voyages RESTART IDENTITY"))
        
        if not DATA_FILE.exists():
            print(f"  ⚠️  Data file not found: {DATA_FILE}")
            return

        with open(DATA_FILE, encoding="utf-8") as f:
            records = json.load(f)

        added, skipped = 0, 0
        sumatra_ports = {"Barus", "Air Bangis", "Padang", "Pulau Cingkuak", "Air Haji"}

        for rec in records:
            raw_asal = rec.get("Asal", "").strip()
            raw_tujuan = rec.get("Tujuan", "").strip()
            
            origin_name = clean_name(raw_asal)
            dest_name = clean_name(raw_tujuan)

            origin_fort = fort_map.get(origin_name)
            dest_fort = fort_map.get(dest_name)

            if not origin_fort and not dest_fort:
                skipped += 1
                continue

            direction = None
            if origin_name in sumatra_ports:
                direction = "outbound"
            elif dest_name in sumatra_ports:
                direction = "inbound"

            voyage = Voyage(
                origin_id=origin_fort.id if origin_fort else None,
                destination_id=dest_fort.id if dest_fort else None,
                origin_name_raw=raw_asal,
                destination_name_raw=raw_tujuan,
                ship_name=rec.get("Nama_Kapal", "Unknown"),
                captain=rec.get("Kapten"),
                year=rec.get("Tahun"),
                total_gulden=rec.get("Total_Gulden_NL"),
                main_product=rec.get("Produk_Utama"),
                all_products=rec.get("Semua_Produk"),
                destination=dest_name,
                duration_days=rec.get("Durasi_Hari"),
                direction=direction,
                source_url=rec.get("URL"),
            )
            session.add(voyage)
            added += 1

        session.commit()
        print(f"  ✔ Seeding Done: {added} voyages added. {skipped} records skipped.")

if __name__ == "__main__":
    wait_for_db()
    seed()
