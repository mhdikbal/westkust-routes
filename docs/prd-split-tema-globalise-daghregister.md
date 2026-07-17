# PRD — Pisah Tampilan Tema Korpus: Dagh-register vs GLOBALISE

Status: in-progress · 2026-07-17

## Latar Belakang

`/riset/tema` saat ini menggabungkan dua korpus dengan sifat berbeda ke satu
Sankey (dekade→tema→pelabuhan):

- **Dagh-register Batavia** — narasi peristiwa harian, kutipan asli pendek
  (~2.7KB), cocok dibaca sebagai "kutipan sumber primer".
- **GLOBALISE (Huygens ING)** — metadata katalog/finding-aid arsip VOC
  (deskripsi inventaris, bukan narasi kejadian). `text_asli` untuk baris ini
  BUKAN kutipan — sudah diganti pointer sitasi oleh `slim_corpus_for_db.py`
  (`docs/thesis/dr/slim_corpus_for_db.py:110-121`).

Menyajikan keduanya sebagai satu jenis "peristiwa" di panel yang sama
menyesatkan: entri katalog GLOBALISE dibaca seolah kutipan mata-saksi. Setelah
diskusi (lihat riwayat sesi), diputuskan:

1. Dua halaman/route terpisah (bukan tab di satu halaman).
2. Sankey gabungan **dihapus** — diganti sepenuhnya oleh dua tampilan baru.
3. Halaman GLOBALISE diberi label **"Petunjuk Arsip" / "Indeks Katalog"**
   (bukan "Sankey tema" generik) untuk menegaskan sifatnya sebagai finding-aid,
   bukan narasi.

## Keputusan Desain

| | Dagh-register (existing URL) | GLOBALISE (baru) |
|---|---|---|
| Route | `/riset/tema/` (tetap, tak berubah) | `/riset/petunjuk-arsip/` |
| View/template | `riset_tema.html` (di-retrofit) | `riset_petunjuk_arsip.html` (baru) |
| Framing | "Sankey tema" narasi peristiwa | "Petunjuk Arsip" / "Indeks Katalog" |
| Sumber data | `corpus_asal=daghregister` | `corpus_asal=globalise` |
| Detail per-baris | kutipan `text_asli` asli (Belanda pendek) | sitasi arsip (`inventaris_ref`), bukan kutipan |
| Badge korpus per-kartu | dihapus (single-corpus, jadi redundan) | dihapus (idem) |

URL `/riset/tema/` dipertahankan (bukan diganti) supaya tidak breaking link
lama — cukup konten & framing di-retrofit jadi Dagh-register-only.

## Perubahan Backend

`backend/routers/research.py`:
- `GET /sankey-tema/triples` — tambah query param opsional
  `corpus_asal: Literal["daghregister","globalise"]`. Filter diterapkan
  di Python (bukan SQL WHERE) di loop agregasi yang sudah ada — pola sama
  dengan filter `tema` di `get_network_pelabuhan`. Alasan: endpoint ini
  fetch seluruh tabel tanpa filter SQL sama sekali, dan filtering Python
  membuatnya unit-testable lewat mock DB yang ada (mock mengabaikan klausa
  WHERE, cuma meneruskan `rows` mentah).
- `GET /sankey-tema/rows` — tambah query param opsional `corpus_asal` sama,
  filter di Python bersamaan dengan filter `pelabuhan` yang sudah ada
  (post-fetch, sebelum pagination slice).
- Cache key (`make_key`) di kedua endpoint diperbarui menyertakan
  `corpus_asal` agar tak ada cache collision antar dua halaman.

Endpoint lama `/sankey-tema` (non-triples, dipakai entah oleh siapa —
grep dulu sebelum dianggap mati) TIDAK diubah untuk PRD ini (di luar
cakupan; halaman yang pakai hanya `/triples`).

## Perubahan Frontend (Django)

- `frontend/map_app/templates/map_app/riset_tema.html` — retrofit:
  fetch `?corpus_asal=daghregister`, hapus semua copy/statistik campuran
  GLOBALISE (`prov`, footer tag `sumber:`), hapus badge korpus per-kartu,
  tambah link nav ke halaman Petunjuk Arsip.
- `frontend/map_app/templates/map_app/riset_petunjuk_arsip.html` — baru,
  disalin dari struktur `riset_tema.html` tapi:
  - Judul & lede reframe sebagai indeks katalog arsip, bukan narasi.
  - Kotak penjelas: ini finding-aid GLOBALISE/Huygens, bukan kutipan
    peristiwa — link ke `/riset/tema/` untuk narasi Dagh-register.
  - Detail drill-down: label "sitasi arsip" bukan "teks asli", karena
    `text_asli` sudah berupa pointer sitasi (bukan OCR).
  - footer tag: `sumber: GLOBALISE (Huygens ING)`.
- `frontend/map_app/urls.py` — tambah `path("riset/petunjuk-arsip/", ...,
  name="riset_petunjuk_arsip")`.
- `frontend/map_app/views.py` — tambah view `riset_petunjuk_arsip` (statis,
  render saja — pola sama `riset_tema`/`riset_jaringan`).
- Nav cross-link 3 file (`linimasa.html`, `riset_jaringan.html`,
  `riset_atjeh.html`): ganti satu link "Sankey tema" jadi dua link
  terpisah ("Tema Dagh-register" + "Petunjuk arsip").

## Testing (TDD wajib per CLAUDE.md)

- `backend/tests/test_research_triples.py` — RED test dulu: kirim rows
  campuran `corpus_asal`, assert hanya subset yang cocok filter muncul
  di triples & meta (`n_dagh`/`n_glob`/`total` konsisten dgn subset).
- `backend/tests/test_research_drilldown.py` — RED test dulu: kirim rows
  campuran corpus_asal, assert `?corpus_asal=globalise` cuma
  mengembalikan baris itu.
- `frontend/map_app/tests.py` — Django `TestCase` utk view baru
  `riset_petunjuk_arsip` (status 200, template dipakai benar).

## Verifikasi

- `docker compose exec backend pytest -v` → semua hijau.
- `docker compose exec frontend python manage.py test map_app` → hijau.
- `docker compose up -d --build backend frontend`.
- `curl http://localhost:8084/riset/tema/` dan
  `curl http://localhost:8084/riset/petunjuk-arsip/` → 200.
- `curl 'http://localhost:8084/api/research/sankey-tema/triples?corpus_asal=daghregister'`
  → meta.n_glob harus 0.
- Playwright: screenshot kedua halaman, klik satu link Sankey di tiap
  halaman, pastikan panel drill-down cuma menampilkan baris korpus yang
  relevan.
