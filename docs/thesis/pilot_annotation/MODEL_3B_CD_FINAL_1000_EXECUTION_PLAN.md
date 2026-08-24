# MODEL 3B-CD: FINAL 1,000-REPLICATE EXECUTION PLAN

> **FINAL SIMULATION-RECOVERY EXECUTION PLAN**  
> **DEPENDENCY: MODEL_3B_CD_MASTER_BLUEPRINT.md**  
> **DEPENDENCY: MODEL_3B_CD_PILOT_INSTRUMENTATION_10x10_PLAN.md**  
> **GRAPH CONTEXT: GRAPH_OUTPUT_CURRENT**  
> **REAL-DATA FITTING NOT AUTHORIZED**  
> **RESEARCHER AUTHORIZATION REQUIRED BEFORE EXECUTION**

## 1. Tujuan

Menjalankan studi simulation-recovery final untuk Model 3B-CD:

```text
10 frozen cells x 1,000 replicates = 10,000 synthetic event sequences
```

Setiap sequence di-fit dengan:

```text
M1
M2
M3B-CD
```

Total estimasi yang direncanakan:

```text
30,000 model fits
```

Tujuan final run adalah mengevaluasi seluruh numerical decision gates yang telah dipraspesifikasikan sebelum simulasi final.

Final run tidak mengotorisasi fitting 141 event nyata secara otomatis.

---

## 2. Sumber Kebenaran

Claude Code wajib membaca sebelum melakukan pekerjaan apa pun:

```text
MODEL_3B_CD_MASTER_BLUEPRINT.md
MODEL_3B_CD_PILOT_INSTRUMENTATION_10x10_PLAN.md
MODEL_3B_CD_SIMULATION_RECOVERY_PLAN.md
MODEL_3B_CD_SIMULATION_CELL_MANIFEST.md
MODEL_3B_CD_PILOT_100_AUDIT.md
MODEL_3B_CD_INSTRUMENTATION_PILOT_10x10_AUDIT.md
```

Jika nama blueprint lokal memiliki awalan `Unduh `, gunakan file tersebut selama checksum dan isi cocok.

Graphify berstatus:

```text
GRAPH_OUTPUT_CURRENT
```

Graph hanya konteks. Graph bukan sumber parameter simulasi dan tidak boleh mengubah manifest atau numerical gates.

---

## 3. Status Prasyarat

Prasyarat yang telah selesai:

```text
OBSERVATION_PROCESS_CD: COMPLETE
SIMULATOR: COMPLETE
MATHEMATICAL_AUDIT: PASSED
GAMMA_GENERATOR: COMPLETE
NUMERICAL_GATES: FROZEN
STATISTICAL_INSTRUMENTATION: COMPLETE
EVENT_SEQUENCE_PERSISTENCE: COMPLETE
PILOT_INSTRUMENTATION_10x10: TECHNICALLY_READY
GRAPH_OUTPUT: CURRENT
```

Final run hanya boleh dimulai jika seluruh status di atas tetap berlaku.

---

## 4. Komponen yang Dilarang Diulang

Jangan ulang:

- sensus CD1-CD6;
- remediasi document key;
- annual density CD;
- audit GM;
- audit Daghregister;
- comparison matrix;
- mathematical audit simulator;
- Gamma generator audit;
- pemilihan numerical gates;
- Pilot 100 lama;
- Pilot Instrumentasi 10x10;
- implementasi instrumentasi statistik;
- implementasi persistence event sequence;
- ekstraksi Graphify yang sudah berstatus current.

Jangan tambah test baru kecuali defect konkret ditemukan sebelum run.

---

## 5. Sepuluh Frozen Cells

Gunakan tepat:

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

Dilarang:

- menambah cell;
- menghapus cell;
- mengubah parameter truth;
- mengubah transformasi density;
- mengubah simulation kernel;
- mengubah fitted kernel;
- menambah grid point;
- melakukan recalibration dari hasil pilot.

---

## 6. Replikasi dan Seed

Gunakan tepat:

```text
1,000 replicates per cell
10,000 replicates total
```

Seed harus:

