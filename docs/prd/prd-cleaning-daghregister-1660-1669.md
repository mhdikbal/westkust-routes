# PRD: Pembersihan & Validasi Data Pelayaran Dagh-register 1660-1669 (Pantai Barat ↔ Batavia)

**Status:** P0.1-P0.5 SELESAI (2026-07-07) — lihat §8 Workflow & Board
**Disusun:** 2026-07-07
**Tim:** Tim Data (ekstraksi/pembersihan) + DBA (skema/keputusan model data) — Scrum Master: Muhammad Ikbal
**Melengkapi:** `docs/prd/prd-daghregister-voyage-data.md` (keputusan staging-first sudah dikunci di sana — PRD ini tidak mengubahnya)

---

## 1. Latar Belakang

`docs/thesis/dr/daghregister_corpus.csv` (282 entri, 6 dari 13 jilid Dagh-register: 1661, 1663, 1664, 1665, 1666-1667, 1668-1669 — semuanya sudah punya lapisan teks asli, **tidak butuh OCR**) adalah sumber paling kaya untuk window 1660-1669, mengalahkan `pelayaran_daghregister_final.csv` (119 baris) yang ternyata membuang format tally-bulanan-per-pelabuhan lewat filter regex-cari-kapal.

Sesi analisis 2026-07-07 menemukan 4 masalah kualitas data konkret yang harus dibereskan SEBELUM data ini di-insert ke staging/`voyages`:

1. **Duplikasi lintas-jilid** — tanggal yang sama (mis. "20 MAERT", "18 EN 19 MAERT", "9-11 MEY") muncul dengan teks nyaris identik di file jilid `1666-1667` DAN `1668-1669`. **[Koreksi 2026-07-07 — lihat P0.2]**: setelah dedup script jalan, terbukti duplikasi HANYA antara jilid 1666-1667↔1668-1669 (41 baris), bukan gejala umum lintas jilid lain — klaim "20 MAERT dll" di atas benar tapi contoh spesifik itu; jangan generalisasi ke jilid lain.
2. **Kesalahan digit OCR/HTR** — kasus fluyt Bunschoten (20 Maret 1668): Dagh-register mencatat "1922 bahar lada" & "1722 kapur barus", sementara sumber independen (*Padang Abad XVII-XVIII*, Ikbal & Arsya, `data_perdagangan_1660_1690_ikbal_arsya.json`) mencatat kejadian yang SAMA (nilai gulden identik 76140:9:5) sebagai "192 bahar lada" & "172½ kapur barus" — pola sisipan angka "1" khas kesalahan HTR.
3. **Cakupan kata kunci tidak lengkap** — `KEYWORDS_WESTKUST` (dipakai scan ke-6 jilid ini) awalnya tidak punya varian utk **Barus, Bayang, Cingkuak/Cingkuk, Air Haji** (ditemukan sbg "Aijerhadja"/"Ayerhadja" di korpus), dan varian ejaan "Indiapoura" utk Indrapura. **Sudah diperbaiki di notebook (2026-07-07)**, tapi ke-6 jilid ini perlu **rescan** dgn keyword baru — belum dijalankan.
4. **Dua bentuk record tercampur tanpa penanda** — (a) entri naratif per-kapal (nama kapal + kargo + nilai), dan (b) entri tally bulanan per-pelabuhan-asal (jumlah kapal tak bernama + total kargo agregat, mis. "31 Maret 1661: 1 dari Ticco, 20 pikul kemenyan"). Keduanya butuh perlakuan berbeda saat masuk skema `Voyage` (`ship_name` `nullable=False`).

**Independen dari OCR 7 jilid yang masih kosong** (1670-1671, 1676-1681, di luar window 1660-1669) — PRD ini bisa jalan sekarang, tapi **butuh rescan Tahap 1 keyword-baru untuk 6 jilid yang sudah ada teksnya** sebelum klaim "cakupan lengkap 10 pelabuhan".

### 1.1 Update 2026-07-07 — hasil rescan + OCR 7 jilid sudah masuk

User menjalankan Colab dan menghasilkan `docs/thesis/dr/daghregister_corpus-update.csv` (511 baris) + `dr_scan_mentah-update.json`. Review DBA:

