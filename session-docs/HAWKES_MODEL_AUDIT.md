# Hawkes Model Audit

Audit dilakukan 2026-08-20 terhadap implementasi "Proses Hawkes: Kaskade Defeksi" (Model 3) di repository `westkust-routes`. Tidak ada kode, data, atau konfigurasi yang diubah selama audit ini. Semua klaim di bawah diverifikasi terhadap file yang benar-benar ada di repo, bukan dari README/PRD saja.

---

## 1. Executive Summary

Model 3 adalah proses Hawkes univariat, kernel eksponensial, yang di-fit MLE terhadap **waktu kemunculan seluruh 141 baris `linimasa_events`** (semua `event_type`, tanpa pembedaan kategori). Implementasinya nyata, jalan, dan hasil signifikan secara statistik (branching ratio 0.677, p≈0.0000 vs Poisson homogen) — ini bukan prototipe kosong. Tim proyek juga sudah melakukan tinjauan literatur dan uji lanjutan yang jarang terlihat di riset serupa: evaluasi MMHP, evaluasi kernel alternatif (shifted-NB/Gamma), validasi silang ontologis via MBPP, permutation test distinctness antar-klaster, dan cek confound kapasitas administratif Model 6.

**Namun**, model ini menguji sebuah klaim jauh lebih sempit daripada tesis "Iyokan nan di urang, laluan nan di awak". Ia menjawab: *"apakah peristiwa politik/suksesi/perjanjian/konflik/diplomasi/administratif di pantai barat cenderung mengelompok dalam waktu (self-exciting), dibanding kejadian acak?"* — Ia **tidak** menjawab: *"apakah persetujuan formal diikuti ketidakpatuhan aktual, dan apakah ketidakpatuhan itu memicu ketidakpatuhan tetangga?"* Data `linimasa_events` tidak punya struktur pasangan persetujuan↔pelaksanaan, tidak punya label "defeksi" eksplisit, dan model tidak membedakan siapa memicu siapa. "Kaskade defeksi" saat ini adalah **framing naratif pada narasi peristiwa**, bukan struktur yang dikodekan secara operasional ke dalam titik data yang di-fit.

Beberapa temuan penting sudah dikoreksi ulang oleh tim sendiri (lihat memory `project_markov_hawkes_models`): klaim lama "kaskade eksklusif milik klaster Siklus" **tidak replikasi** terhadap korpus yang membesar, dan uji distinctness formal (permutation test) menunjukkan Siklus vs Stabil **tidak terbukti beda secara statistik** (p=0.0995). Disiplin self-koreksi ini kredibel dan harus dipertahankan — tapi berarti klaim spesifik-klaster yang sempat dikutip di beberapa PRD/dashboard sudah stale.

---

## 2. Repository Components

