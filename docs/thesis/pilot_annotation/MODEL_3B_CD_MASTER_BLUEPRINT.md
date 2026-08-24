# MODEL 3B-CD MASTER BLUEPRINT

> **MASTER RESEARCH AND EXECUTION BLUEPRINT**  
> **SOURCE OF TRUTH FOR CONTINUING WORK**  
> **REAL-DATA FITTING NOT YET AUTHORIZED**  
> **NUMERICAL DECISION GATES PRE-SPECIFIED**  
> **RESEARCHER APPROVAL REQUIRED AT MAJOR GATES**

## 1. Tujuan Utama

Model 3B-CD dikembangkan untuk menjawab pertanyaan:

> Apakah pengelompokan temporal pada 141 peristiwa sejarah tetap terdeteksi setelah perubahan kepadatan dokumentasi *Corpus Diplomaticum* dikontrol?

Model ini tidak dirancang untuk membuktikan:

- resistensi;
- defeksi;
- penyebaran pembangkangan;
- hubungan kausal antarlokasi;
- satu mekanisme historis yang homogen.

Klaim maksimum yang dapat diuji:

> Apakah komponen *self-excitation* dalam proses Hawkes tetap diperlukan setelah baseline intensitas diberi covariate kepadatan dokumentasi CD?

---

## 2. Model 3 yang Telah Di-deploy

Model produksi saat ini adalah *pooled exploratory Hawkes baseline*:

\[
\lambda(t)=\mu+\sum_{t_i<t}\alpha e^{-\beta(t-t_i)}
\]

Parameter produksi:

```text
event count: 141
mu: 0.2573
alpha: 0.4207
beta: 0.6215
branching ratio: alpha / beta approximately 0.6769
kernel: exponential
window: [1600, 1784)
```

Interpretasi publik dibatasi pada:

- *temporal clustering*;
- *self-excitation*;
- perbedaan dari Poisson homogen.

Model 3 bukan bukti satu mekanisme sejarah. Label lama **Kaskade Defeksi** telah dibekukan dan tidak boleh digunakan kembali.

---

## 3. Temuan Process Tracing

```text
Barus:
local contractual breach + internal factional conflict

Indrapura:
VOC nonfulfillment + reciprocal contractual dispute
+ sequential strategic switching

Pariaman:
administrative aggregation remains interpretive
+ actor identity ambiguity

Sillida/Salido:
open conflict + commercial reconciliation
+ resource governance change

Padang:
VOC contractual succession control
+ administrative classification
```

Implikasi:

\[
\text{temporal proximity} \neq \text{same historical mechanism}
\]

---

## 4. Masalah Observation Process

Jumlah peristiwa yang dapat diamati dipengaruhi oleh dokumentasi dan kurasi:

```text
historical process
-> historical events

documentation process
-> surviving and selected records

research curation
-> records entering the event dataset
```

Istilah yang digunakan:

```text
observed archival documentation density
```

Bukan:

```text
true archival density
```

---

## 5. Status Tiga Koleksi

### 5.1 Corpus Diplomaticum

```text
CD_SOURCE_NUMBERING: PARTIALLY_READY
CD_ANALYTICAL_NUMBERING: PARTIALLY_READY
CD_WORKING_RECORD_ID: READY
CD_DATE: READY
CD_ANNUAL_DENSITY_WORKING: READY
```

Hasil utama:

```text
raw heading candidates: 1,152
recovered false negative: 1
accepted documents: 1,045
rejected candidates: 108
unresolved candidates: 0
```

Working record ID:

```text
volume + document_number_as_printed + pdf_page_start
```

Peran:

```text
primary_exposure_candidate
```

Risiko utama: CD bukan exposure eksogen sempurna karena sebagian event Model 3 juga bersumber dari CD.

### 5.2 Generale Missiven

```text
GM_DOCUMENT_KEY: READY
GM_DATE: READY
GM_ANNUAL_DENSITY_WORKING: PARTIALLY_READY
GM_SELECTION_RISK: HIGH
GM_DENSITY_FOR_MODEL_FITTING: NOT_AUTHORIZED
```

Peran:

```text
requires_selection_provenance
```

Korpus GM adalah seleksi tematik. Mekanisme pengurangan kandidat menjadi 100 dokumen belum terdokumentasi penuh.

### 5.3 Daghregister