- **P0.1 (rescan 6 jilid lama) TERBUKTI BERHASIL** — 282 → 311 baris utk jilid 1661/1663/1664/1665/1666-1667/1668-1669 (+29 baris baru ketemu berkat keyword Barus/Bayang/Cingkuak/Air Haji/Indiapoura yang diperluas). Ini mengonfirmasi hipotesis: keyword lama memang melewatkan entri.
- **6 jilid baru (1676-1681) berhasil diproses** — 200 baris tambahan, di luar window 1660-1669 PRD ini tapi tetap dalam window thesis (1660-1789). Salido/Sillida muncul 3x — perpanjang narasi tambang.
- ⚠️ **Jilid 1670-1671 KOSONG (0 halaman relevan dari 946 halaman discan)** — dibanding jilid tetangga seukuran (1666-1667, 964 halaman → 135 relevan), ini implausible. Kemungkinan besar **kegagalan kualitas OCR** (jilid ini butuh Tesseract, tidak punya lapisan teks asli), bukan genuinely tidak ada konten pantai barat Sumatra. **Belum boleh dianggap selesai** — jadi P0.6 baru di bawah.
- ⚠️ **File tak dikenal muncul di scan: `Dagh_register_gehouden_int_casteel_Batavia-1659.pdf`** (287 halaman, 0 relevan) — bukan bagian dari 13 jilid yang terdokumentasi, tidak ada di `docs/thesis/dr/` lokal (hanya di Google Drive Colab user). Perlu klarifikasi + sync ke lokal — jadi bagian Open Question #5.
- Kualitas OCR jilid baru (1676-1681) lebih rendah dari jilid ber-teks-asli — beberapa `tanggal_perkiraan` jelas artefak OCR rusak (mis. "Mm MAENT, rz0"). P0.5 (sanity-check) makin penting utk jilid-jilid ini.

### 1.2 Keputusan Scope (2026-07-07): fokus 1660, prioritas pasca-1663 Perjanjian Painan

User memutuskan **skip file 1659** (di luar window thesis) dan **deprioritas P0.6** (verifikasi OCR 1670-1671, juga di luar window inti 1660-1669) — bukan blocking. Alasan eksplisit: **1660 ke atas, terutama pasca-1663 (Perjanjian/Painan Traktat), adalah puncak dimulainya suksesi VOC di pantai barat** — periode ini yang paling bernilai utk thesis, bukan jilid tambahan di ekor (1670-1671, 1676-1681).

Implikasi: `daghregister_corpus.csv` resmi **sudah digabung (2026-07-07)** — jadi 511 baris (6 jilid inti 1660-1669 + jilid 1676-1681). Catatan: jilid 1670-1671 tidak perlu "dikecualikan" secara manual — ia sudah berkontribusi 0 baris ke corpus (konsisten dengan 0 halaman relevan di scan), jadi merge-nya otomatis tidak menyertakannya. `dr_scan_mentah.json` juga sudah diperbarui dari versi `-update`. Jilid 1663 (tahun Perjanjian Painan) layak dapat perhatian ekstra saat P0.2-P0.5 dijalankan — cross-check dgn `corpudiplomaticum.docx`/`cp/CD2-6` yang sudah punya teks perjanjian itu (CCLXXV, hal. 339 di salah satu sumber cp).

## 2. Cakupan Pelabuhan (wajib diperiksa satu per satu)

Barus, Tiku, Pariaman, Padang, Salido, Bayang, Pulau Cingkuk, Painan, Indrapura, Air Haji — **dua arah**: pelayaran dari pantai barat ke Batavia, DAN dari Batavia ke pantai barat (`arah` saat ini hanya terisi eksplisit di ~35% baris `pelayaran_daghregister_final.csv`; sisanya perlu direkonstruksi dari `daghregister_corpus.csv` atau ditandai `unknown`).

| Pelabuhan | Varian ejaan sumber (dikonfirmasi ada di korpus) | Status keyword |
|---|---|---|
| Barus | barus, baros | ✅ ditambahkan 2026-07-07 |
| Tiku | tico, ticco | ✅ sudah ada |
| Pariaman | priaman, pariaman | ✅ sudah ada |
| Padang | padang | ✅ sudah ada |
| Salido | salida, silida, sillida, sillidase | ✅ sudah ada + diperluas |
| Bayang | bayang | ✅ ditambahkan 2026-07-07 |
| Pulau Cingkuk | pulo chinko, pulo-chinko, chinco, cingkuak, cingkuk | ✅ ditambahkan 2026-07-07 |
| Painan | painan | ✅ sudah ada |
| Indrapura | indrapura, indrapoura, **indiapoura** | ✅ varian ejaan ditambahkan 2026-07-07 |
| Air Haji | ayerhadja, aijerhadja, ayerhadji, aijerhadji, air hadji, ayer hadji | ✅ ditambahkan 2026-07-07 (ditemukan sbg "Aijerhadja" di GLOBALISE, belum pernah ter-scan di Dagh-register) |

