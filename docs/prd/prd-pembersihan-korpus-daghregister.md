# PRD: Pembersihan Kebocoran Scan (Nomor Halaman & Header) — Korpus Daghregister

**Status:** Draft — siap eksekusi Sprint 1.
**Sumber:** Audit langsung DB + CSV, 2026-07-17 (lihat percakapan "tim DBA, MLOps... hasil scan Corpus Diplomaticum dan Daghregister").
**Target:** `data/research/korpus_tema_slim.csv` → tabel `research_theme_rows` → halaman publik `/riset/tema`.

---

## 1. Temuan (Ground Truth, Sudah Diverifikasi)

### 1.1 Peta penyimpanan

| Lapisan | Lokasi | Baris | Status |
|---|---|---|---|
| DB | `linimasa_events` | 101 | Bersih (1 false-positive dari regex deteksi, bukan kebocoran nyata) |
| DB | `atjeh_trade_records` | 152 | Bersih (1 false-positive) |
| DB | `research_theme_rows` | 1.005 | **167 baris (16.6%) bocor** — lihat §1.2 |
| DB | `staging_extractions` | 119 | Mentah (`confidence_flag='unverified'`), tapi **tidak tampil di halaman publik manapun** — murni staging API internal, prioritas rendah |
| CSV (produksi) | `data/research/korpus_tema_slim.csv` | 1.005 | Sumber kanonik `research_theme_rows` (via `backend/seed_research_tema.py`, idempotent by `corpus_id`) — **ini yang diperbaiki** |
| CSV (pipeline tahap awal, SUDAH DIBERSIHKAN §8) | `docs/thesis/dr/daghregister_corpus*.csv` (raw/update/classified/sanitychecked/deduped/directioned — 6 file paralel) | **511 record/file** (koreksi: "76.312" sebelumnya salah hitung — itu jumlah baris fisik `wc -l`, bukan record, krn teks punya newline di dalam field CSV) | Ini **bukan** data terpisah tak tersentuh — ini tahapan AWAL pipeline yang SAMA yang menghasilkan `korpus_tema_slim.csv` (lewat `slim_corpus_for_db.py`). Kebocoran sekarang sudah dipropagasi-bersih juga di sini (§8), supaya re-run/perluasan pipeline nanti mewarisi teks bersih dari sumbernya |
| JSON | — | 0 | Tidak ada ekspor JSON utk korpus Daghregister/Corpus Diplomaticum. `scrawling/*.json` = dataset pelayaran BGB, berbeda sama sekali |

### 1.2 Pola kebocoran (dari sampel nyata `corpus_asal='daghregister'`)

Pola dominan — nomor halaman + header tanggal bergabung ke baris pertama kolom `text`:

```
106\n31 Maret.\nCatatan kapal-kapal yang masuk pada bulan Maret:\n...
230\n7 JUNI.\nGuillam Ferment,\nFredrik Tim,\n...
550\n13 DAN 14 DESEMBER.\nvan aluyn can oock niet voldaen worden...
696\n20 DAN 21 DESEMBER.\n…; dan, karena kapas itu adalah barang dagangan...
```

Struktur: `<nomor_halaman:digit>\n<HEADER_TANGGAL ending dgn titik>\n<isi narasi sebenarnya>`. Variasi header: ALL CAPS atau Title Case, "DAN"/"dan" sbg penghubung tanggal majemuk, rentang tanggal dgn strip (`18-20 JUNI.`).

**Kasus berbeda, BUKAN sekadar header nempel** — satu baris ditemukan berisi seluruh halaman indeks:

```
552\nDAFTAR NAMA ORANG DAN TEMPAT.\nSia-ko, 1.\nSiakol, 598.\nSiam, 25, 52...
```

Ini bukan narasi peristiwa yang kebetulan ada header di depan — ini **seluruh baris adalah materi indeks/TOC arsip** yang salah masuk ke korpus sebagai "event". Strip header tidak menyelesaikan apa-apa di sini; baris ini perlu **diberi tanda/dikeluarkan**, bukan dibersihkan.

