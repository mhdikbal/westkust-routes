> **DRAFT SIMULATION/RECOVERY DESIGN**
> **NO SIMULATION EXECUTED**
> **NO FITTING ON REAL DATA**
> **NOT PRODUCTION DATA**
> **RESEARCHER REVIEW REQUIRED**

---

## 0. Scope

Merancang — **bukan menjalankan** — protokol simulasi/parameter-recovery
untuk memutuskan apakah spesifikasi **M3B-CD** (Hawkes + kovariat densitas
arsip CD) layak di-fit terhadap 141 event `linimasa_events` nyata. Tidak
ada simulasi dijalankan, tidak ada fitting 141 event, GM/Daghregister
tidak dipakai sebagai co-primary exposure, tidak ada combined density
dibuat, Model 3/3B produksi tidak diubah.

**Konteks nyata yang dipakai untuk mengalibrasi rancangan** (dibaca dari
`HAWKES_MODEL_AUDIT.md`, bukan diasumsikan):
- Model 3 (Hawkes baseline) hasil aktual: `mu=0.2573, alpha=0.4207,
  beta=0.6215, n=141, T0=1600, T1=1784` → branching ratio `alpha/beta =
  0.677`. Signifikan vs Poisson homogen (p≈0.0000), tervalidasi silang
  via MBPP (<0.1% selisih branching ratio).
- CD density (`CD_ANNUAL_DOCUMENT_DENSITY_WORKING.csv`, window 1600–1784):
  Spec A total inside window = 1.003 dokumen/185 tahun, 172 tahun
  `observed_positive`, 13 tahun `observed_zero` (dipercaya), tahun
  count tertinggi 1695 (n=28), median tahunan 4.
- Status komparasi (`MODEL_3B_ARCHIVAL_DENSITY_COMPARISON_MATRIX.md`):
  CD = `CD_PRIMARY_EXPOSURE_READY_FOR_SIMULATION_REVIEW` (bukan
  `READY_FOR_FITTING`) — `circularity_risk: possible` (CD adalah salah
  satu korpus sumber `linimasa_events.csv`) — **inilah alasan tepat
  kenapa tahap simulation/recovery ini diperlukan SEBELUM fitting nyata**.

---

## 1. Spesifikasi Model

### M1 — Hawkes baseline (Model 3 produksi, referensi)
```
lambda(t) = mu + sum_{ti<t} alpha * exp[-beta*(t - ti)]
```
Parameter: `mu > 0`, `alpha >= 0`, `beta > 0`. Nilai produksi (untuk
kalibrasi grid simulasi, §3): `mu=0.2573, alpha=0.4207, beta=0.6215`.

### M2 — CD-density-only Poisson (inhomogen, tanpa self-excitation)
```
lambda(t) = exp[theta0 + theta1 * x_CD(t)]
```
`x_CD(t)` = kovariat densitas arsip CD pada waktu `t` (lihat §1.3 untuk
transformasi kandidat — **bukan final**).

### M3B-CD — gabungan density + self-excitation
```
lambda(t) = exp[theta0 + theta1 * x_CD(t)] + sum_{ti<t} alpha * exp[-beta*(t - ti)]
```
**Catatan struktural penting** (dikoreksi dari notasi instruksi, yang
menuliskan `sum[theta0 + [-beta(t-ti)]` — ini digabungkan sesuai makna
matematis yang konsisten dengan M1+M2, bukan disalin apa adanya karena
bentuk asli tidak well-formed): base-rate log-linear (dari M2)
**ditambah** komponen self-excitation eksponensial standar (dari M1).
`theta0` hanya muncul SEKALI, di dalam `exp[...]`, bukan di dalam
penjumlahan self-excitation.

