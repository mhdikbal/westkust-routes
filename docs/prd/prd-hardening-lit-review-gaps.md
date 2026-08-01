# PRD: Pengerasan Model 3/5/6 dari Temuan Tinjauan Literatur (Cliodynamics, MMHP, ABM, QuantCrit)

**Status:** Draft — hasil sintesis tim MLOps atas tinjauan literatur `lit-review` mode (2026-07-29), dipetakan ke gap yang sudah tercatat sebagai Opsional/Pertanyaan Terbuka di `prd-rerun-pemodelan-data-terbaru.md` dan `prd-pemodelan-system-dynamics-game-theory.md`. **Ditambah 2026-07-31**: gap §3b dari pembacaan penuh terpisah (Porter & White 2012, Luthra dkk. 2022, `three-way-scan` mode) — independen dari lit-review 2026-07-29, tapi menyentuh gap yang sama (Model 3 Hawkes).
**Konteks:** Model 1-6 (Sentralitas/Markov/Hawkes/CLD/System Dynamics/Game Theory) sudah dieksekusi, konvergensi 5-metode terverifikasi ulang thd n=141 (`project_rerun_model_2356_n141`). PRD ini BUKAN model baru — ini paket kerja untuk mengisi gap metodologis yang literatur akademik (cliodynamics, pemodelan stokastik peristiwa, ABM, metodologi kuantitatif kritis) tunjukkan relevan terhadap gap yang SUDAH tercatat di PRD sebelumnya, bukan gap baru yang ditemukan dari nol.

---

## 1. Ringkasan Pemetaan Literatur → Gap

