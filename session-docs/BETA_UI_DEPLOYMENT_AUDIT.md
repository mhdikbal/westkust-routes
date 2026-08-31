# Beta UI Deployment Audit

> **READ-ONLY UI DEPLOYMENT AUDIT**
> **NO CODE CHANGED**
> **NO MODEL REFIT**
> **NO DEPLOYMENT EXECUTED**
> **RESEARCHER DECISION REQUIRED**

---

## 1. Executive Summary

Aplikasi memiliki **SATU** permukaan publik yang menampilkan Model 3 secara
langsung: rute `/riset/pemodelan` (Django SSR → FastAPI `/api/research/pemodelan-dashboard`
→ `backend/build_bokeh_dashboard.py`). Audit ini menemukan **pelanggaran
label yang MASIH AKTIF dan tampil ke pengguna**: frasa **"Kaskade Defeksi"**
(padanan langsung "Defection Cascade") muncul di **DUA lokasi berbeda** —
heading `<h2>` di template DAN judul chart Bokeh itu sendiri (embed
script/div yang dikirim ke browser). **Ini mengoreksi laporan checkpoint
deployment sebelumnya** (`Deployment Readiness Checkpoint` turn sebelumnya)
yang menyatakan status `not_found_in_local_searchable_sources` — pencarian
sebelumnya hanya menyisir string Inggris "Defection Cascade" secara
case-insensitive dan TIDAK menyisir padanan Indonesia "Kaskade Defeksi"/
"defeksi". **Koreksi eksplisit dicatat di §9.**

Tidak ditemukan satu pun rute/API publik yang membaca `graphify-out/graph.json`
atau dokumen `docs/thesis/pilot_annotation/*.md` (dossier mekanisme, audit
Westenenk, legal-institutional layer) — seluruh pekerjaan graph/dossier sesi
ini **belum terhubung ke UI apa pun**. Akibatnya, sebagian besar item
checklist "Audit graph-facing UI" (§7) berstatus **`not_applicable — belum
dibangun`**, bukan lulus/gagal.

Tidak ditemukan klaim historis terlarang (regent=adat/VOC, Pagaruyung
memerintah langsung, Priaman sbg aktor homogen, dst.) di template publik
manapun yang dapat digrep — status `not_found_in_local_searchable_or_generated_sources`
untuk seluruh item §"Audit kasus historis", BUKAN "terverifikasi tak akan
pernah muncul".

---

## 2. Public Routes and Components

| Rute | Komponen | File | noindex? |
|---|---|---|---|
| `/riset/pemodelan/` | Dashboard Bokeh Model 2/3/5/6 (SSR) | `frontend/map_app/views.py:150` (`riset_pemodelan`), `frontend/map_app/templates/map_app/riset_pemodelan.html`, `backend/build_bokeh_dashboard.py`, `backend/routers/research.py:591` (`/api/research/pemodelan-dashboard`) | Ya (`<meta name="robots" content="noindex, nofollow">`) |
| `/riset/jaringan/` | Graf co-occurrence pelabuhan (client-side fetch) | `frontend/map_app/templates/map_app/riset_jaringan.html` | Ya (thesis-only, tak di navbar) |
| `/riset/atjeh-dagang/` | Tabel dagang Atjeh 1643-1644 | `frontend/map_app/templates/map_app/riset_atjeh.html` | Ya |
| `/riset/tema/` | Klaster tema korpus, toggle low-confidence | `frontend/map_app/templates/map_app/riset_tema.html` | Ya |
| `/riset/petunjuk-arsip/` | Indeks katalog GLOBALISE | `frontend/map_app/templates/map_app/riset_petunjuk_arsip.html` | Ya |
| `/riset/enclave-1682/` | Explorer topologi lokasi (fitur berbeda, sesi sebelumnya) | `frontend/map_app/templates/map_app/riset_enclave_1682.html` | Ya |
| `/linimasa/` | Linimasa suksesi Atjeh (SSR) | `frontend/map_app/templates/map_app/linimasa.html` | Tidak diperiksa detail (di luar cakupan Model 3) |
| `/atlas` (peta utama, index) | Popup fort — chip klaster Model 2/5/6, sparkline Model 5 | `frontend/map_app/templates/map_app/index.html`, `frontend/map_app/static/map_app/js/atlas.js` | Publik, DI navbar |