### 1.3 — Kandidat Transformasi Densitas (Tidak Final)
```
x_CD(t) = log(1 + CD_t)
```
Dipakai sebagai **kandidat kerja** untuk simulasi — **BUKAN** ditetapkan
sebagai transformasi final untuk fitting nyata. Alasan memilih ini
sebagai titik awal: `CD_t` berkisar 0–28 per tahun (median 4, §0),
`log(1+x)` meredam pengaruh tahun-ekstrem (mis. 1695, n=28) tanpa
membuang informasi tahun `CD_t=0` (13 tahun `observed_zero`, dipercaya —
lihat §0). Transformasi alternatif yang HARUS diuji di tahap
identifiability terpisah (di luar cakupan simulasi ini, dicatat sbg
keputusan terbuka §6): `x_CD(t) = CD_t` (linear), `x_CD(t) = sqrt(CD_t)`,
`x_CD(t)` dikategorikan (tercile/kuartil).

---

## 2. Skenario Simulasi (Dirancang, Belum Dijalankan)

Delapan skenario minimum diminta + kalibrasi konkret per skenario:

| # | Skenario | Parameter simulasi (ground truth) | Tujuan uji |
|---|---|---|---|
| 1 | **Density effect saja** | `alpha=0` (murni M2); `theta0`, `theta1` bervariasi (§3) | Pastikan fitting M3B-CD **tidak** memunculkan `alpha` palsu ketika data sungguh murni digerakkan densitas (kriteria gate §5 poin 1) |
| 2 | **Self-excitation saja** | `theta1=0` (murni M1); `mu`≈exp(theta0) dikalibrasi ke `mu=0.2573` produksi | Pastikan fitting M3B-CD **tidak** memaksakan `theta1` signifikan palsu ketika data murni Hawkes tanpa kovariat |
| 3 | **Density + self-excitation bersama** | `alpha=0.4207, beta=0.6215` (nilai produksi) + `theta1` sedang (§3) | Uji recovery gabungan — kasus paling mendekati realita jika M3B-CD benar |
| 4 | **Density sangat kuat, excitation lemah** | `theta1` besar (mis. 3× nilai skenario 3); `alpha` kecil (mis. 0.1×`alpha` produksi) | Uji apakah `theta1` "menyerap" sisa variasi yang sebetulnya berasal dari `alpha` kecil (kriteria gate §5 poin 2, arah sebaliknya) |
| 5 | **Density lemah, excitation kuat** | `theta1` kecil (mendekati 0 tapi bukan nol); `alpha` besar (mis. mendekati batas branching ratio 0.9) | Uji apakah `alpha`/`beta` bisa dipulihkan tanpa terdistorsi oleh `theta1` residual kecil |
| 6 | **Window & jumlah event ≈ Model 3** | `T0=1600, T1=1784` (identik produksi); simulasikan realisasi hingga **n≈141 event** (bukan dipaksa persis 141 — dicatat rentang target n=130–150 dgn banyak replikasi) | Kalibrasi realistis langsung ke ukuran sampel aktual, bukan asimtotik n besar |
| 7 | **Misspecification density** | Data disimulasikan dengan `x_CD(t)` versi TIDAK log — mis. `x_CD_true(t) = CD_t` linear atau `sqrt(CD_t)` — TAPI model fitting tetap memakai `log(1+CD_t)` (§1.3) | Uji sensitivitas kesimpulan (khususnya `alpha`/branching ratio) terhadap transformasi densitas yang salah dipilih (kriteria gate §5 poin 4) |
| 8 | **Kernel Gamma disimulasikan, di-fit eksponensial** | Data disimulasikan dgn kernel Hawkes ber-densitas Gamma (shape≠1) untuk waktu-tunggu excitation; model fitting tetap eksponensial standar (M1/M3B-CD) | Uji apakah misspecification kernel (bukan cuma misspecification kovariat) mendistorsi `alpha`/`beta`/branching ratio yang dipulihkan — relevan krn `HAWKES_MODEL_AUDIT.md` sendiri mencatat evaluasi kernel Gamma sbg salah satu uji lanjutan Model 3 |