Semua 10 kini ada di `KEYWORDS_WESTKUST` (`daghregister_extraction.ipynb` cell scan + `globalise_extraction.ipynb` cell scan) — **tapi rescan belum dijalankan**, jadi tabel ini adalah target, bukan hasil terverifikasi.

## 3. Keputusan Desain

Tetap staging-first (lihat `docs/prd/prd-daghregister-voyage-data.md` §3) — PRD ini menambahkan **lapisan pembersihan** di antara "hasil scan Colab" dan "masuk `staging_extractions`", bukan mengubah tabel staging itu sendiri.

## 4. Requirements

### P0 — Wajib sebelum data window 1660-1669 boleh masuk staging

**P0.1 — Rescan Tahap 1 (6 jilid, keyword lengkap)** ✅ **SELESAI (2026-07-07)**
- Tim Data menjalankan ulang Tahap 1 `daghregister_extraction.ipynb` untuk jilid 1661, 1663, 1664, 1665, 1666-1667, 1668-1669 dengan `KEYWORDS_WESTKUST` yang sudah diperluas.
- Hasil: 282 → 311 baris (+29). Acceptance terpenuhi — keyword lama terbukti melewatkan entri.

**P0.6 — Verifikasi ulang OCR jilid 1670-1671** — **DEPRIORITAS (2026-07-07):** user eksplisit fokuskan scope ke 1660, khususnya pasca-1663 (Perjanjian Painan/Painan Traktat — puncak dimulainya suksesi VOC di pantai barat). 1670-1671 di luar window inti PRD ini (1660-1669) sejak awal; anomali 0-halaman-relevan dicatat sbg technical debt tapi TIDAK blocking utk P0.2-P0.5 berjalan di 6 jilid inti. Boleh disusul kapan saja, bukan prasyarat.

**P0.2 — Deduplikasi lintas-jilid** ✅ **SELESAI (2026-07-07)**
- Script: `docs/thesis/dr/dedup_daghregister.py`. Bandingkan tiap pasang entri `tanggal_perkiraan` sama, `volume` beda, ukur similarity teks (`difflib.SequenceMatcher`).
- **Koreksi atas asumsi awal** (yang tercatat di §1 latar belakang, poin 1) — duplikasi TERNYATA bukan gejala umum lintas banyak jilid. Setelah dicek similarity teks sungguhan: dari 233 pasangan tanggal-sama, **176 pasangan (di luar jilid 1666-1667↔1668-1669) similarity maksimum cuma 0.059** — itu cuma kebetulan tanggal-di-bulan sama tapi tahun/isi beda total, BUKAN duplikat. Duplikasi genuine **HANYA** ada di 57 pasangan antara jilid **1666-1667 dan 1668-1669** — ada celah alami di similarity (0.038→0.163, karena LLM menerjemahkan ulang event yang sama dgn kata beda tiap kali, jadi similarity teks duplikat cuma ~0.4-0.84, bukan ~1.0). Ambang final: **0.1**.
- Hasil: **41 baris ditandai `duplicate_of`** (kanonik dipilih dari teks lebih panjang). `daghregister_corpus.csv` resmi sudah punya kolom `duplicate_of` ini (511 baris total, 41 terisi). Laporan pasangan: `docs/thesis/dr/daghregister_corpus_dedup_report.csv`.
- Acceptance terpenuhi: field `duplicate_of` menunjuk ke entri kanonik; saat promosi ke `voyages` nanti, baris dengan `duplicate_of` terisi WAJIB di-skip (bukan dihitung pelayaran terpisah).

**P0.3 — Klasifikasi tipe record** ✅ **SELESAI (2026-07-07)**
- Script: `docs/thesis/dr/classify_record_type.py`. Setiap baris diberi `record_type`.
- **Pendekatan (setelah 2 iterasi regex-murni gagal presisi):** entri Dagh-register sering multi-topik per hari — "ada kata kapal di suatu tempat dalam teks" TIDAK cukup jadi sinyal (contoh nyata: entri ttg aturan dagang Siam yang baru menyebut kapal fluyt Elburg di paragraf TERAKHIR). Solusi: `single_voyage` di-JOIN ke `pelayaran_daghregister_final.csv` (file hasil ekstraksi LLM khusus voyage dari sesi sebelumnya, jauh lebih andal) via volume+tanggal_perkiraan ternormalisasi. `port_tally_aggregate` pakai pola "N dari [Tempat], dengan M orang" yang WAJIB muncul di 150 karakter pembuka entri (bukan di mana pun — iterasi pertama salah tandai entri single-kapal sbg tally krn pola itu kebetulan muncul di paragraf lain).
- Hasil (511 baris): **lainnya 346 (67,7%)** — administrasi/diplomasi VOC tanpa pelayaran, konsisten dgn temuan tema sebelumnya. **single_voyage 128 (25,0%)** — confidence tinggi (berbasis ekstraksi LLM tervalidasi, bukan regex). **kandidat_belum_diverifikasi 25 (4,9%)** — HANYA dari jilid 1676-1681 yang belum punya file kandidat voyage khusus; regex ship+cargo match tapi belum ada validasi setara jilid lain, PERLU review manual sebelum dipromosikan. **port_tally_aggregate 12 (2,3%)** — sudah di-spot-check manual, semua genuine.
- Acceptance terpenuhi: 100% dari 511 baris punya `record_type` terisi, tidak ada yang di-skip diam-diam. `daghregister_corpus.csv` resmi sekarang punya kolom ini.

