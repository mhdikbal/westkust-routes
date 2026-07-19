# PRD: Pemodelan Matematis Dinamika Kekuasaan & Dagang Pantai Barat

**Status:** Draft desain analitis — untuk dikerjakan tim MLOps di Google Colab (runtime T4) sesi berikutnya. Belum ada notebook/kode ditulis.
**Konteks:** Enam sesi sisir `docs/CD1.pdf`–`docs/CD6.pdf` (Corpus Diplomaticum Neerlando-Indicum) + sembilan volume Daghregister menghasilkan tiga tabel bertahun dan bersitasi kutipan primer: `atjeh_trade_records` (152 baris), `linimasa_events` (101 peristiwa, 1600–1775), dan `voyages` (4.700+ pelayaran). PRD ini merancang **model matematis** yang menjadikan data itu bisa dihitung — bukan cuma ditampilkan sebagai linimasa/peta — untuk kerangka riset IETPD × Ekonomi Sumbar (`docs/thesis-ietpd-hefrizal-kerangka.md`).

---

## 1. Tiga Objek Matematis dari Tiga Sumber Data

Data yang ada bukan satu jenis objek — jangan dipaksa jadi satu model:

| Sumber | Bentuk data | Objek matematis yang pas |
|---|---|---|
| `voyages` (4.700+ baris, `year`, `origin_id`→`destination_id`) | Pelayaran bertahun antar-pelabuhan | **Graf berarah berbobot, berubah tiap tahun** (temporal directed weighted graph) |
| `linimasa_events` + rencana kolom `dominion_status` (`docs/prd/prd-atlas-power-model.md`) | Status kekuasaan per fort, berubah di titik-titik event | **Rantai Markov / fungsi tangga (step function) per node** |
| Waktu kemunculan 101 event itu sendiri | Tidak seragam — mengelompok di 1656–57, 1663, 1755 | **Proses titik (point process)**, kandidat kuat: Hawkes self-exciting |

---

## 2. Model 1 — Sentralitas Pelabuhan dari `voyages`

**Sudah ada fondasinya**: Network Graph Fase 1 (`project_network_graph_fase1`) sudah membangun endpoint co-occurrence pelabuhan. Model ini memperluasnya jadi *time-aware*.

- Node = 13 fort. Edge berarah `i→j` pada tahun `t`, bobot = jumlah voyage (atau tonase jika tersedia).
- Sentralitas per tahun: mulai dari in-degree berbobot (murah), naik ke eigenvector/PageRank kalau ingin menangkap "penting karena terhubung ke yang penting":

```
C(t) = f(A(t))          # A(t) = matriks adjacency berbobot tahun t
PageRank: C = d·A·C + (1-d)/N
```

- **Output**: `C_i(t)` per fort per tahun — dipakai lihat kapan Padang naik jadi hub sekunder VOC pasca-1663, atau kapan Barus turun menjelang 1775.

---

## 3. Model 2 — Rantai Markov `dominion_status`

**Prasyarat belum terpenuhi** (lihat §6) — model ini butuh kolom `dominion_status`/`fort_id` yang baru *dirancang*, belum di-migrasi (`backend/models.py` belum punya, `alembic/versions` belum ada migrasi 011).

Begitu terisi: status tiap fort adalah fungsi tangga `s(t) ∈ {aceh_dominion, voc_alliance, independence, relapse_aceh, foreign_orbit, voc_withdrawal, internal_conflict}` yang berubah di titik-titik event. Ini definisi rantai Markov waktu-diskrit (index = urutan event, bukan tahun kalender):

```
P(i→j) = n(i→j) / Σ_k n(i→k)      # matriks transisi, dihitung dari frekuensi
E[dwell(i)] = 1 / (1 - P(i→i))    # ekspektasi lama-tinggal di state i
```

**Output konkret**: peluang Priaman relaps ke Aceh dalam N tahun setelah merdeka, ekspektasi lama sebuah fort bertahan di `voc_alliance` sebelum event berikutnya — angka, bukan narasi era.

**Trade-off yang perlu diputuskan**: Markov standar mengasumsikan *memoryless* (peluang transisi tak bergantung sudah berapa lama di state itu) — historis ini kemungkinan salah (fort loyal 50 tahun ≠ fort baru relaps 2 tahun). Semi-Markov (dwell-time-dependent) lebih jujur tapi 101 event dibagi 13 fort = rata-rata ~8 event/fort → risiko overfit kalau langsung pakai model itu. Rekomendasi: mulai Markov standar, laporkan lebar interval-kepercayaan per fort supaya jujur soal data tipis.

---

## 4. Model 3 — Proses Titik pada Waktu Kemunculan Event

Menguji kuantitatif apakah "kaskade" (mis. Traktat Painan 1663 memicu defeksi berantai) itu nyata secara statistik, bukan cuma kesan naratif dari cara linimasa ditulis.

```
λ(t) = μ + Σ_{tᵢ<t} α · exp(-β(t - tᵢ))
```

