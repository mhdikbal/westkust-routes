"""
seed_atjeh_trade.py

Muat data/research/atjeh_trade.csv (ekstraksi manual laporan dagang dari/ke/di
Atjeh, sumber: tujuh volume docs/"Dagh-register gehouden int casteel Batavia"
-- 1643-1644, 1631-1634, 1637, 1636, 1624-1629, 1644-1645, 1647-1648, 1656-1657, dan 1659) ke tabel atjeh_trade_records.
Idempotent -- truncate & reload tiap run (dataset kecil, hand-curated, tak ada
natural key stabil lintas revisi).

commodity_raw/unit_raw/actor_raw SENGAJA memakai ejaan asli VOC-Belanda dari
sumber -- BUKAN terjemahan Indonesia (mis. "salpeter", bukan "sendawa"). Lihat
CommodityGlossary utk padanan/definisi bila perlu.

confidence_flag='unverified' pada semua baris: hasil pembacaan teks OCR PDF,
belum dicocokkan ulang thd scan halaman asli. source_document membedakan
volume PDF asal ("1643-1644" | "1631-1634" | "1637" | "1636" | "1624-1629" | "1644-1645" | "1647-1648" | "1656-1657" | "1659")
-- source_page saja ambigu lintas volume.

GOTCHA regex sisir (2026-07-13): regex lama a[et]tch[ei]n|atjeh|acheh|achem|
atchem TIDAK match ejaan dominan corpus ini ("Atchijn"/"Atchin"/"Atchien" --
tanpa huruf ganda) -- verified False utk semua tiga. Baris hasil sisir volume
1643-1644 & 1631-1634 SEBELUM tanggal ini kemungkinan undercount parah (regex
lama cuma nemu 11/51 & 2/40 halaman asli). Regex benar (lihat scratchpad
sesi, bukan file project): atch, aetch, atjeh, acheh, achem sbg awalan kata
(lalu filter false-positive "Daetcheron"/"Datcherum", nama tempat Coromandel
yg kebetulan mirip).

GOTCHA regex kedua (volume 1647-1648): surat-surat asli dari panglima pantai
barat (Priaman, Sileda/Salida, Bhandar Galiffa/Tikoe, koning Indrapoera) TIDAK
match regex Atjeh di atas sama sekali krn nama tempatnya beda -- perlu regex
tambahan `indrapoe|salida|sillida|cillida|priaman|tikoe|bhandar|westcust`
dijalankan terpisah, lalu diverifikasi silang ke REGISTER (indeks) akhir buku.
Kalau sisir volume baru lain dan cuma nemu sedikit hit regex Atjeh padahal
user minta "pantai barat", curigai pola yg sama -- jalankan regex nama
pelabuhan westkust langsung, jangan cuma regex Atjeh.

source_document="CD1" (2026-07-14): BEDA SUMBER dari 9 volume Dagh-register di
atas -- docs/CD1.pdf adalah Corpus Diplomaticum Neerlando-Indicum jilid I
(ed. J.E. Heeres), kompilasi TRAKTAT/KONTRAK VOC, bukan jurnal harian. Masih
diekstraksi via OCR pipeline kita sendiri (bukan korpus_tema_slim.csv), ejaan
VOC-Belanda asli dipertahankan di text_asli, TAPI buku ini juga berisi banyak
narasi/catatan kaki editorial modern (bahasa Belanda Heeres, awal abad 20) --
saat kutip text_asli, prioritaskan teks traktat periode VOC asli (mis. "Aldus
gedaen...", "Contract ende overeencominge..."), bukan prosa editor, KECUALI
faktanya cuma tersedia lewat anotasi editor (tandai eksplisit di notes kalau
begitu). Baris CD1 wajib tag "SUMBER: Corpus Diplomaticum" di notes utk
bedakan dari 9 volume Dagh-register.

source_document="CD2" (2026-07-15): docs/CD2.pdf, Corpus Diplomaticum
Neerlando-Indicum jilid II (ed. J.E. Heeres, 639 halaman) -- lanjutan
kronologis CD1 (~1655-1673). Lensa sisir sesi ini: tol/pajak & hadiah
diplomasi. 14 traktat ditemukan, termasuk RANGKAIAN pelepasan diri pantai
barat dari Atjeh (Indrapoura 1663, Sillida 1667, Barus 1668, Priaman 1671,
Cinkel/Singkil 1672) -- pola bahasa berulang "onverdraeglijck jock" (kuk tak
tertahankan) di semua traktat ini. TEMUAN BESAR: traktat Barus 29 April 1668
mundurkan bukti hubungan Aceh-Barus dari 1681 (13 tahun lebih awal) --
caveat lama "Barus nihil sampai 1681" WAJIB direvisi. Sama pola tag notes
spt CD1 ("SUMBER: Corpus Diplomaticum jilid II").

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
    Path("/app/data/research/atjeh_trade.csv"),
    _BASE / "data" / "research" / "atjeh_trade.csv",
]
CSV_FILE = next((c for c in CSV_CANDIDATES if c.exists()), None)

ALLOWED_SOURCE_DOCUMENTS = {"1643-1644", "1631-1634", "1637", "1636", "1624-1629", "1644-1645", "1647-1648", "1656-1657", "1659", "CD1", "CD2"}

ALLOWED_DIRECTIONS = {"naar_atjeh", "van_atjeh", "in_atjeh", "politik"}
# "politik": fakta politik/administratif Atjeh (klaim yurisdiksi, penegakan tol,
# suksesi raja, status ratu, dst) -- BUKAN transaksi dagang. Dipisah dari
# "in_atjeh" 2026-07-13 supaya "in_atjeh" murni transaksi yg terjadi di Atjeh
# lagi, bukan bucket ganda dagang+politik. Lihat feedback_sisir_semua_titik_pemakaian.


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
    source_document = _clean(row.get("source_document"))
    if source_document not in ALLOWED_SOURCE_DOCUMENTS:
        raise ValueError(f"source_document '{source_document}' tidak valid, harus salah satu dari {ALLOWED_SOURCE_DOCUMENTS}")

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
        "source_document": source_document,
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
        raise RuntimeError(f"atjeh_trade.csv tidak ditemukan di: {CSV_CANDIDATES}")
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
        by_document = session.execute(text(
            "SELECT source_document, COUNT(*) FROM atjeh_trade_records GROUP BY source_document ORDER BY source_document"
        )).all()

    print("=" * 60)
    print(f"atjeh_trade_records: {after} baris")
    print(f"per arah: {dict(by_direction)}")
    print(f"per volume: {dict(by_document)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
