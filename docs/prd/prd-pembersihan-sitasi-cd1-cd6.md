# Workflow — Pembersihan Sitasi Corpus Diplomaticum (CD1-CD6)

Status: selesai · 2026-07-17

## Masalah

`/linimasa` dan `/riset/atjeh-dagang` menampilkan kode file scan internal
("CD1.pdf".."CD6.pdf") langsung ke pengunjung, alih-alih judul buku asli:

- Kolom `notes` (140 baris total di `linimasa_events.csv` + `atjeh_trade.csv`)
  menyimpan literal `"...Corpus Diplomaticum (CD1.pdf)..."` — nama file scan
  bocor ke teks sitasi yang tampil di halaman.
- Kolom `source_document` (`"CD1"`.."CD6"`) ditampilkan mentah sbg
  `"vol. CD1"` di kartu peristiwa/tabel dagang, bukan judul buku.
- Footer `/linimasa` mengklaim co-editor "G.K. Niemeijer" yang tak bisa
  dilacak sumbernya (PDF asli CD1-CD6 tidak ada di repo utk verifikasi
  halaman judul persis) — dihapus, disepakati user.
- Warning "Belum diverifikasi silang" (`confidence_flag=unverified`) dicek:
  akurat, tidak ada baris manapun yang pernah diverifikasi silang manual thd
  scan asli — dibiarkan apa adanya, TIDAK diubah.

## Solusi (reusable, TDD)

`backend/citation_cleaning.py` — dua fungsi:
- `cd_source_label(source_document)`: `"CD1"`→`"Corpus Diplomaticum
  Neerlando-Indicum, Jilid I"` dst; nilai non-CD (mis. `"1624-1629"`,
  volume Dagh-register) dibiarkan apa adanya.
- `clean_cd_citation(notes)`: strip `"(CDn.pdf)"` dari teks `notes`, ganti
  jadi judul buku lengkap + jilid yang benar. CD1 satu-satunya yang di data
  mentah tak menyertakan label "jilid I" sama sekali — ditangani.

Diuji `backend/tests/test_citation_cleaning.py` (9 test, sampel nyata dari
CSV) SEBELUM implementasi (RED → GREEN).

## Penerapan

1. `data/research/linimasa_events.csv` + `atjeh_trade.csv`: kolom `notes`
   dibersihkan (70 baris/file), lalu reseed (`seed_linimasa_events.py`,
   `seed_atjeh_trade.py`) — row count tidak berubah (101 + 152), cuma isi
   `notes`. Backup diambil dulu sebelum overwrite.
2. `frontend/map_app/views.py`: `CD_JILID` dict + `cd_source_label()` (duplikat
   kecil dari backend, sengaja — hindari cross-app import rapuh), dipakai
   utk isi `source_label` per event SEBELUM di-render/di-JSON-kan.
3. `linimasa.html`: `{{ r.source_document }}` → `{{ r.source_label }}` di
   kedua kartu (biasa + treaty-highlight) dan panel detail JS
   (`ev.source_label || ev.source_document`, fallback aman).
4. `riset_atjeh.html`: mapping JS `CD_JILID`/`sourceLabel()` setara, dipakai
   di kolom tabel "Volume" — filter dropdown TETAP pakai kode mentah
   (`r.source_document===doc`), cuma tampilan yang diubah.
5. Footer `/linimasa`: hapus klaim "G.K. Niemeijer" yang tak terverifikasi,
   pertahankan "ed. J.E. Heeres, dkk." yang konsisten catatan sejarah standar.

## Regression guard permanen

`backend/tests/test_citation_no_leaks.py` — baca CSV langsung (tanpa DB),
gagal keras kalau ada baris baru masuk dgn `.pdf` di `notes` tanpa lewat
`clean_cd_citation()` dulu. Pola sama `test_corpus_no_leaks.py` (Sprint
pembersihan Daghregister/GLOBALISE sebelumnya).

## Verifikasi

- `docker compose exec backend pytest -q` → 418 passed, 41 skipped.
- `docker compose exec frontend python manage.py test map_app` → 156 passed.
- `curl localhost:8084/linimasa/` → 0 kemunculan `.pdf`/`Niemeijer`, 282
  kemunculan sitasi jilid I-VI yang benar (22/60/72/80/16/32 per jilid).
- Playwright: kartu Dagh-register tetap tampil `vol. 1624-1629` (tidak
  ikut berubah, benar), kartu CD tampil `vol. Corpus Diplomaticum
  Neerlando-Indicum, Jilid I` dst. Badge "Belum diverifikasi silang" masih
  ada (akurat, sesuai keputusan — tidak ada verifikasi silang yang
  benar-benar terjadi).

## Di luar cakupan (sengaja tidak disentuh)

- `confidence_flag`/badge verifikasi — tidak diubah, karena belum ada
  verifikasi silang nyata yang terjadi utk baris manapun.
- Tampilan mentah `confidence_flag: {{ r.confidence_flag }}` di kartu
  (terlihat spt debug output) — di luar scope permintaan ini, belum diminta.
- Judul/tahun terbitan persis per jilid (mis. tahun cetak BKI) — PDF sumber
  tak ada di repo utk verifikasi halaman judul asli; kalau user punya akses
  fisik PDF, bisa dikonfirmasi & diupdate terpisah.
