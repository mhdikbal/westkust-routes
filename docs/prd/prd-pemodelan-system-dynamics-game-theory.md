# PRD: Model 5 (System Dynamics) & Model 6 (Game Theory) — Aktor & Strategi Kekuasaan

**Status:** Draft desain analitis — lanjutan `docs/prd/prd-pemodelan-kekuasaan-dagang.md` (Model 1–4). Belum ada kode ditulis, ini murni spesifikasi untuk direview sebelum eksekusi.
**Konteks:** Model 2 (Markov `dominion_status`) & Model 3 (Hawkes kaskade event) sudah dieksekusi dan divisualisasikan (`docs/thesis/colab/model2_markov_dominion_status.py`, `model3_hawkes_kaskade_event.py`). Review user thd hasilnya: *"sudah menuju pemodelan namun masih kurang tajam dalam analisa, siapa pihak, nama orang kemudian afiliasi, lokasi"* — model dagang statistik-lah, tapi belum menjawab **siapa** yang mengambil keputusan dan **mengapa** kaskade defeksi terjadi (bukan cuma *bahwa* itu terjadi, sudah dijawab Model 3). User usulkan dua arah: **causal system dynamics** dan **game theory** ("siapa dapat apa dengan cara apa").

---

## 1. Fondasi Baru: Ekstraksi Aktor dari `ruler_actor`

Sebelum Model 5/6 bisa jalan, ada temuan dari eksplorasi cepat (rule-based regex, BUKAN LLM — transparan & terverifikasi, sesuai disiplin `feedback_verify_entity_extraction_before_trusting`) yang jadi **fondasi wajib** kedua model:

- `linimasa_events.ruler_actor` **terisi 101/101** (selalu ada), tapi selama ini cuma teks bebas — belum pernah diekstrak jadi struktur pihak/afiliasi.
- Split by `->`/`&`/`;` menghasilkan 234 segmen aktor dari 101 event. Klasifikasi afiliasi (Istana Aceh / VOC / Elite lokal / Tawanan-warga) via keyword: 75 Elite lokal, 68 VOC, 25 Istana Aceh, 60 tak terklasifikasi (kebanyakan sebutan populasi generik "orang-orang Padang", atau nama diri tanpa gelar yg kehilangan konteks pas displit — **jujur ditandai, bukan dipaksa masuk kategori**).
- **5 tokoh berulang lintas event** (dicocokkan token nama, bukan cuma afiliasi) — ini yang jadi bahan utama Model 5/6:

| Nama | Muncul | Fort | Peran tersirat |
|---|---|---|---|
| vaandrig Joannes Sas | 9× (1693) | Nias, Batahan, Barus | Komandan tunggal ekspedisi Nias — node paling sentral di seluruh dataset |
| Groenewegen | 3× (1660–63) | Painan, Pariaman | Resident/negosiator — jembatan ke Traktat Painan |
| Pits (Jacob Jorissen) | 3× (1667–71) | Barus, Pariaman, P. Cingkuak | Penerima penyerahan Sillida & P. Cingkuak |
| Van Leene | 3× (1681–84) | Barus, Pariaman, Tiku | Komandan pasca-aliansi umum 1680 |
| Safiatuddin | 3× (1641–59) | — (istana Aceh) | Ratu Aceh — rentang cocok sejarah nyata (1641–1675), validasi internal |

**Keterbatasan yang harus dijaga di Model 5/6**: ekstraksi ini regex sederhana thd 101 baris — bukan sensus lengkap tiap individu yg disebut di `text_asli` (yg jauh lebih kaya tapi tak terstruktur). Skor akurasi belum diverifikasi manual baris-per-baris. **Sebelum dipakai sbg input formal Model 5/6, minimal spot-check 15–20 baris thd `text_asli` asli** (pola sama yg sudah berulang kali dipakai proyek ini sepanjang sesi backfill `dominion_status`).

---

## 2. Model 5 — System Dynamics (Stock, Flow, Loop Umpan-Balik)

### 2.1 Kenapa ini beda dari Model 2 (Markov)

Markov (Model 2) menjawab "P(status berikutnya | status sekarang)" — statistik transisi, tanpa mekanisme. System dynamics menjawab **mengapa** transisi itu terjadi: variabel apa naik/turun, dan lewat loop umpan-balik apa. Markov jadi **sumber kalibrasi** buat laju flow di sini (lihat §2.3) — bukan digantikan, dilengkapi.

### 2.2 Stock: "Pengaruh VOC" per fort

