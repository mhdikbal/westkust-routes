# PRD: Sankey Tema-Korpus GLOBALISE + Dagh-register (Thesis)

**Status:** Draft — Open Question #1 (kategori tema) SUDAH DIPUTUSKAN (2026-07-08), sel Colab siap (`docs/thesis/colab/part_f_sankey_tema_korpus.py`), belum dijalankan
**Disusun:** 2026-07-08
**Tim (role framing):** Scrum Master, DBA, MLOps — Muhammad Ikbal
**Konteks:** lanjutan `docs/brainstorm-globalise-data-modeling.md` (2026-07-07) — dari 3 arah Sankey yang dipetakan, user memilih **arah #3 "Tema-Korpus GLOBALISE"**: jilid/tahun → tema (klasifikasi zero-shot) → pelabuhan disebut.

---

## 0. Prior Art — Baca Dulu Sebelum Membangun Apa Pun

Dua temuan yang mengubah titik berangkat spec ini:

1. **Endpoint Sankey SUDAH ADA** (`backend/routers/voyages.py` — `GET /api/voyages/analytics/sankey`, `SankeyNode`/`SankeyLink`/`SankeyResponse`) dan **hidup di production** — tapi kualitasnya belum layak: node berisi `"Batavia,Batavia (Tujuan)"` (nama mentah tak dibersihkan lewat `clean_name()`), mencampur destinasi di luar skope Westkust (Kanton, Coromandel, Republiek/Belanda). Dibangun utk arah **#1 "Perdagangan Klasik"** (Asal→Tujuan→Produk), bukan arah #3 yang dipilih di sini — endpoint ini TIDAK dipakai ulang langsung, tapi pola query-nya (SQLAlchemy group-by ke node/link) bisa jadi referensi.
2. **Frontend Sankey (`CommoditySankey.jsx`) sudah ada tapi MATI** — bagian dari stack React (`frontend/src/`) yang sudah ditinggalkan; `frontend/Dockerfile` yang aktif sekarang murni Django (`manage.py`). Jangan coba hidupkan kembali React ini — UI baru utk fitur ini harus dibangun di `frontend/map_app/` (Django+Leaflet+Chart.js, stack yang benar-benar dideploy).
3. **Pipeline zero-shot SUDAH PERNAH DIJALANKAN** (`docs/thesis/colab/slr_nlp_pipeline.ipynb`, Part C) — model `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` (NLI multibahasa, GPU T4), 4 label: `pdr_drainase`, `etr_retensi`, `hak_adat`, `tidak_relevan` (hipotesis Bahasa Indonesia). **Tapi dijalankan ke `corpus_diplomaticum`/`corpudiplomaticum_docx` (148 baris)** — bukan GLOBALISE (535 baris) atau Dagh-register, yang dipilih sbg sumber utk spec ini. Output sudah terbukti (`docs/thesis/colab/korpus_final_dengan_topik.csv`, tiap baris punya skor 0–1 per kategori) — teknik ini VALID dan siap dipakai ulang, tinggal ganti korpus input.

**Kesimpulan:** ini bukan "mulai dari nol" — model & 4 kategori sudah tervalidasi di korpus lain. Pekerjaan riil = (a) jalankan pipeline yang SAMA ke GLOBALISE+Dagh-register, (b) deteksi pelabuhan per baris (pola regex `PORT_PATTERNS` di `docs/thesis/dr/promote_coastal.py` sudah reusable), (c) agregasi jilid/tahun→tema→pelabuhan, (d) render Sankey di Django/Chart.js.

---

## 1. Problem Statement

GLOBALISE (535 baris, dataverse.nl/DANS) dan Dagh-register (470 baris non-duplikat, `daghregister_corpus.csv`) sudah discan & diterjemahkan, tapi baru "dilihat lewat satu lensa": ekstrak pelayaran per baris. 98% GLOBALISE ternyata administrasi/surat, bukan pelayaran — nilainya justru ada di *tema* (sengketa, tambang, pajak, syahbandar) yang tersebar lintas waktu dan pelabuhan, sesuatu yang tidak bisa dibaca dari daftar linear 535 baris. Tanpa agregasi visual, temuan bertema (spt sengketa Salido 1699, laporan tambang Sillida 1683-1686) tetap terkubur sbg poin data terpisah, tidak pernah menunjukkan **pola** (pelabuhan mana paling sering muncul di tema apa, sepanjang waktu). Ini menghambat Bab 3 thesis (butuh bukti "cross-check cakupan & konsistensi" komputasional atas kategori PDR/ETR/hak-adat, per Chapter Plan §revisi 2026-07-06) — validitas mixed-methods QUAL-dominant thesis SECARA EKSPLISIT butuh lapisan NLP ini, bukan cuma pembacaan kualitatif.

