# Archival Density Measurement Plan

> **DRAFT FOR RESEARCHER REVIEW — NOT IMPLEMENTED — NOT A FINAL HISTORICAL INTERPRETATION**

Ini audit **struktur**, bukan perhitungan kepadatan final. Tidak ada angka kepadatan yang dihasilkan di dokumen ini — unit dokumen belum tervalidasi cukup untuk itu (lihat §Keterbatasan). Seluruh angka di bawah adalah hasil pemeriksaan struktural read-only atas file yang ada, bukan model atau agregasi baru yang mengklaim kebenaran final.

---

## 1. Unit Dokumen — Temuan Utama (B1)

**Peringatan yang terbukti benar dalam pemeriksaan ini:** `wc -l` pada kedua file korpus utama **BUKAN** jumlah dokumen/entri, karena kedua file memuat field teks yang berisi baris-baru literal di dalam nilai CSV berkutip (`text`, `text_asli`, dll.). Ini bukan dugaan — dikonfirmasi dengan membandingkan dua metode langsung:

| Berkas | `wc -l` (baris file mentah) | Baris CSV terparse benar (`csv.DictReader`) | Rasio |
|---|---|---|---|
| `docs/thesis/GM/gm_corpus_filtered_1660_1789.csv` | 102.381 | **100** | ~1024× lipat ganda |
| `docs/thesis/dr/daghregister_corpus_classified.csv` | 75.651 | **511** | ~148× lipat ganda |

**Konsekuensi langsung:** setiap perhitungan kepadatan yang pernah memakai `wc -l` atau penghitungan baris mentah pada berkas ini (tidak ditemukan bukti hal ini pernah dilakukan di repository, tapi dicatat sebagai risiko eksplisit) akan salah dengan faktor dua-tiga orde besaran. Rekomendasi teknis untuk pekerjaan lanjutan: **hitung selalu via parser CSV yang benar** (`csv.DictReader` dengan `field_size_limit` dinaikkan, seperti dipakai dalam pemeriksaan ini), tidak pernah via `wc -l`.

### 1.1 Field yang membedakan unit — per korpus

**`gm_corpus_filtered_1660_1789.csv`** (Generale Missiven, WP6 pipeline):

| Field | Peran unit |
|---|---|
| `volume` | Koleksi/jilid RGP (Rijks Geschiedkundige Publicatiën) |
| `surat_id` | **Unit dokumen** — satu surat, format `{volume}/p{halaman}.xml` |
| `page` | Halaman buku RGP |
| `tahun_surat` | Tahun surat ditulis (berdasarkan tanda tangan/isi) |
| `tahun_efektif` | Tahun yang dipakai untuk pengurutan efektif — **BEDA dari `tahun_surat`** pada sebagian baris (belum diverifikasi berapa persen berbeda dalam pemeriksaan ini; perlu perhitungan terpisah) |
| `tanggal_perkiraan` | Tanggal presisi (contoh: `1661-01-26`) bila diketahui |
| `penulis`, `tempat_asal_surat` | Metadata dokumen |
| `source` | Selalu `generale_missiven_wp6` pada sampel yang diperiksa |

Unit dokumen yang defensibel: **`surat_id`** (setara `SourceRecord` di ontologi episode). `volume` adalah unit koleksi, bukan unit dokumen individual.

**`daghregister_corpus_classified.csv`** (Daghregister Batavia, per-entri):

| Field | Peran unit |
|---|---|
| `volume` | Nama volume/tahun jurnal (contoh: `Dagh_register_gehouden_int_Casteel_Batavia-1664`) — **memuat tahun di dalam nama volume**, bukan field tahun terpisah |
| `book_page_start` / `book_page_end` | Rentang halaman buku cetak — **inilah unit yang paling dekat dengan "satu entri jurnal harian"** |
| `tanggal_perkiraan` | **Format tidak konsisten** — contoh yang ditemukan: `"14 JANUARY"` (tanpa tahun; tahun harus diambil dari nama `volume`) |
| `duplicate_of` | Menunjuk ke baris lain bila entri ini duplikat — **41/511 baris (8%) terisi** |
| `record_type` | `lainnya` (346) · `single_voyage` (128) · `port_tally_aggregate` (12) · `kandidat_belum_diverifikasi` (25) |
| `corpus_cleaning_flag` | Kosong pada sampel yang diperiksa |