Definisikan stock `I_f(t)` (influence) per fort `f`, skala kontinu, bukan kategori diskrit spt `dominion_status`. Pemetaan `dominion_status` → skor numerik (perlu dikonfirmasi user, ini usulan awal berbasis definisi PRD induk §3.2):

| `dominion_status` | Skor `I` | Alasan |
|---|---|---|
| `voc_alliance` | `+1.0` | Kontrol VOC penuh |
| `independence` | `+0.3` | Bukan Aceh, tapi bukan VOC penuh — otonomi |
| `internal_conflict` | `0.0` | Netral, tak ada kekuatan luar dominan |
| `relapse_aceh` | `-0.5` | Kembali ke Aceh, tapi siklus (bukan awal) |
| `aceh_dominion` | `-1.0` | Kontrol Aceh penuh |
| `voc_withdrawal` | `-0.7` | VOC mundur sendiri — beda dari kalah ke Aceh |
| `foreign_orbit` | `-0.6` | Bukan Aceh, bukan VOC — pesaing Eropa lain |

**Peringatan eksplisit**: skala ini SATU DIMENSI (Aceh↔VOC), padahal `foreign_orbit`/`voc_withdrawal` secara konsep bukan titik di garis yg sama (lihat kritik serupa di PRD induk §7.1 soal warna "dua sumbu, bukan satu"). Kalau user mau model lebih jujur, alternatifnya **stock 2 dimensi** (`I_aceh`, `I_voc` terpisah, tak harus jumlah 1) — lebih rumit tapi tak memaksakan trade-off palsu. **Keputusan terbuka, lihat §5.**

### 2.3 Flow: kalibrasi dari Markov, bukan ditebak

Laju perubahan `dI_f/dt` didorong oleh event — pada titik event, `I_f` melompat sebesar `Δ(status_lama → status_baru)`. **Besaran lompatan dikalibrasi dari matriks transisi Model 2 yang SUDAH dihitung** (`data/export/markov_transition_matrix.csv`): transisi dgn `P` tinggi (mis. `voc_alliance→voc_alliance`, P=0.844) = flow stabil/lemah; transisi jarang (mis. `aceh_dominion→voc_withdrawal`, n=1) = flow "kejutan", tak boleh dikasih bobot loop sama kuat spt pola berulang.

### 2.4 Loop umpan-balik kandidat (dari pola yang SUDAH terlihat di Model 2/3, bukan spekulasi kosong)

Empat loop diusulkan, tiap satu berpijak ke temuan yang sudah ada:

1. **Loop penyeimbang "tekan-lalu-lepas"**: VOC ekspedisi hukuman (naikkan `I`) → represi berlebih → resentimen lokal → relaps (turunkan `I`). Berpijak ke siklus Priaman berulang (1678/1682/1684/1712, sudah di Model 2).
2. **Loop penguat "aliansi-investasi"**: `voc_alliance` terbentuk → VOC tambah pos/faktorij → ikatan makin kuat → `I` makin tinggi. Berpijak ke `E[dwell(voc_alliance)]=4.07 event` (n=57, P(self)=0.754 [95% CI 0.629–0.848], Model 2, jauh lebih lama dari status lain -- **diperbarui 2026-08-01** dari angka lama 6.4 event, drift akibat korpus linimasa terus diperluas sejak PRD ini ditulis; lihat `data/export/markov_counts.csv`/`markov_transition_matrix.csv`).
3. **Loop kejut-eksternal**: aktivitas Inggris/Prancis naik → VOC percepat renovasi traktat (rangkaian 1755, puncak Hawkes ke-5) → `I` naik sementara, tapi cuma reaktif bukan organik.
4. **Loop aktor-berulang**: kehadiran komandan yg sama (Sas/Groenewegen/Pits/Van Leene, §1) di banyak fort berturutan mengindikasikan "kapasitas administratif VOC" sendiri sbg stock terpisah yg membatasi berapa fort bisa ditangani bersamaan — komandan yg sama dipindah-pindah, bukan tiap fort dapat komandan baru.

### 2.5 Metode simulasi

Integrasi Euler sederhana pada `dI_f/dt` per fort dgn parameter loop dikalibrasi dari §2.3, dijalankan di rentang 1600–1775. Output: kurva `I_f(t)` simulasi vs `dominion_status` aktual (Model 2) sbg validasi — kalau simulasi meleset jauh dari pola nyata, loop-nya salah desain, bukan datanya salah.

---

## 3. Model 6 — Game Theory ("siapa dapat apa, dengan cara apa")

### 3.1 Pemain

Bukan individu (data terlalu tipis per-individu, §1), tapi **3 tipe pemain** per fort per episode keputusan:

