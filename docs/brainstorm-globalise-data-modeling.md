# Brainstorm: Pemodelan Data GLOBALISE/DANS untuk Westkust Routes

**Tanggal:** 2026-07-07
**Peserta (role framing):** Scrum Master, DBA, MLOps — Muhammad Ikbal
**Konteks:** `docs/thesis/globalise_corpus.csv` (535 baris, dataverse.nl/DANS, KNAW) sudah di-scraping dan dianalisis mendalam sesi ini, tapi baru dilihat lewat satu lensa: "gimana masukin ke tabel `voyages`". Sesi brainstorm ini mundur satu langkah — apa lagi yang bisa dibangun dari korpus ini, dan apakah `voyages` bahkan bentuk yang tepat.

---

## Frame

**Fakta kunci yang sudah diverifikasi (bukan asumsi):**
- GLOBALISE = 535 baris valid, **98% administrasi/register-surat**, bukan catatan pelayaran (lihat analisis tema 2026-07-07 sebelumnya di percakapan).
- Temuan paling berharga sejauh ini (syahbandar Jacobus Sedel 1694, sengketa Salido 1699, laporan tambang Sillida 1683-1686) adalah **orang & peristiwa**, bukan pelayaran — tidak akan pernah muat rapi ke `Voyage.ship_name nullable=False`.
- Data `voyages`+`cargo_items` yang SUDAH ADA (4.738 baris, BGB Huygens, bersih) justru sumber yang jauh lebih kuat untuk visualisasi flow/Sankey — belum pernah dipakai ke arah itu.
- **Pertanyaan framing yang belum terjawab:** pemodelan ini untuk pengunjung publik salido.my.id, atau untuk thesis (Bab 3/4/5)? Jawaban ini menentukan bentuk data yang benar — belum diputuskan, lihat Open Questions.

---

## Diverge — 6 arah pemodelan data (bukan variasi dari 1 ide)

| # | Ide | Sumber data | Butuh apa | Untuk siapa (dugaan) |
|---|---|---|---|---|
| 1 | **Registri orang/jabatan** (`voc_officials`: nama, jabatan, pelabuhan, rentang tanggal, sumber) | GLOBALISE + Dagh-register (ekstraksi manual/LLM per nama) | Ekstraksi NER/manual, tabel baru | Publik (layer baru di peta) + thesis |
| 2 | **Timeline insiden/sengketa** (`historical_events`: tanggal, aktor, lokasi, ringkasan, source_ref) | GLOBALISE + Dagh-register | Ekstraksi naratif per kejadian | Publik (klik pin → cerita) |
| 3 | **Heatmap densitas-sebutan** (pelabuhan × waktu, tanpa ekstraksi fakta) | GLOBALISE mentah (matched_terms sudah ada) | Cuma agregasi, TIDAK butuh GPU | Publik + thesis (Bab 3.6 keterbatasan cakupan) |
| 4 | **Halaman bibliografi/sitasi "Sumber Primer"** (inventaris/jilid/hal → topik/pelabuhan) | GLOBALISE + Dagh-register + Data Perdagangan 1660-1690 | Kurasi manual/semi-otomatis | Thesis (kredibilitas sitasi) + publik (kredibilitas app) |
| 5 | **Dashboard topik-dari-waktu** (tema pelayaran/kargo/pajak/konflik sbg tren 1607-1834) | GLOBALISE (tema sudah ditag kasar via keyword) | Klasifikasi lebih rapi (opsional GPU utk zero-shot skala besar) | Thesis SAJA (bukan diusulkan utk peta publik) |
| 6 | **Tidak masukkan GLOBALISE ke app sama sekali** — murni materi riset thesis, `voyages` tetap bersih tanpa data 98%-noise | — | — | Opsi eksplisit, bukan default |

**Insting sesi ini:** #2 (insiden/sengketa) paling kuat utk publik, #4 (bibliografi) paling kuat utk thesis. Keduanya TIDAK butuh menyelesaikan masalah `single_voyage` vs `port_tally_aggregate` dari `docs/prd-cleaning-daghregister-1660-1669.md` — masalah itu cuma muncul karena kita berasumsi "pelayaran" adalah satu-satunya bentuk target.