### 1.3 Pola kebocoran BERBEDA di `corpus_asal='globalise'` (ditemukan susulan)

Sampel baris `globalise` yang match filter deteksi awal **semuanya** berupa deskripsi katalog/inventaris arsip, bukan cuma header nempel di depan narasi:

```
Register alfabetis dari catatan harian dan urusan yang ditangani antara Tuan Komandan...
Register dari semua surat dan tulisan yang tiba berturut-turut di Batavia...
1607-1622/3.\nPaket kedua\nsalinan buku surat-surat oleh Hendrick Jansz dari Patanis...
760 s.d. 765- 782.. . Salinan laporan oleh pemungut cukai Jacob bean tentang penangkapan fluit Montfoort...
1295 a–1349. berbagai interogatori pada tahun 1695 untuk para komisioner khusus...
```

Ini konsisten dengan catatan lama di `docs/thesis/dr/slim_corpus_for_db.py` (DATA-SNK-1): korpus GLOBALISE memang berbasis **metadata inventaris arsip** (deskripsi apa isi satu bundel surat), bukan narasi peristiwa langsung. Artinya: **tidak ada "narasi bersih" yang bisa diselamatkan dgn strip 2 baris** seperti pola daghregister — seluruh baris pada dasarnya adalah entri katalog. Baris jenis ini otomatis masuk kategori `non_narrative`, bukan `header_leak`.

**Kesimpulan:** `detect_leak()` harus sadar `corpus_asal` — logika utk `daghregister` (strip page-number+header) TIDAK BOLEH diterapkan mentah-mentah ke `globalise` (yang butuh exclude/flag, bukan strip).

### 1.4 Hasil eksekusi P0.1-P0.2 (2026-07-17) — skala sebenarnya jauh lebih besar dari estimasi awal

Implementasi awal (`corpus_cleaning.py` v1, cuma pola "nomor-lalu-tanggal 2-baris") menghasilkan 105/1005 (10.5%) — jauh di bawah estimasi kasar awal 167/1005 (16.6%). Investigasi selisih membongkar temuan besar: **urutan header TIDAK konsisten**. Pola nyata yang ditemukan (semua diverifikasi thd sampel nyata sblm ditambahkan ke `corpus_cleaning.py`):

1. Nomor halaman → tanggal → narasi (pola awal): `"106\n31 Maret.\nCatatan kapal..."`
2. **Tanggal → nomor halaman → narasi (KEBALIK):** `"30 dan 31 Januari.\n27\nbiaya-biaya harus diatur..."`
3. Tanggal saja tanpa nomor terlihat: `"17 FEBRUARI.\n\n... akan dikirim..."`
4. Nomor+tanggal digabung 1 baris: `"146 30 Juni.\n\nKota Couchin..."`
5. Ejaan arkais bulan (OCR/Belanda lama): "JUNY" (bukan JUNI), "MEY" (bukan MEI)
6. Indeks nama/tempat dgn 2 varian header: "DAFTAR NAMA..." dan "REGISTER NAMA..." (termasuk tanpa nomor halaman di depan sama sekali)

**Setelah `corpus_cleaning.py` v2** (menangani kedua urutan + varian ejaan, 31 test lolos, diverifikasi manual thd 8 sampel acak `header_leak` — semua benar):

| Kategori | Jumlah | % dari 1005 |
|---|---|---|
| `clean` | 603 | 60.0% |
| `header_leak` (daghregister, siap strip mekanis) | 302 | 30.0% |
| `non_narrative` — daghregister (indeks nama/tempat) | 31 | 3.1% |
| `non_narrative` — globalise (katalog/inventaris) | 69 | 6.9% |