**Catatan penting**: popup `/atlas` (peta utama, publik & DI navbar — BUKAN
thesis-only) menampilkan sinyal Model 2/5/6 (cincin kestabilan Markov,
sparkline System Dynamics, chip klaster) TAPI **TIDAK menampilkan Model 3
(Hawkes) sama sekali** — index.html:965 eksplisit berjudul "Dashboard
interaktif Model 2/5/6" (Model 3 tidak disebut dalam link title, meski
halaman tujuannya `/riset/pemodelan` sebenarnya juga menampilkan Model 3).
Ini berarti **Model 3 HANYA terekspos di `/riset/pemodelan` yang noindex &
tak di navbar publik** — permukaan-blast-radius pelanggaran label lebih
kecil dari halaman utama, tapi tetap publicly reachable (URL langsung,
tidak diautentikasi).

---

## 3. Model 3 Labels

| Lokasi | Teks persis ditemukan | Tampil ke pengguna? |
|---|---|---|
| `frontend/map_app/templates/map_app/riset_pemodelan.html:112` | `<h2>Model 3 — Proses Hawkes: Kaskade Defeksi</h2>` | **Ya — heading section langsung** |
| `frontend/map_app/templates/map_app/riset_pemodelan.html:114` | `menguji apakah "kaskade" defeksi berantai nyata secara statistik, bukan cuma kesan dari cara linimasa ditulis` | **Ya — caption paragraf** |
| `backend/build_bokeh_dashboard.py:170` | `f"Model 3 — Proses Hawkes: kaskade defeksi "` (bagian dari `figure(title=...)`) | **Ya — judul chart Bokeh itu sendiri, di-render ke SVG/canvas yg dikirim browser via `components()`** |

**Label wajib `Pooled Exploratory Hawkes Baseline` — status: `not_found_in_local_searchable_or_generated_sources`.**
Tidak ada satu pun lokasi (template, backend script, API response) yang
memakai frasa ini. **Tidak boleh diklaim sudah diterapkan.**

**Kesimpulan §3**: Label terlarang **AKTIF dan tampil ke pengguna di 3
lokasi**, dua di antaranya (`h2` + judul chart Bokeh) adalah elemen paling
menonjol di section tsb. Label wajib pengganti **belum diterapkan sama
sekali**. Ini adalah **temuan blocking** (lihat §11, §13).

---

## 4. Model 3 Numerical Claims

Sumber angka: `data/export/hawkes_model_output.json`:
```
mu=0.2573, alpha=0.4207, beta=0.6215, LR=75.668, p_value=0.0 (dibulatkan), n=141, T0=1600, T1=1784
```
Branching ratio (dihitung manual, TIDAK disimpan sbg field terpisah di
JSON) = alpha/beta = 0.4207/0.6215 ≈ **0.677** — cocok dgn nilai yg dirujuk
user (`0.677`).