```text
DAGH_DOCUMENT_UNIT: PARTIALLY_READY
DAGH_DATE: PARTIALLY_READY
DAGH_ANNUAL_DENSITY_WORKING: PARTIALLY_READY
DAGH_SELECTION_RISK: HIGH
DAGH_DENSITY_FOR_MODEL_FITTING: NOT_AUTHORIZED
```

Unitnya campuran:

- *daily entry*;
- *thematic extract*;
- *continuation*;
- *multi-event passage*;
- unit ambigu.

Peran:

```text
diagnostic_series_only
```

### 5.4 Keputusan lintas-koleksi

```text
CD: primary exposure candidate
GM: sensitivity term not ready
Daghregister: diagnostic only
combined density: not ready
```

Annual counts ketiga koleksi dilarang dijumlahkan secara mentah karena unitnya tidak sebanding.

---

## 6. Model Kandidat

### M1: Pooled Hawkes baseline

\[
\lambda(t)=\mu+\sum_{t_i<t}\alpha e^{-\beta(t-t_i)}
\]

### M2: CD-density-only inhomogeneous Poisson

\[
\lambda(t)=\exp\left(\theta_0+\theta_1x_{CD}(t)\right)
\]

### M3B-CD: CD-density-controlled Hawkes

\[
\lambda(t)=\exp\left(\theta_0+\theta_1x_{CD}(t)\right)+\sum_{t_i<t}\alpha e^{-\beta(t-t_i)}
\]

Transformasi kandidat utama:

\[
x_{CD}(t)=\log(1+CD_t)
\]

Transformasi ini belum boleh dianggap final sebelum sensitivity analysis selesai.

---

## 7. Pertanyaan Statistik Utama

Simulation-recovery study harus menjawab:

1. Apakah model menemukan excitation palsu ketika data hanya digerakkan density?
2. Apakah density effect dan self-excitation dapat dipisahkan?
3. Apakah theta0, theta1, alpha, beta, dan branching ratio dapat dipulihkan?
4. Apakah interval kepercayaan mempunyai coverage yang benar?
5. Apakah M1, M2, dan M3B-CD dapat dipilih dengan benar melalui AIC/BIC?
6. Apakah hasil sensitif terhadap transformasi density, excitation lemah, dan kernel?

---

## 8. Sepuluh Frozen Simulation Cells

```text
S1-G1
S1-G2
S1-G3
S2-G1
S3-G1
S4-G1
S5-G1
S6-G1
S7-G1
S8-G1
```

Fungsi skenario:

```text
S1: density-only, alpha_true = 0
S2: excitation-only
S3: density + excitation, production-calibrated
S4: strong density + weak excitation
S5: weak density + strong excitation
S6: event count and window calibrated near Model 3
S7: density-transform misspecification
S8: Gamma-kernel simulation fitted by exponential kernel
```

Dilarang menambah cell, grid point, atau skenario sebelum evaluasi final selesai.

---

## 9. Numerical Decision Gates

Hard gates utama:

```text
convergence rate >= 0.95
invalid-estimate rate <= 0.05
false-positive excitation <= 0.05
production-scenario power >= 0.80
absolute relative bias theta1/alpha/beta <= 0.10
normalized absolute bias theta0 <= 0.25
branching-ratio absolute bias <= 0.05
branching-ratio relative bias <= 0.10
95% CI coverage between 0.925 and 0.975
sign recovery >= 0.95
abs correlation theta1_hat and alpha_hat < 0.70
correct-model-selection rate >= 0.80
normalized RMSE <= 0.20
```

Ambang tidak boleh diubah berdasarkan hasil pilot atau final simulation.

Untuk `alpha_true = 0`:

- relative bias alpha tidak digunakan;
- boundary pile-up hanya diagnostic;
- false-positive formal memakai boundary-aware LR test.

Boundary-aware test:

```text
restricted model: M2
unrestricted model: M3B-CD
null hypothesis: alpha = 0
LR = 2 * (logLik_M3B-CD - logLik_M2)
reference distribution: 0.5 chi-square_0 + 0.5 chi-square_1
```

---

## 10. Infrastruktur yang Telah Selesai

### Simulator

```text
IMPLEMENTED
MATHEMATICALLY_AUDITED
COMMITTED_AND_PUSHED
```

### Gamma simulator

```text
IMPLEMENTED
TESTED
COMMITTED_AND_PUSHED
```

Menggunakan exact cluster representation:

```text
offspring count ~ Poisson(branching ratio)
offspring lag ~ Gamma(shape=2, rate=2.38095)
```

