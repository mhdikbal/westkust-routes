"""
seed_atjeh_trade.py

Muat data/research/atjeh_trade_1643_1644.csv (ekstraksi manual laporan dagang
dari/ke/di Atjeh, sumber: docs/"Dagh-register gehouden int casteel Batavia ...
1643-1644".pdf) ke tabel atjeh_trade_records. Idempotent -- truncate & reload
tiap run (dataset kecil, hand-curated, tak ada natural key stabil lintas revisi).

commodity_raw/unit_raw/actor_raw SENGAJA memakai ejaan asli VOC-Belanda dari
sumber -- BUKAN terjemahan Indonesia (mis. "salpeter", bukan "sendawa"). Lihat
CommodityGlossary utk padanan/definisi bila perlu.

confidence_flag='unverified' pada semua baris: hasil pembacaan teks OCR PDF,
belum dicocokkan ulang thd scan halaman asli.

Jalankan: docker compose exec backend python seed_atjeh_trade.py
"""
import csv
import os
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

_BASE = Path(__file__).parent.parent
CSV_CANDIDATES = [
    Path("/app/data/research/atjeh_trade_1643_1644.csv"),
    _BASE / "data" / "research" / "atjeh_trade_1643_1644.csv",
]
CSV_FILE = next((c for c in CSV_CANDIDATES if c.exists()), None)

ALLOWED_DIRECTIONS = {"naar_atjeh", "van_atjeh", "in_atjeh"}


def _clean(v):
    v = (v or "").strip()
    return v or None


def _float(v):
    v = (v or "").strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def parse_row(row):
    source_page = _clean(row.get("source_page"))
    if not source_page:
        raise ValueError("source_page wajib ada (halaman PDF sumber)")

    direction = _clean(row.get("direction"))
    if direction not in ALLOWED_DIRECTIONS:
        raise ValueError(f"direction '{direction}' tidak valid, harus salah satu dari {ALLOWED_DIRECTIONS}")

    text_asli = _clean(row.get("text_asli"))
    if not text_asli:
        raise ValueError("text_asli wajib ada -- jejak verifikasi ke sumber OCR")

    return {
        "source_page": int(source_page),
        "book_page": _clean(row.get("book_page")),
        "entry_date_raw": _clean(row.get("entry_date_raw")),
        "direction": direction,
        "commodity_raw": _clean(row.get("commodity_raw")),
        "quantity_raw": _clean(row.get("quantity_raw")),
        "unit_raw": _clean(row.get("unit_raw")),
        "price_value": _float(row.get("price_value")),
        "price_unit_raw": _clean(row.get("price_unit_raw")),
        "actor_raw": _clean(row.get("actor_raw")),
        "text_asli": text_asli,
        "notes": _clean(row.get("notes")),
        "confidence_flag": "unverified",
    }


def main():
    if CSV_FILE is None:
        raise RuntimeError(f"atjeh_trade_1643_1644.csv tidak ditemukan di: {CSV_CANDIDATES}")
    print(f"Sumber : {CSV_FILE}")

    records = []
    with CSV_FILE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            records.append(parse_row(row))
    print(f"Terbaca: {len(records)} baris")

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    for r in records:
        r["created_at"] = now

    engine = create_engine(DATABASE_SYNC_URL, future=True)
    from models import AtjehTradeRecord  # tabel dibuat via init_db()

    with Session(engine) as session:
        session.execute(text("TRUNCATE TABLE atjeh_trade_records RESTART IDENTITY"))
        session.execute(AtjehTradeRecord.__table__.insert(), records)
        session.commit()
        after = session.execute(text("SELECT COUNT(*) FROM atjeh_trade_records")).scalar()

        by_direction = session.execute(text(
            "SELECT direction, COUNT(*) FROM atjeh_trade_records GROUP BY direction ORDER BY direction"
        )).all()

    print("=" * 60)
    print(f"atjeh_trade_records: {after} baris")
    print(f"per arah: {dict(by_direction)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