- deterministik;
- unik untuk seluruh 10.000 replikasi;
- tidak bertabrakan dengan Pilot 100 lama;
- tidak bertabrakan dengan Pilot Instrumentasi 10x10;
- dapat direkonstruksi dari `cell_id` dan `replicate_id`;
- disimpan dalam setiap hasil replikasi.

Buat seed ledger sebelum run.

Validasi:

```text
unique_seed_count = 10,000
missing_seed_count = 0
duplicate_seed_count = 0
```

---

## 7. Provenance per Replikasi

Setiap hasil wajib menyimpan:

```text
result_kind
cell_id
replicate_id
base_seed
replicate_seed
simulator_commit
instrumentation_commit
persistence_commit
manifest_checksum
numerical_gate_checksum
density_checksum
simulation_kernel
fitted_kernel
truth_parameters
event_times
event_times_sha256
n_events
fit_M1
fit_M2
fit_M3B_CD
boundary_alpha_test
model_selection
runtime_seconds
result_status
failure_status
```

`result_kind` wajib:

```text
new_result_with_event_times
```

Output legacy tidak boleh digunakan sebagai pengganti final run.

---

## 8. Event Sequence Integrity

`event_times` wajib:

- berupa array float64;
- finite;
- terurut menaik;
- berada dalam `[1600, 1784)`;
- panjangnya sama dengan `n_events`;
- diserialisasi tanpa pembulatan destruktif;
- memiliki checksum SHA-256 dari representasi little-endian `<f8`;
- lolos validasi setelah round-trip load.

Jika checksum event sequence gagal, replikasi dinyatakan invalid dan stop policy diterapkan.

Jangan merekonstruksi event times setelah run dari seed, event count, atau fitted parameters.

---

## 9. Model Fits

Setiap event sequence di-fit dengan:

### M1

Pooled Hawkes baseline.

### M2

CD-density-only inhomogeneous Poisson.

### M3B-CD

CD-density-controlled Hawkes.

Untuk setiap model simpan:

```text
parameter_estimates
log_likelihood
number_of_parameters
convergence_status
optimizer_status
optimizer_message
boundary_flags
Hessian_status
covariance_status
minimum_eigenvalue
condition_number
standard_errors
Wald_CI_95
AIC
BIC
runtime_seconds
failure_status
```

Dilarang menyembunyikan fit gagal, covariance singular, atau hasil nonfinite.

---

## 10. Covariance dan Confidence Intervals

Covariance dianggap valid hanya jika:

- Hessian finite;
- symmetry dalam toleransi;
- positive definite;
- minimum eigenvalue valid;
- condition number dilaporkan;
- inverse tersedia;
- tidak ada standard error nonfinite.

Status yang diperbolehkan:

```text
valid
regularized
singular
non_positive_definite
unavailable
```

`regularized` tidak boleh digabungkan dengan `valid`.

CI Wald 95% hanya digunakan untuk parameter interior dan diagnostic yang sesuai.

---

## 11. Boundary-Aware Alpha Test

Untuk M3B-CD gunakan tepat:

```text
restricted model: M2
unrestricted model: M3B-CD
H0: alpha = 0
LR = 2 x (logLik_M3B-CD - logLik_M2)
reference = 0.5 chi-square_0 + 0.5 chi-square_1
```

Simpan:

```text
restricted_model
unrestricted_model
loglik_restricted
loglik_unrestricted
LR
p_value
reject_at_0_05
alpha_at_boundary
```

Wald CI alpha tidak boleh menggantikan boundary-aware test untuk false-positive formal pada `alpha_true = 0`.

---

## 12. Branching-Ratio Uncertainty

Untuk M1 dan M3B-CD:

```text
branching_ratio = alpha / beta
```

Simpan:

```text
branching_ratio
branching_ratio_standard_error
branching_ratio_CI_95
delta_method_status
```

Delta method hanya tersedia jika covariance alpha-beta valid.

Jika covariance tidak valid:

```text
delta_method_status = unavailable
```

---

## 13. AIC, BIC, dan Model Selection

Simpan per sequence:

