"""
corpus_cleaning.py — deteksi & bersihkan kebocoran scan pada kolom `text` di
data/research/korpus_tema_slim.csv (sumber tabel research_theme_rows).

Lihat docs/prd/prd-pembersihan-korpus-daghregister.md untuk konteks lengkap.
Dua sub-korpus punya pola kebocoran BERBEDA -- jangan pakai logika yang sama:

- corpus_asal='daghregister': nomor halaman + header tanggal fisik buku scan
  bocor ke baris-baris awal, urutannya TIDAK konsisten (kadang nomor dulu lalu
  tanggal, kadang tanggal dulu lalu nomor, kadang tanggal+nomor digabung satu
  baris, kadang cuma tanggal tanpa nomor terlihat) -- OCR membaca kolom/margin
  halaman asli dengan urutan yang bervariasi. Narasi asli ada SETELAH baris
  pembuka ini, bisa diselamatkan dgn strip baris-baris pembuka (header_leak).
- corpus_asal='globalise': seluruh baris pada dasarnya deskripsi katalog/
  inventaris arsip (bukan narasi peristiwa), diawali kata "Register", nomor
  folio polos, atau rentang nomor inventaris. Tidak ada narasi tersembunyi
  utk diselamatkan (non_narrative) -- kandidat exclude/flag, bukan strip.

CATATAN SCOPE: sebagian baris yang berhasil di-strip header-nya tetap punya
narasi yang "berantakan" (satu kata per baris) -- itu masalah OCR pembacaan
kolom halaman asli yang TERPISAH dari kebocoran header/nomor halaman, dan
TIDAK ditangani modul ini. Laporan tetap menyertakan baris ini apa adanya
utk direview manusia.
"""
import re

_MONTHS = (
    r"januari|februari|maret|april|mei|mey|juni|juny|juli|"
    r"agustus|september|oktober|november|desember"
)

# Baris (atau gabungan nomor+tanggal satu baris) yang mengandung angka di awal
# dan nama bulan dlm rentang pendek -- menangkap kedua urutan (nomor-lalu-
# tanggal ATAU tanggal-lalu-nomor digabung) dan variasi ejaan arkais/OCR
# (mis. "JUNY", "MEY", konektor "dan"/"ex"/"-" utk tanggal majemuk).
_HEADER_ISH_RE = re.compile(
    rf"^\d{{1,5}}\b.{{0,45}}?\b(?:{_MONTHS})\b.{{0,15}}$", re.IGNORECASE
)

# Penanda halaman indeks/TOC -- berlaku lintas corpus_asal (bukan cuma
# daghregister), krn ini indikator generik "ini indeks, bukan narasi",
# terlepas dari sumbernya.
_INDEX_MARKERS = (
    "DAFTAR NAMA", "DAFTAR ISI", "REGISTER NAMA", "REGISTER DARI NAMA", "REGISTER VON",
)

_GLOBALISE_CATALOG_RE = re.compile(
    r"^register\b"
    r"|^\d{4}-\d{2,4}(?:/\d)?\."
    r"|^\d{3,4}(?:\s+[a-z]\b)?\s*(?:s\.d\.|sampai|[-–])",
    re.IGNORECASE,
)
# GLOBALISE = katalog/inventaris arsip sepenuhnya (bukan narasi peristiwa) --
# nomor folio polos di baris pertama (diikuti baris kosong/konten katalog)
# terbukti 100% non_narrative pd audit manual (22/22 sampel dicek), beda dgn
# daghregister yg nomor halamannya diikuti NARASI asli di baris berikutnya.
_GLOBALISE_BARE_FOLIO_RE = re.compile(r"^\d{1,5}[ \t\xa0]*\n")


def detect_leak(text: str, corpus_asal: str) -> str:
    """Klasifikasi kebocoran scan. Return 'clean' | 'header_leak' | 'non_narrative'."""
    text = text or ""

    lines = text.split("\n")
    line0 = lines[0].strip() if lines else ""
    line1 = lines[1].strip() if len(lines) > 1 else ""

    if any(l.upper().startswith(marker) for l in (line0, line1) for marker in _INDEX_MARKERS):
        return "non_narrative"

    if corpus_asal == "globalise":
        if _GLOBALISE_CATALOG_RE.match(line0) or _GLOBALISE_BARE_FOLIO_RE.match(text):
            return "non_narrative"
        return "clean"

    # daghregister (dan default lainnya)
    if _HEADER_ISH_RE.match(line0):
        return "header_leak"
    if line0.isdigit() and _HEADER_ISH_RE.match(line1):
        return "header_leak"
    return "clean"


def strip_header_leak(text: str) -> str:
    """Hapus baris-baris pembuka (nomor halaman &/atau header tanggal, dlm
    urutan apapun) sampai baris pertama yang bukan salah satu dari itu.
    Dibatasi 4 baris pertama sbg pengaman -- kalau tak ketemu narasi dlm 4
    baris, kemungkinan bukan header_leak yg valid, kembalikan apa adanya
    supaya tidak diam-diam menghapus konten. Hanya dipanggil utk baris
    berkategori 'header_leak' -- panggil detect_leak() dulu."""
    lines = (text or "").split("\n")
    i = 0
    while i < len(lines) and i < 4:
        line = lines[i].strip()
        if line == "" or line.isdigit() or _HEADER_ISH_RE.match(line):
            i += 1
            continue
        break
    return "\n".join(lines[i:]).strip()