| Pemain | Diwakili oleh | Sumber data |
|---|---|---|
| VOC | Komandan/komisaris yg ditugaskan (Sas, Pits, dst) | segmen afiliasi "VOC", §1 |
| Istana Aceh | Sultan/Ratu/utusan | segmen afiliasi "Istana Aceh", §1 |
| Elite lokal (fort) | Panglima/Radja/regenten | segmen afiliasi "Elite lokal", §1 |

### 3.2 Strategi per pemain

- **Elite lokal**: `{beraliansi VOC, tetap Aceh, dua-jalur/hedging, berdaulat sendiri}`
- **VOC**: `{tawarkan traktat, ekspedisi hukuman, mundur, abaikan}`
- **Istana Aceh**: `{tuntut tol/upeti, serang balik, biarkan}`

### 3.3 Payoff — dari hasil transisi EMPIRIS, bukan diasumsikan

Alih-alih menebak payoff, **balik dari data**: tiap kombinasi strategi yg benar-benar terjadi (dibaca dari `dominion_status` hasil + siapa aktor yg terlibat, §1) dianggap "revealed preference" — payoff diestimasi dari **frekuensi & dwell-time hasil itu** (Model 2 sudah menghitung `E[dwell]` per status = proxy "berapa lama suatu hasil bertahan", makin lama makin tinggi payoff bagi pemain yg diuntungkan status itu).

### 3.4 Jenis game & pertanyaan yang diuji

Given konteks 175 tahun & fort yg sama menghadapi pilihan berulang (bukan sekali potong): **repeated game**, bukan game statis satu-shot. Pertanyaan yang bisa diuji kuantitatif:

- Apakah kaskade defeksi (Model 3, signifikan p<0.0001) konsisten dgn **efek bandwagon/coordination game** — begitu 1-2 fort tetangga beraliansi VOC, biaya/risiko fort lain ikut beraliansi turun (lihat puncak Hawkes 1693: 7 traktat Nias serentak persis pola ini)?
- Apakah pola relaps Priaman (Model 2) cocok **prisoner's-dilemma berulang** (Aceh & VOC sama-sama untung dari status quo pendek, tapi tergoda "khianat" jangka pendek yg berujung siklus)?

---

## 4. Kontrak Keluaran

Sama pola Model 2/3 — CSV/JSON hasil komputasi + artifact visualisasi terpisah (dashboard baru, bukan ditambah ke dashboard Model 2/3 yg sudah ada, biar tak terlalu padat satu halaman):
- `data/export/system_dynamics_output.json` — kurva `I_f(t)` simulasi per fort
- `data/export/game_theory_payoffs.json` — matriks payoff terestimasi + hasil uji kesesuaian-kaskade

---

## 5. Pertanyaan Terbuka (WAJIB dijawab user sebelum eksekusi)

1. **Stock 1 dimensi (Aceh↔VOC, §2.2) atau 2 dimensi terpisah** (`I_aceh`, `I_voc` independen, lebih jujur tapi lebih rumit)?
2. **Verifikasi aktor dulu** (§1, spot-check 15–20 baris thd `text_asli`) sebelum Model 5/6 jalan, atau langsung pakai draft ekstraksi dgn disclaimer "belum diverifikasi"?
3. Model 6 pakai **3 tipe pemain generik** (VOC/Aceh/Elite lokal, §3.1) atau coba tetap per-individu utk 5 tokoh berulang (Sas dkk, §1) meski datanya tipis (9 observasi utk Sas terbanyak, sisanya cuma 2–3)?
4. Prioritas eksekusi: **System Dynamics dulu** (bisa langsung kalibrasi dari Model 2 yg sudah ada, lebih siap) atau **Game Theory dulu** (lebih relevan langsung ke pertanyaan "siapa dapat apa" yg diajukan user)?
5. Dashboard baru terpisah, atau pertimbangkan gabung ke artifact Model 2/3 yg sudah ada (trade-off: halaman makin padat vs konteks makin utuh satu tempat)?

---

## 6. Non-Goals Sesi Ini

- Verifikasi manual ekstraksi aktor (§1) — perlu sesi baca `text_asli` terpisah, sama disiplin `feedback_verify_entity_extraction_before_trusting`.
- Implementasi kode Model 5/6 — PRD ini murni spesifikasi utk direview, follow-up terpisah setelah §5 dijawab.
- Ekstraksi entitas penuh dari `text_asli` (di luar `ruler_actor`) — cakupan jauh lebih besar, di luar scope PRD ini.
- Payoff/parameter final Model 6 — §3.3 baru usulan pendekatan ("revealed preference dari dwell-time"), bukan angka final.