Unit dokumen yang defensibel: **`(volume, book_page_start, book_page_end)`** — satu entri jurnal harian. `volume` sendiri adalah unit koleksi/tahun-terbitan, bukan unit dokumen.

**Corpus Diplomaticum (CD1–CD6) — TEMUAN KRITIS:**

Tidak ditemukan berkas CSV terstruktur untuk Corpus Diplomaticum sebanding dengan dua di atas. Yang ada:

- `docs/thesis/cd_instrumen_candidates.csv` (8 baris terparse) dan `docs/thesis/cd_nader_verbond_candidates.csv` (86 baris terparse) — **ini adalah hasil pencarian kata kunci** (kolom `keyword`, `context`), bukan indeks penuh korpus. Tidak ada baseline "total halaman CD per jilid" di dalamnya.
- `docs/thesis/cd_resistance_signal_candidates.csv` (13 baris) — sama, hasil pencarian kata kunci, bukan indeks penuh.
- **Berkas sumber `docs/CD1.pdf`–`docs/CD6.pdf` sendiri TIDAK DITEMUKAN di repository saat pemeriksaan ini dijalankan** (`NOT AVAILABLE` secara fisik, dicek dengan pencarian nama file di seluruh direktori proyek). `linimasa_events` merujuk dokumen-dokumen ini secara ekstensif (`source_document` CD1–CD6 mencakup 65/141 = 46% dari seluruh baris `linimasa_events`), tapi sumber fisiknya sendiri sudah tidak berada di repository yang bisa diperiksa ulang.

**Konsekuensi:** korpus yang paling banyak dipakai (CD1–CD6, 46% dari `linimasa_events`) adalah korpus dengan **paling sedikit** bahan mentah untuk mengukur kepadatan dokumennya sendiri — kebalikan tepat dari yang dibutuhkan untuk menguji confound kepadatan arsip terhadap periode yang paling banyak menyumbang event ke Model 3.

## 2. Audit Deduplikasi (B2)

| Risiko | Ditemukan? | Bukti |
|---|---|---|
| Satu dokumen muncul di banyak baris | **Ya, terkonfirmasi** — Daghregister | `duplicate_of` terisi pada 41/511 baris (8%); `docs/thesis/dr/daghregister_corpus_dedup_report.csv` (41 baris) sudah ada dan mencatat pasangan volume duplikat/kanonik dengan skor `similarity` — **pekerjaan deduplikasi sebagian sudah dilakukan tim sebelumnya untuk Daghregister**, belum untuk GM |
| Satu halaman menghasilkan banyak record | `NOT AVAILABLE untuk dipastikan` — GM: `(volume, page)` unik 100/100 pada sampel; Daghregister: `(volume, book_page_start)` unik 511/511 pada sampel — **tidak ditemukan bukti dalam sampel yang diperiksa**, tapi sampel GM hanya 100 baris (lihat §Keterbatasan) |
| Satu event `linimasa_events` dirujuk banyak dokumen | **Ya** — bukan anomali, ini normal (mis. episode Barus [57] merujuk balik ke traktat 1668 & yang lain) |
| Satu dokumen diklasifikasikan ke banyak kategori | `NOT AVAILABLE untuk dipastikan` dari struktur yang diperiksa — `record_type` di Daghregister tampak eksklusif (satu nilai per baris) |
| Salinan/versi dokumen dihitung ganda | **Berisiko tinggi untuk GM** — file bernama `korpus_final_dengan_topik(1).csv` vs `korpus_final_dengan_topik.csv`, `korpus_primer_gabungan(1).csv` vs `korpus_primer_gabungan.csv`, `slr_bab2_hasil(1).csv` vs `slr_bab2_hasil.csv` ditemukan di `docs/thesis/colab/` — pasangan berkas dengan akhiran `(1)` mengindikasikan unduhan ganda/versi paralel yang **belum diperiksa apakah identik atau berbeda** |