**P0.3b — Pembeda provenance di peta publik**
- Sebelum data staging window 1660-1699 manapun (Dagh-register, GLOBALISE, atau hasil promosi lain di luar BGB Huygens) di-*promote* dan tampil di peta publik `salido.my.id`, frontend WAJIB punya pembeda visual (warna pin / legend terpisah) yang menunjukkan pin itu bersumber dari Dagh-register/GLOBALISE — beda dari pin BGB Huygens yang sudah ada (`voyages.source_url` saat ini semua mengarah ke BGB). Ini resolusi dari open question #4 di `docs/prd/prd-daghregister-voyage-data.md` §6 — sekarang jadi requirement P0, bukan pertanyaan terbuka.
- Acceptance: tidak ada pin hasil promosi Dagh-register/GLOBALISE yang tampil identik (warna/legend) dengan pin BGB Huygens di peta; user (pengunjung publik) bisa membedakan tingkat kepastian data hanya dari tampilan peta, tanpa buka modal detail.

**P0.4 — Klasifikasi arah (dua arah, bukan cuma satu)** ✅ **SELESAI (2026-07-07)**
- Script: `docs/thesis/dr/classify_direction.py`. Scope: HANYA baris `record_type == single_voyage` (128 baris) — `port_tally_aggregate`/`lainnya` diberi `direction = tidak_relevan` (jalur promosinya sendiri belum diputuskan, bukan tugas P0.4 ini).
- Sumber, urutan prioritas: (1) kolom `arah` yang SUDAH ADA di `pelayaran_daghregister_final.csv` (join via volume+tanggal ternormalisasi — 49/119 baris kandidat sudah eksplisit dari sesi sebelumnya, bukan ditebak sekarang); (2) fallback regex eksplisit ("tiba...dari Pantai Barat/Sumatra" / "berangkat/berlayar...ke Pantai Barat/Sumatra") di teks korpus sendiri; (3) `unknown` kalau dua-duanya nihil.
- Hasil (128 baris single_voyage): **unknown 83 (64,8%)**, **pantai_barat_ke_batavia 28 (21,9%)**, **batavia_ke_pantai_barat 17 (13,3%)**. Rasio unknown tinggi TAPI jujur — sudah dicek sampel, sisanya memang teks yang tidak eksplisit soal arah (banyak entri single_voyage yang kandungan kapalnya "terkubur" di paragraf tengah/akhir teks yang topik utamanya diplomasi, bukan pelayaran).
- Acceptance terpenuhi: 0% tebakan diam-diam — semua `unknown` genuinely tidak eksplisit, bukan default.

**P0.5 — Sanity-check nilai kargo vs Data Perdagangan 1660-1690**
- Untuk entri yang tanggal+kapalnya cocok dengan salah satu dari 18 entri `data_perdagangan_1660_1690_ikbal_arsya.json`, bandingkan angka kargo. Kalau beda tapi nilai gulden totalnya sama (pola spt kasus Bunschoten), tandai `cargo_qty_flagged_ocr_error=true` dan pakai angka dari Data Perdagangan (sumber buku ber-editor) sbg nilai yang dipromosikan, bukan angka Dagh-register HTR.
- Acceptance: seluruh 18 titik overlap tercek manual; laporan berapa yang cocok persis vs berapa yang punya selisih digit.

#### Skema P0.5 (disiapkan 2026-07-07, BELUM dieksekusi)

Beda dari P0.1-P0.4: sumber `data_perdagangan_1660_1690_ikbal_arsya.json` masih 15 blob teks per-halaman (bukan per-kejadian), jadi butuh 1 artefak antara baru sebelum bisa dibandingkan.

**Artefak 1 — `docs/thesis/dr/data_perdagangan_structured.csv`** (ekstraksi terstruktur dari 15 blob halaman, per kejadian pelayaran):