| Field | File:baris | Teks | Tampil ke pengguna? | Status |
|---|---|---|---|---|
| `mu` | `data/export/hawkes_model_output.json` (params.mu) | `0.2573` | **Tidak** — dipakai internal saat load JSON (`build_bokeh_dashboard.py:158 params = hk["params"]`), TIDAK dimasukkan ke judul chart maupun caption | `internal_only` |
| `alpha` | `backend/build_bokeh_dashboard.py:171` | `α={params['alpha']:.3f}` di judul chart | Ya | `valid` (angka benar, tapi tanpa penjelasan makna — lihat §5) |
| `beta` | `backend/build_bokeh_dashboard.py:171` | `β={params['beta']:.3f}/thn` | Ya | `valid` |
| `branching_ratio` (0.677) | **Tidak ditemukan di manapun** | — | Tidak ditampilkan sama sekali | `missing_limitation` — narasi wajib poin 4 ("branching ratio bukan persentase defeksi") tak bisa ditampilkan krn angkanya sendiri tak pernah dihitung/ditampilkan publik |
| `p-value` | `backend/build_bokeh_dashboard.py:167,172` | `p<0.0001` (dibulatkan dari `p_value=0.0`) | Ya | `valid` — sudah ditangani benar (tidak menampilkan literal "p=0.0", ada komentar eksplisit di kode soal ini) |
| `exponential kernel` | `riset_pemodelan.html:113` | "kernel eksponensial" | Ya | `valid` — istilah tekniks disebut benar di caption |
| `Gamma kernel` | **Tidak ditemukan** | — | — | `not_found_in_local_searchable_or_generated_sources` — model saat ini memang tidak pakai Gamma kernel, bukan pelanggaran |
| `141 events` (n) | `backend/build_bokeh_dashboard.py:146,172` (docstring + judul via `n={params['n']}`) | "141 event linimasa" (docstring); `n=141` (judul chart, via variabel bukan literal) | **Ya, TAPI hanya sbg `n=141` singkat di ujung judul chart** — TIDAK ada penjelasan "141 event CAMPURAN [multi-lokasi/multi-mekanisme]" di caption manapun | `missing_limitation` — angka tampil tapi narasi wajib poin 1 (event CAMPURAN, bukan satu mekanisme) tidak dijelaskan |
| `self-excitation` | **Tidak ditemukan** di teks publik manapun | — | Tidak | `missing_limitation` — narasi wajib poin 3 tak dijelaskan dlm bahasa awam; caption hanya bilang "intensitas kondisional λ(t)" (istilah teknis, tak dijelaskan) |
| `temporal clustering` | **Tidak ditemukan** secara eksplisit | — | Tidak (kata "kaskade" dipakai sbg gantinya, TAPI itu justru istilah yg dilarang) | `too_strong` — istilah netral "temporal clustering" digantikan istilah bermuatan interpretif "kaskade defeksi" |
| `causal`/`kausal` | **Tidak ditemukan** secara literal di teks publik | — | Tidak literal, TAPI tersirat kuat via framing "kaskade defeksi berantai" | `too_strong` (implisit) |
| `trigger` | **Tidak ditemukan** | — | — | `not_found_in_local_searchable_or_generated_sources` |
| `cascade`/`kaskade` | `riset_pemodelan.html:112,114`; `build_bokeh_dashboard.py:170` | Lihat §3 | Ya | `too_strong` |
| `defection`/`defeksi` | Sama 3 lokasi dgn "kaskade" | Lihat §3 | Ya | `too_strong` |
| `resistance`/`resistensi` | **Tidak ditemukan** di permukaan Model 3 manapun | — | Tidak | `not_found_in_local_searchable_or_generated_sources` — TAPI juga berarti disclaimer wajib poin 7 ("model tidak membuktikan resistensi") tak pernah dinyatakan krn topiknya tak disinggung sama sekali |

---

## 5. Statistical Limitations

Kesepuluh narasi wajib dicek terhadap teks publik `/riset/pemodelan` (footer
"Metode & batas" + caption Model 3 + judul chart):

| # | Narasi wajib | Status di permukaan publik |
|---|---|---|
| 1 | Model menggunakan 141 event campuran | **Sebagian** — angka `n=141` tampil di judul chart, tapi kata "campuran" (lintas-lokasi/lintas-mekanisme) tak pernah dijelaskan |
| 2 | Model = Hawkes univariat pooled | **Tidak ada** — tak ada teks yg menyatakan "univariat" atau "pooled" secara eksplisit |
| 3 | Model mendeteksi temporal clustering/self-excitation | **Tidak ada** — istilah ini diganti "kaskade defeksi" (§4) |
| 4 | Branching ratio 0.677 ≠ persentase defeksi | **Tidak ada** — branching ratio bahkan tak ditampilkan (§4) |
| 5 | Model tidak identifikasi mekanisme historis tunggal | **Tidak ada** |
| 6 | Model tidak membuktikan kausalitas | **Tidak ada** |
| 7 | Model tidak membuktikan resistensi | **Tidak ada** |
| 8 | Process tracing menemukan mekanisme heterogen | **Tidak ada** — temuan process-tracing sesi ini (Barus/Indrapura/Priaman/Sillida, heterogen per dossier) sama sekali tak dirujuk di UI publik |
| 9 | Marked Hawkes belum siap | **Tidak ada** |
| 10 | Multivariate Hawkes belum siap | **Tidak ada** |