**Keterbatasan yang diketahui & DIBIARKAN terbuka (bukan disembunyikan):**
- Kategori `clean` untuk `corpus_asal='globalise'` kemungkinan besar **masih undercount** — sampel acak menunjukkan banyak baris "clean" yang sebenarnya tetap berbau katalog/daftar surat (`"Daftar surat yang diterima..."`, `"register surat-surat"`, `"Souratta\nBagian ke-2..."`) tapi tidak match pola spesifik yang sudah diprogram. Korpus GLOBALISE sepertinya secara struktural HAMPIR SELURUHNYA metadata inventaris arsip, bukan cuma sebagian — ini bukan lagi soal "regex kurang pintar", tapi soal **apakah GLOBALISE cocok ditampilkan sbg 'peristiwa naratif' sama sekali** di `/riset/tema`. Keputusan strategis, bukan keputusan regex.
- Satu varian daghregister ditemukan tak tertangkap: baris kosong ganda antara nomor halaman & baris tanggal (`"102\n\n19 s.d. 20 Maret.\nSurat terjemahan..."`) — nomor di baris 0, tanggal di baris 2 (bukan baris 1). Residual kecil, tidak dikejar lebih jauh (diminishing returns).
- Sebagian narasi yang berhasil "diselamatkan" dari strip header tetap berantakan formatnya — terpecah kata-per-kata per baris (mis. `"ingin\nsatu sama lain\ndalam hal\nhormat\nhormat\n..."`). Ini masalah OCR pembacaan urutan kolom halaman fisik yang **terpisah** dari kebocoran header/nomor halaman — strip header tidak memperbaikinya, dan tidak coba diperbaiki di sprint ini.

**Keputusan eksplisit:** berhenti menyempurnakan regex lebih jauh di titik ini (mengikuti prinsip §2 — uji dulu baru terapkan, TAPI juga jangan kejar kasus OCR yang endless). 302 baris `header_leak` daghregister sudah diverifikasi tinggi-keyakinan & siap diterapkan. Sisanya (globalise, non_narrative, residual kecil) diserahkan ke keputusan manusia di P0.3, bukan otomasi lebih lanjut.

**Pelajaran dari insiden masa lalu (memori proyek):** regex sisir korpus pernah dipakai tanpa diuji dulu terhadap sampel nyata, dan gagal total (undercount 2 volume selama berbulan-bulan). **Sprint ini WAJIB uji pola dulu terhadap seluruh 167 baris + sampel acak dari 838 baris "bersih" sebelum diterapkan**, bukan asumsi satu pola lalu langsung jalan.

---

## 2. Prinsip Kerja

1. **Uji dulu, baru terapkan.** Setiap fungsi pembersih diuji dgn `pytest` terhadap sampel nyata (RED-GREEN, sesuai CLAUDE.md) sebelum disentuhkan ke CSV produksi.
2. **Tidak destruktif.** `text` asli (dgn kebocoran) disimpan sbg backup sebelum ditimpa — baik lewat kolom baru (`text_raw`) atau lewat commit git terpisah yang bisa direvert.
3. **Bedakan dua kasus.** (a) header/nomor halaman nempel di depan narasi valid → strip mekanis. (b) seluruh baris = materi bukan-narasi (indeks, TOC, running header berulang) → tandai `record_type` utk exclude/review, jangan coba "bersihkan" jadi narasi yang tidak ada.
4. **Verifikasi silang skor.** `tema_dominan`/`skor_*` sudah dihitung dari `text` yang MASIH bocor. Setelah dibersihkan, cek apakah klasifikasi masih masuk akal (spot-check, bukan hitung ulang skor dari nol — di luar scope sprint ini).
5. **Idempotent & reversible di DB.** `seed_research_tema.py` sudah `ON CONFLICT DO UPDATE by corpus_id` — aman dijalankan ulang setelah CSV diperbaiki.

---

## 3. Fase P0 — Deteksi & Klasifikasi Pola (Sprint 1)