| Kolom | Isi |
|---|---|
| `entry_id` | urutan sekuensial |
| `halaman_buku` | dari sumber asli |
| `tanggal` | teks asli, mis. "20 Maret 1668" |
| `nama_kapal` | mis. "fluit Bunschoten" |
| `arah` | `dari_pantai_barat` / `ke_pantai_barat` (dari frasa "dari/ke Pantai Barat Sumatra") |
| `nilai_gulden_raw` | teks asli notasi Belanda, mis. "76140:9:5" |
| `nilai_gulden_utama` | integer bagian gulden saja (76140) — **anchor pencocokan paling andal**, krn di kasus Bunschoten inilah yang identik persis di kedua sumber, sedangkan kuantitas kargo yang justru beda krn galat OCR |
| `cargo_items_json` | list `{produk, qty, unit}` hasil parse regex pola "ANGKA UNIT PRODUK" (mis. `[{"produk":"lada hitam","qty":192,"unit":"bahar"}]`) — **diakui tidak sempurna**, prosa bahasa Indonesia hasil terjemahan bervariasi bentuknya |

**Artefak 2 — `docs/thesis/dr/cargo_sanity_report.csv`** (hasil pencocokan, 1 baris per pasangan yang match):

| Kolom | Isi |
|---|---|
| `dagh_register_volume`, `dagh_register_tanggal_perkiraan` | identitas baris di `daghregister_corpus.csv` (harus `record_type=single_voyage`) |
| `data_perdagangan_entry_id` | rujuk ke Artefak 1 |
| `match_method` | `gulden_exact` (prioritas 1 — cocokkan `nilai_gulden_utama`) atau `kapal_tanggal` (fallback — nama kapal ternormalisasi + kedekatan tanggal) |
| `nilai_gulden_dagh_register`, `nilai_gulden_data_perdagangan` | utk verifikasi manual |
| `qty_discrepancies_json` | list `{produk, qty_dagh_register, qty_data_perdagangan, unit, rasio}` — rasio ~10x/~100x = sinyal kuat sisipan-digit OCR (pola Bunschoten) |
| `rekomendasi` | `pakai_data_perdagangan` / `konsisten` / `perlu_review_manual` |

**Kolom baru di `daghregister_corpus.csv`** (cuma utk baris `single_voyage` yang match ke Artefak 2): `cargo_sanity_checked` (bool), `cargo_qty_flagged_ocr_error` (bool), `cargo_value_source_recommended` (`data_perdagangan`/`dagh_register`/`n/a`).

**Keterbatasan yang diakui di muka**: parsing `cargo_items_json` dari prosa itu heuristik (regex pola angka+unit+produk), bukan NLP terlatih — akan ada kasus yang gagal ter-parse rapi (ditandai `cargo_items_json=[]`, bukan dipaksa). Match rate realistis dari 18 titik overlap yang sudah diverifikasi manual sebelumnya (bukan janji 18/18 otomatis).

#### Eksekusi P0.5 ✅ SELESAI (2026-07-07)

Script: `docs/thesis/dr/extract_data_perdagangan.py` (Artefak 1) + `docs/thesis/dr/cargo_sanity_check.py` (Artefak 2).

**Artefak 1** — 15 halaman sumber dipecah jadi **69 kejadian** (rentang penuh 1660-1690, bukan cuma 1660-1669): 48 punya nama_kapal, 60 punya nilai_gulden_utama, 60 punya ≥1 cargo_item ter-parse.

**Temuan penting — blind spot P0.3 ditemukan saat eksekusi**: kasus motivasi P0.5 (fluit Bunschoten, ƒ76140:9:5) TERNYATA berlabel `record_type=lainnya`, BUKAN `single_voyage` — karena LLM re-verifikasi (P0.1 rescan) menghasilkan label `tanggal_perkiraan` berbeda antar-run ("20 MAERT" jadi "20 d.") sehingga join P0.3 ke `pelayaran_daghregister_final.csv` gagal match, padahal isi barisnya genuine single-voyage yang terkubur di entri multi-topik. **Keputusan**: P0.5 dijalankan ke SEMUA 511 baris (bukan cuma yang berlabel `single_voyage`) — gulden match jadi bukti overlap, terlepas dari `record_type`. Ini technical debt yang diwariskan ke P1.1/promosi nanti: `record_type` TIDAK 100% diandalkan sbg gerbang, harus tetap cross-check gulden/kapal.

**Hasil awal**: 25 baris cocok (2 flagged, 18 konsisten, 5 perlu_review_manual — 5 ini semua via `match_method=kapal_nama`).