**Kesimpulan §5**: **0 dari 10** narasi wajib hadir secara eksplisit dan
lengkap di permukaan publik saat ini. Footer "Metode & batas" HANYA
membahas keterbatasan `dominion_status` backfill (fort <2 event) — sama
sekali tidak membahas keterbatasan statistik Model 3 itu sendiri.

---

## 6. Historical Claims

| Klaim terlarang | Ditemukan di UI publik? |
|---|---|
| Priaman sbg satu aktor homogen | `not_found_in_local_searchable_or_generated_sources` |
| Tiku sama dengan Priaman | `not_found...` |
| Maharadja Indra sama dengan Mara Laout | `not_found...` |
| Indrapura ditumpas langsung oleh VOC | `not_found...` |
| Sillida = episode defeksi | `not_found...` |
| Barus kolektif melawan VOC | `not_found...` |
| Regent = representasi adat Minangkabau | `not_found...` |
| Regent = representasi VOC atas Minangkabau | `not_found...` |
| Pagaruyung memerintah langsung seluruh nagari | `not_found...` |
| Rantau Basa Ampek Balai = wilayah pemerintahan langsung | `not_found...` |

**Konteks penting**: `riset_atjeh.html` (§2) memuat narasi historis rinci
ttg Tiku/Priaman/Indrapura/Barus/Sillida (periode 1625-1668, di luar
cakupan dossier 1705-1713 sesi ini) — dibaca penuh, **tidak ditemukan** satu
pun klaim di atas. Halaman ini secara eksplisit menandai seluruh baris
`confidence_flag=unverified` (§2, riset_atjeh.html:153) dan mencantumkan
**koreksi historiografis yg sudah dilakukan sebelumnya** (baris 226-228:
klaim "bukti Atjeh-Barus pertama" dikoreksi setelah temuan baru) — pola
kehati-hatian yg KONSISTEN dgn temuan dossier sesi ini, meski dibuat
terpisah/lebih awal.

---

## 7. Graph Presentation

**Prasyarat**: TIDAK ada rute/API publik yang membaca `graphify-out/graph.json`
atau `docs/thesis/pilot_annotation/*.md` (dikonfirmasi §"Executive Summary" —
grep `graphify-out|graph.json|pilot_annotation|mechanism_status` di seluruh
`backend/routers/`, `views.py`, template = 0 hasil).

| Item checklist | Status |
|---|---|
| Membedakan documentary report dari historical event | `not_applicable — belum dibangun` |
| Membedakan parent episode dari child event | `not_applicable — belum dibangun` |
| Membedakan supported dari interpretive_only | `not_applicable — belum dibangun` |
| Menampilkan confidence | `partially_applicable` — `riset_atjeh.html`/`riset_tema.html` PUNYA sistem confidence_flag/low-confidence UNTUK KORPUS LAIN (Atjeh trade, tema umum), TAPI bukan utk data dossier mekanisme sesi ini |
| Tidak menyamakan graph relation dgn kausalitas | `not_applicable — belum dibangun` |
| Tidak menyamakan lokasi dgn aktor | `not_applicable — belum dibangun` |
| Tidak menggabungkan Maharadja Indra & Mara Laout | `not_applicable — belum dibangun` (dan sesuai §6, tak ditemukan penggabungan krn topik ini tak muncul di UI sama sekali) |
| Tidak menggabungkan kelompok aktor Sillida | `not_applicable — belum dibangun` |
| Tidak menampilkan strategic_resistance sbg supported | `not_applicable — belum dibangun` |
| Tidak menampilkan defection sbg supported | `partially_applicable` — istilah "defeksi" MUNCUL (§3/§4) TAPI sbg NAMA LABEL model, bukan sbg klaim `mechanism_status: supported` yg eksplisit dari dossier; tetap **`too_strong`** krn penamaan itu sendiri menyiratkan status terverifikasi |

---

## 8. Tooltip and Legend Audit

Bokeh HoverTool tooltips diperiksa langsung dari `build_bokeh_dashboard.py`:

| Chart | Tooltip | Status |
|---|---|---|
| Model 2 Markov heatmap | `("Dari","@y"),("Ke","@x"),("P(transisi)","@prob"),("Observasi","@n")` | `valid` — netral, tak overclaim |
| Model 3 Hawkes — kurva | `("Tahun","@year{0.0}"),("λ(t)","@lam{0.000}")` | `valid` — netral secara numerik, TAPI tidak menjelaskan λ(t) itu apa (tak ada disclaimer inline) |
| Model 3 Hawkes — event | `("Tahun event","@year{0.0}")` | `valid` |
| Model 5 dynamics | `("Tahun","@year"),("I aktual","@actual{0.00}")` | `valid` |
| Model 6 reafirmasi | `("Klaster","@cluster"),("Rate rata2","@rate{0.000}/thn"),("Per fort","@breakdown")` | `valid` |

**Legend Model 3**: `"λ(t) tercocokkan"` dan `"Event nyata (linimasa)"` — netral,
`valid`. **Tidak ada legend/tooltip yang secara individual overclaim** — seluruh
masalah label ada di **judul chart & heading section**, bukan di
tooltip/legend granular.

---

## 9. Stale or Overstated Claims

1. **`[BLOCKING]`** "Kaskade Defeksi"/"kaskade defeksi" — 3 lokasi (§3).
   Status `too_strong`: nama ini menyiratkan (a) fenomena "kaskade" sudah
   terverifikasi sbg pola nyata (bukan sekadar diuji), dan (b) "defeksi"
   sbg interpretasi historis tunggal — bertentangan langsung dgn narasi
   wajib poin 3, 5, 6, 7 (§5) dan dgn seluruh temuan process-tracing sesi
   ini (mekanisme heterogen per lokasi, `strategic_resistance: not_supported`
   di semua dossier yg diaudit).
2. **`[KOREKSI TERHADAP LAPORAN SEBELUMNYA]`** Turn "Deployment Readiness
   Checkpoint" sebelumnya melaporkan `Defection Cascade:
   not_found_in_local_searchable_sources` — **ini keliru**, krn pencarian
   sebelumnya tidak menyisir padanan Bahasa Indonesia. Dicatat di sini
   sbg koreksi eksplisit, bukan dihapus dari riwayat.
3. Caption "menguji apakah 'kaskade' defeksi berantai nyata secara
   statistik" — tanda kutip di sekitar "kaskade" menunjukkan KESADARAN
   penulis sebelumnya bahwa istilah ini perlu dipagari, TAPI pagar itu tak
   cukup: kalimat tetap memakai "defeksi berantai" tanpa tanda kutip, dan
   heading section (§3, baris 112) memakai istilah itu TANPA tanda kutip
   sama sekali.

---

## 10. Missing Disclaimers

Seluruh 10 narasi wajib §5 **absen** dari permukaan publik. Prioritas
tertinggi untuk ditambahkan sebelum beta (urutan dampak):
1. Disclaimer "tidak membuktikan kausalitas/resistensi" (poin 6, 7) — paling
   kritis krn nama chart saat ini justru menyiratkan sebaliknya.
2. Definisi branching ratio bukan persentase defeksi (poin 4) — TAPI angka
   itu sendiri harus dihitung & ditampilkan dulu sebelum disclaimernya
   bermakna.
3. Status kesiapan marked/multivariate Hawkes (poin 9, 10) — mencegah
   pembaca berasumsi model saat ini sudah per-mekanisme/per-lokasi.

---

## 11. Required Changes Before Beta

1. **Ganti heading** `riset_pemodelan.html:112` dari `Model 3 — Proses
   Hawkes: Kaskade Defeksi` → `Model 3 — Pooled Exploratory Hawkes Baseline`.
2. **Ganti caption** `riset_pemodelan.html:113-116` — hapus "kaskade
   defeksi berantai", ganti dgn deskripsi netral (temporal
   clustering/self-excitation) + tambahkan narasi wajib poin 1,2,5,6,7,8,9,10.
3. **Ganti judul chart Bokeh** `backend/build_bokeh_dashboard.py:170`
   (`f"Model 3 — Proses Hawkes: kaskade defeksi "`) → gunakan label wajib.
   **CATATAN: ini adalah perubahan KODE, bukan hanya teks statis** — di
   luar cakupan "read-only" audit ini, harus dieksekusi di turn terpisah.
4. **Tambahkan branching ratio** (alpha/beta) sbg field yg dihitung &
   ditampilkan, disertai disclaimer poin 4.
5. **Tambahkan blok disclaimer statistik** ke footer "Metode & batas" —
   mencakup narasi wajib poin 2,3,5,6,7,9,10 scr eksplisit dan ringkas.

---

## 12. Optional Improvements

- Tambahkan `n=141` + kata "campuran" scr eksplisit di caption (bukan hanya
  di ujung judul chart).
- Pertimbangkan menampilkan `mu` (intensitas dasar) di caption/tooltip,
  saat ini hanya internal.
- Selaraskan `index.html:965` (`title="Dashboard interaktif Model 2/5/6"`)
  agar menyebut juga Model 3, konsisten dgn isi halaman tujuan.
- Pertimbangkan menautkan singkat ke ringkasan temuan process-tracing
  (heterogenitas mekanisme per lokasi) sbg konteks tambahan — opsional,
  di luar cakupan blocking.

---

## 13. Deployment Decision

```
APPLICATION_BETA_BLOCKED
```

**Alasan**: Label terlarang "Kaskade Defeksi"/"kaskade defeksi" AKTIF dan
tampil ke pengguna di section paling menonjol dari satu-satunya permukaan
publik Model 3 (`/riset/pemodelan`), termasuk di JUDUL CHART Bokeh itu
sendiri (bukan sekadar teks template yg mudah diedit terpisah — perubahan
di `build_bokeh_dashboard.py` memerlukan sentuhan kode, di luar cakupan
read-only audit ini). Kombinasi label bermuatan + KETIADAAN TOTAL (0/10)
narasi limitasi wajib membuat halaman ini, dalam bentuknya SAAT INI,
membawa klaim historis-interpretif ("defeksi berantai" sbg fenomena nyata)
tanpa pagar epistemik apa pun — bertentangan langsung dgn seluruh temuan
process-tracing sesi ini (`strategic_resistance: not_supported`,
mekanisme heterogen per lokasi).

## Keputusan Terpisah

```
GRAPH_CONTEXT_READY: TIDAK BERLAKU (not_applicable)
  - Tidak ada UI publik yg membaca graph/dossier sesi ini sama sekali.
  - Pekerjaan graph/dossier itu sendiri (per checkpoint sebelumnya) SIAP
    sbg dokumen riset internal — TAPI belum ada permukaan UI utk dinilai.