Global Ogata bound lama tidak boleh digunakan kembali.

### Statistical instrumentation

```text
IMPLEMENTED
TESTED
COMMITTED_AND_PUSHED
```

Mencakup:

- Hessian;
- covariance;
- standard error;
- Wald CI;
- boundary-aware alpha test;
- log-likelihood M1/M2/M3B-CD;
- AIC;
- BIC;
- branching-ratio delta method;
- model-selection output.

### Event-sequence persistence

```text
IMPLEMENTED
TESTED
COMMITTED_AND_PUSHED
```

Setiap replikasi baru menyimpan:

```text
event_times
event_times_sha256
truth_parameters
fit_parameters
seed
simulator_commit
instrumentation_commit
density_checksum
```

Pilot 100 lama tidak menyimpan event times dan tidak boleh direkonstruksi diam-diam.

---

## 11. Hasil Pilot yang Telah Selesai

### Pilot teknis 100 replikasi per cell

```text
10/10 cells technically ready
1,000/1,000 replicates completed
optimizer failures: 0
nonfinite results: 0
reproducibility: passed
```

### Temuan preliminary

- branching ratio under-recovery sekitar 13-20% pada beberapa core scenarios;
- S4 memperlihatkan ketidakstabilan ketika beta menyentuh batas bawah;
- S7 memperlihatkan transform misspecification bekerja sebagai stress test;
- S8 Gamma misspecification memperlihatkan branching-ratio recovery yang baik;
- korelasi theta1_hat dan alpha_hat belum menunjukkan krisis identifikasi.

Temuan ini belum menjadi keputusan final.

---

## 12. Immediate Next Action

Langkah operasional berikutnya:

```text
PILOT INSTRUMENTASI 10 CELL x 10 REPLIKASI
```

Tujuan:

- menghasilkan 100 synthetic sequences baru;
- menyimpan event times sejak awal;
- fit M1, M2, dan M3B-CD pada setiap sequence;
- menguji kestabilan Hessian, covariance, SE, CI, LR, AIC, dan BIC;
- berhenti sebelum final 1.000 replikasi.

Pilot 10x10 bukan recovery assessment final.

Output status yang diperbolehkan:

```text
INSTRUMENTATION_PILOT_TECHNICALLY_READY
INSTRUMENTATION_PILOT_REQUIRES_REVISION
```

---

## 13. Final Simulation Design

Jika pilot instrumentasi 10x10 lulus:

```text
10 frozen cells
x 1,000 replicates per cell
= 10,000 synthetic sequences
```

Setiap sequence di-fit dengan:

```text
M1
M2
M3B-CD
```

Total estimasi:

```text
30,000 model fits
```

Final run hanya boleh dimulai setelah researcher authorization.

---

## 14. Global Recovery Decision

### SIMULATION_RECOVERY_PASSED

Semua hard gate utama lulus.

### SIMULATION_RECOVERY_CONDITIONAL

Tidak ada false-positive failure, tetapi terdapat warning pada weak-effect atau stress scenarios.

### SIMULATION_RECOVERY_FAILED

Salah satu kegagalan kritis terjadi, misalnya:

```text
false-positive excitation > 0.075
convergence < 0.90
invalid estimate rate > 0.05
production-scenario power < 0.70
branching-ratio relative bias > 0.20
coverage < 0.90
parameter correlation >= 0.85
```

Keputusan final wajib dilaporkan tanpa mengubah ambang setelah hasil tersedia.

---

## 15. Real-Data Fitting Authorization Gate

Simulation recovery tidak otomatis mengizinkan fitting.

Status maksimal setelah final simulation:

```text
SIMULATION_RECOVERY_PASSED
REAL_DATA_FITTING_REQUIRES_RESEARCHER_AUTHORIZATION
```

Jika diizinkan, real-data stage meliputi:

1. fit M1;
2. fit M2;
3. fit M3B-CD;
4. AIC/BIC comparison;
5. boundary-aware alpha test;
6. time-rescaling residuals;
7. parameter uncertainty;
8. branching-ratio comparison;
9. sensitivity Spec A/B/C;
10. sensitivity density transform;
11. kernel sensitivity.

---

## 16. Goal Ilmiah Akhir

Goal bukan membuktikan kaskade defeksi.

Goal akhir:

> Apakah pengelompokan temporal pada 141 event tetap memerlukan komponen self-excitation setelah perubahan kepadatan dokumentasi Corpus Diplomaticum diperhitungkan?

