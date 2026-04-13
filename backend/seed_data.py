"""
Seed script — inserts fort metadata and voyage data from JSON into PostgreSQL.
Safe to run multiple times (idempotent via upsert logic).

Data source: scrawling/Data_BGS_Sumatra_Full.json (31MB, 4700+ records)
Direction algorithm:
  - OUTBOUND = origin is a Sumatera Westkust port (Padang, Barus, Air Bangis, etc.)
  - INBOUND  = destination is a Sumatera Westkust port
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

# ── Data file resolution ─────────────────────────────────────────────────────
# Priority: scrawling folder (full dataset) > data folder > docker path
_BASE = Path(__file__).parent.parent
DATA_FILE_CANDIDATES = [
    _BASE / "scrawling" / "Data_BGS_Sumatra_Full.json",
    _BASE / "data" / "Data_Westkust_Map.json",
    Path("/app/scrawling/Data_BGS_Sumatra_Full.json"),
    Path("/app/data/Data_Westkust_Map.json"),
]
DATA_FILE = None
for candidate in DATA_FILE_CANDIDATES:
    if candidate.exists():
        DATA_FILE = candidate
        break


# ── Port definitions ─────────────────────────────────────────────────────────
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
    # ── Arrival ports ────────────────────────────────────────────────────
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

# ── Name cleaning & direction classification ─────────────────────────────────

# Ports that define "Sumatera Westkust" — the focus area
SUMATRA_WESTKUST_PORTS = {"Padang", "Barus", "Air Bangis", "Pulau Cingkuak", "Air Haji"}
# All known ports for matching
ALL_KNOWN_PORTS = {f["name"] for f in FORTS_META}

# Spelling mapping from raw JSON variants → canonical name
NAME_MAPPING = {
    "Baros":           "Barus",
    "Airbangis":       "Air Bangis",
    "Aijer Bangis":    "Air Bangis",
    "Air-Bangis":      "Air Bangis",
    "Djambi":          "Jambi",
    "Jamby":           "Jambi",
    "Lampongs":        "Lampung",
    "Lampong":         "Lampung",
    "Sunda Kelapa":    "Batavia",
    "Jakarta":         "Batavia",
    "Poeloe Tjinkoek": "Pulau Cingkuak",
    "Poelau Cingkuak": "Pulau Cingkuak",
    "P. Cingkuak":     "Pulau Cingkuak",
    "Indrapoera":      "Pulau Cingkuak",
    "Indrapura":       "Pulau Cingkuak",
    "Ajer Hadji":      "Air Haji",
    "Aijer Hadji":     "Air Haji",
    "Ayer Haji":       "Air Haji",
    "Air Hadji":       "Air Haji",
}


def clean_name(raw_name: str) -> str:
    """
    Normalize port names from raw JSON data to match canonical fort names.
    
    Handles patterns like:
      - "Batavia,Batavia" → "Batavia"
      - "Padang,Sumatra's Westkust" → "Padang"
      - "Baros" → "Barus"
      - "-,Bengalen" → "Bengalen" (unmapped, will be skipped)
    """
    if not raw_name:
        return ""
    
    # Split by comma and take first meaningful part
    parts = [p.strip() for p in raw_name.split(",")]
    name = parts[0] if parts[0] and parts[0] != "-" else (parts[1] if len(parts) > 1 else "")
    name = name.strip()
    
    # Apply spelling mapping
    return NAME_MAPPING.get(name, name)


def classify_direction(origin_clean: str, dest_clean: str) -> str:
    """
    Classify voyage direction based on origin and destination.
    
    OUTBOUND = ship departs FROM Sumatera Westkust port
    INBOUND  = ship arrives AT Sumatera Westkust port
    
    Returns: "outbound", "inbound", or "transit" (neither endpoint is Westkust)
    """
    origin_is_westkust = origin_clean in SUMATRA_WESTKUST_PORTS
    dest_is_westkust = dest_clean in SUMATRA_WESTKUST_PORTS
    
    if origin_is_westkust and not dest_is_westkust:
        return "outbound"
    elif dest_is_westkust and not origin_is_westkust:
        return "inbound"
    elif origin_is_westkust and dest_is_westkust:
        return "outbound"  # Internal Westkust, treat as outbound
    else:
        return "transit"   # e.g. Palembang → Batavia


# ── Database helpers ─────────────────────────────────────────────────────────

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
    from models import Fort, Voyage, CargoItem, Base
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
                existing.description = meta["description"]
                fort_map[meta["name"]] = existing
            else:
                f = Fort(**meta)
                session.add(f)
                session.flush()
                fort_map[meta["name"]] = f
        session.commit()
        print(f"  ✔ Forts seeded: {len(fort_map)} ports")

        # ---------- Check if data already exists to speed up boot ----------
        from sqlalchemy import func
        existing_voyages = session.execute(select(func.count()).select_from(Voyage)).scalar()
        if existing_voyages > 0:
            print(f"  ✔ Database already contains {existing_voyages} voyages. Skipping seed.")
            return

        # ---------- Seed voyages + cargo ----------
        session.execute(text("TRUNCATE TABLE cargo_items RESTART IDENTITY CASCADE"))
        session.execute(text("TRUNCATE TABLE voyages RESTART IDENTITY CASCADE"))
        
        if not DATA_FILE or not DATA_FILE.exists():
            print(f"  ⚠️  Data file not found. Searched: {[str(c) for c in DATA_FILE_CANDIDATES]}")
            return

        print(f"  📂 Loading data from: {DATA_FILE}")
        with open(DATA_FILE, encoding="utf-8") as f:
            records = json.load(f)
        print(f"  📊 Loaded {len(records)} records from JSON")

        added = 0
        skipped = 0
        cargo_total = 0
        direction_counts = {"outbound": 0, "inbound": 0, "transit": 0}

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

            direction = classify_direction(origin_name, dest_name)
            direction_counts[direction] += 1

            # Extract dates from nested JSON objects
            dep_date = None
            arr_date = None
            tgl_berangkat = rec.get("Tgl_Berangkat")
            tgl_tiba = rec.get("Tgl_Tiba")
            if isinstance(tgl_berangkat, dict):
                dep_date = tgl_berangkat.get("iso")
            if isinstance(tgl_tiba, dict):
                arr_date = tgl_tiba.get("iso")

            voyage = Voyage(
                voyage_ref=rec.get("ID"),
                origin_id=origin_fort.id if origin_fort else None,
                destination_id=dest_fort.id if dest_fort else None,
                origin_name_raw=raw_asal,
                destination_name_raw=raw_tujuan,
                ship_name=rec.get("Nama_Kapal", "Unknown"),
                captain=rec.get("Kapten"),
                tonnage=str(rec.get("Tonaj", "")) if rec.get("Tonaj") else None,
                year=rec.get("Tahun"),
                departure_date=dep_date,
                arrival_date=arr_date,
                total_gulden=rec.get("Total_Gulden_NL"),
                main_product=rec.get("Produk_Utama"),
                all_products=rec.get("Semua_Produk"),
                cargo_count=rec.get("Jumlah_Item_Kargo"),
                destination=dest_name,
                duration_days=rec.get("Durasi_Hari"),
                direction=direction,
                source_url=rec.get("URL"),
            )
            session.add(voyage)
            session.flush()  # Get voyage.id for cargo items

            # Seed cargo items from Kargo[] array
            kargo_list = rec.get("Kargo", [])
            if kargo_list and isinstance(kargo_list, list):
                for kargo in kargo_list:
                    cargo_item = CargoItem(
                        voyage_id=voyage.id,
                        produk=kargo.get("produk", "unknown"),
                        spesifikasi=kargo.get("spesifikasi"),
                        qty_asli=kargo.get("qty_asli"),
                        unit=kargo.get("unit"),
                        nilai_numerik=kargo.get("nilai_numerik"),
                        gram=kargo.get("gram"),
                        gulden_nl=kargo.get("gulden_nl"),
                        gulden_india=kargo.get("gulden_india"),
                        catatan=kargo.get("catatan"),
                    )
                    session.add(cargo_item)
                    cargo_total += 1

            added += 1

            # Batch commit every 500 voyages for performance
            if added % 500 == 0:
                session.commit()
                print(f"    ... {added} voyages, {cargo_total} cargo items seeded")

        session.commit()
        
        print(f"\n  ══════════════════════════════════════════")
        print(f"  ✔ Seeding Complete!")
        print(f"  ──────────────────────────────────────────")
        print(f"  📦 Total voyages added:  {added}")
        print(f"  📋 Total cargo items:    {cargo_total}")
        print(f"  ⏭️  Total skipped:        {skipped}")
        print(f"  🚢 Outbound:             {direction_counts['outbound']}")
        print(f"  🏠 Inbound:              {direction_counts['inbound']}")
        print(f"  🔄 Transit:              {direction_counts['transit']}")
        print(f"  ══════════════════════════════════════════\n")


if __name__ == "__main__":
    wait_for_db()
    seed()