---

## Provoke — Sankey & pertanyaan GPU

Permintaan MLOps: infografis/Sankey, dijalankan di Colab, "kalau memungkinkan" pakai T4 GPU.

**Tantangan yang diajukan:** Sankey diagram = agregasi (groupby+sum) + plot — CPU biasa cukup, selesai dalam detik. GPU cuma relevan KALAU ada langkah klasifikasi/embedding SEBELUM Sankey-nya. Jangan pilih T4 karena kebiasaan Colab, bukan karena kebutuhan task.

**3 ide Sankey konkret, sumber & effort beda:**

1. **Sankey Perdagangan Klasik** — Asal → Tujuan → Produk → nilai. Sumber: `voyages`+`cargo_items` (4.738 baris, SUDAH BERSIH). **Tanpa GPU**, bisa jalan hari ini (pandas+plotly, menit).
2. **Sankey Era-Kategori Analitis** — Era (VOC-syahbandar 1660-1789 vs kontemporer PETI/IETPD) → kategori PDR/ETR/hak-adat → hasil (retensi-lokal vs ekstraksi). Sumber: data existing + kategori analitis thesis. **Tanpa GPU.** Visualisasi UNIK milik thesis — belum pernah dibuat siapa pun, langsung mengangkat argumen inti Bab 4/5 jadi gambar.
3. **Sankey Tema-Korpus GLOBALISE** — Jilid/tahun → tema (hasil zero-shot classification, BUKAN keyword-counting kasar) → pelabuhan disebut. Sumber: GLOBALISE+Dagh-register. **Di sinilah GPU baru masuk akal** — `docs/thesis/colab/slr_nlp_pipeline.ipynb` (T4, zero-shot) sudah ada tapi belum pernah dijalankan ke korpus GLOBALISE.

---

## Open Questions (belum dijawab, jangan diasumsikan)

1. **(User)** Pemodelan ini utamanya utk pengunjung publik salido.my.id atau utk thesis Bab 3/4/5? Menentukan mana dari 6 ide di atas yang diprioritaskan.
2. **(User)** Dari 3 ide Sankey — mau yang cepat-jalan-sekarang (opsi 1/2, data sudah ada, tanpa GPU), atau yang butuh investasi NLP dulu (opsi 3, GPU relevan)?
3. **(User, keras)** Apakah opsi #6 (jangan masukkan GLOBALISE ke app sama sekali) justru jawaban yang benar? Belum ditolak eksplisit — masih opsi hidup.
4. Kalau opsi 2 (Sankey Era-Kategori) yang paling relevan ke thesis — apakah ini menggeser prioritas dari "bersihkan Dagh-register dulu" (`docs/prd-cleaning-daghregister-1660-1669.md`) ke "bangun Sankey era-kategori duluan"? Belum diputuskan.

## Yang disisihkan (bukan sekarang, bukan dibuang)

- Dashboard topik-dari-waktu (#5) — menarik tapi eksplisit ditandai "thesis saja, bukan usulan ke peta publik" — jangan campur ke keputusan produk publik tanpa diskusi ulang.

## Next Steps yang disarankan (belum dieksekusi, tunggu jawaban Open Questions)

- Kalau publik jadi prioritas → mulai dari ide #2 (insiden/sengketa) + Sankey opsi 1 (keduanya tanpa kerja NLP baru).
- Kalau thesis jadi prioritas → mulai dari ide #4 (bibliografi) + Sankey opsi 2 (era-kategori).
- Status paralel: user sedang menjalankan OCR (Tahap 0, `daghregister_extraction.ipynb`) utk 7 jilid Dagh-register yang belum ada lapisan teks (1670-1671, 1676-1681) di Google Colab — di luar PDF, bukan OCR sebelumnya. Ini pekerjaan terpisah dari brainstorm ini, tapi hasil akhirnya (cakupan 13/13 jilid) akan memperkaya sumber data utk ide #1/#2/#4 di atas begitu selesai.