## 3. Rancangan Ukuran Kepadatan (B3) — RANCANGAN SAJA, BELUM DIHITUNG

Sepuluh ukuran berikut dirancang secara konseptual. **Tidak satu pun dihitung sebagai angka final dalam dokumen ini** karena unit dokumen CD1–CD6 belum tervalidasi (§1) dan sampel GM yang diperiksa (100 baris) belum tentu mewakili keseluruhan berkas.

| Ukuran | Formula konseptual | Unit dasar | Status kesiapan |
|---|---|---|---|
| `document_count` per tahun | Hitung `surat_id`/entri per `tahun_efektif` (GM) atau per tahun dari nama `volume` (Daghregister) | Sudah ada field | **Dapat dihitung untuk GM & Daghregister**, TIDAK untuk CD |
| `document_count` per dekade | Sama, dikelompokkan per 10 tahun | — | Sama |
| `unique_document_count` | `count(distinct surat_id)` / `count(distinct (volume, book_page_start))`, dikurangi baris ber-`duplicate_of` | Perlu terapkan hasil dedup report Daghregister lebih dulu | **Daghregister: metodenya sudah ada (dedup report), belum diterapkan**; GM: dedup belum diperiksa sama sekali |
| `unique_page_or_folio_count` | `count(distinct (volume, page))` | Sudah ada field | Dapat dihitung, dengan catatan sampel GM terbatas |
| `source_collection_share` | Proporsi event `linimasa_events` per `source_document` dibagi (jika tersedia) volume dokumen koleksi itu | Butuh penyebut dari §1 | **TIDAK dapat dihitung untuk CD1–CD6** (penyebut `NOT AVAILABLE`) |
| `event_count` per document | Jumlah baris `linimasa_events` yang merujuk satu `surat_id`/entri spesifik | Perlu pemetaan `linimasa_events.source_page`/`book_page` ke `surat_id`/entri korpus mentah — **belum ada pemetaan ini** | Belum siap |
| `event_count` per unique document | Sama, dikoreksi duplikat | — | Belum siap |
| `coverage_gap` | Rentang tahun/halaman TANPA entri korpus sama sekali, dibandingkan rentang TANPA `linimasa_events` | Perlu §document_count per tahun lebih dulu | Belum siap |
| `report_date` density | Distribusi jeda antara tanggal peristiwa vs tanggal dokumen per tahun | `NOT AVAILABLE` — lihat §4 | **Tidak dapat dihitung — field sumbernya sendiri tidak ada** |
| `event_date` density (bila tersedia) | Distribusi tanggal peristiwa (bukan tanggal dokumen) per tahun, dibandingkan `event_count` `linimasa_events` per tahun | GM: `tanggal_perkiraan` sebagian tersedia; Daghregister: `tanggal_perkiraan` tanpa tahun (harus digabung dgn `volume`) | **Dapat dirancang, belum dihitung** |

### 3.1 Pemisahan per koleksi

| Koleksi | `document_count`/`unique_document_count` dapat dihitung? | Catatan |
|---|---|---|
| GM (Generale Missiven) | **Ya**, dari `surat_id` — TAPI hanya untuk 100 baris yang terperiksa dalam audit ini, bukan seluruh berkas (lihat §Keterbatasan) |
| Daghregister | **Ya**, dari `(volume, book_page_start)`, dengan dedup diterapkan dari `daghregister_corpus_dedup_report.csv` | 511 baris terperiksa penuh (bukan sampel — seluruh file berhasil diparse) |
| Corpus Diplomaticum (CD1–6) | **Tidak** — tidak ada indeks penuh, hanya hasil pencarian kata kunci parsial, dan berkas sumber (PDF) `NOT AVAILABLE` di repo saat ini | **Gap kritis** — 46% dari `linimasa_events` bersumber dari koleksi yang paling sedikit terukur |
| Koleksi lain (`buku-padang-1718`, `buku-vogel-1690`, `kathirithamby-1965`, surat individu Botham/Harries/Kempen, dll.) | **Tidak** — sumber-sumber sekunder/tunggal ini tidak punya indeks korpus sama sekali; masing-masing adalah satu buku/dokumen, bukan korpus multi-entri | `document_count` = 1 per koleksi (trivial, tidak informatif untuk density per-tahun) |
| Seluruh koleksi gabungan | **Tidak** — tidak dapat digabung tanpa unit yang sepadan untuk CD | — |

