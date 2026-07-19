"""
Seed script — inserts fort metadata and voyage data from JSON into PostgreSQL.
Safe to run multiple times (idempotent via upsert logic).

Data sources:
  - scrawling/Data_BGS_Sumatra_Full.json  (4700+ outbound/transit records)
  - scrawling/Data_BGS_Inbound_Full.json  (375 Batavia→Westkust inbound records)
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
DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

# ── Data file resolution ─────────────────────────────────────────────────────
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

INBOUND_FILE_CANDIDATES = [
    _BASE / "scrawling" / "Data_BGS_Inbound_Full.json",
    Path("/app/scrawling/Data_BGS_Inbound_Full.json"),
]
INBOUND_FILE = None
for candidate in INBOUND_FILE_CANDIDATES:
    if candidate.exists():
        INBOUND_FILE = candidate
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
        "description": "Fort de Goede Hoop di Padang adalah pusat ekspor emas dan lada utama VOC di Sumatera Westkust.",
        "amh_url": "https://www.atlasofmutualheritage.nl/page/5751/padang",
        "amh_images": [
            {
                "title": "Gezicht op het Fort te Padang",
                "creator": "Isaac de Graaff",
                "year": "1695",
                "thumbnail_url": None,
                "page_url": "https://www.atlasofmutualheritage.nl/page/5751/padang",
            },
            {
                "title": "Kaart van de Westkust van Sumatra",
                "creator": "Johannes van Keulen II",
                "year": "1728",
                "thumbnail_url": None,
                "page_url": "https://www.atlasofmutualheritage.nl/page/5751/padang",
            },
            {
                "title": "Plattegrond van Fort de Goede Hoop te Padang",
                "creator": "VOC Cartographer",
                "year": "1780",
                "thumbnail_url": None,
                "page_url": "https://www.atlasofmutualheritage.nl/page/5751/padang",
            },
        ],
    },
    {
        "name": "Pulau Cingkuak",
        "latitude": -1.3531125710383205,
        "longitude": 100.55921198502948,
        "color": "#e67e22",
        "port_type": "departure",
        "description": "Pulau Cingkuak (Fort van Indrapura) adalah pos perdagangan lada vital di pesisir selatan.",
        "amh_url": "https://www.atlasofmutualheritage.nl/page/5764/pulau-cingkuak",
        "amh_images": [
            {
                "title": "Fort van Indrapura te Poeloe Tjinkoek",
                "creator": "VOC Cartographer",
                "year": "1750",
                "thumbnail_url": None,
                "page_url": "https://www.atlasofmutualheritage.nl/page/5764/pulau-cingkuak",
            },
            {
                "title": "Gezicht op Indrapura",
                "creator": "Cornelis de Jonge",
                "year": "1762",
                "thumbnail_url": None,
                "page_url": "https://www.atlasofmutualheritage.nl/page/5764/pulau-cingkuak",
            },
        ],
    },
    {
        "name": "Air Haji",
        "latitude": -1.9339388,
        "longitude": 100.8669821,
        "color": "#27ae60",
        "port_type": "departure",
        "description": "Pos perdagangan VOC di wilayah selatan yang mengumpulkan lada dan hasil hutan."
    },
    {
        "name": "Tiku",
        "latitude": -0.40257599785703735,
        "longitude": 99.91467276260393,
        "color": "#f39c12",
        "port_type": "departure",
        "description": "Tiku (Tico/Ticco) adalah salah satu pelabuhan lada tertua di pantai barat Sumatra, disebut dalam Dagh-register Batavia sejak abad ke-17."
    },
    {
        "name": "Pariaman",
        "latitude": -0.6661663190442159,
        "longitude": 100.15006330858158,
        "color": "#1abc9c",
        "port_type": "departure",
        "description": "Pariaman (Priaman) adalah pos pengumpulan lada dan kemenyan yang berulang kali disebut dalam Dagh-register Batavia."
    },
    {
        "name": "Salido",
        "latitude": -1.3371097960700769,
        "longitude": 100.57240227882507,
        "color": "#9b59b6",
        "port_type": "departure",
        "description": "Salido (Sillida) adalah lokasi tambang emas VOC yang dikelola lewat sewa kepada penambang lokal/Cina, dengan penghulu setempat mempertahankan klaim hak ulayat."
    },
    {
        "name": "Bayang",
        "latitude": -1.302468150977219,
        "longitude": 100.50573673465257,
        "color": "#34495e",
        "port_type": "departure",
        "description": "Bayang adalah pos pengumpulan lada di pesisir selatan, disebut dalam Dagh-register Batavia."
    },
    {
        "name": "Painan",
        "latitude": -1.3499330477593903,
        "longitude": 100.56415483786208,
        "color": "#e84393",
        "port_type": "departure",
        "description": "Painan adalah pusat administratif pesisir selatan, dekat dengan lokasi tambang Salido dan Pulau Cingkuak."
    },
    {
        "name": "Inderapura",
        "latitude": -2.20,
        "longitude": 100.87,
        "color": "#8e6c3a",
        "port_type": "both",
        "description": "Kerajaan/pelabuhan lada di selatan Air Haji. Dagh-register 1661: 'Indrapoura levert alleen meer peper uyt als Sillida, Priaman en Ticco te zamen'. Pos residen VOC (Pieter Ketting, 1661)."
    },
    # ── Arrival ports ────────────────────────────────────────────────────
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

# Pelabuhan pantai timur — dihapus dari skope atlas (rev.11, 2026-07-08).
# Dicek TERHADAP RAW NAME (sebelum clean_name()), krn mapping ejaan varian
# (Djambi/Jamby/Lampongs/Lampong) sengaja dihapus dari NAME_MAPPING bersamaan --
# kalau exclusion ini dicek pasca clean_name(), varian yg tak lagi dinormalisasi
# akan lolos filter dan masuk sbg voyage ber-origin/destination tak ter-resolve.
EAST_PORTS_EXCLUDED_RAW = {"Jambi", "Djambi", "Jamby", "Palembang", "Lampung", "Lampongs", "Lampong"}

# Ports that define "Sumatera Westkust" — the focus area
SUMATRA_WESTKUST_PORTS = {"Padang", "Barus", "Air Bangis", "Pulau Cingkuak", "Air Haji", "Tiku", "Pariaman", "Salido", "Bayang", "Painan"}
# All known ports for matching
ALL_KNOWN_PORTS = {f["name"] for f in FORTS_META}

# Spelling mapping from raw JSON variants → canonical name
NAME_MAPPING = {
    "Baros":           "Barus",
    "Airbangis":       "Air Bangis",
    "Aijer Bangis":    "Air Bangis",
    "Air-Bangis":      "Air Bangis",
    "Sunda Kelapa":    "Batavia",
    "Jakarta":         "Batavia",
    "Poeloe Tjinkoek": "Pulau Cingkuak",
    "Poelau Cingkuak": "Pulau Cingkuak",
    "P. Cingkuak":     "Pulau Cingkuak",
    "Indrapoera":      "Inderapura",
    "Indrapura":       "Inderapura",
    "Ajer Hadji":      "Air Haji",
    "Aijer Hadji":     "Air Haji",
    "Ayer Haji":       "Air Haji",
    "Air Hadji":       "Air Haji",
    "Airhadji":        "Air Haji",
    "Pulau Tjinkuk":   "Pulau Cingkuak",
    "Poeloe Tjinkuk":  "Pulau Cingkuak",
    # Dagh-register / GLOBALISE spelling variants (docs/prd/prd-cleaning-daghregister-1660-1669.md P1.1)
    "Tico":            "Tiku",
    "Ticco":           "Tiku",
    "Priaman":         "Pariaman",
    "Sillida":         "Salido",
    "Salida":          "Salido",
    "Sillidase":       "Salido",
    # Perluasan P1.1 (2026-07-07) -- hasil scan penuh daghregister_corpus.csv (511 baris)
    # + globalise_corpus.csv (535 baris), dibandingkan thd varian yang sudah ada di atas.
    "Silida":          "Salido",
    "Periaman":        "Pariaman",
    "Piriaman":        "Pariaman",
    "Chinco":          "Pulau Cingkuak",
    "Chinko":          "Pulau Cingkuak",
    "Indrapoura":      "Inderapura",
    "Indiapoura":      "Pulau Cingkuak",
    "Aijerhadja":      "Air Haji",
    "Aijerhadji":      "Air Haji",
    "Ayerhadja":       "Air Haji",
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

    name = _split_raw_name(raw_name)
    # Apply spelling mapping
    return NAME_MAPPING.get(name, name)


def _split_raw_name(raw_name: str) -> str:
    """Bagian split-comma+strip dari clean_name(), TANPA substitusi NAME_MAPPING --
    dipakai utk cek EAST_PORTS_EXCLUDED_RAW sebelum ejaan varian dinormalisasi."""
    parts = [p.strip() for p in raw_name.split(",")]
    name = parts[0] if parts[0] and parts[0] != "-" else (parts[1] if len(parts) > 1 else "")
    return name.strip()


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


def _insert_records(session, records, fort_map, label="", existing_refs=None):
    """Insert voyage records from a list of JSON dicts. Returns (added, skipped, cargo_total, dir_counts)."""
    from models import Voyage, CargoItem
    added = 0
    skipped = 0
    cargo_total = 0
    direction_counts = {"outbound": 0, "inbound": 0, "transit": 0}

    for rec in records:
        # Skip if voyage_ref already in DB (avoid UniqueViolation on overlap)
        if existing_refs is not None and rec.get("ID") in existing_refs:
            skipped += 1
            continue
        raw_asal = rec.get("Asal", "").strip()
        raw_tujuan = rec.get("Tujuan", "").strip()

        # Cek exclusion pantai timur thd nama SEBELUM NAME_MAPPING -- varian ejaan
        # (Djambi/Lampongs dst) tidak lagi dinormalisasi, jadi harus dicek di sini.
        if _split_raw_name(raw_asal) in EAST_PORTS_EXCLUDED_RAW or _split_raw_name(raw_tujuan) in EAST_PORTS_EXCLUDED_RAW:
            skipped += 1
            continue

        origin_name = clean_name(raw_asal)
        dest_name = clean_name(raw_tujuan)

        origin_fort = fort_map.get(origin_name)
        dest_fort = fort_map.get(dest_name)

        if not origin_fort and not dest_fort:
            skipped += 1
            continue

        direction = classify_direction(origin_name, dest_name)
        direction_counts[direction] += 1

        dep_date = arr_date = None
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
        session.flush()

        kargo_list = rec.get("Kargo", [])
        if kargo_list and isinstance(kargo_list, list):
            for kargo in kargo_list:
                session.add(CargoItem(
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
                ))
                cargo_total += 1

        added += 1
        if added % 500 == 0:
            session.commit()
            print(f"    {label}... {added} voyages, {cargo_total} cargo items")

    session.commit()
    return added, skipped, cargo_total, direction_counts


def seed():
    from models import Fort, Voyage, Base
    from sqlalchemy import func
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
                existing.port_type   = meta["port_type"]
                existing.color       = meta["color"]
                existing.description = meta["description"]
                existing.amh_url     = meta.get("amh_url")
                existing.amh_images  = meta.get("amh_images")
                existing.latitude    = meta["latitude"]
                existing.longitude   = meta["longitude"]
                fort_map[meta["name"]] = existing
            else:
                # Fort(**meta) passes all keys including optional amh_url/amh_images
                fort_kwargs = {k: v for k, v in meta.items()
                               if k in {"name", "latitude", "longitude", "color",
                                        "port_type", "description", "amh_url", "amh_images"}}
                f = Fort(**fort_kwargs)
                session.add(f)
                session.flush()
                fort_map[meta["name"]] = f
        session.commit()
        print(f"  ✔ Forts seeded: {len(fort_map)} ports")

        # ---------- Seed outbound/transit voyages ----------
        existing_total = session.execute(select(func.count()).select_from(Voyage)).scalar()
        if existing_total == 0:
            if not DATA_FILE or not DATA_FILE.exists():
                print(f"  ⚠️  Outbound data file not found.")
            else:
                session.execute(text("TRUNCATE TABLE cargo_items RESTART IDENTITY CASCADE"))
                session.execute(text("TRUNCATE TABLE voyages RESTART IDENTITY CASCADE"))
                print(f"  📂 Loading outbound data: {DATA_FILE}")
                with open(DATA_FILE, encoding="utf-8") as f:
                    records = json.load(f)
                print(f"  📊 {len(records)} outbound records")
                added, skipped, cargo_total, dir_counts = _insert_records(session, records, fort_map, "outbound")
                print(f"  ✔ Outbound: {added} voyages ({dir_counts['outbound']} out, {dir_counts['transit']} transit), {skipped} skipped, {cargo_total} cargo items")
        else:
            print(f"  ✔ Outbound/transit voyages already present ({existing_total}). Skipping.")

        # ---------- Fix inbound voyages (UPDATE mis-scraped records) ----------
        # The outbound scraper captured arrival_place as Asal for 375 Batavia→Westkust voyages.
        # The inbound scraper has the correct data (Asal=Batavia).
        # We UPDATE those records rather than INSERT (same voyage_ref, wrong origin).
        existing_inbound = session.execute(
            select(func.count()).select_from(Voyage).where(Voyage.direction == "inbound")
        ).scalar()
        if existing_inbound == 0:
            if not INBOUND_FILE or not INBOUND_FILE.exists():
                print(f"  ⚠️  Inbound data file not found.")
            else:
                print(f"  📂 Loading inbound data (UPDATE mode): {INBOUND_FILE}")
                with open(INBOUND_FILE, encoding="utf-8") as f:
                    inbound_records = json.load(f)
                print(f"  📊 {len(inbound_records)} inbound records to reconcile")

                updated = 0
                inserted = 0
                skipped_ib = 0

                existing_refs = {
                    row[0]: row[1]
                    for row in session.execute(
                        select(Voyage.voyage_ref, Voyage.id).where(Voyage.voyage_ref.isnot(None))
                    ).all()
                }

                for rec in inbound_records:
                    raw_asal  = rec.get("Asal", "").strip()
                    raw_tujuan = rec.get("Tujuan", "").strip()
                    origin_name = clean_name(raw_asal)
                    dest_name   = clean_name(raw_tujuan)
                    origin_fort = fort_map.get(origin_name)
                    dest_fort   = fort_map.get(dest_name)

                    if not origin_fort and not dest_fort:
                        skipped_ib += 1
                        continue

                    direction = classify_direction(origin_name, dest_name)

                    voyage_ref = rec.get("ID")
                    if voyage_ref in existing_refs:
                        # UPDATE existing record with correct origin data
                        voyage_id = existing_refs[voyage_ref]
                        voyage = session.get(Voyage, voyage_id)
                        if voyage:
                            voyage.origin_name_raw = raw_asal
                            voyage.destination_name_raw = raw_tujuan
                            voyage.origin_id = origin_fort.id if origin_fort else None
                            voyage.destination_id = dest_fort.id if dest_fort else None
                            voyage.direction = direction
                            voyage.destination = dest_name
                            updated += 1
                    else:
                        # New record — insert
                        dep_date = arr_date = None
                        tgl_b = rec.get("Tgl_Berangkat")
                        tgl_t = rec.get("Tgl_Tiba")
                        if isinstance(tgl_b, dict): dep_date = tgl_b.get("iso")
                        if isinstance(tgl_t, dict): arr_date = tgl_t.get("iso")
                        session.add(Voyage(
                            voyage_ref=voyage_ref,
                            origin_id=origin_fort.id if origin_fort else None,
                            destination_id=dest_fort.id if dest_fort else None,
                            origin_name_raw=raw_asal,
                            destination_name_raw=raw_tujuan,
                            ship_name=rec.get("Nama_Kapal", "Unknown"),
                            captain=rec.get("Kapten"),
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
                        ))
                        inserted += 1

                session.commit()
                print(f"  ✔ Inbound reconcile: {updated} updated, {inserted} inserted, {skipped_ib} skipped")
        else:
            print(f"  ✔ Inbound voyages already present ({existing_inbound}). Skipping.")

    # Data berubah → cache API basi. Flush prefix voc:* (DBA-3, ADR-001).
    from cache import invalidate_prefix_sync
    flushed = invalidate_prefix_sync()
    print(f"  ✔ Cache invalidated: {flushed} key voc:* dihapus")

    print(f"\n  ══════════════════════════════════════════")
    print(f"  ✔ Seed complete.")
    print(f"  ══════════════════════════════════════════\n")


if __name__ == "__main__":
    wait_for_db()
    seed()