```text
AIC_M1
AIC_M2
AIC_M3B_CD
BIC_M1
BIC_M2
BIC_M3B_CD
best_model_by_AIC
best_model_by_BIC
delta_AIC
delta_BIC
```

Definisi BIC:

```text
n_BIC = number of events in the fitted sequence
```

Gunakan `n_BIC` identik untuk ketiga model pada sequence yang sama.

---

## 14. Numerical Decision Gates

Gunakan numerical gates yang telah dibekukan.

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

Ambang tidak boleh diubah setelah hasil final tersedia.

Untuk `alpha_true = 0`:

- relative bias alpha tidak dihitung;
- boundary pile-up hanya diagnostic;
- gunakan false-positive formal dari boundary-aware LR test;
- gunakan RMSE absolut alpha.

---

## 15. Core dan Stress Scenarios

Bedakan:

```text
core scenarios
stress scenarios
```

Core scenarios menilai recovery pada spesifikasi yang benar.

Stress scenarios menilai robustness terhadap:

- transformasi density yang salah;
- kernel Gamma yang di-fit dengan eksponensial;
- excitation lemah;
- density effect yang dominan.

Kegagalan stress scenario tidak otomatis sama dengan kegagalan core model, tetapi wajib membatasi interpretasi.

---

## 16. Output Directory

Gunakan direktori ignored:

```text
data/model3b_working/final_1000/
```

Struktur:

```text
final_1000/
  manifests/
  S1-G1/
  S1-G2/
  S1-G3/
  S2-G1/
  S3-G1/
  S4-G1/
  S5-G1/
  S6-G1/
  S7-G1/
  S8-G1/
  aggregate/
  checkpoints/
  logs/
```

Output per cell:

```text
replicate_results_part_*.jsonl
failure_log.jsonl
cell_metadata.json
cell_progress.json
cell_summary.json
seed_ledger.json
checksum_report.json
runtime_summary.json
```

Output agregat:

```text
FINAL_1000_AGGREGATE_SUMMARY.json
FINAL_1000_GATE_EVALUATION.json
FINAL_1000_FAILURE_LEDGER.json
FINAL_1000_CHECKSUM_REPORT.json
FINAL_1000_RUNTIME_REPORT.json
```

Jangan menimpa Pilot 100 atau Pilot Instrumentasi 10x10.

---

## 17. Chunking dan Checkpoint Strategy

Jalankan setiap cell dalam chunk:

```text
100 replicates per chunk
10 chunks per cell
```

Total:

```text
100 chunks
```

Setelah setiap chunk:

1. flush output;
2. validasi jumlah record;
3. validasi replicate IDs;
4. validasi seeds;
5. validasi event-time checksums;
6. tulis progress checkpoint;
7. hitung checksum file chunk;
8. simpan runtime;
9. evaluasi stop conditions teknis;
10. lanjut hanya jika checkpoint valid.

Jangan menunggu 1.000 replikasi selesai untuk menulis output.

---

## 18. Resume Policy

Final run harus restart-safe.

Saat resume:

- baca progress checkpoint;
- validasi checksum chunk yang sudah selesai;
- verifikasi replicate IDs yang sudah ada;
- verifikasi seed ledger;
- jangan mengulang replikasi selesai;
- jangan membuat duplicate replicate ID;
- jangan mengganti seed;
- jangan menimpa chunk valid;
- lanjut dari replicate ID berikutnya.

Jika checkpoint korup atau checksum gagal:

- jangan melanjutkan cell;
- laporkan blocker;
- jangan memperbaiki otomatis.

---

## 19. Runtime Budget

Gunakan hasil pilot sebagai dasar estimasi, tetapi jangan menganggap runtime seragam antarskenario.

Plan harus menghitung sebelum run:

```text
estimated runtime per cell
estimated runtime per chunk
estimated total serial runtime
estimated output size per cell
estimated total output size
free disk space
memory budget
```

S7 dan cell dengan event count tinggi harus mendapat estimasi runtime khusus.

Jangan menjalankan run jika ruang disk bebas tidak mencukupi untuk:

```text
estimated output x 2
```

Faktor dua diperlukan untuk output, checkpoint, dan margin aman.

---

## 20. Parallelization Policy

