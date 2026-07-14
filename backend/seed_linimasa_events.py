"""
seed_linimasa_events.py

Muat data/research/linimasa_events.csv (peristiwa suksesi/politik kekuasaan
Atjeh atas pantai barat Sumatra, dari Sultan Iskandar Muda sampai Traktat
Painan 1663 dan pengusiran Atjeh 1664-1665, sampai penyerahan Sillida 1667 &
traktat Barus 1681) ke tabel linimasa_events. Idempotent -- truncate & reload
tiap run (dataset kecil, hand-curated, sama pola dgn seed_atjeh_trade.py).

Dua sumber pipeline campur di CSV ini -- dibedakan via source_document:
  - "1624-1629" | "1631-1634" | "1636" | "1637" | "1643-1644" | "1647-1648" |
    "1656-1657": didistilasi dari baris direction='politik' di
    atjeh_trade_records (OCR PDF docs/ kita, ejaan asli VOC-Belanda
    dipertahankan di text_asli). Baris 1624-1629 (1625) berisi klaim
    yurisdiksi TERLUAS -- event TERTUA di linimasa. Baris 1656-1657
    mengungkap PERANG TERBUKA VOC-Atjeh, 6 tahun sebelum Traktat Painan.
    GOTCHA: SETIAP kali atjeh_trade_records dapat volume baru dgn baris
    politik, cek juga apakah perlu didistilasi ke sini -- jangan cuma proses
    volume yg lagi disisir sesi itu (kejadian nyata: 1624-1629 & 1636
    terlewat berbulan-bulan sampai user menegur).
  - "1661" | "1663" | "1664" | "1665" | "1681": dari
    docs/thesis/dr/korpus_tema_slim.csv (corpus GLOBALISE/Huygens TERPISAH,
    sudah diterjemahkan Indonesia) -- text_asli di sini BUKAN OCR Belanda,
    melainkan kutipan terjemahan Indonesia. Provenance (corpus_id asal)
    dicatat eksplisit di kolom notes tiap baris. TEMUAN BESAR baris 1681:
    traktat Barus -- bukti Atjeh-Barus PERTAMA di seluruh korpus riset.

Jalankan: docker compose exec backend python seed_linimasa_events.py
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
    Path("/app/data/research/linimasa_events.csv"),
    _BASE / "data" / "research" / "linimasa_events.csv",
]
CSV_FILE = next((c for c in CSV_CANDIDATES if c.exists()), None)

ALLOWED_SOURCE_DOCUMENTS = {"1624-1629", "1631-1634", "1636", "1637", "1643-1644", "1647-1648", "1656-1657", "1659", "1661", "1663", "1664", "1665", "1681", "CD1", "CD2"}
ALLOWED_EVENT_TYPES = {"suksesi", "perjanjian", "konflik", "diplomasi", "administratif"}
ALLOWED_ERAS = {"klaim-awal", "ratu-puncak", "perang-damai", "retak-painan", "pengusiran-penataan"}
# Babak naratif Fase 1 /linimasa (docs/prd-linimasa-kronik-pantai-barat.md) --
# label/headline tiap era ada di frontend/map_app/views.py ERAS dict, BUKAN di sini
# (data event vs copy editorial sengaja dipisah). Rentang tahun berbasis data
# yg BENAR2 ada, bukan skema 1600-1690 design spec sumber.
#
# source_document="CD1" (2026-07-14): docs/CD1.pdf, Corpus Diplomaticum
# Neerlando-Indicum jilid I (ed. J.E. Heeres) -- kompilasi traktat/kontrak VOC,
# BEDA dari 9 volume Dagh-register (jurnal harian) & korpus_tema_slim.csv
# (GLOBALISE, sudah diterjemahkan). CD1 tetap OCR pipeline kita sendiri, ejaan
# VOC-Belanda asli dipertahankan -- TAPI buku ini juga berisi anotasi editorial
# modern (footnote Heeres) yg kadang jadi satu-satunya sumber suatu fakta (mis.
# identitas "Iskander Tsani"/Iskandar Thani) -- baris begitu ditandai eksplisit
# "catatan editor" di notes, beda dari kutipan traktat periode VOC asli. Mundurkan
# titik awal linimasa dari 1625 ke 1600 (2 traktat VOC-Atjeh pertama, 1600 & 1607).
#
# source_document="CD2" (2026-07-15): docs/CD2.pdf, Corpus Diplomaticum
# Neerlando-Indicum jilid II -- lanjutan kronologis CD1 (~1655-1673), lensa
# sisir tol/pajak & hadiah diplomasi. 14 event baru, termasuk RANGKAIAN
# pelepasan diri pantai barat dari Atjeh (Indrapoura 1663, Sillida 1667,
# Barus 1668, Priaman 1671, Cinkel/Singkil 1672) -- semua pakai frasa "kuk tak
# tertahankan" (onverdraeglijck jock). Beberapa baris CD2 MELENGKAPI event yg
# sudah ada dari source_document lain (mis. 1663 Songypagouers CD2 melengkapi
# 'Traktat Painan' dari korpus_tema_slim.csv dgn teks traktat primer) --
# ditandai eksplisit di notes sbg pelengkap, BUKAN duplikat/pengganti. Traktat
# Barus 1668 (CD2) mundurkan bukti Aceh-Barus dari 1681 -- caveat lama "Barus
# nihil sampai 1681" di riset_atjeh.html & sini WAJIB update.


def _clean(v):
    v = (v or "").strip()
    return v or None


def _int(v):
    v = (v or "").strip()
    if not v:
        return None
    try:
        return int(v)
    except ValueError:
        return None


def parse_row(row):
    source_document = _clean(row.get("source_document"))
    if source_document not in ALLOWED_SOURCE_DOCUMENTS:
        raise ValueError(f"source_document '{source_document}' tidak valid, harus salah satu dari {ALLOWED_SOURCE_DOCUMENTS}")

    source_page = _clean(row.get("source_page"))
    if not source_page:
        raise ValueError("source_page wajib ada")

    event_type = _clean(row.get("event_type"))
    if event_type not in ALLOWED_EVENT_TYPES:
        raise ValueError(f"event_type '{event_type}' tidak valid, harus salah satu dari {ALLOWED_EVENT_TYPES}")

    title = _clean(row.get("title"))
    if not title:
        raise ValueError("title wajib ada")

    text_asli = _clean(row.get("text_asli"))
    if not text_asli:
        raise ValueError("text_asli wajib ada -- jejak verifikasi ke sumber")

    era_slug = _clean(row.get("era_slug"))
    if era_slug not in ALLOWED_ERAS:
        raise ValueError(f"era_slug '{era_slug}' tidak valid, harus salah satu dari {ALLOWED_ERAS}")

    return {
        "source_document": source_document,
        "source_page": int(source_page),
        "book_page": _clean(row.get("book_page")),
        "event_date_raw": _clean(row.get("event_date_raw")),
        "year": _int(row.get("year")),
        "event_type": event_type,
        "ruler_actor": _clean(row.get("ruler_actor")),
        "title": title,
        "era_slug": era_slug,
        "text_asli": text_asli,
        "notes": _clean(row.get("notes")),
        "confidence_flag": "unverified",
    }


def main():
    if CSV_FILE is None:
        raise RuntimeError(f"linimasa_events.csv tidak ditemukan di: {CSV_CANDIDATES}")
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
    from models import LinimasaEvent  # tabel dibuat via migration 009

    with Session(engine) as session:
        session.execute(text("TRUNCATE TABLE linimasa_events RESTART IDENTITY"))
        session.execute(LinimasaEvent.__table__.insert(), records)
        session.commit()
        after = session.execute(text("SELECT COUNT(*) FROM linimasa_events")).scalar()

        by_type = session.execute(text(
            "SELECT event_type, COUNT(*) FROM linimasa_events GROUP BY event_type ORDER BY event_type"
        )).all()
        by_document = session.execute(text(
            "SELECT source_document, COUNT(*) FROM linimasa_events GROUP BY source_document ORDER BY source_document"
        )).all()
        by_era = session.execute(text(
            "SELECT era_slug, COUNT(*) FROM linimasa_events GROUP BY era_slug ORDER BY MIN(year)"
        )).all()

    print("=" * 60)
    print(f"linimasa_events: {after} baris")
    print(f"per tipe: {dict(by_type)}")
    print(f"per volume: {dict(by_document)}")
    print(f"per era: {dict(by_era)}")
    print("=" * 60)

    try:
        from cache import invalidate_prefix_sync
        flushed = invalidate_prefix_sync("voc:research_linimasa")
        print(f"cache linimasa di-invalidate: {flushed} key")
    except Exception as e:
        print(f"(cache invalidate dilewati: {e})")


if __name__ == "__main__":
    main()