| # | Gap terbuka (sumber PRD) | Temuan literatur | Jenis pekerjaan |
|---|---|---|---|
| 1 | Keterbatasan Model 6 (payoff "revealed preference") — `prd-pemodelan-system-dynamics-game-theory.md` §3.3 | QuantCrit (Gillborn, Warmington & Demack, 2018) | Dokumentasi, tanpa re-run |
| 2 | Model 3 Hawkes — kaskade vs "periode sunyi" belum dimodelkan eksplisit sbg rezim | Markov-Modulated Hawkes Process, Junuthula et al. (*Annals of Applied Statistics*, 2022) | Evaluasi + kandidat model baru |
| 3 | Skala stock `I_f(t)` 1D vs 2D — `prd-pemodelan-system-dynamics-game-theory.md` §2.2 & §5.1 (Pertanyaan Terbuka #1) | Turchin & Nefedov, *Secular Cycles* (2009) — 4 variabel independen, bukan 1 sumbu | Keputusan riset + kemungkinan re-desain Model 5 |
| 4 | Opsional: join `voyages` ↔ `linimasa_events`, 6 fort 0-voyage nyata (Painan/Bayang/Nias/Natal/Singkil/Sorkam) | ABM gravity+XTENT, Chliaoutakis & Chalkiadakis (*JASSS*, 2020) | Model komplementer baru |
| 5 | Opsional: integrasi GM (409 halaman) ke Model 5 Loop 3/4 | Bayesian network dari arsip korespondensi kolonial, Ferreira & Alves (*Social Networks*, 2020) | Cetak biru integrasi data |
| 6 | Model 3 Hawkes — kernel eksponensial berasumsi eksitasi *instan*, tak menangkap jeda logistik (waktu tempuh kapal/pesan antar-fort) sebelum defeksi tetangga terjadi | Self-Exciting Hurdle Model, Porter & White (*Annals of Applied Statistics*, 2012) — kernel peluruhan **shifted negative binomial**, ditambah log-probability-gain score sbg pelengkap LR-test/p-value | Evaluasi + kandidat kernel alternatif (independen dari #2/MMHP) |

---

## 2. Prioritas #1 — Catatan Keterbatasan QuantCrit-style pada Model 6 (termurah, tanpa re-run)

**Kenapa lebih dulu**: tidak butuh komputasi ulang, murni dokumentasi. Payoff Model 6 diestimasi dari dwell-time `dominion_status` — status itu sendiri hasil pembacaan `text_asli` yang mayoritas berasal dari arsip VOC (Generale Missiven, Daghregister, CD1-CD6 ditulis dari sudut pandang VOC). QuantCrit menegaskan: kategori kuantitatif bukan netral, harus eksplisit soal siapa yang mengonstruksinya.

- **Kerjakan**: tambahkan satu paragraf keterbatasan di dekat `game_theory_payoff_matrix.csv`/`game_theory_h2_reaffirmation.json` (di skrip `docs/thesis/colab/model6_game_theory.py`, bagian docstring/print output, pola sama seperti GOTCHA di `actor_affiliation_extraction.py`): payoff "revealed preference" merefleksikan hasil yang **tercatat dan dianggap penting oleh sumber VOC**, bukan payoff riil semua pihak (kolom sudut-pandang-sumber di `project_aktor_siri_nara` sudah punya disiplin sama, tinggal diterapkan eksplisit di sini).
- **Kriteria selesai**: satu paragraf keterbatasan tertulis, dikutip di dashboard konsolidasi (`prd-dashboard-konsolidasi-pemodelan.md`) kalau ada bagian Model 6 di sana.
- **Bukan tugas sesi ini**: mengubah metode estimasi payoff — itu keputusan riset terpisah.

---

## 3. Prioritas #2 — Evaluasi Markov-Modulated Hawkes Process (MMHP) untuk Model 3

**Kenapa**: Model 3 Hawkes (n=141, branching ratio 0.677, signifikan p<0.0001) sudah kuat, tapi klaster Siklus vs Stabil/Sisa saat ini dibedakan lewat **stratifikasi post-hoc manual** (fit Hawkes terpisah per klaster). MMHP (Junuthula et al. 2022) menawarkan rezim aktif/sunyi sebagai **hidden state yang diestimasi langsung dari data**, bukan ditentukan klasternya dulu secara manual.

- **Kerjakan**:
  1. Baca `docs/thesis/colab/model3_hawkes_kaskade_event.py` dan `hawkes_model_output.json` yang ada — catat parameter (`μ, α, β`) dan hasil stratifikasi klaster saat ini sebagai baseline.
  2. Implementasi eksperimental MMHP terhadap `data/export/all_event_years.csv` (141 titik waktu) — 2 hidden state (aktif/sunyi) cukup untuk data seukuran ini, jangan overfit lebih dari itu.
  3. Bandingkan: apakah pembagian rezim MMHP (otomatis) match dengan klaster Siklus/Stabil/Sisa (manual, dari Model 2/5/6)? Kalau cocok → penguat independen keenam untuk klaim konvergensi. Kalau tidak cocok → temuan itu sendiri yang harus dilaporkan, bukan disembunyikan.
- **Kriteria selesai**: notebook/skrip eksperimen tersimpan di `docs/thesis/colab/`, hasil perbandingan (cocok/tidak) dicatat sebagai temuan baru terpisah dari klaim konvergensi 5-metode yang sudah ada — **tidak menggantikan** Model 3 lama kecuali hasilnya jelas lebih baik dan diverifikasi.
- **Bukan tugas sesi ini**: mengganti Model 3 produksi — ini eksplorasi/validasi tambahan dulu.

---

## 3b. Prioritas #2b — Evaluasi Kernel Shifted Negative Binomial (Porter & White) untuk Model 3

**Kenapa**: Model 3 kami pakai kernel eksponensial standar (eksitasi meluruh langsung setelah event pemicu). Porter & White (2012) memodelkan serangan teroris dengan kernel **shifted negative binomial** — peluruhan yang PUNCAK-nya tertunda, bukan langsung di t=0, karena butuh waktu logistik sebelum efek pemicu terasa penuh. Untuk kasus VOC, ini historis masuk akal: defeksi fort tetangga butuh waktu kapal/pesan sampai, bukan reaksi hari-yang-sama. **Independen dari MMHP (§3)** — MMHP menjawab "apakah ada rezim aktif/sunyi tersembunyi", kernel shifted-NB menjawab "bagaimana bentuk peluruhan eksitasi itu sendiri"; keduanya bisa digabung tapi tidak saling menggantikan.

- **Kerjakan**:
  1. Baca ulang `docs/thesis/colab/model3_hawkes_kaskade_event.py` — catat kernel eksponensial saat ini (parameter β) sebagai baseline pembanding.
  2. Implementasi eksperimental kernel shifted-NB terhadap `data/export/all_event_years.csv` (141 titik waktu yang sama dgn §3) — fit ulang via MLE, bandingkan AIC/log-likelihood vs kernel eksponensial produksi.
  3. Tambahkan **log-probability-gain score** (Porter & White §4) sebagai metrik pelengkap LR-test/p-value yang sudah dilaporkan — tak perlu re-run apa pun, murni metrik tambahan atas fit yang ada.
  4. Kalau AIC kernel shifted-NB menang jelas → catat sebagai kandidat, JANGAN otomatis ganti produksi (sama disiplin dgn §3). Kalau kalah/setara → catat sbg negative finding, kernel eksponensial tetap dipertahankan dgn alasan tertulis.
- **Kriteria selesai**: skrip eksperimen tersimpan terpisah di `docs/thesis/colab/`, tabel perbandingan AIC/log-prob-gain (eksponensial vs shifted-NB) dicatat, keputusan pertahankan/ganti kernel didokumentasikan eksplisit dgn alasan.
- **Bukan tugas sesi ini**: mengganti kernel produksi tanpa hasil perbandingan; menggabungkan dgn MMHP (§3) dalam satu eksperimen — jalankan terpisah dulu, evaluasi gabungan kalau keduanya sudah punya hasil independen.

---

## 4. Prioritas #3 (Keputusan Riset, Bukan Teknis) — Stock 2 Dimensi Model 5

**Kenapa**: `prd-pemodelan-system-dynamics-game-theory.md` §2.2 sudah mengakui skala `I_f(t)` satu sumbu (Aceh↔VOC) memaksakan trade-off palsu untuk `foreign_orbit`/`voc_withdrawal`. Ini SUDAH jadi Pertanyaan Terbuka #1 di PRD itu — belum dijawab pemilik riset. Turchin & Nefedov memberi preseden konkret: teori structural-demographic yang mapan memakai ≥4 variabel independen, bukan 1 sumbu, justru untuk menghindari pemaksaan trade-off semacam ini.

- **Bukan pekerjaan MLOps sepihak** — ini tetap keputusan pemilik riset, PRD ini hanya menambahkan rujukan literatur konkret sebagai bahan pertimbangan.
- **Kalau dijawab "ya, 2D"**: re-desain stock `I_aceh(t)`, `I_voc(t)` independen (tak harus jumlah 1), kalibrasi ulang loop dari matriks transisi Model 2 (pola sama seperti §2.3 PRD induk), re-run Model 5, verifikasi ulang apakah konvergensi klaster Siklus tetap berdiri dengan skala baru.
- **Kalau dijawab "tetap 1D"**: catat eksplisit alasan (mis. data terlalu tipis untuk 2 dimensi independen) di §2.2 PRD induk sebagai keputusan final, sama pola dengan keputusan "Markov standar bukan Semi-Markov" yang sudah didokumentasikan.

---

## 5. Opsional (Dampak Besar, Biaya Tinggi — Tidak Wajib)

### 5.1 ABM gravity+XTENT untuk join `voyages` ↔ `linimasa_events`

- **Kenapa**: 6 fort (Painan, Bayang, Nias, Natal, Singkil, Sorkam) adalah pos pesisir/pulau sungguhan dengan 0 voyage tercatat di `voyages` — gap data nyata, bukan struktural (beda dari Koto Tangah/Pauh yang pedalaman, lihat koreksi di `project_rerun_model_2356_n141`).
- **Kerjakan (kalau dikerjakan)**: adaptasi model gravity Chliaoutakis & Chalkiadakis — pakai `dominion_status`/`fort_id` yang sudah ada sebagai proxy "importance" node, estimasi kemungkinan hubungan dagang tersirat untuk 6 fort itu berdasarkan jarak + status kekuasaan tetangga, uji apakah hasilnya konsisten dengan `atjeh_trade_records` (152 baris) yang sudah menyebut sebagian fort ini secara naratif.
- **Kenapa opsional**: butuh desain skema baru, tidak memblokir klaim konvergensi yang sudah berdiri.

### 5.2 Bayesian archive-network sebagai cetak biru integrasi GM ke Model 5 Loop 3/4

- **Kenapa**: Loop "kejut-eksternal" (§2.4 poin 3, `prd-pemodelan-system-dynamics-game-theory.md`) berpijak ke korpus GM (409 halaman, parser sudah diperbaiki) yang belum masuk pipeline model.
- **Kerjakan (kalau dikerjakan)**: ikuti pola Ferreira & Alves — GM diperlakukan sebagai korespondensi terarah-berbobot (edge = surat/laporan, bobot = frekuensi topik, arah = pengirim→penerima), lalu volume "kejut-eksternal" (aktivitas Inggris/Prancis) per tahun diekstrak sebagai time series numerik yang jadi input eksternal Loop 3.
- **Kenapa opsional**: pekerjaan besar (ekstraksi + klasifikasi tambahan di luar yang sudah ada), tidak menghalangi validasi konvergensi yang sudah berdiri.

---

## 6. Urutan Pengerjaan Disarankan

```
#1 (catatan QuantCrit Model 6, murah)
        │
#2 (evaluasi MMHP Model 3, eksperimen terpisah, tak menggantikan produksi)
        │
#2b (evaluasi kernel shifted-NB Model 3, eksperimen terpisah dari #2 — bisa paralel dgn #2, sama-sama tak menggantikan produksi)
        │
#3 (keputusan 2D — TUNGGU jawaban pemilik riset, bukan dieksekusi otomatis)
        │
opsional (ABM join voyages, Bayesian GM Loop 3/4) — independen, paralel kalau ada kapasitas
```

---

## 7. Kontrak Keluaran

- Paragraf keterbatasan QuantCrit ditambahkan ke output/docstring Model 6 (Prioritas #1).
- Notebook eksperimen MMHP tersimpan terpisah dari skrip Model 3 produksi, hasil perbandingan rezim otomatis vs klaster manual dicatat (Prioritas #2).
- Skrip eksperimen kernel shifted-NB tersimpan terpisah, tabel AIC/log-prob-gain (eksponensial vs shifted-NB) dan keputusan pertahankan/ganti kernel dicatat (Prioritas #2b).
- Keputusan 1D/2D Model 5 didokumentasikan eksplisit di `prd-pemodelan-system-dynamics-game-theory.md` §2.2 (Prioritas #3), siapa pun jawabannya.
- Opsional (§5) hanya dieksekusi dengan persetujuan eksplisit — didaftarkan untuk visibilitas backlog.

---

## 8. Pertanyaan Terbuka (Wajib Dijawab Sebelum/Selama Eksekusi)

1. Prioritas #3 (stock 2D) — siapa pemilik keputusan riset yang perlu dikonfirmasi sebelum dieksekusi?
2. ✅ **TERJAWAB 2026-08-01**: Prioritas #2 (MMHP) — kalau hasil rezim otomatis TIDAK cocok dengan klaster manual, apakah itu dilaporkan sebagai temuan baru terpisah, atau memicu re-evaluasi klaim konvergensi yang sudah dikutip? **Jawaban: memicu re-evaluasi.** MMHP menemukan "tidak jelas" (gap Siklus 4.9pp), yang mendorong reproduksi ulang stratifikasi manual (`model3_hawkes_stratified.py`, skrip lamanya tak pernah ter-checked-in) — hasilnya klaim lama "Siklus eksklusif" TAK REPLIKASI thd data terbaru (Stabil kini juga signifikan, p=0.0031). `prd-dashboard-konsolidasi-pemodelan.md` §1 baris #2 dan memory `project_markov_hawkes_models`/`project_rerun_model_2356_n141` sudah dikoreksi. MMHP dan Hawkes-per-klaster ternyata menguji klaim kausal BEDA JENIS (regime pooled-global vs self-excitation per-klaster) — bukan kontradiksi metodologis, tapi dua pertanyaan berbeda yang kebetulan disandingkan.
3. ✅ **TERJAWAB 2026-08-01**: Prioritas #2b (kernel shifted-NB) — kalau AIC menang tipis, apa ambang batas? **Jawaban: konvensi Burnham & Anderson (2002/2004)** — ΔAIC 0-2 = dukungan substansial keduanya, 4-7 = jauh lebih lemah utk model kalah, **>10 = essentially no support utk model kalah (decisive)**. Hasil eksperimen kami: ΔAIC=18.3 (baseline=287.39, gamma=269.07) — **jauh melewati ambang 10, decisive menang kernel Gamma**. Ambang batas ini dicatat sbg keputusan metodologis baku utk perbandingan model serupa ke depan (bukan cuma sekali pakai). **TAPI**: menerapkan hasil ini ke kernel PRODUKSI (`model3_hawkes_kaskade_event.py`/`hawkes_model_output.json`) BELUM dieksekusi — itu langkah terpisah dgn efek berantai (dashboard live, angka α/β/branching yg sudah dikutip di banyak PRD/memory) yg butuh persetujuan eksplisit pemilik riset dulu, bukan otomatis krn AIC menang. Lihat §3b kriteria selesai: skrip eksperimen TETAP terpisah dari produksi.
4. Opsional §5.1/§5.2 — mana yang masuk sprint berikutnya vs tetap backlog terbuka?

---

## 9. Non-Goals Sesi Ini

- Tidak mengganti Model 3 produksi dengan MMHP tanpa hasil perbandingan eksplisit lebih dulu.
- Tidak mengganti kernel Model 3 produksi dengan shifted-NB tanpa hasil perbandingan AIC/log-prob-gain eksplisit lebih dulu (§3b).
- Tidak mengeksekusi opsional (§5) tanpa persetujuan eksplisit.
- Tidak menulis narasi thesis baru — menyusul setelah Prioritas #1-3 selesai.
- Tidak mengubah keputusan yang sudah final di PRD sebelumnya (mis. Markov standar bukan Semi-Markov) — di luar scope PRD ini.