**Review manual To-Do #3 (2026-07-07) — kapal_nama fallback DIHAPUS**: kelima kandidat `kapal_nama` dicek satu-satu vs teks aslinya — **0/5 lolos verifikasi**. 4 false-match total (nama jenis kapal generik kebetulan disebut di konteks tak terkait — mis. "5 Desember" soal rekomendasi fiskaal dicocokkan ke "17 Agustus" soal kargo Tortelduyf, tidak ada hubungan). 1 kasus (jacht Zeehont) kapalnya memang sama tapi **pelayaran berbeda** (kapal melakukan banyak trip; nama kapal tanpa kedekatan tanggal bukan sinyal cukup). **Keputusan: `kapal_nama` dihapus dari script**, `gulden_exact` jadi satu-satunya match_method (terbukti 100% andal di semua sampel yg dicek).

**Hasil final (setelah fix)**: **20 baris cocok** — **2 flagged `cargo_qty_flagged_ocr_error`**: (1) Bunschoten 20 Maret 1668 — lada hitam 1922 vs 192 bahar (rasio 10.01, pola sisipan-digit klasik, dikonfirmasi via gulden identik 76140); (2) jilid 1678, 23 Agustus — lada hitam 558.200 vs 338.200 pon (rasio 1.65). **18 konsisten. 0 perlu_review_manual** — bersih, tidak ada match ambigu tersisa.

Output: `daghregister_corpus.csv` resmi sekarang punya 3 kolom baru (`cargo_sanity_checked`, `cargo_qty_flagged_ocr_error`, `cargo_value_source_recommended`). Laporan lengkap: `docs/thesis/dr/cargo_sanity_report.csv`.

### P1 — Nice-to-have, bisa menyusul

**P1.1 — Kamus varian ejaan pelabuhan → nama kanonik**
- Tabel lookup (mis. `docs/thesis-port-name-variants.md` atau tabel kecil di DB) memetakan tiap varian ejaan historis (Tico→Tiku, Sillida→Salido, Aijerhadja→Air Haji, dst.) ke `Fort` yang sudah ada di `forts`. Dipakai ulang oleh pipeline manapun ke depan (GLOBALISE, jilid 7 yang belum di-OCR).

**P1.2 — Dashboard/query review manual sederhana**
- Sudah jadi open question di `docs/spec-daghregister-ingestion-api.md` — belum ada progress, tetap terbuka.

### P2 — Future considerations

- Deteksi otomatis kesalahan digit HTR tanpa perlu cross-reference manual (heuristik: total per-item vs nilai gulden dilaporkan tidak konsisten secara matematis).
- Perluasan lookup varian ejaan ke jilid 1670-1671/1676-1681 setelah OCR selesai.

## 5. Open Questions

1. ~~**(DBA)** `port_tally_aggregate` — dimodelkan gimana?~~ **RESOLVED (2026-07-07):** masuk `staging_extractions` dulu (sama seperti `single_voyage`), TIDAK live ke `salido.my.id` sampai jalur promosinya sendiri (kemungkinan `port_arrival_tallies` terpisah) diputuskan. Lihat P0.3/P0.3b.
2. **(Data)** Ambang kemiripan teks utk P0.2 (dedup) — pakai threshold otomatis (mis. Levenshtein ratio > 0.85) atau semua kandidat duplikat direview manusia satu-satu (hanya ada segelintir kasus per jilid, jadi manual mungkin lebih aman)? Non-blocking, bisa mulai manual dulu.
3. **(User)** P0.1 (rescan) ini dijalankan sebelum atau sesudah OCR 7 jilid sisanya? Keduanya sama-sama di notebook `daghregister_extraction.ipynb` tapi P0.1 tidak butuh OCR — bisa jalan duluan tanpa menunggu Tahap 0 selesai.
4. ~~**(Design/DBA)** P0.3b — bentuk konkret?~~ **RESOLVED (2026-07-07):** toggle filter navbar (pola sama toggle arah) + label teks "Sumber Data" di modal voyage — BUKAN warna/ikon pin baru (kanal warna sudah dipakai identitas Fort + arah rute). Implementasi selesai: `Voyage.source` (migration `004`, default `bgb_huygens`), `RouteAggregation`/`VoyageSchema` expose `source`, filter `?source=` di `/api/voyages` + `/api/voyages/routes` (grouped by source juga, tidak tercampur). Frontend: `.source-toggle-group` navbar + `setSource()` di `atlas.js` + `MODAL_SOURCE_LABELS`. 4 test backend baru + 9 test Django baru, semua pass. Diverifikasi Playwright (desktop 1440px bersih, mobile 390px cek — `.nav-center` memang hidden by design utk SEMUA toggle termasuk yg lama, bukan regresi baru).
5. ~~File `...1659.pdf` yang tidak dikenal~~ — **SKIP (2026-07-07, keputusan user):** tidak dikejar sekarang. Fokus scope tetap 1660 ke atas, terutama pasca-1663 (Perjanjian Painan) — periode puncak suksesi VOC di pantai barat. 1659 (di luar window thesis 1660-1789 sama sekali) tidak prioritas.