Setiap skenario: **≥200 replikasi Monte Carlo** disarankan sbg minimum
metodologis standar untuk recovery study (bukan dieksekusi di tahap ini
— dicatat sbg parameter desain, keputusan jumlah pasti replikasi
ditinggalkan ke §6).

---

## 3. Parameter Grid

| Parameter | Nilai kalibrasi dasar (dari Model 3 produksi) | Rentang grid yang diusulkan untuk simulasi |
|---|---|---|
| `mu` (atau `theta0` via `mu=exp(theta0)` saat `theta1=0`) | 0.2573 | {0.5×, 1×, 2×} → {0.129, 0.257, 0.514} |
| `alpha` | 0.4207 | {0, 0.1×, 0.5×, 1×, ~2×(mendekati batas stabil)} → {0, 0.042, 0.210, 0.421, 0.75} |
| `beta` | 0.6215 | {0.5×, 1×, 2×} → {0.311, 0.622, 1.243} (memengaruhi durasi efektif excitation, bukan hanya branching ratio) |
| Branching ratio (`alpha/beta`) turunan | 0.677 | {0, 0.2, 0.5, 0.677, ~0.9 (dekat rezim eksplosif)} |
| `theta1` | tidak ada nilai produksi (M3B-CD belum pernah di-fit) | {0 (skenario 2), kecil, sedang (dikalibrasi agar kontribusi rata-rata `theta1*x_CD(t)` sebanding urutan-besaran dgn `mu` produksi), besar (skenario 4)} — **nilai eksak grid ditentukan saat implementasi**, bukan di sini |
| `theta0` | — | dikalibrasi agar `exp(theta0)` di kisaran `mu` produksi saat `x_CD(t)=0` (13 tahun observed_zero, §0) |
| `T0, T1` | 1600, 1784 | tetap (skenario 6 wajib pakai ini, skenario lain boleh variasikan panjang window sbg uji tambahan opsional) |
| `n` (jumlah event realisasi) | 141 (Model 3 aktual) | target 130–150 per replikasi (skenario 6); skenario lain boleh n lebih besar untuk isolasi bias asimtotik dari bias-sampel-kecil |
| `x_CD(t)` realisasi | Spec A CD 1.003 dokumen/185 tahun (§0) | dipakai APA ADANYA sbg kovariat riil (bukan disimulasikan sintetik) — realisme desain: proses titik event DISIMULASIKAN, tapi kovariat densitas dipakai dari data CD asli agar recovery test relevan dgn struktur kovariat sesungguhnya (termasuk 13 tahun nol, lonjakan 1695, dst.) |

---

## 4. Evaluation Metrics

Untuk setiap parameter (`theta0, theta1, alpha, beta`, dan turunan
`branching_ratio = alpha/beta`), dan untuk setiap skenario (§2) ×
titik grid (§3):

| Metrik | Definisi operasional |
|---|---|
| **Bias** | `mean(estimate) - true_value` lintas replikasi |
| **RMSE** | `sqrt(mean((estimate - true_value)^2))` |
| **Interval coverage** | proporsi replikasi di mana CI (mis. profile-likelihood atau bootstrap — metode ditentukan saat implementasi) memuat nilai sebenarnya; target nominal 95% CI harus dekati ~95% empirik |
| **False-positive excitation** | proporsi replikasi skenario 1 (`alpha_true=0`) di mana `alpha` estimasi signifikan berbeda dari 0 (mis. LR-test p<0.05 ATAU CI tidak memuat 0) |
| **False-negative excitation** | proporsi replikasi skenario 3/5 (`alpha_true>0` bermakna) di mana `alpha` estimasi TIDAK signifikan berbeda dari 0 |
| **Convergence failure** | proporsi replikasi di mana optimizer (mis. L-BFGS-B, mengikuti pola Model 3 produksi §0) gagal konvergen, menyentuh batas (`bounds`), atau menghasilkan `alpha→0`/`beta→∞` patologis (pola persis yang sudah pernah ditemukan di Model 3 produksi dgn Nelder-Mead unconstrained, `HAWKES_MODEL_AUDIT.md` §7) |