Kemungkinan hasil:

### Excitation bertahan

> Dokumentasi CD tidak sepenuhnya menjelaskan pengelompokan temporal.

### Excitation bertahan secara bersyarat

> Self-excitation terdeteksi, tetapi hasil sensitif terhadap effect size, transformasi density, atau kernel.

### Density dan excitation tidak dapat dipisahkan

> Observation process dan dinamika temporal tidak dapat dipisahkan secara andal dengan data dan model saat ini.

Ketiganya merupakan hasil ilmiah yang sah.

---

## 17. Gap yang Masih Terbuka

### Gap operasional

1. Pilot instrumentasi 10x10 belum dijalankan.
2. Final 1.000 replikasi per cell belum dijalankan.
3. Recovery gates belum dievaluasi secara final.
4. Fitting 141 event belum diizinkan.
5. Sensitivity analysis belum dijalankan.
6. Model 3 dan Model 3B belum dibandingkan pada data nyata.
7. Model 3B belum siap untuk publik.

### Gap struktural

1. Circularity CD dengan event dataset.
2. CD bukan exposure eksogen murni.
3. Event coding bergantung pada surviving records.
4. Mechanism-coded layer belum cukup untuk marked Hawkes.
5. GM dan Daghregister belum siap menjadi covariate utama.
6. Statistical clustering tidak mengidentifikasi mekanisme historis.

---

## 18. Komponen yang Dilarang Diulang

Jangan ulang:

- sensus CD1-CD6;
- remediasi document keys;
- annual density CD;
- audit GM;
- audit Daghregister;
- comparison matrix;
- mathematical audit simulator;
- Gamma generator audit;
- numerical gate selection;
- Pilot 100 lama;
- statistical instrumentation implementation;
- event-sequence persistence implementation.

Jangan menambah test baru kecuali ada defect konkret.

---

## 19. Kebijakan Commit dan Push

Commit hanya pada milestone:

1. setelah audit pilot instrumentasi 10x10;
2. setelah final 1.000-replicate recovery report;
3. setelah real-data fitting, jika diizinkan;
4. setelah visualisasi dan narasi publik final.

Jangan commit:

- setiap run kecil;
- setiap metrik;
- output scratch;
- JSONL replikasi;
- working data;
- temporary logs.

Working outputs harus tetap ignored.

---

## 20. Anti-Loop Rules

Claude Code wajib:

1. membaca blueprint sebelum memulai task Model 3B;
2. tidak mengulang fase berstatus complete;
3. tidak menambah skenario tanpa izin;
4. tidak mengubah decision gates;
5. tidak recalibrate parameter menggunakan hasil pilot;
6. tidak menjalankan real-data fitting tanpa izin eksplisit;
7. tidak menjalankan dua fase dalam satu turn;
8. berhenti pada stop condition;
9. melaporkan blocker, bukan memperbaiki otomatis;
10. membedakan bug implementasi dari kegagalan identifikasi statistik.

---

## 21. Progress Snapshot

Persentase ini merupakan estimasi manajemen proyek, bukan hasil statistik.

```text
Model 3B infrastructure: 95%
Simulation-recovery study: 65%
Readiness for real-data fitting decision: 55%
Public Model 3B: 40%
```

---

## 22. Current Status

```text
OBSERVATION_PROCESS_CD: COMPLETE
SIMULATOR: COMPLETE
MATHEMATICAL_AUDIT: PASSED
GAMMA_GENERATOR: COMPLETE
NUMERICAL_GATES: FROZEN
STATISTICAL_INSTRUMENTATION: COMPLETE
EVENT_SEQUENCE_PERSISTENCE: COMPLETE
PILOT_INSTRUMENTATION_10x10: NEXT
FINAL_1000: NOT RUN
SIMULATION_RECOVERY: NOT YET ASSESSED
REAL_DATA_FITTING: NOT AUTHORIZED
PUBLIC_MODEL_3B: NOT READY
```

---

## 23. Immediate Stop Condition

Setelah blueprint tersimpan:

- jangan menjalankan pilot 10x10;
- jangan menjalankan simulasi;
- jangan mengubah source;
- jangan commit;
- jangan push;
- jangan Graphify;
- jangan deploy.

Tunggu instruksi peneliti:

> Jalankan Pilot Instrumentasi 10x10 sesuai MODEL 3B-CD MASTER BLUEPRINT.
