"""
Seed commodity_glossary dari hasil scraping VOC Glossarium.

Jalankan SETELAH:
  1. python3 scrawling/voc_glossarium_scraper.py --pdf /tmp/VOCGlossarium.pdf
  2. docker compose exec -e SYNC_DATABASE_URL=postgresql://vocuser:vocpassword@db:5432/vocdb \
       backend alembic upgrade head   # pastikan tabel commodity_glossary ada

Jalankan:
  docker compose exec backend python /app/../scrawling/seed_glossary.py
  atau dari host (dengan DATABASE_SYNC_URL env):
  SYNC_DATABASE_URL=postgresql://vocuser:vocpassword@localhost:5433/vocdb \
    python3 scrawling/seed_glossary.py
"""

import json
import os
import sys
from pathlib import Path

# Tambah path backend agar bisa import database.py
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

DATABASE_SYNC_URL = os.environ.get(
    "SYNC_DATABASE_URL",
    "postgresql://vocuser:vocpassword@localhost:5433/vocdb",
)

GLOSSARIUM_JSON = Path(__file__).parent / "glossarium_output" / "voc_glossarium.json"

# Terjemahan manual untuk istilah yang paling sering muncul di dataset
# Tambah di sini setelah review atau setelah proses terjemahan
MANUAL_ID_DEFS = {
    "benzoë":         "Kemenyan; resin harum dari pohon Styrax benzoin, tumbuh di Sumatra",
    "benzoin":        "Kemenyan; resin harum dari pohon Styrax benzoin, tumbuh di Sumatra",
    "kamfer":         "Kamper; zat kristal putih beraroma dari pohon Cinnamomum camphora",
    "peper":          "Lada hitam; rempah utama perdagangan VOC dari Sumatra Barat",
    "goud":           "Emas; logam mulia, komoditas ekspor utama dari tambang Minangkabau",
    "foelie":         "Fuli; selaput biji pala (Myristica fragrans), rempah bernilai tinggi",
    "nootmuskaat":    "Pala; biji Myristica fragrans dari Maluku, monopoli VOC",
    "bindrotan":      "Rotan ikat; rotan kecil untuk anyaman dan pengikat",
    "tin":            "Timah putih; logam dari Bangka-Belitung, komoditas ekspor penting",
    "koper":          "Tembaga; logam merah untuk peralatan dan persenjataan",
    "indigo":         "Nila; tanaman penghasil pewarna biru alami",
    "sapanhout":      "Kayu secang (Caesalpinia sappan); kayu merah untuk pewarna dan obat",
    "arak":           "Arak; minuman keras sulingan dari beras atau nira kelapa",
    "rijst":          "Beras; bahan makanan pokok dan perbekalan kapal",
    "zeep":           "Sabun; produk manufaktur VOC",
    "lood":           "Timbal; logam untuk peluru dan pemberat jaring",
    "buskruit":       "Mesiu; campuran bubuk senjata api",
    "garioffelnagel": "Cengkih (Syzygium aromaticum); rempah Maluku, monopoli VOC",
    "kamferolie":     "Minyak kapur barus; minyak esensial dari kayu kamper Sumatra",
    "drakenbloed":    "Damar naga (Daemonorops draco); resin merah untuk cat dan obat",
    "calaturshout":   "Kayu kalatur; kayu keras tropis Sumatra",
    "kadjangmat":     "Kajang; tikar anyaman dari daun pandan atau rumbia",
    "sits":           "Kain cetis (chintz); kain katun bermotif dari India",
    "salempuris":     "Kain salempuri; kain katun putih halus dari India",
    "laken":          "Kain laken; kain wol tebal dari Eropa",
    "brandewijn":     "Brendi; minuman keras sulingan dari Eropa",
    "spijker":        "Paku besi; bahan bangunan dan perkapalan",
    "ijzer":          "Besi; logam dasar untuk perkakas dan bangunan kapal",
    "koffieboon":     "Biji kopi; tanaman introduksi VOC dari Arabia ke Jawa (~1696)",
    "poedersuiker":   "Gula bubuk; hasil penggilingan dari perkebunan tebu Jawa",
}


def seed(db_url: str, json_path: Path):
    from sqlalchemy import create_engine, text

    engine = create_engine(db_url)

    if not json_path.exists():
        print(f"[SKIP] File tidak ditemukan: {json_path}")
        print("       Jalankan scraper dulu:")
        print("       python3 scrawling/voc_glossarium_scraper.py --pdf /tmp/VOCGlossarium.pdf")
        # Seed manual definitions saja jika JSON belum ada
        entries = []
    else:
        with open(json_path, encoding="utf-8") as f:
            entries = json.load(f)
        print(f"[INFO] {len(entries)} entri dibaca dari {json_path}")

    # Jika tidak ada hasil scraper, seed dari MANUAL_ID_DEFS saja
    if not entries:
        entries = [
            {"term": k, "term_display": k, "variants": [], "definition_nl": None}
            for k in MANUAL_ID_DEFS
        ]
        print(f"[INFO] Menggunakan {len(entries)} entri manual")

    upserted = 0
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS commodity_glossary (
                id            SERIAL PRIMARY KEY,
                term          VARCHAR(200) NOT NULL UNIQUE,
                term_display  VARCHAR(200),
                variants      TEXT[],
                definition_nl TEXT,
                definition_id TEXT,
                category      VARCHAR(100)
            )
        """))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_glossary_term ON commodity_glossary (term)"
        ))

        for entry in entries:
            term = entry.get("term", "").strip().lower()
            if not term:
                continue
            def_id = MANUAL_ID_DEFS.get(term)
            conn.execute(text("""
                INSERT INTO commodity_glossary
                    (term, term_display, variants, definition_nl, definition_id)
                VALUES
                    (:term, :display, :variants, :def_nl, :def_id)
                ON CONFLICT (term) DO UPDATE SET
                    term_display  = EXCLUDED.term_display,
                    variants      = EXCLUDED.variants,
                    definition_nl = COALESCE(EXCLUDED.definition_nl, commodity_glossary.definition_nl),
                    definition_id = COALESCE(EXCLUDED.definition_id, commodity_glossary.definition_id)
            """), {
                "term":     term,
                "display":  entry.get("term_display", term),
                "variants": entry.get("variants", []),
                "def_nl":   entry.get("definition_nl"),
                "def_id":   def_id,
            })
            upserted += 1

    print(f"[OK] {upserted} entri di-upsert ke commodity_glossary")
    print(f"     {len(MANUAL_ID_DEFS)} istilah punya terjemahan Indonesia")


if __name__ == "__main__":
    seed(DATABASE_SYNC_URL, GLOSSARIUM_JSON)
