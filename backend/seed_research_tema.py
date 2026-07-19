"""
seed_research_tema.py — SNK-1 (docs/sprint/sprint-sankey-tema-korpus.md)

Muat data/research/korpus_tema_slim.csv (1.005 baris klasifikasi tema-korpus)
ke tabel research_theme_rows. Idempotent by corpus_id (ON CONFLICT DO UPDATE) —
aman dijalankan berulang, tidak menduplikat.

File slim (3.6MB) = hasil docs/thesis/dr/slim_corpus_for_db.py:
  - text_asli GLOBALISE diganti pointer inventaris (DATA-SNK-1)
  - tahun/dekade sudah dikoreksi fallback volume (FIX #1)

Jalankan: docker compose exec backend python seed_research_tema.py
"""
import csv
import os
import sys
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

csv.field_size_limit(10 ** 9)

DATABASE_SYNC_URL = os.getenv("DATABASE_SYNC_URL") or os.getenv("SYNC_DATABASE_URL")
if not DATABASE_SYNC_URL:
    raise RuntimeError("DATABASE_SYNC_URL env var is required but not set")

_BASE = Path(__file__).parent.parent
CSV_CANDIDATES = [
    Path("/app/data/research/korpus_tema_slim.csv"),
    _BASE / "data" / "research" / "korpus_tema_slim.csv",
]
CSV_FILE = next((c for c in CSV_CANDIDATES if c.exists()), None)
if CSV_FILE is None:
    raise RuntimeError(f"korpus_tema_slim.csv tidak ditemukan di: {CSV_CANDIDATES}")

SKOR_COLS = [
    "skor_pdr_drainase", "skor_etr_retensi", "skor_hak_adat", "skor_pelayaran",
    "skor_sengketa", "skor_syahbandar", "skor_tidak_relevan",
]


def _int(v):
    v = (v or "").strip()
    return int(v) if v else None


def _float(v):
    v = (v or "").strip()
    try:
        return float(v) if v else None
    except ValueError:
        return None


def _bool(v):
    return str(v).strip().lower() in ("true", "1", "yes")


def parse_row(row):
    rec = {
        "corpus_id": _int(row.get("corpus_id")),
        "corpus_asal": (row.get("corpus_asal") or "").strip(),
        "source": (row.get("source") or "").strip() or None,
        "volume": (row.get("volume") or "").strip() or None,
        "inventaris_ref": (row.get("inventaris_ref") or "").strip() or None,
        "tanggal_perkiraan": (row.get("tanggal_perkiraan") or "").strip() or None,
        "tahun": _int(row.get("tahun")),
        "dekade": _int(row.get("dekade")),
        "pelabuhan_disebut": (row.get("pelabuhan_disebut") or "Tidak diketahui").strip(),
        "tema_dominan": (row.get("tema_dominan") or "").strip(),
        "skor_dominan": _float(row.get("skor_dominan")),
        "low_confidence": _bool(row.get("low_confidence")),
        "text": row.get("text") or "",
        "text_asli": row.get("text_asli") or None,
    }
    for c in SKOR_COLS:
        rec[c] = _float(row.get(c))
    return rec


def main():
    print(f"Sumber : {CSV_FILE}")
    records = []
    with CSV_FILE.open(newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            rec = parse_row(row)
            if rec["corpus_id"] is None or not rec["tema_dominan"]:
                # jangan skip diam-diam — laporkan
                print(f"  ! baris dilewati (corpus_id/tema kosong): {row.get('corpus_id')!r}")
                continue
            records.append(rec)
    print(f"Terbaca: {len(records)} baris valid")

    engine = create_engine(DATABASE_SYNC_URL, future=True)
    from models import ResearchThemeRow  # tabel dibuat via init_db()/alembic

    with Session(engine) as session:
        before = session.execute(text("SELECT COUNT(*) FROM research_theme_rows")).scalar()
        stmt = pg_insert(ResearchThemeRow.__table__)
        update_cols = {c.name: stmt.excluded[c.name]
                       for c in ResearchThemeRow.__table__.columns
                       if c.name not in ("id", "corpus_id")}
        stmt = stmt.on_conflict_do_update(index_elements=["corpus_id"], set_=update_cols)
        # batch insert
        for i in range(0, len(records), 200):
            session.execute(stmt, records[i:i + 200])
        session.commit()
        after = session.execute(text("SELECT COUNT(*) FROM research_theme_rows")).scalar()

        # ringkasan verifikasi granular
        by_corpus = session.execute(text(
            "SELECT corpus_asal, COUNT(*) FROM research_theme_rows GROUP BY corpus_asal ORDER BY corpus_asal"
        )).all()
        null_dek = session.execute(text(
            "SELECT COUNT(*) FROM research_theme_rows WHERE dekade IS NULL"
        )).scalar()
        low_conf = session.execute(text(
            "SELECT COUNT(*) FROM research_theme_rows WHERE low_confidence = true"
        )).scalar()

    print("=" * 60)
    print(f"research_theme_rows: {before} -> {after} baris")
    print(f"per corpus: {dict(by_corpus)}")
    print(f"dekade NULL (tak bertahun): {null_dek}")
    print(f"low_confidence: {low_conf}")
    print("=" * 60)

    # Invalidasi cache endpoint research (ADR-001) — data berubah, cache lama basi.
    # Prefix "voc:research_" mencakup research_sankey / research_triples / research_rows.
    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:research_")
        print(f"cache research di-invalidate: {flushed} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