Dilaporkan **per skenario, per titik grid** — bukan agregat tunggal
lintas semua kondisi (agregasi tunggal akan menyembunyikan pola
kegagalan spesifik-kondisi, bertentangan dgn §5 poin 5).

---

## 5. Identifiability Risks

1. **`theta1` menyerap self-excitation** — bila densitas arsip CD dan
   pengelompokan temporal event kebetulan berkorelasi (mis. tahun padat
   dokumen CD juga tahun padat event linimasa — plausibel krn CD
   sebagian menjadi SUMBER event, `circularity: possible`, §0), `theta1`
   bisa menangkap variasi yang sebetulnya berasal dari `alpha` murni
   (skenario 2 dirancang khusus mendeteksi ini).
2. **`alpha` menyerap efek densitas** — arah sebaliknya: base-rate yang
   sebetulnya digerakkan `x_CD(t)` bisa keliru ditafsir sbg self-excitation
   bila lonjakan densitas CD (mis. 1695, n=28) kebetulan berdekatan
   waktu dgn klaster event lain (skenario 4 dirancang khusus ini).
3. **Circularity structural** (bukan cuma statistik) — CD adalah salah
   satu korpus SUMBER `linimasa_events.csv` (§0, dari
   `MODEL_3B_ARCHIVAL_DENSITY_COMPARISON_MATRIX.md` §D). Simulasi
   parameter-recovery di sini HANYA menguji identifiability statistik
   (bisakah `theta1` dan `alpha` dibedakan secara numerik) — **TIDAK
   menguji/menyelesaikan** pertanyaan provenance (apakah exposure CD
   dan outcome event punya sumber data yang tumpang tindih secara
   desain). Ini risiko terpisah yang HARUS diselesaikan lewat penelusuran
   provenance historis (di luar simulasi statistik), dicatat eksplisit
   sbg keputusan terbuka §6 — bukan sesuatu yang bisa "lolos" hanya
   krn simulasi recovery menunjukkan hasil bagus secara numerik.
4. **Sensitivitas transformasi tunggal** — bila kesimpulan (arah/besaran
   `theta1`, atau bahkan tanda `alpha`) berubah drastis hanya krn ganti
   `log(1+CD_t)` → `CD_t` linear (skenario 7), itu tandanya kesimpulan
   TIDAK robust terhadap pilihan transformasi — model belum layak
   dipakai utk klaim substantif apapun sampai sensitivitas ini
   dikarakterisasi.
5. **Window sempit + n kecil (141 event/185 tahun)** — kombinasi window
   pendek dan jumlah event moderat (bukan asimtotik besar) adalah rezim
   di mana bias parameter Hawkes DIKETAHUI bisa besar di literatur umum
   proses titik — skenario 6 dirancang KHUSUS mengukur ini pada skala
   realistis proyek, bukan skala ideal buku teks.
6. **Misspecification kernel tak terdeteksi** — bila data sebenarnya
   berkernel Gamma tapi selalu di-fit eksponensial (standar praktik
   proyek ini sejauh ini), branching ratio yang dilaporkan bisa bias
   sistematis TANPA tanda-tanda kegagalan konvergensi (skenario 8) —
   risiko "salah tapi terlihat meyakinkan", bukan "gagal dan terlihat
   gagal".

---

## 6. Failure Criteria (Decision Gate)

Simulation dinyatakan **memadai** (`SIMULATION_PLAN_READY` setelah
DIJALANKAN — status dokumen ini sendiri di §7 hanya menilai kesiapan
RANCANGAN, bukan hasil eksekusi) hanya jika, setelah dijalankan nanti,
seluruh berikut terpenuhi:

1. **Skenario 1** (density-only): tingkat false-positive excitation
   **rendah** (ambang eksak, mis. ≤10%, ditentukan bersama peneliti
   saat implementasi — TIDAK ditetapkan di sini sebagai angka final).