| Komponen | Lokasi | Status |
|---|---|---|
| Skrip produksi Hawkes (kernel eksponensial, pooled) | `docs/thesis/colab/model3_hawkes_kaskade_event.py` | **Berfungsi** — dijalankan manual, bukan via API |
| Output produksi | `data/export/hawkes_model_output.json` | Ada, `mu/alpha/beta/LR/p_value/n/T0/T1` + grid intensitas + daftar tahun event (di-jitter) |
| Fit terstratifikasi per klaster arketipe (Siklus/Stabil/Sisa) | `docs/thesis/colab/model3_hawkes_stratified.py` | Eksperimen, dilabeli eksplisit "BUKAN pengganti produksi" |
| Evaluasi Markov-Modulated Hawkes Process (rezim aktif/sunyi otomatis) | `docs/thesis/colab/model3_mmhp_regime_eval.py` | Eksperimen — hand-rolled 2-state Poisson-HMM (Baum-Welch), tanpa dependency `hmmlearn` |
| Evaluasi kernel alternatif shifted-NB/Gamma | `docs/thesis/colab/model3_kernel_shiftednb_eval.py` | Eksperimen — AIC decisive menang gamma (Δ18.3) tapi **tidak diterapkan ke produksi** |
| Validasi ontologis via MBPP (interval-censored, tanpa jitter) | `docs/thesis/colab/model3_mbpp_full.py` (menggantikan `model3_mbpp_eval.py` versi "lite") | Eksperimen — closed-form Eq (9)/(10)/(18) dari Rizoiu dkk. 2022, diverifikasi manual thd PDF |
| Permutation test distinctness antar-klaster | `docs/thesis/colab/model3_cluster_distinctness_test.py` | Eksperimen — hasil: TIDAK signifikan (p=0.0995) |
| Confound kapasitas administratif (terkait Model 6, bukan Model 3 langsung) | `docs/thesis/colab/model6_capacity_confound_check.py` | Eksperimen |
| Data model (skema sumber event) | `backend/models.py` `class LinimasaEvent` (L279-425) | Berfungsi, live di Postgres, endpoint `/api/research/linimasa` |
| Dashboard visual (Bokeh, embed script+div) | `backend/build_bokeh_dashboard.py` fungsi `build_hawkes_intensity()` (L144) | **Berfungsi** — baca `hawkes_model_output.json`, TIDAK menghitung ulang model apa pun |
| Endpoint API dashboard | `backend/routers/research.py` `get_pemodelan_dashboard()` (L590+) | Berfungsi, cache-aside Redis 24 jam, field `hawkes: Optional[BokehChart]` |
| PRD desain awal (Model 1-4) | `docs/prd/prd-pemodelan-kekuasaan-dagang.md` | Deskripsi model asli, §4 |
| PRD hardening/lit-review lanjutan | `docs/prd/prd-hardening-lit-review-gaps.md` | Berisi pemetaan gap→literatur, sebagian besar **sudah dieksekusi dan dijawab** (§8 pertanyaan terbuka #2-6 berstatus ✅ terjawab) |
| PRD konsolidasi dashboard | `docs/prd/prd-dashboard-konsolidasi-pemodelan.md` | Tidak dibaca detail pada audit ini — lihat §5 untuk batas cakupan |

**Belum ada / tidak ditemukan** di repository:
- Model Hawkes multivariat (matriks eksitasi antar-aktor atau antar-fort) — semua fit yang ada univariat (pooled atau split-per-klaster, tidak ada kernel silang eksplisit "fort A memicu fort B").
- Struktur data yang memasangkan event "persetujuan formal" dengan event "pelaksanaan/ketidakpatuhan" sebagai satu unit kausal.
- Endpoint atau tabel yang membedakan tipe respons VOC (represi vs abai vs negosiasi ulang) sebagai variabel model, bukan cuma narasi `notes`/`text_asli`.
- Test otomatis (pytest) untuk skrip Model 3 — semua skrip di `docs/thesis/colab/` dijalankan manual via `python3 <script>.py`, tidak ada di `backend/tests/`.

---

## 3. Current Data Pipeline

1. **Sumber dokumen**: Corpus Diplomaticum Neerlando-Indicum jilid I-VI, Daghregister (beberapa rentang tahun 1624-1659), dan korpus GLOBALISE/Huygens terjemahan (`korpus_tema_slim.csv`) — didokumentasikan panjang di docstring `LinimasaEvent` (`backend/models.py` L279-396), termasuk provenance per volume dan koreksi historis (mis. gotcha volume terlewat 2026-07-14).
2. **Ekstraksi/pembentukan event**: manual/tim (sisir volume per volume), bukan otomatis NLP untuk tabel ini — setiap baris wajib `text_asli` (kutipan verbatim). `confidence_flag` default `'unverified'` sampai dicocokkan scan asli.
3. **Normalisasi**:
   - **Tanggal**: `event_date_raw` (string bebas, mis. "27 Maret 1663") + `year` (integer, untuk sort/filter) — **presisi tahun saja**, bukan tanggal presisi hari untuk sebagian besar baris.
   - **Lokasi**: `fort_id` (FK ke `forts`, nullable) — diisi HANYA jika event jelas soal satu fort di roster 13/roster diperluas; event multi-lokasi/di luar roster → `fort_id` NULL. Dari `data/export/event_years_with_cluster.csv`: **109 dari 141 event (77%) punya fort_id** — 32 event (23%) tidak bisa dipetakan ke lokasi tunggal.
   - **Aktor**: `ruler_actor` (string bebas) — ekstraksi afiliasi terpisah (`actor_affiliation_extraction.py`) diverifikasi manual, tapi **tidak diikutsertakan sebagai variabel Model 3** sama sekali.
   - **Kategori**: `event_type` — vokabular terkendali **5 nilai**: `suksesi | perjanjian | konflik | diplomasi | administratif`. `dominion_status` — vokabular terkendali **7 nilai** (`aceh_dominion, voc_alliance, independence, relapse_aceh, foreign_orbit, voc_withdrawal, internal_conflict`), diisi hanya untuk event yang jelas soal transisi status satu fort.
4. **Penyusunan urutan peristiwa**: query SQL `SELECT year, event_date_raw, title FROM linimasa_events WHERE year IS NOT NULL ORDER BY year` diekspor manual ke `data/export/all_event_years.csv` (docstring `model3_hawkes_kaskade_event.py` L9-15) — **`event_type` dan `dominion_status` TIDAK diikutsertakan dalam ekspor input Model 3.**
5. **Input yang diterima model**: hanya `year` (dan `event_date_raw`/`title` untuk keterbacaan output, tidak dipakai fit). 141 titik waktu tak berlabel kategori apa pun.
6. **Jenis Proses Hawkes**: univariat, self-exciting, kernel eksponensial standar `λ(t) = μ + Σ α·exp(-β(t-tᵢ))` — persis rumus di PRD §4.
7. **Parameter model** (hasil aktual di `data/export/hawkes_model_output.json`, dibaca langsung): `mu=0.2573, alpha=0.4207, beta=0.6215, n=141, T0=1600, T1=1784` → branching ratio `alpha/beta = 0.677`.
8. **Proses fitting**: MLE via `scipy.optimize.minimize` metode L-BFGS-B dengan bounds eksplisit (`mu∈[1e-4,5], alpha∈[0,5], beta∈[1e-3,5]`) — bounds ditambahkan setelah ditemukan Nelder-Mead unconstrained lari ke solusi patologis (β→∞, delta-spike). **Jitter deterministik** (`jitter_ties()`) diterapkan pada event yang berbagi tahun persis sama (diverifikasi: 48/101 di korpus lama berbagi tahun, proporsi serupa di n=141) — event disebar rata dalam tahun yang sama, urutan asli dipertahankan, reproducible (bukan acak per-run).
9. **Proses evaluasi**: Likelihood Ratio Test terhadap model null Poisson homogen, `LR = 2×(nll_poisson - nll_hawkes)`, df=2, `p = 1 - chi2.cdf(LR, 2)`. Hasil produksi: `LR=75.67, p≈0.0000` → signifikan.
10. **Bentuk output & visualisasi**: JSON (`params`, grid intensitas 400 titik, daftar tahun event ter-jitter) → dirender ulang jadi kurva intensitas Bokeh oleh `build_hawkes_intensity()`, diekspos via endpoint `/api/research/pemodelan-dashboard` field `hawkes`, ditampilkan di halaman `/riset/pemodelan`.
11. **Keterhubungan hasil model ↔ sumber arsip**: **LEMAH secara teknis.** `hawkes_model_output.json` hanya menyimpan `params`, grid `intensity`, dan daftar `events` berupa **float tahun ter-jitter** — tidak ada `id`, `title`, atau `text_asli` yang disertakan. Pencocokan "5 puncak intensitas ke kluster historis nyata (1626, 1660, 1682, 1694, 1756)" yang dicatat di memory dilakukan **secara naratif/manual oleh peneliti**, bukan sebagai field terprogram yang bisa diklik-lacak dari dashboard ke baris `linimasa_events` asal.

**Perbedaan dokumentasi vs implementasi**: PRD §4 (`prd-pemodelan-kekuasaan-dagang.md`) menyebut Model 3 "Estimasi μ, α, β via MLE pada 101 titik waktu event" tanpa menyebut kategori event sama sekali — jadi dalam hal ini **implementasi konsisten dengan desain PRD** (PRD sendiri tidak pernah merancang pembedaan kategori event untuk Model 3; itu murni proses titik waktu tanpa mark). Diskrepansi yang ADA adalah antara **framing bahasa** ("kaskade defeksi" dipakai bebas di docstring/komentar berulang kali — `model6_game_theory.py` L16, `model3_kernel_shiftednb_eval.py` L9, PRD §4 sendiri) dan **apa yang benar-benar diuji** (self-excitation semua tipe event politik, bukan defeksi spesifik).

---

## 4. Current Hawkes Modeling Process

Sudah tercakup di §3 (fitting/parameter/evaluasi/output identik). Ringkasan varian yang dieksplorasi (bukan produksi):

| Varian | File | Tujuan | Hasil |
|---|---|---|---|
| Stratifikasi per klaster arketipe | `model3_hawkes_stratified.py` | Uji apakah kaskade cuma milik klaster "Siklus" (Barus/Pariaman) | Siklus n=38 branching=0.759 p<0.0001; **Stabil n=34 branching=0.368 p=0.0031 (JUGA signifikan)**; Sisa n=21 tidak signifikan (p=0.58) |
| Permutation distinctness Siklus vs Stabil | `model3_cluster_distinctness_test.py` | Apakah dua klaster signifikan itu genuinely BEDA satu sama lain | **p=0.0995 — TIDAK signifikan** pada ambang 0.05 |
| MMHP (rezim aktif/sunyi otomatis) | `model3_mmhp_regime_eval.py` | Apakah ada hidden-state rezim yang match klaster manual | Gap Siklus vs klaster lain "tidak jelas" (2.0-6.8pp di bin-width 3/5/10 tahun, semua di bawah ambang 10pp) |
| Kernel shifted negative-binomial/Gamma | `model3_kernel_shiftednb_eval.py` | Apakah eksitasi instan (eksponensial) kalah dibanding kernel puncak-tertunda | **ΔAIC=18.3 (decisive, ambang Burnham & Anderson >10)** — kernel Gamma menang jelas, k≈3.1 (puncak tertunda ~0.42 tahun) — **belum diterapkan ke produksi** |
| MBPP interval-censored (tanpa jitter) | `model3_mbpp_full.py` | Apakah branching ratio produksi artefak jitter | Branching ratio nyaris identik (0.6763 vs 0.6769, selisih <0.1%) — **memvalidasi silang klaim inti**, tapi ξ(t) MBPP terbukti monoton sehingga TIDAK bisa mengkonfirmasi/membantah temuan puncak-tertunda kernel Gamma |

Catatan metodologis kredibel yang ditemukan tim sendiri: kernel Gamma menang decisive di AIC tapi TIDAK dipindah ke produksi karena "efek berantai" (dashboard live, angka α/β/branching sudah dikutip di banyak PRD/memory) membutuhkan persetujuan eksplisit sebelum diganti (`prd-hardening-lit-review-gaps.md` §8 poin 3). Ini disiplin yang baik — tapi berarti **kurva intensitas & narasi "puncak" yang ditampilkan user saat ini masih berdasar kernel yang tim sendiri sudah punya bukti AIC lebih lemah**.

---

## 5. Current Results

- **Klaim yang bisa dipertanggungjawabkan secara statistik** (level pooled, seluruh 141 event, tanpa kategori): waktu kemunculan peristiwa politik pantai barat 1600-1784 **tidak konsisten dengan proses Poisson homogen** — ada pengelompokan temporal (self-excitation) yang signifikan (p≈0.0000), branching ratio 0.677 (di bawah 1, jadi rezim stabil/tidak eksplosif menurut definisi matematis). Klaim ini **divalidasi silang** oleh metode independen (MBPP, branching ratio konvergen <0.1% selisih).
- **Klaim yang TIDAK bisa dipertanggungjawabkan lagi** (sudah dikoreksi tim sendiri, 2026-08-01): "kaskade eksklusif milik klaster Siklus (Barus/Pariaman)" — TIDAK replikasi; Stabil juga signifikan individual, dan distinctness test formal antara keduanya gagal (p=0.0995).
- **Klaim yang belum bisa dijawab sama sekali oleh setup saat ini**: apakah event "penyulut" secara spesifik adalah persetujuan formal yang diingkari (bukan sekadar peristiwa politik apa pun), apakah kaskade menjalar antar-fort/antar-aktor tertentu (arah kausal siapa→siapa), apakah puncak intensitas historis (1626/1660/1682/1694/1756) benar-benar berkorespondensi dengan struktur "iyokan-laluan" atau cuma kepadatan arsip pada periode itu.
- Batas interpretasi eksplisit sudah ditulis tim sendiri di beberapa tempat (MBPP: ξ(t) monoton, tak bisa uji puncak tertunda; QuantCrit: payoff Model 6 dari sudut pandang sumber VOC, bukan netral) — pola kehati-hatian ini konsisten, patut dipertahankan untuk Model 3 juga.

---

## 6. Alignment with the Historical Thesis

Tesis: **"Iyokan nan di urang, laluan nan di awak"** — persetujuan formal ditampilkan, pelaksanaan aktual menyimpang/tidak penuh.

1. **Representasi operasional saat ini**: TIDAK ADA. Tidak ada kolom, tabel, atau field yang secara eksplisit mengodekan "ini event persetujuan" vs "ini event pelaksanaan/ketidakpatuhan atas persetujuan X". `event_type` (5 nilai) dan `dominion_status` (7 nilai) adalah proxy KASAR yang paling dekat, tapi keduanya dirancang untuk keperluan lain (Model 2 Markov `dominion_status` per fort, bukan pasangan janji↔tindakan).
2. **Event mana yang dianggap "persetujuan"?** Tidak didefinisikan secara terprogram. Secara naratif, `event_type='perjanjian'` adalah kandidat terdekat, tapi Model 3 tidak memfilter berdasarkan itu — semua 5 tipe dimasukkan tanpa pembedaan ke dalam satu rangkaian titik waktu.
3. **Event mana yang dianggap "defeksi"?** Tidak ada label eksplisit. `dominion_status='relapse_aceh'` atau `'voc_withdrawal'` adalah kandidat konseptual terdekat, tapi (a) hanya terisi untuk sebagian event berlabel fort, (b) **relapse_aceh dan foreign_orbit tercatat NOL observasi** di beberapa titik korpus (memory `project_markov_hawkes_models` L23-24) — data terlalu tipis untuk kategori paling relevan dengan konsep "defeksi", dan (c) Model 3 tidak memakai kolom ini sama sekali.
4. **Apakah persetujuan dan tindakan aktual bisa dipasangkan?** Tidak, secara struktural. Skema data linear-per-event (satu baris = satu peristiwa), bukan relasional (tidak ada foreign key `responds_to_event_id` atau semacamnya). Kalau ada traktat 1663 dan pelanggaran 1667, keduanya dua baris independen yang kebetulan dekat waktu — hubungan kausal itu ada di kepala peneliti (dan di `notes`/`text_asli`), bukan di struktur data yang dipakai model.
5. **Apakah model hanya mendeteksi pengelompokan temporal?** **Ya, murni ini.** Self-excitation Hawkes secara matematis persis "kejadian A meningkatkan probabilitas kejadian B segera sesudahnya" — tapi tidak tahu APA jenis A dan B, apakah A "sebab" dan B "akibat" dalam makna historis, atau keduanya kebetulan tercatat berdekatan karena arsip padat di periode itu (lihat §7 bias kepadatan arsip).
6. **Apakah model bisa menunjukkan kaskade antar-aktor/antar-lokasi?** Tidak. Semua fit yang ada (produksi + stratifikasi klaster) adalah univariat — satu λ(t) untuk sekumpulan event, bukan matriks eksitasi `α_ij` antar-fort/antar-aktor. Stratifikasi per klaster (Siklus/Stabil/Sisa) MEMBAGI data jadi grup terpisah dan fit ulang secara independen — ini BUKAN model yang menunjukkan "fort A memicu fort B", ia hanya membandingkan apakah tingkat self-excitation berbeda antar-grup fort yang sudah diklasifikasi manual sebelumnya (dari CLD, di luar Model 3 itu sendiri).
7. **Apakah hasil saat ini hanya berupa korelasi temporal?** **Ya.** LR test membuktikan self-excitation lebih baik dari Poisson homogen — ini adalah pernyataan tentang *bentuk distribusi waktu kemunculan*, bukan pernyataan kausal tentang mekanisme "persetujuan diingkari → tetangga ikut mengingkari".
8. **Klaim historis apa yang DIDUKUNG data**: "Peristiwa politik pantai barat 1600-1784 cenderung mengelompok dalam waktu, bukan tersebar acak" — pernyataan deskriptif-statistik netral, berlaku untuk SEMUA jenis event politik (suksesi, perjanjian, konflik, diplomasi, administratif), bukan spesifik defeksi.
9. **Klaim historis yang BELUM DIDUKUNG**: (a) bahwa pengelompokan itu spesifik pola "janji→ingkar", (b) bahwa Siklus (Barus/Pariaman) adalah rezim defeksi yang secara statistik berbeda dari fort lain (dikoreksi TIDAK signifikan berbeda, §5), (c) arah kausal antar-fort/antar-aktor, (d) hubungan antara puncak intensitas dan respons VOC spesifik (represi vs abai vs negosiasi ulang) — tidak ada variabel respons VOC dalam model sama sekali.
10. **Risiko kalau hasil Hawkes langsung disebut "bukti perlawanan"**: TINGGI. (a) Model tidak membedakan event penyebab formal-agreement dari sekadar suksesi/administratif — klaim "kaskade defeksi" akan mengaburkan bahwa yang diuji adalah gabungan SEMUA tipe peristiwa politik. (b) Klaim spesifik-klaster (Siklus) sudah terbukti rapuh (koreksi 2026-08-01, distinctness p=0.0995) — mengutipnya sebagai "bukti Siklus = pola perlawanan berulang" tanpa catatan koreksi itu menyesatkan. (c) Data condong ke sumber VOC (Corpus Diplomaticum, Daghregister, Generale Missiven — arsip administrasi kolonial) — kepadatan pencatatan bisa mencerminkan intensitas administrasi VOC pada periode tertentu (mis. pasca-1755 renovasi 30 negeri), bukan murni intensitas perlawanan lokal (bias kepadatan arsip, belum diuji formal). (d) Kernel yang dipakai (eksponensial) sudah punya bukti AIC lebih lemah dari alternatif (Gamma) — kurva/puncak yang ditampilkan ke publik berpotensi berbentuk berbeda kalau kernel diganti.

**Kesimpulan §6**: implementasi saat ini adalah **prasyarat teknis** yang berguna (membuktikan ada struktur temporal non-acak untuk digali lebih jauh) tapi **belum operasionalisasi konsep tesis**. Menyebut hasil Model 3 sebagai bukti langsung "iyokan nan di urang, laluan nan di awak" akan memaksakan kecocokan yang belum didukung struktur data maupun desain model saat ini.

---

## 7. Gaps and Weaknesses

**Data gaps**
- `relapse_aceh` dan `foreign_orbit` (2 dari 7 nilai `dominion_status`, paling relevan secara konseptual untuk "defeksi") tercatat nol/sangat sedikit observasi di beberapa titik korpus (`project_markov_hawkes_models`).
- 32/141 event (23%) tidak punya `fort_id` — tidak bisa dipetakan ke lokasi tunggal, otomatis dikeluarkan dari analisis berstrata klaster.
- Presisi tanggal hanya tahun untuk sebagian besar baris — proses Hawkes waktu-kontinu butuh workaround jitter buatan (lihat temporal gaps).

**Event-modeling gaps**
- `event_type` (5 nilai umum) dan `dominion_status` (7 nilai per-fort) tidak pernah dipakai sebagai filter/mark dalam fit Model 3 — semua kategori event dicampur jadi satu proses titik tak berlabel.
- Tidak ada struktur pasangan "persetujuan ↔ pelaksanaan/pelanggaran" — unit data adalah event tunggal, bukan episode bertahap (janji → tindakan dijanjikan → tindakan aktual → kepatuhan/ketidakpatuhan → respons).
- Tidak ada varian Hawkes bertanda (marked Hawkes process) yang membedakan tipe titik pemicu vs titik terpicu, walau literatur ini eksplisit disebut sebagai kemungkinan (marked/multivariate Hawkes) dan tidak diimplementasikan.

**Temporal gaps**
- Jitter deterministik (`jitter_ties()`) menyisipkan urutan sub-tahun buatan untuk 48+/141 event yang berbagi tahun persis — perlu untuk stabilitas numerik, tapi berarti urutan presisi-hari yang ditampilkan (mis. di intensitas grid) sebagian artifisial, bukan dari sumber.
- Puncak tertunda kernel Gamma (~0.42 tahun) berada DI BAWAH resolusi asli data (presisi-tahun) — tim sendiri mencatat ini sebagai risiko interpretasi (§3c PRD hardening), MBPP tidak bisa menjawabnya tuntas karena ξ(t) MBPP terbukti monoton.

**Actor and spatial gaps**
- Tidak ada dimensi aktor dalam Model 3 sama sekali — `ruler_actor`/afiliasi (VOC/Istana Aceh/Elite lokal, sudah diverifikasi terpisah di `actor_affiliation_extraction.py`) tidak diikutsertakan.
- Tidak ada matriks eksitasi antar-lokasi (siapa memicu siapa) — hanya perbandingan tingkat self-excitation ANTAR grup, bukan hubungan kausal DI DALAM grup.

**Statistical gaps**
- Tidak ada laporan interval kepercayaan untuk α, β, atau branching ratio (hanya titik estimasi MLE + LR-test p-value) — ketidakpastian parameter tidak dikuantifikasi.
- Bounds optimisasi (`beta ≤ 5`, `alpha ≤ 5`) ditambahkan untuk mencegah solusi patologis — perlu diverifikasi bahwa hasil optimal tidak menempel di batas bound (tidak ditemukan pengecekan eksplisit ini di skrip manapun yang dibaca).

**Validation gaps**
- Kernel eksponensial produksi memiliki bukti AIC lebih lemah (Δ18.3, decisive) dibanding kernel Gamma, tapi **belum diganti** dan dashboard publik (`/riset/pemodelan`) masih menampilkan kurva kernel eksponensial tanpa catatan ini di UI.
- Klaim "Siklus = klaster kaskade" sudah terbukti tidak distinctive secara statistik (p=0.0995) — perlu dicek apakah dashboard/PRD lain yang sudah mengutip klaim lama ("prd-dashboard-konsolidasi-pemodelan.md" disebut sudah dikoreksi di memory, tapi TIDAK dibaca ulang detail pada audit ini — perlu verifikasi terpisah).

**Historiographical gaps**
- Bias kepadatan arsip (event lebih banyak tercatat di periode aktivitas administratif VOC tinggi, mis. rangkaian renovasi 1755) belum diuji formal sebagai confound terhadap "kaskade" — kemungkinan λ(t) yang tinggi mencerminkan intensitas pencatatan VOC, bukan (atau tidak murni) intensitas perlawanan lokal.
- Semua sumber (Corpus Diplomaticum, Daghregister, Generale Missiven) ditulis dari sudut pandang VOC — catatan keterbatasan QuantCrit-style sudah ditambahkan untuk Model 6 (payoff) tapi **belum untuk Model 3**.

**Technical gaps**
- Tidak ada test otomatis untuk skrip Model 3 (`docs/thesis/colab/*.py` dijalankan manual, tidak masuk `backend/tests/`).
- Output Model 3 (`hawkes_model_output.json`) tidak menyimpan referensi ke `id`/`title`/`text_asli` sumber — pelacakan "puncak intensitas ↔ event historis" bergantung pada verifikasi manual peneliti, tidak bisa diklik-lacak dari dashboard.
- `docs/thesis/colab/` gitignored sebagian (dicatat di memory) — reproducibility bergantung pada disiplin commit manual; setidaknya satu skrip lama (`stratified_analysis.py` versi awal) diketahui HILANG dan harus dibangun ulang (`model3_hawkes_stratified.py`).

---

## 8. Priority Improvements

### Critical

1. **Masalah**: Model 3 tidak membedakan tipe event sama sekali — "kaskade defeksi" adalah nama tapi bukan definisi operasional dalam kode.
   **Bukti**: `data/export/all_event_years.csv` hanya berisi `year, event_date_raw, title`; skrip `model3_hawkes_kaskade_event.py` tidak pernah membaca `event_type`/`dominion_status`.
   **Dampak**: klaim publik "kaskade defeksi tervalidasi secara statistik" melebihi apa yang benar-benar diuji.
   **Komponen yang perlu diperbaiki**: definisi operasional "defeksi" (keputusan riset, lihat §9), skema ekspor data Model 3.
   **Hasil yang diharapkan**: minimal, dokumentasi eksplisit di dashboard/PRD bahwa Model 3 menguji SEMUA tipe event politik, bukan defeksi spesifik — idealnya, varian Model 3 yang di-fit hanya pada subset event berlabel eksplisit sebagai ketidakpatuhan/pelanggaran traktat.

2. **Masalah**: kurva kernel yang ditampilkan ke publik (eksponensial) sudah punya bukti AIC lebih lemah dari alternatif (Gamma, Δ18.3 decisive) tanpa catatan ini terlihat di UI.
   **Bukti**: `docs/prd/prd-hardening-lit-review-gaps.md` §8 poin 3; `model3_kernel_shiftednb_eval.py`.
   **Dampak**: pembaca dashboard melihat bentuk kurva/puncak yang tim sendiri tahu lebih lemah secara AIC dibanding alternatif yang sudah dihitung.
   **Komponen**: `build_hawkes_intensity()`, halaman `/riset/pemodelan`, atau minimal catatan footnote di dashboard.
   **Hasil yang diharapkan**: entah migrasi kernel produksi (dengan persetujuan eksplisit pemilik riset, sesuai disiplin proyek), atau catatan keterbatasan eksplisit di UI bahwa kernel alternatif terbukti lebih baik secara AIC.

### High

3. **Masalah**: klaim "Siklus = klaster kaskade eksklusif" masih mungkin dikutip di dokumen/dashboard lain yang belum diverifikasi ulang pada audit ini.
   **Bukti**: memory `project_markov_hawkes_models` mencatat koreksi 2026-08-01 diterapkan ke `prd-dashboard-konsolidasi-pemodelan.md` §1 dan beberapa memory — tapi audit ini TIDAK membaca ulang isi file itu untuk verifikasi langsung.
   **Dampak**: risiko klaim usang tetap tersebar di beberapa tempat.
   **Komponen**: `docs/prd/prd-dashboard-konsolidasi-pemodelan.md`, dashboard `/riset/pemodelan`, artifact yang dipublish sebelumnya.
   **Hasil yang diharapkan**: audit terpisah (grep semua kutipan "Siklus.*eksklusif"/"Siklus.*satu-satunya" di seluruh docs/frontend) untuk memastikan tidak ada sisa klaim lama.

4. **Masalah**: tidak ada linkage terprogram dari output model ke baris arsip sumber.
   **Bukti**: `hawkes_model_output.json` hanya berisi `params`/`intensity`/`events` (float tahun), tanpa `id`/`title`/`text_asli`.
   **Dampak**: klaim "puncak intensitas cocok dengan kluster historis X" tidak bisa diverifikasi ulang otomatis, rawan drift kalau korpus bertambah.
   **Komponen**: `model3_hawkes_kaskade_event.py` (ekspor), skema output JSON.
   **Hasil yang diharapkan**: tambahkan `event_id`/`title` ke setiap titik `events` di output, supaya dashboard bisa link balik ke `/linimasa`.

5. **Masalah**: bias kepadatan arsip (intensitas pencatatan VOC vs intensitas perlawanan riil) belum diuji sebagai confound.
   **Bukti**: tidak ditemukan skrip/analisis yang menguji korelasi antara volume dokumen per-periode (mis. halaman GM/CD per tahun) dan λ(t) Hawkes.
   **Dampak**: puncak intensitas Hawkes bisa sebagian mencerminkan "kapan VOC menulis lebih banyak", bukan murni "kapan lebih banyak defeksi terjadi" — ancaman validitas langsung terhadap interpretasi tesis.
   **Komponen**: perlu proxy volume arsip per tahun (jumlah halaman/entri korpus per tahun), uji korelasi dengan λ(t) atau jumlah event/tahun.
   **Hasil yang diharapkan**: laporan eksplisit apakah confound ini signifikan atau tidak, mengikuti pola disiplin yang sudah dipakai untuk confound Model 6 (`model6_capacity_confound_check.py`).

### Medium

6. **Masalah**: tidak ada interval kepercayaan untuk parameter Hawkes (α, β, branching ratio) — hanya titik estimasi.
   **Dampak**: sulit menilai seberapa presisi klaim "branching ratio 0.677".
   **Komponen**: `model3_hawkes_kaskade_event.py` — tambahkan bootstrap (resample event dengan penggantian, refit) atau profil likelihood.
   **Hasil yang diharapkan**: interval kepercayaan yang bisa dikutip di samping titik estimasi.

7. **Masalah**: dimensi aktor (VOC/Istana Aceh/Elite lokal, sudah diverifikasi di `actor_affiliation_extraction.py`) tidak diikutsertakan ke Model 3 sama sekali, walau sudah tersedia dan bersih.
   **Dampak**: peluang riset hilang — data yang sudah diverifikasi (0 salah klasifikasi di sampel independen) tidak dipakai untuk pertanyaan "siapa memicu siapa".
   **Komponen**: desain varian Hawkes bertanda (marked) atau bivariat sederhana (mis. event dipicu-VOC vs dipicu-lokal).
   **Hasil yang diharapkan**: eksplorasi apakah kaskade berbeda intensitasnya tergantung aktor pemicu.

8. **Masalah**: catatan keterbatasan sudut pandang sumber (QuantCrit-style, sudah ada untuk Model 6) belum ditulis untuk Model 3.
   **Komponen**: docstring/output `model3_hawkes_kaskade_event.py`.
   **Hasil yang diharapkan**: satu paragraf eksplisit bahwa event yang "tercatat" adalah yang dianggap penting oleh penulis arsip VOC, bukan seluruh peristiwa yang benar-benar terjadi.

### Low

9. **Masalah**: tidak ada test otomatis untuk skrip Model 3.
   **Dampak**: risiko regresi diam-diam kalau skrip diedit ulang (mis. saat migrasi kernel).
   **Hasil yang diharapkan**: minimal smoke test (fit terhadap data sintetik kecil, cek `alpha/beta > 0` dan p-value masuk akal) di `backend/tests/` atau folder terpisah.

10. **Masalah**: reproducibility bergantung pada disiplin manual commit `docs/thesis/colab/` (gitignored sebagian) — setidaknya satu skrip pernah hilang.
    **Hasil yang diharapkan**: audit cepat file mana di `docs/thesis/colab/` yang di-`.gitignore` vs yang tercommit, pastikan semua skrip aktif tercommit.

---

## 9. Questions Requiring Researcher Decision

Daftar ini SENGAJA tidak dijawab oleh audit ini — ini keputusan konseptual/historiografis, bukan teknis:

1. **Definisi operasional "defeksi"**: event mana secara eksplisit dianggap "persetujuan formal", mana "pelaksanaan/ketidakpatuhan"? Apakah `dominion_status='relapse_aceh'`/`'voc_withdrawal'` cukup, atau perlu kategori baru yang lebih halus (mis. "kepatuhan sebagian", "penundaan", "penghindaran diam-diam" — 5 dari 8 kategori yang diminta di §3 prompt audit ini TIDAK ADA padanan langsungnya di skema saat ini)?
2. **Apakah data cukup untuk memasangkan janji↔pelaksanaan secara formal?** Kalau tidak (kemungkinan besar, mengingat 23% event tak berlokasi & sebagian dominion_status nol observasi), apakah tesis "iyokan-laluan" tetap layak diuji kuantitatif dengan data SAAT INI, atau perlu putaran sisir arsip tambahan yang secara eksplisit mencari pasangan traktat↔pelanggaran?
3. **Kernel produksi**: apakah migrasi ke kernel Gamma (AIC menang decisive) disetujui, mengingat efek berantai ke dashboard live dan angka yang sudah dikutip di banyak PRD/memory?
4. **Skala klaim "Siklus"**: setelah distinctness test gagal (p=0.0995), apakah taksonomi Siklus/Stabil/Sisa (dari CLD, dipakai di 5+ model lain) masih layak jadi kerangka utama narasi thesis, atau perlu direvisi/dilonggarkan bahasanya di semua tempat yang mengutipnya?
5. **Bias kepadatan arsip**: apakah confound ini cukup penting untuk diuji formal SEBELUM klaim Model 3 dipakai di bab thesis, atau cukup dicatat sebagai keterbatasan naratif?
6. **Prioritas riset**: dari 10 rekomendasi §8, mana yang masuk sebelum penulisan bab thesis terkait Model 3 vs mana yang bisa jadi catatan keterbatasan tertulis saja (pola yang sudah dipakai proyek ini untuk gap lain, mis. QuantCrit Model 6)?

---

## 10. Final Assessment

**Apa yang telah berjalan**: pipeline data (arsip → `linimasa_events` terkurasi dengan disiplin sitasi kuat) berjalan dan kredibel. Model 3 sebagai proses Hawkes univariat pooled berjalan, MLE konvergen, hasil signifikan, dan — jarang terjadi di riset serupa — sudah divalidasi silang lewat metode independen (MBPP) dan diuji ulang terhadap alternatif metodologis (MMHP, kernel Gamma, permutation distinctness). Dashboard live menampilkan hasil ini ke publik via `/riset/pemodelan`.

**Apa yang bisa dipercaya**: klaim pooled-level "peristiwa politik pantai barat 1600-1784 mengelompok dalam waktu, bukan acak" (branching ratio 0.677, p≈0.0000, tervalidasi silang MBPP <0.1% selisih). Ini murni klaim statistik deskriptif tentang bentuk distribusi waktu — bukan klaim tentang defeksi, bukan klaim tentang arah kausal.

**Apa yang BELUM bisa dipercaya**: (a) setiap framing yang menyebut hasil ini sebagai "bukti kaskade defeksi" secara spesifik — kategori event tidak difilter; (b) klaim spesifik-klaster "Siklus" sebagai rezim kaskade yang berbeda secara statistik dari klaster lain — sudah dikoreksi TIDAK signifikan (p=0.0995); (c) segala interpretasi arah-kausal ("A memicu B") — model tidak punya struktur untuk itu; (d) bentuk kurva/puncak kernel eksponensial yang ditampilkan publik — kernel alternatif terbukti lebih baik secara AIC tapi belum diadopsi maupun diberi catatan di UI.

**Apakah model sudah siap dipakai dalam thesis untuk menguji "Iyokan nan di urang, laluan nan di awak"?**
**Belum.** Model saat ini menguji sebuah pertanyaan yang berdekatan tapi berbeda ("apakah event politik mengelompok dalam waktu") dari tesis yang diajukan ("apakah persetujuan formal diikuti ketidakpatuhan aktual, dan apakah ketidakpatuhan itu menular"). Menyandingkan hasil Model 3 langsung sebagai bukti tesis tanpa syarat di bawah akan memaksakan kecocokan yang tidak didukung struktur data.

**Syarat minimum sebelum analisis dilanjutkan** (bukan urutan wajib, tapi semua perlu keputusan eksplisit sebelum Model 3 dikutip sebagai bukti tesis, lihat §9):
1. Definisi operasional "defeksi" vs "kepatuhan sebagian" vs "penundaan" dll. disepakati dan dipetakan ke data yang ADA (atau data baru yang perlu disisir).
2. Keputusan eksplisit soal kernel produksi (tetap eksponensial dengan alasan tertulis, atau migrasi ke Gamma).
3. Uji confound kepadatan arsip dijalankan (atau eksplisit ditolak dengan alasan).
4. Semua kutipan klaim "Siklus eksklusif" di dokumen/dashboard lain diverifikasi ulang dan dikoreksi jika masih stale.
5. Catatan keterbatasan sudut pandang sumber (QuantCrit-style) ditambahkan ke Model 3, sama seperti Model 6.

Sampai lima syarat itu terpenuhi (atau secara eksplisit dinyatakan tidak relevan oleh pemilik riset), Model 3 sebaiknya dikutip di thesis sebagai **temuan pendukung tentang struktur temporal peristiwa politik secara umum**, bukan sebagai bukti langsung pola "iyokan nan di urang, laluan nan di awak".