## 6. Success Metrics

- **Leading**: 100% dari 10 pelabuhan target punya ≥1 kata kunci matching di scan hasil rescan (bukan cuma di daftar `KEYWORDS_WESTKUST`, tapi benar-benar match di halaman) — kalau ada pelabuhan dgn 0 match, itu sinyal ejaan historisnya belum ditemukan.
- **Leading**: 0 baris `single_voyage` yang di-insert ke staging tanpa `direction` resolved-atau-eksplisit-unknown (tidak ada tebakan diam-diam).
- **Lagging**: setelah promosi ke `voyages`, jumlah kontradiksi yang ditemukan reviewer tesis (Bab 3) turun ke nol dibanding kalau data mentah langsung dipakai tanpa pembersihan ini.

## 7. Timeline

- Tidak ada deadline keras eksternal. Dependency utama: P0.1 (rescan) harus selesai sebelum P0.2-P0.5 bisa jalan penuh (semuanya bekerja di atas `daghregister_corpus.csv` versi ter-update).
- P0.1 tidak menunggu OCR 7 jilid sisanya (jilid itu di luar window 1660-1669) — bisa dikerjakan sekarang, paralel dgn OCR kalau user mau jalankan keduanya di sesi Colab yang sama.

---

## 8. Workflow & Board

Proyek solo — "tim" adalah topi peran dengan tanggung jawab dan gerbang keputusan berbeda (pola sama dgn `docs/sprint/sprint-board-salido-live.md`). Satu orang boleh pindah topi, **tapi item tidak boleh ke Done tanpa tanda tangan topi QA**.

### Tim DBA — skema & keputusan model data
**Scope:** kolom baru di `daghregister_corpus.csv` (`duplicate_of`, `record_type`, `direction`, `cargo_sanity_checked`, `cargo_qty_flagged_ocr_error`, `cargo_value_source_recommended`), keputusan penempatan `port_tally_aggregate` di staging, lookup varian ejaan pelabuhan (`NAME_MAPPING` di `backend/seed_data.py`).
**Gerbang keputusan:** bentuk skema kolom baru, threshold ambang (similarity dedup, gulden-match), keputusan "record_type tidak 100% jadi gerbang" (P0.5).

### Tim DevSecOps — integritas file & keamanan proses
**Scope:** semua script baca file mentah TANPA menimpa langsung (`docs/thesis/dr/*_deduped.csv`, `*_classified.csv`, `*_directioned.csv`, `*_sanitychecked.csv` sbg staging-lokal sebelum promosi manual ke `daghregister_corpus.csv`), tidak ada credential/secret di script.
**Gerbang keputusan:** kapan file staging-lokal boleh dipromosikan jadi `daghregister_corpus.csv` resmi (selalu setelah spot-check, bukan otomatis).

### Tim Tester — verifikasi tiap script
**Scope:** jalankan tiap script, spot-check hasil vs kasus known-good SEBELUM lapor ke QA. Contoh nyata sesi ini: uji ambang dedup di seluruh 233 pasangan (celah 0.038→0.163 baru dipercaya setelah dicek manual per pasangan), uji 3 iterasi classifier P0.3 (2 gagal presisi sebelum versi final), temuan blind spot P0.5 (Bunschoten salah label `record_type`) ditemukan justru saat verifikasi, bukan diabaikan.
**Gerbang keputusan:** menolak hasil script yang belum tervalidasi sample manual, walau angka agregatnya terlihat masuk akal.

### Tim QA — gerbang kualitas
**Scope:** cek acceptance criteria tiap P0.x terpenuhi (lihat §4) sebelum tandai selesai.
**Gerbang keputusan:** satu-satunya peran yang boleh memindahkan kartu ke **Done**.

### Board