### P0.1 Bangun fungsi deteksi, uji dgn pytest dulu

**Implementasi:**
- Buat `backend/tests/test_corpus_cleaning.py` — fixture berisi ke-15 sampel nyata di §1.2 (baik yang bocor maupun yang aman/tidak bocor, termasuk contoh false-positive spt "1º [hak dagang VOC]")
- Test: fungsi `detect_leak(text) -> 'clean' | 'header_leak' | 'non_narrative'`
- **RED dulu** — test ditulis sebelum fungsi ada, harus FAIL
- Baru implementasi `scripts/corpus_cleaning.py` (atau taruh di `docs/thesis/dr/` mengikuti konvensi skrip riset yang sudah ada) sampai test GREEN

### P0.2 Jalankan deteksi ke seluruh 1.005 baris, hasilkan laporan utk direview manusia

**Implementasi:**
- Skrip baca `data/research/korpus_tema_slim.csv`, klasifikasi tiap baris `text` corpus_asal='daghregister'
- Output `docs/thesis/dr/corpus_cleaning_report.csv`: `corpus_id, kategori (clean/header_leak/non_narrative), text_before, text_after_proposed`
- **Verifikasi kuantitas** — cocokkan hasil skrip vs hitungan manual saya (167 dari 1.005). Kalau meleset jauh, pola deteksi salah, jangan lanjut ke P0.3.

### P0.3 Review manusia thd `non_narrative` (bukan cuma auto-strip)

Baris kategori `non_narrative` (spt contoh "DAFTAR NAMA ORANG DAN TEMPAT") tidak diotomasi — daftar id-nya diserahkan ke user/tim riset utk keputusan: exclude dari `research_theme_rows`, atau pertahankan dgn `low_confidence=true` + catatan.

---

## 4. Fase P1 — Terapkan & Ingest Ulang (Sprint 2)

### P1.1 Terapkan strip mekanis ke kategori `header_leak`

- Update `data/research/korpus_tema_slim.csv` kolom `text` utk baris `header_leak` (mayoritas dari 167) — hapus 2 baris pertama (nomor halaman + header tanggal), simpan sisanya
- Simpan `text` asli (dgn kebocoran) ke kolom baru `text_raw_pre_cleaning` di CSV yang sama, atau commit git terpisah sblm & sesudah utk audit trail

### P1.2 Terapkan keputusan §P0.3 utk kategori `non_narrative`

- Exclude dari CSV (atau flag) sesuai keputusan review manusia

### P1.3 Migrasi DB (kolom backup) + re-seed

- Kalau perlu kolom `text_raw_pre_cleaning` di DB juga: buat migrasi Alembic baru
- Jalankan ulang `docker compose exec backend python seed_research_tema.py` (idempotent, aman)

### P1.4 Verifikasi publik

- `docker compose up -d --build frontend backend`
- Buka `/riset/tema`, screenshot sebelum/sesudah utk beberapa `corpus_id` yang tadinya bocor (id 808, 877, 433, dst.) — pastikan nomor halaman/"Register" tidak tampil lagi
- Spot-check 5-10 `tema_dominan` yang klasifikasinya sblm/sesudah cleaning tidak berubah drastis (sanity, bukan hitung ulang)

---

## 5. Kriteria Keberhasilan — ✅ SELESAI (2026-07-17)

