# PRD: Dashboard Konsolidasi Pemodelan Kekuasaan (Model 2-3-5-6)

**Status:** Draft breakdown tim — hasil diskusi lintas-peran (Frontend Design, DevSecOps, MLOps, DBA), 2026-07-21.
**Konteks:** Model 2 (Markov), Model 3 (Hawkes), Model 5 (System Dynamics), Model 6 (Game Theory) dari
`docs/prd/prd-pemodelan-kekuasaan-dagang.md` dan `docs/prd/prd-pemodelan-system-dynamics-game-theory.md`
SEMUA sudah dieksekusi. Tiga artifact HTML sudah dipublish terpisah (Markov/Hawkes+stratifikasi, CLD,
System Dynamics). Model 6 belum punya visual — hasilnya (payoff matrix, H1/H2) masih di terminal +
`data/export/game_theory_payoff_matrix.csv`.

---

## 1. Masalah (Frontend Design)

Empat model, dieksekusi terpisah sepanjang sesi, masing-masing menghasilkan bukti yang **secara
independen menunjuk kesimpulan yang sama**: klaster Siklus (Barus+Pariaman) adalah rezim kausal yang
berbeda struktural dari Stabil dan Sisa.

| # | Metode | Bukti Siklus berbeda | Artifact |
|---|---|---|---|
| 1 | Markov (Model 2) | E[dwell] `aceh_dominion` lebih pendek di Siklus (P(self)=0.5 vs pooled 0.2) | `pemodelan_kekuasaan.html` |
| 2 | Hawkes (Model 3) | ~~SATU-SATUNYA klaster signifikan~~ **KOREKSI 2026-08-01**: direproduksi ulang thd korpus n=141 saat ini (`model3_hawkes_stratified.py`, skrip lama tak pernah ter-checked-in) -- Siklus TETAP terkuat (branching=0.759, p<0.0001) tapi Stabil KINI JUGA signifikan (branching=0.368, p=0.0031); cuma Sisa yg tetap tidak (p=0.58). Klaim "eksklusif Siklus" tidak lagi berdiri. **KOREKSI LANJUTAN 2026-08-01 sore**: `model3_cluster_distinctness_test.py` (permutation test 2000x) -- selisih branching Siklus-Stabil TIDAK signifikan beda dari pembelahan acak (p=0.0995). Baris ini TAK BISA lagi dikutip sbg "Siklus berbeda dari Stabil", hanya "Siklus branching TERKUAT scr deskriptif". **NAMUN**: branching ratio POOLED (0.677, dasar klaim "kaskade nyata & stabil") tervalidasi silang independen via MBPP penuh (`model3_mbpp_full.py`, selisih <0.1% dari metode conditional-MLE) -- klaim inti Model 3 MALAH lebih kuat, cuma klaim STRATIFIKASI-nya yg melemah. Lihat `data/export/model3_cluster_distinctness_output.json` + `model3_mbpp_full_output.json` | `pemodelan_kekuasaan.html` (section `#stratified`, ANGKA DI ARTIFACT INI STALE) |
| 3 | CLD (kausalitas) | Loop "merunduk bukan tunduk" berulang 3× Barus, 3× Pariaman | `causal_loop_diagram.html` |
| 4 | System Dynamics (Model 5) | β khusus-klaster memperbaiki fit Barus/Pariaman, tak berlaku sama di Stabil | `model5_system_dynamics.html` |
| 5 | Game Theory (Model 6) | Rate re-afirmasi kesetiaan 2,7× lebih tinggi drpd Stabil | **belum ada artifact** |

**Temuan ini — konvergensi 4-5 metode independen — adalah hasil terkuat seluruh sesi, tapi sekarang
tersebar di 3 URL berbeda tanpa benang merah, dan Model 6 belum kelihatan sama sekali.**

**KOREKSI 2026-08-01**: baris #2 (Hawkes) tidak lagi "eksklusif Siklus" setelah direproduksi ulang
thd data saat ini -- lihat baris tabel & `project_markov_hawkes_models` (memory). Klaim "Siklus =
rezim kausal berbeda" masih berdiri dari 4 baris lain (#1/3/4/5), tapi kekuatan bukti Hawkes-nya
lebih lemah dari yg dikutip di sini -- "SATU-SATUNYA" perlu direvisi jadi "TERKUAT, tapi tak eksklusif"
di narasi thesis manapun yg mengutip tabel ini.