| ID | Kartu | Tim | Status |
|----|-------|-----|--------|
| DR-P0.1 | Rescan 6 jilid lama, keyword lengkap — 282→311 baris (+29) | DBA ✓Tester ✓QA | **Done** |
| DR-P0.2 | Dedup lintas-jilid (`dedup_daghregister.py`) — 41 baris `duplicate_of`, ambang 0.1 tervalidasi empiris | DBA ✓Tester ✓QA | **Done** |
| DR-P0.3 | Klasifikasi `record_type` (`classify_record_type.py`) — join ke file kandidat lama + pola tally-di-pembuka, 2 iterasi ditolak Tester sebelum versi final | DBA ✓Tester ✓QA | **Done** |
| DR-P0.4 | Klasifikasi `direction` (`classify_direction.py`) — scope `single_voyage`, unknown 64,8% (jujur, bukan bug) | DBA ✓Tester ✓QA | **Done** |
| DR-P0.5 | Sanity-check kargo (`extract_data_perdagangan.py` + `cargo_sanity_check.py`) — 25 match, 2 flagged OCR-error, 1 bug parsing notasi Belanda terisolasi ke perlu_review_manual | DBA ✓Tester ✓QA | **Done** |
| DR-P0.3b | `Voyage.source` + toggle navbar + label modal (migration 004, 4+9 test baru) | DBA + DevSecOps ✓Tester ✓QA | **Done** |
| DR-STAGE-1 | Push 119 baris bersih (single_voyage+port_tally_aggregate, exclude duplikat) ke `staging_extractions` lokal (`push_to_staging.py`), idempotent-retry diverifikasi | DBA + DevSecOps ✓QA | **Done** |
| DR-BUG-2 | Bug produksi ditemukan+fixed: `staging.py` created_at/reviewed_at overflow `String(30)` (isoformat penuh 32 char) — lolos test lama krn DB di-mock. Test baru RED→GREEN, fix `.replace(microsecond=0)` | Tester (temuan) + DBA (fix) ✓QA | **Done** |
| DR-BUG-1 | Bug ditemukan Tester saat P0.5: kasus motivasi (Bunschoten) salah `record_type` krn label tanggal berubah antar-run LLM — P0.3 join TIDAK 100% andal | DevSecOps (diagnosis) ✓QA (diterima sbg known limitation, bukan blocking) | **Done** (didokumentasikan, bukan diperbaiki — technical debt eksplisit) |

**Sprint (To Do) — belum dikerjakan:**
| # | Kartu | Tim | Catatan |
|---|-------|-----|---------|
| 1 | ~~P1.1 lanjutan — perluas `NAME_MAPPING`~~ | DBA ✓QA | ✅ **Done (2026-07-07)** — scan penuh `daghregister_corpus.csv` (511 baris) + `globalise_corpus.csv` (535 baris), 10 varian baru ditemukan & ditambahkan: Silida, Periaman, Piriaman → sudah ada; Chinco/Chinko/Indrapoura/Indiapoura → Pulau Cingkuak; Aijerhadja/Aijerhadji/Ayerhadja → Air Haji. 38 entri total di `NAME_MAPPING`. 169 backend test tetap pass. |
| 2 | ~~P0.3b — bentuk konkret pembeda provenance di peta~~ | DBA + Design ✓QA | ✅ **Done (2026-07-07)** |
| 3 | ~~Review manual 5 baris `perlu_review_manual`~~ | Tester → QA | ✅ **Done (2026-07-07)** — 0/5 lolos verifikasi, `kapal_nama` fallback dihapus dari `cargo_sanity_check.py`, hasil final 20 match (2 flagged, 18 konsisten, 0 ambigu) |
| 4 | Keputusan model tabel `port_tally_aggregate` (Open Question #1, sudah resolved arah besarnya — staging dulu — tapi bentuk tabel akhir blm final) | DBA | Blocking sebelum promosi lanjut tipe ini (BUKAN blocking utk insert ke `staging_extractions` — staging_extractions generik, tidak butuh keputusan ini dulu) |
| 5 | ~~Promosi baris `single_voyage`+`port_tally_aggregate` bersih ke `staging_extractions`~~ | DBA + DevSecOps ✓QA | ✅ **Done (2026-07-07)** — script `docs/thesis/dr/push_to_staging.py`, 119 baris (108 single_voyage + 11 port_tally_aggregate, exclude 20+1 duplikat) berhasil masuk, semua `confidence_flag=unverified`. Idempotent-retry diverifikasi (0 inserted, 119 skipped_duplicate). **Bug produksi ditemukan+fixed saat eksekusi**: `staging.py` `created_at`/`reviewed_at` pakai `.isoformat()` penuh (32 char) overflow kolom `String(30)` — lolos semua test lama krn DB di-mock, baru ketahuan pas insert ke Postgres asli. Test baru `test_post_extractions_created_at_fits_column_length` (RED→GREEN), fix `.replace(microsecond=0)`. 169 backend test pass.