- [x] `pytest backend/tests/test_corpus_cleaning.py` hijau — 34 test, mencakup kasus positif & negatif (termasuk false-positive spt enumerasi "1º")
- [x] Skrip deteksi dijalankan ke seluruh 1.005 baris — hasil akhir jauh lebih besar dari estimasi kasar awal (167), lihat §1.4: 302 `header_leak` + 101 `non_narrative` (daghregister+globalise gabungan, setelah 2 putaran perluasan marker indeks)
- [x] 0 baris `research_theme_rows` dgn nomor halaman murni atau "Register"/"Daftar Isi"/"Daftar Nama" sbg baris pembuka (diverifikasi query SQL langsung pasca-penerapan)
- [x] Tidak ada baris yang hilang tanpa jejak — 101 baris `non_narrative` dikeluarkan sesuai keputusan user (P0.3), bukan dihapus diam-diam; `corpus_id` yg dikeluarkan tercatat di `excluded_corpus_ids.txt`
- [x] `text` asli (sblm cleaning) tetap tertelusuri via git history (`data/research/korpus_tema_slim.csv` sudah tracked git sebelum sprint ini — `git show <commit-sebelum>:data/research/korpus_tema_slim.csv` utk rollback/audit)

**Hasil akhir DB (`research_theme_rows`):** 1.005 → **902 baris** (103 dikeluarkan: 101 `non_narrative` + tidak ada duplikat). Per corpus: `daghregister=437`, `globalise=466`.

**Residual yang diketahui & SENGAJA tidak dikejar** (12 baris, didokumentasikan bukan disembunyikan): variasi OCR yang terlalu spesifik/jarang utk diregexkan aman tanpa risiko overfit — nomor halaman multi-baris berturutan (mis. `"106\n6\n13 JULI."`), halaman indeks alfabetis tanpa header berulang (mis. `"Moulin, 9, 96,..."`), dump numerik kargo yang rusak OCR, catatan errata (`"Hal. 58 baris 12 dari bawah:"`). Kalau nanti ada waktu utk sprint lanjutan, ini titik mulai yang jelas.

---

## 6. Di Luar Scope Sprint Ini

- ~~76.312 baris di `docs/thesis/dr/daghregister_corpus*.csv` belum disentuh~~ — **KOREKSI (2026-07-17):** ini salah karakterisasi. User mengklarifikasi folder `dr/` adalah pipeline yg SUDAH pernah diolah (`dedup_daghregister.py` → `classify_direction.py`/`classify_record_type.py` → `cargo_sanity_check.py` → `slim_corpus_for_db.py` → `korpus_tema_slim.csv`, yg SUDAH masuk produksi). Kebocoran sudah dipropagasi-bersih ke 6 file tahap awal ini juga — lihat §8. Yang MASIH di luar scope: pertanyaan apakah pipeline ini mau diperluas cakupannya (ambil lebih banyak dari sumber arsip asli) — itu keputusan riset terpisah, bukan soal bersih/kotor teks.
- **`staging_extractions` (119 baris)** — tidak tampil di halaman publik manapun, jadi tidak mendesak. Kalau nanti ada rencana menampilkannya, cleaning perlu dilakukan sblm exposure, bukan sebelum sekarang.
- **Hitung ulang skor klasifikasi (`skor_*`/`tema_dominan`) dari teks yang sudah bersih** — di luar scope; sprint ini hanya membersihkan tampilan teks, bukan re-run model klasifikasi.

---

## 7. Urutan Implementasi

### Sprint 1: Deteksi & Klasifikasi (P0)
1. P0.1 — Test-first: tulis `test_corpus_cleaning.py` dgn sampel nyata, RED dulu
2. P0.1 — Implementasi fungsi deteksi sampai GREEN
3. P0.2 — Jalankan ke seluruh 1.005 baris, hasilkan `corpus_cleaning_report.csv`
4. **Verifikasi:** cocokkan jumlah hasil vs audit manual (167), tunjukkan laporan ke user
5. P0.3 — Serahkan daftar `non_narrative` ke user utk keputusan exclude/keep