Default:

```text
serial by cell
```

Parallelization hanya boleh digunakan jika:

- seed independence terjamin;
- output directory terpisah;
- tidak ada shared mutable state;
- density source read-only;
- determinism teruji;
- researcher menyetujui jumlah worker.

Jangan mengubah jumlah worker otomatis saat run berlangsung.

Jika paralel digunakan, simpan:

```text
worker_id
process_id
chunk_id
start_time
end_time
```

---

## 21. Preflight Guards

Sebelum final run, seluruh guard wajib lulus:

1. HEAD sinkron dengan `origin/main`.
2. Blueprint tersedia dan checksum dicatat.
3. Cell manifest tersedia dan checksum dicatat.
4. Numerical-gate plan tersedia dan checksum dicatat.
5. Simulator commit cocok.
6. Instrumentation commit cocok.
7. Persistence commit cocok.
8. Pilot 10x10 audit berstatus technically ready.
9. Seluruh unit test lulus.
10. Density checksum cocok.
11. Final output directory baru atau resume-valid.
12. Tidak ada proses final lain aktif.
13. Source code bersih dari perubahan lokal terkait.
14. Working directory tetap ignored Git.
15. Seed ledger memiliki 10.000 seed unik.
16. Manifest parameters cocok dengan frozen cells.
17. Ruang disk memenuhi minimum aman.
18. Runtime dan storage budget disetujui peneliti.
19. Graph berstatus current atau perbedaan konteks dijelaskan.
20. Otorisasi eksplisit peneliti untuk final run tersedia.

Jika satu guard gagal, jangan menjalankan final run.

---

## 22. Stop Conditions Teknis

Hentikan cell dan laporkan jika:

- event-time checksum gagal;
- density checksum berubah;
- duplicate seed ditemukan;
- duplicate replicate ID ditemukan;
- event nonfinite;
- event di luar window;
- output chunk korup;
- LR tidak cocok dengan perhitungan manual;
- boundary-test label salah;
- source code berubah selama run;
- manifest berubah;
- gates berubah;
- disk free space turun di bawah margin aman;
- proses tidak menunjukkan progres dalam batas waktu;
- failure rate teknis melebihi ambang hard gate;
- output lama tertimpa;
- resume checkpoint tidak konsisten.

Jangan memperbaiki otomatis dalam final run.

---

## 23. Stop Conditions Statistik

Final run tidak boleh dihentikan hanya karena hasil recovery tampak buruk, kecuali ada bukti bug implementasi.

Kegagalan statistik harus diselesaikan sebagai hasil ilmiah, bukan diperbaiki dengan:

- recalibration;
- perubahan gate;
- penghapusan cell;
- penghapusan outlier tanpa rule;
- penambahan parameter;
- penggantian transformasi setelah melihat hasil.

Jika core scenario gagal gate, tetap selesaikan laporan dan klasifikasikan hasil secara jujur.

---

## 24. Gate Evaluation per Cell

Hitung per cell:

```text
attempted
completed
convergence rate
invalid-estimate rate
boundary-pileup rate
false-positive excitation
power
parameter bias
parameter relative bias
normalized bias theta0
RMSE
normalized RMSE
CI coverage
sign recovery
branching-ratio bias
branching-ratio CI coverage
theta1-alpha correlation
correct-model-selection rate AIC
correct-model-selection rate BIC
covariance-valid rate
SE availability
CI availability
boundary-test availability
AIC/BIC availability
runtime distribution
```

Sertakan Monte Carlo uncertainty untuk metrik proporsi.

---

## 25. Global Recovery Decision

Gunakan tepat satu:

### SIMULATION_RECOVERY_PASSED

Semua hard gates core scenarios lulus.

### SIMULATION_RECOVERY_CONDITIONAL

Tidak ada kegagalan false-positive kritis, tetapi terdapat warning pada weak-effect atau stress scenarios.

### SIMULATION_RECOVERY_FAILED

Salah satu kegagalan kritis berlaku sesuai preregistered gates.

Jangan membuat kategori keempat setelah melihat hasil.

---

## 26. Researcher Authorization Gate