## 4. Tanggal Peristiwa vs Tanggal Laporan (B4)

| Korpus | `event_date` | `document_date` | `report_date` | `receipt_date` | `publication_date` |
|---|---|---|---|---|---|
| `linimasa_events.csv` (produksi Model 3) | `year` + `event_date_raw` | — | **`NOT AVAILABLE`** | `NOT AVAILABLE` | `NOT AVAILABLE` |
| GM (`gm_corpus_filtered_1660_1789.csv`) | `tahun_surat`/`tahun_efektif`/`tanggal_perkiraan` | **Tersedia** — surat GM secara definisi bertanggal saat ditulis, dan `tahun_surat` mendekati ini | `NOT AVAILABLE` sbg field terpisah — GM adalah kompilasi laporan tahunan Gubernur-Jenderal, jeda antara peristiwa yang dilaporkan surat dan tanggal surat itu sendiri **tidak dibedakan secara field**, hanya dapat diperkirakan dari isi teks (`text`/`text_asli`) per kasus | `NOT AVAILABLE` | `NOT AVAILABLE` |
| Daghregister (`daghregister_corpus_classified.csv`) | `tanggal_perkiraan` (tanpa tahun, digabung dgn `volume`) | Entri jurnal ditulis pada/dekat hari kejadian (sifat genre "daghregister" = catatan harian) — **`document_date` ≈ `event_date` secara struktural untuk genre ini**, TAPI ini asumsi genre, bukan field terverifikasi per-baris | `NOT AVAILABLE` | `NOT AVAILABLE` | `NOT AVAILABLE` |
| CD1–6 (tidak ada indeks) | `NOT AVAILABLE` di level korpus (hanya ada di `linimasa_events` per-baris hasil sisir manual) | — | — | — | — |

**Kesimpulan B4:** **tidak satu pun korpus yang diperiksa membedakan `report_date` dari `event_date` sebagai field eksplisit.** Untuk Daghregister ada argumen genre yang masuk akal (catatan harian ditulis dekat waktu kejadian) — tapi ini asumsi struktural berdasarkan jenis dokumen, bukan verifikasi per-entri. Untuk GM (surat administratif tahunan/berkala), jeda ini berpotensi jauh lebih besar dan sama sekali tidak terukur dari field yang ada. **Ini adalah gap yang sama persis dengan yang sudah diidentifikasi di audit-audit sebelumnya untuk `linimasa_events` — sekarang dikonfirmasi berlaku juga di korpus mentah yang menjadi sumbernya.**

## 5. Hubungan yang Kelak Dapat Diuji terhadap Intensitas Model 3

**Belum dihubungkan pada tahap ini.** Rancangan pengujian, untuk dilakukan setelah §3 memiliki angka tervalidasi:

1. **Uji korelasi sederhana:** `document_count` per dekade (GM+Daghregister, TANPA CD karena `NOT AVAILABLE`) vs jumlah `linimasa_events` per dekade. Perlu diingat: ini uji PARSIAL — mengecualikan CD berarti mengecualikan 46% sumber data Model 3, sehingga hasil uji ini **tidak bisa mengklaim menjawab confound kepadatan arsip secara menyeluruh**, hanya untuk irisan non-CD.
2. **Uji distribusi residual:** apakah dekade dengan λ(t) Model 3 tinggi (1660s, 1680s per audit sebelumnya) juga dekade dengan `document_count` tinggi di GM/Daghregister — bila ya, ini **sinyal peringatan** (bukan bukti definitif) bahwa puncak intensitas Hawkes mungkin sebagian mencerminkan volume pelaporan, bukan murni intensitas peristiwa.
3. **Uji koleksi-tunggal:** apakah dekade dengan event `linimasa_events` terbanyak juga didominasi SATU `source_document` (mis. 1680s didominasi CD3, dicatat di audit sebelumnya sbg observasi awal, belum diuji formal) — relevan langsung untuk §3.1 CD1–6 sekali indeksnya tersedia.