POOLED_HAWKES_BASELINE_READY: TIDAK — diblokir oleh temuan §3/§4/§5/§9
  (label salah + 0/10 disclaimer wajib). Data statistik itu sendiri (mu,
  alpha, beta, LR, p-value, n) VALID dan tak perlu fitting ulang — murni
  masalah presentasi/label, yg berarti BISA diperbaiki cepat begitu izin
  edit kode diberikan (di luar cakupan audit read-only ini).

ADVANCED_MODEL_READY: TIDAK — marked Hawkes & multivariate Hawkes belum
  dibangun sama sekali (dikonfirmasi tak ada di build_bokeh_dashboard.py
  maupun data/export/), konsisten dgn keputusan checkpoint sebelumnya.
```

---

## 14. Files Requiring Modification

| File | Baris | Perubahan diperlukan |
|---|---|---|
| `frontend/map_app/templates/map_app/riset_pemodelan.html` | 112, 113-116 | Ganti heading + caption Model 3, hapus "kaskade"/"defeksi", tambahkan narasi limitasi wajib |
| `backend/build_bokeh_dashboard.py` | 170-173 | Ganti judul chart Bokeh; **ini kode Python, bukan teks statis** — bukan perubahan "hanya label" sederhana, perlu tinjauan sblm dieksekusi |
| `frontend/map_app/templates/map_app/riset_pemodelan.html` | 149-153 (footer) | Tambahkan blok disclaimer statistik lengkap |
| `frontend/map_app/templates/map_app/index.html` | 965 | (opsional) selaraskan judul link Model 2/5/6 → sebut Model 3 juga |

**Tidak ada file di atas yang diubah dalam audit ini** — seluruh temuan
bersifat identifikasi lokasi, bukan eksekusi perbaikan.

---

Tidak ada kode, model, graph, dataset, atau dashboard yang diubah dalam
penyusunan audit ini. Tidak ada fitting, migrasi, deployment, atau operasi
Git yang dijalankan.