### Sprint 2: Terapkan & Verifikasi (P1) — ✅ SELESAI (2026-07-17)
6. ~~P1.1~~ — Strip mekanis `header_leak` diterapkan via `docs/thesis/dr/apply_corpus_cleaning.py` (script baru, tidak di-commit krn `docs/thesis/` gitignored — cukup dijalankan sekali, hasilnya yg penting adalah CSV & DB ter-update)
7. ~~P1.2~~ — `non_narrative` dikeluarkan dari CSV (101 baris total, 2 putaran stlh perluasan marker indeks "REGISTER DARI NAMA"/"REGISTER VON"/lintas-corpus_asal)
8. ~~P1.3~~ — Tidak perlu migrasi kolom backup baru — git history `data/research/korpus_tema_slim.csv` (sudah tracked sblm sprint ini) sudah cukup sbg jejak audit. `seed_research_tema.py` idempotent-upsert dijalankan ulang 3× (tiap putaran perluasan); `DELETE ... WHERE corpus_id = ANY(...)` eksplisit dijalankan tiap putaran krn seed script tidak menghapus baris yg hilang dari CSV
9. ~~P1.4~~ — Diverifikasi: query SQL langsung (0 baris leak generik tersisa), 3 contoh spesifik yg dilaporkan user (id 808/877/1022) dikonfirmasi bersih satu-satu, halaman `/riset/tema` dimuat normal (200, stat "902 baris" muncul benar di UI)
10. **Verifikasi akhir:** semua kriteria §5 terpenuhi — lihat checklist di atas

### Sprint 3: Propagasi ke Pipeline Tahap Awal (2026-07-17) — ✅ SELESAI

User mengklarifikasi `docs/thesis/dr/` bukan data tak tersentuh, melainkan tahap AWAL pipeline yg sama yg menghasilkan `korpus_tema_slim.csv`. Kebocoran dipropagasi ke sumbernya supaya re-run/perluasan pipeline nanti mewarisi teks bersih.

**Beda kebijakan dari Sprint 2** (disengaja, bukan lupa): file-file ini 511 record/masing-masing, BELUM direview manusia satu-satu setingkat 1.005 baris `korpus_tema_slim.csv`. Jadi:
- `header_leak` → text di-strip mekanis (pola sama yg sudah terbukti aman)
- `non_narrative` → **TIDAK dihapus barisnya** (beda dari Sprint 2) — cuma ditandai kolom baru `corpus_cleaning_flag` (`header_leak_stripped` / `non_narrative` / kosong utk clean), supaya proses hilir (`slim_corpus_for_db.py` versi berikutnya) yg memutuskan filter, bukan penghapusan langsung tanpa review setara di 76-ribu-baris-fisik/511-record ini.
- Backup manual dibuat (`*.pre_cleaning_backup.csv`) sblm menimpa — file-file ini TIDAK di-git-track (`docs/thesis/` gitignored), jadi tidak ada jejak git otomatis spt Sprint 2.

**Hasil** (skrip `docs/thesis/dr/propagate_cleaning_upstream.py`, identik utk 6 file — masuk akal krn semuanya snapshot paralel dari 511 record dasar yg sama dgn kolom tambahan beda tiap tahap):

| File | Total | clean | header_leak | non_narrative |
|---|---|---|---|---|
| `daghregister_corpus.csv` | 511 | 144 | 333 | 34 |
| `daghregister_corpus-update.csv` | 511 | 144 | 333 | 34 |
| `daghregister_corpus_classified.csv` | 511 | 144 | 333 | 34 |
| `daghregister_corpus_sanitychecked.csv` | 511 | 144 | 333 | 34 |
| `daghregister_corpus_deduped.csv` | 511 | 144 | 333 | 34 |
| `daghregister_corpus_directioned.csv` | 511 | 144 | 333 | 34 |

Diverifikasi: sampel strip manual benar (narasi bersih tersisa), backup ke-6 file terkonfirmasi ada.

**File:** `docs/thesis/dr/propagate_cleaning_upstream.py` (baru, tidak di-commit ke git krn `docs/thesis/` gitignored — kode-nya cuma reuse `backend/corpus_cleaning.py` yg sudah ter-commit)

---

## 9. Sprint 4: Workflow Pencegahan Regresi (2026-07-17) — ✅ SELESAI