**Batasan tegas:** hasil dari ketiga uji ini, bila dijalankan, **tidak boleh dibaca sebagai bukti kausal** apa pun tentang bias pelaporan — hanya sebagai deskripsi ko-variasi. Ini konsisten dengan §Causal Readiness Framework di `EPISODE_ONTOLOGY_ANNOTATION_PROTOCOL_DRAFT.md`.

## 6. Keterbatasan

1. **Sampel GM tidak lengkap dalam audit ini.** Pemeriksaan struktural ini membaca dan mem-parsing **seluruh** `daghregister_corpus_classified.csv` (511 baris, semuanya), tapi hanya **100 baris pertama-terparsing** dari `gm_corpus_filtered_1660_1789.csv` sebelum dihentikan untuk efisiensi audit — **BUKAN seluruh isi berkas**. Berapa banyak baris total sebenarnya dalam berkas GM ini (setelah parsing benar) **belum diketahui** dan wajib dihitung ulang penuh sebelum angka kepadatan final dipakai.
2. **Unit dokumen CD1–6 sepenuhnya tidak tervalidasi** — gap kritis yang dicatat di §1 dan §3.1.
3. **Pemetaan `linimasa_events` ↔ entri korpus mentah belum ada.** `linimasa_events.source_page`/`book_page` adalah nomor halaman BUKU CETAK (mis. Corpus Diplomaticum jilid III halaman 219), sedangkan `gm_corpus_filtered_1660_1789.csv`/`daghregister_corpus_classified.csv` punya skema penomoran halaman/volume sendiri yang belum tentu selaras satu-satu. Membangun `event_count per document` (§3) membutuhkan pemetaan ini terlebih dulu — pekerjaan tersendiri, di luar cakupan dokumen ini.
4. **File berpasangan dengan akhiran `(1)`** (§2) belum diverifikasi identik atau berbeda — bila berbeda dan keduanya ikut terhitung, risiko penghitungan ganda nyata.
5. **Ambang "kepadatan tinggi/rendah" belum didefinisikan.** Bahkan setelah angka tersedia, diperlukan keputusan peneliti tentang ambang yang berarti secara historiografis (bukan hanya statistik), sejalan dengan disiplin ambang AIC yang sudah dipakai proyek ini di tempat lain.

## 7. Keputusan Peneliti yang Masih Dibutuhkan

| ID | Keputusan |
|---|---|
| DP-1 | Apakah pengukuran kepadatan GM diselesaikan penuh (bukan sampel 100 baris) sebelum dipakai untuk uji apa pun? |
| DP-2 | Apakah CD1–6 disisir ulang untuk membangun indeks penuh (bukan hanya kandidat kata kunci), mengingat berkas PDF sumber sendiri saat ini `NOT AVAILABLE` di repo — perlu diperoleh ulang dulu? |
| DP-3 | Apakah uji korelasi §5 dijalankan sebagai uji PARSIAL (GM+Daghregister saja, mengecualikan 46% data CD) dengan peringatan eksplisit, atau ditunda sampai CD terindeks? |
| DP-4 | Apakah pasangan berkas `(1)` di `docs/thesis/colab/` diverifikasi/dibersihkan sebelum dipakai sbg sumber apa pun? |
| DP-5 | Siapa yang membangun pemetaan `linimasa_events` ↔ entri korpus mentah (§Keterbatasan poin 3), dan dengan metode apa (manual vs pencocokan otomatis nomor halaman)? |

---

**Tidak ada angka kepadatan final dihasilkan dokumen ini.** Tabel di §3 adalah rancangan ukuran, bukan hasil perhitungan yang siap dikutip.