2. **Skenario 2/4** (excitation-only atau density-dominan):
   `theta1` **tidak** menunjukkan bias sistematis besar ke arah menutupi
   `alpha` yang sebenarnya kecil/nol dengan cara yang tak terdeteksi.
3. **Skenario 3/5**: branching ratio (`alpha/beta`) dipulihkan dengan
   bias yang **dapat diterima** relatif terhadap ukuran efek 0.677
   produksi (mis. bias absolut tidak melebihi orde-besaran yang bisa
   mengubah kesimpulan "rezim stabil di bawah 1" menjadi "mendekati
   eksplosif" atau sebaliknya).
4. **Skenario 7**: kesimpulan kualitatif (tanda & signifikansi `theta1`
   dan `alpha`, arah branching ratio) **tidak berubah total** hanya
   karena transformasi densitas berbeda — perbedaan KUANTITATIF boleh
   ada, perbedaan KUALITATIF (mis. signifikan→tidak signifikan) berarti
   gagal kriteria ini.
5. **Seluruh skenario**: tingkat `convergence failure` dilaporkan
   eksplisit per skenario/grid-point — **kegagalan identifikasi HARUS
   dilaporkan, bukan disembunyikan** lewat pemilihan starting-value yang
   menghindari kegagalan atau pelaporan hanya replikasi yang konvergen.

**Jika salah satu dari lima kriteria di atas gagal** setelah simulasi
benar-benar dijalankan (di luar cakupan dokumen ini) → M3B-CD **tidak
boleh** langsung di-fit ke 141 event nyata; diperlukan revisi
spesifikasi (transformasi berbeda, reparameterisasi, atau kernel
alternatif) sebelum tahap fitting nyata dipertimbangkan lagi.

---

## 7. Penggunaan Spec A/B/C (Belum Final)

- **Spec A** (`cd_documents_all_accepted`, 1.003 dokumen/185 tahun) —
  **kandidat utama** untuk realisasi kovariat `x_CD(t)` dalam simulasi
  (§3) — dipilih krn representasi paling lengkap yang tersedia dari
  working density series CD.
- **Spec B** (`cd_documents_excluding_key_review`, 996) — dipakai
  sbg **sensitivity check terpisah**: ulangi simulasi kunci (minimal
  skenario 3, 6, 7) dengan `x_CD(t)` dari Spec B, bandingkan apakah
  kesimpulan recovery berubah material krn selisih 7 record
  review-sensitive (CD2-255/CD2-354/CD6-1152/CD6-1156, dari audit
  sensus sebelumnya).
- **Spec C** (`cd_documents_boundary_verified_only`, lower-bound
  diagnostic, cakupan 5,4% korpus) — **TIDAK** dipakai sbg kovariat
  simulasi utama (terlalu jarang/tidak representatif untuk realisasi
  kovariat tahunan penuh) — hanya disebut sbg referensi diagnostic bila
  hasil Spec A/B mencurigakan pada tahun-tahun tertentu.

**Tidak ada pemilihan Spec final** pada tahap ini — ketiganya tetap
berstatus kandidat sesuai instruksi.

---

## 8. Keputusan yang Masih Diperlukan

1. **Ambang numerik eksak** untuk kriteria gate §6 (mis. berapa persen
   false-positive rate dianggap "rendah") — perlu disepakati peneliti
   sebelum implementasi kode simulasi ditulis.
2. **Jumlah replikasi Monte Carlo** per skenario/grid-point (disarankan
   ≥200 sbg minimum, angka final belum diputuskan).
3. **Metode interval kepercayaan** (profile-likelihood vs bootstrap vs
   asimtotik) untuk metrik "interval coverage" (§4) — `HAWKES_MODEL_AUDIT.md`
   mencatat Model 3 produksi TIDAK melaporkan CI sama sekali, jadi tidak
   ada preseden proyek untuk dipakai langsung.
4. **Resolusi risiko circularity struktural** (§5 poin 3) — provenance
   historis CD↔`linimasa_events.csv` perlu ditelusuri terpisah dari
   simulasi statistik ini; simulasi TIDAK bisa menjawab pertanyaan ini.
5. **Pemilihan transformasi `x_CD(t)` final** (§1.3) — menunggu hasil
   skenario 7 (misspecification test) sebelum diputuskan, bukan
   ditetapkan di awal.
6. **Pemilihan kernel final** (eksponensial vs Gamma) — menunggu hasil
   skenario 8, konsisten dgn evaluasi kernel Gamma yang sudah pernah
   dilakukan terpisah untuk Model 3 murni (`HAWKES_MODEL_AUDIT.md`).
7. **Pemilihan Specification A/B/C final** untuk kovariat CD — menunggu
   hasil sensitivity check §7, bukan diputuskan sekarang.

---

## 9. Pre-Specified Numerical Decision Gates

> **NUMERICAL_GATES_PRE_SPECIFIED**
> **SIMULATION_NOT_YET_RUN**

Ambang berikut dibekukan (pre-registrasi) oleh peneliti SEBELUM simulasi
dijalankan, menggantikan placeholder "ambang eksak ditentukan saat
implementasi" di §6 dan §8 poin 1. Prioritas epistemik eksplisit yang
melandasi seluruh gate di bawah:

```
false-positive excitation  >  parameter recovery  >  model selection
```

Artinya lebih baik M3B-CD gagal mendeteksi self-excitation lemah
daripada mengklaim self-excitation ketika pola sebenarnya hanya
dihasilkan oleh kepadatan dokumentasi (`x_CD(t)`) — konsisten dgn risiko
identifiability §5 poin 1 dan `circularity_risk: possible` §0.

### Desain Replikasi (Frozen)

| Parameter desain | Nilai dibekukan |
|---|---|
| Pilot replicates | 100 per grid-cell (§2 × §3) |
| Final replicates | 1000 per grid-cell (menggantikan "≥200 disarankan" §2 sbg angka final) |

### A. Hard Implementation Gate

Prasyarat teknis murni — dievaluasi SEBELUM metrik recovery apapun
dipercaya, krn fit yang tidak konvergen tidak bermakna dievaluasi lebih
lanjut.

| Metrik | Ambang |
|---|---|
| Convergence rate | PASS ≥ 0.95; FAIL < 0.90; 0.90–0.95 = REVIEW (bukan otomatis lolos/gagal) |
| Invalid estimate rate (bounds-hit, `alpha→0`/`beta→∞` patologis, non-finite) | ≤ 0.05 |

### B. Parameter-Recovery Gate

Berlaku hanya pada grid-cell yang lolos Gate A.

| Metrik | Ambang |
|---|---|
| False-positive excitation (skenario 1) | ≤ 0.05 — ambang paling ketat, sesuai prioritas epistemik di atas |
| Parameter absolute relative bias (`theta1, alpha, beta` individual) | ≤ 0.10 |
| Normalized absolute bias (`theta0`) | ≤ 0.25 |
| Branching-ratio (`alpha/beta`) absolute bias | ≤ 0.05 |
| Branching-ratio (`alpha/beta`) relative bias | ≤ 0.10 (DAN, bukan ATAU, dgn baris di atas) |
| Nominal 95% CI coverage empirik | 0.925 – 0.975 |
| Sign recovery (`alpha`, `theta1`) | ≥ 0.95 |

### C. Identifiability Gate

Menguji risiko §5 poin 1–2 (theta1 menyerap self-excitation, atau
sebaliknya) secara numerik.

| Metrik | Ambang |
|---|---|
| `\|correlation(theta1, alpha)\|` (skenario 3/4/5) | < 0.70 |
| Correct-model-selection rate (M1 vs M2 vs M3B-CD; metode eksak — AIC/BIC/LR-test — ditentukan saat implementasi) | ≥ 0.80 |

Gate ini menguji identifiability **statistik** saja — TIDAK
menyelesaikan risiko circularity struktural (§5 poin 3, §8 poin 4), yang
tetap keputusan terbuka di luar cakupan gate numerik manapun.

### D. Misspecification Stress Gate

Ambang **terpisah** dari Gate B — skenario 7/8 sengaja menguji kondisi
model salah, sehingga membandingkan terhadap ambang B (dikalibrasi utk
model benar) tidak sesuai.

| Skenario | Metrik | Ambang |
|---|---|---|
| 7 (misspecification transformasi densitas) | Normalized RMSE (parameter terpengaruh, terutama `theta1`) | ≤ 0.20 |
| 7 | Transform sensitivity — delta branching ratio (fit `log(1+CD_t)` vs kebenaran-simulasi non-log) | ≤ 0.05 absolut |
| 8 (misspecification kernel Gamma→eksponensial) | Kriteria kualitatif §6 poin 4 (tidak ada flip tanda/signifikansi) DITAMBAH normalized RMSE branching ratio | ≤ 0.20 |

Kegagalan Gate D **tidak otomatis** menggagalkan M3B-CD secara
keseluruhan, tapi WAJIB dilaporkan eksplisit sbg batasan interpretasi
(konsisten §6 poin 5) dan memicu keputusan terbuka §8 poin 5/6.

### E. Global Decision Gate

M3B-CD dinyatakan layak dipertimbangkan untuk fitting 141 event nyata
HANYA jika seluruh berikut terpenuhi:

1. Gate A lolos untuk seluruh grid-point skenario 1–8.
2. Gate B lolos untuk skenario inti recovery 1, 2, 3, 4, 5.
3. Gate C lolos.
4. Gate D dilaporkan lengkap (lolos ATAU gagal-tapi-terdokumentasi) —
   kegagalan D sendiri tidak otomatis REJECT, tapi kegagalan D
   **bersamaan** dgn kegagalan B atau C = REJECT.
5. Production-scenario power ≥ 0.80 — didefinisikan sbg proporsi
   replikasi skenario 3 (density + excitation gabungan, kalibrasi
   paling mendekati realita, §2) di mana `alpha` estimasi terdeteksi
   signifikan berbeda dari 0 pada nilai produksi sebenarnya
   (`alpha=0.4207`).

**Jika salah satu dari kriteria 1, 2, 3, atau 5 gagal → REJECT** —
konsisten dgn penutup §6: diperlukan revisi spesifikasi (transformasi
berbeda, reparameterisasi, atau kernel alternatif) sebelum fitting
nyata dipertimbangkan lagi. Bagian ini **mempertegas** §6 dgn ambang
numerik eksak, bukan menggantikan isinya.

---

## Status

```
NUMERICAL_GATES_PRE_SPECIFIED
SIMULATION_NOT_YET_RUN
```

**Alasan**: rancangan simulasi/recovery (§1–§8, status desain semula
`SIMULATION_PLAN_READY`) kini dilengkapi ambang numerik yang dibekukan
peneliti (§9: hard implementation gate, parameter-recovery gate,
identifiability gate, misspecification stress gate, global decision
gate) — menggantikan seluruh placeholder "ambang ditentukan saat
implementasi" di §6 dan §8 poin 1. Ini **BUKAN** pernyataan bahwa
simulasi sudah dijalankan atau bahwa M3B-CD siap di-fit ke data nyata —
gate hanya bisa dievaluasi SETELAH simulasi benar-benar dijalankan
sesuai desain §1–§3 dan diperiksa terhadap ambang §9.

---

**STOP** — pembekuan ambang numerik decision gate selesai. Tidak ada
simulasi dijalankan, tidak ada fitting data nyata (141 event), Model
3/3B produksi tidak diubah, Graphify tidak dijalankan, Git/deployment
tidak dijalankan.
