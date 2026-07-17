"""
test_corpus_no_leaks.py — regression guard permanen: pastikan
data/research/korpus_tema_slim.csv (sumber research_theme_rows) tidak
pernah lagi kemasukan kebocoran scan (nomor halaman/header tanggal/
entri katalog arsip) di kolom `text`.

Lihat docs/prd-pembersihan-korpus-daghregister.md -- data ini pernah
bocor & sudah dibersihkan (Sprint 2, 2026-07-17). Test ini mencegah
kebocoran itu balik lagi diam-diam kalau CSV di-regenerate dari pipeline
docs/thesis/dr/ tanpa melewati corpus_cleaning.py lagi.

Pure CSV read, tidak butuh DB -- cepat, bisa jalan di CI.
"""
import csv
import os
import sys
from pathlib import Path

csv.field_size_limit(10 ** 9)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from corpus_cleaning import detect_leak

# Dua kandidat spt seed_research_tema.py -- /app/... di dalam container
# (backend/ = /app), fallback ke path relatif repo kalau dijalankan di host.
_CSV_CANDIDATES = [
    Path("/app/data/research/korpus_tema_slim.csv"),
    Path(__file__).resolve().parents[2] / "data" / "research" / "korpus_tema_slim.csv",
]
_CSV_FILE = next((c for c in _CSV_CANDIDATES if c.exists()), _CSV_CANDIDATES[0])


def _load_rows():
    with _CSV_FILE.open(newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def test_csv_file_exists():
    assert _CSV_FILE.exists(), f"tidak ditemukan: {_CSV_FILE}"


def test_no_header_leak_or_non_narrative_rows_remain():
    rows = _load_rows()
    assert rows, "korpus_tema_slim.csv kosong -- kemungkinan bug baca file"

    leaked = []
    for row in rows:
        kategori = detect_leak(row.get("text", "") or "", corpus_asal=row.get("corpus_asal", ""))
        if kategori != "clean":
            leaked.append((row.get("corpus_id"), kategori, (row.get("text") or "")[:60]))

    assert not leaked, (
        f"{len(leaked)} baris terdeteksi bocor lagi di korpus_tema_slim.csv -- "
        f"kemungkinan CSV di-regenerate dari pipeline tanpa lewat corpus_cleaning.py. "
        f"Contoh: {leaked[:5]}"
    )


def test_row_count_matches_last_known_clean_state():
    # Baseline setelah Sprint 2+lanjutan (2026-07-17): 902 baris. Test ini
    # BUKAN utk melarang jumlah berubah selamanya (korpus boleh tumbuh saat
    # riset dilanjutkan) -- ini alarm supaya perubahan jumlah baris (naik
    # ATAU turun) diperiksa sengaja, bukan efek samping tak disadari dari
    # re-generate CSV yg lupa lewat cleaning.
    rows = _load_rows()
    assert len(rows) == 902, (
        f"Jumlah baris korpus_tema_slim.csv berubah dari baseline 902 -> {len(rows)}. "
        "Kalau ini perubahan yang disengaja (mis. korpus diperluas), update angka "
        "baseline test ini. Kalau tidak disengaja, cek apakah CSV ter-regenerate "
        "dari pipeline mentah tanpa lewat corpus_cleaning.py."
    )