Setelah global recovery decision, status maksimum:

```text
REAL_DATA_FITTING_REQUIRES_RESEARCHER_AUTHORIZATION
```

Dilarang otomatis menjalankan fitting 141 event nyata.

Peneliti harus memberikan izin eksplisit pada turn terpisah.

---

## 27. Laporan Final Simulation

Buat:

```text
docs/thesis/pilot_annotation/MODEL_3B_CD_FINAL_1000_RECOVERY_AUDIT.md
```

Status kepala:

> **FINAL SIMULATION-RECOVERY AUDIT**  
> **10 CELLS x 1,000 REPLICATES**  
> **NUMERICAL GATES PRE-SPECIFIED**  
> **REAL-DATA FITTING NOT AUTOMATICALLY AUTHORIZED**  
> **RESEARCHER DECISION REQUIRED**

Struktur minimum:

1. Scope
2. Blueprint Compliance
3. Preflight
4. Runtime and Storage Budget
5. Seed Ledger
6. Checkpoint and Resume Integrity
7. Event-Sequence Integrity
8. Cell-by-Cell Technical Results
9. M1 Recovery
10. M2 Recovery
11. M3B-CD Recovery
12. Covariance and CI Results
13. Boundary-Aware Alpha Test
14. False-Positive Excitation
15. Power
16. Parameter Bias and RMSE
17. Branching-Ratio Recovery
18. Model Selection
19. Identifiability Diagnostics
20. Stress Tests
21. Core Scenario Gate Evaluation
22. Global Recovery Decision
23. Remaining Structural Gaps
24. Real-Data Authorization Gate
25. Reproducibility and Provenance
26. Conclusions

---

## 28. Graphify Policy

Jangan menjalankan Graphify selama final simulation berlangsung.

Setelah laporan final selesai dan direview, Graphify dapat diperbarui dengan:

- global recovery decision;
- gate results;
- remaining gaps;
- authorization status.

Jangan mengekstrak:

- individual replicates;
- event_times;
- JSONL working output;
- failure logs per replikasi.

---

## 29. Git Policy

Jangan commit selama final run.

Commit milestone hanya setelah:

- final report selesai;
- gate evaluation lengkap;
- researcher review dilakukan.

Commit tidak boleh memuat:

- replicate JSONL;
- event_times;
- working output;
- checkpoint files;
- runtime logs;
- failure logs.

Working data tetap ignored.

---

## 30. Batas Keras

Selama final run:

- jangan fit 141 event nyata;
- jangan mengubah numerical gates;
- jangan mengubah manifest;
- jangan mengubah density source;
- jangan menggunakan GM/Daghregister sebagai co-primary;
- jangan menambah cell;
- jangan menghapus cell;
- jangan recalibrate;
- jangan deploy;
- jangan Graphify;
- jangan commit output working;
- jangan push output working;
- jangan otomatis masuk real-data fitting.

---

## 31. Output Terminal Akhir

Tampilkan:

1. preflight result;
2. cells completed;
3. replicates attempted/completed;
4. model fits attempted/completed;
5. checksum-valid rate;
6. convergence rate per model;
7. covariance-valid rate per model;
8. SE/CI availability;
9. boundary-test availability;
10. AIC/BIC availability;
11. technical failures;
12. runtime total;
13. output size;
14. checkpoint/resume status;
15. per-cell gate summary;
16. core-scenario gate summary;
17. stress-test summary;
18. global recovery decision;
19. remaining structural gaps;
20. real-data authorization status;
21. output directory;
22. audit-report path;
23. confirmation that real data was not fit.

---

## 32. Immediate Stop Condition

Setelah plan ini dibuat:

- jangan menjalankan final simulation;
- jangan mengubah source;
- jangan commit;
- jangan push;
- jangan Graphify;
- jangan deploy.

Tunggu instruksi peneliti:

> Jalankan preflight Final 1,000-Replicate Run sesuai MODEL 3B-CD MASTER BLUEPRINT dan MODEL 3B-CD FINAL 1,000-REPLICATE EXECUTION PLAN. Jangan mulai simulasi sebelum saya menyetujui runtime dan storage budget.