`μ` = laju dasar kemunculan event, suku kedua = efek penyulut dari event sebelumnya yang meluruh eksponensial (`β` = laju peluruhan, `α` = kekuatan penyulutan). Estimasi `μ, α, β` via MLE pada 101 titik waktu event. Kalau `α` signifikan >0 → kaskade itu nyata secara statistik, bukan cuma framing narasi.

---

## 5. Model 4 (opsional) — Elastisitas Tol pada Volume Dagang

Lensa tol/pajak/hadiah yang sudah jadi fokus sisir CD5/CD6 bisa diuji sebagai model gravitasi:

```
V_ij(t) ∝ (M_i · M_j) / tarif_tol(t)^γ
```

`M_i` = "massa ekonomi" pelabuhan (proxy: total voyage/kargo historis), `γ` diestimasi dari data untuk lihat seberapa sensitif volume dagang terhadap kenaikan tol yang disebut eksplisit di kutipan `text_asli` CD5/CD6. Prioritas rendah — butuh data tarif tol terstruktur yang saat ini masih berupa kutipan bebas, bukan kolom numerik (`docs/prd/prd-atlas-power-model.md` §8 non-goals eksplisit menolak parsing nilai tol jadi numerik — keputusan itu perlu ditinjau ulang kalau Model 4 mau dijalankan).

---

## 6. Dependency & Blocker

- **Model 2 tak bisa jalan hari ini.** `dominion_status`/`fort_id`/`tags` di `linimasa_events` baru desain di `docs/prd/prd-atlas-power-model.md`, belum migrasi (dicek: `backend/models.py` `LinimasaEvent` belum punya kolom itu, `backend/alembic/versions/` belum ada file `011_*`). Dua opsi sebelum Colab:
  - **Opsi A — backfill manual**: isi `dominion_status` per baris `linimasa_events.csv` dengan pola sisir yang sudah dipakai selama ini (baca `text_asli`, tetapkan status, catat di `notes` kalau ambigu). Konsisten dengan disiplin provenance proyek ini, tapi 101 baris = beberapa sesi.
  - **Opsi B — backfill berbantuan model di Colab (pakai T4)**: jalankan classifier/LLM ringan di Colab untuk mengusulkan `dominion_status` dari `text_asli` tiap event, lalu **verifikasi manual sebelum dipakai** — konsisten `feedback_verify_entity_extraction_before_trusting` (dua kali proyek ini kena masalah karena mempercayai ekstraksi otomatis tanpa verifikasi 1:1 ke teks asli). Ini kemungkinan alasan T4 dibutuhkan — Model 1/2/3/4 sendiri (Markov, Hawkes, PageRank, gravitasi) ringan secara komputasi dan jalan di CPU biasa untuk skala data ini (101–4.700 baris).
  - **Perlu dikonfirmasi besok**: mana dari dua opsi ini yang jadi alasan pakai T4, supaya notebook Colab dirancang sesuai (Opsi B butuh load model, Opsi A tidak).

---

## 7. Rencana Ekspor Data ke Colab

Tak ada bind-mount volume Colab↔Postgres — data diekspor sebagai CSV/JSON dulu:

```bash
docker compose exec db psql -U vocuser -d vocdb -c "\copy (SELECT * FROM voyages) TO '/tmp/voyages.csv' CSV HEADER"
docker compose exec db psql -U vocuser -d vocdb -c "\copy (SELECT * FROM linimasa_events) TO '/tmp/linimasa_events.csv' CSV HEADER"
docker compose exec db psql -U vocuser -d vocdb -c "\copy (SELECT * FROM atjeh_trade_records) TO '/tmp/atjeh_trade.csv' CSV HEADER"
docker compose exec db psql -U vocuser -d vocdb -c "\copy (SELECT * FROM forts) TO '/tmp/forts.csv' CSV HEADER"
```

lalu `docker compose cp db:/tmp/*.csv ./data/export/` dan upload ke Colab (atau mount Google Drive). **Sumber kebenaran tetap Postgres/CSV di repo** — output Colab (angka Markov, parameter Hawkes) adalah hasil turunan, tidak menggantikan `linimasa_events.csv`.

---

## 8. Deliverables Sesi Colab

1. Notebook (disimpan balik ke `docs/notebooks/` atau `scrawling/` — TBD lokasi, putuskan besok) berisi Model 1–3 minimal, Model 4 opsional.
2. Ringkasan angka yang bisa dikutip di thesis: matriks transisi Markov per fort, parameter Hawkes (`μ, α, β`) dengan interpretasi signifikansi, time series sentralitas 13 fort.
3. Rekomendasi apakah angka ini layak jadi endpoint baru (`/api/research/power-dynamics`?) atau cukup jadi lampiran statis thesis — keputusan setelah lihat hasil, bukan diasumsikan sekarang.

---

## 9. Non-Goals Sesi Ini

- Tidak menulis migrasi/kode backend (itu scope `prd-atlas-power-model.md`, terpisah).
- Tidak memutuskan Opsi A vs B untuk backfill `dominion_status` — diputuskan di awal sesi Colab besok.
- Tidak membangun UI/visualisasi baru — output sesi ini angka & notebook, bukan halaman.
