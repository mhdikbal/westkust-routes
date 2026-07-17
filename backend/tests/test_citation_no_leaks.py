"""
test_citation_no_leaks.py — regression guard permanen: pastikan
data/research/linimasa_events.csv dan atjeh_trade.csv tidak pernah lagi
kemasukan nama file scan mentah ("CD1.pdf".."CD6.pdf") di kolom `notes`.

Lihat backend/citation_cleaning.py -- data ini pernah bocor & sudah
dibersihkan (2026-07-17). Test ini mencegah kebocoran itu balik lagi diam-diam
kalau CSV di-regenerate/ditambah baris baru tanpa lewat citation_cleaning.py.

Pure CSV read, tidak butuh DB -- cepat, bisa jalan di CI.
"""
import csv
import os
from pathlib import Path

csv.field_size_limit(10**9)

def _resolve(name):
    """/app/... di dalam container (backend/ = /app), fallback ke path relatif
    repo kalau dijalankan di host -- pola sama test_corpus_no_leaks.py."""
    candidates = [
        Path("/app/data/research") / name,
        Path(__file__).resolve().parents[2] / "data" / "research" / name,
    ]
    return next((c for c in candidates if c.exists()), candidates[0])


_CSV_FILES = [_resolve("linimasa_events.csv"), _resolve("atjeh_trade.csv")]


def _load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_csv_files_exist():
    for path in _CSV_FILES:
        assert path.exists(), f"tidak ditemukan: {path}"


def test_no_pdf_filename_leak_in_notes():
    for path in _CSV_FILES:
        rows = _load_rows(path)
        leaked = [r.get("id") or r.get("source_page") for r in rows if ".pdf" in (r.get("notes") or "")]
        assert not leaked, (
            f"{len(leaked)} baris di {path.name} masih menyimpan nama file scan mentah "
            f"'.pdf' di kolom notes -- kemungkinan baris baru ditambah tanpa lewat "
            f"citation_cleaning.clean_cd_citation(). Baris: {leaked[:5]}"
        )