## 2. Goals

1. Setiap baris GLOBALISE + Dagh-register terklasifikasi ke kategori tema (skor 0-1 per kategori), direplikasi dari pipeline yang sudah tervalidasi di `corpus_diplomaticum`.
2. Deteksi pelabuhan-tersebut per baris (10 pelabuhan target + varian ejaan, pola sudah ada), termasuk baris tanpa pelabuhan spesifik (`tidak diketahui`).
3. Sankey 3-tingkat (jilid/tahun → tema → pelabuhan) yang bisa dibuka thesis-reader/peneliti, menunjukkan konsentrasi tema per pelabuhan per rentang waktu.
4. Angka scorenya bisa di-drill-down ke baris teks asli (transparansi utk audit thesis — reviewer harus bisa cek "kenapa baris ini diberi skor pdr_drainase 0.94").
5. Hasil dipakai sbg *exhibit* cross-check komputasional Bab 3 (bukan pengganti koding kualitatif manual) — outputnya CSV/JSON yang bisa dirujuk sbg lampiran, + halaman/komponen visual (lokasi: thesis-only, lihat Non-Goals).

## 3. Non-Goals

1. **Tidak menggantikan Sankey "Perdagangan Klasik"** (arah #1) — endpoint lama tetap ada, tidak disentuh; ini fitur BARU, bukan perbaikan yang lama (lihat §6 Timeline utk urutan kalau dua-duanya akan dikerjakan).
2. **Tidak ditampilkan di peta publik salido.my.id/atlas** — user brainstorm sebelumnya eksplisit menandai arah ini "thesis SAJA, bukan diusulkan utk peta publik". Kalau nanti berubah pikiran, itu keputusan produk terpisah yang perlu dibuka ulang, bukan asumsi default.
3. **Tidak membangun ulang React (`CommoditySankey.jsx`)** — stack itu mati, UI baru (kalau P1 di bawah dikerjakan) dibangun di Django/Leaflet yang aktif.
4. **Tidak mengganti/menghapus 4 kategori (PDR/ETR/hak_adat/tidak_relevan) yang sudah divalidasi thesis** — RESOLVED 2026-07-08: 3 kategori baru (`pelayaran`/`sengketa`/`syahbandar`) DITAMBAH di atasnya (bukan mengganti), lihat Open Question #1.
5. **Tidak memvalidasi ulang kappa/inter-rater agreement** utk kategori PDR/ETR/hak_adat itu sendiri — itu sudah/sedang dikerjakan di jalur thesis lain (`kappa = 0,000/0,051` tercatat di chapter plan, isu terpisah dari scope teknis Sankey ini).

## 4. User Stories

- Sebagai **peneliti (Ikbal)**, saya ingin tiap baris GLOBALISE+Dagh-register punya skor PDR/ETR/hak_adat/tidak_relevan, supaya saya bisa cross-check cakupan kategori analitis thesis secara komputasional-terukur (bukan cuma impresi baca manual).
- Sebagai **peneliti**, saya ingin tiap baris terklasifikasi juga terhubung ke pelabuhan yang disebut (kalau ada), supaya saya bisa melihat "pelabuhan mana yang paling sering muncul dgn tema PDR tinggi" — bukti pola, bukan anekdot tunggal.
- Sebagai **peneliti**, saya ingin lihat Sankey jilid/tahun→tema→pelabuhan dalam satu gambar, supaya saya punya *exhibit* visual siap-pakai utk Bab 3/4 tanpa membangun ulang chart dari nol tiap kali butuh.
- Sebagai **peneliti**, saya ingin klik/hover satu alur Sankey dan lihat baris teks asli penyusunnya, supaya saya (atau pembimbing/reviewer) bisa audit "kenapa baris ini dapat skor segini" — transparansi wajib utk klaim akademik.
- Sebagai **pembimbing/reviewer thesis**, saya ingin tahu berapa baris yg skor `tidak_relevan`-nya tinggi (di luar 3 kategori), supaya saya percaya cakupan klasifikasi bukan "dipaksakan masuk kategori apa pun".

## 5. Requirements

### P0 — Must-Have

1. **Jalankan pipeline zero-shot ke GLOBALISE (535 baris) + Dagh-register non-duplikat (470 baris)** — reuse model dari `slr_nlp_pipeline.ipynb` Part C + **7 kategori** (4 lama + `pelayaran`/`sengketa`/`syahbandar`, RESOLVED Open Question #1). Output: CSV per-baris dgn kolom `skor_<7 kategori>` + `tema_dominan` + `skor_dominan` (pola diperluas dari `korpus_final_dengan_topik.csv`). **Sel siap pakai:** `docs/thesis/colab/part_f_sankey_tema_korpus.py`.
   - **AC:** 1.005 baris (535+470) semua terklasifikasi, tidak ada baris terlewat; runtime dicatat (baseline GPU T4 dari run corpus_diplomaticum 148 baris = referensi estimasi).
2. **Deteksi pelabuhan per baris** — reuse `PORT_PATTERNS` (regex, `docs/thesis/dr/promote_coastal.py`) diperluas ke 10 pelabuhan target penuh (termasuk Inderapura, yg belum ada di pola lama). Baris tanpa match → label eksplisit `"Tidak diketahui"` (BUKAN di-drop).
   - **AC:** setiap baris py tepat 1 label pelabuhan (termasuk "Tidak diketahui"); baris dgn >1 pelabuhan disebut → ambil SEMUA (baris ikut construct multi-link, bukan pilih satu sembarang — lihat AC Sankey di bawah).
3. **Agregasi Sankey 3-tingkat**: Node tingkat 1 = jilid/rentang-tahun (binning per dekade, konsisten dgn slider tahun app), tingkat 2 = tema (4 kategori, ambil skor TERTINGGI per baris sbg tema dominan baris itu — bukan multi-tema per baris, sederhanakan dulu di v1), tingkat 3 = pelabuhan. Link weight = jumlah baris.
   - **AC:** endpoint baru `GET /api/research/sankey-tema?year_from=&year_to=` (namespace `research`, BUKAN `voyages` — data ini bukan voyage) mengembalikan `{nodes, links}` format sama dgn `SankeyResponse` yg sudah ada (reuse schema).
4. **Drill-down ke teks asli**: tiap link/node bisa di-klik → tampilkan daftar baris penyusun (teks Indonesia + skor + tanggal + pelabuhan + sumber corpus). Endpoint: `GET /api/research/sankey-tema/rows?tema=&pelabuhan=&year_from=&year_to=`.
   - **AC:** klik link Sankey → panel/modal menampilkan minimal 1 baris teks lengkap, bisa discroll kalau >1.
5. **Kualitas gerbang**: baris dgn skor kategori dominan < 0.5 (ambang, bisa disesuaikan) ditandai `low_confidence=true` di data — TIDAK di-drop, tapi visual/UI menandainya beda (lihat P1) supaya tidak menyamarkan ketidakpastian klasifikasi.
   - **AC:** field `low_confidence` ada di output CSV & response API drill-down.

### P1 — Nice-to-Have

1. **UI Sankey di halaman thesis-only** (`frontend/map_app/`, route baru mis. `/research/tema/`, TIDAK di navbar publik `/atlas/`) — pakai Chart.js (sudah ada dependency di app) atau library Sankey ringan, bukan D3 penuh baru.
2. **Toggle low_confidence** di UI — sembunyikan/tampilkan baris skor rendah, biar reviewer bisa lihat "gambar penuh" vs "gambar yang confident saja".
3. **Export CSV/JSON hasil klasifikasi** sbg lampiran thesis siap-sitasi (mis. Lampiran D).
4. **Multi-tema per baris** (kalau baris py skor tinggi di 2 kategori sekaligus, bukan cuma ambil dominan) — v2, butuh keputusan visual (Sankey multi-tema per node lebih rumit; v1 sengaja disederhanakan single-tema-dominan per AC #3 di atas).

### P2 — Future Considerations

1. **Sankey BGB Huygens tersendiri** (dikonfirmasi ulang user 2026-07-08: "data dari Huygens menarik jg utk dibikinkan pemodelannya") — arah #1 "Perdagangan Klasik" dari brainstorm awal (Asal→Tujuan→Produk→Nilai). Sumber: 4.203 voyage+cargo_items yg SUDAH bersih & live, TIDAK butuh pipeline NLP/GPU sama sekali. Endpoint `/api/voyages/analytics/sankey` sudah ada — pekerjaannya PERBAIKAN (pakai `clean_name()`/fort-mapping, batasi ke pelabuhan Westkust, bukan bangun dari nol), bukan fitur baru. **Sengaja ditunda** sampai Sankey Tema-Korpus (spec ini) selesai — jangan mulai sebelum P0 spec ini kelar.
2. Kalau GLOBALISE/Dagh-register bertambah cakupan (7 jilid OCR yg masih kosong selesai), re-run pipeline — desain skema output HARUS idempotent by `corpus_id`/`external_ref` (pola sudah established sesi ini di script promosi voyage) supaya re-run tidak duplikat.

## 6. Success Metrics

**Leading (minggu pertama pasca-selesai):**
- 100% dari 1.005 baris terklasifikasi tanpa error (tidak ada baris ke-skip diam-diam — pelajaran dari [[feedback-verify-entity-extraction-before-trusting]] & rev.9 idempotency-gap sesi ini: verifikasi row-count granular, bukan cuma total).
- Endpoint Sankey response time < 2 detik (data kecil, ~1000 baris agregat — seharusnya jauh di bawah ini, jadi ambang longgar sbg sanity check bukan target ambisius).

**Lagging (dipakai thesis, 1 bulan+):**
- Minimal 1 Sankey (atau breakdown datanya) benar-benar disitasi sbg exhibit di draft Bab 3/4.
- Cross-check komputasional dari Sankey ini SETIDAKNYA disebut eksplisit di subbagian metodologi NLP Bab 3 (bukti "dipakai", bukan cuma "dibuat").

## 7. Open Questions

1. ~~(User, thesis-metodologis, BLOCKING) GLOBALISE isinya beda konten...~~ **RESOLVED (2026-07-08):** tambah 3 kategori tema baru — `pelayaran`, `sengketa`, `syahbandar` — di ATAS 4 kategori lama (tidak mengganti). Total 7 label, `multi_label=True` (sudah dipakai Part C) sehingga tiap label tetap skor independen, tidak mengganggu 4 skor lama scr semantik. Hipotesis `tidak_relevan` ditulis ulang ("kategori-kategori tematik di atas", bukan "ketiga hal" — basisnya kini 6 kategori bertema, bukan 3). Sel Colab siap: `docs/thesis/colab/part_f_sankey_tema_korpus.py` — tempel setelah Part C (reuse `zero_shot` pipeline + `klasifikasi_batch`, JANGAN load ulang model).
2. **(User/Data)** Binning tahun: per dekade (konsisten slider app, tapi GLOBALISE rentang 1607-1834 py `tanggal_perkiraan` yg tidak selalu presisi tahun) — atau per-jilid/per-sumber sbg gantinya? Mempengaruhi bentuk node tingkat-1 Sankey.
3. **(Data)** Ambang `low_confidence` (skor < 0.5 diusulkan di P0 #5) — apakah 0.5 angka yg tepat, atau perlu dikalibrasi dari distribusi skor aktual korpus_diplomaticum yg sudah ada (148 baris) sbg referensi sebelum jalan ke 1.005 baris baru?
4. **(Non-blocking, P1)** Apakah halaman UI thesis-only ini perlu proteksi akses (mis. tidak di-index Google, atau password) — atau cukup "tidak ditaruh di navbar publik" (security-by-obscurity) sbg standar yg sama dgn halaman lain di app ini sejauh ini?

## 8. Timeline Considerations

- **Dependency keras**: Open Question #1 HARUS dijawab sebelum jalan pipeline (P0 #1) — kalau kategori berubah, seluruh run 1.005 baris perlu diulang (GPU time, meski murah, tetap bukan nol).
- **Tidak ada deadline eksternal tercatat** utk fitur ini spesifik — tapi thesis Bab 3 draft sedang berjalan (chapter plan sudah masuk revisi 2026-07-06), jadi selama ini "tertunda" NLP cross-check-nya, itu gap terbuka di draft.
- **Fase disarankan**: (1) jawab Open Question #1-3 lebih dulu (diskusi singkat, bukan riset panjang), (2) jalankan pipeline P0 #1-2 di Colab (kerja MLOps/GPU), (3) bangun endpoint+drill-down P0 #3-5 (kerja DBA/backend), (4) UI P1 kalau exhibit CSV/JSON mentah dari (2) ternyata belum cukup utk draft Bab 3/4.