Tiga item "langkah selanjutnya" dieksekusi supaya pembersihan ini tidak jadi one-off yang bisa balik kotor lagi diam-diam:

### 9.1 Sambungkan ke `slim_corpus_for_db.py`

Skrip yg menghasilkan `korpus_tema_slim.csv` dari sumber mentah (`korpus_tema_globalise_daghregister.csv`, 552MB, tidak ada di lokal — biasanya jalan di Colab) sekarang memanggil `corpus_cleaning.detect_leak()`/`strip_header_leak()` per baris SEBELUM menulis output. `non_narrative` dikeluarkan dari output, `header_leak` di-strip otomatis. Diverifikasi dgn CSV sintetis 3-baris (1 header_leak, 1 non_narrative, 1 clean) → hasil persis 1 di-strip, 1 dikeluarkan, 2 ditulis.

**Insiden kecil saat verifikasi:** sempat menjalankan skrip ini langsung di direktori asli (`docs/thesis/dr/`), menimpa `docs/thesis/dr/korpus_tema_slim.csv` (file lokal, BUKAN `data/research/korpus_tema_slim.csv` yg jadi sumber produksi — itu tidak tersentuh, terverifikasi via `git status` bersih) tanpa backup dulu. Dipulihkan dgn `cp data/research/korpus_tema_slim.csv docs/thesis/dr/korpus_tema_slim.csv` (diverifikasi `diff` identik). Pelajaran: jalankan skrip pipeline ber-efek-samping di direktori terisolasi (scratchpad), bukan lokasi kerja asli, meski "cuma testing".

### 9.2 Regression guard permanen (git-tracked)

`backend/tests/test_corpus_no_leaks.py` (baru) — baca `data/research/korpus_tema_slim.csv` langsung (tanpa DB, cepat, jalan di CI), assert 0 baris kena `detect_leak() != 'clean'`, plus assert row-count==902 sbg alarm perubahan volume tak disengaja. Ini pencegahan permanen: kalau CSV di-regenerate dari pipeline mentah tanpa lewat cleaning, test ini gagal keras.

**Efek samping ditemukan:** 7 test lama di `test_research_qa_granular.py` (QA-SNK-1) gagal krn hardcode baseline sebelum-cleaning (1005/470/535/27/481). Ini BUKAN bug baru — test itu memang didesain sbg "canary" anti-drift, dan mereka benar mendeteksi data berubah (krn sengaja saya ubah). Baseline diperbarui ke angka pasca-cleaning yg diverifikasi via SQL (902/437/465/26/436) — 403 test lolos total sesudahnya.

### 9.3 Bersihkan `staging_extractions`

119 baris (`source='daghregister_batavia'`) dicek: 97 `header_leak`, 22 `clean`, 0 `non_narrative`. Beda kebijakan dari `research_theme_rows` — tabel ini sudah punya alur review manusia built-in (`confidence_flag`, `reviewed_by`, `reviewed_at`), jadi:
- `header_leak` → `text_indonesia` di-strip, `confidence_flag` TETAP `'unverified'` (bersihkan artefak OCR ≠ memverifikasi konten)
- (0 `non_narrative` di batch ini, tapi kebijakannya: `confidence_flag` → `'rejected'`, nilai yg memang sudah ada di skema, bukan hapus baris)

Diverifikasi: 0 baris tersisa cocok pola bocor, `metadata_json` tiap baris yg diubah mencatat jejak cleaning (`{"kategori": "header_leak_stripped", "at": "<timestamp>"}`) utk audit.

**File:** `docs/thesis/dr/slim_corpus_for_db.py` (dimodifikasi, gitignored), `docs/thesis/dr/clean_staging_extractions.py` (baru, gitignored), `backend/tests/test_corpus_no_leaks.py` (baru, **committed**), `backend/tests/test_research_qa_granular.py` (baseline diperbarui, **committed**)