## 2. Rekomendasi Desain (Frontend Design)

Bukan gabung semua jadi 1 halaman raksasa (kontras dgn craft masing-masing artifact yg sudah baik).
Sebaliknya: **1 halaman indeks/ringkasan baru** yang:
1. Membuka dengan tabel konvergensi di atas sebagai hero — ini punchline-nya, bukan pengantar
2. Tiap model jadi 1 kartu ringkas (takeaway 1-kalimat + angka kunci + tombol "lihat detail" ke artifact aslinya)
3. Model 6 butuh artifact sendiri dulu (lihat backlog #3) sebelum bisa masuk susunan ini
4. Palet & token desain SAMA dgn 3 artifact yg sudah ada (OKLCH-validated, `--st-aceh` dst) — konsistensi brand, bukan desain baru dari nol

## 3. Status Keamanan (DevSecOps)

Tidak ada temuan baru. Checklist cepat:
- [x] `WESTKUST_API_KEY` sudah dihapus dari `generale_missiven_extraction.ipynb` (diganti simpan-ke-Drive)
- [x] `HF_TOKEN` pakai Colab Secret, bukan hardcode
- [x] `docs/thesis/` tetap gitignored (skrip Model 5/6 + data GM tak ke-commit)
- [x] Tak ada endpoint/permukaan input baru dibuka sesi ini (analisis data lokal murni)
- [x] **Terverifikasi 2026-07-21**: `data/export/` tercakup `.gitignore` baris 87 (`data/export/`), `git status` bersih — `game_theory_payoff_matrix.csv`/`system_dynamics_output.json` baru otomatis aman, tak perlu aksi tambahan

## 4. Breakdown Backlog (Scrum Master)

| # | Task | Peran | Estimasi | Blocker |
|---|---|---|---|---|
| 1 | ~~Verifikasi `.gitignore` mencakup `data/export/*` baru~~ **SELESAI** (sudah tercakup, no-op) | DBA | kecil | — |
| 2 | ~~Bangun artifact visualisasi Model 6~~ **SELESAI** — https://claude.ai/code/artifact/02d80f8e-fb99-4c1b-b034-34c217123f15 | MLOps + Frontend Design | sedang | — |
| 3 | ~~Bangun halaman indeks konsolidasi~~ **SELESAI** — https://claude.ai/code/artifact/8c9db240-cb6c-46d2-ad00-f76238fdb1b1 | Frontend Design | sedang | — |
| 4 | Eksekusi PRD Fase 2 roster (Nias/Natal/Singkil/Paoeh/Sorkam) — prasyarat uji ulang H1 bandwagon yg adil | DBA + MLOps | besar | data primer sudah ada (CD1-CD6), tinggal backfill dominion_status |
| 5 | Rerun Google (Gemma) classification leg Generale Missiven di Colab (parser sudah diperbaiki+diuji) | MLOps (di luar sesi ini, butuh GPU T4) | sedang | akses Colab GPU pengguna |
| 6 | Setelah #5 selesai: spot-check 15-20 baris GM thd XML asli sebelum dipromosikan formal | MLOps | kecil | task #5 |
| 7 | Setelah #4: integrasikan GM (Loop 3/4 Model 5 yg belum diimplementasi) | MLOps | besar | task #4 + #6 |

**Urutan prioritas disarankan**: #1 (murah, cegah kebocoran) → #2 → #3 (menyatukan cerita yg sudah ada,
nilai tinggi/biaya rendah) → #4 (buka kunci uji H1 yg valid) → #5/#6/#7 (rantai GM, sebagian besar di
luar kendali sesi chat ini, butuh Colab GPU pengguna).

## 5. Pertanyaan Terbuka

1. Task #3 (halaman indeks) — taruh di `salido.my.id/atlas/riset/...` (live, publik) atau tetap artifact
   scratchpad (privat, thesis-only) seperti 4 artifact sebelumnya? Beda skop besar (deploy vs sekali-buat).
2. Task #4 (Fase 2 roster) besar — apakah dipecah per-negeri (Nias dulu, karena itu yg langsung
   dibutuhkan uji H1) atau sekaligus 5 lokasi?
